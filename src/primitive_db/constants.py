#!/usr/bin/env python3

from pathlib import Path

current_file = Path(__file__).resolve()
PROJECT_ROOT = current_file.parent.parent.parent
DATA_DIR = PROJECT_ROOT/"data"
METADATA_FILE = PROJECT_ROOT/"db_meta.json"

VALID_TYPES = {"int", "str", "bool"}
