# Projecting supply costs and retail energy prices (legacy CPAT method, as implemented in CPAT-AI-Mitigation-Prototype v6.4)

Equations: `Equations.md`; workbook formulas: `Formulas.md`.

How the model projects fuel supply costs and retail prices, following legacy CPAT cut down to the basics, and the existing carbon pricing on top of them (section 5b). Subsidy phase-outs and price liberalisation are left out; electricity prices are in `PowerPrices_Method.md`. The workbook sheet `LegacyDiff` lists all differences with legacy. Two data rules differ from legacy by user decision (A10, A11); legacy bug L14 is fixed (A10).

Sources: CPAT documentation, Mitigation chapter 3.2 (github.com/cpmodel/cpat_public); legacy workbook `CPAT 1.0pre_456_NoPropData.xlsb`, sheet `Mitigation` (rows 452/455 US deflator and CPI, 456/467/725 inflation indices, 633-695 international prices by source) and sheet `Prices_int` (regional assumptions); `coded/cpat_model/mitigation/prices/` (`prices.py`, `domestic_prices.py`, `international_prices.py`), which ports the legacy formulas line by line.

## 0. Assumptions: what the numbers mean

| # | Assumption |
|---|---|
| A1 | **Every price, tax and policy value is in real US dollars of the results year** (ScenarioDefinition `ResultsYear`, 2026, from scenario 1), per GJ. A constant real price is a constant number. There is no inflation after the conversion, and fuel use responds only to real price changes. |
| A2 | **Two indices, both 1 in the results year.** The CPI index (US CPI of the results year / of the year) converts nominal *domestic* values; the deflator index (US GDP deflator, same form) converts nominal *international* prices. This is the legacy split (CPI rows 456/725, deflator row 467; row 630 is its reciprocal). Up to 2030 they differ by up to 1.2% (2022: 1.137 vs 1.124; 2030: 0.918 vs 0.929), so one index would not reproduce legacy. |
| A3 | **Domestic price data are nominal USD of their own year** (IMF price dataset, `Prices_dom`: supply cost, excise and other taxes, retail price). Each is converted with that year's CPI index and divided by GJ per price unit. Units: $/liter for gasoline, diesel, LPG and kerosene; $/bbl for other oil products; $/GJ for coal, gas and biomass. |
| A4 | **Forecasting coefficients are base-year (2022) nominal values**: the margin over international prices and the domestic production cost. They are converted with the 2022 CPI index and held constant in real terms. (`coded` applies no conversion here; to check against legacy in bucket 5.) |
| A5 | **International prices are nominal by source** (IMF, WB, IEA, EIA, averages, Manual: IMF to 2025, then sheet `Manual inputs` D221:AF225 at the legacy addresses, by label and year), converted with the deflator. Only their year-on-year ratio moves the supply cost, so their units and level drop out. Beyond a source's horizon the data hold them constant in real terms. |
| A6 | **ScenarioDefinition policy inputs are real (results-year USD)**: the carbon price, feebate rates and fuel price reform increases (in price units, e.g. $/liter real). Only the carbon price has a nominal option: `NomorReal` = Nominal makes the path nominal, then multiplied by the CPI index (legacy row 2249). |
| A7 | **History vs projection.** Prices up to the last historical price year (Settings C10; default 2022, as legacy) come from data; later years are projected. Fuel use is data in the base year (2022) and modelled from 2023. The IMF dataset also holds 2023-2024; setting C10 to 2024 uses them (issue I4). |
| A8 | **Global vs per scenario.** Global (Settings, ScenarioDefinition scenario 1): results year, government price controls (pass-through), last historical year, the country's gas market. Per scenario: international price source and High/Low adjustment, carbon price and its nominal/real switch, fuel price reform, feebates, coverage. |
| A9 | **Horizon.** Values after 2030 are not compared with legacy. The legacy CPI is held flat after 2031 (WEO horizon), the deflator is not, and some legacy rules (A10) misbehave over long horizons. The model computes to 2041 (the legacy horizon of the power block), but 2031-2041 are not a target. |
| A10 | **Legacy rules are copied as they are, except the bugs.** v4.10 (user rule: bugs are never replicated): legacy bug L14 is fixed: with pass-through 0.5 or 0.8, legacy's other taxes jumped in the first projected year (the floating subsidy multiplied by (1 - pcc) a second time); the prototype applies (1 - pcc) once (no effect for Egypt, pass-through 0 or 1). **Changed (user decision): other oil products are treated like the other oil products**, taking pass-through and margin from the dataset (Egypt: 0 and 7.95 $/bbl) instead of the legacy hardcodes 1 and 0. Under the legacy rule their retail price fell with the oil price to the 0.01 floor (3.79 $/GJ in 2024, 0.23 in 2030), and their fuel use rose 10x by 2030. |
| A11 | **VAT rate (user decision).** Use the dataset's VAT rate where it is filled. Otherwise use the country's general VAT rate (Egypt 14%) for residential coal and gas and the all-sector oil products (gasoline, diesel, LPG, kerosene, other oil products), and 0 for power, industry (VAT is credited to firms) and biomass (largely informal). For Egypt the dataset's own retail prices imply exactly this: rp = (sp + txo) x 1.14 for residential gas and the oil products, and rp = sp + txo for power and industry. So historical oil-product retail prices equal the dataset's (14% higher than without the rule), and new policies pay 14% VAT in those sectors. |

