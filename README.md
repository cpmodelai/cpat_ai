# CPAT-AI

Workspace for the World Bank **Climate Policy Assessment Tool (CPAT)**: models of the fiscal, economic, energy and distributional effects of carbon pricing and related climate policy.

## Start here

| You want to... | Go to |
|---|---|
| **Use the Excel prototype** (modellers, reviewers) | [`excel_ai/`](excel_ai/README.md): the workbook, the bug-fix register and the deck sit at its top |
| **See what differs from legacy CPAT** | [`excel_ai/BUGS.md`](excel_ai/BUGS.md) (legacy bugs, all fixed) and [`excel_ai/ISSUES.md`](excel_ai/ISSUES.md) (legacy issues, replicated and tracked) |
| **Work on the data** | [`data/`](data/README.md): every data table, the converters, the tests |
| **Work on the Python model** | [`coded/`](coded/README.md) |
| **Work as an AI agent** | [`AGENTS.md`](AGENTS.md) |

## Layout

```
README.md, AGENTS.md, CLAUDE.md   This page; instructions for AI agents
NORMS.md                          Rules for every task (task log, method vs version notes, data)
CAVEATS.md                        Log of every finished task (newest at the bottom)
excel_ai/                         The Excel prototypes (Excel-AI): workbook, register, deck at the top;
                                  mitigation/ (builder, checks, notes), legacy/ (legacy CPAT and fix plans),
                                  releases/, plans/, shared/, templates/
data/                             All data (Python and CPAT formats), converters, tests
coded/                            The Python model (Coded CPAT) and its Shiny app
other/                            Research papers, other decks, earlier prototypes and notes
users/                            Personal folders
```

**Rule for every model: bugs are never replicated; issues are replicated and tracked.** Legacy CPAT (`excel_ai/legacy/workbooks/`) is the reference for both models; codes are shared between Excel and Python.
