<!-- Source of ../QuickStart.docx. Regenerate from the repository root: cp QuickStart.docx /tmp/qs_ref.docx && pandoc docs/QuickStart.md -o QuickStart.docx --reference-doc=/tmp/qs_ref.docx -->

---
title: "CPAT-AI: Quick Start for People"
---

A short, human-readable orientation to the cpat_ai repository, mostly about the Excel prototypes (Excel-AI). Written 2026-10-29, updated 2026-10-31 for release 1.2.0: Excel-AI 1.2.0 (the Master workbook; Mitigation and Distribution without macros, activated by the Master), Coded CPAT 1.1.0p1.4, data edition Public01. The detail lives in the documents listed in section 1; this guide only points to them.

# 1. Key documents (start here)

Paths are relative to the repository root. Files named `_v<version>` carry the current version (today 1.2.0 for the workbooks; 1.1.0 for the bug book, tracker, codes map and deck); older versions are kept with their module (`releases/` folders).

**The website** <https://cpmodelai.github.io/cpat_ai/> has a home page and three tabs: Methodology (`#methodology`, the CPAT methodology), CPAT Excel-AI (`#excel-ai`, the Excel prototypes) and CPAT Python (`#python`, the Python model). Offline: `docs/index.html`.

## Human-readable documents

| **Document** | **What it is for** |
|---|---|
| `QuickStart.docx` | This guide (root folder). |
| `excel_ai/active_workbooks/CPAT-AI-Master_UserGuide.xlsm` | The Master workbook: the user guide inside Excel (tab UserGuide) and every macro. |
| `excel_ai/mitigation/docs/CPAT-AI-Mitigation_Documentation.docx` | Short documentation of the mitigation module: what it is, quick start, how it works, limits. |
| `excel_ai/mitigation/docs/CPAT-AI-Mitigation_Methods.docx` | Methods volume: one chapter per block, with equations. |
| `excel_ai/bugs_and_legacy/Tracking_Legacy_Bugs_v<version>.xlsx` | **The master list of bugs and issues**, every module, with the CPAT team's own tabs. |
| `excel_ai/bugs_and_legacy/Legacy_CPAT_Bugs_v<version>.docx` | Every legacy bug found, with its cell-level fix plan for legacy CPAT. |
| `excel_ai/CPAT-AI_CodesMap_v<version>.xlsx` | Codes, variables and every input (legacy row, name, Python key). |
| `other/SetupGuide.docx` | Getting set up: GitHub, the repos, the AI tools, git in brief. |

## Key PowerPoints

| **Deck** | **What it is for** |
|---|---|
| `excel_ai/CPAT-AI_Overview_v<version>.pptx` | The CPAT-AI deck: status, how to use the prototype, results. The quickest overview. |
| `coded/cpat_documentation/Coded-CPAT_Overview_v<version>.pptx` | The Coded CPAT (Python) deck. |
| `other/presentations/AIClimate-FiscalTools_v2.6.pptx` | The overarching deck on the team's AI climate-fiscal tools, CPAT-AI among them. |

## Computer-readable files

Plain-text (Markdown) files that the AI and the scripts read; GitHub shows them formatted, so people can read them too. The Excel-AI rules and records are in `excel_ai/core/`.

| **File** | **What it is for** |
|---|---|
| `README.md`, `excel_ai/README.md` | Front page of the repo and of the Excel prototypes: who reads what, folder map. Each module folder has its own README. |
| `AGENTS.md` (and `CLAUDE.md`) | The entry point for any AI working in the repo. |
| `excel_ai/core/NORMS.md` | The rules for every task (people and AI alike). |
| `excel_ai/core/CAVEATS.md` | Log of every finished task and its caveats (newest at the bottom). |
| `excel_ai/core/CHANGELOG.md` | One line per release of the prototype. |
| `excel_ai/core/BUGS.md`, `excel_ai/core/ISSUES.md` | Short lists of bugs and issues (generated from the register). |
| `excel_ai/core/TODO.md` | The single list of open work; one file per open plan in `excel_ai/core/plans/`. |
| `data/README.md` | The data editions, every table, the scripts and the tests. |
| `coded/README.md` | The Python model (Coded CPAT): layout, running, tests. |

# 2. What the Excel prototype is, and the plan

The World Bank/IMF **Climate Policy Assessment Tool (CPAT)** models the fiscal, economic, energy, emissions and distributional effects of carbon pricing and related policies. The legacy CPAT (version CPAT 1.0pre_465) is a very large single workbook; the repository holds it as a shell, `data/legacy/CPAT 1.0pre_465_Shell.xlsb`, with its six proprietary tabs empty (section 4).

