#!/bin/bash
set -e
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           STARDANCE PHASE 0 QUICK START SCRIPT                 ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

PROJECT_ROOT="$(pwd)"
CLAUDE_DIR="${PROJECT_ROOT}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
DOCS_DIR="${CLAUDE_DIR}/docs"
MCP_CONFIGS_DIR="${CLAUDE_DIR}/mcp-configs"

echo -e "${BLUE}[Step 1/8]${NC} Creating directory structure..."
mkdir -p "${SKILLS_DIR}/9md-framework-validator"
mkdir -p "${SKILLS_DIR}/sbox-translation-debugger"
mkdir -p "${SKILLS_DIR}/dimension-analysis"
mkdir -p "${DOCS_DIR}"
mkdir -p "${MCP_CONFIGS_DIR}"
echo -e "${GREEN}✓${NC} Directory structure created"
echo ""

echo -e "${BLUE}[Step 2/8]${NC} Creating PROJECT_STRUCTURE.md..."
cat > "${CLAUDE_DIR}/PROJECT_STRUCTURE.md" << 'INNER_EOF'
# StarDance Claude Code Integration

## Directory Structure
```
.claude/
├── skills/                          # Agent Skills (auto-loaded)
│   ├── 9md-framework-validator/
│   │   ├── SKILL.md                # 9MD validation logic
│   │   └── examples.md             # Usage examples
│   ├── sbox-translation-debugger/
│   │   ├── SKILL.md                # SBOX debugging logic
│   │   └── examples.md
│   └── dimension-analysis/
│       ├── SKILL.md                # Content scoring
│       └── examples.md
├── mcp-configs/
│   ├── stardance-api-mcp.json      # Live API connections
│   └── github-mcp.json
├── CLAUDE.md                        # Project-level instructions
├── PROJECT_STRUCTURE.md             # This file
└── docs/
    ├── skills-usage-guide.md        # How to use skills
    └── mcp-setup-guide.md           # How to set up MCP
```

## Key Files
- **CLAUDE.md**: Project context, loaded every session
- **Skills**: Auto-discovered from .claude/skills/
- **MCP Configs**: Connection to live APIs
INNER_EOF
echo -e "${GREEN}✓${NC} PROJECT_STRUCTURE.md created"
echo ""

echo -e "${BLUE}[Step 3/8]${NC} Creating CLAUDE.md..."
cat > "${CLAUDE_DIR}/CLAUDE.md" << 'INNER_EOF'
# StarDance Project Context

## Quick Start
You are assisting with StarDance, an AI-powered content commerce platform built on the 9 Dimensions of Human Conversion (9MD) framework.

## Available Skills (Auto-Loaded)
- **9md-framework-validator**: Validates CIM allocations against 9MD framework
- **sbox-translation-debugger**: Debugs SBOX parameter translation
- **dimension-analysis**: Analyzes content against 9 dimensions

## Key Directories
- `/app`: FastAPI backend code
- `/data`: Presets, translation rules, configs
- `/tests`: Test suite
- `/.claude/skills`: Your domain expertise (encoded as skills)
- `/.claude/docs`: Reference documentation

## Current Status
- **MVP**: COMPLETE (production at stardance-mvp)
- **Phase 0**: IN PROGRESS (scaffolding and documentation)
- **Phase 1**: UPCOMING (write 3 skills)
- **Phase 2**: UPCOMING (configure MCP servers)

## Important Principles
1. **Two Environments**: stardance-mvp (FROZEN) and stardance-v2 (ACTIVE)
2. **Never mix code** between environments
3. **9MD Framework**: Ground truth for all allocations
4. **Skills First**: When unsure about framework, ask the skill

## Quick Reference - 9 Dimensions
1. **Presence**: Stop the scroll, attention capture
2. **Authenticity**: Genuineness vs manufactured
3. **Trust**: Credibility signals
4. **Empathy**: Understanding viewer pain/aspirations
5. **Taste**: Aesthetic sophistication
6. **Ethics**: Values alignment
7. **Autonomy**: Respect for choice, no manipulation
8. **Momentum**: Propulsive energy toward action
9. **Resonance**: Cultural fit, memorability

## For Phase 2 Developers
Read in order:
1. `/.claude/docs/skills-usage-guide.md`
2. `/.claude/docs/9md-framework-complete.md`
3. `/.claude/docs/sbox-translation-complete.md`
INNER_EOF
echo -e "${GREEN}✓${NC} CLAUDE.md created"
echo ""

echo -e "${BLUE}[Step 4/8]${NC} Creating skills-usage-guide.md..."
cat > "${DOCS_DIR}/skills-usage-guide.md" << 'INNER_EOF'
# Agent Skills Usage Guide

## What Are Skills?

