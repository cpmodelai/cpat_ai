"""Quick check of CPAT-AI-Mitigation-MVP (a few minutes): run after every change. The full check (check_v7_0.py,
about an hour) runs only when the user asks (milestones, end of the day): user rule 2026-10-15.

1. Structure of the shipped file (no recalculation): tab order; every plain formula at most 100 characters; no
   numeric literal in any formula (same rules as the full check); no defined name or LAMBDA parameter that reads like
   a cell reference; every sheet a formula or name points to exists; newer functions carry the _xlfn. prefix.
2. One LibreOffice recalculation with the LAMBDA calls expanded (LibreOffice cannot evaluate LAMBDAs; v4.9: the
   expanded copy written from the file's XML and recalculated in a LibreOffice session while 1 runs): no error
   value anywhere.
3. Every output code (all scenario groups, all years but the LAMBDA year) against the last release in Old/
   (recalculated once and cached in .quickcheck/): shared codes, max difference, the codes that change.
4. v3.7: Excel (Windows with Excel only, else skipped): the shipped file opens without a repair (v3.6 lost the
   formulas calling the LAMBDAs SCALE and SHARE) and a full recalculation, LAMBDAs live, gives no error value.

    python check_quick_v7_0.py            # report to the screen and check_quick_report_v7.0.md
"""
import glob
import json
import os
import re
import sys
import time
import zipfile

import openpyxl

import build_v7_2 as B
import check_v7_0 as C
import lo_session_v7_0 as LO

HERE = os.path.dirname(os.path.abspath(__file__))
if os.environ.get('QUICK'):                         # v3.9: check the quick build (QUICK=1 build_v<n>.py)
    B.OUT = B.OUT.replace('.xlsm', '_quick.xlsx')
RESERVED = {l.strip().upper() for l in open(os.path.join(HERE, 'excel_reserved_names.txt'), encoding='utf-8')
            if l.strip() and not l.startswith('#')}     # v3.9: NORMS 3d rule 1
GRANDFATHERED = {'base', 'growth', 'price', 'rate', 'share', 'value', 'year'}   # LAMBDA parameters accepted by Excel
CACHE = os.path.join(HERE, '.quickcheck')
REPORT = os.path.join(HERE, f'check_quick_report_v{B.VERSION}.md')
NEWER = ['MAXIFS', 'MINIFS', 'AGGREGATE', 'IFNA', 'IFS', 'XLOOKUP', 'XMATCH', 'LET', 'LAMBDA', 'CONCAT', 'TEXTJOIN',
         'SWITCH', 'FILTER', 'UNIQUE', 'SORT', 'SORTBY', 'SEQUENCE', 'MAP', 'REDUCE', 'SCAN', 'BYROW', 'BYCOL']
CELLISH = re.compile(r'^(?:[A-Za-z]{1,3}\d+|[Rr]\d*[Cc]\d*|[Rr]\d*|[Cc]\d*)$')
ERRORS = ('#REF!', '#NAME?', '#VALUE!', '#DIV/0!', '#N/A', '#NUM!', '#NULL!', 'Err:')
lines, fails = [], []


def log(msg, ok=True):
    lines.append(f'- {msg}: {"OK" if ok else "FAIL"}')
    print(lines[-1])
    if not ok:
        fails.append(msg)


