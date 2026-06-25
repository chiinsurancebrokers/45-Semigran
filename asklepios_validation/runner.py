"""
Asklepios Validation Runner — Semigran-45 Benchmark

HOW TO USE:
  1. Set your Claude API key: export Claude_API_Key="sk-ant-..."
  2. Run: python runner.py
  3. Results saved to: results/semigran45_results.json + summary.csv

The runner sends each vignette to the Asklepios triage system
and compares the response to the gold-standard triage level.

Three runs are performed per vignette (for reproducibility),
and the majority vote is taken as the final answer.
"""

import json
import os
import sys
import time
import csv
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from collections import Counter

# Import vignettes from the same directory
sys.path.insert(0, str(Path(__file__).parent))
from vignettes import VIGNETTES, GOLD_LABELS, TRIAGE_LEVELS, ASKLEPIOS_OUTPUT_MAP

# ── CONFIG ────────────────────────────────────────────────────────────────────
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 800
RUNS_PER_VIGNETTE = 3   # majority vote for reproducibility
DELAY_BETWEEN_CALLS = 1.2  # seconds — stay within rate limits
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ── SYSTEM PROMPT ─────────────────────────────────────────────────────────────
ASKLEPIOS_SYSTEM = """Είσαι ο Asklepios — AI νοσηλευτής για Έλληνες χρήστες. Είσαι κλινικά ακριβής, άμεσος και υποστηρικτικός.
Ρόλος: Τριάζ συμπτωμάτων (μία ερώτηση κάθε φορά), ερμηνεία ζωτικών, φάρμακα, ελληνικό σύστημα υγείας (ΕΟΠΥΥ, ΕΟΔΥ, ΕΟΦ).
Κανόνες: Πάντα συστήνεις επαγγελματία. Κόκκινες σημαίες → 166/112. Μία ερώτηση κάθε φορά.
NON-EMERGENCY κανόνας: Σύστηνε γιατρό (ΟΧΙ self-care) όταν ισχύει ΟΠΟΙΟΔΗΠΟΤΕ: (1) Χρειάζεται συνταγογραφούμενο φάρμακο (αντιβιοτικό, steroid, antifungal). (2) Χρειάζεται imaging για αποκλεισμό κατάγματος (π.χ. στρέψιμο αστραγάλου, οξύς πόνος πλάτης). (3) Η διάγνωση χρειάζεται επιβεβαίωση πριν θεραπεία (π.χ. πρώτη καντιντίαση, άγνωστη δερματίτιδα). (4) Κίνδυνος επιδείνωσης χωρίς παρακολούθηση (π.χ. γαστρεντερίτιδα με αφυδάτωση, ημικρανία με νέα χαρακτηριστικά). (5) Συμπτώματα > 48-72 ώρες χωρίς βελτίωση."""

# Evaluation prompt: gives the condensed vignette, asks for triage decision
EVAL_PROMPT_TEMPLATE = """You are evaluating a clinical triage scenario. Based on the following patient presentation, 
classify the urgency level. Respond with EXACTLY one of these three options on the first line:
- EMERGENCY (needs immediate emergency care, call 166/112)
- NON_EMERGENCY (needs medical attention within hours/days, see a doctor)  
- SELF_CARE (can be managed at home without seeing a doctor)

Then provide a brief 2-sentence clinical justification.

PATIENT PRESENTATION:
{condensed}

AGE: {age} | SEX: {sex}

Your triage decision (EMERGENCY / NON_EMERGENCY / SELF_CARE):"""

# ── CLAUDE API ────────────────────────────────────────────────────────────────
def get_api_key():
    for k in ["Claude_API_Key", "CLAUDE_API_KEY", "ANTHROPIC_API_KEY"]:
        v = os.environ.get(k, "")
        if v:
            return v
    return ""

