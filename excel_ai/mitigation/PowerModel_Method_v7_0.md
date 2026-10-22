# Power engineer model: method (CPAT-AI-Mitigation-MVP v6.4)

Equations: `Equations_v7_0.md`; workbook formulas: `Formulas_v7_0.md`.

**Scope.** The quantity side of the power sector: power demand (legacy table H), dispatch (I), capacity and retirement (K), investment (L), and the cost rows investment needs: shadow price and rebate (D6), levelised variable cost (D9) and levelised investment cost (E1). The price side is in `PowerPrices_Method_v7_0.md`. The legacy reference is Mitigation section 4 of `CPAT 1.0pre_456_NoPropData.xlsb`: rows 2954-4297 for the baseline, rows 9285-10628 for the carbon-tax run.

**Inputs by scenario.** Every ScenarioDefinition power input is read in the scenario's own ScenarioDefinition column (section 1, "Power sector settings": rows 242, 262, 342-415 and 482), as legacy runs each column with its own runs. Sub-table A0 of section 3 applies them to the power data of the country (Inputs): capacity factor, efficiency, WACC and discounted lifetime, fuel per kWh, base-year capacity, new investment permitted and its start year, scale-up and retirement rates, the early-retirement factor, the capex decline scenario, storage, PPA, renewable subsidy, rebate and excise settings. Scenario 1 is the baseline of every scenario, so a technical input (logit constants, WACC, capacity-factor bounds, storage, cost decline) changed in a policy scenario changes that scenario only, and its difference to scenario 1 mixes the input change with the policy; technical inputs are not usually changed across scenarios. Not read (no MVP feature): CostBreakdownYear, ElasticityModel, PowGenCostsOldNew, UseElasticityModelPowerDemandInEngineerModel, SupplyCostDeltaSubsidy, the coal implicit cost (369-371). The final deficit to gas is a global switch (Settings C45, PwDeficitGas), as legacy's typed cell.

**Alignment.** The MVP follows legacy formula by formula, except for ten bugs, which are fixed; `CPAT-AI-Mitigation-MVP_BugsAndIssues_v6.4.docx` lists them with their effects. `power_model_ref_v7_0.py` implements the method in Python with one switch per bug; with all switches off it reproduces 208 cached legacy rows of both runs to 1e-13. Planned retirement is available for every generation type; legacy offers it for coal only.

**Links with the rest of the model.** Power demand follows its own elasticities (H). Sector policies (carbon tax, ETS, feebates, fuel price reform) act on the fuel blocks only, not on power demand; electricity demand by sector is a memo, not part of the fuel totals, so nothing is counted twice. Power CO2 enters the CO2 totals (by fuel and as ETS sector power, so a new ETS covering power sees it, and the baseline CO2 data include it). Generation fuel use of coal, gas, oil and biomass enters total fuel use; nuclear, wind, solar, hydro and other renewables have no fuel. Power revenues enter the revenue totals: fuel taxes and subsidies on generation, the change in existing carbon pricing, electricity VAT and subsidy gap, and new policies with the ETS at the permit price. Existing carbon pricing changes the variable cost before new policies (`PriceProjection_Method_v7_0.md` section 5b). A Settings switch turns the legacy 2023-2024 demand shock on (default off, as for fuels).

Units: generation and capacity in MW / MWy; demand in ktoe; costs in real $/kWh of 2026.

## 1. Order within a year and across years

```
year t:  H  demand(t)        <- demand(t-1), GDP(t), price(t-1)              (no circularity: price lagged)
         K1 capacity(t)      <- capacity(t-1) - retirement(t-1) + investment(t-1)
         I  dispatch(t)      <- capacity(t), required generation(t), variable costs(t)
            shares(t)        -> J VRE share -> storage cost(t) -> B (vintages), C (levelised)
            shares(t)        -> E average generation cost(t) -> G supply cost(t+1) -> price(t+1) -> demand(t+2)
         K  retirement(t)    <- capacity(t), early coal retirement (coal variable cost vs wind and solar costs)
         L  investment(t)    <- required generation(t) - capacity after retirement(t); logit on E1(t)
                             -> capacity(t+1); share in the stock phi(t) -> B vintages(t+1)
```

The levelised variable cost D9(t) averages the variable cost from t to the end of the horizon. Variable costs depend only on prices and policies, not on the generation mix, so D9 is computed before the year loop, backwards from the last year.

## 2. Method (with fixes)

