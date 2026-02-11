"""
calibration_tracker.py
A2 Calibration Tracker
Passive tracking for false positive/negative detection (Phase 3 activation)
"""
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4, UUID


@dataclass
class CalibrationEvent:
    event_id: UUID
    timestamp: datetime
    sector_id: str
    pla_system_sequence: str
    system_confidence: float
    actual_performance_percentile: Optional[float] = None
    trigger_id: Optional[str] = None
    adjustment_delta: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'event_id': str(self.event_id),
            'timestamp': self.timestamp.isoformat(),
            'sector_id': self.sector_id,
            'pla_system_sequence': self.pla_system_sequence,
            'system_confidence': self.system_confidence,
            'actual_performance_percentile': self.actual_performance_percentile,
            'trigger_id': self.trigger_id,
            'adjustment_delta': self.adjustment_delta
        }


class CalibrationTracker:
    TRIGGERS = {
        'FALSE_POSITIVE_CLUSTER': {
            'system_confidence_gt': 0.75,
            'performance_percentile_lt': 0.40,
            'count_window': 3,
            'action': 'decrease_confidence_baseline',
            'max_delta': -0.10
        },
        'FALSE_NEGATIVE_CLUSTER': {
            'system_confidence_lt': 0.55,
            'performance_percentile_gt': 0.65,
            'count_window': 3,
            'action': 'increase_confidence_baseline',
            'max_delta': 0.10
        }
    }
    
    def __init__(self):
        self.events = []
    
    def track_evaluation(self,
                        sector_id: str,
                        pla_system_sequence: str,
                        system_confidence: float) -> CalibrationEvent:
        event = CalibrationEvent(
            event_id=uuid4(),
            timestamp=datetime.now(timezone.utc),
            sector_id=sector_id,
            pla_system_sequence=pla_system_sequence,
            system_confidence=system_confidence,
            actual_performance_percentile=None,
            trigger_id=None,
            adjustment_delta=0.0
        )
        self.events.append(event)
        return event
    
    def update_performance(self, 
                          event_id: UUID, 
                          actual_performance_percentile: float) -> Optional[CalibrationEvent]:
        for event in self.events:
            if event.event_id == event_id:
                event.actual_performance_percentile = actual_performance_percentile
                trigger, delta = self._evaluate_triggers(event)
                if trigger:
                    event.trigger_id = trigger
                    event.adjustment_delta = delta
                return event
        return None
    
    def _evaluate_triggers(self, event: CalibrationEvent) -> tuple:
        if (event.system_confidence > self.TRIGGERS['FALSE_POSITIVE_CLUSTER']['system_confidence_gt'] and
            event.actual_performance_percentile < self.TRIGGERS['FALSE_POSITIVE_CLUSTER']['performance_percentile_lt']):
            return ('FALSE_POSITIVE_CLUSTER', -0.05)
        
        if (event.system_confidence < self.TRIGGERS['FALSE_NEGATIVE_CLUSTER']['system_confidence_lt'] and
            event.actual_performance_percentile > self.TRIGGERS['FALSE_NEGATIVE_CLUSTER']['performance_percentile_gt']):
            return ('FALSE_NEGATIVE_CLUSTER', 0.05)
        
        return (None, 0.0)
    
    @staticmethod
    def get_sql_schema() -> str:
        return """
CREATE TABLE IF NOT EXISTS system_confidence_calibration_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    sector_id VARCHAR(50) NOT NULL,
    pla_system_sequence VARCHAR(50) NOT NULL,
    system_confidence FLOAT NOT NULL CHECK (system_confidence >= 0 AND system_confidence <= 1),
    actual_performance_percentile FLOAT NULL CHECK (actual_performance_percentile >= 0 AND actual_performance_percentile <= 1),
    trigger_id VARCHAR(50) NULL,
    adjustment_delta FLOAT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_calibration_sector ON system_confidence_calibration_events(sector_id);
CREATE INDEX IF NOT EXISTS idx_calibration_sequence ON system_confidence_calibration_events(pla_system_sequence);
CREATE INDEX IF NOT EXISTS idx_calibration_timestamp ON system_confidence_calibration_events(timestamp);
        """.strip()
