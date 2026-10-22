# Data tabs of CPAT-AI-Mitigation-MVP v6.4: legacy order, legacy tables, all-country readiness

User request (2026-10-17): align the data tabs with legacy CPAT (grouped by module, legacy order, legacy names and
content where possible, without undoing principled decisions); check that the model would work with the full
all-country data; put every Egypt-only table alone on its tab or at the bottom; check how far the legacy data tables
can be copied in. Then (same day): align more fully, going with the recommendations. The norm is NORMS.md 1.5.

## Summary

- **Order.** The data tabs sit under the legacy dividers in legacy order: `DATA_MITIGATION->>`, `DATA_DISTN->>`,
  `DATA_TRAN->>`, `DATA_OUTPUT->>`; tabs without a legacy data tab come last under `DATA_OTHER->>` (BaselineCO2 only).
- **Copy-in rules (NORMS 1.5).**
  - **L, a single legacy table:** the table itself, unchanged (same columns, column letters and codes; header row 3,
    data from A4; a key formula column right of the table where legacy has no unique key). Paste the legacy data rows
    at A4. 17 tabs: Balances, EnergyCons, CH4Inputs, UNPop, OilProductShares (v4.12), WEO, EF_GHG, SCC, EF_PM,
    IO_GTAP, HHSurvey, HH_Elast, ASPIRE, WHOCooking, GDPRatios, Transport1, Transport2.
  - **A, a legacy tab with several tables:** kept at its legacy cell addresses from row 3 (rows 1-2: source line and
    title bar). Paste the legacy tab from row 3. 10 tabs: Countries, Elasticities, ETS+LTS, Multipliers, Prices_int,
    ECP, Transport3 (stored results, rows 5+) and, since v4.7, Power, CoC and GHGs (the inventory and, rows
    1201-1388, the 2023-2024 emission shocks of the power model).
  - **L*, Prices_dom:** legacy header rows and codes; paste legacy rows 4 onwards at A1.
- **Country selection is a data step (NORMS 1.5, rule 2c).** What legacy Mitigation computes from these tabs for the
  selected country sits in blocks of the Inputs tab, by formula, under the keys the model already used:
  - Inputs_ela: elasticities (the country's column of Elasticities, as legacy column G);
  - Inputs_mult: multipliers (median ± standard deviation by group, instrument and lag);
  - Inputs_macro: GDP growth and levels, deflators, exchange rate (WEO series with legacy's extension past the last data
    year, rows 417-467) and the energy trade balance and share traded (rows 741-743, from Balances);
  - Inputs_pint: international price series by source (rows 633-695);
  - Inputs_ecp: existing carbon pricing (rows 1675-1764; v4.12: carbon tax with single and fuel rates, national ETS and
    EU ETS, each code looked up in its own legacy block of ECP, coverage by data year, and two tables by ECP sector and
    fuel: carbon tax and ETS in $/tCO2);
  - Inputs_ef: CO2 emission factors (rows 980-1011);
  - v4.7, power (legacy section 4, rows 2954-4300): Inputs_pset (the power settings of ScenarioDefinition scenario 1 and derived
    values, each a defined name Ps...), Inputs_ptech (one row per generation type, the former PowerTech: country, else
    world parameters, efficiency and generation from Balances, WACC from CoC, capacity factors), Inputs_ppath (year
    paths, the former PowerPaths: capex time factors, storage, income factor, fuel price shocks, prices) and
    Inputs_ppar (parameters, the former PowerParams). The chains are mapped in `PowerData_Chain_v7_0.md`.
  The Egypt values reproduce legacy's cached values (macro series to 1e-15; power data to 1e-12), apart from one legacy
  bug fixed (L51: the coal trade balance was valued at the oil price) and one stale value in legacy's stored run (I38:
  the wind and solar capex time factors for 2039-2041 differ from the legacy Power cells they reference; the MVP
  follows the Power tab).
- **Proprietary tables.** The public legacy file (`CPAT 1.0pre_456_NoPropData.xlsb`) holds Egypt only in Balances,
  EnergyCons (empty), Prices_dom, EF_PM, IO_GTAP, HHSurvey, ASPIRE, WHOCooking, CalVal and Tran_Scatter. The model
  uses the first eight; all eight paste in directly.
