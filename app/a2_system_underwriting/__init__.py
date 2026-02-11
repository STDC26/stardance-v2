"""
A2 System Underwriting Package v1.1.0-PTC-FINAL
Option A2: Beauty PLA Systems (Image→Video→Landing Page)
"""

from .system_fit_aggregator import SystemFitAggregator
from .transition_penalty_checker import TransitionPenaltyChecker
from .system_decision_engine import SystemDecisionEngine, DecisionBand
from .calibration_tracker import CalibrationTracker
from .system_confidence_calculator import SystemConfidenceCalculator

__version__ = "1.1.0-PTC-FINAL"
__all__ = [
    'SystemFitAggregator',
    'TransitionPenaltyChecker',
    'SystemDecisionEngine',
    'DecisionBand',
    'CalibrationTracker',
    'SystemConfidenceCalculator'
]
