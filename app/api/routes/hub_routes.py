"""
T5 Conversion Interface — Phase 2.4 LIVE
Hub routes for Conversion Interface Activation
"""
import os
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

from app.t5.a2_schema_adapter import map_a2_to_canonical, UnderwritingResult

router = APIRouter(prefix="/v1", tags=["hub"])

# Internal A2 endpoint (same service)
A2_UNDERWRITE_URL = "http://localhost:8000/v1/a2/underwrite"


class HubGenerateRequest(BaseModel):
    allocation_id: str = Field(...)
    translation_id: str = Field(...)
    campaign_id: str = Field(...)
    brand_id: str = Field(...)
    pilot_id: str = Field(...)
    campaign_name: str = Field(...)
    product_name: str = Field(...)
    product_description: str = Field(...)
    price: str = Field(...)
    offer_hook: str = Field(...)


class HubGenerateResponse(BaseModel):
    hub_id: str
    tis: float  # Transition Integrity Score
    gci: float  # Gate Compliance Index
    clg: float  # Conversion Likelihood Gradient
    routing_band: str
    gate_pass: bool
    status: str


@router.post("/hub/generate", response_model=HubGenerateResponse)
async def hub_generate(request: HubGenerateRequest):
    """
    T5 Hub Generation — Live A2 Integration
    Gate 2.4.2: A2 compliance check BEFORE expensive operations
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            a2_resp = await client.post(
                A2_UNDERWRITE_URL,
                json={
                    "allocation_id": request.allocation_id,
                    "translation_id": request.translation_id,
                    "target_stage": "landing_page",
                    "pla_sequence": ["image", "video", "landing_page"]
                }
            )
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

    # Map to canonical T5 vocabulary (A2 field names STOP here)
    canonical = map_a2_to_canonical(a2_resp.json())

    # Gate enforcement: Hard fail if GCI check fails (saves Claude API cost)
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

    return HubGenerateResponse(
        hub_id=f"hub_{request.brand_id}_{request.pilot_id}_001",
        tis=canonical.tis,
        gci=canonical.gci,
        clg=canonical.clg,
        routing_band=canonical.routing_band,
        gate_pass=canonical.gate_pass,
        status="success"
    )


@router.get("/hub/health")
async def hub_health():
    """T5 health check"""
    return {
        "status": "healthy",
        "phase": "2.4",
        "t5": "active",
        "a2_integration": "live"
    }
