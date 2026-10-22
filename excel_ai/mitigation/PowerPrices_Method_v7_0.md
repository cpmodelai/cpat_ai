# Power generation costs and power prices: method (CPAT-AI-Mitigation-MVP v6.4)

Equations: `Equations_v7_0.md`; workbook formulas: `Formulas_v7_0.md`.

**Scope.** The price side of the power sector:
- what each generation type costs per kWh;
- what the generation mix costs on average;
- the end-user electricity prices for residential and industrial users;
- the power-sector carbon cost and its revenue, by user group and by generation type, and the power part of the revenue totals.

It follows legacy CPAT section 4 ("Technoeconomic ('engineer') power model", Mitigation rows 2954-3672 and 3867-3927) and documentation chapter 3, sections 3.4.1 and 3.4.2.5, keeping legacy's sub-table letters (A Inputs, B Amortised costs, C Levelised costs, D Variable costs, E Total costs, F Memos, G End-user prices, J Storage, plus M Revenues by type). The quantities (demand H, dispatch I, capacity K, investment L) come from the engineer model (`PowerModel_Method_v7_0.md`): generation shares, investment shares and consumption. A policy scenario's power prices therefore respond to its own generation mix, investment and demand.

Units: real US dollars of the results year (2026) per kWh, unless stated. Every ScenarioDefinition power setting (pass-through, minimum cost, storage, WACC, capacity factor and efficiency bounds, renewable subsidy, rebate, excise) is read in the scenario's own ScenarioDefinition column (`PowerModel_Method_v7_0.md`, inputs by scenario). Generation types *f*: coal, natural gas, oil, nuclear, wind, solar, hydro, other renewables, biomass (legacy order).

## 1. Interactions

The price block is mostly a one-way chain. The table lists its links with the rest of the model and how legacy keeps them free of circular references; the MVP implements all of them.

| # | From | To | What flows | How the loop is broken (legacy) |
|---|---|---|---|---|
| I1 | Fuel prices (coal and gas for power, oil, biomass) | D Variable costs | Fuel price before new policies ($/GJ, $/bbl) | One way |
| I2 | Policies (carbon price, ETS power coverage, fuel price reform) | D Carbon cost; G end-user prices; revenues | Carbon cost per kWh by generation type | One way |
| I3 | Generation mix (dispatch I, investment L) | E average generation cost; J storage (via the VRE share) | Generation shares by type | Dispatch uses current variable costs, which do not depend on the average cost; prices use last year's average cost (I5) |
| I4 | Investment (L) | B weighted average capex and storage cost of vintages | New investment as a share of remaining capacity Φ | B uses last year's Φ (exact match with legacy, see 3.2) |
| I5 | E average generation cost | G end-user prices | Supply cost = average generation cost + transmission | **Deliberately lagged one year**: the price in *t* uses the cost of *t*−1 |
| I6 | G end-user prices | Electricity demand → generation → I3 | Residential and industrial electricity prices | Through I5's lag; demand (H) uses last year's prices, by demand group |
| I7 | J storage (systems cost of renewables) | B (vintage storage cost) and C (levelised, for investment) | Marginal storage cost of wind, solar, other renewables | Uses the current VRE share from dispatch |
| I8 | C levelised costs, D9 levelised variable costs | Investment logit; F7 switching carbon prices | Levelised total investment cost by type | Investment only: not in end-user prices |
| I9 | G revenues and M revenues by type | Revenue totals | USD million | One way |

Two consequences shape the design:
1. **End-user prices depend on generation costs only through the weighted average** (E) and the transmission add-on. Variable, amortised and storage costs matter for prices only as far as they enter that average.
2. **The renewables systems cost is an interaction inside the price block.** The VRE share sets the marginal storage cost (J), which enters the cost of wind and solar in two ways: **amortised**, through vintages, in the cost of the existing stock (B), which goes into end-user prices; and **levelised**, in the cost of new plants (C), which goes into investment. So a scenario that adds renewables raises their storage cost per kWh, which feeds back into the average generation cost a year later.

## 2. Simplifications against legacy

Each gives the same numbers as legacy (checked in the Python reference, section 4) unless stated.

