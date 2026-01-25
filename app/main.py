"""
StarDance Platform v2.0 - Multi-Agent Architecture
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health & Status Endpoints
@app.get("/")
async def root():
    return {
        "service": "StarDance Platform v2.0",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "healthy",
        "phase_2_features": {
            "video_generation": settings.ENABLE_VIDEO_GENERATION,
            "distribution": settings.ENABLE_DISTRIBUTION,
            "attribution": settings.ENABLE_ATTRIBUTION,
            "learning": settings.ENABLE_LEARNING,
            "regeneration": settings.ENABLE_REGENERATION,
        },
        "message": "Multi-agent platform - Phase 2 development"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }

# Agent Status Endpoint
@app.get("/agents/status")
async def agents_status():
    return {
        "agents": {
            "cim": "ready",
            "sbox": "ready",
            "video_generation": "building" if settings.ENABLE_VIDEO_GENERATION else "disabled",
            "distribution": "building" if settings.ENABLE_DISTRIBUTION else "disabled",
            "attribution": "building" if settings.ENABLE_ATTRIBUTION else "disabled",
            "learning": "building" if settings.ENABLE_LEARNING else "disabled",
            "regeneration": "building" if settings.ENABLE_REGENERATION else "disabled",
        }
    }
