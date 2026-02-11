"""
system_confidence_calculator.py
A2 System Confidence Calculator
Implements PTC 5-component weighted formula
"""
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class ConfidenceComponents:
    stage_component: float
    data_support: float
    risk_component: float
    transition_risk: float
    measurement: float


class SystemConfidenceCalculator:
    WEIGHTS = {
        'stage_component': 0.40,
        'data_support': 0.20,
        'risk_component': 0.20,
        'transition_risk': 0.12,
        'measurement': 0.08
    }
    
    STAGE_CONFIDENCE_WEIGHTS = {
        'image': 0.25,
        'video': 0.35,
        'landing_page': 0.40
    }
    
    def calculate(self,
                 stage_confidences: Dict[str, float],
                 data_support: Dict[str, float],
                 psychological_profile: Dict[str, float],
                 transition_penalty_sum: float,
                 measurement_quality: float = 0.85) -> Dict[str, Any]:
        stage_component = (
            self.STAGE_CONFIDENCE_WEIGHTS['image'] * stage_confidences.get('image', 0.5) +
            self.STAGE_CONFIDENCE_WEIGHTS['video'] * stage_confidences.get('video', 0.5) +
            self.STAGE_CONFIDENCE_WEIGHTS['landing_page'] * stage_confidences.get('landing_page', 0.5)
        )
        
        similarity = data_support.get('similarity', 0.7)
        sample_quality = data_support.get('sample_count', 0.7)
        data_support_score = (0.6 * similarity) + (0.4 * sample_quality)
        
        dimension_values = list(psychological_profile.values())
        if len(dimension_values) > 0:
            mean_dim = sum(dimension_values) / len(dimension_values)
            variance = sum((x - mean_dim) ** 2 for x in dimension_values) / len(dimension_values)
            risk_component = max(0.0, 1.0 - (variance * 2))
        else:
            risk_component = 0.5
        
        transition_risk = max(0.0, 1.0 - (transition_penalty_sum * 2))
        measurement_score = measurement_quality
        
        components = ConfidenceComponents(
            stage_component=stage_component,
            data_support=data_support_score,
            risk_component=risk_component,
            transition_risk=transition_risk,
            measurement=measurement_score
        )
        
        system_confidence = (
            self.WEIGHTS['stage_component'] * components.stage_component +
            self.WEIGHTS['data_support'] * components.data_support +
            self.WEIGHTS['risk_component'] * components.risk_component +
            self.WEIGHTS['transition_risk'] * components.transition_risk +
            self.WEIGHTS['measurement'] * components.measurement
        )
        
        system_confidence = max(0.0, min(1.0, system_confidence))
        
        return {
            'system_confidence': round(system_confidence, 4),
            'components': {
                'stage_component': round(components.stage_component, 4),
                'data_support': round(components.data_support, 4),
                'risk_component': round(components.risk_component, 4),
                'transition_risk': round(components.transition_risk, 4),
                'measurement': round(components.measurement, 4)
            },
            'weighted_contributions': {
                'stage_component': round(self.WEIGHTS['stage_component'] * components.stage_component, 4),
                'data_support': round(self.WEIGHTS['data_support'] * components.data_support, 4),
                'risk_component': round(self.WEIGHTS['risk_component'] * components.risk_component, 4),
                'transition_risk': round(self.WEIGHTS['transition_risk'] * components.transition_risk, 4),
                'measurement': round(self.WEIGHTS['measurement'] * components.measurement, 4)
            },
            'weights_used': self.WEIGHTS,
            'stage_confidence_weights': self.STAGE_CONFIDENCE_WEIGHTS
        }
