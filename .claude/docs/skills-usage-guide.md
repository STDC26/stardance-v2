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
