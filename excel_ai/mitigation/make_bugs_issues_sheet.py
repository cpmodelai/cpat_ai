"""CPAT-AI_BugsAndIssues_latest.xlsx: one consolidated table of legacy bugs, issues and departures, with a column
that says whether the prototype (CPAT-AI-Mitigation-Prototype) replicates each one, and the status of each legacy bug in
the latest legacy file (465).

Source (v8.2): the register itself, through make_replication_lists.parts() (the content of BUGS.md and ISSUES.md) and
make_legacy_fixes (what legacy does, the effect); before v8.2 it parsed BUGS.md, ISSUES.md and LegacyBugFixes.md.

    python make_bugs_issues_sheet.py
"""
import json
import os
import re
import sys
from collections import Counter

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.join(HERE, '..')
VERSION = json.load(open(os.path.join(HERE, 'version.json')))['version']   # v8.2: was a fixed '7.0'
CHECK465 = os.path.join(HERE, '..', 'bugsfixed', 'legacy465_check.json')   # v8.2: the CPAT team's fixes in 465
OUT = os.path.join(HERE, '..', 'CPAT-AI_BugsAndIssues_latest.xlsx')   # v8.0: the register spreadsheet, excel_ai/

COLS = ['Ref', 'Kind', 'Priority / severity', 'Title', 'Replicated in the prototype?', 'How in the prototype',
        'What legacy does', 'Effect', 'Fix / next step', 'Where in legacy / documented', 'Status',
        'Status in legacy 465']
WIDTH = [8, 22, 12, 46, 20, 28, 60, 44, 52, 38, 12, 22]


def legacy465(ref, kind):
    """v8.2: a legacy bug in legacy CPAT 1.0pre_465: Open, or the check of the CPAT team's fix; '' for the rest."""
    if not kind.startswith('Legacy bug'):
        return ''
    chk = json.load(open(CHECK465, encoding='utf-8'))['bugs'] if os.path.exists(CHECK465) else {}
    return {'Confirmed fixed': 'Fixed', 'Fixed with caveats': 'Fixed with caveats',
            'Not fixed': 'Not fixed (marked fixed)'}.get(chk.get(ref, {}).get('status'), 'Open')


def row(ref, kind, prio, title, rep, how, what, fix, where, status, effect=''):
    return [ref, kind, prio, title, rep, how, what, effect, fix, where, status]


def load():
    """v8.2: straight from the register (make_replication_lists.parts(), the data of BUGS.md and ISSUES.md, and
    make_legacy_fixes for what legacy does and the effect); it parsed the two lists and LegacyBugFixes.md before.
    Texts as in the lists (cell(): no "|" or line breaks), so the sheet is unchanged."""
    import make_legacy_fixes as F
    import make_replication_lists as L
    import issues_register as R
    t = lambda x: L.cell(x).strip()
    p = L.parts()
    out = []
    for lid, title, where, what, fix, eff in p['b_not']:
        how = F.mvp_status(lid)
        out.append(row(lid, 'Legacy bug', F.PRIORITY[lid], t(title), 'No',
                       how if how.lower().startswith(('fixed', 'not built')) else f'Fixed or left out ({how})',
                       what.strip(), t(fix), t(where), 'Closed', eff.strip()))
    for i, title, desc, where in p['i_not']:
        sev, st, nxt = R.ISSUE_STATUS[i]
        out.append(row(i, 'Issue (departure from legacy)', sev, t(title), 'No',
                       {'Accepted': 'Departs from legacy by decision',
                        'Dropped': 'Departs from legacy: dropped by the user (v6.1)'}.get(
                           st, 'Departs from legacy; queued to replicate'), t(desc), t(nxt), t(where), st))
    for k, d in p['ld_not']:
        out.append(row(f'LD{k}', 'LegacyDiff departure', d[5], t(d[0]), 'No', 'Departs from legacy: ' + t(d[2]),
                       'Legacy: ' + t(d[1]), '', 'Sheet LegacyDiff', '', t(d[4])))
    for i, title, desc, where in p['i_rep']:
        sev, st, nxt = R.ISSUE_STATUS[i]
        out.append(row(i, 'Issue (replicated)', sev, t(title), 'Yes', 'Kept as legacy, tracked', t(desc), t(nxt),
                       t(where), st))
    for k, d in p['ld_rep']:
        out.append(row(f'LD{k}', 'LegacyDiff, kept as legacy', d[5], t(d[0]), 'Yes', 'Kept as legacy: ' + t(d[2]),
                       'Legacy: ' + t(d[1]), '', 'Sheet LegacyDiff', '', t(d[4])))
    for lid, title, where, _what, fix, _eff in p['b_rep']:
        out.append(row(lid, 'Legacy bug', F.PRIORITY[lid], t(title), 'Yes (bug, to fix)',
                       'Copied from legacy; queued to be fixed', '', t(fix), t(where), 'Open'))
    for i, title, desc, where in p['i_mvp']:
        sev, st, nxt = R.ISSUE_STATUS[i]
        out.append(row(i, 'Issue of the prototype', sev, t(title), 'n/a (no legacy counterpart)',
                       'Limitation of the workbook and its tooling', t(desc), t(nxt), t(where), st))
                                        # v6.1: the distribution register and prototype bugs (as the tracker)
    for c, t, w, what, st in R.DIST_BUGS:
        out.append(row(c, 'Legacy bug (distribution)', 'Low', t, 'No', 'Fixed', what, st, w, 'Closed'))
    for c, t, d_, st in R.DIST_ISSUES:
        rep = st.startswith('Replicated')
        out.append(row(c, 'Issue (distribution)', '', t, 'Yes' if rep else 'No', st, d_, '',
                       'Methods, chapter Distribution', 'Open' if rep else 'Closed'))
    for c, t, when, what, fix in R.MVP_BUGS:
        out.append(row(c, 'Prototype bug', '', t, 'n/a', 'Fixed', what, fix, f'prototype {when}', 'Closed'))
    return out


