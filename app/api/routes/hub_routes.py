"""
T5 Conversion Interface — Phase 2.5A LIVE
Hub routes with Asset Scorer Integration (Gate 5 Deferred)
"""
import os
import asyncio
import httpx
import boto3
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional

from app.t5.a2_schema_adapter import map_a2_to_canonical
from app.asset_scoring.asset_schema import AssetProperties
from app.asset_scoring.asset_scorer import AssetScorer

router = APIRouter(prefix="/v1", tags=["hub"])

A2_UNDERWRITE_URL = "https://stardance-a2-underwriting-production.up.railway.app/v1/a2/underwrite"
ASSET_SCORER_TIMEOUT = 0.75

asset_scorer = AssetScorer()

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
    stage_profiles: Dict[str, StageProfile]
    stage_fits: Dict[str, float]
    stage_confidences: Dict[str, float]
    stage_gates_passed: Dict[str, bool]
    asset_properties: Optional[AssetProperties] = None

class HubGenerateResponse(BaseModel):
    hub_id: str
    hub_url: str
    tis: float
    gci: float
    clg: float
    routing_band: str
    gate_pass: bool
    status: str
    asset_scoring: Optional[dict] = None

def generate_hub_html(request, result, hub_id, asset_score=None):
    asset_script = ""
    if asset_score:
        import json
        asset_json_str = json.dumps(asset_score)
        asset_script = f'<script id="asset-scoring" type="application/json">{asset_json_str}</script>'
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{request.brand_id} - Conversion Hub</title>
    <meta name="tis_score" content="{result.tis}">
    <meta name="gci_score" content="{result.gci}">
    <meta name="decision" content="{result.routing_band}">
    {asset_script}
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
        <div class="decision">{result.routing_band}</div>
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

@router.get("/hub/health")
async def hub_health():
    try:
        s3 = get_r2_client()
        s3.head_bucket(Bucket=os.getenv('R2_BUCKET_NAME'))
        r2_status = "connected"
    except Exception as e:
        r2_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "phase": "2.5A",
        "t5": "active",
        "a2_integration": "external",
        "r2_storage": r2_status,
        "asset_scoring": "enabled"
    }

@router.post("/hub/generate", response_model=HubGenerateResponse)
async def hub_generate(request: HubGenerateRequest):
    asset_score_result = None
    
    if request.asset_properties:
        try:
            asset_score_result = await asyncio.wait_for(
                asyncio.to_thread(asset_scorer.score, request.asset_properties),
                timeout=ASSET_SCORER_TIMEOUT
            )
        except asyncio.TimeoutError:
            asset_score_result = None
        except Exception:
            asset_score_result = None
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            a2_payload = {
                "brand_id": request.brand_id,
                "stage_profiles": {k: v.dict() for k, v in request.stage_profiles.items()},
                "stage_fits": request.stage_fits,
                "stage_confidences": request.stage_confidences,
                "stage_gates_passed": request.stage_gates_passed
            }
            a2_resp = await client.post(A2_UNDERWRITE_URL, json=a2_payload)
            a2_resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"A2 underwrite failed: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"A2 underwriting unavailable: {str(e)}")

    canonical = map_a2_to_canonical(a2_resp.json())
    
    # Gate enforcement bypassed for Phase 2.5A demo — HUMAN_REVIEW hubs generate
    # TODO Phase 3: Reinstate gate enforcement with explicit override mechanism
    pass

    hub_id = str(uuid.uuid4())[:8]
    hub_path = f"{request.pilot_id}/{request.brand_id}/hub_{hub_id}.html"
    html_content = generate_hub_html(request, canonical, hub_id, asset_score_result)

    try:
        s3 = get_r2_client()
        s3.put_object(
            Bucket=os.getenv('R2_BUCKET_NAME'),
            Key=hub_path,
            Body=html_content if isinstance(html_content, bytes) else str(html_content).encode('utf-8'),
            ContentType='text/html'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"R2 upload failed: {str(e)}")

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
        status="success",
        asset_scoring=asset_score_result
    )
