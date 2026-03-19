from pathlib import Path

from genoexpect.parsers import parse_star_log


def test_parse_star_log_extracts_metrics():
    path = Path(__file__).parent / "fixtures" / "star_Log.final.out"
    metrics = parse_star_log(path)

    assert metrics["n_reads"] == 41234567
    assert metrics["uniquely_mapped_rate"] == 82.5
    assert metrics["multi_mapped_rate"] == 4.2
    assert metrics["alignment_rate"] == 87.5
