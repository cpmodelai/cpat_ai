# NORMS - Coded CPAT (Python)

Rules for every task in `coded/`. They add to the repository-wide [`../NORMS.md`](../NORMS.md), of which these sections apply to Python as written: **0** (never replicate a legacy bug; always replicate a legacy issue, and track it), **4** (inputs: MTInputs rows and `NameOfParameter` names), **6, 6b** (task completion: `CAVEATS.md`; norms follow the lessons), **7** (methodology and version notes are different documents) and **8** (data). Its Excel sections (1-3, 5: columns, style, LAMBDA encoding, releases) do not apply, except where this file points to them.

Rules marked **(provisional, Dn)** depend on design choice Dn of the spec ([`cpat_documentation/project/Spec.qmd`](cpat_documentation/project/Spec.qmd) section 10), still to be decided with the user; until then they state the recommended option.

| Section | Contents |
|---|---|
| 0 | The overriding norm: follow Excel-AI |
| 1 | Readability: equations, names, comments |
| 2 | Where things go (folders and files) |
| 3 | Model structure: dimensions, the year loop, modules, equation forms |
| 4 | Inputs: scenarios and advanced inputs |
| 5 | Data: databases |
| 6 | Results and codes |
| 7 | Tests and comparisons |
| 8 | Documents: qmd, Word, the website |
| 9 | Task completion and bookkeeping |
| 10 | Python conventions |

## 0. The overriding norm: follow Excel-AI

1. **Excel-AI is the specification.** Coded CPAT replicates the mitigation and distribution modules of Excel-AI (`../excel_ai/CPAT-AI-Mitigation-Prototype_v<version>.xlsm`, `../excel_ai/CPAT-AI-Distribution-Prototype_v<version>.xlsm`) number for number. When the methodology (`../docs/01_MainDocumentation/`), legacy CPAT and Excel-AI disagree, the code follows Excel-AI and the difference is already, or is then, in the register.
2. **Which version.** Each module states the Excel-AI version it replicates (one constant, `EXCEL_AI_VERSION`, and the version in its module docstring). Moving to a new Excel-AI version is a task of its own: port the changed rows (the Excel version log and `../CAVEATS.md` list them), then rerun the comparison.
3. **Never "fix" Excel-AI silently.** If an Excel-AI formula looks wrong or strange, replicate it, register it (a prototype bug `M`, a legacy bug `L` or an issue `I`, root `NORMS.md` section 0) and tell the user. The Python fix follows the Excel fix, in the same version, so both stay equal.
4. **Codes are shared.** Variable codes, input names (`NameOfParameter`) and output codes are those of Excel-AI and the codes map `../excel_ai/CPAT-AI_CodesMap_v<version>.xlsx`. Python never invents a second name for a quantity that has a code.
5. **One register.** Bugs and issues found while porting go in the one register (`../excel_ai/mitigation/issues_register.py`; root `NORMS.md` section 0 rule 3), with module "Coded CPAT" where only Python is affected. Coded CPAT keeps no list of its own.

## 1. Readability: equations, names, comments

The purpose of the code is that a person with the equation list open can find, read and check every equation.

1. **One equation, one function.** Each equation of the equation list ([`cpat_documentation/equations/`](cpat_documentation/equations/)) is one small function (or one clearly marked line in a short function), named after the quantity it computes. Its docstring starts with the equation id and the equation in the notation of the equation list, then the Excel-AI rows it replicates:

   ```python
   def ener(ener_prev, atp, atp_prev, ...):
       """EQ-M4.1  Fuel use, CPAT constant-elasticity form.

       Q_t = Q_{t-1} * (1 + g_t)^(eps_Y) * (P_t / P_{t-1})^(eps_U) * ...      (over fuels i, sectors j)
       Excel-AI: Mitigation section 6, code ener.<sector>.<fuel>; Equations.md E69.
       """
   ```

