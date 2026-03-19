from genoexpect.study import Study


def test_study_from_dict_loads_fields():
    study = Study.from_dict(
        "TEST1",
        {
            "organism": "homo_sapiens",
            "genome": "GRCh38",
            "steps": {"alignment": {"metrics": {"alignment_rate": {"min": 80}}}},
        },
    )

    assert study.study_id == "TEST1"
    assert study.organism == "homo_sapiens"
    assert study.expected_metrics_for_step("alignment") == {"alignment_rate": {"min": 80}}
