# AGENTS.md - the entry point for any AI agent working in this repository

Tool-neutral (Claude, Codex, Gemini, Copilot, Cursor, ...); `CLAUDE.md` points here. This file routes only: the rules live in each project's own documents.

## The repository

Workspace for the World Bank **Climate Policy Assessment Tool (CPAT)**. People start at [`README.md`](README.md).

| Folder | What it is | Read first |
|---|---|---|
| `excel_ai/` | **Excel-AI**: the Excel prototypes (mitigation, distribution, air pollution), the legacy bug register | [`excel_ai/core/AGENTS.md`](excel_ai/core/AGENTS.md): its rules, records and plans are all in `excel_ai/core/` |
| `coded/` | **Coded CPAT**: the Python model and its Shiny app | [`coded/README.md`](coded/README.md), [`coded/NORMS.md`](coded/NORMS.md), [`coded/TODO.md`](coded/TODO.md) |
| `data/` | **All data**, as editions (`data/editions.csv`; `data/Public01/` here), the legacy workbook shell, the data scripts | [`data/README.md`](data/README.md) |
| `docs/` | The documentation website (Quarto sources and built pages) | `docs/index.html` |
| `other/` | Research, earlier prototypes, notes | - |

## Rules that hold everywhere

- **Never replicate a legacy bug; always replicate a legacy issue, and track it** ([`excel_ai/core/NORMS.md`](excel_ai/core/NORMS.md) section 0; lists [`excel_ai/core/BUGS.md`](excel_ai/core/BUGS.md), [`excel_ai/core/ISSUES.md`](excel_ai/core/ISSUES.md)).
- **Data:** six tables are proprietary (Balances, EnergyCons, Prices_dom, IO_GTAP, HHSurvey, Tran_Scatter). This repository holds them only perturbed, never real; real data live in the private data repository ([`data/README.md`](data/README.md)).
- **Every finished task** ends with an entry in the project's log ([`excel_ai/core/CAVEATS.md`](excel_ai/core/CAVEATS.md) for Excel-AI and data; Coded CPAT: `coded/CHANGELOG.md` and `coded/TODO.md`).
- **Do not commit unless the user asks.**

## Keeping this file useful

Routing only. A rule for one project goes in that project's documents; a rule for every project goes in the section above, briefly, pointing to where it is explained.
