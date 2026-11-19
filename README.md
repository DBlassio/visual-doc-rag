# visual-doc-rag

Visual document retrieval over public PDF reports: pages are rendered as images and
retrieved with late-interaction models (ColPali / ColQwen family), then improved with
LoRA fine-tuning and measured with a pre-registered evaluation protocol.

**Status:** Session 1 (setup). Nothing is indexed yet.

## Principles (carried over from the arXiv RAG project)

- Failures must be loud: no silent empty results, blank pages or mismatched settings.
- Every silent failure found becomes a test.
- Evaluation is designed before models are tuned: document-level splits, hand-written
  queries, metric chosen in advance (nDCG@10 per stratum), bootstrap confidence intervals.

## Setup

```bash
conda create -n docrag python=3.11 -y
conda activate docrag
pip install -e ".[dev]"
cp .env.example .env   # Windows PowerShell: Copy-Item .env.example .env
pytest
ruff check .
```

## Layout

```
src/docrag/     library code (config, render, ...)
scripts/        runnable entry points
tests/          pytest suite (runs in CI)
data/raw/       source PDFs (git-ignored; check licenses before adding)
data/pages/     rendered page images (git-ignored)
docs/           decisions and notes
```
