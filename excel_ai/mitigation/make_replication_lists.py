"""The two lists at the top of excel_ai/, generated from the register (issues_register.py) at every release.

User rule 2026-10-15: bugs are never replicated (the prototype fixes them); issues are replicated (the prototype matches legacy)
and tracked. A departure from legacy that is not a bug fix is an exception: kept only by user decision, otherwise
queued to be replicated.

- NotReplicated.md, copied to excel_ai/BUGS.md: where the prototype departs from legacy.
  Part 1: bugs not replicated (fixed, or the feature not built). Part 2: issues not replicated (the exceptions).
- Replicated.md, copied to excel_ai/ISSUES.md: where the prototype matches legacy on purpose.
  Part 1: issues replicated. Part 2: bugs replicated (each one queued to be fixed). Part 3: the prototype's own issues.

    python make_replication_lists.py
"""
import os

import build as B
import issues_register as R
import make_legacy_fixes as F

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.join(HERE, '..')
FILES = {'not': (None, 'BUGS.md'), 'rep': (None, 'ISSUES.md')}   # v8.0: excel_ai/ only (no copies here)
ORDER = {'Open': 0, 'Accepted': 1, 'Dropped': 2, 'Resolved': 3}   # v6.1: Dropped (user 2026-10-20)
DEPART = ('Decision', 'Assumption', 'Data', 'Method', 'Design', 'Simplification', 'Not yet', 'To check (bucket 5)')
RULE = ['**The rule (user, 2026-10-15).** **Bugs are never replicated:** the prototype fixes every legacy bug (or leaves the '
        'feature out). **Issues are replicated:** where legacy works as intended but is questionable (old data, '
        'simplifications, design choices), the prototype does what legacy does, and tracks the issue. A departure from '
        'legacy that is not a bug fix is an exception: it stays only by user decision; otherwise it is queued to be '
        'replicated. Bug = legacy does not do what it means to (wrong row, double application, a dead reference); '
        'issue = legacy does what it means to, but the choice is open to question.', '',
        f'Both lists are generated from the register (`mitigation/issues_register.py`) by '
        '`mitigation/make_replication_lists.py` at every release. The other list: '
        '[`BUGS.md`](BUGS.md) (where the prototype departs from legacy) and '
        '[`ISSUES.md`](ISSUES.md) (where it matches legacy on purpose).', '']


def cell(s):
    return str(s).replace('|', '/').replace('\n', ' ')


def issues(side):
    key = lambda x: (R.ISSUE_STATUS[x[0]][0] != 'Major', ORDER[R.ISSUE_STATUS[x[0]][1]], int(x[0][1:]))
    return sorted([x for x in R.ISSUES if R.ISSUE_LEGACY[x[0]] == side], key=key)


def issue_table(items):
    out = ['| ID | Severity | Status | Issue | What | Next step | Where |', '|---|---|---|---|---|---|---|']
    for i, title, desc, where in items:
        sev, st, nxt = R.ISSUE_STATUS[i]
        out.append(f'| {i} | {sev} | {st} | **{cell(title)}** | {cell(desc)} | {cell(nxt)} | {cell(where)} |')
    return out


def bug_table(rows):
    out = ['| ID | Priority | In legacy 465 | Bug | Where in legacy | Fix | In the prototype |',
           '|---|---|---|---|---|---|---|']
    for lid, title, where, _what, fix, _eff in rows:
        out.append(f'| {lid} | {F.PRIORITY[lid]} | {F.legacy465(lid)} | {cell(title)} | {cell(where)} | {cell(fix)} | '
                   f'{F.mvp_status(lid)} |')
    return out


def ld_table(rows):
    out = ['| Row | Area | Type | Legacy | This model | Effect |', '|---|---|---|---|---|---|']
    for k, d in rows:
        out.append(f'| LD{k} | {cell(d[0])} | {d[5]} | {cell(d[1])} | {cell(d[2])} | {cell(d[4])} |')
    return out


