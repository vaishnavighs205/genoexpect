# genoexpect · live

A browser-based companion to [genoexpect](https://github.com/vaishnavighs205/genoexpect) that automatically fetches genomics study metadata from NCBI and generates a validated `studies.yaml` config — no manual editing required.

🔗 **[Open the tool](https://vaishnavighs205.github.io/genoexpect/genoexpect_live.html)**

---

## What it does

The original `genoexpect` package requires you to manually write a YAML study profile before you can validate QC metrics. This tool eliminates that step:

1. **Enter any SRA or BioProject accession** — it queries NCBI live
2. **Study metadata is auto-populated** — organism, genome build, assay type, library layout, read length, sample count, platform
3. **QC thresholds are inferred** from the assay type (RNA-seq, ChIP-seq, ATAC-seq, WGS, WGBS, Amplicon)
4. **Edit thresholds** directly in the browser if you want to tighten or relax them
5. **Export a ready-to-use `studies.yaml`** — paste it straight into your `genoexpect` workflow

---

## Supported accession formats

| Format | Example |
|--------|---------|
| NCBI BioProject | `PRJNA279196` |
| SRA Study | `SRP040765` |
| ENA Study | `ERP123456` |

---

## How to use

### 1. Open the tool
Open `genoexpect_live.html` in any browser — no installation, no internet connection required beyond NCBI API access.

### 2. Enter an accession
Type or paste a BioProject or SRA study accession into the search box and press **Fetch Study** or hit Enter.

### 3. Review the auto-populated profile
The tool displays:
- Study title and accession
- Organism and reference genome
- Assay type, library layout, read length
- All run accessions with read counts

### 4. Adjust thresholds (optional)
Default QC thresholds are inferred per assay type. You can edit the **Min** and **Max** values in the threshold table, then click **↻ Regenerate** to update the YAML.

### 5. Copy your `studies.yaml`
Switch to the **studies.yaml** tab and click **Copy**. Save the file, then use it with `genoexpect` as normal.

---

## Auto-inferred thresholds by assay

| Assay | Metrics |
|-------|---------|
| RNA-seq | Alignment rate, uniquely mapped rate, total reads, mRNA bases %, median CV coverage |
| ChIP-seq | Alignment rate, total reads, FRiP score, NRF |
| ATAC-seq | Alignment rate, total reads, FRiP score, TSS enrichment |
| WGS | Alignment rate, mean coverage, bases at 20x %, dedup rate |
| WGBS | Alignment rate, total reads, bisulfite conversion rate |
| Amplicon | Total reads, on-target reads % |

---

## Using the generated YAML with genoexpect

Once you have your `studies.yaml`, use it with the `genoexpect` CLI or Python API as normal.

**CLI:**
```bash
genoexpect check \
  --study PRJNA279196 \
  --config studies.yaml \
  --step alignment \
  --parser star \
  --input Log.final.out \
  --format text
```

**Python:**
```python
from genoexpect import Step, load_study_profile
from genoexpect.parsers import parse_star_log

study = load_study_profile("PRJNA279196", "studies.yaml")

step = Step(name="alignment", study=study)
step.log_observed(parse_star_log("Log.final.out"))

result = step.check_against_expectations()
print(result.summary())
```

---

## Requirements

- A modern browser (Chrome, Firefox, Safari, Edge)
- Internet access to reach the [NCBI E-utilities API](https://www.ncbi.nlm.nih.gov/books/NBK25497/)

No Python, no pip install, no setup.

---

## Notes

- Read length is estimated from total bases ÷ total spots across runs — it may differ slightly from the nominal value
- Up to 50 experiments are fetched per query; for very large studies only the first 50 are shown
- QC status for individual runs shows as **pending** until you run `genoexpect` locally with actual tool outputs

---

## License

MIT — same as the main genoexpect package.
