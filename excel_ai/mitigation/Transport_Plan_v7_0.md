# Engineer road transport model: plan (CPAT-AI-Mitigation-MVP, for v3.5)

Sources: the methodology note (`Transportation_methodology.docx`, user, 2026-10-14) and a survey of legacy CPAT (`Transport_Legacy_Survey_v7_0.md`: Mitigation section 5 rows 4302-5378, key inputs 15 rows 2015-2171, sheets Transport1-3, Dashboard rows 61-98 and 540-558, Manual inputs rows 373-377).

## 1. What legacy does

- **Road only.** Rail, aviation, navigation, and coal, kerosene and other oil products in road stay on the elasticity model.
- **Vehicle classes and powertrains.**
  - Passenger and light vehicles, new and used: gasoline, diesel, LPG, CNG, PHEV, BEV.
  - Freight: diesel, LPG, LNG, BEV.
  - 2-3 wheelers: gasoline, BEV.
  - Buses: scaled with passenger vehicles; no stock model.
- **Chain, year by year:**
  - **Vehicle demand:** Gompertz ownership in GDP per capita, with partial adjustment and growth caps. Freight and 2-3 wheelers follow as income-dependent shares of passenger ownership.
  - **Stock:** retirement of 1/life of the trailing-average stock; purchases = demand − remaining stock, split new/used.
  - **Total cost of ownership (TCO) per km**, ICEV and BEV: purchase price with customs, VAT, ad-valorem tax, feebate and subsidy; depreciation and salvage; insurance and maintenance; fuel; distance tax; range anxiety for BEVs.
  - **EV choice:** logit `exp(−k · TCO/avgTCO)`, with k = 3, 2, 4 for passenger, freight, 2-3 wheelers.
  - **ICE fuel split:** own- and cross-price elasticities of TCO.
  - **New fuel economy:** price elasticity plus autonomous improvement. The stock average turns over with new purchases.
  - **Distance per vehicle:** elasticity to cost per km and to income.
  - **Fuel use** = vehicles × distance / fuel economy, in two calibration steps to the energy balance.
- **Links to the rest of the model.**
  - In: post-tax retail fuel prices (carbon tax, fuel reform and existing taxes pass through) and power prices, lagged one year.
  - Out: road fuel use by fuel and road electricity into power demand.
  - A switch `TrModel` (Engineer / Elasticity) picks the road fuel-use rows. **The legacy Egypt run uses Elasticity.** The engineer block is still calculated, so the cached xlsb holds a full engineer reference run for both scenarios.
- **Data.**
  - All-country, so the model can be generic:
    - Transport1: fuel shares, fuel economy, ownership, EV shares, distance, used share, duties, charging stations, saturation point; 221 countries, 2022-2025.
    - Transport2: vehicle prices, 2022-2040.
    - Transport3: range-anxiety calibration per country.
  - Global paths, hardcoded in legacy: BEV fuel economy and charging cost per port.
  - Parameters and policies sit on the Dashboard, not on ScenarioDefinition.
- **18 legacy bugs or oddities**, listed in the survey; candidate register entries L25 onward. Examples:
  - The baseline gets the distance tax and 2-3 wheeler EV subsidy (`$C2227>1`).
  - Freight income growth is zero from 2038 (wrong row).
  - The ownership calibration only scales up and uses 2024 as the last data year.
  - The bus block reads the wrong rows.
  - The PHEV share is negative.
  - Freight is discounted at the power-sector cost of capital.
  - About ten literals are hardcoded, among them the Gompertz −5.897 and gas /26.

The cached Egypt engineer baseline more than doubles road fuel use by 2035 (gasoline 16,286 against 9,079 ktoe from the elasticity model). It is driven by ownership growing at the 7.5% a year cap, toward a Gompertz level of 139 per 1,000 against 58 observed. The ownership bug drives this, and it matters for any default.

## 2. Plan

