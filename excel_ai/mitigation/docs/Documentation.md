# CPAT-AI Mitigation

*The short guide. Details of every block: the Methods volume. Every legacy bug and issue: the bug-fix register.*

# 1. What it is

The mitigation module of the IMF/World Bank **Climate Policy Assessment Tool (CPAT)**, rebuilt as one readable Excel workbook for one country at a time.

It answers: **what do carbon pricing and related policies do to energy prices, energy use, emissions, government revenue and GDP, year by year to 2041?**

- **Policies in:** carbon tax, a new emissions trading system (ETS) with a cap, feebates, fuel excises, fuel subsidy reform, a methane fee, existing carbon pricing, power-sector policies.
- **Results out:** retail energy prices, fuel use in 16 sectors and 8 fuels, electricity generation and prices, revenue, CO₂ and other greenhouse gases, local air pollutants, GDP effects, the gap to the country's NDC, and and the exports the other modules read (section 19; household effects by decile are the separate Distribution module).
- **One country, any country:** formulas contain no country numbers. Every country value comes from the data tabs, looked up by the country code on `ScenarioDefinition` (MTInputs, Model settings). The shipped data are complete for Egypt.
- **Same as legacy, minus its bugs:** it follows legacy CPAT except where legacy has a bug (all fixed) or an open question that we track (issues). See section 5.
- **Readable and checked:** every formula is short (target 90 characters, at most 115) and one formula serves a whole block of cells. An independent Python recomputation checks every number.

# 2. Quick start

Since 1.2.0 the module workbooks have **no macros**. Every macro is in the **Master workbook**, `excel_ai/active_workbooks/CPAT-AI-Master_UserGuide.xlsm`, which is also the user guide. The mitigation module ships as `excel_ai/mitigation/CPAT-AI-Mitigation_latest.xlsx` (every version in `excel_ai/mitigation/releases/`) with formulas to 2035, so it is small and quick to open; the Master **activates** it into the workbook you work in, `excel_ai/active_workbooks/CPAT-AI-Mitigation_latest.xlsb`, with formulas to 2041.

1. **Get the files.** Keep the repository clone up to date (git, or the SyncRepo script). The Master finds the modules in the clone (else it downloads them from GitHub, the links of its module table).
2. **Open the Master** (`active_workbooks/CPAT-AI-Master_UserGuide.xlsm`) in Excel 365 and enable macros (if the file was downloaded, unblock it first: file Properties > Unblock). Its tab `UserGuide` lists each module (latest version, the `.xlsx`, its GitHub link, the `.xlsb` it writes, when it was last activated) and has the buttons.
3. **Activate:** click *Activate Mitigation* (or *Activate all modules*). The Master opens the `.xlsx`, copies the 2035 column of each scenario group of `Mitigation` and `MTOutputs` across to 2041, records the activation on the module's tab `FromMaster`, recalculates fully and saves `CPAT-AI-Mitigation_latest.xlsb` next to itself. The workbook stays open. Activate again whenever a new `.xlsx` arrives; the `.xlsb` is a generated file (never merge it on a git conflict: take either side and activate again).
4. **Work in the `.xlsb`.** It is in manual calculation: **press F9 after any change** (Ctrl+Alt+F9 for a full recalculation).
5. **Change a policy** on `ScenarioDefinition` (the legacy MTInputs rows). Column J is the baseline, column K the live policy scenario: for example change `CPLevelTarget` (the carbon price in the target year), then F9. Columns L onwards are scenario definitions for the batch run.
6. **Read the results** on `MTOutputs` (every scenario group side by side, by output code) and `ScenarioCompare` (the dashboard: choose the year; key table and time-series charts of the live scenarios against the baseline).
7. **Store and compare scenarios** in the Master: *Store live scenarios* copies the scenario groups of `MTOutputs` into its `StoredScenarios` (values, ten slots); *Run stored scenarios* runs every definition with Run? = Yes through the live column K (ETS goal seek where needed) and stores each; `CompareStored` compares them. *Clear stored scenarios* empties every slot but the baseline.
8. **Update the data** in the Master: choose the data source and the rows (one country or all countries) on its tab `Settings`, then *Update data tables* (Power Query). The mitigation workbook records the source on `FromMaster`; the status is on its `Cover`.
9. **Distribution:** activate the distribution module too, then *Update Distribution from Mitigation* copies section 19a of the activated mitigation workbook into it, recalculates and saves it.

Run a module for a particular country on your local drive; a workbook holding real data is never committed.

