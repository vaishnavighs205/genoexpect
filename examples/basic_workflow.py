from pathlib import Path

from genoexpect import Step, load_study_profile
from genoexpect.parsers import parse_star_log

repo_root = Path(__file__).resolve().parents[1]

study = load_study_profile("PRJNA123456", repo_root / "examples" / "studies.yaml")
step = Step(name="alignment", study=study)
step.log_observed(parse_star_log(repo_root / "tests" / "fixtures" / "star_Log.final.out"))

result = step.check_against_expectations()
print(result.summary())