def structure(wb):
    tail = ['REF->>'] + [t for t, _b in B.MERGES[2:]]
    log(f'tab order (main, inputs, data, reference last; {len(wb.sheetnames)} tabs)',
        wb.sheetnames[:len(B.TAB_ORDER)] == B.TAB_ORDER and wb.sheetnames[-len(tail):] == tail)
    long_, lits, missing = [], {}, set()
    sheets = set(wb.sheetnames)
    n = 0
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if not (isinstance(v, str) and v.startswith('=')):
                    continue
                n += 1
                if not C.LAMBDA_CALL.search(v):
                    if len(v) > 100:
                        long_.append(f'{ws.title}!{c.coordinate}')
                    x = v
                    for rx, _w in C.ALLOWED:
                        x = rx.sub('', x)
                    x = re.sub(r'"[^"]*"', '""', x)
                    for m in re.finditer(r"('[^']+'|[A-Za-z_][\w\.]*)!", x):
                        if m.group(1).strip("'") not in sheets:
                            missing.add(m.group(1))
                    x = re.sub(r"('[^']+'|[A-Za-z_][\w\.]*)!", '', x)
                    x = re.sub(r"\$?[A-Z]{1,3}\$?\d+", 'R', x)
                    for m in re.finditer(r'(?<![A-Za-z_\d.])(\d+\.?\d*)', x):
                        if m.group(1) not in ('0', '1'):
                            lits.setdefault(m.group(1), f'{ws.title}!{c.coordinate}')
    log(f'{n} formulas; plain formulas over 100 characters: {long_[:5]}', not long_)
    log(f'numeric literals in formulas: {dict(list(lits.items())[:6])}', not lits)
    z = zipfile.ZipFile(B.OUT)
    wbx = z.read('xl/workbook.xml').decode()
    names = re.findall(r'<definedName name="([^"]+)"[^>]*>(.*?)</definedName>', wbx, re.S)
    bad = [n_ for n_, _v in names if CELLISH.match(n_)]
    bad += [p for _n, v in names for p in re.findall(r'_xlpm\.([A-Za-z0-9_]+)', v) if CELLISH.match(p)]
    log(f'{len(names)} defined names; names or LAMBDA parameters that read like cells: {sorted(set(bad))[:6]}', not bad)
    res = [n_ for n_, _v in names if n_.upper() in RESERVED] + [n_ for n_ in B.LAMBDAS if n_.upper() in RESERVED]
    res += [p for _n, (ps, _b) in B.LAMBDAS.items() for p in ps if p.upper() in RESERVED and p not in GRANDFATHERED]
    log(f'reserved names (Excel functions, keywords, names Excel rejected; NORMS 3d) used: {sorted(set(res))[:6]}',
        not res)
    for _n, v in names:
        for m in re.finditer(r"(&apos;[^&]+&apos;|'[^']+'|[A-Za-z_][\w\.]*)!", v):
            s = m.group(1).replace('&apos;', "'").strip("'")
            if s not in sheets:
                missing.add(s)
    log(f'sheets named by formulas and names exist: missing {sorted(missing)[:6]}', not missing)
    unpref = set()
    for part in [p for p in z.namelist() if p.startswith('xl/worksheets/sheet')] + ['xl/workbook.xml']:
        text = ' '.join(re.findall(r'<f[^>]*>(.*?)</f>', z.read(part).decode(), re.S)) if 'worksheets' in part \
            else ' '.join(re.findall(r'<definedName[^>]*>(.*?)</definedName>', z.read(part).decode(), re.S))
        for fn in NEWER:
            if re.search(rf'(?<![\w\.]){fn}\(', text):
                unpref.add(fn)
    log(f'newer functions without the _xlfn. prefix: {sorted(unpref)}', not unpref)
    style(wb)
    tabs(wb)
    return wb


def tabs(wb):
    """v4.2 (NORMS 2.7): Cover first; every tab but Mitigation, MTInputs, Prices_dom and the Cover has a dark green
    title bar in row 2 and its light green sub-heading bars across the same width; no table header has a fill."""
    dark, light = '00AE49', '92D050'
    rgb = lambda c: str(c.fill.fgColor.rgb)[-6:] if c.fill and c.fill.fill_type else ''
    bad, heads = [], []
    for ws in wb.worksheets:
        if ws.title in ('Mitigation', 'ScenarioDefinition', 'Prices_dom', 'Cover'):
            continue
        w = max(c for c in range(1, ws.max_column + 1) if rgb(ws.cell(2, c)) == dark) if rgb(ws['A2']) == dark else 0
        if w < min(ws.max_column, 4):
            bad.append(f'{ws.title}: title bar {w} of {ws.max_column} columns')
            continue
        for r in range(3, ws.max_row + 1):
            if rgb(ws.cell(r, 1)) == light:
                wl = max(c for c in range(1, ws.max_column + 1) if rgb(ws.cell(r, c)) == light)
                if wl != w:
                    bad.append(f'{ws.title}!{r}: sub-heading bar {wl} vs title {w}')
        heads += [f'{ws.title}!{c.coordinate}' for row in ws.iter_rows() for c in row
                  if c.font and c.font.b and rgb(c) == 'EBF1DE']
    log(f'tab title bars and sub-heading bars of equal width on every tab: exceptions {bad[:5]}', not bad)
    log(f'table headers without the input fill: exceptions {heads[:5]}', not heads)
    log(f'v6.7: front tabs Cover, ScenarioCompare, ScenarioDefinition, then the MAIN divider and Mitigation: '
        f'{wb.sheetnames[:5]}', wb.sheetnames[:5] == ['Cover', 'ScenarioCompare', 'ScenarioDefinition', 'MAIN->>',
                                                       'Mitigation'])


