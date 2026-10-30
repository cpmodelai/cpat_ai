# CPAT-AI Air Pollution Module

Standalone Excel rebuild of the Air Pollution module in CPAT 1.0pre_459. The workbook reproduces the legacy module's supported methods and outputs, while making its calculation steps inspectable and its Mitigation handoff explicit.

## Boundary

The workbook starts from pollutant emissions produced by Mitigation. It does not recalculate fuel use or emissions. The input section accepts the baseline and policy scenario series keyed by the existing codes `aps.<pollutant>.<sector>`, with year, country, unit, scenario, and source/version traceability. The current Mitigation method defines these series in kt. The workbook must verify the 1.0pre_459 unit convention and convert at the boundary where required; it must not silently assume that legacy formulas and current Mitigation use identical units.

After the input block is populated, the workbook must run without links to another CPAT workbook. Reference tables required by its calculations belong in the workbook and their source data belong under the repository's canonical `data/` tree. No proprietary data are to be added to the repository.

## Scope

- Reproduce the Air Pollution calculations and options supported by CPAT 1.0pre_459, including emissions-to-concentration methods, exposure and health burden, and economic outputs.
- Calculate baseline and policy levels and their differences, using the same scenario semantics as the reference.
- Report fuel externalities as outputs only. Do not feed them back into Mitigation prices in this version.
- Design for the supported country set and use Senegal as the first regression case, matching the NoPropData Dashboard selection.
- Keep all inputs, data, intermediate calculations, outputs, and checks labeled and traceable. Do not hide calculations behind external workbook links.

## Sources and reconciliation

- Method equations: [`../../coded/cpat_documentation/user/06_Air_pollution.html`](../../coded/cpat_documentation/user/06_Air_pollution.html).
- Working equation inventory: [`Equations_v1_0.md`](docs/Equations_v1_0.md); reconcile it with 1.0pre_459 and the coded implementation before finalizing formulas.
- Python comparison: [`Python_Comparison_v0_2.md`](docs/Python_Comparison_v0_2.md). The external implementation is a secondary cross-check, not the legacy authority.
- Upstream pollutant input codes and units: [`../mitigation/docs/methods/Emissions.md`](../mitigation/docs/methods/Emissions.md).
- Legacy target: legacy 1.0pre_459 (the workbook was removed 2026-10-30; the reference is now [`CPAT 1.0pre_465_Shell.xlsb`](../../data/legacy/CPAT%201.0pre_465_Shell.xlsb), read-only).
- Mitigation and Distribution workbook layout, visual, formula, data, versioning, and bug/issue rules: [`../core/NORMS.md`](../core/NORMS.md).

In 1.0pre_459, the Mitigation-to-Air-Pollution handoff is `country.mit.em.<pollutant>.<sector>.<scenario>` in tonnes per year (`.1` baseline, `.2` policy). The current Mitigation module uses country-neutral `aps.<pollutant>.<sector>` outputs in kt. The input sheet shows this code crosswalk, but conversion and calculation are not implemented until verified against the coded module and legacy formulas.

The NoPropData workbook's Dashboard selects Senegal, now also selected for the first regression. The overlapping Python implementation is at `C:\Users\wb549707\OneDrive - WBG\Documents\GitHub\cpat_python\cpat_model\modules\air_pollution`; use it to identify missing inputs and compare calculations, but resolve disagreements against 1.0pre_459. Legacy bugs are fixed and tracked; legacy issues are reproduced and tracked unless the user explicitly approves a departure.

## Validation

The first numerical comparison is Senegal against CPAT 1.0pre_459_NoPropData. Compare each selected output by scenario and year, and classify differences as a confirmed bug fix, a replicated issue, or unresolved. Do not claim numerical equivalence until the selected country has populated, reproducible reference values.

## Current Scaffold

- Latest workbook: [`CPAT-AI-Air-Pollution-Standalone-v0.3.xlsx`](releases/CPAT-AI-Air-Pollution-Standalone-v0.3.xlsx) (permalinked copy: [`../active_workbooks/`](../active_workbooks/)); v0.1 and v0.2 are in [`releases/`](releases/).
- Builder: [`build_workbook.py`](build_workbook.py).
- Python cross-check: [`Python_Comparison_v0_2.md`](docs/Python_Comparison_v0_2.md).
- Rebuild command: `python excel_ai/air_pollution/build_workbook.py`. The recovered v0.3 workbook is retained unchanged; use a new version/output path for a released rebuild.
- Extracted AP reference tables: the legacy 459 tables kept as they are in the data edition, `data/Public01/tidy/ap459_*.csv` ([`data/README.md`](../../data/README.md)); the builder reads the default edition.
- Recovery provenance and retained backup files: [`Recovery_2026_10_27.md`](docs/Recovery_2026_10_27.md).

Version 0.3 contains Cover, Data Sources, Mitigation Inputs, a DATA_AIR_POLL divider, and the nine extracted AP data tabs. Raw CSV rows are retained; ConcMat and Air_meta source row-2 headers move to row 3 under the workbook title band. Calculations, unit conversion, outputs, and numerical regression are still not implemented.