**CPAT-AI** rebuilds it, with AI help, as readable modular Excel workbooks (Excel-AI). The mitigation prototype answers: what do carbon taxes, ETSs, feebates, excises, subsidy reform and a methane fee do to prices, energy use, emissions, revenue and GDP, year by year to 2041, for one country at a time?

## The plan

1. **Replicate CPAT-legacy in Excel.** Match legacy results, but without its bugs (every bug is fixed). Issues are replicated as legacy has them, not yet upgraded: improvements are proposed and tracked, then decided later.
2. **Make Python replicate the Excel prototype** (`coded/`, the Coded CPAT and its Shiny app), using the same codes and input names, so the two can be compared number for number. Done for 1.1.0: Coded CPAT 1.1.0p1.4 matches Excel-AI Mitigation and Distribution 1.1.0 on Public01 within 1e-9.

## Key improvements over legacy

- Every known legacy bug fixed, and documented with a fix plan the CPAT team can apply to legacy.
- Readable: formulas are short (target 90 characters, at most 115) and one formula serves a whole block; sections follow legacy's section numbers.
- Any country: formulas contain no country numbers; all country data come from the data tabs, chosen by the country code on ScenarioDefinition (MTInputs, Model settings).
- Linked data: the data tables refresh from a data workbook (Power Query) instead of being pasted in.
- Scenarios: MTOutputs shows the live scenarios side by side and a dashboard (ScenarioCompare) compares them; the Master stores up to 10 as values and compares them (CompareStored); every output has a code shared with Python (e.g. `egy.mit.co2.tot.tot.2`).
- Modular: one workbook per module (Mitigation, Distribution, Air Pollution; Transport Co-benefits to follow), without macros; one Master workbook holds every macro.
- Checked: an independent Python model (Coded CPAT), a quick check after every change, and a full check at milestones.

# 3. The modules and who is responsible

| **Module** | **Workbook (activated by the Master into `excel_ai/active_workbooks/`)** | **Responsible** |
|---|---|---|
| Master (1.2.0) | `CPAT-AI-Master_UserGuide.xlsm` in `excel_ai/active_workbooks/`: the user guide and every macro; sources in `excel_ai/master/` | Stephen |
| Mitigation (1.2.0) | `CPAT-AI-Mitigation_latest.xlsx` in `excel_ai/mitigation/`, activated as `CPAT-AI-Mitigation_latest.xlsb` | Stephen (others joining soon) |
| Distribution (1.2.0) | `CPAT-AI-Distribution_latest.xlsx` in `excel_ai/distribution/`, activated as `..._latest.xlsb` | Faustyna (Victor joining soon) |
| Air Pollution (AP) (scaffold v0.3, a separate track) | `CPAT-AI-AirPollution_latest.xlsx` in `excel_ai/air_pollution/` | Paulina |
| Transport Co-benefits | Planned (`excel_ai/core/plans/Transport_cobenefits.md`) | Alexandra |

## The active workbooks

Open **`excel_ai/active_workbooks/CPAT-AI-Master_UserGuide.xlsm`** first (Excel 365, macros on). It is the user guide and the only workbook with macros. Its module table lists each module's latest version, its `.xlsx` in the repository and its GitHub link. **Activate** a module there: the Master opens the `.xlsx` (shipped with formulas to 2035, so it is small and quick to open), fills the formulas across to 2041, recalculates and saves `<Name>_latest.xlsb` next to itself in `active_workbooks/`. Work in the `.xlsb` (manual calculation: press F9 after a change). The `.xlsb` are generated: on a git conflict take either side and activate again; never commit the `~$` lock files Excel writes while a workbook is open (`.gitignore` skips them). Run a module for a particular country there, on your local drive; keep copies holding real data local and never commit them. Every version is kept in the module's `releases/` folder (`excel_ai/mitigation/releases/`, ...) as `<Name>_v<version>`.

## How the modules connect and how data flow

- Mitigation is the hub. The blocks other modules read are named in their section bands: section 19a for Distribution, section 15 for Air Pollution, section 5b for Transport Co-benefits.
- Distribution receives its block from the Master: **Update Distribution from Mitigation** copies section 19a of the activated mitigation workbook into the activated distribution workbook, by code.
- Data tables: the Master's **Update data tables** loads them from the data workbook `data/Public01/legacy_xlsx/CPAT_LegacyData.xlsx` (or GitHub, or another data repository) into the module's data tabs by Power Query, for the module's country or all countries (tab Settings of the Master).
- Results: MTOutputs in the mitigation workbook shows the live scenarios side by side; the Master stores them as values (StoredScenarios) and compares them (CompareStored).