def style(wb):
    """v3.9: style guide (NORMS 2) on Mitigation: one blank row before each section band (v4.1) and one after;
    sub-section headings bold underlined in column B; label (header) rows bold with a bottom border; Arial 10 body;
    v4.1: every section rolls up to its summary row(s); notes not italic; scenario groups copy-pasteable."""
    ws = wb['Mitigation']
    w = min(ws.max_column, 12)
    empty = lambda r: all(ws.cell(r, c).value is None for c in range(1, w + 1))
    bands = sorted(b for b in B.BAND_ROWS if b > 3)
    bad = [b for b in bands if not (empty(b - 1) and not empty(b - 2) and empty(b + 1))]
    log(f'{len(bands)} section bands with one blank row before and one after: exceptions {bad[:6]}', not bad)
    heads_ = [r for r in range(B.B_POL, ws.max_row + 1) if ws.cell(r, 2).font.u and ws.cell(r, 2).value]
    badg = [r for r in heads_ if r > B.B_POL + 2 and not empty(r - 1) or empty(r - 1) and empty(r - 2)]
    log(f'{len(heads_)} sub-section headings with exactly one blank row before: exceptions {badg[:6]}', not badg)
    rd = ws.row_dimensions
    shown = lambda r: not rd[r].hidden and not (rd[r].outlineLevel or 0)
    vis = [r for r in range(B.R_SCEN + 1, ws.max_row + 1) if shown(r) and not empty(r)]
    want = sorted({B.R_GDP} | {b for b, _t, _z in B.SECTION_GROUPS} | {t for _b, t, _z in B.SECTION_GROUPS}
                  | B.SUMMARY2)
    log(f'rolled up: visible rows below the frozen rows are the bands and summary rows only ({len(vis)}); '
        f'differences {sorted(set(vis) ^ set(want))[:6]}', vis == want and all(t for _b, t, _z in B.SECTION_GROUPS))
    ital = [r for r in range(1, ws.max_row + 1) if ws.cell(r, 8).font.i and isinstance(ws.cell(r, 8).value, str)
            and not ws.cell(r, 8).value.startswith('=')]
    log(f'notes in column H not italic: exceptions {ital[:6]}', not ital)
    log(f'section 0 numbered: A{B.R_SEC0} = {ws.cell(B.R_SEC0, 1).value!r}', str(ws.cell(B.R_SEC0, 1).value) == '0')
    copy_paste(ws)
    forward_reads(ws)                       # v6.2: no reads of later years (circular-reference robustness)
    heads = [r for r in range(1, ws.max_row + 1) if ws.cell(r, 2).font.u and ws.cell(r, 2).value]
    badh = [r for r in heads if not (ws.cell(r, 2).font.b and ws.cell(r, 8).value is None)]
    log(f'{len(heads)} sub-section headings bold underlined in column B, nothing in H: exceptions {badh[:6]}',
        len(heads) > 20 and not badh)
    labs = [r for r in range(1, ws.max_row + 1) if isinstance(ws.cell(r, 4).value, str) and 'VarP' in ws.cell(r, 4).value]
    badl = [r for r in labs if not (ws.cell(r, 4).font.b and ws.cell(r, 8).border.bottom.style == 'thin')]
    log(f'{len(labs)} label rows bold with a thin bottom border: exceptions {badl[:6]}', not badl)
    sizes = {ws.cell(r, c).font.sz for r in range(B.B_POL, ws.max_row + 1, 7) for c in (1, 8, B.COL_G0 + 2)
             if ws.cell(r, c).value is not None and r not in B.BAND_ROWS}
    log(f'body font sizes on Mitigation (sample): {sorted(sizes)}', sizes == {10})


def copy_paste(ws):
    """v4.1: scenario groups are copy-pasteable left to right: every cell of group 2 has the same relative (R1C1)
    formula or value as the cell of group 1 in the same position (a third group pasted from the next code column
    works the same way)."""
    tok = re.compile(r"(?<![A-Za-z_\d\.!$])(\$?)([A-Z]{1,3})(\$?)(\d+)(?![\d\(A-Za-z_])")

    def rel(v, r, c):
        if not (isinstance(v, str) and v.startswith('=')):
            return v

        def sub(m):
            cd, col, rdl, row = m.groups()
            cc, rr = openpyxl.utils.column_index_from_string(col), int(row)
            return (f'R{rr}' if rdl else f'R[{rr - r}]') + (f'C{cc}' if cd else f'C[{cc - c}]')
        return ''.join(p if p.startswith('"') else tok.sub(sub, p) for p in re.split(r'("[^"]*")', v))
    g1, g2 = B.group_cols(1)[0], B.group_cols(2)[0]
    lam = lambda v: isinstance(v, str) and C.LAMBDA_CALL.search(v)   # v6.6: group 2 calls the LAMBDAs (tested by the regression)
    bad = [f'{openpyxl.utils.get_column_letter(g1 + k)}{r}' for r in range(1, ws.max_row + 1) for k in range(B.GW)
           if not lam(ws.cell(r, g2 + k).value)
           and rel(ws.cell(r, g1 + k).value, r, g1 + k) != rel(ws.cell(r, g2 + k).value, r, g2 + k)]
    log(f'scenario groups 1 and 2 identical in relative form outside the LAMBDA cells of group 2 '
        f'({ws.max_row * B.GW} cells; copy-paste left to right): differences {bad[:6]}', not bad)


def rename_code(k):
    """v7.2: an output code of the last release as the rename map (code_renames_v7_2.csv) writes it."""
    parts = k.split('.')
    if not hasattr(B, 'rn_stem') or len(parts) < 3:
        return k
    return '.'.join([parts[0], B.rn_stem('.'.join(parts[1:-1])), parts[-1]])


def codes(path, data):
    """Output code -> values (base year and years before the LAMBDA year) of every scenario group."""
    ws = data['Mitigation']
    out = {}
    for g, *_r in B.SCENARIOS:
        code, base, years = B.group_cols(g)
        cols = [base] + years[:-1]
        for r in range(1, ws.max_row + 1):
            k = ws.cell(r, code).value
            if isinstance(k, str) and '.mit.' in k:
                out[k] = [ws.cell(r, c).value for c in cols]
    return out


