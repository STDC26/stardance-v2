import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.a2_system_underwriting.a2_underwriting_router import router as a2_router
from app.api.routes.hub_routes import router as hub_router
from app.api.routes.asset_routes import router as asset_router

app = FastAPI(title="Stardance V2", version="2.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(a2_router)
app.include_router(asset_router)
logger.info("📊 Asset Scorer mounted at /v1/asset")
logger.info("🔒 A2 Router mounted at /v1/a2")

app.include_router(hub_router)
logger.info("🔗 Hub Router mounted at /v1/hub")

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

@app.on_event("startup")
async def run_migrations():
    """Idempotent — safe to run on every startup. Uses asyncpg directly."""
    import os, asyncio
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        logger.warning("DATABASE_URL not set — skipping migrations")
        return
    # asyncpg requires postgresql:// not postgres://
    asyncpg_url = database_url.replace("postgres://", "postgresql://").split("?")[0]
    for attempt in range(5):
        try:
            import asyncpg
            conn = await asyncpg.connect(asyncpg_url, ssl=False)
            await conn.execute("""
                ALTER TABLE calibrations 
                  ADD COLUMN IF NOT EXISTS asset_id VARCHAR(255),
                  ADD COLUMN IF NOT EXISTS asset_scoring_json JSONB,
                  ADD COLUMN IF NOT EXISTS asset_scoring_version VARCHAR(50)
            """)
            await conn.close()
            logger.info("✅ Migrations complete — asset scoring columns confirmed")
            return
        except Exception as e:
            logger.warning(f"Migration attempt {attempt+1}/5 failed: {e}")
            await asyncio.sleep(3)
    logger.error("❌ Migration failed after 5 attempts")
