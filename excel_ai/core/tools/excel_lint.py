"""
Check a finished .xlsx/.xlsm package for the faults that make Excel show "We found a problem with some content
... Repaired Records" while openpyxl and LibreOffice accept the file without a word. Rules: NORMS.md section 3g.
Each rule below is a cause Excel has actually repaired in our files, or a documented Excel limit.

    python excel_ai/core/tools/excel_lint.py FILE [FILE ...]      exit code 1 if any problem is found

Library use: excel_lint.lint(path) -> list of problem strings (empty = clean). Every builder calls it on its
output and fails the build on a problem.
"""
import posixpath
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'pr': 'http://schemas.openxmlformats.org/package/2006/relationships'}
CELL_A1 = re.compile(r'^\$?([A-Za-z]{1,3})\$?(\d+)$')
NAME_OK = re.compile(r'^[A-Za-z_\\][A-Za-z0-9_.\\]*$')
BAD_SHEET = set('[]:*?/\\')
MAX_ROW, MAX_COL = 1048576, 16384


def _col(letters):
    n = 0
    for ch in letters.upper():
        n = n * 26 + ord(ch) - 64
    return n


def _ref(ref):
    """'A1:C5' -> (c1, r1, c2, r2)."""
    a, _, b = ref.partition(':')
    b = b or a
    (ca, ra), (cb, rb) = CELL_A1.match(a).groups(), CELL_A1.match(b).groups()
    return _col(ca), int(ra), _col(cb), int(rb)


def _cell_like(name):
    """A1 or R1C1 look-alike (Excel rejects these as defined or table names)."""
    m = re.match(r'^([A-Za-z]{1,3})(\d+)', name)
    if m and _col(m.group(1)) <= MAX_COL and int(m.group(2)) <= MAX_ROW:
        return True
    return bool(re.fullmatch(r'[RrCc]\d*|[Rr]\d*[Cc]\d*', name))


def _rels(z, part):
    d, f = posixpath.split(part)
    p = posixpath.join(d, '_rels', f + '.rels')
    if p not in z.namelist():
        return {}
    out = {}
    for rel in ET.fromstring(z.read(p)).findall('pr:Relationship', NS):
        t = rel.get('Target')
        out[rel.get('Id')] = t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(d, t))
    return out


