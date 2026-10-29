# TODO - Excel-AI, open work (one list, in order)

Status key: ☐ not started · ◐ in progress · ⏸ waiting. Done work is logged in [`../../CAVEATS.md`](../../CAVEATS.md). Plans with details: one file per plan in this folder. Python work: [`../../coded/TODO.md`](../../coded/TODO.md).

## 1. Release v0.7.2 and the clean-up: done (2026-10-22)

- ☑ v0.7.2 full check PASS, on main; restructure (`excel_ai/`, `data/`, `coded/`, `other/`); history reset; v0.8.0 prototype naming, stable script names, `_latest` and `_v0.8.0` copies; one NORMS; plans split; short documentation and Methods volume.

## 2. Clean-up, left over

- ☑ v0.8.0 full check PASS; old method notes replaced by `docs/methods/`; v0.8.0 on main.
- ☐ Old session branches on GitHub (7, old history): the user deletes them (or allows the AI to).
- ☑ The register spreadsheet built straight from the register (v0.8.3; was parsed from `BUGS.md`, `ISSUES.md`, `LegacyBugFixes.md`).

## 3. Modular CPAT ([`Modules.md`](Modules.md); after 2)

- ☑ **M1 money units** (v0.8.1): one vocabulary (`USD`, `USD m`, `USD bn`, `LCU`, `USD/GJ`, ... real/nominal; never `$`); labels only.
- ☑ **M2 prototype exports** (v0.8.1; 19b/19c come with M4): Mitigation section 15 (air pollution) moved to the end; new section 19 "Exports to modules" (19a Distribution, 19b AP right after section 15, 19c TCB; one defined name each, plain copies, codes as keys, a scale column); a `FromMitigation` tab first for Distribution, which reads only it (no hard-coded `Billion`/`Thousand` scaling).
- ☑ **M3 standalone Distribution v0.1.0**: `excel_ai/distribution/` (cut from the built prototype; Cover with the link to `CPAT-AI-Mitigation-Prototype_latest.xlsm`, button Update from Mitigation; check PASS: equal to the prototype cell for cell, and end to end). Left: a data-workbook link for its data tabs (Update data tables), and Excel 365 test of the macro.
- ☐ **M4 AP and TCB v0.1**: export blocks and small workbooks with the data import and export only (no model).
- ◐ **M5 documents** for the modules: module rules in `NORMS.md` section 9 and the prompts and Word guides in [`prompts/`](prompts/README.md) (2026-10-29). Left: run the prompts (TCB v0.1.0, AP v0.1.0, Distribution v0.1.4); register the TCB `Engineer` mode as an upgrade (U) linked to I100; then Mitigation reads `OutTCB` and `OutAP` instead of the typed values of FromTransportCB and FromAirPollution.
- ◐ **M6 `permalink_countryeditable/`** (user 2026-10-29; NORMS 5a): done 2026-10-29: the folder, a copy of `permalink/`; both hold mitigation, distribution and the air-pollution standalone (`_latest`); `shared/release.py` publishes to both (mitigation and distribution builders). Left: transport co-benefits when it exists; the air-pollution builder to publish through `release.py`; the modules read mitigation's export block from `permalink_countryeditable/` by Power Query (Distribution: replaces the Update from Mitigation file search); document it in the module READMEs.
- ☑ **Quick start counts** (done for v0.9.0, 2026-10-29; repeat at each release): after the v0.9.0 release regenerates `BUGS.md` and `ISSUES.md`, update `HumanReadme-QuickStart.docx` (section 5 counts and major open issues, version mentions v0.8.5) to match; keep doing so at each release (hand-written, no version table).

Air Pollution recovery (2026-10-27): the v0.3 input/data scaffold is restored under [`../air_pollution/`](../air_pollution/README.md), with public extracts under `data/air_pollution/legacy_459/`. This does not complete M4/M5 or the model work below.

- [x] Recover the missing Paulina Air Pollution files without replacing current shared documents or workbook releases.
- [ ] Reconcile the recovered legacy-459/v0.7.1 handoff with the current prototype and legacy 465; verify codes, years and kt-to-tonnes conversion, implement calculations and outputs, then run Senegal numerical regression.

## 4. Codes leftovers (after 3)

- ☐ Crosswalk rows marked review (89): `rnew`, `rsub`, `rmf`, `rtx`, `rnet`, `rvt`, `rbe`, `gdp.*`, `scc`, `ch4.em`, `co2.sec`, `apf.all.all`, other price rows; applied only with evidence.
- ☐ C6 vocabularies (prototype members `vkt`, `own`, `pit`... into the sheets); the legacy MTOutputs code as a second alias; `coded` `ele` -> `ecy` with the shared data (with the Coded CPAT owner).
- ☑ NOx forcing -6.25 against legacy -5.54 Mt CO2e (Egypt 2022): explained (v0.8.3 check), the same GWP factor (-7.058 per Mt NOx) on 12.9% more NOx (885.9 against 785.0 kt) from the fixed legacy bugs L22, L23, L58, L59; nothing to register.

## 4a. Remaining functionality and alignment ([`Remaining_functionality.md`](Remaining_functionality.md); decisions open)

