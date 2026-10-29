# TODO - Coded CPAT (Python), open work only

Status key: ☐ not started · ◐ in progress · ☑ done (ticked items leave at the next update; their record is [`../CAVEATS.md`](../CAVEATS.md)). Excel work: [`../excel_ai/plans/TODO.md`](../excel_ai/plans/TODO.md). Rules: [`NORMS.md`](NORMS.md).

**The project (user 2026-10-29): the full build of Coded CPAT**, a human-readable Python model that replicates the mitigation and distribution modules of Excel-AI number for number. Specification, design choices and the plan in words: [`cpat_documentation/project/Spec.qmd`](cpat_documentation/project/Spec.qmd) (Word copy `Spec.docx`). The phases below are the plan's checklist; section numbers refer to the spec.

## Phase 0 - Planning documents (the steps requested first)

- ☑ Folder and code structure for readability: spec sections 3-4; `NORMS.md`; six box diagrams (spec section 4, mermaid, rendered to `project/figures/` for Word). Draft for the user's review.
- ☑ Spec: the request cleaned up (section 1), principles, structure, data, inputs, equation forms, tests, documents, design choices, plan, Excel-AI choices to flag and methodology errata (sections 2-12), as qmd with a Word copy (`cpat_documentation/make_docs.py`). Draft for the user's review.
- ◐ Equation list, first draft: executive summary of the core equations (M1 policies to M8 GDP, D distribution: 36 equations; 3 adjustments started) in the notation of the methodology, Greek and code-name versions generated from one source (`cpat_documentation/equations/equations.yaml`, D13). Next: (1) complete appendices A (mitigation adjustments) and B (distribution) from `../excel_ai/mitigation/Equations.md`, `Equations_addendum.md`, `Formulas.md` and the Methods chapters, block by block (can run alongside phase 2; each block's equations before its code); (2) confirm the code names marked † in the codes map (or propose codes for them).
- ☑ Design choices written up with options and recommendations (spec section 10): D1-D16.

## Phase 1 - Design choices with the user: done

- ☑ D1-D16 decided by the user (2026-10-29): spec section 10; `NORMS.md` rules made final.
- ☑ Detailed plan: spec section 11 (the tasks below, each with its check).
- ☐ Correct `../HumanReadme-QuickStart.docx` when it is next regenerated: every table in `data/dummy/` is dummy, not only the four proprietary tables (user 2026-10-29).
- ☐ Send the documentation bugs DOC1-DOC20 (`../excel_ai/BUGS.md` section 3) to the CPAT team with the next tracker release.

## Phase 2 - Foundations (spec 11, phase 2)

- ☑ 2.1 Data interface for the data person: `../data/INTERFACE.md` and `../data/interface_manifest.csv` (41 files in three groups; legacy layout as Excel-AI; `full` and `dummy`; input files in `../data/inputs/`; 8 open points). The check (loaders read only what the manifest lists) comes with the loaders (2.6).
- ☑ Tidy CSV as the input of Coded CPAT, with two-way converters legacy layout <-> tidy (`../data/scripts/tidy/`, `../data/tidy/`; user 2026-10-29). Domestic prices cut to Egypt (user 2026-10-29).
- ☐ Data, from 2.1: assemble the `dummy` database (public files plus dummy Balances, EnergyCons, Prices_dom in the 99-column layout, HHSurvey, IO_GTAP); bring ASPIRE and WHOCooking back whole; extract the FromAirPollution and FromTransportCB values from `build.py` to a data file (2.10).
- ☑ 2.2 Package skeleton (`cpat_model/` folders, `run()`, `settings.py`), versions `EXCEL_AI_VERSION` and `__version__` = `<Excel-AI>p<Python>` (D14; Excel-AI numbering rebased 2026-10-29: 0.9.0, distribution 0.1.3).
- ☑ 2.3 Index sets (`core/dims.py`) from the codes map. Check: equal to the codes map.
- ☑ 2.4 Variable registry (`core/variables.py`, `core/variables.csv`: 7,541 coded rows, 1,255 stems with description and unit, from Excel-AI's Mitigation sheet). Of the 33 names marked † in the equation list, 4 are stems (cons, pop, reg, trown); the rest are parameters or data and are settled block by block in phase 3.
- ☑ 2.5 Loop (`core/loop.py`): baseline first, then each scenario (D15); prepare, year loop, finish; `mitigation/chain.py`; policy paths and price indices (`core/paths.py`).
- ☑ 2.6 Data layer (`data/`): reads the tidy tables of `../data/tidy/` (`DATA_ENVIRONMENT` = `full` or `dummy`, path of the private tidy folder); loaders to labelled arrays; exact float parsing; cache. The old Python-format data (`../data/dummy/`, `convert_data_workbook.py`, `export_to_legacy.py`) serve the old code only and retire with it (6.3).
- ☑ 2.7 Inputs (`inputs/`): scenario-set table (MTInputs rows + Excel-AI additions + `ModelForm`), advanced-inputs workbook, validation, global-settings check (D16). Check: Excel-AI `ScenarioDefinition` J, K read back unchanged.
- ☑ 2.8 Forms (`forms/`): registry, slots, the `CPAT` form (its equations come with phase 3); `ModelForm` in the Python scenario set. ☐ The `ModelForm` row in Excel-AI's `ScenarioDefinition`: at its next release (user 2026-10-29).
- ☑ 2.9 Results (`results/`) by output code; export in the Excel layout.
- ☑ 2.10 Placeholder modules `air_pollution/`, `transport_cobenefits/`: `prepare` (FromAirPollution, FromTransportCB values) and empty `step(t)` (D10).
- ☑ 2.11 Comparison harness (`cpat_testing/compare/`): reference values by code from the stored values of Excel-AI 0.9.1 (user 2026-10-29): `compare.py`, `reference/excel_ai_0.9.1.csv`.
- ☑ 2.12 Equation-id test (every id has a function and every cited id exists).

## Phase 3 - Mitigation, block by block (each: equation list appendix, functions, unit tests, comparison for Egypt, register differences)

Decided 2026-10-29 (user): a block that still differs after a reasonable effort is logged (codes, years, suspected cause; `CAVEATS.md`), marked ◐, and the next block follows. Stored scenario-1 values of Excel-AI (ETS baseline CO2 `bco2`, methane activity `ch4bs`, goal-seek ETS prices `ets.ovr`) are read as data for now; once emissions are built, a check that the baseline run reproduces them. Phase 4: reference = stored values of Excel-AI Distribution 0.1.3, open items fixed as that workbook does. Phase 5 for now: 5.4 speed only (5.1-5.3 need heavy recalculations: later).

- ☑ 3.1 Header (0; macro series, matches Excel-AI) · ◐ 3.2 Policies (1; matches Excel-AI; Pigouvian taxes and producer subsidies with 3.3 and 3.10) · ☑ 3.3 Prices (2; build-up and the averages over fuel use match Excel-AI) · ☑ 3.4 Power costs incl. levelised costs (3; data steps and the 722 quantity-free rows match Excel-AI) · ☑ 3.5 GDP level (16; matches Excel-AI) · ☐ 3.6 Road engineer model (5b; three tasks) · ◐ 3.7 Fuel demand (5-8) and leakage, exempt use (6b; fuel | subsector table, price rows and the year step incl. biofuels and leakage match Excel-AI, scenarios 1-2) · ☑ 3.8 Power quantities and prices (3; matches Excel-AI, scenarios 1-2) · ◐ 3.9 Totals and revenues (11, 12; match Excel-AI, scenarios 1-2; section 2 averages to do) · ◐ 3.10 CO2 and ETS check, other GHGs, local pollutants (13-15; 13-14 match Excel-AI, scenarios 1-2; 15 to do) · ◐ 3.11 Module steps and GDP effects (16; GDP effects and external balance match Excel-AI, scenarios 1-2; module steps with 3.12) · ☐ 3.12 Indicators, welfare, exports (17, 17b, 18, 19a).

## Phase 4 - Distribution

- ☐ 4.1 The distribution package on the new inputs, data and results, reading the 19a results (its 48 tests unchanged).
- ☐ 4.2 The open distribution items below (revenue units, national totals, projected electricity price). Check: `distribution_ref.py`, then Excel-AI Distribution.

## Phase 5 - Systematic comparisons

- ☐ 5.1 Excel-AI values by code from the recalculated release workbook; Python against them, Egypt.
- ☐ 5.2 Every country (`full` where available, else `dummy`).
- ☐ 5.3 Against legacy CPAT: Egypt, then every country, through LegacyDiff.
- ☐ 5.4 Speed: under 1 second for one country and two scenarios (D11); cache data and the baseline run.

## Phase 6 - Running the model

- ☐ 6.1 `run_model.py` for scenario-set files (many countries, many scenarios).
- ☐ 6.2 Shiny on `cpat_model.run`; rerun only changed scenarios.
- ☐ 6.3 Retire the replaced code (old `mitigation/` subpackages, `dashboard_inputs.py`, `distribution_inputs.py`, `data_read/`, `indicators/`).
- ☐ 6.4 Website: the Coded CPAT tab of the Quarto site at `../docs/` (D12).
- ☐ 6.5 First release `<Excel-AI version>p0.1`.

## Later (not now)

- ☐ Demand forms through `ModelForm`: `CPAT partial adjustment`, `CES partial adjustment` (CES-compatible service prices), `CDPM-FTT` (SISEPUEDE-like and FTT-like); each added to Excel-AI and Python together.
- ☐ Air-pollution and transport co-benefits modules (transport co-benefits linked to the road engineer model).

## Existing open items (before the project; to be absorbed by the phases above)

Status (user 2026-10-20): the Python part was about 40% complete. Most items below are resolved by the rebuild (phases 2-4) rather than fixed in the old code; each is closed with a note when its phase is done.

- ☐ **Distribution: carbon-pricing revenue units.** `derive_cp_revenue_from_scenarios` multiplies the carbon price (USD/t) by emissions (Mt), i.e. USD million, while the recycling steps treat it as local currency against household consumption in LCU; convert (exchange rate, millions) and validate against the Excel `MTOutputs` revenue. Until then recycling effects from a model run are far too small (the tests use the Excel revenue, so they are not affected).
- ☐ **Distribution: national totals.** `run_distribution` passes `national_totals=None` (the survey's own population and consumption); wire population and household consumption (GDP x `distn_gdp_ratios`) once GDP exposes a real consumption series.
- ☐ **Distribution: projected electricity price.** It now uses the power model's simplified price (last historical price + carbon price x emission intensity, `power.demand.rp_demand`); switch to the full electricity price build-up (legacy G1, G2) when it is ported. `EnergyPrices.ele_prices['rp']` holds historical years only.
- ☐ **Distribution in the Shiny app and the indicators** (results tables by decile).
- ☐ **Data: other oil products** fall to the 0.01 price floor in the sample data (negative retail price in 2024), so their price change is 0; check the data.
- ☐ **Data loaders**: the target format is `.pkl.bz2` (developer guide); the policies, GHGs and CH4 loaders read CSV from `DATA_PATH` until the pickles exist there.
- ☐ Port the validated mitigation logic of the Excel prototype, CPAT-AI-Mitigation-Prototype (`../excel_ai/mitigation/`; methods in `docs/methods/`), keeping the codes identical; the prototype's Python recomputations (`check_full.py`, `power_model_ref.py`, `transport_model_ref.py`, `distribution_ref.py`) are a starting point.
- ☐ **Legacy export: missing price columns and Balances.** `../data/scripts/export_to_legacy.py` leaves 48 `Prices_dom` columns blank (source/reliability flags, `taxa`, `sub.or`, production, spot prices) and cannot write the IEA flow-level `Balances` sheet; add them to the real data (or a second source) if legacy runs need them. Confirm a paste into the full legacy workbook in Excel.
- ☐ **Data workbook, CPAT format: the multi-table legacy tabs.** `../data/scripts/convert_data_workbook.py` writes 17 legacy data sheets; 21 tables are still carried in the Python layout (`py_` sheets) because their legacy tab holds several tables at fixed addresses: ECP (`existing_ct`, `existing_ets_nat`, `existing_ets_reg`, `do_ct_ets_exist`), Power (`mpp`, `lcoe_tmp`), Prices_int (`prices_int`), Elasticities (`elasticities`), Mapping (the five `distn_mapping_*`), the GHG shocks block of GHGs (`ghg_adjustments`) and tables with no legacy sheet (`co2_efs_global`, `co_benefits_ffs`, `fuel_carbon_price_inclusion`, `sectors_carbon_price_inclusion`, `global_fuel_demand`, `ic`, `int_prices_reg_assumptions`). Map each to its legacy block (`../data/mvp_legacy_extracts/legacy_<Tab>_cells.csv` give the addresses). Also confirm the four WEO code renames (BCA_BP6, BCA_GDP_BP6, ENDA, PCPI_PCH) with the team.
- ☐ **Data loaders: CSV float precision.** pandas' default float parser can be up to about 1e-12 off the CSV text (e.g. `0.0001198124434142994` reads as `0.0001198124434142`); `export_to_legacy.py` now reads with `float_precision='round_trip'`; the model's loaders still use the default.
- ☐ **Input keys: the rest of the names.** v0.8.4 renamed the input keys to the ScenarioDefinition names (`NameOfParameter`, codes map tab Inputs). Still to do: split the keys that stand for a policy input and its baseline twin (`energy_sector_reform`: ProdSubPh / ProdSubPhaBaseline, FFSProdPhaseoutPeriod / FFSProdPhaseoutPeriodBA, ShareofProdSubPha / ShareOfProdSubPhaBA, ConsSubPha / ConsSubPhaBaseline, FFPhaseOut / FFSConsPhaseoutPeriodBA, ShareOfConsSubPha / ShareofConsSubPhaBA; CTaxTrajectoryType / ExtendCarbonPriceBeyondOutro), flatten the groups `adj_eff_margins_shadow_pricing` (SPPEffAdj*) and `additional_eff_gains` (AdditionalEfficiency*), use legacy option values (ScenarioSelected ' - Carbon tax', AddEfficientTaxes, PublicInfrastructureInvType), and read the inputs from a ScenarioDefinition sheet. Python-only inputs without a legacy row: behavioral_response_adj_factor, exempt_cooking_fuel_code, exempt_cooking_fuel_share, labor_tax_cut_coefficient.
- ◐ **Port the remaining functionality of v0.9.0** (Excel built R1-R3, R6-R11, R13 and the reverts LD1, LD10, I47, LD16, LD80 on 2026-10-29; R4, R5, R12 deferred by the user, branch `wip-r4-r5-r12`): port the new rows from `../excel_ai/mitigation/Equations_addendum.md` (A reverts and R13, B R1-R2, C R3, D R11, E R6-R10, F output blocks), next to `Equations.md`, keeping the codes of the prototype (`<variable>.<sector>.<fuel>`; deviations from the addendum codes in `../CAVEATS.md` 2026-10-29). Data: `../data/range_anxiety_fit/` (range-anxiety start values fitted on the prototype). Not to port yet: R4, R5, R12.
