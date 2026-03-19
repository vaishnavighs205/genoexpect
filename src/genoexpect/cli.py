from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable, Dict

from .loaders.yaml_loader import load_study_profile
from .parsers.star import parse_star_log
from .report import Report
from .step import Step

PARSERS: Dict[str, Callable[[str | Path], dict]] = {
    "star": parse_star_log,
}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="genoexpect", description="Validate genomics metrics against expected study config")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="Run checks for one step")
    check.add_argument("--study", required=True, help="Study identifier")
    check.add_argument("--config", required=True, help="Path to YAML config")
    check.add_argument("--step", required=True, help="Step name, for example alignment")
    check.add_argument("--parser", required=True, choices=sorted(PARSERS), help="Observed-metric parser")
    check.add_argument("--input", required=True, help="Path to parser input file")
    check.add_argument("--format", choices=["text", "json", "markdown"], default="text")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.command == "check":
        study = load_study_profile(args.study, args.config)
        parser_fn = PARSERS[args.parser]
        observed = parser_fn(args.input)

        step = Step(name=args.step, study=study)
        step.log_observed(observed)
        result = step.check_against_expectations()

        report = Report(study_id=study.study_id)
        report.add(result)

        if args.format == "text":
            sys.stdout.write(report.to_text() + "\n")
        elif args.format == "markdown":
            sys.stdout.write(report.to_markdown() + "\n")
        else:
            sys.stdout.write(json.dumps(report.to_dict(), indent=2) + "\n")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
