# TODO - Excel-AI, open work (one list, in order)

Status key: ☐ not started · ◐ in progress · ⏸ waiting. Done work is logged in [`../../CAVEATS.md`](../../CAVEATS.md). Plans with details: one file per plan in this folder. Python work: [`../../coded/TODO.md`](../../coded/TODO.md).

## 1. Release v7.2 and the clean-up: done (2026-10-22)

- ☑ v7.2 full check PASS, on main; restructure (`excel_ai/`, `data/`, `coded/`, `other/`); history reset; v8.0 prototype naming, stable script names, `_latest` and `_v8.0` copies; one NORMS; plans split; short documentation and Methods volume.

## 2. Clean-up, finishing

- ◐ v8.0 full check running; then: the old method notes in `mitigation/` replaced by `docs/` (builder texts point to the Methods chapters), commit, push v8.0 to main.
- ☐ Old session branches on GitHub (7, old history): the user deletes them (or allows the AI to).
- ☐ The register spreadsheet without `LegacyBugFixes.md` as an intermediate source.

## 3. Modular CPAT ([`Modules.md`](Modules.md); after 2)

- ☐ **M1 money units**: one vocabulary (`USD`, `USD m`, `USD bn`, `LCU`, `USD/GJ`, ... real/nominal; never `$`); labels only.
- ☐ **M2 prototype exports**: Mitigation section 15 (air pollution) moved to the end; new section 19 "Exports to modules" (19a Distribution, 19b AP right after section 15, 19c TCB; one defined name each, plain copies, codes as keys, a scale column); a `FromMitigation` tab first for Distribution, which reads only it (no hard-coded `Billion`/`Thousand` scaling).
- ☐ **M3 standalone Distribution v1.0 (priority)**: own workbook built from the same code, data-link Cover to `CPAT-AI-Mitigation_latest.xlsm` and the data workbook, its scenario inputs and data tabs; one scenario at a time (no batch interaction); check: equal to the prototype's Distribution cell for cell.
- ☐ **M4 AP and TCB v0.1**: export blocks and small workbooks with the data import and export only (no model).
- ☐ **M5 documents** for the modules.

## 4. Codes leftovers (after 3)

- ☐ Crosswalk rows marked review (89): `rnew`, `rsub`, `rmf`, `rtx`, `rnet`, `rvt`, `rbe`, `gdp.*`, `scc`, `ch4.em`, `co2.sec`, `apf.all.all`, other price rows; applied only with evidence.
- ☐ C6 vocabularies (prototype members `vkt`, `own`, `pit`... into the sheets); the legacy MTOutputs code as a second alias; `coded` `ele` -> `ecy` with the shared data (with the Coded CPAT owner).

## 5. With the user

- ☐ **Excel 365 review** on Windows (macros, no repair prompt, no circular warning, CheckBatchRun, LAMBDAs, dashboard).
- ☐ **ETS goal seek (I30)**: tested by the user.
- ☐ **Data requests**: I64 GAINS factor paths, I65 blank VAT cells, I13 proprietary tables for other countries, I68 historical GHGs 2018-2020.
- ☐ **Report the legacy bugs to the CPAT team** (the register); high-priority legacy issues for them: I62, I71, I72-I74.
- ☐ **Policy taxonomy with the FTT policies** ([`Policy_taxonomy.md`](Policy_taxonomy.md)): user decisions first.

## 6. AI backlog

- ☐ **New legacy file 459**: reconcile the register and fix plans (keyed to 456); numerical check against the legacy Egypt run sector by sector (I14); `CPATMasterProcessesCodesAndDefaults.xlsx`; `Tracking issues.xlsx`.
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