- ☐ **A. Measure** the gap: legacy 465 with every cell plan applied against the prototype (U2).
- ☑ **C. Mitigation functions R1-R13** (all agreed 2026-10-29; **built in v0.9.0: R1-R3, R6-R11, R13** and the reverts LD1, LD10, I47, LD16, LD80, LD41, LD58; record in `CAVEATS.md` 2026-10-29; `remaining_functionality.json`): AP and TCB inputs section, social costs and welfare, Pigouvian taxes, CBAM process emissions, green public investment, producer-subsidy price effect, Manual inputs, small items, current account and GVA (typed Egypt values), LD16/LD41/LD58; section 15 as the output block to the air pollution module and section 5b to the transport co-benefits module (no copies; headings say so; 19c dropped); I100 (TCB on engineer vehicle-km, replicated); equations in `../mitigation/Equations_addendum.md` (written 2026-10-29; notes and new codes L173-L222, I101-I146, LD80 in `Equations_addendum_notes.md`); open points in `remaining_functionality.json`.
- ☐ **R4, R5, R12 deferred** (user 2026-10-29: the legacy WIP is not linked up): CBAM process emissions, green public investment, emissions intensity of industrial output; designs in the commit message on branch `wip-r4-r5-r12`; their bugs (L197-L213, L216-L219) and issues (I123-I128, I131-I134) stay "not built: deferred"; LegacyDiff 90.
- ☐ **v0.9.0 follow-ups (check_full)**: recomputations not yet written: the 17b/18 rows (cheap first: R1.10, R2.11, R3.17), the Python `ntx` and `ccp` with the [scenario > 1] factor and the Pigouvian netting, the exempt split (lkx) and the R10 rows, the E2 power cost memos; electricity subsidies only through `power_model_ref`'s txo inputs.
- ☐ **v0.9.0 follow-ups (model)**: (1) I147: section-15 food & forestry emissions far above the legacy AP input (drives wel.air); (2) possible double count of the electricity producer subsidy (its phase-out enters both `rgap` and `rpsu`; Egypt 0); (3) the methane-fee deadweight cost (`mfc`) without the intensity index; (4) last historical price year 2022 against legacy 465's 2024 (issue I89, kept by earlier user decision; recheck only if the user asks); (5) the stored scenario-1 rows of BaselineCO2 (Pigouvian transport and residential coal) are filled only by the full build (quick build: 0).
- ☐ **v0.9.0 power (POW465), deferred by the user**: the detailed power checks of `check_full` and the cell-by-cell check of the register mapping (`Power_465.md` section 2) against `issues_register.py` / `legacy/bugfixes/check465/legacy465_check.json`.
- ☐ **D. Modules**: air pollution, transport co-benefits, social costs and benefits (user decision: in or standalone).
- ☐ **E. MTOutputs** like legacy, without the price build-up intermediates.
- Not built by decision: the elasticity-based power model.

## 4b. Consolidation v0.8.4-v0.8.5 (2026-10-28/29): left over

- ☐ **Data problems** (issues of area Data, `Legacy_CPAT_Bugs` section 3): I98 (Extremely high) GAINS factor paths or confirmation of the base and final factors, the 2040-2041 extrapolation and the EFSel average with the CPAT team; I97 (Very high) the data team says which blank VAT cells are true zeros, and the CPAT team applies the cell plan of L170; I99 the corrected Egypt prices to the CPAT data team.
- ☐ **Confirm L135, L136** (found by the cell plans, were N1, N2) with the CPAT team.
- ☐ **LD41 to classify** (data vintage: energy use via the kernel, IIASA EFs without inventory adjustment): an issue replicated, a departure by decision, or a bug.
- ☐ **Quick check: recalculation of the old release** (v0.8.5): the LibreOffice recalculation of v0.8.4 (cache `.quickcheck/`) returned blanks for about 100 average-price codes (`pav`) that the stored values of both releases hold equally, so the quick check reported 546 changes where the stored values differ in 339 (emissions, GHG, NDC, climate welfare only). Find why and fix the check.
- ☐ **Air pollution and transport co-benefits**: their bugs and issues go in the same register (NORMS 0) when their models are built.
- ☐ **Data extracts on 465**: the input rows are on 465 (v0.8.4); the data extracts and Methods row numbers still read 456 (item in section 6).

## 5. With the user

- ☐ **Excel 365 review** on Windows (macros, no repair prompt, no circular warning, CheckBatchRun, LAMBDAs, dashboard).
- ☐ **ETS goal seek (I30)**: tested by the user.
- ☐ **Data requests**: I98 GAINS factor paths, I97 blank VAT cells, I90 proprietary tables for other countries, I95 historical GHGs 2018-2020.
- ☐ **Report the legacy bugs to the CPAT team**: send `../Legacy_CPAT_Bugs_v0.8.4.docx` and the tracker `../Tracking_Legacy_Bugs_v0.8.4.xlsx`, first Appendix A (fixed with caveats), the caveats on their 465 fixes: L115 wrong row, L95 rows still reading the cleared row 3719, L62 and L63 not fixed, L45, L16, L87, L84; high-priority legacy issues for them: I62, I71, I72-I74.
- ☐ **Policy taxonomy with the FTT policies** ([`Policy_taxonomy.md`](Policy_taxonomy.md)): user decisions first.

