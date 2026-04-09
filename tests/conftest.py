"""Test configuration.

Adds the project root to the import path so tests can import the src package
when pytest is executed from the repository root.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
