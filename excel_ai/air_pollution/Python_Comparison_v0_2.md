# Python Air Pollution Module Comparison (v0.2)

Status: read-only comparison of the external `cpat_python` implementation with the standalone Excel specification. The Python implementation is a secondary method/code reference, not the replication authority. CPAT 1.0pre_459 remains the legacy target. No files in the external Python repository were changed.

External source: `C:\Users\wb549707\OneDrive - WBG\Documents\GitHub\cpat_python\cpat_model\modules\air_pollution\`.

## 1. Inputs and boundary

`AirPollutionModule` accepts three input-source paths:

- Energy (`ec` / `times`): country, sector, fuel, scenario and annual energy data. It calculates emissions using GAINS or uploaded emission factors.
- Emissions: detailed emissions indexed by country, sector, fuel and pollutant, with annual columns.
- Concentrations (`conc`): precomputed PM2.5 concentrations by country and area.

The Excel v0.2 interface remains the user-approved `aps.<pollutant>.<AP sector>` aggregate emissions input, with baseline and policy values, rather than Python's detailed fuel/subsector emissions input. The comparison must therefore aggregate Python emissions to the matching AP sector and convert units before comparing concentrations. The legacy sheet uses `country.mit.em.<pollutant>.<sector>.<scenario>` in tonnes/year; the current Mitigation `aps` codes are in kt.

When energy is the source, Python groups residential road fuels (`bgs` to gasoline, `bdi` to diesel), calculates emissions from the selected EFs, then maps emissions to Air Pollution sectors. The EF modes in `Pollution.prepare_emission_factors` are `constant`, `variable`, and `average`; the factor source is either the built-in processed GAINS table or a user-supplied table with coefficients `m` and `b`.

## 2. Emissions and concentration methods

Python derives primary organic matter and other PM2.5 after mapping emissions to Air Pollution sectors:

- `POM = 1.3 * OC`.
- `OPM = max(PM2.5 - BC - POM, 0)`.

PM2.5 method selectors implemented in `Pollution` are:

- `fasst`: built-in country/pollutant coefficients.
- `fasst_adj`: FASST coefficients adjusted to source-apportionment shares.
- `intake_fractions`.
- `avg_iF_FASST_adj`: arithmetic mean of intake-fraction and adjusted-FASST results.
- `elastic_net`: FASST plus the annualized Elastic Net and OLS allocation.
- `machine_learning` variants, including the configured no-pixel and DACCIWA coefficient/data sets.

Ozone selectors are `fasst` and `machine_learning`.

For adjusted FASST, the code calculates each sector's modeled share in the first year, compares it with source apportionment, and applies `share / share_fasst`; a zero adjustment is changed to 1. This zero-share fallback must be checked against 459 before it is reused.

For total PM2.5, Python calculates `C0 = max(WHO observed mean - modeled first-year concentration, 0)` by area and adds it to each year. For ozone, it floors the observed baseline at the O3 TMREL, then uses `C0 = max(observed - modeled first year, 0)`. These nonnegative floors differ from the literal documentation equation `C0 = observed - modeled`; reconcile against 459 and classify before adoption.

## 3. Health burden

The Python health selector is `gbd` or `burnett`.

For GBD, the code expands a relative-risk grid by country, area, disease, and age; combines OAP and HAP relative risks using the household exposure share; and computes `PAF = (RR - 1) / RR`. Attributable deaths, YLL, and YLD multiply the corresponding incidence rate by population, exposure allocation, and `10^-5`. O3 is applied to COPD only and omits age groups under 25. Confirm exact age, sex, disease, and urban/rural mappings against the 459 sheet; this code is not evidence that the 459 age-denominator issue is resolved.

For Burnett, the code aggregates NCD and LRI baseline outcomes, uses country/area/age-specific linear risk coefficients, and applies `PAF = 1 - 1 / (slope * concentration + intercept)`.

## 4. Economic outputs

`CostOfAirPollution` currently calculates:

- mortality value from deaths, VSL and a cessation-lag discount factor;
- working days lost and their wage value;
- YLD value using average disability weights and daily earnings;
- air-pollution health expenditure;
- these values as shares of baseline GDP and a morbidity-to-mortality ratio.

The constructor sets `productivity_gains = None`. The inspected class does not calculate the legacy per-fuel unit damage/externality table. These Python outputs and omissions must be matched to the 459 scope; do not infer that an output is out of scope just because this implementation lacks it.

## 5. Registered data bundle

The external `DataModule('Air_Pollution_Data', selected_countries)` loads these registered datasets:

`Air_Data`, `ambient_pm25`, `Apte`, `Coefs_ML`, `Coefs_ML_DACCIWA`, `Coefs_ML_no_pixel`, `Data_ML`, `Data_ML_DACCIWA`, `Data_ML_no_pixel`, `ef_local_pollutants_processed`, `ElasticNet_Beta`, `ElasticNet_Coefs`, `ElasticNet_Delta`, `ElasticNet_sector_mapping`, `FASST_Ozone`, `FASST_PM`, `food_share`, `hap_levels`, `hap_prop`, `incidence_rates`, `iF_PP`, `IHME`, `ILO`, `nh3_emissions`, `OLS_Coefs`, `Ozone_conc`, `Ozone_Coefs_ML`, `Ozone_Data_ML`, `source_apportionment`, `list of economies`, `WEO`, `population`, `urb_rur_pop_share`, and `WHO_PM25`.

These names are an inventory only. Before copying data into the workbook or `data/`, verify source, vintage, license/proprietary status, keys, units, country coverage, and correspondence with the nine 459 Air Pollution data tabs.

## 6. Reconciliation checklist

| Topic | Compare in 1.0pre_459 and coded module | Do not assume |
|---|---|---|
| Input mapping | `aps` aggregate vs detailed country/sector/fuel/pollutant inputs; emissions units and scenario years | Same aggregation or unit scale |
| Emissions | EF vintage, interpolation, sector mapping, POM/OPM, fuel fallbacks | Python EF modes equal 459's selectors |
| PM2.5 | Method selectors, coefficients, source-share mapping, zero-share fallback | Python selector names or formulas equal legacy names/formulas |
| Baseline calibration | OAP area-specific and O3 `C0` calculations, floors, missing-observation fallback | `C0` is always nonnegative or uses one method for both pollutants |
| Health | GBD/Burnett selector, age/disease population denominators, HAP allocation, O3 scope | Python and 459 use identical incidence tables or risk curves |
| Costs | VSL currency/year path, discount and lag, WDL, YLD, health spending | Python cost outputs include legacy GDP-loss or per-fuel damages |
| Horizon | Input/output year columns and extensions | Python's GDP simulation horizon equals the Air Pollution output horizon |

The next comparison should use Senegal for the legacy workbook's direct NoPropData case. Per the user's choice, the initial numerical regression country is Senegal; compare the Python implementation on the same inputs after mapping its detailed outputs to the workbook's aggregate codes.
