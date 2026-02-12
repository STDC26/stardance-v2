"""
a2_underwriting_router.py - Production Fix v3
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

def safe_get_event_id(cal_event):
    """Safely extract event_id from object, dict, or UUID"""
    if cal_event is None:
        return None
    if isinstance(cal_event, dict):
        event_id = cal_event.get('event_id')
    else:
        event_id = getattr(cal_event, 'event_id', None)
    
    # Convert UUID to string if needed
    if event_id is not None:
        return str(event_id)
    return None

def extract_penalty_names(penalties_list):
    """Convert PenaltyResult objects or dicts to penalty name strings"""
    if not penalties_list:
        return []
    
    result = []
    for p in penalties_list:
        if isinstance(p, str):
            result.append(p)
        elif isinstance(p, dict):
            result.append(p.get('penalty_name', p.get('id', 'unknown')))
        else:
            # Object - try common attributes
            name = getattr(p, 'penalty_name', None) or getattr(p, 'id', None) or getattr(p, 'name', 'unknown')
            result.append(str(name))
    return result

@router.post("/underwrite", response_model=A2UnderwritingResponse)
async def underwrite_pla_system(request: A2UnderwritingRequest):
    logger.info(f"Processing underwriting for brand: {request.brand_id}")
    
    try:
        # Extract profiles
        image_9pd = request.stage_profiles.image.model_dump()
        video_9pd = request.stage_profiles.video.model_dump()
        lp_9pd = request.stage_profiles.landing_page.model_dump()
        
        # Check penalties
        penalties = penalty_checker.check_penalties(image_9pd, video_9pd, lp_9pd)
        
        # Calculate system fit
        fit_result = aggregator.aggregate(
            image_fit=request.stage_fits.get('image', 0.0),
            video_fit=request.stage_fits.get('video', 0.0),
            landing_page_fit=request.stage_fits.get('landing_page', 0.0),
            transition_penalty_sum=penalties['transition_penalty_sum']
        )
        
        # Aggregate profile
        aggregated_profile = {k: (image_9pd.get(k, 0.5) + video_9pd.get(k, 0.5) + lp_9pd.get(k, 0.5)) / 3 
                             for k in image_9pd.keys()}
        
        # Handle data support
        data_support = request.data_support if request.data_support else DataSupportInput()
        
        # Calculate confidence
        confidence_result = confidence_calculator.calculate(
            stage_confidences=request.stage_confidences,
            data_support={'similarity': data_support.similarity, 'sample_count': data_support.sample_count},
            psychological_profile=aggregated_profile,
            transition_penalty_sum=penalties['transition_penalty_sum'],
            measurement_quality=request.measurement_quality
        )
        system_confidence = confidence_result['system_confidence']
        
        # Make decision
        decision_result = decision_engine.make_decision(
            system_fit=fit_result['system_fit'],
            system_confidence=system_confidence,
            transition_penalty_sum=penalties['transition_penalty_sum'],
            stage_gates_passed=request.stage_gates_passed
        )
        
        # Handle missing rationale gracefully
        rationale = decision_result.get('rationale', [f"Decision: {decision_result.get('decision', 'UNKNOWN')}"])
        
        # Track calibration
        cal_event = calibration_tracker.track_evaluation(
            sector_id=request.sector,
            pla_system_sequence="image_video_landing_page",
            system_confidence=system_confidence
        )
        
        # Safely extract event_id and convert to string
        cal_event_id = safe_get_event_id(cal_event)
        
        # Extract penalty names as strings
        penalty_names = extract_penalty_names(penalties.get('triggered_penalties', []))
        
        logger.info(f"Underwriting complete for {request.brand_id}: {decision_result.get('decision')}")
        
        return A2UnderwritingResponse(
            brand_id=request.brand_id,
            decision=decision_result.get('decision', 'ERROR'),
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
            triggered_penalties=penalty_names,
            decision_rationale=rationale,
            calibration_event_id=cal_event_id
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
