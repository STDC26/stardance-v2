# StarDance Platform v2.0

Multi-agent AI platform for intelligent content creation, distribution, and optimization.

## Architecture

Phase 2 introduces a complete multi-agent system:

- **CIM Agent**: Content Intelligence Matrix (9-dimensional psychological allocation)
- **SBOX Agent**: Translation engine (psychology → creative parameters)
- **Video Generation Agent**: AI-powered video creation (Runway, Pika, Stability AI)
- **Distribution Agent**: Multi-platform publishing (TikTok, Instagram, YouTube)
- **Attribution Agent**: Performance data collection and analysis
- **Learning Agent**: Correlation engine and pattern recognition
- **Regeneration Agent**: Intelligent content optimization based on performance

## Development Status

- **Version**: 2.0.0-dev
- **Phase**: Active Development
- **Production MVP**: Separate repo (stardance-mvp)

## Setup
```bash
# Install dependencies
pip install -r requirements.txt --break-system-packages

# Run development server
uvicorn app.main:app --reload

# Run tests
pytest tests/
```

## Deployment

- **Development**: Railway (stardance-v2-dev)
- **Production MVP**: Separate Railway service (unchanged)

## Architecture Docs

See `/docs` folder for detailed architecture diagrams and agent specifications.
# T5 Deploy Thu Feb 12 18:54:26 MST 2026
