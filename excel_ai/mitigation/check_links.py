"""v0.7.1: test of the linked data tables (DATA_LINKS) without Excel. Power Query does not run in LibreOffice, so the
macro UpdateDataTables is emulated in Python exactly as it copies (RefreshLink): the rows of the data-workbook table
(the country's rows, or all rows), each column of the prototype tab filled from the data-workbook column of the same header
name, the tab's header row and its formula columns left as they are, the old rows cleared.

    python check_links.py [data workbook]     (default: data/workbooks/CPAT_Data_dummy_python.xlsx)

Test A (identity, no recalculation): a data workbook made from the prototype's own tabs, columns in reverse order and an
extra column; the update must give back every cell of every linked tab. Test B (the dummy data workbook): every
link finds its table and every prototype column in it, the country has rows; the prototype recalculated in LibreOffice after the
update has no error values in the plain scenario group (group 1) and LiveOutputs block 1; a link whose data fail the
sanity check (negative retail prices: the model needs positive prices) is reported and left out of that run; the change
of the key results is reported (dummy values differ from the shipped Egypt data).
Report: check_links_report_v0.7.1.md.
"""
import os
import random
import sys

import openpyxl

import build as B
import check_full as C

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'data', 'workbooks', 'CPAT_Data_dummy_python.xlsx')
REPORT = os.path.join(HERE, 'check_links_report.md')
LINES = []


def log(s=''):
    print(s, flush=True)
    LINES.append(s)


def key(v):
    """HeaderKey of the macro: numbers without decimals, text trimmed."""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return str(int(v)) if float(v).is_integer() else repr(float(v))
    return '' if v is None else str(v).strip()


def table_of(dw, name):
    for ws in dw.worksheets:
        if name in ws.tables:
            rows = list(ws.iter_rows(values_only=True))
            return list(rows[0]), [list(r) for r in rows[1:]]
    return None


def tab_header(ws, hdr, ncol):
    c0 = openpyxl.utils.cell.coordinate_from_string(hdr)
    col0, row0 = openpyxl.utils.column_index_from_string(c0[0]), c0[1]
    return row0, col0, [ws.cell(row0, col0 + j).value for j in range(ncol)]


def update(wb, dw, iso):
    """The macro's copy, per link: (tab, rows written, prototype columns missing in the table)."""
    out = []
    for tab, tbl, hdr, ncol, rows_of in B.DATA_LINKS:
        t = table_of(dw, tbl)
        if t is None:
            out.append((tab, None, ['table missing']))
            continue
        head, rows = t
        fi = head.index(B.FILTER_COL) if B.FILTER_COL in head else None
        if rows_of != 'all':
            rows = [r for r in rows if fi is not None and r[fi] == iso]
        ws = wb[tab]
        row0, col0, mh = tab_header(ws, hdr, ncol)
        pos = {key(h): i for i, h in enumerate(head)}
        miss = [key(h) for h in mh if key(h) and key(h) not in pos]
        if rows:
            for r in range(row0 + 1, max(ws.max_row, row0 + len(rows)) + 1):
                for j in range(ncol):
                    ws.cell(r, col0 + j).value = None
            for i, r in enumerate(rows):
                for j, h in enumerate(mh):
                    k = pos.get(key(h))
                    if k is not None:
                        ws.cell(row0 + 1 + i, col0 + j).value = r[k]
        out.append((tab, len(rows), miss))
    return out


def negative_prices(dw, iso):
    """(country_year, code, value) of every negative retail price (mit.rp.*) of the country in L_Prices_dom."""
    head, rows = table_of(dw, 'L_Prices_dom')
    fi = head.index(B.FILTER_COL)
    return [(r[0], h, round(r[j], 3)) for r in rows if r[fi] == iso for j, h in enumerate(head)
            if str(h).startswith('mit.rp.') and isinstance(r[j], (int, float)) and r[j] < 0]


def new_errors(vals, shipped):
    """Error cells in group 1 (2022-2040) of Mitigation and in LiveOutputs block 1 that the shipped file has not."""
    _c, b, ys = B.group_cols(1)
    errs = []
    for sheet, cols in (('Mitigation', [b] + ys[:-1]), ('LiveOutputs', None)):
        ws, w0 = vals[sheet], shipped[sheet]
        for row in ws.iter_rows():
            for c in row:
                if (cols is None or c.column in cols) and C.is_err(c.value) and not C.is_err(w0[c.coordinate].value):
                    if sheet == 'LiveOutputs' and not (B.MTO_R0 <= c.row < B.MTO_R0 + B.MTO_BLOCK):
                        continue
                    errs.append(f'{sheet}!{c.coordinate}')
    return errs


def own_workbook(wb):
    """Test A: a data workbook from the prototype's own linked tabs (columns reversed, an extra column, FilterISO3)."""
    dw = openpyxl.Workbook()
    dw.remove(dw.active)
    iso = B.COUNTRY
    for tab, tbl, hdr, ncol, rows_of in B.DATA_LINKS:
        ws = wb[tab]
        row0, col0, mh = tab_header(ws, hdr, ncol)
        cols = [j for j in range(ncol) if key(mh[j])]
        data = []
        for r in range(row0 + 1, ws.max_row + 1):
            v = [ws.cell(r, col0 + j).value for j in cols]
            if any(x not in (None, '') for x in v):
                data.append(v)
        head = [key(mh[j]) for j in cols][::-1] + ['ExtraColumn', B.FILTER_COL]
        rows = [v[::-1] + ['x', iso] for v in data]
        if rows_of != 'all':
            rows.append([None] * len(cols) + ['other country', 'ZZZ'])   # filtered out
        random.Random(1).shuffle(rows) if rows_of == 'all' else None
        out = dw.create_sheet(tbl[:31])
        out.append(head)
        for r in rows:
            out.append(r)
        out.add_table(openpyxl.worksheet.table.Table(
            displayName=tbl, ref=f'A1:{openpyxl.utils.get_column_letter(len(head))}{len(rows) + 1}'))
    return dw


