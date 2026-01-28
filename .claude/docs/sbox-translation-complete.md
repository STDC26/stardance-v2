# SBOX Translation Engine - Complete Documentation

**Version**: 1.0
**Source**: StarDance Knowledge Library v1

## Overview
SBOX translates CIM dimension allocations into 16 creative parameters across 5 creative levers.

## The Five Creative Levers

### Lever 1: PACING
**Parameters**: cuts_per_30s (4-20), bpm_equivalent (60-140), hold_duration (0.5-5s)

**Formula**:
```
cuts_per_30s = 4 + (momentum/100 * 12) + (presence/100 * 4)
bpm_equivalent = 60 + (momentum/100 * 50) + (presence/100 * 30)
```

**Drivers**: momentum (+), presence (+), autonomy (-)

### Lever 2: COLOR
**Parameters**: saturation (0.3-1.0), contrast (low/medium/high), palette

**Formula**:
```
saturation = 0.3 + (presence/100 * 0.4) + (taste/100 * 0.3)
```

**Drivers**: presence (+), taste (+), authenticity (-)

### Lever 3: COMPOSITION
**Parameters**: framing (wide/medium/tight), motion_style, focal_point

### Lever 4: AUDIO
**Parameters**: voiceover_style, music_energy, voice_tone

**Logic**:
```
IF momentum > 70 THEN voiceover_style = "direct"
ELSE IF authenticity > 70 THEN voiceover_style = "conversational"
```

### Lever 5: NARRATIVE
**Parameters**: structure, cta_strength, proof_elements, hook_placement

**Logic**:
```
IF momentum > 20 AND autonomy < 15 THEN cta_strength = "urgent"
ELSE IF momentum > 15 THEN cta_strength = "medium"
```

## Phase 1 Task

This documentation will be used to write the **sbox-translation-debugger** skill in Phase 1 (Days 5-6).