2. **Names are CPAT codes (provisional, D3).** A variable that has a code in the codes map is called by its code stem in the code (`ener`, `atp`, `ctx`); the previous year adds `_prev`, the baseline (scenario 1) value adds `_ref`, a change against the baseline `_chg` (as Excel-AI `.ref`, `.chg`). The variable registry (`cpat_model/core/variables.py`, generated from the codes map) gives each code its description, unit, dimensions and Greek symbol. Names without a code (local helpers) are plain English words in `snake_case`, never single letters other than the index letters of the equation list.
3. **The equation list and the code agree.** An equation added, removed or changed in the code is changed in the equation list in the same task, and the other way round. A test lists every equation id and fails if one has no function or one function cites an unknown id.
4. **No hard-coded numbers.** Apart from 0, 1 and array positions, every number comes from the inputs, the data or a named constant in `cpat_model/core/constants.py` with its source and unit (as root `NORMS.md` section 3, "No hard-coded constants").
5. **Units in the registry, conversions in one place.** Money units follow the Excel-AI vocabulary (`USD m`, `LCU bn`, `USD/GJ`, real or nominal; root `NORMS.md` section 3, "Money units"). A function body does not multiply by `1e3`, `1e6` or `1e9`; it calls a named conversion.
6. **Short and flat.** A function that needs scrolling is split. No clever one-liners, no metaprogramming in model code, no inheritance deeper than one level. Prefer explicit arguments to reading a global state.
7. **Comments say why, not what.** The docstring says what; a comment explains a choice, an Excel-AI quirk (with its register code, e.g. `# I85: percentages typed as whole numbers, as legacy`) or a unit.

## 2. Where things go (folders and files)

1. **The layout** is in [`README.md`](README.md) and in the spec, section 3. Code goes in `cpat_model/` (the model), `cpat_shiny/` (the app), `cpat_testing/` (tests); documents in `cpat_documentation/`. The top of `coded/` holds only the entry points (`run_model.py`, `app.py`), configuration (`config.py`, `.env`, environment files) and the three guides (`README.md`, `NORMS.md`, `TODO.md`).
2. **No working files in the core folders.** Scratch scripts, notebooks, exports and one-off comparisons do not go in `cpat_model/`, `cpat_shiny/` or `cpat_testing/`. Comparison scripts that are kept go in `cpat_testing/compare/`; run outputs go in `coded/outputs/` (git-ignored); anything else temporary stays outside the repository.
3. **Folders, not long lists.** A folder gets at most three new files in one task; more become a subfolder with one pointer file (a `README.md` or `__init__.py` that says what is inside).
4. **The package follows the model.** `cpat_model/mitigation/` has one subpackage per Excel-AI block, named for what it computes (`policies`, `prices`, `power`, `fuel_use`, `revenues`, `emissions`, `gdp`, ...), and one file, `chain.py`, that lists the order in which the blocks run (spec section 3). A reader learns the model order from that one file.
5. **No `Old/`, `tmp_`, `new_`, `_v2` files.** Git keeps the history; a replaced file is deleted in the task that replaces it.
6. **Data never in `coded/`.** All data are in `../data/` (root `NORMS.md` section 8); test fixtures with their tests (`cpat_testing/**/data_expected/`).

## 3. Model structure: dimensions, the year loop, modules, equation forms