# 4. Data and information security

- **All data live in `data/`, organised in editions.** An edition is a folder with the same structure as every other; `data/editions.csv` is the registry and `data/catalog.csv` the catalogue of every table. The scripts that convert the data are in `data/scripts/`.
- **Public01** (in this public repository, the default edition) holds the public tables plus the **six proprietary tables**, Balances, EnergyCons, Prices_dom, IO_GTAP, HHSurvey and Tran_Scatter, as perturbed values (±3%, identities kept): not the real data. The real data are only in the private edition Full01, never in this repository.
- **Tidy CSV is the source of truth:** `data/Public01/tidy/`. The data workbook the prototype's data links read, `data/Public01/legacy_xlsx/CPAT_LegacyData.xlsx` (tables `L_<Tab>` with a FilterISO3 column), is written from it and never edited by hand.
- **The legacy workbook:** `data/legacy/CPAT 1.0pre_465_Shell.xlsb` has the six proprietary tabs empty; `data/Public01/legacy/CPAT 1.0pre_465_Public01.xlsb` is the shell filled with Public01's data. Its cached formula results are still from the real data until it is recalculated and saved in Excel.
- **Documents shared beyond the team** (the bugs document, the tracker, the codes map and the decks) must hold no proprietary data or values derived from it.
- **Never upload any form of CPAT containing real data to the repo** (a workbook, an export, a CSV or a screenshot). That breaks information security. Real data stay in the private data repository or on your local drive (see `data/README.md` for pointing the scripts at them); check the changed files before every commit.

## Loading data into the mitigation module

