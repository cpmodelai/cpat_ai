"""Word documentation of CPAT-AI-Mitigation-Prototype v4.7, assembled from the Markdown notes (pandoc): quick start, the
model in equations, the legacy bug fixes needed, the method notes; appendices read from the shipped workbook
(differences with legacy CPAT, version log), the check report (verification) and the register (upgrades).

    python make_docs.py  ->  CPAT-AI-Mitigation_Documentation_v7.0.docx
"""
import datetime
import glob
import os
import re
import subprocess
import tempfile

import openpyxl

import issues_register as IR

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE,   # excel_ai/mitigation/ (restructure 2026-10-22; was root documentation/)
                   'CPAT-AI-Mitigation_Documentation.docx')   # v7.0: root documentation/
WORKBOOK = __import__('build').OUT   # v8.0: the release copy
REPORT = os.path.join(HERE, 'check_report.md')
PARTS = [('Quick start', 'QuickStart.md'),
         ('The model in equations', 'Equations.md'),
         ('Method: domestic energy prices and existing carbon pricing', 'PriceProjection_Method.md'),
         ('Method: power generation costs and electricity prices', 'PowerPrices_Method.md'),
         ('Method: power engineer model', 'PowerModel_Method.md'),
         ('Method: road transport, engineer model', 'Transport_Method.md'),
         ('Method: new ETS', 'ETS_Method.md'),
         ('Method: multiple scenarios and stored results', 'Scenarios_Method.md'),
         ('Method: non-CO2 GHGs and methane', 'GHG_Method.md'),
         ('Method: local air pollutants', 'AirPollutants_Method.md'),
         ('Method: GDP effects', 'GDP_Method.md'),
         ('Method: calibration of energy CO2', 'CO2Calibration_Method.md'),
         ('Method: results sections (memos, 11b-17, 18)', 'ResultsSections_Method.md'),   # v3.13-v3.18
         ('Method: distribution module', 'Distribution_Method.md'),   # v6.4: distribution and data tabs added
         ('Data tabs: legacy tables and how to load a country', 'DataTabs.md')]


def part(title, name):
    text = open(os.path.join(HERE, name), encoding='utf-8').read()
    text = re.sub(r'\A# .*\n', '', text)                      # drop the note's own title
    text = re.sub(r'^(#+) ', lambda m: '#' + m.group(1) + ' ', text, flags=re.M)   # demote one level
    return f'# {title}\n\n*Source: `{name}`.*\n\n{text}\n'


def cell(v):
    return str(v if v is not None else '').replace('|', '/').replace('\n', ' ')


def table(header, rows, widths=None):
    """Pipe table; widths = relative column widths (pandoc reads them from the separator dashes)."""
    widths = widths or [1] * len(header)
    out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join('-' * (6 * w) for w in widths) + '|']
    out += ['| ' + ' | '.join(cell(v) for v in r) + ' |' for r in rows]
    return '\n'.join(out) + '\n'


