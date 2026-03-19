from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(slots=True)
class Study:
    """Represents a study and its expected properties."""

    study_id: str
    organism: Optional[str] = None
    genome: Optional[str] = None
    assay_type: Optional[str] = None
    library_layout: Optional[str] = None
    read_length_nominal: Optional[int] = None
    n_samples_expected: Optional[int] = None
    defaults: Dict[str, Any] = field(default_factory=dict)
    steps: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, study_id: str, data: Dict[str, Any]) -> "Study":
        return cls(
            study_id=study_id,
            organism=data.get("organism"),
            genome=data.get("genome"),
            assay_type=data.get("assay_type"),
            library_layout=data.get("library_layout"),
            read_length_nominal=data.get("read_length_nominal"),
            n_samples_expected=data.get("n_samples_expected"),
            defaults=data.get("defaults", {}),
            steps=data.get("steps", {}),
        )

    def expected_metrics_for_step(self, step_name: str) -> Dict[str, Dict[str, Any]]:
        step = self.steps.get(step_name, {})
        return step.get("metrics", {})

    def to_dict(self) -> Dict[str, Any]:
        return {
            "study_id": self.study_id,
            "organism": self.organism,
            "genome": self.genome,
            "assay_type": self.assay_type,
            "library_layout": self.library_layout,
            "read_length_nominal": self.read_length_nominal,
            "n_samples_expected": self.n_samples_expected,
            "defaults": self.defaults,
            "steps": self.steps,
        }
