# Distribution module: sources

The sources of `../CPAT-AI-Distribution-Prototype_latest.xlsm`, the standalone distribution module (household effects by decile of a mitigation scenario). Plan: [`../plans/Modules.md`](../plans/Modules.md). Rules: [`../../NORMS.md`](../../NORMS.md).

## How it works

- The module is **cut from the built mitigation prototype** (`../CPAT-AI-Mitigation-Prototype_latest.xlsm`): its Distribution and FromMitigation tabs, the distribution data tabs, ScenarioDefinition (distribution rows shown) and Settings. There is no second copy of the Distribution formulas: change them in `../mitigation/build.py`, rebuild the prototype, then rebuild the module.
- Its only input from Mitigation is the tab **FromMitigation**: values of Mitigation section 19a (defined name `ExportDistn`), in the Mitigation column layout.
- **Update from Mitigation** (button on Cover) copies those values from the mitigation workbook named on Cover (default `CPAT-AI-Mitigation-Prototype_latest.xlsm`, next to the module or one folder up). If that workbook is open, its current values are used; otherwise it is opened read-only, without macros or recalculation. One scenario at a time: no batch runs.
- Formulas that read a dropped tab (Settings lookups of country data) are values, those of the prototype (Egypt).

## Build and check

```
python build_distribution.py    # ../releases/CPAT-AI-Distribution-Prototype_v<version>.xlsm and ../..._latest.xlsm (about 1 min)
python check_distribution.py    # about 4 min; report check_distribution_report.md
```

The check: Distribution equals the prototype's cell for cell; FromMitigation equals section 19a through the macro's row mapping; no formula reads a dropped tab or an undefined name; the VBA module and its identifiers; lint; and end to end (the prototype's live carbon price changed and recalculated, the module updated from it and recalculated: the same Distribution).

| File | What it is |
|---|---|
| `build_distribution.py` | The builder (version in `VERSION`, version log in `VERSION_LOG`) |
| `CPATDistribution.bas` | The VBA module: UpdateFromMitigation, RecalculateNow, ToggleRecalculation |
| `check_distribution.py`, `check_distribution_report.md` | The check and its last report |
