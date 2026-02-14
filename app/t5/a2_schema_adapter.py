"""
A2SchemaAdapter — Production Boundary Layer (DTC Updated)
Maps A2 system_underwriting response → T5 canonical (TIS/GCI/CLG)
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class UnderwritingResult:
    """Canonical T5 representation."""
    tis: float                    # ← system_fit
    gci: float                    # ← system_confidence (mapped directly)
    clg: float                    # ← system_confidence (same as GCI in Phase 2)
    routing_band: str             # ← decision
    gate_pass: bool               # ← derived from decision == "AUTO_LAUNCH"
    penalty_sum: float
    calibration_event_id: Optional[str] = None
    raw_a2_response: Optional[Dict[str, Any]] = None


def map_a2_to_canonical(a2_response: dict) -> UnderwritingResult:
    """SOLE boundary function. A2 field names STOP here."""
    decision = a2_response.get("decision", "NO_LAUNCH")
    gate_pass = decision == "AUTO_LAUNCH"
    
    # GCI maps from system_confidence (not derived from gates)
    system_confidence = float(a2_response.get("system_confidence", 0.0))

    return UnderwritingResult(
        tis=float(a2_response.get("system_fit", 0.0)),
        gci=system_confidence,
        clg=system_confidence,  # Phase 2: CLG = GCI
        routing_band=decision,
        gate_pass=gate_pass,
        penalty_sum=float(a2_response.get("transition_penalty_sum", 0.0)),
        calibration_event_id=a2_response.get("calibration_event_id"),
        raw_a2_response=a2_response
    )
