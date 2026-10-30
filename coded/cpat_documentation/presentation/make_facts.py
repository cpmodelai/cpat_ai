"""The numbers of the Coded CPAT deck, from the repository (facts.json beside this file): versions, reference codes
compared, tests (the last generated test status of the documentation book), database tables, equations.

    python make_facts.py && NODE_PATH=<node_modules> PPTX_SKILL=<pptx skill dir> node build_deck.js
"""
import csv
import json
import re
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
CODED = HERE.parents[1]
REPO = CODED.parent
init = (CODED / 'cpat_model' / '__init__.py').read_text()
v = {k: re.search(rf"^{k} = '([^']+)'", init, re.M).group(1) for k in ('EXCEL_AI_VERSION', 'DISTRIBUTION_VERSION',
                                                                     'PYTHON_VERSION')}
ref = CODED / 'cpat_testing' / 'compare' / 'reference'
def codes(f, suffix):
    """Codes of the reference file ending in suffix that have a value (rows with parameters only are not results)."""
    import pandas as pd
    t = pd.read_csv(ref / f, index_col=0)                  # as the comparison reads it (compare.reference)
    return int((t.index.str.endswith(suffix) & t.notna().any(axis=1)).sum())
status = (REPO / 'docs' / 'CPAT_coded_documentation_qmd' / '_test_status.md').read_text()
m = re.search(r'\*\*(\d+) passed, (\d+) failed\*\*', status)
eqs = yaml.safe_load((CODED / 'cpat_documentation' / 'equations' / 'equations.yaml').read_text())
n_eq = sum(len(s.get('equations', [])) for p in eqs['parts'] for s in p['sections'])
manifest = list(csv.DictReader(open(REPO / 'data' / 'Public01' / 'tidy' / '_manifest.csv', encoding='utf-8')))
facts = {
    'version': f"{v['EXCEL_AI_VERSION']}p{v['PYTHON_VERSION']}", 'excel_ai': v['EXCEL_AI_VERSION'],
    'distribution': v['DISTRIBUTION_VERSION'],
    'codes_per_scenario': codes(f"excel_ai_{v['EXCEL_AI_VERSION']}.csv", '.1'),
    'distribution_codes': codes(f"excel_ai_distribution_{v['DISTRIBUTION_VERSION']}.csv", ''),
    'stored_codes': codes(f"excel_ai_{v['EXCEL_AI_VERSION']}_stored_outputs.csv", ''),
    'tests_passed': int(m.group(1)), 'tests_failed': int(m.group(2)),
    'tables': sum(r['kind'] != 'cells layout' for r in manifest),
    'proprietary': sum(r['proprietary'] == 'yes' for r in manifest) + 1,   # energy consumption with the balances
    'equations': n_eq,
}
(HERE / 'facts.json').write_text(json.dumps(facts, indent=1))
print(facts)