| # | Legacy | MVP | Same numbers? |
|---|---|---|---|
| S1 | Five amortised-cost tables (B3 capital, B4 interest, B5 decommissioning, B6 storage, B7 fixed O&M) summed in B8 | One amortised fixed cost per type (3.2) | Yes (algebraically identical) |
| S2 | Six levelised tables (C1-C6) summed in C7; discount-factor tables A5, A6 | One levelised fixed cost per type (3.3), with the discounted lifetime in closed form | Yes |
| S3 | Duplicates: A16 = B7 = C4 (fixed O&M), D7 = D8 (variable cost), E1 = E4 (investment cost), F2/F3 (fuel prices and fuel cost), E2 (cost before storage), E5 (breakdown memo) | Each quantity once | n/a |
| S4 | Residential and industrial price: supply cost + producer subsidy + other tax + "over/under-estimated costs" residual, the last three held at their last-historical-year values, then VAT | Telescoped: after the last historical year the price before policies changes by pass-through × the change in supply cost × (1 + VAT); data before. The three held components cancel out of the change | Yes (pass-through 1, VAT constant after the last historical year, as legacy) |
| S5 | Fuel prices for power: 5-year moving average (A18; spot prices are a dashboard option) | v6.2 (legacy bug L126, user 2026-10-20): trailing average of the price before new policies over t-4 .. t within the scenario's own years (legacy t-2 .. t+2 read later years); spot prices a switch | Price changes reach power costs about two years later | Bug fix |
| S6 | Coal implicit cost (D3) and the additional shadow price (D6) | Not built (both 0 in the Egypt run, no coal in Egypt's mix) | Yes for Egypt |
| S7 | Producer-side subsidies and the over/under-estimate residual as rows | Not needed for prices (S4). Reported as one subsidy gap = price before VAT − supply cost (negative = subsidy), for revenue analysis | Yes for prices |

The price chain for one scenario has about 330 rows in legacy (A5-G4, J1-J3) and about 140 in the MVP.

## 3. Method by legacy sub-table

### 3.1 A. Inputs (one row of constants per generation type, and a few year paths)

| Symbol | Meaning | Legacy |
|---|---|---|
| cax0, N | Capital cost at capex time factor 1 ($/kW; legacy base-year cost ÷ base-year factor), lifetime (years) | A2, B2 |
| tcf(t) | Capex time factor (renewables fall; others 1) | A7 |
| cax(t) = cax0 × tcf(t) | Capital cost path | A13 |
| wacc | Country WACC + technology premium | A3, B4 "Final WACC" |
| cf | Capacity factor (constant) | A8 |
| ν | Thermal efficiency, NCV (constant) | A9 |
| dtc, tcx | Decommissioning cost; levelised transmission capex ($/kW) | A14, A15 |
| opf | Fixed O&M ($/kWh) | A16 |
| vop | Variable O&M ($/kWh); nuclear fuel 0.004 $/kWh included as fuel | D1, D2 |
| rns | Renewable subsidy ($/kWh, negative = subsidy; 3.3b) | A17 |
| dlf | Discounted lifetime (1 − (1+wacc)^−N) / (1 − (1+wacc)^−1) | A6 |

### 3.2 B. Amortised (cost-recovery) fixed costs: the cost of the existing stock

- Weighted average capex of the stock: last year's average and last year's new capex, weighted by last year's Φ; in the base year, the base-year capex. Exact match with legacy.
- Weighted average storage cost of vintages: the same, but new vintages take the current-year marginal storage cost. Exact match with legacy.
- Amortised fixed cost (S1) = (average capex × (1/N + wacc/2) + dtc/N) / (cf × 8,760) + average storage cost + opf.

### 3.3 C. Levelised (forward-looking) fixed costs: new plants (investment)

Levelised fixed cost (S2) = (cax + dtc + tcx) / (cf × 8,760 × dlf) + marginal storage cost + opf + rns.

### 3.3b Renewable subsidies (A17, C5)

- Subsidy per kWh rns(t) = −(base subsidy RenewableSubsidyBL + additional subsidy RenSubsidyAddUSDkwh × MAX(0, 1 − (t − start)/n) from the start year RenSubsidyAddStartYear, policy scenarios only), with n = RenSubsidyAddPhaseoutYrs. The inputs are labelled nominal and used as real, as legacy.
- It applies to wind, solar, other renewables and biomass, and to hydro if RenewableSubsidyHydro = Yes.
- It enters the levelised fixed cost (investment), not the cost of the existing stock or the end-user price; its revenue is rns × generation by type (negative), in the power subsidies and in row ren of the revenue by policy.

### 3.4 D. Current variable costs

- Fuel price for power (A18; v6.2, legacy bug L126): average of the fuel price before new policies `fpn` over t-4 .. t from the base year (one year in 2022, five from 2026); legacy averages t-2 .. t+2, which reads later years. The spot price is a switch. Row `fpn` holds this year's price, so the average reads one row and only the scenario's own years.
- Fuel cost per kWh = fuel price × 0.0036 / ν. Nuclear: 0.004 $/kWh. Renewables 0.
- Change in existing carbon pricing against the price data (`PriceProjection_Method_v7_0.md` section 5b): tCO2/kWh × the change in the existing carbon tax and ETS price, weighted by their coverage of power and the fuel (0 for Egypt).
- Variable cost before new policies = variable O&M + fuel cost + change in existing carbon pricing.
- Carbon cost per kWh generated = the new policy wedge on the fuel in power ($/GJ) × 0.0036 / ν. The wedge sums the carbon tax (carbon price × EF × fuel coverage × power coverage × (1 − ETS coverage of power)), the ETS (tax-equivalent price × EF × ETS coverage of power × (1 − OBR share of power)) and the fuel price reform for coal and gas in power.
- Total variable cost = cost before new policies + carbon cost + shadow price + rebate (feebates and the output-based part of the ETS). Dispatch uses it.

### 3.5 E. Total costs

- Generation cost before carbon (cost recovery, legacy E3) = amortised fixed cost + variable cost before new policies.
- Average generation cost = generation-share-weighted average of that cost.
- Average carbon cost per kWh consumed = share-weighted carbon cost × generation / consumption. The ratio covers losses, own use and net exports, from the base-year balance.

Carbon is kept out of the average generation cost and added separately (legacy, documentation 3.4.1.7), so a rebate can be computed against it.

### 3.6 F. Memos

F7 switching carbon prices, F1 system cost and F4 carbon intensity are memos. Only F4 (tCO2 per kWh = EF × 0.0036/ν) is built, as a parameter.

### 3.7 J. Systems integration cost of renewables (storage)

- VRE share v = share of wind + solar + other renewables (legacy row 3851).
- Short-term storage (batteries): marginal hours = ast × 18 × v, with ast = 1 the share allocated to VRE and 18 = d(9 v²)/dv. Cost per hour per kWh = (battery capex + interface capex / 2 hours kWh/kW) / (dlf of renewables × 8,760) + battery opex / 8,760.
- Long-term storage (electrolysers): marginal units = LongTermStorageFor100pcVRE × 2 × max(0, v − x) / (1 − x)², with x = StartingPointWhenLTStorageIsNeeded (0.75). Cost per unit = (electrolyser capex + LT storage capex per kWh × StorageHoursForLTStorage) / (dlf of renewables × 8,760) + fixed opex / 8,760 + variable opex.
- Marginal storage cost of wind, solar and other renewables = hours × cost per hour + units × cost per unit; 0 for other types.

Legacy has a 33% "allocation of LT storage to VRE" parameter and applies it twice (rows 3911 and 3912, a bug). The MVP applies it once.

### 3.8 G. End-user prices (residential and industrial)

- Supply cost (I5, lagged) = last year's average generation cost + transmission (0.040 $/kWh residential, 0.015 industrial). In the base year, the base-year average cost.
- Price before new policies (S4): up to the last historical year L, the historical retail price including VAT from the price dataset (nominal → real with the CPI index); after L, last year's value + pass-through × change in supply cost × (1 + VAT of L), with pass-through 1 (legacy hardcode).
- End-user price = price before new policies + (average carbon cost × pass-through × (1 − rebate switch) + excise) × (1 + VAT). As in legacy (rows 3614-3617), VAT is charged on the new policy terms.
- Rebate switch (legacy rows 261, 2188, J3595): 1 in policy scenarios with PowerRebates = Yes (or Yes*) or a feebate scenario of the legacy scenario table (Feebates, Power Supply Feebates, Power feebate); the carbon cost is then not passed to electricity users.
- Excise per kWh before VAT = electricity excise + pass-through × (manual excise − its value in the last historical year) after that year. The electricity excise (scenario Electricity excise, policy scenarios; legacy row 2253) = grid CO2 intensity of the base year (CO2 of the fuel input to power / power output, Balances) × carbon price. The manual excise (policy scenarios with AdditionalExcise = Yes; legacy rows 3602, 3631) is the new electricity excise of 'Manual inputs' rows 161-162 (real, or nominal × the deflator index if NomorReal is not Real); like legacy it enters the price before policy, so up to the last historical year it is absorbed by the price data and later its change is passed through.
- Subsidy gap (S7) = price before new policies / (1 + VAT) − supply cost. Negative = price below the modelled supply cost (subsidies are negative).

### 3.9 G4 and M. Revenues (USD million real) and the revenue totals

By user group (G), each × consumption of the group:
- VAT = price before new policies × VAT / (1 + VAT);
- VAT on the new-policy cost passed through = (average carbon cost × pass-through × (1 − rebate switch) + excise) × VAT;
- rebate (negative) = − rebate switch × average carbon cost × pass-through: the carbon cost returned to users (the VAT on it is not collected);
- excise = excise per kWh × consumption, of which the electricity excise of the scenario (carbon-based) and the manual excise;
- subsidy gap (signed: negative = fiscal cost, positive when the price is above the modelled supply cost);
- new-policy cost (memo; it values the ETS at the tax-equivalent price) = average carbon cost.

By generation type (M), with a fuel flag of 1 for coal, gas, oil and biomass:
- existing taxes on generation fuels = flag × fuel use × (excise + VAT) of the price fuel;
- existing subsidies on generation fuels = flag × fuel use × subsidy (negative);
- change in existing carbon pricing × generation;
- new policies = generation × carbon cost − CO2 × the power ETS cost rate × (1 − revenue factor): the ETS part at the permit price, as in the subsectors;
- existing carbon pricing level (memo) = CO2 × the covered existing carbon tax and ETS prices.

The revenue totals add a power row: existing taxes = fuel taxes + change in existing carbon pricing + electricity VAT; subsidies = fuel subsidies + subsidy gap + renewable subsidies; new policies = new-policy revenue by type + VAT on new policies + rebate + excise; existing carbon pricing level = the memo by type. In the revenue by policy (12e), the rebate and the carbon-based excise count with the carbon tax, the manual excise with the excise, and the renewable subsidies in their own row (as legacy rows 7749, 7762, 7903, the base subsidy once). The fuel subsidy and the subsidy gap do not overlap: the supply cost already uses the subsidised fuel price, so the gap is what remains between that cost and the tariff.

## 4. Validation

1. **Method = legacy.** A Python reference feeds the legacy inputs (its fuel prices, shares, Φ, prices and VAT) into this method and reproduces the cached legacy rows B2, B6, B8, C7, D4, E3, the weighted average, J storage, and G1/G2 supply cost and prices, to a relative error below 1e-6.
2. **Workbook = Python** for the MVP's own inputs (corrected Egypt prices, moving-average fuel prices as legacy), as for the other checks.
3. **Formula uniformity** and copies of scenario groups, as for the rest of the sheet.
4. **Regression** against the previous version (shared output codes). The power block feeds total fuel use (generation fuel use), revenues and CO2.

Result at the first build of the price block (`check_report_v1.05.md`, PASS): 80 legacy rows reproduced, largest relative difference 5.6e-17; all 28 power variables equal the Python reference in every scenario test, largest relative difference about 5e-15; one formula per block; 3,642 codes unchanged against the previous version.

## 5. Decisions

1. Fuel prices for power: moving average as legacy (user decision); spot prices remain a switch (S5).
2. VAT on power policy terms: legacy charges VAT (row 3614); the MVP does too, as for fuels.
3. Historical electricity prices: the corrected Egypt block (residential 0.054, 0.048, 0.043 $/kWh nominal, 2022-2024) differs from legacy's vintage (0.097 in 2022). The MVP uses the corrected block.
4. Producer-side subsidy data: the corrected block has none for electricity; legacy used −9.2 bn USD in 2022. The MVP reports the modelled subsidy gap instead (S7).


## v5.6: fuel price reform, price floor, renewable subsidies in real terms

- The electricity fuel price reform path of the scenario (section-1 rows fpr.ecy.res, fpr.ecy.ind; ScenarioDefinition 148-149, 162-163) enters the manual excise of policy scenarios (row entx), as legacy row 216 (issue I59, replicated).
- End-user electricity prices are floored at MinPostSubsidyPowerPrice (row rp), as legacy rows 3617 and 3646 (issue I60, replicated; 0.01 $/kWh: not binding for Egypt).
- The renewable subsidy inputs (ScenarioDefinition 354-355, labelled nominal) are converted to real with the CPI factor of the year (row rnsp; legacy bug L114, fixed).
- The levelised cost includes TransmissionCostShare (ScenarioDefinition appendix block B, default 1) of the transmission capex (legacy IncludeTransmissionCostsInGenerationCostsPercent).
