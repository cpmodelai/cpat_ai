"""Update the CPAT team's tracker legacy/workbooks/Tracking issues.xlsx from the register (user 2026-10-18: "I put
a bug tracker in legacy folder. You could edit that by adding extra rows and extra columns. Continue to use our
codes").

Sheet BUGSandISSUES (an export of our register, v3.18): every row is refreshed from BUGSandISSUES.xlsx (run
make_replication_lists and make_bugs_issues_sheet first); codes no longer in the register stay, marked "Retired"
with where they went; new codes (later legacy bugs, distribution bugs D and issues DI, prototype bugs M) are
appended. Extra columns: type (as the Word bug list), code group, prototype version that settled it, cell-level fix plan,
status in the 459 legacy file, related items of the team's own sheets, last update.

The team's sheets (CPAT_issues, Mit+Disn_DeepDive, MT_issues, Slicer_issues) keep their content and get two extra
columns: our code(s) and a short note, from data/tracker_mapping.json (or the file given as the first argument;
JSON {sheet: {item number: {"codes": [...], "note": "..."}}, "new_codes": [...]}; keys "Dist n" for the second
table of Mit+Disn_DeepDive, "General n" for its numbered general concerns). The new codes the mapping proposed are
in the register (v5.1: L95-L97, D9).

    python update_tracker.py [mapping.json]
"""
import copy
import json
import os
import re
import sys

import openpyxl
from openpyxl.styles import Alignment, Font

import issues_register as R
import make_bugfix_book as BK

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = '7.0'
TRACKER = os.path.join(HERE, '..', 'legacy', 'workbooks', 'Tracking issues.xlsx')
SHEET_SRC = os.path.join(HERE, '..', 'CPAT-AI_BugsAndIssues_latest.xlsx')
HEAD = 3                                                   # header row of BUGSandISSUES
BASE = 11                                                  # columns A-K: as our register export
EXTRA = ['Type', 'Code group', 'Settled in (prototype version)', 'Cell-level fix plan', 'Status in legacy 459',
         'Related CPAT team items', 'Updated']
EXTRA_W = [18, 20, 14, 12, 18, 26, 12]
MAPPING = os.path.join(HERE, '..', '..', 'data', 'mvp_legacy_extracts', 'tracker_mapping.json')   # team items -> our codes (kept with the register)
TEAM = ['CPAT_issues', 'Mit+Disn_DeepDive', 'MT_issues', 'Slicer_issues']
GROUP = {'L': 'Legacy bug (mitigation)', 'D': 'Legacy bug (distribution)', 'DI': 'Issue (distribution)',
         'I': 'Issue (mitigation)', 'M': 'Prototype bug', 'LD': 'LegacyDiff row'}


def group(code):
    return GROUP[re.match(r'[A-Z]+', code).group(0)]


def order(code):
    pre = {'L': 0, 'D': 1, 'M': 2, 'I': 3, 'DI': 4, 'LD': 5}
    return pre[re.match(r'[A-Z]+', code).group(0)], int(re.search(r'\d+', code).group(0))


def current_rows():
    """{code: 11 values} of the register sheet, plus the distribution and prototype bugs and distribution issues."""
    ws = openpyxl.load_workbook(SHEET_SRC)['BUGSandISSUES']
    rows = {r[0]: list(r[:BASE]) for r in ws.iter_rows(min_row=HEAD + 1, values_only=True) if r[0]}
    for c, t, w, what, st in R.DIST_BUGS:
        rows.setdefault(c, [c, 'Legacy bug (distribution)', 'Low', t, 'No', 'Fixed', what, '', st, w, 'Closed'])
    for c, t, d, st in R.DIST_ISSUES:
        rows.setdefault(c, [c, 'Issue (distribution)', '', t, 'Yes' if st.startswith('Replicated') else 'No', st,
                            d, '', '', 'Methods, chapter Distribution', 'Open' if st.startswith('Replicated') else
                            'Closed'])
    for c, t, when, what, fix in R.MVP_BUGS:
        rows.setdefault(c, [c, 'Prototype bug', '', t, 'n/a', 'Fixed', what, '', fix, f'prototype {when}', 'Closed'])
    return rows