## 1. Dimensions and units

- Prices are kept by **fuel x price sector**, as in the IMF dataset: 12 price fuels, namely coal and natural gas for power, residential and industry; gasoline, diesel, LPG, kerosene, other oil products and biomass for all sectors. Electricity is left to the power module. Subsectors take the price of their price sector (road and residential use the residential coal and gas prices).
- All in real $/GJ of the results year (A1-A3).

## 2. International prices `gp`

`gp_t` = international price of the source and commodity x deflator x adjustment factor.

- Source: ScenarioDefinition `IntEnerPricForeSource`, asterisk dropped (`IMF-WB*` = average of IMF and WB).
- Commodity: crude oil (gasoline, diesel, LPG, kerosene, other oil products); coal; gas of the country's market (Egypt *Global* = average of LNG, North America and Europe); a flat 1 (biomass).
- Factor (ScenarioDefinition `IntEnerPricForecastAdjustment`): *Base* = 1; *High* / *Low* = 1.5 / 0.5 for oil and 1.25 / 0.75 for gas and coal, after the last historical year.

## 3. Supply cost `sp`

Data up to the last historical year L; then `sp_t = fixsp + (sp_{t-1} - fixsp - ps_{t-1}) x gp_t / gp_{t-1} + ps_t`: a fixed part, a part that floats with the international price, and the existing producer subsidy `ps` (block row `psp`, $/GJ; legacy `sp = fixsp + fltsp + ps`, rows 2455-2708; v6.1, I49). The producer subsidy phase-out is not in `sp`: it is a separate new-policy wedge (section 6b; v6.2).

`fixsp = (margin + bucketed pass-through x production cost [coal, gas]) x CPI index(2022) / GJ per unit`. The margin of biomass is 0 (legacy hardcode; other oil products from data, A10). Producer subsidies enter through `ps` (section 6b; 0 for Egypt).

## 4. Excise and other taxes `txo` (pass-through)

- Pass-through `pcc`: raw = the dataset's base-year value (blank = 0; biomass = 1; other oil products from data, A10). Bucketed: <= 0.25 -> 0, <= 0.5 -> 0.5, else 1. Settings `GovPriceControls` chooses *Bucketed* (default), *Manual* or *None* = 1. *Manual* takes the retail price control (pass-through) of the block from sheet `Manual inputs` J167:J180, the legacy addresses, by the code in column G (`mit.rp.<fuel>.<sector>.ctrl`; legacy default 0.8 for every block); a blank cell gives 1, as legacy rows 747-760. The electricity rows (J178:J179) are not read: electricity prices come from the power section. Egypt bucketed: coal 1, gas 0, oil products incl. other oil products 0, biomass 1.
- Historical `txo` (as legacy): coal, gas and biomass `rp / (1 + vr) - sp`; oil products the dataset's `txo` (legacy builds their retail price as `sp + txo`, times `(1 + vr)`).
- Projected: `txo_t = txo_L x pcc + cs_t`, with the floating subsidy `cs_t = (sp_L - sp_t + txo_L(1 - pcc)) x (1 - pcc)`, and `cs_t` not below `txo_L(1 - pcc)` when that is >= 0.
- pcc = 1: supply-cost changes are passed on in full. pcc = 0: the retail price before new policies stays at its value in L, and the floating subsidy absorbs the change.

