# Codes remediation plan: bringing the prototype onto the CPAT code protocol

Status: **plan, not built; blocked until the prototype rebuild in progress is finished** (queue: `../TODO_Codes.md`). The user's decisions of 2026-10-21 are in. The work goes in small steps (R0-R9). Each step is built and checked on its own and can be undone on its own.

References:
- **Protocol:** sheet `Protocol` of `CPAT_CodesMap_v0_7_1.xlsx`, rules C0-C11. The workbook also holds the evidence: sheets `Crosswalk`, `LiveOutputs`, `MVPOnly` and `Checks`.
- **Builder:** `make_codes_map_v0_7_1.py`.
- **Crosswalk data:** `data/mvp_legacy_extracts/codes_crosswalk_v0_7_1.csv` (233 rows).

## 1. Decisions (user, 2026-10-21)

| # | Decision | Effect on the work |
|---|---|---|
| D1 | Variable names: legacy's, where legacy computes the same quantity. Codes: self-consistent, in the protocol's structure for every variable, so legacy's whole code is an alias where its structure differs (C11) | 169 Crosswalk fix codes in protocol form; 89 rows marked `review` (51 partial, 4 unsure, 34 with no mechanical fix) are settled before their step |
| D2 | No model letters at all (C7) | 1,935 prototype codes lose `.e` (863) or `.a` (1,072); the power model has none already. No two prototype codes become equal. Legacy's lettered codes are aliases |
| D3 | `tot` for totals; `all` fills an unused slot (C5) | Only totals change. About 150 `all` rows are explicit sums over members and are clear candidates; the other `all` rows stay. `code_formula` keeps its fixed sector and fuel slots |
| D4 | Generation units: `gen` becomes `gen_mwy`; `gen_gwh` and `gen_ktoe` are added only if an output needs them | One rename in step R1 |
| D5 | N2O and NOx are different gases; `nox` is NOx | Checked in the 456 file, Egypt, 2022 (detail below). The prototype will carry `n2o.tot` and `nox.tot`; legacy's codes are aliases and both go in the register as a legacy bug |

D5 detail, as found in the legacy file:
- Legacy row 7628 is labelled "Nitrous oxide (N2O)" and holds 28.5 Mt CO2e. It adds into total GHGs (307.6 + 53.1 + 28.5 + 11.7 = 400.9). Its code is `nox.tot`.
- The real NOx row is 7634, labelled "Nitrogen oxides (NOx, exc. N2O)". It holds -5.5 Mt CO2e, a cooling forcing. Its code is `oc.tot.`: organic carbon's code, with no scenario number. The same applies to rows 13945 and 13951.
- The prototype already has the right quantities under other names: `ghg.all.n2o` (28.5, equal to legacy) and `apf.all.nox`.
- `apf.all.nox` is -6.3 against legacy's -5.5. That value difference is outside this plan.

## 2. How the rename works without breaking anything

**One rename map, applied only where text is written.** The build keeps its internal variable names: the Python row dictionaries, formulas, LAMBDAs and cell references stay as they are. A rename map changes only the text the build writes out:

1. columns A (variable), B (fuel) and C (sector) of a Mitigation row;
2. the key of the variable dictionary (sheet `Check, Variables, Lambdas`);
3. the member-label pairs;
4. the code literals of LiveOutputs, StoredOutputs and ScenarioCompare;
5. the code end of the dictionary (column K, `.e.`, `.a.` or `.`), which is where the model letters come from: dropping them is one column.

The code cell formula (`code_formula`) is unchanged. It still builds the code from A, C, B and the dictionary, so codes follow automatically and copy-paste of rows and scenario groups works as before.

**What must not be renamed.** Three LAMBDAs select Mitigation rows by the text in columns A-C:
- `FUELSPEND` and `FUELQTY` use `SecVar = "atp"` and `"ener"`, and the fuel;
- `BLOCKQTY` uses `PVar = "atp"`.

These variables keep their names. A `tot` total row must stay out of their fuel matches (it does: they match a single fuel). The step check below catches any other text match.

**The map file.** `data/mvp_legacy_extracts/code_renames_v0_7_2.csv` has these columns:
- `step`;
- `kind`: variable, member, row (one row's sector or fuel token, for totals) or codeend (a variable's code end);
- `old`, `new`;
- `scope`: the variable, for member and row renames;
- `crosswalk_ref`;
- `status`: planned or applied.

The build, the checks and the codes map all read this one file. A step is undone by setting its rows back to planned.

**Every step follows the same loop.** No step needs the full check.

| # | Action | Time |
|---|---|---|
| 1 | Set the step's map rows to applied | - |
| 2 | Build (`build.py`) | 2-3 min |
| 3 | `check_codes_v0_7_2.py`, a new structural check with no recalculation (detail below) | about 1 min |
| 4 | Quick check with a rename-aware regression: old codes are mapped before comparing. The pass condition is 0 changed, 0 new, 0 gone, and no error values | 1.5-3 min |
| 5 | Rerun `make_codes_map_v0_7_1.py`: Crosswalk rows done, the Checks counts | seconds |
| 6 | One commit per step (when the user wants commits) | - |