**H Demand.** Four demand groups (transport, residential, industry, services), with electricity elasticities to income, usage, efficiency and autonomous efficiency (eps_Y, eps_U, eps_F, alpha).
- Each group's price is last year's residential and industrial prices weighted 0.5/0.5 for transport, 1/0 for residential, 0/1 for industry and services.
- Each group's demand multiple combines autonomous efficiency, GDP growth (with the income factor), the price change and an optional shock: (1 / (1 + alpha + extra))^(1 + eps_U) × (1 + GDP growth)^(eps_Y × inc) × (price ratio)^(eps_U + eps_F + eps_U eps_F) × (1 + shock × switch).
- Demand of each of the 15 subsectors = last year's × its group's multiple (services use the services multiple in every year).
- Required generation (MWy) = demand × (1 + net exports + transmission + own use + statistical difference shares), converted from ktoe. In the base year it is actual generation.
- Memo: demand by group, and electricity demand by subsector, sector and in total.

**A0 Data of the scenario.**
- Capacity factor = actual (base-year output / installed capacity) when strictly between the CFOverride bounds of the scenario (wind and solar: CFOverrideIfBelowWndSol; others: CFOverrideIfBelowFosOth; upper CFOverrideIfAbove), else the studies value. Efficiency = actual (output / input) unless below MinimumThermalEfficiency (or without input), else the studies value.
- WACC: Country* (country WACC + coal premium), Tech (country WACC + technology premium), else MAX(WACCUserGlobal (User), the income-group WACC (Income*) or the studies WACC, MinimumWACC). Discounted lifetime = (1 − (1 + WACC)^−N) / (1 − (1 + WACC)^−1); renewables use the average of wind and solar.
- New investment: the type's NewInv setting; "If Present*" = Yes when the type has more than 0.1% of base-year capacity; from the NewInv year (hydro from the base year when its generation share is above one half).
- Scale-up rates: coal, gas, hydro MaxNonVREAsPCOfTotalGen; wind and solar the country default (CtryDefault*), MaxWindSolarScaleup (UserDefined) or the category rate (Low, Medium*, High, Vhigh); the others MaxNonNucOreBioAsPCOfTotalGen. Retirement rate 1/N, hydro 0 if HydroDoesntRetire = Yes.
- Capex time factors of the decline scenario of RenewableCostDeclineRate (renewables; others medium); where the Power tab has no series for the option (Low and Vhigh for wind and solar, Vhigh for other renewables), the older series of the same option, else medium.

**I Dispatch.**
- Fixed-output types (wind, solar, hydro, other renewables, oil, nuclear, biomass) generate capacity × capacity factor.
- Coal and gas cover the rest. Each first gets the minimum it must supply given the other's maximum (maximum = capacity × MaximumCoalCF for coal, × MaximumGasCF for gas; 0.9 by default); the remainder is shared by a logit EXP(-kDispatch × variable cost / lowest variable cost), capped at the maximum.
- PPAs: a share p of coal and gas generation (PPAProportionCoalGas × phase-out factor) runs at its capacity factor, scaled to the need, whatever its cost: generation = logit dispatch × (1 − p) + effective capacity × (coal and gas need / coal and gas effective capacity) × p. The phase-out factor falls linearly to 0 over YearsToPhaseOutPPAs years after YearPPACoalGas when the switch of the scenario (PhaseOutCoalAndGasPPAsBaseline in scenario 1, PhaseOutCoalAndGasPPAsPolicy in the others) is Yes or Yes*; else 1.
- Fuel use = generation / efficiency (ktoe); CO2 = fuel use × EF.

