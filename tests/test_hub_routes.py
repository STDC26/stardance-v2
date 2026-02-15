import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

# HIGH SCORES to pass A2 gates
BASE_PAYLOAD = {
    "allocation_id": "test_alloc_001",
    "translation_id": "test_trans_001", 
    "campaign_id": "test_camp_001",
    "brand_id": "lumiere",
    "pilot_id": "a2_beauty",
    "campaign_name": "LUMIERE Vitamin C Serum",
    "product_name": "LUMIERE Adaptive Vitamin C Serum",
    "product_description": "Clinical-grade Vitamin C serum. 21-day results.",
    "price": "$89",
    "offer_hook": "Clinically proven results in 21 days or your money back",
    "stage_profiles": {
        "image": {"presence": 0.95, "trust": 0.95, "authenticity": 0.95, "momentum": 0.95, "taste": 0.95, "empathy": 0.95, "autonomy": 0.95, "resonance": 0.95, "vitality": 0.95, "ethics": 0.95},
        "video": {"presence": 0.95, "trust": 0.95, "authenticity": 0.95, "momentum": 0.95, "taste": 0.95, "empathy": 0.95, "autonomy": 0.95, "resonance": 0.95, "vitality": 0.95, "ethics": 0.95},
        "landing_page": {"presence": 0.95, "trust": 0.95, "authenticity": 0.95, "momentum": 0.95, "taste": 0.95, "empathy": 0.95, "autonomy": 0.95, "resonance": 0.95, "vitality": 0.95, "ethics": 0.95}
    },
    "stage_fits": {"image": 0.95, "video": 0.95, "landing_page": 0.95},
    "stage_confidences": {"image": 0.98, "video": 0.98, "landing_page": 0.98},
    "stage_gates_passed": {"image": True, "video": True, "landing_page": True},
    "asset_properties": None
}

ASSET_PROPERTIES = {
    "asset_id": "lumiere_img_001",
    "asset_type": "image",
    "color_temperature": "cool",
    "text_density": 0.2,
    "visual_complexity": 0.35,
    "cta_present": False,
    "face_present": False,
    "product_visible": True,
    "background_style": "clean",
    "saturation": 0.65
}

@pytest.fixture(autouse=True)
def mock_r2():
    """Mock R2 upload to avoid external calls and template issues."""
    with patch("app.api.routes.hub_routes.get_r2_client") as mock_client:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        yield mock_s3

def test_hub_generate_with_asset_properties_returns_nine_pd(mock_r2):
    """Gate 2: NinePD properties included → triggers asset scoring."""
    payload = {**BASE_PAYLOAD, "asset_properties": ASSET_PROPERTIES}
    response = client.post("/v1/hub/generate", json=payload)
    assert response.status_code == 200, f"Failed: {response.text}"
    data = response.json()
    assert "hub_url" in data
    assert data["status"] == "success"
    assert data["asset_scoring"] is not None
    # FIXED: Field name is 'nine_pd_profile', not 'nine_pd'
    assert "nine_pd_profile" in data["asset_scoring"]
    assert data["asset_scoring"]["nine_pd_schema_version"] == "A2.NinePDProfile.v1"
    mock_r2.put_object.assert_called_once()

def test_hub_generate_without_asset_properties_returns_null_asset_scoring(mock_r2):
    """Gate 3: No asset properties → asset_scoring is null."""
    response = client.post("/v1/hub/generate", json=BASE_PAYLOAD)
    assert response.status_code == 200, f"Failed: {response.text}"
    data = response.json()
    assert "hub_url" in data
    assert data["status"] == "success"
    assert data["asset_scoring"] is None
    mock_r2.put_object.assert_called_once()

def test_asset_scorer_exception_does_not_block_hub(mock_r2, monkeypatch):
    """Resilience: Asset scorer failure doesn't break hub generation."""
    from app.asset_scoring import asset_scorer as scorer_module
    def raise_error(self, *args, **kwargs):
        raise RuntimeError("Simulated scorer failure")
    monkeypatch.setattr(scorer_module.AssetScorer, "score", raise_error)
    payload = {**BASE_PAYLOAD, "asset_properties": ASSET_PROPERTIES}
    response = client.post("/v1/hub/generate", json=payload)
    assert response.status_code == 200, f"Failed: {response.text}"
    data = response.json()
    assert data["asset_scoring"] is None
    mock_r2.put_object.assert_called_once()

def test_asset_scoring_does_not_influence_a2_fields(mock_r2):
    """Gate 4: asset_scoring is additive only — must NOT change core A2 fields."""
    response_base = client.post("/v1/hub/generate", json=BASE_PAYLOAD)
    assert response_base.status_code == 200
    base = response_base.json()
    
    payload_scored = {**BASE_PAYLOAD, "asset_properties": ASSET_PROPERTIES}
    payload_scored["allocation_id"] = "test_alloc_invariant_002"
    response_scored = client.post("/v1/hub/generate", json=payload_scored)
    assert response_scored.status_code == 200
    scored = response_scored.json()
    
    # FIXED: Compare invariant A2 fields (not hub_url which has unique ID)
    # These should be identical because asset_scoring doesn't affect underwriting
    assert base["tis"] == scored["tis"]
    assert base["gci"] == scored["gci"]
    assert base["clg"] == scored["clg"]
    assert base["status"] == scored["status"]
    assert base["gate_pass"] == scored["gate_pass"]
    assert base["routing_band"] == scored["routing_band"]
    
    # Asset scoring should only be present in scored variant
    assert scored["asset_scoring"] is not None
    assert base["asset_scoring"] is None
    assert mock_r2.put_object.call_count == 2
