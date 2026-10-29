# Coded CPAT (Python)

The Python model of CPAT (Coded CPAT): it replicates Excel-AI's mitigation and distribution modules number for number, readable first; the one entry point is `cpat_model.run`. This page is for Python developers; the developer guide is [`cpat_documentation/developer/dev_documentation.md`](cpat_documentation/developer/dev_documentation.md) and the website has a Coded CPAT tab (`../docs/index.html#coded`). Excel work is in [`../excel_ai/`](../excel_ai/README.md); rules for every task (logging in `CAVEATS.md`, method vs version notes) are in the root [`../NORMS.md`](../NORMS.md).

**Status (2026-10-29).** Version `0.9.1p0.1`: Python version 0.1 of the replication of Excel-AI 0.9.1 (mitigation) and Distribution 0.1.3.

- **Mitigation** (plan phase 3): every output code of Excel-AI's stored values for Egypt, scenarios 1 and 2, is produced and matches within 1e-9, 2022-2041 (7,470 codes per scenario). Not built: the road engineer model driving fuel use (`TrModel = Engineer`), country-estimated and manual fiscal multipliers.
- **Distribution** (phase 4): every code of Excel-AI Distribution 0.1.3 matches for Egypt, scenario groups 1 and 2 (1,684 codes, basket and deciles).
- **Speed** (5.4): one country and two scenarios in 0.8 s once the baseline is cached (first run of a session about 3 s).
- **Excel-AI bugs replicated**: eight open prototype bugs (M15-M22, `../excel_ai/BUGS.md`) are replicated so the numbers stay equal; Python follows when Excel-AI fixes them (`TODO.md`).
- **Next**: systematic comparisons (phase 5.1-5.3: the recalculated release workbook, every country, legacy CPAT).

Start with the spec and plan [`cpat_documentation/project/Spec.qmd`](cpat_documentation/project/Spec.qmd) (Word: `Spec.docx`), the Python norms [`NORMS.md`](NORMS.md), the plan's checklist [`TODO.md`](TODO.md) and the equation list [`cpat_documentation/equations/`](cpat_documentation/equations/) (`Equations.qmd`, code-name version `Equations_codes.qmd`, both generated from `equations.yaml`).

## Layout

| Path | Contents |
|---|---|
| `cpat_model/` | The model: `run()` and versions (`__init__.py`), `settings.py` |
| `cpat_model/core/` | Index sets (`dims.py`), the variable registry (`variables.py`, `variables.csv`: every Excel-AI row and its output code), the run loop (`loop.py`: baseline first, then each scenario; prepare, year loop, finish; the baseline cache), the rows of a block (`rows.py`: `Rows`, `State`), policy paths, module values, Excel-AI tables (`excel_ai/`) |
| `cpat_model/data/` | The database: tidy CSV tables (`../data/tidy/`, [`../data/INTERFACE.md`](../data/INTERFACE.md)) |
| `cpat_model/inputs/` | Scenario sets (inputs by `NameOfParameter`, one column per scenario; `../data/inputs/scenarios_excel_ai.csv` is Excel-AI's) |
| `cpat_model/mitigation/` | The blocks of the Mitigation sheet in calculation order (`chain.py` is the only place the order is written): header, policies, Pigouvian taxes, prices, power, fuel use, road engineer model, totals and revenues, emissions, GDP effects, module inputs, welfare |
| `cpat_model/distribution/` | `mapping.py` (DistMapping data), `incidence.py` (the Distribution sheet); the earlier package (`distribution.py` and its steps) is kept for its tests until retired |
| `cpat_model/results/` | `Results`: `by_code(country)` (mitigation rows by output code and year), `distribution_by_code(country)` (basket and deciles) |
| `cpat_model/air_pollution/`, `transport_cobenefits/` | Placeholder modules: Excel-AI's typed module values |
| `cpat_model/forms/` | Switchable equation forms (`ModelForm`; only the CPAT form is built) |
| `run_model.py` | Command line: a scenario-set file in, results by country out (CSV, optional workbook) |
| `cpat_shiny/`, `app.py` | Shiny application on `cpat_model.run` |
| `cpat_testing/` | pytest suite: each mitigation block and the distribution sheet against Excel-AI's stored values; `compare/` extracts the reference values (`extract_excel_ai.py`, `reference/`) |
| [`NORMS.md`](NORMS.md), [`TODO.md`](TODO.md) | Python norms (add to the root `NORMS.md`); the plan and open work |
| `cpat_documentation/` | `project/` spec and plan, `equations/` equation list, `developer/` developer guide, `user/` texts of the app; `make_docs.py` writes the Word copies |

## Running

```bash
conda env create -f environment.yml && conda activate cpat_p    # or: pip install -r requirements.txt -r dev-requirements.txt  (Python 3.12)
python run_model.py                                     # the Excel-AI scenario set for Egypt; results to outputs/
python run_model.py my_set.csv --scenarios 1 2 --xlsx   # a scenario-set file; also one workbook
shiny run app.py                                        # the app
pytest                                                  # the tests (from coded/; about 1 minute)
```

From Python:

```python
import cpat_model
from cpat_model.inputs import read_scenario_set
results = cpat_model.run(read_scenario_set())           # Settings(): dummy database, Egypt, 2022-2041
results.by_code('EGY').loc['egy.mit.co2.tot.tot.2']     # CO2 of scenario 2 by year
results.distribution_by_code('EGY').loc['egy.distn.net.tot.dec.ove.2']   # net effect by decile
```

## Conventions

- Codes (`NameOfParameter`, variable and output codes) are Excel-AI's and the codes map's (`../excel_ai/CPAT-AI_CodesMap_v<version>.xlsx`); Python never invents a second name (NORMS 0.4).
- Excel-AI is the specification (NORMS 0): an Excel-AI bug is replicated, registered and marked in the code (`# Excel-AI bug M<n>`), never fixed silently.
- Python 3.12, pandas 2.2.3, numpy 2.2.0 (`environment.yml`, `requirements.txt`); the code also runs on pandas 3 and Python 3.13.
- Every finished task gets a `../CAVEATS.md` entry (root `NORMS.md` section 6).
