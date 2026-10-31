# Distribution module: sources

The sources of the distribution module `CPAT-AI-Distribution` (every version in [`releases/`](releases/), to 1.1.0 named `CPAT-AI-Distribution-Prototype_v<version>.xlsm`; the latest unactivated copy here, `CPAT-AI-Distribution_latest.xlsx`; activated by the Master workbook into `../active_workbooks/CPAT-AI-Distribution_latest.xlsb`): household effects by decile of a mitigation scenario. Plan: [`../core/plans/Modules.md`](../core/plans/Modules.md). Rules: [`../core/NORMS.md`](../core/NORMS.md) (9, 9.7).

## How it works

- The module is **cut from a full build of the mitigation workbook** (v1.2.0: the mitigation workbook no longer holds Distribution; this builder runs the mitigation builder with `CPAT_WITH_DIST=1`, takes the baseline CO2 from `../mitigation/CPAT-AI-Mitigation_latest.xlsx`, recalculates in LibreOffice): its Distribution and FromMitigation tabs, the distribution data tabs, ScenarioDefinition (distribution rows shown), FromMaster and Constants and Mappings. There is no second copy of the Distribution formulas: change them in `../mitigation/build.py`, rebuild Mitigation, then rebuild the module.
- Its only input from Mitigation is the tab **FromMitigation**: values of Mitigation section 19a (defined name `ExportDistn`), in the Mitigation column layout.
- **No macros** (v1.2.0): the Master workbook's *Update Distribution from Mitigation* copies those values from the activated mitigation workbook into the activated distribution workbook, recalculates and saves it. One scenario at a time.
- Formulas that read a dropped tab (lookups of country data) are values, those of the build (Egypt).

## Build and check

```
python build_distribution.py    # releases/CPAT-AI-Distribution_v<version>.xlsx and CPAT-AI-Distribution_latest.xlsx (about 4 min)
python check_distribution.py    # about 4 min; report check_distribution_report.md
```

The check: Distribution equals the prototype's cell for cell; FromMitigation equals section 19a through the macro's row mapping; no formula reads a dropped tab or an undefined name; lint; and end to end (the prototype's live carbon price changed and recalculated, the module updated from it and recalculated: the same Distribution).

| File | What it is |
|---|---|
| `build_distribution.py` | The builder (version in `VERSION`, version log in `VERSION_LOG`) |
| `CPATDistribution.bas` | The VBA module: UpdateFromMitigation, RecalculateNow, ToggleRecalculation |
| `check_distribution.py`, `check_distribution_report.md` | The check and its last report |
