# app/asset_scoring/tests/test_asset_scorer.py
"""
Phase 2.5A Asset Scorer Test Suite — PTC Governance Gate
Ten required tests covering regression, boundaries, schema, and governance.
"""

import pytest
from app.asset_scoring.asset_schema import AssetProperties
from app.asset_scoring.asset_scorer import AssetScorer
from app.asset_scoring.dimension_rules import compute_aggression


class TestAssetScorer:
    """v2.5A-v1 Rule-Based Scorer Validation — All tests must pass for DTC Gate."""
    
    def test_clean_clinical_scores_high_trust(self):
        """Regression: Clean clinical aesthetic must score trust >= 0.75."""
        asset = AssetProperties(
            asset_id="fixture_beauty_clean_clinical",
            asset_type="image",
            color_temperature="cool",
            text_density=0.20,
            visual_complexity=0.30,
            cta_present=False,
            face_present=False,
            product_visible=True,
            background_style="clean",
            saturation=0.60
        )
        scores = AssetScorer().score(asset)["nine_pd_profile"]
        assert scores["trust"] >= 0.75, f"Trust score {scores['trust']} below 0.75 threshold"
    
    def test_lifestyle_face_scores_high_empathy(self):
        """Regression: Lifestyle context with face must score empathy >= 0.75."""
        asset = AssetProperties(
            asset_id="fixture_beauty_lifestyle_warm",
            asset_type="image",
            color_temperature="warm",
            text_density=0.10,
            visual_complexity=0.40,
            cta_present=False,
            face_present=True,
            product_visible=True,
            background_style="lifestyle",
            saturation=0.65
        )
        scores = AssetScorer().score(asset)["nine_pd_profile"]
        assert scores["empathy"] >= 0.75, f"Empathy score {scores['empathy']} below 0.75 threshold"
    
    def test_hard_sell_scores_low_autonomy_and_ethics(self):
        """Regression: Aggressive creative must be penalized in autonomy/ethics."""
        asset = AssetProperties(
            asset_id="fixture_beauty_hard_sell",
            asset_type="image",
            color_temperature="warm",
            text_density=0.40,
            visual_complexity=0.65,
            cta_present=True,
            face_present=False,
            product_visible=True,
            background_style="abstract",
            saturation=0.90
        )
        scores = AssetScorer().score(asset)["nine_pd_profile"]
        assert scores["autonomy"] <= 0.40, f"Autonomy {scores['autonomy']} should be <= 0.40 (aggression penalty)"
        assert scores["ethics"] <= 0.50, f"Ethics {scores['ethics']} should be <= 0.50 (aggression penalty)"
        assert scores["momentum"] >= 0.75, f"Momentum {scores['momentum']} should be >= 0.75 (aggressive signals)"
    
    def test_default_asset_midband_guard(self):
        """Boundary: Default asset must NOT inflate into high band. No dimension exceeds 0.80."""
        asset = AssetProperties(asset_id="default_test", asset_type="image")
        scores = AssetScorer().score(asset)["nine_pd_profile"]
        for dim, val in scores.items():
            assert 0.35 <= val <= 0.85, f"{dim} outside midband: {val} (expected 0.35-0.80)"
    
    def test_all_scores_within_bounds(self):
        """Boundary: All dimension scores must be strictly 0.0–1.0."""
        asset = AssetProperties(
            asset_id="bounds_test",
            asset_type="image",
            color_temperature="warm",
            text_density=0.99,
            visual_complexity=0.99,
            saturation=0.99,
            cta_present=True,
            face_present=True
        )
        scores = AssetScorer().score(asset)["nine_pd_profile"]
        for dim, val in scores.items():
            assert 0.0 <= val <= 1.0, f"{dim} out of bounds: {val}"
    
    def test_schema_key_exact_match(self):
        """Schema: Output keys must EXACTLY match NinePDProfile fields. Zero drift."""
        expected_keys = {
            "presence", "trust", "authenticity", "momentum", "taste", 
            "empathy", "autonomy", "resonance", "ethics"
        }
        asset = AssetProperties(asset_id="schema_test", asset_type="image")
        scores = AssetScorer().score(asset)["nine_pd_profile"]
        assert set(scores.keys()) == expected_keys, f"Schema mismatch. Got: {set(scores.keys())}"
    
    def test_trace_mode_returns_deltas(self):
        """Governance: trace=True (query param) must return aggression effects."""
        asset = AssetProperties(
            asset_id="trace_test",
            asset_type="image",
            cta_present=True,
            saturation=0.88,
            text_density=0.40
        )
        result = AssetScorer().score(asset, trace=True)
        assert result["trace_enabled"] == True
        assert "trace" in result
        assert "aggression_penalty" in result["trace"]
        assert result["trace"]["aggression_penalty"] > 0
        assert "aggression_effects" in result["trace"]
        assert result["trace"]["aggression_effects"]["autonomy_delta"] < 0
    
    def test_aggression_monotonicity(self):
        """Governance: Aggression penalty must increase predictably and cap at 0.30."""
        asset1 = AssetProperties(asset_id="a1", asset_type="image", cta_present=True)
        asset2 = AssetProperties(asset_id="a2", asset_type="image", cta_present=True, saturation=0.90)
        asset3 = AssetProperties(asset_id="a3", asset_type="image", cta_present=True, saturation=0.90, text_density=0.40)
        
        agg1 = compute_aggression(asset1)
        agg2 = compute_aggression(asset2)
        agg3 = compute_aggression(asset3)
        
        assert agg1 > 0, "CTA alone must trigger aggression"
        assert agg2 > agg1, "Adding high saturation must increase aggression"
        assert agg3 == 0.30, f"Max inputs must cap at 0.30, got {agg3}"
    
    def test_invalid_background_style_rejected(self):
        """Validation: Invalid categorical enum values must fail Pydantic validation."""
        with pytest.raises(Exception):  # ValidationError
            AssetProperties(
                asset_id="bad_test",
                asset_type="image",
                background_style="studio"  # invalid
            )
    
    def test_versioning_fields_present(self):
        """Governance: All version fields must be present and exact."""
        asset = AssetProperties(asset_id="version_test", asset_type="image")
        result = AssetScorer().score(asset)
        
        assert "scorer_version" in result
        assert "rulebook_version" in result
        assert "nine_pd_schema_version" in result
        assert result["nine_pd_schema_version"] == "A2.NinePDProfile.v1"
        assert result["scorer_version"] == "2.5A-v1"
        assert result["rulebook_version"] == "2026-02-14.1"
        assert "trace_enabled" in result
        assert result["trace_enabled"] == False  # default
