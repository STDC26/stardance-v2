"""
A2SchemaAdapter — Production Boundary Layer
Maps A2 system_underwriting response → T5 canonical (TIS/GCI/CLG)
Location: app/t5/ (stardance-v2 project)
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class UnderwritingResult:
    """Canonical T5 representation."""
    tis: float                    # ← system_fit
    gci: float                    # ← stage_gates_passed (derived)
    clg: float                    # ← system_confidence
    routing_band: str             # decision
    gate_pass: bool               # all gates passed
    penalty_sum: float
    calibration_event_id: Optional[str] = None
    raw_a2_response: Optional[Dict[str, Any]] = None


def map_a2_to_canonical(a2_response: dict) -> UnderwritingResult:
    """SOLE boundary function. A2 field names STOP here."""
    gates = a2_response.get("stage_gates_passed", {})
    all_gates_pass = all(gates.values()) if isinstance(gates, dict) and gates else False

    return UnderwritingResult(
        tis=float(a2_response.get("system_fit", 0.0)),
        gci=1.0 if all_gates_pass else 0.0,
        clg=float(a2_response.get("system_confidence", 0.0)),
        routing_band=a2_response.get("decision", "NO_LAUNCH"),
        gate_pass=all_gates_pass,
        penalty_sum=float(a2_response.get("transition_penalty_sum", 0.0)),
        calibration_event_id=a2_response.get("calibration_event_id"),
        raw_a2_response=a2_response
    )
