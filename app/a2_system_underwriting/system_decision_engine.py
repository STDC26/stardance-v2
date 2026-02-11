"""
system_decision_engine.py
A2 System Decision Engine
"""
from typing import Dict, List, Any
from enum import Enum


class DecisionBand(Enum):
    AUTO_LAUNCH = "AUTO_LAUNCH"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    NO_LAUNCH = "NO_LAUNCH"


class SystemDecisionEngine:
    THRESHOLDS = {
        'auto_launch': {
            'min_system_fit': 0.82,
            'min_system_confidence': 0.72,
            'max_transition_penalty': 0.08
        },
        'human_review': {
            'min_system_fit': 0.70,
            'max_system_fit': 0.82,
            'min_system_confidence': 0.50,
            'max_system_confidence': 0.72,
            'max_transition_penalty': 0.18
        },
        'no_launch': {
            'max_system_fit': 0.70,
            'max_system_confidence': 0.50,
            'max_transition_penalty': 0.18
        }
    }
    
    def make_decision(self,
                     system_fit: float,
                     system_confidence: float,
                     transition_penalty_sum: float,
                     stage_gates_passed: Dict[str, bool]) -> Dict[str, Any]:
        rationale = []
        
        no_launch_triggered = self._check_no_launch(
            system_fit, system_confidence, transition_penalty_sum, 
            stage_gates_passed, rationale
        )
        
        if no_launch_triggered:
            return {
                'decision': DecisionBand.NO_LAUNCH.value,
                'decision_rationale': rationale,
                'system_fit': system_fit,
                'system_confidence': system_confidence,
                'transition_penalty_sum': transition_penalty_sum
            }
        
        auto_launch_eligible = self._check_auto_launch(
            system_fit, system_confidence, transition_penalty_sum,
            stage_gates_passed, rationale
        )
        
        if auto_launch_eligible:
            return {
                'decision': DecisionBand.AUTO_LAUNCH.value,
                'decision_rationale': rationale,
                'system_fit': system_fit,
                'system_confidence': system_confidence,
                'transition_penalty_sum': transition_penalty_sum
            }
        
        rationale.append("System does not meet AUTO_LAUNCH thresholds and does not trigger NO_LAUNCH")
        return {
            'decision': DecisionBand.HUMAN_REVIEW.value,
            'decision_rationale': rationale,
            'system_fit': system_fit,
            'system_confidence': system_confidence,
            'transition_penalty_sum': transition_penalty_sum
        }
    
    def _check_no_launch(self, fit: float, conf: float, penalty: float,
                        gates: Dict[str, bool], rationale: List[str]) -> bool:
        triggered = False
        
        if fit < self.THRESHOLDS['no_launch']['max_system_fit']:
            rationale.append(f"system_fit {fit} < 0.70 (NO_LAUNCH threshold)")
            triggered = True
            
        if conf < self.THRESHOLDS['no_launch']['max_system_confidence']:
            rationale.append(f"system_confidence {conf} < 0.50 (NO_LAUNCH threshold)")
            triggered = True
            
        if penalty > self.THRESHOLDS['no_launch']['max_transition_penalty']:
            rationale.append(f"transition_penalty_sum {penalty} > 0.18 (NO_LAUNCH threshold)")
            triggered = True
            
        if not all(gates.values()):
            failed_stages = [k for k, v in gates.items() if not v]
            rationale.append(f"Stage gates failed for: {failed_stages}")
            triggered = True
            
        return triggered
    
    def _check_auto_launch(self, fit: float, conf: float, penalty: float,
                          gates: Dict[str, bool], rationale: List[str]) -> bool:
        checks = [
            (fit >= self.THRESHOLDS['auto_launch']['min_system_fit'], 
             f"system_fit {fit} >= 0.82"),
            (conf >= self.THRESHOLDS['auto_launch']['min_system_confidence'],
             f"system_confidence {conf} >= 0.72"),
            (penalty <= self.THRESHOLDS['auto_launch']['max_transition_penalty'],
             f"transition_penalty_sum {penalty} <= 0.08"),
            (all(gates.values()), "All stage gates passed")
        ]
        
        all_passed = all(check[0] for check in checks)
        
        if all_passed:
            rationale.append("All AUTO_LAUNCH conditions satisfied: " + 
                           ", ".join([c[1] for c in checks]))
        else:
            failed = [c[1] for c in checks if not c[0]]
            rationale.append(f"AUTO_LAUNCH conditions not met: {failed}")
            
        return all_passed
