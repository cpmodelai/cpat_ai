# Coded CPAT (Python)

A component-based Python reimplementation of the CPAT model: the mitigation module and the household distribution module, run by `run_model.py` (or the Shiny app, `app.py`). This page is for Python developers; the full developer guide is [`cpat_documentation/developer/dev_documetation.md`](cpat_documentation/developer/dev_documetation.md). Excel work is in [`../excel_ai/`](../excel_ai/README.md); rules for every task (logging in `CAVEATS.md`, method vs version notes) are in the root [`../NORMS.md`](../NORMS.md).

## Layout

| Path | Contents |
|---|---|
| `cpat_model/mitigation/` | Mitigation module components |
| `cpat_model/distribution/` | Distribution module (household incidence by decile, revenue recycling, welfare); specification and validation status in [`../other/distribution/README.md`](../excel_ai/distribution/README.md) |
| `cpat_model/data_read/`, `dashboard_inputs.py`, `distribution_inputs.py`, `scenario_results.py`, `indicators/`, `constants.py` | Data loading, inputs, cross-scenario results, indicators, codes |
| `cpat_shiny/`, `app.py` | Shiny application |
| `../data/dummy/` | Input data used by default (all data are in the root [`data/`](../data/README.md)) (`.env`: `DATA_ENVIRONMENT=dummy`; `real` reads `REAL_DATA_PATH`). `energy_consumption.csv`, `prices_dom.csv`, `distn_hh_survey.csv` and `distn_io_gtap.csv` must agree with the dummy legacy-data files in `../data/legacy_dummy/` (root `NORMS.md` section 8) |
| `../data/scripts/` | The data conversion scripts ([`../data/README.md`](../data/README.md)): `export_to_legacy.py` (the four proprietary tables in the legacy layout), `build_data_workbook.py` (data workbook, Python format), `convert_data_workbook.py` (Python format <-> CPAT format); tests in `../data/tests/` |
| `cpat_testing/` | pytest suite mirroring `cpat_model/` |
| [`TODO.md`](TODO.md) | Open Python work |

## Conventions

- Codes (`Input Code`, `Output Code`, `NameOfParameter`) are identical to the Excel models. The input keys of `dashboard_inputs.py` and `distribution_inputs.py` are the ScenarioDefinition names (`NameOfParameter`, legacy MTInputs column H; the list with each Python key: tab Inputs of `../excel_ai/CPAT-AI_CodesMap_v<version>.xlsx`), in legacy units (percentages typed as whole numbers where legacy does, issue I85).
- The legacy workbook `../excel_ai/legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb` is the reference for values (inputs: the rows and names of the latest file, `CPAT 1.0pre_465`); validated Excel prototypes (e.g. the mitigation MVP in `../excel_ai/mitigation/`) are ported here once checked.
- Python 3.12 (as the repository's Windows environment `cpat312`), pandas 2.2.3, numpy 2.2.0 (`environment.yml`, `requirements.txt`); the code also runs on pandas 3 (copy-on-write rules).
- Every finished task gets a `../CAVEATS.md` entry (root `NORMS.md` section 6).

## Getting started

```bash
conda env create -f environment.yml && conda activate cpat_p    # or: pip install -r requirements.txt -r dev-requirements.txt  (Python 3.12)
python run_model.py            # mitigation for the scenarios in config.py, then distribution against the baseline
pytest                         # 48 tests (the data scripts: cd ../data && pytest tests, 15 more)
shiny run app.py               # the app
```
