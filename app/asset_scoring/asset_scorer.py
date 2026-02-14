# app/asset_scoring/asset_scorer.py
"""
Asset Scoring Pipeline - Phase 2.5A
Rule-based 9PD (Nine Dimensions of Psychological Conversion) scoring.

Version: 2.5A-v1
Rulebook: 2026-02-14.1
Schema: A2.NinePDProfile.v1

# TODO Phase 2.5B: Add raw file -> property extraction layer
# TODO Phase 3: Replace rule engine with Claude-assisted scoring
"""

from .asset_schema import AssetProperties
from .dimension_rules import (
    compute_aggression,
    score_presence,
    score_trust,
    score_authenticity,
    score_momentum,
    score_taste,
    score_empathy,
    score_autonomy,
    score_resonance,
    score_ethics,
)

# Version constants for governance and audit trails
SCORER_VERSION = "2.5A-v1"
RULEBOOK_VERSION = "2026-02-14.1"
NINE_PD_SCHEMA_VERSION = "A2.NinePDProfile.v1"


class AssetScorer:
    """
    v2.5A-v1 Rule-Based Asset -> 9PD Scorer
    
    Converts observable creative properties into Nine Dimensions of 
    Psychological Conversion scores. Deterministic. Traceable. Auditable.
    
    Args:
        asset: AssetProperties with observable creative attributes
        trace: If True, returns per-dimension rule contributions for audit
        
    Returns:
        dict: NinePDProfile-compatible score vector with governance metadata
    """

    def score(self, asset: AssetProperties, trace: bool = False) -> dict:
        """
        Execute all 9 dimension scoring rules with governance audit trail.
        
        Trace mode returns aggression penalties and input snapshots for PTC
        calibration disputes without polluting the core asset schema.
        """
        # Compute shared aggression penalty term
        aggression = compute_aggression(asset)

        # Score all 9 dimensions
        profile = {
            "presence":     round(score_presence(asset), 4),
            "trust":        round(score_trust(asset, aggression), 4),
            "authenticity": round(score_authenticity(asset), 4),
            "momentum":     round(score_momentum(asset), 4),
            "taste":        round(score_taste(asset), 4),
            "empathy":      round(score_empathy(asset), 4),
            "autonomy":     round(score_autonomy(asset, aggression), 4),
            "resonance":    round(score_resonance(asset), 4),
            "ethics":       round(score_ethics(asset, aggression), 4),
        }

        # Assemble response with governance metadata
        result = {
            "asset_id": asset.asset_id,
            "asset_type": asset.asset_type,
            "nine_pd_profile": profile,
            "nine_pd_schema_version": NINE_PD_SCHEMA_VERSION,
            "scorer_version": SCORER_VERSION,
            "rulebook_version": RULEBOOK_VERSION,
            "trace_enabled": trace,
        }

        # Add audit trail if requested (query param, not asset property)
        if trace:
            result["trace"] = self._build_trace(asset, aggression, profile)

        return result

    def _build_trace(self, asset: AssetProperties, aggression: float, profile: dict) -> dict:
        """
        Returns per-dimension rule contributions for governance audit.
        
        Includes aggression penalty calculation and input snapshot for
        immutable audit trails. Prevents post-hoc manipulation accusations
        during PTC calibration disputes.
        """
        return {
            "aggression_penalty": round(aggression, 4),
            "aggression_effects": {
                "autonomy_delta": round(-aggression * 0.8, 4),
                "ethics_delta":   round(-aggression * 0.6, 4),
                "trust_delta":    round(-aggression * 0.3, 4),
            },
            "inputs": {
                "color_temperature": asset.color_temperature,
                "saturation": asset.saturation,
                "cta_present": asset.cta_present,
                "face_present": asset.face_present,
                "background_style": asset.background_style,
                "text_density": asset.text_density,
                "visual_complexity": asset.visual_complexity,
            }
        }
