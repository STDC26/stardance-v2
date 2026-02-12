"""
Debug endpoint to isolate module failures
"""
import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "debug"}

@app.post("/v1/a2/underwrite")
async def debug_underwrite():
    """Debug version with full error exposure"""
    try:
        logger.info("Starting import test...")
        
        # Test each import
        logger.info("Importing SystemFitAggregator...")
        from app.a2_system_underwriting.system_fit_aggregator import SystemFitAggregator
        agg = SystemFitAggregator()
        logger.info("✅ Aggregator imported")
        
        logger.info("Importing TransitionPenaltyChecker...")
        from app.a2_system_underwriting.transition_penalty_checker import TransitionPenaltyChecker
        pen = TransitionPenaltyChecker()
        logger.info("✅ Penalty checker imported")
        
        logger.info("Importing SystemDecisionEngine...")
        from app.a2_system_underwriting.system_decision_engine import SystemDecisionEngine
        dec = SystemDecisionEngine()
        logger.info("✅ Decision engine imported")
        
        logger.info("Importing CalibrationTracker...")
        from app.a2_system_underwriting.calibration_tracker import CalibrationTracker
        cal = CalibrationTracker()
        logger.info("✅ Calibration tracker imported")
        
        logger.info("Importing SystemConfidenceCalculator...")
        from app.a2_system_underwriting.system_confidence_calculator import SystemConfidenceCalculator
        conf = SystemConfidenceCalculator()
        logger.info("✅ Confidence calculator imported")
        
        # Test method calls with dummy data
        logger.info("Testing aggregator.aggregate...")
        fit_result = agg.aggregate(
            image_fit=0.8, video_fit=0.8, landing_page_fit=0.8, transition_penalty_sum=0.0
        )
        logger.info(f"Fit result: {fit_result}")
        
        return {
            "status": "success",
            "modules_loaded": 5,
            "fit_result": fit_result,
            "message": "All modules working"
        }
        
    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