VBA_KNOWN = set('''and as boolean byref byval call case const currency date dim do double each else elseif end enum erase error exit
explicit false for function get global gosub goto if in integer is let lib like long loop me mod new next not nothing null
on option optional or paramarray preserve private property public redim rem resume return select set single static step
stop string sub then to true type typeof until variant wend while with xor object byte attribute vb_name base compare
binary text raise err private debug print len left right mid instr instrrev replace trim ltrim rtrim ucase lcase cstr clng
cdbl cint cbool cdate cvar isnumeric isempty isnull isarray isobject isdate isError iserror val str format now timer date time
doevents msgbox inputbox createobject getobject array ubound lbound split join iif abs int fix sgn sqr exp log round rnd
vartype typename chr chrw asc ascw space string dir environ vbcr vblf vbcrlf vbtab vbnullstring vbyes vbno vbyesno vbquestion
vbinformation vbexclamation vbcritical vbokonly vbokcancel vbstring vbempty vbdouble vblong vbinteger vbboolean vbdate
vbnewline application thisworkbook worksheets workbooks sheets activesheet activeworkbook range cells rows columns
selection rgb filter datediff dateadd year month day hour minute second weekday dateserial timeserial nz
optionbase'''.split())
VBA_NAMED_TYPES = {'after', 'backgroundquery', 'destination', 'key', 'order', 'shift', 'source', 'sourcetype', 'chart',
                   'listobject', 'series', 'worksheet', 'range', 'workbook', 'shape', 'chartobject', 'name'}
VBA_CONSTS = {'vbcrlf', 'vbexclamation', 'vbinformation', 'vblf', 'vbobjecterror', 'vbquestion', 'vbstring', 'vbyes',
              'vbyesno', 'xlascending', 'xlcalculationautomatic', 'xlcalculationmanual', 'xlcmdsql', 'xlmarkerstylenone',
              'xlno', 'xlup', 'xldescending', 'xltoleft', 'xldown', 'xlvalues', 'xlpart', 'xlwhole', 'xlnone'}


def vba_names():
    """v7.1: every identifier the VBA module uses is declared in it, a VBA keyword or built-in, an Excel object-model
    name (members after a dot are not checked) or a listed xl/vb constant. The embedded project references only the
    Excel library and stdole, so an Office constant (msoTrue: v7.0) is "Variable not defined" under Option Explicit;
    LibreOffice Basic does not report it."""
    lines = []
    for ln in open(B.BAS, encoding='utf-8', errors='ignore').read().splitlines():
        out, ins = '', False
        for ch in ln:
            if ch == '"':
                ins = not ins
                out += ' '
            elif ins:
                out += ' '
            elif ch == "'":
                break
            else:
                out += ch
        lines.append(out)
    code = '\n'.join(lines).replace(' _\n', ' ')
    declared = set()
    for m in re.finditer(r'\b(?:Dim|Const|Static|ReDim(?: Preserve)?)\s+(.+)', code, re.I):
        for part in m.group(1).split(','):
            nm = re.match(r'\s*(\w+)', part)
            if nm:
                declared.add(nm.group(1).lower())
    for m in re.finditer(r'\b(?:Sub|Function)\s+(\w+)\s*\(([^)]*)\)', code, re.I):
        declared.add(m.group(1).lower())
        for p in m.group(2).split(','):
            nm = re.match(r'\s*(?:Optional\s+)?(?:ByVal\s+|ByRef\s+)?(?:ParamArray\s+)?(\w+)', p)
            if nm:
                declared.add(nm.group(1).lower())
    declared |= {m.group(1).lower() for m in re.finditer(r'^\s*(\w+):', code, re.M)}
    bad = sorted({w for w in re.findall(r'(?<![.\w])([A-Za-z_]\w*)', code)
                  if w.lower() not in VBA_KNOWN | VBA_NAMED_TYPES | VBA_CONSTS | declared})
    log(f'VBA module {os.path.basename(B.BAS)}: identifiers not declared, not VBA, Excel or a known constant: '
        f'{bad or "none"}', not bad)


PROTO_CODE = re.compile(r'^[a-z]{3}\.mit(\.[a-z0-9_]+)+\.\d+$')   # C1: lower case, digits, _; no empty token
MODEL_LETTERS = {'e', 'a', 't', 's', 'b'}