The tabs, left to right: the front (`Cover`, `ScenarioDefinition`), `MAIN->>` (`Mitigation`), `OUTPUT->>` (`MTOutputs`, `ScenarioCompare`), `INPUTS->>` (`Manual inputs`, `Constants and Mappings`), `OTHER MODULES->>` (`FromMaster`, `FromAirPollution`, `FromTransportCB`), the data tabs (`DATA_MITIGATION->>`, `DATA_TRAN->>`, `DATA_OUTPUT->>`, `DATA_OTHER->>`: legacy tables, unchanged) and `REF->>` (version log, differences with legacy, variable dictionary and LAMBDAs).

# 3. How it works

The `Mitigation` tab runs top to bottom, one section per step, with the section numbers of legacy CPAT. The method of each block, with its equations and pseudocode, is in the website's CPAT-AI Model tab (<https://cpmodelai.github.io/cpat_ai/#model>; sources `docs/CPAT_model_documentation_qmd/`), shared with CPAT Python; the Word Methods volume (`docs/methods/`) is the compact version. Each scenario is a group of columns: group 1 is the baseline, group 2 the live scenario (further groups: copy group 2 to the right; MTOutputs has room for four). Years run across, 2022 to 2041.

| Section | Step | Methods chapter |
|---|---|---|
| 1 | Policies: the price signals of each policy | Prices |
| 2 | Retail energy prices before and after policies | Prices |
| 3 | Power: demand, dispatch, investment, electricity prices | Power |
| 5, 5b | Transport, and the optional road engineer model | Transport |
| 6, 6b, 7, 8 | Buildings, residential leakage to biomass, industry, other energy use | Appendix A |
| 11 | Energy consumption totals | - |
| 12 | Revenues | Macro and results |
| 13, 14, 15 | CO₂, other greenhouse gases, local air pollutants | Emissions |
| 16, 17, 18 | GDP effects, carbon pricing indicators, welfare | Macro and results |

## 3.1 Policies (section 1)

Each policy is a path from a start year to a target year, set per scenario on `ScenarioDefinition`. The carbon price follows that path:

```
τ(t) = path(t; start year, target year, start level, target level) · (CPI index if the inputs are nominal)
```

A new ETS starts at a price estimate and is checked against its cap (the goal seek refines it). Feebates act through a shadow price, which changes efficiency but raises no revenue. Existing carbon taxes and ETS prices come from the World Bank Carbon Pricing Dashboard data.

*Details: Methods, chapter Prices; chapter ETS.*

## 3.2 Energy prices (section 2)

For each fuel and sector, the retail price builds up from the international price:

```
supply cost  C(t) = fixed part + (C(t−1) − fixed part) · international price(t) / international price(t−1)
retail price R    = (C + excise and other taxes) · (1 + VAT)
after policy P    = R + new carbon tax + ETS price + new excise, each with VAT
```

Subsidies are negative taxes. Historical prices come from the IMF price data up to the last historical year (2022, as legacy); later years are projected.

*Details: Methods, chapter Prices.*

## 3.3 Energy demand (sections 5-8, 11)

Fuel use in each sector changes each year with income, its own price and efficiency:

```
Q(t) = Q(t−1) · (efficiency gain) · (1 + GDP growth)^(income elasticity) · (P(t)/P(t−1))^(price elasticity) · (efficiency response to prices)
```

The elasticities are legacy CPAT's. Section 11 adds up fuel use by sector and fuel, including the fuel burnt in power plants.

*Details: Methods, appendix A (equations, section 4); chapter Transport for road.*

## 3.4 Power (section 3)

Electricity demand comes from the sectors. The power model, as legacy's engineer model, decides each year:

- **Dispatch:** which plants run, by their variable cost (fuel, carbon price, operation).
- **Investment:** new capacity by technology, chosen by levelised cost with a logit share, within scale-up limits.
- **Prices:** electricity prices from the cost of generation, with taxes, subsidies and price controls.

Power-sector policies (no new coal, nuclear from a year, renewable subsidies, PPAs, rebating revenue, an electricity excise) are set per scenario.

*Details: Methods, chapter Power.*

## 3.5 Road transport (sections 5, 5b)

By default road fuel use follows the demand elasticities, as every other sector. With `TrModel` = Engineer, the road engineer model replaces it: vehicle stocks by class, cost of ownership, the choice between combustion and electric vehicles, and vehicle policies (feebates, EV subsidies, purchase taxes, distance tax).

*Details: Methods, chapter Transport.*

