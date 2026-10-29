"""The two lists at the top of excel_ai/, generated from the register (register.py) at every release (v8.4: every
module and kind, the same columns as the tracker).

- BUGS.md: the bugs. Legacy bugs (L) and data bugs (DB), with the prototype's fix and the status in legacy 465; the
  prototype's own bugs (M).
- ISSUES.md: the issues. Data issues (DI) and issues (I), replicated or departures by user decision; the departures
  of the LegacyDiff sheet (LD); the upgrades (U).

    python make_replication_lists.py
"""
import os

import issues_register as R
import register as G

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.join(HERE, '..')
V = R.REGISTER_VERSION
RULE = ['**The rule (NORMS 0).** Never replicate a legacy bug; always replicate a legacy issue, and track it. A bug: '
        'legacy does not compute what it means to (a wrong row, a double application, a dead reference); the prototype '
        'fixes it. An issue: legacy does what it means to, but the choice is open to question; the prototype does the '
        'same and tracks it. A departure that is not a bug fix is kept only by user decision. Data: a data issue (DI) '
        'is replicated exactly; a data bug (DB) is not replicated and is fixed by changing the input data (it has a '
        'plan); when the fix needs formulas, it is a legacy bug (L).', '',
        f'Generated from the register (`mitigation/register.py`) by `mitigation/make_replication_lists.py`. The same '
        f'items, every column: the tracker `Tracking_Legacy_Bugs_v{V}.xlsx` (the master list). Bugs in detail: '
        f'`Legacy_CPAT_Bugs_v{V}.docx`. Issues in detail: the appendices of the Documentation '
        f'(`mitigation/CPAT-AI-Mitigation_Documentation.docx`). Lists: [`BUGS.md`](BUGS.md), [`ISSUES.md`](ISSUES.md).',
        '']


def cell(s):
    return str(s or '').replace('|', '/').replace('\n', ' ')


def table(header, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join('---' for _ in header) + '|']
    return out + ['| ' + ' | '.join(cell(v) for v in r) + ' |' for r in rows] + ['']


def bugs_md():
    c = G.counts()
    L = G.by_kind('L')
    lines = [f'# BUGS: legacy CPAT bugs, data bugs and prototype bugs (v{V})', ''] + RULE + [
        f'**{c["L"]} legacy bugs, {c["DB"]} data bugs, {c["M"]} prototype bugs.** Legacy 465: '
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
    lines += ['## 2. Data bugs (DB)', '', 'Not replicated; fixed by changing the input data, each with its plan.', '']
    lines += table(['Code', 'Former', 'Severity', 'Status', 'Data bug', 'Plan', 'See also'],
                   [(r['id'], r['former'], r['priority'], r['status'], r['title'], r['fix'], r['see_also'])
                    for r in G.by_kind('DB')])
    lines += ['## 3. Prototype bugs (M)', '', 'Defects of the prototype itself, all fixed.', '']
    lines += table(['Code', 'Bug', 'Fixed'], [(r['id'], r['title'], r['prototype']) for r in G.by_kind('M')])
    return lines


def issues_md():
    c = G.counts()
    lines = [f'# ISSUES: data issues, issues, departures and upgrades (v{V})', ''] + RULE + [
        f'**{c["DI"]} data issues, {c["I"]} issues, {c["LD"]} departures (LegacyDiff), {c["U"]} upgrades.**', '',
        '## 1. Data issues (DI)', '', 'Replicated exactly: the prototype does what legacy does with the data as they '
                                      'are.', '']
    lines += table(['Code', 'Former', 'Severity', 'Status', 'Data issue', 'In the prototype', 'Next step'],
                   [(r['id'], r['former'], r['priority'], r['status'], r['title'], r['prototype'], r['fix'])
                    for r in G.by_kind('DI')])
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
