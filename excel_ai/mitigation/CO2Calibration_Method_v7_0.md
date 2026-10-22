# Calibration of energy CO2 to the GHG inventory: method (CPAT-AI-Mitigation-MVP v6.4)

Equations: `Equations_v7_0.md`; workbook formulas: `Formulas_v7_0.md`. Decision and numbers: `Old/Calibration_Plan_v3_6.md`.

## 1. Method

Every CO2 emission factor (EF), by subsector and fuel and by generation type, is multiplied by one factor, `EFCalib`. **Since v4.11 this is legacy's rule (user decision 2026-10-18: go with legacy; issue I32 replicated)**: legacy Mitigation rows 623, 839 and 976-977.

`EFCalib` = inventory energy CO2 of the year before the base year / scenario-1 energy CO2 of the base year with uncalibrated EFs (the base-year energy balance x the EFs); 1 if the switch is off. **The switch is Settings C27, Yes by default**, as legacy (EFsAdjustmentAnnexI and EFsAdjustmentNonAnnexI are both Yes*). With the shipped data (Egypt): 2021 inventory 211.05 Mt against the 2022 estimate 226.97 Mt, **EFCalib = 0.930** (legacy: 0.930).

The uncalibrated scenario-1 CO2 is data written by the build, like the ETS baseline: a live formula would be circular (EFs feed carbon prices, which feed fuel use). Scenario-1 fuel use does not depend on the EFs in value (no new carbon price; existing carbon pricing changes only after the historical years), so the calibrated baseline is the uncalibrated one times the factor. The rows are keyed by country (`EGY|raw`, `EGY|pow`, ...), so another country finds no rows (#N/A) rather than Egypt's: rebuild with its code (about 2 minutes since v4.9), or paste its scenario-1 values under its key.

Everything downstream follows: CO2 by subsector, fuel and power type; carbon tax, ETS cost and existing carbon pricing per unit of fuel and their revenue; the ETS baseline; energy CO2 in the GHG totals. Scenario-1 fuel use and prices do not change. In policy scenarios, carbon prices per unit of fuel are 7% lower for Egypt, so fuel use, revenue and the GDP effect change.

## 2. Results for Egypt (scenario 1, energy CO2, Mt; v4.11)

| Year | Inventory | Uncalibrated | Calibrated (x 0.930) |
|---|---|---|---|
| 2022 | 252.2 | 227.0 | 211.1 |
| 2023 | 267.4 | 196.7 | 182.9 |
| 2024 | 285.3 | 218.9 | 203.5 |

The calibrated base year equals the 2021 inventory (211.1), as legacy. Egypt's inventory jumps 19% from 2021 to 2022 (register I17), and legacy's rule carries that break into every year: calibrated CO2 is 16-29% below the 2022-2024 inventory. The 2023 dip is the fuel-use shock of legacy row 483 (I22, replicated).

## 3. Differences with legacy (sheet LegacyDiff)

- **Year and switch**: as legacy since v4.11 (before: the last inventory year GHGYear and the switch off, user decisions v3.2 and v3.4).
- **Switch**: legacy reads one switch for Annex I countries (ScenarioDefinition row 237) and another for the others, both Yes*; the MVP has one switch on Settings (C27), Yes.
- **Scope**: inventory energy CO2 includes fugitive CO2 (7.1 Mt in 2024), which the model does not compute separately. The factor absorbs it, as in legacy.
