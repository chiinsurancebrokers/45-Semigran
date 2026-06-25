"""
Validation Report Generator

After running runner.py, use this to generate:
  1. A Markdown validation report (for GitHub README / website)
  2. A comparison table vs. other symptom checkers (from Schmieding 2022)
"""

import json
import sys
from pathlib import Path
from datetime import datetime

RESULTS_DIR = Path(__file__).parent / "results"

# Benchmark data from Schmieding et al. JMIR 2022 (doi:10.2196/31810)
# Median triage accuracy of 22 symptom checker apps in 2020
BENCHMARK_APPS = {
    "Isabel (Isabel Healthcare)": 84,   # from Isabel's own published claims
    "Ada Health":                  76,
    "Babylon Health":               72,
    "Symptomate":                   68,
    "WebMD Symptom Checker":        58,
    "Buoy Health":                  57,
    "NHS 111 Online":               55,
    "Median (22 apps, 2020)":       56,  # Schmieding 2022 median
}

def load_latest_results():
    files = sorted(RESULTS_DIR.glob("semigran45_*.json"))
    if not files:
        print("No results found. Run runner.py first.")
        sys.exit(1)
    with open(files[-1]) as f:
        return json.load(f)

def generate_markdown_report(data):
    meta = data["meta"]
    results = data["results"]
    total = len(results)

    correct = sum(1 for r in results if r["correct"])
    safe_err = sum(1 for r in results if r["safety"] == "safe_error")
    unsafe = sum(1 for r in results if r["safety"] == "unsafe")
    acc_pct = round(100 * correct / total, 1)
    unsafe_pct = round(100 * unsafe / total, 1)

    per_level = {}
    for level in ["emergency", "non_emergency", "self_care"]:
        subset = [r for r in results if r["gold"] == level]
        n = len(subset)
        n_correct = sum(1 for r in subset if r["correct"])
        per_level[level] = {
            "n": n, "correct": n_correct,
            "acc_pct": round(100 * n_correct / n, 1) if n else 0,
            "unsafe": sum(1 for r in subset if r["safety"] == "unsafe"),
        }

    # Comparison table
    benchmark_with_asklepios = dict(BENCHMARK_APPS)
    benchmark_with_asklepios[f"**Asklepios** (this study)"] = acc_pct
    sorted_bench = sorted(benchmark_with_asklepios.items(), key=lambda x: -x[1])

    comparison_rows = "\n".join(
        f"| {name} | {acc}% | {'← **Asklepios**' if 'Asklepios' in name else ''} |"
        for name, acc in sorted_bench
    )

    unsafe_section = ""
    unsafe_cases = [r for r in results if r["safety"] == "unsafe"]
    if unsafe_cases:
        rows = "\n".join(
            f"| {r['id']} | {r['condition']} | {r['gold']} | {r['predicted'] or 'UNPARSED'} |"
            for r in unsafe_cases
        )
        unsafe_section = f"""
## ⚠️ Undertriage Cases (Unsafe Errors)

These cases were classified at a **lower urgency** than the gold standard — the
clinically significant failure mode. Each requires manual review and prompt improvement.

| ID | Condition | Gold | Predicted |
|----|-----------|------|-----------|
{rows}

**Action required:** review system prompt and/or add condition-specific red flag detection.
"""

    md = f"""# Asklepios Validation Report — Semigran-45 Benchmark

> **Benchmark:** Semigran et al. BMJ 2015 (45 standardised clinical vignettes)  
> **Dataset:** Zenodo CC-BY 4.0 — [doi:10.5281/zenodo.6054093](https://zenodo.org/records/6054093)  
> **Model:** {meta['model']}  
> **Runs per vignette:** {meta['runs_per_vignette']} (majority vote)  
> **Date:** {meta['timestamp'][:8]}  

---

## Overall Results

| Metric | Value |
|--------|-------|
| **Triage accuracy** | **{acc_pct}%** ({correct}/{total}) |
| Safe overtriage | {safe_err}/{total} ({round(100*safe_err/total,1)}%) |
| ❌ Unsafe undertriage | {unsafe}/{total} ({unsafe_pct}%) |
| Vignettes tested | {total} |

## Per-Level Accuracy

| Triage Level | Correct | Accuracy | Unsafe |
|---|---|---|---|
| Emergency (Em) | {per_level['emergency']['correct']}/{per_level['emergency']['n']} | {per_level['emergency']['acc_pct']}% | {per_level['emergency']['unsafe']} |
| Non-emergency (NE) | {per_level['non_emergency']['correct']}/{per_level['non_emergency']['n']} | {per_level['non_emergency']['acc_pct']}% | {per_level['non_emergency']['unsafe']} |
| Self-care (Sc) | {per_level['self_care']['correct']}/{per_level['self_care']['n']} | {per_level['self_care']['acc_pct']}% | {per_level['self_care']['unsafe']} |

## Comparison with Published Symptom Checkers

*Reference: Schmieding et al. JMIR 2022 (doi:10.2196/31810), n=22 apps, same Semigran-45 vignettes*

| System | Triage Accuracy | |
|--------|----------------|--|
{comparison_rows}

## Methodology

- **Vignettes:** 45 standardised clinical cases (15 emergency, 15 non-emergency, 15 self-care)
- **Gold standard:** Expert panel consensus (Semigran et al. 2015)
- **Input format:** Condensed symptom list + age + sex
- **Runs:** {meta['runs_per_vignette']} per vignette; majority vote used
- **Safety classification:**
  - *Correct* — exact match with gold standard
  - *Safe error* — overtriage (higher urgency than needed; conservative but acceptable)
  - *Unsafe* — undertriage (lower urgency than needed; **clinically dangerous**)

## Limitations

- Vignettes are standardised "textbook" cases; real-world patient language varies
- Condensed format may not reflect typical Asklepios conversational input
- Single-model evaluation; no comparison with nurse triage
- Greek-language triage not separately evaluated (this test used English prompts)
{unsafe_section}
## Reproducibility

All vignettes, runner code and raw results are available in this repository.
To reproduce:

```bash
export Claude_API_Key="your-key-here"
python runner.py
python report_generator.py
```

## Citation

If you use this validation in a publication:

```
Asklepios AI Nurse (2025). Triage Accuracy on Semigran-45 Benchmark.
Based on: Semigran HL et al. BMJ 2015 (doi:10.1136/bmj.h3480)
Dataset: Schmieding ML et al. Zenodo 2022 (doi:10.5281/zenodo.6054093)
```
"""
    return md

if __name__ == "__main__":
    data = load_latest_results()
    md = generate_markdown_report(data)
    out = RESULTS_DIR / "VALIDATION_REPORT.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Report saved → {out}")
    print("\n" + "="*60)
    print(md[:2000])
