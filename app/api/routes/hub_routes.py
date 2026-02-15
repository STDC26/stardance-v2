import os
import uuid
from typing import Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
import boto3
from botocore.exceptions import ClientError

from app.core.ga4_template import get_ga4_snippet
from app.core.utm_builder import build_hub_url

router = APIRouter()

class StageProfile(BaseModel):
    presence: float
    trust: float
    authenticity: float
    momentum: float
    taste: float
    empathy: float
    autonomy: float
    resonance: float
    vitality: float
    ethics: float

class HubGenerateRequest(BaseModel):
    allocation_id: str = Field(...)
    translation_id: str = Field(...)
    campaign_id: str = Field(...)
    brand_id: str = Field(...)
    pilot_id: str = Field(default="a2_beauty")
    campaign_name: str = Field(...)
    product_name: str = Field(...)
    product_description: str = Field(...)
    price: str = Field(...)
    offer_hook: str = Field(...)
    affiliate_url: Optional[str] = Field(default=None, description="Destination URL for affiliate CTA clicks")
    stage_profiles: Dict[str, StageProfile]
    stage_fits: Dict[str, float]
    stage_confidences: Dict[str, float]
    stage_gates_passed: Dict[str, bool]
    asset_properties: Optional[dict] = None

class HubGenerateResponse(BaseModel):
    hub_id: str
    hub_url: str
    status: str

class EmailCaptureRequest(BaseModel):
    email: EmailStr
    hub_id: str
    allocation_id: str = "direct"

def get_r2_client():
    return boto3.client(
        's3',
        endpoint_url=os.getenv('R2_ENDPOINT_URL'),
        aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
        region_name='auto'
    )

def generate_hub_html(hub_data: dict, request: HubGenerateRequest) -> str:
    hub_id = hub_data.get("hub_id", "unknown")
    ga4_snippet = get_ga4_snippet()
    affiliate_url = request.affiliate_url or "#"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{hub_data.get('campaign_name', 'Stardance Hub')}</title>
  {ga4_snippet}
</head>
<body data-hub-id="{hub_id}">
  <div class="hub-container">
    <h1>{hub_data.get('campaign_name')}</h1>
    <p>{hub_data.get('product_description')}</p>
    
    <video controls preload="metadata" style="max-width: 100%;">
      <source src="{hub_data.get('video_url', '')}" type="video/mp4">
    </video>
    
    <form data-capture="email" action="/capture" method="POST">
      <input type="email" name="email" placeholder="Enter your email" required>
      <button type="submit">Get Early Access</button>
    </form>
    
    <a href="{affiliate_url}" data-affiliate="true" class="cta-button">
      {hub_data.get('offer_hook', 'Shop Now')}
    </a>
  </div>
</body>
</html>"""
    return html

@router.post("/capture")
async def capture_email(request: EmailCaptureRequest):
    """Mock email capture endpoint for GA4 Event 3 validation."""
    return {
        "status": "success",
        "message": "Email captured",
        "hub_id": request.hub_id,
        "allocation_id": request.allocation_id
    }

@router.post("/generate", response_model=HubGenerateResponse)
async def generate_hub(request: HubGenerateRequest):
    """Generate attribution-ready T5 Hub with GA4 instrumentation."""
    
    # Generate unique hub ID
    hub_id = f"hub_{uuid.uuid4().hex[:8]}"
    
    # Build UTM-attributed URL using Phase 2.6 builder
    hub_url = build_hub_url(
        hub_id=hub_id,
        allocation_id=request.allocation_id,
        campaign_id=request.campaign_id,
        brand_id=request.brand_id,
        utm_source="direct",
        utm_medium="none"
    )
    
    # Prepare hub data
    hub_data = {
        "hub_id": hub_id,
        "campaign_name": request.campaign_name,
        "product_description": request.product_description,
        "offer_hook": request.offer_hook,
        "video_url": "",  # Populated from asset generation in Phase 2.7
    }
    
    # Generate HTML with GA4 injection (Phase 2.6)
    html_content = generate_hub_html(hub_data, request)
    
    # Upload to R2
    try:
        s3 = get_r2_client()
        s3.put_object(
            Bucket=os.getenv("R2_BUCKET_NAME"),
            Key=f"{hub_id}.html",
            Body=html_content,
            ContentType="text/html"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"R2 upload failed: {str(e)}")
    
    return HubGenerateResponse(
        hub_id=hub_id,
        hub_url=hub_url,
        status="success"
    )

@router.get("/health")
async def hub_health():
    try:
        s3 = get_r2_client()
        s3.head_bucket(Bucket=os.getenv('R2_BUCKET_NAME'))
        r2_status = "connected"
    except Exception as e:
        r2_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "phase": "2.6",
        "t5": "active",
        "a2_integration": "external",
        "r2_storage": r2_status,
        "ga4_attribution": "enabled"
    }
