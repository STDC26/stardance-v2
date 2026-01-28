"""Pydantic models for video generation API contracts."""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class Platform(str, Enum):
    """Supported video platforms."""
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    REELS = "reels"


class ContentType(str, Enum):
    """Content classification."""
    UGC = "ugc"
    BRAND = "brand"
    PRODUCT = "product"
    TESTIMONIAL = "testimonial"


class VideoGenerationRequestInput(BaseModel):
    """Input: SBOX translation → Video Generation Agent."""
    
    translation_id: str = Field(
        ..., 
        description="SBOX translation ID (from Phase 1)"
    )
    allocation_id: str = Field(
        ..., 
        description="CIM allocation ID (from Phase 1)"
    )
    sbox_parameters: Dict[str, Any] = Field(
        ..., 
        description="16 SBOX parameters (cuts_per_30s, tempo_curve, etc)"
    )
    platform: Platform = Field(
        default=Platform.TIKTOK,
        description="Target platform"
    )
    duration: int = Field(
        default=30,
        ge=15,
        le=180,
        description="Video duration in seconds"
    )
    content_type: Optional[ContentType] = Field(
        default=None,
        description="Content classification"
    )
    
    @validator('sbox_parameters')
    def validate_sbox_params(cls, v):
        """Ensure 16 SBOX parameters present."""
        required = {
            'cuts_per_30s', 'bpm_equivalent', 'tempo_curve',
            'saturation', 'contrast', 'palette',
            'framing', 'motion_style', 'focal_point',
            'voiceover_style', 'music_energy', 'voice_tone',
            'structure', 'cta_strength', 'proof_elements', 'hook_placement'
        }
        provided = set(v.keys())
        if not required.issubset(provided):
            missing = required - provided
            raise ValueError(f"Missing SBOX parameters: {missing}")
        return v


class VideoGenerationInstructionOutput(BaseModel):
    """Output: Video Generation Agent → Ready for Runway."""
    
    instruction_id: str = Field(
        ...,
        description="Unique instruction ID"
    )
    request_id: str = Field(
        ...,
        description="Links back to request"
    )
    status: str = Field(
        default="ready",
        description="Instruction status"
    )
    
    # Prompts (deterministic output)
    main_prompt: str = Field(
        ...,
        description="Main prompt for Runway (100-300 words)"
    )
    negative_prompt: str = Field(
        ...,
        description="What to avoid in video"
    )
    style_guidance: str = Field(
        ...,
        description="Style and format guidance"
    )
    
    # Technical specs
    resolution: str = Field(
        default="1080x1920",
        description="Video resolution"
    )
    frame_rate: int = Field(
        default=30,
        description="Frames per second"
    )
    codec: str = Field(
        default="h264",
        description="Video codec"
    )
    
    # Runway parameters
    runway_mode: str = Field(
        default="gen3",
        description="Runway generation mode"
    )
    runway_motion_bucket_id: int = Field(
        default=127,
        description="Motion bucket ID for Runway"
    )
    runway_conditioning_scale: float = Field(
        default=1.0,
        description="Conditioning scale"
    )
    runway_steps: int = Field(
        default=30,
        description="Generation steps"
    )
    
    # Estimates
    estimated_generation_time: int = Field(
        ...,
        description="Estimated time in seconds (typically 45)"
    )
    estimated_cost: float = Field(
        ...,
        description="Estimated cost in USD"
    )
    
    # Metadata for learning
    dimension_mapping: Dict[str, Any] = Field(
        default_factory=dict,
        description="How each SBOX dimension influenced prompt"
    )
    sbox_parameters_snapshot: Dict[str, Any] = Field(
        default_factory=dict,
        description="Original SBOX parameters stored for learning"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When was this instruction created?"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "instruction_id": "vgen_instr_abc123xyz",
                "request_id": "vgen_req_abc123xyz",
                "status": "ready",
                "main_prompt": "Fast-paced TikTok video (8 cuts per 30 seconds)...",
                "negative_prompt": "No watermarks, no blurry footage...",
                "style_guidance": "TikTok native format, 9:16...",
                "estimated_generation_time": 45,
                "estimated_cost": 0.10,
                "created_at": "2025-01-27T23:57:00Z"
            }
        }


class VideoGenerationOutputResult(BaseModel):
    """Output: Video after Runway generation (Phase 2.2 n8n calls this)."""
    
    output_id: str = Field(
        ...,
        description="Unique output ID"
    )
    instruction_id: str = Field(
        ...,
        description="Links to instruction"
    )
    request_id: str = Field(
        ...,
        description="Links to request"
    )
    status: str = Field(
        default="completed",
        description="completed | failed"
    )
    
    # Video result
    video_url: str = Field(
        ...,
        description="URL to generated video (S3 or Runway hosted)"
    )
    video_duration: int = Field(
        ...,
        description="Actual video duration in seconds"
    )
    video_resolution: str = Field(
        ...,
        description="Actual video resolution"
    )
    video_size_bytes: Optional[int] = Field(
        None,
        description="File size in bytes"
    )
    
    # Runway metadata
    runway_generation_id: str = Field(
        ...,
        description="Runway generation ID (for tracking)"
    )
    runway_processing_time: int = Field(
        ...,
        description="Actual processing time in milliseconds"
    )
    runway_cost: float = Field(
        ...,
        description="Actual cost incurred (USD)"
    )
    
    # Error info (if failed)
    error_code: Optional[str] = Field(
        None,
        description="Error code if generation failed"
    )
    error_message: Optional[str] = Field(
        None,
        description="Error message if generation failed"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )
    
    class Config:
        schema_extra = {
            "example": {
                "output_id": "vgen_output_xyz789",
                "instruction_id": "vgen_instr_abc123xyz",
                "request_id": "vgen_req_abc123xyz",
                "status": "completed",
                "video_url": "s3://bucket/runway_xyz.mp4",
                "video_duration": 30,
                "video_resolution": "1080x1920",
                "video_size_bytes": 5242880,
                "runway_generation_id": "gen_xyz789",
                "runway_processing_time": 42000,
                "runway_cost": 0.09,
                "created_at": "2025-01-27T23:58:00Z"
            }
        }


class VideoAgentStatus(BaseModel):
    """Agent status and metrics."""
    
    agent_name: str = Field(
        default="video_generation",
        description="Agent name"
    )
    status: str = Field(
        default="operational",
        description="operational | degraded | down"
    )
    version: str = Field(
        ...,
        description="Agent version"
    )
    completed_instructions: int = Field(
        default=0,
        description="Total instructions processed"
    )
    pending_instructions: int = Field(
        default=0,
        description="Currently pending"
    )
    failed_instructions: int = Field(
        default=0,
        description="Failed instructions"
    )
    avg_execution_time_ms: float = Field(
        default=0.0,
        description="Average execution time"
    )
    success_rate: float = Field(
        default=100.0,
        ge=0.0,
        le=100.0,
        description="Success rate percentage"
    )
    last_health_check: datetime = Field(
        default_factory=datetime.utcnow,
        description="When was last health check?"
    )
    uptime_percentage: float = Field(
        default=100.0,
        ge=0.0,
        le=100.0,
        description="Uptime percentage"
    )
