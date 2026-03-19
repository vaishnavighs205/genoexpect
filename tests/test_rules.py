from genoexpect.rules import evaluate_metric_rules


def test_min_rule_passes():
    result = evaluate_metric_rules(
        study_id="S1",
        step_name="alignment",
        expected_metrics={"alignment_rate": {"min": 80}},
        observed_metrics={"alignment_rate": 85},
    )
    assert result.overall_status == "PASS"


def test_min_rule_fails():
    result = evaluate_metric_rules(
        study_id="S1",
        step_name="alignment",
        expected_metrics={"alignment_rate": {"min": 80}},
        observed_metrics={"alignment_rate": 76},
    )
    assert result.overall_status == "FAIL"
    assert "expected >= 80" in result.checks[0].message


def test_between_rule_passes():
    result = evaluate_metric_rules(
        study_id="S1",
        step_name="alignment",
        expected_metrics={"n_reads": {"between": [20000000, 200000000]}},
        observed_metrics={"n_reads": 30000000},
    )
    assert result.overall_status == "PASS"


def test_missing_metric_warns():
    result = evaluate_metric_rules(
        study_id="S1",
        step_name="alignment",
        expected_metrics={"alignment_rate": {"min": 80}},
        observed_metrics={},
    )
    assert result.overall_status == "WARN"
    assert result.checks[0].status == "WARN"
