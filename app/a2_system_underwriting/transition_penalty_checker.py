"""
transition_penalty_checker.py
A2 Transition Penalty Checker
"""
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum


class PenaltyID(Enum):
    IMG_VID_TRUST_DROP = "IMG_VID_TRUST_DROP"
    IMG_VID_MOMENTUM_SPIKE = "IMG_VID_MOMENTUM_SPIKE"
    VID_LP_TRUST_INSUFFICIENT_LIFT = "VID_LP_TRUST_INSUFFICIENT_LIFT"
    VID_LP_AUTONOMY_DROP = "VID_LP_AUTONOMY_DROP"
    VID_LP_MOMENTUM_NO_TAPER = "VID_LP_MOMENTUM_NO_TAPER"


@dataclass
class PenaltyResult:
    id: str
    transition: str
    dimension: str
    triggered: bool
    delta: float
    penalty_value: float
    rationale: str


class TransitionPenaltyChecker:
    PENALTY_RULES = [
        {
            'id': PenaltyID.IMG_VID_TRUST_DROP,
            'transition': 'image_to_video',
            'dimension': 'trust',
            'check': lambda v, i: v - i < -0.10,
            'penalty': 0.10,
            'rationale': 'Trust regression after attention capture predicts shallow engagement'
        },
        {
            'id': PenaltyID.IMG_VID_MOMENTUM_SPIKE,
            'transition': 'image_to_video',
            'dimension': 'momentum',
            'check': lambda v, i: v - i > 0.20,
            'penalty': 0.06,
            'rationale': 'Early urgency escalation increases reactance before value formation'
        },
        {
            'id': PenaltyID.VID_LP_TRUST_INSUFFICIENT_LIFT,
            'transition': 'video_to_landing_page',
            'dimension': 'trust',
            'check': lambda lp, v: lp - v < 0.10,
            'penalty': 0.08,
            'rationale': 'LP must materially increase trust to resolve risk'
        },
        {
            'id': PenaltyID.VID_LP_AUTONOMY_DROP,
            'transition': 'video_to_landing_page',
            'dimension': 'autonomy',
            'check': lambda lp, v: lp - v < -0.10,
            'penalty': 0.07,
            'rationale': 'Coercive LP following persuasive video triggers reactance'
        },
        {
            'id': PenaltyID.VID_LP_MOMENTUM_NO_TAPER,
            'transition': 'video_to_landing_page',
            'dimension': 'momentum',
            'check': lambda lp, v: lp - v > 0.00,
            'penalty': 0.06,
            'rationale': 'Failure to taper urgency undermines decision confidence'
        }
    ]
    
    def check_penalties(self, 
                       image_9pd: Dict[str, float],
                       video_9pd: Dict[str, float],
                       landing_page_9pd: Dict[str, float]) -> Dict[str, Any]:
        results = []
        total_penalty = 0.0
        
        for rule in self.PENALTY_RULES:
            if rule['transition'] == 'image_to_video':
                from_val = image_9pd.get(rule['dimension'], 0.5)
                to_val = video_9pd.get(rule['dimension'], 0.5)
            else:
                from_val = video_9pd.get(rule['dimension'], 0.5)
                to_val = landing_page_9pd.get(rule['dimension'], 0.5)
            
            delta = to_val - from_val
            triggered = rule['check'](to_val, from_val)
            penalty = rule['penalty'] if triggered else 0.0
            
            result = PenaltyResult(
                id=rule['id'].value,
                transition=rule['transition'],
                dimension=rule['dimension'],
                triggered=triggered,
                delta=round(delta, 4),
                penalty_value=penalty,
                rationale=rule['rationale']
            )
            results.append(result)
            total_penalty += penalty
        
        return {
            'transition_penalty_sum': round(total_penalty, 4),
            'triggered_penalties': [r for r in results if r.triggered],
            'all_checks': [
                {
                    'id': r.id,
                    'transition': r.transition,
                    'dimension': r.dimension,
                    'triggered': r.triggered,
                    'delta': r.delta,
                    'penalty_value': r.penalty_value,
                    'rationale': r.rationale
                } for r in results
            ]
        }