def _shared_strings(z):
    if 'xl/sharedStrings.xml' not in z.namelist():
        return []
    return [''.join(t.text or '' for t in si.iter('{%s}t' % NS['m']))
            for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', NS)]


def _cell_text(c, sst):
    t = c.get('t')
    if t == 's':
        v = c.find('m:v', NS)
        return sst[int(v.text)] if v is not None else ''
    if t == 'inlineStr':
        return ''.join(x.text or '' for x in c.iter('{%s}t' % NS['m']))
    v = c.find('m:v', NS)
    return None if v is None else v.text            # a number or formula result: not text


def lint(path):
    p = []
    z = zipfile.ZipFile(path)
    sst = _shared_strings(z)
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    wrels = _rels(z, 'xl/workbook.xml')

    # sheet names
    sheets, seen = [], set()
    for s in wb.find('m:sheets', NS):
        n = s.get('name')
        if len(n) > 31 or not n or set(n) & BAD_SHEET or n.startswith("'") or n.endswith("'"):
            p.append(f'sheet name not allowed: {n!r}')
        if n.lower() in seen:
            p.append(f'duplicate sheet name (case-insensitive): {n}')
        seen.add(n.lower())
        sheets.append((n, wrels[s.get('{%s}id' % NS['r'])]))

    # defined names
    names = set()
    dn = wb.find('m:definedNames', NS)
    for d in (dn if dn is not None else []):
        n, scope = d.get('name'), d.get('localSheetId')
        if n.startswith('_xlnm.'):
            continue
        if not NAME_OK.match(n) or len(n) > 255 or _cell_like(n) or n.upper() in ('TRUE', 'FALSE'):
            p.append(f'defined name not allowed: {n}')
        if (n.lower(), scope) in names:
            p.append(f'duplicate defined name (case-insensitive): {n}')
        names.add((n.lower(), scope))
        if len(d.get('comment') or '') > 255:
            p.append(f'defined name {n}: comment longer than 255 characters ({len(d.get("comment"))})')
        if len(d.text or '') > 8192:
            p.append(f'defined name {n}: formula longer than 8192 characters')
    global_names = {n for n, s in names if s is None}

    # sheets: cells, tables, data validations
    table_names = {}
    for sname, part in sheets:
        if part not in z.namelist():
            p.append(f'{sname}: part {part} missing')
            continue
        root = ET.fromstring(z.read(part))
        cells = {}
        for c in root.iter('{%s}c' % NS['m']):
            r = c.get('r')
            f = c.find('m:f', NS)
            if f is not None and f.text and len(f.text) > 8192:
                p.append(f'{sname}!{r}: formula longer than 8192 characters')
            if f is not None and f.get('t') == 'shared' and f.text \
                    and any(x in f.text for x in ('!', '{', '_xl')):   # NORMS 3k: Excel rejects these shared
                p.append(f'{sname}!{r}: shared formula with a sheet reference, an array constant or a newer function')
            txt = _cell_text(c, sst)
            if txt is not None and c.get('t') in ('s', 'inlineStr', 'str') and len(txt) > 32767:
                p.append(f'{sname}!{r}: text longer than 32767 characters')
            cells[r] = (c, txt)
        for dv in root.iter('{%s}dataValidation' % NS['m']):
            f1 = dv.find('m:formula1', NS)
            if dv.get('type') == 'list' and f1 is not None and f1.text and f1.text.startswith('"') \
                    and len(f1.text) - 2 > 255:
                p.append(f'{sname}: list validation {dv.get("sqref")}: list longer than 255 characters')
        areas = []
        for rid, tpart in _rels(z, part).items():
            if not tpart.startswith('xl/tables/'):
                continue
            t = ET.fromstring(z.read(tpart))
            tn, ref = t.get('displayName'), t.get('ref')
            where = f'table {tn} ({tpart}, sheet {sname})'
            if not NAME_OK.match(tn) or _cell_like(tn) or len(tn) > 255:
                p.append(f'{where}: name not allowed')
            if tn.lower() in table_names or tn.lower() in global_names:
                p.append(f'{where}: name used twice (tables and defined names share one namespace)')
            table_names[tn.lower()] = tpart
            c1, r1, c2, r2 = _ref(ref)
            for a in areas:
                if not (c2 < a[0] or c1 > a[2] or r2 < a[1] or r1 > a[3]):
                    p.append(f'{where}: overlaps another table')
            areas.append((c1, r1, c2, r2))
            af = t.find('m:autoFilter', NS)
            if af is not None and af.get('ref') != ref:
                p.append(f'{where}: autoFilter ref {af.get("ref")} differs from table ref {ref}')
            cols = t.find('m:tableColumns', NS).findall('m:tableColumn', NS)
            if len(cols) != c2 - c1 + 1 or int(t.find('m:tableColumns', NS).get('count')) != len(cols):
                p.append(f'{where}: {len(cols)} columns declared for a range {c2 - c1 + 1} wide')
            lower = {}
            for i, col in enumerate(cols):
                n = col.get('name') or ''
                if not n.strip():
                    p.append(f'{where}: blank column name (column {i + 1})')
                if n.lower() in lower:
                    p.append(f'{where}: column names "{lower[n.lower()]}" and "{n}" are equal '
                             '(Excel compares them case-insensitively)')
                lower[n.lower()] = n
                if t.get('headerRowCount', '1') != '0':
                    letters = ''
                    k = c1 + i
                    while k:
                        k, m = divmod(k - 1, 26)
                        letters = chr(65 + m) + letters
                    cell = cells.get(f'{letters}{r1}')
                    if cell is None or cell[1] is None:
                        p.append(f'{where}: header cell {letters}{r1} is empty or a number (must be the text "{n}")')
                    elif cell[0].get('t') not in ('s', 'inlineStr', 'str'):
                        p.append(f'{where}: header cell {letters}{r1} is not text')
                    elif cell[1] != n:
                        p.append(f'{where}: header cell {letters}{r1} "{cell[1]}" differs from column name "{n}"')
    return p


def check(path):
    """Lint a file a script has just written; stop the script if Excel would repair it (every writer calls this)."""
    problems = lint(path)
    if problems:
        raise SystemExit(f'{path}: Excel would repair it:\n  ' + '\n  '.join(problems))


def main(argv):
    bad = 0
    for f in argv:
        probs = lint(f)
        print(f'{f}: {"clean" if not probs else str(len(probs)) + " problem(s)"}')
        for x in probs:
            print('  ' + x)
        bad += bool(probs)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