Skills are domain expertise encoded as Markdown files that Claude Code automatically loads. When you ask a question relevant to a skill, Claude automatically applies it.

## The Three StarDance Skills

### Skill 1: 9md-framework-validator
**Purpose**: Validates CIM allocations and explains 9MD framework

**Use when**:
- "Validate this allocation"
- "What does Authenticity mean?"
- "Why is my allocation invalid?"
- "Explain the dimension interaction matrix"

### Skill 2: sbox-translation-debugger
**Purpose**: Explains and debugs SBOX parameter generation

**Use when**:
- "Why did I get cuts_per_30s: 7?"
- "Debug this pacing parameter"
- "What should saturation be for authenticity: 70?"
- "Should CTA be 'urgent' for momentum: 20?"

### Skill 3: dimension-analysis
**Purpose**: Analyzes content against 9 dimensions

**Use when**:
- "Score this TikTok against 9MD"
- "Analyze this campaign's authenticity"
- "Where is this content weak?"

## How to Trigger Skills

Skills activate automatically when relevant:

✓ GOOD: "Validate this allocation: [...]"
✓ GOOD: "Why is momentum in tension with autonomy?"
✓ GOOD: "Debug: why did I get saturation: 0.35?"

✗ BAD: "Tell me about validation"
✗ BAD: "What's SBOX?"

## Workflow Example
```
Step 1: Propose
"I want to test a flash sale TikTok"

Step 2: Get template
"What's the recommended allocation?"

Step 3: Validate
"Validate this allocation: [your values]"
→ Skill validates mathematically

Step 4: Translate (Phase 2+)
"Translate to SBOX parameters"
→ API generates 16 parameters

Step 5: Verify
"Does the pacing work for 30-second TikTok?"
→ Skill analyzes

Total time: 10 minutes
```

## Phase 1 Status
⏳ Phase 1: Write skill SKILL.md files (Days 3-7)
⏳ Phase 2: Configure MCP servers (Days 8-11)
⏳ Phase 3: Validate and test (Days 12-15)
INNER_EOF
echo -e "${GREEN}✓${NC} skills-usage-guide.md created"
echo ""

echo -e "${BLUE}[Step 5/8]${NC} Creating 9md-framework-complete.md..."
cat > "${DOCS_DIR}/9md-framework-complete.md" << 'INNER_EOF'
# 9 Dimensions of Human Conversion (9MD) - Complete Framework

**Version**: 1.0
**Source**: StarDance Knowledge Library v1
**Status**: Foundation documentation for Phase 1 skill development

## Quick Overview

The 9 Dimensions are psychological drivers that influence purchase behavior. Each dimension scores 0-100 and all 9 must sum to exactly 100 for a valid allocation.

## The Nine Dimensions

### 1. PRESENCE - Attention Capture
**Definition**: Capacity to command immediate attention and create "being here now"
**High Score** (75-100): Bold visuals, unexpected motion, direct address, immediate hook
**Low Score** (0-25): Gradual fade-in, generic footage, delayed hook

### 2. AUTHENTICITY - Genuineness
**Definition**: Perceived genuineness signaling real experience
**High Score** (75-100): UGC-style, visible imperfections, unscripted, real people
**Low Score** (0-25): Over-produced, perfect staging, actors, corporate VO

### 3. TRUST - Credibility
**Definition**: Cumulative signals reducing perceived risk
**High Score** (75-100): Visible ratings, logos, guarantees, real testimonials
**Low Score** (0-25): No proof, vague claims, hidden pricing

### 4. EMPATHY - Understanding
**Definition**: Understanding viewer's pain, situation, aspirations
**High Score** (75-100): Names pain, shows transformation, relatable, identity reflection
**Low Score** (0-25): Product-first, generic messaging, no acknowledgment

### 5. TASTE - Aesthetic Sophistication
**Definition**: Aesthetic sophistication signaling cultural alignment
**High Score** (75-100): Intentional palette, on-trend, curated music
**Low Score** (0-25): Generic stock aesthetic, dated, default music

### 6. ETHICS - Values Alignment
**Definition**: Alignment with viewer values around sustainability, responsibility
**High Score** (75-100): Certifications, diverse casting, transparency, mission-driven
**Low Score** (0-25): No values, homogeneous, profit-driven

### 7. AUTONOMY - Respect for Choice
**Definition**: Respect for viewer agency and avoidance of manipulation
**High Score** (75-100): Options presented, educational, no false urgency, easy exit
**Low Score** (0-25): Ultimatums, countdown timers, fake scarcity

### 8. MOMENTUM - Propulsive Energy
**Definition**: Propulsive energy moving viewers toward action
**High Score** (75-100): Clear specific CTA, legitimate urgency, fast pacing
**Low Score** (0-25): No CTA, meandering pacing, multiple actions