**K Capacity and retirement.**
- Retirement = planned retirement (data in nameplate MW per year, if the type's switch is Yes) or else capacity / lifetime; plus early retirement for coal; at most the capacity. Hydro does not retire. Effective retirement = retirement × capacity factor.
- For Egypt the legacy file has no planned-retirement data, so every switch is No.
- Early coal retirement: room = MAX(0, maximum wind and solar additions − last year's increase in generation − last year's non-coal effective retirements); early = MAX(0, MIN(0.8 × coal effective capacity, room) × (1 − coal share of a logit over coal variable cost and wind and solar investment costs)) / coal capacity factor × factor × (1 − PPA share). The factor is MaxCostBasedEarlyRetirement, and 0 in scenario 1 unless EarlyRetirementInBaseline = Yes (legacy F3993); plants under PPA do not retire early.
- Capacity needed = MAX(required generation − (effective capacity − effective retirement), 0). Capacity bought in year t is available in t+1.

**L Investment.**
- First round, permitted types only: logit share EXP(-2 × E1 / lowest permitted E1), limited by a scale-up limit (rate × total effective capacity).
- Second round: the remaining deficit goes to types with space left, cheapest first.
- Final deficit: with PwDeficitGas = Yes (Settings C45; default No, as legacy's typed switch E4248) the deficit left after the second round goes to gas (legacy row 4252).
- Nameplate investment = effective / capacity factor; USD = nameplate × capital cost of the year.
- phi = nameplate / (capacity + nameplate − retirement), the new-vintage share used in the vintage averages B2 and B6.

**D5, D6, D9, E1.** Each sector has three policy rates ($/tCO2), the same for the fuel blocks and power:
- carbon tax = carbon price × sector coverage × (1 − ETS coverage);
- ETS cost = ETS tax-equivalent price × ETS coverage × (1 − OBR share);
- shadow price = feebate (and regulation) rate × share impacting efficiency + ETS tax-equivalent price × ETS coverage × OBR share.

New policy cost per kWh (D5) = tCO2/kWh × (carbon tax × fuel coverage + ETS cost) + fuel price reform per kWh. The levelised fixed cost (C) includes the renewable subsidy per kWh of the scenario (`PowerPrices_Method_v7_0.md` 3.3). The shadow price per kWh is the power shadow price × tCO2/kWh; the rebate returns it in proportion to base-year shares, per kWh generated. Total variable cost = cost before new policies + new policy cost + shadow price + rebate. D9 = discounted average of the total variable cost to 2041, the last year (as legacy). E1 = MAX(levelised fixed cost + D9, 0.01).

## 3. Validation (`check_report_v6.4.md`)

1. **Method = legacy.** The Python reference, fed with the cached legacy inputs and the bugs switched on, reproduces 208 legacy rows of the baseline and the carbon-tax run.
2. **Workbook = Python.** With all bugs fixed and the MVP inputs, the workbook matches the Python reference for every power row, in every scenario test.
3. **Properties:** generation = required generation; the capacity balance holds; investment is at most the capacity needed (scale-up limits can leave part unplaced); the supply cost lag holds; a carbon price raises the VRE share and lowers power CO2.
4. **Planned retirement.** With the switch on for gas and oil and test data, the workbook matches the Python reference, and retirement equals the data.
4b. **Power features.** One test scenario per feature (check section 5d): MaximumGasCF and long-term storage; the power inputs of the scenario (two scenarios with many inputs changed, including WACC options, capacity-factor and efficiency bounds, permits, scale-up categories, decline options, storage, logit constants, pass-through, spot prices); PPAs; renewable subsidies; the rebate; the electricity excise and the manual excise; the final deficit to gas with tight scale-up limits. Each matches the Python reference.
5. **Memo lines** equal power demand by subsector and add up by sector and in total.
6. **Totals.** Fuel use, revenue and CO2 totals with power equal the Python reference; with non-zero existing carbon pricing test data, the power variable cost, revenues by type and totals match too. Check rows confirm that the totals equal their sector, power and fuel parts.


## Manual capacity and investment (v5.6, power plan P3)

Where a scenario's NewInv<type> = Manual (ScenarioDefinition rows 397-405), the type follows the capacity path of 'Manual inputs' (rows 349-357 for scenario 1, rows 363-371 for the other scenarios; names ManCapVal, ManCapYr). Row mancap reads the path; row mani is the manual new effective investment, MAX(0, next year's path - this year's path + retirement) x capacity factor (0 in 2041); the type gets no logit investment (permit 0). Row needm = MAX(need - SUM(mani), 0) sizes the logit and second-round investment: legacy computes this need (row 4108) but never uses it, so its logit investment comes on top of the manual one (legacy bug L118, fixed). New effective investment nei = first + second (+ gas deficit) + mani. Test (scenario 2, nuclear 2,400 MW from 2030): 2,400 MW nameplate built in 2029, then the retirements replaced.

## Coal implicit cost (v5.6, power plan P5)

Rows cics, cicl and cic (sub-table D): AdditionalCoalIntangibleCost (ScenarioDefinition 369) No = 0, Manual = ScenarioDefinition 370-371, else the GoalSeekCoal table (legacy tab, 85 countries, not Egypt) by country; linear from the first year of calculations to CoalICYr (2030), as legacy rows 3360-3363. It is added to the coal variable cost (dispatch, levelised cost, investment) and, unless Settings PwCoalICTariff = No (default Yes, as legacy; decision 6), to the generation cost and tariffs. Memo rows (sub-table E): fce (post-tax fuel cost per kWh, legacy F2-F3), cik (tCO2 per kWh, F4), swi and swd (switching carbon prices gas over coal for new investment and dispatch, F7; F1, F5 and F6 are rows lfx/tic and tvc). The GoalSeekCoal calibration script is not built.
