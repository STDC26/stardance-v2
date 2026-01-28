"""Unit tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def sample_payload():
    """Sample request payload."""
    return {
        "translation_id": "sbox_test_123",
        "allocation_id": "cim_test_456",
        "sbox_parameters": {
            'cuts_per_30s': 8,
            'bpm_equivalent': 82,
            'tempo_curve': 'accelerating',
            'saturation': 0.379,
            'contrast': 'medium',
            'palette': 'vibrant',
            'framing': 'medium',
            'motion_style': 'dynamic',
            'focal_point': 'distributed',
            'voiceover_style': 'direct',
            'music_energy': 'driving',
            'voice_tone': 'friendly',
            'structure': 'observational',
            'cta_strength': 'medium',
            'proof_elements': 'moderate',
            'hook_placement': 'gradual'
        },
        "platform": "tiktok",
        "duration": 30
    }


class TestRootEndpoint:
    """Test root endpoint."""
    
    def test_root_returns_200(self, client):
        """Root should return 200."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_has_endpoints(self, client):
        """Root should describe endpoints."""
        response = client.get("/")
        data = response.json()
        assert "endpoints" in data


class TestHealthEndpoint:
    """Test health check endpoints."""
    
    def test_health_returns_200(self, client):
        """Health endpoint should return 200."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_status_healthy(self, client):
        """Health should report healthy."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"


class TestTranslateEndpoint:
    """Test POST /agents/video/translate."""
    
    def test_translate_returns_201(self, client, sample_payload):
        """Translate should return 201 Created."""
        response = client.post("/agents/video/translate", json=sample_payload)
        assert response.status_code == 201
    
    def test_translate_returns_instruction(self, client, sample_payload):
        """Translate should return instruction object."""
        response = client.post("/agents/video/translate", json=sample_payload)
        data = response.json()
        assert "instruction_id" in data
        assert "main_prompt" in data
        assert "estimated_cost" in data
    
    def test_translate_missing_params_returns_422(self, client):
        """Missing SBOX params should return 422."""
        payload = {
            "translation_id": "test",
            "allocation_id": "test",
            "sbox_parameters": {"cuts_per_30s": 8},
            "platform": "tiktok",
            "duration": 30
        }
        response = client.post("/agents/video/translate", json=payload)
        assert response.status_code == 422


class TestStatusEndpoint:
    """Test GET /agents/video/status."""
    
    def test_status_returns_200(self, client):
        """Status should return 200."""
        response = client.get("/agents/video/status")
        assert response.status_code == 200
    
    def test_status_has_metrics(self, client):
        """Status should include metrics."""
        response = client.get("/agents/video/status")
        data = response.json()
        assert "completed_instructions" in data
        assert "success_rate" in data
        assert "uptime_percentage" in data


class TestHealthCheckEndpoint:
    """Test GET /agents/video/health."""
    
    def test_video_health_returns_200(self, client):
        """Video health endpoint should return 200."""
        response = client.get("/agents/video/health")
        assert response.status_code == 200
    
    def test_video_health_is_healthy(self, client):
        """Video health should be healthy."""
        response = client.get("/agents/video/health")
        data = response.json()
        assert data["status"] == "healthy"
        assert data["agent"] == "video_generation"
