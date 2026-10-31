"""The reference values of the engineer road model switched on (TrModel = Engineer), which the shipped workbook has no
stored run of: Excel-AI's release workbook recalculated in LibreOffice (LAMBDAs expanded, as the Excel-AI checks do)
with scenario 2 switched to the engineer model.

    cpat_testing/compare/reference/excel_ai_<v>_engineer.csv   every coded row of Mitigation group 2, years as columns

First it recalculates the shipped scenarios and counts the codes where LibreOffice differs from the values Excel
stored (reference/excel_ai_<v>.csv), beyond the comparison's tolerance: 0 for 1.1.0.

Run from coded/ (about 8 minutes; needs LibreOffice and its Python bridge):
    python cpat_testing/compare/make_engineer_reference.py
"""
import csv
import re
import sys
from pathlib import Path

CODED = Path(__file__).resolve().parents[2]
REPO = CODED.parent
sys.path.insert(0, str(CODED))
sys.path.insert(0, str(REPO / 'excel_ai' / 'mitigation' / 'checks'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cpat_model import EXCEL_AI_VERSION                     # noqa: E402
import check_full as C                                       # noqa: E402  (the LAMBDA expansion of the Excel-AI checks)
import check_quick as Q                                      # noqa: E402
import lo_session as LO                                      # noqa: E402
from extract_excel_ai import WORKBOOK, text                  # noqa: E402
from compare import ATOL, RTOL, reference                     # noqa: E402

import numpy as np                                           # noqa: E402
import pandas as pd                                          # noqa: E402

OUT = CODED / 'cpat_testing' / 'compare' / 'reference'
TRMODEL = (338, 11)                                          # ScenarioDefinition K338: TrModel of scenario 2
GROUP2 = 33                                                  # Mitigation: code column AG, the 20 years follow


def group2(doc):
    sh = doc.Sheets.getByName('Mitigation')
    cur = sh.createCursor()
    cur.gotoEndOfUsedArea(False)
    last = cur.getRangeAddress().EndRow + 1
    rows = LO.Session.grid(doc, 'Mitigation', 1, 1, last, GROUP2 + 20).data
    years = [int(y) for y in rows[0][11:31]]
    out, seen = [], set()
    for r in rows:
        code = r[GROUP2 - 1]
        if isinstance(code, str) and code.count('.') >= 2 and code not in seen:   # section 19 repeats codes
            seen.add(code)
            out.append([code] + [text(v if v != '' else None) for v in r[GROUP2:GROUP2 + 20]])
    return years, out


def write(path, years, rows):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f, lineterminator='\n').writerows([['code'] + years] + rows)
    print('wrote', path, len(rows), 'rows')


def main():
    lam = Q.file_lambdas(str(WORKBOOK))
    call = re.compile(r'(?<![A-Za-z_.])(' + '|'.join(sorted(lam, key=len, reverse=True)) + r')\(')
    path = LO.expanded_zip(str(WORKBOOK), call, lambda f: C.expand(f, lam))
    with LO.Session(timeout=300) as s:
        doc = s.load(path)
        s.calc(doc)
        years, rows = group2(doc)
        stored = reference()
        off = [r[0] for r in rows if r[0] in stored.index and not np.allclose(
            pd.to_numeric(pd.Series(r[1:]).replace('', np.nan), errors='coerce').values.astype(float),
            stored.loc[r[0]].values.astype(float), rtol=RTOL, atol=ATOL, equal_nan=True)]
        print(f'LibreOffice against the stored values: {len(off)} of {len(rows)} codes differ', off[:10])
        doc.Sheets.getByName('ScenarioDefinition').getCellByPosition(TRMODEL[1] - 1, TRMODEL[0] - 1).setString('Engineer')
        s.calc(doc)
        years, rows = group2(doc)
        write(OUT / f'excel_ai_{EXCEL_AI_VERSION}_engineer.csv', years, rows)


if __name__ == '__main__':
    main()
