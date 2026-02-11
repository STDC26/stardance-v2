"""
system_fit_aggregator.py
A2 System Fit Aggregation Engine
"""
from typing import Dict


class SystemFitAggregator:
    STAGE_WEIGHTS = {
        'image': 0.30,
        'video': 0.35,
        'landing_page': 0.35
    }
    PENALTY_CAP = 0.25
    
    def aggregate(self, 
                  image_fit: float, 
                  video_fit: float, 
                  landing_page_fit: float,
                  transition_penalty_sum: float) -> Dict[str, float]:
        self._validate_fit_score(image_fit, "image_fit")
        self._validate_fit_score(video_fit, "video_fit")
        self._validate_fit_score(landing_page_fit, "landing_page_fit")
        self._validate_penalty(transition_penalty_sum)
        
        system_fit_raw = (
            self.STAGE_WEIGHTS['image'] * image_fit +
            self.STAGE_WEIGHTS['video'] * video_fit +
            self.STAGE_WEIGHTS['landing_page'] * landing_page_fit
        )
        
        capped_penalty = min(transition_penalty_sum, self.PENALTY_CAP)
        system_fit = max(0.0, min(1.0, system_fit_raw - capped_penalty))
        
        return {
            'system_fit_raw': round(system_fit_raw, 4),
            'system_fit': round(system_fit, 4),
            'penalty_applied': round(capped_penalty, 4),
            'stage_contributions': {
                'image': round(self.STAGE_WEIGHTS['image'] * image_fit, 4),
                'video': round(self.STAGE_WEIGHTS['video'] * video_fit, 4),
                'landing_page': round(self.STAGE_WEIGHTS['landing_page'] * landing_page_fit, 4)
            }
        }
    
    def _validate_fit_score(self, score: float, name: str):
        if not 0.0 <= score <= 1.0:
            raise ValueError(f"{name} must be in [0,1], got {score}")
    
    def _validate_penalty(self, penalty: float):
        if penalty < 0:
            raise ValueError(f"Penalty sum must be >= 0, got {penalty}")
