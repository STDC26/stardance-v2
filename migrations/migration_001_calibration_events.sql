-- A2 System Underwriting Database Migration
-- Migration: 001_calibration_events
-- Gate 2 Approved: 2026-02-11

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

CREATE INDEX IF NOT EXISTS idx_calibration_sector 
    ON system_confidence_calibration_events(sector_id);

CREATE INDEX IF NOT EXISTS idx_calibration_sequence 
    ON system_confidence_calibration_events(pla_system_sequence);

CREATE INDEX IF NOT EXISTS idx_calibration_timestamp 
    ON system_confidence_calibration_events(timestamp);

CREATE INDEX IF NOT EXISTS idx_calibration_trigger 
    ON system_confidence_calibration_events(trigger_id) 
    WHERE trigger_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_calibration_awaiting_performance
    ON system_confidence_calibration_events(event_id)
    WHERE actual_performance_percentile IS NULL;

COMMENT ON TABLE system_confidence_calibration_events IS 
    'Tracks system confidence vs actual performance for Phase 3 calibration.';
