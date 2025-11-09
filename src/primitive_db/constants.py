#!/usr/bin/env python3

from pathlib import Path

PROJECT_ROOT = Path.cwd()
DATA_DIR = PROJECT_ROOT / "data"
METADATA_FILE = PROJECT_ROOT / "db_meta.json"

VALID_TYPES = ["int", "str", "bool"]
