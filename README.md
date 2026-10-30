# CPAT-AI

Workspace for the World Bank **Climate Policy Assessment Tool (CPAT)**: models of the fiscal, economic, energy and distributional effects of carbon pricing and related climate policy.

## Start here

| You want to... | Go to |
|---|---|
| **A short human-readable orientation** | [`QuickStart.docx`](QuickStart.docx) |
| **Use the Excel prototype** (modellers, reviewers) | [`excel_ai/active_workbooks/`](excel_ai/README.md): the current workbooks; the bug book, tracker, codes map and deck sit at the top of `excel_ai/` |
| **See what differs from legacy CPAT** | [`excel_ai/core/BUGS.md`](excel_ai/core/BUGS.md) (legacy bugs, all fixed) and [`excel_ai/core/ISSUES.md`](excel_ai/core/ISSUES.md) (legacy issues, replicated and tracked) |
| **Work on the data** | [`data/`](data/README.md): the data editions (`Public01` here), the catalogue of every table, the legacy workbook shell |
| **Work on the Python model** (Coded CPAT) | [`coded/`](coded/README.md); its documentation book: the Coded CPAT tab of the website (`docs/`) |
| **Work as an AI agent** | [`AGENTS.md`](AGENTS.md) |

## Layout

```
README.md                         This page
AGENTS.md, CLAUDE.md              The entry point for AI agents (routes to each project's rules)
QuickStart.docx                   Quick start guide for people (Word)
excel_ai/                         The Excel prototypes (Excel-AI): active_workbooks/ (the current workbooks),
                                  core/ (rules, task log, bug lists, TODO, plans, prompts, tools),
                                  mitigation/, distribution/, air_pollution/ (each with releases/), legacy/
data/                             All data, as editions (data/Public01/), the catalogue, the legacy shell, scripts
coded/                            The Python model (Coded CPAT) and its Shiny app
docs/                             Documentation website: index.html (three tabs: CPAT documentation, CPAT-AI project,
                                  Coded CPAT); CPAT_full_, CPAT_ai_ and CPAT_coded_documentation_qmd/ (Quarto
                                  sources) and the matching _html/ folders (built pages)
other/                            Research papers, other decks, earlier prototypes and notes
users/                            Personal folders
```

**Rule for every model: bugs are never replicated; issues are replicated and tracked.** Legacy CPAT (`data/legacy/`) is the reference for both models; codes are shared between Excel and Python.
