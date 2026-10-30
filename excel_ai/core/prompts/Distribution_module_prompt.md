# Prompt: bring the distribution module up to the module norms (v0.1.4)

The distribution module already exists (`excel_ai/CPAT-AI-Distribution-Prototype_v0.1.3.xlsm`, sources in `excel_ai/distribution/`). This prompt does not rebuild it: it links it through `active_workbooks/`, checks it against legacy, and closes the open items of the module norms. Paste this whole file into GitHub Copilot (Current checkout, Interactive, Claude Opus), with `@AGENTS.md` attached, or attach this file and type "Follow this file. Do phase 0 only, then stop and report." Work one phase per message. Human guide: `CPAT-AI_HowTo_Distribution.docx` in this folder.

---

You are working in the CPAT-AI repository on the local checkout. Follow `AGENTS.md` and every document it points to, above all `NORMS.md` section 0 (bugs and issues), section 1.1b (the distribution layout) and **section 9 (how modules work)**. Read before you start: `excel_ai/distribution/README.md`, `build_distribution.py`, `CPATDistribution.bas`, `check_distribution.py` and its last report; `excel_ai/core/plans/Modules.md` (M3, M6); the distribution items of the register (`excel_ai/legacy/register/issues_register.py`, Module = Distribution; former codes D1-D31, DI1-DI4) and of `excel_ai/core/BUGS.md` and `excel_ai/core/ISSUES.md`; `other/distribution/LESSONS_LEARNED.md`; `excel_ai/mitigation/checks/distribution_ref.py`; the bottom of `CAVEATS.md`.

## Rules (do not break them)

1. **Legacy first** (the legacy `Distribution` sheet of `data/legacy/CPAT 1.0pre_465_Shell.xlsb`, read-only). Never replicate a legacy bug: fix it and register it (`L`, with cells and a cell-level fix plan). Always replicate a legacy issue and register it (`I`). When unsure, treat it as an issue, replicate it, and ask me. Next free codes from `register.py`; one register, no list of your own.
2. **The distribution formulas have one source**: `excel_ai/mitigation/build.py`. The module is cut from the built prototype. Change a formula there, rebuild the prototype, then rebuild the module; never edit the module workbook by hand.
3. **Column norms**: the distribution layout of `NORMS.md` 1.1b (A-J descriptors as Mitigation; per group a code column, basket, deciles 1-10, spacer; group *n* reads Mitigation group *n*); `FromMitigation` keeps the Mitigation column layout (1.1, 9.2).
4. **Encapsulated**: the `Distribution` sheet reads only `FromMitigation`, `ScenarioDefinition`, its data tabs and Settings constants (NORMS 9.2); its results stay on the `Distribution` sheet under the LiveOutputs codes `<iso>.distn.*`, because no other workbook reads them yet (an output tab of plain copies, NORMS 9.2, is added only if I agree).
5. Excel rules as `NORMS.md` 3, 3b, 3d, 3g, 3h. If Python, openpyxl or LibreOffice is missing on this computer, say so before you start: install nothing without my OK; where LibreOffice is missing, skip the recalculation steps and list what was not run (I review in Excel 365). Never commit real data. Do not commit or push unless I ask.

## Phases (one per message; stop after each and report)

**Phase 0. Review (no change).** Build nothing. Report: (a) how the module meets `NORMS.md` section 9, item by item, and what is missing; (b) the macro's file search (it looks for the mitigation workbook next to the module, in `permalink\`, one folder up, then in `permalink\` one folder up: it does **not** look in `permalink_countryeditable\` yet, NORMS 5a and 9.3); (c) the distribution bugs and issues in the register on 465 (any legacy 465 change to the `Distribution` sheet since 456: rows moved, bugs the CPAT team fixed); (d) the date and result of the last `check_distribution.py`; (e) the Cover: its title and version log still use the old numbering (v1.3 for 0.1.3) and not the version-table columns of NORMS 5b (Version, Date, Description, Max abs regression diff).

**Phase 1. Link through `active_workbooks/`.** In `CPATDistribution.bas` (`MitPath`): look first in `active_workbooks/` (was `permalink_countryeditable\` (next to the module, then one folder up), then the current places; Cover says which file was used (link table: path, saved time, scenario names). Same change in the builder's Cover text and README. Test the search order with a Python emulation of the macro and the VBA name scan of `check_distribution.py`.

**Phase 2. Legacy check on 465.** Compare the module (Egypt, the scenario of the prototype) with legacy 465's cached `Distribution` values and `MTOutputs` distribution results, decile by decile, through `distribution_ref.py`; every difference explained by a registered bug fix or issue, or reported as new. Register what is new.

**Phase 3. Release.** Bump `VERSION` to 0.1.4, rebuild (`python excel_ai/distribution/build_distribution.py`), run `python excel_ai/distribution/check_distribution.py` (PASS), lint, publish with `release.py` `publish(link=True)` to `excel_ai/`, `releases/`, `active_workbooks/` and `active_workbooks/`. Cover title and version table in the 0.1.x numbering and the NORMS 5b columns, with a row naming the mitigation version used. Update `excel_ai/distribution/README.md`, `excel_ai/core/TODO.md` (M6: distribution done), the register lists, and add the entry at the bottom of `CAVEATS.md`.

## Report after each phase

What you did; files changed; check results (PASS/FAIL with numbers); bugs and issues (codes); open questions for me. Do not go to the next phase until I say so.
