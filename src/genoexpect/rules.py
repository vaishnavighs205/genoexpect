from __future__ import annotations

from typing import Any, Dict, Iterable, List

from .result import CheckResult, StepCheckResult


def _rule_to_string(rule: Dict[str, Any]) -> str:
    parts: List[str] = []
    if "min" in rule:
        parts.append(f">= {rule['min']}")
    if "max" in rule:
        parts.append(f"<= {rule['max']}")
    if "eq" in rule:
        parts.append(f"== {rule['eq']}")
    if "between" in rule:
        low, high = rule["between"]
        parts.append(f"between {low} and {high}")
    return ", ".join(parts) if parts else str(rule)


def _normalize_iterable(value: Any) -> Iterable[Any]:
    if isinstance(value, (list, tuple, set)):
        return value
    return [value]


def evaluate_metric_rules(
    study_id: str,
    step_name: str,
    expected_metrics: Dict[str, Dict[str, Any]],
    observed_metrics: Dict[str, Any],
) -> StepCheckResult:
    checks: List[CheckResult] = []

    for metric, rule in expected_metrics.items():
        observed = observed_metrics.get(metric)
        expected_str = _rule_to_string(rule)

        if observed is None:
            checks.append(
                CheckResult(
                    metric=metric,
                    expected=expected_str,
                    observed=None,
                    status="WARN",
                    message="metric missing in observed results",
                )
            )
            continue

        status = "PASS"
        messages: List[str] = []

        if "min" in rule and observed < rule["min"]:
            status = "FAIL"
            messages.append(f"expected >= {rule['min']}, observed {observed}")

        if "max" in rule and observed > rule["max"]:
            status = "FAIL"
            messages.append(f"expected <= {rule['max']}, observed {observed}")

        if "eq" in rule and observed != rule["eq"]:
            status = "FAIL"
            messages.append(f"expected == {rule['eq']}, observed {observed}")

        if "between" in rule:
            low, high = rule["between"]
            if not (low <= observed <= high):
                status = "FAIL"
                messages.append(f"expected between {low} and {high}, observed {observed}")

        if "in" in rule:
            allowed = list(_normalize_iterable(rule["in"]))
            if observed not in allowed:
                status = "FAIL"
                messages.append(f"expected one of {allowed}, observed {observed}")

        if not messages:
            messages.append(f"observed {observed}, within expected range")

        checks.append(
            CheckResult(
                metric=metric,
                expected=expected_str,
                observed=observed,
                status=status,
                message="; ".join(messages),
            )
        )

    for metric in sorted(set(observed_metrics) - set(expected_metrics)):
        checks.append(
            CheckResult(
                metric=metric,
                expected="no explicit expectation",
                observed=observed_metrics[metric],
                status="WARN",
                message="observed metric has no configured expectation",
            )
        )

    return StepCheckResult(study_id=study_id, step_name=step_name, checks=checks)