def protocol(wbf, data):
    """v7.2 (codes R9): the CPAT code protocol on the Mitigation codes the workbook computes: C1 characters, C7 no
    model letter, C10 one code per row of a scenario group, C5 a total row (explicit SUM, SUMIF or SUMIFS in its year
    formula) writes tot, not all, unless the rename map names the row's code. A new row in the old style fails."""
    if not hasattr(B, 'rn_body'):
        return
    wf, wv = wbf['Mitigation'], data['Mitigation']
    sd = wbf['ScenarioDefinition']                 # C1 exception: pass-through rows of an input use its NameOfParameter
    params = {sd.cell(r, B.MT_COL_PARAM if hasattr(B, 'MT_COL_PARAM') else 8).value for r in range(1, sd.max_row + 1)}
    bad1, bad7, bad5, dup = [], [], [], []
    for g, *_r in B.SCENARIOS:
        code, _base, years = B.group_cols(g)
        seen = set()
        for r in range(1, wv.max_row + 1):
            k = wv.cell(r, code).value
            if not (isinstance(k, str) and '.mit.' in k):
                continue
            a, c_, b_ = wf.cell(r, 1).value, wf.cell(r, 3).value or '', wf.cell(r, 2).value or ''
            if not PROTO_CODE.match(k) and not (k.split('.')[2] in params and PROTO_CODE.match(k.lower())):
                bad1.append(k)
            v0 = B.RN_VAR_INV.get(a, a)
            own = set(B.rn_body(v0, c_, b_).split('.')) if v0 in B.VAR_SFX else set()   # variable name, members
            if k.split('.')[-2] in MODEL_LETTERS and k.split('.')[-2] not in own:
                bad7.append(k)
            if k in seen:
                dup.append(k)
            seen.add(k)
            if g == 1:
                f = str(wf.cell(r, years[1]).value)
                mapped = B.rn_body(v0, c_, b_) != '.'.join(x for x in (B.rn_code(v0), c_, b_) if x)   # map decided
                if (re.match(r'=(SUM|SUMIFS|SUMIF)\(', f) and not re.match(r'=SUM\([A-Z]+\d+\)$', f)
                        and 'all' in k.split('.')[2:-1] and not mapped):
                    bad5.append(k)
    log(f'code protocol C1 (lower case, digits, underscore, no empty token): {len(bad1)} codes break it {bad1[:5]}', not bad1)
    log(f'code protocol C7 (no model letter): {len(bad7)} codes end in a model letter {bad7[:5]}', not bad7)
    log(f'code protocol C10 (unique in a scenario group): {len(dup)} duplicates {dup[:5]}', not dup)
    log(f'code protocol C5 (a total row writes tot): {len(bad5)} explicit-sum rows write all {bad5[:5]} (a row whose '
        f'code the rename map code_renames_v7_2.csv writes is decided)', not bad5)


def stored_complete(path):
    """v6.7: every stored scenario (StoredOutputs, values written by the build's emulation of the batch run) has its
    indicator rows found and numeric (v6.6 shipped the definitions empty: the batch copy blanked the live group)."""
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)['StoredOutputs']
    ids, bad = {}, []
    for r in ws.iter_rows(min_row=B.SR_FIRST, values_only=True):
        if r[2] is None:
            continue
        ids[r[0]] = ids.get(r[0], 0) + 1
        if r[4] == 'code not found' or not any(isinstance(v, (int, float)) for v in r[B.SR_Y0 - 1:]):
            bad.append((r[0], r[2]))
    if not ids and os.environ.get('QUICK'):      # v7.2: the quick build runs no batch (StoredOutputs empty)
        lines.append('- StoredOutputs: empty in the quick build (no batch run): skipped')
        print(lines[-1])
        return
    log(f'StoredOutputs: rows by scenario ID {ids}; rows without values {len(bad)} {bad[:4]}', ids and not bad)


def lambda_group(data):
    """v6.6: group 2 (the live scenario) calls the named LAMBDAs in every year (v4.3-v6.5: a third LAMBDA test group
    running group 2's scenario). The LAMBDAs are tested by the regression below: every output code of every group
    (every Mitigation row, base year to 2040) against the last release, whose group 2 was plain formulas up to v6.5;
    and on Distribution by the Python reference. Here: group 2 holds LAMBDA calls and no error value."""
    ws = data['Mitigation']
    _c2, b2, y2 = B.group_cols(B.LAMBDA_GROUP)
    n = sum(1 for r in range(B.R_GDP, ws.max_row + 1) for c in [b2] + y2
            if isinstance(ws.cell(r, c).value, (int, float)))
    log(f'LAMBDA group {B.LAMBDA_GROUP} (the live scenario, LAMBDAs base year to {B.LAST_YEAR}): {n} numeric cells; '
        f'tested against plain formulas by the output-code regression (last release) and the Distribution reference',
        n > 0)


