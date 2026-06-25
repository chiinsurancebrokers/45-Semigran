# Asklepios — Semigran-45 Validation (Run 2)

**Date:** 2026-06-25 · **Model:** claude-sonnet-4-6 · **System prompt:** v2 (NON-EMERGENCY rule)

## Results

| Level | Correct | Accuracy | Unsafe |
|-------|---------|----------|--------|
| Emergency | 15/15 | 100% | 0 |
| Non-emergency | 15/15 | 100% | 0 |
| Self-care | 10/15 | 67% | 0 |
| **Overall** | **40/45** | **88.9%** | **0** |

## vs Benchmarks

| | Accuracy | Unsafe undertriage |
|-|----------|--------------------|
| **Asklepios Run 2** | **88.9%** | **0%** |
| Asklepios Run 1 | 80.0% | 13.3% |
| Isabel DDx | ~84% | — |
| Ada | ~76% | — |
| Babylon | ~72% | — |
| WebMD / NHS 111 | ~57% | — |

## What changed

Added NON-EMERGENCY rule to system prompt: recommend doctor (not self-care) when prescription, imaging, diagnosis confirmation, deterioration risk, or symptoms >48-72h.

**Impact:** 6 unsafe undertriage errors → 0. Non-emergency accuracy 60% → 100%.

Remaining 5 errors are safe overtriage (self-care predicted as non-emergency).
