from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class CheckResult:
    metric: str
    expected: str
    observed: Optional[Any]
    status: str
    message: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric": self.metric,
            "expected": self.expected,
            "observed": self.observed,
            "status": self.status,
            "message": self.message,
        }


@dataclass(slots=True)
class StepCheckResult:
    study_id: str
    step_name: str
    checks: List[CheckResult] = field(default_factory=list)

    @property
    def overall_status(self) -> str:
        statuses = {check.status for check in self.checks}
        if "FAIL" in statuses:
            return "FAIL"
        if "WARN" in statuses:
            return "WARN"
        return "PASS"

    def summary(self) -> str:
        lines = [f"{self.study_id} :: {self.step_name} :: {self.overall_status}"]
        for check in self.checks:
            lines.append(f"- {check.metric}: {check.message} [{check.status}]")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "study_id": self.study_id,
            "step_name": self.step_name,
            "overall_status": self.overall_status,
            "checks": [check.to_dict() for check in self.checks],
        }