| Phase | Work | Output |
|---|---|---|
| 1 Data | Extract the inputs to `data/` keyed by country (all countries): Transport1 (`transport_data.csv`), Transport2 (`vehicle_prices.csv`), Transport3 (`range_anxiety.csv`); legacy Dashboard parameters, Manual inputs paths and hardcoded Mitigation paths (`transport_params.csv`, `transport_paths.csv`). Engineer reference values of both cached scenarios (`legacy_transport_reference.csv`). | `extract_transport_v7_0.py`, data sheets |
| 2 Python reference | `transport_model_ref_v7_0.py`: the legacy equations with one switch per bug, as for the power model. Tests: (a) with legacy behaviour it reproduces the cached engineer run to rounding, both scenarios, 2022-2041; (b) the effect of each fix. | Reference and bug list (register L25+) |
| 3 Workbook | Mitigation section 5b "Road transport, engineer model". Each block takes one formula across years and rows, at most 100 characters; 2041 calls LAMBDAs. Blocks: policies; charging and range anxiety; new fuel economy; distance; TCO; demand, stock and choice; fuel use and calibration; buses; results. Inputs sheet `Inputs_transport` (one row per class × powertrain: parameters and data). Policies are added to ScenarioDefinition as scenario rows (feebate by class, distance tax, EV subsidy, ad-valorem tax, VAT and customs for BEVs, charging subsidy). The switch `TrModel` replaces road gasoline, diesel, LPG and gas; road electricity feeds power demand. Biofuels scale with gasoline and diesel. | v3.5 workbook |
| 4 Check | Independent Python copy of section 5b. Legacy match (with the legacy switches) on cached values. Policy tests: EV subsidy raises the EV share; the distance tax lowers distance; a carbon tax lowers fuel use. Regression: with the switch on Elasticity, every other output is unchanged. | Check PASS |
| 5 Docs | `Transport_Method_v7_0.md`, equations (section 5b), LegacyDiff, register, deck slide. | |

Rough size: about 700 Mitigation rows per scenario group, about 25 LAMBDAs, one input sheet, five data sheets. This is about the size of the power model (v1.05-v1.07), so it is best done in two releases: phases 1-2, then 3-5.

## 3. Decisions (user, 2026-10-14: "Go with recommendations" — the first option of each)

1. **Default model:** **Elasticity by default, Engineer by switch** (Settings or ScenarioDefinition `TrModel`). Results stay unchanged until the engineer run is reviewed; this matches the v3.4 rule that a calibration that is not general is off by default. Alternative: Engineer on, as legacy's template default.
2. **Bugs:** **fix all, keeping legacy behaviour as switches in the Python reference only** (same approach as the power model). Two fixes change the Egypt results a lot:
   - ownership calibration two-sided and the last data year read from the data;
   - ownership allowed to fall.
3. **Parameters where the methodology note and legacy differ.** Recommendation: **legacy values by default, the note's values listed on sheet Constants**; switch after review. The differences are:

   | Parameter | Methodology note | Legacy |
   |---|---|---|
   | Consumer discount rate | 10-30% by income | 5-15% |
   | Income elasticity of distance driven | 0.05 | 0.1 (−0.4 for 2-3 wheelers) |
   | Driving elasticity | −0.3 / −0.2 | −0.4 / −0.3 |
   | Maintenance cost | Varies with wages | Fixed $/km |
   | ICEV price | Rises with income | Transport2 path |
4. **Range anxiety:** **take Transport3's stored per-country values** (all countries, so general). A live goal seek (VBA, like the ETS one) comes later. If a country has no value, BEV choice falls back to the Dashboard value with a visible flag.
5. **Calibration to the energy balance:** **keep the two steps.** They are live formulas from data, so they work for any country. Report the scale factors, since Egypt's distance factor is 2.7, which signals data problems.
6. **Out of scope for v3.5:** the Transport externality sheet (accidents, congestion, road damage) and mode shift. Buses stay simple.
7. **Policy inputs:** **new ScenarioDefinition rows** (scenario-specific, run by the batch macro), in a block after the legacy rows. Legacy keeps them on the Dashboard.
