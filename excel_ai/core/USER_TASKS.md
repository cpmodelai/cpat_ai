# Manual tasks for the user (after release 1.1, 2026-10-30)

These need a person: a GitHub admin, Excel on Windows, the CPAT team, or a decision. Each item says what to do and
what to tell the agent afterwards. Source: `TODO.md` (sections 5 and "Open at thread close") and `CAVEATS.md`.

## A. Quick (minutes)

1. **Turn on the documentation website.** GitHub > `cpmodelai/cpat_ai` > Settings > Pages > Build and deployment >
   Source: **GitHub Actions**. Then Actions > *Documentation website* > Run workflow (or push any change to `docs/`).
   The site is then at <https://cpmodelai.github.io/cpat_ai/> (tabs `#documentation`, `#cpat-ai`, `#coded`).
   The workflow already builds both books; only the publish step failed ("Ensure GitHub Pages has been enabled").
2. **Delete the seven old branches** on GitHub (Code > Branches): they still hold the old history with the real
   values (the agent may not delete branches: HTTP 403).
3. **Ask GitHub Support to purge the old pull-request refs** (`refs/pull/*`, 11 of them) and cached views of the old
   commits: only GitHub can remove those.
4. **Accept or reject release 1.1.** If accepted, tell the agent "freeze Public01": it marks the edition frozen in
   `data/editions.csv` (an edition is not changed once released) and tags it.

## B. In Excel on Windows (an hour or two)

5. **Recalculate the legacy copy.** Open `data/Public01/legacy/CPAT 1.0pre_465_Public01.xlsb`, set calculation to
   automatic (or press Ctrl+Alt+F9), let it finish, save (keep .xlsb), and push it (or send it). Its stored results
   still come from the real data. Then tell the agent "rebuild the legacy references": it re-extracts the five
   `xai_legacy_*` tables, and the full check's section 4b can pass.
6. **Excel 365 review of the prototype** (`excel_ai/active_workbooks/CPAT-AI-Mitigation-Prototype_latest.xlsm`):
   opens without a repair prompt, no circular-reference warning, macros run (CheckBatchRun, the store macros, the
   dashboard buttons), LAMBDAs live, ETS goal seek (issue I30). Report anything odd, with a screenshot.
7. **Distribution module** (`CPAT-AI-Distribution-Prototype_latest.xlsm`, same folder): press *Update from
   Mitigation* with the prototype beside it; the Distribution tab should change with the prototype's scenario.
8. **Data link test in Excel** (Power Query does not run here): on ScenarioCompare choose the source
   "Public01 - GitHub (public repository)", press *Update data tables* on Cover; the key results should not change
   (the shipped data are Public01's).

## C. With the CPAT team or data owners

9. **Report the legacy bugs**: send `excel_ai/bugs_and_legacy/Legacy_CPAT_Bugs_v1.1.0.docx` and
   `Tracking_Legacy_Bugs_v1.1.0.xlsx` (details of what to stress in `TODO.md` section 5).
10. **Data requests** outstanding: I98 (GAINS factor paths), I97 (blank VAT cells), I99, I90 (proprietary tables for
    other countries), I95 (historical GHGs 2018-2020).
11. **Private data repository (Full01)**: set up the private edition with the real data in the same structure
    (`data/<edition>/` with `EDITION.json` of type `full-real`), if not done.

## D. Decisions

12. **Policy taxonomy with the FTT policies** (`plans/Policy_taxonomy.md`): your decisions come first.
13. **MTOutputs map review**: 64 guessed and 263 unmapped legacy rows in
    `data/Public01/tidy/xai_mtoutputs_map_465.csv` (column `reason`); confirm or correct, or ask the agent to propose.
14. **MTOutputs scenarios side by side** (TODO E2): confirm the layout before it is built (scenario groups across the
    sheet as on Mitigation, the scenario number at the top of each group driving every lookup).
