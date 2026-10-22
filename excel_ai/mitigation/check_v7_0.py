"""Checks for CPAT-AI-Mitigation-MVP-v6.4.xlsm (v3.5: section 5b, the engineer road transport model, row by row
against transport_model_ref_v7_0.engine with all bug fixes in scenarios 1 and 2 and in copied scenarios with TrModel =
Engineer and transport policies, the whole model with the engine's road fuels and electricity, policy directions;
regression vs v3.4 0) (v2.7: short bands and title, summary rows without decimals,
macro buttons on ScenarioCompare; regression vs v2.6 0) (v2.6: price blocks with a parameter row, international
reference price row gpi, one row group per section with its summary row last, tab groups, names not bold, plain D:G;
regression vs v2.5 0) (v2.5: section 2 reordered into price build-ups by fuel and sector,
new row spf, txf = excise and other taxes before the floor; regression vs v2.4 0 apart from txf) (v2.4: years in row 1, every number in D:G labelled by a label row, one
level of row groups, no constant typed or written into a Mitigation formula, subsidies negative: regression vs v2.3
with the subsidy rows compared as new = -old) (v2.2: one version number for every current file, regression 0
against v1.09, consistency of versions, file references, LegacyDiff and the issues register) (v1.09: existing carbon
pricing with test data, power in the fuel and revenue totals, consistency section) (v1.08: the workbook works without LAMBDA support: no cell calls a
LAMBDA, the shipped file recalculates in LibreOffice without a single error, every value equals the independent Python
recomputation; the optional LAMBDA library (sheet Lambdas) is tested by copying each row's LAMBDA formula over the
whole row) (v1.07: every cell formula at most 100 characters (section 0);
LAMBDAs also outside the right column (ROWLABEL in column H), so every variant expands all LAMBDA calls; planned
retirement by type vs power_model_ref_v7_0 (test with data switched on); electricity demand memo lines; power
indicators on MTOutputs and Charts; regression vs v1.06 on every shared code with no intended change)
(v1.06: power engineer model, section 3 H-L: power_model_ref_v0_1 = cached legacy
rows with the bugs switched on; workbook = Python with all bug fixes; power CO2 in section 13; regression vs v1.05 apart
from the intended power and CO2 changes) (v1.05: power generation costs and electricity prices, section 3: Python
reference = cached legacy rows with the legacy inputs, workbook = Python with the MVP inputs, uniformity, outline)
(v1.04: first-run test macro CheckBatchRun and sheet MacroCheck,
run in LibreOffice, including a negative test) (v1.03: scenario definitions, VBA batch run, StoredResults,
ScenarioCompare; the macro itself is run in LibreOffice and compared with the Python emulation)
(v1.02: new ETS with cap, benchmarks, volatility, goal seek)
(v1.01: MTOutputs and Charts sheets) (v0.12 revenues; v0.13 CO2; v0.14 corrected Egypt prices;
v0.15 layout: row group buttons below, rolled up, Mitigation first at 75%; v0.16: one level of column groups incl.
2030-2039, light beige for the LAMBDA column and the price history block, blank column between scenario groups). Needs LibreOffice (soffice) to recalculate.

LibreOffice 24.2 cannot evaluate LAMBDA, so the 2035 LAMBDA cells are checked by expansion (body with the
arguments substituted) and by dragging the plain 2034 formula forward.

1. Shipped file: errors only in the 2035 columns.
2. Uniformity (relative R1C1): one formula per variable for base year / plain years / 2035, across all
   subsectors, fuels and scenarios; one formula per D:G column per variable; Section-1 input rows; paths;
   label and code columns.
3. LAMBDA encoding.
4. Values vs an independent Python recomputation from the CSVs (both 2035 variants): international prices,
   supply cost, taxes, retail price before new policies, the subsector variables and fuel use.
5. Scenario tests (MTInputs column + Mitigation group copied as a user would): copy = source; zero carbon price =
   baseline; legacy Egypt carbon-tax settings = legacy row 8582; fuel price reform, feebates, price source
   IMF-WB* with High adjustment and a nominal carbon price vs Python; feebates lower fuel use only where covered;
   global price controls None and Manual vs Python.
6. Regression vs v0.9 on every output code the two versions share, except the intended price changes
   (other oil products like the other oil products; VAT-rate assumption).
7. Labels and codes; 8. outline; 9. MTInputs = template; 10. format; 11. sanity and results.

    python check_v7_0.py   ->  writes check_report_v6.4.md
"""
import csv
import importlib.util
import math
import os
import re
import shutil
import subprocess
import tempfile
import types

import openpyxl
from openpyxl.formula.translate import Translator
from openpyxl.utils import get_column_letter as L, column_index_from_string as CI

import build_v7_2 as B
RS = getattr(B, 'rn_stem', lambda st: st)   # v7.2 (codes R9): a v7.1 code stem as the rename map writes it


def RC(code):
    """v7.2: a v7.1 output code country.mit.<stem>.<scenario> as the rename map writes it."""
    p = code.split('.')
    return '.'.join([p[0], RS('.'.join(p[1:-1])), p[-1]]) if len(p) > 3 else code
import power_model_ref_v7_0 as PM
import transport_model_ref_v7_0 as TM

HERE = os.path.dirname(os.path.abspath(__file__))
ISO = B.COUNTRY                 # v3.3: country of the build (Settings C4); its data come from the CSVs by this key
REF = re.compile(r"(?<![A-Za-z_\d.\"])(\$?)([A-Z]{1,3})(\$?)(\d+)(?![\d(])")
TOL = 1e-9
VAT_CONSUMER = {'coa.res', 'nga.res', 'gso.all', 'die.all', 'lpg.all', 'ker.all', 'oop.all'}   # independent copy
report = []


def log(line=''):
    print(line)
    report.append(line)


def auto_calc(path, tmp):
    """v7.0: a copy in automatic calculation with a full calculation on load, if the file is in manual calculation
    (the shipped workbook since v6.6; calcId of an older Excel, as openpyxl writes, so LibreOffice recalculates every cell): LibreOffice leaves the formulas of an openpyxl copy (no cached values)
    uncalculated in manual mode."""
    import zipfile
    with zipfile.ZipFile(path) as z:
        xml = z.read('xl/workbook.xml').decode('utf-8')
        if 'calcMode="manual"' not in xml:
            return path
        os.makedirs(os.path.join(tmp, 'in'), exist_ok=True)
        new = os.path.join(tmp, 'in', os.path.basename(path))   # own folder: the output keeps the name
        xml = re.sub(r'<calcPr[^>]*/>', '<calcPr calcId="124519" fullCalcOnLoad="1"/>', xml)
        with zipfile.ZipFile(new, 'w', zipfile.ZIP_DEFLATED) as zo:
            for it in z.infolist():
                zo.writestr(it, xml.encode('utf-8') if it.filename == 'xl/workbook.xml' else z.read(it.filename))
    return new


def hard_recalc(path, res):
    """v7.0: load in a LibreOffice session, calculateAll, save as xlsx. The conversion on load (soffice --convert-to,
    v4.16-v6.5) gives wrong values for the trailing averages of the power fuel prices (fpp; then swi, swd) in
    this LibreOffice: its recalculation on load evaluates some INDEX(...):cell ranges before their inputs."""
    import lo_session_v7_0 as LO
    with LO.Session(timeout=600) as s_:
        import uno
        from com.sun.star.beans import PropertyValue
        doc = s_.load(path)
        s_.calc(doc)             # two calculateAll (lo_session Session.calc; NORMS 3i.2)
        doc.storeToURL(uno.systemPathToFileUrl(res), (PropertyValue(Name='FilterName', Value='Calc MS Excel 2007 XML'),))


def recalc_path(path):
    cache = os.environ.get('CHECK_CACHE')            # v5.0: reuse LibreOffice results of identical files (debugging)
    if cache:
        import hashlib
        import zipfile
        h = hashlib.sha1()
        with zipfile.ZipFile(path) as z:               # contents only: openpyxl stamps docProps with the time
            for n in sorted(z.namelist()):
                if not n.startswith('docProps/'):
                    h.update(n.encode() + z.read(n))
        key = h.hexdigest()
        hit = os.path.join(cache, key + '.xlsx')
        if os.path.exists(hit):
            return hit
    out = tempfile.mkdtemp()
    path = auto_calc(path, out)                      # v7.0: the shipped file is in manual calculation
    res = os.path.join(out, os.path.splitext(os.path.basename(path))[0] + '.xlsx')
    hard_recalc(path, res)
    if cache:
        os.makedirs(cache, exist_ok=True)
        shutil.copy(res, hit)
    return res


def recalc_wb(path):
    return openpyxl.load_workbook(recalc_path(path), data_only=True)


def add_mto_blocks(wb, groups):
    """Add MTOutputs blocks as a user would: copy the last block (header to blank row) directly below."""
    ws = wb['LiveOutputs']
    for g in groups:
        s0, d0 = B.mto_row(g - 1, 0) - 1, B.mto_row(g, 0) - 1
        for k in range(B.MTO_BLOCK):
            for c in range(1, ws.max_column + 1):
                v = ws.cell(s0 + k, c).value
                if isinstance(v, str) and v.startswith('='):
                    v = Translator(v, origin=f'{L(c)}{s0 + k}').translate_formula(f'{L(c)}{d0 + k}')
                ws.cell(d0 + k, c).value = v
    return wb


def check_mto(wbv, groups, label):
    """Every MTOutputs indicator cell equals the Mitigation cell of its output code (searched in Python)."""
    wm, wo = wbv['Mitigation'], wbv['LiveOutputs']
    found, worst, n, missing = {}, 0.0, 0, []
    for g in groups:
        code, base, years = B.group_cols(g)
        for r in range(1, wm.max_row + 1):
            k = wm.cell(r, code).value
            if isinstance(k, str):
                found[k] = [wm.cell(r, c).value for c in [base] + years]
    for g in groups:
        num = wo.cell(B.mto_row(g, 0) - 1, 5).value
        for k, (stem, _f) in enumerate(B.MTO_INDICATORS):
            r = B.mto_row(g, k)
            key = wo.cell(r, 1).value
            if key not in found or num != g:
                missing.append(key)
                continue
            for j in range(B.NY):
                a, b = wo.cell(r, B.MTO_C0 + j).value, found[key][j]
                worst = max(worst, abs(a - b) if isinstance(a, (int, float)) and isinstance(b, (int, float))
                            else float('inf'))
                n += 1
    ok = not missing and worst < TOL
    log(f'- MTOutputs {label}: {len(groups)} scenario blocks x {len(B.MTO_INDICATORS)} indicators, {n} cells equal '
        f'the Mitigation cell of their output code (max abs diff {worst:.3g}); block numbers 1..{groups[-1]} '
        f'{"OK" if ok else "FAIL " + str(missing[:5])}')
    return ok


def check_charts():
    """v7.0: the dashboard charts (ScenarioCompare; the Charts sheet is gone): one bar chart on the chart-data row,
    one line chart per time-series block, each series on one slot row of its block with its short name as label."""
    wb = openpyxl.load_workbook(B.OUT)
    good = 'Charts' not in wb.sheetnames
    charts = wb['ScenarioCompare']._charts
    good &= len(charts) == 1 + len(B.SC_TS)
    ref = lambda s: s.val.numRef.f.replace("'", '').replace('$', '')
    bar = charts[0]
    good &= [ref(s) for s in bar.series] == [f'ScenarioCompare!{L(B.SC_C0 + 1)}{B.SC_BAR_R}:'   # slots 2-10 (vs Base)
                                             f'{L(B.SC_C0 + B.SC_SLOTS - 1)}{B.SC_BAR_R}']
    nser = []
    for i, ch in enumerate(charts[1:]):
        _h, _yr, s0, s1 = B.sc_ts_rows(i)
        for s in ch.series:
            m = re.match(r'ScenarioCompare!([A-Z]+)(\d+):([A-Z]+)(\d+)$', ref(s))
            good &= bool(m) and m.group(2) == m.group(4) and s0 <= int(m.group(2)) <= s1 \
                and m.group(1) == L(B.SC_C0) and m.group(3) == L(B.SC_Y1) \
                and s.tx.strRef.f.replace("'", '').replace('$', '') == f'ScenarioCompare!C{m.group(2)}'
        nser.append(len(ch.series))
    log(f'- v7.0 dashboard charts: no Charts sheet; {len(charts)} charts on ScenarioCompare (1 bar on row {B.SC_BAR_R}, '
        f'{len(charts) - 1} line charts with {nser} series on the slot rows of their block, short-name labels) '
        f'{"OK" if good else "FAIL"}')
    return good


def recalc(path):
    return openpyxl.load_workbook(recalc_path(path), data_only=True)['Mitigation']


def r1c1(formula, row, col):
    def sub(m):
        c, rw = CI(m.group(2)), int(m.group(4))
        return (f'R{rw}' if m.group(3) else f'R[{rw - row}]') + (f'C{c}' if m.group(1) else f'C[{c - col}]')
    return REF.sub(sub, str(formula))


ERR_VALUES = ('#NULL!', '#DIV/0!', '#VALUE!', '#REF!', '#NAME?', '#NUM!', '#N/A', 'Err:')


def is_err(v):
    return isinstance(v, str) and v.startswith(ERR_VALUES)


def split_args(text):
    """Split a function's argument text at top-level commas (INDEX(...) arguments contain commas)."""
    args, depth, cur = [], 0, ''
    for ch in text:
        if ch == ',' and depth == 0:
            args.append(cur)
            cur = ''
            continue
        depth += (ch == '(') - (ch == ')')
        cur += ch
    return args + [cur]


def expand(formula, lambdas=None):
    """Replace every call of a named LAMBDA (anywhere in the formula) by its body with the arguments substituted."""
    lambdas = lambdas or B.LAMBDAS
    pat = re.compile(r'(?<![A-Za-z_.])(' + '|'.join(lambdas) + r')\(')
    while True:
        m = pat.search(formula)
        if not m:
            return formula
        depth, k = 1, m.end()
        while depth:
            depth += (formula[k] == '(') - (formula[k] == ')')
            k += 1
        params, body = lambdas[m.group(1)]
        args = split_args(formula[m.end():k - 1])
        assert len(args) == len(params), formula
        for prm in sorted(params, key=len, reverse=True):
            body = re.sub(rf'(?<![A-Za-z_.]){prm}(?![A-Za-z_\d(])', f'({args[params.index(prm)]})', body)
        formula = formula[:m.start()] + '(' + body + ')' + formula[k:]


def rows_of(var):
    """(row, sector-or-subsector, fuel) of a variable: section 2 price rows or sector-section rows."""
    if var in B.PVARS:
        return [(B.prow(var, pc), pc.split('.')[1], pc.split('.')[0]) for pc, _l in B.PRICES]   # v2.5: fuel blocks
    if var in B.VARS:                      # subsector variables first (power CO2 shares the name co2)
        return B.var_rows(var)
    return [(r, c_, b_) for r, v, b_, c_, _k in B.PW_ROWS if v == var]


def groups_in(ws):
    return [g for g in range(1, 40) if ws.cell(B.R_SCEN, B.group_cols(g)[0]).value not in (None, '')]


LAMBDA_CALL = re.compile(r'(?<![A-Za-z_.])(' + '|'.join(B.LAMBDAS) + r')\(')


def lambda_rows(ws, c):
    """Rows whose cell in column c calls a named LAMBDA."""
    return [r for r in range(1, ws.max_row + 1)
            if isinstance(ws.cell(r, c).value, str) and LAMBDA_CALL.search(ws.cell(r, c).value)]


def lambda_table(lam):
    """v4.2: sheet Lambdas -> {Mitigation row: (first row of its line, formula of the first row)}."""
    out = {}
    for i in range(5, lam.max_row + 1):
        rows, f = lam.cell(i, 4).value, lam.cell(i, 3).value
        if not rows or not f:
            continue
        rr = []
        for part in str(rows).split(','):
            a, _s, b = part.strip().partition('-')
            rr += list(range(int(a), int(b or a) + 1))
        for r in rr:
            out[r] = (rr[0], f)
    return out


def variant(wb, how):
    """how = 'expand': LAMBDA bodies substituted in the right column; 'drag': plain formula of the previous year
    dragged into the right column; 'everywhere': the right-column LAMBDA formula copied back over the whole row
    (base year included, except fuel use whose base year is data), then expanded."""
    ws = wb['Mitigation']
    if how == 'everywhere':                # v1.08: the optional LAMBDA library (sheet Lambdas) over whole rows
        lam = B.tab(wb, 'Lambdas')
        src_c = B.group_cols(1)[2][-1]
        ener = ({r for r, *_ in B.var_rows('enel')} | {r for r, v, *_ in B.PW_ROWS if v in B.PW_BASE}
                | B.TR_OWNBASE | B.LK_OWNBASE                 # v3.5: section 5b rows with their own base year (v5.1: 6b)
                | {B.R_GHG[k] for k in B.GHG_LAM}             # v2.8: section 14 rows have their own base year
                | {B.R_GDPS[k] for k in B.GDP_OWNBASE} | {B.R_GDP})                 # v3.1
        for r, (r0, f) in lambda_table(lam).items():     # v4.2: one line per formula pattern, rows in column D
            for g in groups_in(ws):
                _, base, years = B.group_cols(g)
                for k in ([base] if r not in ener else []) + years:
                    ws.cell(r, k).value = expand(Translator('=' + f, origin=f'{L(src_c)}{r0}')
                                                 .translate_formula(f'{L(k)}{r}'))
    for wsx in wb.worksheets:              # v1.07: LAMBDA calls elsewhere (ROWLABEL in column H)
        for row in wsx.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and cell.value.startswith('=') and LAMBDA_CALL.search(cell.value):
                    cell.value = expand(cell.value)
    path = os.path.join(tempfile.mkdtemp(), f'{how}.xlsx')
    wb.save(path)
    return path


# ------------------------------------------------------------------ independent recomputation
def read(name):
    with open(os.path.join(HERE, '..', '..', 'data', 'mvp_legacy_extracts', name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


_MT_TPL = {}


def mt_used():
    if not _MT_TPL:                              # v5.1: the template read once (scenario_mt is called per recompute)
        tpl = openpyxl.load_workbook(B.MT_TEMPLATE)['MTInputs']
        _MT_TPL.update({r: tpl.cell(r, 6).value for r in range(8, tpl.max_row + 1)})
    mt = dict(_MT_TPL)
    par = {r['key']: r['value'] for r in read('transport_params.csv')}     # v3.5: transport policy rows (defaults)
    for i, (k, *_x) in enumerate(B.TR_MT):
        v = TM.fnum(par[k])
        mt[B.MT_TR0 + 1 + i] = int(v) if isinstance(v, float) and v.is_integer() and v >= 1000 else v
    for name, _lab, _unit, v in B.PW_MT_NEW:        # v5.4: power rows after the transport rows
        mt[B.MT_NAMES[name]] = v
    return mt


def series(row, years):
    return {y: float(row[str(y)]) for y in years if row.get(str(y)) not in ('', None)}


ETS_VOL = {lab: (v, i) for lab, v, i in B.ETS_VOL}                 # legacy table (Settings C16:F18)
K = B.const_values()                # v3.4: sheet Constants values (no literals in the recomputation)
_PC = {(int(r['row']), int(r['col'])): r['value'] for r in csv.DictReader(open(os.path.join(HERE, '..', '..', 'data', 'mvp_legacy_extracts',
                                                                                   'legacy_Power_cells.csv'),
                                                                      encoding='utf-8')) if int(r['row']) < 30}
K_SCALE = {_PC[(r, 9)]: float(_PC[(r, 10)]) for r in range(20, 24) if (r, 9) in _PC}   # v5.4: Power I20:J23
_MI = {}


def mi(cell=None):
    """v5.2: the typed values of sheet Manual inputs (legacy addresses) of the shipped file, read once: the
    recomputation reads these inputs (never the formulas that read them). mi('J196') = one value; mi() = all."""
    if not _MI:
        from openpyxl.utils import get_column_letter
        wb = openpyxl.load_workbook(B.OUT, read_only=True)
        for row in wb['Manual inputs'].iter_rows(min_row=1, max_row=400):
            for c in row:
                if getattr(c, 'value', None) is not None:
                    _MI[f'{get_column_letter(c.column)}{c.row}'] = c.value
        wb.close()
    return _MI if cell is None else _MI.get(cell)


def mi_row(r, c0, c1):
    """v5.2: values of Manual inputs row r, columns c0..c1 (numbers)."""
    from openpyxl.utils import get_column_letter
    return [mi(f'{get_column_letter(c)}{r}') for c in range(c0, c1 + 1)]


def mi_controls():
    """v5.2: price control (pass-through) of each price code when GovPriceControls = Manual: Manual inputs J167:J180
    by code (G); blank = 1, as legacy L747:L760."""
    out = {}
    for r in range(167, 181):
        code, v = mi(f'G{r}'), mi(f'J{r}')
        out[str(code)] = float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else 1.0
    return out


def mi_pint(years):
    """v5.2: manual international prices {commodity: {year: value}}, Manual inputs D221:AF225 (years row 220; blank
    = 0, as a reference to an empty cell), global gas = average of LNG, North America, Europe."""
    yrs = mi_row(220, 10, 32)
    out = {}
    for r in range(221, 226):
        lab = mi(f'D{r}')
        c_ = next(c for c, l_, _u in B.IPI_COMS if l_ == lab)
        out[c_] = {int(y): (float(v) if isinstance(v, (int, float)) else 0.0)
                   for y, v in zip(yrs, mi_row(r, 10, 32)) if int(y) in years}
    out['nga.glo'] = {y: sum(out[k][y] for k in ('nga.lng', 'nga.nam', 'nga.eur')) / 3 for y in out['oil']}
    return out


def mi_bev(years):
    """v5.2: BEV fuel economy of new vehicles (km/kWh), Manual inputs J375:AC377 by year (row 374), as the
    transport reference's paths bev_fe_new|pass, fre, cyc."""
    yrs = [int(y) for y in mi_row(374, 10, 29)]
    return {k: [float(dict(zip(yrs, mi_row(r, 10, 29)))[y]) for y in years]
            for k, r in (('bev_fe_new|pass', 375), ('bev_fe_new|fre', 376), ('bev_fe_new|cyc', 377))}
_BASE = {}


def baseline_co2():
    """Baseline CO2 by ETS sector (scenario 1, template price controls), from the Python recomputation."""
    if not _BASE:
        r = _recompute_once(scenario_mt(1), base={})
        _BASE.update({s: [sum(r[('co2', s, f)][k] for f in [x[0] for x in B.FUELS] if ('co2', s, f) in r)
                          for k in range(len(B.YEARS) + 1)] for s in B.COV_SECTORS})
    return _BASE


def _ecp_cells():
    """v4.12: the legacy ECP tab as {(row, column): value} (data/legacy_ECP_cells.csv; error values left out)."""
    out = {}
    for r in read('legacy_ECP_cells.csv'):
        v = r['value']
        if re.fullmatch(r'0x[0-9a-f]{2}', v):
            continue
        try:
            v = float(v) if v.lower() not in ('nan', 'inf', '-inf', 'infinity') else v
        except ValueError:
            pass
        out[(int(r['row']), int(r['col']))] = v
    return out


ECP_CELLS = _ecp_cells()


def ecp_tables(cells, cpi):
    """v4.12, independent copy of Inputs_ecp (legacy rows 1677-1764): each code looked up by key (column E) in its
    legacy block; country information rows 11-66 (C code, E single price, K EU ETS); prices x CPI factor, blanks 0;
    fuel tax rate = single rate where the country has a single price or no fuel rate. Returns the carbon tax and ETS
    tables {(ECP sector, fuel): {year: $/tCO2 real}} and the national ETS sector coverage {sector: {year: share}}."""
    txt = lambda v: '' if v is None else (str(int(v)) if isinstance(v, float) and v.is_integer() else str(v))
    info = next((r for r in range(11, 67) if txt(cells.get((r, 3))).lower() == ISO.lower()), None)
    sgl = txt(cells.get((info, 5))).lower() == 'yes' if info else False
    euon = txt(cells.get((info, 11))).lower() in ('yes', 'both') if info else False
    keys = {}
    for (r, c), v in sorted(cells.items()):
        if c == 5:
            keys.setdefault(txt(v).lower(), []).append(r)
    col = {y: 6 + y - 2015 for y in B.ECP_YEARS}
    num = lambda r, y: cells.get((r, col[y])) if isinstance(cells.get((r, col[y])), float) else 0.0
    vals = {}
    for code, lkey in B.ECP_CODES:
        kind, m = code.split('.')
        a, b = B.ECP_BLOCKS[kind]
        key = 'eu.mit.eer.all' if code == 'rer.all' else f'{ISO.lower()}.mit.{lkey}'
        r = next((x for x in keys.get(key, []) if a <= x <= b), 0)
        if kind in ('rer', 'res', 'ref') and not euon:
            r = 0
        if kind == 'ecr' and m != 'all':
            vals[code] = {y: vals['ecr.all'][y] if sgl or not r else num(r, y) * cpi[y] for y in B.ECP_YEARS}
        elif kind in ('ecr', 'eer', 'rer'):
            vals[code] = {y: num(r, y) * cpi[y] if r else 0.0 for y in B.ECP_YEARS}
        else:
            vals[code] = {y: num(r, y) if r else 0.0 for y in B.ECP_YEARS}
    XT, XE = {}, {}
    for s_ in B.ECP_SECS:
        for f_ in [x[0] for x in B.FUELS]:
            g = lambda c_, y: vals[c_][y]
            XT[(s_, f_)] = {y: g('ecr.' + f_, y) * g('ecs.' + s_, y) * g('ecf.' + f_, y) for y in B.ECP_YEARS}
            XE[(s_, f_)] = {y: g('eer.all', y) * g('ees.' + s_, y) * g('eef.' + f_, y)
                            + g('rer.all', y) * g('res.' + s_, y) * g('ref.' + f_, y) for y in B.ECP_YEARS}
    return XT, XE, {s_: vals['ees.' + s_] for s_ in B.ECP_SECS}


ECP_SEC = lambda s: 'pow' if s == 'pow' else {'tra': 'trs', 'bld': 'res'}.get(  # independent copy (legacy ECP sectors)
    next(x[2] for x in B.SUBSECTORS if x[0] == s), 'ind')


def co2k():
    """v3.2: CO2 calibration factor: inventory energy CO2 / scenario-1 energy CO2 with uncalibrated EFs (independent
    copy of Settings C29; the template's scenario-1 switch). v4.11, as legacy: the inventory of the year before the
    base year against the base-year estimate."""
    if _CO2K.get('busy'):                  # inside the uncalibrated run (its scenario-1 reference): uncalibrated
        return 1.0
    if 'k' not in _CO2K:
        _CO2K['busy'] = True
        inv = {int(r['year']): float(r['enr.co2']) for r in read('ghg_inventory.csv') if r['iso'] == ISO}
        on = str(B.CO2_CALIB)[:3] == 'Yes'                 # Settings C27 (v4.11: on, as legacy)
        raw = _recompute_once(scenario_mt(1), base={}, k_co2=1.0)[('co2', 'all', 'all')]
        _CO2K['k'] = inv[B.BASE_YEAR - 1] / raw[0] if on else 1.0   # v4.11: legacy rows 623, 839
        _CO2K['busy'] = False
    return _CO2K['k']


_CO2K = {}


_PDATA = {}


PDATA_NAMES = [n for n in B.MT_NAMES if n.startswith('NewInv')] + [
    'RenewableCostDeclineRate', 'MinimumThermalEfficiency', 'CFOverrideIfBelowWndSol', 'CFOverrideIfBelowFosOth',
    'CFOverrideIfAbove', 'HydroDoesntRetire', 'WACCSource', 'WACCUserGlobal', 'MinimumWACC',
    'MaxNonVREAsPCOfTotalGen', 'MaxNonNucOreBioAsPCOfTotalGen', 'MaxWindSolarScaleup', 'MaxScaleUpRateCategory',
    'StorageHoursForLTStorage']


def power_data(years, mt=None):
    """v5.2: power data of the country as the MVP's data step computes them (power_model_ref_v7_0.mvp_data: legacy
    data-step bugs L52-L55 fixed), from the legacy Power tab and Balances. v5.4 (P2): with the settings of the
    scenario (mt: its MTInputs column; default the template, scenario 1)."""
    mt = mt or mt_used()
    s = {nm: mt[B.MT_NAMES[nm]] for nm in PDATA_NAMES}
    key = (tuple(years), tuple(sorted((k, str(v)) for k, v in s.items())))
    if key not in _PDATA:
        _PDATA[key] = PM.mvp_data(ISO, list(years), s, B.BASE_YEAR, K['HydInvShare'], K['InvPresentShare'])
    return _PDATA[key]


DEFICIT_GAS = {'on': False}     # v5.4: Settings C45 PwDeficitGas (global switch) of the run
MI_EXCISE = {}                  # v5.4: 'Manual inputs' new electricity excise of the run {group: {year: $/kWh}}


def power_settings(mt, years, cp, defl, cpi=None):
    """v5.4 (power plan P1, P2, P4): the power settings of the scenario (MTInputs column mt) and the power policy
    paths (PPA share, renewable subsidy, rebate switch, electricity excise, manual excise), recomputed from the
    inputs independently of the workbook. cp: carbon price trajectory {year: $/tCO2}; defl: deflator index."""
    n = B.MT_NAMES
    g = lambda nm: mt[n[nm]]
    yes = lambda v: str(v)[:3] == 'Yes'
    scen = mt.get('scen', 1)
    par = {'pass': float(g('PowerSectorPriceChangePassOn')), 'k_dispatch': float(g('kDispatch')),
           'k_invest': float(g('kInvestment')), 'min_cost': float(g('MinPostSubsidyPowerPrice')),
           'st_alloc': float(g('AllocateSTStorageToVRE')),
           'st_marg_hours': K['StMargFactor'] * float(g('TotalHoursStorageFor100pcVRE')),
           'st_ratio': float(g('StorageToInterfaceRatioSTStorage')), 'lt_start': float(g('StartingPointWhenLTStorageIsNeeded')),
           'lt_alloc': float(g('AllocateLTStorageToVRE')), 'lt100': float(g('LongTermStorageFor100pcVRE')),
           'extra_eff': float(g('AdditionalEfficiencyPower')), 'maxcf_coa': float(g('MaximumCoalCF')),
           'maxcf_nga': float(g('MaximumGasCF')), 'shock_k': float(g('EngineerModelProportionOfCovidFactor')),
           'early_factor': 0.0 if scen == 1 and g('EarlyRetirementInBaseline') != 'Yes'
           else float(g('MaxCostBasedEarlyRetirement')), 'dgas': DEFICIT_GAS['on']}
    on = yes(g('PhaseOutCoalAndGasPPAsBaseline') if scen == 1 else g('PhaseOutCoalAndGasPPAsPolicy'))
    y0, ny_ = float(g('YearPPACoalGas')), float(g('YearsToPhaseOutPPAs'))
    ppa = [float(g('PPAProportionCoalGas')) * (max(0.0, 1 - max(0.0, y - y0) / ny_) if on else 1.0) for y in years]
    s0, sa, ys, yn = (float(g('RenewableSubsidyBL')), float(g('RenSubsidyAddUSDkwh')),
                      float(g('RenSubsidyAddStartYear')), float(g('RenSubsidyAddPhaseoutYrs')))
    rnsp = [-(s0 + (sa * max(0.0, 1 - (y - ys) / yn) if scen > 1 and y >= ys else 0.0)) * (cpi[y] if cpi else 1.0)
            for y in years]                                # v6.0: nominal inputs to real (L114 fixed, v5.6)
    elig = [1.0 if f in ('wnd', 'sol', 'ore', 'bio') else 1.0 if f == 'hyd' and yes(g('RenewableSubsidyHydro'))
            else 0.0 for f in POWER_TECH]
    scn = [r[1] for r in B.SCN_TABLE]                       # legacy scenario table (MTInputs ScenarioSelected)
    sel = [r[0] for r in B.SCN_TABLE]
    name = scn[sel.index(g('ScenarioSelected'))] if g('ScenarioSelected') in sel else None
    reb = 1.0 if scen > 1 and (yes(g('PowerRebates')) or B.SCN_POWER.get(name, ('No', 'No'))[0] == 'Yes') else 0.0
    exs_on = scen > 1 and name is not None and B.SCN_POWER.get(name, ('No', 'No'))[1] == 'Yes'
    exs = [grid_intensity() * cp[y] if exs_on else 0.0 for y in years]
    real = str(g('NomorReal'))[:4] == 'Real'
    ntxd = {u: [MI_EXCISE.get(u, {}).get(y, 0.0) for y in years] for u in ('res', 'ind')}
    ntx = {u: [ntxd[u][k] * (1.0 if real else defl[y]) if scen > 1 and yes(g('AdditionalExcise')) else 0.0
               for k, y in enumerate(years)] for u in ('res', 'ind')}
    return {'par': par, 'ppa': ppa, 'rns': [[e * x for x in rnsp] for e in elig], 'reb': reb, 'exs': exs,
            'ntx': ntx}, {'rnsp': rnsp, 'ntxd': ntxd}


def grid_intensity():
    """v5.4: base-year CO2 of the fuel input to power / power output (tCO2 per kWh; legacy C2253 = G623 / E603), with
    the power EFs of the MVP (calibrated) and the Balances of the country."""
    bal = {r['flow_code']: r for r in read('legacy_Balances.csv') if r['country_code'] == ISO}
    kc = co2k()
    ef = {r['key']: float(r['ef_tco2_per_gj']) * kc for r in read('ef_co2.csv')}
    fuels = {'oop': ['oop', 'gso', 'die', 'ker', 'lpg', 'jfu']}
    co2 = out = 0.0
    for f in POWER_TECH:
        fl = fuels.get(f, [f])
        inp = -sum(float(bal['power'][u] or 0) for u in fl)
        out += sum(float(bal['eloutput'][u] or 0) for u in fl)
        co2 += inp * B.PJ_PER_KTOE * ef.get(f'{ISO}|{f}|pow', 0.0)
    return co2 / out


def _recompute_once(mt, controls=None, bench=None, ovr=None, base=None, shock_on=1, power=None, ecp=None,
                    spot=False, gdp=None, k_co2=None, road=None):
    """mt: MTInputs row -> value for one scenario; controls: global GovPriceControls (default: template); bench:
    {group: (start, target)} ETS benchmarks (default 1 - the MTInputs auctioned shares, v4.15); ovr: {year: price} override row (default blank);
    base: baseline CO2 by ETS sector (default: scenario 1 recomputed); ecp: {code: {year: nominal value}} existing
    carbon pricing data of the country (default: data/ecp.csv rows of the country).
    v1.09: existing carbon pricing, power fuel use in the fuel totals, power revenues in the revenue totals.
    Returns {(var, sector-or-subsector, fuel): [values base..last]} for gp, sp, txo, rpb and the subsector
    variables, all from the CSVs."""
    tpl = mt_used()
    ry, controls = tpl[B.MT_NAMES['ResultsYear']], controls or tpl[B.MT_NAMES['GovPriceControls']]
    units = {r['fuel']: float(r['gj_per_price_unit']) for r in read('fuel_units.csv')}
    dom = {r['country_year']: r for r in read('prices_dom.csv')}
    kc = co2k() if k_co2 is None else k_co2                         # v3.2: calibrated CO2 EFs
    ef = {r['key']: float(r['ef_tco2_per_gj']) * kc for r in read('ef_co2.csv')}
    el = {r['key']: float(r[INCOME[ISO]]) for r in read('elasticities.csv')}
    use0 = {(r['subsector'], r['fuel']): float(r['ktoe']) for r in read('energy_use.csv')}
    weo = read('weo.csv')[0]
    yrs_all = list(range(2021, 2046))
    us = {r['key']: series(r, yrs_all) for r in read('weo_us.csv')}
    cpi = {y: us['USA|pcpi'][ry] / us['USA|pcpi'][y] for y in us['USA|pcpi']}
    dfl = {y: us['USA|ngdp_d'][ry] / us['USA|ngdp_d'][y] for y in us['USA|ngdp_d']}
    pint = {r['key']: series(r, yrs_all) for r in read('prices_int.csv')}
    for c_, vals in mi_pint(yrs_all).items():          # v5.2: Manual from 2026 = sheet Manual inputs D221:AF225
        pint[f'Manual|{c_}'].update({y: v for y, v in vals.items() if y >= 2026})
    pctrl = mi_controls()
    gas = {'Global': 'glo', 'LNG': 'lng', 'Europe': 'eur', 'North Am': 'nam'}[
        next(r['gas_market'] for r in read('price_assumptions.csv') if r['country_name'] == NAME)]
    sub = {s[0]: s for s in B.SUBSECTORS}
    fue = {f[0]: f for f in B.FUELS}
    years = [B.BASE_YEAR] + B.YEARS
    last_hist = B.LAST_HIST
    n = B.MT_NAMES
    gdpg = list(gdp) if gdp is not None else [float(weo[str(y)]) for y in years]   # v3.1: growth after the feedback

    def val(col, y):
        v = dom[f'{ISO}{y}'].get(col, '')
        return float(v) if v not in ('', None) else 0.0

    def path(y, y0, y1, s0, t, linear=True):
        if y < y0:
            return 0.0
        k = y - y0 if (y <= y1 or linear) else y1 - y0
        return s0 + (t - s0) / max(y1 - y0, 1) * k
    nominal = str(mt[n['NomorReal']]).startswith('Nominal')
    cp = {y: path(y, mt[n['CPIntro']], mt[n['CPOutro']], mt[n['CPLevelStart']], mt[n['CPLevelTarget']],
                  mt[n['ExtendCarbonPriceBeyondOutro']] == 'Linear*') * (cpi[y] if nominal else 1) for y in years}
    fpr = {pc: {y: path(y, mt[140], mt[141], mt[r0] or 0, mt[r1] or 0) for y in years}
           for pc, _l, r0, r1 in B.PRICE_FUELS}
    fb = {s: {y: path(y, mt[n['D_FeebateIntro']], mt[n['D_FeebateOutro']], mt[n[a]], mt[n[b]]) for y in years}
          for s, a, b in B.FEEBATE_SECTORS}
    y0, y1 = mt[n['D_ETSIntro']], mt[n['D_ETSOutro']]
    ets_on = {y: str(mt[n['D_NewETS']]).startswith('Yes') and y >= y0 for y in years}
    ets_cov = {s: {y: 1.0 if ets_on[y] and bool(mt[B.MT_ROWS_FIXED['etscov0'] + k]) else 0.0 for y in years}
               for k, s in enumerate(B.COV_SECTORS)}
    auct = (float(mt[n['D_ETSAuctStart']] or 0), float(mt[n['D_ETSAuctTarget']] or 0))   # v4.15 (I21): MTInputs 90-91
    bench = bench or {g: (1 - auct[0], 1 - auct[1]) for g, *_ in B.ETS_GROUPS}
    bm = {g: {y: 0.0 if y < y0 else b0 + (b1 - b0) / max(y1 - y0, 1) * (min(y, y1) - y0) for y in years}
          for g, (b0, b1) in bench.items()}
    obr = {s: {y: min(1.0, max(0.0, bm[B.ETS_GROUP_OF[s]][y])) for y in years} for s in B.COV_SECTORS}
    vol = ETS_VOL[str(mt[n['D_ETSVolatility']]).replace('*', '')][0]
    imp = ETS_VOL[str(mt[n['D_ETSVolImpact']]).replace('*', '')][1]
    vadj = (1 + mt[n['D_ETSCTRisk']] * imp) / (1 + vol * imp)
    base = baseline_co2() if base is None else base
    bco2 = {s: base.get(s, [0.0] * len(years)) for s in B.COV_SECTORS}
    yi = {y: k for k, y in enumerate(years)}
    bce = {y: sum(bco2[s][yi[y]] * ets_cov[s][y] for s in B.COV_SECTORS) for y in years}
    rs, rt = mt[n['D_ETSChangeRelStart']], mt[n['D_ETSChangeRelTarget']]
    cap = {}
    for y in years:
        if not ets_on[y]:
            cap[y] = 0.0
        elif y > y1 and str(mt[n['D_ETSCapCont']]).startswith('Constant'):
            cap[y] = cap[y - 1]
        else:
            cap[y] = bce[y] * (1 + rs + (rt - rs) / max(y1 - y0, 1) * (min(y, y1) - y0))
    es = next(r for r in read('ets_semi.csv') if r['iso'] == ISO)   # v3.3: legacy ETS+LTS table, by country
    semi = {s: float(es[B.ETS_SEMI_OF[s]]) for s in B.COV_SECTORS}   # sector -> group (also tested in Variables)
    se = {y: (sum(bco2[s][yi[y]] * ets_cov[s][y] * semi[s] * (1 - (1 - B.OBR_EFF) * obr[s][y]) for s in B.COV_SECTORS) / bce[y]
              if bce[y] > 0 else 0.0) for y in years}
    est = {y: math.log(cap[y] / bce[y]) / (se[y] * vadj) if ets_on[y] and 0 < cap[y] < bce[y] and se[y] < 0 else 0.0
           for y in years}
    override = str(mt[n['D_ETSPriceOverride']]).startswith('Yes')
    ets_p = {y: ((cp[y] if (ovr or {}).get(y) in (None, '') else ovr[y]) if override else est[y]) if ets_on[y]
             else 0.0 for y in years}
    ets_pe = {y: ets_p[y] * vadj for y in years}
    # existing carbon pricing (v4.12, as legacy rows 1677-1764): tables by ECP sector | fuel from the legacy ECP tab
    if ecp is None:
        ecp = ECP_CELLS
    XT, XE, ees_nat = ecp_tables(ecp, cpi)
    ecp_last = max(B.ECP_YEARS)
    yd = lambda y: min(y, ecp_last)                    # data year of a model year
    yemb = min(last_hist, ecp_last)                    # level embedded in the price data
    xf = {}
    for sch, sw, gr in (('xct', 'ExistingCTApply', 'ExistingCTGrowth'), ('xets', 'ExistingETSApply', 'ExistingETSGrowth')):
        on, g_ = str(mt[n[sw]]).startswith('Yes'), float(mt[n[gr]] or 0)
        xf[sch] = {y: (1 + g_) ** max(0, y - ecp_last) if on else 0.0 for y in years}
    xlev = lambda j, f, y: XT.get((j, f), {}).get(yd(y), 0.0) * xf['xct'][y] + XE.get((j, f), {}).get(yd(y), 0.0) * xf['xets'][y]
    xemb = lambda j, f: XT.get((j, f), {}).get(yemb, 0.0) + XE.get((j, f), {}).get(yemb, 0.0)
    comp = str(mt[n['CTaxComplimentaryToETS']]).startswith('Yes')
    sc_used = lambda s, sw, y: (1 - ees_nat.get(ECP_SEC(s), {}).get(yd(y), 0.0)) if comp else float(bool(sw))

    res = {}
    res[('cptraj', '', '')] = [cp[y] for y in years]
    for k_, d_ in (('ets.p', ets_p), ('ets.pe', ets_pe), ('ets.cap', cap), ('ets.est', est), ('ets.bce', bce),
                   ('ets.se', se), ('xct.p', xf['xct']), ('xets.p', xf['xets']),
                   ('xct.c', {y: B.ECP_YEARS.index(yd(y)) + 1 for y in years})):
        res[(k_, '', '')] = [d_[y] for y in years]
    for s in B.COV_SECTORS:
        res[('bco2', s, '')] = bco2[s]
        res[('obr', s, '')] = [obr[s][y] for y in years]
    # international prices
    src = str(mt[n['IntEnerPricForeSource']]).replace('*', '')
    adj = str(mt[n['IntEnerPricForecastAdjustment']])
    gp = {}
    for fu, _lab, _key, hi, lo in B.GP_ROWS:
        comm = {'oil': 'oil', 'coa': 'coa', 'nga': f'nga.{gas}'}.get(fu)
        fac = hi if adj.startswith('High') else (lo if adj.startswith('Low') else 1)
        gp[fu] = [1.0 if comm is None else pint[f'{src}|{comm}'][y] * dfl[y] * (fac if y > last_hist else 1)
                  for y in years]
        res[('gp', 'int', fu)] = gp[fu]
    # v4.16 (LD18, LD19): phase-out factors (legacy rows 2211-2218), lines by price fuel | sector and by fuel
    yes = lambda v: v is True or str(v).startswith('Yes')
    sc_ = mt.get('scen', 2)
    pof = {}
    for k_, _lab, psw, bsw, yr_, pn_, bn_, psh, bsh in B.PHASEOUTS:
        on = (yes(mt[n[psw]]) and (sc_ > 1 or yes(mt[n[bsw]]))) if k_ == 'pc' else yes(mt[n[bsw if sc_ == 1 else psw]])
        per = float(mt[n[bn_ if sc_ == 1 else pn_]])
        sh = float(mt[n[bsh]]) if sc_ == 1 else max(float(mt[n[bsh]]), float(mt[n[psh]]))
        t0 = float(mt[n[yr_]])
        pof[k_] = {y: max(1 - sh, 1 - sh * (y - t0) / max(per, 1) if on and y > t0 else 1.0) for y in years}
    def scope(incl):                    # v6.0: v5.6 moved the scope switches from Constants to MTInputs rows
        pre, a_, b_ = incl.split('|')
        name = {'csi': 'ConsSubPhaseScope_', 'pci': 'PriceCtrlPhaseScope_', 'psi': 'ProdSubPhaseScope_'}[pre] \
            + (a_ if pre == 'psi' else f'{a_}_{b_}')
        if name not in n:
            return float(K[incl])
        v = mt[n[name]]
        return 1.0 if v is True or v == 1 or str(v).startswith('Yes') else 0.0
    line = lambda incl, k_: {y: 1 - scope(incl) * (1 - pof[k_][y]) for y in years}
    csf = {pc: line(f'csi|{pc.replace(".", "|")}', 'cs') for pc, _l in B.PRICES}
    pcf = {pc: line(f'pci|{pc.replace(".", "|")}', 'pc') for pc, _l in B.PRICES}
    psf = {f: line(f'psi|{f}|all', 'ps') for f, _l in B.PROS_FUELS}
    pros = {}
    for f, _l in B.PROS_FUELS:                     # USD m real: data up to the last price year, then held
        pros[f] = []
        for y in years:
            pros[f].append(val(f'mit.pros.{f}.all', y) * cpi[y] * 1000 if y <= last_hist else pros[f][-1])
    # v4.16 (LD9): regulations as shadow prices (main scenario, legacy scenario table)
    srow = next((i for i, t in enumerate(B.SCN_TABLE) if t[0] == mt[n['ScenarioSelected']]), None)
    expl = srow is None or B.SCN_TABLE[srow][2] == 'Yes'
    adjpos = 0 if srow is None else B.SCN_TABLE[srow][3]
    regadj = float(mt[n[B.REG_PARAMS[adjpos]]]) if adjpos else 0.0
    covs = [] if srow is None else (B.COV_SECTORS if B.SCN_TABLE[srow][4] == '*' else B.SCN_TABLE[srow][4])
    cpx = {y: cp[y] if expl else 0.0 for y in years}
    reg = {s: {y: (cp[y] - cpx[y]) * regadj * (1.0 if s in covs else 0.0) for y in years} for s in B.COV_SECTORS}
    fbadj = float(mt[n['SPPEffAdjFeebates']])
    res[('cpx', '', '')] = [cpx[y] for y in years]
    # domestic prices
    rpb, vrate = {}, {}
    for pc, _lab in B.PRICES:
        fuel, sec = pc.split('.')
        gj = units[fuel]
        pccr = 1.0 if fuel == 'bio' else val(f'mit.ps.{pc}', B.BASE_YEAR)
        pccb = 0.0 if pccr <= K['PassLo'] else (K['PassMid'] if pccr <= K['PassHi'] else 1.0)
        pcc = pctrl[f'mit.rp.{pc}.ctrl'] if controls.startswith('Manual') else (1.0 if controls.startswith('None')
                                                                                 else pccb)   # v5.2: Manual inputs
        mar = 0.0 if fuel == 'bio' else val(f'mit.mar.{pc}', B.BASE_YEAR)
        pcost = val(f'mit.{fuel}.prod.cost', B.BASE_YEAR) if fuel in ('coa', 'nga') else 0.0
        fixsp = (mar + pccb * pcost) * cpi[B.BASE_YEAR] / gj
        def vat(y):                      # dataset rate if the cell is filled (0 included), else the assumption
            raw = dom[f'{ISO}{y}'].get(f'mit.vatrate.{pc}', '')
            if raw not in ('', None):
                return float(raw)
            return val('VAT_WEO', y) if pc in VAT_CONSUMER else 0.0
        vr = vat(last_hist) * OIL_SHARE.get(pc, 1.0)     # v4.12 (LD5): VAT x household share, as legacy 801-816
        vrate[pc] = vr

        def hist_txo(y):
            vry = vat(y)
            raw = (val(f'mit.rp.{pc}', y) / (1 + vry) - val(f'mit.sp.{pc}', y) if fuel in B.RP_FROM_DATA
                   else val(f'mit.txo.{pc}', y))
            return raw * cpi[y] / gj
        sp_l, txo_l = val(f'mit.sp.{pc}', last_hist) * cpi[last_hist] / gj, hist_txo(last_hist)
        g = gp[{1: 'oil', 2: 'coa', 3: 'nga', 4: 'one'}[B.GP_POS[fuel]]]
        sp, txo = [], []
        for k, y in enumerate(years):
            if y <= last_hist:
                sp.append(val(f'mit.sp.{pc}', y) * cpi[y] / gj)
                txo.append(hist_txo(y))
            else:
                sp.append(fixsp + (sp[-1] - fixsp) * g[k] / g[k - 1])
                cs_l = txo_l * (1 - pcc)
                cs = cs_l + (sp_l - sp[-1]) * (1 - pcc)          # v4.10: L14 fixed (legacy: (sp_l - sp + cs_l)(1 - pcc))
                txo.append(txo_l * pcc + (max(cs_l, cs) if cs_l >= 0 else cs))
        rpb[pc] = [(a + b) * (1 + vr) for a, b in zip(sp, txo)]
        res[('sp', sec, fuel)], res[('txo', sec, fuel)], res[('rpb', sec, fuel)] = sp, txo, rpb[pc]
        res[('txf', sec, fuel)] = [t_ if y <= last_hist          # v2.5: before the floor; v4.10: L14 fixed
                                   else txo_l + (sp_l - s_) * (1 - pcc)
                                   for y, s_, t_ in zip(years, sp, txo)]
        res[('spf', sec, fuel)] = [fixsp] * len(years)
        res[('gpi', sec, fuel)] = list(g)                                 # v2.6: international reference price
        res[('vat', sec, fuel)] = [(a + b) * vr for a, b in zip(sp, txo)]
        res[('etx', sec, fuel)] = [max(t, 0.0) for t in txo]
        res[('esub', sec, fuel)] = [min(t, 0.0) for t in txo]          # v2.4: subsidies negative
        txfx = [pcc * (t_ if y <= last_hist else txo_l) for y, t_ in zip(years, txo)]   # v4.16: fixed, floating part
        res[('txfx', sec, fuel)], res[('txfl', sec, fuel)] = txfx, [a - b for a, b in zip(txo, txfx)]
        res[('pcsw', sec, fuel)] = [-(1 - csf[pc][y]) * min(x_, 0.0) for y, x_ in zip(years, txfx)]
        res[('ppcw', sec, fuel)] = [-(1 - pcf[pc][y]) * x_ for y, x_ in zip(years, res[('txfl', sec, fuel)])]
        res[('esubpu', sec, fuel)] = [min(t, 0.0) * gj for t in txo]
    shock_f = [float(r[str(y)]) for r in read('power_paths.csv') if r['country'] == ISO and r['key'] == 'shock'
               for y in years]                       # v3.11: fuel-use shock (legacy row 2439), Settings C19
    incf = [float(r[str(y)]) for r in read('power_paths.csv') if r['country'] == ISO and r['key'] == 'incf'
            for y in years]                          # v4.12: income factor on eps_Y (legacy row 2433; I23)
    incp = list(incf)                                # v5.4: IncElAdj of the scenario (power data: Yes*)
    if str(mt[n['IncElAdj']])[:3] != 'Yes':
        incf = [1.0] * len(years)
    exi_ = {}                                         # v4.15 (LD37): existing taxes and subsidies by pair (12e)
    # v5.1 (D9): residential leakage to biomass (section 6b), global settings of scenario 1 (as BiomassNormal);
    # the most-used cooking fuel from WHOCooking, sigma from the legacy Elasticities cell C131, lag from Constants
    mt1 = scenario_mt(1)
    leak = str(mt1[n['BiomassLeakage']]).startswith('Yes')
    cook = next((r['main_fuel'] for r in read('legacy_WHOCooking.csv') if r['code'] == f'{ISO}.distn.pcoff.ove'), '')
    e_ck = {f_: float(mt1[n[nm]]) for f_, nm in (('nga', 'NatGasEff'), ('lpg', 'LPGEff'), ('ker', 'KerEff'),
                                                 ('bio', 'BioEff'))}
    sigma = float(next(r['value'] for r in read('legacy_Elasticities_cells.csv') if r['row'] == '131' and r['col'] == '3'))
    lk_on = {f_: 1.0 if leak and f_ == cook else 0.0 for f_ in B.LK_FUELS}
    lk_coef = {f_: sigma * e_ck['bio'] / e_ck[f_] / K['ResSubstLag'] for f_ in B.LK_FUELS}
    lkb = [0.0] * len(years)                          # biomass replacing the fuels, by year (sum over the fuels)
    exempt = str(mt[n['AlwaysExemptResLPGKer']]).strip().upper().startswith('YES')   # v5.1 (D16, I50): per scenario
    for s, f in B.PAIRS:
        _, _, grp, es, efs, cgs, fbs = sub[s]
        _, _, elf, aef, rule, _ = fue[f]
        pf = B.PRICE_FUEL_OF.get(f, f)                 # v3.11: jet fuel takes the kerosene price build-up
        code = f'{pf}.{cgs if rule == "sub" else "all"}'
        e = ef[f'{ISO}|{f}|{efs}']
        fcov = 1 if f == 'bio' else bool(mt[n['MCov' + pf.capitalize()]])
        swc = mt[n['MCov' + s.capitalize()]]
        xj = cgs if rule == 'sub' else ('ind' if f == 'oop' else 'trs')   # v4.12: ECP sector of the price fuel
        fbcov = bool(mt[66 + B.COV_SECTORS.index(s)])
        eY, eU, eF = el[f'inc|{elf}|{es}'], el[f'usg|{elf}|{es}'], el[f'eff|{elf}|{es}']
        if (s, f) == ('res', 'bio') and not str(scenario_mt(1)[n['BiomassNormal']]).startswith('Yes'):
            eY = 0.0                                  # v4.13 (I24): legacy row 5567, BiomassNormal (scenario 1)
        a = el[f'aei|{aef}|{es}'] + float(mt[n[B.ADDEFF_PARAMS[B.AEG.get(s, 3) - 1]]] or 0)   # v4.13 (LD21)
        v = {k: [] for k in B.VARS}
        exf = 0.0 if exempt and s == 'res' and f in ('lpg', 'ker') else 1.0   # v5.1: exemption factor
        lk = {k_: [] for k_ in ('lkt', 'lkp', 'lkd', 'lkb', 'lkc')}            # v5.1: section 6b rows of the pair
        for k, y in enumerate(years):
            v['ctxnew'].append(cpx[y] * e * fcov * sc_used(s, swc, y) * (1 - ets_cov[s][y]) * exf)   # v4.16: explicit
            v['ets'].append(ets_pe[y] * e * ets_cov[s][y] * (1 - obr[s][y]) * exf)
            v['ntx'].append(fpr[code][y] / units[f] * exf)
            v['nce'].append(v['ctxnew'][-1] + v['ets'][-1] + v['ntx'][-1])
            v['xcp'].append(e * xlev(xj, f, y))
            v['xcpd'].append(e * (xlev(xj, f, y) - xemb(xj, f)))
            v['csw'].append(res[('pcsw', code.split('.')[1], pf)][k])            # v4.16 (LD18): phase-out wedges
            v['pcw'].append(res[('ppcw', code.split('.')[1], pf)][k])
            v['atp'].append(max(rpb[code][k] + (v['nce'][-1] + v['xcpd'][-1] + v['csw'][-1] + v['pcw'][-1])
                                * (1 + vrate[code]), K['PriceFloor']))
            v['shp'].append((fb[fbs][y] * fbcov * fbadj + reg[s][y] + ets_pe[y] * ets_cov[s][y] * obr[s][y]) * e)
            v['aef'].append((1 / (1 + a)) ** (1 + eU))   # v5.1: the efficiency factor row (v4.13), compared too
            if y == B.BASE_YEAR:
                v['enel'].append(use0[(s, f)])
            else:
                ratio = v['atp'][-1] / v['atp'][-2]
                eff = (v['atp'][-1] + v['shp'][-1]) / (v['atp'][-2] + v['shp'][-2])
                v['enel'].append(v['enel'][-1] * (1 / (1 + a)) ** (1 + eU) * (1 + gdpg[k]) ** (eY * incf[k])
                                 * ratio ** eU * eff ** (eF * (1 + eU)) * (1 + shock_f[k] * shock_on))   # v3.11
            # v3.5: road fuels from the engineer road model where TrModel = Engineer (section 5b)
            q = road[f][k] if road and s == 'rod' and f in road else v['enel'][-1]
            if s == 'res' and f in B.LK_FUELS:          # v5.1 (D9): leakage of the most-used cooking fuel to biomass
                lk['lkt'].append(v['nce'][-1] * (1 + vrate[code]))
                p_ = 0.0 if k == 0 else lk_on[f] * min((1 + (lk['lkt'][-1] - lk['lkt'][-2]) / v['atp'][-2])
                                                       ** lk_coef[f] - 1, 1)
                d_ = 0.0 if k == 0 else -v['ener'][-1] * e_ck[f] * p_      # on last year's actual use
                lk['lkp'].append(p_)
                lk['lkd'].append(d_)
                lk['lkb'].append(-d_ * e_ck[f] / e_ck['bio'])            # same useful energy (L90 fixed)
                lk['lkc'].append((lk['lkc'][-1] if k else 0.0) + d_)
                lkb[k] += lk['lkb'][-1]
                q += lk['lkc'][-1]
            elif (s, f) == ('res', 'bio'):
                q += sum(lkb[:k + 1])
            v['ener'].append(q)
        kpj = B.PJ_PER_KTOE                              # PJ per ktoe (Settings C13)
        k_code = [pc for pc, _l in B.PRICES].index(code)
        v['co2'] = [u * kpj * e for u in v['ener']]
        _f = 'jfu' if (s, f) == ('avi', 'ker') else f
        ef0, ef1 = NC_EF.get(nc_sub(s, _f), (0.0, 0.0))           # v4.12: bug L59 fallback
        v['ch4'] = [u * ch4_ef(ef0, ef1, y) / 1000 for u, y in zip(v['ener'], years)]   # v2.8: kt CH4
        for k, y in enumerate(years):
            ext = res[('etx', code.split('.')[1], pf)][k] + res[('vat', code.split('.')[1], pf)][k]
            v['rtx'].append(v['ener'][k] * kpj * (ext + v['xcpd'][k] * (1 + vrate[code])))
            v['rxcp'].append(v['ener'][k] * kpj * v['xcp'][k])
            vat_ = res[('vat', code.split('.')[1], pf)][k]
            v['rex'].append(v['ener'][k] * kpj * v['ntx'][k])                       # v4.15 (LD37)
            v['rvt'].append(v['ener'][k] * kpj * (vat_ + (v['xcpd'][k] + v['nce'][k] + v['csw'][k] + v['pcw'][k])
                                                  * vrate[code]))
            v['rsr'].append(v['ener'][k] * kpj * (v['csw'][k] + v['pcw'][k]) * (1 + vrate[code]))   # v4.16
            v['rsub'].append(v['ener'][k] * kpj * res[('esub', code.split('.')[1], pf)][k])
            exi_.setdefault((s, f), []).append(v['ener'][k] * kpj * (res[('etx', code.split('.')[1], pf)][k]
                                                                     + v['xcpd'][k]) + v['rsub'][k])
            v['rnew'].append(v['ener'][k] * kpj * (v['ctxnew'][k] + v['ntx'][k] + v['ets'][k] / vadj
                                                    + v['nce'][k] * vrate[code]))
        for k in B.VARS:
            res[(k, s, f)] = v[k]
        if s == 'res' and f in B.LK_FUELS:
            for k_, x_ in lk.items():
                res[(k_, 'res', f)] = x_
    res[('lkz', 'res', 'none')] = [0.0] * len(years)
    res[('lkcb', 'res', 'bio')] = [sum(lkb[:k + 1]) for k in range(len(years))]
    res[('lks', 'res', 'all')] = [sum(res[('lkc', 'res', f_)][k] for f_ in B.LK_FUELS) + res[('lkcb', 'res', 'bio')][k]
                                  for k in range(len(years))]
    for var in B.REV_VARS + ['co2']:
        res[(var, 'all', 'all')] = [sum(res[(var, s, f)][k] for s, f in B.PAIRS) for k in range(len(years))]
    res[('co2.ets', 'all', 'all')] = [sum(res[('co2', s, f)][k] * ets_cov[s][y] for s, f in B.PAIRS)
                                      for k, y in enumerate(years)]
    res[('rtot', 'all', 'all')] = [a + b + c for a, b, c in zip(res[('rtx', 'all', 'all')],
                                                                 res[('rsub', 'all', 'all')],
                                                                 res[('rnew', 'all', 'all')])]
    # 3. Power (engineer model, power_model_ref_v7_0 with all bug fixes): MVP prices and policies as inputs
    pdata = power_data(years, mt)                   # v5.2: the MVP data step (L52-L55 fixed, tcf from the Power tab);
    tech = pdata[0]                                 # v5.4: with the settings of the scenario
    paths_p = {**{r['key']: [float(r[str(y)]) for y in years] for r in read('power_paths.csv') if r['country'] == ISO},
               **pdata[1]}
    paths_p['incp'], paths_p['incf'] = incp, incf
    pset, pext = power_settings(mt, years, cp, dfl, cpi)
    spot = spot or str(mt[n['UseSpotFuelPricesInEngineerModel']])[:3] == 'Yes'   # v5.4: or the scenario's switch
    spow = lambda y: sc_used('pow', mt[n['MCovPow']], y)
    xck, fpps, fpns = [], [], []
    # v6.0 (v5.6 P5): coal implicit cost, $/kWh (COALICPICK, COALIC; GoalSeekCoal by country or Manual)
    icset = str(mt[n['AdditionalCoalIntangibleCost']])
    gsc = {r['Region']: r for r in read('legacy_GoalSeekCoal.csv')}

    def ic_pick(st):
        if icset[:1] == 'N':
            return 0.0
        if icset == 'Manual':
            return float(mt[n['ManualCoalIntangibleCost' + ('ST' if st else 'LT')]] or 0)
        r_ = gsc.get(ISO)
        return float(r_['First Year of Calculations' if st else 'Year 2030']) if r_ else 0.0
    cics, cicl = ic_pick(True), ic_pick(False)
    cyr = next(v for nm, v, *_x in B.NAMED_CONSTANTS if nm == 'CoalICYr')
    cic = [cics + (cicl - cics) * min(1, (y - B.BASE_YEAR) / (cyr - B.BASE_YEAR)) for y in years]
    efs = []
    fbcov_pow = bool(mt[66])
    vbc, d5, shp = [], [], []
    for f in POWER_TECH:
        t = tech[f]
        pc, eff = t['price_code'], float(t['efficiency'])
        k_ = K['GJperkWh'] / eff if pc else 0.0
        e = ef.get(f'{ISO}|{f}|pow', 0.0) if pc else 0.0
        fu = pc.split('.')[0] if pc else ''
        fcov = 1 if fu == 'bio' else (bool(mt[n['MCov' + fu.capitalize()]]) if pc else 0)
        fixed = float(t['vop_usd_per_kwh']) + float(t['fuel_fixed_usd_per_kwh'])
        isfuel = f in [x[0] for x in B.FUELS]
        xck.append([e * k_ * (xlev('pow', f, y) - xemb('pow', f)) if isfuel else 0.0 for y in years])
        n_ = len(years)                  # v2.3: fuel price for power = moving average (A18); v6.2 (L126): t-4 .. t
        w_ = lambda x, k: x[max(0, k - 4):k + 1]
        fpp = [(rpb[pc][k] if spot else sum(w_(rpb[pc], k)) / len(w_(rpb[pc], k)))
               if pc else rpb['coa.pow'][k] if spot else
               sum(w_(rpb['coa.pow'], k)) / len(w_(rpb['coa.pow'], k)) for k in range(n_)]
        fpps.append(fpp)
        fpns.append(list(rpb[pc] if pc else rpb['coa.pow']))   # v6.2: fpn, this year's rpb (fpp averages it)
        efs.append(e)
        vbc.append([fixed + (fpp[k] * k_ if pc else 0.0) + xck[-1][k] + (cic[k] if f == 'coa' else 0.0)
                    for k in range(n_)])
        d5.append([e * k_ * (cpx[y] * fcov * spow(y) * (1 - ets_cov['pow'][y]) + ets_pe[y] * ets_cov['pow'][y]
                             * (1 - obr['pow'][y])) + (fpr[pc][y] / units[fu] * k_ if pc else 0.0) for y in years])
        shp.append([(fb['pow'][y] * fbcov_pow * fbadj + reg['pow'][y] + ets_pe[y] * ets_cov['pow'][y] * obr['pow'][y]) * e
                    for y in years])
    hist = {g: [val(f'mit.rp.ecy.{g}', y) * cpi[y] if y <= last_hist else 0.0 for y in years] for g in ('res', 'ind')}
    pinp = {'iso': ISO, 'elast': PM.elasticities(INCOME[ISO]), 'gdp': list(gdpg), 'inc': paths_p['incf'],
            'shock': paths_p['shock'], 'cpf': [0.0] * len(years),
            'rp2021_res': val('mit.rp.ecy.res', 2021) * cpi[2021], 'rp2021_ind': val('mit.rp.ecy.ind', 2021) * cpi[2021],
            'rphist_res': hist['res'], 'rphist_ind': hist['ind'], 'vat_res': val('mit.vatrate.ecy.res', last_hist),
            'vat_ind': val('mit.vatrate.ecy.ind', last_hist), 'last_hist': last_hist, 'vbc': vbc, 'd5': d5,
            'shp_gj': shp, 'co2k': kc, 'data': pdata, **pset, **(power or {})}
    if road:                                          # v3.5: road electricity from the engineer road model
        pinp['dem_fixed'] = {'rod': road['ele']}
    res[('TRIN', '', '')] = {'vrate': dict(vrate), 'units': units, 'el': el, 'use0': use0, 'ef': ef, 'gdpg': gdpg,
                             'rp2021_res': pinp['rp2021_res'], 'cp': [reg['rod'][y] for y in years],   # v4.16
                             'fbcov_rod': 1.0,
                             'vat_weo': {y: val('VAT_WEO', y) for y in range(2019, 2026) if f'{ISO}{y}' in dom},
                             'gwh': PM.base_data(years, ISO)[2]['ktoe_gwh'],
                             'd0_rod': next(float(r['ktoe_2022']) for r in read('power_demand.csv')
                                            if r['country'] == ISO and r['subsector'] == 'rod')}
    o = PM.engine(pinp, years, fix=PM.ALL_FIXES, shock=bool(shock_on))
    ny_ = len(years)                                  # v5.4: the singles of A0 and G recomputed here
    g_ = lambda nm: mt[n[nm]]
    cat = str(g_('MaxScaleUpRateCategory'))
    o['scat'] = [K_SCALE.get(cat, 0.0)] * ny_
    o['scv'] = [float(tech['wnd']['scaleup_rate'])] * ny_
    o['spot'] = [1.0 if spot else 0.0] * ny_
    o['stm'] = [pset['par']['st_alloc'] * pset['par']['st_marg_hours']] * ny_
    o['ltu'] = [pset['par']['lt_alloc'] * pset['par']['lt100']] * ny_
    o['rnsp'], o['rbs'], o['exs'] = pext['rnsp'], [pset['reb']] * ny_, pset['exs']
    # v6.0 (v5.6 P3, P5): manual capacity and investment, need net of it, coal implicit cost, memo rows
    o['cics'], o['cicl'], o['cic'] = [cics] * ny_, [cicl] * ny_, cic
    mi = {}
    for r_ in read('legacy_ManualInputs_cells.csv'):
        mi[(int(r_['row']), int(r_['col']))] = r_['value']
    yr_col = {int(float(v)): c_ for (r_, c_), v in mi.items() if r_ == 348 and c_ >= 10 and str(v).replace('.', '').isdigit()}
    off = 0 if mt.get('scen', 2) == 1 else 14
    sc = lambda v: v[0] if isinstance(v, list) else v
    o['mancap'], o['mani'] = [], []
    for i, f in enumerate(POWER_TECH):
        row_ = next((r_ for (r_, c_), v in mi.items() if 349 <= r_ <= 357 and c_ == 4 and v == f), None)
        mc = []
        for y in years:
            v = mi.get((row_ + off, yr_col.get(y, 0))) if row_ else None
            try:
                mc.append(float(v))
            except (TypeError, ValueError):
                mc.append(0.0)
        o['mancap'].append(mc)
        manual = str(sc(o['invs'][i]) if 'invs' in o else '') == 'Manual'
        cf_ = o['cfu'][i]
        o['mani'].append([max(0.0, mc[k + 1] - mc[k] + o['ret'][i][k]) * (cf_[k] if isinstance(cf_, list) else cf_)
                          if manual and k + 1 < ny_ else 0.0 for k in range(ny_)])
    o['needm'] = [max(o['need'][k] - sum(o['mani'][i][k] for i in range(len(POWER_TECH))), 0.0) for k in range(ny_)]
    kw = lambda i: o['kwh'][i] if not isinstance(o['kwh'][i], list) else None
    o['fce'] = [[fpps[i][k] * (kw(i) if kw(i) is not None else o['kwh'][i][k]) for k in range(ny_)]
                for i in range(len(POWER_TECH))]
    o['cik'] = [[efs[i] * (kw(i) if kw(i) is not None else o['kwh'][i][k]) for k in range(ny_)]
                for i in range(len(POWER_TECH))]
    ic_, ig_ = POWER_TECH.index('coa'), POWER_TECH.index('nga')

    def swp(v):
        out = []
        for k in range(ny_):
            d = o['cik'][ic_][k] - o['cik'][ig_][k]
            out.append((o[v][ig_][k] - o[v][ic_][k]) / d if d else 0.0)
        return out
    o['swi'], o['swd'] = swp('tic'), swp('tvc')
    o['entxd_res'], o['entxd_ind'] = pext['ntxd']['res'], pext['ntxd']['ind']
    o['entx_res'], o['entx_ind'] = o['ntx_res'], o['ntx_ind']
    o['rexs'] = [pset['exs'][k] * (o['cons_res'][k] + o['cons_ind'][k]) for k in range(ny_)]
    o['rexm'] = [o['rpex_res'][k] + o['rpex_ind'][k] - o['rexs'][k] for k in range(ny_)]
    o['cel'] = paths_p['cel']
    o['incf'] = paths_p['incf']
    text_rows = {'wsel', 'wfx', 'invs', 'perm', 'ctf'}   # options and Yes / No (checked through their numbers)
    for v in B.PW_VARS:
        if v in ('xck', 'prtx', 'prsub', 'prxc', 'prnew', 'prxl', 'rnvat', 'fpp', 'fpn', 'tvcx') or v in text_rows:
            continue                                  # set below / text
        kind = B.PW_KIND[v]
        for m in B.PW_MEMBERS.get(kind, ['']):
            if kind == 'tech':
                i = POWER_TECH.index(m)
                val_ = {'vbc': vbc[i], 'ccp': d5[i]}.get(v) or (pdata[1][f'tcf|{m}'] if v == 'tcf' else o[v][i])
                res[(v, 'pow', m)] = val_
            elif kind == 'user':
                res[(v, m, 'ecy')] = o[f'{v}_{m}']
            elif kind == 'dgroup':
                res[(v, m, 'ecy')] = o[v][m]
            elif kind == 'dsub':
                res[(v, m, 'ecy')] = o['dem'][m]
            else:
                res[(v, '', '')] = paths_p[v] if v in B.PW_DATA else o[v]
    # v1.09: power revenues by type (M), VAT on the passed-through policy cost (G), totals with power
    par = PM.base_data(years, ISO)[2]
    ny = len(years)
    fflag = [1.0 if f in [x[0] for x in B.FUELS] else 0.0 for f in POWER_TECH]
    etr_pow = [ets_pe[y] * ets_cov['pow'][y] * (1 - obr['pow'][y]) for y in years]
    rf = 1 / vadj if vadj > 0 else 0.0
    pw = {v: [[0.0] * ny for _ in POWER_TECH] for v in ('prtx', 'prsub', 'prxc', 'prnew', 'prxl', 'xck')}
    for i, f in enumerate(POWER_TECH):
        pc = tech[f]['price_code']
        sec_, fu_ = (pc.split('.')[1], pc.split('.')[0]) if pc else ('pow', 'coa')   # no fuel: position 1 (x flag 0)
        isfuel = fflag[i] == 1.0
        for k, y in enumerate(years):
            q = fflag[i] * o['pe'][i][k] * B.PJ_PER_KTOE
            pw['prtx'][i][k] = q * (res[('etx', sec_, fu_)][k] + res[('vat', sec_, fu_)][k])
            pw['prsub'][i][k] = q * res[('esub', sec_, fu_)][k]
            pw['xck'][i][k] = xck[i][k]
            pw['prxc'][i][k] = xck[i][k] * K['MWyMkWh'] * o['gen'][i][k]
            pw['prnew'][i][k] = o['gen'][i][k] * K['MWyMkWh'] * d5[i][k] - o['co2'][i][k] * etr_pow[k] * (1 - rf)
            pw['prxl'][i][k] = o['co2'][i][k] * (xlev('pow', f, y) if isfuel else 0.0)
    vat_g = {'res': pinp['vat_res'], 'ind': pinp['vat_ind']}
    rnvat = {g: o[f'rnvat_{g}'] for g in ('res', 'ind')}     # v5.4: less the rebate, plus the excise (engine)
    for v in pw:
        for i, m in enumerate(POWER_TECH):
            res[(v, 'pow', m)] = pw[v][i]
    for i, m in enumerate(POWER_TECH):                 # v2.3
        res[('fpp', 'pow', m)] = fpps[i]
        res[('fpn', 'pow', m)] = fpns[i]
        res[('tvcx', 'pow', m)] = o['tvc'][i]
    for g in ('res', 'ind'):
        res[('rnvat', g, 'ecy')] = rnvat[g]
    tsum = lambda v: [sum(pw[v][i][k] for i in range(9)) for k in range(ny)]
    gsum = lambda v: [o[f'{v}_res'][k] + o[f'{v}_ind'][k] for k in range(ny)]
    for i, m in enumerate(POWER_TECH):                # v5.4: renewable subsidies by type (engine)
        pw.setdefault('prrns', [None] * 9)[i] = o['prrns'][i]
    rpow = {'rtx': [a_ + b_ + c_ for a_, b_, c_ in zip(tsum('prtx'), tsum('prxc'), gsum('rvat'))],
            'rsub': [a_ + b_ + c_ for a_, b_, c_ in zip(tsum('prsub'), gsum('rgap'), tsum('prrns'))],
            'rnew': [a_ + b_ + c_ + d_ for a_, b_, c_, d_ in zip(tsum('prnew'), rnvat['res'], gsum('rreb'),
                                                                  gsum('rpex'))],
            'rxcp': tsum('prxl'), 'rsr': [0.0] * ny}        # v4.16: no electricity phase-out
    rpow['rnew'] = [a_ + b_ for a_, b_ in zip(rpow['rnew'], rnvat['ind'])]
    for v in B.REV_VARS:
        res[(v, 'pow', 'all')] = rpow[v]
        res[(v, 'all', 'all')] = [a_ + b_ for a_, b_ in zip(res[(v, 'all', 'all')], rpow[v])]
    res[('rpsu', 'all', 'all')] = [-sum(pros[f][k] * psf[f][y] for f, _l in B.PROS_FUELS)
                                   for k, y in enumerate(years)]                         # v4.16 (LD19)
    res[('rtot', 'all', 'all')] = [a + b + c + d + e_ for a, b, c, d, e_ in zip(
        res[('rtx', 'all', 'all')], res[('rsub', 'all', 'all')], res[('rnew', 'all', 'all')],
        res[('rsr', 'all', 'all')], res[('rpsu', 'all', 'all')])]
    epow = [sum(fflag[i] * o['pe'][i][k] for i in range(9)) for k in range(ny)]
    res[('ener', 'pow', 'all')] = epow
    res[('ener', 'all', 'all')] = [sum(res[('ener', s, f)][k] for s, f in B.PAIRS) + epow[k] for k in range(ny)]
    pco2 = [sum(o['co2'][i][k] for i in range(9)) for k in range(len(years))]
    res[('co2', 'all', 'all')] = [a_ + b_ for a_, b_ in zip(res[('co2', 'all', 'all')], pco2)]
    res[('co2.ets', 'all', 'all')] = [a_ + b_ * ets_cov['pow'][y] for a_, b_, y in
                                      zip(res[('co2.ets', 'all', 'all')], pco2, years)]
    res[('co2.pow', '', '')] = pco2
    ref_fn = lambda: _recompute_once(scenario_mt(1), controls=controls, base=base, shock_on=shock_on, power=power,
                                     ecp=ecp, spot=spot)     # scenario 1 (baseline calibration, effort reference)
    res[('gdp.pos.pct', '', '')] = list(gdpg)
    ghg_section(res, mt, years, {t: o['pe'][i] for i, t in enumerate(POWER_TECH)}, ref_fn)   # v2.8: section 14
    ap_section(res, years, {t: o['pe'][i] for i, t in enumerate(POWER_TECH)})                 # v2.9: section 15
    # v4.15 (LD37): 12e, total revenue by policy (legacy rows 8016-8027), each policy explicitly
    kpj = B.PJ_PER_KTOE
    psum = lambda var, fac=1.0: [sum(res[('ener', s, f)][k] * kpj * res[(var, s, f)][k] * fac for s, f in B.PAIRS)
                                 for k in range(ny)]
    vsum = lambda var: [sum(res[(var, s, f)][k] for s, f in B.PAIRS) for k in range(ny)]
    fct = [float(bool(mt[n['MCov' + t.capitalize()]])) if t in ('coa', 'nga', 'oop') else 0.0 for t in POWER_TECH]
    ctr_pow = [cpx[y] * spow(y) * (1 - ets_cov['pow'][y]) for y in years]
    ctp = [sum(o['co2'][i][k] * fct[i] for i in range(9)) * ctr_pow[k] for k in range(ny)]
    etp = [pco2[k] * etr_pow[k] * rf for k in range(ny)]
    rp = {'ct': [a + b + c + d for a, b, c, d in zip(psum('ctxnew'), ctp, gsum('rreb'), o['rexs'])],   # v5.4
          'ets': [a + b for a, b in zip(psum('ets', rf), etp)],
          'exc': [a + b - c - d + e_ for a, b, c, d, e_ in zip(vsum('rex'), tsum('prnew'), ctp, etp, o['rexm'])],
          'vat': [a + b + c + d for a, b, c, d in zip(vsum('rvt'), gsum('rvat'), rnvat['res'], rnvat['ind'])],
          'psu': [a + b for a, b in zip(gsum('rgap'), res[('rpsu', 'all', 'all')])],      # v4.16: + producer
          'exi': [sum(exi_[p][k] for p in B.PAIRS) + a + b + c + d for k, (a, b, c, d) in
                  enumerate(zip(tsum('prtx'), tsum('prxc'), tsum('prsub'), res[('rsr', 'all', 'all')]))],
          'ren': tsum('prrns'), 'trs': [0.0] * ny,      # v5.4: renewable subsidies
          'mf': res[('rmf', 'all', 'all')], 'ctp': ctp, 'etp': etp}
    rp['tot'] = [sum(rp[q][k] for q in B.RPOL_SUM) for k in range(ny)]
    rp['chk'] = [abs(a - b) for a, b in zip(rp['tot'], res[('rtot', 'all', 'all')])]
    for q, v_ in rp.items():
        res[(f'rpol.{q}', '', '')] = v_
    return res


# v3.1: section 16 (GDP effects), an independent copy from the CSVs (GDP_Method_v7_0.md)
MULT = {(r['group'], r['stat'], r['instrument']): [float(r[f'lag{k}']) for k in range(20)] for r in read('multipliers.csv')}
GDP_USD = {int(k): float(v) for k, v in read('gdp_level.csv')[0].items() if k.isdigit()}
INCOME = {r['code']: r['income_group'] for r in read('countries.csv')}
NAME = {r['code']: r['name'] for r in read('countries.csv')}[ISO]   # v3.3
REGION = {r['iso']: r['gains_region'] for r in read('gains_region.csv')}[ISO]
USES = [('exc', None), ('pit', 'EXPLabortax'), ('cit', 'EXPCIT'), ('capt', 'EXPCapex'), ('gnfs', 'EXPGoodsandserv'),
        ('trns', 'EXPTransfers')]


def total_rev(res):
    """v4.15 (LD55): total revenue without the methane fee (rtot - rmf; v4.16: + subsidy reform, producer subsidies)."""
    return [a + b + c + d + e for a, b, c, d, e in zip(res[('rtx', 'all', 'all')], res[('rsub', 'all', 'all')],
                                                       res[('rnew', 'all', 'all')], res[('rsr', 'all', 'all')],
                                                       res[('rpsu', 'all', 'all')])]   # v4.16: + reform, producer


def _mult_est():
    """v4.15 (LD56): the country's estimated multipliers, lags 0-19 (lags past 11 hold lag 11), from the legacy
    Multipliers tab (independent copy): table by its label in column B, the country in column C (exact match)."""
    cells = {(int(r['row']), int(r['col'])): r['value'] for r in read('legacy_Multipliers_cells.csv')}
    lab = {'exc': 'Excise tax', 'pit': 'Labor tax', 'capt': 'Public investment', 'gnfs': 'Public consumption',
           'trns': 'Transfers', 'vat': 'VAT'}                     # CIT (no table) and WAGE: income group (bug L76)
    out = {}
    for i, t in lab.items():
        h = min(r for (r, c), v in cells.items() if c == 2 and v == t and r > 200)
        r = h + 2
        while cells.get((r, 3), '') not in ('', ISO) and len(cells.get((r, 3), '')) == 3:
            r += 1
        if cells.get((r, 3)) == ISO:
            v = [float(cells.get((r, 4 + k), 0) or 0) for k in range(12)]
            out[i] = v + [v[-1]] * 8
    return out


MULT_EST = _mult_est()
MULT_MAN = {i: [0.0] * 20 for i in ('exc', 'pit', 'cit', 'vat', 'capt', 'gnfs', 'trns', 'wage')}   # Manual inputs blank


def gdp_section(res, mt, ref_rev):
    """Fiscal space = new-policy revenue above scenario 1 / GDP; impulses = its yearly change; GDP effect = sum
    over uses and lags of share x impulse x multiplier (median, -/+ sd for low/high); level factor = 1 + last
    year's effect; growth = (1 + baseline growth) x factor / factor(t-1) - 1. Returns the new growth path."""
    years = [B.BASE_YEAR] + B.YEARS
    ny = len(years)
    m_ = lambda k: mt[B.MT_NAMES[k]]
    weo = read('weo.csv')[0]
    gb = [float(weo[str(y)]) for y in years]
    usd = [GDP_USD[y] for y in years]
    rev = total_rev(res)                                   # v4.15 (LD55): total revenue (legacy rev.new.usd)
    if ('rmf', 'all', 'all') in res:                       # v6.2 (I47): + methane fee (the workbook's ch4.revf uses the
                                                           # stored scenario-1 gas and biomass activity: 0 when no fee)
        rev = [a + b for a, b in zip(rev, res[('rmf', 'all', 'all')])]
    sp = [(rev[k] - ref_rev[k]) / (usd[k] * 1000) for k in range(ny)]
    st = int(m_('GDPStartYear'))                           # v4.15 (LD55): legacy row 14356, from GDPStartYear
    imp = [0.0 if years[k] < st else sp[k] - (sp[k - 1] * usd[k - 1] / usd[k] if k else 0.0) for k in range(ny)]
    cpi0 = float(m_('CPIntro'))
    impp = [0.0 if years[k] < cpi0 else imp[k] for k in range(ny)]   # v6.0 (I43): legacy rows 96-100
    src = str(m_('MultipliersSource'))
    inc = INCOME[ISO].lower()
    grp = 'global' if src.startswith('Glo') else src[:3].lower() if src[:3] in ('Est', 'Man') else inc
    rng = str(m_('FmAdj')).replace('*', '').lower()
    sg = {'base': 0, 'low': -1, 'high': 1}[rng]
    eff = {}
    for i, mt_name in USES:
        med = MULT_EST.get(i, MULT[(inc, 'median', i)]) if grp == 'est' else MULT_MAN[i] if grp == 'man' \
            else MULT[(grp, 'median', i)]
        mult = [a + sg * b for a, b in zip(med, MULT[(inc if grp in ('est', 'man') else grp, 'sd', i)])]
        share = -1.0 if mt_name is None else float(m_(mt_name)) / K['PctPerUnit']
        im_ = imp if mt_name is None else impp            # v6.0 (I43): the uses count impulses from CPIntro
        eff[i] = [share * sum(im_[t - k] * mult[k] for k in range(min(t, 19) + 1)) for t in range(ny)]
    on = str(m_('GDPEndogenous'))[:3] == 'Yes'
    tot = [sum(eff[i][t] for i, _m in USES) * (1 if on else 0) for t in range(ny)]
    lvl = [1.0] + [1 + tot[t - 1] for t in range(1, ny)]
    g = [gb[0]] + [(1 + gb[t]) * lvl[t] / lvl[t - 1] - 1 for t in range(1, ny)]
    lags = {f'fis.lag.{k}': [0.0] * k + imp[:ny - k] for k in range(1, 20)}
    lags.update({f'fis.lagp.{k}': [0.0] * k + impp[:ny - k] for k in range(1, 20)})
    # v6.0 (8A): memo rows: growth effect by use, by year of the reform, change in GDP level
    gg = lambda e: [0.0] + [(1 + gb[t]) * (e[t - 1] - (e[t - 2] if t > 1 else 0.0)) / lvl[t - 1] for t in range(1, ny)]
    memo = {f'gdpg.{i}': [x * (1 if on else 0) for x in gg(eff[i])] for i, _m in USES}
    memo['gdpg.all'] = gg(tot)
    memo['gdpy'] = [float(y - int(m_('GDPStartYear')) + 1) for y in years]   # v6.0: year of the reform
    memo['gdp.chg.usd'] = [a * b - a for a, b in zip(usd, lvl)]
    memo['fis.impp'] = impp
    out = {'gdp.base': gb, 'gdp.usd': usd, 'fis.rev': rev, 'fis.ref': list(ref_rev), 'fis.sp': sp, 'fis.imp': imp,
           **lags, **{f'fis.eff.{i}': eff[i] for i, _m in USES}, 'gdp.eff': tot, 'gdp.lvl': lvl,
           'gdp.pos.usd': [a * b for a, b in zip(usd, lvl)], **memo}
    for k_, v_ in out.items():
        res[(f'S16:{k_}', '', '')] = v_
    return g


def recompute(mt, controls=None, **kw):
    """v3.5: the recomputation with the GDP feedback (_recompute_gdp) and the engineer road model
    (transport_model_ref_v7_0.engine with all bug fixes, inputs from the recomputation). Where TrModel = Engineer the
    road fuels and road electricity come from the engine: the engine's inputs depend on the rest of the model only
    through earlier years (power price, GDP feedback) or not at all (fuel prices), so iterating converges."""
    res = _recompute_gdp(mt, controls, **kw)
    o, inp = tr_run(res, mt)
    if str(mt[B.MT_NAMES['TrModel']]).startswith('Engineer'):
        for _it in range(len(B.YEARS) + 3):
            road = tr_road(o, inp)
            res = _recompute_gdp(mt, controls, road=road, **kw)
            o, inp = tr_run(res, mt)
            new = tr_road(o, inp)
            if max(abs(a - b) / max(1.0, abs(b)) for f in road for a, b in zip(road[f], new[f])) < 1e-14:
                break
    res[('TR', '', '')] = (o, inp)
    res[('TRMT', '', '')] = mt
    return res


def tr_inputs(res, mt):
    """v3.5: inputs of the engineer road model from the recomputation: an independent copy of the input mapping of
    section 5b (Transport_Workbook_Notes_v7_0.md): road after-tax prices of section 5 in $/liter (gas $/GJ),
    industrial gas price with the road new policies, power prices (section 3), GDP growth after the feedback,
    population, GDP per capita, carbon price and road feebate coverage, road elasticities, EFs and energy balance."""
    T = res[('TRIN', '', '')]
    years = [B.BASE_YEAR] + B.YEARS
    n = len(years)
    u, vr, el, ef = T['units'], T['vrate'], T['el'], T['ef']
    par = TM.params()
    for k, name, *_x in B.TR_MT:                       # policies: the scenario's MTInputs rows
        par[k] = mt[B.MT_NAMES[name]]
    data, prices, _ra = TM.country_data(ISO)
    ra = TM.range_anxiety(ISO, par)[0]
    atp = lambda f: res[('atp', 'rod', f)]
    rp = {f: [a * u[f] for a in atp(f)] for f in ('gso', 'die', 'lpg')}
    rp['nga_res'] = list(atp('nga'))
    rp['nga_ind'] = [max(a + (b + c) * (1 + vr['nga.ind']), K['PriceFloor'])
                     for a, b, c in zip(res[('rpb', 'ind', 'nga')], res[('nce', 'rod', 'nga')], res[('xcpd', 'rod', 'nga')])]
    amt = lambda xs, rate: [x_ * rate / (1 + rate) for x_ in xs]           # VAT amount in a price incl. VAT
    pop_th = res[('S14:pop', '', '')]
    g21 = next((r['2021'] for r in read('legacy_WEO.csv')      # v5.2: WEO growth of the year before the base year
                if r['SERIES_CODE'] == f'{ISO}.NGDP_RPCH.A'), '')    # (trgdl 2022, fix B2; CAVEATS v4.x)
    g21 = float(g21) / 100 if g21 not in ('', None) else ''
    efr = lambda f: ef[f'{ISO}|{f}|rod']
    lk = {f: B.PJ_PER_KTOE * 1e6 / u[f] for f in ('gso', 'die', 'lpg')}
    lk['nga'] = lk['gso']                                # as legacy: gas uses the gasoline factor
    u0 = T['use0']
    return {
        'iso': ISO, 'par': par, 'paths': {**TM.paths(years), **mi_bev(years)}, 'data': data, 'prices': prices, 'ra': ra,
        'scen': mt.get('scen', 1), 'rp': rp,
        'sp_gso': rp['gso'], 'txo_gso': [0.0] * n, 'vatr_gso': [0.0] * n,     # 2-3 wheelers: price incl. policies
        'vat_die': amt(rp['die'], vr['die.all']), 'vat_lpg': amt(rp['lpg'], vr['lpg.all']),
        'vat_nga_ind': amt(rp['nga_ind'], vr['nga.ind']),
        'pp_res': res[('rp', 'res', 'ecy')], 'pp_ind': res[('rp', 'ind', 'ecy')],
        'gdp_growth': list(res[('gdp.pos.pct', '', '')]), 'gdp_growth_2021': float(g21) if g21 not in ('', None) else 0.0,
        'row2455': [0.0] * n, 'cprice': T['cp'], 'fb_cov': [T['fbcov_rod']] * n,
        'pop': [p_ / 1000 for p_ in pop_th],
        'gdppc': [x_ * 1e9 / (p_ * 1000) for x_, p_ in zip(res[('S16:gdp.pos.usd', '', '')], pop_th)],
        'rp0': {'gso': [a * u['gso'] for a in res[('rpb', 'all', 'gso')]],
                'die': [a * u['die'] for a in res[('rpb', 'all', 'die')]], 'vatr_die': [vr['die.all']] * n,
                'ele_res': res[('rppre', 'res', 'ecy')], 'ele_ind': res[('rppre', 'ind', 'ecy')]},
        'rp0_ele_res_2021': T['rp2021_res'], 'vat_veh': T['vat_weo'][int(par['customs_year'])], 'wacc_avg': 0.0,
        'el_dem_gso': el['usg|gso|tra'], 'el_dem_die': el['usg|die|tra'], 'el_eff_gso': el['eff|gso|tra'],
        'el_eff_die': el['eff|die|tra'], 'aei_oil': el['aei|oil|tra'],
        'l_ktoe': lk, 'gwh_ktoe': T['gwh'],
        'ef': {'gso': efr('gso') * u['gso'], 'die': efr('die') * u['die'], 'lpg': efr('lpg') * u['lpg'],
               'nga_gj': efr('nga')},
        'ef_name': {'gso': efr('gso') * u['gso'], 'die': efr('die') * u['die'], 'lpg': efr('lpg') * u['lpg'],
                    'nga_gj': efr('nga')},
        'eb': {'gso': u0[('rod', 'gso')], 'die': u0[('rod', 'die')], 'lpg': u0[('rod', 'lpg')],
               'nga': u0[('rod', 'nga')], 'bgs': BIO_EB['bgs'], 'bdi': BIO_EB['bdi'], 'obf': BIO_EB['obf'],
               'ele': T['d0_rod']}}


def tr_run(res, mt):
    inp = tr_inputs(res, mt)
    return TM.engine(inp, [B.BASE_YEAR] + B.YEARS, fix=TM.ALL_FIXES), inp


def tr_road(o, inp):
    """Road fuel use (ktoe) of the engineer model: gasoline, diesel, LPG, gas, biofuels (v4.12, LD62 as legacy rows
    5436-5438: bioethanol and other biofuels x gasoline / base year, biodiesel x diesel / base year) and road
    electricity."""
    eb = inp['eb']
    sc = lambda b, x, x0: b if x0 == 0 else b * x / x0
    bio = [sc(eb['bgs'] + eb['obf'], a, eb['gso']) + sc(eb['bdi'], b, eb['die']) for a, b in zip(o[5325], o[5326])]
    return {'gso': o[5325], 'die': o[5326], 'lpg': o[5327], 'nga': o[5328], 'bio': bio, 'ele': o[5331]}


TR_PIV = {'pas': ('pass', 4407), 'fre': ('fre', 4435), 'cyc': ('cyc', 4448)}


def tr_expected(o, inp, mt):
    """v3.5: expected values of every section-5b row with year values, by row key: the engine row (legacy row
    number) or the helper rows of the workbook rebuilt from the engine (held base-year factors, data-year values
    held from the last data year, the two feebate pivot types, inputs)."""
    years = [B.BASE_YEAR] + B.YEARS
    n, nd = len(years), sum(1 for y in years if y in TM.DATA_YEARS)
    P, gpc = inp['par'], inp['gdppc']
    z = lambda v: 0.0 if v is None else v
    hold = lambda f: [f(k) for k in range(nd)] + [f(nd - 1)] * (n - nd)
    data = lambda f: [f(k) if k < nd else None for k in range(n)]
    gomp = lambda sat, inc, b: sat * math.exp(P['gomp_a'] * math.exp(inc * b / 1000))
    e = {}
    for k_, v_ in o.items():
        if isinstance(k_, int) and isinstance(v_, list):
            e[k_] = v_
    tm = mt[B.MT_NAMES['TrModel']]
    e['TrModel'] = [tm] * n
    for _k, name, *_x in B.TR_MT:
        e[name] = [mt[B.MT_NAMES[name]]] * n
    e['tr.sw'] = [1 if str(tm).startswith('Engineer') else 0] * n
    e['tr.dk'] = [1 if y in TM.DATA_YEARS else 0 for y in years]
    e['tr.col'] = [k + 1 for k in range(n)]
    e['tr.pol'] = [1 if inp['scen'] > 1 else 0] * n
    for it in B.TR_ROWS:                                 # Transport1 shares of the base year split (data rows)
        if it['kind'] == 'plain' and it['var'] == 'trshf':
            e[it['key']] = data(lambda k, v=it['par'][0]: inp['data'].get(v, {}).get(years[k], 0.0))
    e['trpri'] = inp['rp']['nga_ind']
    e['trpop'] = inp['pop']
    for i, f in enumerate(('gso', 'die', 'lpg', 'nga')):
        e[f'vk0.{f}'] = [o[2072 + i][0]] * n
        e[f'bu.{f}'] = [o[f'cO{5170 + i}']] * n
        e[f'cq.{f}'] = [o[f'cQ{5170 + i}']] * n
        e[f'cf2.{f}'] = [o[f'cE{5325 + i}']] * n
    for i, f in enumerate(('die', 'lpg', 'nga')):
        e[f'vr0.{f}'] = [o[2097 + i][0]] * n
    e['cf2.ecy'] = [o['cE5331']] * n
    e['df.pas'], e['df.fre'], e['df.cyc'] = ([o[c]] * n for c in ('cU5170', 'cV5170', 'cW5170'))
    e['trnc'] = hold(lambda k: o[2108][k] / (o[2036][k] + o[2037][k]))
    e['trjc'] = hold(lambda k: (1 + (1 - gpc[k] / P['cyc_peak_inc']) * P['cyc_scale']) * o[2129][k])
    for c, (cp, avg) in TR_PIV.items():
        a = [z(v) for v in o[avg]]
        e[f'pva.{c}'] = [None if k < 2 else a[k] * a[k] / a[k - 1] for k in range(n)]
        pm = []
        for k, y in enumerate(years):
            fy = P[f'fb_year|{cp}']
            pm.append(None if k < 2 else P[f'fb_pivot|{cp}'] if y == fy else
                      max(0, z(pm[-1]) - P[f'fb_pivot_chg|{cp}']) if y > fy else 0)
        e[f'pvm.{c}'] = pm
    for c, satf, own in (('pas', lambda k: o[2166][k] * (1 - o[2168][k]), lambda k: o[2087][k] + o[2086][k]),
                         ('fre', lambda k: o[2166][k] * o[2168][k], lambda k: o[2110][k] + o[2109][k])):
        b_ = P[f'own_gomp_b|{"pass" if c == "pas" else "fre"}']
        e[f'jh.{c}'] = hold(lambda k: gomp(satf(k), gpc[k], b_))
        e[f'ji.{c}'] = hold(own)
        e[f'jj.{c}'] = [a / b for a, b in zip(e[f'ji.{c}'], e[f'jh.{c}'])]
        sat = o[4783 if c == 'pas' else 4899]
        e[f'gt.{c}'] = [gomp(sat[k], gpc[k], b_) * (e[f'jj.{c}'][k - 1] if k else 0) for k in range(n)]
    phev = data(lambda k: max(0.0, o[2063][k] - o[2065][k]) * o[2038][k])
    e['icd.phv'] = phev
    for i, f in enumerate(('gso', 'die', 'lpg', 'nga')):
        e[f'icd.{f}'] = data(lambda k: o[4835 + i][k] / sum(o[4835 + j][k] for j in range(4))
                             * (1 - o[4805][k] - phev[k]))

    def cross(sh0, rat0, m, i, k):
        if k == 0:
            return None
        den = sum(z(o[sh0 + j][k - 1]) for j in range(m) if j != i)
        return None if den == 0 else sum(z(o[sh0 + j][k - 1]) * o[rat0 + j][k] for j in range(m) if j != i) / den
    for i, f in enumerate(('gso', 'die', 'lpg', 'nga', 'phv')):
        e[f'crs.{f}'] = [cross(4846, 4840, 5, i, k) for k in range(n)]
    for i, f in enumerate(('die', 'lpg', 'nga')):
        e[f'crf.{f}'] = [cross(4936, 4932, 3, i, k) for k in range(n)]
    e['bus0'] = [sum(o[r][0] for r in range(5310, 5315))] * n
    e['trbio'] = tr_road(o, inp)['bio']
    e['afe.num'] = [o[5207][k] * o[5223][k] + o[5251][k] * o[5265][k] + o[5285][k] * o[5299][k] for k in range(n)]
    for c, calc, act in (('pas', 4827, 4805), ('fre', 4914, 4916), ('cyc', 4990, 4992)):
        e[f'raf.{c}'] = data(lambda k: o[calc][k] - o[act][k])
    e['trsum'] = [sum(o[r][k] for r in (5325, 5326, 5327, 5328, 5331)) + e['trbio'][k] for k in range(n)]
    return e


TR_PAR_CHECK = {  # section-5b parameter rows compared with the engine's side-table scalars: row key -> D:G keys
    **{f'bs.{f}.{v}': (f'cL{r}', f'cM{r}', f'cN{r}') for f, v, r in (
        ('gso', 'pas', 2017), ('gso', 'cyc', 2018), ('gso', 'lgt', 2019), ('die', 'pas', 2020), ('die', 'bus', 2021),
        ('die', 'fre', 2022), ('die', 'lgt', 2023), ('lpg', 'pas', 2024), ('lpg', 'bus', 2025), ('lpg', 'fre', 2026),
        ('lpg', 'lgt', 2027), ('nga', 'pas', 2028), ('nga', 'bus', 2029), ('nga', 'fre', 2030), ('nga', 'lgt', 2031))},
    'tax.pas': ('cV4304', 'cV4308', 'cV4309', 'cV4312'), 'tax.fre': (None, 'cW4308', 'cW4309', 'cW4312'),
    'tax.cyc': ('cX4304', 'cX4308', 'cX4309', 'cX4312'), 'tr.bus': ('cL2140', 'cL2141', 'cL2142', 'cL2143')}


def check_transport(ws, g, res, label):
    """v3.5: every section-5b row with year values (and the side-table parameter rows) vs the engine."""
    o, inp = res[('TR', '', '')]
    e = tr_expected(o, inp, res[('TRMT', '', '')])
    _, base, years = B.group_cols(g)
    worst, n, missing, by_key = (0.0, None), 0, [], {}
    blank = lambda v: v is None or v == ''
    for r, what, it in B.TR_LAYOUT:
        if what != 'row':
            continue
        key = it['key']
        if it['kind'] == 'par':
            for j, ek in enumerate(TR_PAR_CHECK.get(key, ())):
                if ek is None:
                    continue
                v, x = ws.cell(r, 4 + j).value, o[ek]
                d = float('inf') if not isinstance(v, (int, float)) else abs(v - x) / max(1.0, abs(x))
                n += 1
                if d > worst[0]:
                    worst = (d, f'{L(4 + j)}{r} ({key})')
            continue
        if key not in e:
            missing.append(key)
            continue
        for k, c in enumerate([base] + years):
            v, x = ws.cell(r, c).value, e[key][k]
            if blank(x) and blank(v):
                d = 0.0
            elif isinstance(x, str) or isinstance(v, str):
                d = 0.0 if v == x else float('inf')
            elif blank(x) or blank(v):
                d = float('inf')
            else:
                d = abs(v - x) / max(1.0, abs(x))
            n += 1
            if d > by_key.get(key, (0.0, ''))[0]:
                by_key[key] = (d, f'{L(c)}{r} {B.BASE_YEAR + k}')
            if d > worst[0]:
                worst = (d, f'{L(c)}{r} ({key}, {B.BASE_YEAR + k})')
    ok = worst[0] < TOL and not missing
    bad = sorted(((d, k_, at) for k_, (d, at) in by_key.items() if d >= TOL), key=lambda t: t[0], reverse=True)
    if bad:                                       # v5.2: the rows over the tolerance, worst first
        log(f'  - {label}: section-5b rows over the tolerance (worst first, {len(bad)} rows): '
            f'{[(k_, at, float(f"{d:.3g}")) for d, k_, at in bad[:30]]}')
    log(f'- {label}: section 5b, {sum(1 for _r, w, _i in B.TR_LAYOUT if w == "row")} rows ({n} cells incl. the '
        f'side-table parameters) vs transport_model_ref_v7_0.engine (all fixes), max relative diff {worst[0]:.2e} '
        f'(at {worst[1]}){"; no expected value for " + str(missing[:8]) if missing else ""} {"OK" if ok else "FAIL"}')
    return ok


def _recompute_gdp(mt, controls=None, **kw):
    """v3.1: the recomputation with the GDP feedback: growth depends on earlier years only, so iterating the
    whole recomputation on the growth path converges (exactly after at most one pass per year)."""
    kw.pop('gdp', None)
    kw['controls'] = controls
    ref_kw = {k: v for k, v in kw.items() if k in ('controls', 'base', 'shock_on', 'power', 'ecp', 'spot')}
    ref_rev = total_rev(_recompute_once(scenario_mt(1), **ref_kw))
    res = _recompute_once(mt, **kw)
    g = res[('gdp.pos.pct', '', '')]
    for _it in range(len(B.YEARS) + 2):
        g_new = gdp_section(res, mt, ref_rev)
        if max(abs(a - b) for a, b in zip(g_new, g)) < 1e-15:
            break
        g = g_new
        res = _recompute_once(mt, gdp=g, **kw)
    return res


# v2.8: section 14 (non-CO2 GHGs and methane), an independent copy from the CSVs (GHG_Method_v7_0.md)
BIO_EB = {f: next((float(r[f] or 0) for r in read('legacy_Balances.csv') if r['country_code'] == ISO
                   and r['flow_code'] == 'road'), 0.0) for f in ('bgs', 'bdi', 'obf')}   # v4.12 (LD62)
class _MFeeOn(dict):
    """v5.2: 1 where the methane fee applies to the source: sheet Manual inputs J196:J200 (legacy addresses; v4.12,
    LD46), read on first use."""
    def __missing__(self, j):
        sw = {nm: mi(f'J{lr}') for _r, nm, _l, _v, lr in B.MFEE_SETTINGS}
        self.update({k: 1.0 if str(sw[B.MFEE_SW[k]])[:3] == 'Yes' else 0.0 for k in B.MFEE_SW})
        return self[j]


MFEE_ON = _MFeeOn()
OIL_SHARE = {pc: float(r[pc.split('.')[0] + '_share']) for r in read('legacy_OilProductShares.csv')
             if r['countrycode'] == ISO for pc in B.OIL_SHARE}      # v4.12 (LD5)
NC_EF = {(r['subsector'], r['fuel']): (float(r['fe_in']), float(r['fe_fin'])) for r in read('ef_nonco2.csv')
         if r['pollutant'] == 'ch4' and r['country'] == ISO.lower()}
_GHG_REF = {}
NC_ALL = {(r['subsector'], r['fuel'], r['pollutant']): (float(r['fe_in']), float(r['fe_fin']))
          for r in read('ef_nonco2.csv') if r['country'] == ISO.lower()}
GWP_AP = {r['pollutant']: float(r['gwp100']) for r in read('gwp_pollutants.csv') if r['region'] == REGION}
NC_PAIRS = {(s_, f_) for s_, f_, _p in NC_ALL}


def nc_sub(s_, f_):
    """v4.12 (bug L59, was I35): GAINS subsector and fuel of the factors of subsector s_ and EF_PM fuel f_: its own
    (CH4_SUB) if that has factors for the fuel, else the fallback (B.ef_fallback)."""
    g = B.CH4_SUB.get(s_, 'mnf')
    return (g, f_) if (g, f_) in NC_PAIRS else B.ef_fallback(s_, f_)


def ap_section(res, years, pe):
    """v2.9: local air pollutants (kt), independent copy: fuel use x EF (kt/PJ x 41.868 = t/ktoe), the base-year
    factor moving linearly to the final factor in 2039, flat after; forcing = total x GWP100 (Egypt: region afr)."""
    ny = len(years)
    w = [min(1.0, (y - B.BASE_YEAR) / (K['EFEndYear'] - B.BASE_YEAR)) for y in years]
    ef = lambda sub, fu, p, k: ((lambda a: (a[0] * (1 - w[k]) + a[1] * w[k]) * K['EFtPerKtoe'])(NC_ALL.get((sub, fu, p), (0.0, 0.0))))
    out = {'ap.w': w}
    grp = {x[0]: x[2] for x in B.SUBSECTORS}
    for p, _l in B.AP_POLS:
        for s_ in [x[0] for x in B.SUBSECTORS]:
            fe = lambda f_: 'jfu' if (s_, f_) == ('avi', 'ker') else f_
            out[f'ap.{p}.{s_}'] = [sum(res[('ener', s_, f_)][k] * ef(*nc_sub(s_, fe(f_)), p, k)
                                       for f_ in [x[0] for x in B.FUELS]) / 1000 for k in range(ny)]
        out[f'ap.{p}.pow'] = [sum(pe[t][k] * ef('pow', t, p, k) for t in POWER_TECH) / 1000 for k in range(ny)]
        for g_ in B.AP_GROUPS:
            out[f'ap.{p}.{g_}'] = [sum(out[f'ap.{p}.{s_}'][k] for s_ in grp if grp[s_] == g_) for k in range(ny)]
        out[f'ap.{p}.all'] = [sum(out[f'ap.{p}.{s_}'][k] for s_ in grp) + out[f'ap.{p}.pow'][k] for k in range(ny)]
    bal = {r['flow_code']: r for r in read('legacy_Balances.csv') if r['country_code'] == ISO}
    for f_ in [x[0] for x in B.FUELS]:               # v5.2 (v4.11, LD53): food share of food & forestry by fuel
        num = float(bal.get('info_food', {}).get(f_) or 0)
        den = sum(float(bal.get(fl, {}).get(f_) or 0) for fl in ('info_agrc', 'info_fish', 'info_food', 'info_wood'))
        out[f'apfd.{f_}'] = [res[('ener', 'foo', f_)][k] * (num / den if den else 0.0) for k in range(ny)]
    for p, _l in B.AP_POLS:                          # food part of food & forestry and the rest (rows 6702-6703)
        out[f'ap.{p}.fod'] = [sum(out[f'apfd.{f_}'][k] * ef(*nc_sub('foo', f_), p, k) for f_ in [x[0] for x in B.FUELS])
                              / 1000 for k in range(ny)]
        out[f'ap.{p}.fag'] = [a - b for a, b in zip(out[f'ap.{p}.foo'], out[f'ap.{p}.fod'])]
    for p, _l in B.AP_POLS:                          # v3.0: air-pollution module sectors (legacy rows 6693-6704)
        pw = lambda t, k: pe[t][k] * ef('pow', t, p, k) / 1000
        sec = {'cpp': lambda k: pw('coa', k), 'gpp': lambda k: pw('nga', k),
               'opp': lambda k: sum(pw(t, k) for t in POWER_TECH if t not in ('coa', 'nga')),
               'rod': lambda k: out[f'ap.{p}.rod'][k],
               'gro': lambda k: sum(out[f'ap.{p}.{s_}'][k] for s_ in ('res', 'srv', 'cst')),
               'oth': lambda k: sum(out[f'ap.{p}.{s_}'][k] for s_ in grp if s_ not in ('rod', 'res', 'srv', 'cst', 'foo')),
               'foo': lambda k: out[f'ap.{p}.foo'][k]}
        for s_, fn in sec.items():
            out[f'aps.{p}.{s_}'] = [fn(k) for k in range(ny)]
    for s_, _n in B.AP_SECS:                         # POM = 1.3 x OC; other PM2.5 = max(0, PM2.5 - BC - POM)
        out[f'aps.pom.{s_}'] = [K['PomPerOC'] * x for x in out[f'aps.oc.{s_}']]
        out[f'aps.opm.{s_}'] = [max(0.0, a - b - c) for a, b, c in zip(out[f'aps.pm2.{s_}'], out[f'aps.bc.{s_}'],
                                                                         out[f'aps.pom.{s_}'])]
    g14 = lambda k_, k: res[(f'S14:{k_}', '', '')][k]          # v3.12: CH4 as legacy (section 14 rows)
    chs = lambda subs, k: sum(res[('ch4', s_, f_)][k] for s_, f_ in B.PAIRS if s_ in subs)
    oth = [s_ for s_ in grp if s_ not in ('rod', 'res', 'srv', 'cst', 'foo')]
    agw = [j for j, *x in B.CH4_SOURCES if x[4] in ('agr', 'wst')]
    sec = {'cpp': lambda k: g14('ch4.pw.coa', k), 'gpp': lambda k: g14('ch4.pw.nga', k),
           'opp': lambda k: g14('ch4.pw.oop', k) + g14('ch4.pw.bio', k), 'rod': lambda k: chs(['rod'], k),
           'gro': lambda k: chs(['res', 'srv', 'cst'], k), 'oth': lambda k: chs(oth, k) + g14('ch4.sup', k),
           'foo': lambda k: chs(['foo'], k) + sum(g14(f'ch4.em.{j}', k) for j in agw)}
    for s_, fn in sec.items():
        out[f'aps.ch4.{s_}'] = [fn(k) for k in range(ny)]
    for q in B.APS_POLS:                             # v3.12: a total for every pollutant
        out[f'aps.{q}.all'] = [sum(out[f'aps.{q}.{s_}'][k] for s_, _n in B.AP_SECS) for k in range(ny)]
    for p in B.AP_GWP:
        out[f'apf.{p}'] = [x * GWP_AP[p] / 1000 for x in out[f'ap.{p}.all']]
    out['apf.all'] = [sum(out[f'apf.{p}'][k] for p in B.AP_GWP) for k in range(ny)]
    for k_, v_ in out.items():
        res[(f'S15:{k_}', '', '')] = v_


def ch4_ef(ef0, ef1, y):
    """CH4 EF in t/ktoe: kt/PJ x 41.868, linear from the base year to 2039, flat after."""
    w = min(1.0, (y - B.BASE_YEAR) / (K['EFEndYear'] - B.BASE_YEAR))
    return (ef0 + (ef1 - ef0) * w) * K['EFtPerKtoe']


def ghg_section(res, mt, years, pe, ref_fn):
    """The source shares, the base activity of each source and the energy-CH4 calibration are those of scenario 1
    in the last inventory year (as the workbook: calibration to the observed inventory, i.e. the baseline)."""
    iso, ny = ISO, len(years)
    inv = {int(r['year']): {k: float(v) for k, v in r.items() if k not in ('iso', 'year') and v != ''}
           for r in read('ghg_inventory.csv') if r['iso'] == iso}
    gy = max(inv)
    kg = years.index(gy)
    popd = {int(r['year']): float(r['population_thousands']) for r in read('population.csv') if r['iso'] == iso}
    gdp = read('weo.csv')[0]
    ch4i = {B.CH4_TIER[r['source']]: r for r in read('ch4_inputs.csv') if r['iso'] == iso}
    bal = {r['fuel']: float(r['production'] or 0) for r in read('energy_balance.csv') if r['country'] == ISO}
    gwp = {n: K[n] for n in ('GWPCH4F', 'GWPCH4NF')}
    el = {}                         # v5.2: Manual inputs K325:M327 (legacy addresses; text such as "na" = 0, as N())
    for col, c_ in zip('KLM', [next(k for k, v in B.MI_GHG_CAT.items() if v == mi(f'{x}325')) for x in 'KLM']):
        for d_, r in (('pop', 326), ('gdppc', 327)):
            v = mi(f'{col}{r}')
            el[(c_, d_)] = float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else 0.0
    m_ = lambda name: mt[B.MT_NAMES[name]]
    yes = lambda v: str(v)[:3] == 'Yes'
    out = {}
    put = lambda k, vals: out.__setitem__(k, list(vals))
    y0, y1, s0, s1 = (float(m_(x)) for x in ('MPIntro', 'MPOutro', 'MPLevelStart', 'MPLevelTarget'))
    path = [0.0 if y < y0 else s0 + (s1 - s0) / max(y1 - y0, 1) * (y - y0) for y in years]
    cp = res[('cptraj', '', '')]
    pol = 1.0 if mt.get('scen', 1) > 1 else 0.0          # v4.12 (LD46): the fee only in policy scenarios (legacy 2238)
    fee = [p * pol + (cp[k] if yes(m_('CTforMethane')) else 0.0) for k, p in enumerate(path)]
    res[('mfee.p', '', '')], res[('mfee', '', '')] = path, fee
    pop = [popd[y] for y in years]
    popg = [pop[0] / popd[years[0] - 1] - 1] + [pop[k] / pop[k - 1] - 1 for k in range(1, ny)]
    gpc = [(1 + res[('gdp.pos.pct', '', '')][k]) / (1 + popg[k]) - 1 for k, y in enumerate(years)]   # v3.1
    co2 = res[('co2', 'all', 'all')]
    ref1 = None                                        # scenario 1 results (None while computing scenario 1)
    if not _GHG_REF.get('busy'):
        _GHG_REF['busy'] = True
        try:
            ref1 = ref_fn()
        finally:
            _GHG_REF['busy'] = False
    if yes(m_('AdditionMitigationPoliciesNonEnergy')) and ref1 is not None:
        ref = ref1[('co2', 'all', 'all')]
        m = [co2[k] / ref[k] if ref[k] > 0 else 1.0 for k in range(ny)]
    else:
        m = [1.0] * ny
    grp = {x[0]: x[2] for x in B.SUBSECTORS}
    co2i = [sum(res[('co2', s_, f_)][k] for s_, f_ in B.PAIRS if grp[s_] == 'ind') for k in range(ny)]
    gi = [0.0] + [co2i[k] / co2i[k - 1] - 1 if co2i[k - 1] else 0.0 for k in range(1, ny)]
    dr = {c: [1.0] + [(1 + gpc[k]) ** el[(c, 'gdppc')] * (1 + popg[k]) ** el[(c, 'pop')] * m[k] / m[k - 1]
                      for k in range(1, ny)] for c in B.GHG_DRV}
    put('pop', pop), put('pop.g', popg), put('gdppc.g', gpc), put('ghg.m', m), put('ghg.gi', gi)
    for c in B.GHG_DRV:
        put(f'ghg.dr.{c}', dr[c])
    fuel_tot = lambda fu: [sum(res[('ener', s_, fu)][k] for s_ in [x[0] for x in B.SUBSECTORS]) + pe[fu][k]
                           for k in range(ny)]
    src = {j: x for j, *x in B.CH4_SOURCES}
    per = {j: (float(ch4i[x[1]][x[2]]) if x[2] else 1.0) for j, x in src.items()}
    abt_ = {}
    for j, (lab, tier, sc, gw, cat) in src.items():
        a_, b_ = float(ch4i[tier]['avg_pow_a']), float(ch4i[tier]['avg_pow_b'])
        abt_[j] = [min(1.0, max(0.0, a_ * (fee[k] * gwp[gw] * MFEE_ON[j]) ** b_)) for k in range(ny)]
    # v6.0 (v5.6, I66): oil, gas and coal production grow with world demand and the producer price (legacy 6132-6149)
    pic = {}
    for r_ in read('legacy_Prices_int_cells.csv'):
        pic[(int(r_['row']), int(r_['col']))] = r_['value']
    ycol = {}
    for (r_, c_), v in pic.items():
        if r_ == 322 and c_ >= 7:
            try:
                ycol[int(float(v))] = c_
            except ValueError:
                pass
    ged = str(m_('GlobalEnergyDemand'))
    widx = min(next((i + 1 for i, t in enumerate(('Stated Policies*', 'Announced Pledges', 'Sustainable Development',
                                                   'Net Zero')) if ged == t), 1), 3)
    num_ = lambda v: float(v) if v not in (None, '') else 0.0
    wd = {f_: [num_(pic.get((322 + pos + widx - 1, ycol.get(y, 0)))) for y in years]
          for f_, pos in (('oil', 5), ('coa', 1), ('nga', 9))}
    upk = {'oil': 41868 / 6.1408, 'coa': 41868 / 29.3076, 'nga': 41868 / 1.055056}
    elp = {f_: float(mi(c_) or 0) for f_, c_ in (('oil', 'J190'), ('coa', 'J191'), ('nga', 'J192'))}
    ptr = float(mi('J194') or 0)
    prd0 = {'oil': bal['oop'], 'coa': bal['coa'], 'nga': bal['nga']}
    d_fk = {'og': prd0['oil'] + prd0['nga'], 'cm': prd0['coa']}
    enc = {r['CPAT Code']: r for r in read('legacy_EnergyCons.csv')}
    cons = lambda f_: sum(float(v or 0) for k_, v in enc.get(f'{iso.lower()}.mit.enc.{f_}', {}).items()
                          if k_ not in ('CPAT Code', 'Year', 'CountryName', 'FuelType', 'elec', 'wav'))
    e_gy0 = {'og': d_fk['og'], 'cm': d_fk['cm'], 'dg': cons('nga'), 'bm': cons('bio'),
             'liv': 1.0, 'ric': 1.0, 'wst': 1.0}                  # v6.0 (I47): data activity, as legacy row 894
    w0 = {j: min(K['MethShareCap'] * e_gy0[j] / sum(e_gy0[i] for i in B.CH4_FOSSIL), per[j]) for j in B.CH4_FOSSIL}
    sh0 = {j: (w0[j] / sum(w0.values()) if sum(w0.values()) else 0.0) if j in w0 else per[j] for j in src}
    invb0 = {c: inv[gy][f'{c}.{g_}'] for c, g_ in (('enr', 'ch4'), ('agr', 'ch4'), ('wst', 'ch4'))}
    em0 = {j: invb0[src[j][4]] * sh0[j] * 1000 / gwp[src[j][3]] for j in ('og', 'cm')}
    fk = {j: [0.0] + [0.0 if d_fk[j] == 0 else fee[k] * gwp[src[j][3]] * MFEE_ON[j] * 1000 * em0[j] / d_fk[j]
                      * (1 - abt_[j][k]) for k in range(1, ny)] for j in ('og', 'cm')}
    gpi = {f_: res[('gp', 'int', f_)] for f_ in ('oil', 'coa', 'nga')}
    pi = {f_: [1.0] + [1 + (fk['cm' if f_ == 'coa' else 'og'][k] - fk['cm' if f_ == 'coa' else 'og'][k - 1])
                       / (gpi[f_][k] * upk[f_]) * ptr for k in range(1, ny)] for f_ in ('oil', 'coa', 'nga')}
    prd = {}
    for f_ in ('oil', 'coa', 'nga'):
        v_ = []
        for k, y in enumerate(years):
            v_.append(prd0[f_] if y <= B.BASE_YEAR + 1 else
                      v_[-1] * pi[f_][k] ** elp[f_] * wd[f_][k - 1] / wd[f_][k - 2] if wd[f_][k - 2] else v_[-1])
        prd[f_] = v_
    for f_ in ('oil', 'coa', 'nga'):
        put(f'ch4.wd.{f_}', wd[f_]), put(f'ch4.pi.{f_}', pi[f_]), put(f'ch4.prd.{f_}', prd[f_])
    put('ch4.fk.og', fk['og']), put('ch4.fk.cm', fk['cm'])
    act = {'og': [a + b for a, b in zip(prd['oil'], prd['nga'])], 'cm': prd['coa'], 'dg': fuel_tot('nga'),
           'bm': fuel_tot('bio')}
    for j, c in (('liv', 'agr'), ('ric', 'agr'), ('wst', 'wst')):
        a = [1.0]
        for k in range(1, ny):
            a.append(a[-1] * (1 + gpc[k]) ** el[(c, 'gdppc')] * (1 + popg[k]) ** el[(c, 'pop')])
        act[j] = a
    e_gy = dict(e_gy0)                                    # v6.0 (I47): data activity (legacy row 894)
    w = {j: min(K['MethShareCap'] * e_gy[j] / sum(e_gy[i] for i in B.CH4_FOSSIL), per[j]) for j in B.CH4_FOSSIL}
    share = {j: (w[j] / sum(w.values()) if sum(w.values()) else 0.0) if j in w else per[j] for j in src}
    invb = {c: inv[gy][f'{c}.{g_}'] for c, g_ in (('enr', 'ch4'), ('agr', 'ch4'), ('wst', 'ch4'), ('lucf', 'co2'))}
    em = {}
    for j, (lab, tier, sc, gw, cat) in src.items():
        base = invb[cat] * share[j] * 1000 / gwp[gw]
        abt = abt_[j]                                     # v4.12 (LD46): Settings switch of the source
        em[j] = [0.0 if e_gy[j] == 0 else base * act[j][k] / e_gy[j] * (1 - abt[k]) for k in range(ny)]
        put(f'ch4.act.{j}', act[j]), put(f'ch4.abt.{j}', abt), put(f'ch4.em.{j}', em[j])
        if j == 'og':
            flare = float(ch4i[tier]['per_flare'])
            put('ghg.flr', [0.0 if e_gy[j] == 0 else K['FlareCO2perCH4'] * flare * base * act[j][k] / e_gy[j] * abt[k] / 1000
                            for k in range(ny)])
    for f_ in B.CH4_PW:
        ef0, ef1 = NC_EF.get(('pow', f_), (0.0, 0.0))
        put(f'ch4.pw.{f_}', [pe[f_][k] * ch4_ef(ef0, ef1, y) / 1000 for k, y in enumerate(years)])
    for g_ in ['tra', 'bld', 'ind', 'oen']:
        put(f'ch4.c.{g_}', [sum(res[('ch4', s_, f_)][k] for s_, f_ in B.PAIRS if grp[s_] == g_) for k in range(ny)])
    put('ch4.c.pow', [sum(out[f'ch4.pw.{f_}'][k] for f_ in B.CH4_PW) for k in range(ny)])
    put('ch4.c.all', [sum(out[f'ch4.c.{g_}'][k] for g_ in ['tra', 'bld', 'ind', 'oen', 'pow']) for k in range(ny)])
    put('ch4.sup', [sum(em[j][k] for j in B.CH4_FOSSIL) for k in range(ny)])
    if 'default' not in _GHG_REF and not _GHG_REF.get('busy') and not _CO2K.get('busy'):   # v7.0: ghg.k reads the
        # stored baseline methane; never inside the uncalibrated CO2 pass of co2k (its results would be cached)
        _GHG_REF['busy'] = True                                    # (sheet BaselineCO2, v6.2 I47): the shipped
        try:                                                       # baseline, also when a test changes a global
            _GHG_REF['default'] = _recompute_once(scenario_mt(1))  # setting (price controls, PwDeficitGas)
        finally:
            _GHG_REF['busy'] = False
    refd = _GHG_REF.get('default') if not _CO2K.get('busy') else None
    r1 = (lambda k_: refd[(f'S14:{k_}', '', '')][kg]) if refd else (lambda k_: out[k_][kg])
    mod = (r1('ch4.c.all') + r1('ch4.sup')) * gwp['GWPCH4F'] / 1000
    kc = invb['enr'] / mod if mod else 0.0
    put('ghg.k', [kc] * ny)
    hist = [y in inv for y in years]
    for c in B.GHG_CATS:
        for g_ in B.GHG_GASES:
            iv = [inv[y].get(f'{c}.{g_}', 0.0) if hist[k] else None for k, y in enumerate(years)]
            vals = []
            for k, y in enumerate(years):
                if (c, g_) == ('enr', 'co2'):
                    x = co2[k] + out['ghg.flr'][k]
                elif (c, g_) == ('enr', 'ch4'):
                    x = kc * (out['ch4.c.all'][k] + out['ch4.sup'][k]) * gwp['GWPCH4F'] / 1000
                elif g_ == 'ch4' and c in ('agr', 'wst'):
                    js = ('liv', 'ric') if c == 'agr' else ('wst',)
                    x = iv[k] if hist[k] else sum(em[j][k] for j in js) * gwp['GWPCH4NF'] / 1000
                elif hist[k]:
                    x = iv[k]
                elif k == 0:
                    x = 0.0
                elif (c, g_) == ('enr', 'n2o'):
                    x = vals[-1] * (co2[k] / co2[k - 1] if co2[k - 1] else 1)
                elif c == 'ipr':
                    x = vals[-1] * (1 + (gi[k] if yes(m_('IndustrialProcessEmissionsScaleEner')) else 0))
                elif (c, g_) == ('lucf', 'co2'):
                    p_ = vals[-1]
                    x = p_ if p_ < 0 else p_ / m[k - 1] * m[k] - abs(invb['lucf']) * float(m_('LULUCFAnnualEmissionsDecline'))
                elif c in B.GHG_DRV:
                    x = vals[-1] * dr[c][k]
                else:
                    x = vals[-1]
                vals.append(x)
            put(f'ghg.{c}.{g_}', vals)
    for g_ in B.GHG_GASES:
        put(f'ghg.g.{g_}', [sum(out[f'ghg.{c}.{g_}'][k] for c in B.GHG_CATS if c != 'lucf') for k in range(ny)])
    for c in B.GHG_CATS:
        put(f'ghg.c.{c}', [sum(out[f'ghg.{c}.{g_}'][k] for g_ in B.GHG_GASES) for k in range(ny)])
    put('ghg.all', [sum(out[f'ghg.g.{g_}'][k] for g_ in B.GHG_GASES) for k in range(ny)])
    put('ghg.inc', [a_ + b_ for a_, b_ in zip(out['ghg.all'], out['ghg.c.lucf'])])
    nonf = [sum(em[j][k] * MFEE_ON[j] for j in ('liv', 'ric', 'wst')) for k in range(ny)]
    fosf = [sum(em[j][k] * MFEE_ON[j] for j in B.CH4_FOSSIL) for k in range(ny)]   # v4.12: liable sources only
    put('ch4.rev', [(fosf[k] * gwp['GWPCH4F'] + nonf[k] * gwp['GWPCH4NF']) * fee[k] * 1000 / 1e6 for k in range(ny)])
    for k_, v_ in out.items():
        res[(f'S14:{k_}', '', '')] = v_
    res[('rmf', 'all', 'all')] = out['ch4.rev']
    res[('rtot', 'all', 'all')] = [a_ + b_ for a_, b_ in zip(res[('rtot', 'all', 'all')], out['ch4.rev'])]
    return out


POWER_TECH = ['coa', 'nga', 'oop', 'nuc', 'wnd', 'sol', 'hyd', 'ore', 'bio']    # independent copy (legacy order)


def check_power_method():
    """Method = legacy: power_model_ref_v7_0 with no bug fixes and the legacy demand shock, fed with the cached legacy
    inputs (fuel and policy costs D4-D6, GDP, prices of 2021 and the historical years), reproduces every cached legacy
    row of the engineer model and the price chain, for the baseline and the carbon-tax run."""
    ok = True
    for run, label in (('base', 'baseline'), ('ctax', 'carbon-tax run')):
        res = PM.legacy_test(run)
        worst = res[0]
        good = worst[0] < 1e-9 and len(res) >= 200
        ok &= good
        log(f'- {label}: {len(res)} legacy rows (demand by subsector, required generation, capacity, generation, shares, '
            f'fuel use, retirements, investment shares and both rounds, nameplate and USD investment, B1 phi, E1 '
            f'investment cost, C7, B2, B6, E3, J, G1 prices, early retirement), 2022-2040: max relative diff '
            f'{worst[0]:.1e} (at {worst[1]} {worst[2]}) {"OK" if good else "FAIL"}')
    years = list(range(2022, 2041))
    k40 = years.index(2040)
    log('')
    log('Effect of each bug fix on the legacy Egypt inputs (2040; % change against legacy):')
    log('')
    log('| Fix | legacy rows | generation (base) | power CO2 (base) | generation (carbon tax) | VRE share (carbon tax) | '
        'investment USD 2022-2040 (base) |')
    log('|---|---|---|---|---|---|---|')

    def kpi(o):
        return (sum(o['gen'][i][k40] for i in range(9)), sum(o['co2'][i][k40] for i in range(9)),
                o['vre'][k40], sum(o['usd'][i][k] for i in range(9) for k in range(len(years))))
    leg = {run: kpi(PM.engine(PM.legacy_inputs(run), years, fix=frozenset(), shock=True)) for run in ('base', 'ctax')}
    for name, (rows, _d) in list(PM.FIXES.items()) + [('all', ('', ''))]:
        fx = PM.ALL_FIXES if name == 'all' else frozenset([name])
        b = kpi(PM.engine(PM.legacy_inputs('base'), years, fix=fx, shock=True))
        c = kpi(PM.engine(PM.legacy_inputs('ctax'), years, fix=fx, shock=True))
        pct = lambda a, z: f'{(a / z - 1) * 100:+.2f}%' if z else '0'
        log(f'| {name} | {rows} | {pct(b[0], leg["base"][0])} | {pct(b[1], leg["base"][1])} | '
            f'{pct(c[0], leg["ctax"][0])} | {pct(c[2], leg["ctax"][2])} | {pct(b[3], leg["base"][3])} |')
    return ok


GLOBAL_MT = {}                  # v5.1: global settings edited in a test (MTInputs scenario-1 column, e.g. BiomassLeakage)


def scenario_mt(g):
    mt = mt_used()
    for k, v in B.MT_SCENARIO_INPUTS[g].items():
        mt[B.MT_NAMES[k]] = v
    for k, v in GLOBAL_MT.items():
        mt[B.MT_NAMES[k]] = v
    mt['scen'] = g                              # v3.5: scenario number (section 5b policies act above 1)
    return mt


def gp_rows():
    return [(B.R_GP0 + k, 'int', fu) for k, (fu, *_r) in enumerate(B.GP_ROWS)]


FOCUS = {}                      # v5.1: label -> (max relative difference, cell) over the focus rows of compare


def compare(ws, g, exp, label, focus=None):
    """Group g against the Python recomputation exp. v5.1: focus = rows whose largest difference is also kept in
    FOCUS[label] (a test of one feature, apart from known differences elsewhere)."""
    _, base, years = B.group_cols(g)
    worst, n, fworst, missing = (0.0, None), 0, (0.0, None), set()
    pk = ('cptraj', 'ets.p', 'ets.pe', 'ets.cap', 'ets.est', 'ets.bce', 'ets.se', 'xct.p', 'xets.p',
          'xct.c', 'mfee.p', 'mfee', 'cpx')    # v4.15: data column of the year (v4.12); v4.16: explicit price
    rev = [(B.R_REV[f'{v}.all'], 'all', 'all') for v in B.REV_VARS + ['rtot']]
    for var, rows in ([(k, [(B.R_POL[k], '', '')]) for k in pk]
                      + [(v, [(B.R_POL[f'{v}.{s}'], s, '') for s in B.COV_SECTORS]) for v in ('bco2', 'obr')]
                      + [(v, [row]) for v, row in zip(B.REV_VARS + ['rtot'], rev)]
                      + [(v, [(B.R_REV[f'{v}.pow'], 'pow', 'all')]) for v in B.REV_VARS]
                      + [('ener', [(B.R_TOTAL, 'all', 'all'), (B.R_EPOW, 'pow', 'all')])]
                      + [('co2', [(B.R_EMI['co2.all'], 'all', 'all')])]
                      + [('co2.ets', [(B.R_EMI['co2.ets'], 'all', 'all')])] + [('gp', gp_rows())]
                      + [('co2.pow', [(B.R_EMI['co2.pow'], '', '')])]
                      + [(v, rows_of(v)) for v in B.PVARS + B.VARS if v not in PB_ONLY]
                      + [(v, [(r, c_, b_) for r, v_, b_, c_, _k in B.PW_ROWS if v_ == v]) for v in B.PW_VARS]
                      + [('rmf', [(B.R_REV['rmf.all'], 'all', 'all')])]
                      + [('rpsu', [(B.R_REV['rpsu.all'], 'all', 'all')])]                          # v4.16
                      + [(f'rpol.{q}', [(B.R_FIS[f'rpol.{q}'], '', '')]) for q in B.RPOL_KEYS + ['chk']]   # v4.15
                      + [(f'S14:{k}', [(B.R_GHG[k], '', '')]) for k, *_x in B.GHG_ROWS     # v2.8: section 14
                         if k not in B.GHG_PARONLY | {'ghg.h', 'ghg.ref', 'ghg.chg', 'ghg.pct'}]
                      + [(f'S15:{k}', [(B.R_AP[k], '', '')]) for k, *_x in B.AP_ROWS]       # v2.9: section 15
                      + [(f'S16:{k}', [(B.R_GDPS[k], '', '')]) for k, *_x in B.GDP_ROWS     # v3.1: section 16
                         if k not in ('fis.grp', 'fis.key') and k not in B.GDP_PARAMS]
                      + [('gdp.pos.pct', [(B.R_GDP, '', '')])]
                      + [(it['var'], [(B.R_LK[it['key']], 'res', it['b'])]) for it in B.LK_ROWS   # v5.1: 6b
                         if it['kind'] != 'head'] + [('lks', [(B.R_LKSUM, 'res', 'all')])]):
        for r, s, f in rows:
            if len(exp.get((var, s, f), ())) < 1 + len(years):    # v5.1: rows the Python reference does not
                missing.add(var.split(':')[-1])                     # recompute are reported, not compared
                continue
            for k, c in enumerate([base] + years):
                v, e = ws.cell(r, c).value, exp[(var, s, f)][k]
                d = float('inf') if not isinstance(v, (int, float)) else abs(v - e) / max(1.0, abs(e))
                n += 1
                if d > worst[0]:
                    worst = (d, f'{L(c)}{r}')
                if focus and r in focus and d > fworst[0]:
                    fworst = (d, f'{L(c)}{r}')
    ok = worst[0] < TOL
    if focus:                                  # v5.1: judged on the focus rows; the rest reported
        FOCUS[label] = fworst
        ok = fworst[0] < TOL
    log(f'- {label}: carbon price, ETS rows (price, tax-equivalent, cap, estimate, baseline, semi-elasticity, '
        f'baseline CO2 and OBR share by sector), revenue, CO2 and covered CO2 totals, gp, {len(B.PVARS)} price-fuel and {len(B.VARS)} '
        f'subsector variables, {len(B.PW_VARS)} power variables, sections 14-16 (GHGs, methane, local air pollutants, '
        f'GDP effects), GDP growth, '
        f'{n} cells, max relative '
        f'diff {worst[0]:.2e} (at {worst[1]})'
        + (f'; judged on the focus rows (residential block, section 6b): max relative diff {fworst[0]:.2e} (at '
           f'{fworst[1]})' if focus else '') + f' {"OK" if ok else "FAIL"}'
        + (f'; not in the Python reference (not compared): {sorted(missing)}' if missing else ''))
    return ok


# ------------------------------------------------------------------ checks
def check_shipped(ws_x):
    """v2.3: a host without LAMBDA support (LibreOffice here; Excel before 365) cannot evaluate the LAMBDA year 2041.
    Errors may appear only in the 2041 columns (Mitigation, and the 2041 column of MTOutputs); every year 2022-2040
    calculates. The years 2022-2040 then equal the LAMBDA host (ws_x: LAMBDAs expanded) everywhere except the power
    rows and the totals that include power: there the levelised window (D9) uses tvcx = last year's cost for 2041 and
    the moving average of fuel prices for power leaves 2041 out of 2039-2040 (reported, not a failure)."""
    wbv = openpyxl.load_workbook(recalc_path(B.OUT), data_only=True)
    ws_lo = wbv['Mitigation']
    last = {B.group_cols(g)[2][-1] for g, *_ in B.SCENARIOS}
    ok, parts, n41 = True, [], 0
    for wsx in wbv.worksheets:
        y41 = {c.column for c in wsx[4] if c.value == B.LAST_YEAR} if wsx.title == 'LiveOutputs' else set()
        errs, lam3 = [], lam_cols(wsx.title)
        for row in wsx.iter_rows():
            for c in row:
                if is_err(c.value):
                    if wsx.title == 'ScenarioCompare' and c.value == '#N/A' and \
                            B.cmp_na_only('ScenarioCompare', f'ScenarioCompare.{c.coordinate}'):   # v7.0: no result
                        continue
                    if (wsx.title == 'Mitigation' and c.column in last) or c.column in y41 | lam3:
                        n41 += 1
                    else:
                        errs.append(c.coordinate)
        ok &= not errs
        if errs:
            parts.append(f'{wsx.title}: {len(errs)} {errs[:6]}')
    log(f'- shipped file recalculated by LibreOffice (no LAMBDA support): {n41} error values in the LAMBDA year '
        f'{B.LAST_YEAR} and the LAMBDA test group {B.LAMBDA_GROUP} (with its spacer test column); elsewhere in all {len(wbv.worksheets)} sheets: {"none OK" if not parts else "FAIL " + "; ".join(parts)}')
    pw_rows = {r for r, *_ in B.PW_ROWS}
    subs = {r for v in B.PVARS + B.VARS for r, *_ in rows_of(v)} - pw_rows
    d_sub, d_pow = 0.0, 0.0
    for g, *_ in B.SCENARIOS:
        if g == B.LAMBDA_GROUP:            # v7.0: group 2 is the LAMBDA group (every year calls the LAMBDAs)
            continue
        _c, b, ys = B.group_cols(g)
        for c in [b] + ys[:-1]:
            for r in subs:
                a_, x_ = ws_lo.cell(r, c).value, ws_x.cell(r, c).value
                if isinstance(x_, (int, float)):
                    d_sub = max(d_sub, abs(a_ - x_) / max(1.0, abs(x_)))
            for r in (B.R_PW[('gtot', '')], B.R_EMI['co2.pow'], B.R_PW[('rp', 'res')]):
                a_, x_ = ws_lo.cell(r, c).value, ws_x.cell(r, c).value
                d_pow = max(d_pow, abs(a_ - x_) / max(1e-9, abs(x_)))
    good = d_sub < TOL
    ok &= good
    log(f'- 2022-2040 without LAMBDA support vs with it: price and subsector rows identical (max rel diff {d_sub:.2g}) '
        f'{"OK" if good else "FAIL"}; power (generation, power CO2, residential price) max rel diff {d_pow:.2%} '
        f'(levelised window and moving average without the 2041 values)')
    return ok


def uniform(ws, cells, label):
    forms = {r1c1(ws.cell(r, c).value, r, c) for r, c in cells}
    ok = len(forms) == 1
    log(f'- {label}: {len(cells)} cells, {len(forms)} formula {"OK" if ok else "FAIL"}')
    return ok, next(iter(forms))


def check_uniformity(wb):
    """One relative-R1C1 formula per variable and column block: section-2 prices have a history block (base year to
    the last historical year, data) and a projection block; every other variable a base-year column and a plain
    block to 2040; the last year 2041 calls the named LAMBDA of the row (v2.3: the LAMBDA year, one formula per row
    block too); sheet Lambdas lists the LAMBDA formula of every calculated row."""
    LAMY = (f'LAMBDA year {B.LAST_YEAR}', lambda b, ys: [ys[-1]])
    ws = wb['Mitigation']
    ok = True
    grp = [B.group_cols(g) for g, *_ in B.SCENARIOS if g != B.LAMBDA_GROUP]   # v7.0: the plain groups (group 1)
    grp3 = [B.group_cols(B.LAMBDA_GROUP)]   # v4.16: since v4.3 only the LAMBDA test group calls the LAMBDAs (groups
    on = lambda label: grp3 if label == LAMY[0] else grp   # 1-2 are plain in 2041 too): the LAMBDA year is group 3's
    nh = B.LAST_HIST - B.BASE_YEAR           # plain years in the history block after the base year
    for var in B.PVARS + B.VARS:
        rows = [r for r, _s, _f in rows_of(var)]
        if var in ('sp', 'txo', 'txf', 'txfx'):          # v4.16: txfx has a history and a projection formula
            blocks = [(f'history {B.BASE_YEAR}-{B.LAST_HIST}', lambda b, ys: [b] + ys[:nh]),
                      (f'projection {B.LAST_HIST + 1}-{B.YEARS[-2]}', lambda b, ys: ys[nh:-1]), LAMY]
        elif var in ('spf', 'gpi'):            # v2.5/v2.6: data rows (no LAMBDA)
            blocks = [('base year', lambda b, ys: [b]), (f'{B.YEARS[0]}-{B.LAST_YEAR}', lambda b, ys: ys)]
        elif var in B.PVARS:
            blocks = [(f'{B.BASE_YEAR}-{B.YEARS[-2]}', lambda b, ys: [b] + ys[:-1]), LAMY]
        else:
            blocks = [('base year', lambda b, ys: [b]), (f'{B.YEARS[0]}-{B.YEARS[-2]}', lambda b, ys: ys[:-1]), LAMY]
        good, forms = True, []
        for label, cols in blocks:
            g, f = uniform(ws, [(r, c) for r in rows for _, b, ys in on(label) for c in cols(b, ys)], f'`{var}` {label}')
            good &= g
            forms.append(f)
        g4 = all(uniform(ws, [(r, CI(pc)) for r in rows], f'`{var}` column {pc}')[0] for pc in B.PARAM_COLS)
        if not (var in ('spf', 'gpi') or LAMBDA_CALL.search(forms[-1])):   # v7.2: logged (NORMS 3b.4)
            log(f'  - `{var}` LAMBDA year: the formula calls no named LAMBDA FAIL')
            good = False
        for f in forms:
            log(f'  - `{f[:150]}`')
        if var in ('sp', 'txo'):
            plain_if = any('Settings!R10C3' in f for f in forms)      # the last-historical-year switch
            log(f'  - history and projection blocks without the history/projection IF (no reference to the last '
                f'historical year): {"OK" if not plain_if else "FAIL"}')
            good &= not plain_if
        ok &= good and g4
    mt_rows = ([B.R_POL[k] for k, v_, _f, _s, kind, _m in B.POL if kind == 'mt' and v_ != 'ctcov']
               + [B.R_PRI[p] for p in B.PRI_PARAMS])
    ok &= uniform(ws, [(r, c) for r in mt_rows for _, b, ys in grp for c in [b] + ys],
                  'Section 1 and 2 MTInputs rows')[0]
    cov_rows = [B.R_POL[k] for k, v_, _f, _s, kind, _m in B.POL if kind == 'mt' and v_ == 'ctcov']   # v5.6: phase-out
    ok &= uniform(ws, [(r, c) for r in cov_rows for _, b, ys in grp for c in [b] + ys],
                  'Section 1 carbon-tax coverage rows (MTInputs, uncovered share phased in: exph)')[0]
    ok &= uniform(ws, [(r, c) for r, *_ in gp_rows() for _, b, ys in grp for c in [b] + ys],
                  'section 2 international prices `gp` (data rows, plain)')[0]
    ok &= uniform(ws, [(B.R_GPN0 + k, c) for k in range(len(B.GP_ROWS)) for _, b, ys in grp for c in [b] + ys],
                  'section 2 international prices before the adjustment `gpn` (data rows, plain)')[0]
    for k_ in ('gp.src', 'gp.adj'):
        ok &= uniform(ws, [(B.R_PRI[k_], c) for _, b, ys in grp for c in [b] + ys], f'section 2 `{k_}` (plain)')[0]
    eld = [h + 1 for h in B.SUB_HEAD.values()]
    ok &= uniform(ws, [(r, c) for r in eld for _, b, ys in grp for c in [b] + ys],
                  'electricity demand memo lines in the sector blocks')[0]
    for r, lab in ((B.R_CPI, 'infl'), (B.R_DEFL, 'defl')):
        ok &= uniform(ws, [(r, c) for _, b, ys in grp for c in [b] + ys], f'index row `{lab}`')[0]
    calc = [k for k, _v, _f, _s, kind, _m in B.POL if kind == 'calc']
    exact = ('cptraj', 'cp.t', 'cp.nom', 'ets.on', 'ets.vol', 'ets.imp', 'ets.vadj', 'ets.bce', 'ets.chg', 'ets.cap',
             'ets.se', 'ets.est', 'ets.p', 'ets.pe', 'ets.rf', 'scn', 'cp.exp', 'cpx', 'cp.shd', 'regadj',   # v4.16
             'exf.res')                                                                                    # v5.1
    exact += tuple(f'{v}.{k}' for v in ('po.on', 'po.n', 'po.sh', 'pof') for k, *_x in B.PHASEOUTS)   # v4.16
    for prefix in exact + ('fpr.', 'fb.', 'etsc.', 'etsb.', 'obr.', 'regc.', 'reg.', 'ssc.', 'ctr.', 'etr.', 'shpx.',
                           'csf.', 'pcf.', 'psf.', 'pros.'):
        keys = [k for k in calc if (k == prefix if prefix in exact else k.startswith(prefix))]
        assert keys, prefix
        ok &= uniform(ws, [(B.R_POL[k], c) for k in keys for _, b, ys in grp for c in [b] + ys[:-1]],
                      f'Section 1 `{prefix}*` plain')[0]
        g, f = uniform(ws, [(B.R_POL[k], ys[-1]) for k in keys for _, b, ys in grp3], f'Section 1 `{prefix}*` LAMBDA year')
        if g and not LAMBDA_CALL.search(f):
            log(f'  - Section 1 `{prefix}*` LAMBDA year: the formula calls no named LAMBDA FAIL')
        ok &= g and bool(LAMBDA_CALL.search(f))
    heads = list(B.SUB_HEAD.values())
    ok &= uniform(ws, [(h, c) for h in heads for _, b, ys in grp for c in [b] + ys], 'subsector heading totals')[0]
    for var in B.PW_VARS:                       # section 3 (power)
        rows = [r for r, v, *_ in B.PW_ROWS if v == var]
        if var in B.PW_DATA or var in B.PW_SUMS or var in B.PW_NOLAM:
            blocks = [(f'{B.BASE_YEAR}-{B.LAST_YEAR} (data, sum or look-ahead: one formula)', lambda b, ys: [b] + ys)]
        elif var == 'rppre':
            blocks = [(f'history {B.BASE_YEAR}-{B.LAST_HIST}', lambda b, ys: [b] + ys[:nh]),
                      (f'projection {B.LAST_HIST + 1}-{B.YEARS[-2]}', lambda b, ys: ys[nh:-1]), LAMY]
        elif var in B.PW_BASE:
            blocks = [('base year', lambda b, ys: [b]), (f'{B.YEARS[0]}-{B.YEARS[-2]}', lambda b, ys: ys[:-1]), LAMY]
        else:
            blocks = [(f'{B.BASE_YEAR}-{B.YEARS[-2]}', lambda b, ys: [b] + ys[:-1]), LAMY]
        good = True
        for label, cols in blocks:
            g, f = uniform(ws, [(r, c) for r in rows for _, b, ys in on(label) for c in cols(b, ys)],
                           f'power `{var}` {label}')
            good &= g and (label != LAMY[0] or bool(LAMBDA_CALL.search(f)))
            log(f'  - `{f[:150]}`')
            if g and label == LAMY[0] and not LAMBDA_CALL.search(f):           # v7.2: logged (NORMS 3b.4)
                log(f'  - power `{var}` LAMBDA year: the formula calls no named LAMBDA FAIL')
        good &= all(uniform(ws, [(r, CI(pc)) for r in rows], f'power `{var}` column {pc}')[0] for pc in B.PARAM_COLS)
        ok &= good
    bad_tr, n_tr = [], 0                         # v3.5: section 5b, one formula per row and column block
    for r, what, it in B.TR_LAYOUT:
        if what != 'row' or it['kind'] == 'par':
            continue
        n_tr += 1
        if it['kind'] == 'calc':
            blocks = [lambda b, ys: [b], lambda b, ys: ys[:-1], lambda b, ys: [ys[-1]]]
        elif it['base'] is not None:
            blocks = [lambda b, ys: [b], lambda b, ys: ys]
        else:
            blocks = [lambda b, ys: [b] + ys]
        forms = [{r1c1(ws.cell(r, c).value, r, c) for _, b, ys in (grp3 if it['kind'] == 'calc' and i == 2 else grp)
                  for c in cols(b, ys)} for i, cols in enumerate(blocks)]       # v4.16: LAMBDA year of group 3
        lam_need = it['kind'] == 'calc' and r in B.TR_LAMROWS          # v4.15: rows with a LAMBDA (TR_LAMROWS)
        if any(len(f) != 1 for f in forms) or (lam_need and not LAMBDA_CALL.search(next(iter(forms[-1])))):
            bad_tr.append(r)
    ok &= not bad_tr
    log(f'- section 5b (road engineer model): {n_tr} rows, one relative formula per row for the base year, 2023-2040 '
        f'and the LAMBDA year {B.LAST_YEAR} (which calls a named LAMBDA where the row has one) in every scenario group '
        f'{"OK" if not bad_tr else "FAIL " + str(bad_tr[:8])}')
    by_var = {}                                  # v5.1: section 6b, one relative formula per variable and column block
    for r, what, it in B.LK_LAYOUT:
        if what == 'row':
            by_var.setdefault(it['var'], []).append((r, it))
    bad_lk = []
    for var, items in by_var.items():
        rows, calc_ = [r for r, _it in items], items[0][1]['kind'] == 'calc'
        blocks = ([lambda b, ys: [b], lambda b, ys: ys[:-1], lambda b, ys: [ys[-1]]] if calc_
                  else [lambda b, ys: [b] + ys])
        forms = [{r1c1(ws.cell(r, c).value, r, c) for r in rows for _, b, ys in (grp3 if calc_ and i == 2 else grp)
                  for c in cols(b, ys)} for i, cols in enumerate(blocks)]
        pars = [{r1c1(ws.cell(r, CI(pc)).value, r, CI(pc)) for r in rows
                 if str(ws.cell(r, CI(pc)).value).startswith('=')} for pc in B.PARAM_COLS]   # v6.0: data by row
        pars = [p_ or {None} for p_ in pars]
        if any(len(f) != 1 for f in forms + pars) or (calc_ and not LAMBDA_CALL.search(next(iter(forms[-1])))):
            bad_lk.append(var)
    n_lk = len(by_var) == 12                     # v7.2: 12 since v6.x (was 7, failing silently: NORMS 3b.4)
    ok &= not bad_lk and n_lk
    log(f'- section 6b (residential leakage): {len(by_var)} variables (expected 12), one relative formula per variable '
        f'for the base year, 2023-2040 and the LAMBDA year {B.LAST_YEAR} (a named LAMBDA in test group '
        f'{B.LAMBDA_GROUP}), one per D:G column {"OK" if not bad_lk and n_lk else "FAIL " + str(bad_lk)}')
    lam = B.tab(wb, 'Lambdas')
    lam_rows = {r: f for r, (_r0, f) in lambda_table(lam).items()}   # v4.2: condensed sheet
    calc_rows = ({r for v in B.PVARS + B.VARS if v not in ('spf', 'gpi') for r, *_ in rows_of(v)}
                 | {B.R_POL[k] for k in calc}
                 | {r for r, v, *_ in B.PW_ROWS if v not in B.PW_DATA | B.PW_SUMS | B.PW_NOLAM}
                 | {B.R_GHG[k] for k in B.GHG_LAM}                        # v2.8: section 14
                 | {B.R_AP[k] for k in B.AP_LAM}                          # v2.9: section 15
                 | {B.R_GDPS[k] for k in B.GDP_LAM} | {B.R_GDP}           # v3.1: section 16, GDP growth
                 | B.TR_LAMROWS                                           # v3.5: section 5b
                 | B.LK_LAMROWS                                           # v5.1: section 6b
                 | set(B.R_PIX.values()) | {B.R_XR}                       # v3.10 memo, v3.13 exchange rate
                 | {B.R_FIS[k] for k in B.FIS_LAM}                        # v3.13: 12d shares of GDP
                 | {B.R_E13B[k] for k in B.E13B_LAM}                      # v3.14: 13b grid intensity, Kaya
                 | {B.R_CPR[k] for k in B.CPR_LAM}                        # v3.15: section 17
                 | {B.R_EXT[k] for k in B.EXT_LAM}                        # v3.16: 16b
                 | {B.R_WEL[k] for k in B.WEL_LAM})                       # v3.17: section 18
    good = set(lam_rows) == calc_rows and all(LAMBDA_CALL.search('=' + f) for f in lam_rows.values())
    ok &= good
    log(f'- sheet Lambdas: an optional LAMBDA formula for each of the {len(calc_rows)} calculated rows '
        f'({len(lam_rows)} listed, each calls a named LAMBDA) '
        f'{"OK" if good else "FAIL " + str(sorted(calc_rows ^ set(lam_rows))[:10])}')
    cd = ws.column_dimensions
    ycols = [L(c) for _, b, ys in grp for c in ys if 2030 <= B.year_of(c) <= 2039]
    grouped = list(B.COL_OUTLINE) + ycols                 # v3.9: column B stays visible
    visible = ['A', 'B', 'H'] + [L(c) for _, b, ys in grp for c in [b] + ys if not 2030 <= B.year_of(c) <= 2039]
    hidden = (all(cd[c].hidden and cd[c].outline_level == 1 for c in grouped)
              and not any(cd[c].hidden or (cd[c].outline_level or 0) > 0 for c in visible)
              and max((cd[c].outline_level or 0) for c in cd) == 1)
    log(f'- column groups, one level: C:G, I:K and 2030-2039 of each scenario ({len(ycols)} columns), rolled up; '
        f'other columns visible: {"OK" if hidden else "FAIL"}')
    test_ok = lambda v, code: v is None or (isinstance(v, str) and v.startswith(   # v4.3: spacer test formulas
        f'=IF({L(code + B.GW)}${B.R_SCEN}={L(code)}${B.R_SCEN},'))
    spacer = all(test_ok(ws.cell(r, ys[-1] + 1).value, code) for code, b, ys in grp for r in range(1, ws.max_row + 1)) \
        and all(code == B.COL_G0 + (g - 1) * B.GW for g, (code, b, ys) in enumerate(grp, 1)) and B.GW == B.NY + 2
    log(f'- spacer column after each scenario group (group width {B.GW}): blank or the group test formula '
        f'{"OK" if spacer else "FAIL"}')
    light = 'EEECE1'
    _c3, _b3, ys3 = B.group_cols(B.LAMBDA_GROUP)   # v4.15: the LAMBDA cells of test group 3 are light beige
    lcells = [(r, c) for r in calc_rows for c in ys3 if LAMBDA_CALL.search(str(ws.cell(r, c).value))]
    lam_ok = bool(lcells) and all(ws.cell(r, c).fill.start_color.rgb.endswith(light) for r, c in lcells)
    nh = B.LAST_HIST - B.BASE_YEAR
    hist_ok = all(ws.cell(r, c).fill.start_color.rgb.endswith(light) for v in ('sp', 'txo', 'rppre') for r, *_ in rows_of(v)
                  for _, b, ys in grp for c in ys[:nh]) \
        and all(ws.cell(r, b).fill.start_color.rgb.endswith('DDD9C4') for v in ('sp', 'txo', 'rppre') for r, *_ in rows_of(v)
                for _, b, ys in grp) \
        and not any(ws.cell(r, ys[nh]).fill.start_color.rgb.endswith(light) for v in ('sp', 'txo')
                    for r, *_ in rows_of(v) for _, b, ys in grp)
    log(f'- light beige (EEECE1): {len(lcells)} LAMBDA cells of test group {B.LAMBDA_GROUP} {"OK" if lam_ok else "FAIL"}; 2023-2024 history block of sp, txo, rppre '
        f'(base year darker beige, projection white) {"OK" if hist_ok else "FAIL"}')
    hidden = hidden and spacer and lam_ok and hist_ok
    return ok and hidden


def check_encoding():
    ok = True
    for name, (params, body) in B.LAMBDAS.items():
        xml = B.lambda_xml(name)
        bare = [p for p in params if re.search(rf'(?<![A-Za-z_.]){p}(?![A-Za-z_\d(])', xml)]
        good = not bare and xml.startswith('_xlfn.LAMBDA(')
        ok &= good
        log(f'- {name}: {len(params)} parameters, {xml.count("_xlpm.")} _xlpm. tokens, bare names {bare} '
            f'{"OK" if good else "FAIL"}')
    # v5.2: the formula texts of the LAMBDA library (sheet Lambdas, column C) must name sheets that exist: the tabs
    # merged in v3.6 (Inputs_power, Constants, ...) are gone, so a text naming one fails when pasted (bug M12)
    lam = B.tab(openpyxl.load_workbook(B.OUT, read_only=False), 'Lambdas')
    tmap = B.tab_map()
    gone = sorted(b for b, (t, _o, _h) in tmap.items() if t != b)
    stale = []
    for i in range(5, lam.max_row + 1):
        f, rows = lam.cell(i, 3).value, lam.cell(i, 4).value
        if isinstance(f, str):
            hit = [g for g in gone if re.search(rf"(?<![A-Za-z_\d])'?{re.escape(g)}'?!", f)]
            if hit:
                stale.append((rows, hit[0]))
    good = not stale
    ok &= good
    log(f'- sheet Lambdas: formula texts naming a sheet merged away (v3.6 tab merge): {len(stale)}'
        f'{" (Mitigation rows " + ", ".join(str(r) for r, _g in stale[:30]) + "; sheet " + stale[0][1] + ")" if stale else ""} '
        f'{"OK" if good else "FAIL"}')
    return ok


def mt_set(wsm, col, row_or_name, value):
    r = row_or_name if isinstance(row_or_name, int) else B.MT_NAMES[row_or_name]
    wsm.cell(r, col).value = value


def add_scenario(wb, src_g, dst_g, name, edits, mit_edits=None, mt_g=None):
    """Copy MTInputs column of src_g to dst_g's column (keeping the auto number) and the Mitigation group. v5.1: mt_g =
    the MTInputs column (scenario number) the pasted group reads when it differs from dst_g (a group pasted right of the
    LAMBDA test group, which repeats the scenario on its left)."""
    ws, wsm = wb['Mitigation'], wb['ScenarioDefinition']
    ms, md = B.MT_COL0 + src_g - 1, B.MT_COL0 + (mt_g or dst_g) - 1
    for r in range(1, B.MT_END + 1):
        v = wsm.cell(r, ms).value
        if isinstance(v, str) and v.startswith('='):
            v = Translator(v, origin=f'{L(ms)}{r}').translate_formula(f'{L(md)}{r}')
        wsm.cell(r, md).value = v
    wsm.cell(B.MT_ROW_SCEN, md).value = f'={L(md - 1)}{B.MT_ROW_SCEN}+1'
    wsm.cell(B.MT_ROW_NAME, md).value = name
    for k, v in edits.items():
        mt_set(wsm, md, k, v)
    s0, d0 = B.group_cols(src_g)[0], B.group_cols(dst_g)[0]
    for k in range(B.GW):
        for r in range(1, ws.max_row + 1):
            v = ws.cell(r, s0 + k).value
            if isinstance(v, str) and v.startswith('='):
                v = Translator(v, origin=f'{L(s0 + k)}{r}').translate_formula(f'{L(d0 + k)}{r}')
            ws.cell(r, d0 + k).value = v
    ws.cell(B.R_SCEN, d0).value = f'={L(d0 - B.GW)}{B.R_SCEN}+1'
    for key, v in (mit_edits or {}).items():          # typed Section-1 rows (benchmarks), every year column
        for c in [d0 + 1] + B.group_cols(dst_g)[2]:
            ws.cell(B.R_POL[key], c).value = v


LEGACY_CP = {2022: 0, 2023: 0, 2024: 0, 2025: 0, 2026: 0, 2027: 12.5, 2028: 25, 2029: 37.5, 2030: 50,
             2031: 62.5, 2032: 75, 2033: 87.5, 2034: 100, 2035: 112.5}   # legacy Mitigation row 8582
FPR_TEST = {140: 2027, 141: 2030, 150: 0.05, 164: 0.20, 146: 0.5, 160: 2.0,   # gasoline $/l, gas res $/GJ
            'ConsSubPha': True, 'YearConsSubPha': 2026, 'FFPhaseOut': 4, 'PrcContPha': True,   # v4.16 (LD18):
            'YearPrcContPha': 2027, 'PrcControlPhaseout': 5, 'ProdSubPh': True}               # phase-outs too
ETS_TEST = {'D_NewETS': 'Yes', 'D_ETSIntro': 2027, 'D_ETSOutro': 2035, 'D_ETSChangeRelStart': -0.02,
            'D_ETSChangeRelTarget': -0.15, 'D_ETSCapCont': 'Constant'}   # template coverage: power, mch, irn, nfm, cem
ETS_EQUIV = {**ETS_TEST, 'D_ETSPriceOverride': 'Yes', 'D_ETSVolatility': 'Zero',   # blank override: carbon price;
             'D_ETSCTRisk': 0, 'D_ETSAuctStart': 1, 'D_ETSAuctTarget': 1}         # adjustment 1; full auctioning (v4.15)
PRICE_TEST = {'IntEnerPricForeSource': 'IMF-WB*', 'IntEnerPricForecastAdjustment': 'High',
              'NomorReal': 'Nominal', 'MultipliersSource': 'Estimated', 'FmAdj': 'High',   # v4.15: country multipliers
              'ScenarioSelected': ' - Energy efficiency regulations'}   # v4.16 (LD9): shadow pricing, no carbon tax
EXEMPT_TEST = {'AlwaysExemptResLPGKer': 'Yes'}   # v5.1 (D16, I50): residential LPG and kerosene always exempted
FB_TEST = {'D_FeebateIntro': 2027, 'D_FeebateOutro': 2030, 'D_Feb_Level_Start_Trans': 10,
           'D_Feb_Level_Target_Trans': 50, 'D_Feb_Level_Start_Ind': 5, 'D_Feb_Level_Target_Ind': 25,
           67: True, 74: True, 75: True,                                  # feebate coverage: rod, mch, irn
           'MultipliersSource': 'Manual', 'FmAdj': 'Low', 'GDPStartYear': 2028}   # v4.15: Manual inputs, start year


TR_POL_SUB = {'TrSubYearPas': 2027, 'TrSubAmountPas': 5000, 'TrSubChgPas': 250}
TR_POL_DT = {'TrDtYearPas': 2027, 'TrDtStartPas': 0.01, 'TrDtTargetYearPas': 2030, 'TrDtTargetPas': 0.05}
TR_POL_FB = {'TrFbYearPas': 2027, 'TrFbRatePas': 100, 'TrFbYearFre': 2028, 'TrFbRateFre': 50, 'TrCsStartYear': 2026,
             'TrCsStartLevel': 0.2, 'TrCsTargetYear': 2030, 'TrCsTargetLevel': 0.5}
TR_TESTS = {  # v3.5: group -> (source group, name, MTInputs edits); engineer road model switched on
    11: (1, 'Test 11: engineer road model, no carbon price (copy of 1)', {'TrModel': 'Engineer'}),
    12: (2, 'Test 12: engineer road model, carbon tax (copy of 2)', {'TrModel': 'Engineer'}),
    13: (2, 'Test 13: as 12 + EV purchase subsidy', {'TrModel': 'Engineer', **TR_POL_SUB}),
    14: (2, 'Test 14: as 12 + distance tax', {'TrModel': 'Engineer', **TR_POL_DT}),
    15: (2, 'Test 15: as 12 + subsidy, distance tax, feebates, charging subsidy',
         {'TrModel': 'Engineer', **TR_POL_SUB, **TR_POL_DT, **TR_POL_FB})}


PB_ONLY = {'rpn', 'pnq', 'pctx', 'pets', 'pntx', 'pxcd', 'pvatn', 'pnce'}   # v5.0: weighted from the subsector rows
# of the sheet, checked by price_blocks (not recomputed by pair here)


def price_blocks(ws):
    """v4.1: recompute the new-policy rows of every section-2 price block from the subsector rows: the atp rows whose
    D is the block position, weights ener; returns (max relative difference, cells)."""
    num = lambda v: v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0.0
    off = lambda v: B.VOFF[v] - B.VOFF['atp']
    worst, n = 0.0, 0
    for pc, _l in B.PRICES:
        rows = [r for r, _s, _f in B.var_rows('atp') if num(ws.cell(r, 4).value) == B.PV_POS[pc]]
        for g, *_r in B.SCENARIOS:
            _, bg, yg = B.group_cols(g)
            for c in [bg] + yg[:-1]:
                v = lambda var, r: num(ws.cell(r + off(var), c).value)
                q = sum(v('ener', r) for r in rows)
                avg = lambda var: sum(v(var, r) * v('ener', r) for r in rows) / q if q else 0.0
                rpb = num(ws.cell(B.prow('rpb', pc), c).value)
                exp = {'pnq': q, 'pctx': avg('ctxnew'), 'pets': avg('ets'), 'pntx': avg('ntx'), 'pxcd': avg('xcpd'),
                       'rpn': avg('atp') if q else rpb}
                exp['pnce'] = exp['rpn'] - rpb
                wedge = sum(num(ws.cell(B.prow(w_, pc), c).value) for w_ in ('pcsw', 'ppcw'))   # v4.16 (own rows)
                exp['pvatn'] = exp['pnce'] - exp['pctx'] - exp['pets'] - exp['pntx'] - exp['pxcd'] - wedge
                for var, x in exp.items():
                    got = num(ws.cell(B.prow(var, pc), c).value)
                    worst, n = max(worst, abs(got - x) / max(1.0, abs(x))), n + 1
    return worst, n


PAV_METHOD = 'Legacy*'                  # v4.15 (I31): Settings C54 default
LEG_SUBS = {'qr': ['res'], 'qi': ['mch', 'irn', 'nfm', 'mac', 'cem', 'omn', 'cst', 'ftr']}   # legacy F5b weights


def legacy_avg(ws, f, c, cq, num, parts=False):
    """v4.15 (I31): legacy F5b average price of fuel f in column c with the quantities of column cq (scenario 1):
    coal, gas = residential, industry and power prices (section 2 blocks; power: pre-policy price + policy cost per GJ)
    weighted by residential, 8-industry and power fuel use; oil products: the price of the .all block."""
    cell = lambda r, c_: num(ws.cell(r, c_).value)
    if f in B.PAVL_OIL:
        return cell(B.prow('rpn', f + '.all'), c)
    fi = [x[0] for x in B.FUELS].index(f)
    q = {k: sum(cell(B.SUB_HEAD[s_] + B.VOFF['ener'] + fi, cq) for s_ in subs) for k, subs in LEG_SUBS.items()}
    q['qp'] = cell(B.R_PW[('pe', f)], cq)
    pe = cell(B.R_PW[('pe', f)], c)
    pp = cell(B.prow('rpb', f + '.pow'), c) + (cell(B.R_PW[('gen', f)], c) * K['MWyMkWh'] * cell(B.R_PW[('ccp', f)], c)
                                               / (pe * B.PJ_PER_KTOE) if pe else 0.0)
    if parts:
        return {**q, 'pp': pp}
    tq = q['qr'] + q['qi'] + q['qp']
    if not tq:
        return cell(B.R_PIX[('pav.uv', f)], c)
    return (cell(B.prow('rpn', f + '.res'), c) * q['qr'] + cell(B.prow('rpn', f + '.ind'), c) * q['qi']
            + pp * q['qp']) / tq


TRADE_GJ = {'oil': (['oop', 'gso', 'die', 'ker', 'lpg', 'jfu'], 6.12), 'nga': (['nga'], 1.055056),
            'coa': (['coa'], 25.14)}   # independent copy: Balances fuels and GJ per unit of the price (legacy G727:G729)


def trade_balance():
    """v5.2: energy trade balance (exports - imports, USD bn real) by group and year, as legacy rows 741-743 with bug
    L51 fixed (v4.6: coal valued at the coal price, legacy at the crude oil price; oil and gas equal the legacy values
    of gdp_level.csv): base-year net imports (legacy Balances) x the international price of the scenario-1 source
    (prices_int.csv, real with the US GDP deflator, no High/Low adjustment)."""
    tpl = mt_used()
    src = str(tpl[B.MT_NAMES['IntEnerPricForeSource']]).replace('*', '')
    ry = tpl[B.MT_NAMES['ResultsYear']]
    yrs = list(range(2021, 2046))
    us = {r['key']: series(r, yrs) for r in read('weo_us.csv')}
    dfl = {y: us['USA|ngdp_d'][ry] / us['USA|ngdp_d'][y] for y in us['USA|ngdp_d']}
    pint = {r['key']: series(r, yrs) for r in read('prices_int.csv')}
    gas = {'Global': 'glo', 'LNG': 'lng', 'Europe': 'eur', 'North Am': 'nam'}[
        next(r['gas_market'] for r in read('price_assumptions.csv') if r['country_name'] == NAME)]
    bal = {r['flow_code']: r for r in read('legacy_Balances.csv') if r['country_code'] == ISO}
    out = {}
    for g, (fs, gj) in TRADE_GJ.items():
        q = -sum(float(bal['imports'][f] or 0) + float(bal['exports'][f] or 0) for f in fs)    # net imports, ktoe
        comm = f'nga.{gas}' if g == 'nga' else g
        out[g] = {y: q * B.PJ_PER_KTOE / 1000 * pint[f"{src}|{comm}"][y] * dfl[y] / gj for y in [B.BASE_YEAR] + B.YEARS}
    return out


def check_results_memos(ws):
    """v3.10 onwards: independent Python recomputation of the results memos and sections added from legacy's
    post-processing (NORMS 3f rule 3), in every scenario group against scenario 1. v3.10: section 2 price indices."""
    num = lambda v: v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0.0
    d = B.VOFF['ener'] - B.VOFF['atp']
    _, b1, y1 = B.group_cols(1)
    worst, n = 0.0, 0
    for g, *_r in B.SCENARIOS:
        _, bg, yg = B.group_cols(g)
        for f in [x[0] for x in B.FUELS]:
            rows = [r for r, _s, ff in B.var_rows('atp') if ff == f]
            for cA, cB in zip([b1] + y1[:-1], [bg] + yg[:-1]):
                sp1 = sum(num(ws.cell(r, cA).value) * num(ws.cell(r + d, cA).value) for r in rows)
                sp = sum(num(ws.cell(r, cB).value) * num(ws.cell(r + d, cB).value) for r in rows)
                spr = sum(num(ws.cell(r, cB).value) * num(ws.cell(r + d, cA).value) for r in rows)
                sp0 = sum(num(ws.cell(r, cB).value) * num(ws.cell(r + d, b1).value) for r in rows)
                q = sum(num(ws.cell(r + d, cB).value) for r in rows)
                q1 = sum(num(ws.cell(r + d, cA).value) for r in rows)
                sp1b = sum(num(ws.cell(r, b1).value) * num(ws.cell(r + d, b1).value) for r in rows)
                las = spr / sp1 if sp1 else 0.0
                uv, uv1 = (sp / q if q else 0.0), (sp1 / q1 if q1 else 0.0)
                exp = {'pav.sp': sp, 'pav.q': q, 'pav.uv': uv, 'pav.spr': spr, 'pav.las': las, 'pav.sp0': sp0,
                       'pav.time': sp0 / sp1b if sp1b else 0.0, 'pav.mix': uv / uv1 / las if uv1 * las else 0.0}
                leg = lambda c_, cq: legacy_avg(ws, f, c_, cq, num)          # v4.15 (I31)
                lg, lg1 = (leg(cB, cA), leg(cA, cA)) if f in B.PAVL_FUELS + B.PAVL_OIL else (0.0, 0.0)   # v5.2: jfu,
                # bio have no legacy average (and no power type)
                lidx = (lg / lg1 if lg1 else 0.0) if f in B.PAVL_FUELS + B.PAVL_OIL else las
                exp.update({'pav.leg': lg if f in B.PAVL_FUELS + B.PAVL_OIL else uv, 'pav.lidx': lidx,
                            'pav.idx': lidx if PAV_METHOD.startswith('Leg') else las})
                if f in B.PAVL_FUELS:
                    exp.update({f'pavl.{k}': v_ for k, v_ in legacy_avg(ws, f, cB, cA, num, parts=True).items()})
                for v, x in exp.items():
                    got = num(ws.cell(B.R_PIX[(v, f)], cB).value)
                    worst, n = max(worst, abs(got - x) / max(1.0, abs(x))), n + 1
    good = worst < 1e-9
    log(f'- section 2 price indices (unit value, Laspeyres, time index, mix) vs Python, every scenario group and fuel: '
        f'{n} cells, max relative diff {worst:.3g} {"OK" if good else "FAIL"}')
    wb_, nb_ = price_blocks(ws)                        # v4.1: new taxes and subsidies by price block
    good &= wb_ < 1e-9
    log(f'- section 2 price blocks: full retail price, weights and new taxes and subsidies (fuel-use weighted over the '
        f'subsectors of the block) vs Python, every scenario group: {nb_} cells, max relative diff {wb_:.3g} '
        f'{"OK" if wb_ < 1e-9 else "FAIL"}')
    # v3.13: 12d fiscal reports, from the subsector rows (columns A, B) and section 3 rows
    w2, n2 = 0.0, 0
    cell = lambda r, c: num(ws.cell(r, c).value)
    s_rows = [(r, ws.cell(r, 1).value, ws.cell(r, 2).value) for r in range(B.S_FIRST, B.S_LAST + 1)]
    pw = lambda v, m, c: cell(B.R_PW[(v, m)], c)
    mem = lambda v: B.PW_MEMBERS[B.PW_KIND[v]]
    for g, *_r in B.SCENARIOS:
        _, bg, yg = B.group_cols(g)
        for k, c in enumerate([bg] + yg):
            c1 = ([b1] + y1)[k]
            gdp = cell(B.R_GDPUSD, c) * 1000
            exp = {f'rfu.{f}': sum(cell(r, c) for r, v, ff in s_rows if v in ('rtx', 'rsub', 'rnew', 'rsr') and ff == f)
                   for f, *_x in B.FUELS}
            exp['rfu.ecy'] = sum(pw(v, m, c) for v in ('rvat', 'rgap', 'rnvat') for m in mem(v))
            exp.update({f'rfg.{t}': sum(pw(v, t, c) for v in ('prtx', 'prxc', 'prsub', 'prnew')) for t in B.RFG_TECH})
            tot = sum(exp.values())
            exp['rfu.chk'] = abs(tot - cell(B.R_REV['rnet.all'], c) - cell(B.R_REV['rnew.all'], c)
                                 - cell(B.R_REV['rsr.all'], c))
            exp['rbe'] = cell(B.R_REV['rnet.all'], c) - cell(B.R_REV['rnet.all'], c1)
            src = {'tot': 'rtot.all', 'net': 'rnet.all', 'sub': 'rsub.all', 'new': 'rnew.all', 'chg': 'rtot.chg'}
            exp.update({f'rpct.{q}': cell(B.R_REV[v], c) / gdp for q, v in src.items()})
            exp['rpct.be'] = exp['rbe'] / gdp
            exp['xr'] = cell(B.R_GDPLCU, c) / cell(B.R_GDPUSD, c)
            for key, x in exp.items():
                got = cell(B.R_XR if key == 'xr' else B.R_FIS[key], c)
                w2, n2 = max(w2, abs(got - x) / max(1.0, abs(x))), n2 + 1
            w2 = max(w2, exp['rfu.chk'] / max(1.0, tot))
    ok2 = w2 < 1e-9
    # v3.14: 11b, 13b, 14b from their source rows
    w3, n3, at3 = 0.0, 0, None
    lv11 = {**{f: B.R_FUEL0 + i for i, (f, *_x) in enumerate(B.FUELS)}, **{g: B.SEC_SUM[g] for _n, g, _t in B.SECTIONS},
            'pow': B.R_EPOW, 'all': B.R_TOTAL}
    _, b1_, y1_ = B.group_cols(1)
    for g, *_r in B.SCENARIOS:
        _, bg, yg = B.group_cols(g)
        for k, c in enumerate([bg] + yg):
            c1 = ([b1_] + y1_)[k]
            exp = {}
            for key, var, fu, sec in [x for _h, rr in B.E11B_BLOCKS for x in rr]:
                lv = lv11[fu if fu != 'all' else sec]
                ch = cell(lv, c) - cell(lv, c1)
                lvl = cell(lv, c)
                exp[('11', key)] = ch if var == 'echg' else (0.0 if lvl - ch == 0 else ch / (lvl - ch))
            for key, var, fu, sec in B.E13B_BLOCKS[0][1]:
                lv = B.R_EMI[f'co2.f.{fu}' if fu != 'all' else f'co2.{sec}']
                exp[('13', key)] = cell(lv, c) - cell(lv, c1)
            gt = cell(B.R_PW[('gtot', '')], c) * 8760
            exp[('13', 'co2.grid')] = cell(B.R_EMI['co2.pow'], c) * 1e6 / gt if gt else 0.0
            tp = lambda cc: cell(B.R_TOTAL, cc) + sum(cell(B.R_PW[('pe', t)], cc) for t in B.PRIM_ELEC)   # v3.18
            pop, gdp, en, co2 = (cell(B.R_GHG['pop'], c) / 1000, cell(B.R_GDPUSD, c), tp(c),
                                 cell(B.R_GHG['ghg.g.co2'], c))
            pop0, gdp0, en0, co20 = (cell(B.R_GHG['pop'], b1_) / 1000, cell(B.R_GDPUSD, b1_), tp(b1_),
                                     cell(B.R_GHG['ghg.g.co2'], b1_))
            kay = {'pop': pop, 'gpc': gdp / pop, 'tpes': en, 'ei': en / gdp, 'ci': co2 * 1000 / en}
            kay0 = {'pop': pop0, 'gpc': gdp0 / pop0, 'tpes': en0, 'ei': en0 / gdp0, 'ci': co20 * 1000 / en0}
            exp.update({('13', f'kaya.{q}'): v for q, v in kay.items()})
            idx = {q: kay[q] / kay0[q] for q in kay if q != 'tpes'}
            idx.update({'gdp': gdp / gdp0, 'co2': co2 / co20})
            idx['chk'] = idx['pop'] * idx['gpc'] * idx['ei'] * idx['ci']
            exp.update({('13', f'kidx.{q}'): v for q, v in idx.items()})
            w3 = max(w3, abs(idx['chk'] - idx['co2']))
            for key, var, fu, sec in B.E14B_BLOCKS[0][1]:
                lv = B.R_GHG[f'ghg.c.{sec}' if fu == 'all' else f'ghg.g.{fu}']
                exp[('14', key)] = cell(lv, c) - cell(lv, c1)
            exp[('14', 'ghg.enrp')] = cell(B.R_GHG['ghg.c.enr'], c) + cell(B.R_AP['apf.all'], c)
            R = {'11': B.R_E11B, '13': B.R_E13B, '14': B.R_E14B}
            for (sx, key), x in exp.items():
                got = cell(R[sx][key], c)
                d3 = abs(got - x) / max(1.0, abs(x))
                if d3 > w3:
                    w3, at3 = d3, (key, c, got, x)
                n3 += 1
    ok3 = w3 < 1e-9
    # v3.15: section 17 from its source rows (independent of the formulas: switches, rates, CO2 by fuel)
    w4, n4, at4 = 0.0, 0, None
    fl = lambda r, c: float(bool(ws.cell(r, c).value)) if isinstance(ws.cell(r, c).value, bool) else cell(r, c)
    sd = lambda a, b: a / b if b else 0.0
    for g, *_r in B.SCENARIOS:
        _, bg, yg = B.group_cols(g)
        for c in [bg] + yg:
            co2 = cell(B.R_EMI['co2.all'], c)
            exp = {}
            for f in B.CPI_FUELS:
                rev = cell(B.R_FIS[f'rfu.{f}'], c) + (cell(B.R_FIS[f'rfg.{f}'], c) if f in B.RFG_TECH else 0.0)
                exp[f'cpi.{f}'] = sd(rev, cell(B.R_EMI[f'co2.f.{f}'], c))
            rev = sum(cell(B.R_FIS[f'rfu.{f}'], c) for f in B.CPI_FUELS) + sum(
                cell(B.R_FIS[f'rfg.{t}'], c) for t in B.RFG_TECH if t != 'bio')
            exp['cpi.all'] = sd(rev, co2)
            exp['ecr'] = sd(cell(B.R_REV['rnet.all'], c) + cell(B.R_REV['rnew.all'], c) + cell(B.R_REV['rsr.all'], c),
                            co2)
            cov = {}
            for cs in B.COV_SECTORS:
                on = cell(B.R_POL[f'ctr.{cs}'], c) > 0
                if cs == 'pow':
                    v = sum(cell(B.R_PW[('co2', t)], c) * fl(B.R_POL[f'fc.{t}'], c) for t in B.RFG_TECH if t != 'bio')
                else:
                    h = B.SUB_HEAD[cs] + B.VOFF['co2']
                    v = sum(cell(h + i, c) * fl(B.R_POL[f'fc.{f}'], c) for i, (f, *_x) in enumerate(B.FUELS))
                cov[cs] = v * on
                exp[f'covct.{cs}'] = cov[cs]
            grp = {x[0]: x[2] for x in B.SUBSECTORS}
            grp['pow'] = 'pow'
            for gg in B.CHG_GROUPS:
                exp[f'cov.ct.{gg}'] = sd(sum(v for cs, v in cov.items() if grp[cs] == gg), co2)
            exp['cov.ct.all'] = sd(sum(cov.values()), co2)
            exp['cov.ets'] = sd(cell(B.R_EMI['co2.ets'], c), co2)
            exp['cov.all'] = exp['cov.ct.all'] + exp['cov.ets']
            exp['cpeff'] = cell(B.R_POL['cptraj'], c) * exp['cov.ct.all']
            for key, x in exp.items():
                got = cell(B.R_CPR[key], c)
                d4 = abs(got - x) / max(1.0, abs(x))
                if d4 > w4:
                    w4, at4 = d4, (key, c, got, x)
                n4 += 1
    ok4 = w4 < 1e-9
    # v3.16: 16b from section 11b, the supply prices and the data
    w5, n5, at5 = 0.0, 0, None
    dat = {r['key']: r for r in read('gdp_level.csv')}
    tb = trade_balance()                               # v5.2: L51 fixed (coal at the coal price), from the CSVs
    for g, *_r in B.SCENARIOS:
        _, bg, yg = B.group_cols(g)
        for c in [bg] + yg:
            y = B.year_of(c)
            exp = {}
            for f in B.CPI_FUELS:
                sh = float(dat[f'{ISO}|ts_{B.XGROUP[f]}'][str(y)])
                sp = cell(B.prow('sp', B.XPRICE.get(f, f + '.all')), c)
                exp[f'xnim.{f}'] = cell(B.R_E11B[f'echg.f.{f}'], c) * B.PJ_PER_KTOE * sp * sh / 1000
            for gg in B.XG:
                exp[f'xnim.g.{gg}'] = sum(v for k, v in exp.items() if k.split('.')[1] in B.XGROUP
                                          and B.XGROUP[k.split('.')[1]] == gg)
            exp['xnim.all'] = sum(exp[f'xnim.g.{gg}'] for gg in B.XG)
            for gg in B.XG:
                exp[f'xtb.{gg}'] = tb[gg][y]
            exp['xtb.all'] = sum(exp[f'xtb.{gg}'] for gg in B.XG)
            exp['xtbp'] = exp['xtb.all'] - exp['xnim.all']
            gdp = cell(B.R_GDPUSD, c)
            exp['xtb.pct'] = exp['xtbp'] / gdp
            exp['xnim.pct'] = exp['xnim.all'] / gdp
            for key, x in exp.items():
                got = cell(B.R_EXT[key], c)
                d5 = abs(got - x) / max(1.0, abs(x))
                if d5 > w5:
                    w5, at5 = d5, (key, c, got, x)
                n5 += 1
    ok5 = w5 < 1e-9
    # v3.17: section 18 from the settings, the data and the source rows
    w6, n6, at6 = 0.0, 0, None
    st = ws.parent['Settings']
    sv = lambda r: st.cell(r, 3).value
    tgt, tyr, gr, nsrc, gsrc, rho, eta, epa = (sv(r) for r in range(33, 41))
    rk = {r['code']: float(r['central_usd_per_tco2']) for r in read('scc.csv')}
    rho = int(rho) if isinstance(rho, float) and rho.is_integer() else rho
    if '%' in str(rho):                                  # v6.0: v5.6 Settings C38-C39 hold the legacy texts (C41-C42)
        rho = str(rho)[0]
    if '%' in str(eta):
        eta = str(eta).split('%')[0].replace('.', 'p')
    mi_ = ws.parent['Manual inputs']                    # v5.2 (L103 fixed): the Manual inputs SCC block, rows 236-240:
    g0, gr_m = float(mi_['F238'].value), float(mi_['F239'].value)   # 2025 level (column M), real growth back and forward
    man = {str(y): g0 * ((1 + gr_m) ** (y - 2025) if y >= 2025 else (1 - gr_m) ** (2025 - y)) for y in range(2022, 2045)}
    fu11 = {**{f: B.R_FUEL0 + i for i, (f, *_x) in enumerate(B.FUELS)}, 'ecy': B.R_ELD['all']}
    for g, *_r in B.SCENARIOS:
        _, bg, yg = B.group_cols(g)
        for k_, c in enumerate([bg] + yg):
            c1 = ([b1_] + y1_)[k_]
            y = B.year_of(c)
            ex = {'scc.tgt': tgt * (1 + gr) ** (y - tyr),
                  'scc.rkn': rk[f'{ISO.lower()}.{rho}.{eta}'] * (1 + gr) ** (y - B.BASE_YEAR),
                  'scc.rkg': rk[f'wld.{rho}.{eta}'] * (1 + gr) ** (y - B.BASE_YEAR),
                  'scc.man': man[str(y)], 'scc.epa': epa * (1 + gr) ** (y - B.BASE_YEAR)}
            pick = lambda src, r_: ex[{'T': 'scc.tgt', 'R': r_, 'M': 'scc.man', 'U': 'scc.epa', 'E': 'scc.epa'}[str(src)[:1]]]   # v5.6 texts
            ex['scc.nat'], ex['scc.glo'] = pick(nsrc, 'scc.rkn'), pick(gsrc, 'scc.rkg')
            ghg_c, ghg_1 = cell(B.R_GHG['ghg.all'], c), cell(B.R_GHG['ghg.all'], c1)
            for q in ('nat', 'glo'):
                ex[f'dmg.{q}'] = ex[f'scc.{q}'] * ghg_c / 1000
                ex[f'wcli.{q}'] = cell(B.R_WEL[f'scc.{q}'], c1) * ghg_1 / 1000 - ex[f'dmg.{q}']
            eff = 0.0
            for f in B.WDG_FUELS:
                rev = lambda cc: (cell(B.R_FIS['rfu.ecy'], cc) if f == 'ecy' else cell(B.R_FIS[f'rfu.{f}'], cc)
                                  + (cell(B.R_FIS[f'rfg.{f}'], cc) if f in B.RFG_TECH else 0.0))
                q1, q0 = cell(fu11[f], c), cell(fu11[f], c1)
                w1, w0 = (rev(c) / q1 if q1 else 0.0), (rev(c1) / q0 if q0 else 0.0)
                ex[f'wdg.{f}'] = w1
                ex[f'eff.{f}'] = -(w1 + w0) / 2 * (q1 - q0) / 1000
                eff += ex[f'eff.{f}']
            ex['eff.all'] = eff
            mfc = 0.0
            for j, *_x in B.CH4_SOURCES:
                ab = B.R_GHG[f'ch4.abt.{j}']
                a_, b_, f_ = ws.cell(ab, 4).value or 0.0, ws.cell(ab, 5).value or 0.0, ws.cell(ab, 6).value or 0.0
                fee = cell(B.R_POL['mfee'], c) * f_ * MFEE_ON[j]          # v4.12 (LD46)
                ex[f'mfp.{j}'] = 0.0 if a_ == 0 else min(fee, (1 / a_) ** (1 / b_))
                src = ws.cell(B.R_GHG[f'ch4.src.{j}'], 5).value or 0.0
                base = 0.0 if src == 0 else ws.cell(B.R_GHG[f'ch4.em.{j}'], 4).value * cell(B.R_GHG[f'ch4.act.{j}'], c) / src
                ex[f'mfc.{j}'] = base * cell(ab, c) * ex[f'mfp.{j}'] * b_ / (1 + b_) / 1e6
                mfc += ex[f'mfc.{j}']
            ex['mfc.all'] = mfc
            gdp = cell(B.R_GDPUSD, c)
            ex['wel.usd'] = ex['wcli.nat'] - eff - mfc
            ex['wel.pct'], ex['wel.cli'], ex['wel.eff'] = ex['wel.usd'] / gdp, ex['wcli.nat'] / gdp, (eff + mfc) / gdp
            for key, x in ex.items():
                got = cell(B.R_WEL[key], c)
                d6 = abs(got - x) / max(1.0, abs(x))
                if d6 > w6:
                    w6, at6 = d6, (key, c, got, x)
                n6 += 1
    ok6 = w6 < 1e-9
    log(f'- section 18 welfare, climate part (SCC options, damages, efficiency costs of energy and of the methane fee, '
        f'summary) vs Python, every scenario group: {n6} cells, max relative diff {w6:.3g} (at {at6}) '
        f'{"OK" if ok6 else "FAIL"}')
    log(f'- 16b external balance (change in net energy imports, trade balance, % of GDP) vs Python, every scenario '
        f'group: {n5} cells, max relative diff {w5:.3g} (at {at5}) {"OK" if ok5 else "FAIL"}')
    log(f'- section 17 carbon pricing (implicit carbon price, effective carbon rate and tax, CO2 covered, coverage) '
        f'vs Python, every scenario group: {n4} cells, max relative diff {w4:.3g} (at {at4}) {"OK" if ok4 else "FAIL"}')
    log(f'- 11b, 13b, 14b (changes, % changes, grid intensity, Kaya incl. its identity, energy GHGs with forcing) vs '
        f'Python, every scenario group: {n3} cells, max relative diff {w3:.3g} (at {at3}) {"OK" if ok3 else "FAIL"}')
    log(f'- 12d fiscal reports (revenue by fuel = rnet + rnew, % of GDP, base erosion) and exchange rate vs Python, '
        f'every scenario group: {n2} cells, max relative diff {w2:.3g} {"OK" if ok2 else "FAIL"}')
    return good and ok2 and ok3 and ok4 and ok5 and ok6


def check_transport_scenarios(ws):
    """v3.5: the engineer road model switched on (TrModel = Engineer) in copied groups, with and without policies:
    every section-5b row vs the engine and the whole model vs the Python recomputation (road fuels and road
    electricity from the engine); road fuel use = section 5b; policy directions."""
    ok = True
    for g, (src, name, edits) in TR_TESTS.items():
        mt = scenario_mt(src)
        for k, v in edits.items():
            mt[B.MT_NAMES[k]] = v
        mt['scen'] = g
        exp = recompute(mt)
        ok &= check_transport(ws, g, exp, f'scenario {g} ({name[9:]})')
        ok &= compare(ws, g, exp, f'scenario {g} vs Python (engineer road model on)')
    h = B.SUB_HEAD['rod'] + B.VOFF['ener']
    _, b11, y11 = B.group_cols(11)
    d = max(abs(ws.cell(h + i, c).value - ws.cell(B.R_TR[k], c).value) for c in [b11] + y11[:-1]
            for i, k in ((2, 5325), (3, 5326), (4, 5327), (1, 5328), (7, 'trbio')))
    d_el = max(abs(ws.cell(B.R_PW[('dem', 'rod')], c).value - ws.cell(B.R_TR[5331], c).value) for c in y11[:-1])
    good = d < 1e-9 and d_el < 1e-9
    ok &= good
    log(f'- scenario 11: road gasoline, diesel, LPG, gas and biofuels of section 5 = section 5b (max abs diff '
        f'{d:.2g} ktoe); road electricity demand of section 3 H = section 5b from 2023 ({d_el:.2g}) '
        f'{"OK" if good else "FAIL"}')
    yc = lambda g, y: B.group_cols(g)[1] + (y - B.BASE_YEAR)
    v = lambda g, k, y: ws.cell(B.R_TR[k], yc(g, y)).value
    fuel = lambda g, y: sum(v(g, k, y) for k in (5325, 5326, 5327, 5328))
    tests = [('carbon tax lowers road fuel use (12 vs 11, 2035)', fuel(12, 2035) < fuel(11, 2035),
              f'{fuel(11, 2035):,.0f} -> {fuel(12, 2035):,.0f} ktoe'),
             ('EV purchase subsidy raises the passenger EV sales share (13 vs 12, 2030)',
              v(13, 4828, 2030) > v(12, 4828, 2030), f'{v(12, 4828, 2030):.4f} -> {v(13, 4828, 2030):.4f}'),
             ('distance tax lowers passenger distance driven (14 vs 12, 2035)', v(14, 5333, 2035) < v(12, 5333, 2035),
              f'{v(12, 5333, 2035):.2f} -> {v(14, 5333, 2035):.2f} bln km'),
             ('policies of 15 lower road fuel use (15 vs 12, 2035)', fuel(15, 2035) < fuel(12, 2035),
              f'{fuel(12, 2035):,.0f} -> {fuel(15, 2035):,.0f} ktoe')]
    for lab, good, txt in tests:
        ok &= good
        log(f'- direction: {lab}: {txt} {"OK" if good else "FAIL"}')
    return ok


def compare_res(ws, g, mt, label):
    """v5.1: group g against _recompute_once with the sheet's own GDP growth (row R_GDP), judged on the residential block
    and section 6b: the GDP feedback carries the known differences of the Python power reference into every fuel row."""
    _, base, years = B.group_cols(g)
    gdp = [ws.cell(B.R_GDP, c).value for c in [base] + years]
    return compare(ws, g, _recompute_once(mt, gdp=gdp), label + " (Python with the sheet's GDP growth)",
                   focus=res_focus())


def res_focus():
    """v5.1: rows of the residential subsector block (prices, fuel use, CO2, CH4, revenues), section 6b and its summary
    (the totals include power, whose Python reference has known differences)."""
    h = B.SUB_HEAD['res']
    return set(range(h, h + B.SB)) | set(B.R_LK.values()) | {B.R_LKSUM}


def check_exempt(ws, g):
    """v5.1 (D16, I50): group g = scenario 2 ($20 carbon price) with AlwaysExemptResLPGKer = Yes. Residential LPG and
    kerosene: no new carbon tax, ETS or excise, so the after-tax price equals scenario 1 and the new-policy revenue,
    excise revenue and VAT on the new policies are 0; residential gas keeps the carbon tax."""
    (_c1, b1, y1), (_c2, b2, y2), (_c, bg, yg) = B.group_cols(1), B.group_cols(2), B.group_cols(g)
    h = B.SUB_HEAD['res']
    row = lambda v, f: h + B.VOFF[v] + [x[0] for x in B.FUELS].index(f)
    d_atp = max(abs(ws.cell(row('atp', f), x).value - ws.cell(row('atp', f), y).value)
                for f in ('lpg', 'ker') for x, y in zip([b1] + y1, [bg] + yg))
    newp = max(abs(ws.cell(row(v, f), c).value) for v in ('ctxnew', 'ets', 'ntx', 'nce', 'rnew', 'rex')
               for f in ('lpg', 'ker') for c in [bg] + yg)
    per = lambda r_v, f, c: (ws.cell(row(r_v, f), c).value / ws.cell(row('ener', f), c).value
                             if ws.cell(row('ener', f), c).value else 0.0)        # per ktoe
    d_rvt = max(abs(per('rvt', f, x) - per('rvt', f, y)) for f in ('lpg', 'ker') for x, y in zip(y1, yg))
    k27 = 2027 - B.BASE_YEAR
    lpg2, nga = ws.cell(row('rnew', 'lpg'), y2[k27 - 1]).value, ws.cell(row('ctxnew', 'nga'), yg[k27 - 1]).value
    good = d_atp < TOL and newp < TOL and d_rvt < 1e-6 and lpg2 > 0 and nga > 0
    log(f'- scenario {g} (carbon price $20, AlwaysExemptResLPGKer = Yes): residential LPG and kerosene after-tax price = '
        f'scenario 1 (max abs diff {d_atp:.2g}); their new carbon tax, ETS, excise, total new policy, new-policy and '
        f'excise revenue 0 (max abs {newp:.2g}); VAT revenue per ktoe = scenario 1 ({d_rvt:.2g}); 2027 residential LPG '
        f'new-policy revenue in scenario 2 {lpg2:.1f} USD m; residential gas carbon tax kept ({nga:.3f} $/GJ) '
        f'{"OK" if good else "FAIL"}')
    return good


def check_exempt_scenario():
    """v5.1 (D16, I50): a group pasted right of the LAMBDA test group runs scenario 3 = scenario 2 ($20) with
    AlwaysExemptResLPGKer = Yes (own small workbook: the 15-group scenario workbook is at the LibreOffice time limit);
    against the Python recomputation (residential rows) and the properties of check_exempt."""
    wb = openpyxl.load_workbook(B.OUT)
    add_scenario(wb, 2, 3, 'Test: carbon price $20, residential LPG and kerosene exempt', EXEMPT_TEST)   # v7.0: group 3
    ws = recalc_wb(variant(wb, 'expand'))['Mitigation']
    mt3 = scenario_mt(2)
    mt3[B.MT_NAMES['AlwaysExemptResLPGKer']] = 'Yes'
    ok = compare_res(ws, 3, mt3, 'exemption, group 3 (scenario 3 = 2 + residential LPG/kerosene exempt) vs Python')
    return check_exempt(ws, 3) and ok


def check_leakage():
    """v5.1 (D9): BiomassLeakage = Yes (global: MTInputs scenario-1 column, Settings C59). Scenarios 1, 2 ($20) and a
    group pasted right of the LAMBDA test group running scenario 3 = scenario 2 with AlwaysExemptResLPGKer = Yes, against
    the Python recomputation; the LAMBDA test group (LAMBDA bodies expanded) against group 2 on the section-6b rows and
    residential fuel use; useful energy conserved (sum of efficiency x cumulative change = 0); an exempt fuel does not
    leak; the 2027 effect in the $20 scenario."""
    wb = openpyxl.load_workbook(B.OUT)
    mt_set(wb['ScenarioDefinition'], B.MT_COL0, 'BiomassLeakage', 'Yes')
    add_scenario(wb, 2, 3, 'Test: leakage, carbon price $20, residential LPG and kerosene exempt', EXEMPT_TEST)
    GLOBAL_MT['BiomassLeakage'] = 'Yes'
    try:
        ws = recalc_wb(variant(wb, 'expand'))['Mitigation']
        mt3 = scenario_mt(2)
        mt3[B.MT_NAMES['AlwaysExemptResLPGKer']] = 'Yes'
        ok = True
        for g, mt_, lab in ((1, scenario_mt(1), 'leakage on, scenario 1 vs Python'),
                            (2, scenario_mt(2), 'leakage on, scenario 2 ($20) vs Python'),
                            (3, mt3, 'leakage on, group 3 (scenario 3 = 2 + residential LPG/kerosene exempt) vs Python')):
            ok &= compare_res(ws, g, mt_, lab)
    finally:
        GLOBAL_MT.clear()
    (_c2, b2, y2), (_c3, b3, y3), (_c4, b4, y4) = (B.group_cols(g) for g in (2, B.LAMBDA_GROUP, 3))   # v7.0: group 3
    h = B.SUB_HEAD['res']
    fi = [x[0] for x in B.FUELS].index
    rows = [B.R_LK[it['key']] for it in B.LK_ROWS if it['kind'] != 'head'] + [B.R_LKSUM]
    rows += [h + B.VOFF['ener'] + fi(f) for f in B.LK_FUELS + ['bio']]
    num = lambda v: v if isinstance(v, (int, float)) else float('inf')
    d_lam = max(abs(sum(num(ws.cell(r, c).value) for c in [b2] + y2) - sum(num(ws.cell(r, c).value) for c in [b3] + y3))
                for r in rows)
    v = lambda key, c: ws.cell(B.R_LK[key], c).value
    eff = {f: ws.cell(B.R_LK[f'lkd.{f}'], 4).value for f in B.LK_FUELS}
    e_b = ws.cell(B.R_LK[f'lkb.{B.LK_FUELS[0]}'], 5).value
    bal = max(abs(sum(eff[f] * v(f'lkc.{f}', c) for f in B.LK_FUELS) + e_b * v('lkcb.bio', c))
              for b, ys in ((b2, y2), (b4, y4)) for c in [b] + ys)
    gap = max(abs(ws.cell(h + B.VOFF['ener'] + fi(f), c).value - ws.cell(h + B.VOFF['enel'] + fi(f), c).value
                  - v(f'lkc.{f}' if f != 'bio' else 'lkcb.bio', c)) for f in B.LK_FUELS + ['bio'] for c in [b2] + y2)
    k27 = 2027 - B.BASE_YEAR
    c27 = y2[k27 - 1]
    lpg, bio, p27 = v('lkc.lpg', c27), v('lkcb.bio', c27), v('lkp.lpg', c27)
    after = [round(v('lkp.lpg', c), 6) for c in y2[k27:k27 + 3]]
    ex = max(abs(v(f'lkd.{f}', c)) for f in ('lpg', 'ker') for c in [b4] + y4)
    good = (d_lam < 1e-9 and bal < 1e-9 and gap < 1e-9 and lpg < 0 < bio and ex < TOL
            and abs(bio + lpg * eff['lpg'] / e_b) < 1e-9)
    ok &= good
    log(f'- leakage on: LAMBDA test group = group 2 on the 6b rows and residential fuel use (max abs row-sum diff '
        f'{d_lam:.2g}); useful energy conserved, sum of e x cumulative change {bal:.2g}; fuel use = elasticity model + '
        f'cumulative change ({gap:.2g}); exempt LPG and kerosene do not leak (group 3: {ex:.2g}); scenario 2 in 2027: '
        f'LPG share moved {p27:.4%}, residential LPG {lpg:+.1f} ktoe, biomass {bio:+.1f} ktoe (useful energy: '
        f'{lpg * eff["lpg"]:+.1f} vs {bio * e_b:+.1f}); share in 2028-2030 {after} {"OK" if good else "FAIL"}')
    return ok


# v5.4 (power plan P1, P2, P4): a test scenario per power feature (MTInputs edits in a pasted group), recomputed in Python
PW_TESTS = {  # group -> (source group, name, MTInputs edits)
    3: (2, 'Test 3: MaximumGasCF 0.6, long-term storage from 2% VRE x 2 (P1)',
        {'MaximumGasCF': 0.6, 'StartingPointWhenLTStorageIsNeeded': 0.02, 'LongTermStorageFor100pcVRE': 2}),
    4: (2, 'Test 4: power inputs of the scenario (P2)',
        {'NewInvNga': 'No', 'NewInvNuc': 'Yes', 'NewInvNucYear': 2030, 'NewInvWndYear': 2026, 'kDispatch': 3,
         'kInvestment': 1.5, 'MinimumThermalEfficiency': 0.5, 'CFOverrideIfAbove': 0.5, 'CFOverrideIfBelowWndSol': 0.2,
         'WACCSource': 'User', 'WACCUserGlobal': 0.06, 'MinimumWACC': 0.07, 'RenewableCostDeclineRate': 'High',
         'PowerSectorPriceChangePassOn': 0.8, 'AdditionalEfficiencyPower': 0.01, 'MaxScaleUpRateCategory': 'High',
         'MaxNonVREAsPCOfTotalGen': 0.08, 'HydroDoesntRetire': 'No', 'EngineerModelProportionOfCovidFactor': 0.5,
         'IncElAdj': 'No', 'StorageHoursForLTStorage': 500, 'AllocateSTStorageToVRE': 0.8,
         'TotalHoursStorageFor100pcVRE': 12, 'StorageToInterfaceRatioSTStorage': 4, 'MinPostSubsidyPowerPrice': 0.02,
         'UseSpotFuelPricesInEngineerModel': 'Yes'}),
    5: (2, 'Test 5: power inputs of the scenario, other options (P2; Low decline: L109)',
        {'RenewableCostDeclineRate': 'Low', 'WACCSource': 'Income*', 'MaxScaleUpRateCategory': 'UserDefined',
         'MaxWindSolarScaleup': 0.04, 'MaxNonNucOreBioAsPCOfTotalGen': 0.03, 'NewInvOre': 'Yes', 'NewInvOreYear': 2025,
         'CFOverrideIfBelowFosOth': 0.2, 'NewInvCoa': 'Yes', 'MaximumCoalCF': 0.8}),
    6: (1, 'Test 6: PPAs, half of coal and gas, phased out 2030-2035 (P4; copy of 1, new coal permitted)',
        {'NewInvCoa': 'Yes', 'PPAProportionCoalGas': 0.5, 'PhaseOutCoalAndGasPPAsPolicy': 'Yes', 'YearPPACoalGas': 2030,
         'YearsToPhaseOutPPAs': 5}),
    7: (2, 'Test 7: renewable subsidies, base 0.01 and additional 0.02 $/kWh from 2028 over 5 years, hydro (P4)',
        {'RenewableSubsidyBL': 0.01, 'RenSubsidyAddUSDkwh': 0.02, 'RenSubsidyAddPhaseoutYrs': 5,
         'RenSubsidyAddStartYear': 2028, 'RenewableSubsidyHydro': 'Yes'}),
    8: (2, 'Test 8: power revenues rebated (PowerRebates = Yes; P4)', {'PowerRebates': 'Yes'}),
    9: (2, 'Test 9: electricity excise scenario and manual electricity excise (P4)',
        {'ScenarioSelected': ' - Electricity excise', 'AdditionalExcise': 'Yes'})}
PW_MI_EXCISE = {'res': {y: 0.01 + 0.002 * (y - 2026) for y in range(2026, 2045)},   # 'Manual inputs' rows 161-162
                'ind': {y: 0.005 for y in range(2027, 2045)}}
PW_GLOBAL = {'EarlyRetirementInBaseline': 'No', 'MaxNonVREAsPCOfTotalGen': 0.005, 'MaxScaleUpRateCategory':
             'UserDefined', 'MaxWindSolarScaleup': 0.005, 'MaxNonNucOreBioAsPCOfTotalGen': 0.005}


def check_power_features():
    """v5.4: power plan P1, P2, P4 switched on, one test scenario per feature (PW_TESTS, groups 3-9 pasted from groups 1
    and 2), each against the Python recomputation (power_model_ref_v7_0.engine with the scenario's settings); the global
    switch PwDeficitGas (Settings C45) with tight scale-up limits in scenarios 1 and 2."""
    ok = True
    wb = openpyxl.load_workbook(B.OUT)
    for g, (src, name, edits) in PW_TESTS.items():
        add_scenario(wb, src, g, name, edits)
    wmi = wb['Manual inputs']
    for u, row in (('res', 161), ('ind', 162)):
        for y, v in PW_MI_EXCISE[u].items():
            wmi.cell(row, 10 + y - B.BASE_YEAR).value = v
    MI_EXCISE.update(PW_MI_EXCISE)
    try:
        ws = recalc_wb(variant(wb, 'expand'))['Mitigation']
        exp = {}
        for g, (src, name, edits) in PW_TESTS.items():
            mt = scenario_mt(src)
            for k, v in edits.items():
                mt[B.MT_NAMES[k]] = v
            mt['scen'] = g
            exp[g] = recompute(mt)
            ok &= compare(ws, g, exp[g], f'power test, group {g} ({name}) vs Python')
    finally:
        MI_EXCISE.clear()
    cell = lambda key, g, y: ws.cell(B.R_PW[key] if isinstance(key, tuple) else key, B.group_cols(g)[2][y - B.BASE_YEAR - 1]).value
    rows = [('gen', 'nga'), ('gmx', 'nga'), ('gen', 'coa'), ('cap', 'nuc'), ('rp', 'res')]
    for g, (src, name, _e) in PW_TESTS.items():
        log(f'  - group {g}: ' + '; '.join(f'{v}.{m} 2030 {cell((v, m), g, 2030):,.4g} (source group {src}: '
                                            f'{cell((v, m), src, 2030):,.4g})' for v, m in rows))
    log(f'  - group 6 (PPAs): ppa share 2029-2036 {[round(cell(("ppa", ""), 6, y), 3) for y in range(2029, 2037)]}; coal '
        f'generation 2030 {cell(("gen", "coa"), 6, 2030):,.1f} MWy (logit {cell(("glg", "coa"), 6, 2030):,.1f}); early '
        f'coal retirement 2030 {cell(("early", ""), 6, 2030):,.1f} MW')
    log(f'  - group 7 (renewable subsidies): rns wind 2027-2034 {[round(cell(("rns", "wnd"), 7, y), 4) for y in range(2027, 2035)]}; '
        f'wind + solar capacity 2041 {cell(("cap", "wnd"), 7, 2041) + cell(("cap", "sol"), 7, 2041):,.0f} MW (group 2: '
        f'{cell(("cap", "wnd"), 2, 2041) + cell(("cap", "sol"), 2, 2041):,.0f}); renewable subsidy revenue 2030 '
        f'{ws.cell(B.R_FIS["rpol.ren"], B.group_cols(7)[2][2030 - B.BASE_YEAR - 1]).value:,.1f} USD m')
    log(f'  - group 8 (rebate): residential price 2030 {cell(("rp", "res"), 8, 2030):.4f} $/kWh (group 2: '
        f'{cell(("rp", "res"), 2, 2030):.4f}; before new policies {cell(("rppre", "res"), 8, 2030):.4f}); rebate 2030 '
        f'{cell(("rreb", "res"), 8, 2030) + cell(("rreb", "ind"), 8, 2030):,.1f} USD m')
    log(f'  - group 9 (excise): excise $/kWh 2030 {cell(("exs", ""), 9, 2030):.5f} (grid intensity x carbon price), '
        f'residential pex 2030 {cell(("pex", "res"), 9, 2030):.5f}, industry {cell(("pex", "ind"), 9, 2030):.5f}; '
        f'revenue 2030: carbon-based {cell(("rexs", ""), 9, 2030):,.1f}, manual {cell(("rexm", ""), 9, 2030):,.1f} USD m')
    # the global switch PwDeficitGas (Settings C45) with tight scale-up limits in scenarios 1 and 2
    wb = openpyxl.load_workbook(B.OUT)
    wb['Settings']['C45'].value = 'Yes'
    for g in (1, 2):
        for k, v in PW_GLOBAL.items():
            mt_set(wb['ScenarioDefinition'], B.MT_COL0 + g - 1, k, v)
    DEFICIT_GAS['on'] = True
    GLOBAL_MT.update(PW_GLOBAL)              # both columns edited: scenario 1 is also the reference run (section 14)
    try:
        ws2 = recalc_wb(variant(wb, 'expand'))['Mitigation']
        for g in (1, 2):
            ok &= compare(ws2, g, recompute(scenario_mt(g)), f'PwDeficitGas = Yes, tight scale-up limits, scenario {g} '
                                                             f'vs Python')
    finally:
        DEFICIT_GAS['on'] = False
        GLOBAL_MT.clear()
    c2 = lambda key, g, y: ws2.cell(B.R_PW[key], B.group_cols(g)[2][y - B.BASE_YEAR - 1]).value
    dg = [round(c2(('dgas', ''), 1, y), 1) for y in range(2025, 2033)]
    log(f'  - PwDeficitGas: deficit to gas 2025-2032 (scenario 1) {dg} MW; gas investment 2030 '
        f'{c2(("nei", "nga"), 1, 2030):,.1f} MW, first + second round {c2(("first", "nga"), 1, 2030) + c2(("second", "nga"), 1, 2030):,.1f}')
    return ok


PO_SCEN_ROWS = {B.R_POL[f'{v_}.{k_}'] for k_, *_x in B.PHASEOUTS for v_ in ('po.on', 'po.n', 'po.sh')}


def check_scenarios():
    wb = openpyxl.load_workbook(B.OUT)
    zero = {'CPLevelStart': 0, 'CPLevelTarget': 0}
    add_scenario(wb, 2, 3, 'Test 3: copy of 2', {})
    add_scenario(wb, 3, 4, 'Test 4: copy of 2, carbon price 0', zero)
    add_scenario(wb, 4, 5, 'Test 5: legacy Egypt carbon tax', {'CPIntro': 2026, 'CPLevelStart': 0,
                                                                'CPLevelTarget': 50, 'CPOutro': 2030})
    add_scenario(wb, 4, 6, 'Test 6: fuel price reform', FPR_TEST)
    add_scenario(wb, 4, 7, 'Test 7: feebates', FB_TEST)
    add_scenario(wb, 2, 8, 'Test 8: IMF-WB*, High, nominal carbon price', PRICE_TEST)
    add_scenario(wb, 2, 9, 'Test 9: new ETS with cap (fast estimate) + carbon tax elsewhere', ETS_TEST)
    add_scenario(wb, 2, 10, 'Test 10: ETS override blank, no volatility, full auctioning', ETS_EQUIV)
    for g, (src, name, edits) in TR_TESTS.items():       # v3.5: engineer road model switched on, with policies
        add_scenario(wb, src, g, name, edits)
    wb_t = recalc_wb(variant(add_mto_blocks(wb, range(3, 11)), 'expand'))
    ws = wb_t['Mitigation']
    ok = True
    for a, b, label in [(2, 3, 'scenario 3 (copy of 2) = scenario 2'),
                        (1, 4, 'scenario 4 (copy of 2, carbon price 0 in MTInputs) = scenario 1')]:
        ca, cb = B.group_cols(a), B.group_cols(b)
        diff, n = 0.0, 0
        for r in range(B.R_YEAR, ws.max_row + 1):
            if r in (B.R_SCEN, B.R_NAME, B.R_LHCOL):     # v2.5: row 4 holds the group's own column numbers
                continue
            if r == B.R_TR['tr.pol']:            # v3.5: policy-scenario flag (scenario number > 1, fix B1)
                continue
            if b == 4 and r in PO_SCEN_ROWS:     # v5.2 (v4.16, LD18/LD19): scenario 1 takes the baseline phase-out
                continue                         # switch, period and share, the others the policy ones (by design)
            for x, y in zip([ca[1]] + ca[2], [cb[1]] + cb[2]):
                va, vb = ws.cell(r, x).value, ws.cell(r, y).value
                if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
                    if b == 4 and r in (B.R_POL['CPLevelStart'], B.R_POL['CPLevelTarget']):
                        continue
                    diff, n = max(diff, abs(va - vb)), n + 1
                elif va != vb:
                    diff = float('inf')
        good = diff < TOL
        ok &= good
        log(f'- {label}: {n} numeric cells, max abs diff {diff:.3g} {"OK" if good else "FAIL"}')
    for g in (3, 4, 5, 6, 7, 8, 9, 10):
        code, base, _ = B.group_cols(g)
        num_, name = ws.cell(B.R_SCEN, code).value, ws.cell(B.R_NAME, base).value
        c = ws.cell(B.SUB_HEAD['rod'] + B.VOFF['ener'], code).value
        good = (num_ == g and c == RC(f'{B.COUNTRY.lower()}.mit.ener.rod.coa.e.{g}')   # v7.2: through the map
                and str(name).startswith(f'Test {g}'))
        ok &= good
        log(f'- pasted group {g}: number {num_}, name "{name}", code `{c}` {"OK" if good else "FAIL"}')
    _, base, years = B.group_cols(5)
    got = {ws.cell(B.R_YEAR, c).value: ws.cell(B.R_CP, c).value for c in [base] + years}
    d = max(abs(got[y] - v) for y, v in LEGACY_CP.items())
    ok &= d < TOL
    log(f'- scenario 5 (legacy Egypt carbon tax): carbon price {[got[y] for y in (2026, 2027, 2030, 2035)]} vs '
        f'legacy row 8582, max abs diff {d:.3g} {"OK" if d < TOL else "FAIL"}')
    base_mt = scenario_mt(2)
    for g, edits in ((5, {'CPIntro': 2026, 'CPLevelStart': 0, 'CPLevelTarget': 50, 'CPOutro': 2030}),
                     (6, {**zero, **FPR_TEST}), (7, {**zero, **FB_TEST}), (8, PRICE_TEST), (9, ETS_TEST),
                     (10, ETS_EQUIV)):
        mt = dict(base_mt)
        for k, v in edits.items():
            mt[k if isinstance(k, int) else B.MT_NAMES[k]] = v
        ok &= compare(ws, g, recompute(mt), f'scenario {g} vs Python')
    ok &= check_transport_scenarios(ws)
    ok &= check_results_memos(ws)          # v3.10: memos and results sections recomputed in Python
    r_ntx = B.SUB_HEAD['rod'] + B.VOFF['ntx'] + 2
    r_shp = B.SUB_HEAD['rod'] + B.VOFF['shp'] + 2
    _, b6, y6 = B.group_cols(6)
    _, b7, y7 = B.group_cols(7)
    log(f'  - scenario 6, road gasoline new excise ($/GJ) 2026-2031: '
        f'{[round(ws.cell(r_ntx, c).value, 3) for c in y6[3:9]]}')
    log(f'  - scenario 7, road gasoline feebate shadow price ($/GJ) 2026-2031: '
        f'{[round(ws.cell(r_shp, c).value, 3) for c in y7[3:9]]}')
    (_, b1, y1), (_, b4, y4) = B.group_cols(1), B.group_cols(7)
    mt7 = dict(scenario_mt(2))
    for k, v in {**{'CPLevelStart': 0, 'CPLevelTarget': 0}, **FB_TEST}.items():
        mt7[k if isinstance(k, int) else B.MT_NAMES[k]] = v
    rate = {s: mt7[B.MT_NAMES[b]] for s, a, b in B.FEEBATE_SECTORS}
    fbsec = {s[0]: s[6] for s in B.SUBSECTORS}
    covered = {s for s, *_ in B.SUBSECTORS if mt7[66 + B.COV_SECTORS.index(s)] and rate[fbsec[s]]}
    # v5.2: since the GDP feedback (v3.1, section 16) the other subsectors change with GDP growth only: their fuel use
    # in scenario 7 = the Python scenario 1 run at scenario 7's growth path (relative diff)
    g7 = recompute(mt7)[('gdp.pos.pct', '', '')]
    r1g = _recompute_once(scenario_mt(1), gdp=g7)
    d_unc = max(abs(ws.cell(r, y).value - r1g[('ener', s, f_)][k]) / max(1.0, abs(r1g[('ener', s, f_)][k]))
                for r, s, f_ in B.var_rows('ener') if s not in covered for k, y in enumerate([b4] + y4))
    lower = [(s, ws.cell(B.SUB_HEAD[s], y4[-2]).value / ws.cell(B.SUB_HEAD[s], y1[-2]).value - 1)
             for s in covered if ws.cell(B.SUB_HEAD[s], y1[-2]).value > 0]   # mch: no fuel use in the base data
    good = d_unc < TOL and len(lower) >= 2 and all(x < 0 for _s, x in lower)
    ok &= good
    log(f'- scenario 7 vs scenario 1 (covered with a non-zero rate: {", ".join(sorted(covered))}): '
        f'other subsectors unchanged apart from the GDP feedback (= scenario 1 at the growth path of scenario 7, '
        f'max rel diff {d_unc:.3g}); covered subsectors '
        f'in {B.YEARS[-2]}: {", ".join(f"{s} {x:+.2%}" for s, x in sorted(lower))} {"OK" if good else "FAIL"}')
    _, b8, y8 = B.group_cols(8)
    r_oil = B.R_GP0
    log(f'  - scenario 8: crude oil gp 2024-2026 (real) {[round(ws.cell(r_oil, c).value, 2) for c in y8[1:4]]}, '
        f'carbon price 2027-2030 (nominal 20 x infl) {[round(ws.cell(B.R_CP, c).value, 3) for c in y8[4:8]]}')
    # ETS with blank override, no volatility and full auctioning = carbon tax: same nce and fuel use as scenario 2
    (_, b2, y2), (_, b9, y9) = B.group_cols(2), B.group_cols(10)
    d_nce = max(abs(ws.cell(r, x).value - ws.cell(r, y).value) for v in ('nce', 'atp', 'ener')
                for r, *_ in B.var_rows(v) for x, y in zip([b2] + y2, [b9] + y9))
    ets_sum = sum(ws.cell(r, y9[-2]).value for r, *_ in B.var_rows('ets'))
    ctx_cem = sum(ws.cell(r, y9[-2]).value for r, s_, _f in B.var_rows('ctxnew') if s_ == 'cem')
    good = d_nce < TOL and ets_sum > 0 and abs(ctx_cem) < TOL
    ok &= good
    log(f'- scenario 10 (new ETS on power and industry from 2027, override row blank = carbon price, volatility '
        f'Zero, policy risk 0, benchmarks 0): nce, atp and fuel use equal scenario 2 (max abs diff {d_nce:.3g}); ETS cost > 0 '
        f'({ets_sum:.2f}, sum over rows {B.YEARS[-2]}); carbon tax in cement 0 ({ctx_cem:.3g}) '
        f'{"OK" if good else "FAIL"}')
    _, b9, y9 = B.group_cols(9)
    row = lambda k, sec=B.R_POL: [round(ws.cell(sec[k], c).value, 3) for c in y9[3:14]]
    log(f'  - scenario 9 (cap -2% in 2027 to -15% in 2035 vs baseline covered emissions; benchmarks 1.0 flat, the legacy default; '
        f'volatility Medium), 2026-2036:')
    for k, lab in (('ets.bce', 'baseline covered emissions (MtCO2)'), ('ets.cap', 'cap (MtCO2)'),
                   ('ets.vadj', 'volatility adjustment'), ('ets.se', 'effective semi-elasticity'),
                   ('ets.est', 'fast estimate ($/tCO2)'), ('ets.p', 'permit price used'),
                   ('obr.cem', 'OBR share, cement')):
        log(f'    - {lab}: {row(k)}')
    for k, lab in (('co2.ets', 'covered emissions (MtCO2)'), ('co2.gap', 'covered / cap - 1'),
                   ('ets.next', 'next price proposal')):
        log(f'    - {lab}: {row(k, B.R_EMI)}')
    va = ws.cell(B.R_POL['ets.vadj'], y9[-2]).value
    good9 = abs(va - 1 / 1.1) < 1e-12
    ok &= good9
    log(f'  - volatility adjustment at Medium = 1/1.1 as legacy row 2191 ({va:.6f}) {"OK" if good9 else "FAIL"}')
    chk = max(abs(ws.cell(B.R_EMI['bco2.chk'], c).value) for g in range(1, 11)
              for c in [B.group_cols(g)[1]] + B.group_cols(g)[2])
    ok &= chk < 1e-9
    log(f'- bco2.chk (baseline data vs scenario 1 CO2) in all 10 groups: max abs {chk:.3g} '
        f'{"OK" if chk < 1e-9 else "FAIL"}')
    for controls in ('None', 'Manual'):          # global setting: MTInputs scenario-1 column
        wbc = openpyxl.load_workbook(B.OUT)
        wbc['ScenarioDefinition'].cell(B.MT_NAMES['GovPriceControls'], B.MT_COL0).value = controls
        wsc = recalc(variant(wbc, 'expand'))
        for g in (1, 2):
            ok &= compare(wsc, g, recompute(scenario_mt(g), controls),
                          f'price controls {controls} (global), scenario {g} vs Python')
    ok &= check_mto(wb_t, list(range(1, 11)), 'with blocks 3-10 added by copying (scenario tests)')
    return ok


PRICE_VARS = {'sp', 'txo', 'rpb', 'vat', 'etx', 'esub', 'esubpu', 'atp', 'ener', 'co2', 'rtx', 'rsub', 'rnew',
              'rnet', 'rtot'}


POWER_OLD = {'tcf', 'gns', 'phi', 'cbat', 'cint', 'obat', 'cel', 'cons', 'cax', 'caxav', 'stoav', 'fix', 'lfx', 'vbc',
             'ccp', 'gnc', 'gncav', 'ccpav', 'sc', 'rppre', 'rp', 'sgap', 'rvat', 'rcarb', 'rgap', 'vre', 'cph', 'msc'}


SIGN_FLIP = set()                       # v2.4 (vs v2.3): esub, esubpu, rsub, prsub, sgap, rgap changed sign


V60_S1 = {'ch4', 'ghg', 'gchg', 'aps', 'ap', 'apf', 'ndc', 'dmg', 'wcli', 'wel', 'kaya', 'kidx', 'ch4.em', 'ch4.act',
          'ch4.src', 'ch4.sup', 'ch4.rev', 'ghg.k', 'ghg.flr'}


def foo_dependent(k):
    """v6.0 intended changes against v5.7: I47 (methane intensities on base-year data activity: methane by source,
    GHG totals, the local-pollutant table, NDC rows and climate damages in every scenario), I43 (revenue uses from
    CPIntro: the GDP feedback of scenario 2 and everything downstream of it), the NDC GDP rows (local currency)."""
    parts = k.split('.')
    return parts[-1] == '2' or parts[2] in V60_S1 or '.'.join(parts[2:4]) in V60_S1


def _foo_dependent_v313(k):
    """v3.13: none against the previous version (new rows only)."""
    return False


def _foo_dependent_v34(k):
    """v3.4: the CO2 calibration is off by default (EFCalib = 1): the v3.2 set changes back (CO2 rows and the GHG rows
    built on energy CO2 in every scenario; scenario 2 throughout)."""
    return _foo_dependent_v32(k)


def _foo_dependent_v33(k):
    """v3.3: none: the country data moved into keyed tables, the Egypt values are the same."""
    return False


def _foo_dependent_v32(k):
    """v3.2: CO2 rows (and the GHG rows built on energy CO2) scale by the calibration factor in every scenario;
    scenario 2 (policies priced per tonne) changes throughout. Fuel use, prices and revenues of scenario 1 do not."""
    return k.endswith('.2') or k.split('.')[2] in ('co2', 'bco2', 'ghg', 'ef', 'efk')


def _foo_dependent_v23(k):
    """v2.3 intended changes: power (moving-average fuel prices, levelised window to 2041) and everything that
    includes power (totals, ETS baseline and cap, revenues, electricity memo lines). Price and subsector rows of the
    sector blocks must not change."""
    p = k.split('.')
    fixed = (set(B.VARS) | {'gp', 'gpn'}) - {'eldem'}
    groups = {s_[0] for s_ in B.SUBSECTORS} | {g for _n, g, _t in B.SECTIONS}
    return not (p[2] in set(B.PVARS) or (p[2] in fixed and p[3] in groups))


def _foo_dependent_v22(k):
    """v2.2: none. (v1.09 intended changes: power generation fuel use enters the fuel totals (total, by fuel, reference and
    change rows of section 11) and power revenues enter the revenue totals (rtx, rsub, rnew, rnet, rtot and the
    reference and change rows).)"""
    return False                     # v2.2: no intended change against v1.09


def _unused(k):
    """Fuel-use codes that change with the food & forestry elasticities (v0.11): foo itself and its aggregates."""
    p = k.split('.')
    return p[2] == 'ener' and (p[3] in ('foo', 'all', 'bld', 'ref', 'pct', 'chk'))


def _prev_version():
    """v5.2: the previous version = the highest build_v<major>_<minor>.py in Old/ below this version (v3.13: minor - 1,
    which gave 5.-1 after v4.16); minor - 1 when Old/ has none."""
    cur = tuple(int(x) for x in B.VERSION.split('.'))
    rel = os.path.join(HERE, '..', 'releases')       # restructure 2026-10-22: released workbooks (was Old/)
    vs = [tuple(int(x) for x in m.groups()) for m in (re.fullmatch(re.escape(B.NAME) + r'-v(\d+)\.(\d+)\.xlsm', fn)
                                                      for fn in (os.listdir(rel) if os.path.isdir(rel) else [])) if m]
    below = [v for v in vs if v < cur]
    return '.'.join(map(str, max(below or [v for v in vs if v == cur] or [(cur[0], cur[1] - 1)])))


PREV = _prev_version()                   # v3.13: the previous version


def check_regression(ws_new):
    """v3.13: against the previous version (v3.11 changed every result on purpose; each version since adds rows only,
    so every shared output code keeps its value)."""
    pv = PREV.replace('.', '_')
    bo = B                                         # restructure 2026-10-22: the release's layout = this builder's
    wbo = openpyxl.load_workbook(os.path.join(HERE, '..', 'releases', f'{B.NAME}-v{PREV}.xlsm'))   # (was Old/)
    wso = wbo['Mitigation']
    for g in (1, 2):
        c = bo.group_cols(g)[2][-1]
        for r in range(1, wso.max_row + 1):
            v = wso.cell(r, c).value
            if isinstance(v, str) and v.startswith('='):
                wso.cell(r, c).value = expand(v, bo.LAMBDAS)
    path = os.path.join(tempfile.mkdtemp(), 'old.xlsx')
    wbo.save(path)
    old = recalc(path)
    vo, vn = {}, {}
    for g in (1, 2):
        for src, mod, dst in ((old, bo, vo), (ws_new, B, vn)):
            code, base, years = mod.group_cols(g)
            for r in range(1, src.max_row + 1):
                k = src.cell(r, code).value
                if isinstance(k, str) and k.startswith(B.COUNTRY.lower() + '.'):
                    dst[RC(k) if dst is vo else k] = [src.cell(r, c).value for c in [base] + years]   # v7.2: map
    shared = set(vo) & set(vn)
    intended = {k for k in shared if foo_dependent(k)}
    common = sorted(shared - intended)
    sgn = lambda k: -1 if k.split('.')[2] in SIGN_FLIP else 1           # v2.4: subsidy rows: new = -old
    dk = {k: max([abs(a - sgn(k) * b) for a, b in zip(vo[k], vn[k])
                  if isinstance(a, (int, float)) and isinstance(b, (int, float))] or [0]) for k in common}
    flipped = [k for k in common if sgn(k) < 0 and any(abs(a) > TOL for a in vo[k] if isinstance(a, (int, float)))]
    diff = max(dk.values())
    ok = diff < TOL and len(common) > 1000
    log(f'- {len(common)} output codes in both versions ({len(intended)} intended changes), '
        f'{B.BASE_YEAR}-{B.LAST_YEAR}: max abs diff {diff:.3g} {"OK" if ok else "FAIL " + str([k for k in dk if dk[k] > TOL][:8])}')
    if SIGN_FLIP:
        log(f'- rows compared as new = -old: {", ".join(sorted(SIGN_FLIP))}; {len(flipped)} of them non-zero')
    new = sorted({k.split('.')[2] for k in set(vn) - set(vo)})
    log(f'- variables added: {", ".join(new)}')
    fam = sorted({'.'.join(k.split('.')[2:4]) for k in intended if max(
        [abs(a - b) for a, b in zip(vo[k], vn[k]) if isinstance(a, (int, float)) and isinstance(b, (int, float))]
        or [0]) > TOL})
    log(f'- intended changes that differ: {", ".join(fam) or "none"}')
    return ok


ECP_TEST = {  # existing carbon pricing test data for the country (nominal $/tCO2 by year; coverage shares, all years)
    'ecr.all': {2021: 5.0, 2022: 5.0, 2023: 6.0, 2024: 8.0, 2025: 10.0}, 'ecs.trs': 1.0, 'ecs.res': 0.5,
    'ecf.gso': 1.0, 'ecf.die': 1.0, 'ecf.nga': 1.0, 'ecf.lpg': 0.5,
    'eer.all': {2021: 0.0, 2022: 0.0, 2023: 0.0, 2024: 15.0, 2025: 20.0}, 'ees.pow': 1.0, 'ees.ind': 0.6,
    'eef.coa': 1.0, 'eef.nga': 1.0, 'eef.oop': 1.0,
    'res.trs': 0.3, 'ref.die': 1.0}   # v4.15: regional EU ETS coverage (EU price from the legacy data)
ECP_SCEN = {3: ('Test 3: existing pricing grows 3% / 2% a year', {'ExistingCTGrowth': 0.03, 'ExistingETSGrowth': 0.02}),
            4: ('Test 4: existing pricing switched off', {'ExistingCTApply': 'No', 'ExistingETSApply': 'No'}),
            5: ('Test 5: new carbon tax complementary to the existing ETS', {'CTaxComplimentaryToETS': 'Yes'})}


STALE = ['not yet in the section-12', 'Power and electricity are not yet included', 'power revenues stay',
         'power 0 until', 'no power sector', '; no power,', 'Power ETS revenue about 10% high', 'interim data until',
         'not in the fuel totals above)', 'Existing ETS and existing carbon taxes', 'LAMBDA in the right column (2040)',
         'right column calls a named LAMBDA']
DOC_REF = re.compile(r'[A-Za-z][\w-]*_v\d+(?:[._]\d+)*\.(?:md|py|docx|bas)')


def check_consistency(ws):
    """v1.09 full consistency check of the shipped workbook: check rows and accounting identities in every scenario
    group, file references in the workbook texts exist (current versions, not Old/), version strings, no stale
    statements about power or existing carbon pricing."""
    ok = True
    groups = [g for g, *_ in B.SCENARIOS]
    cols = [c for g in groups for c in [B.group_cols(g)[1]] + B.group_cols(g)[2]]
    v = lambda r, c: ws.cell(r, c).value
    chk = {k: max(abs(v(r, c)) for c in cols) for k, r in (('ener.chk', B.R_CHK), ('rev.chk', B.R_REV['rev.chk']),
                                                          ('co2.chk', B.R_EMI['co2.chk']),
                                                          ('bco2.chk', B.R_EMI['bco2.chk']),
                                                          ('ch4bs.chk', B.R_GHG['ch4bs.chk']))}   # v6.2 (I47)
    good = all(x < 1e-6 for x in chk.values())
    ok &= good
    log(f'- check rows in groups {groups}: ' + ', '.join(f'{k} {x:.2g}' for k, x in chk.items()) +
        f' {"OK" if good else "FAIL"}')
    R_ = B.R_REV
    iden = []
    for c in cols:
        iden.append(abs(v(R_['rnet.all'], c) - (v(R_['rtx.all'], c) + v(R_['rsub.all'], c))))
        iden.append(abs(v(R_['rtot.all'], c) - (v(R_['rnet.all'], c) + v(R_['rnew.all'], c))))
        iden.append(abs(v(B.R_TOTAL, c) - sum(v(B.SEC_SUM[g], c) for _n, g, _t in B.SECTIONS) - v(B.R_EPOW, c)))
        pe = sum(v(B.R_PW[('pe', m)], c) * (m in [f for f, *_ in B.FUELS]) for m, _n in B.PW_TECH)
        iden.append(abs(v(B.R_EPOW, c) - pe))
        co2p = sum(v(B.R_PW[('co2', m)], c) for m, _n in B.PW_TECH)
        iden.append(abs(v(B.R_EMI['co2.pow'], c) - co2p))
        iden.append(abs(v(B.R_EMI['co2.sec.pow'], c) - co2p))
    d = max(iden)
    good = d < 1e-6
    ok &= good
    log(f'- identities in every column: rnet = rtx + rsub (subsidies negative), rtot = rnet + rnew, fuel use = sector totals + power, '
        f'power fuel use = fuel types of pe, power CO2 = CO2 by type = ETS sector power: max abs {d:.2g} '
        f'{"OK" if good else "FAIL"}')
    wbf = openpyxl.load_workbook(B.OUT)
    texts = [(w.title, c.coordinate, c.value) for w in wbf.worksheets for row in w.iter_rows() for c in row
             if isinstance(c.value, str) and not c.value.startswith('=')]
    refs = sorted({m for _t, _c, s in texts for m in DOC_REF.findall(s)})
    hist = {m for _t, _c, s in texts if s.startswith(('v0.', 'v1.')) for m in DOC_REF.findall(s)}
    vlog = {m for t, _c, s in texts if t == B.TAB_REF for m in DOC_REF.findall(s)}   # v3.6: version log tab
    missing = [m for m in refs if m not in hist | vlog and not os.path.exists(os.path.join(HERE, m))
               and not os.path.exists(os.path.join(HERE, 'presentation', m))]
    ok &= not missing
    log(f'- file references in the workbook texts ({len(refs)}): current ones exist in the folder: '
        f'{"OK" if not missing else "FAIL " + str(missing)}')
    stale = [(t, c, p) for t, c, s in texts for p in STALE if p in s]
    ok &= not stale
    log(f'- stale statements about power, revenues or interim data in the workbook texts: '
        f'{"none OK" if not stale else "FAIL " + str(stale[:6])}')
    st = B.tab(wbf, 'VersionLog')
    last_log = max((r for r in range(B.SET_LOG + 2, st.max_row + 1) if st.cell(r, 1).value), default=None)
    title_ok = wbf['Mitigation']['A2'].value == 'Mitigation Module'   # v2.7: version in Settings log, ReadMe, file name
    readme = open(os.path.join(HERE, 'README.md'), encoding='utf-8').read()
    good = (st.cell(last_log, 1).value == B.VERSION and title_ok and f'{B.NAME}-v{B.VERSION}.xlsm' in readme
            and f'build_v{B.VERSION.replace(".", "_")}.py' in readme)
    ok &= good
    log(f'- versions: Settings log ends with {st.cell(last_log, 1).value}, Mitigation title "Mitigation Module", folder README '
        f'names the workbook and builder of v{B.VERSION} {"OK" if good else "FAIL"}')
    fut = re.compile(r'(?<![\w.])(MAXIFS|MINIFS|AGGREGATE|IFNA|IFS|SWITCH|XLOOKUP|XMATCH|LET|LAMBDA|FILTER|SORT|'
                     r'UNIQUE|SEQUENCE|TEXTJOIN|CONCAT|FORECAST\.LINEAR|STDEV\.S)\(')
    nofx = [(w_.title, c_.coordinate) for w_ in wbf.worksheets for row_ in w_.iter_rows() for c_ in row_
            if isinstance(c_.value, str) and c_.value.startswith('=') and fut.search(c_.value.replace('_xlfn.', '_xlfn_'))]
    for n_, d_ in wbf.defined_names.items():
        if d_.attr_text and fut.search(d_.attr_text.replace('_xlfn.', '_xlfn_')):
            nofx.append(('name', n_))
    ok &= not nofx
    log(f'- v2.8: newer Excel functions (MAXIFS, MINIFS, AGGREGATE, IFNA, ...) carry the _xlfn. prefix in the file '
        f'(else Excel removes the formula on repair): {"OK" if not nofx else "FAIL " + str(nofx[:6])}')
    import make_equations_v7_0 as EQ                    # equation list regenerated from the shipped workbook
    n_eq, miss_eq = EQ.main()
    good = not miss_eq and os.path.exists(EQ.OUT)
    ok &= good
    log(f'- equations: {os.path.basename(EQ.OUT)} regenerated from the workbook, {n_eq} variables; every variable of the '
        f'dictionary has its equation {"OK" if good else "FAIL " + str(miss_eq[:8])}')
    cur = [f for d in ('', 'presentation') for f in os.listdir(os.path.join(HERE, d))
           if re.search(r'_v\d+[._]\d+', f) and os.path.isfile(os.path.join(HERE, d, f))
           and not f.startswith('Plan_')]                 # v3.13: a plan keeps the name of its span
    tags = {B.VERSION, B.SCRIPTS_TAG.replace('_', '.')}   # v7.1: point release: scripts and notes keep the x.0 tag
    off = [f for f in cur if not any(re.search(r'_v' + t.replace('.', r'[._]') + r'\.\w+$', f)
                                     or re.search(r'-v' + t.replace('.', r'\.') + r'\.\w+$', f) for t in tags)]
    vnum = lambda f: tuple(int(x) for x in re.search(r'[_-]v(\d+)[._](\d+)', f).groups())
    cur_v = tuple(int(x) for x in B.VERSION.split('.'))
    nxt = [f for f in off if vnum(f) > cur_v]          # v3.4: work in progress for the next version is allowed
    base_v = tuple(int(x) for x in B.SCRIPTS_TAG.split('_'))
    pnt = [f for f in off if base_v < vnum(f) < cur_v]  # v7.2: a file new at a point release keeps its tag
    off = [f for f in off if f not in nxt and f not in pnt]
    ok &= not off
    log(f'- every current versioned file of the folder carries version {B.VERSION} or the scripts tag '
        f'{B.SCRIPTS_TAG} ({len(cur)} files; new at a point release, keeping its tag: {pnt}): '
        f'{"OK" if not off else "FAIL " + str(off)}')
    import issues_register_v7_0 as IR
    ids = [i for i, *_ in IR.items()]
    ld_n = sum(1 for d in B.LEGACY_DIFFS if d[5] in IR.LD_TYPES)
    ld_in = sum(1 for i in ids if i.startswith('LD'))
    good = len(ids) == len(set(ids)) and ld_in == ld_n and all(t for _i, t, *_ in IR.items())
    st_ok = ({i for i, *_ in IR.ISSUES} == set(IR.ISSUE_STATUS) and
             all(s in ('Major', 'Minor') and st in ('Open', 'Accepted', 'Resolved', 'Dropped') for s, st, _n in
                 IR.ISSUE_STATUS.values()))    # v3.7: every issue has a severity and a status (issues list)
    good &= st_ok
    ok &= good
    log(f'- issues register (issues_register_v7_0.py, Word register): {len(ids)} items, unique IDs; LegacyDiff rows of '
        f'type {", ".join(IR.LD_TYPES)} all included ({ld_in} of {ld_n}) {"OK" if good else "FAIL"}')
    notes = [f for f in os.listdir(HERE) if f.endswith('.md') and DOC_REF.fullmatch(f)]
    stems = {}
    for f in notes:
        stems.setdefault(re.sub(r'_v\d.*', '', f), []).append(f)
    dup = {k: x for k, x in stems.items() if len(x) > 1}
    ok &= not dup
    log(f'- one current version of each method note in the folder ({len(notes)} notes): '
        f'{"OK" if not dup else "FAIL " + str(dup)}')
    return ok


def check_ecp():
    """v1.09: existing carbon pricing with non-zero test data for Egypt, in the shipped scenarios and three test
    scenarios, against the Python recomputation; properties. v4.15: the test data are written into the legacy layout
    of sheet ECP (an information row for the country, and one row per code at the end of its legacy block)."""
    wb = openpyxl.load_workbook(B.OUT)
    we = wb['ECP']
    data = dict(ECP_CELLS)
    edits = {}
    info = next(r for r in range(11, 67) if (r, 3) not in ECP_CELLS)       # a blank information row
    edits.update({(info, 3): ISO, (info, 5): 'No', (info, 11): 'Yes'})        # no single price; EU ETS applies
    used = {}
    lkey = dict(B.ECP_CODES)
    for code, v in ECP_TEST.items():
        vals = v if isinstance(v, dict) else {y: v for y in B.ECP_YEARS}
        a, b = B.ECP_BLOCKS[code.split('.')[0]]
        r = b - used.get(b, 0)
        used[b] = used.get(b, 0) + 1
        edits[(r, 5)] = f'{ISO.lower()}.mit.{lkey[code]}'
        for c in range(6, 17):
            edits[(r, c)] = vals.get(2015 + c - 6)
    for (r, c), x in edits.items():
        we.cell(r, c).value = x
        if x is None:
            data.pop((r, c), None)
        else:
            data[(r, c)] = float(x) if isinstance(x, (int, float)) else x
    for g, (name, edits) in ECP_SCEN.items():
        add_scenario(wb, 2, g, name, edits)
    ws = recalc(variant(wb, 'expand'))
    ok = True
    for g in (1, 2, 3, 4, 5):
        mt = dict(scenario_mt(1 if g == 1 else 2))
        for k, v in ECP_SCEN.get(g, ('', {}))[1].items():
            mt[B.MT_NAMES[k]] = v
        ok &= compare(ws, g, recompute(mt, ecp=data), f'ECP test data, scenario {g} vs Python')
    yr = lambda g: dict(zip([ws.cell(B.R_YEAR, c).value for c in [B.group_cols(g)[1]] + B.group_cols(g)[2]],
                            [B.group_cols(g)[1]] + B.group_cols(g)[2]))
    c2, c4 = yr(2), yr(4)
    lh = B.LAST_HIST
    d_hist = max(abs(ws.cell(r_, c2[lh]).value or 0) for r_, *_ in B.var_rows('xcpd'))   # v4.12: embedded year
    d_after = max(ws.cell(r_, c2[2030]).value for r_, *_ in B.var_rows('xcpd'))
    lvl = sum(ws.cell(r_, c2[2030]).value for r_, *_ in B.var_rows('xcp'))
    off = min(ws.cell(r_, c4[2030]).value for r_, *_ in B.var_rows('xcpd'))
    rx = [round(ws.cell(B.R_REV[k], c2[2030]).value, 1) for k in ('rxcp.all', 'rxcp.pow')]
    xk = max(ws.cell(B.R_PW[('xck', m)], c2[2030]).value for m, _n in B.PW_TECH)
    good = d_hist < TOL and d_after > 0 and lvl > 0 and off < 0 and rx[0] > 0 and rx[1] > 0 and xk > 0
    ok &= good
    log(f'- scenario 2 with the test data: change against the price data xcpd = 0 in {lh} (max {d_hist:.2g}), '
        f'> 0 in 2030 (data 2025 above 2024: max {d_after:.3f} $/GJ); level xcp > 0; power xck 2030 max {xk:.5f} $/kWh; '
        f'existing carbon pricing revenue 2030 (all, power) {rx} USD m; scenario 4 (switched off): xcpd < 0 '
        f'(min {off:.3f}) {"OK" if good else "FAIL"}')
    c5 = yr(5)
    ctr = {s: ws.cell(B.R_POL[f'ctr.{s}'], c5[2030]).value for s in ('pow', 'cem', 'rod')}
    cp = ws.cell(B.R_CP, c5[2030]).value
    good = abs(ctr['pow']) < TOL and abs(ctr['cem'] - cp * 0.4) < 1e-9 and abs(ctr['rod'] - cp) < 1e-9
    ok &= good
    log(f'- scenario 5 (complementary): new carbon tax rate 2030 = carbon price {cp:.2f} x (1 - existing ETS sector '
        f'coverage): power {ctr["pow"]:.2f}, cement {ctr["cem"]:.2f}, road {ctr["rod"]:.2f} {"OK" if good else "FAIL"}')
    chk = max(abs(ws.cell(rr, c).value) for g in (1, 2, 3, 4, 5) for c in [B.group_cols(g)[1]] + B.group_cols(g)[2]
              for rr in (B.R_CHK, B.R_REV['rev.chk'], B.R_EMI['co2.chk']))
    ok &= chk < 1e-6
    log(f'- check rows ener.chk, rev.chk, co2.chk in groups 1-5: max abs {chk:.2g} {"OK" if chk < 1e-6 else "FAIL"}')
    return ok


def check_codes(wsf, wsv):
    ok = True
    described = [r for r in range(1, wsf.max_row + 1)
                 if isinstance(wsf[f'H{r}'].value, str) and wsf[f'H{r}'].value.startswith('=INDEX(VarLab')
                 and wsf[f'A{r}'].value]                 # v2.4: label rows (A empty) name the block, no code
    for col in 'HIJ':
        ok &= uniform(wsf, [(r, CI(col)) for r in described], f'column {col}')[0]
    for g, *_ in B.SCENARIOS:
        code = B.group_cols(g)[0]
        blank = {r for r in described if wsf.cell(r, code).value is None}   # v7.2 (codes R7): the copy rows carry no
        own = {r for r in described if 'RowCode' in str(wsf.cell(r, code).value)}   # v7.2: rows coded by the map
        ok &= uniform(wsf, [(r, code) for r in described if r not in blank | own], f'code column {L(code)} (scenario {g})')[0]
        if own:
            ok &= uniform(wsf, [(r, code) for r in own], f'code column {L(code)} (scenario {g}), rows with their own code')[0]
        good = len(blank) == (18 if hasattr(B, 'copy_rows') else 0)       # code: the 18 copies of v7.2
        ok &= good
        log(f'- code column {L(code)}: {len(blank)} rows without a code (the section 11 copies, R7) '
            f'{"OK" if good else "FAIL " + str(sorted(blank)[:8])}')
    k1, k2 = B.group_cols(1)[0], B.group_cols(2)[0]
    h = B.SUB_HEAD['rod']
    expected = [(h + B.VOFF['ener'] + 2, k1, f'{ISO.lower()}.mit.ener.rod.gso.e.1', 'Fuel use | Road | Gasoline'),
                (B.prow('sp', 'coa.pow'), k1, f'{ISO.lower()}.mit.sp.pow.coa.a.1', 'Supply cost (pre-tax price) | Power | Coal'),
                (B.prow('rpb', 'gso.all'), k2, f'{ISO.lower()}.mit.rpb.all.gso.a.2',
                 'Retail price before new taxes and subsidies | All sectors | Gasoline'),   # v5.2: label of the dictionary
                (B.R_GP0, k1, f'{ISO.lower()}.mit.gp.int.oil.1', 'International energy price (real; source and adjustment from '
                                                     'MTInputs) | International | Crude oil'),
                (B.R_CPI, k1, f'{ISO.lower()}.mit.infl.1', None),
                (h + B.VOFF['ets'] + 1, k2, f'{ISO.lower()}.mit.ets.rod.nga.a.2', 'New ETS cost in the fuel price (tax-equivalent, auctioned part) | Road | Natural gas'),
                (B.prow('esub', 'die.all'), k1, f'{ISO.lower()}.mit.esub.all.die.a.1',
                 'Existing consumer subsidy (negative part of txo; negative = subsidy) | All sectors | Diesel'),
                (B.R_POL['ets.p'], k2, f'{ISO.lower()}.mit.ets.p.2', None),
                (h + B.VOFF['rnew'] + 2, k2, f'{ISO.lower()}.mit.rnew.rod.gso.2', None),
                (B.R_REV['rsub.tra'], k1, f'{ISO.lower()}.mit.rsub.tra.all.1', None),
                (B.R_REV['rtot.chg'], k2, f'{ISO.lower()}.mit.rtot.chg.all.all.2', None),
                (h + B.VOFF['co2'] + 3, k1, f'{ISO.lower()}.mit.co2.rod.die.e.1', 'CO2 emissions from fuel combustion | Road | Diesel'),
                (B.R_EMI['co2.f.nga'], k2, f'{ISO.lower()}.mit.co2.all.nga.e.2', None),
                (B.R_EMI['co2.pct'], k2, f'{ISO.lower()}.mit.co2.pct.all.all.2', None),
                (h + B.VOFF['atp'] + 2, k2, f'{ISO.lower()}.mit.atp.rod.gso.e.2', 'After-tax price | Road | Gasoline'),
                (h + B.VOFF['ctxnew'] + 3, k2, f'{ISO.lower()}.mit.ctxnew.rod.die.a.2', 'New carbon tax | Road | Diesel'),
                (h + B.VOFF['shp'] + 2, k1, f'{ISO.lower()}.mit.shp.rod.gso.1', None),
                (h, k1, f'{ISO.lower()}.mit.ener.rod.all.e.1', 'Fuel use | Road | All fuels'),
                (B.SEC_SUM['tra'], k1, f'{ISO.lower()}.mit.ener.tra.all.e.1', 'Fuel use | Transport | All fuels'),
                (B.R_CP, k2, f'{ISO.lower()}.mit.cptraj.2', 'Carbon price trajectory used'),
                (B.R_POL['sc.oen'], k1, f'{ISO.lower()}.mit.ctcov.oen.all.1', None),
                (B.R_TOTAL, k2, f'{ISO.lower()}.mit.ener.all.all.e.2', 'Fuel use | All sectors | All fuels'),
                (B.R_PW[('gnc', 'nga')], k1, f'{ISO.lower()}.mit.gnc.pow.nga.1',
                 'Generation cost before new policies (cost recovery) | Power | Natural gas'),
                (B.R_PW[('caxav', 'sol')], k2, f'{ISO.lower()}.mit.caxav.pow.sol.2', None),
                (B.R_PW[('gncav', '')], k1, f'{ISO.lower()}.mit.gncav.1', 'Average generation cost (weighted by generation shares)'),
                (B.R_PW[('rp', 'res')], k2, f'{ISO.lower()}.mit.rp.res.ecy.2', 'End-user electricity price | Residential | Electricity'),
                (B.R_PW[('msc', '')], k1, f'{ISO.lower()}.mit.msc.1', None),
                (B.R_PW[('ccp', 'oop')], k2, f'{ISO.lower()}.mit.ccp.pow.oop.2', None),
                (B.R_PW[('gen', 'sol')], k1, f'{ISO.lower()}.mit.gen.pow.sol.1', 'Generation | Power | Solar'),
                (B.R_PW[('dem', 'srv')], k2, f'{ISO.lower()}.mit.dem.srv.ecy.2', None),
                (B.R_PW[('mult', 'tra')], k1, f'{ISO.lower()}.mit.mult.tra.ecy.1', None),
                (B.R_EMI['co2.pow'], k1, f'{ISO.lower()}.mit.co2.pow.all.e.1', 'CO2 emissions from fuel combustion | Power | All fuels')]
    for r, c, code, label in expected:
        got, lab = wsv.cell(r, c).value, wsv[f'H{r}'].value
        code = RC(code)
        good = got == code and (label is None or lab == label)
        ok &= good
        log(f'- {L(c)}{r}: `{got}` | {lab} {"OK" if good else "FAIL (expected " + code + ")"}')
    return ok


def check_outline(wsf):
    ok = wsf.sheet_properties.outlinePr.summaryBelow is True
    log(f'- row group buttons below the groups (summaryBelow): {"OK" if ok else "FAIL"}')
    lv = lambda r: (wsf.row_dimensions[r].outlineLevel or 0, bool(wsf.row_dimensions[r].hidden))
    checks = []
    for band, tot, last in B.SECTION_GROUPS:     # v2.6: one group per section; only its summary row shows
        inner = list(range(band + 1, tot if tot else last + 1))
        checks.append((f'section at row {band}: rows {band + 1}-{(tot or last + 1) - 1} grouped and hidden', inner,
                       (1, True)))
        checks.append((f'section at row {band}: band and summary row visible', [band] + ([tot] if tot else []),
                       (0, False)))
    lvl = {r: wsf.row_dimensions[r].outlineLevel or 0 for r in range(1, wsf.max_row + 2)}
    one = max(lvl.values()) == 1 and wsf.sheet_format.outlineLevelRow == 1
    ok &= one
    log(f'- one level of row groups (v2.4, no nesting): max level {max(lvl.values())} {"OK" if one else "FAIL"}')
    rolled = all(wsf.row_dimensions[r].hidden for r in lvl if lvl[r])
    flags = all(bool(wsf.row_dimensions[r + 1].collapsed) == (lvl[r + 1] < lvl[r])
                for r in range(1, wsf.max_row) if lvl[r])
    ok &= rolled and flags
    log(f'- opens rolled up: every grouped row hidden; collapsed flag on the row after each group '
        f'{"OK" if rolled and flags else "FAIL"}')
    wbf = openpyxl.load_workbook(B.OUT)
    first = (wbf.sheetnames[:5] == ['Cover', 'ScenarioCompare', 'ScenarioDefinition', 'MAIN->>', 'Mitigation']
             and wbf.active.title == 'ScenarioCompare')   # v4.2; v6.7: the front tabs, opens on the dashboard
    zoom = wbf['Mitigation'].sheet_view.zoomScale == 75
    ok &= first and zoom
    log(f'- front tabs Cover, ScenarioCompare, ScenarioDefinition, then MAIN->> and Mitigation; opens on '
        f'ScenarioCompare: {"OK" if first else "FAIL"}; Mitigation zoom 75%: '
        f'{"OK" if zoom else "FAIL"}')
    want = B.TAB_ORDER                                   # v3.6: consolidated tabs; reference group last
    tail = ['REF->>'] + [t for t, _b in B.MERGES[2:]]
    tabs = wbf.sheetnames[:len(want)] == want and wbf.sheetnames[-len(tail):] == tail
    ok &= tabs
    log(f'- tab groups MAIN->>, INPUTS->>, DATA->>, REF->> (last) in that order: {"OK" if tabs else "FAIL " + str(wbf.sheetnames[:22])}')
    for label, rows, exp in checks:
        good = all(lv(r) == exp for r in rows)
        ok &= good
        log(f'- {label}: {len(rows)} rows at level {exp[0]}, {"hidden" if exp[1] else "visible"} '
            f'{"OK" if good else "FAIL"}')
    return ok


def check_mtinputs():
    tpl = openpyxl.load_workbook(B.MT_TEMPLATE)['MTInputs']
    ws = openpyxl.load_workbook(B.OUT)['ScenarioDefinition']
    diffs = [f'{L(c)}{r}' for r in range(1, tpl.max_row + 1) for c in range(1, 9)
             if tpl.cell(r, c).value != ws.cell(r, c).value
             and (r, c) != (B.MT_ROW_SHORT, 8)]          # v6.7: H2 labels the short names (legends) of row 2
    ok = not diffs and ws.column_dimensions['D'].hidden and ws.column_dimensions['E'].hidden
    log(f'- columns A:H, rows 1-{tpl.max_row}: {len(diffs)} cells differ from the template; D:E hidden '
        f'{"OK" if ok else "FAIL " + str(diffs[:10])}')
    return ok


def check_format(wsf):
    bands = [3, B.B_POL, B.B_PRI, B.B_POW, B.B_RES, B.B_REV, B.B_EMI] + list(B.SEC_BAND.values())
    t_ = lambda r: 'B'                                # v3.9: number in A, title in B (legacy band)
    ok = all(str(wsf[f'{t_(r)}{r}'].font.color.rgb).endswith('FFFFFF') and wsf[f'{t_(r)}{r}'].font.b for r in bands)
    texts = [str(wsf[f'{t_(r)}{r}'].value)[:22] for r in sorted(bands)]
    log(f'- section bands {texts}: white bold text {"OK" if ok else "FAIL"}')
    ip = B.tab(openpyxl.load_workbook(B.OUT), 'Inputs_prices')
    marked = sorted({ip.cell(B.IP_HDR, c.column).value[:40] for row in ip.iter_rows(min_row=B.IP_R0, max_row=B.IP_R1)
                     for c in row if c.fill.start_color.rgb.endswith('FFFF00')})
    oop = B.IP_R0 + [pc for pc, _l in B.PRICES].index('oop.all')
    good = (all(ip[f'{B.IPC[k]}{r}'].fill.start_color.rgb.endswith('FFFF00') for k in ('vatc', 'vrx')
                for r in range(B.IP_R0, B.IP_R1 + 1))
            and all(ip[f'{B.IPC[k]}{oop}'].fill.start_color.rgb.endswith('FFFF00') for k in ('pccr', 'mar')))
    ok &= good
    pdm = openpyxl.load_workbook(B.OUT)['Prices_dom']
    with open(os.path.join(HERE, '..', '..', 'data', 'mvp_legacy_extracts', 'prices_dom_changes.csv'), encoding='utf-8') as f:
        ch = list(csv.DictReader(f))
    hdr = {pdm.cell(5, j).value: j for j in range(1, pdm.max_column + 1)}
    rowi = {pdm.cell(i, 1).value: i for i in range(6, pdm.max_row + 1)}
    n_marked = sum(1 for c in ch if pdm.cell(rowi[c['country_year']], hdr[c['column']]).fill.start_color.rgb.endswith('FFFF00'))
    vals = all(abs(float(pdm.cell(rowi[c['country_year']], hdr[c['column']]).value or 0) - float(c['new'] or 0)) < 1e-9
               for c in ch)
    unmarked_other = sum(1 for i in range(6, pdm.max_row + 1) for j in range(6, pdm.max_column + 1)
                         if not str(pdm.cell(i, 1).value).startswith(ISO)
                         and pdm.cell(i, j).fill.start_color.rgb.endswith('FFFF00'))
    good = n_marked == len(ch) and vals and unmarked_other == 0
    ok &= good
    log(f'- Prices_dom: {n_marked} of {len(ch)} changed Egypt cells bright yellow with the new values; no other '
        f'country marked {"OK" if good else "FAIL"}')
    ld = B.tab(openpyxl.load_workbook(B.OUT), 'LegacyDiff')
    n_ld = sum(1 for r in range(5, ld.max_row + 1) if ld.cell(r, 2).value)
    names = openpyxl.load_workbook(B.OUT).sheetnames
    good_ld = n_ld == len(B.LEGACY_DIFFS) >= 20 and B.TAB_REF in names    # v2.6: tab order checked in section 8
    ok &= good_ld
    log(f'- tabs {names[:8]}; sheet LegacyDiff: {n_ld} differences listed {"OK" if good_ld else "FAIL"}')
    log(f'- Inputs_prices: data changed by assumption marked bright yellow (columns {marked}; other oil products '
        f'pass-through and margin) {"OK" if good else "FAIL"}')
    return ok


def check_sanity(ws):
    ok = True
    (_, b1, y1), (_, b2, y2) = B.group_cols(1), B.group_cols(2)
    cols1, cols2, years = [b1] + y1, [b2] + y2, [B.BASE_YEAR] + B.YEARS
    pre = max(abs(ws.cell(r, x).value - ws.cell(r, y).value) for r, *_ in B.var_rows('ener')
              for x, y, yr in zip(cols1, cols2, years) if yr < 2027)
    ok &= pre < TOL
    log(f'- scenario 1 vs 2 before 2027 (fuel use): max abs diff {pre:.3g} {"OK" if pre < TOL else "FAIL"}')
    oen = max(abs(ws.cell(r, y).value) for r, s, f in B.var_rows('ctxnew') if s == 'oen' for y in cols2)
    ok &= oen < TOL                  # v3.1: its fuel use now moves with GDP (section 16), so test the tax itself
    log(f'- other energy use not taxed (MCovOen FALSE): new carbon tax ctxnew in scenario 2 = 0, max abs {oen:.3g} '
        f'{"OK" if oen < TOL else "FAIL"}')
    chk = max(abs(ws.cell(B.R_CHK, c).value) for c in cols1 + cols2)
    secs = max(abs(sum(ws.cell(B.SEC_SUM[g], c).value for g in B.SEC_SUM) + ws.cell(B.R_EPOW, c).value
                   - ws.cell(B.R_TOTAL, c).value) for c in cols1 + cols2)
    ok &= chk < 1e-6 and secs < 1e-6
    log(f'- check row {B.R_CHK}: max abs {chk:.3g}; sector totals and power sum to total: max abs {secs:.3g} '
        f'{"OK" if chk < 1e-6 and secs < 1e-6 else "FAIL"}')
    ip = B.tab(openpyxl.load_workbook(recalc_path(B.OUT), data_only=True), 'Inputs_prices')
    pcc = {ip.cell(r, CI(B.IPC['key'])).value: ip.cell(r, CI(B.IPC['pcc'])).value for r in range(B.IP_R0, B.IP_R1 + 1)}
    flat = [pc for pc, _l in B.PRICES if pcc[pc] == 0]
    i_l = years.index(B.LAST_HIST)
    rows = {pc: r for (r, *_), (pc, _l) in zip(rows_of('rpb'), B.PRICES)}
    dflat = max(abs(ws.cell(rows[pc], c).value - ws.cell(rows[pc], cols1[i_l]).value) for pc in flat
                for c in cols1[i_l:-1])
    ok &= dflat < 1e-9
    log(f'- pass-through 0 ({", ".join(flat)}): retail price before new policies stays at its {B.LAST_HIST} '
        f'value, max abs diff {dflat:.3g} {"OK" if dflat < 1e-9 else "FAIL"}')
    log('')
    log('Retail price before new policies, scenario 1 (real $/GJ of ResultsYear), and chosen pass-through:')
    log('')
    log('| Price fuel | pass-through | 2022 | 2024 | 2027 | 2030 | 2040 | VAT 2024 | existing tax 2024 | '
        'existing subsidy 2024 | subsidy per price unit 2024 |')
    log('|---|---|---|---|---|---|---|---|---|---|---|')
    i24 = cols1[years.index(2024)]
    for pc, _l in B.PRICES:
        vals = [ws.cell(rows[pc], cols1[years.index(y)]).value for y in (2022, 2024, 2027, 2030, 2040)]
        k = [pc2 for pc2, _l2 in B.PRICES].index(pc)
        ext = [ws.cell(B.prow(v, pc), i24).value for v in ('vat', 'etx', 'esub', 'esubpu')]
        log(f'| {pc} | {pcc[pc]:g} | ' + ' | '.join(f'{v:.3f}' for v in vals + ext) + ' |')
    rsum = max(abs(sum(ws.cell(B.R_REV[f'{v}.{g}'], c).value for g in [g_ for _n, g_, _t in B.SECTIONS] + ['pow'])
                   - ws.cell(B.R_REV[f'{v}.all'], c).value) for v in B.REV_VARS for c in cols1 + cols2)
    zero_new = max(abs(ws.cell(B.R_REV['rnew.all'], c).value) for c in cols1)
    good = rsum < 1e-6 and zero_new < TOL
    ok &= good
    log(f'- revenues: sectors and power sum to totals (max abs {rsum:.3g}); no new-policy revenue in scenario 1 '
        f'(max abs {zero_new:.3g}) {"OK" if good else "FAIL"}')
    esum = max(max(abs(sum(ws.cell(B.R_EMI[f'co2.{g}'], c).value for _n, g, _t in B.SECTIONS)
                       + ws.cell(B.R_EMI['co2.pow'], c).value - ws.cell(B.R_EMI['co2.all'], c).value),
                   abs(sum(ws.cell(B.R_EMI[f'co2.f.{f}'], c).value for f, *_x in B.FUELS)
                       - ws.cell(B.R_EMI['co2.all'], c).value)) for c in cols1 + cols2)
    bio = max(abs(ws.cell(B.R_EMI['co2.f.bio'], c).value) for c in cols1 + cols2)
    pre = max(abs(ws.cell(B.R_EMI['co2.chg'], c).value - ws.cell(B.R_EMI['co2.pow'], c).value
                  + ws.cell(B.R_EMI['co2.pow'], c1).value) for c, c1, yr in zip(cols2, cols1, years) if yr < 2027)
    pre_pow = max(abs(ws.cell(B.R_EMI['co2.pow'], c).value - ws.cell(B.R_EMI['co2.pow'], c1).value)
                  for c, c1, yr in zip(cols2, cols1, years) if yr < 2027)
    good = esum < 1e-9 and bio < TOL and pre < TOL
    ok &= good
    log(f'- CO2: sectors incl. power and fuels sum to the total (max abs {esum:.3g}); biomass 0; no change vs scenario 1 '
        f'before 2027 outside power (max abs {pre:.3g}) {"OK" if good else "FAIL"}')
    log(f'  - power CO2 before 2027 differs by up to {pre_pow:.3f} MtCO2: investment looks ahead (levelised variable cost '
        f'includes the future carbon price), as legacy')
    log('')
    log('CO2 emissions from fuel combustion incl. power generation (MtCO2; no process emissions):')
    log('')
    log('| Year | Scenario 1 | Scenario 2 | Change | Transport | Buildings | Industry | Other | Power (scen. 2) |')
    log('|---|---|---|---|---|---|---|---|---|')
    for x, y, yr in zip(cols1, cols2, years):
        if yr in (2022, 2024, 2027, 2030, 2035, 2040):
            a, b = ws.cell(B.R_EMI['co2.all'], x).value, ws.cell(B.R_EMI['co2.all'], y).value
            secs = [ws.cell(B.R_EMI[f'co2.{g}'], y).value for _n, g, _t in B.SECTIONS] + [ws.cell(B.R_EMI['co2.pow'], y).value]
            log(f'| {yr} | {a:,.1f} | {b:,.1f} | {b / a - 1:+.1%} | ' + ' | '.join(f'{v:,.1f}' for v in secs) + ' |')
    log('')
    log('Revenues (USD million, real 2026):')
    log('')
    log('| Year | existing taxes | existing subsidies | new policies | total | change vs scenario 1 |')
    log('|---|---|---|---|---|---|')
    for g, cols in ((1, cols1), (2, cols2)):
        for x, yr in zip(cols, years):
            if yr in (2022, 2027, 2030, 2040):
                vals = [ws.cell(B.R_REV[k], x).value for k in ('rtx.all', 'rsub.all', 'rnew.all', 'rtot.all',
                                                               'rtot.chg')]
                log(f'| {yr} (scenario {g}) | ' + ' | '.join(f'{v:,.0f}' for v in vals) + ' |')
    log('')
    log('| Year | Scenario 1 (ktoe) | Scenario 2 (ktoe) | Change |')
    log('|---|---|---|---|')
    for x, y, yr in zip(cols1, cols2, years):
        if yr in (2022, 2023, 2024, 2026, 2027, 2030, 2035, 2040):
            a, b = ws.cell(B.R_TOTAL, x).value, ws.cell(B.R_TOTAL, y).value
            log(f'| {yr} | {a:,.0f} | {b:,.0f} | {b / a - 1:+.1%} |')
    return ok


def check_power_results(ws):
    """Power block: properties that must hold, and the key numbers of scenarios 1 and 2."""
    (_, b1, y1), (_, b2, y2) = B.group_cols(1), B.group_cols(2)
    cols1, cols2, years = [b1] + y1, [b2] + y2, [B.BASE_YEAR] + B.YEARS
    row = lambda v, m='': B.R_PW[(v, m)]
    val = lambda v, m, c: ws.cell(row(v, m), c).value
    tech = [f for f, _n in B.PW_TECH]
    ok = True
    ccp1 = max(abs(ws.cell(r, c).value) for r, v, *_ in B.PW_ROWS if v in ('ccp', 'ccpav', 'rcarb') for c in cols1)
    vbc = max(abs(val('vbc', f, x) - val('vbc', f, y)) for f in tech for x, y in zip(cols1, cols2))
    shares = max(abs(sum(val('shr', f, c) for f in tech) - 1) for c in cols1 + cols2)
    good = ccp1 < TOL and vbc < TOL and shares < 1e-9
    ok &= good
    log(f'- scenario 1: no new policy cost in power (max abs {ccp1:.3g}); variable costs before policy equal in '
        f'scenarios 1 and 2 (max abs {vbc:.3g}); generation shares sum to 1 (max abs {shares:.3g}) '
        f'{"OK" if good else "FAIL"}')
    meet = max(abs(val('gtot', '', c) - val('req', '', c)) for c in cols1[1:] + cols2[1:])
    cap = max(abs(val('cap', f, c) - (val('cap', f, c - 1) - val('ret', f, c - 1) + val('nim', f, c - 1)))
              for f in tech for c in cols1[1:] + cols2[1:])
    over = max(sum(val('nei', f, c) for f in tech) - val('need', '', c) for c in cols1 + cols2)
    resid = [(B.year_of(c), val('need', '', c) - sum(val('nei', f, c) for f in tech)) for c in cols1]
    neg = min(val('nei', f, c) for f in tech for c in cols1 + cols2)
    good = meet < 1e-6 and cap < 1e-6 and over < 1e-6 and neg > -1e-9
    ok &= good
    log(f'- generation = required generation from {B.YEARS[0]} (max abs {meet:.3g} MWy); capacity = last year less '
        f'retirements plus new nameplate investment (max abs {cap:.3g} MW); new effective investment >= 0 and at most the '
        f'capacity needed (max excess {over:.3g} MW) {"OK" if good else "FAIL"}')
    log('  - scale-up limits leave investment unplaced (MW, scenario 1; gas then runs at a higher capacity factor, as '
        'legacy): ' + (', '.join(f'{y} {x:,.0f}' for y, x in resid if x > 1e-6) or 'none'))
    lag = max(abs(val('sc', g, c) - val('gncav', '', c - 1) - (val('sc', g, cols1[1]) - val('gncav', '', cols1[0])))
              for g, _l in B.PW_GROUPS for c in cols1[1:])
    ok &= lag < TOL
    log(f'- supply cost = average generation cost of the previous year + constant T&D add-on (max abs {lag:.3g}) '
        f'{"OK" if lag < TOL else "FAIL"}')
    c40_1, c40_2 = cols1[-1], cols2[-1]
    # v5.2: the carbon price shifts the investment choice (cost-based logit shares pni) towards wind, solar and other
    # renewables in every year, and lowers power CO2. The VRE share of generation is reported only: since the data
    # fixes of v4.10 (L52-L56) and L67 (v4.14) the lower demand of scenario 2 lowers new investment, wind and solar
    # stay at their scale-up caps (a share of the smaller total effective capacity) and the existing gas fleet runs
    # more, so the VRE share of generation can fall (Egypt 2041: 0.394 -> 0.387) although CO2 falls.
    vre_t = [f for f in tech if f in ('wnd', 'sol', 'ore')]
    pni = lambda c: sum(val('pni', f, c) for f in vre_t)
    shift = min(pni(y) - pni(x) for x, y in zip(cols1, cols2))
    good = shift >= -TOL and \
        ws.cell(B.R_EMI['co2.pow'], c40_2).value <= ws.cell(B.R_EMI['co2.pow'], c40_1).value
    ok &= good
    log(f'- carbon price (scenario 2) shifts the investment choice towards renewables (wind, solar, other renewables '
        f'share of the investment logit not lower in any year: min change {shift:+.4f}; {B.LAST_YEAR} '
        f'{pni(c40_1):.3f} -> {pni(c40_2):.3f}) and lowers power CO2 ({ws.cell(B.R_EMI["co2.pow"], c40_1).value:.2f} -> '
        f'{ws.cell(B.R_EMI["co2.pow"], c40_2).value:.2f} MtCO2); VRE share of generation (memo) '
        f'{val("vre", "", c40_1):.3f} -> {val("vre", "", c40_2):.3f} {"OK" if good else "FAIL"}')
    log('')
    log('Power, scenario 1 (baseline) and 2 (carbon price $20 from 2027):')
    log('')
    log('| Year | generation TWh (1) | (2) | gas share (1) | (2) | VRE share (1) | (2) | power CO2 Mt (1) | (2) | '
        'price res $/kWh (1) | (2) | capacity GW (1) | investment USD m (1) |')
    log('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for k, yr in enumerate(years):
        if yr in (2022, 2023, 2025, 2027, 2030, 2035, 2040):
            c1, c2 = cols1[k], cols2[k]
            v = [val('gtot', '', c1) * K['MWyMkWh'] / 1000, val('gtot', '', c2) * K['MWyMkWh'] / 1000, val('shr', 'nga', c1),
                 val('shr', 'nga', c2), val('vre', '', c1), val('vre', '', c2), ws.cell(B.R_EMI['co2.pow'], c1).value,
                 ws.cell(B.R_EMI['co2.pow'], c2).value, val('rp', 'res', c1), val('rp', 'res', c2),
                 sum(val('cap', f, c1) for f in tech) / 1000, val('usdtot', '', c1)]
            fm = ['{:.1f}', '{:.1f}', '{:.3f}', '{:.3f}', '{:.3f}', '{:.3f}', '{:.1f}', '{:.1f}', '{:.4f}', '{:.4f}',
                  '{:.1f}', '{:,.0f}']
            log(f'| {yr} | ' + ' | '.join(f_.format(x) for f_, x in zip(fm, v)) + ' |')
    log('')
    log('Generation cost by type, scenario 1, 2022 and 2040 ($/kWh): ' + ', '.join(
        f'{n} {val("gnc", f, cols1[0]):.3f} / {val("gnc", f, cols1[-1]):.3f}' for f, n in B.PW_TECH))
    return ok


def lam_cols(sheet):
    """v4.15: columns of the LAMBDA test group (v4.3: group 3 calls the LAMBDA of every row in every year) and the
    spacer test column on its left, which compares group 3 with group 2 (Mitigation and Distribution)."""
    if sheet == 'Mitigation':
        code = B.group_cols(B.LAMBDA_GROUP)[0]
        return set(range(code - 1, code + B.GW - 1))
    if sheet == 'Distribution':
        code = B.dist_group_cols(B.LAMBDA_GROUP)[0]
        return set(range(code - 1, code + B.DGW - 1))
    return set()


def check_formula_length():
    """v1.07: every plain cell formula of the shipped workbook has at most 100 characters (as Excel shows it, without
    the file prefixes _xlfn. / _xlpm.); v2.3: cells that call a named LAMBDA sit in the LAMBDA year 2041 of
    Mitigation only (their arguments may make them longer)."""
    last = {B.group_cols(g)[2][-1] for g, *_ in B.SCENARIOS}
    misplaced = []
    wb = openpyxl.load_workbook(B.OUT)
    n, worst, over, lam_calls = 0, (0, ''), [], 0
    for ws in wb.worksheets:
        lam3 = lam_cols(ws.title)
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and v.startswith('='):
                    k = len(v.replace('_xlfn.', '').replace('_xlpm.', ''))
                    n += 1
                    is_lam = bool(LAMBDA_CALL.search(v))
                    lam_calls += is_lam
                    if is_lam and not ((ws.title == 'Mitigation' and c.column in last) or c.column in lam3):
                        misplaced.append(f'{ws.title}!{c.coordinate}')
                    if is_lam:
                        continue
                    if k > worst[0]:
                        worst = (k, f'{ws.title}!{c.coordinate}')
                    if k > 100:
                        over.append(f'{ws.title}!{c.coordinate}')
    ok = not over and not misplaced and lam_calls > 0
    names = [d for d in wb.defined_names if d not in B.LAMBDAS]
    log(f'- LAMBDA calls only in the LAMBDA year {B.LAST_YEAR} of Mitigation and the LAMBDA test group '
        f'{B.LAMBDA_GROUP} (Mitigation, Distribution): {lam_calls} cells '
        f'{"OK" if not misplaced and lam_calls else "FAIL " + str(misplaced[:8])}')
    longest = max((len(B.lambda_xml(k).replace('_xlfn.', '').replace('_xlpm.', '')), k) for k in B.LAMBDAS)
    log(f'- {n} cell formulas in {len(wb.worksheets)} sheets ({lam_calls} call a named LAMBDA): longest plain {worst[0]} '
        f'characters ({worst[1]}); over 100: {len(over)} {"OK" if ok else "FAIL " + str(over[:8])}')
    log(f'- {len(B.LAMBDAS)} named LAMBDAs (longest: {longest[1]}, {longest[0]} characters); {len(names)} defined '
        f'names for data tables and fixed ranges: {", ".join(names)}')
    return ok


ALLOWED = [(re.compile(r'"High",2,IF\(LEFT\([^)]*\)="Low",3,1\)'), 'choice codes of gp.adj (1 none, 2 High, 3 Low)'),
           (re.compile(r'AGGREGATE\(1,6,'), 'AGGREGATE function codes (average, skip errors)'),
           (re.compile(r'LEFT\(([^(),]|\([^()]*\))+,\d\)'), 'text length in LEFT(switch, n) = "Yes" / "High" ...'),
           (re.compile(r'\+2\*MAX\(0,'), 'functional form of the long-term storage cost (legacy: 2 x, squared)'),
           (re.compile(r'\)\^2\*'), 'functional form of the long-term storage cost (squared)')]


def check_v24_layout(ws):
    """v2.4 (user rules 2026-10-13): years in row 1; a label row names D:G above every block, so every number in
    D:G is labelled; no constant typed or written into a Mitigation formula (only 0 and 1, function codes, text
    lengths and the functional form of the storage cost; inputs: the scenario number and the ETS override row)."""
    ok = True
    groups = [g for g, *_ in B.SCENARIOS]
    yr = all(ws.cell(1, c).value == B.BASE_YEAR + k for g in groups
             for k, c in enumerate([B.group_cols(g)[1]] + B.group_cols(g)[2]))
    ok &= yr
    log(f'- years in row 1 of every scenario group ({B.BASE_YEAR}-{B.LAST_YEAR}): {"OK" if yr else "FAIL"}')
    wbf = openpyxl.load_workbook(B.OUT)
    wf = wbf['Mitigation']
    nums, unlabelled, lab_rows = 0, [], 0
    for r in range(B.R_DEFL + 1, wf.max_row + 1):
        d = wf.cell(r, 4).value
        if isinstance(d, str) and 'VarP1' in d:
            lab_rows += 1
            continue
        a_ = wf.cell(r, 1).value              # variable rows (band rows hold a title in A)
        if a_ and ' ' not in str(a_) and any(wf.cell(r, c).value not in (None, '') for c in range(4, 8)):
            nums += 1
            a = r - 1
            while a > B.R_DEFL and not (isinstance(wf.cell(a, 4).value, str) and 'VarP1' in wf.cell(a, 4).value):
                a -= 1
            lab = [ws.cell(a, c).value for c in range(4, 8)]
            used = [c for c in range(4, 8) if wf.cell(r, c).value not in (None, '')]
            if a == B.R_DEFL or any(not ws.cell(a, c).value for c in used):
                unlabelled.append(r)
    good = not unlabelled and nums > 1000
    ok &= good
    log(f'- {lab_rows} label rows; {nums} rows with values in D:G, each with a label in its label row above for every '
        f'column it uses: {"OK" if good else "FAIL " + str(unlabelled[:10])}')
    allowed_typed = {(B.R_SCEN, B.group_cols(1)[0])}
    ovr = B.R_POL['ets.ovr']
    typed, lits = [], {}
    for row in wf.iter_rows(min_row=B.R_DEFL + 1):
        for c in row:
            v = c.value
            if isinstance(v, (int, float, bool)) and c.row != ovr:
                typed.append(c.coordinate)
            elif isinstance(v, str) and v.startswith('=') and not LAMBDA_CALL.search(v):
                x = v
                for rx, _why in ALLOWED:
                    x = rx.sub('', x)
                x = re.sub(r'"[^"]*"', '""', x)
                x = re.sub(r"\$?[A-Z]{1,3}\$?\d+", 'R', x)
                for m in re.finditer(r'(?<![A-Za-z_\d.])(\d+\.?\d*)', x):
                    if m.group(1) not in ('0', '1'):
                        lits.setdefault(m.group(1), c.coordinate)
    for wso in wbf.worksheets:                     # v3.4: every other sheet's formulas too (data cells are data)
        if wso.title == 'Mitigation':
            continue
        for row in wso.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and v.startswith('=') and not LAMBDA_CALL.search(v):
                    x = v
                    for rx, _why in ALLOWED:
                        x = rx.sub('', x)
                    x = re.sub(r'"[^"]*"', '""', x)
                    x = re.sub(r"'[^']*'!", '', x)
                    x = re.sub(r"\$?[A-Z]{1,3}\$?\d+", 'R', x)
                    for m in re.finditer(r'(?<![A-Za-z_\d.])(\d+\.?\d*)', x):
                        if m.group(1) not in ('0', '1'):
                            lits.setdefault(m.group(1), f'{wso.title}!{c.coordinate}')
    typed = [t for t in typed if t != f'{B.L(B.group_cols(1)[0])}{B.R_SCEN}']   # scenario number of group 1 (input)
    good = not typed and not lits
    ok &= good
    log(f'- no typed numbers below the top rows (inputs: scenario number {B.L(B.group_cols(1)[0])}{B.R_SCEN}, ETS '
        f'override row ets.ovr) and no numeric constants in the formulas of any sheet: {"OK" if good else "FAIL " + str(typed[:8]) + " " + str(lits)}')
    log('  allowed in formulas besides 0 and 1: ' + '; '.join(w for _rx, w in ALLOWED))
    cst = B.tab(wbf, 'Constants')
    named = all(n in wbf.defined_names for n, *_r in B.NAMED_CONSTANTS)
    ok &= named
    log(f'- sheet Constants: {len(B.NAMED_CONSTANTS)} named constants ({", ".join(n for n, *_r in B.NAMED_CONSTANTS)}) '
        f'and {len(B.POLICY_CONSTANTS)} policy assumptions by key {"OK" if named else "FAIL"}; MWyMkWh = '
        f'{cst.cell(B.CONST_ROW["MWyMkWh"], 2).value}')
    heads = {r for r in range(1, wf.max_row + 1) if wf.cell(r, 2).font.u and wf.cell(r, 2).value}   # v3.9: headings
    labs = {r for r in range(1, wf.max_row + 1) if wf.cell(r, 8).font.b and wf.cell(r, 8).border.bottom.style == 'thin'}
    keep = B.BAND_ROWS | heads | labs                 # v3.9: sub-headings and label (header) rows are bold
    bold = [f'{c}{r}' for r in range(1, wf.max_row + 1) for c in 'ABC' if wf[f'{c}{r}'].font.b and r not in keep
            and r > 1]
    fills = [f'{c}{r}' for r in range(1, wf.max_row + 1) for c in B.PARAM_COLS if r not in B.BAND_ROWS
             and wf[f'{c}{r}'].fill.fill_type]
    good = not bold and not fills
    ok &= good
    log(f'- v2.6: variable, fuel and sector names (A:C) never bold; no fill colour in D:G outside the bands: '
        f'{"OK" if good else "FAIL " + str(bold[:5]) + str(fills[:5])}')
    sums = {t for _b, t, _z in B.SECTION_GROUPS if t}
    sums |= {B.prow('rpn', pc) for pc, _l in B.PRICES} | B.SUMMARY2   # v5.2: the retail price incl. new policies of
    # each price block and the second summary rows (change vs scenario 1) are bold since v4.1 (builder BOLD_ROWS,
    # filled only while building; SUMMARY2)
    bold = [f'{L(c)}{r}' for r in range(B.B_POL + 1, wf.max_row + 1) if r not in keep and r not in sums
            for c in range(1, wf.max_column + 1) if wf.cell(r, c).font.b]
    green = [f'A{r}' for r in range(2, wf.max_row + 1) if r not in B.BAND_ROWS and wf.cell(r, 1).value
             and not str(wf.cell(r, 1).value)[:1].isdigit()
             and (str(wf.cell(r, 1).font.color.rgb if wf.cell(r, 1).font.color else '')[-6:] != B.C_VARNAME
                  or wf.cell(r, 1).fill.fill_type)]
    good = not bold and not green
    ok &= good
    log(f'- v2.7: bold only on the summary rows; variable names (column A) light green text, no fill: '
        f'{"OK" if good else "FAIL " + str(bold[:5]) + str(green[:5])}')
    import zipfile
    z = zipfile.ZipFile(B.OUT)
    dr = [n for n in z.namelist() if n.startswith('xl/drawings/drawing')]
    btn = [m.decode() for n in dr for m in re.findall(rb'macro="\[0\]!(\w+)"', z.read(n))]
    good = btn == [m for _l, m in B.MACRO_BUTTONS + B.MORE_BUTTONS]   # v6.7: core then other buttons
    ok &= good
    log(f'- v2.7: macro buttons on ScenarioCompare: {", ".join(btn)} {"OK" if good else "FAIL"}')
    t2 = wf['A2'].value
    t0 = all(wf.cell(t, c).number_format == '#,##0' for _b, t, _z in B.SECTION_GROUPS if t
             for g, *_ in B.SCENARIOS for c in [B.group_cols(g)[1]] + B.group_cols(g)[2])
    bands = all(len(str(wf.cell(b, 1).value)) <= 30 for b, _t, _z in B.SECTION_GROUPS)
    good = t2 == 'Mitigation Module' and t0 and bands
    ok &= good
    log(f'- v2.7: title "{t2}", section bands at most 30 characters, summary rows without decimals: '
        f'{"OK" if good else "FAIL"}')
    from openpyxl.utils import column_index_from_string as ci_
    celllike = [n for n in wbf.defined_names
                if (m_ := re.match(r'([A-Za-z]{1,3})(\d+)', n)) and ci_(m_.group(1).upper()) <= 16384]
    good = not celllike
    ok &= good
    log(f'- v2.7: no defined name begins like a cell reference (Excel cannot parse formulas using them; v2.4-v2.6 '
        f'had BCO2Key/Val/Year): {"OK" if good else "FAIL " + str(celllike)}')
    def reflike(t):                           # A1 (or starts like one) or R1C1 (r, c, R2, C3, R2C3)
        m_ = re.match(r'([A-Za-z]{1,3})(\d+)', t)
        return bool(m_ and ci_(m_.group(1).upper()) <= 16384) or bool(re.fullmatch(r'[Rr]\d*([Cc]\d*)?|[Cc]\d*', t))
    badp = sorted({(n, p) for n, (ps, _b) in B.LAMBDAS.items() for p in ps if reflike(p)})
    good = not badp
    ok &= good
    log(f'- v2.7: no LAMBDA parameter reads as a cell reference (Excel removes every cell calling such a LAMBDA on '
        f'repair; v2.3-v2.7 first build had y1, co2, c, tco2_kwh): {"OK" if good else "FAIL " + str(badp)}')
    mp = B.tab(ws.parent, 'Mapping')                # recalculated values
    bad = [k for i, (k, row) in enumerate(B.MT_KEYS) if mp.cell(B.MAP_MT0 + i, 6).value != row]
    rows = {B.R_POL[k]: mt for k, *_r, mt in B.POL if mt}
    rows.update({B.R_PRI[p]: B.MT_NAMES[p] for p in B.PRI_PARAMS})
    bad += [r for r, mt in rows.items() if ws.cell(r, 4).value != mt]
    good = not bad
    ok &= good
    log(f'- MTInputs rows found by the Mapping table ({len(B.MT_KEYS)} keys: NameOfParameter, or label below a '
        f'heading) and looked up in Mitigation D ({len(rows)} rows) = the template rows: '
        f'{"OK" if good else "FAIL " + str(bad[:8])}')
    bco = ws.parent['BaselineCO2']
    n_b = sum(isinstance(bco.cell(4 + i, 4 + k).value, (int, float)) for i in range(len(B.COV_SECTORS))
              for k in range(B.NY))
    good = n_b == len(B.COV_SECTORS) * B.NY
    ok &= good
    log(f'- sheet BaselineCO2: {n_b} values (sectors x years) read by the bco2 rows {"OK" if good else "FAIL"}')
    n_m = sum(isinstance(bco.cell(B.BCO2_RAW + 1 + i, 4 + k).value, (int, float)) for i in range(len(B.CH4S_STORE))
              for k in range(B.NY))          # v6.2 (I47, ghg.k): stored scenario-1 methane rows
    good = n_m == len(B.CH4S_STORE) * B.NY
    ok &= good
    log(f'- sheet BaselineCO2: {n_m} methane values (dg, bm, ch4c, ch4sup x years) read by the ch4bs rows and ghg.k '
        f'{"OK" if good else "FAIL"}')
    return ok


PRET_TEST = {'nga': (2025, 1500.0), 'oop': (2024, 400.0)}   # planned retirement test: type -> (from year, MW/yr)


def check_planned_retirement():
    """Planned retirement switched on for gas and oil with data (PowerTech, PowerPaths edited as a user would):
    workbook = power_model_ref_v7_0 in scenarios 1 and 2; retirement = the data; capacity balance holds."""
    wb = openpyxl.load_workbook(B.OUT)
    pt, pp = B.tab(wb, 'Inputs_ptech'), B.tab(wb, 'Inputs_ppath')   # v5.2: the data-step blocks (v4.7; tabs
    hdr = {pt.cell(B.IPT_HDR, j).value: j for j in range(1, pt.max_column + 1)}   # PowerTech, PowerPaths before)
    years = [B.BASE_YEAR] + B.YEARS
    ycol = {pp.cell(B.IPP_HDR, j).value: j for j in range(B.IPP_Y0, pp.max_column + 1)}
    pflag, pret = [], []
    for f in POWER_TECH:
        on = f in PRET_TEST
        r = next(i for i in range(B.IPT_R0, pt.max_row + 1) if pt.cell(i, hdr['code']).value == f)
        pt.cell(r, hdr['planned_retirement']).value = 'Yes' if on else 'No'
        rp = next(i for i in range(B.IPP_R0, pp.max_row + 1) if pp.cell(i, 3).value == f'pret|{f}')
        series_ = [PRET_TEST[f][1] if on and y >= PRET_TEST[f][0] else 0.0 for y in years]
        for y, v in zip(years, series_):
            pp.cell(rp, ycol[y]).value = v
        pflag.append(1.0 if on else 0.0)
        pret.append(series_)
    ws = recalc(variant(wb, 'expand'))
    ok = True
    for g in (1, 2):
        ok &= compare(ws, g, recompute(scenario_mt(g), power={'pflag': pflag, 'pret': pret}),
                      f'planned retirement on (gas 1,500 MW/yr from 2025, oil 400 MW/yr from 2024), scenario {g} vs '
                      f'Python')
    _, b1, y1 = B.group_cols(1)
    cols = [b1] + y1
    ret = max(abs(ws.cell(B.R_PW[('ret', f)], c).value - min(PRET_TEST[f][1] if y >= PRET_TEST[f][0] else 0.0,
                                                               ws.cell(B.R_PW[('cap', f)], c).value))
              for f in PRET_TEST for c, y in zip(cols, years))
    good = ret < 1e-6
    ok &= good
    k30 = years.index(2030)
    log(f'- retirement of gas and oil = the planned data (capped at capacity), max abs diff {ret:.3g} MW; gas capacity '
        f'2030 {ws.cell(B.R_PW[("cap", "nga")], cols[k30]).value:,.0f} MW, new investment 2030 '
        f'{ws.cell(B.R_PW[("nimtot", "")], cols[k30]).value:,.0f} MW {"OK" if good else "FAIL"}')
    return ok


def check_memo(ws):
    """Electricity demand memo lines: each subsector line = power demand of the subsector (section 3 H); section 11
    by sector sums the subsector lines; the total = total power demand; fuel totals exclude them."""
    ok = True
    for g in (1, 2):
        _, b, ys = B.group_cols(g)
        cols = [b] + ys
        d_sub = max(abs(ws.cell(B.SUB_HEAD[s] + 1, c).value - (ws.cell(B.R_PW[('dem', s)], c).value
                                                                if s in B.DEM_SUBS else 0.0))
                    for s in B.SUB_HEAD for c in cols)
        d_tot = max(abs(ws.cell(B.R_ELD['all'], c).value - ws.cell(B.R_PW[('demtot', '')], c).value) for c in cols)
        d_grp = max(abs(sum(ws.cell(B.SUB_HEAD[s[0]] + 1, c).value for s in B.SUBSECTORS if s[2] == grp)
                        - ws.cell(B.R_ELD[grp], c).value) for grp in B.ELD_GROUPS[1:] for c in cols)
        d_dg = max(abs(sum(ws.cell(B.R_PW[('demg', m)], c).value for m, _l in B.DEM_GROUPS)
                       - ws.cell(B.R_PW[('demtot', '')], c).value) for c in cols)
        good = max(d_sub, d_tot, d_grp, d_dg) < 1e-6
        ok &= good
        log(f'- scenario {g}: memo by subsector = power demand of the subsector (max abs {d_sub:.3g}); by sector = sum of '
            f'its subsectors ({d_grp:.3g}); total = total power demand ({d_tot:.3g}); demand by group sums to the '
            f'total ({d_dg:.3g}) {"OK" if good else "FAIL"}')
    _, b1, y1 = B.group_cols(1)
    log('  - electricity demand by sector, scenario 1 (ktoe), 2022 / 2030 / 2040: ' + '; '.join(
        f'{grp} ' + ' / '.join(f'{ws.cell(B.R_ELD[grp], c).value:,.0f}' for c in (b1, y1[7], y1[-1]))
        for grp in B.ELD_GROUPS))
    return ok


def check_goalseek():
    """ets_goalseek_v7_0.py on a copy with the ETS test scenario as group 3: the cap is met within tolerance."""
    import ets_goalseek_v7_0 as G
    wb = openpyxl.load_workbook(B.OUT)
    add_scenario(wb, 2, 3, 'Test 3: new ETS with cap, goal seek', ETS_TEST)
    path = os.path.join(tempfile.mkdtemp(), 'goalseek.xlsx')
    wb.save(path)
    lines = []
    tol, max_it, fresh = G.settings(wb)                 # v5.2: Manual inputs E10:E12, as the macro
    p, worst, it = G.solve(path, [3], log=lines.append)
    for ln in lines:
        log(ln)
    log(f'- goal-seek settings (Manual inputs E10:E12): max iterations {max_it}, start fresh {fresh}, tolerance {tol}')
    ok = worst[3] < tol
    years = [B.BASE_YEAR] + B.YEARS
    est = recompute({**scenario_mt(2), **{B.MT_NAMES[k]: v for k, v in ETS_TEST.items()}})[('ets.est', '', '')]
    log(f'- goal seek, scenario 3 (ETS test settings): worst |covered/cap - 1| {worst[3]:.4f} after {it} iterations '
        f'{"OK" if ok else "FAIL"}')
    log('  - price $/tCO2, fast estimate -> goal seek: ' + ', '.join(
        f'{y} {est[k]:.1f} -> {p[3][k]:.1f}' for k, y in enumerate(years) if y in (2027, 2030, 2035, 2040)))
    return ok


# ------------------------------------------------------------------ v1.03: scenarios, stored results, macro
STEM_KEYS = {RS(k_): v_ for k_, v_ in {'mit.co2.all.all.e': ('co2', 'all', 'all'), 'mit.rtx.all.all': ('rtx', 'all', 'all'),
             'mit.rsub.all.all': ('rsub', 'all', 'all'), 'mit.rnew.all.all': ('rnew', 'all', 'all'),
             'mit.rtot.all.all': ('rtot', 'all', 'all'), 'mit.cptraj': ('cptraj', '', ''),
             'mit.ets.p': ('ets.p', '', ''), 'mit.co2.ets.all.all': ('co2.ets', 'all', 'all'),
             'mit.co2.cap.all.all': ('ets.cap', '', ''), 'mit.rp.res.ecy': ('rp', 'res', 'ecy'),
             'mit.rp.ind.ecy': ('rp', 'ind', 'ecy'), 'mit.gncav': ('gncav', '', ''),
             'mit.co2.pow.all.e': ('co2.pow', '', ''), 'mit.gtot': ('gtot', '', ''), 'mit.vre': ('vre', '', ''),
             'mit.shr.pow.nga': ('shr', 'pow', 'nga'), 'mit.usdtot': ('usdtot', '', '')}.items()}


def stored_blocks(ws):
    """{id: {stem: [values base..last]}} and {id: name} of StoredResults (values workbook or shipped file)."""
    out, names = {}, {}
    r = B.SR_FIRST
    while ws.cell(r, 3).value not in (None, ''):
        sid = ws.cell(r, 1).value
        out.setdefault(sid, {})[ws.cell(r, 3).value] = [ws.cell(r, B.SR_Y0 + j).value for j in range(B.NY)]
        names[sid] = ws.cell(r, 2).value
        r += 1
    return out, names


def definition_mt(num):
    mt = mt_used()
    edits = next(e for n, _nm, _r, e in B.DEFINITIONS if n == num)
    for k, v in edits.items():
        mt[k if isinstance(k, int) else B.MT_NAMES[k]] = v
    return mt


def rel(a, b):
    return abs(a - b) / max(1.0, abs(b)) if isinstance(a, (int, float)) and isinstance(b, (int, float)) else float('inf')


def check_definitions():
    ws = openpyxl.load_workbook(B.OUT, read_only=True)['ScenarioDefinition']     # v6.0: read-only (memory)
    ok = True
    for n, nm, run, edits in B.DEFINITIONS:
        c = B.MT_COL0 + n - 1
        good = (ws.cell(B.MT_ROW_SCEN, c).value == f'={L(c - 1)}{B.MT_ROW_SCEN}+1' and ws.cell(B.MT_ROW_NAME, c).value == nm
                and ws.cell(B.MT_ROW_RUN, c).value == run
                and all(ws.cell(k if isinstance(k, int) else B.MT_NAMES[k], c).value == v for k, v in edits.items()))
        ok &= good
        log(f'- definition {n} (column {L(c)}): "{nm}", Run? {run}, {len(edits)} inputs changed from the template '
            f'{"OK" if good else "FAIL"}')
    live = B.MT_COL0 + 1
    good = ws.cell(B.MT_ROW_RUN, B.MT_COL0).value.startswith('Baseline') and ws.cell(B.MT_ROW_RUN, live).value.startswith('Live')
    ok &= good
    log(f'- J4 / K4: "{ws.cell(B.MT_ROW_RUN, B.MT_COL0).value}" / "{ws.cell(B.MT_ROW_RUN, live).value}" {"OK" if good else "FAIL"}')
    return ok


def check_vba():
    from oletools.olevba import VBA_Parser
    vp = VBA_Parser(B.OUT)
    mods = {n.rsplit('.', 1)[0]: c for (_f, _s, n, c) in vp.extract_macros()}
    src = open(B.BAS, encoding='cp1252').read().replace('\r\n', '\n')
    got = mods.get('CPATScenarios', '').replace('\r\n', '\n')
    wb = openpyxl.load_workbook(B.OUT)
    codes = [w.sheet_properties.codeName for w in wb.worksheets]
    good = (got.strip() == src.strip() and set(codes) | {'ThisWorkbook'} == set(mods) - {'CPATScenarios'}
            and wb.code_name == 'ThisWorkbook')
    log(f'- VBA project: module CPATScenarios = {os.path.basename(B.BAS)} ({len(src.splitlines())} lines); document '
        f'modules ThisWorkbook + {len(codes)} sheets matching the sheet code names {"OK" if good else "FAIL"}')
    procs = re.findall(r'^Public (?:Sub|Function) (\w+)', src, flags=re.M)
    log(f'  - public macros: {", ".join(procs)}')
    return good


def check_stored(ws_vals):
    """Shipped StoredResults vs the shipped workbook recalculated (baseline, definition 3 = live scenario 2) and vs the
    independent Python recomputation (definitions 4 and 5; 5 with its stored ETS prices)."""
    wb = openpyxl.load_workbook(B.OUT, data_only=True)
    st, names = stored_blocks(wb['StoredOutputs'])
    ok = sorted(st) == [1] + [n for n, _nm, run, _e in B.DEFINITIONS if run == 'Yes'] and \
        all(len(v) == len(B.MTO_INDICATORS) for v in st.values())
    log(f'- StoredResults: scenario IDs {sorted(st)}, {len(B.MTO_INDICATORS)} rows each; values only: '
        f'{"OK" if ok else "FAIL"}')
    mo = ws_vals['LiveOutputs']
    for sid, src in ((1, 1), (3, 2)):
        h = B.MTO_R0 + (src - 1) * B.MTO_BLOCK
        d = max(rel(st[sid][stem][j], mo.cell(h + 1 + k, B.MTO_C0 + j).value)
                for k, (stem, _f) in enumerate(B.MTO_INDICATORS) for j in range(B.NY)
                if isinstance(mo.cell(h + 1 + k, B.MTO_C0 + j).value, (int, float)))
        ok &= d < 1e-9
        log(f'- stored ID {sid} = MTOutputs block {src} of the shipped workbook recalculated (same inputs): max rel diff '
            f'{d:.2e} {"OK" if d < 1e-9 else "FAIL"}')
    years = [B.BASE_YEAR] + B.YEARS
    for sid in (4, 5):
        mt = definition_mt(sid)
        ovr = None
        if sid == 5:          # the stored prices as override (the goal seek switches the override on)
            ovr = {y: st[sid][RS('mit.ets.p')][k] for k, y in enumerate(years)}
            mt[B.MT_NAMES['D_ETSPriceOverride']] = 'Yes'
        exp = recompute(mt, ovr=ovr)
        d = max(rel(st[sid][stem][k], exp[key][k]) for stem, key in STEM_KEYS.items() for k in range(len(years)))
        ok &= d < 1e-9
        log(f'- stored ID {sid} ({names[sid][:40]}...) vs independent Python recomputation ({len(STEM_KEYS)} '
            f'indicators: CO2, revenues, carbon and ETS price, covered CO2, cap, electricity prices, generation cost): max rel diff {d:.2e} '
            f'{"OK" if d < 1e-9 else "FAIL"}')
    # v5.2: the build runs no ETS goal seek (user rule 2026-10-17, CAVEATS v4.9): definition 5 is stored at the
    # workbook's own price estimate (fast estimate ets.est); RunAllScenarios in Excel goal-seeks the cap (section 5b
    # tests the goal seek). The cap gap of the stored estimate is a memo (issue I30).
    cov, cap = st[5][RS('mit.co2.ets.all.all')], st[5][RS('mit.co2.cap.all.all')]
    gap = max(abs(a / b - 1) for a, b in zip(cov, cap) if b)
    est = recompute(definition_mt(5))[('ets.est', '', '')]
    d = max(rel(st[5][RS('mit.ets.p')][k], est[k]) for k in range(len(years)))
    ok &= d < 1e-9
    log(f'- stored ID 5 (ETS package, build without goal seek): ETS price = the fast estimate of the independent '
        f'recomputation, max rel diff {d:.2e} {"OK" if d < 1e-9 else "FAIL"}; memo: worst |covered/cap - 1| {gap:.4f} '
        f'(I30); ETS price 2027/2030/2035/2040: '
        f'{[round(st[5][RS("mit.ets.p")][y - B.BASE_YEAR], 1) for y in (2027, 2030, 2035, 2040)]}')
    return ok


def check_compare():
    """v7.0: the dashboard (Stored by default): slot IDs and short names follow ScenarioDefinition; the key table
    (level, difference, % difference vs the baseline) and the time series equal StoredOutputs by output code; a slot
    without stored results is blank in the table and #N/A in the chart data."""
    wbf = openpyxl.load_workbook(B.OUT)
    ws = wbf['ScenarioCompare']
    vals = recalc_wb(B.OUT)
    wv = vals['ScenarioCompare']
    st, _names = stored_blocks(vals['StoredOutputs'])
    y = wv.cell(B.SC_R_YEAR, 3).value
    cols = range(B.SC_C0, B.SC_C0 + B.SC_SLOTS)
    ids = [wv.cell(B.SC_R_ID, c).value for c in cols]
    shorts = [wv.cell(B.SC_R_SHORT, c).value for c in cols]
    ok = wv.cell(B.SC_R_SRC, 3).value == 'Stored'
    if not ok:                             # v7.2: every failing condition is logged (NORMS 3b.4)
        log(f'- ScenarioCompare source switch: {wv.cell(B.SC_R_SRC, 3).value!r}, expected Stored FAIL')
    sdv = vals['ScenarioDefinition']
    exp_ids = [sdv.cell(B.MT_ROW_SCEN, B.MT_COL0 + k).value if sdv.cell(B.MT_ROW_NAME, B.MT_COL0 + k).value else ''
               for k in range(B.SC_SLOTS)]
    good = [i if i is not None else '' for i in ids] == [i if i is not None else '' for i in exp_ids]
    ok &= good
    if not good:
        log(f'- ScenarioCompare slot IDs {ids}, expected the ScenarioDefinition IDs {exp_ids} FAIL')
    worst, blanks, nonblank = 0.0, 0, []
    base = st.get(ids[0], {})
    for k, c in enumerate(cols):
        sid = ids[k]
        for i, (stem, _lab) in enumerate(B.SC_KEY):
            r = B.SC_KEY_R0 + 3 * i
            v = wv.cell(r, c).value
            if sid in (None, '') or sid not in st:
                if v not in (None, ''):
                    nonblank.append(f'{L(c)}{r}={v!r}')
                blanks += 1
                continue
            e = st[sid][stem][y - B.BASE_YEAR]
            worst = max(worst, rel(v, e))
            if k:
                b = base[stem][y - B.BASE_YEAR]
                worst = max(worst, rel(wv.cell(r + 1, c).value, e - b))
                if stem in B.SC_PCT_KEYS and b:
                    worst = max(worst, rel(wv.cell(r + 2, c).value, e / b - 1))
    good = worst < 1e-9 and not nonblank
    ok &= good
    log(f'- ScenarioCompare {y} (Stored): IDs {[i for i in ids if i not in (None, "")]}, short names '
        f'{[s for s in shorts if s]}; key table equals StoredOutputs (max rel diff {worst:.2e}; {blanks} blank cells '
        f'of slots without stored results{", not blank: " + str(nonblank[:5]) if nonblank else ""}) {"OK" if good else "FAIL"}')
    for j, label in enumerate(('levels', 'differences')):
        cs = list(cols) if j == 0 else list(cols)[1:]
        ok &= uniform(ws, [(B.SC_KEY_R0 + 3 * i + j, c) for i in range(len(B.SC_KEY)) for c in cs],
                      f'ScenarioCompare key {label}')[0]
    worst, gaps, cells, not_na = 0.0, 0, [], []
    for i in range(len(B.SC_TS)):
        h, yr, s0, _s1 = B.sc_ts_rows(i)
        stem = wv.cell(h, 1).value
        for j in range(B.SC_SLOTS):
            sid = wv.cell(s0 + j, 2).value
            for k in range(B.NY):
                c = B.SC_C0 + k
                cells.append((s0 + j, c))
                v = wv.cell(s0 + j, c).value
                if sid in (None, '') or sid not in st:
                    gaps += 1
                    if v != '#N/A':
                        not_na.append(f'{L(c)}{s0 + j}={v!r}')
                else:
                    worst = max(worst, rel(v, st[sid][stem][k]))
    good = worst < 1e-9 and not not_na
    ok &= good
    log(f'- time series ({len(B.SC_TS)} blocks x {B.SC_SLOTS} slots x {B.NY} years) equal StoredOutputs (max rel '
        f'diff {worst:.2e}); {gaps} cells of slots without results #N/A'
        f'{" (not #N/A: " + str(len(not_na)) + ", e.g. " + str(not_na[:4]) + ")" if not_na else ""} {"OK" if good else "FAIL"}')
    for i in range(len(B.SC_TS)):                   # one formula per block (each reads its own year row)
        _h, _yr, s0, s1 = B.sc_ts_rows(i)
        ok &= uniform(ws, [(r, c) for r, c in cells if s0 <= r <= s1], f'ScenarioCompare time series, block {i + 1}')[0]
    log(f'  - CO2 {y} (MtCO2): ' + ', '.join(f'{shorts[k]}: {wv.cell(B.SC_KEY_R0, c).value:,.1f}'
                                            for k, c in enumerate(cols) if isinstance(wv.cell(B.SC_KEY_R0, c).value, (int, float))))
    return ok


def check_macro():
    """Run CPATScenarios.RunAll in LibreOffice on the shipped workbook (LAMBDAs expanded, StoredResults emptied) and
    compare what the macro stores with the shipped StoredResults (Python emulation); the live column and the ETS
    override row must be restored."""
    from vba_project_v7_0 import embed_vba
    wb = openpyxl.load_workbook(B.OUT)
    sr = wb['StoredOutputs']
    for row in sr.iter_rows(min_row=B.SR_FIRST, max_row=sr.max_row):
        for c in row:
            c.value = None
    for num, _n, _r, e in B.DEFINITIONS:   # v6.0 (NORMS 5): no goal seek in the macro run: new-ETS definitions at the
        if str(e.get('D_NewETS', '')).startswith('Yes'):                    # override (not compared, as before)
            wb['ScenarioDefinition'].cell(B.MT_NAMES['D_ETSPriceOverride'], B.MT_COL0 + num - 1).value = 'Yes'
    xlsx = variant(wb, 'expand')
    xlsm = xlsx[:-5] + '.xlsm'
    embed_vba(xlsx, xlsm, {'CPATScenarios': B.vba_module_source()})
    out = xlsx[:-5] + '_ran.xlsx'
    res = subprocess.run(['python3', os.path.join(HERE, 'lo_run_macro_v7_0.py'), xlsm, 'CPATScenarios.RunAll', out],
                         capture_output=True, text=True, timeout=3000)
    log(f'- LibreOffice ran the embedded macro: {res.stdout.strip().splitlines()[-1] if res.stdout.strip() else res.stderr[-300:]}')
    if not os.path.exists(out):
        log('  FAIL: no output')
        return False
    ran = openpyxl.load_workbook(out, data_only=True)
    got, gnames = stored_blocks(ran['StoredOutputs'])
    ship, snames = stored_blocks(openpyxl.load_workbook(B.OUT, data_only=True)['StoredOutputs'])
    worst, where = 0.0, None
    ets_ids = {num for num, _n, _r, e in B.DEFINITIONS if str(e.get('D_NewETS', '')).startswith('Yes')
               and not str(e.get('D_ETSPriceOverride', '')).startswith('Yes')}   # v5.2: goal-seeked by the macro
    for sid in ship:
        if sid in ets_ids:          # the build stores them at the fast estimate (no goal seek, user rule 2026-10-17)
            continue
        for stem in ship[sid]:
            for j in range(B.NY):
                d = rel(got.get(sid, {}).get(stem, [None] * B.NY)[j], ship[sid][stem][j])
                if d > worst:
                    worst, where = d, (sid, stem, B.BASE_YEAR + j)
    good = sorted(got) == sorted(ship) and gnames == snames and worst < 1e-6
    by_id = {sid: max([rel(got.get(sid, {}).get(st_, [None] * B.NY)[j], ship[sid][st_][j]) for st_ in ship[sid]
                       for j in range(B.NY)] or [0.0]) for sid in ship}       # v5.2: per stored ID
    log(f'  - macro stored IDs {sorted(got)} with the same names; values vs the Python emulation: max rel diff '
        f'{worst:.2e}{" at " + str(where) if where else ""} (by ID: '
        f'{", ".join(f"{k} {v:.1e}" for k, v in sorted(by_id.items()))}; new-ETS IDs {sorted(ets_ids)} re-solved by the '
        f'macro goal seek, a memo: the build stores them at the fast estimate) {"OK" if good else "FAIL"}')
    orig = openpyxl.load_workbook(B.OUT)
    live = B.MT_COL0 + 1
    mt_o, mt_r = orig['ScenarioDefinition'], openpyxl.load_workbook(out)['ScenarioDefinition']
    lo_bool = {'=TRUE()': True, '=FALSE()': False}         # LibreOffice saves boolean cells as =TRUE() / =FALSE()
    norm = lambda v: lo_bool.get(v, v) if isinstance(v, str) else v
    diffs = [r for r in range(1, B.MT_END + 1) if r != B.MT_ROW_SCEN and mt_o.cell(r, live).value != norm(mt_r.cell(r, live).value)
             and not (isinstance(mt_o.cell(r, live).value, str) and mt_o.cell(r, live).value.startswith('='))]
    ovr = [ran['Mitigation'].cell(B.R_POL['ets.ovr'], c).value for c in [B.group_cols(2)[1]] + B.group_cols(2)[2]]
    good2 = not diffs and all(v in (None, '') for v in ovr)
    log(f'  - live column K restored ({len(diffs)} cells differ) and ETS override row empty again '
        f'{"OK" if good2 else "FAIL " + str(diffs[:5])}')
    return good and good2


def run_macro_lo(wb, proc, tag):
    """Expanded variant of wb with the VBA module embedded, run proc in LibreOffice; (stdout line, values workbook)."""
    from vba_project_v7_0 import embed_vba
    xlsx = auto_calc(variant(wb, 'expand'), tempfile.mkdtemp())   # v7.1: the shipped file is in manual calculation;
    xlsm = xlsx[:-5] + f'_{tag}.xlsm'                              # an openpyxl copy has no values (NORMS 3i.3)
    embed_vba(xlsx, xlsm, {'CPATScenarios': B.vba_module_source()})
    out = xlsx[:-5] + f'_{tag}_ran.xlsx'
    res = subprocess.run(['python3', os.path.join(HERE, 'lo_run_macro_v7_0.py'), xlsm, f'CPATScenarios.{proc}', out],
                         capture_output=True, text=True, timeout=3000)
    line = res.stdout.strip().splitlines()[-1] if res.stdout.strip() else res.stderr[-300:]
    return line, (openpyxl.load_workbook(out, data_only=True) if os.path.exists(out) else None)


def check_first_run():
    """v1.04: the first-run test macro CheckBatch, run in LibreOffice on the shipped workbook (stored results kept):
    Result PASS and the largest relative difference below 1e-6; and on a copy where a row code is broken: FAIL
    before any run."""
    ok = True
    ws = B.tab(openpyxl.load_workbook(B.OUT), 'MacroCheck')
    good = ws[f'A{B.CHK_FIRST}'].value == 'Result' and ws[f'B{B.CHK_FIRST}'].value == 'not run yet'
    ok &= good
    log(f'- sheet MacroCheck as shipped: "{ws[f"B{B.CHK_FIRST}"].value}" {"OK" if good else "FAIL"}')
    line, ran = run_macro_lo(openpyxl.load_workbook(B.OUT), 'CheckBatch', 'check')
    log(f'- LibreOffice ran CheckBatch: {line}')
    if ran is None:
        return False
    mc = B.tab(ran, 'MacroCheck')
    rows = [(mc.cell(r, 1).value, mc.cell(r, 2).value) for r in range(B.CHK_FIRST, B.CHK_FIRST + 40)
            if mc.cell(r, 1).value]
    for a, b in rows:
        log(f'  - {a}: {b}')
    result = dict(rows).get('Result')
    worst = float(dict(rows).get('Largest relative difference (baseline and batch)', 'inf'))
    lookups = sum(1 for a, b in rows if str(b).startswith('OK ('))
    good = result == 'PASS' and worst < 1e-6 and lookups == 15          # v5.2: + the three goal-seek names
    ok &= good
    log(f'- first-run test: Result {result}, {lookups} lookups found, largest relative difference {worst:.1e} '
        f'{"OK" if good else "FAIL"}')
    wb = openpyxl.load_workbook(B.OUT)
    wb['Mitigation'].cell(B.R_POL['ets.ovr'], 1).value = 'ets.ovr.broken'
    line, ran = run_macro_lo(wb, 'CheckBatch', 'neg')
    mc = B.tab(ran, 'MacroCheck') if ran else None
    res = mc.cell(B.CHK_FIRST, 2).value if mc else None
    fails = [mc.cell(r, 1).value for r in range(B.CHK_FIRST + 1, B.CHK_FIRST + 40)
             if mc and str(mc.cell(r, 2).value or '').startswith('FAIL')] if mc else []
    good = str(res).startswith('FAIL') and fails == ['Mitigation: row ets.ovr (ETS override prices)'] and \
        line.split(' returned ')[-1].startswith('-1')
    ok &= good
    log(f'- negative test (row code ets.ovr broken): CheckBatch {line.split(" returned ")[-1]}; Result "{res}"; '
        f'failed lookup: {fails} {"OK" if good else "FAIL"}')
    return ok


FAILED = []


def named(name, value):
    """v7.1: the result of a check section; a failing section is named in the report (no silent FAIL, NORMS 3b.4)."""
    if not value:
        FAILED.append(name)
    return value


def main():
    partial = os.environ.get('CHECK_PARTIAL') == '1'   # v6.2: time-efficient run (sections 0-4b, 7, 8b, 14; the
    log(f'# Check report - {B.NAME}-v{B.VERSION}'      # regression is the quick check's; variant B and 5-13 skipped)
        + (' (partial: CHECK_PARTIAL=1, sections 0-4b, 7, 8b, 14; LAMBDA-library variant B skipped)' if partial else ''))
    results = []
    log('\n## 0. Formula length (at most 100 characters per cell formula)')
    results.append(named('check_formula_length', check_formula_length()))
    log('\n## 1. Shipped file recalculated in LibreOffice (no LAMBDA support)')
    ws_a = recalc(variant(openpyxl.load_workbook(B.OUT), 'expand'))
    results.append(named('check_shipped', check_shipped(ws_a)))
    log('\n## 2. Formula uniformity (relative R1C1)')
    results.append(named('check_uniformity', check_uniformity(openpyxl.load_workbook(B.OUT))))
    log('\n## 3. LAMBDA encoding')
    results.append(named('check_encoding', check_encoding()))
    log('\n## 4. Values vs independent Python recomputation')
    ws_c = None if partial else recalc(variant(openpyxl.load_workbook(B.OUT), 'everywhere'))
    for g, *_ in B.SCENARIOS:
        exp = recompute(scenario_mt(g))
        results.append(named('compare', compare(ws_a, g, exp, f'A. as shipped, evaluated as a LAMBDA host (2041 LAMBDAs expanded), '
                                             f'scenario {g}')))
        if ws_c is not None:
            results.append(named('compare', compare(ws_c, g, exp, f'B. optional LAMBDA library (sheet Lambdas) copied over every '
                                                 f'calculated row, LAMBDAs expanded, scenario {g}')))
        results.append(named('check_transport', check_transport(ws_a, g, exp, f'A. as shipped, scenario {g}')))   # v3.5: section 5b
        if ws_c is not None:
            results.append(named('check_transport', check_transport(ws_c, g, exp, f'B. LAMBDA library over every row, scenario {g}')))
    del ws_c                               # v5.2: free the variant-B workbook (memory: the run was OOM-killed)
    import gc
    gc.collect()
    log('\n## 4b. Power method = legacy (Python reference with the legacy inputs vs cached legacy rows)')
    results.append(named('check_power_method', check_power_method()))
    if partial:
        log('\n## 7. Labels and codes')
        results.append(named('check_codes', check_codes(openpyxl.load_workbook(B.OUT)['Mitigation'], ws_a)))
        log('\n## 8b. Layout and constants (v2.4): years in row 1, labelled D:G, nothing typed')
        results.append(named('check_v24_layout', check_v24_layout(ws_a)))
        log('\n## 14. Consistency (v1.09, v2.4): check rows, identities, references, versions, stale texts')
        results.append(named('check_consistency', check_consistency(ws_a)))
        log(f'\n**Overall (partial): {"PASS" if all(results) else "FAIL"}**')
        with open(os.path.join(HERE, f'check_report_v{B.VERSION}.md'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(report) + '\n')
        return
    log('\n## 5. Scenario tests (copied MTInputs column + Mitigation group)')
    results.append(named('check_scenarios', check_scenarios()))
    log('\n## 5d. Power features switched on (v5.4, power plan P1, P2, P4)')
    results.append(named('check_power_features', check_power_features()))
    log('\n## 5a. Residential leakage to biomass switched on (v5.1, global setting BiomassLeakage)')
    results.append(named('check_leakage', check_leakage()))
    results.append(named('check_exempt_scenario', check_exempt_scenario()))
    log('\n## 5b. ETS goal seek (ets_goalseek_v7_0.py): skipped (user rule 2026-10-19, NORMS 5: the user tests the '
        'goal seek separately, issue I30)')
    log('\n## 5c. Existing carbon pricing with non-zero test data (v1.09)')
    results.append(named('check_ecp', check_ecp()))
    log(f'\n## 6. Regression vs v{PREV} (shared output codes, 2022-2041: no change)')
    results.append(named('check_regression', check_regression(ws_a)))
    log('\n## 6b. MTOutputs and Charts')
    results.append(named('check_mto', check_mto(recalc_wb(variant(openpyxl.load_workbook(B.OUT), 'expand')), [1, 2], 'as shipped')))
    results.append(named('check_charts', check_charts()))
    log('\n## 7. Labels and codes')
    results.append(named('check_codes', check_codes(openpyxl.load_workbook(B.OUT)['Mitigation'], ws_a)))
    log('\n## 8. Row outline')
    results.append(named('check_outline', check_outline(openpyxl.load_workbook(B.OUT)['Mitigation'])))
    log('\n## 8b. Layout and constants (v2.4): years in row 1, labelled D:G, nothing typed')
    results.append(named('check_v24_layout', check_v24_layout(ws_a)))
    log('\n## 9. MTInputs')
    results.append(named('check_mtinputs', check_mtinputs()))
    log('\n## 10. Format')
    results.append(named('check_format', check_format(openpyxl.load_workbook(B.OUT)['Mitigation'])))
    log('\n## 11. Sanity and results')
    results.append(named('check_sanity', check_sanity(ws_a)))
    log('\n## 11b. Power sector: properties and results')
    results.append(named('check_power_results', check_power_results(ws_a)))
    log('\n## 11c. Planned retirement switched on (v1.07)')
    results.append(named('check_planned_retirement', check_planned_retirement()))
    log('\n## 11d. Electricity demand memo lines (v1.07)')
    results.append(named('check_memo', check_memo(ws_a)))
    log('\n## 12. Scenario definitions, VBA module, stored results, comparison, macro run')
    import gc
    gc.collect()                           # v6.0: free the earlier sections' workbooks before the large loads (memory)
    results.append(named('check_definitions', check_definitions()))
    gc.collect()
    results.append(named('check_vba', check_vba()))
    results.append(named('check_stored', check_stored(recalc_wb(variant(openpyxl.load_workbook(B.OUT), 'expand')))))
    results.append(named('check_compare', check_compare()))
    results.append(named('check_macro', check_macro()))
    log('\n## 13. First-run test macro CheckBatchRun (v1.04)')
    results.append(named('check_first_run', check_first_run()))
    log('\n## 14. Consistency (v1.09, v2.4): check rows, identities, references, versions, stale texts')
    results.append(named('check_consistency', check_consistency(ws_a)))
    if FAILED:
        log(f'\nSections that failed: {", ".join(FAILED)}')
    log(f'\n**Overall: {"PASS" if all(results) else "FAIL"}**')
    with open(os.path.join(HERE, f'check_report_v{B.VERSION}.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(report) + '\n')


if __name__ == '__main__':
    main()
