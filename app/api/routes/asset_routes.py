# app/api/routes/asset_routes.py
"""
Asset Scoring API Routes - Phase 2.5A
FastAPI router for 9PD (Nine Dimensions) scoring pipeline.
"""

from fastapi import APIRouter, HTTPException
from app.asset_scoring.asset_schema import AssetProperties
from app.asset_scoring.asset_scorer import AssetScorer

router = APIRouter(prefix="/v1", tags=["asset"])
scorer = AssetScorer()


@router.post("/asset/score")
async def score_asset(asset: AssetProperties, trace: bool = False):
    """
    Phase 2.5A — Asset Properties → 9PD Scoring Pipeline (rule-based 2.5A-v1)
    
    Accepts pre-extracted asset properties. Returns NinePDProfile-compatible vector.
    
    Args:
        asset: AssetProperties with observable creative attributes
        trace: If true, returns per-dimension rule contributions for governance audit
        
    Returns:
        dict: 9PD score vector with versioning and optional trace metadata
    """
    try:
        result = scorer.score(asset, trace=trace)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Asset scoring failed: {str(e)}"
        )


@router.get("/asset/scorer/health")
async def scorer_health():
    """Health check for asset scoring service."""
    return {
        "status": "healthy",
        "scorer_version": "2.5A-v1",
        "rulebook_version": "2026-02-14.1",
        "mode": "rule_based_deterministic"
    }
