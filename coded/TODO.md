# TODO - Coded CPAT (Python), open work only

Status key: ☐ not started · ◐ in progress · ☑ done (ticked items leave at the next update; their record is [`../CAVEATS.md`](../CAVEATS.md)). Excel work: [`../excel_ai/plans/TODO.md`](../excel_ai/plans/TODO.md). Rules: [`NORMS.md`](NORMS.md).

**The project (user 2026-10-29): the full build of Coded CPAT**, a human-readable Python model that replicates the mitigation and distribution modules of Excel-AI number for number. Specification, design choices and the plan in words: [`cpat_documentation/project/Spec.qmd`](cpat_documentation/project/Spec.qmd) (Word copy `Spec.docx`). The phases below are the plan's checklist; section numbers refer to the spec.

## Phase 0 - Planning documents (the steps requested first)

- ☑ Folder and code structure for readability: spec sections 3-4; `NORMS.md`; six box diagrams (spec section 4, mermaid, rendered to `project/figures/` for Word). Draft for the user's review.
- ☑ Spec: the request cleaned up (section 1), principles, structure, data, inputs, equation forms, tests, documents, design choices, plan, Excel-AI choices to flag and methodology errata (sections 2-12), as qmd with a Word copy (`cpat_documentation/make_docs.py`). Draft for the user's review.
- ◐ Equation list, first draft: executive summary of the core equations (M1 policies to M8 GDP, D distribution: 36 equations; 3 adjustments started) in the notation of the methodology, Greek and code-name versions generated from one source (`cpat_documentation/equations/equations.yaml`, D13). Next: (1) complete appendices A (mitigation adjustments) and B (distribution) from `../excel_ai/mitigation/Equations.md`, `Equations_addendum.md`, `Formulas.md` and the Methods chapters, block by block (can run alongside phase 2; each block's equations before its code); (2) confirm the code names marked † in the codes map (or propose codes for them).
- ☑ Design choices written up with options and recommendations (spec section 10): D1-D16.

## Phase 1 - Design choices with the user

- ☐ Go through D1-D16 with the user, one question at a time ("ask me the design questions"); record each answer in spec section 10 (status, date) and `../CAVEATS.md`; turn the provisional rules of `NORMS.md` into rules.
- ☐ Then write the detailed plan (phase 2 onwards broken into tasks of a day or less, with their checks) in spec section 11 and here.

## Phase 2 - Foundations (after phase 1)

- ☐ `cpat_model/core/`: index sets (`dims.py`), variable registry generated from `../excel_ai/CPAT-AI_CodesMap_v<version>.xlsx` (`variables.py`), policy paths, units and constants, the three-stage loop (`loop.py`).
- ☐ `cpat_model/data/`: databases `public`, `full`, `dummy` (D6); manifest; loaders to labelled arrays; the four proprietary tables kept apart.
- ☐ `cpat_model/inputs/`: scenario set (MTInputs rows x scenarios, `NameOfParameter` keys, D5) read from a file or built by the app; advanced inputs (time series, `Manual inputs`, `Settings`); validation.
- ☐ `cpat_model/forms/`: the registry and the `standard_cpat` slots (D4).
- ☐ `cpat_model/results/`: results by Excel-AI output code; export in the Excel layout.
- ☐ Placeholder modules `air_pollution/` and `transport_cobenefits/` with their declared inputs and outputs (D10).
- ☐ `cpat_testing/compare/`: Excel-AI values by code from the recalculated release workbook (D8); comparison report by code and block.

## Phase 3 - Mitigation, block by block in Excel-AI order (each: equations, unit tests, Excel-AI comparison for Egypt)

- ☐ 1 Policies · ☐ 2 Prices · ☐ 3 Power · ☐ 5 Transport (elasticity and road engineer model) · ☐ 6 Buildings and residential leakage · ☐ 7-8 Industry, other energy use · ☐ 11 Totals · ☐ 12 Revenues · ☐ 13-15 Emissions (CO2, other GHGs, local pollutants) · ☐ 16 GDP · ☐ 17 Carbon-pricing indicators · ☐ 18 Welfare and externalities · ☐ 19 Exports to modules.

## Phase 4 - Distribution on the new structure

- ☐ Move `cpat_model/distribution/` onto the new inputs, data and results (D7); its tests unchanged; compare with Excel-AI Distribution v1.3, end to end from mitigation.

## Phase 5 - Systematic comparisons

- ☐ Python against Excel-AI: every code, Egypt; then every country (D8).
- ☐ Python or Excel-AI against legacy CPAT: Egypt, then every country, on the systematic dataset (D6).

## Phase 6 - Running the model

- ☐ `run_model.py`: a scenario-set file in, results out (many countries, many scenarios).
- ☐ Shiny: the app builds the scenario set and calls `cpat_model.run` (one country, two or more scenarios; D11).
- ☐ Retire the replaced code (old `mitigation/` subpackages, `dashboard_inputs.py`, `distribution_inputs.py`, `data_read/`, `indicators/`) as each replacement passes.
- ☐ Website: the Python pages in the Quarto site (D12).

## Later (not now)

- ☐ Equation forms: `simple_cpat`, `cpat_partial_adjustment`, `ces_partial_adjustment` (CES-compatible service prices), `cdpm_ftt` (SISEPUEDE-like and FTT-like).
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
- ☐ **Input keys: the rest of the names.** v8.4 renamed the input keys to the ScenarioDefinition names (`NameOfParameter`, codes map tab Inputs). Still to do: split the keys that stand for a policy input and its baseline twin (`energy_sector_reform`: ProdSubPh / ProdSubPhaBaseline, FFSProdPhaseoutPeriod / FFSProdPhaseoutPeriodBA, ShareofProdSubPha / ShareOfProdSubPhaBA, ConsSubPha / ConsSubPhaBaseline, FFPhaseOut / FFSConsPhaseoutPeriodBA, ShareOfConsSubPha / ShareofConsSubPhaBA; CTaxTrajectoryType / ExtendCarbonPriceBeyondOutro), flatten the groups `adj_eff_margins_shadow_pricing` (SPPEffAdj*) and `additional_eff_gains` (AdditionalEfficiency*), use legacy option values (ScenarioSelected ' - Carbon tax', AddEfficientTaxes, PublicInfrastructureInvType), and read the inputs from a ScenarioDefinition sheet. Python-only inputs without a legacy row: behavioral_response_adj_factor, exempt_cooking_fuel_code, exempt_cooking_fuel_share, labor_tax_cut_coefficient.
- ◐ **Port the remaining functionality of v9.0** (Excel built R1-R3, R6-R11, R13 and the reverts LD1, LD10, I47, LD16, LD80 on 2026-10-29; R4, R5, R12 deferred by the user, branch `wip-r4-r5-r12`): port the new rows from `../excel_ai/mitigation/Equations_addendum.md` (A reverts and R13, B R1-R2, C R3, D R11, E R6-R10, F output blocks), next to `Equations.md`, keeping the codes of the prototype (`<variable>.<sector>.<fuel>`; deviations from the addendum codes in `../CAVEATS.md` 2026-10-29). Data: `../data/range_anxiety_fit/` (range-anxiety start values fitted on the prototype). Not to port yet: R4, R5, R12.
