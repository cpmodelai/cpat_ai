# TODO - Excel-AI, open work only (one list, in order)

Status key: ☐ not started · ◐ in progress · ⏸ waiting. Done work is logged in [`../CAVEATS.md`](../CAVEATS.md). Plans with details: [`mitigation/Plans.md`](mitigation/Plans.md) (sections named below). Python work: [`../coded/TODO.md`](../coded/TODO.md).

## 1. Now: release v7.2 (codes on the protocol)

- ◐ Full check of v7.2 running; when it passes: report committed, v7.2 pushed to main.

## 2. Clean-up and restructure (Plan_Restructure, section 10; starts as soon as 1 is done)

- ☐ **Move**: `excel_ai` -> `excel_ai` (mitigation in `excel_ai/mitigation/`, legacy CPAT in `excel_ai/legacy/`, plans in `excel_ai/plans/`, shared code in `excel_ai/shared/`), `data` -> `data`, `coded` -> `coded`; `documentation/` abolished (Excel documents to `excel_ai/`, the rest to `other/`: research, other decks, archive). Old copies (`Old/`, `excel_ai/old`, old images and variants) removed. Every path in scripts and notes updated; quick check, codes check, data tests and document builds rerun.
- ☐ **History reset**: one fresh commit of the cleaned tree, force-pushed to main and the branch (user: drop outright).
- ☐ **Rename to prototype, v8.0**: `CPAT-AI-Mitigation-Prototype`; every main file twice, `_latest` (top of `excel_ai/`) and `_v8.0` (`excel_ai/releases/`), with one version table (`releases.md` = the workbook's version log); scripts and notes with stable names, releases as git tags.
- ☐ **Documents, few and simple**: top of `excel_ai/`: the workbook, the one bug-fix Word document (register with every fix plan), the register spreadsheet, the deck, `BUGS.md`, `ISSUES.md`, README. In `excel_ai/mitigation/`: a short main documentation (about 20 pages) and a Methods volume (6 merged method notes, equations appendix). One NORMS, one TODO (this file), one README per folder, a short CHANGELOG. Dropped: separate fix-plan Word/PDF files, `LegacyBugFixes`, the duplicate replication lists, finished plans.
- ☐ **Scripts**: about 20 for build, checks and documents (one `make_documents.py` entry); one-off extractors and tools to `excel_ai/legacy/tools/`.

## 3. Modular CPAT (Plan_Modules, section 9; after 2)

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
- ☐ **Policy taxonomy with the FTT policies** (PolicyTaxonomy_Plan): user decisions first.

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
- AP and TCB models (Plan_AirPollution, Plan_TransportExternalities) beyond the data parts.

Dropped by the user: engineer road model follow-ups (I61), demand on real local-currency prices (I63).
