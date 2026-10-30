# repository restructure (plan, 2026-10-22; decisions open)

**Request (user 2026-10-22).** The structure and documentation are out of date: build files mixed with human-readable places, legacy names (`copypaste`, `bugfix_procedure`, the old `distribution`), old and previous prototypes, a separate root `documentation/` folder that confuses. A total rethink.

## What is there (2026-10-22)

| Where | Files | Size | Problem |
|---|---|---|---|
| `excel_ai/mitigation/` (top) | 76 | | 36 scripts, 33 notes, workbook, reports in one folder; every name carries a version (`_v7_0`, `_v7_2`) |
| `.../mitigation/Old/` | 3,701 | 646 MB | every earlier script, note, workbook (69 .xlsm), already in git history |
| `.../presentation/` | 394 | | deck builder and screenshots of every version |
| `excel_ai/old/`, `standalone_initial_prototypes/`, `tecp_and_validation/`, `bugfix_procedure/` (v0.6.4 variants), `distribution/` (the pre-prototype distribution pipeline) | 131 | 230 MB | earlier prototypes and procedures, not current |
| `documentation/` (root) | 119 | 112 MB | decks and Word outputs, legacy fix plans with their tools and JSON, research PDFs; method notes live elsewhere |
| Root notes | | | `NORMS.md` (120 lines) and `NORMS.md` (509), `CAVEATS.md` (2,811 lines), `Plans.md` (1,500) |
| `.git` | | 966 MB | the binaries of every release |

## Principles

