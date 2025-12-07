import os
import sys

# Ensure the project root (where app.py lives) is on sys.path
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app


def test_dummy():
    # This trivial test just checks that the Flask app object exists.
    assert app is not None