def successor(code):
    """Where a code that left the register went (from the register's own text 'was issue I8' etc.)."""
    pat = re.compile(rf'was (?:issue )?{code}\b')
    for c, t, *rest in R.LEGACY:
        if any(pat.search(str(x)) for x in rest):
            return f'Retired: now {c} ({t})'
    for row in getattr(R, 'UPGRADES', []):
        if any(pat.search(str(x)) for x in row[1:]):
            return f'Retired: now {row[0]} ({row[1]})'
    m = re.search(rf'{code} (v\d+\.\d+)', ' '.join(str(v) for v in R.ISSUE_STATUS.values()))
    if m:
        return f'Retired: replicated {m.group(1)} (closed)'
    if code.startswith('LD'):
        k = int(code[2:])
        if k <= len(BK.B.LEGACY_DIFFS):
            typ = BK.B.LEGACY_DIFFS[k - 1][5]
            return ('Retired: now as legacy (LegacyDiff "Same", closed)' if typ == 'Same' else
                    f'Retired: LegacyDiff "{typ}": a legacy bug fixed (see its L code)')
    return 'Retired: closed'


def type_of(code, kind):
    if code.startswith('L') and not code.startswith('LD'):
        return BK.TYPE_NAME[BK.bug_type(code)]
    if code.startswith('D'):
        return 'Distribution'
    if code.startswith('M'):
        return 'Prototype'
    return 'Issue' if code.startswith('I') else 'LegacyDiff'


def settled(values):
    m = re.search(r'\bv(\d+\.\d+)\b', ' '.join(str(v or '') for v in values[5:]))
    return m.group(1) if m else ''


def related(code, mapping):
    out = []
    for sheet in TEAM:
        for num, m in (mapping.get(sheet) or {}).items():
            if code in m.get('codes', []):
                out.append(f'{sheet} {num}')
    return '; '.join(out)


def style_like(ws, src_row, dst_row, ncols):
    for j in range(1, ncols + 1):
        s, d = ws.cell(src_row, j), ws.cell(dst_row, j)
        if s.has_style:
            d.font, d.fill, d.border = copy.copy(s.font), copy.copy(s.fill), copy.copy(s.border)
            d.alignment, d.number_format = copy.copy(s.alignment), s.number_format


def update_register_sheet(wb, mapping, plans):
    ws = wb['BUGSandISSUES']
    ncol = BASE + len(EXTRA)
    for j, (h, w) in enumerate(zip(EXTRA, EXTRA_W), BASE + 1):
        c = ws.cell(HEAD, j, h)
        src = ws.cell(HEAD, BASE)
        c.font, c.fill, c.border, c.alignment = (copy.copy(src.font), copy.copy(src.fill), copy.copy(src.border),
                                                 copy.copy(src.alignment))
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    cur = current_rows()
    seen, last = set(), HEAD
    for r in range(HEAD + 1, ws.max_row + 1):
        code = ws.cell(r, 1).value
        if not code:
            continue
        last = r
        seen.add(code)
        vals = cur.get(code)
        if vals is None:                                    # left the register: kept, marked
            ws.cell(r, BASE).value = successor(code)
            vals = [ws.cell(r, j).value for j in range(1, BASE + 1)]
        else:
            for j, v in enumerate(vals, 1):
                ws.cell(r, j).value = v
        fill_extra(ws, r, code, vals, mapping, plans, retired=code not in cur)
    for code in sorted((c for c in cur if c not in seen), key=order):
        last += 1
        style_like(ws, HEAD + 1, last, ncol)
        for j, v in enumerate(cur[code], 1):
            ws.cell(last, j).value = v
        fill_extra(ws, last, code, cur[code], mapping, plans, retired=False)
    for r in range(HEAD + 1, last + 1):
        for j in range(BASE + 1, ncol + 1):
            if not ws.cell(r, j).has_style:
                s = ws.cell(r, BASE)
                ws.cell(r, j).font, ws.cell(r, j).border = copy.copy(s.font), copy.copy(s.border)
                ws.cell(r, j).alignment = copy.copy(s.alignment)
    ws.auto_filter.ref = f'A{HEAD}:{openpyxl.utils.get_column_letter(ncol)}{last}'
    ws['A1'].value = (f'Bugs and issues of legacy CPAT and whether CPAT-AI-Mitigation-Prototype v{VERSION} replicates them '
                      '(our codes: L legacy bugs, D distribution bugs, I issues, DI distribution issues, M prototype '
                      'bugs, LD LegacyDiff rows)')
    ws['A2'].value = (f'Updated from the register (issues_register.py) by '
                      'update_tracker.py. Details, fix procedure and cell-level plans: '
                      'excel_ai/CPAT-AI_BugsAndIssues_latest.docx. Columns L-R added. Codes '
                      'are keyed to legacy file 456; the 459 file is not reconciled yet.')
    ws['A2'].font = Font(name='Arial', size=9, italic=True)
    return last - HEAD


