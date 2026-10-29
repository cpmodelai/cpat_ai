# Excel-AI: the CPAT prototypes in Excel

New here? Read the human quick start first: [`../HumanReadme-QuickStart.docx`](../HumanReadme-QuickStart.docx).

## The main files

The current version of each main file, `<Name>_v<version>` (NORMS 5a); older versions are in `releases/`.

| File | What it is |
|---|---|
| `CPAT-AI-Mitigation-Prototype_v<version>.xlsm` | **The integrated prototype** (mitigation, with the distribution tab): open it in Excel 365, macros on |
| `CPAT-AI-Distribution-Prototype_v<version>.xlsm` | **The standalone distribution module**: household effects by decile of a mitigation scenario; its Cover links to the prototype in `permalink/` (button Update from Mitigation) |
| `Legacy_CPAT_Bugs_v<version>.docx` | **The legacy CPAT bugs**: the rule (bugs and issues; data problems are issues), the stock table of every legacy bug found and fixed (prototype and legacy 465), the data problems by priority, each bug with its cell-level fix plan |
| `Tracking_Legacy_Bugs_v<version>.xlsx` | **The master list of bugs and issues** (every module, the same columns): tabs ReadMe, Bugs, Issues, then the CPAT team's tabs |
| `CPAT-AI_CodesMap_v<version>.xlsx` | **The codes map**: the code protocol, vocabularies, variables, output codes and every input (tab Inputs: row, name, legacy name, Python key) |
| `CPAT-AI_Overview_v<version>.pptx` | **The slide deck**: status, how to use it, results |
| [`BUGS.md`](BUGS.md), [`ISSUES.md`](ISSUES.md) | The two short lists: bugs (L, M) and issues (I, data problems first; LD, U) |

## Folders

| Folder | Contents |
|---|---|
| [`mitigation/`](mitigation/README.md) | The prototype's sources: builder, VBA, checks, the register and its documents, method notes, the Word documentation (issues and the bug-fixing procedure in its appendices) |
| [`distribution/`](distribution/README.md) | The distribution module's sources: builder (cuts the module from the prototype), VBA, check |
| [`air_pollution/`](air_pollution/README.md) | Recovered standalone v0.3 scaffold, public reference tables, equation inventory and Python comparison; calculations and numerical regression remain open |
| `permalink/` | Only what other files link to: `CPAT-AI-Mitigation-Prototype_latest.xlsm` (data transfer to the modules) |
| `permalink_countryeditable/` | Planned (TODO): a copy of `permalink/` for local, country-specific runs; the modules link to it (NORMS 5a) |
| `releases/` | Every earlier version of the main files since v7.2 |
| `legacy/` | Legacy CPAT: the reference workbooks and codes master (`workbooks/`); the fix-plan sources and tools (`bugfixes/`, with the 456 to 465 row map and `check465/`, the check of the bugs the CPAT team fixed in 465); the bug-fix procedure; the register as JSON (`Legacy_CPAT_Register.json`); the v7.1 codes work (`codes/`) |
| [`plans/`](plans/TODO.md) | The to-do list and the plans |
| `shared/`, `templates/` | Code (release layout, Excel lint) and the input row template used by the builders |

Rules: [`../NORMS.md`](../NORMS.md).
