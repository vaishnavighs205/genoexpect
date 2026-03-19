from pathlib import Path

from genoexpect.loaders import load_study_profile


def test_load_study_profile_from_yaml():
    path = Path(__file__).parent / "fixtures" / "studies.yaml"
    study = load_study_profile("PRJNA123456", path)
    assert study.study_id == "PRJNA123456"
    assert study.organism == "homo_sapiens"