## 5. Retail price before new policies `rpb` and the after-tax price `atp`

`rpb = (sp + txo) x (1 + vr)`, with `vr` the VAT rate of L (A11). For gasoline, diesel, LPG and kerosene `vr` is the VAT rate x the household share of the product (sheet `OilProductShares`; Egypt: gasoline 1, diesel 0.03, LPG 0.99, kerosene 0.39), as legacy rows 797-816: VAT is charged on the household part only, firms reclaim it (v4.12, LD5; issue I39). Other oil products and the other fuels take the full rate, as legacy.

By subsector: `atp = max(rpb + (nce + xcpd) x (1 + vr), 0.01)`. New policies (`nce` = new carbon tax + new ETS cost + new excise) are passed through in full and pay VAT (legacy `vat = (sp + txo) x vr` with `nce` inside `txo`); `xcpd` is the change in existing carbon pricing (section 5b). The 0.01 floor is legacy's.

**Residential LPG and kerosene always exempted** (ScenarioDefinition `AlwaysExemptResLPGKer`, row 268, by scenario; default No*; legacy rows 5546-5547). If the switch starts with "Yes" (Yes or Yes*), the new carbon tax, the new ETS cost and the new excise of the residential LPG and kerosene rows are 0: each is multiplied by the exemption factor of Section-1 rows `exf` (`exf.all` = 1, `exf.res` = 0 if Yes), at the row's position in Inputs column `exg` (2 for residential LPG and kerosene, 1 elsewhere). Their `nce` is then 0, so `atp = max(rpb + (xcpd + csw + pcw) x (1 + vr), 0.01)`: no new policy and no VAT on it, while existing taxes, the change in existing carbon pricing and the subsidy phase-outs stay, as legacy (row 2651, the price before new policies). The shadow price `shp` is not exempted, as legacy. The new-policy revenue of these rows (`rnew`, the excise revenue `rex` and the VAT on the new policies in `rvt`) is 0 with the price. ETS-covered emissions still count them where the residential sector is in an ETS. The residential leakage to biomass reads the row's own `nce`, so an exempt fuel does not leak (`Equations.md` 4a).

### Layout of a price block and the price incl. new policies by block

Each fuel | sector block of section 2 reads: settings (italic: parameter row, international reference price `gpi`, fixed supply cost `spf`, existing subsidy per price unit `esubpu`); the **full retail price `rpn`** (bold); the build-up `sp`, `txf`, `txo`, `etx`, `esub`, `vat` ending with `rpb`; then the new taxes and subsidies.

New policies act by subsector (sections 5-8). The block shows them as averages over the subsectors priced by the block (the `atp` rows whose D is the block position), weighted by their fuel use `ener`:

- `pnq = sum of ener` over those subsectors (ktoe);
- `pctx`, `pets`, `pntx`, `pxcd` = fuel-use weighted averages of `ctxnew`, `ets`, `ntx`, `xcpd`;
- `rpn = sum(atp x ener) / pnq` (`rpb` where `pnq = 0`);
- `pnce = rpn - rpb`, the total new policy; `pvatn = pnce - (pctx + pets + pntx + pxcd)`, the VAT on the new policies (and the 0.01 floor).

These are weighted averages with each scenario's own quantities, not price indices; price changes between scenarios are the indices of section 7.

## 5b. Existing carbon pricing

Legacy CPAT adds existing carbon taxes and ETS from its sheet `ECP` (WB Carbon Pricing Dashboard, ICAP; as of 1 April 2025) as parts of `txo` (Mitigation rows 1675-1764). Since v4.12 the prototype follows legacy with several schemes (user decision 2026-10-18; was issue I7), with legacy bugs L61-L65 fixed. It differs in how the level enters: the IMF retail prices already contain whatever existing carbon pricing a country had, so only the change against that level enters (below); legacy subtracts the same level from the fixed part of `txo`, which gives the same numbers.

