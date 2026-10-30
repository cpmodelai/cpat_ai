"""Tracking_Legacy_Bugs_v<version>.xlsx (excel_ai/): the master list of bugs and issues (v0.8.4, user 2026-10-28).

The CPAT team's tracker (was excel_ai/legacy/Tracking issues.xlsx) with three tabs in front, written from the register
(register.py): ReadMe (the rule, the codes, where each item is documented), Bugs (L legacy bugs, M prototype bugs)
and Issues (I issues, data included; LD departures; U upgrades). Every module in the same columns: the
team's columns A-I (as on CPAT_issues), then ours. The team's own tabs are kept as they are: the tabs are written
into the file's XML, so threaded comments and the rest of the team's file survive.

Source: the latest Tracking_Legacy_Bugs_v*.xlsx (top of excel_ai/ or releases/), else legacy/Tracking issues.xlsx.
The columns Date, CPAT Version with identified issue and Issue raised by of tab Bugs are read back from the source, so
an edit there is kept.

    python make_tracker.py
"""
import os as _os, sys as _sys  # the excel_ai code folders and data/scripts on the path (core/tools/xlpaths.py)
_xl = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_xl) != 'excel_ai':
    _xl = _os.path.dirname(_xl)
_sys.path.insert(0, _os.path.join(_xl, 'core', 'tools'))
import xlpaths  # noqa: E402,F401
import glob
import os
import re
import shutil
import sys
import tempfile
import zipfile
from xml.sax.saxutils import escape

import build as B
import issues_register as R
import register as G

HERE = xlpaths.MIT                     # excel_ai/mitigation/ (the script sits in a subfolder)
XL = os.path.join(HERE, '..')
NAME = 'Tracking_Legacy_Bugs'
OUT = B.REL.versioned(NAME, R.REGISTER_VERSION, 'xlsx')
OLD = os.path.join(XL, 'legacy', 'Tracking issues.xlsx')
OURS = ('ReadMe', 'Bugs', 'Issues', 'CPAT-AI_bugs')        # tabs written here (CPAT-AI_bugs: the tab before v0.8.4)

# style indices of the team's xl/styles.xml (as on CPAT_issues): header, centred, wrapped, Fixed = Solved / In progress / No
S_HEAD, S_HEAD_WRAP, S_CENTRE, S_WRAP = 1, 23, 4, 3
S_FIXED = {'Solved': 19, 'In progress': 20, 'No': 21}
COLS = [  # header, style of the values, width; A-I are the team's columns of CPAT_issues
    ('Number', S_CENTRE, 8.9), ('Issues', S_WRAP, 60), ('CPAT Version with identified issue', S_CENTRE, 12),
    ('Date', S_CENTRE, 11), ('Materiality/Priority', S_CENTRE, 11), ('Fixed', S_CENTRE, 11.3),
    ('Issue raised by', 0, 14.6), ('Issue solved by', 0, 16), ('Additional comments', S_WRAP, 60),
    ('Kind', S_CENTRE, 12), ('Former code', S_CENTRE, 9), ('Module', S_CENTRE, 14), ('Area', S_WRAP, 18),
    ('In the prototype', S_WRAP, 30), ('Status', S_CENTRE, 11), ('Legacy 465', S_CENTRE, 14),
    ('Where in legacy', S_WRAP, 26), ('Description', S_WRAP, 70), ('Fix or plan', S_WRAP, 60), ('Effect', S_WRAP, 40),
    ('See also', S_WRAP, 14), ('Documented in', S_WRAP, 26)]
PRI = {'High': '5 (High)', 'Medium': '3 (Medium)', 'Low': '1 (Low)'}
FIXED = {'Fixed': 'Solved', 'Fixed with caveats': 'In progress', 'Not fixed (marked fixed)': 'No', 'Open': 'No'}


def source():
    new = B.REL.all_versions(NAME, 'xlsx')
    return new[-1] if new else OLD


def col(i):
    s = ''
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def comment(r):
    out = []
    st, note = r['legacy465'], r['legacy465_note']
    if r['kind'] == 'Legacy bug':
        out.append({'Fixed': 'Fixed in legacy 465 (checked cell by cell, 2026-10-22)',
                    'Fixed with caveats': 'Fixed with caveats in legacy 465',
                    'Not fixed (marked fixed)': 'Marked fixed by the CPAT team, but not fixed in legacy 465',
                    'Open': 'Open in legacy 465 (not marked fixed by the CPAT team)'}[st] + (f': {note}' if note else '')
                   + '.')
        if r['where']:
            out.append(f'Where: {r["where"]}.')
    return ' '.join(out)


def bug_rows():
    rows = []
    for r in G.records():
        p = G.prefix(r['id'])
        if p not in ('L', 'M', 'DOC'):
            continue
        ver, date, by = (G.found(r['id']) if p == 'L' else ('', '2026-10-29', 'CPAT-AI (Coded CPAT planning)')
                         if p == 'DOC' else ('', '', 'Stephen (CPAT-AI)'))
        fixed = FIXED[r['legacy465']] if p == 'L' else 'No' if p == 'DOC' else 'Solved'
        solved = ('CPAT team (465)' if p == 'L' and fixed != 'No' else 'CPAT-AI (prototype)' if p == 'M' else '')
        rows.append([r['id'], r['title'], ver, date, PRI.get(r['priority'], r['priority']), fixed, by, solved,
                     comment(r), r['kind'], r['former'], r['module'], r['area'], r['prototype'], r['status'],
                     r['legacy465'], r['where'], r['description'], r['fix'], r['effect'], r['see_also'],
                     r['documented']])
    return rows


