"""
FastAPI routes for Video Generation Agent.

Endpoints:
- POST /agents/video/translate - Main: SBOX params → instructions
- GET /agents/video/instruction/{id} - Retrieve instruction
- POST /agents/video/result - Store Runway result (Phase 2.2)
- GET /agents/status - Agent status
"""

from fastapi import APIRouter, HTTPException, status
from typing import Optional
import uuid

from app.agents.video_generation.agent import VideoGenerationAgent
from app.agents.video_generation.models import (
    VideoGenerationRequestInput,
    VideoGenerationInstructionOutput,
    VideoGenerationOutputResult,
    VideoAgentStatus
)

# Initialize router and agent
router = APIRouter(prefix="/agents/video", tags=["video_generation"])
agent = VideoGenerationAgent()

# In-memory storage (for Phase 2.1 - will migrate to database in production)
instructions_cache = {}
outputs_cache = {}


@router.post(
    "/translate",
    response_model=VideoGenerationInstructionOutput,
    status_code=status.HTTP_201_CREATED,
    summary="Translate SBOX parameters to video instruction",
    description="Convert SBOX translation (16 params) into Runway-ready prompt instruction"
)
async def translate_sbox_to_instruction(
    request: VideoGenerationRequestInput
) -> VideoGenerationInstructionOutput:
    """
    Main endpoint: Convert SBOX parameters to video generation instruction.
    
    **Input:**
    - translation_id: SBOX translation ID (from Phase 1)
    - allocation_id: CIM allocation ID (from Phase 1)
    - sbox_parameters: All 16 SBOX dimensions
    - platform: tiktok, youtube, instagram, reels
    - duration: Video length in seconds (15-180)
    - content_type: ugc, brand, product, testimonial (optional)
    
    **Output:**
    - instruction_id: Unique instruction ID
    - main_prompt: Ready for Runway API
    - negative_prompt: What to avoid
    - style_guidance: Format/style hints
    - estimated_generation_time: Seconds (typically 45)
    - estimated_cost: USD
    
    **Status:** 201 Created
    """
    try:
        # Validate SBOX parameters have all 16 dimensions
        required_params = {
            'cuts_per_30s', 'bpm_equivalent', 'tempo_curve',
            'saturation', 'contrast', 'palette',
            'framing', 'motion_style', 'focal_point',
            'voiceover_style', 'music_energy', 'voice_tone',
            'structure', 'cta_strength', 'proof_elements', 'hook_placement'
        }
        
        provided = set(request.sbox_parameters.keys())
        if not required_params.issubset(provided):
            missing = required_params - provided
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Missing SBOX parameters: {missing}"
            )
        
        # Generate instruction using agent
        instruction = agent.translate(request)
        
        # Cache instruction (Phase 2.1 - later: save to database)
        instructions_cache[instruction.instruction_id] = instruction
        
        return instruction
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Video generation failed: {str(e)}"
        )


@router.get(
    "/instruction/{instruction_id}",
    response_model=VideoGenerationInstructionOutput,
    summary="Retrieve generated instruction",
    description="Get a previously generated video instruction by ID"
)
async def get_instruction(
    instruction_id: str
) -> VideoGenerationInstructionOutput:
    """
    Retrieve a previously generated video instruction.
    
    **Path Parameters:**
    - instruction_id: The instruction ID (e.g., vgen_instr_abc123xyz)
    
    **Returns:**
    - VideoGenerationInstructionOutput
    
    **Status:**
    - 200 OK: Instruction found
    - 404 Not Found: Instruction not found
    """
    if instruction_id not in instructions_cache:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instruction {instruction_id} not found"
        )
    
    return instructions_cache[instruction_id]


@router.post(
    "/result",
    response_model=VideoGenerationOutputResult,
    status_code=status.HTTP_201_CREATED,
    summary="Store video generation result",
    description="Store result after Runway generates video (called by Phase 2.2 n8n)"
)
async def store_video_result(
    output: VideoGenerationOutputResult
) -> VideoGenerationOutputResult:
    """
    Store video generation result from Runway.
    
    This endpoint is called by n8n after Runway completes video generation.
    
    **Input:**
    - instruction_id: Links to generated instruction
    - request_id: Links to original request
    - video_url: S3 or Runway-hosted URL
    - video_duration: Actual duration in seconds
    - runway_generation_id: Runway's generation ID
    - runway_processing_time: Milliseconds
    - runway_cost: Actual USD cost
    - status: completed | failed
    
    **Output:**
    - VideoGenerationOutputResult (same as input, confirmed)
    
    **Status:** 201 Created
    """
    try:
        # Verify instruction exists
        if output.instruction_id not in instructions_cache:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Instruction {output.instruction_id} not found"
            )
        
        # Generate unique output ID if not provided
        if not output.output_id:
            output.output_id = f"vgen_output_{uuid.uuid4().hex[:12]}"
        
        # Cache output (Phase 2.1 - later: save to database)
        outputs_cache[output.output_id] = output
        
        return output
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store result: {str(e)}"
        )


@router.get(
    "/output/{output_id}",
    response_model=VideoGenerationOutputResult,
    summary="Retrieve video output result",
    description="Get a previously generated video output by ID"
)
async def get_output(
    output_id: str
) -> VideoGenerationOutputResult:
    """
    Retrieve a previously stored video output result.
    
    **Path Parameters:**
    - output_id: The output ID (e.g., vgen_output_xyz789)
    
    **Returns:**
    - VideoGenerationOutputResult
    
    **Status:**
    - 200 OK: Output found
    - 404 Not Found: Output not found
    """
    if output_id not in outputs_cache:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Output {output_id} not found"
        )
    
    return outputs_cache[output_id]


@router.get(
    "/status",
    response_model=VideoAgentStatus,
    summary="Get agent status",
    description="Get Video Generation Agent status and metrics"
)
async def get_agent_status() -> VideoAgentStatus:
    """
    Get Video Generation Agent status and performance metrics.
    
    **Returns:**
    - agent_name: video_generation
    - status: operational | degraded | down
    - version: Agent version
    - completed_instructions: Total processed
    - failed_instructions: Total failures
    - avg_execution_time_ms: Average response time
    - success_rate: Percentage (0-100)
    - uptime_percentage: Percentage (0-100)
    
    **Status:** 200 OK
    """
    return agent.get_status()


@router.get(
    "/health",
    summary="Health check",
    description="Quick health check endpoint"
)
async def health_check():
    """
    Quick health check.
    
    **Returns:**
    - status: healthy
    - agent: video_generation
    - version: Agent version
    - timestamp: Current time
    
    **Status:** 200 OK
    """
    return agent.health_check()