def appendices():
    wb = openpyxl.load_workbook(WORKBOOK, read_only=True)
    ld = [(r[4], r[1], r[3], r[2], r[5], r[6], r[0]) for r in   # v4.2 columns: Type, Area, This model, Legacy, #, ...
          IR.B.tab(wb, 'LegacyDiff').iter_rows(min_row=5, max_col=7, values_only=True) if r[1]]
    log = [r[0:4] for r in IR.B.tab(wb, 'VersionLog').iter_rows(min_row=IR.B.SET_LOG + 2, max_col=4, values_only=True)
           if r[0]]
    # v7.1 (user 2026-10-22): the legacy bugs, the road-model bugs, the differences with legacy (LegacyDiff) and the
    # upgrades are in the register (CPAT-AI_BugsAndIssues_v<n>.docx) only; this document points to it
    text = ['# Bugs, issues, differences with legacy and upgrades', '',
            'In the register `excel_ai/CPAT-AI_BugsAndIssues_latest.docx`: the legacy '
            f'CPAT bugs ({len(ld)} differences with legacy are listed there too) with the bug-fixing procedure and '
            'the cell-level plans (`bugfixes/`), the issues, the departures from legacy and the potential upgrades. '
            'This document does not repeat them.', '',
            '# Appendix A. Version log', '', '*Source: workbook sheet `Settings`.*', '',
            table(['Version', 'Date', 'Description', 'Max abs regression diff'], log, [2, 3, 12, 5]),
            '# Appendix B. Verification', '',
            '*Source: `check_report.md` (`python check_full.py`, LibreOffice recalculation). Every check '
            'section and its result:*', '']
    rep = REPORT if os.path.exists(REPORT) else max(glob.glob(os.path.join(HERE, 'Old', 'check_report_v*.md')),
                                                    key=os.path.getmtime)   # v6.4: last full check if none yet
    if rep != REPORT:
        text[-2] = (f'*Source: `{os.path.basename(rep)}`, the last full check (not yet run on this version; the '
                    f'quick check passes). Every check section and its result:*')
    rep_lines = open(rep, encoding='utf-8').read().splitlines()
    sec, oks, fails, rows = None, 0, 0, []
    for ln in rep_lines + ['## end']:
        if ln.startswith('## '):
            if sec:
                rows.append([sec, oks, fails])
            sec, oks, fails = ln[3:], 0, 0
        elif ln.strip().startswith('- ') or ln.strip().startswith('  - '):
            oks += ln.rstrip().endswith('OK')
            fails += 'FAIL' in ln
    overall = next((ln for ln in rep_lines if ln.startswith('**Overall')), '')
    text += [table(['Check section', 'Checks OK', 'Checks failed'], rows[:-1] if rows[-1][0] == 'end' else rows, [8, 2, 2]),
             f'{overall}', '',
             'The checks recompute every value independently in Python from the source data; test the formula '
             'variants (the optional LAMBDA library copied over whole rows); test existing carbon pricing with non-zero data; '
             'copy scenario groups as a user would; compare with the previous version on every shared output code; '
             'run a consistency check (check rows and identities in every column, file references, versions, stale texts); '
             'and run the embedded VBA macro in LibreOffice against the Python emulation.', '']
    return '\n'.join(text)


METHODS = ['Prices.md', 'Power.md', 'Transport.md', 'Emissions.md', 'ETS.md', 'Macro_and_results.md',
           'Distribution.md']                       # v8.0: the six merged method chapters (+ distribution)
METHODS_OUT = os.path.join(HERE, 'CPAT-AI-Mitigation_Methods.docx')


def pandoc(md, out, toc=2):
    src = os.path.join(tempfile.mkdtemp(), 'doc.md')
    open(src, 'w', encoding='utf-8').write(md)
    subprocess.run(['pandoc', src, '-o', out, '--toc', f'--toc-depth={toc}',
                    '-f', 'markdown-yaml_metadata_block+yaml_metadata_block-tex_math_dollars'], check=True)
    print('wrote', out)


def meta(title, subtitle):
    return (f'---\ntitle: "{title}"\nsubtitle: "{subtitle}"\n'
            f'date: "{datetime.date.today().isoformat()}"\n---\n\n')


def main():
    """v8.0: two documents (user 2026-10-22): the short documentation (docs/Documentation.md, hand-written) and the
    Methods volume (docs/methods/, one chapter per block; the equations and the data tabs as appendices)."""
    import make_equations as EQ                       # keeps Formulas.md current (not part of the documents)
    EQ.main()
    d = os.path.join(HERE, 'docs')
    doc = re.sub(r'\A# .*\n', '', open(os.path.join(d, 'Documentation.md'), encoding='utf-8').read())
    pandoc(meta(f'CPAT-AI Mitigation Prototype v{IR.B.VERSION}', 'Documentation') + doc, OUT)
    chapters = [open(os.path.join(d, 'methods', m), encoding='utf-8').read() for m in METHODS]
    appx = [part('Appendix A: the model in equations', 'Equations.md'),
            part('Appendix B: data tabs', os.path.join('docs', 'methods', 'Data_tabs.md'))]
    pandoc(meta(f'CPAT-AI Mitigation Prototype v{IR.B.VERSION}', 'Methods') + '\n'.join(chapters + appx), METHODS_OUT)


if __name__ == '__main__':
    main()
