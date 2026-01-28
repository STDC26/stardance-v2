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