def sort_key(r):
    kind_order = {'Legacy bug': 0, 'Issue (departure from legacy)': 1, 'Issue (replicated)': 2,
                  'LegacyDiff departure': 3, 'LegacyDiff, kept as legacy': 4, 'Issue of the prototype': 5,
                  'Legacy bug (distribution)': 6, 'Issue (distribution)': 7, 'Prototype bug': 8}   # v6.1
    m = re.match(r'([A-Z]+)(\d+)', r[0])
    return kind_order[r[1]], m.group(1), int(m.group(2))


def main():
    data = [r + [legacy465(r[0], r[1])] for r in sorted(load(), key=sort_key)]
    refs = [r[0] for r in data]
    assert len(refs) == len(set(refs)), [k for k, v in Counter(refs).items() if v > 1]

    wb = Workbook()
    thin = Side(style='thin', color='BFBFBF')
    fill = {'Yes': 'EBF1DE', 'No': 'FFF2CC', 'n/a': 'F2F2F2'}
    base = Font(name='Arial', size=10)

    # --- README / rule + counts
    ws0 = wb.active
    ws0.title = 'ReadMe'
    ws0['A1'] = f'BUGSandISSUES: CPAT-AI-Mitigation-Prototype v{VERSION} against legacy CPAT'
    ws0['A1'].font = Font(name='Arial', size=14, bold=True, color='FFFFFF')
    for c in range(1, 7):
        ws0.cell(1, c).fill = PatternFill('solid', fgColor='00B050')
    lines = [
        'Rule (user, 2026-10-15): bugs are never replicated (the prototype fixes them or leaves the feature out); issues '
        'are replicated (the prototype does what legacy does, and tracks the issue). A departure from legacy that is not '
        'a bug fix stays only by user decision; otherwise it is queued to be replicated.',
        'Bug = legacy does not do what it means to (wrong row, double application, dead reference). '
        'Issue = legacy does what it means to, but the choice is open to question.',
        'One row per item in sheet BUGSandISSUES. Column "Replicated in the prototype?": Yes = the prototype matches '
        'legacy; No = it departs (fixed, left out, or a decided/queued departure); n/a = the item is about the prototype '
        'itself. Filter on Kind and on that column.',
        'Source: the register (issues_register.py; the same content as BUGS.md and ISSUES.md). '
        'Not included: potential upgrades (U), and bugs found and fixed in the prototype during development (M); both are '
        'in the Word register CPAT-AI_BugsAndIssues_latest.docx. Details and effects of the legacy '
        'bugs: LegacyBugFixes.md. Column "Status in legacy 465": the legacy bugs in the latest CPAT file '
        '(CPAT 1.0pre_465), where the CPAT team fixed part of them (checked cell by cell); cell references are 465 rows.',
    ]
    for i, t in enumerate(lines, 3):
        ws0.cell(i, 1, t).alignment = Alignment(wrap_text=True, vertical='top')
        ws0.cell(i, 1).font = base
        ws0.merge_cells(start_row=i, start_column=1, end_row=i, end_column=6)
        ws0.row_dimensions[i].height = 48
    ws0['A8'] = 'Summary'
    ws0['A8'].font = Font(name='Arial', size=11, bold=True, underline='single')
    kinds = []
    for r in data:
        if r[1] not in kinds:
            kinds.append(r[1])
    cnt = Counter((r[1], r[4].split(' ')[0] if r[4] != 'n/a (no legacy counterpart)' else 'n/a') for r in data)
    hdr = ['Kind', 'Replicated (Yes)', 'Not replicated (No)', 'n/a', 'Total']
    for c, h in enumerate(hdr, 1):
        cell = ws0.cell(9, c, h)
        cell.font = Font(name='Arial', size=10, bold=True)
        cell.border = Border(bottom=thin)
    for i, k in enumerate(kinds, 10):
        y, n, na = cnt[(k, 'Yes')], cnt[(k, 'No')], cnt[(k, 'n/a')]
        for c, v in enumerate([k, y, n, na, y + n + na], 1):
            ws0.cell(i, c, v).font = base
    t = 10 + len(kinds)
    ws0.cell(t, 1, 'All').font = Font(name='Arial', size=10, bold=True)
    for c in range(2, 6):
        col = get_column_letter(c)
        cell = ws0.cell(t, c, f'=SUM({col}10:{col}{t - 1})')
        cell.font = Font(name='Arial', size=10, bold=True)
    ws0.column_dimensions['A'].width = 34
    for col in 'BCDEF':
        ws0.column_dimensions[col].width = 20

    # --- the table
    ws = wb.create_sheet('BUGSandISSUES')
    ws['A1'] = f'Bugs and issues of legacy CPAT and whether CPAT-AI-Mitigation-Prototype v{VERSION} replicates them'
    ws['A1'].font = Font(name='Arial', size=14, bold=True, color='FFFFFF')
    for c in range(1, len(COLS) + 1):
        ws.cell(1, c).fill = PatternFill('solid', fgColor='00B050')
    for c, h in enumerate(COLS, 1):
        cell = ws.cell(3, c, h)
        cell.font = Font(name='Arial', size=10, bold=True)
        cell.fill = PatternFill('solid', fgColor='EBF1DE')
        cell.border = Border(bottom=thin)
        cell.alignment = Alignment(wrap_text=True, vertical='top')
        ws.column_dimensions[get_column_letter(c)].width = WIDTH[c - 1]
    for i, r in enumerate(data, 4):
        for c, v in enumerate(r, 1):
            cell = ws.cell(i, c, v)
            cell.font = base
            cell.alignment = Alignment(wrap_text=True, vertical='top')
            cell.border = Border(bottom=Side(style='hair', color='BFBFBF'))
        key = r[4].split(' ')[0] if not r[4].startswith('n/a') else 'n/a'
        ws.cell(i, 5).fill = PatternFill('solid', fgColor=fill[key])
        ws.cell(i, 5).font = Font(name='Arial', size=10, bold=True)
    ws.freeze_panes = 'E4'
    ws.auto_filter.ref = f'A3:{get_column_letter(len(COLS))}{3 + len(data)}'
    wb.save(OUT)
    sys.path.insert(0, os.path.join(HERE, '..', 'shared'))
    import excel_lint
    excel_lint.check(OUT)                   # NORMS 3g
    print(f'{len(data)} rows -> {OUT}')
    for k in kinds:
        print(f'  {k}: ' + ', '.join(f'{v}={cnt[(k, v)]}' for v in ('Yes', 'No', 'n/a') if cnt[(k, v)]))


if __name__ == '__main__':
    main()
