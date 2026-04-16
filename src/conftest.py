"""Pytest configuration — makes all day subdirectories importable."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "day1"))
