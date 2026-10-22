"""BUGSandISSUES.xlsx: one consolidated table of legacy bugs, issues and departures, with a column that says
whether the prototype (CPAT-AI-Mitigation-Prototype) replicates each one.

Source: the two generated lists at the top of excel_ai/ (BUGS.md, ISSUES.md),
which make_replication_lists.py writes from the register (issues_register.py) at every release. Regenerate
those first, then run this (plain Python with openpyxl; it does not import the builder):

    python make_bugs_issues_sheet.py
"""
import os
import re
from collections import Counter

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.join(HERE, '..')
VERSION = '7.0'
OUT = os.path.join(HERE, '..', 'CPAT-AI_BugsAndIssues_latest.xlsx')   # v8.0: the register spreadsheet, excel_ai/

COLS = ['Ref', 'Kind', 'Priority / severity', 'Title', 'Replicated in the prototype?', 'How in the prototype',
        'What legacy does', 'Effect', 'Fix / next step', 'Where in legacy / documented', 'Status']
WIDTH = [8, 22, 12, 46, 20, 28, 60, 44, 52, 38, 12]


def tables(path):
    """Yield (section heading, header cells, list of row cells) for every markdown table in the file."""
    sec, header, rows = '', None, []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('#'):
                if header:
                    yield sec, header, rows
                sec, header, rows = line.lstrip('# ').strip(), None, []
            elif line.startswith('|'):
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                if header is None:
                    header = cells
                elif not re.match(r'^-+$', cells[0]):
                    rows.append(cells)
            elif header and not line.strip():
                yield sec, header, rows
                header, rows = None, []
    if header:
        yield sec, header, rows


def row(ref, kind, prio, title, rep, how, what, fix, where, status, effect=''):
    return [ref, kind, prio, title, rep, how, what, effect, fix, where, status]


def details():
    """ID -> (what legacy does, effect) from the Details part of LegacyBugFixes.md."""
    out, cur = {}, None
    with open(os.path.join(HERE, 'LegacyBugFixes.md'), encoding='utf-8') as f:
        for line in f:
            m = re.match(r'\*\*(L\d+) \(', line)
            if m:
                cur = m.group(1)
                out[cur] = ['', '']
            elif cur and line.startswith('- Legacy:'):
                out[cur][0] = line[len('- Legacy:'):].strip()
            elif cur and line.startswith('- Effect:'):
                out[cur][1] = line[len('- Effect:'):].strip()
    return out


def load():
    out = []
    det = details()
    for fname in ('BUGS.md', 'ISSUES.md'):
        for sec, hdr, rows in tables(os.path.join(TOP, fname)):
            for r in rows:
                d = dict(zip(hdr, r))
                if sec.startswith('1. Bugs not replicated'):
                    how = d['In the prototype']
                    out.append(row(d['ID'], 'Legacy bug', d['Priority'], d['Bug'], 'No',
                                   how if how.lower().startswith(('fixed', 'not built')) else f'Fixed or left out ({how})',
                                   det.get(d['ID'], ['', ''])[0], d['Fix'], d['Where in legacy'], 'Closed',
                                   det.get(d['ID'], ['', ''])[1]))
                elif sec.startswith('2a'):
                    out.append(row(d['ID'], 'Issue (departure from legacy)', d['Severity'], d['Issue'].strip('*'),
                                   'No', {'Accepted': 'Departs from legacy by decision',
                                          'Dropped': 'Departs from legacy: dropped by the user (v6.1)'}.get(
                                       d['Status'], 'Departs from legacy; queued to replicate'),
                                   d['What'], d['Next step'], d['Where'], d['Status']))
                elif sec.startswith('2b'):
                    out.append(row(d['Row'], 'LegacyDiff departure', d['Type'], d['Area'], 'No',
                                   'Departs from legacy: ' + d['This model'], 'Legacy: ' + d['Legacy'],
                                   '', 'Sheet LegacyDiff', '', d['Effect']))
                elif sec.startswith('1. Issues replicated') and 'ID' in d:
                    out.append(row(d['ID'], 'Issue (replicated)', d['Severity'], d['Issue'].strip('*'), 'Yes',
                                   'Kept as legacy, tracked', d['What'], d['Next step'], d['Where'], d['Status']))
                elif sec.startswith('1. Issues replicated'):
                    out.append(row(d['Row'], 'LegacyDiff, kept as legacy', d['Type'], d['Area'], 'Yes',
                                   'Kept as legacy: ' + d['This model'], 'Legacy: ' + d['Legacy'], '',
                                   'Sheet LegacyDiff', '', d['Effect']))
                elif sec.startswith('2. Bugs replicated'):
                    out.append(row(d['ID'], 'Legacy bug', d['Priority'], d['Bug'], 'Yes (bug, to fix)',
                                   'Copied from legacy; queued to be fixed', '', d['Fix'], d['Where in legacy'],
                                   'Open'))
                elif sec.startswith('3. Issues of the prototype'):
                    out.append(row(d['ID'], 'Issue of the prototype', d['Severity'], d['Issue'].strip('*'),
                                   'n/a (no legacy counterpart)', 'Limitation of the workbook and its tooling',
                                   d['What'], d['Next step'], d['Where'], d['Status']))
    import issues_register as R         # v6.1: the distribution register and prototype bugs (as the tracker)
    for c, t, w, what, st in R.DIST_BUGS:
        out.append(row(c, 'Legacy bug (distribution)', 'Low', t, 'No', 'Fixed', what, st, w, 'Closed'))
    for c, t, d_, st in R.DIST_ISSUES:
        rep = st.startswith('Replicated')
        out.append(row(c, 'Issue (distribution)', '', t, 'Yes' if rep else 'No', st, d_, '',
                       'Distribution_Method.md', 'Open' if rep else 'Closed'))
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
    data = sorted(load(), key=sort_key)
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
        'Source: BUGS.md and ISSUES.md (generated from issues_register.py). '
        'Not included: potential upgrades (U), and bugs found and fixed in the prototype during development (M); both are '
        'in the Word register CPAT-AI_BugsAndIssues_v7.0.docx. Details and effects of the legacy '
        'bugs: LegacyBugFixes.md.',
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
    print(f'{len(data)} rows -> {OUT}')
    for k in kinds:
        print(f'  {k}: ' + ', '.join(f'{v}={cnt[(k, v)]}' for v in ('Yes', 'No', 'n/a') if cnt[(k, v)]))


if __name__ == '__main__':
    main()
