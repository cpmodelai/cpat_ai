"""Front tab "CPAT-AI_bugs" of the team's tracker excel_ai/legacy/Tracking issues.xlsx: our legacy bugs (L, N, D codes)
and their status in legacy, in the column format of the team's sheet CPAT_issues.

Run from anywhere: python excel_ai/mitigation/tracker_status_tab.py. Idempotent (the tab is replaced on every run).
Sources: the register export legacy/CPAT-AI_BugsAndIssues_latest.json (codes, titles, priority, where, fix) and the
cell-by-cell check of the CPAT team's fixes, bugsfixed/legacy465_check.json (the latest knowledge of fixed bugs). The
date a bug was found is its first mention in CAVEATS.md (blank when the bug predates the log).

The workbook is edited at the XML level, not with openpyxl, so the team's threaded comments, customXml and printer
settings survive; the new sheet reuses the cell styles of CPAT_issues (header, wrap, the green/orange/red "Fixed" fills).
"""
import json, os, re, shutil, sys, tempfile, zipfile
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
XL = os.path.normpath(os.path.join(HERE, '..'))
TRACKER = os.path.join(XL, 'legacy', 'Tracking issues.xlsx')
REGISTER = os.path.join(XL, 'legacy', 'CPAT-AI_BugsAndIssues_latest.json')
CHECK465 = os.path.join(XL, 'bugsfixed', 'legacy465_check.json')
CAVEATS = os.path.join(XL, '..', 'CAVEATS.md')
SHEET = 'CPAT-AI_bugs'
LEGACY465_FROM = '2026-10-22'           # date the 465 file arrived; earlier finds were made in 456

# Style indices of xl/styles.xml as used on CPAT_issues (header, centred, wrapped, Fixed = Solved / In progress / No)
S_HEAD, S_HEAD_WRAP, S_HEAD_LEFT, S_CENTRE, S_WRAP = 1, 23, 18, 4, 3
S_FIXED = {'Solved': 19, 'In progress': 20, 'No': 21}
COLS = [  # (header, header style, width) as on CPAT_issues
    ('Number', S_HEAD, 8.9), ('Issues', S_HEAD, 71), ('CPAT Version with identified issue', S_HEAD_WRAP, 17.9),
    ('Date', S_HEAD_WRAP, 11), ('Materiality/Priority', S_HEAD_WRAP, 11), ('Fixed', S_HEAD, 11.3),
    ('Issue raised by', S_HEAD_LEFT, 14.6), ('Issue solved by', S_HEAD_LEFT, 20.7), ('Additional comments', S_HEAD, 90)]
PRIORITY = {'High': '5 (High)', 'Medium': '3 (Medium)', 'Low': '1 (Low)'}
FIXED = {'Confirmed fixed': 'Solved', 'Fixed with caveats': 'In progress', 'Not fixed': 'No'}


def first_mentions(codes):
    """{code: date of the first CAVEATS.md entry naming it on a line about bugs or the register}; ranges such as
    L90-L94 count for every code in them."""
    dates, date = {}, None
    known = set(codes)
    for line in open(CAVEATS, encoding='utf-8'):
        m = re.match(r'## (\d{4}-\d{2}-\d{2})', line)
        if m:
            date = m.group(1)
            continue
        if not date or not re.search(r'bug|register|Register', line):      # D1-D4, N2 also name other things
            continue
        # a code, not a cell: not after "Mitigation "/"cell "/"!"/":"/"/", not followed by ":", "/" or a letter or digit
        for m in re.finditer(r'(?<![\w!$:/])(?<!Mitigation )(?<!cell )([LDN])(\d+)(?:-\1?(\d+))?(?![\w:/])', line):
            hi = int(m.group(3)) if m.group(3) and int(m.group(3)) - int(m.group(2)) < 20 else int(m.group(2))
            for n in range(int(m.group(2)), hi + 1):
                c = f'{m.group(1)}{n}'
                if c in known and (c not in dates or date < dates[c]):
                    dates[c] = date
    return dates


def rows():
    reg = json.load(open(REGISTER, encoding='utf-8'))
    check = json.load(open(CHECK465, encoding='utf-8'))['bugs']
    bugs = reg['legacy_bugs'] + reg['distribution_bugs']
    dates = first_mentions([b['code'] for b in bugs])
    out = []
    for b in bugs:
        code, chk = b['code'], check.get(b['code'])
        fixed = FIXED[chk['status']] if chk else 'No'
        date = dates.get(code, '')
        comment = []
        if chk is None:
            comment.append('Open in legacy 465 (not marked fixed by the CPAT team).')
        elif chk['status'] == 'Confirmed fixed':
            comment.append('Fixed in legacy 465 (checked cell by cell, 2026-10-22).')
        elif chk['status'] == 'Fixed with caveats':
            comment.append('Fixed with caveats in legacy 465: ' + chk['note'] + '.')
        else:
            comment.append('Marked fixed by the CPAT team, but not fixed in legacy 465: ' + chk['note'] + '.')
        if chk and chk['status'] == 'Confirmed fixed' and chk['note']:
            comment[-1] = comment[-1][:-1] + ': ' + chk['note'] + '.'
        comment.append('Where: ' + b['where'] + '.')
        if fixed != 'Solved' and b.get('fix'):
            comment.append('Fix: ' + b['fix'])
        out.append([code, b['title'], ('465' if date >= LEGACY465_FROM else '456') if date else '456', date,
                    PRIORITY.get(b['priority'].split()[0], b['priority']), fixed, 'Stephen (CPAT-AI)',
                    'CPAT team (465)' if fixed != 'No' else '', ' '.join(comment)])
    return out