def main():
    data = sys.argv[1] if len(sys.argv) > 1 else DATA
    log(f'# Linked data tables - {B.NAME} v{B.VERSION}\n')
    log(f'Links: {len(B.DATA_LINKS)} ({", ".join(f"{t} <- {n} ({r})" for t, n, _h, _c, r in B.DATA_LINKS)})\n')
    ok = True
    log('## A. Identity: a data workbook made from the prototype tabs (columns reversed, extra column, other rows)')
    wb0 = openpyxl.load_workbook(B.OUT, keep_vba=True)
    ref = {tab: [[c.value for c in row] for row in wb0[tab].iter_rows()] for tab, *_ in B.DATA_LINKS}
    res = update(wb0, own_workbook(wb0), B.COUNTRY)
    for (tab, n, miss), (_t, _n, hdr, ncol, _r) in zip(res, B.DATA_LINKS):
        got = [[c.value for c in row] for row in wb0[tab].iter_rows()]
        row0, col0, _mh = tab_header(wb0[tab], hdr, ncol)
        same = all((got[i][j] if i < len(got) and j < len(got[i]) else None) ==
                   (ref[tab][i][j] if i < len(ref[tab]) and j < len(ref[tab][i]) else None)
                   for i in range(max(len(got), len(ref[tab]))) for j in range(max(len(r) for r in ref[tab])))
        if not same:      # all-rows links come back in another row order: compare the sets of rows
            key_rows = lambda t: sorted(repr(r[col0 - 1:col0 - 1 + ncol]) for r in t[row0:]
                                        if any(x not in (None, '') for x in r[col0 - 1:col0 - 1 + ncol]))
            same = _r == 'all' and key_rows(got) == key_rows(ref[tab]) and got[:row0] == ref[tab][:row0]
        ok &= same and not miss
        log(f'- {tab}: {n} rows written, every cell as shipped {"OK" if same and not miss else "FAIL " + str(miss[:5])}')
    log(f'\n## B. Dummy data workbook: {os.path.relpath(data, HERE)}')
    dw = openpyxl.load_workbook(data, read_only=False)
    wb = openpyxl.load_workbook(B.OUT, keep_vba=True)
    res = update(wb, dw, B.COUNTRY)
    for tab, n, miss in res:
        good = bool(n) and not miss
        ok &= good
        log(f'- {tab}: {n} rows of {B.COUNTRY}; prototype columns not in the table: {miss[:8] or "none"} '
            f'{"OK" if good else "FAIL"}')
    neg = negative_prices(dw, B.COUNTRY)
    log(f'- data sanity: negative retail prices (mit.rp.*) of {B.COUNTRY} in L_Prices_dom: {len(neg)} {neg[:6]} '
        f'{"OK" if not neg else "(data problem: the model needs positive prices)"}')
    shipped = C.recalc_wb(C.variant(openpyxl.load_workbook(B.OUT), 'expand'))
    errs_all = new_errors(C.recalc_wb(C.variant(wb, 'expand')), shipped)
    log(f'- all {len(B.DATA_LINKS)} links updated, recalculated in LibreOffice: new error values in group 1 '
        f'(2022-2040) and LiveOutputs block 1: {len(errs_all)} {errs_all[:6]}')
    skip = {'Prices_dom'} if neg else set()           # v0.7.1: a link whose data fail the sanity check is left out
    wb = openpyxl.load_workbook(B.OUT, keep_vba=True)
    links = [l for l in B.DATA_LINKS if l[0] not in skip]
    saved, B.DATA_LINKS[:] = list(B.DATA_LINKS), links
    update(wb, dw, B.COUNTRY)
    B.DATA_LINKS[:] = saved
    path = C.variant(wb, 'expand')
    vals = C.recalc_wb(path)
    errs = new_errors(vals, shipped)
    good = not errs
    ok &= good
    log(f'- the {len(links)} links {"without " + ", ".join(sorted(skip)) if skip else ""} updated, recalculated in '
        f'LibreOffice: new error values in group 1 (2022-2040) and LiveOutputs block 1: {len(errs)} {errs[:10]} '
        f'{"OK" if good else "FAIL"}')
    lo, lo0 = vals['LiveOutputs'], shipped['LiveOutputs']
    log('- key results of the baseline (LiveOutputs block 1, 2030), shipped Egypt data -> dummy data:')
    y = B.MTO_C0 + 2030 - B.BASE_YEAR
    for r in range(B.MTO_R0 + 1, B.MTO_R0 + B.MTO_BLOCK):
        stem = lo.cell(r, 2).value
        if stem in [s for s, _l in B.SC_KEY]:
            log(f'  - {stem}: {lo0.cell(r, y).value} -> {lo.cell(r, y).value}')
    log(f'\n**Overall: {"PASS" if ok else "FAIL"}**')
    with open(REPORT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(LINES) + '\n')
    return ok


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