## 3.6 Revenues (section 12)

Revenue is fuel use times the tax per unit, by fuel and sector, for existing taxes, existing subsidies (negative) and new policies:

```
revenue from new policies = fuel use · (carbon tax + excise + auctioned share · ETS price + VAT on them)
total revenue             = existing taxes + subsidies + new policies + methane fee
```

The power sector adds its own revenue and subsidies. Feebates are revenue neutral.

*Details: Methods, chapter Macro and results.*

## 3.7 Emissions (sections 13-15)

```
CO₂ = fuel use · emission factor        (factors optionally calibrated to the GHG inventory)
```

Other greenhouse gases (methane, nitrous oxide, F-gases) follow their drivers; methane from fuel supply responds to the methane fee. Local air pollutants (fine particles, sulphur and nitrogen oxides, and others) are fuel use times pollutant factors.

*Details: Methods, chapter Emissions.*

## 3.8 GDP, carbon pricing indicators, welfare (sections 16-18)

New revenue is fiscal space. How it is used (tax cuts, investment, transfers) moves GDP through fiscal multipliers, one year later:

```
fiscal space fs(t)  = (new revenue in the scenario − in the baseline) / GDP
GDP effect          = Σ over uses: share of the use · Σ over lags (change in fs · multiplier of the use)
```

Section 17 reports carbon prices and coverage; section 18 the welfare effects and the gap to the NDC.

*Details: Methods, chapter Macro and results.*

## 3.9 Exports to the other modules (section 19)

Section 19 holds what the other modules read, by code: section 19a (defined name `ExportDistn`) is the input of the Distribution module (household effects by decile in one analysis year: price changes reach households directly and indirectly, revenue recycling offsets them). The Master copies it into the distribution workbook (*Update Distribution from Mitigation*).

*Details: CPAT-AI Model, chapter Distribution; `excel_ai/distribution/README.md`.*

# 4. Results and the dashboard

- **MTOutputs** shows the key results of every live scenario side by side, in the columns of the scenario groups of `Mitigation` (row 5: the scenario number; rows as legacy MTOutputs, then the outputs legacy does not list, by topic). Every row carries a code (for example `egy.mit.co2.tot.tot.2`: country, module, variable, sector, fuel, scenario), the same codes as the Python model.
- **ScenarioCompare** (the dashboard) reads MTOutputs only (live results): one slot per scenario group, the year, a key table (energy CO₂, GHGs, revenue, GDP effect and welfare: level, difference and % difference from the baseline) and four time series with their line charts; the title of each is a dropdown of indicators.
- **Stored results** are in the Master: `StoredScenarios` (values, MTOutputs' rows, ten slots) and `CompareStored` (the stored scenarios against the baseline, for a chosen year).

# 5. Limits and differences from legacy

The rule: never replicate a legacy bug; always replicate a legacy issue, and track it. A **bug** (L) is legacy computing what it does not intend; the prototype fixes it. An **issue** (I) is legacy doing what it means to, where the choice is open to question; the prototype does the same. Problems of the input data are issues too (area Data): where legacy reads the data wrongly, the formula fix is a bug with a cell plan and the issue is Very high; where no cell plan is possible, the prototype does exactly what legacy does and the issue is Extremely high (Appendix B). Every item has a code; the codes are explained in Appendix A.

- **Legacy bugs:** the prototype fixes every one, in every module (mitigation, distribution, the inputs). The bugs, with the cell-level fix for legacy CPAT and the status of each in the latest legacy file `CPAT 1.0pre_465`, are in `excel_ai/bugs_and_legacy/Legacy_CPAT_Bugs_v<version>.docx`; the master list of bugs and issues is the tracker `excel_ai/bugs_and_legacy/Tracking_Legacy_Bugs_v<version>.xlsx`.
- **Issues (data problems first), departures, prototype bugs and upgrades:** the appendices below (and the tracker, tab Issues).
- **Legacy row numbers in the Methods volume** are rows of `CPAT 1.0pre_456_NoPropData.xlsb`, the file the prototype was built and checked against (its data extracts read that file). In `CPAT 1.0pre_465` Mitigation rows from 5667 on sit 11 to 15 rows higher. The input sheet ScenarioDefinition has the rows of the 465 MTInputs.
- **Not built:** a few legacy features (upgrades, Appendix E), and the air-pollution co-benefits and transport externalities modules.
- **Data:** the shipped data are Egypt's; proprietary tables for other countries must be pasted in or linked (issue I90).