### 9. RESONANCE - Cultural Fit
**Definition**: Cultural and contextual fit making content native
**High Score** (75-100): Platform-native, current trends, shareable, community language
**Low Score** (0-25): Repurposed, dated, generic, outsider perspective

## Validation Rules

### Rule 1: Mathematical Validity
- Sum must equal exactly 100
- Each dimension must be 0-100 (inclusive)

### Rule 2: Dimension Interaction Matrix
**Synergies** (reinforce each other):
- Authenticity + Empathy
- Trust + Ethics
- Empathy + Momentum

**Tensions** (require careful balance):
- Authenticity ↔ Taste (raw vs polished)
- Trust ↔ Momentum (proof takes time, urgency requires speed)
- Presence ↔ Autonomy (demanding attention vs respecting choice)

### Rule 3: Context-Appropriateness
**DTC Conversion**: High Momentum, Trust, Presence
**Brand Awareness**: High Resonance, Taste, Presence
**UGC Style**: High Authenticity, Empathy, Resonance

## Phase 1 Task

This documentation will be used to write the **9md-framework-validator** skill in Phase 1 (Days 3-4).
INNER_EOF
echo -e "${GREEN}✓${NC} 9md-framework-complete.md created"
echo ""

echo -e "${BLUE}[Step 6/8]${NC} Creating sbox-translation-complete.md..."
cat > "${DOCS_DIR}/sbox-translation-complete.md" << 'INNER_EOF'
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
INNER_EOF
echo -e "${GREEN}✓${NC} sbox-translation-complete.md created"
echo ""

echo -e "${BLUE}[Step 7/8]${NC} Creating translation-rules-reference.md..."
cat > "${DOCS_DIR}/translation-rules-reference.md" << 'INNER_EOF'
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
INNER_EOF
echo -e "${GREEN}✓${NC} translation-rules-reference.md created"
echo ""

echo -e "${BLUE}[Step 8/8]${NC} Creating README.md..."
cat > "${CLAUDE_DIR}/README.md" << 'INNER_EOF'
# StarDance .claude Directory

## Quick Navigation

### 📚 Essential Reading
- **CLAUDE.md** - Project context and quick reference
- **PROJECT_STRUCTURE.md** - Directory layout
- **docs/skills-usage-guide.md** - How to use the 3 skills

### 📖 Reference Documentation
- **docs/9md-framework-complete.md** - 9MD framework definitions
- **docs/sbox-translation-complete.md** - SBOX translation overview
- **docs/translation-rules-reference.md** - Complete formulas and rules

## Phase Implementation
- **Phase 0**: ✅ COMPLETE (this folder)
- **Phase 1**: Create 3 skills (Days 3-7)
- **Phase 2**: Configure MCP servers (Days 8-11)
- **Phase 3**: Validate and test (Days 12-15)
- **Phase 4**: Onboarding docs (Days 16-20)
- **Phase 5**: Team launch (Day 21+)

## Quick Commands
```bash
# Start Claude Code
claude

# Check token usage
/context

# Switch to Sonnet
/model sonnet
```

## Getting Help

### Learn the framework
```bash
claude
"What are the 9 dimensions of human conversion?"
```

### Create an allocation
```bash
"What template should I use for a flash sale?"
"Validate this allocation: [values]"
```

### Debug a parameter
```bash
"Why did I get cta_strength: 'medium' for momentum: 20?"
```

## Success Criteria

Phase 0 is complete when:
- ✅ All files created
- ✅ Directory structure ready
- ✅ Documentation accurate
- ✅ Ready for Phase 1

**Current Status**: Phase 0 ✅ COMPLETE

**Next**: Phase 1 - Write the 3 skills (Days 3-7)
INNER_EOF
echo -e "${GREEN}✓${NC} README.md created"
echo ""

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    PHASE 0 SETUP COMPLETE!                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✅ Deliverables:${NC}"
echo "  ✓ Directory structure created"
echo "  ✓ PROJECT_STRUCTURE.md"
echo "  ✓ CLAUDE.md"
echo "  ✓ skills-usage-guide.md"
echo "  ✓ 9md-framework-complete.md"
echo "  ✓ sbox-translation-complete.md"
echo "  ✓ translation-rules-reference.md"
echo "  ✓ README.md"
echo ""
echo -e "${BLUE}📁 Directory created:${NC}"
ls -la .claude/
echo ""
echo -e "${BLUE}⏭️  Next Steps:${NC}"
echo "1. Start Claude Code: claude"
echo "2. Ask: 'What is the 9MD framework?'"
echo "3. Ready for Phase 1 (Days 3-7)"
echo ""
echo -e "${GREEN}Phase 0 Status: ✅ COMPLETE${NC}"
