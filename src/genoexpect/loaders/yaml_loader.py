from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

from ..exceptions import InvalidConfigError, StudyNotFoundError
from ..study import Study


def load_study_profile(study_id: str, config_path: str | Path) -> Study:
    """Load a study profile by id from a YAML config file."""

    path = Path(config_path)
    with path.open("r", encoding="utf-8") as handle:
        raw: Dict[str, Any] = yaml.safe_load(handle) or {}

    studies = raw.get("studies")
    if studies is None:
        raise InvalidConfigError("YAML config must contain a top-level 'studies' mapping")

    if study_id not in studies:
        raise StudyNotFoundError(f"Study '{study_id}' not found in {path}")

    data = studies[study_id]
    if not isinstance(data, dict):
        raise InvalidConfigError(f"Study '{study_id}' must map to a dictionary")

    return Study.from_dict(study_id, data)
