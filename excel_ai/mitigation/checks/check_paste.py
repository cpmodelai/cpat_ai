"""v0.4.4 copy-paste test, scenario capacity (NORMS 3e; run at every release that touches the column groups, about
3.5 minutes since v0.4.9): python check_paste.py CPAT-AI-Mitigation-Prototype-v0.7.0.xlsm
Paste scenario group 2 into groups 3-6 (plain copy-paste; v0.7.0: two groups shipped), recalculate with the
LAMBDAs expanded, and check: no error values on any sheet; the pasted groups number themselves 3-6; every pasted
group whose scenario has a StoredResults ID equals it by output code (Python emulation of RunAllScenarios); every
difference row equals its level minus scenario 1's level (v0.4.7: a definition with a new ETS is compared too: the
build stores it at the price estimate, without the ETS goal seek). Distribution groups 4-7 are pasted the same way.
v0.4.1-v0.4.3: groups 3 and 4 only. v0.4.9: the paste is written into the file's XML with the LAMBDA expansion
(lo_session.expanded_zip), and the values are read in a LibreOffice session; the stored results are read
meanwhile."""
import os as _os, sys as _sys  # the excel_ai code folders and data/scripts on the path (core/tools/xlpaths.py)
_xl = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_xl) != 'excel_ai':
    _xl = _os.path.dirname(_xl)
_sys.path.insert(0, _os.path.join(_xl, 'core', 'tools'))
import xlpaths  # noqa: E402,F401
import sys, os, time
sys.path.insert(0, os.getcwd())
import openpyxl
import build as B, check_full as C
import lo_session as LO

PASTE = (3, 4, 5, 6)                      # groups pasted: scenarios 3-6 (v0.7.0: two groups shipped, no LAMBDA test group)
ETS_GOALSEEK = {}   # v0.4.7: the build no longer goal-seeks (user rule 2026-10-17), so a new ETS is compared too
ERRORS = ('#DIV/0!', '#N/A', '#NAME?', '#NULL!', '#NUM!', '#REF!', '#VALUE!', 'Err:')   # not a literal '#' header


def pastes(cols, width):
    """v0.4.9: group 2 copy-pasted into the groups PASTE, in the file's XML (lo_session.expanded_zip; formulas
    shifted by build.shift_cols, identical to openpyxl's Translator for these same-row copies)."""
    s0 = cols(2)[0]
    return (s0, s0 + width - 1, [cols(g)[0] for g in PASTE])


if __name__ == '__main__':
    t0 = time.time()
    path = sys.argv[1]
    plan = {'Mitigation': pastes(B.group_cols, B.GW)}
    wb = openpyxl.load_workbook(path, read_only=True)
    if 'Distribution' in wb.sheetnames:
        plan['Distribution'] = pastes(B.dist_group_cols, B.DGW)
    wait = LO.start_values(LO.expanded_zip(path, C.LAMBDA_CALL, C.expand, plan, B.shift_cols), ['Mitigation'])
    stored = {}                                   # meanwhile: the stored results
    for row in wb['StoredOutputs'].iter_rows(min_row=6, values_only=True):
        if row[0] and row[3]:
            stored.setdefault(row[0], {})[row[3]] = row[7:7 + B.NY]
    data, errs = wait()
    errs = [e for e in errs if not B.cmp_na_only(*e)]   # v0.6.4: #N/A of the empty dashboard slots (chart gaps)
    ok = not errs
    for sheet, rng in errs:
        print('error values', sheet, rng[:200])
    d = data['Mitigation']
    g1 = B.group_cols(1)[0]
    chk = [(B.R_E11B['echg.all'], B.R_TOTAL), (B.R_REV['rtot.chg'], B.R_REV['rtot.all']), (B.R_EMI['co2.chg'], B.R_EMI['co2.all']),
           (B.R_GHG['ghg.chg'], B.R_GHG['ghg.all'])]
    for g in PASTE:
        c0 = B.group_cols(g)[0]
        scen = d.cell(B.R_SCEN, c0).value
        ok &= scen == g                     # v0.7.0: group g numbers itself g (no LAMBDA test group)
        n, mx, worst = 0, 0, None
        for r in range(1, d.max_row + 1):
            code = d.cell(r, c0).value
            if code in stored.get(scen, {}):
                for k in range(B.NY):
                    a, b = d.cell(r, c0 + 1 + k).value, stored[scen][code][k]
                    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        n += 1
                        if abs(a - b) / max(1, abs(b)) > mx:
                            mx, worst = abs(a - b) / max(1, abs(b)), (code, B.BASE_YEAR + k)
        ets = ETS_GOALSEEK.get(scen)
        if ets:                                   # the batch macro runs the ETS goal seek; a pasted group the estimate
            md = max(abs(d.cell(rd, c0 + 1 + k).value - (d.cell(rl, c0 + 1 + k).value - d.cell(rl, g1 + 1 + k).value))
                     for rd, rl in chk for k in range(B.NY))
            ok &= md < 1e-6
            print(f'group {g}: scenario {scen} (new ETS: StoredResults holds the goal-seek price, the pasted group the '
                  f'fast estimate; not compared: max rel diff {mx:.3g} at {worst}); differences vs scenario 1: {md:.3g}')
            continue
        md = max(abs(d.cell(rd, c0 + 1 + k).value - (d.cell(rl, c0 + 1 + k).value - d.cell(rl, g1 + 1 + k).value))
                 for rd, rl in chk for k in range(B.NY))
        ok &= mx < 1e-6 and md < 1e-6
        print(f'group {g}: scenario {scen} ({d.cell(B.R_NAME, c0 + 1).value}); vs StoredResults: {n} values, '
              f'max rel diff {mx:.3g} (at {worst}); differences vs scenario 1: max abs diff {md:.3g}')
    print('PASS' if ok else 'FAIL', f'{time.time() - t0:.0f} s')