def distribution(data):
    """v4.4: Distribution (NORMS 1.1b): group 2 (v6.6: the LAMBDA group) equals the
    Python reference (distribution_ref_v7_0.run) fed with the sheet's own section-1 settings and section-2 inputs."""
    import distribution_ref_v7_0 as DR
    ws = data['Distribution']
    if not B.DSPEC:                                 # the row plan, as the build made it (Mitigation row keys)
        wm, mitrow = data['Mitigation'], {}
        for r_, (a_, f_, s_) in enumerate(wm.iter_rows(min_row=1, max_col=3, values_only=True), 1):
            if isinstance(a_, str) and a_:
                mitrow.setdefault((a_, f_ or '', s_ or ''), r_)
        B._dist_layout(mitrow)
    num = lambda v: v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0.0
    (c2, b2, d2, s2) = B.dist_group_cols(2)
    v = lambda key, k=0: ws.cell(B.DROW[key], b2 + k).value
    st = {n_: v(n_) for n_ in B.DIST_MT}
    st['aspire_code'], st['exempt_fuel'] = v('aspcode'), v('exfuel')
    st['tgt_code'] = v('tgtcode')                    # v6.0: transfer program (Cash or ASPIRE code)
    inp = {'dp_res': {it: v(f'dpr.{it}') for it, *_x in B.DIST_FUELS},
           'dp_all': {f: v(f'dpa.{f}') for f, *_x in B.DIST_MITFUEL},
           'spend': {f: v(f'spend.{f}') for f, *_x in B.DIST_MITFUEL},
           'defl_gtap': None, 'gdp_lcu': v('gdp'), 'pop': v('pop'), 'rev_lcu': v('rev'), 'cons_gdp': v('consgdp'),
           'settings': st}
    dm = data['DistMapping']                        # v4.7: the input-output tables of the country are on DistMapping
    inp['defl_gtap'] = next(dm.cell(r_, 5).value for r_ in range(1, dm.max_row + 1)
                            if dm.cell(r_, 1).value == 'Deflator ratio (ResultsYear / GTAP year)')
    out = DR.run(inp)
    worst, at, m = 0.0, None, 0
    pairs = [(('tef', s_), f'tef.{s_}', True) for s_, _l in B.DIST_SAMPLES]
    pairs += [((k, s_), f'{k}.{s_}', False) for k in ('rec', 'net', 'pit', 'pui', 'cts', 'tgt') for s_, _l in B.DIST_SAMPLES]
    pairs += [(('pctrev_comp', s_), f'comp.{s_}', False) for s_, _l in B.DIST_SAMPLES]
    pairs += [(('def', it), f'def.{it}', True) for it, *_x in B.DIST_FUELS]
    pairs += [(('ief', it), f'ief.{it}', True) for it, *_x in B.DIST_CATS]
    for (k, key, basket) in pairs:
        ref = out[k]
        ref = ref if basket else [None] + ref
        for j in range(0 if basket else 1, 11):
            a = num(v(key, j))
            d = abs(a - ref[j]) / max(1.0, abs(ref[j]))
            m += 1
            if d > worst:
                worst, at = d, (key, j)
    for s_, _l in B.DIST_SAMPLES:
        for k in ('pct_gini_norec', 'pct_gini_rec'):
            d = abs(num(v(f'{k}.{s_}')) - out[(k, s_)])
            m += 1
            if d > worst:
                worst, at = d, (f'{k}.{s_}', 0)
    for c in [c_ for c_, *_x in B.DIST_CATS]:
        d = abs(num(v(f'dpr.{c}')) - out['dp'][c]) / max(1e-12, abs(out['dp'][c]))
        m += 1
        if d > worst:
            worst, at = d, (f'dpr.{c}', 0)
    log(f'Distribution group 2 vs the Python reference (distribution_ref_v7_0, same inputs): {m} values, '
        f'max relative difference {worst:.2g} {at or ""}; tef.ove deciles 1, 10: {v("tef.ove", 1):.3f}, '
        f'{v("tef.ove", 10):.3f}; Gini change with recycling {v("pct_gini_rec.ove"):.3f}', worst < 1e-9)
    geo = all(ws.cell(5, B.dist_group_cols(g)[0]).value == data['Mitigation'].cell(5, B.group_cols(g)[0]).value
              for g in range(1, B.DGROUPS + 1))
    log(f'Distribution scenario numbers equal Mitigation group by group (1-{B.DGROUPS}): {geo}', geo)


def last_release():
    """The last released workbook in excel_ai/releases/ before this version (restructure 2026-10-22: was Old/); the
    release of this version itself while it is the only one."""
    files = glob.glob(os.path.join(HERE, '..', 'releases', f'{B.NAME}-v*.xlsm'))
    ver = lambda f: tuple(int(x) for x in re.search(r'-v(\d+)\.(\d+)\.xlsm$', f).groups())
    cur = tuple(int(x) for x in B.VERSION.split('.'))
    before = [f for f in files if ver(f) < cur]
    return max(before or [f for f in files if ver(f) == cur], key=ver)


def recalc_values(path):
    """v4.9: Mitigation of path recalculated in a LibreOffice session (lo_session_v7_0); v7.0: LAMBDAs expanded (since
    v6.6 the live group 2 calls them, which LibreOffice cannot evaluate)."""
    return LO.start_values(LO.expanded_zip(path, C.LAMBDA_CALL, C.expand), ['Mitigation'])()[0]




