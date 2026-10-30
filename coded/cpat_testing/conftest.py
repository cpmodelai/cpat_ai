"""Shared test setup: the coded/ folder on the import path (tests run from coded/ with `pytest`)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