- **Data** (sheet `ECP` at its legacy addresses, 52 countries; Egypt has none). Each code is looked up in its own legacy block (sheet `Inputs_ecp`, columns K:L give the block's first and last row):
  - carbon tax: single rate `ecr.all`, fuel rates `ecr.<fuel>`, sector coverage `ecs.<sector>`, fuel coverage `ecf.<fuel>` (rows 69-559);
  - national ETS: price `eer.all`, coverage `ees`, `eef` (rows 600-615, 619-737, 1040-1093);
  - regional EU ETS: the EU price (row 616) and the country's regional coverage (rows 738-1036, 1094-1223), where the country's "EU ETS?" flag (general information, column K) is Yes or Both (legacy row 1695).
- **Prices** in real USD of ResultsYear (nominal x CPI index). **Coverage** of each data year (2021-2025; blank = 0, as legacy), the last data year after.
- **Carbon tax rate by fuel** (legacy rows 1752-1764): the fuel rate where the country has one and no "single price" flag (general information, column E), else the single rate.
- **Sector of a price**: the ECP sector of the price fuel, as legacy: coal and gas by their price sector (power, residential, industry); oil products, biomass and jet fuel transport; other oil products industry (power: power).
- **Tables** (sheet `Inputs_ecp`), by ECP sector | fuel and data year, $/tCO2: carbon tax = rate x sector coverage x fuel coverage; ETS = national price x its coverage + EU price x the regional coverage (the two schemes add up, as legacy).
- **Scenario factors** (section 1, ScenarioDefinition): `xct.p` = 1 if `ExistingCTApply` = Yes, x (1 + `ExistingCTGrowth`)^(years after the last data year), else 0; `xets.p` the same with `ExistingETSApply`, `ExistingETSGrowth` (legacy grows the EU ETS with the carbon-tax growth: bug L61). `xct.c` is the data column of the year.
- **Per subsector and fuel**: level `xcp` = EF x (carbon tax x `xct.p` + ETS x `xets.p`) ($/GJ); change `xcpd` = the level minus the level embedded in the price data (`xcp0`, Inputs: the tables in the last historical price year L). Only the change enters the after-tax price, so a country's history is not counted twice: switching a scheme off lowers the price by its embedded level; growth or new data raise it.
- **Power**: the same change per kWh (row pow | fuel of the tables) is part of the variable cost before new policies, so dispatch, investment and electricity prices respond.
- **New carbon tax**: if `CTaxComplimentaryToETS` = Yes (legacy rows 2270-2288), it covers 1 - the national ETS sector coverage of the year (legacy: of the previous year, bug L65). Otherwise new instruments add to existing ones.
- **Revenue**: existing-tax revenue includes `xcpd x (1 + vr)`; a memo shows the level, fuel use x `xcp`. Existing ETS revenue is valued at the full permit price, as legacy; legacy's free-allocation and revenue data (ECP rows 560-597, 1225-1322) are not used in legacy's model either.
- **Legacy bugs fixed** (register): L61 (EU ETS growth), L62 (transport diesel, LPG and kerosene take the rate row as coverage), L63 (fuel coverage lookup stops at row 403 of a block that ends at 425), L64 (no ETS on other oil products outside power), L65 (complementary tax with last year's coverage).

## 6. Existing taxes and subsidies

Per price fuel and year, real $/GJ:

| Item | Formula | Use |
|---|---|---|
| VAT | (sp + txo) x vr | VAT before new policies (revenue) |
| Existing excise and other taxes | max(txo, 0) | revenue |
| Existing consumer subsidy | min(txo, 0) | negative (subsidies are negative) |
| Subsidy per price unit | subsidy x GJ per price unit | in ScenarioDefinition price units ($/liter, $/bbl, $/GJ), for a later per-fuel subsidy reform through the fuel price reform inputs, which use the same units |

Legacy splits `txo` into a fixed tax, a fixed subsidy and a floating part; the sign split gives the same totals. VAT on oil products is (sp + txo) x rate x household share; legacy divides the retail price by 1 + the full rate (bug L60). Revenue, as fuel use (PJ) x the rate: existing taxes = excise + VAT + `xcpd x (1 + vr)`; existing subsidies = the subsidy (negative); net existing = taxes + subsidies; new = new carbon tax + new excise + ETS x revenue factor + VAT on new policies. Power adds its rows (`PowerPrices_Method.md`).

## 6b. Subsidy and price-control phase-outs, producer subsidies (v4.16; LD18, LD19)

User decision 2026-10-18: separate policy lines by sector and fuel, not meshed with the pre-policy price build-up. `sp`, `txo` and `rpb` are unchanged; the reforms are wedges added to the after-tax price, like the new policies.

- **Factors (section 1, legacy rows 2211-2218).** One per phase-out: producer subsidies (ScenarioDefinition 123-129), consumer subsidies (131-137) and price controls (191-195). Scenario 1 reads the baseline switch, period and share; other scenarios the policy switch and period, with share = MAX(baseline, policy) (legacy rows 264-274). The price-control phase-out applies if its switch is on and the scenario is a policy scenario or its baseline switch is on, and it takes the consumer share (as legacy: issue I48). Factor `pof` = MAX(1 - share, 1 - share x (year - start) / period after the start year): the share of the original kept, the same year for every line (legacy lags the fixed subsidy a year: bug L81).
- **Lines by price fuel | sector.** `csf.<block>` = 1 - `csi` x (1 - factor), `pcf.<block>` likewise with `pci`; the inclusion switches `csi`, `pci` (sheet Constants, default 1 for every block, as legacy) let a reform cover some fuels and sectors only. Producer subsidies by fuel (coal, gas, oil, biomass, electricity): `psi`, `psf`.
- **Split of `txo` (each price block).** Fixed part `txfx` = pass-through x `txo` (history: of the year; projection: of the last historical year); floating part `txfl` = `txo` - `txfx` (it absorbs the supply-cost changes not passed through). As legacy rows 2597-2599.
- **Wedges (each block, $/GJ before VAT).** Consumer subsidy reform `pcsw` = -(1 - `csf`) x MIN(`txfx`, 0): only a fixed subsidy goes (legacy: the fixed subsidy x factor). Price-control phase-out `ppcw` = -(1 - `pcf`) x `txfl`: the floating part goes, subsidy or tax (legacy row 2599). For Egypt every subsidised fuel has pass-through 0, so only the price-control phase-out removes subsidies, as in legacy.
- **Subsectors.** `csw`, `pcw` = the wedges of the subsector's block; `atp` = MAX(`rpb` + (`nce` + `xcpd` + `csw` + `pcw`) x (1 + vr), floor). Revenue `rsr` = fuel use x PJ/ktoe x (`csw` + `pcw`) x (1 + vr): the subsidy saved plus VAT on it (section 12; 12e books it under existing taxes and subsidies, its VAT under VAT). `rnet` stays the pre-reform existing revenue.
- **Producer subsidies (fiscal line).** `pros.<fuel>` = Prices_dom `mit.pros.<fuel>.all` (USD bn nominal) x CPI factor, held after the last price year; `rpsu.all` = -SUMPRODUCT(`pros`, `psf`) in section 12 (negative = cost), in the total revenue and the fiscal space; 12e producer subsidies = the electricity subsidy gap + `rpsu`. **Price effect (v6.1, I49, as legacy rows 825-829):** section-1 rows `psd.<fuel>` hold the demand that carries the subsidy: oil, world demand x liters per ktoe (legacy `_conv_ktoe_liter_oil` = 1,108,792); coal and gas, the average of world demand and domestic consumption (EnergyCons, excluding electricity and heat) x GJ per ktoe; biomass, domestic consumption x GJ per ktoe. `psu.<fuel>` = -`pros` x USDperM / `psd` up to the last price year, then held: the existing subsidy. Each price block reads the `psu` of its fuel by its international price position (G) into `psp` ($/GJ: x liters per barrel for other oil products, / GJ per price unit), which stays in the supply cost and so in the price before new policies `rpb`.

**Producer subsidy reform (v6.2, user rule 2026-10-20: subsidy reforms are always separate from the before-tax build-up).** `psr.<fuel>` = -`psu` x (1 - `psf`) (legacy: the base value x the phase-out factor, row 2213). The block wedge `ppsw` = `psr` of its fuel ($/GJ as `psp`) x the block's pass-through `pcc`, beside the consumer subsidy and price-control wedges `pcsw` and `ppcw`; the subsectors read it as `psw` into the after-tax price (`atp` = `rpb` + (new taxes + `xcpd` + `csw` + `pcw` + `psw`) x (1 + VAT)), and the VAT on it is in the subsidy-reform revenue `rsr`. Legacy puts the phase-out into the supply cost, where the price controls absorb (1 - `pcc`) of it; the wedge x `pcc` gives the same price except where the excise floor binds. Legacy bugs fixed: L124 (residential gas read the oil value) and L125 (other oil products added a per-liter value to a per-barrel price). Egypt: no producer subsidy data (0).
- **Not yet:** electricity consumer subsidy phase-out (PowerSubsidyExemptInclude, default DoNotPhaseOut) and the electricity producer subsidy in the power price: with the power features (legacy bugs L83, L84 to fix then).

## 7. Average prices and price indices (memo at the end of section 2)

The memo summarises the after-tax prices including new policies (`atp`, sections 5-8; electricity `rp`, section 3). There is one block per fuel, one for electricity and one for all energy. Sums run over the 16 subsectors; electricity runs over the residential and industry price groups.

| Row | Formula | Meaning |
|---|---|---|
| `pav.sp` | Σ p·q | Spending, own quantities |
| `pav.q` | Σ q | Fuel use |
| `pav.uv` | Σ p·q / Σ q | Average price (unit value); legacy F5b |
| `pav.spr` | Σ p·q₁ | Spending at scenario 1 quantities of the same year |
| `pav.las` | Σ p·q₁ / Σ p₁·q₁ | **Price index against scenario 1** (Laspeyres; scenario 1 = 1) |
| `pav.sp0` | Σ p·q₀ | Spending at base-year quantities |
| `pav.time` | Σ p·q₀ / Σ p₀·q₀ | **Price index over time** (base year = 1) |
| `pav.mix` | (uv / uv₁) / las | Mix effect: what the unit-value ratio adds to the price index |
| `pav.leg` | see below | **Average price as legacy F5b** (v4.15, I31) |
| `pav.lidx` | leg / leg₁ | Legacy average price against scenario 1 (fuels without a legacy average: `pav.las`) |
| `pav.idx` | Settings C54 | **Price index reported** (LiveOutputs `mit.pav.idx`): Legacy* = `pav.lidx` (default), Laspeyres = `pav.las` |

Legacy averages (v4.15, issue I31, user 2026-10-18: legacy as the default; legacy rows 16293-16405): coal and gas average the prices of power generation, residential and industry (section 2 blocks `.res`, `.ind`: `rpn`; power: the pre-policy price `rpb` of `.pow` plus the policy cost per GJ of the power type, `pavl.pp`) with the scenario-1 quantities of the same year (residential subsector `pavl.qr`, the 8 industry subsectors `pavl.qi`, power generation `pavl.qp`): a Laspeyres index on three sectors. Electricity averages residential and industry with each scenario's own consumption (= `pav.uv`). Oil products take the single price of their `.all` block. Biomass, jet fuel and all energy have no legacy average: their reported index is the Laspeyres one. Legacy bug L77 fixed (its index rows read the wrong fuels).

Notes on the rows:
- **Subscripts.** ₁ is scenario 1 in the same year; ₀ is the base year. Base-year quantities and prices are data, so they are equal in every scenario.
- **Unit-value ratio = price index × mix effect.** Legacy reports the unit-value ratio as the price change (issue I31); here the two parts are separate.
- **All energy.** Spending is in USD million: fuel spending × PJ per ktoe, plus electricity spending (USD/kWh × GWh). Fuel use is in ktoe, with electricity converted (GWh × GJ per kWh / PJ per ktoe).
- **Electricity.** Units are USD/kWh and GWh.
- **Lookups.** Header row 10 gives the position of scenario 1's column for each year, so the scenario-1 quantities are a lookup (`INDEX(...,0,row 10)`).

## 8. Left out (later steps)

- Electricity subsidy phase-outs (power features).
- The Europe shift to LNG.
- Ad-valorem baseline taxes (Egypt: Fixed).


## Europe gas market: shift to LNG (v5.6, LD20)

For countries in the European gas market, the international gas price is Europe x (1 - s) + LNG x s, with s the share of gas from outside Russia (Inputs_pint row 3: 0.58 in 2022, 0.603 in 2023, 0.734 in 2024, 0.834 from 2025; legacy rows 699, 706), series nga.eus by source. Legacy reads a per-country ad-valorem flag for baseline taxes (Prices_int H, Mitigation F77) but no formula uses it: taxes are fixed in both.
