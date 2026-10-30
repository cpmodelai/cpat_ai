"""The two lists at the top of excel_ai/, generated from the register (register.py) at every release (v0.8.4: every
module and kind, the same columns as the tracker).

- BUGS.md: the bugs. Legacy bugs (L), with the prototype's fix and the status in legacy 465; the
  prototype's own bugs (M).
- ISSUES.md: the issues (I; the data problems first), replicated or departures by user decision; the departures
  of the LegacyDiff sheet (LD); the upgrades (U).

    python make_replication_lists.py
"""
import os as _os, sys as _sys  # the excel_ai code folders and data/scripts on the path (core/tools/xlpaths.py)
_xl = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_xl) != 'excel_ai':
    _xl = _os.path.dirname(_xl)
_sys.path.insert(0, _os.path.join(_xl, 'core', 'tools'))
import xlpaths  # noqa: E402,F401
import os

import issues_register as R
import register as G

HERE = xlpaths.MIT                     # excel_ai/mitigation/ (the script sits in a subfolder)
TOP = xlpaths.CORE                                   # BUGS.md, ISSUES.md: excel_ai/core/ (2026-10-30)
V = R.REGISTER_VERSION
RULE = ['**The rule (NORMS 0).** Never replicate a legacy bug; always replicate a legacy issue, and track it. A bug: '
        'legacy does not compute what it means to (a wrong row, a double application, a dead reference); the prototype '
        'fixes it. An issue: legacy does what it means to, but the choice is open to question; the prototype does the '
        'same and tracks it. A departure that is not a bug fix is kept only by user decision. Data problems are '
        'issues (area Data): replicated; where legacy needs a formula fix, that fix is a legacy bug (L) and the issue '
        'is Very high; where no cell plan is possible, the prototype aligns with legacy and the issue is Extremely '
        'high.', '',
        f'Generated from the register (`../bugs_and_legacy/register/register.py`) by '
        f'`../bugs_and_legacy/register/make_replication_lists.py`. The same items, every column: the tracker '
        f'`../bugs_and_legacy/Tracking_Legacy_Bugs_v{V}.xlsx` (the master list). Bugs in detail: '
        f'`../bugs_and_legacy/Legacy_CPAT_Bugs_v{V}.docx`. Issues in detail: the appendices of the Documentation '
        f'(`../mitigation/docs/CPAT-AI-Mitigation_Documentation.docx`). Lists: [`BUGS.md`](BUGS.md), [`ISSUES.md`](ISSUES.md).',
        '']


def cell(s):
    return str(s or '').replace('|', '/').replace('\n', ' ')


def table(header, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join('---' for _ in header) + '|']
    return out + ['| ' + ' | '.join(cell(v) for v in r) + ' |' for r in rows] + ['']


def bugs_md():
    c = G.counts()
    L = G.by_kind('L')
    lines = [f'# BUGS: legacy CPAT bugs, prototype bugs and documentation bugs (v{V})', ''] + RULE + [
        f'**{c["L"]} legacy bugs, {c["M"]} prototype bugs, {c["DOC"]} documentation bugs.** Legacy 465: '
        f'{sum(r["legacy465"] == "Fixed" for r in L)} fixed (confirmed), '
        f'{sum(r["legacy465"] == "Fixed with caveats" for r in L)} fixed with caveats, '
        f'{sum(r["legacy465"] == "Not fixed (marked fixed)" for r in L)} marked fixed but not fixed, '
        f'{sum(r["legacy465"] == "Open" for r in L)} open.', '',
        '## 1. Legacy bugs (L)', '',
        'Fixed in the prototype (or the feature not built); never replicated.', '']
    lines += table(['Code', 'Former', 'Area', 'Priority', 'Bug', 'Where in legacy (465)', 'In the prototype',
                    'Legacy 465', 'See also'],
                   [(r['id'], r['former'], r['area'], r['priority'], r['title'], r['where'], r['prototype'],
                     r['legacy465'], r['see_also']) for r in L])
    M = G.by_kind('M')
    lines += ['## 2. Prototype bugs (M)', '', f'Defects of the prototype itself: '
              f'{sum(r["status"] not in ("Open", "Withdrawn") for r in M)} fixed, '
              f'{sum(r["status"] == "Open" for r in M)} open, {sum(r["status"] == "Withdrawn" for r in M)} withdrawn. '
              'Prototype bugs are never put into Coded CPAT: it has the correct formula and the prototype is fixed to '
              'align (NORMS 0, rule 6). M15-M22 were found by Coded CPAT and fixed in v0.9.2 '
              '([`plans/Fix_prototype_bugs_M15-M22.md`](plans/Fix_prototype_bugs_M15-M22.md)).', '']
    lines += table(['Code', 'Priority', 'Bug', 'Where', 'Fix', 'Status'],
                   [(r['id'], r['priority'], r['title'], r['where'], r['fix'] if r['status'] == 'Open' else '',
                     r['prototype']) for r in M])
    lines += ['## 3. Documentation bugs (DOC)', '', 'Errors in the CPAT methodology documentation '
              '(`docs/01_MainDocumentation/`); no model is affected, the documentation is to be corrected.', '']
    lines += table(['Code', 'Priority', 'Bug', 'Where', 'Correction'],
                   [(r['id'], r['priority'], r['title'], r['where'], r['fix']) for r in G.by_kind('DOC')])
    return lines


def issues_md():
    c = G.counts()
    lines = [f'# ISSUES: issues (data problems first), departures and upgrades (v{V})', ''] + RULE + [
        f'**{c["I"]} issues ({len(G.data_items())} data problems), {c["LD"]} departures (LegacyDiff), {c["U"]} upgrades.**',
        '', '## 1. Data problems', '', 'Most urgent first. Extremely high: no cell plan possible, the prototype does '
                                     'exactly what legacy does. Very high: a legacy bug (L) covers it; the data still '
                                     'need fixing.', '']
    lines += table(['Code', 'Former', 'Kind', 'Priority', 'Status', 'Title', 'In the prototype', 'Next step'],
                   [(r['id'], r['former'], r['kind'], r['priority'], r['status'], r['title'], r['prototype'], r['fix'])
                    for r in G.data_items()])
    lines += ['## 2. Issues (I)', '', 'Replicated, a departure by user decision, or a limitation of the prototype.', '']
    lines += table(['Code', 'Former', 'Module', 'Severity', 'Status', 'Issue', 'In the prototype', 'See also'],
                   [(r['id'], r['former'], r['area'], r['priority'], r['status'], r['title'], r['prototype'],
                     r['see_also']) for r in G.by_kind('I')])
    lines += ['## 3. Departures (LD, sheet LegacyDiff)', '']
    lines += table(['Code', 'Type', 'Area', 'Departure', 'Why', 'See also'],
                   [(r['id'], r['priority'], r['title'], r['description'], r['fix'], r['see_also'])
                    for r in G.by_kind('LD')])
    lines += ['## 4. Upgrades (U)', '']
    lines += table(['Code', 'Priority', 'Upgrade', 'What and why'],
                   [(r['id'], r['priority'], r['title'], r['description']) for r in G.by_kind('U')])
    return lines


def main():
    for name, lines in (('BUGS.md', bugs_md()), ('ISSUES.md', issues_md())):
        path = os.path.join(TOP, name)
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines))
        print('wrote', path)


if __name__ == '__main__':
    main()