In the Master, tab **Settings**: choose the data source and the rows to load (the module's country, or all countries), then click **Update data tables** on UserGuide. The activated mitigation workbook records the choice on its tab FromMaster; the status is on its Cover.

| **Source** | **What it does** |
|---|---|
| Embedded (shipped data, no update) | Uses the data shipped inside the workbook (Public01); the default. |
| Public01 - GitHub (public repository) | Reads `data/Public01/legacy_xlsx/CPAT_LegacyData.xlsx` from the public repository. |
| Public01 - local file | Reads `CPAT_LegacyData.xlsx` in your clone's `data/Public01/legacy_xlsx/` (or a path you type). |
| Data repository (type its URL) | Reads a data workbook from a separate data repository; a workbook you then save with real data must not be committed. |
| SharePoint (type its URL) | Reads a data workbook from SharePoint. |

# 5. Bugs, issues and how they are tracked

**The rule (`excel_ai/core/NORMS.md` section 0): never replicate a legacy bug; always replicate a legacy issue, and track it.**

| | **Bug** | **Issue** |
|---|---|---|
| Meaning | Legacy does not do what it means to: a wrong row, a term applied twice, a sign error. | Legacy does what it means to, but the choice is open to question: old data, a simplification, a missing feature. |
| We | Fix it. Never replicated. | Replicate it exactly; depart only by explicit user decision. |
| Example | L1: services electricity demand grows with the industrial multiple after 2023. | I98: combustion emission factors use only the GAINS base and final factors, as legacy. |

Codes: L legacy bug, M prototype bug, I issue (data problems are issues), LD departure from legacy, U upgrade. One register for every module (`excel_ai/bugs_and_legacy/register/`) generates the tracker, the bugs document, `BUGS.md` and `ISSUES.md` at every release.

## Where things stand (1.1.0)

| **Count** | **Status** |
|---|---|
| 231 legacy bugs (L) | Fixed in the prototype, or in parts not built. In legacy 465 (CPAT team): 52 fixed, 9 fixed with caveats, 2 marked fixed but not fixed, 168 open. |
| 22 prototype bugs (M) | All fixed (1 withdrawn: not a bug); M15-M22 were found by Coded CPAT. |
| 135 issues (I), 14 of them data problems | 90 accepted, 9 open, 18 resolved, 14 dropped, 4 closed. |
| 35 departures (LD), 14 upgrades (U) | Each one a recorded user decision or proposal. |
| 20 documentation bugs | Corrections to the methodology documentation (no model change). |

## Major open issues

- **I98 (Extremely high):** combustion emission factors use only the GAINS base and final factors; the year-by-year paths are needed.
- **I148 (Extremely high):** the current-account data are typed for Egypt only (other countries need the WEO data).
- **I97 (Very high):** blank VAT cells in the IMF price dataset (legacy fix L170 is in the prototype).
- **I90:** the proprietary tables are Egypt only, so other countries need data.
- **I1:** the prototype has not yet had a full run in Excel 365 by the team (it is built and checked in LibreOffice).
- CBAM process emissions, green public investment, industrial emissions intensity and the Air Pollution and Transport Co-benefits modules are upgrades U15-U19, outside the current scope.

To raise a bug or issue: add it to the tracker (or ask the AI to register it). It must appear in `BUGS.md` or `ISSUES.md` the same day.

# 6. Key norms, with examples

`excel_ai/core/NORMS.md` holds all of them. The ones to know first:

- **Bugs vs issues** (section 0): as above. When in doubt, treat it as an issue, replicate it and ask.
- **Never improve legacy silently:** newer data or a better method is an upgrade (U) for the team to decide, e.g. a new population source.
- **Versions** (section 5): never edit a released workbook; build the next version. Workbooks are `<Name>_v<version>` in the module's `releases/`, e.g. `CPAT-AI-Mitigation_v1.2.0.xlsx` (to 1.1.0: `CPAT-AI-Mitigation-Prototype_v1.1.0.xlsm`).
- **Latest and active workbooks** (sections 5a, 9.7): the latest `.xlsx` of each module sits in its folder; `excel_ai/active_workbooks/` holds the Master and the activated `.xlsb`.
- **Inputs** (section 4): use legacy MTInputs names, e.g. CPLevelTarget for the carbon price in the target year, the same in Excel and Python.
- **Style** (sections 1-2): fixed column layout and CPAT colours, e.g. input cells light green, code cells light blue, calculation cells unfilled; formulas short (target 90 characters, at most 115).
- **Data** (section 8): all data live in `data/`, as editions; tidy is the source of truth; only public or perturbed data are committed.
- **Every finished task is logged** in `excel_ai/core/CAVEATS.md` (section 6); methodology and version notes are separate documents (section 7).

# 7. How the AI works here

Any AI tool (Claude, Codex, Copilot, ...) starts from the root `AGENTS.md` (Claude's `CLAUDE.md` just points to it). `AGENTS.md` routes the AI to each project's rules: for Excel-AI, `excel_ai/core/AGENTS.md`, which points to `NORMS.md`, `BUGS.md`, `ISSUES.md`, `TODO.md` and `CAVEATS.md` in `excel_ai/core/`; for Coded CPAT, `coded/README.md`, `coded/NORMS.md` and `coded/TODO.md`. So it follows the same rules as people and logs what it did. To change how the AI behaves, change the project's rules (`NORMS.md`), not the AI's own file.

## Queries you can ask

- "Which legacy bugs are still open in legacy 465, and which affect revenue?"
- "Explain how the retail price of diesel is built up, with the cells in the prototype."
- "Is this difference from legacy a bug or an issue? Register it."
- "What changed between 1.0.4 and 1.1.0?" (it reads `CHANGELOG.md` and `CAVEATS.md`)
- "Where does the Distribution module get its fuel price changes from?"
- "Run the quick check and tell me if anything broke."

# 8. The repos and git

The repos sit under the GitHub organisation **cpmodelai**:

| **Repo** | **Purpose** |
|---|---|
| cpat_ai (public) | This repo: the CPAT Excel prototypes, the Python model, the public data edition and documents. Public, so never put real data or internal material here. |
| climate-fiscal-ai-tools (public) | The wider set of AI climate-fiscal tools beyond CPAT (e.g. the excise diagnostic, the tax dashboard). Public, so never put CPAT data or internal material there. |
| repo-tools (public) | The helper scripts that make git easy: CloneRepos.bat, SyncRepo.bat, SyncAllRepos.bat, RepoDirectory.csv (in Repos.zip). |

The real data (edition Full01) are in a separate private data repository.

Getting set up and a short guide to git are in `other/SetupGuide.docx`. In short: double-click SyncAllRepos.bat to pull and push every repo; if it stops with a merge conflict, **GitHub Desktop** shows the clashing files and helps you resolve them.

# 9. Further information

- Folder map: `README.md` (root) and `excel_ai/README.md`; each module folder has its own README.
- Documentation: the website <https://cpmodelai.github.io/cpat_ai/> (sources in `docs/`).
- How-to guides: the setup and tools guide `other/SetupGuide.docx`; the quick start in the mitigation Documentation; the data editions and scripts in `data/README.md`; module guides and prompts in `excel_ai/core/prompts/`.
- Supporting material in `other/`: research papers, decks (`other/presentations/`), distribution notes and earlier prototypes.
- Plans: `excel_ai/core/plans/` (e.g. `Modules.md` for the modular design).
- Python model (Coded CPAT 1.1.0p1.4): `coded/README.md` (`run_model.py`, the Shiny app `app.py`, tests in `coded/cpat_testing/`), its deck and the Coded CPAT tab of the website.
- Personal working folders: `users/`.