def col(i):
    return 'ABCDEFGHI'[i]


def sheet_xml(data):
    cell = lambda ref, s, v: (f'<c r="{ref}" s="{s}" t="inlineStr"><is><t xml:space="preserve">{escape(str(v))}</t></is></c>'
                              if v not in ('', None) else f'<c r="{ref}" s="{s}"/>')
    body = ['<row r="1" spans="1:9" ht="28.5" customHeight="1">' +
            ''.join(cell(f'{col(i)}1', s, h) for i, (h, s, _) in enumerate(COLS)) + '</row>']
    styles = [S_CENTRE, S_WRAP, S_CENTRE, S_CENTRE, S_CENTRE, None, 0, 0, S_WRAP]
    for r, row in enumerate(data, start=2):
        cells = ''.join(cell(f'{col(i)}{r}', S_FIXED[v] if i == 5 else styles[i], v) for i, v in enumerate(row))
        body.append(f'<row r="{r}" spans="1:9">{cells}</row>')
    last = len(data) + 1
    cols = ''.join(f'<col min="{i + 1}" max="{i + 1}" width="{w}" customWidth="1"/>' for i, (_, _, w) in enumerate(COLS))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheetPr><tabColor rgb="FF1F4E78"/></sheetPr>'
            f'<dimension ref="A1:I{last}"/><sheetViews><sheetView tabSelected="1" workbookViewId="0">'
            '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
            '<selection pane="bottomLeft" activeCell="A2" sqref="A2"/></sheetView></sheetViews>'
            '<sheetFormatPr defaultRowHeight="14.25"/>'
            f'<cols>{cols}</cols><sheetData>{"".join(body)}</sheetData>'
            f'<autoFilter ref="A1:I{last}"/>'
            '<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/></worksheet>')


def main():
    data = rows()
    z = zipfile.ZipFile(TRACKER)
    parts = {n: z.read(n) for n in z.namelist()}
    order = z.namelist()
    z.close()
    wb = parts['xl/workbook.xml'].decode('utf-8')
    rels = parts['xl/_rels/workbook.xml.rels'].decode('utf-8')
    m = re.search(rf'<sheet name="{re.escape(SHEET)}" sheetId="\d+" r:id="(rId\d+)"/>', wb)
    if m:                                               # rerun: overwrite the existing part
        target = re.search(rf'Id="{m.group(1)}"[^>]*Target="([^"]+)"', rels) or \
                 re.search(rf'Target="([^"]+)"[^>]*Id="{m.group(1)}"', rels)
        part = 'xl/' + target.group(1)
    else:
        n = 1
        while f'xl/worksheets/sheet{n}.xml' in parts:
            n += 1
        part = f'xl/worksheets/sheet{n}.xml'
        rid = 'rId' + str(max(int(x) for x in re.findall(r'Id="rId(\d+)"', rels)) + 1)
        sid = max(int(x) for x in re.findall(r'sheetId="(\d+)"', wb)) + 1
        rels = rels.replace('</Relationships>', f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                            f'officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{n}.xml"/></Relationships>')
        wb = wb.replace('<sheets>', f'<sheets><sheet name="{SHEET}" sheetId="{sid}" r:id="{rid}"/>')
        # sheet-scoped defined names count sheets by position: shift them by the new first sheet
        wb = re.sub(r'localSheetId="(\d+)"', lambda k: f'localSheetId="{int(k.group(1)) + 1}"', wb)
        ct = parts['[Content_Types].xml'].decode('utf-8')
        parts['[Content_Types].xml'] = ct.replace('</Types>', f'<Override PartName="/{part}" ContentType="application/'
                                                  'vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>').encode()
        app = parts['docProps/app.xml'].decode('utf-8')
        k = int(re.search(r'<vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>(\d+)', app).group(1))
        app = app.replace(f'<vt:i4>{k}</vt:i4>', f'<vt:i4>{k + 1}</vt:i4>', 1)
        app = re.sub(r'<TitlesOfParts><vt:vector size="(\d+)" baseType="lpstr">',
                     lambda q: f'<TitlesOfParts><vt:vector size="{int(q.group(1)) + 1}" baseType="lpstr"><vt:lpstr>{SHEET}</vt:lpstr>', app)
        parts['docProps/app.xml'] = app.encode()
        order.append(part)
    # the new tab opens first: active tab 0, no other tab selected
    wb = re.sub(r'<workbookView [^>]*>', lambda v: re.sub(r'\s(?:activeTab|firstSheet)="\d+"', '', v.group(0))
                .replace('<workbookView ', '<workbookView activeTab="0" ', 1), wb, count=1)
    parts['xl/workbook.xml'] = wb.encode()
    parts['xl/_rels/workbook.xml.rels'] = rels.encode()
    for n in order:
        if n.startswith('xl/worksheets/sheet') and n != part:
            parts[n] = parts[n].replace(b' tabSelected="1"', b'')
    parts[part] = sheet_xml(data).encode('utf-8')
    fd, tmp = tempfile.mkstemp(suffix='.xlsx', dir=os.path.dirname(TRACKER))
    os.close(fd)
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as out:
        for n in order:
            out.writestr(n, parts[n])
    shutil.move(tmp, TRACKER)
    sys.path.insert(0, os.path.join(XL, 'shared'))
    import excel_lint
    excel_lint.check(TRACKER)                   # NORMS 3g
    from collections import Counter
    print(f'{SHEET}: {len(data)} bugs', dict(Counter(r[5] for r in data)))


if __name__ == '__main__':
    main()