def main():
    bugs = sorted(F.bugs(), key=lambda b: (F.ORDER[F.PRIORITY[b[0]]], int(b[0][1:])))
    b_not = [b for b in bugs if b[0] not in R.BUGS_REPLICATED]
    b_rep = [b for b in bugs if b[0] in R.BUGS_REPLICATED]
    i_not, i_rep, i_mvp = issues('not replicated'), issues('replicated'), issues('mvp')
    lds = list(enumerate(B.LEGACY_DIFFS, 1))
    ld_not = [(k, d) for k, d in lds if d[5] in DEPART and k not in R.LD_REPLICATED]
    ld_rep = [(k, d) for k, d in lds if k in R.LD_REPLICATED]
    n_same = sum(1 for _k, d in lds if d[5] == 'Same')
    n_open = sum(1 for x in i_not if R.ISSUE_STATUS[x[0]][1] == 'Open')

    no = [f'# NOT REPLICATED (mostly bugs): where CPAT-AI-Mitigation-Prototype v{B.VERSION} departs from legacy CPAT', ''] + RULE
    no += [f'**{len(b_not)} legacy bugs not replicated; {len(i_not)} tracked issues not replicated ({n_open} open: '
           f'queued to be replicated), and {len(ld_not)} departures in sheet LegacyDiff.**', '',
           '## 1. Bugs not replicated', '',
           'Legacy bugs the prototype fixes, or whose feature it leaves out. Legacy CPAT still needs the fixes, except '
           'where column "In legacy 465" says Fixed (the CPAT team fixed them in CPAT 1.0pre_465; checked cell by cell): '
           f'details and effects in the register `CPAT-AI_BugsAndIssues_latest.docx`.', ''] + bug_table(b_not)
    no += ['', '## 2. Issues not replicated (exceptions)', '',
           'Departures from legacy that are not bug fixes. Each one is either a user decision (Accepted) or open and '
           'queued to be replicated (TODO).', '', '### 2a. Tracked issues', ''] + issue_table(i_not)
    no += ['', '### 2b. Every departure in sheet LegacyDiff', '',
           'The workbook sheet LegacyDiff (tab Version Log and Reference) records every difference with legacy. These '
           'rows are departures that are not bug fixes (bug fixes are part 1); the major ones are tracked in 2a.',
           ''] + ld_table(ld_not)

    re = [f'# REPLICATED (mostly issues): where CPAT-AI-Mitigation-Prototype v{B.VERSION} matches legacy CPAT on purpose',
          ''] + RULE
    re += [f'**{len(i_rep)} tracked issues replicated; {len(b_rep)} legacy bug{"s" if len(b_rep) != 1 else ""} still replicated (to fix); '
           f'{len(i_mvp)} issues of the prototype itself. A further {n_same} rows of sheet LegacyDiff are "Same" as legacy.**',
           '', '## 1. Issues replicated', '',
           'Legacy behaviour the prototype copies although it is open to question. Kept to match legacy; tracked here.', '']
    re += issue_table(i_rep) + ['', 'Rows of sheet LegacyDiff kept as legacy:', ''] + ld_table(ld_rep)
    re += ['', '## 2. Bugs replicated (to fix)', '',
           'Legacy bugs the prototype still copies. The rule says no bug is replicated, so each one is queued to be fixed '
           '(TODO).', ''] + (bug_table(b_rep) if b_rep else
                             ['None: every legacy bug in the register is fixed (since v4.10).'])
    re += ['', '## 3. Issues of the prototype itself (no legacy counterpart)', '',
           'Limitations of the workbook and its tooling; nothing to replicate.', ''] + issue_table(i_mvp)

    for side, lines in (('not', no), ('rep', re)):
        text = '\n'.join(lines) + '\n'
        for path in (os.path.join(TOP, FILES[side][1]),):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
    print(f'not replicated: {len(b_not)} bugs, {len(i_not)} issues ({n_open} open), {len(ld_not)} LegacyDiff rows; '
          f'replicated: {len(i_rep)} issues, {len(b_rep)} bugs, {len(ld_rep)} LegacyDiff rows; prototype: {len(i_mvp)}')


if __name__ == '__main__':
    main()