## 6. AI backlog

- ◐ **Full check (`check_full.py`)** (2026-10-29): repaired; `CHECK_PARTIAL=1` PASSES on 1.0.1 (CAVEATS). Still to do: recompute the rows listed as not recomputed (16 v0.9.0 power rows: cost memos `sys`, `pcbcap`, `pcbom`, `pcbfu`, `pcbchk`, the electricity subsidy chain; `ores` before the last price year; 6 R10 rows: other road biofuels, aviation and navigation renewables); run the full check without CHECK_PARTIAL (variant B, macro tests). With the repair, `coded/cpat_testing/compare/check_recomputations.py` can compare the mitigation recomputation too.
- ☑ (v0.9.2, Distribution 0.1.4: M15-M17, M19-M22 fixed, M18 withdrawn as not a bug; legacy checked, see CAVEATS 2026-10-29) **Prototype bugs M15-M22, found by Coded CPAT (user 2026-10-29; NORMS 0 rule 6):** fix all eight in the builder (Mitigation and Distribution), then check each in legacy CPAT (registered? fixed in 465?); brief and steps: [`Fix_prototype_bugs_M15-M22.md`](Fix_prototype_bugs_M15-M22.md). M15 VAT rate of the year (data to LastHistPriceYear, then held; user assumption), M16 freight BEV feebate distance, M17 PHEV cost basis (confirm), M18 bus electricity column, M19 gdpn units, M20 World Bank gas series by name, M21 methane fee b = 0, M22 Distribution percentile recycling rows.
- ☑ **New legacy file**: the register, fix plans and lists moved to the latest file, 465 (v0.8.2, 2026-10-23; 459 superseded); the CPAT team's 62 fixes checked (52 confirmed, 8 with caveats, L62 and L63 not fixed; `../legacy/bugfixes/check465/`).
- ☐ **Numerical check on legacy 465** (U2, I14): the legacy Egypt run against the prototype, sector by sector; align with `CPATMasterProcessesCodesAndDefaults.xlsx`. (The caveats for the CPAT team: section 5.)
- ☐ **Prototype data extracts on 465**: the extracts (`extract_*.py`) and the Methods still read 456; move them when the numerical check (U2) is done.
- ☐ **Data links, rest**: GHGs, EF_GHG, CH4Inputs, Elasticities, Prices_int, OilProductShares (converters to the prototype layout), Transport1-2 (no dummy data yet).
- ☑ **Excel lint in every writer** (v0.8.3; NORMS 3g): `excel_lint.check()` after every save (prototype, distribution, register spreadsheet, tracker, data workbooks, legacy-data export, `other/distribution`).
- ☐ **No Excel COM needed (checked 2026-10-28)**: the mitigation, distribution and air-pollution builders all write with openpyxl and recalculate in LibreOffice; COM appears only in the optional Excel-open test of `check_quick.py` (skipped on Linux). `AGENTS.md` and the hard rules still say builders run via COM: correct them. Distribution unchanged since v0.1.0 (2026-10-22; last touched by v0.8.3, 2026-10-23); the Excel 365 test of its macro (section 3, M3) stays with the user.
- ☐ **Copy-paste stress test**: add a fuel, a subsector and a scenario by dragging; fix what breaks.
- ☑ **Tracker leads** (v0.8.3): Manual inputs J178:J179 are read (Mitigation L753:L754, chosen in K when the price-control option is manual): no bug. MTInputs 182-183 units: legacy bug L134 (labels), fixed in the prototype.

- ☐ **`ModelForm` scenario input (user 2026-10-29, Coded CPAT design D4)**: add a `ModelForm` row at the end of the `ScenarioDefinition` additions (below the legacy rows, NORMS 4), default `CPAT`, read by the LAMBDAs of the demand equations (`FUELUSE`, `DEMANDMULT`); the same row in Coded CPAT's scenario sets. The engineer-or-elasticity selectors of power and road transport are unchanged. Values unchanged (quick check 0 change). Coordinated with `../../coded/TODO.md` task 2.8.
- ☑ **Version numbering rebased** (done on main 2026-10-29: 9.0 to 0.9.0, distribution 1.3 to 0.1.3); Coded CPAT versions are `<Excel-AI version>p<Python version>` (Coded CPAT design D14).

## Later (not now)

- Power engineer model: final deficit to gas, MaximumGasCF, storage factor; planned retirement data; elasticity-based power model.
- Regulations as shadow prices; green public investment; ETS benchmarks by sector; inventory-adjusted EFs and process CO2; legacy block F reports (social costs, Kaya, CBAM, policy coverage).
- Data for more countries; Python port (`../coded/TODO.md`).
- AP and TCB models ([`Air_pollution.md`](Air_pollution.md), [`Transport_cobenefits.md`](Transport_cobenefits.md)) beyond the data parts.

Dropped by the user: engineer road model follow-ups (I61), demand on real local-currency prices (I63).