def issue_rows():
    rows = []
    for r in G.records():
        if G.prefix(r['id']) not in ('I', 'LD', 'U'):
            continue
        rows.append([r['id'], r['title'], '', '', r['priority'], r['status'], '', '', '', r['kind'], r['former'],
                     r['module'], r['area'], r['prototype'], r['status'], '', r['where'], r['description'], r['fix'],
                     r['effect'], r['see_also'], r['documented']])
    return rows


def readme_rows():
    c = G.counts()
    rows = [('Tracking legacy bugs', f'Version {R.REGISTER_VERSION}: the master list of the bugs and issues of legacy '
                                     f'CPAT and the CPAT-AI prototypes (every module). Generated from the register '
                                     f'(excel_ai/legacy/register/register.py) by make_tracker.py; the tabs after Issues are '
                                     f'the CPAT team\'s, kept as they are.'),
            ('The rule', 'Never replicate a legacy bug; always replicate a legacy issue, and track it (NORMS 0). A bug: '
                         'legacy does not compute what it means to; the prototype fixes it. An issue: legacy does what '
                         'it means to, but the choice is open to question; the prototype does the same and tracks '
                         'it. A departure from legacy that is not a bug fix is kept only by user decision.'),
            ('Bugs and issues', 'Bugs are in tab Bugs (L, M, DOC) and in the document Legacy_CPAT_Bugs_v'
                                f'{R.REGISTER_VERSION}.docx (L). Issues are in tab Issues (I, LD, U; data problems: area Data) and in '
                                'the appendices of the Documentation (CPAT-AI-Mitigation_Documentation.docx). Every row '
                                'gives its code, its former code (renumbered in v0.8.4), the codes it relates to (See '
                                'also) and where it is documented.')]
    for p, d, w in G.DEFINITIONS:
        rows.append((f'{p} ({c[p]})', f'{d} Prototype: {w}'))
    rows += [('Columns', 'A-I as the team\'s tab CPAT_issues (Fixed, for a legacy bug: Solved = fixed in legacy 465 '
                         'and confirmed, In progress = fixed with caveats, No = open). J onwards: kind, former code, '
                         'module, area, what the prototype does, status, status in legacy 465, legacy cells, '
                         'description, fix or plan, effect, see also, documented in.'),
             ('Legacy file', 'Cell references are rows of CPAT 1.0pre_465_NoPropData.xlsb.')]
    return rows


def sheet_xml(name, data, header=True, widths=None, selected=False):
    cell = lambda ref, s, v: (f'<c r="{ref}" s="{s}" t="inlineStr"><is><t xml:space="preserve">{escape(str(v))}</t>'
                              '</is></c>' if v not in ('', None) else f'<c r="{ref}" s="{s}"/>')
    body, cols = [], COLS
    if header:
        hdr = [h if not (name == 'Issues' and h == 'Fixed') else 'Status (team column)' for h, _s, _w in cols]
        body.append('<row r="1" ht="28.5" customHeight="1">' +
                    ''.join(cell(f'{col(i)}1', S_HEAD_WRAP, h) for i, h in enumerate(hdr)) + '</row>')
    r0 = 2 if header else 1
    for r, row in enumerate(data, start=r0):
        cells = ''.join(cell(f'{col(i)}{r}', (S_FIXED.get(v, S_CENTRE) if header and i == 5 else
                                              cols[i][1] if header else (S_HEAD if i == 0 else S_WRAP)), v)
                        for i, v in enumerate(row))
        body.append(f'<row r="{r}">{cells}</row>')
    n = len(data[0]) if data else len(cols)
    last = len(data) + r0 - 1
    ws = widths or [w for _h, _s, w in cols]
    cx = ''.join(f'<col min="{i + 1}" max="{i + 1}" width="{w}" customWidth="1"/>' for i, w in enumerate(ws))
    pane = ('<pane xSplit="2" ySplit="1" topLeftCell="C2" activePane="bottomRight" state="frozen"/>'
            '<selection pane="bottomRight" activeCell="C2" sqref="C2"/>' if header else '')
    filt = f'<autoFilter ref="A1:{col(n - 1)}{last}"/>' if header else ''
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheetPr><tabColor rgb="FF1F4E78"/></sheetPr>'
            f'<dimension ref="A1:{col(n - 1)}{max(last, 1)}"/><sheetViews><sheetView '
            f'{"tabSelected=\"1\" " if selected else ""}workbookViewId="0">{pane}</sheetView></sheetViews>'
            '<sheetFormatPr defaultRowHeight="14.25"/>'
            f'<cols>{cx}</cols><sheetData>{"".join(body)}</sheetData>{filt}'
            '<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/></worksheet>')


