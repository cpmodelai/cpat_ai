"""Every equation id cited in the code (`EQ-<id>`) exists in the equation list (cpat_documentation/equations/
equations.yaml), and the cited ids are listed (NORMS 1.3). Ids of the list without a function yet are reported."""
import re
from pathlib import Path

import yaml

CODED = Path(__file__).resolve().parents[1]
EQ = CODED / 'cpat_documentation' / 'equations' / 'equations.yaml'


def defined_ids():
    src = yaml.safe_load(EQ.read_text(encoding='utf-8'))
    return {e['id'] for p in src['parts'] for s in p['sections'] for e in s.get('equations', [])}


def cited_ids():
    ids = {}
    for f in (CODED / 'cpat_model').rglob('*.py'):
        for m in re.finditer(r'EQ-([A-Z]\d+(?:\.\d+)+)', f.read_text(encoding='utf-8')):
            ids.setdefault(m.group(1), set()).add(f.relative_to(CODED).as_posix())
    return ids


def test_cited_ids_exist():
    unknown = {i: sorted(f) for i, f in cited_ids().items() if i not in defined_ids()}
    assert not unknown, f'equation ids cited in the code but not in equations.yaml: {unknown}'


def test_report_coverage(capsys):
    done = set(cited_ids())
    todo = sorted(defined_ids() - done)
    with capsys.disabled():
        print(f'\nequation list: {len(done)} ids with a function, {len(todo)} not yet')
