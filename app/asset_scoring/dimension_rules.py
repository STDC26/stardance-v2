# app/asset_scoring/dimension_rules.py
"""
Nine Dimensions of Psychological Conversion (9PD) — Rule-Based Scoring v2.5A-v1

Each function maps observable asset properties to psychological predictions.
Rules derived from conversion psychology heuristics:

- Presence: Visual weight and attention command
- Trust: Credibility signals and informational clarity  
- Authenticity: Realness vs. staged/marketing feel
- Momentum: Urgency and energetic drive
- Taste: Premium perception and aesthetic restraint
- Empathy: Emotional connection and human warmth
- Autonomy: User agency preservation (non-manipulative)
- Resonance: Cultural/category fit and relevance
- Ethics: Honesty and non-deception signals

Rulebook Version: 2026-02-14.1

# TODO Phase 3: Replace rule heuristics with Claude-assisted scoring
# Maintain v1 as fallback and calibration baseline.
"""

from .asset_schema import AssetProperties


def compute_aggression(asset: AssetProperties) -> float:
    """
    Shared penalty term for aggressive creative signals.
    Applied to autonomy, ethics, trust to prevent gaming.
    
    CTA presence: +0.15
    Saturation > 0.85: +0.10  
    Text density > 0.35: +0.05
    Cap: 0.30 (prevents over-penalization)
    """
    aggression = 0.0
    if asset.cta_present:
        aggression += 0.15
    if asset.saturation > 0.85:
        aggression += 0.10
    if asset.text_density > 0.35:
        aggression += 0.05
    return min(aggression, 0.30)


def score_presence(asset: AssetProperties) -> float:
    """
    How commanding is this asset?
    
    Rule logic: Faces command attention (+0.20). High saturation arrests (+0.15).
    Clean backgrounds reduce cognitive load, increasing command (+0.10).
    Low text density signals visual confidence (+0.05).
    """
    score = 0.5  # baseline
    if asset.face_present:
        score += 0.20
    if asset.saturation > 0.7:
        score += 0.15
    if asset.visual_complexity < 0.4:
        score += 0.10
    if asset.text_density < 0.2:
        score += 0.05
    return min(score, 1.0)


def score_trust(asset: AssetProperties, aggression: float) -> float:
    """
    Does this feel credible?
    
    Rule logic: Cool colors signal professionalism (+0.15).
    Clean backgrounds signal organization (+0.15).
    Moderate text density signals transparency (+0.10).
    Product visibility signals honesty (+0.10).
    Aggression signals reduce trust (-0.3x penalty).
    """
    score = 0.5
    if asset.color_temperature == "cool":
        score += 0.15
    if asset.background_style == "clean":
        score += 0.15
    if asset.text_density > 0.2:
        score += 0.10
    if asset.product_visible:
        score += 0.10
    score -= aggression * 0.3
    return max(min(score, 1.0), 0.0)


def score_authenticity(asset: AssetProperties) -> float:
    """
    Does this feel real, not staged?
    
    Rule logic: Lifestyle backgrounds suggest real contexts (+0.20).
    Faces suggest real people (+0.15).
    Lower saturation suggests less digital manipulation (+0.10).
    Warmth suggests human touch (+0.05).
    """
    score = 0.5
    if asset.background_style == "lifestyle":
        score += 0.20
    if asset.face_present:
        score += 0.15
    if asset.saturation < 0.6:
        score += 0.10
    if asset.color_temperature == "warm":
        score += 0.05
    return min(score, 1.0)


def score_momentum(asset: AssetProperties) -> float:
    """
    Does this feel urgent/energetic?
    
    Rule logic: CTAs demand action (+0.20). High saturation creates urgency (+0.15).
    Visual complexity suggests movement/dynamism (+0.10). Warm colors accelerate (+0.05).
    
    Video modifiers: Fast pacing (+0.10), high scene count (+0.05).
    """
    score = 0.5
    if asset.cta_present:
        score += 0.20
    if asset.saturation > 0.75:
        score += 0.15
    if asset.visual_complexity > 0.6:
        score += 0.10
    if asset.color_temperature == "warm":
        score += 0.05
    # Video modifiers (guarded for Phase 2.5B)
    if asset.pacing is not None and asset.pacing > 0.7:
        score += 0.10
    if asset.scene_count is not None and asset.scene_count > 8:
        score += 0.05
    return min(score, 1.0)


def score_taste(asset: AssetProperties) -> float:
    """
    Does this feel premium/considered?
    
    Rule logic: Clean backgrounds signal curation (+0.20).
    Low complexity signals restraint (+0.15).
    Moderate saturation signals sophistication (+0.10).
    Neutral temps signal timelessness (+0.05).
    """
    score = 0.5
    if asset.background_style == "clean":
        score += 0.20
    if asset.visual_complexity < 0.35:
        score += 0.15
    if 0.5 < asset.saturation < 0.75:
        score += 0.10
    if asset.color_temperature == "neutral":
        score += 0.05
    return min(score, 1.0)


def score_empathy(asset: AssetProperties) -> float:
    """
    Does this connect emotionally?
    
    Rule logic: Faces enable mirror neurons (+0.25).
    Lifestyle contexts enable narrative (+0.15).
    Warm colors enable emotional warmth (+0.10).
    Narration adds human voice (+0.10 video only).
    """
    score = 0.5
    if asset.face_present:
        score += 0.25
    if asset.background_style == "lifestyle":
        score += 0.15
    if asset.color_temperature == "warm":
        score += 0.10
    # Video modifier (guarded for Phase 2.5B)
    if asset.narration_present:
        score += 0.10
    return min(score, 1.0)


def score_autonomy(asset: AssetProperties, aggression: float) -> float:
    """
    Does this feel empowering, not pushy?
    
    Rule logic: Absence of CTA preserves user agency (+0.15).
    Low text density reduces pressure (+0.10).
    Clean backgrounds reduce manipulation tactics (+0.10).
    Simplicity respects intelligence (+0.05).
    Aggression signals heavily penalize autonomy (-0.8x - strongest effect).
    """
    score = 0.5
    if not asset.cta_present:
        score += 0.15
    if asset.text_density < 0.15:
        score += 0.10
    if asset.background_style == "clean":
        score += 0.10
    if asset.visual_complexity < 0.4:
        score += 0.05
    score -= aggression * 0.8  # strongest aggression penalty
    return max(min(score, 1.0), 0.0)


def score_resonance(asset: AssetProperties) -> float:
    """
    Does this feel culturally/categorically right?
    
    Rule logic: Product visibility ensures relevance (+0.15).
    Warm + face = human connection (+0.15).
    Lifestyle context = cultural embedding (+0.10).
    """
    score = 0.5
    if asset.product_visible:
        score += 0.15
    if asset.color_temperature == "warm" and asset.face_present:
        score += 0.15
    if asset.background_style == "lifestyle":
        score += 0.10
    return min(score, 1.0)


def score_ethics(asset: AssetProperties, aggression: float) -> float:
    """
    Does this feel honest, not manipulative?
    
    Rule logic: Low text density = no fine print (+0.10).
    Non-abstract = grounded claims (+0.10).
    Aggression signals suggest manipulation (-0.6x penalty).
    """
    score = 0.5
    if asset.text_density < 0.3:
        score += 0.10
    if asset.background_style != "abstract":
        score += 0.10
    score -= aggression * 0.6
    return max(min(score, 1.0), 0.0)
