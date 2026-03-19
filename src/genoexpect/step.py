from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .result import StepCheckResult
from .rules import evaluate_metric_rules
from .study import Study


@dataclass(slots=True)
class Step:
    """Represents a pipeline step and observed metrics for a study."""

    name: str
    study: Study
    observed_metrics: Dict[str, Any] = field(default_factory=dict)
    sample_id: Optional[str] = None

    def log_observed(self, metrics: Dict[str, Any]) -> None:
        self.observed_metrics.update(metrics)

    def check_against_expectations(self) -> StepCheckResult:
        expected = self.study.expected_metrics_for_step(self.name)
        return evaluate_metric_rules(
            study_id=self.study.study_id,
            step_name=self.name,
            expected_metrics=expected,
            observed_metrics=self.observed_metrics,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "study_id": self.study.study_id,
            "sample_id": self.sample_id,
            "observed_metrics": dict(self.observed_metrics),
        }