def excel_open():
    """v3.7: open the shipped file in Excel (macros disabled, alerts off): Excel fails to open a file it would have to
    repair, and writes a repair log error*.xml to %TEMP%. Then recalculate fully and count error values."""
    try:
        import win32com.client
        xl = win32com.client.DispatchEx('Excel.Application')
    except Exception as e:                          # no pywin32 or no Excel (Linux, cloud)
        lines.append(f'- Excel open and recalculation: skipped (no Excel here: {type(e).__name__})')
        print(lines[-1])
        return
    import shutil
    import tempfile
    tmp = os.environ.get('TEMP', tempfile.gettempdir())
    before = set(glob.glob(os.path.join(tmp, 'error*.xml')))
    cp = os.path.join(tempfile.mkdtemp(), os.path.basename(B.OUT))
    shutil.copy(B.OUT, cp)
    xl.Visible, xl.DisplayAlerts, xl.AutomationSecurity = False, False, 3       # 3 = macros disabled
    try:
        try:
            wb = xl.Workbooks.Open(cp, 0, True)
        except Exception:
            wb = None
        repair = [open(p, encoding='utf-8', errors='ignore').read()
                  for p in set(glob.glob(os.path.join(tmp, 'error*.xml'))) - before]
        removed = [m for r in repair for m in re.findall(r'<removedRecord>(.*?)</removedRecord>', r)]
        log(f'Excel opens the file without a repair: {"no" if wb is None or removed else "yes"} {removed[:4]}',
            wb is not None and not removed)
        if wb is None:
            return
        xl.CalculateFull()
        errs = []
        for name in ('Mitigation', 'LiveOutputs', 'ScenarioCompare', 'StoredOutputs'):
            vals = wb.Worksheets(name).UsedRange.Value or ()
            errs += [(name, i, j) for i, row in enumerate(vals, 1) for j, v in enumerate(row, 1)
                     if isinstance(v, int) and v < -2146820000]                 # COM error values (#NAME? etc.)
        log(f'Excel full recalculation (LAMBDAs live): error values {len(errs)} {errs[:6]}', not errs)
        wb.Close(False)
    finally:
        xl.Quit()


FWD_OK = {'mani', 'dsum', 'lvc'}   # v6.2 (NORMS circular references): rows allowed to read a later year
FWD_INPUT_ONLY = {'lvc': 'tvc'}    # ... and the row whose precedents must be inputs only (no quantity, no GDP)


def forward_reads(ws):
    """v6.2 (user 2026-10-20: robustness to circular references): (1) no formula of a scenario group reads a later
    year except the whitelisted rows (mani: the manual capacity path, data; dsum, lvc: the levelised variable cost);
    (2) what lvc levelises (tvc) depends on inputs only: its precedents within the column never reach the fuel-use
    sections (5 onwards), the GDP rows or the power quantity rows. Ranges over the price-block area count as inputs
    (prices before new policies: fpn reads one rpb row)."""
    CI = openpyxl.utils.column_index_from_string
    ref = re.compile(r"(?<![A-Za-z_!'.])(\$?)([A-Z]{1,3})(\$?)(\d+)(?::(\$?)([A-Z]{1,3})(\$?)(\d+))?(?![\w(])")
    code, base, yrs = B.group_cols(2)
    cols = [base] + yrs[:-1]
    var = {r: ws.cell(r, 1).value for r in range(1, ws.max_row + 1)}
    bad = set()
    for c in cols:
        for r in range(1, ws.max_row + 1):
            v = ws.cell(r, c).value
            if not (isinstance(v, str) and v.startswith('=')) or var[r] in FWD_OK:
                continue
            v2 = re.sub(r"'?[A-Za-z_ ]+'?!\$?[A-Z]+\$?\d+(:\$?[A-Z]+\$?\d+)?", '', v)
            for m in ref.finditer(''.join(p for p in re.split(r'("[^"]*")', v2) if not p.startswith('"'))):
                hi = max(CI(m.group(2)), CI(m.group(6)) if m.group(6) else 0)
                if c < hi <= yrs[-1]:
                    bad.add(f'{var[r]} ({openpyxl.utils.get_column_letter(c)}{r})')
    log(f'no formula reads a later year except {sorted(FWD_OK)}: exceptions {sorted(bad)[:8]}', not bad)
    par = set()                                    # parameter cells (D:G) act in every year: no model year after the
    first_years = {B.group_cols(g)[2][0] for g in range(1, 11)}   # base year (v6.2: ghg.k read GHGYear)
    last_col = B.group_cols(10)[2][-1]
    for r in range(1, ws.max_row + 1):
        for c in range(4, 8):
            v = ws.cell(r, c).value
            if not (isinstance(v, str) and v.startswith('=')):
                continue
            v2 = re.sub(r"'?[A-Za-z_ ]+'?!\$?[A-Z]+\$?\d+(:\$?[A-Z]+\$?\d+)?", '', v)
            for m in ref.finditer(''.join(p for p in re.split(r'("[^"]*")', v2) if not p.startswith('"'))):
                lo_ = CI(m.group(2))
                hi = max(lo_, CI(m.group(6)) if m.group(6) else 0)
                if hi >= min(first_years) and lo_ <= last_col and any(B.group_cols(g)[2][0] <= hi for g in range(1, 11)):
                    rr_ = int(m.group(4))                  # a data row (its year cells read no other model row) is fine
                    f_ = str(ws.cell(rr_, B.group_cols(1)[2][0]).value)
                    others = {int(x) for x in re.findall(r'(?<![A-Za-z_!])\$?[A-Z]{1,3}\$?(\d+)', f_)} - {1, rr_}
                    if f_.startswith('=') and others:
                        par.add(f'{var[r]} ({openpyxl.utils.get_column_letter(c)}{r})')
    log(f'no parameter cell (D:G) reads a model year after the base year: exceptions {sorted(par)[:8]}', not par)
    c = cols[5]
    forbid = (set(range(B.S_FIRST, ws.max_row + 1)) | set(range(B.R_GDPUSD, B.R_GDP + 1))
              | {r for (v_, _f), r in B.R_PW.items() if v_ in ('req', 'gen', 'pdem', 'dem', 'cap', 'effcap', 'need',
                                                              'kafter', 'cons', 'demtot', 'captot')})
    prices = set(range(B.R_PV0, B.R_PV1 + 1))
    hits = []
    for v_, src in FWD_INPUT_ONLY.items():
        todo = [r for r in var if var[r] == src]
        seen = set(todo)
        while todo:
            r = todo.pop()
            f = ws.cell(r, c).value
            if not (isinstance(f, str) and f.startswith('=')):
                continue
            f2 = re.sub(r"'?[A-Za-z_ ]+'?!\$?[A-Z]+\$?\d+(:\$?[A-Z]+\$?\d+)?", '', f)
            for m in ref.finditer(f2):
                r1, r2 = int(m.group(4)), int(m.group(8)) if m.group(8) else int(m.group(4))
                rows = range(min(r1, r2), max(r1, r2) + 1)
                if set(rows) <= prices:
                    continue
                for rr in rows:
                    if rr in forbid:
                        hits.append((var.get(r), var.get(rr), rr))
                    elif rr not in seen:
                        seen.add(rr)
                        todo.append(rr)
    log(f'{sorted(FWD_INPUT_ONLY)} levelise inputs only (precedents reach no fuel use, GDP or power quantity row): '
        f'exceptions {sorted(set(hits))[:6]}', not hits)