def fill_extra(ws, r, code, vals, mapping, plans, retired):
    legacy = re.match(r'(L|D|I|DI)\d', code) and not code.startswith('LD')
    extra = [type_of(code, vals[1]), group(code), settled(vals),
             'Yes' if code in plans else '', 'Not reconciled yet' if legacy and not retired else 'n/a',
             related(code, mapping), f'v{VERSION}']
    for j, v in enumerate(extra, BASE + 1):
        ws.cell(r, j).value = v
        ws.cell(r, j).alignment = Alignment(wrap_text=True, vertical='top')


def update_team_sheets(wb, mapping):
    n = 0
    for sheet in TEAM:
        if sheet not in wb.sheetnames or sheet not in mapping:
            continue
        ws = wb[sheet]
        hr = next(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value)    # header: first filled row
        heads = [ws.cell(hr, j).value for j in range(1, ws.max_column + 1)]
        if 'CPAT-AI code(s)' in heads:                       # rerun: the columns of the previous update
            ca = heads.index('CPAT-AI code(s)') + 1
            width, cb = ca - 1, ca + 1
        else:
            width = max(j for j in range(1, ws.max_column + 1) if ws.cell(hr, j).value)
            ca, cb = width + 1, width + 2
        for j, h in ((ca, 'CPAT-AI code(s)'), (cb, 'CPAT-AI note')):
            ws.cell(hr, j, h)
            src = ws.cell(hr, width)
            ws.cell(hr, j).font, ws.cell(hr, j).fill = copy.copy(src.font), copy.copy(src.fill)
            ws.cell(hr, j).border, ws.cell(hr, j).alignment = copy.copy(src.border), copy.copy(src.alignment)
        ws.column_dimensions[openpyxl.utils.get_column_letter(ca)].width = 16
        ws.column_dimensions[openpyxl.utils.get_column_letter(cb)].width = 48
        m = {str(k).strip(): v for k, v in mapping[sheet].items()}
        head, part = str(ws.cell(hr, 1).value), ''
        for r in range(hr + 1, ws.max_row + 1):
            a_, b_ = ws.cell(r, 1).value, str(ws.cell(r, 2).value or '')
            if a_ is not None and str(a_) == head:          # a second table (Mit+Disn_DeepDive: distribution)
                part = 'Dist '
                continue
            if a_ is None and re.match(r'\d+\.', b_):           # numbered lines without a number in A (General)
                key = 'General ' + b_.split('.')[0]
            else:
                key = (part + str(a_).strip()) if a_ is not None else ''
            if key in m:
                ws.cell(r, ca).value = ', '.join(m[key].get('codes', [])) or '-'
                ws.cell(r, cb).value = m[key].get('note', '')
                for j in (ca, cb):
                    ws.cell(r, j).alignment = Alignment(wrap_text=True, vertical='top')
                    ws.cell(r, j).font = copy.copy(ws.cell(r, width).font)
                n += 1
    return n


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else MAPPING
    mapping = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {}
    wb = openpyxl.load_workbook(TRACKER)
    rows = update_register_sheet(wb, mapping, BK.plans())
    n = update_team_sheets(wb, mapping)
    wb.save(TRACKER)
    print(f'updated {TRACKER}: BUGSandISSUES {rows} rows; team items mapped {n}')


if __name__ == '__main__':
    main()