def main():
    src = source()
    z = zipfile.ZipFile(src)
    parts = {n: z.read(n) for n in z.namelist()}
    order = z.namelist()
    z.close()
    wb = parts['xl/workbook.xml'].decode('utf-8')
    rels = parts['xl/_rels/workbook.xml.rels'].decode('utf-8')
    ct = parts['[Content_Types].xml'].decode('utf-8')
    sheets = re.findall(r'<sheet name="([^"]+)" sheetId="(\d+)"(?: state="\w+")? r:id="(rId\d+)"/>', wb)
    target = lambda rid: 'xl/' + (re.search(rf'Id="{rid}"[^>]*Target="([^"]+)"', rels) or
                                  re.search(rf'Target="([^"]+)"[^>]*Id="{rid}"', rels)).group(1)
    team = [(n, sid, rid) for n, sid, rid in sheets if n not in OURS]
    old_pos = {n: i for i, (n, _s, _r) in enumerate(sheets)}
    for n, _sid, rid in sheets:                         # drop our old tabs (rewritten below)
        if n in OURS:
            p = target(rid)
            order.remove(p)
            parts.pop(p)
            rels = re.sub(rf'<Relationship Id="{rid}"[^>]*/>', '', rels)
            ct = ct.replace(f'<Override PartName="/{p}" ContentType="application/vnd.openxmlformats-officedocument.'
                            'spreadsheetml.worksheet+xml"/>', '')
    data = {'ReadMe': readme_rows(), 'Bugs': bug_rows(), 'Issues': issue_rows()}
    new = []
    nid = max(int(x) for x in re.findall(r'Id="rId(\d+)"', rels)) + 1
    sid = max(int(s) for _n, s, _r in sheets) + 1
    k = 1
    for name in ('ReadMe', 'Bugs', 'Issues'):
        while f'xl/worksheets/sheet{k}.xml' in parts:
            k += 1
        p = f'xl/worksheets/sheet{k}.xml'
        if name == 'ReadMe':
            parts[p] = sheet_xml(name, data[name], header=False, widths=[24, 140], selected=True).encode('utf-8')
        else:
            parts[p] = sheet_xml(name, data[name]).encode('utf-8')
        order.append(p)
        rid = f'rId{nid}'
        nid += 1
        rels = rels.replace('</Relationships>', f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                            f'officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{k}.xml"/>'
                            '</Relationships>')
        ct = ct.replace('</Types>', f'<Override PartName="/{p}" ContentType="application/vnd.openxmlformats-'
                        'officedocument.spreadsheetml.worksheet+xml"/></Types>')
        new.append((name, str(sid), rid))
        sid += 1
    allsheets = new + team
    wb = re.sub(r'<sheets>.*?</sheets>', '<sheets>' + ''.join(f'<sheet name="{n}" sheetId="{s}" r:id="{r}"/>'
                                                               for n, s, r in allsheets) + '</sheets>', wb, flags=re.S)
    newpos = {n: i for i, (n, _s, _r) in enumerate(allsheets)}
    inv = {i: n for n, i in old_pos.items()}
    wb = re.sub(r'localSheetId="(\d+)"', lambda q: f'localSheetId="{newpos.get(inv.get(int(q.group(1))), 0)}"', wb)
    wb = re.sub(r'<workbookView [^>]*>', lambda v: re.sub(r'\s(?:activeTab|firstSheet)="\d+"', '', v.group(0))
                .replace('<workbookView ', '<workbookView activeTab="0" ', 1), wb, count=1)
    app = parts['docProps/app.xml'].decode('utf-8')
    titles = ''.join(f'<vt:lpstr>{escape(n)}</vt:lpstr>' for n, _s, _r in allsheets)
    app = re.sub(r'<vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>\d+',
                 f'<vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>{len(allsheets)}', app)
    app = re.sub(r'<TitlesOfParts><vt:vector size="\d+" baseType="lpstr">.*?</vt:vector>',
                 f'<TitlesOfParts><vt:vector size="{len(allsheets)}" baseType="lpstr">{titles}</vt:vector>', app,
                 flags=re.S)
    parts['docProps/app.xml'] = app.encode()
    for n in order:
        if n.startswith('xl/worksheets/sheet') and n not in [target(r) for _n, _s, r in new]:
            parts[n] = parts[n].replace(b' tabSelected="1"', b'')
    parts['xl/workbook.xml'] = wb.encode()
    parts['xl/_rels/workbook.xml.rels'] = rels.encode()
    parts['[Content_Types].xml'] = ct.encode()
    fd, tmp = tempfile.mkstemp(suffix='.xlsx', dir=XL)
    os.close(fd)
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as out:
        for n in order:
            out.writestr(n, parts[n])
    shutil.move(tmp, OUT)
    import excel_lint
    excel_lint.check(OUT)                               # NORMS 3g
    B.REL.publish(OUT)
    print(f'wrote {OUT} from {os.path.basename(src)}: Bugs {len(data["Bugs"])}, Issues {len(data["Issues"])}, team '
          f'tabs {[n for n, _s, _r in team]}')


if __name__ == '__main__':
    main()
