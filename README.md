# Asklepios Validation Framework

Standardised benchmark testing for the Asklepios AI Nurse triage system,
using the Semigran-45 clinical vignettes (the same set used to benchmark
Isabel, Ada, WebMD, NHS 111, and 18 other symptom checkers).

## Quick Start

```bash
# 1. Install dependencies (already in requirements.txt)
pip install anthropic pandas openpyxl

# 2. Set your API key
export Claude_API_Key="sk-ant-..."

# 3. Dry run — see all 45 vignettes without API calls
python asklepios_validation/runner.py --dry-run

# 4. Test a single vignette first
python asklepios_validation/runner.py --vignette V01

# 5. Full validation (45 vignettes × 3 runs = 135 API calls, ~5 min)
python asklepios_validation/runner.py

# 6. Generate Markdown report
python asklepios_validation/report_generator.py
```

## What you get

| File | Contents |
|------|----------|
| `results/semigran45_TIMESTAMP.json` | Full results with per-run texts |
| `results/semigran45_TIMESTAMP_summary.csv` | One row per vignette |
| `results/VALIDATION_REPORT.md` | Publication-ready report |

## Benchmark

The 45 vignettes are from Semigran et al. BMJ 2015, reproduced in:
- Zenodo CC-BY 4.0: https://zenodo.org/records/6054093
- Schmieding et al. JMIR 2022: doi:10.2196/31810

Published triage accuracy of other symptom checkers on the same vignettes:
- Isabel Healthcare: ~84% (company claim)
- Ada Health: ~76%
- Median of 22 apps (2020): ~56%

## Safety Metric

The key metric is **undertriage rate** (unsafe errors):
cases where Asklepios assigned a LOWER urgency than the expert gold standard.
This is the clinically dangerous direction (missing an emergency).

Overtriage (assigning higher urgency) is recorded separately as "safe errors".
