"""Unit tests for Video Generation Agent."""

import pytest
from app.agents.video_generation.agent import VideoGenerationAgent
from app.agents.video_generation.models import VideoGenerationRequestInput, Platform


@pytest.fixture
def agent():
    """Initialize agent."""
    return VideoGenerationAgent()


@pytest.fixture
def sample_request():
    """Sample request for testing."""
    return VideoGenerationRequestInput(
        translation_id="sbox_test_123",
        allocation_id="cim_test_456",
        sbox_parameters={
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
        platform=Platform.TIKTOK,
        duration=30
    )


class TestAgentTranslate:
    """Test agent translate method."""
    
    def test_translate_returns_instruction(self, agent, sample_request):
        """Translate should return valid instruction."""
        instruction = agent.translate(sample_request)
        assert instruction.instruction_id.startswith("vgen_instr_")
        assert instruction.request_id.startswith("vgen_req_")
        assert instruction.status == "ready"
    
    def test_translate_generates_main_prompt(self, agent, sample_request):
        """Instruction should have main prompt."""
        instruction = agent.translate(sample_request)
        assert len(instruction.main_prompt) > 100
    
    def test_translate_generates_negative_prompt(self, agent, sample_request):
        """Instruction should have negative prompt."""
        instruction = agent.translate(sample_request)
        assert len(instruction.negative_prompt) > 20
    
    def test_translate_estimates_cost(self, agent, sample_request):
        """Instruction should estimate cost."""
        instruction = agent.translate(sample_request)
        assert instruction.estimated_cost > 0


class TestAgentMetrics:
    """Test agent metrics tracking."""
    
    def test_agent_tracks_completed(self, agent, sample_request):
        """Agent should track completed instructions."""
        initial_count = agent.completed_count
        agent.translate(sample_request)
        assert agent.completed_count == initial_count + 1
    
    def test_agent_get_status(self, agent, sample_request):
        """Agent status should be available."""
        agent.translate(sample_request)
        status = agent.get_status()
        assert status.status == "operational"
        assert status.completed_instructions == 1