1. **Labelled arrays (provisional, D2).** Model quantities are labelled arrays (`xarray`) with named dimensions: `country`, `scenario`, `year`, and the dimensions of the quantity (`fuel`, `sector`, `tech`, `user`, `decile`, ...), using the index names of the equation list. Equations broadcast by name; no positional axis arithmetic in model code.
2. **Two passes, three stages (provisional, D1, D15).** The baseline (scenario 1) runs first, then all policy scenarios together, reading the baseline values they need (as Excel-AI's `BaselineCO2` and `.ref`). Each pass has three stages: **prepare** (everything that depends on no model quantity, for all years at once: policy paths, international prices and the price chain, power cost paths including the levelised variable cost, exogenous drivers, the module values that feed Pigouvian taxes), the **year loop** (for each year t, every block in the order of `chain.py`, each reading only year t and earlier years: all of mitigation, then the air-pollution and transport co-benefit modules for year t, then the GDP effect that reaches t+1), and **finish** (all-year results: carbon-pricing indicators, welfare, exports; then distribution in its analysis year). No equation reads a later model year (root `NORMS.md` 5c, circular references, rule 1); a look-ahead on exogenous paths belongs in prepare.
3. **Countries and scenarios together.** Every function works for any number of countries and scenarios at once (they are array dimensions); nothing loops over countries or scenarios in model code. Scenario 1 is the baseline (`scenario=1`); `_ref` values are read from the baseline pass in the same year, as Excel-AI's `ref_formula`.
4. **Modules talk through declared interfaces.** Each module declares what it reads and what it writes (codes). Downstream modules (distribution, air pollution, transport co-benefits) read only their declared inputs, as the Excel modules read only `FromMitigation` (root `NORMS.md` section 3, "Exports to modules").
5. **Switchable equation forms (provisional, D4).** The behavioural core equations (fuel demand, electricity demand, power supply, road transport) are called through the forms registry `cpat_model/forms/`, never directly. The global setting `model_form` picks the form of each; the default, `standard_cpat`, is the Excel-AI form and is the only one built until the user asks for another. A new form never changes the numbers of `standard_cpat`.

## 4. Inputs: scenarios and advanced inputs

1. **Scenario inputs are MTInputs.** A scenario set is a table with the rows of legacy MTInputs (`NameOfParameter`, root `NORMS.md` section 4) and one column per scenario; the Shiny app builds the same table. Input keys are the `NameOfParameter` names, in legacy units (I85).
2. **Advanced inputs** (time series and longer-form inputs, the legacy `Manual inputs` tab and Excel-AI `Settings`) come from one advanced-inputs file per run (format: provisional, D5), with defaults from Excel-AI.
3. **Validated once.** Inputs are read and checked (names known, types, ranges, option values as legacy) in `cpat_model/inputs/` before the model runs; model code never reads a raw input file.

## 5. Data: databases

1. **Databases (provisional, D6).** The model reads its data from a named database: `full` (every table, including the four proprietary tables: energy balances, domestic prices, GTAP input-output, household survey; a private repository, never this one), `public` (every table except those four; in `../data/`), and `dummy` (today's `../data/dummy/`, fake values in the real formats). The choice is a setting (`.env`: `DATA_ENVIRONMENT`, the path of the full database outside the repository). The comparisons use the systematic set: `public` with the same four tables in every model.
2. **Never commit proprietary data,** nor results computed from them (root `NORMS.md` section 8).
3. **Loaders read, never compute.** `cpat_model/data/` loads and reshapes tables to the model's dimensions; any calculation on data is a model equation with an id.

## 6. Results and codes

1. **Results are keyed by Excel-AI output codes** (`<variable>.<sector>.<fuel>` as the prototype) and dimensions `country`, `scenario`, `year`, so every Python result can be set against the Excel-AI row with the same code.
2. **Results belong to the scenario; differences as Excel-AI** (root `NORMS.md` section 3c: `x.ref`, `x.chg`, `x.pct` only for strictly positive quantities; price changes are price indices; ratios from summed levels).

## 7. Tests and comparisons

1. **Three levels.** Unit tests per equation (small hand-checked cases); module tests against Excel-AI values by code (fixtures extracted from the recalculated Excel-AI workbook, one country); end-to-end comparisons (all codes, then all countries).
2. **Tolerance.** Python equals Excel-AI to a relative difference of 1e-9 (absolute 1e-9 near zero) unless a difference is explained and registered.
3. **Comparison order:** Python against Excel-AI, one country (Egypt), then all countries; Python or Excel-AI against legacy CPAT, one country, then all; always on the systematic dataset (section 5).
4. **`pytest` passes before every commit.** A failing comparison is not skipped or loosened to pass; it is fixed or registered.

## 8. Documents: qmd, Word, the website

1. **qmd is the source.** Documents for people (spec, plan, design choices, equation list, method notes) are Quarto markdown (`.qmd`) in `cpat_documentation/`; Word copies (`.docx`) are generated from them (`cpat_documentation/make_docs.py`), never edited by hand. Guides for agents and developers (`README.md`, `NORMS.md`, `TODO.md`) stay `.md`: GitHub shows them formatted, every tool reads them, and Quarto renders `.md` as well as `.qmd`, so they can join the website unchanged.
2. **Diagrams** are mermaid blocks in the qmd (Quarto draws them); `make_docs.py` renders them to PNG for Word.
3. **Notation.** The equation list uses the Greek letters and index letters of the methodology (`../docs/01_MainDocumentation/`); where the methodology has none, it says so and uses the Excel-AI note (`../excel_ai/mitigation/Equations.md`). Its code version uses the codes map.
4. **Methodology, not history** (root `NORMS.md` section 7): the equation list and method notes describe the current model only.

## 9. Task completion and bookkeeping

As root `NORMS.md` section 6: every finished task gets a `../CAVEATS.md` entry; open work is in [`TODO.md`](TODO.md) (tick it, add the follow-ups); a lesson with a cause that can repeat becomes a norm here, with its check (root section 6b).

## 10. Python conventions

- Python 3.12, pandas, numpy, xarray (`environment.yml`, `requirements.txt`); new dependencies only with a reason in the task's `CAVEATS.md` entry.
- Type hints on public functions; `ruff` for lint and format (provisional).
- Functions are pure: inputs in, results out, no file or global state inside model code. Reading files happens in `cpat_model/data/` and `cpat_model/inputs/` only.
- The one public entry point is `cpat_model.run(...)` (spec section 3); `run_model.py`, the Shiny app and the tests all call it.
