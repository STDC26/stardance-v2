# app/asset_scoring/asset_schema.py
from pydantic import BaseModel, Field
from typing import Literal, Optional

class AssetProperties(BaseModel):
    """
    Observable, extractable properties from any SBOX-generated asset.
    Phase 2.5A Rule-Based Pipeline input schema.
    
    Note: 'trace' is NOT included here - it is a query parameter on the API endpoint
    to keep asset properties pure (observable inputs only).
    
    # TODO Phase 2.5B: Add automated extraction from raw files
    # TODO Phase 3: Expand with embedding vectors for semantic scoring
    """
    asset_id: str = Field(..., description="Unique identifier from SBOX generation")
    asset_type: Literal["image", "video"] = Field(..., description="Media type for routing logic")
    
    # Image properties
    color_temperature: Literal["warm", "cool", "neutral"] = Field(
        default="neutral", description="Dominant color temperature"
    )
    text_density: float = Field(
        default=0.15, ge=0.0, le=1.0, 
        description="Ratio of text pixels to total (0.0=none, 1.0=all text)"
    )
    visual_complexity: float = Field(
        default=0.45, ge=0.0, le=1.0, 
        description="Edge density / information entropy (0.0=min, 1.0=max chaos)"
    )
    cta_present: bool = Field(
        default=False, description="Call-to-action button or text visible"
    )
    face_present: bool = Field(
        default=False, description="Human face detected in asset"
    )
    product_visible: bool = Field(
        default=True, description="Product is clearly visible (not abstract)"
    )
    background_style: Literal["clean", "lifestyle", "abstract"] = Field(
        default="clean", description="Categorical background type"
    )
    saturation: float = Field(
        default=0.65, ge=0.0, le=1.0, 
        description="Color saturation level (0.0=grayscale, 1.0=neon)"
    )

    # Video-specific properties (scaffold — Phase 2.5B)
    pacing: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, 
        description="Video pacing speed (0.0=slow, 1.0=rapid cuts)"
    )
    scene_count: Optional[int] = Field(
        default=None, ge=0, 
        description="Number of scene changes"
    )
    narration_present: Optional[bool] = Field(
        default=None, description="Voiceover or narration present"
    )
    sfx_present: Optional[bool] = Field(
        default=None, description="Sound effects present"
    )
    on_screen_text_density: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, 
        description="Text overlay density specific to video"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "asset_id": "lumiere_img_001",
                "asset_type": "image",
                "color_temperature": "cool",
                "text_density": 0.20,
                "visual_complexity": 0.35,
                "cta_present": False,
                "face_present": False,
                "product_visible": True,
                "background_style": "clean",
                "saturation": 0.65
            }
        }
