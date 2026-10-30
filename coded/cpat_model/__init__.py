"""Coded CPAT: the Python model that replicates Excel-AI (mitigation and distribution), readable first.

The one entry point is `run` (coded/NORMS.md section 10); the command line, the Shiny app and the tests call it.
Structure and order of the calculation: coded/cpat_documentation/project/Spec.qmd sections 3-4.
"""

EXCEL_AI_VERSION = '1.1.0'            # the Excel-AI version this code replicates (NORMS 0.2, D14)
DISTRIBUTION_VERSION = '1.1.0'        # the Excel-AI distribution module replicated
PYTHON_VERSION = '1.3'
__version__ = f'{EXCEL_AI_VERSION}p{PYTHON_VERSION}'


def run(scenarios, settings=None):
    """Run a scenario set: the baseline first, then each policy scenario in turn (D15).

    scenarios  a ScenarioSet (cpat_model.inputs), e.g. read_scenario_set(path)
    settings   run settings (cpat_model.settings.Settings); default: the dummy database, Egypt, Excel-AI years
    Returns a Results object (cpat_model.results).
    """
    from cpat_model.core.loop import run_scenarios
    from cpat_model.settings import Settings
    return run_scenarios(scenarios, settings or Settings())
