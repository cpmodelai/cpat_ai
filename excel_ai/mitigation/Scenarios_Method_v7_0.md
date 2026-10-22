# Multiple scenarios: definitions, batch run, stored results, comparison (CPAT-AI-Mitigation-MVP v7.0)

Equations: `Equations_v7_0.md`; workbook formulas: `Formulas_v7_0.md`.

The model calculates two scenarios at a time: the baseline and one live policy scenario. A batch macro copies each scenario definition into the live scenario, calculates it and stores its results as values, which are compared afterwards. This follows legacy CPAT, where a macro copies each scenario column into the column used for calculation and stores the outputs.

## 1. Where things are

| Place | What it holds |
|---|---|
| ScenarioDefinition, scenario 1 | The **baseline**, stored once. |
| ScenarioDefinition, scenario 2 | The **live policy scenario**. The batch run overwrites it with each definition and restores it at the end. |
| ScenarioDefinition, columns to the right | **Scenario definitions**, one full ScenarioDefinition column each: short name (row 2, the legend in the charts), Run? (Yes/No), number (previous + 1), name, then the inputs. Red cells differ from the template. To add one, copy the last definition one column to the right and edit it. Blank columns are grouped and collapsed. |
| Mitigation, Distribution | Two scenario groups: 1 = the baseline (plain formulas), 2 = the live scenario (every calculated cell calls its named LAMBDA). More live scenarios: copy group 2 to the right and set its scenario number; LiveOutputs has room for 12 scenario blocks. |
| LiveOutputs | The key indicators of every scenario group, one block per scenario, found on Mitigation by output code. |
| StoredOutputs | Results as **values only**: the LiveOutputs indicators of each scenario, under its ID and output code (country.stem.ID). ID 1 is the baseline; a definition keeps its ScenarioDefinition number. Sorted by indicator, then ID (like variables together); every lookup matches the output code, so any order works. |
| ScenarioCompare | The **dashboard** and every user entry of the front: results from Live (LiveOutputs) or Stored (StoredOutputs), the year, the data source of the linked tables. Core buttons (green) and the others (grey); key results for one year of up to 10 scenarios against the baseline; a bar chart; time series with their chart beside them. |
| VBA module CPATScenarios | The macros below. The workbook is an .xlsm; the source is also in `CPATScenarios_v7_0.bas`. |
| MacroCheck | Report of the first-run test macro CheckBatchRun. |

## 2. Shipped definitions

| No. | Name | Inputs changed from the template |
|---|---|---|
| 3 | Carbon price $20/tCO2 from 2027 | The live scenario's settings |
| 4 | Package A: carbon tax to $50 by 2030 + feebates (transport, industry) | Carbon tax $10 (2027) to $50 (2030). Feebates 2027-2030: transport $10 → $50, industry $5 → $25. Feebate coverage adds road, mining & chemicals, and iron & steel |
| 5 | Package B: ETS on power and industry + carbon tax $25 elsewhere | Carbon tax $25 from 2027. New ETS from 2027: cap −5% (2027) to −20% (2035) of baseline covered emissions, constant afterwards. Template ETS coverage (power, mining & chemicals, iron & steel, non-ferrous metals, cement), default benchmarks and volatility |

Paths continue after their target year as set in the model: the carbon price follows its ScenarioDefinition switch, and feebates continue linearly.

## 2b. Main scenario choice and regulations as shadow prices (v4.16, LD9)

ScenarioDefinition row 13 (`ScenarioSelected`, " - Carbon tax" in every shipped scenario) picks a row of the legacy scenario table (legacy Mitigation rows 222-262, columns N:AC; sheet Mapping, block "Main scenarios"): whether the scenario prices carbon explicitly (legacy row 259), its efficiency adjustment (ScenarioDefinition rows 247-251) and the sectors its shadow price covers (rows 240-257).

- Explicit scenarios (carbon tax, total carbon price, coal excise, road fuel tax, electricity emissions tax and excise): the carbon price path of ScenarioDefinition rows 18-21 is the carbon tax (`cpx` = `cptraj`), as before.
- Shadow-pricing scenarios (feebates, power supply feebates, energy efficiency regulations, power feebate, vehicle fuel economy, residential and industrial efficiency regulations; and "Baseline"): no explicit carbon tax (`cpx` = 0); the carbon price path becomes a shadow price on the efficiency margin, `reg.<sector>` = `cp.shd` x the scenario's adjustment (energy efficiency 247, vehicle fuel economy 248, residential 249, industrial 250, feebates 251; Egypt 0.7, feebates 1) x 1 if the scenario covers the sector. It enters `shpx` (with the feebate part, now x row 251, and the ETS benchmark part), so fuel use responds through efficiency only, and power through `shk` (legacy bugs L87, L88 fixed: legacy's regulation share is 0 and never reaches power).
- The road vehicle feebate of the engineer road model adds `reg.rod` (the road regulation shadow price) instead of the carbon price, which is in the fuel price already (prototype bug M13).
- A text that is not in the table counts as explicit pricing (as the shipped " - Carbon tax").

## 3. Macros

Core buttons (green, on ScenarioCompare): **Recalculate now**, **Recalculation on/off**, **Run stored scenarios**, **Update data tables**. The others are grey, below them.

