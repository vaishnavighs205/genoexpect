from genoexpect.step import Step
from genoexpect.study import Study


def test_step_check_against_expectations():
    study = Study.from_dict(
        "S1",
        {
            "steps": {
                "alignment": {
                    "metrics": {
                        "alignment_rate": {"min": 80},
                        "n_reads": {"min": 10000000},
                    }
                }
            }
        },
    )

    step = Step(name="alignment", study=study)
    step.log_observed({"alignment_rate": 90, "n_reads": 50000000})

    result = step.check_against_expectations()
    assert result.overall_status == "PASS"
