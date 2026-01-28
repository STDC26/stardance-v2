"""
Stardance Platform - Main FastAPI Application

Phase 2.1: Video Generation Agent
- Accepts SBOX parameters
- Generates video generation instructions
- Ready for Runway integration (Phase 2.2)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.agents.video_generation.routes import router as video_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Stardance Video Generation API",
    description="Phase 2.1: Video Generation Agent - Convert SBOX parameters to Runway prompts",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(video_router)

# Root endpoint
@app.get("/", tags=["health"])
async def root():
    """Root endpoint - API info."""
    return {
        "name": "Stardance Video Generation API",
        "version": "2.0.0",
        "phase": "2.1 - Video Generation Agent",
        "status": "operational",
        "docs": "/docs",
        "endpoints": {
            "translate": "POST /agents/video/translate",
            "status": "GET /agents/status",
            "health": "GET /agents/video/health"
        }
    }

# Health check endpoint
@app.get("/health", tags=["health"])
async def health():
    """General health check."""
    return {"status": "healthy", "service": "stardance-video-generation"}

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
