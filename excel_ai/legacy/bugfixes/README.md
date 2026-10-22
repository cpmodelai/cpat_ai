# Legacy CPAT bug-fix plans (cell by cell)

Manual fix plans for the legacy workbook `excel_ai/legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb` (sheet Mitigation). For every bug: the cell, its current formula, the new formula, the columns to fill and the policy-block row. Bug IDs follow the register (`excel_ai/mitigation/LegacyBugFixes_v7_0.md` for L1-L50; `excel_ai/mitigation/LegacyBugFixes_v5_4.md` and `issues_register_v5_4.py` for the later ones). All 49 legacy bugs of the v4.0 register (L1-L50; L17 was an MVP bug) are covered, plus two new ones (N1, N2), and 15 engineer-power bugs of the v5.4 register: L52-L56, L67, L83, L84, L88, L95, L107-L111 (64 bugs in all).

**Since 2026-10-22 the plans are printed in the one register, `../CPAT-AI-Mitigation-MVP_BugsAndIssues_v7.2.docx` (section 3: power, transport, other mitigation in 10 areas by priority, distribution), and exported with it to `../CPAT-AI-Mitigation-MVP_BugsAndIssues_v7.2.json`** (`excel_ai/mitigation/make_bugfix_book_v7_0.py`). The separate Word and PDF plans were retired (git history). This folder keeps their sources:

| File | Content |
|---|---|
| `data/fixes_power_engineer.json` | Engineer power model: L1-L12, L52-L56, L67, L83, L84, L88, L95, L107-L111, L126, L127 |
| `data/fixes_transport_engineer.json` | Engineer road-transport model, L25-L41 |
| `data/fixes_other_mitigation.json`, `fixes_other_mitigation_2.json` | Other mitigation, both batches (L13-L24, L42-L51, L57-L125, L128, N1, N2) |
| `data/cfg_other_sections.json` | The 10 other-mitigation areas (ETS, prices, ...) in rough priority order: the register's section 3.3 follows it; move a bug by editing its `ids` |
| `data/fixes_distribution.json` | Distribution module, D1-D31 |
| `data/fixes_*.json` (all) | Machine-readable (`cell`, `now`, `new`, `fill`, `policy` per cell); usable for a fix macro |
| `data/cfg_*.json` (others) | Texts of the retired Word plans (title, intro, order) |
| `data/legacy_defined_names.tsv` | All 1,942 defined names of the legacy file and the cells they point to |
| `tools/` | Scripts that produced the plans (below) |

## Findings to know before applying

- L15 and L18 do not reproduce in this file (no cell to change); L22 needs inserted rows; L107 needs a new MTInputs input row and defined name (appended as row 416) besides its cell edits.
- L50: the current-account rows read WEO codes the WEO sheet does not have and an empty defined name (WEO); the "reversed sign" of rows 18215-18219 is a label error (rows 741-743 are a trade balance).
- Policy block: +6,331 rows below the baseline up to about row 6070, +6,317 after. L43's policy rows are edited by hand.
- The transport fixes change only the engineer run (the legacy Egypt run uses TrModel = Elasticity).
- N1 and N2 are not in the register; confirm before applying.
- L32: the defined names in G4376:G4378 and G4419:G4421 point to the wrong rows of the EF table; the fix references the road rows (O988, O990, O991) directly.
- L36: the formula's reading of the charging-subsidy inputs matches the default values, so the fix keeps it and relabels Dashboard C95:C98.
- L28: a helper cell J2168 holds the freight share at the last data year, so row 2168 does not point into itself.
- Made from the legacy file as it was before commit d82efd0 restored the original; the Mitigation formulas (A:AF, rows 1-15000) of the restored original are identical, including every cell in the plans.
- The LibreOffice conversion drops the first argument of the newer functions (`_xlfn.IFNA`, `_xlfn.XLOOKUP`) and garbles `LET`: 23,115 Mitigation cells (rows 1-15000) read wrong in the .xlsx, e.g. L5568 shows `=_xlfn.IFNA(0)` for `=_xlfn.IFNA(IF($L$1784=B5568,$K$1795*L5554,0),0)`. `tools/dec.py` decodes the formulas from the .xlsb itself; `tools/chkplans.py` checks every plan's "now" against it. All power and transport cells agree; in the other-mitigation plan L48 (L5564-L5566, L5568-L5570) and L50 (L18197, L18206) were built from truncated texts and must be redone before use (L50 finding (c) is wrong: rows 18197 and 18206 do look up `INDEX(WEO, ...)`, the empty name). Not corrected here.
- Register L87 rests on such a truncated text: C2371 is `=_xlfn.IFNA(INDEX($F$86:$F$90,MATCH(C2370,$C$86:$C$90,0)),0)`; it reads F86:F90 but never matches, because C86:C90 hold " - " & the scenario name. The share is still 0.
- Rows 2377-2388 (shadow prices with the regulation term): their policy copies 8708-8719 keep `$D$2369` and `L$2375`, so in the policy block the regulation term reads the baseline general carbon price (0 in the file). Not in the register; the L88 fix does not use these rows.
- L108: rows 7897-7903 sit at +6,317 in the policy block but read the power rows at +6,331, so their policy formulas are spelled out (as for L43).
- The file holds 35,787 single-cell array formulas in Mitigation (e.g. P2981:T2985, L52); `tools/pol.py` now compares their text.
- Nothing was recalculated in Excel. Effects: Python copies of the legacy power and road models (`excel_ai/mitigation/power_model_ref_v4_0.py`, `transport_model_ref_v4_0.py`; the same models as v3.8, when the plans were made), cached values and the register.
- Log: `CAVEATS.md`, entries "Legacy CPAT bug-fix plans" (2026-10-16). 2026-10-19: power plan extended by the 15 v5.4-register bugs (L52-L56, L67, L83, L84, L88, L95, L107-L111; effects from the register and `power_model_ref_v5_4.py`); tools `dec.py`, `h.py`, `dumpo.py`, `gen_pow2.py`, `chkplans.py`, `arr.py` added, `pol.py` and `render.js` fixed (array formulas; multi-line formulas and non-"fix" statuses).


