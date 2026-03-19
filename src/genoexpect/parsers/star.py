from __future__ import annotations

from pathlib import Path
from typing import Dict


_KEY_TO_METRIC = {
    "Number of input reads": ("n_reads", int),
    "Average input read length": ("average_input_read_length", float),
    "Uniquely mapped reads number": ("uniquely_mapped_reads", int),
    "Uniquely mapped reads %": ("uniquely_mapped_rate", float),
    "% of reads mapped to multiple loci": ("multi_mapped_rate", float),
    "% of reads mapped to too many loci": ("too_many_loci_rate", float),
    "% of reads unmapped: too many mismatches": ("pct_unmapped_mismatches", float),
    "% of reads unmapped: too short": ("pct_unmapped_too_short", float),
    "% of reads unmapped: other": ("pct_unmapped_other", float),
}


def _coerce_number(value: str, cast):
    cleaned = value.strip().replace(",", "").replace("%", "")
    return cast(cleaned)


def parse_star_log(path: str | Path) -> Dict[str, float | int]:
    """Parse STAR Log.final.out into normalized metric names."""

    metrics: Dict[str, float | int] = {}

    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            if "|" not in line:
                continue
            key, value = [part.strip() for part in line.split("|", 1)]
            if key not in _KEY_TO_METRIC:
                continue
            metric_name, caster = _KEY_TO_METRIC[key]
            metrics[metric_name] = _coerce_number(value, caster)

    total_alignment = 0.0
    for component in ("uniquely_mapped_rate", "multi_mapped_rate", "too_many_loci_rate"):
        if component in metrics:
            total_alignment += float(metrics[component])
    if total_alignment:
        metrics["alignment_rate"] = round(total_alignment, 2)

    return metrics