1. **One folder per product, self-contained**: what it is (README), the workbook, its sources, its checks, its documents. A reader finds everything for a model in one place; nothing generated sits beside a hand-written note.
2. **Versions live in git, not in file names**: scripts and notes have stable names (`build.py`, `check_full.py`, `Methods/Prices.md`); a release is a git tag (`mitigation-v0.8.0`) and a versioned workbook in `releases/`. No `Old/` folders: the history and the tags keep every earlier file. (Replaces NORMS 5's versioned names and `Old/` rule.)
3. **Separate what people read from what machines run**: `docs/` (hand-written and generated documents) vs `src/` (builders, VBA, deck builder) vs `checks/` (check scripts and their latest reports).
4. **Legacy CPAT and archived work in one clearly named place each**: `legacy/` (the reference workbook, codes master, tracker, our cell-level fix plans), `archive/` (earlier prototypes, kept only if still useful; otherwise only in history).
5. **Names say what things are**: prototype (not prototype), module names (mitigation, distribution, air_pollution, transport_cobenefits), no `copypaste`.

## Target layout

```
README.md                 What CPAT-AI is, the products, start here (one page)
AGENTS.md, CLAUDE.md      AI instructions (pointer)
NORMS.md                  One norms file (root + Excel norms merged, current rules only)
CHANGELOG.md              Releases (one line per release, newest first); CAVEATS.md stays the task log
mitigation/               The mitigation prototype
  README.md               What it does, how to use it, how to build and check it
  CPAT-AI-Mitigation_latest.xlsm   Stable name, rewritten by every build (modules link to it)
  releases/               Released workbooks (latest few; earlier ones by git tag)
  docs/                   Quick start, methods (one note per topic), equations, the Word documentation and core deck
  src/                    build.py, vba/CPATScenarios.bas, extract_*.py, deck/ (builder, screenshots)
  checks/                 check_quick.py, check_full.py, check_codes.py, check_paste.py, check_links.py, reports/
distribution/             The standalone distribution module (same sub-layout); its own releases
air_pollution/            Module v0.1 (data import and export only)
transport_cobenefits/     Module v0.1 (data import and export only)
shared/                   Python used by every module: LibreOffice session, VBA embedding, codes map, lint
legacy/                   Legacy CPAT: the reference workbooks, codes master, issue tracker; bug register sources,
                          cell-level fix plans (Word, PDF, JSON, tools) and the bug-fix procedure
data/                     Today's data (all data, converters, tests)
coded/                    Today's coded (Python model)
docs/                     Cross-cutting only: the bug and issue register (Word), decks for audiences, research PDFs, plans
archive/                  (optional) the few earlier prototypes worth keeping visible; everything else only in history
users/
```

The separate root `documentation/` disappears: each product's documents move into its own `docs/`; what concerns all products (the register of legacy bugs, audience decks, research, plans) goes to root `docs/`.

## Mapping (main moves)

| From | To |
|---|---|
| `excel_ai/mitigation/build.py`, `CPATScenarios.bas`, `extract_*`, `make_*` (build side) | `mitigation/src/` (stable names) |
| `check_*_v7_0.py`, `check_report_*.md`, `check_quick_report_*.md` | `mitigation/checks/`, reports in `checks/reports/` |
| `*_Method_v7_0.md`, `QuickStart`, `Equations`, `Formulas`, `DataTabs`, `Transport_*` notes | `mitigation/docs/` (stable names; generated ones marked as generated) |
| `presentation/` | `mitigation/src/deck/` (builder), deck output in `mitigation/docs/` |
| `lo_session`, `lo_run_macro`, `vba_project`, `excel_lint.py`, `xlsb_*` | `shared/` |
| `documentation/*_Documentation_*.docx`, `*_Overview_*.pptx` | `mitigation/docs/` |
| `documentation/*_BugsAndIssues_*.docx`, `excel_ai/bugs_and_legacy/fixes/`, `excel_ai/bugs_and_legacy/fixes/procedure/BugFixProcedure.md`, `LegacyBugFixes`, `Replicated`/`NotReplicated` lists, `issues_register` | `legacy/` (register sources and outputs; the two lists stay linked from the root README) |
| `excel_ai/bugs_and_legacy/workbooks/` | `legacy/workbooks/` |
| `other/research/`, `presentations/`, `more/` | `docs/research/`, `docs/decks/`, `docs/` |
| `Plans.md`, `TODO*.md`, `Codes_Remediation_Plan`, `CPAT_CodesMap` | `docs/plans/` (one file per plan) and `mitigation/TODO.md` |
| `Old/`, `excel_ai/old/`, `standalone_initial_prototypes/`, `tecp_and_validation/`, `distribution/` (pre-prototype pipeline), `bugfix_procedure/` variants | removed from the tree (git tag `archive-2026-10` keeps them); anything still used moves first |
| `data/`, `coded/` | `data/`, `coded/` (paths updated in scripts and tests) |

## Steps (after the v0.7.2 full check; before the modules, so they are born in the new layout)

- **S0 - inventory and tag**: tag `archive-2026-10`; list every file the current builds, checks and documents read (a script trace), so nothing in use is removed.
- **S1 - move and rename** in one commit per product (git mv keeps history): mitigation, legacy, docs, shared, data, coded; scripts get stable names and a `PATHS` module instead of hard-coded `../..` paths; the full build and quick check run from the new place.
- **S2 - remove** `Old/` folders and the archived folders from the tree.
- **S3 - documents rewritten, not patched**: root README (one page), each product README (use, build, check), one NORMS (current rules only; history of rules to CAVEATS), CHANGELOG from the version log; "prototype" -> "prototype" everywhere (merges with modules step M0, which then needs no file renames).
- **S4 - checks**: quick check, full check, paste and links tests from the new layout; a link check over every Markdown file (no broken relative link).
- **Then** the modules plan (section 9), M1 onwards, in the new layout.

## Decisions (user 2026-10-22; they replace the target layout and decisions above where they differ)

1. **No `documentation/` folder.** Excel documents go into `excel_ai/`; everything else (research, other decks, `more/`) into `other/`.
2. **No `cpat_` prefix**: `excel_ai` -> `excel_ai` (user 2026-10-22: a name with AI; underscore as the other folders), `data` -> `data`, `coded` -> `coded` (every path in scripts, tests, READMEs and NORMS updated).
3. **`excel_ai/` shows three main files at its top**: the latest prototype workbook, the bug-fix documentation (the register of bugs and issues, Word) and the integrated slide deck. The integrated mitigation tool is the special one and is shown there; its sources live in `excel_ai/mitigation/` (src, checks, docs). Modules in `excel_ai/distribution/`, `excel_ai/air_pollution/`, `excel_ai/transport_cobenefits/`; `excel_ai/core/tools/`, `excel_ai/bugs_and_legacy/` as above.
4. **`BUGS.md` and `ISSUES.md`** (short names, in `excel_ai/`) replace `BUGS.md` and `ISSUES.md`.
5. **History removed**: the repository restarts from one commit of the cleaned tree (966 MB of history dropped; nobody else works on it yet). Dropped outright, no archive (user 2026-10-22).
6. **Versioned and latest copies, both kept**: each main file exists twice with equivalent contents, `..._v0.8.0` and `..._latest` (workbook, register, deck); the version table (the workbook's version log) is the same in both, and `excel_ai/<module>/releases/.md` lists every release (version, date, summary, files). The `_latest` copies sit at the top of `excel/`, the versioned copies of every release from v0.7.2 on in `excel_ai/<module>/releases/`. Scripts and notes keep stable names (the git tag of each release marks their state).
7. **When**: as soon as it is safe, i.e. right after the v0.7.2 full check has passed and v0.7.2 is on main, with no build or check running; before the modules (plan section 9), so the modules start in the new layout.

## Target layout (as decided)

```
README.md, AGENTS.md, CLAUDE.md, NORMS.md (one, merged), CAVEATS.md
excel_ai/
  README.md                                   Start here
  CPAT-AI-Mitigation-Prototype_latest.xlsm    The integrated tool (stable name; modules link to it)
  CPAT-AI_BugsAndIssues_latest.docx           Bug-fix documentation: every legacy bug and issue, fix plans
  CPAT-AI_Overview_latest.pptx                The integrated slide deck
  BUGS.md, ISSUES.md                          The two short lists (generated)
  releases.md, releases/                      Every release from v0.7.2: the three files with _v<n>, one table
  mitigation/   src/ (build, VBA, extractors, deck builder), checks/ (and reports/), docs/ (quick start,
                methods, equations, formulas, the Word documentation)
  distribution/, air_pollution/, transport_cobenefits/   Modules (same sub-layout, own releases)
  shared/       LibreOffice session, VBA embedding, codes map, lint
  legacy/       Legacy CPAT workbooks, codes master, tracker; cell-level fix plans (Word, PDF, JSON, tools);
                bug-fix procedure; register sources
  plans/        Plans and TODOs (one file per plan)
data/           (was data)
coded/          (was coded)
other/          Research PDFs, other decks (AI and climate fiscal tools), more/
users/
```

## Documents and scripts after the restructure (user 2026-10-22)

- **One Word bug-fix document**: the register (`CPAT-AI_BugsAndIssues_latest.docx`, with every cell-level fix plan inside); the five separate fix-plan Word files and their PDFs are dropped (their JSON and tools stay in `legacy/` as sources). **The register spreadsheet stays** (one filterable table). `BUGS.md` and `ISSUES.md` stay; `LegacyBugFixes`, `NotReplicated`, `Replicated` copies and `BugFixProcedure.md` go (inside the register).
- **Method notes merged, 13 -> 6**: Prices; Power; Transport; Emissions; ETS; Macro and results (Distribution's note to the Distribution module).
- **Main documentation: simple and well structured, not everything in** (user: "a firehose of information; we humans can't cope"). Target about 20 pages: 1. what the tool is and what it answers (1 page); 2. quick start (2 pages); 3. how it works: one short section per block (policies, prices, demand, power, transport, revenues, emissions, macro) with the few key equations and a pointer to its method note (about 1 page each); 4. results and the dashboard (2 pages); 5. limits and differences from legacy: a pointer to the register, no lists. Out of it: every formula (`Formulas` stays a generated reference), legacy surveys, version history, bug lists, plans.
- **Scripts**: stable names; one `make_documents.py` entry for every document; one-off extractors and tools to `legacy/tools/`; about 20 scripts for build, checks and documents.
- **Two Word documents for mitigation** (user 2026-10-22), both generated from Markdown notes in the repository, in `excel_ai/mitigation/`: the **main documentation** (about 20 pages, as above; each block ends with "details: Methods, chapter X") and **Methods** (the 6 merged method notes as chapters, the full equations as an appendix; for someone checking or changing the model).