- Batch 2 (other mitigation and distribution, 2026-10-19): **the LibreOffice conversion replaces every formula containing IFNA by a constant** (e.g. `=_xlfn.IFNA(0)`); `tools/dec.py` (or `dec_cells.py Mitigation C2371`) decodes formulas straight from the .xlsb. Every "formula now" on sheet Mitigation of batch 2 was checked against the .xlsb (144 cells, all match). L48 and L50 were redone from the .xlsb on 2026-10-19 (`tools/gen_redo.py`): L48 keeps only the income factor and the starred-Yes test (the exemption split already exists); L50 keeps legacy's carry-forward and changes only the name WEO -> WEO_upd and the codes. All 362 "formula now" cells of every plan were checked against the .xlsb: no other mismatch. L92 does not reproduce (I1784 is a live formula in the .xlsb); L66 is covered by L43; L86's real cause is the range of the names _manual_codes/_manual_prices (stop at row 133), same edit as L100.
- Found while planning and registered 2026-10-19: L115 (Mitigation L2555 reads the LPG ETS row 1720 instead of 1715), L116 (Elasticities H53/H54), L117 (Multipliers D44); the kerosene rows 5587/5588 are already in L45.
- Distribution D10-D31 (2026-10-20, v6.2 register; scratch generator `gen_D10.py`, not kept): every "now" decoded from the .xlsb; `chkplans.py` agrees on all 62 single cells of D10-D31 (the 7 D24 range entries are skipped; the 6 differences it reports are D2's empty "now" written as "" and D7's array braces). D24 needs inserted rows and is applied last; D22, D25 and D23 come before it. Rows L3049:L3062 (D31) and D25's top-20 ties (row 3277) were added while planning.

## How the plans were made (Linux, LibreOffice)

1. Convert the .xlsb to .xlsx with LibreOffice; `tools/dump.py <xlsx> f.pkl v.pkl` caches the Mitigation formulas (rows 1-15000).
2. `tools/fnames.py Mitigation` recovers the defined names per cell from the .xlsb (`cellnames.json`), which replace the `#NAME?` of the conversion; `tools/vals.py Mitigation MTInputs UNPop "Manual inputs"` reads the cached values (`cv.pkl`); `tools/names.py` writes `legacy_defined_names.tsv`. Set the .xlsb path at the top of each script.
3. `tools/gen.py` (power L1-L12 and other mitigation), `tools/gen_pow2.py` (power L52-L111: "now" decoded from the .xlsb by `dec.py` (needs `pip install pyxlsb2` for the function table) and cross-checked with the .xlsx text via `h.py`, which reads `f.pkl`, `cellnames.json`, `cv.pkl` and `fo.pkl` from `dumpo.py <xlsx> Power CoC MTInputs Dashboard`; it also checks every fill range and policy row cell by cell), `tools/gen_A.py`-`gen_D.py` (other mitigation batch 2), `gen_E.py` (distribution; both read formulas through `q.py` and, for IFNA cells, `dec_cells.py`), `tools/gen_tr.py` (transport) and `tools/gen_bop.py` (L49, L50; rows 18165-18225 and 735-745 read into `bop.pkl` the same way as step 1) build each new formula by exact text substitution of the legacy formula; they stop if the legacy text is not found and check the brackets. Output: `partA.json`, `partB.json`, `partT.json` (= `data/fixes_*.json`).
4. (Retired 2026-10-22; the register prints the plans.) `tools/render_other.js` (other mitigation by area) and `tools/mk2.py` turns `tools/render.js` into `render2.js`; `node render2.js <out.docx> data/cfg_<name>.json` writes each document (npm `docx`).

`tools/show.py`, `grp.py` (formulas of a row grouped by identical R1C1 pattern), `pol.py` (finds the policy-block row of a baseline row), `dec.py Sheet A1,B2:C3` (formula text from the .xlsb), `arr.py` (array-formula ranges) and `chkplans.py data/fixes_*.json` (checks every "now" against the .xlsb) are the inspection helpers.