- **RunAllScenarios** (button Run stored scenarios): stores the baseline under ID 1 if none is stored yet. Then, for every definition with Run? = Yes, it copies the definition's inputs and name into the live scenario (skipping two formula rows), clears the ETS price override and recalculates, runs the ETS goal seek if the definition applies a new ETS without "Override ETS price" = Yes, and stores the live scenario's outputs as values under the definition's number and name (replacing that ID's rows wherever they are). At the end it restores the live scenario, the override and the calculation mode it found, sorts StoredOutputs, groups the blank scenario columns and refreshes the dashboard charts.
- **RecalculateNow**: full recalculation (timed), then the dashboard charts. The workbook ships with its values in manual calculation; **ToggleRecalculation** switches automatic calculation on or off (for every open workbook, as Excel does).
- **StoreBaseline**: replaces the stored baseline with the current scenario-1 results, after a confirmation.
- **StoreLiveScenario**: stores the live scenario as it stands, under an ID you choose (default: the next free ID from 100).
- **SolveETSLive**: ETS goal seek for the live scenario only. It fills the override prices and switches the override on.
- **ClearStoredScenarios**: deletes every stored scenario except the baseline.
- **SortStoredOutputs**: sorts StoredOutputs by code stem, then ID.
- **GroupBlankScenarios**: groups and collapses the scenario columns of ScenarioDefinition that have no name.
- **RefreshDashboard**: rebuilds the series of the dashboard charts from the scenarios with results in the chosen source (short names in the legend, baseline dashed grey, one colour per scenario slot) and hides the table rows of the others.
- **CheckBatchRun**: the first-run test (section 4). It reruns the batch, so the stored scenarios are recalculated by the application that runs it.

The ETS goal seek is legacy's damped log-space iteration, as in `ets_goalseek_v7_0.py`. It starts from the override prices, or from the fast estimate if there are none. Each step is p × (proposed price / p) ^ alpha, mixed 0.3 with the previous iterate, with 5% smoothing. Alpha halves when the error grows (minimum 0.0625) and rises ×1.2 when the error more than halves (maximum 1). It stops when the worst |covered / cap − 1| is below 0.5%, or after 20 iterations.

## 4. First run in Excel

The VBA project (written by `vba_project_v7_0.py`) and the stored results were produced without Excel. They are tested in LibreOffice: the module loads, the macros reproduce the Python emulation, and CheckBatchRun passes. To confirm the same in Excel:

1. If the file was downloaded, unblock it first (file Properties > Unblock), or Excel opens it with macros disabled.
2. Open it and choose Enable Content.
3. Run **CheckBatchRun** (Alt+F8); it takes a minute or two. It checks the 12 lookups the macros rely on (sheets, rows by code, scenario columns, LiveOutputs blocks); compares Excel's own recalculation of the baseline with the stored baseline (plain formulas only, so Excel and LibreOffice calculate it the same way); and reruns RunAllScenarios, ETS goal seek included, comparing every stored value with the value stored before.
4. MacroCheck shows **Result PASS** when no value differs by more than 1e-6 (relative). CHECK lists how many values differ; FAIL names the lookup that was not found.
5. If Excel cannot load the VBA project, or Alt+F8 lists no macros: remove the project if one is listed, import `CPATScenarios_v7_0.bas` (Alt+F11 > File > Import), save as .xlsm and run CheckBatchRun again.

## 5. Comparing and keeping results

- **Source and year.** On ScenarioCompare choose Results from (Stored or Live) and the year, then Recalculate now. Stored reads StoredOutputs (every stored scenario); Live reads LiveOutputs (the scenario groups of Mitigation: the baseline and the live scenario, and any group added by copy-paste). The names SCVal, SCCode and SCYear choose the range with CHOOSE; every value is `INDEX(SCVal, MATCH(country.stem.ID, SCCode, 0), year column)`, so the order of the rows never matters.
- **Scenario slots.** Up to 10, in ScenarioDefinition order: ID, short name (the legend), name. A scenario with no result in the chosen source shows blank (key table) or #N/A (time series, hidden by a conditional format, a gap in the charts); the charts leave it out.
- **Key table.** Energy CO2 emissions, GHG emissions excluding LULUCF, revenue as a share of GDP, the GDP effect of the revenue use and the net welfare effect: level, difference from the baseline, and % difference for the two emission levels. The bar chart beside it shows the % difference of energy CO2 by scenario.
- **Time series.** Four tables (default: energy CO2, GHGs, revenue, GDP effect), scenarios down and years across, each with its line chart beside it. The title of each table is a dropdown of the indicator list at the bottom of the tab: every LiveOutputs indicator except the price and Kaya indices.
- StoredOutputs holds values only, so results from other files can be pasted in as values under new IDs, as long as its column layout is kept (output code in column D).
- The baseline changes only when StoreBaseline is run.

## 6. Limits

- The batch run calculates one policy scenario at a time. Further Mitigation scenario groups (copies of group 2) show on the dashboard under Live; the batch macros use the live scenario (group 2) only.
- LiveOutputs (123 indicators, incl. power, fuel use and revenues with power, existing carbon pricing, GHGs, GDP effects) defines what is stored. To store more, add rows to the LiveOutputs blocks first.
