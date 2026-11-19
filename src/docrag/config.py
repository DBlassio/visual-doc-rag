"""Central configuration: paths and environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Repo root = two levels above src/docrag/config.py
REPO_ROOT = Path(__file__).resolve().parents[2]

# Load .env from the repo root (no-op if it does not exist)
load_dotenv(REPO_ROOT / ".env")


def data_dir() -> Path:
    """Base data directory (default: <repo>/data). Overridable via DOCRAG_DATA_DIR."""
    base = Path(os.environ.get("DOCRAG_DATA_DIR", "data"))
    return base if base.is_absolute() else REPO_ROOT / base


def raw_dir() -> Path:
    return data_dir() / "raw"


def pages_dir() -> Path:
    return data_dir() / "pages"
