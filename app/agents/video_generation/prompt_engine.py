"""
Prompt Engine: Convert 16 SBOX parameters → Runway-ready video prompts.

This is the core intelligence that translates creative dimensions into 
deterministic text prompts. Same input = same output (testable, learnable).
"""

from typing import Dict, Any, Tuple
import json


class PromptEngine:
    """Convert SBOX parameters → video generation prompts."""
    
    def __init__(self):
        """Initialize parameter mapping rules."""
        self.version = "2.0.0"
    
    def convert(
        self, 
        sbox_params: Dict[str, Any],
        platform: str,
        duration: int
    ) -> Tuple[str, str, str]:
        """
        Convert 16 SBOX parameters to prompts.
        
        Args:
            sbox_params: All 16 SBOX parameters
            platform: tiktok, youtube, instagram, reels
            duration: video duration in seconds
        
        Returns:
            (main_prompt, negative_prompt, style_guidance)
        """
        # Build prompt components
        pacing_desc = self._describe_pacing(sbox_params, duration)
        color_desc = self._describe_color(sbox_params)
        composition_desc = self._describe_composition(sbox_params)
        audio_desc = self._describe_audio(sbox_params)
        narrative_desc = self._describe_narrative(sbox_params)
        
        # Assemble main prompt
        main_prompt = self._assemble_main_prompt(
            platform, duration, pacing_desc, color_desc, 
            composition_desc, audio_desc, narrative_desc
        )
        
        # Assemble negative prompt
        negative_prompt = self._assemble_negative_prompt(sbox_params)
        
        # Assemble style guidance
        style_guidance = self._assemble_style_guidance(platform, sbox_params)
        
        return main_prompt, negative_prompt, style_guidance
    
    def _describe_pacing(self, params: Dict, duration: int) -> str:
        """Describe pacing from cuts_per_30s, bpm_equivalent, tempo_curve."""
        cuts = params.get('cuts_per_30s', 5)
        bpm = params.get('bpm_equivalent', 100)
        tempo = params.get('tempo_curve', 'constant')
        
        # Map cuts to pacing descriptor
        if cuts >= 8:
            cut_desc = "very fast cuts (8+ cuts per 30 seconds)"
        elif cuts >= 5:
            cut_desc = "fast cuts (5-7 cuts per 30 seconds)"
        elif cuts >= 3:
            cut_desc = "moderate pacing (3-4 cuts per 30 seconds)"
        else:
            cut_desc = "slow, deliberate cuts (1-2 cuts per 30 seconds)"
        
        # Map BPM to energy
        if bpm >= 120:
            bpm_desc = "high-energy, fast-paced rhythm"
        elif bpm >= 90:
            bpm_desc = "moderate, steady rhythm"
        else:
            bpm_desc = "slow, contemplative rhythm"
        
        # Map tempo curve
        if tempo == "accelerating":
            tempo_desc = "building momentum and intensity"
        elif tempo == "decelerating":
            tempo_desc = "slowing down toward conclusion"
        else:
            tempo_desc = "maintaining consistent energy"
        
        return f"{cut_desc}, {bpm_desc}, {tempo_desc}"
    
    def _describe_color(self, params: Dict) -> str:
        """Describe color from saturation, contrast, palette."""
        saturation = params.get('saturation', 0.5)
        contrast = params.get('contrast', 'medium')
        palette = params.get('palette', 'balanced')
        
        # Map saturation to vividness
        if saturation > 0.7:
            sat_desc = "highly saturated, vibrant colors"
        elif saturation > 0.4:
            sat_desc = "moderately saturated colors"
        else:
            sat_desc = "muted, desaturated color palette"
        
        # Map contrast
        if contrast == "high":
            contrast_desc = "high contrast between elements"
        elif contrast == "low":
            contrast_desc = "soft, low-contrast lighting"
        else:
            contrast_desc = "balanced contrast"
        
        # Map palette type
        if palette == "vibrant":
            palette_desc = "vibrant, bold color combinations"
        elif palette == "warm":
            palette_desc = "warm tones (oranges, reds, yellows)"
        elif palette == "cool":
            palette_desc = "cool tones (blues, purples, greens)"
        else:
            palette_desc = "neutral, professional color palette"
        
        return f"{sat_desc}, {contrast_desc}, featuring {palette_desc}"
    
    def _describe_composition(self, params: Dict) -> str:
        """Describe composition from framing, motion_style, focal_point."""
        framing = params.get('framing', 'medium')
        motion = params.get('motion_style', 'smooth')
        focal = params.get('focal_point', 'center')
        
        # Map framing
        if framing == "wide":
            frame_desc = "wide establishing shots showing full scenes"
        elif framing == "close":
            frame_desc = "close-up detailed shots with tight framing"
        else:
            frame_desc = "medium framing balancing detail and context"
        
        # Map motion
        if motion == "dynamic":
            motion_desc = "dynamic, energetic camera movements"
        elif motion == "static":
            motion_desc = "static, stable shots"
        else:
            motion_desc = "smooth, flowing camera movements"
        
        # Map focal point
        if focal == "distributed":
            focal_desc = "distributed attention across frame"
        elif focal == "subject":
            focal_desc = "subject-focused composition"
        else:
            focal_desc = "centered composition"
        
        return f"{frame_desc}, {motion_desc}, {focal_desc}"
    
    def _describe_audio(self, params: Dict) -> str:
        """Describe audio from voiceover_style, music_energy, voice_tone."""
        voiceover = params.get('voiceover_style', 'moderate')
        music = params.get('music_energy', 'moderate')
        voice_tone = params.get('voice_tone', 'professional')
        
        # Map voiceover presence
        if voiceover == "direct":
            vo_desc = "prominent, direct voiceover"
        elif voiceover == "subtle":
            vo_desc = "subtle background narration"
        else:
            vo_desc = "moderate voiceover presence"
        
        # Map music energy
        if music == "driving":
            music_desc = "driving, energetic music"
        elif music == "ambient":
            music_desc = "ambient, atmospheric background music"
        else:
            music_desc = "moderate, supportive music"
        
        # Map voice tone
        if voice_tone == "friendly":
            tone_desc = "friendly, approachable tone"
        elif voice_tone == "authoritative":
            tone_desc = "authoritative, confident tone"
        else:
            tone_desc = "professional, neutral tone"
        
        return f"{vo_desc}, {music_desc}, with {tone_desc}"
    
    def _describe_narrative(self, params: Dict) -> str:
        """Describe narrative from structure, cta_strength, proof_elements, hook_placement."""
        structure = params.get('structure', 'story')
        cta = params.get('cta_strength', 'medium')
        proof = params.get('proof_elements', 'moderate')
        hook = params.get('hook_placement', 'gradual')
        
        # Map narrative structure
        if structure == "observational":
            struct_desc = "observational narrative showing real situations"
        elif structure == "testimonial":
            struct_desc = "testimonial-driven narrative with people speaking"
        elif structure == "data":
            struct_desc = "data-driven narrative with statistics"
        else:
            struct_desc = "story-driven narrative arc"
        
        # Map CTA strength
        if cta == "strong":
            cta_desc = "strong, explicit call-to-action"
        elif cta == "subtle":
            cta_desc = "subtle, implicit call-to-action"
        else:
            cta_desc = "moderate call-to-action"
        
        # Map proof elements
        if proof == "extensive":
            proof_desc = "extensive proof elements (testimonials, data)"
        elif proof == "minimal":
            proof_desc = "minimal proof elements, focus on story"
        else:
            proof_desc = "moderate proof elements"
        
        # Map hook placement
        if hook == "immediate":
            hook_desc = "immediate attention-grabbing hook"
        elif hook == "gradual":
            hook_desc = "gradual build-up to main message"
        else:
            hook_desc = "natural hook placement"
        
        return f"{struct_desc}, {cta_desc}, {proof_desc}, {hook_desc}"
    
    def _assemble_main_prompt(
        self, platform, duration, pacing, color, 
        composition, audio, narrative
    ) -> str:
        """Assemble coherent main prompt from components."""
        
        platform_context = {
            "tiktok": "TikTok video (vertical 9:16 format, native TikTok aesthetic)",
            "youtube": "YouTube Short (vertical 9:16 format, polished production)",
            "instagram": "Instagram Reel (vertical 9:16 format, Instagram-native feel)",
            "reels": "Instagram Reel (mobile-optimized, quick-cutting format)"
        }
        
        platform_desc = platform_context.get(platform, "vertical video format")
        
        main_prompt = f"""
{platform_desc}, {duration} seconds long.

Pacing: {pacing}

Color & Visual: {color}

Composition: {composition}

Audio: {audio}

Narrative: {narrative}

Production quality: Professional, polished, optimized for mobile viewing. 
Avoid text overlays unless essential. Prioritize visual storytelling. 
Generate content that is engaging, memorable, and platform-native.
""".strip()
        
        return main_prompt
    
    def _assemble_negative_prompt(self, params: Dict) -> str:
        """Assemble negative prompt (what to avoid)."""
        negative_elements = [
            "No watermarks",
            "No visible logos unless essential",
            "No blurry footage",
            "No low-quality audio",
            "No static text overlays",
            "No jarring transitions",
            "No long pauses or dead air",
            "No compression artifacts",
            "No out-of-focus critical moments",
            "Avoid corporate, stiff presentation"
        ]
        
        # Add platform-specific negatives
        platform = params.get('platform', 'tiktok')
        if platform in ['tiktok', 'instagram']:
            negative_elements.append("No vertical letterboxing")
        
        return ", ".join(negative_elements)
    
    def _assemble_style_guidance(self, platform: str, params: Dict) -> str:
        """Assemble style guidance for Runway."""
        
        styles = {
            "tiktok": "TikTok native format (9:16), trending aesthetic, authentic feel, quick-cutting, modern",
            "youtube": "YouTube Short format (9:16), polished production, professional quality, cinematic",
            "instagram": "Instagram Reel format (9:16), Instagram-native aesthetic, smooth transitions, engaging",
            "reels": "Reels format (mobile-optimized), fast-paced, native feel, trend-responsive"
        }
        
        base_style = styles.get(platform, "modern, mobile-optimized")
        
        # Add content type styling if present
        content_type = params.get('content_type')
        if content_type == "ugc":
            base_style += ", user-generated content aesthetic, authentic, unpolished"
        elif content_type == "brand":
            base_style += ", brand-focused, professional, cohesive visual identity"
        elif content_type == "testimonial":
            base_style += ", human-centric, authentic testimonials, real people"
        
        return base_style