- **All-country test: PASS.** `check_allcountry_v7_0.py` clones every Egypt row of every single-table tab under a dummy
  country (XEG) at the bottom of its table, renames Egypt's codes to XEG in place on the tabs kept at legacy addresses,
  selects XEG and recalculates: no error values, every output of Mitigation and Distribution identical to Egypt's.
- **No table from legacy's cached Egypt run is left (v4.7).** The former PowerTech, PowerPaths and PowerParams are
  computed from the legacy tabs on Inputs. BaselineCO2 (the scenario-1 CO2 the calibration uses) is derived by the
  build.
- **Legacy bugs in the power data: all fixed (v4.10, NORMS 0; v4.7 still copied them):** L52 every generation type
  takes the country parameters where they exist (Egypt: solar fixed O&M 11.831 instead of 15 $/kW/y); L53 the actual
  capacity factor of the base year (installed capacity, Power rows 358-1635) is used inside the CFOverride bounds (Egypt:
  gas 0.385, wind 0.436, solar 0.347, hydro 0.592; base-year gas capacity 52 GW instead of 35); L54 hydro invests from
  the base year only when its generation share is above 50% (Egypt: from 2030); L55 the country rows are looked up in
  the country block first (China, Japan, Korea); L56 countries without CoC risk data take the default WACC, flagged.
- Balances, EnergyCons, EF_PM, IO_GTAP, HHSurvey, HH_Elast, ASPIRE, WHOCooking and GDPRatios became legacy tables
  (v4.5). Then GHGs, CH4Inputs, UNPop, EF_GHG, SCC, Transport1 and Transport2 followed. The tables come
  from `extract_legacy_tables_v7_0.py`, which writes `data/mvp_legacy_extracts/legacy_<Tab>.csv` verbatim from the legacy file.
- Base-year fuel use and power demand now come from Balances through legacy's flow mapping (Mapping columns J-M), as
  legacy does with BalancesOrConsumption = Balances; the old PowerDemand tab was dropped.
- CO2 emission factors: the legacy EF_GHG table replaces the Egypt factors copied from legacy's run. The selection of
  legacy Mitigation rows 980-1011 is now a data step on Inputs, and it reproduces the Egypt factors exactly:
  - the country's code, else its World Bank region, else the world;
  - LPG and kerosene in power, and coal, LPG, kerosene and other oil products in road, take the row legacy points to;
  - jet fuel uses the IEA factor (EFJetIEA);
  - biomass is zero.
- GHGs: the legacy table adds Zimbabwe 2021 (legacy row 947). The previous extract stopped at row 946.
- All named ranges over data tables reach the capacity of the full legacy tables, with margin.
- v4.6: Countries, Elasticities, ETS+LTS, Multipliers, Prices_int, ECP and Transport3 became legacy tabs at legacy
  addresses (`data/mvp_legacy_extracts/legacy_<Tab>_cells.csv`), WEO the legacy table; the selections legacy makes for the country became
  the Inputs blocks above; the GHG inventory year and every other lookup are unchanged.
- v4.6 results against v4.5: unchanged except the coal trade balance (L51 fixed; external balance rows xtb, about
  0.6 bn USD a year for Egypt) and the base-year lagged GDP growth of the road model (trgdl, 2022: the WEO 2021 growth
  3.25 % instead of 0, transport bug B2 now fixed, as the builder intended; the old WEO copy had no 2021 growth).
