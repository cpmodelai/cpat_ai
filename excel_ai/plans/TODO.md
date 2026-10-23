# TODO - Excel-AI, open work (one list, in order)

Status key: ☐ not started · ◐ in progress · ⏸ waiting. Done work is logged in [`../../CAVEATS.md`](../../CAVEATS.md). Plans with details: one file per plan in this folder. Python work: [`../../coded/TODO.md`](../../coded/TODO.md).

## 1. Release v7.2 and the clean-up: done (2026-10-22)

- ☑ v7.2 full check PASS, on main; restructure (`excel_ai/`, `data/`, `coded/`, `other/`); history reset; v8.0 prototype naming, stable script names, `_latest` and `_v8.0` copies; one NORMS; plans split; short documentation and Methods volume.

## 2. Clean-up, left over

- ☑ v8.0 full check PASS; old method notes replaced by `docs/methods/`; v8.0 on main.
- ☐ Old session branches on GitHub (7, old history): the user deletes them (or allows the AI to).
- ☐ The register spreadsheet without `LegacyBugFixes.md` as an intermediate source.

## 3. Modular CPAT ([`Modules.md`](Modules.md); after 2)

- ☑ **M1 money units** (v8.1): one vocabulary (`USD`, `USD m`, `USD bn`, `LCU`, `USD/GJ`, ... real/nominal; never `$`); labels only.
- ☑ **M2 prototype exports** (v8.1; 19b/19c come with M4): Mitigation section 15 (air pollution) moved to the end; new section 19 "Exports to modules" (19a Distribution, 19b AP right after section 15, 19c TCB; one defined name each, plain copies, codes as keys, a scale column); a `FromMitigation` tab first for Distribution, which reads only it (no hard-coded `Billion`/`Thousand` scaling).
- ☑ **M3 standalone Distribution v1.0**: `excel_ai/distribution/` (cut from the built prototype; Cover with the link to `CPAT-AI-Mitigation-Prototype_latest.xlsm`, button Update from Mitigation; check PASS: equal to the prototype cell for cell, and end to end). Left: a data-workbook link for its data tabs (Update data tables), and Excel 365 test of the macro.
- ☐ **M4 AP and TCB v0.1**: export blocks and small workbooks with the data import and export only (no model).
- ☐ **M5 documents** for the modules.

## 4. Codes leftovers (after 3)

- ☐ Crosswalk rows marked review (89): `rnew`, `rsub`, `rmf`, `rtx`, `rnet`, `rvt`, `rbe`, `gdp.*`, `scc`, `ch4.em`, `co2.sec`, `apf.all.all`, other price rows; applied only with evidence.
- ☐ C6 vocabularies (prototype members `vkt`, `own`, `pit`... into the sheets); the legacy MTOutputs code as a second alias; `coded` `ele` -> `ecy` with the shared data (with the Coded CPAT owner).
- ☐ NOx forcing value differs from legacy (prototype `apf.all.nox`, now `nox.tot`: -6.3 against legacy -5.5 Mt CO2e, Egypt 2022): a value question, not a code one; register it if not already explained.

## 5. With the user

- ☐ **Excel 365 review** on Windows (macros, no repair prompt, no circular warning, CheckBatchRun, LAMBDAs, dashboard).
- ☐ **ETS goal seek (I30)**: tested by the user.
- ☐ **Data requests**: I64 GAINS factor paths, I65 blank VAT cells, I13 proprietary tables for other countries, I68 historical GHGs 2018-2020.
- ☐ **Report the legacy bugs to the CPAT team** (the register); high-priority legacy issues for them: I62, I71, I72-I74.
- ☐ **Policy taxonomy with the FTT policies** ([`Policy_taxonomy.md`](Policy_taxonomy.md)): user decisions first.

## 6. AI backlog

- ☑ **New legacy file**: the register, fix plans and lists moved to the latest file, 465 (v8.2, 2026-10-23; 459 superseded); the CPAT team's 62 fixes checked (52 confirmed, 8 with caveats, L62 and L63 not fixed; `../bugsfixed/`).
- ☐ **Legacy 465 follow-up**: tell the CPAT team the caveats (L115 wrong row, L95 rows still reading the cleared row 3719, L62 and L63 not fixed, L45, L16, L87, L84; Appendix B of the register); numerical check against the legacy Egypt run sector by sector on 465 (U2, I14); `CPATMasterProcessesCodesAndDefaults.xlsx`.
- ☐ **Prototype data extracts on 465**: the extracts (`extract_*.py`) and the Methods still read 456; move them when the numerical check (U2) is done.
- ☐ **Data links, rest**: GHGs, EF_GHG, CH4Inputs, Elasticities, Prices_int, OilProductShares (converters to the prototype layout), Transport1-2 (no dummy data yet).
- ☐ **Excel lint in every builder** (NORMS 3g).
- ☐ **Copy-paste stress test**: add a fuel, a subsector and a scenario by dragging; fix what breaks.
- ☐ **Tracker leads**: legacy electricity price controls (Manual inputs J178:J179) read by nothing?; ScenarioDefinition 182-183 units.

## Later (not now)

- Power engineer model: final deficit to gas, MaximumGasCF, storage factor; planned retirement data; elasticity-based power model.
- Regulations as shadow prices; green public investment; ETS benchmarks by sector; inventory-adjusted EFs and process CO2; legacy block F reports (social costs, Kaya, CBAM, policy coverage).
- Data for more countries; Python port (`../coded/TODO.md`).
- AP and TCB models ([`Air_pollution.md`](Air_pollution.md), [`Transport_cobenefits.md`](Transport_cobenefits.md)) beyond the data parts.

Dropped by the user: engineer road model follow-ups (I61), demand on real local-currency prices (I63).
