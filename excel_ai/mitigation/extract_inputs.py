"""The inputs (legacy MTInputs, the prototype's ScenarioDefinition): names and rows of legacy 465 (v0.8.4, user 2026-10-28).

Reads sheet MTInputs and the Name Manager of CPAT 1.0pre_465_NoPropData.xlsb and writes
  - the legacy-form cache (data/scripts/legacy_csv.py) mtinputs_465.csv: one row per input row of MTInputs: row, label, unit, legacy defaults,
    the legacy NameOfParameter (column H), the name the prototype uses, what changed and why (register code), the Name
    Manager name of the value cell (F) and of the other cells, and the Dashboard twin (D_<name>);
  - excel_ai/templates/MTInputs_template.xlsx, the build's row template: the legacy rows exactly (465: rows 329-330 of
    456, VslElSource and VslEl, are gone), with the prototype names in column H.

Names (user 2026-10-28): a complete set; column H as legacy, except bug L137 (the D_ prefix of 23 inputs, a trailing
space) and the rows legacy leaves without a name (issue I87), which get one. The inconsistencies that are issues stay
(I85 percentages typed as whole numbers, I86 spelling).

    python extract_inputs.py
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', 'data', 'scripts'))
from legacy_csv import legacy_dir, save_to_tidy  # noqa: E402,F401  (data/Public01/tidy/ in the legacy CSV form)
import csv
import os
import re
import struct
import zipfile

import openpyxl
from pyxlsb import open_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
LEGACY = os.path.join(HERE, '..', '..', 'data', 'legacy', 'CPAT 1.0pre_465_Shell.xlsb')
OUT = os.path.join(legacy_dir(), 'mtinputs_465.csv')
TEMPLATE = os.path.join(HERE, '..', 'templates', 'MTInputs_template.xlsx')
LAST = 413                                          # last row of MTInputs in 465

SECTIONS = {'Feebates sector coverage': 'FbCov', 'ETS: sector coverage': 'ETSCov',
            'CBAM Goods Non-Fuel Process Emissions': 'CBAMProc'}
SECTOR = {'power sector': 'Pow', 'road transportation': 'Rod', 'rail transportation': 'Ral', 'domestic aviation': 'Avi',
          'domestic shipping': 'Nav', 'residential sector': 'Res', 'residential': 'Res', 'food & forestry': 'Foo',
          'services (private / public)': 'Srv', 'mining & chemicals': 'Mch', 'iron and steel': 'Irn',
          'non-ferrous metals': 'Nfm', 'machinery': 'Mac', 'cement': 'Cem', 'other manucfacturing': 'Omn',
          'construction': 'Cst', 'fuel transformation': 'Ftr', 'other energy use': 'Oen'}
FUEL = {'Coal': 'Coa', 'Natural gas': 'Nga', 'Electricity': 'Ecy', 'Gasoline': 'Gso', 'Diesel': 'Die', 'LPG': 'Lpg',
        'Kerosene': 'Ker', 'Other oil products': 'Oop', 'Biomass': 'Bio'}
SECTOR2 = {'Power': 'Pow', 'Residential': 'Res', 'Industry': 'Ind', 'All': 'All'}
FPR = {'Starting price increase': 'FprStart', 'Final price increase': 'FprFinal', 'Price increase units': 'FprUnit'}
SCEN = {'Scenario status': 'ScenarioStatus', 'Scenario name': 'ScenarioName',
        'Scenario status for macro': 'ScenarioStatusMacro', 'Scenario parameters override?': 'ScenarioParamOverride'}


def legacy_cells():
    rows = {}
    with open_workbook(LEGACY) as wb:
        with wb.get_sheet('MTInputs') as sh:
            for row in sh.rows():
                for c in row:
                    if c.v is not None:
                        rows.setdefault(c.r + 1, {})[c.c] = c.v
    return rows


def defined_names():
    """{(column, row): [workbook-level names]} of MTInputs and {name lower: target} of every workbook-level name, from
    the BrtName records of xl/workbook.bin (parser of legacy/tools/xlsb_names.py)."""
    b = zipfile.ZipFile(LEGACY).read('xl/workbook.bin')

    def recs():
        i = 0
        while i < len(b):
            t = b[i]
            i += 1
            if t & 0x80:
                t = (t & 0x7f) | ((b[i] & 0x7f) << 7)
                i += 1
            sz = sh = 0
            for _ in range(4):
                x = b[i]
                i += 1
                sz |= (x & 0x7f) << sh
                sh += 7
                if not x & 0x80:
                    break
            yield t, b[i:i + sz]
            i += sz

    def wstr(d, o):
        n = struct.unpack_from('<I', d, o)[0]
        return d[o + 4:o + 4 + 2 * n].decode('utf-16le'), o + 4 + 2 * n
    sheets, xti, names = [], [], []
    for t, d in recs():
        if t == 156:
            _rid, o = wstr(d, 8)
            nm, o = wstr(d, o)
            sheets.append(nm)
        elif t == 362:
            n = struct.unpack_from('<I', d, 0)[0]
            xti.extend(struct.unpack_from('<iii', d, 4 + 12 * k) for k in range(n))
        elif t == 39:
            itab = struct.unpack_from('<i', d, 5)[0]
            nm, o = wstr(d, 9)
            cce = struct.unpack_from('<I', d, o)[0]
            names.append((nm, itab, d[o + 4:o + 4 + cce]))
    cells, every = {}, {}
    for nm, itab, r in names:
        if itab != -1 or not r or r[0] not in (0x3A, 0x5A, 0x7A):
            continue
        ix, row, col = struct.unpack_from('<HiH', r, 1)
        e, f, _l = xti[ix]
        sheet = sheets[f] if f >= 0 else f'ext{e}'
        colL = openpyxl.utils.get_column_letter((col & 0x3fff) + 1)
        every[nm.lower()] = f'{sheet}!{colL}{row + 1}'
        if sheet == 'MTInputs':
            cells.setdefault((colL, row + 1), []).append(nm)
    return cells, every


def new_name(r, label, section):
    lab = label.rstrip('?').replace('Apply tax to ', '').strip()
    if section in SECTIONS:
        return SECTIONS[section] + SECTOR[lab]
    if section == 'Fuel Price Reform':
        if label == 'Starting year':
            return 'FprIntro'
        if label == 'Target year':
            return 'FprOutro'
        m = re.match(r'(Starting price increase|Final price increase|Price increase units), (.+?)\s*, (\w+)', label)
        return FPR[m.group(1)] + FUEL[m.group(2).strip()] + SECTOR2[m.group(3)]
    return SCEN[label]


def rows():
    L = legacy_cells()
    cells, every = defined_names()
    out, section = [], None
    for r in range(8, LAST + 1):
        d = L.get(r, {})
        label = str(d.get(1) or '').strip()
        h = d.get(7)
        has_value = any(k in d for k in (4, 5, 6))
        unnamed_input = has_value and (label in SCEN or section in SECTIONS or section == 'Fuel Price Reform')
        if not h and not unnamed_input:
            if label:
                section = label
            out.append(dict(row=r, kind='heading' if label else 'blank', label=label))
            continue
        name, change, code = h, '', ''
        if h is None:
            name, change, code = new_name(r, label, section), 'name added (legacy has none)', 'I87'
        elif h != h.strip():
            name, change, code = h.strip(), 'trailing space removed', 'L137'
        elif h.startswith('D_'):
            name, change, code = h[2:], 'D_ prefix dropped (D_ names the Dashboard cell)', 'L137'
        twin = every.get('d_' + name.lower()) or (every.get(h.strip().lower()) if h and h.startswith('D_') else '')
        out.append(dict(row=r, kind='input', section=section, label=label, unit=d.get(2) or '',
                        legacy_default=d.get(6), legacy_name=h or '', name=name, change=change, register=code,
                        name_manager_F=';'.join(cells.get(('F', r), [])),
                        name_manager_other=';'.join(f'{c}{rr}:{n}' for (c, rr), ns in cells.items() if rr == r
                                                    and c != 'F' for n in ns),
                        dashboard_twin=twin or ''))
    names = [o['name'] for o in out if o['kind'] == 'input']
    assert len(names) == len(set(names)), [n for n in names if names.count(n) > 1]
    return out


def write_template(data):
    wb = openpyxl.load_workbook(TEMPLATE)
    ws = wb['MTInputs']
    if ws.cell(329, 8).value == 'VslElSource':          # the 456 template: drop the two rows 465 deleted
        ws.delete_rows(329, 2)
    by = {o['row']: o for o in data}
    for r in range(8, LAST + 1):
        o = by[r]
        lab = str(ws.cell(r, 2).value or '').strip()
        assert lab == o['label'], (r, lab, o['label'])
        if o['kind'] == 'input':
            ws.cell(r, 8).value = o['name']
    ws['B1'] = 'MTInputs template - row structure copied exactly from legacy CPAT MTInputs (CPAT 1.0pre_465)'
    ws['B3'] = ('Rows must match legacy 465 exactly. Column H: the names of the codes map (tab Inputs; legacy name kept '
                'there). See NORMS.md section 4.')
    for rr in range(LAST + 1, ws.max_row + 1):
        assert all(ws.cell(rr, c).value is None for c in range(1, 9)), rr
    wb.save(TEMPLATE)


def main():
    data = rows()
    cols = ['row', 'kind', 'section', 'label', 'unit', 'legacy_default', 'legacy_name', 'name', 'change', 'register',
            'name_manager_F', 'name_manager_other', 'dashboard_twin']
    with open(OUT, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        for o in data:
            w.writerow({k: o.get(k, '') for k in cols})
    write_template(data)
    n = [o for o in data if o['kind'] == 'input']
    print(f'wrote {OUT}: {len(n)} inputs ({sum(1 for o in n if o["register"] == "L137")} renamed, bug L137; '
          f'{sum(1 for o in n if o["register"] == "I87")} names added, issue I87); template {TEMPLATE} on 465 rows')


if __name__ == '__main__':
    main()