- v4.7: Power, CoC and GHGs became legacy tabs at legacy addresses; the power data of the country (the former tabs
  PowerTech, PowerPaths and PowerParams, copied from legacy's Egypt run) became the Inputs power blocks, formulas only
  (country, else world parameters; efficiency and generation from Balances; WACC from CoC; capex time factors, storage,
  income factor, emission shocks; settings from ScenarioDefinition scenario 1). The values reproduce the former tables, except
  the wind and solar capex time factors for 2039-2041 (I38). Effect on Egypt's results: none before 2039; from 2039
  new capacity and investment of solar, wind and gas, then power fuel use and emissions (525 output codes; largest:
  new solar investment in the baseline, by up to 149 MW a year).
- Dropped in v4.7: PowerTech, PowerPaths, PowerParams (now Inputs blocks from Power, CoC, Balances, WEO, GHGs).
- v4.12: OilProductShares (legacy table, all countries; household share of diesel, kerosene, LPG and gasoline, and
  their road shares) after UNPop, as legacy. Inputs_prices multiplies the VAT rate of gasoline, diesel, LPG and
  kerosene by the household share, as legacy rows 797-816 (LD5, issue I39). Settings rows 46-51: the methane fee
  switches per source of legacy Manual inputs J196-J200 (LD46; since v5.2 on sheet Manual inputs, shown on Settings). Inputs columns efxs:eff (nearest GAINS factors, bug
  L59) and ecpk, xcp0 (existing carbon pricing), which replace ctc and etc.

## Manual inputs: the second input source, at the legacy addresses

Sheet `Manual inputs` (tab group INPUTS->>, after ScenarioDefinition) is the whole legacy tab of that name, rows 3-378 at their
legacy cell addresses (rows 1-2: source line and title bar), so the legacy tab pasted from row 3 replaces it. The cells
come from `data/mvp_legacy_extracts/legacy_ManualInputs_cells.csv` (`extract_legacy_tables_v7_0.py manual`): legacy values typed, light
green on the input cells. Legacy formulas within the sheet are kept (unit labels, the SCC path, the memo rows, the
residual of the PM2.5 apportionment); formulas that read other legacy tabs are replaced by the MVP equivalent (country
name and code, ScenarioDefinition scenario 1, the Elasticities tab) or typed as their legacy default value, and the note on the
block's title row (column J) says which. ScenarioDefinition stays the main input sheet (NORMS 4).

| Rows | Block | Read by the MVP |
|---|---|---|
| 5-15 | ETS: advanced parameters, sector inclusion, override price | E10:E12, the goal-seek settings (names ETSMaxIterations, ETSStartFreshContinue, ETSErrorTolerance; MVP values 20, Continue, 0.005; legacy 30, Continue, 0.001): macro SolveETS and `ets_goalseek_v7_0.py`. Not read: E7:E9, the inclusion rows and the override row, which the MVP holds per scenario (ScenarioDefinition rows 95-97, 99-115; row ets.ovr of each scenario group) |
| 18-47 | Process emissions (CBAM goods): coverage, emission factors, half elasticities | No: feature not built |
| 49-54 | Feebates: sector flags | No: ScenarioDefinition rows 66-82 per scenario |
| 57-146 | Domestic energy prices and taxes (manual) | No: feature not built (prices: Prices_dom) |
| 148-163 | Excise reform (additional excise) | No: feature not built |
| 165-180 | Domestic energy price controls | J167:J180 by code (names PCtrlKey, PCtrlVal): Inputs_prices column pcm, the pass-through when GovPriceControls = Manual (blank = 1, as legacy); electricity rows not read |
| 183-200 | Methane fee | J196:J200, the fee scope by source (names MFeeBio, MFeeDG, MFeeFF, MFeeAgr, MFeeWst; shown on Settings rows 47-51). Not read: J185:J194 (not built) |
| 202-215 | Imperfect pass-through (Distribution) | No: not built (legacy does not wire it either) |
| 218-225 | International energy price forecasts (manual) | J221:AF225 by label and year (names PIntManVal, PIntManLab, PIntManYear): Inputs_pint rows Manual from 2026, when IntEnerPricForeSource = Manual |
| 228-231 | GDP forecasts (manual) | No: feature not built |
| 234-240 | Social cost of carbon | Yes since v5.2: row 237 is the Manual option of NSCCSource / GSCCSource (legacy bug L103: legacy reads the path typed on Mitigation row 17683 and leaves this block dead) |
| 243-254 | PM2.5 source apportionment | No: feature not built |
| 257-269 | Fiscal multipliers | J261:U268 (names MultMan, MultManKey): Inputs_mult, when MultipliersSource = Manual |
| 271-327 | Elasticities and efficiency improvements | K326:M327, the non-energy GHG elasticities (names GhgElCat, GhgElPop, GhgElInc): section 14 rows ghg.dr and ch4.act. Not read: the manual energy elasticities (not built) |
| 330-340 | Additional mitigation effort (non-energy) | No: feature not built |
| 342-372 | New investments in power (manual capacity) | No: built later with the power features |
| 373-378 | Transport: fuel economy of new EVs | J375:AC377 by label (D375:D377) and year (names BEVFEVal, BEVFELab, BEVFEYr): section 5b rows trfen |

