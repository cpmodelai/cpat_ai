# CPAT-AI

Workspace for the World Bank **Climate Policy Assessment Tool (CPAT)**: models of the fiscal, economic, energy and distributional effects of carbon pricing and related climate policy.

## Start here

| You want to... | Go to |
|---|---|
| **A short human-readable orientation** | [`HumanReadme-QuickStart.docx`](HumanReadme-QuickStart.docx) |
| **Use the Excel prototype** (modellers, reviewers) | [`excel_ai/`](excel_ai/README.md): the workbook, the bug-fix register and the deck sit at its top |
| **See what differs from legacy CPAT** | [`excel_ai/BUGS.md`](excel_ai/BUGS.md) (legacy bugs, all fixed) and [`excel_ai/ISSUES.md`](excel_ai/ISSUES.md) (legacy issues, replicated and tracked) |
| **Work on the data** | [`data/`](data/README.md): the tidy tables, the legacy-compatible workbook, the legacy 465 workbook, the master table of data sources |
| **Work on the Python model** (Coded CPAT) | [`coded/`](coded/README.md); its documentation book: the Coded CPAT tab of the website (`docs/`) |
| **Work as an AI agent** | [`AGENTS.md`](AGENTS.md) |

## Layout

```
README.md, AGENTS.md, CLAUDE.md   This page; instructions for AI agents
HumanReadme-QuickStart.docx       Quick start guide for people (Word)
NORMS.md                          Rules for every task (task log, method vs version notes, data)
CAVEATS.md                        Log of every finished task (newest at the bottom)
excel_ai/                         The Excel prototypes (Excel-AI): workbook, register, deck at the top;
                                  mitigation/ (builder, checks, notes), legacy/ (legacy CPAT and fix plans),
                                  releases/, plans/, shared/, templates/
data/                             All data: tidy CSV (source of truth), legacy xlsx, legacy 465, data_sources.csv
coded/                            The Python model (Coded CPAT) and its Shiny app
docs/                             Documentation website: index.html (three tabs: CPAT documentation, CPAT-AI project,
                                  Coded CPAT); CPAT_full_, CPAT_ai_ and CPAT_coded_documentation_qmd/ (Quarto
                                  sources) and the matching _html/ folders (built pages)
other/                            Research papers, other decks, earlier prototypes and notes
users/                            Personal folders
```

**Rule for every model: bugs are never replicated; issues are replicated and tracked.** Legacy CPAT (`data/legacy/`) is the reference for both models; codes are shared between Excel and Python.
