"""
main.py
Stardance V2 - A2 System Underwriting Integration
Production FastAPI Application
"""
import os
import sys
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# A2 System Underwriting Integration
from app.a2_system_underwriting.a2_underwriting_router import router as a2_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 Stardance V2 Starting up...")
    logger.info("✅ A2 System Underwriting Module Loaded")
    yield
    logger.info("🛑 Shutting down...")

# Initialize FastAPI
app = FastAPI(
    title="Stardance V2 - Brand Intelligence API",
    description="9MD Analysis + A2 System Underwriting + Asset Orchestration",
    version="2.2.0",
    lifespan=lifespan
)

# CORS Configuration
# Adjust origins based on your frontend deployments
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://9md-frontend.vercel.app",
    "https://sbox-motion-frontend.vercel.app",
    "https://stardance.studio",
    # Add your specific Vercel deployment URLs
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include A2 System Underwriting Router
app.include_router(a2_router)
logger.info("🔒 A2 Underwriting Router mounted at /v1/a2")

@app.get("/", tags=["Health"])
async def root():
    """Root health endpoint"""
    return {
        "service": "Stardance V2 API",
        "status": "operational",
        "version": "2.2.0",
        "modules": [
            "9md_analysis",
            "a2_underwriting",
            "asset_orchestration"
        ],
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Comprehensive health check"""
    return {
        "status": "healthy",
        "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
        "services": {
            "api": "ok",
            "a2_underwriting": "loaded"
        }
    }

@app.get("/v1/a2", tags=["A2 System Underwriting"])
async def a2_info():
    """A2 System Underwriting module info"""
    return {
        "module": "A2 System Underwriting",
        "version": "1.1.0-PTC-FINAL",
        "endpoints": [
            {
                "path": "/v1/a2/underwrite",
                "method": "POST",
                "description": "Submit brand for PLA system underwriting"
            },
            {
                "path": "/v1/a2/health",
                "method": "GET", 
                "description": "A2 module health check"
            }
        ],
        "capabilities": [
            "SystemFitAggregation",
            "TransitionPenaltyCheck",
            "ConfidenceCalculation (PTC)",
            "DecisionEngine",
            "CalibrationTracking"
        ]
    }

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "global_error"}
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
