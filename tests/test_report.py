from genoexpect.report import Report
from genoexpect.result import CheckResult, StepCheckResult


def test_report_json_contains_overall_status():
    result = StepCheckResult(
        study_id="S1",
        step_name="alignment",
        checks=[
            CheckResult(
                metric="alignment_rate",
                expected=">= 80",
                observed=90,
                status="PASS",
                message="observed 90, within expected range",
            )
        ],
    )
    report = Report(study_id="S1")
    report.add(result)

    assert '"overall_status": "PASS"' in report.to_json()