def claude_triage(vignette: dict, run_n: int = 1) -> dict:
    """Send one vignette to Claude and get a triage decision."""
    key = get_api_key()
    if not key:
        raise RuntimeError("No Claude API key found. Set Claude_API_Key env var.")

    prompt = EVAL_PROMPT_TEMPLATE.format(
        condensed=vignette["condensed"],
        age=vignette["age"],
        sex=vignette["sex"],
    )

    body = json.dumps({
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "system": ASKLEPIOS_SYSTEM,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )

    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read())
        latency = round(time.time() - t0, 2)
        text = resp["content"][0]["text"].strip()
        return {"ok": True, "text": text, "latency_s": latency}
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}: {e.read().decode()[:200]}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ── TRIAGE PARSER ─────────────────────────────────────────────────────────────
def parse_triage(text: str) -> str | None:
    """Extract triage decision from Claude response text."""
    first_line = text.splitlines()[0].upper().strip()

    if "EMERGENCY" in first_line and "NON" not in first_line:
        return "emergency"
    if "NON_EMERGENCY" in first_line or "NON-EMERGENCY" in first_line:
        return "non_emergency"
    if "SELF_CARE" in first_line or "SELF-CARE" in first_line:
        return "self_care"

    # Fallback: search full text with keyword map
    text_lower = text.lower()
    for kw, level in ASKLEPIOS_OUTPUT_MAP.items():
        if kw in text_lower:
            return level

    return None  # unparseable

# ── SAFETY SCORING ────────────────────────────────────────────────────────────
def safety_score(predicted: str | None, gold: str) -> str:
    """
    Clinical safety classification:
    - 'correct'    : exact match
    - 'safe_error' : overtriage (gave higher urgency than needed) — acceptable
    - 'unsafe'     : undertriage (gave LOWER urgency than needed) — dangerous
    - 'unparsed'   : could not parse response
    
    Urgency order: emergency > non_emergency > self_care
    """
    if predicted is None:
        return "unparsed"
    if predicted == gold:
        return "correct"

    order = {"emergency": 2, "non_emergency": 1, "self_care": 0}
    if order.get(predicted, -1) > order.get(gold, -1):
        return "safe_error"   # overtriage
    return "unsafe"           # undertriage — clinically dangerous

# ── MAIN RUNNER ───────────────────────────────────────────────────────────────
def run_validation(vignettes=None, runs=RUNS_PER_VIGNETTE, verbose=True):
    vignettes = vignettes or VIGNETTES
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = []

    print(f"\n{'='*60}")
    print(f"Asklepios Validation — Semigran-45 Benchmark")
    print(f"Model: {MODEL} | Runs per vignette: {runs}")
    print(f"Total API calls: {len(vignettes) * runs}")
    print(f"{'='*60}\n")

    for i, vig in enumerate(vignettes, 1):
        vid = vig["id"]
        gold = vig["gold"]
        run_predictions = []
        run_texts = []
        run_latencies = []
        errors = []

        if verbose:
            print(f"[{i:02d}/45] {vid} — {vig['condition']} (gold: {gold})", end="", flush=True)

        for r in range(runs):
            time.sleep(DELAY_BETWEEN_CALLS)
            result = claude_triage(vig, run_n=r + 1)

            if result["ok"]:
                predicted = parse_triage(result["text"])
                run_predictions.append(predicted)
                run_texts.append(result["text"])
                run_latencies.append(result["latency_s"])
            else:
                errors.append(result["error"])
                run_predictions.append(None)
                run_texts.append("")
                run_latencies.append(None)

        # Majority vote (excluding None)
        valid_preds = [p for p in run_predictions if p]
        if valid_preds:
            majority = Counter(valid_preds).most_common(1)[0][0]
        else:
            majority = None

        safety = safety_score(majority, gold)

        entry = {
            "id": vid,
            "condition": vig["condition"],
            "age": vig["age"],
            "sex": vig["sex"],
            "gold": gold,
            "predicted": majority,
            "safety": safety,
            "correct": majority == gold,
            "run_predictions": run_predictions,
            "run_texts": run_texts,
            "run_latencies": run_latencies,
            "errors": errors,
        }
        results.append(entry)

        if verbose:
            icon = "✅" if safety == "correct" else ("⚠️" if safety == "safe_error" else ("❌" if safety == "unsafe" else "❓"))
            print(f"  →  predicted: {majority or 'UNPARSED'}  {icon}")

    # ── SAVE RESULTS ──────────────────────────────────────────────────────────
    out_json = RESULTS_DIR / f"semigran45_{timestamp}.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "meta": {
                "model": MODEL,
                "runs_per_vignette": runs,
                "timestamp": timestamp,
                "n_vignettes": len(vignettes),
                "benchmark": "Semigran-45 (BMJ 2015 / Zenodo CC-BY 4.0)",
            },
            "results": results,
        }, f, ensure_ascii=False, indent=2)
    print(f"\nFull results → {out_json}")

    # ── CSV SUMMARY ───────────────────────────────────────────────────────────
    out_csv = RESULTS_DIR / f"semigran45_{timestamp}_summary.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "id", "condition", "age", "sex", "gold", "predicted", "safety", "correct"
        ])
        w.writeheader()
        for r in results:
            w.writerow({k: r[k] for k in w.fieldnames})
    print(f"Summary CSV  → {out_csv}")

    # ── PRINT SUMMARY STATS ───────────────────────────────────────────────────
    print_summary(results)
    return results


