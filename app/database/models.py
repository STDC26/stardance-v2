"""SQLAlchemy ORM models for video generation system."""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class VideoGenerationRequest(Base):
    """Links Phase 1 SBOX output to video generation request."""
    __tablename__ = "video_generation_requests"
    
    id = Column(String(36), primary_key=True)
    translation_id = Column(String(36), nullable=False, index=True)  # Links to SBOX
    allocation_id = Column(String(36), nullable=False, index=True)   # Links to CIM
    platform = Column(String(50), nullable=False)  # tiktok, youtube, instagram
    duration = Column(Integer, nullable=False)  # seconds (30, 60, 120)
    content_type = Column(String(50))  # ugc, brand, product, testimonial
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class VideoGenerationInstruction(Base):
    """Output from Video Generation Agent: ready-for-Runway prompt."""
    __tablename__ = "video_generation_instructions"
    
    id = Column(String(36), primary_key=True)
    request_id = Column(String(36), ForeignKey("video_generation_requests.id"), unique=True)
    
    # Prompts (deterministic output from SBOX params)
    main_prompt = Column(String(2000), nullable=False)
    negative_prompt = Column(String(1000), nullable=False)
    style_guidance = Column(String(500), nullable=False)
    
    # Technical specs for Runway
    resolution = Column(String(20), default="1080x1920")
    frame_rate = Column(Integer, default=30)
    codec = Column(String(20), default="h264")
    
    # Runway parameters
    runway_mode = Column(String(20), default="gen3")
    runway_motion_bucket_id = Column(Integer, default=127)
    runway_conditioning_scale = Column(Float, default=1.0)
    runway_steps = Column(Integer, default=30)
    
    # Cost estimates
    estimated_generation_time = Column(Integer)  # seconds
    estimated_cost = Column(Float)  # USD
    
    # For learning: store snapshot of SBOX params
    sbox_parameters_snapshot = Column(JSON)  # {cuts_per_30s: 8, ...}
    dimension_mapping = Column(JSON)  # How each param influenced prompt
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class VideoGenerationOutput(Base):
    """Result after Runway generates the video."""
    __tablename__ = "video_generation_outputs"
    
    id = Column(String(36), primary_key=True)
    instruction_id = Column(String(36), ForeignKey("video_generation_instructions.id"))
    request_id = Column(String(36), ForeignKey("video_generation_requests.id"))
    
    # Status
    status = Column(String(20), default="pending")  # pending, completed, failed
    error_code = Column(String(50))
    error_message = Column(String(500))
    
    # Video output from Runway
    video_url = Column(String(500))
    video_duration = Column(Integer)
    video_resolution = Column(String(20))
    video_size_bytes = Column(Integer)
    
    # Runway metadata
    runway_generation_id = Column(String(100), unique=True)
    runway_seed = Column(Integer)
    runway_processing_time = Column(Integer)  # milliseconds
    runway_cost = Column(Float)  # actual cost incurred
    
    # Distribution (filled by Phase 2.2 n8n)
    platform_post_id = Column(String(200))
    published_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
