"""
T5 Conversion Interface — Phase 2.4 LIVE (DTC Updated)
Hub routes with External A2 Integration + R2 Deployment
"""
import os
import httpx
import boto3
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

from app.t5.a2_schema_adapter import map_a2_to_canonical, UnderwritingResult

router = APIRouter(prefix="/v1", tags=["hub"])

# External A2 endpoint (validated service)
A2_UNDERWRITE_URL = "http://localhost:8080/v1/a2/underwrite"

# R2 Client
def get_r2_client():
    return boto3.client(
        's3',
        endpoint_url=os.getenv('R2_ENDPOINT_URL'),
        aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
        region_name='auto'
    )

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
    stage_profiles: Dict[str, StageProfile] = Field(default={"image": {"presence":0.85,"trust":0.75,"authenticity":0.75,"momentum":0.60,"taste":0.75,"empathy":0.65,"autonomy":0.70,"resonance":0.72,"vitality":0.68,"ethics":0.80},"video": {"presence":0.75,"trust":0.80,"authenticity":0.78,"momentum":0.70,"taste":0.75,"empathy":0.70,"autonomy":0.72,"resonance":0.80,"vitality":0.72,"ethics":0.80},"landing_page": {"presence":0.65,"trust":0.85,"authenticity":0.80,"momentum":0.55,"taste":0.75,"empathy":0.72,"autonomy":0.75,"resonance":0.72,"vitality":0.69,"ethics":0.82}})
    stage_fits: Dict[str, float] = Field(default={"image":0.85,"video":0.84,"landing_page":0.87})
    stage_confidences: Dict[str, float] = Field(default={"image":0.91,"video":0.88,"landing_page":0.91})
    stage_gates_passed: Dict[str, bool] = Field(default={"image":True,"video":True,"landing_page":True})
    stage_profiles: Dict[str, StageProfile]
    stage_fits: Dict[str, float]
    stage_confidences: Dict[str, float]
    stage_gates_passed: Dict[str, bool]

class HubGenerateResponse(BaseModel):
    hub_id: str
    hub_url: str
    tis: float
    gci: float
    clg: float
    routing_band: str
    gate_pass: bool
    status: str

def generate_hub_html(request: HubGenerateRequest, result: UnderwritingResult, hub_id: str) -> str:
    """Generate Hub HTML with TIS/GCI embedded."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{request.brand_id} - Conversion Hub</title>
    <meta name="tis_score" content="{result.tis}">
    <meta name="gci_score" content="{result.gci}">
    <meta name="decision" content="{result.routing_band}">
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background: #fafafa; color: #333; }}
        .container {{ background: white; padding: 40px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .metric {{ background: #f5f5f5; padding: 20px; margin: 15px 0; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }}
        .metric-label {{ font-weight: 600; color: #666; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #111; }}
        .decision {{ font-size: 28px; font-weight: bold; margin: 20px 0; padding: 20px; background: #{'#4CAF50' if result.gate_pass else '#FF9800'}; color: white; border-radius: 8px; text-align: center; }}
        .product-info {{ border-bottom: 2px solid #eee; padding-bottom: 20px; margin-bottom: 30px; }}
        .price {{ font-size: 32px; color: #2c5282; font-weight: bold; }}
        .offer {{ background: #ebf8ff; padding: 15px; border-radius: 6px; margin-top: 20px; border-left: 4px solid #2c5282; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="product-info">
            <h1>{request.campaign_name}</h1>
            <h2>{request.product_name}</h2>
            <div class="price">{request.price}</div>
            <p>{request.product_description}</p>
        </div>
        
        <div class="decision">
            {result.routing_band}
        </div>
        
        <div class="metric">
            <span class="metric-label">Transition Integrity Score (TIS)</span>
            <span class="metric-value">{result.tis:.4f}</span>
        </div>
        
        <div class="metric">
            <span class="metric-label">Gate Compliance Index (GCI)</span>
            <span class="metric-value">{result.gci:.4f}</span>
        </div>
        
        <div class="metric">
            <span class="metric-label">Conversion Likelihood (CLG)</span>
            <span class="metric-value">{result.clg:.4f}</span>
        </div>
        
        <div class="offer">
            <strong>Special Offer:</strong> {request.offer_hook}
        </div>
        
        <p style="margin-top: 40px; color: #999; font-size: 12px;">
            Hub ID: {hub_id} | Calibration: {result.calibration_event_id or 'N/A'}
        </p>
    </div>
</body>
</html>"""

@router.post("/hub/generate", response_model=HubGenerateResponse)
async def hub_generate(request: HubGenerateRequest):
    """
    T5 Hub Generation — External A2 + R2 Deployment
    """
    # 1. Call External A2 Underwriting
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            a2_payload = {
                "brand_id": request.brand_id,
                "stage_profiles": {
                    k: v.dict() for k, v in request.stage_profiles.items()
                },
                "stage_fits": request.stage_fits,
                "stage_confidences": request.stage_confidences,
                "stage_gates_passed": request.stage_gates_passed
            }
            
            a2_resp = await client.post(A2_UNDERWRITE_URL, json=a2_payload)
            a2_resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"A2 underwrite failed: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"A2 underwriting unavailable: {str(e)}"
        )

    # 2. Map to canonical metrics using adapter
    canonical = map_a2_to_canonical(a2_resp.json())
    
    # Gate enforcement
    if not canonical.gate_pass:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "HUB_GATE_FAILURE",
                "message": "A2 gate compliance check failed",
                "tis": canonical.tis,
                "gci": canonical.gci,
                "clg": canonical.clg,
                "decision": canonical.routing_band
            }
        )

    # 3. Generate Hub HTML
    hub_id = str(uuid.uuid4())[:8]
    hub_path = f"{request.pilot_id}/{request.brand_id}/hub_{hub_id}.html"
    html_content = generate_hub_html(request, canonical, hub_id)

    # 4. Upload to R2
    try:
        s3 = get_r2_client()
        s3.put_object(
            Bucket=os.getenv('R2_BUCKET_NAME'),
            Key=hub_path,
            Body=html_content,
            ContentType='text/html'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"R2 upload failed: {str(e)}")

    # 5. Construct URL
    base_url = os.getenv('HUB_BASE_URL', 'https://hubs.stardance.io')
    hub_url = f"{base_url}/{hub_path}"

    return HubGenerateResponse(
        hub_id=hub_id,
        hub_url=hub_url,
        tis=canonical.tis,
        gci=canonical.gci,
        clg=canonical.clg,
        routing_band=canonical.routing_band,
        gate_pass=canonical.gate_pass,
        status="success"
    )

@router.get("/hub/health")
async def hub_health():
    """T5 health check with R2 status"""
    try:
        s3 = get_r2_client()
        s3.head_bucket(Bucket=os.getenv('R2_BUCKET_NAME'))
        r2_status = "connected"
    except Exception as e:
        r2_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "phase": "2.4",
        "t5": "active",
        "a2_integration": "external",
        "r2_storage": r2_status
    }
