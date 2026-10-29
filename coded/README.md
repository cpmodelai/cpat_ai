# Coded CPAT (Python)

The Python model of CPAT (Coded CPAT): it replicates Excel-AI's mitigation and distribution modules, readable first; the entry point is `cpat_model.run`. This page is for Python developers; the full developer guide is [`cpat_documentation/developer/dev_documentation.md`](cpat_documentation/developer/dev_documentation.md). Excel work is in [`../excel_ai/`](../excel_ai/README.md); rules for every task (logging in `CAVEATS.md`, method vs version notes) are in the root [`../NORMS.md`](../NORMS.md).

**Project under way (2026-10-29): the full build.** Coded CPAT is being rebuilt to replicate Excel-AI (mitigation and distribution) number for number, with human readability first. Start with the spec and plan [`cpat_documentation/project/Spec.qmd`](cpat_documentation/project/Spec.qmd) (Word: `Spec.docx`), the Python norms [`NORMS.md`](NORMS.md), the plan's checklist [`TODO.md`](TODO.md) and the equation list [`cpat_documentation/equations/`](cpat_documentation/equations/) (`Equations.qmd`, code-name version `Equations_codes.qmd`, both generated from `equations.yaml`). The layout below is today's; the target layout is in the spec, section 3.

## Layout

| Path | Contents |
|---|---|
| `cpat_model/` | The model (rebuilt from 2026-10-29, spec section 3.2): `run()` and versions (`__init__.py`), `settings.py`, `core/` (index sets, policy paths, the run loop, module values), `data/` (the tidy database), `inputs/` (scenario sets, D5), `forms/` (switchable demand equations, D4), `mitigation/` (`chain.py`: the order of the blocks; the blocks come in phase 3), `results/`, `air_pollution/` and `transport_cobenefits/` (placeholders, D10) |
| `cpat_model/distribution/`, `distribution_inputs.py`, `constants.py` | The earlier distribution module (validated against Excel); moves onto the new structure in phase 4 |
| `cpat_shiny/`, `app.py` | Shiny application (calls the earlier model: not working until phase 6) |
| `../data/tidy/` | The input data: tidy CSV ([`../data/INTERFACE.md`](../data/INTERFACE.md)); `../data/inputs/scenarios_excel_ai.csv` the Excel-AI scenario set |
| `cpat_testing/` | pytest suite; `compare/` extracts Excel-AI's scenario set and reference values by code (`extract_excel_ai.py`, `reference/`) |
| [`NORMS.md`](NORMS.md), [`TODO.md`](TODO.md) | Python norms (add to the root `NORMS.md`); open work and the plan |
| `cpat_documentation/` | `project/` spec and plan, `equations/` equation list, `developer/`, `user/`; `make_docs.py` writes the Word copies |

## Conventions

- Codes (`Input Code`, `Output Code`, `NameOfParameter`) are identical to the Excel models. The input keys of `dashboard_inputs.py` and `distribution_inputs.py` are the ScenarioDefinition names (`NameOfParameter`, legacy MTInputs column H; the list with each Python key: tab Inputs of `../excel_ai/CPAT-AI_CodesMap_v<version>.xlsx`), in legacy units (percentages typed as whole numbers where legacy does, issue I85).
- The legacy workbook `../excel_ai/legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb` is the reference for values (inputs: the rows and names of the latest file, `CPAT 1.0pre_465`); validated Excel prototypes (e.g. the mitigation MVP in `../excel_ai/mitigation/`) are ported here once checked.
- Python 3.12 (as the repository's Windows environment `cpat312`), pandas 2.2.3, numpy 2.2.0 (`environment.yml`, `requirements.txt`); the code also runs on pandas 3 (copy-on-write rules).
- Every finished task gets a `../CAVEATS.md` entry (root `NORMS.md` section 6).

## Getting started

```bash
conda env create -f environment.yml && conda activate cpat_p    # or: pip install -r requirements.txt -r dev-requirements.txt  (Python 3.12)
pytest                         # the tests of coded/ (from coded/) (the data scripts: cd ../data && pytest tests, 15 more)
shiny run app.py               # the app
```
