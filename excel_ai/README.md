# Excel-AI: the CPAT prototypes in Excel

New here? Read the human quick start first: [`../QuickStart.docx`](../QuickStart.docx). AI agents: [`core/AGENTS.md`](core/AGENTS.md).

## The workbooks

Open the permalinked copies in **[`active_workbooks/`](active_workbooks/)** (Excel 365, macros on): they are the current versions, and the modules link to each other there.

| File | What it is |
|---|---|
| `active_workbooks/CPAT-AI-Mitigation-Prototype_latest.xlsm` | **The integrated prototype** (mitigation, with the distribution tab) |
| `active_workbooks/CPAT-AI-Distribution-Prototype_latest.xlsm` | **The standalone distribution module**: household effects by decile of a mitigation scenario (button Update from Mitigation reads the prototype beside it) |
| `active_workbooks/CPAT-AI-Air-Pollution-Standalone_latest.xlsx` | The air-pollution scaffold (calculations and regression open) |

Every version, the current one included, is in the module's `releases/` folder (`<Name>_v<version>`).

## The documents

| File | What it is |
|---|---|
| [`bugs_and_legacy/`](bugs_and_legacy/)`Legacy_CPAT_Bugs_v<version>.docx` | **The legacy CPAT bugs**: the rule (bugs and issues; data problems are issues), every legacy bug found and fixed (prototype and legacy 465), the data problems by priority, each bug with its cell-level fix plan |
| [`bugs_and_legacy/`](bugs_and_legacy/)`Tracking_Legacy_Bugs_v<version>.xlsx` | **The master list of bugs and issues** (every module, the same columns): tabs ReadMe, Bugs, Issues, then the CPAT team's tabs |
| `CPAT-AI_CodesMap_v<version>.xlsx` (here) | **The codes map**: the code protocol, vocabularies, variables, output codes and every input |
| `CPAT-AI_Overview_v<version>.pptx` (here) | **The slide deck**: status, how to use it, results |

Older versions: `bugs_and_legacy/register/releases/` (bug book, tracker, codes map), `mitigation/releases/` (deck).

## Folders

| Folder | Contents |
|---|---|
| [`active_workbooks/`](active_workbooks/) | The permalinked `_latest` copy of each module: what people open, what the modules and links read |
| [`core/`](core/AGENTS.md) | The rules, records and plans (read by people and agents): `AGENTS.md`, `CLAUDE.md`, `NORMS.md`, [`BUGS.md`](core/BUGS.md), [`ISSUES.md`](core/ISSUES.md), `CAVEATS.md` (task log), `CHANGELOG.md`, [`TODO.md`](core/TODO.md) (the one list), `plans/` (open plans), `prompts/` (module prompts and guides), `tools/` (`xlpaths.py`, `release.py`, `excel_lint.py`, the MTInputs template) |
| [`mitigation/`](mitigation/README.md) | The prototype: `build.py`, the VBA module and build files at the top; `checks/` (quick and full checks, reference models, LibreOffice session, reports), `extract/` (the extract scripts from the legacy workbook, goal seeks), `docs/` (equations, formulas, method notes, Word documentation, deck), `releases/` |
| [`distribution/`](distribution/README.md) | The distribution module: builder (cuts the module from the prototype), VBA, check, `releases/` |
| [`air_pollution/`](air_pollution/README.md) | The air-pollution scaffold: builder, `docs/` (equation inventory, Python comparison, recovery notes), `releases/` |
| [`bugs_and_legacy/`](bugs_and_legacy/) | The legacy bugs and legacy CPAT (the workbook itself is in `../data/legacy/`): at the top the bug book and the tracker (above); `register/` (the register `Legacy_CPAT_Register.json` and the scripts that write `core/BUGS.md`, `core/ISSUES.md`, the tracker and the bug book; `releases/` of those documents), `fixes/` (cell-level fix plans, the 456-to-465 row map, `check465/`, the bug-fix procedure, their tools), `reference/` (the CPAT team's codes master, surveys, the v0.7.1 codes work), `tools/` (.xlsb readers) |

Rules: [`core/NORMS.md`](core/NORMS.md). Data: [`../data/README.md`](../data/README.md).
