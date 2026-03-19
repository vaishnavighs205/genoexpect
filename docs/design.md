# genoexpect design notes

## Core model

- `Study`: expected study properties and per-step metric rules
- `Step`: observed metrics for a named processing step
- `rules`: generic rule evaluation layer
- `Report`: multi-step aggregation and export

## v0.1 principles

- study-driven configuration first
- parser outputs must normalize metric names
- rule engine stays small and explicit
- output should be simple enough for CI and pipelines

## Planned extensions

- sample-level results
- batch comparison across all samples in a study
- accession metadata enrichment hooks
- richer assay templates
