# Restructure the Excel-AI workbooks: lean modules plus a Master user guide (v1.2.0)

Agreed with the user on 2026-10-31. The work is done in stages, and each stage is committed and pushed before the next starts.

## A. Mitigation workbook: contents and grouping

1. Remove the tabs that belong to other modules:
   - Distribution: the `Distribution` tab and the `DATA_DISTN->>` group;
   - Transport: the `DATA_TRAN->>` group;
   - Air Pollution data.

   Keep every mitigation tab and every output tab, even if no formula reads it, and report which ones are unused.
2. Keep an `OUTPUT->>` group: MTOutputs, ScenarioCompare and Multipliers.
3. Put the interfaces to and from other modules (FromMitigation/exports, FromAirPollution, FromTransportCB) in a separate group, `OTHER MODULES->>`.
4. Split `Settings` and `Inputs` by role:
   - constants and mappings go to a new tab, `Constants and Mappings`;
   - anything a user may change goes into a new section of MTInputs.
5. Below the legacy table in MTInputs, group the extra settings into **New policies**, **Treatment of existing policies** and **Model settings**, in a logical order.
6. Data tabs: a dark-green bar at the top describes the tab, and each table has its own light-green header.
7. All tabs: consistent formatting, zoom set to 80%.

## B. MTOutputs and ScenarioCompare

1. MTOutputs takes the structure of Mitigation:
   - a scenario-number row at the top;
   - scenarios side by side, as many as Mitigation has scenario groups.

   Where the legacy MTOutputs column layout conflicts with Mitigation and Air Pollution, follow Mitigation and Air Pollution. Leave spare columns as white space on the left for graphs.
2. Remove the extra columns (calculation helpers, dashboard links, MTInputs echoes) and, for now, the comparison columns on the right. Apply the same clean-up to other tabs that have the same problem.
3. ScenarioCompare compares only active scenarios, read from MTOutputs. There is no stored option, so its formulas are simpler. Fix the blank column 2.
4. Move `StoredOutputs` out of Mitigation and into the Master. It does not have to keep its current form.

## C. Master workbook (`CPAT-AI-Master_UserGuide.xlsm`)

1. A short user guide to the modules. It is the **only workbook with macros**:
   - all VBA is removed from Mitigation, Distribution and Air Pollution, which become `.xlsx`;
   - the Master takes over activation, Update data tables, Update from Mitigation and scenario storage.
2. A version table showing each module's latest version and where to find it:
   - the GitHub link to the unactivated `.xlsx` in the main repository;
   - the path to the activated `.xlsb` in `active_workbooks/`.
3. A store of **10 scenario slots**, each with a name, date, module version and country. Results are pasted in as values from the modules, and the stored scenarios can be compared in the Master.
4. **Activation** (a macro), for each module:
   - open `_latest.xlsx`;
   - copy the 2035 formula column across to 2041 (baseline and policy);
   - recalculate fully;
   - save as `.xlsb` in `active_workbooks/`.

   Modules ship with formulas only to 2035.

## D. Storage

1. `_latest.xlsx` sits in each module's folder. The activated `.xlsb` sits in `active_workbooks/`. **Both are committed.**
2. NORMS records that the `.xlsb` is a generated file: on a conflict, take either side and regenerate it rather than merging.
3. The first `.xlsb` files come from the user running Activation in Excel. LibreOffice cannot write `.xlsb`.

## E. Data extraction (Power Query)

1. Add "All countries" to the country selector of the data refresh.
2. Move the biggest embedded tables to Power Query loading now. Candidates: EF_PM, Balances, CH4Inputs and WEO, confirmed by size.
3. These tables still ship as values in the `.xlsx`, so a module opens and calculates without a connection. The refresh replaces those values. Update NORMS to say so.

## F. Naming

1. New file names: `CPAT-AI-Mitigation_latest`, `CPAT-AI-Distribution_latest`, `CPAT-AI-AirPollution_latest` and `CPAT-AI-Master_UserGuide`. "Prototype" and "Standalone" are dropped.
2. Old releases keep their names.
3. Update the builders, the links between workbooks and the docs.

## G. Finish

1. Version 1.2.0.
2. Update CAVEATS and CHANGELOG.
3. Run a quick rebuild and the quick checks.
4. Commit and push to `claude/dreamy-bohr-rp8npt` after each stage.

## Untested in Excel

The activation macro, the Power Query loads and the `.xlsb` save are Excel-only. They are listed as untested until the user tries them (NORMS rule). The checks imitate the copy-across to 2041 in LibreOffice and compare the results against legacy.
