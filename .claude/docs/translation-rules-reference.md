# SBOX Translation Rules - Developer Reference

**Version**: 1.0
**Source**: StarDance Knowledge Library v1
**Purpose**: Canonical source for understanding parameter generation

## Formula Rules

### PACING FORMULAS
```
cuts_per_30s = 4 + (momentum/100 * 12) + (presence/100 * 4)
Range: 4-20 (integer)

Example: momentum: 20, presence: 15
= 4 + 2.4 + 0.6 = 7 cuts
```

### COLOR FORMULAS
```
saturation = 0.3 + (presence/100 * 0.4) + (taste/100 * 0.3)
Range: 0.3-1.0 (float)

Example: presence: 15, taste: 8
= 0.3 + 0.06 + 0.024 = 0.384
```

## Decision Tree Rules

### AUDIO - VOICEOVER STYLE
```
IF momentum > 70 THEN "direct"
ELSE IF authenticity > 70 THEN "conversational"
ELSE IF authenticity > 40 THEN "ambient"
ELSE "none"
```

### NARRATIVE - CTA STRENGTH
```
IF momentum > 20 AND autonomy < 15 THEN "urgent"
ELSE IF momentum > 15 THEN "medium"
ELSE "soft"
```

## Common Issues

### Issue 1: "Pacing is too slow"
**Debug**: formula may need higher momentum weighting
**Fix**: Increase momentum to 25+ or presence to 20+

### Issue 2: "CTA isn't urgent for momentum: 20"
**Debug**: Rule is momentum > 20 (exclusive), 20 doesn't trigger
**Fix**: Increase momentum to 21+ or adjust rule to momentum >= 20

## Phase 1 Task

This documentation will be used to write the **sbox-translation-debugger** skill in Phase 1 (Days 5-6).
