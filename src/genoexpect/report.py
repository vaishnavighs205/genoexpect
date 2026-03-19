from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Dict, List

from .result import StepCheckResult


@dataclass(slots=True)
class Report:
    """Collects multiple step check results into one report."""

    study_id: str
    results: List[StepCheckResult] = field(default_factory=list)

    def add(self, result: StepCheckResult) -> None:
        self.results.append(result)

    @property
    def overall_status(self) -> str:
        statuses = {result.overall_status for result in self.results}
        if "FAIL" in statuses:
            return "FAIL"
        if "WARN" in statuses:
            return "WARN"
        return "PASS"

    def to_dict(self) -> Dict[str, object]:
        return {
            "study_id": self.study_id,
            "overall_status": self.overall_status,
            "steps": [result.to_dict() for result in self.results],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_markdown(self) -> str:
        lines = [f"# genoexpect report: {self.study_id}", "", f"Overall status: **{self.overall_status}**", ""]
        for result in self.results:
            lines.append(f"## Step: {result.step_name}")
            lines.append("")
            lines.append("| Metric | Expected | Observed | Status | Message |")
            lines.append("|---|---|---:|---|---|")
            for check in result.checks:
                lines.append(
                    f"| {check.metric} | {check.expected} | {check.observed} | {check.status} | {check.message} |"
                )
            lines.append("")
        return "\n".join(lines)

    def to_text(self) -> str:
        lines = [f"{self.study_id} :: {self.overall_status}"]
        for result in self.results:
            lines.append(result.summary())
        return "\n\n".join(lines)