What `check_codes_v0_7_2.py` checks:
- it compares every cell of the new workbook with the last release, and every difference must be explained by the map;
- every code is unique;
- every code that LiveOutputs, StoredOutputs or ScenarioCompare reads exists in Mitigation.

Because the map changes only text, a value change at step 4 means a missed text reader. The step is reverted, not patched forward.

The full check, the paste test, the Word documents and the deck run once, after R9.

## 3. Steps

| Step | What | Size | Notes |
|---|---|---|---|
| **R0** | The mechanism, with an empty map: map loader, the five write points, `check_codes`, rename-aware regression in `check_quick`. Version per `NORMS.md` 5 (the release before it to `Old/`) | build edits in about 6 places | Pass: the workbook equals the last release cell for cell. Then a dry run with one rename (`gen` -> `gen_mwy`), reverted, to prove the loop |
| **R1** | Model letters: every variable's code end becomes `.` (D2) | 1,935 codes, one dictionary column | The largest change by count and the simplest: the best first real use of the loop |
| **R2** | Power model: `gen` -> `gen_mwy`, `usd` -> `nid`, `reteff` -> `rec`, `ccp` -> `xac`. Totals `captot` -> `cap.pow.tot`, `gtot` -> `gen_mwy.pow.tot`, `nimtot` -> `nim.pow.tot`, `usdtot` -> `nid.pow.tot` | 8 variables | `pe` and `dem` keep their prototype names: renamed to `ener`, with no model letters, they would equal the elasticity rows `ener.pow.<fuel>` and `ener.<sector>.ecy` |
| **R3** | Prices and policies: `psp` -> `ps`, `pets` -> `etsnew`, `rpb` -> `pbc`, `txfx` -> `fadtx`, `txfl` -> `cs`, `incf` -> `inc.ela.adj`, `cpi` -> `tcp`, and the rest of the price rows of the Crosswalk | about 12 variables | `shp` and `pros` keep the prototype's sector-first order (legacy's fuel-first codes are aliases; the Prices_dom data keys stay as legacy, C9) |
| **R4** | Transport: `trevst`/`trevsf`/`trevsc` -> `stockcalc`; `trevcc`… -> `shrcalc`; `trevsh`… -> `shract`; `trkmp`/`trkmf`/`trkmc`/`trkmt` -> `pass`/`fre`/`motor`/`all.vkt`; `trvht`… -> `*.own`; `trafg`/`trafo`/`trafe` -> `fecon`; `trkt` -> `tot.rod`. Vehicle members `pas` -> `pass`, `cyc` -> `motor` (legacy `freight` -> `fre`) | about 25 variables, 2 members | The road engineer model only |
| **R5** | Emissions: `ap`/`aps` -> `em` (`em.<sector>.<pollutant>`); `apf.all.<pol>` -> `<pol>.tot`; `ghg.all.n2o` -> `n2o.tot`, `apf.all.nox` -> `nox.tot` (D5); `ghg.all.<gas>` -> `<gas>.tot`; `co2.sec.*` -> `co2` in the protocol structure | about 10 variables | Legacy `em` is in t/yr, the prototype in kt: the unit stays in the dictionary |
| **R6** | Fiscal and welfare: `rtot`, `rnet`, `rfu`, `rsub`, `rmf`, `rpct` -> `rev.*`; `gdp.*`, `wel.*`, `scc.*` sub-codes as legacy | about 20 variables | The fiscal rows, after their review |
| **R7** | Totals: `all` -> `tot` on the total rows (about 150 explicit sums, plus totals written another way, found per variable). The section 11 copies (17 duplicate codes) read the section 5-8 rows and drop their own code | row renames | Check: no duplicates; the LAMBDA text matches unaffected |
| **R8** | Output sheets: LiveOutputs, StoredOutputs and ScenarioCompare carry the protocol codes, with the legacy MTOutputs code in an alias column (C11b); the macro accepts the old prototype codes for one release (alias lookup) | output sheets, macro | Saved StoredOutputs and ScenarioCompare selections keep working |
| **R9** | Outside the workbook: `check_v7`, `legacy_compare`, `check_links`, the Python references; `coded` `ele` -> `ecy` and the shared codes; register (one issue: legacy code inconsistencies; legacy bugs: duplicated codes, capitals, empty tokens, `nox.tot`/`oc.tot.`); the protocol checks (C1, C5, C6, C7, C10) added to `check_quick`; full check, paste test, documents | scripts, register | After this, a new row in the old style fails the quick check |

The order is R0, then R1 (one dictionary column) and R2 (the best-evidenced renames). R3-R6 can go in any order. R7 and R8 come after the renames they rely on. Before each of R2-R6, a person settles that step's `review` rows in the Crosswalk: a rename is applied only with evidence.

## 4. Parallel work

R0 is the only step that edits the build's logic. It touches `code_formula`'s neighbours, the dictionary writer, the member table and the output code lists, so it should go on a branch from the latest main and be merged quickly.

After R0, every rename is a row in the CSV. That rarely conflicts with other work. A new row that reuses a renamed variable is renamed with it. Until R9 adds the protocol check, new variables should already follow the protocol: legacy variable names, no model letter, `tot` for totals, members from the vocabularies.