def main():
    t0 = time.time()
    stage = lambda what: print(f'[{time.time() - t0:5.0f} s] {what}', flush=True)   # v4.9: stage timings
    wait = LO.start_values(LO.expanded_zip(B.OUT, C.LAMBDA_CALL, C.expand),   # v4.9: recalculated meanwhile
                           ['Mitigation', 'Distribution', 'DistMapping'])
    stage('expanded copy written, LibreOffice session started')
    wbf = openpyxl.load_workbook(B.OUT)
    structure(wbf)
    stage('structure checked')
    data, errs = wait()                            # LAMBDA calls expanded, so every cell is evaluated
    stage('recalculated values read')
    gaps = [e for e in errs if B.cmp_na_only(*e)]  # v6.4: #N/A of the empty dashboard slots (chart gaps)
    errs = [e for e in errs if e not in gaps]
    log(f'recalculated in LibreOffice (LAMBDAs expanded): error values {len(errs)} {errs[:6]} (accepted: the chart '
        f'data of empty ScenarioCompare slots, {gaps[:2]})', not errs)
    lambda_group(data)
    distribution(data)
    stored_complete(B.OUT)
    vba_names()
    protocol(wbf, data)                            # v7.2 (codes R9)
    stage('LAMBDA groups and Distribution checked')
    excel_open()
    rel = last_release()
    os.makedirs(CACHE, exist_ok=True)
    cfile = os.path.join(CACHE, os.path.basename(rel) + '.json')
    if os.path.exists(cfile) and os.path.getmtime(cfile) > os.path.getmtime(rel):
        old = json.load(open(cfile))
    else:
        old = codes(rel, recalc_values(rel))
        json.dump(old, open(cfile, 'w'))
    if re.search(r'-v7\.[01]\.xlsm$', rel) or re.search(r'-v[1-6]\.\d+\.xlsm$', rel):   # releases before the codes map
        old = {rename_code(k): v for k, v in old.items()}   # v7.2: the last release's codes through the rename map
    new = codes(B.OUT, data)
    if os.environ.get('QC_DUMP'):                  # v4.15: the new codes for a review of the changes
        json.dump(new, open(os.environ['QC_DUMP'], 'w'))
    shared = set(old) & set(new)
    num = lambda v: v if isinstance(v, (int, float)) else 0.0
    diff = {k: max((abs(num(a) - num(b)) for a, b in zip(old[k], new[k])), default=0) for k in shared}
    changed = sorted((k for k, d in diff.items() if d > 1e-9), key=lambda k: -diff[k])
    lines.append(f'- output codes vs {os.path.basename(rel)}: {len(shared)} shared, {len(set(new) - set(old))} new, '
                 f'{len(set(old) - set(new))} gone; {len(changed)} change (max abs diff '
                 f'{max(diff.values(), default=0):.4g}); largest: {changed[:8]}; other than bco2 (with max abs diff): '
                 f'{[(k, round(diff[k], 6)) for k in changed if ".bco2." not in k][:40]}')
    print(lines[-1])
    head = [f'# Quick check, CPAT-AI-Mitigation-MVP v{B.VERSION}', '',
            f'**{"PASS" if not fails else "FAIL"}** ({time.time() - t0:.0f} s; the full check is check_v7_0.py, run '
            f'on request). Changes of output codes are reported, not failed: compare them with what the change '
            f'intended.', '']
    open(REPORT, 'w', encoding='utf-8').write('\n'.join(head + lines) + '\n')
    print('PASS' if not fails else 'FAIL', f'{time.time() - t0:.0f} s')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
