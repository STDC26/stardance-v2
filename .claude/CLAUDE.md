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
