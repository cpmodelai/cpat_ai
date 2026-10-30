"""The folders of excel_ai/ (excel_ai/README.md) and the module path: every Excel-AI script imports this first.

Each script finds this file by walking up to excel_ai/ (four lines at its top) and imports it; this module then puts
every Excel-AI code folder, and data/scripts/, on sys.path, so the scripts import one another by name wherever they
sit (build, check_full, issues_register, legacy_csv, ...).
"""
import os
import sys

XL = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))   # excel_ai/
REPO = os.path.dirname(XL)
CORE = os.path.join(XL, 'core')
TOOLS = os.path.join(CORE, 'tools')
ACTIVE = os.path.join(XL, 'active_workbooks')            # the permalinked _latest copies
MIT = os.path.join(XL, 'mitigation')
DIST = os.path.join(XL, 'distribution')
AP = os.path.join(XL, 'air_pollution')
LEGACY = os.path.join(XL, 'bugs_and_legacy')
REGISTER = os.path.join(LEGACY, 'register')
FIXES = os.path.join(LEGACY, 'fixes')

CODE = [MIT, os.path.join(MIT, 'checks'), os.path.join(MIT, 'extract'), os.path.join(MIT, 'docs'), REGISTER, DIST,
        TOOLS, os.path.join(REPO, 'data', 'scripts')]
for _p in reversed(CODE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
