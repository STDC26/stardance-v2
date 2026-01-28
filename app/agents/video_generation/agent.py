"""
Video Generation Agent: Core intelligence for video generation.

Accepts SBOX parameters, generates deterministic prompts, 
estimates costs, and stores instructions for Runway.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from app.agents.video_generation.prompt_engine import PromptEngine
from app.agents.video_generation.models import (
    VideoGenerationRequestInput,
    VideoGenerationInstructionOutput,
    VideoAgentStatus
)


class VideoGenerationAgent:
    """Agent that translates SBOX parameters into video generation instructions."""
    
    def __init__(self):
        """Initialize agent with prompt engine."""
        self.name = "video_generation"
        self.version = "2.0.0"
        self.prompt_engine = PromptEngine()
        self.completed_count = 0
        self.failed_count = 0
        self.total_execution_time_ms = 0
    
    def translate(
        self,
        request: VideoGenerationRequestInput
    ) -> VideoGenerationInstructionOutput:
        """
        Main entry point: Convert SBOX parameters to video instruction.
        
        Args:
            request: VideoGenerationRequestInput with SBOX params
        
        Returns:
            VideoGenerationInstructionOutput (ready for Runway)
        """
        start_time = datetime.utcnow()
        
        try:
            # Generate unique IDs
            instruction_id = f"vgen_instr_{uuid.uuid4().hex[:12]}"
            request_id = f"vgen_req_{uuid.uuid4().hex[:12]}"
            
            # Generate prompts using prompt engine
            main_prompt, negative_prompt, style_guidance = self.prompt_engine.convert(
                sbox_params=request.sbox_parameters,
                platform=request.platform.value,
                duration=request.duration
            )
            
            # Estimate generation time and cost
            estimated_time = self._estimate_generation_time(
                request.duration,
                request.sbox_parameters
            )
            estimated_cost = self._estimate_cost(
                request.duration,
                request.platform.value
            )
            
            # Create dimension mapping (for learning)
            dimension_mapping = self._create_dimension_mapping(
                request.sbox_parameters,
                main_prompt
            )
            
            # Build output
            instruction = VideoGenerationInstructionOutput(
                instruction_id=instruction_id,
                request_id=request_id,
                status="ready",
                main_prompt=main_prompt,
                negative_prompt=negative_prompt,
                style_guidance=style_guidance,
                resolution="1080x1920",
                frame_rate=30,
                codec="h264",
                runway_mode="gen3",
                runway_motion_bucket_id=127,
                runway_conditioning_scale=1.0,
                runway_steps=30,
                estimated_generation_time=estimated_time,
                estimated_cost=estimated_cost,
                dimension_mapping=dimension_mapping,
                sbox_parameters_snapshot=request.sbox_parameters,
                created_at=datetime.utcnow()
            )
            
            # Update metrics
            self.completed_count += 1
            end_time = datetime.utcnow()
            execution_ms = int((end_time - start_time).total_seconds() * 1000)
            self.total_execution_time_ms += execution_ms
            
            return instruction
        
        except Exception as e:
            self.failed_count += 1
            raise
    
    def _estimate_generation_time(self, duration: int, params: Dict) -> int:
        """
        Estimate Runway generation time in seconds.
        
        Typical: 45 seconds for 30-second video.
        Varies by complexity.
        """
        base_time = 45
        
        # Factor in complexity
        cuts = params.get('cuts_per_30s', 5)
        motion_complexity = 1.0 if params.get('motion_style') == 'dynamic' else 0.8
        
        # More cuts = slightly longer (more transitions to process)
        if cuts >= 8:
            complexity_factor = 1.1
        elif cuts >= 5:
            complexity_factor = 1.0
        else:
            complexity_factor = 0.9
        
        estimated = int(base_time * complexity_factor * motion_complexity)
        return estimated
    
    def _estimate_cost(self, duration: int, platform: str) -> float:
        """
        Estimate Runway generation cost in USD.
        
        Runway pricing: ~$0.003 per second of video
        30-second video ≈ $0.09
        """
        # Base cost: $0.003 per second
        base_cost_per_second = 0.003
        estimated = duration * base_cost_per_second
        
        # Round to nearest cent
        return round(estimated, 2)
    
    def _create_dimension_mapping(
        self,
        sbox_params: Dict[str, Any],
        main_prompt: str
    ) -> Dict[str, Any]:
        """
        Create mapping of how each SBOX dimension influenced the prompt.
        
        This is used for learning: which dimensions correlate to 
        successful videos.
        """
        mapping = {}
        
        # Map each parameter to how it influenced the prompt
        for param_name, param_value in sbox_params.items():
            if param_name in main_prompt.lower():
                mapping[param_name] = {
                    "value": param_value,
                    "influence": "high",  # Parameter explicitly mentioned
                    "examples": [
                        line.strip() 
                        for line in main_prompt.split('\n') 
                        if param_name.replace('_', ' ').lower() in line.lower()
                    ][:2]
                }
            else:
                mapping[param_name] = {
                    "value": param_value,
                    "influence": "medium",  # Parameter influenced structure
                }
        
        return mapping
    
    def get_status(self) -> VideoAgentStatus:
        """Get agent status and metrics."""
        total_processed = self.completed_count + self.failed_count
        success_rate = (
            (self.completed_count / total_processed * 100) 
            if total_processed > 0 else 100.0
        )
        
        avg_execution_time = (
            self.total_execution_time_ms / self.completed_count
            if self.completed_count > 0 else 0
        )
        
        return VideoAgentStatus(
            agent_name=self.name,
            status="operational",
            version=self.version,
            completed_instructions=self.completed_count,
            pending_instructions=0,
            failed_instructions=self.failed_count,
            avg_execution_time_ms=avg_execution_time,
            success_rate=success_rate,
            last_health_check=datetime.utcnow(),
            uptime_percentage=100.0
        )
    
    def health_check(self) -> Dict[str, Any]:
        """Health check endpoint."""
        return {
            "status": "healthy",
            "agent": self.name,
            "version": self.version,
            "timestamp": datetime.utcnow().isoformat()
        }
