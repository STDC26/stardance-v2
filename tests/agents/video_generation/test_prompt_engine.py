"""Unit tests for Prompt Engine (16-param mapping)."""

import pytest
from app.agents.video_generation.prompt_engine import PromptEngine


@pytest.fixture
def engine():
    """Initialize prompt engine."""
    return PromptEngine()


@pytest.fixture
def sample_sbox_params():
    """Sample SBOX parameters for testing."""
    return {
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
    }


class TestPromptEngineDeterminism:
    """Test that same input produces same output."""
    
    def test_determinism_same_params_same_output(self, engine, sample_sbox_params):
        """Same params should produce identical prompts."""
        main1, neg1, style1 = engine.convert(sample_sbox_params, "tiktok", 30)
        main2, neg2, style2 = engine.convert(sample_sbox_params, "tiktok", 30)
        assert main1 == main2
        assert neg1 == neg2
        assert style1 == style2
    
    def test_determinism_different_params_different_output(self, engine, sample_sbox_params):
        """Different params should produce different prompts."""
        params1 = sample_sbox_params.copy()
        params2 = sample_sbox_params.copy()
        params2['cuts_per_30s'] = 2
        main1, _, _ = engine.convert(params1, "tiktok", 30)
        main2, _, _ = engine.convert(params2, "tiktok", 30)
        assert main1 != main2


class TestPacingDescriptions:
    """Test pacing parameter mapping."""
    
    def test_fast_cuts_description(self, engine, sample_sbox_params):
        """Fast cuts (8+) should produce text."""
        sample_sbox_params['cuts_per_30s'] = 10
        main, _, _ = engine.convert(sample_sbox_params, "tiktok", 30)
        assert "fast cuts" in main.lower()
    
    def test_slow_cuts_description(self, engine, sample_sbox_params):
        """Slow cuts (1-2) should produce slow text."""
        sample_sbox_params['cuts_per_30s'] = 1
        main, _, _ = engine.convert(sample_sbox_params, "tiktok", 30)
        assert "slow" in main.lower()


class TestColorDescriptions:
    """Test color parameter mapping."""
    
    def test_high_saturation_description(self, engine, sample_sbox_params):
        """High saturation should produce vibrant text."""
        sample_sbox_params['saturation'] = 0.8
        main, _, _ = engine.convert(sample_sbox_params, "tiktok", 30)
        assert "vibrant" in main.lower() or "saturated" in main.lower()
    
    def test_low_saturation_description(self, engine, sample_sbox_params):
        """Low saturation should produce muted text."""
        sample_sbox_params['saturation'] = 0.2
        main, _, _ = engine.convert(sample_sbox_params, "tiktok", 30)
        assert "muted" in main.lower()


class TestNegativePrompt:
    """Test negative prompt generation."""
    
    def test_negative_prompt_has_content(self, engine, sample_sbox_params):
        """Negative prompt should have content."""
        _, neg, _ = engine.convert(sample_sbox_params, "tiktok", 30)
        assert len(neg) > 50
    
    def test_negative_prompt_mentions_watermarks(self, engine, sample_sbox_params):
        """Negative prompt should mention avoiding watermarks."""
        _, neg, _ = engine.convert(sample_sbox_params, "tiktok", 30)
        assert "watermark" in neg.lower()


class TestStyleGuidance:
    """Test style guidance generation."""
    
    def test_tiktok_style_mentions_tiktok(self, engine, sample_sbox_params):
        """TikTok style should mention TikTok."""
        _, _, style = engine.convert(sample_sbox_params, "tiktok", 30)
        assert "tiktok" in style.lower()
    
    def test_youtube_style_mentions_youtube(self, engine, sample_sbox_params):
        """YouTube style should mention YouTube."""
        _, _, style = engine.convert(sample_sbox_params, "youtube", 30)
        assert "youtube" in style.lower()


class TestPromptCompletion:
    """Test that prompts are well-formed."""
    
    def test_main_prompt_has_content(self, engine, sample_sbox_params):
        """Main prompt should have substantial content."""
        main, _, _ = engine.convert(sample_sbox_params, "tiktok", 30)
        assert len(main) > 200