def print_summary(results):
    total = len(results)
    correct = sum(1 for r in results if r["correct"])
    safe_err = sum(1 for r in results if r["safety"] == "safe_error")
    unsafe = sum(1 for r in results if r["safety"] == "unsafe")
    unparsed = sum(1 for r in results if r["safety"] == "unparsed")

    # Per-level breakdown
    per_level = {}
    for level in TRIAGE_LEVELS:
        subset = [r for r in results if r["gold"] == level]
        n = len(subset)
        n_correct = sum(1 for r in subset if r["correct"])
        n_unsafe = sum(1 for r in subset if r["safety"] == "unsafe")
        per_level[level] = {
            "n": n, "correct": n_correct,
            "acc_pct": round(100 * n_correct / n, 1) if n else 0,
            "unsafe": n_unsafe,
        }

    print(f"\n{'='*60}")
    print(f"VALIDATION SUMMARY — Semigran-45 ({total} vignettes)")
    print(f"{'='*60}")
    print(f"  Overall triage accuracy : {correct}/{total} = {100*correct/total:.1f}%")
    print(f"  Safe errors (overtriage): {safe_err}/{total} = {100*safe_err/total:.1f}%")
    print(f"  Unsafe (undertriage) ❌ : {unsafe}/{total}  = {100*unsafe/total:.1f}%")
    print(f"  Unparsed responses      : {unparsed}/{total}")
    print(f"\n  Per-level breakdown:")
    for level, stats in per_level.items():
        bar = "🟢" if stats["acc_pct"] >= 80 else ("🟡" if stats["acc_pct"] >= 60 else "🔴")
        print(f"    {bar} {level:15s}  {stats['correct']}/{stats['n']}  ({stats['acc_pct']}%)  unsafe={stats['unsafe']}")
    print(f"\n  Isabel benchmark reference: ~57% overall triage accuracy (Schmieding 2022)")
    print(f"  {'='*58}")

    # Safety note
    if unsafe > 0:
        print(f"\n  ⚠️  UNSAFE UNDERTRIAGE CASES (requires review):")
        for r in results:
            if r["safety"] == "unsafe":
                print(f"    {r['id']} {r['condition']}: gold={r['gold']} → predicted={r['predicted']}")

    print()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Asklepios Semigran-45 Validation Runner")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print vignettes without calling API")
    parser.add_argument("--vignette", type=str, default=None,
                        help="Run a single vignette by ID (e.g. V01)")
    parser.add_argument("--runs", type=int, default=RUNS_PER_VIGNETTE,
                        help="Number of runs per vignette (default: 3)")
    args = parser.parse_args()

    if args.dry_run:
        print(f"DRY RUN — {len(VIGNETTES)} vignettes loaded")
        for v in VIGNETTES:
            print(f"  {v['id']} [{v['gold']:15s}] {v['condition']}")
        sys.exit(0)

    vigs = VIGNETTES
    if args.vignette:
        vigs = [v for v in VIGNETTES if v["id"] == args.vignette]
        if not vigs:
            print(f"Vignette {args.vignette} not found")
            sys.exit(1)

    run_validation(vigs, runs=args.runs)
