# genoexpect

`genoexpect` is a Python package for validating observed genomics QC and processing metrics against expected study metadata and assay-specific thresholds.

## Why it exists

Pipelines produce metrics, but they usually do not know what was expected for a given study. This package bridges that gap:

- load a study profile by `study_id`
- parse observed metrics from tool outputs
- compare observed values with expected thresholds
- produce clear `PASS` / `WARN` / `FAIL` results

## Current v0.1 scope

- YAML-based study profiles
- study-level metadata and step-level metric expectations
- reusable rule engine (`min`, `max`, `eq`, `between`)
- step checking with text, markdown, and JSON summaries
- STAR `Log.final.out` parser
- small CLI

## Repository layout

```text
src/genoexpect/
  study.py
  step.py
  rules.py
  result.py
  report.py
  cli.py
  loaders/yaml_loader.py
  parsers/star.py
```

## Installation

```bash
pip install -e .
```

For tests:

```bash
pip install -e .[dev]
pytest
```

## Example study config

```yaml
studies:
  PRJNA123456:
    organism: homo_sapiens
    genome: GRCh38
    assay_type: rna_seq
    library_layout: paired
    read_length_nominal: 150
    n_samples_expected: 24

    steps:
      alignment:
        metrics:
          alignment_rate:
            min: 80.0
          uniquely_mapped_rate:
            min: 70.0
          n_reads:
            min: 30000000
```

## Python usage

```python
from genoexpect import Step, load_study_profile
from genoexpect.parsers import parse_star_log

study = load_study_profile("PRJNA123456", "examples/studies.yaml")

step = Step(name="alignment", study=study)
step.log_observed(parse_star_log("tests/fixtures/star_Log.final.out"))

result = step.check_against_expectations()
print(result.summary())
```

## CLI usage

```bash
genoexpect check \
  --study PRJNA123456 \
  --config examples/studies.yaml \
  --step alignment \
  --parser star \
  --input tests/fixtures/star_Log.final.out \
  --format text
```

## Supported rules

For each metric you can define:

- `min`
- `max`
- `eq`
- `between: [low, high]`

Example:

```yaml
alignment_rate:
  min: 80.0
n_reads:
  between: [20000000, 200000000]
```

## Roadmap

- FastQC parser
- featureCounts parser
- sample-level aggregation
- accession metadata enrichment hooks for GEO/SRA/ENA
- HTML reporting
