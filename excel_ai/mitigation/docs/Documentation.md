# CPAT-AI Mitigation Prototype

*The short guide. Details of every block: the Methods volume. Every legacy bug and issue: the bug-fix register.*

# 1. What it is

The mitigation module of the IMF/World Bank **Climate Policy Assessment Tool (CPAT)**, rebuilt as one readable Excel workbook for one country at a time.

It answers: **what do carbon pricing and related policies do to energy prices, energy use, emissions, government revenue and GDP, year by year to 2041?**

- **Policies in:** carbon tax, a new emissions trading system (ETS) with a cap, feebates, fuel excises, fuel subsidy reform, a methane fee, existing carbon pricing, power-sector policies.
- **Results out:** retail energy prices, fuel use in 16 sectors and 8 fuels, electricity generation and prices, revenue, CO₂ and other greenhouse gases, local air pollutants, GDP effects, the gap to the country's NDC, and household effects by decile (Distribution tab).
- **One country, any country:** formulas contain no country numbers. Every country value comes from the data tabs, looked up by the country code on `Settings` (C4). The shipped data are complete for Egypt.
- **Same as legacy, minus its bugs:** it follows legacy CPAT except where legacy has a bug (all fixed) or an open question that we track (issues). See section 5.
- **Readable and checked:** every formula is at most 100 characters and one formula serves a whole block of cells. An independent Python recomputation checks every number.

# 2. Quick start

1. **Open** `CPAT-AI-Mitigation-Prototype_v<version>.xlsm` (in `excel_ai/`; the same file as `excel_ai/permalink/CPAT-AI-Mitigation-Prototype_latest.xlsm`) in Excel 365 with macros enabled. It opens on `ScenarioCompare`, the dashboard, **without recalculating**: the file ships with its values, in manual calculation.
2. **After any change, click Recalculate now** (or switch automatic calculation on with Recalculation on/off).
3. **Read the results on ScenarioCompare.** Choose Live or Stored results and the year. The key table shows CO₂, GHGs, revenue, the GDP effect and welfare against the baseline; the charts show them over time.
4. **Change a policy** on `ScenarioDefinition`. Column K is the live scenario: for example change `CPLevelTarget` (carbon price in the target year), then Recalculate now.
5. **Store several scenarios:** copy a definition one column to the right, give it a short name (row 2) and Run? = Yes (row 4), then click Run stored scenarios. Results go to `StoredOutputs`; the dashboard compares up to 10.
6. **Update the data** from the data workbook: choose the source on `ScenarioCompare`, click Update data tables. The status is on `Cover`.
7. **First time only:** click First-run test (grey buttons). The check table must show PASS.

The tabs, left to right: the front (`Cover`, `ScenarioCompare`, `ScenarioDefinition`), the model (`Mitigation`, `Distribution`, `MTOutputs`, `StoredOutputs`), the inputs (`Manual inputs`, `Settings`, `Inputs`), the data tabs (legacy tables, unchanged), and the reference tabs (version log, differences with legacy, variable dictionary).

# 3. How it works

The `Mitigation` tab runs top to bottom, one section per step, with the section numbers of legacy CPAT. Each scenario is a group of columns: group 1 is the baseline, group 2 the live scenario. Years run across, 2022 to 2041.

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

## 3.9 Distribution (tab Distribution)

Household effects by decile in one analysis year: price changes reach households directly (energy) and indirectly (other goods, through the input-output table); revenue recycling (transfers, targeted by ASPIRE or the poverty line) offsets them.

*Details: Methods, chapter Distribution.*

# 4. Results and the dashboard

**ScenarioCompare** is the place to read results:

- **Choices:** Live (the scenario groups of `Mitigation`) or Stored (every stored scenario), and the year.
- **Key table:** energy CO₂, GHGs, revenue, GDP effect and welfare, as levels and differences from the baseline.
- **Charts:** one bar chart of CO₂ and four time-series charts; the title of each is a dropdown of indicators.

**MTOutputs** lists the key indicators of each live scenario by output code; **StoredOutputs** keeps the stored scenarios as values. Every row carries a code (for example `egy.mit.co2.tot.tot.2`: country, module, variable, sector, fuel, scenario), the same codes as the Python model.

# 5. Limits and differences from legacy

The rule: never replicate a legacy bug; always replicate a legacy issue, and track it. A **bug** (L) is legacy computing what it does not intend; the prototype fixes it. An **issue** (I) is legacy doing what it means to, where the choice is open to question; the prototype does the same. Problems of the input data are issues too (area Data): where legacy reads the data wrongly, the formula fix is a bug with a cell plan and the issue is Very high; where no cell plan is possible, the prototype does exactly what legacy does and the issue is Extremely high (Appendix B). Every item has a code; the codes are explained in Appendix A.

- **Legacy bugs:** the prototype fixes every one, in every module (mitigation, distribution, the inputs). The bugs, with the cell-level fix for legacy CPAT and the status of each in the latest legacy file `CPAT 1.0pre_465`, are in `excel_ai/Legacy_CPAT_Bugs_v<version>.docx`; the master list of bugs and issues is the tracker `excel_ai/Tracking_Legacy_Bugs_v<version>.xlsx`.
- **Issues (data problems first), departures, prototype bugs and upgrades:** the appendices below (and the tracker, tab Issues).
- **Legacy row numbers in the Methods volume** are rows of `CPAT 1.0pre_456_NoPropData.xlsb`, the file the prototype was built and checked against (its data extracts read that file). In `CPAT 1.0pre_465` Mitigation rows from 5667 on sit 11 to 15 rows higher. The input sheet ScenarioDefinition has the rows of the 465 MTInputs.
- **Not built:** a few legacy features (upgrades, Appendix E), and the air-pollution co-benefits and transport externalities modules.
- **Data:** the shipped data are Egypt's; proprietary tables for other countries must be pasted in or linked (issue I90).
