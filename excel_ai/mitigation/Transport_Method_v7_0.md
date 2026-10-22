# Road transport, engineer model: method (CPAT-AI-Mitigation-MVP v6.4)

Equations: `Equations_v7_0.md` section 4b; workbook layout and names: `Transport_Workbook_Notes_v7_0.md`; bugs fixed and decisions against legacy: `Transport_vs_Legacy_v7_0.md`; the legacy model: `Transport_Legacy_Survey_v7_0.md` and `Transport_Reference_Notes_v7_0.md`.

## 1. What it is

The "technoeconomic" road model of legacy CPAT and of the methodology note (`data/source/Transportation_methodology.docx`). It projects road vehicles, distance driven, fuel economy and energy use from vehicle economics, instead of the single fuel-use equation of the elasticity approach.

- **Vehicle classes:** passenger and light vehicles (new and used), freight trucks and 2-3 wheelers; buses follow passenger vehicles.
- **Powertrains:** gasoline, diesel, LPG and CNG/LNG; PHEVs (passenger); BEVs.
- **Fuels covered:** road gasoline, diesel, LPG, natural gas and electricity; road biofuels follow them as legacy (v4.12, LD62): bioethanol and other biofuels with gasoline, biodiesel with diesel (base year x use / base-year use). The vehicle feebate's CO2 per liter of gasoline and diesel is scaled by their fossil share in the base year (legacy E2146:E2147; issue I40, replicated). Coal, kerosene and other oil products in road, and rail, aviation and navigation, stay on the elasticity approach.

**Switch:** ScenarioDefinition `TrModel` (legacy row 340), per scenario.
- **Elasticity (default):** results are exactly those of v3.4.
- **Engineer:** section 5b replaces road gasoline, diesel, LPG, gas and biofuels in section 5 in every year. Road electricity feeds power demand from the year after the base year. CO2, revenues, methane, air pollutants and the totals follow.

Section 5b is computed in every scenario either way, so the two approaches can be compared side by side.

## 2. How it works (one year at a time)

1. **Vehicle demand:**
   - **Passenger ownership** per 1,000 people follows a Gompertz curve in GDP per capita. Its saturation level comes from the data, and it adjusts partially each year, with limits on annual growth and decline.
   - **Calibration** scales the curve to observed ownership in the last data year, up or down.
   - **Freight and 2-3 wheelers:** freight ownership is an income-dependent share of passenger ownership; 2-3 wheelers follow a hump in income.
2. **Stock:** vehicles retire at 1/lifetime of the trailing-average stock. Purchases are demand minus the remaining stock, split between new and used vehicles by the used share.
3. **Total cost of ownership (TCO) per km, ICEV and BEV:**
   - **Purchase price** after customs, ad-valorem tax, VAT, feebates and EV subsidies.
   - **Depreciation and resale value, insurance and maintenance.**
   - **Fuel or electricity:**
     - retail prices incl. carbon tax and fuel reform;
     - EV electricity at last year's power price plus a charging mark-up that falls with EV penetration.
   - **Distance tax.**
   - **Range anxiety for BEVs:** it falls as charging stations grow; charging stations grow with the BEV stock and with charging subsidies.
   - **Discounting:** at a consumer discount rate that falls with income.
4. **Choice:**
   - **EV share of purchases:** a logit in TCO per km, separately for new and used passenger vehicles, freight and 2-3 wheelers.
   - **Fuel split among ICEVs:** own- and cross-price elasticities of TCO.
5. **Fuel economy:**
   - **New vehicles:** improves autonomously and with the fuel price (incl. the feebate per liter).
   - **Stock:** turns over with purchases.
   - **Distance per vehicle:** responds to the cost per km and to income.
6. **Fuel use:** vehicles × distance / fuel economy, by class and fuel, in two calibration steps to the base-year energy balance:
   - distance factors by class;
   - then a residual factor by fuel.
7. **Buses:** base-year bus fuel scales with passenger fuel use by fuel; bus electricity scales with passenger electricity.

**Policies:** all are scenario rows on ScenarioDefinition (rows 418-479), off by default:
- carbon tax, fuel price reform and existing taxes (through the retail prices);
- feebates by class (rate per t CO2, pivot);
- distance tax;
- EV purchase subsidy;
- ad-valorem purchase taxes;
- VAT and customs on BEVs;
- charging-station subsidy.

## 3. Data (all countries, looked up by the country code)

| Workbook sheet | Content | Source |
|---|---|---|
| Transport1 | 220 countries, 2022-2025: fuel shares by vehicle type, fuel economy, ownership, EV shares, distance, used share, duties, charging stations, ownership saturation | Legacy Transport1 (`data/transport_data.csv`) |
| Transport2 | ICEV and EV purchase prices by class, 2022-2040 | Legacy Transport2 (`vehicle_prices.csv`) |
| Transport3 | Range anxiety by class (stored solver results), 194 countries | Legacy Transport3 (`range_anxiety.csv`) |
| TransportParams | Lifetimes, depreciation, insurance, maintenance, elasticities, logit k, Gompertz and ownership limits, charging parameters; the methodology note's alternative values (not used) | Legacy side tables and Dashboard (`transport_params.csv`) |
| Manual inputs J374:AC377 | BEV fuel economy of new vehicles (km per kWh; passenger / light, freight, 2-3 wheeler; 2022-2041), read by label (D375:D377) and year (row 374) in rows `trfen` | Legacy Manual inputs, same addresses (paste the legacy tab from row 3) |
| TransportPaths | BEV fuel economy of the stock (light, freight, 2-3 wheeler), charging cost per port | Legacy Mitigation rows 2051, 2095, 2122, 2170 (`transport_paths.csv`) |

Data come from `extract_transport_v7_0.py`, which reads the legacy workbook.

## 4. Results for Egypt (engineer model switched on, check scenarios 11-15)

| 2035 | Road fuel use (ktoe) |
|---|---|
| Baseline (no carbon price) | 24,580 |
| Carbon tax (scenario 2 settings) | 22,564 |
| Carbon tax + EV subsidy, distance tax, feebates, charging subsidy | 14,177 |

- **EV subsidy:** raises the passenger EV sales share in 2030 from 0.55% to 3.3%.
- **Distance tax:** cuts passenger distance in 2035 from 285 to 183 billion km.
- **Size of the bug fixes:** the legacy engineer run, with its bugs, gives road fuel a third higher by 2035. The fixes are listed one by one, with their effects, in `Transport_vs_Legacy_v7_0.md`.

## 5. Caveats

- **Range anxiety** uses legacy's stored values, solved in another vintage. For Egypt the calculated 2025 passenger EV share is 0.09% against an actual 0.15%. A goal seek for the corrected model is open (the workbook reports the fit).
- **Calibration factors are large for Egypt:** passenger distance × 2.67, then gasoline × 1.23. The Transport1 data explain only part of road fuel use, so review the data.
- **Kept as legacy:**
  - freight distance in the TCO (Transport1 average, floored at 50,000 km);
  - the data years of vehicle VAT, customs and import shares.
- **Ownership decline:** at most 10% a year, a placeholder value.
- **Not built:** road externalities (legacy sheet Transport) and mode shift.
