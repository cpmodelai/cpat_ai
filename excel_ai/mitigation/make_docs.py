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
    # upgrades are in the register (v8.4: Legacy_CPAT_Bugs_v<n>.docx, the tracker, the appendices); this document points to it
    text = ['# Bugs, issues, differences with legacy and upgrades', '',
            'In the register (`excel_ai/Legacy_CPAT_Bugs_v<version>.docx`, the tracker `excel_ai/Tracking_Legacy_Bugs_v<version>.xlsx`): the legacy '
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


def register_appendices():
    """v8.4 (user 2026-10-28): the issues, data issues, departures, upgrades, prototype bugs and the bug-fixing procedure
    as appendices of the Documentation (the bugs: Legacy_CPAT_Bugs_v<version>.docx; everything: the tracker)."""
    import make_bugfix_book as BB
    import register as G
    v = IR.REGISTER_VERSION
    full = lambda rows: '\n'.join(f'**{r["id"]}{" (was " + r["former"] + ")" if r["former"] else ""}. {r["title"]}.** '
                                   f'{r["description"]} *In the prototype:* {r["prototype"]}.'
                                   + (f' *Next step:* {r["fix"]}' if r['fix'] else '')
                                   + (f' *Status:* {r["status"]}.' if r['status'] else '')
                                   + (f' *See also:* {r["see_also"]}.' if r['see_also'] else '') + '\n'
                                   for r in rows)
    out = ['# Appendix A. The register: bugs and issues', '',
           f'Every bug and issue of legacy CPAT and of the prototypes has a code. The master list is the tracker '
           f'`excel_ai/Tracking_Legacy_Bugs_v{v}.xlsx` (tabs Bugs and Issues, every module in the same columns); the '
           f'bugs are documented in `excel_ai/Legacy_CPAT_Bugs_v{v}.docx`, the rest in these appendices. Codes '
           f'renumbered in v8.4 give their former code.', '',
           table(['Code', 'Number', 'Kind', 'What the prototype does', 'Where'],
                 [(p_, G.counts()[p_], d, w, G.KINDS[p_][2]) for p_, d, w in G.DEFINITIONS], [1, 1, 8, 4, 3]),
           '# Appendix B. Data problems', '',
           'Problems of the input data (issues of area Data, and the legacy bug L170 that covers one), most urgent '
           'first. The prototype does what legacy does with the data, unless the user decided otherwise.', '',
           full(G.data_items()),
           '# Appendix C. Issues (I)', '',
           'Legacy does what it means to, but the choice is open to question; replicated unless the user decided '
           'otherwise. Also the limitations of the prototype itself. (The data problems: appendix B.)', '',
           full([r for r in G.by_kind('I') if r['area'] != 'Data']),
           '# Appendix D. Departures from legacy (LD, sheet LegacyDiff)', '',
           table(['Code', 'Type', 'Area', 'Departure', 'Why'],
                 [(r['id'], r['priority'], r['title'], r['description'], r['fix']) for r in G.by_kind('LD')],
                 [1, 2, 3, 8, 5]),
           '# Appendix E. Upgrades (U)', '',
           table(['Code', 'Priority', 'Upgrade', 'What and why'],
                 [(r['id'], r['priority'], r['title'], r['description']) for r in G.by_kind('U')], [1, 1, 3, 10]),
           '# Appendix F. Prototype bugs (M)', '',
           'Defects of the prototype itself, found and fixed during development, for the record.', '',
           table(['Code', 'Bug', 'Fixed', 'What happened', 'Fix'],
                 [(r['id'], r['title'], r['prototype'], r['description'], r['fix']) for r in G.by_kind('M')],
                 [1, 3, 2, 6, 5]),
           '# Appendix G. The bug-fixing procedure for legacy CPAT', '']
    md = []

    class Doc:
        def add_heading(self, text_, level):
            if level > 1:
                md.extend([f'{"#" * level} {re.sub(r"^2[.]", "G.", text_)}', ''])

    saved = BB.para, BB.table, BB.bullets
    BB.para = lambda d, s, bold_lead=None, **k: md.extend([(f'**{bold_lead}** ' if bold_lead else '') + s, ''])
    BB.table = lambda d, header, rows, widths, **k: md.append(table(header, rows, [max(1, round(w)) for w in widths]))
    BB.bullets = lambda d, items, **k: md.extend([f'- {s}' for s in items] + [''])
    try:
        BB.procedure_steps(Doc())
    finally:
        BB.para, BB.table, BB.bullets = saved
    text_ = '\n'.join(md).replace('section 2.1', 'G.1').replace('section 2.3', 'G.3').replace('section 2.4', 'G.4')
    text_ = text_.replace('The plans are printed with each bug in section 3.',
                          f'The plans are printed with each bug in Legacy_CPAT_Bugs_v{v}.docx.')
    return '\n'.join(out) + '\n' + text_


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
    pandoc(meta(f'CPAT-AI Mitigation Prototype v{IR.B.VERSION}', 'Documentation') + doc + '\n\n' +
           register_appendices(), OUT)
    chapters = [open(os.path.join(d, 'methods', m), encoding='utf-8').read() for m in METHODS]
    appx = [part('Appendix A: the model in equations', 'Equations.md'),
            part('Appendix B: data tabs', os.path.join('docs', 'methods', 'Data_tabs.md'))]
    note = ('*Legacy row numbers in this volume are rows of CPAT 1.0pre_456_NoPropData.xlsb, the file the prototype '
            'was built and checked against. In the latest file, CPAT 1.0pre_465, Mitigation rows from 5667 on sit 11 to '
            '15 rows higher; the bug-fix register quotes 465 rows (v8.2).*\n\n')
    pandoc(meta(f'CPAT-AI Mitigation Prototype v{IR.B.VERSION}', 'Methods') + note + '\n'.join(chapters + appx),
           METHODS_OUT)


if __name__ == '__main__':
    main()
