"""Scenario inputs (the MTInputs rows by NameOfParameter, one column per scenario) and advanced inputs.

Only this package reads input files (NORMS 4). Formats: data/README.md.
"""
from cpat_model.inputs.scenarios import ScenarioSet, read_scenario_set  # noqa: F401
