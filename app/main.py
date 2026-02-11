import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.a2_system_underwriting.a2_underwriting_router import router as a2_router

app = FastAPI(title="Stardance V2", version="2.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(a2_router)
logger.info("🔒 A2 Router mounted at /v1/a2")

@app.get("/")
async def root():
    return {"status": "operational", "a2_underwriting": "active"}

@app.get("/health")
async def health():
    return {"status": "healthy", "a2": "loaded"}

if __name__ == "__main__":
    import uvicorn
    # CRITICAL: Must use Railway's PORT env var
    port = int(os.environ.get("PORT", "8080"))
    host = "0.0.0.0"
    logger.info(f"🚀 Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
