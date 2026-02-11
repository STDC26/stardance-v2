"""
a2_underwriting_router.py - Production with Debug Logging
"""
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException
import logging

logger = logging.getLogger(__name__)

from .system_fit_aggregator import SystemFitAggregator
from .transition_penalty_checker import TransitionPenaltyChecker
from .system_decision_engine import SystemDecisionEngine, DecisionBand
from .calibration_tracker import CalibrationTracker
from .system_confidence_calculator import SystemConfidenceCalculator

router = APIRouter(prefix="/v1/a2", tags=["A2 System Underwriting"])

class NinePDProfile(BaseModel):
    presence: float = Field(..., ge=0.0, le=1.0)
    trust: float = Field(..., ge=0.0, le=1.0)
    authenticity: float = Field(..., ge=0.0, le=1.0)
    momentum: float = Field(..., ge=0.0, le=1.0)
    taste: float = Field(..., ge=0.0, le=1.0)
    empathy: float = Field(..., ge=0.0, le=1.0)
    autonomy: float = Field(..., ge=0.0, le=1.0)
    resonance: float = Field(..., ge=0.0, le=1.0)
    ethics: float = Field(..., ge=0.0, le=1.0)

class StageProfiles(BaseModel):
    image: NinePDProfile
    video: NinePDProfile
    landing_page: NinePDProfile

class DataSupportInput(BaseModel):
    similarity: float = Field(default=0.80, ge=0.0, le=1.0)
    sample_count: float = Field(default=0.70, ge=0.0, le=1.0)

class A2UnderwritingRequest(BaseModel):
    brand_id: str
    sector: str = Field(default="BEAUTY_SKINCARE")
    stage_profiles: StageProfiles
    stage_fits: Dict[str, float]
    stage_confidences: Dict[str, float]
    stage_gates_passed: Dict[str, bool]
    data_support: Optional[DataSupportInput] = Field(default=None)
    measurement_quality: float = Field(default=0.85, ge=0.0, le=1.0)

class ConfidenceBreakdown(BaseModel):
    stage_component: float
    data_support: float
    risk_component: float
    transition_risk: float
    measurement: float
    final_confidence: float

class A2UnderwritingResponse(BaseModel):
    brand_id: str
    decision: str
    system_fit: float
    system_fit_raw: float
    system_confidence: float
    confidence_breakdown: ConfidenceBreakdown
    transition_penalty_sum: float
    triggered_penalties: List[str]
    decision_rationale: List[str]
    calibration_event_id: Optional[str] = None

aggregator = SystemFitAggregator()
penalty_checker = TransitionPenaltyChecker()
decision_engine = SystemDecisionEngine()
calibration_tracker = CalibrationTracker()
confidence_calculator = SystemConfidenceCalculator()

@router.post("/underwrite", response_model=A2UnderwritingResponse)
async def underwrite_pla_system(request: A2UnderwritingRequest):
    logger.info(f"Processing underwriting for brand: {request.brand_id}")
    
    try:
        # Step 1: Extract profiles
        logger.debug("Step 1: Extracting profiles")
        image_9pd = request.stage_profiles.image.model_dump()
        video_9pd = request.stage_profiles.video.model_dump()
        lp_9pd = request.stage_profiles.landing_page.model_dump()
        logger.debug("Profiles extracted successfully")
        
        # Step 2: Check penalties
        logger.debug("Step 2: Checking penalties")
        penalties = penalty_checker.check_penalties(image_9pd, video_9pd, lp_9pd)
        logger.debug(f"Penalties: {penalties}")
        
        # Step 3: Calculate system fit
        logger.debug("Step 3: Calculating system fit")
        fit_result = aggregator.aggregate(
            image_fit=request.stage_fits.get('image', 0.0),
            video_fit=request.stage_fits.get('video', 0.0),
            landing_page_fit=request.stage_fits.get('landing_page', 0.0),
            transition_penalty_sum=penalties['transition_penalty_sum']
        )
        logger.debug(f"Fit result: {fit_result}")
        
        # Step 4: Aggregate profile
        aggregated_profile = {k: (image_9pd.get(k, 0.5) + video_9pd.get(k, 0.5) + lp_9pd.get(k, 0.5)) / 3 
                             for k in image_9pd.keys()}
        logger.debug(f"Aggregated profile keys: {list(aggregated_profile.keys())}")
        
        # Step 5: Handle data support
        data_support = request.data_support if request.data_support else DataSupportInput()
        logger.debug(f"Data support: similarity={data_support.similarity}, sample_count={data_support.sample_count}")
        
        # Step 6: Calculate confidence
        logger.debug("Step 6: Calculating confidence")
        confidence_result = confidence_calculator.calculate(
            stage_confidences=request.stage_confidences,
            data_support={'similarity': data_support.similarity, 'sample_count': data_support.sample_count},
            psychological_profile=aggregated_profile,
            transition_penalty_sum=penalties['transition_penalty_sum'],
            measurement_quality=request.measurement_quality
        )
        system_confidence = confidence_result['system_confidence']
        logger.debug(f"System confidence: {system_confidence}")
        
        # Step 7: Make decision
        logger.debug("Step 7: Making decision")
        decision_result = decision_engine.make_decision(
            system_fit=fit_result['system_fit'],
            system_confidence=system_confidence,
            transition_penalty_sum=penalties['transition_penalty_sum'],
            stage_gates_passed=request.stage_gates_passed
        )
        logger.debug(f"Decision: {decision_result['decision']}")
        
        # Step 8: Track calibration
        logger.debug("Step 8: Tracking calibration")
        cal_event = calibration_tracker.track_evaluation(
            sector_id=request.sector,
            pla_system_sequence="image_video_landing_page",
            system_confidence=system_confidence
        )
        logger.debug(f"Calibration event: {cal_event}")
        
        # Build response
        logger.info(f"Underwriting complete for {request.brand_id}: {decision_result['decision']}")
        
        return A2UnderwritingResponse(
            brand_id=request.brand_id,
            decision=decision_result['decision'],
            system_fit=fit_result['system_fit'],
            system_fit_raw=fit_result['system_fit_raw'],
            system_confidence=system_confidence,
            confidence_breakdown=ConfidenceBreakdown(
                stage_component=confidence_result['components']['stage_component'],
                data_support=confidence_result['components']['data_support'],
                risk_component=confidence_result['components']['risk_component'],
                transition_risk=confidence_result['components']['transition_risk'],
                measurement=confidence_result['components']['measurement'],
                final_confidence=system_confidence
            ),
            transition_penalty_sum=penalties['transition_penalty_sum'],
            triggered_penalties=penalties['triggered_penalties'],
            decision_rationale=decision_result['rationale'],
            calibration_event_id=cal_event.get('event_id') if cal_event else None
        )
        
    except Exception as e:
        logger.error(f"ERROR in underwriting: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"A2 Underwriting Error: {str(e)}")

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "component": "a2_underwriting",
        "version": "1.1.0-PTC-FINAL",
        "pydantic_version": "v2"
    }
