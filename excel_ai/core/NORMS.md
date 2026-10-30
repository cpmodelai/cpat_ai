# CPAT-AI Norms

Rules for every task in this repository. Sections 0-5: the Excel prototypes (`excel_ai/`); sections 6-8: every task (Excel, Python, data, documents). Python conventions: [`coded/README.md`](../../coded/README.md).

| Section | Contents |
|---|---|
| 0 | **Replication rule: never replicate bugs, always replicate issues (and track them)** |
| 1 | Column norms |
| 2 | Visual style guide |
| 3, 3b-3j | Formulas, codes, encoding and LAMBDA rules, results, names, copy-paste, overnight runs, Excel repair prompts, VBA, LibreOffice testing, lessons register |
| 4 | Policy and parameter inputs (ScenarioDefinition) |
| 5 | Versions, releases and documents |
| 6, 6b | Task completion (CAVEATS.md) and norms that follow the lessons |
| 7 | Methodology and version notes are different documents |
| 8 | Data |
| 9 | **Modules: how they work** (free-standing module workbooks, inputs and outputs, links through `active_workbooks/`) |

## 0. Replication rule: never replicate bugs; always replicate issues, and track them

User rules 2026-10-15, 2026-10-28 (one register for every module) and 2026-10-29 (data problems are issues). It decides every difference between a prototype and legacy CPAT, in every module (mitigation, distribution, air pollution, transport co-benefits, the inputs).

| | Bug | Issue |
|---|---|---|
| **What it is** | Legacy does not do what it means to: a wrong row or cell reference, a term applied twice, a dead or blank reference, a sign error, a formula that contradicts its label or the CPAT documentation | Legacy does what it means to, but the choice is open to question: old data, a data vintage, a simplification, a design choice, a missing feature, a result nobody can explain yet |
| **What we do** | **Do not replicate it.** Fix it (or leave the feature out) | **Replicate it.** Do exactly what legacy does |
| **Exceptions** | none: a bug is never replicated | An issue we do not replicate is allowed **only by explicit user decision**, recorded with the issue. Without that decision it is queued to be replicated |

**Data (user rule 2026-10-29, v0.8.5).** Problems of the input data are **issues** (area Data), with the same rule: the prototype does exactly what legacy does with the data, unless the user decided otherwise.

- Where legacy reads the data wrongly (for example a blank read as 0 where a value is meant), the fix is a formula change: a **legacy bug (`L`) with a cell-level fix plan**, and the data problem stays an issue with priority **Very high**.
- Where no cell plan is possible (legacy's formula is not wrong; the data are missing or poor), the prototype **aligns with legacy** and the issue gets priority **Extremely high**.
- A data choice the user wants kept (for example the corrected Egypt prices) is an issue that departs from legacy by user decision.
- The codes `DB` (data bug) and `DI` (data issue) of v0.8.4 are retired (now `I89`-`I99`, `L170`; former codes kept).

**Codes, the same in every module** (one kind per prefix; a module or area is a field, not a prefix):

| Code | Kind |
|---|---|
| `L` | Legacy bug (any module, including the inputs and the data), with a cell-level fix plan where one is possible |
| `M` | Prototype bug (a defect of the prototype itself: fixed, or open where Coded CPAT found it; never replicated in Coded CPAT, rule 6) |
| `DOC` | Documentation bug (user 2026-10-29): the CPAT methodology documentation (`docs/01_MainDocumentation/`) is wrong, missing or contradicts itself (an equation, a sign, a symbol, a unit, a reference). No model is affected; the fix is a correction of the documentation. `DOC`, not `D`: `D1`-`D31` were the former distribution bug codes |
| `I` | Issue (replicated, a departure by user decision, or a limitation of the prototype; data problems in area Data). Priority: Minor, Major; data problems Very high or Extremely high |
| `LD` | Departure: a row of the LegacyDiff sheet that is not "Same" |
| `U` | Upgrade |

Rules that follow:

1. **Default is legacy.** When in doubt whether something is a bug or an issue, treat it as an issue (replicate it), register it, and ask the user.
2. **Never "improve" legacy silently.** A better method, newer data or a cleaner design is an issue, not a bug: replicate legacy, and propose the improvement as an upgrade (`U` item) for the user to decide.
3. **One register, stored the same way for every module.** Every bug found and every issue met goes in the register the same day: data in `excel_ai/bugs_and_legacy/register/issues_register.py` (bugs as `L` items with priority and fix in `make_legacy_fixes.py`; issues with severity or priority, status, next step and legacy side in `ISSUE_STATUS`, `ISSUE_LEGACY`; the data problems listed in `DATA_ISSUES`), read through `register.py`, which gives every item the same fields (code, former code, kind, module, area, title, where, description, fix or plan, effect, priority, in the prototype, status, legacy 465, see also, documented in). A departure also gets a row in sheet LegacyDiff. A module with its own bugs (distribution, air pollution, ...) adds them to the same register with the same codes; it keeps no list of its own.
4. **Where each kind is kept.** The master list is the tracker `excel_ai/bugs_and_legacy/Tracking_Legacy_Bugs_v<version>.xlsx` (tabs Bugs: L, M; Issues: I, LD, U; then the CPAT team's tabs, kept as they are). Legacy bugs are documented in `excel_ai/bugs_and_legacy/Legacy_CPAT_Bugs_v<version>.docx`, which opens with this rule, a stock table of every legacy bug found and fixed and the data problems by priority; issues, departures, prototype bugs and upgrades in the appendices of the Documentation. `excel_ai/core/BUGS.md` and `excel_ai/core/ISSUES.md` are the short lists. All are regenerated at every release from `register.py` (`make_tracker.py`, `make_bugfix_book.py`, `make_docs.py`, `make_replication_lists.py`).
5. **Cross-reference everywhere.** Every entry gives its code, its former code where it was renumbered, and the codes it relates to (a data issue and the bug that fixes it, an issue and its LegacyDiff row). Codes are never reused; a renumbering keeps the former code in `FORMER`.
6. **Coded CPAT and the prototypes (user rules 2026-10-29).** The rule of this section holds between Coded CPAT (`coded/`) and the prototypes too: **a prototype bug (`M`) is never replicated in Coded CPAT; an issue (a potential improvement) is logged for later and replicated for now.** When Coded CPAT finds a prototype bug, the same day: (a) register it as an open prototype bug (`M`, status Open, with where, fix and effect: `OPEN_PROTO_BUGS` in `issues_register.py`; listed in `BUGS.md` section 2); (b) add its fix to the Excel-AI TODO list (`excel_ai/core/TODO.md`, with a fix brief in `excel_ai/core/plans/` when there are several); (c) fix it in Coded CPAT where the fix is obvious, list the codes that then differ from the prototype's stored values in `coded/cpat_testing/compare/known_differences.py`, and note it on `coded/TODO.md`; where the fix is not obvious, Coded CPAT keeps the prototype's formula until the prototype's fixed version shows the fix (`coded/TODO.md` says so). When the prototype is fixed: the item moves to the fixed `M` bugs (`MVP_BUGS`, found / fixed in), Coded CPAT aligns with the prototype's fix in its release for that version, the known differences are deleted (the codes must match again), and `coded/TODO.md` notes the Excel-AI version. A registered bug found not to be one is withdrawn (kept in the register as withdrawn, with the reason) and Coded CPAT follows the prototype again. Then check legacy: if legacy has the same defect, cross-reference the legacy bug (`L`) or register a new one with its cell plan (example: `excel_ai/core/plans/Fix_prototype_bugs_M15-M22.md`).

## 1. Column norms

Match the legacy CPAT column positions exactly so formulas, lookups and Python mappings port 1:1.

### 1.1 Mitigation-layout calculation sheets (e.g. `Mitigation`, kernels)
Matches legacy `Mitigation` exactly. Row 1 = column headers; row 2 = title band; sections start row 3.

| Col | Header |
|---|---|
| A | (section no.) |
| B | Fuel |
| C | Sector |
| D | Description |
| E | Unit |
| F | Source |
| G | Input Code |
| H | Output Code |
| I | Note |
| J | Helper |
| K | Code column of scenario group 1 (`Scenario 1: output code` in row 1) |
| L..AE | Years **2022..2041** (L = base year 2022, as legacy; AE = 2041, the legacy horizon) |
| AF | Blank spacer; scenario group *n* starts at column K + 22 x (n - 1) (group 2 in AG, group 3 in BC, ...; 3e) |

Reference implementation: the `Mitigation` sheet of `excel_ai/CPAT-AI-Mitigation-Prototype_v<version>.xlsm` (constants `COL_G0`, `GW`, `BASE_YEAR`, `LAST_YEAR` in `excel_ai/mitigation/build.py`; corrected 2026-10-29: this table said K..AI = 2021..2045). The module workbooks (section 9) use the same columns.

### 1.1b Distribution-layout sheets (`Distribution`; user decisions 2026-10-17, mitigation prototype v0.4.4)
Distribution is a short-term, single-year analysis (to 2030), close to legacy's outputs. The sheet keeps Mitigation's rows, descriptor columns and scenario logic, with a narrower column group:

| Col / row | Content |
|---|---|
| A-C | Variable, item (fuel or consumption category), sample (`Overall`, `Urban`, `Rural`) |
| D-E | Parameters: data variable, sample label |
| H, I, J | Description, unit, source (legacy rows) |
| Group | Code column, basket, deciles 1-10, spacer (13 columns), from column K; up to 7 groups (scenario capacity, 3e) |
| Row 1 | Header: `Scenario n: output code` in the code column, `Basket`, `1` ... `10` |
| Row 4, 5 | Scenario name, scenario number (the same formulas as Mitigation) |
| Rows 6-12 | Position of the group, Mitigation column of the analysis year (group 1, this group), statistic, survey code parts (rows 10-11), analysis year (row 12, the summary of section 0; v0.4.8). Mitigation column offset of the group: (position - 1) x Mitigation group width + analysis year - base year + 2, where position counts every group header from `$K$1` (`COUNTIF($K$1:K$1,"*output code")`, the LAMBDA test group included) |

Roll-up and columns (v0.4.8, user request): as Mitigation (2.5): one row group per section, the summary row last and one blank row visible; columns C:G and I:K in one column group each, rolled up; zoom 75.

1. **One analysis year and one statistic per scenario**, from ScenarioDefinition (`YearDistn`, `QuantilesStatistic`; legacy `dist.year`, `dist.stat`), normally the same for all. The year can be 2023-2030. Price changes compare the group with scenario 1 in the group's own analysis year.
2. **Group *n* is Mitigation group *n*.** Section 1 reads every Mitigation input with `INDEX(Mitigation!$K$r:$IZ$r, <col>$6)`. Nothing else reads Mitigation.
3. **Basket and deciles in one row.** Every cell refers to its own column (scalars are repeated across the deciles), so a group copies as a block. Three row kinds:
   - **Decile rows:** one formula across all 11 value columns; the decile comes from row 1 (`Basket` = 0).
   - **One-value rows** (settings, prices, totals): the value in the basket column, repeated across the deciles (`=` the cell on the left).
   - **Decile-only rows** (recycling): the basket column is blank.
4. **Samples:** Overall for every item. Urban and Rural rows only where legacy outputs them (total effect, recycling, Gini, compensation).
5. **Differences against scenario 1** as Mitigation (3e rule 2). Effects are against scenario 1 by construction: group 1 shows baseline levels and zero effects.
6. **LAMBDA group** as Mitigation (section 3): group 2, the live scenario, calls the named LAMBDAs; group 1 (the baseline) holds plain formulas.
7. **Outputs** go to the MTOutputs scenario blocks (legacy MTOutputs order) under the prototype's codes (`<iso>.distn.*`, legacy code in column F), deciles 1-10 in K:T.

### 1.2 Time-series data sheets (e.g. `Power`)
- Columns A-E: descriptors (section / methodology / unit / data level / source in the documentation header block; `Data section`, `Methodology` in C, `Unit` in K, `Data level` in N, `Data source` in P).
- Year headers start in **column F = 2000**, one column per year thereafter (F=2000, G=2001, ...).

### 1.3 Country-year data sheets (e.g. `Prices_dom`, `EnergyCons`)
- Row-banded header: `Fuels:` / `Sectors:` / `Indicators:` / `Units:` in column A (rows 4-7), then code row.
- Key columns: `country_year` (A, e.g. `EGY2021`), `countrycode_weo` (B), `countrycode` (C), `countryname` (D), `year` (E); data from F.
- Variable codes follow `mit.<indicator>.<fuel>.<sector>` (e.g. `mit.sp.coa.pow`).
- Sector codes: `pow, ind, res, rod, ral, avi, nav, foo, srv, mch, ...`; fuel codes: `coa, nga, gso, die, lpg, ker, jfu, ecy, bio, oop` (corrected 2026-10-23: legacy uses `nga` and `ecy`, not `gas` and `ele`; code protocol: `excel_ai/bugs_and_legacy/reference/codes_v0_7_1/CPAT_CodesMap_v0_7_1.xlsx`, sheet Protocol). **`tot` and `all` (user decision 2026-10-21, protocol C5):** `tot` is a total over members (a row whose year formula is an explicit SUM, SUMIF or SUMIFS, and a share, rescaling or copy of such a total); `all` only fills a slot the variable does not break down (e.g. `em.tra.all.pm2`: the group code `tra` names the aggregate, there is no fuel dimension). The quick check fails an explicit-sum row coded `all` (C5), except a code the legacy rename map fixes (`code_renames_v0_7_2.csv`). Audit 2026-10-29: no exception left; the vehicle stocks are `pass.own.tot`, `fre.own.tot`, `motor.own.tot` and their sum `tot.own.tot` (user 2026-10-29, v1.0.2; were the legacy MTOutputs codes `*.own.all`).

### 1.4 Sheet order and naming
Follow the legacy tab order: `Cover`, `Data sources`, `Dashboard`, `Manual inputs`, `MODULES->` (`Mitigation`, `Air pollution`, `Distribution`, `Transport`), then `DATA_*->` dividers followed by data tabs. Prototype workbooks keep the same sheet names as the legacy tab they replicate. Each workbook starts with a `Cover` tab (contents, colours, abbreviations; 2.7); the mitigation prototype keeps its about text on tab `Version Log, About, and Diff`.

### 1.5 Data tabs: legacy groups, legacy tables, all-country ranges (user request 2026-10-17, mitigation prototype v0.4.5)
The full legacy data (all countries, partly proprietary) must be usable by pasting it in. The public copy holds Egypt only for the proprietary tables; the model must work unchanged when they are expanded.

1. **Groups and order as legacy.** Data tabs sit under the legacy dividers in legacy order: `DATA_MITIGATION->>` (Power tabs, GHGs, Countries, ECP, Balances, EnergyCons, CH4Inputs, UNPop, Prices_int, Prices_dom, Elasticities, ETSSemi, WEO, EF_GHG, SCC, EF_PM), `DATA_DISTN->>` (DistMapping, IO_GTAP, HHSurvey, HH_Elast, ASPIRE, WHOCooking, GDPRatios), `DATA_TRAN->>` (Transport1-3, TransportParams, TransportPaths), `DATA_OUTPUT->>` (Multipliers). Tabs with no legacy data tab go last under `DATA_OTHER->>`.
2. **Legacy tables unchanged.** Where a tab matches a legacy data table, the legacy table is reproduced unchanged (same columns, same order, same codes): header in row 3, data from **A4**, so the legacy table pasted at A4 replaces it. Rows 1-2 carry the title bar (2.7).
2b. **Tabs with several legacy tables stay at their legacy cell addresses** (v0.4.6: Countries, Elasticities, ETS+LTS, Multipliers, Prices_int, ECP; Transport3 from row 5; v0.4.7: Power, CoC, GHGs): rows 1-2 are the workbook's source line and title bar, everything from row 3 keeps its legacy address, so the legacy tab pasted from row 3 replaces it. Lookups into them use legacy addresses or legacy row numbers, as legacy does.
2c. **Country selection is a data step.** What legacy Mitigation computes from a data tab for the selected country (the country's column of Elasticities, its multipliers, its WEO series and their extension, its ECP rows, the international price series) is a block of the Inputs tab (Inputs_ela, Inputs_mult, Inputs_macro, Inputs_pint, Inputs_ecp, Inputs_ef; v0.4.7, the power data of legacy Mitigation section 4: Inputs_pset, Inputs_ptech, Inputs_ppath, Inputs_ppar), formulas only, keyed as before, so Mitigation formulas do not change and every value follows Settings C4.
3. **Keys to the right.** Where legacy has no unique key column, the workbook adds one as a formula column right of the table (e.g. Balances `country|flow`), prefilled to the capacity of its named range, in the help font. It is never inside the pasted block.
4. **Egypt-only tables alone or at the bottom.** A table that holds Egypt only (because the full table is proprietary) is the only table on its tab, or the last table on it, so that pasting all countries can extend it downwards.
5. **Ranges sized for all countries.** Every named range over a data table reaches the row capacity of the full legacy table with margin (e.g. HHSurvey 40,000 rows, EF_PM 60,000); lookups go by code (`MATCH`), never by position.
6. **Base-year energy use from Balances**, mapped to subsectors with legacy's flow mapping (Mapping table, flows and signs), as legacy with `BalancesOrConsumption = Balances`; `EnergyCons` is the alternative input.
7. **Test.** `check_allcountry_v4_5.py` clones every Egypt row of every data tab under a dummy code (XEG), appended at the bottom of its table, and requires identical outputs with no error values.

## 2. Visual style guide

Every calculation sheet should look like the legacy `Mitigation` sheet: same fonts, colours, borders, heading levels and white space. The legacy values below were read from the legacy workbook (2026-10-13); where a prototype differs, the difference is listed in [`excel_ai/core/TODO.md`](TODO.md) until it is fixed.

### 2.1 Colours

CPAT greens are the primary palette. Values below are the actual legacy fills.

| Use | Hex | Notes |
|---|---|---|
| Module and tab title bar (row 2) | `00AE49` fill, white bold text; on every tab (2.7) | legacy value; the mitigation prototype since v0.3.9 (earlier prototypes `00B050`: align when next touched) |
| Section band; sub-heading bar of other tabs | `92D050` fill | full width: A..last year column; on other tabs as wide as the title bar (2.7) |
| Input cells | `EBF1DE` (light green) | user-editable values only (user rule 2026-10-16: table headers, mappings and data have no fill; 2.7) |
| Code cells (Input/Output Code) | `DCE6F1` (light blue) | |
| Base-year column / derived switches | `DDD9C4` (tan) | e.g. column L (2022) |
| Unused / inactive parameters | `F2F2F2` (light grey) | legacy MTInputs grey |
| Variable names (column A of the calculation sheet) | `70AD47` text (light green), no fill | user rule 2026-10-13; parameter columns D:G stay unfilled |
| Calculation cells | no fill | |
| Results / notes to review | `FFF2CC` (light yellow) | e.g. check summaries |

### 2.2 Fonts

| Element | Legacy style |
|---|---|
| Whole sheet | Arial; body text and numbers 10-11 pt (legacy price blocks 10 pt, other tables 11 pt) |
| Module title band (row 2) | 14 pt bold, white, title band fill across the full width |
| Section band | section number in A (11 pt, not bold), title in B (12 pt bold), white text, `92D050` fill across the full width |
| Sub-section heading | column B, 11 pt **bold underlined**, no fill, no border (e.g. "Elasticities - energy sector", "Emission factors, Residential") |
| Sub-sub-section heading | column C (one column further in), 11 pt bold underlined; a heading for a reference table may be underlined only |
| Memo heading | italic underlined (e.g. "Discount factor workings:"); memo rows italic |
| Codes (Input Code, Output Code) | italic, code fill |
| Notes (long explanatory text in column H) | **not italic** (user rule 2026-10-16: long italic text is hard to read); dark grey `595959`, Arial 10 |
| Helper columns (row numbers, matches) | grey text (theme text at 15%) |
| Names of variables, fuels and sectors | never bold (user rule 2026-10-13); bold only on summary and total values |

### 2.3 Borders

| Element | Legacy style |
|---|---|
| Table header row (Fuel, Sector, Description, Units, Source, Input Code, Output Code, ..., years) | bold, thin **bottom** border across the table |
| First row of each block in a build-up (e.g. a fuel x sector price block) | thin **top** border across the row; the headline row of the block (e.g. Retail price) bold in the legacy, which the prototypes replace by the summary-only bold rule |
| Settings and parameter boxes (e.g. "New policy:", "Fossil fuel subsidy reform") | thin outline box around the group; box title bold in its first row; each input or parameter cell with a thin border on all sides |
| Calculation rows | no borders |

### 2.4 White space

| Where | Legacy convention |
|---|---|
| Before a section band | **one** blank row (user rule 2026-10-16; the legacy has two) |
| After a section band | one blank row before the first sub-section heading |
| Between sub-tables of a section | one blank row, also before a new sub-section heading (user rule 2026-10-16) |
| Between a sub-section heading and its table | none, or one blank row when a settings line sits in between |
| Inside a build-up | no blank rows between blocks; the block's top border separates them |

### 2.5 Sections, roll-up and summary rows (user rules 2026-10-16, mitigation prototype v0.4.1)

1. **Every section is numbered and rolled up by default**, including section 0 (scenario assumptions) at the top of the sheet: its band carries the number 0, rows 1-5 are frozen (years, title band, band 0, scenario name, scenario number) and the rows below them roll up.
2. **Every section ends with its summary row**, the only row visible when rolled up (bold values, no decimals). The workbook opens showing only the bands and the summary rows.
3. **The summary comes last, so the order follows from it.** Detail first, totals last: lettered sub-blocks (e.g. 12d fiscal reports, revenue by fuel; 13b and 14b changes, Kaya identity; 16b external balance) sit inside their section, before the notes and the summary row, never after it.
4. **A second summary row is unusual.** It is allowed when the headline is a level and its change against scenario 1 is the obvious second figure: energy use (11), revenue (12), CO2 (13) and GHGs (14) show the change against scenario 1 below the total. Every other section has exactly one.
5. Sections without a natural total get a summary row chosen as their headline: 2 average retail energy price (all energy, incl. new taxes and subsidies), 17 effective carbon rate, 18 national welfare gain.
6. **Section layout from top to bottom**: band, one blank row, sub-blocks (each: sub-section heading, label row, rows, one blank row), notes, one blank row, summary row(s), one blank row, next band.

### 2.6 Price build-up blocks (section 2; user rules 2026-10-16)

Each fuel | sector block reads from top to bottom:

| Part | Rows | Style |
|---|---|---|
| Label row | names the block's parameters D:G | bold, bottom border (top border on the block) |
| Settings (inputs) | parameter row (pass-through, VAT rate, GJ per price unit, international price position), international reference price, fixed part of the supply cost, existing consumer subsidy per price unit, existing producer subsidy | *italic* (not part of the build-up) |
| Existing build-up | supply cost, excise and other taxes, VAT, ending with the **retail price before new taxes and subsidies**; the memo splits of the taxes (taxes before the floor, fixed and floating parts, existing taxes, existing subsidies) | normal; memo splits *italic* |
| New taxes and subsidies | label row (D: price position), fuel use of the subsectors priced by the block (weights, *italic*), new carbon tax, new ETS cost, new excise (fuel price reform), change in existing carbon pricing, subsidy and price-control reform wedges, VAT on the new policies (and price floor), **total new policy** | normal |
| Post-tax price (last row) | retail price including all new taxes and subsidies | **bold** values; thin top border and thick bottom border across the whole row, titles and numbers (user rule 2026-10-20, v0.6.3) |

**Rule (user 2026-10-20):** in a build-up, every row that is not part of the build-up is in italics, and the build-up ends with its total (here the post-tax price) in bold, with a thin top and a thick bottom border across the titles and the numbers.

The new-policy rows and the full retail price are standard fuel-use weighted averages over the subsectors priced by the block (sections 5-8). They are not price indices: price changes between scenarios are measured by the price indices of the section 2 memo (3c rule 3.2).

### 2.7 Tabs other than Mitigation (user rules 2026-10-16, mitigation prototype v0.4.2)

1. **Title bar.** Row 2 of every tab is a dark green (`00AE49`) bar with white bold text: the tab name and, in a few words, what the tab is for. Mitigation, ScenarioDefinition and Prices_dom keep their legacy layouts.
2. **Sub-heading bars.** Each sub-table of a tab (each block of a consolidated tab) starts with a light green (`92D050`) bar, white bold text.
3. **One width per tab.** The title bar and every sub-heading bar of a tab span the same columns: all the columns the tab uses.
4. **Table headers** are bold with a thin bottom border and no fill. Light green fill (`EBF1DE`) means a user input and nothing else; mapping tables, data tables and headers have no fill.
5. **Cover tab first**, structured as the legacy Cover: title, contents (every tab, its content, whether legacy CPAT has it and which legacy tab), cell colour coding, tab colour coding, abbreviations.
6. **Divider tabs** (`MAIN->>`, `INPUTS->>`, the `DATA_*->>` dividers of 1.5, `REF->>`) carry a table of contents of their group: tab, content, in legacy CPAT (Yes / Partly / No), legacy tab. Tab colours: MAIN green, INPUTS light green, DATA light blue, REF grey, dividers and Cover dark grey.
7. **Data tabs** are grouped by module and ordered as legacy CPAT (1.5): `DATA_MITIGATION->>`, `DATA_DISTN->>`, `DATA_TRAN->>`, `DATA_OUTPUT->>`, then `DATA_OTHER->>` (side tables and derived values with no legacy data tab). Tabs are named as the legacy tab they match.
8. **Consolidated tabs** stack their blocks top to bottom with one wide column, C, for the long text of every block (e.g. tab Version Log, About, and Diff: version description, About text, this model). Tab names list the blocks in order (`Version Log, About, and Diff`; `Check, Variables, Lambdas`).
9. **About table**: category (About, Layout, Assumptions, Algorithm, Use, Version notes), topic, text; the first entry is the name of the workbook. No version tags in headings or topics: change history belongs in the version log.
10. **Differences with legacy**: one row per difference, with the register code (L legacy bug, I issue, LD simplification or not yet), whether it is a bug, an issue or the same as legacy, and its status (fixed, open, accepted, replicated).
11. **Lambdas table**: one line per formula pattern (variable, LAMBDA, formula of the first row, the Mitigation rows that share it as a list such as `257-265, 435-457`), in the order of the build-up. It serves readers and the check (which copies each formula back over its rows).
12. **Constants** are true constants only (definitions, conversion factors, policy assumptions without an ScenarioDefinition row). Groupings and positions are mappings (sheet Mapping); country values are data (data tabs), looked up where used.

**Collapsed columns (mitigation prototype, v0.3.9).** Column B stays visible, because the band titles, the sub-section headings and the fuel sit there; C:G, I:K and 2030-2039 roll up. A heading in B spills over the hidden columns into H, which is therefore empty on heading rows.

Subsections of a prototype follow these conventions: heading levels (band, bold-underlined sub-section heading, sub-sub-section heading), the table header row with its bottom border, top borders between blocks, settings boxes, and the blank rows around them. Where a user rule overrides the legacy (for example bold only on summary rows, short section bands, light green variable names), the user rule wins and is stated in section 3.

Rules: inputs green only; never hard-code values in unfilled calculation cells; keep the legacy font (Arial; title 14pt bold) on legacy-replicating sheets.

## 3. Other conventions

- **Exports to modules (user 2026-10-22, v0.8.1; how modules work: section 9, which takes precedence).** Since v0.9.0 (user 2026-10-29) section 19 holds 19a Distribution only; air pollution reads section 15 and transport co-benefits section 5b, without copies (section 9.3). Original rule: Mitigation section 19 (last, after section 15) holds plain copies of the rows each module reads: 19a Distribution (defined name `ExportDistn`), later 19b air pollution, 19c transport co-benefits; no calculation there. A copy keeps the code of the row it copies (the key the module matches on); the uniqueness rule C10 counts codes outside section 19. Each module reads only its input tab (`FromMitigation`, same column layout as Mitigation; scale to its base unit in column D), never a Mitigation row; the end-to-end process runs one scenario at a time (no batch).
- **Money units (user 2026-10-22, v0.8.1).** One vocabulary, currency first, scale and price basis as words: `USD`, `USD m`, `USD bn`, `LCU`, `LCU bn`, `USD/GJ`, `USD/kWh`, `USD/tCO2`, each with `real` or `nominal` where it matters; never `$`. The builder applies `unit_norm()` to every unit of the variable dictionary. Scaling (bn, m, thousand) lives in the unit label and, where a module converts, in one scale column of its input section: no formula body multiplies by a hard-coded `Billion` or `Thousand` outside that conversion.
- Formulas live in Excel; no macros in prototypes unless documented (build via Python scripts, see `...\build_workbook.py`).
- Every prototype records: source legacy sheet, version, and a validation table vs. legacy values (and vs. `coded` where available).
- Codes (`Input Code`, `Output Code`) must be identical between Excel and Python (`coded\cpat_model\mappings`).
- Country-specific additions are flagged with the country code in the `Scenario`/`Statistic` columns; do not alter the replicated legacy logic.
- Short formulas (user rule, 2026-10-11): keep cell formulas short, at most 100 characters as Excel shows them. A named LAMBDA may hold more complex logic. To shorten a formula, use defined names for data tables, or split it into visible helper rows or columns. Applied in CPAT-AI-Mitigation-Prototype from v0.1.07, and checked there.
- LAMBDA group (user rule 2026-10-20; replaces the LAMBDA test group of 2026-10-17 and the LAMBDA year of 2026-10-12): two scenario groups ship. Group 1 (the baseline) holds plain formulas in every year, the last one included, so the baseline works without LAMBDA support. Group 2 (the live scenario) calls the named LAMBDA of every calculated row in every year, from the base year (unless the row's base year is data) to the last year, so a LAMBDA holds its own switches (e.g. the IF between history and projection) instead of relying on separate column blocks. The test: the quick check's regression of every output code of every group against the last release (whose group 2 was plain up to v0.6.5), and on Distribution the Python reference; a third copy of the model in the shipped file is no longer needed.
- One formula per variable (formula uniformity; checked by `check_full.py`): every row of a variable has the same relative (R1C1) formula in each column block (base year, plain years, LAMBDA year), and each section heading total the same sum. **Exceptions (user 2026-10-29), each checked to be uniform over its own columns:** (1) `ener` road biomass (`bio.rod`) reads the road biofuels of the elasticity road model (section 5b `trbe.bio`, v0.9.0 R10.1) instead of the fuel-use equation; (2) the aviation and navigation heading totals add the self-generated renewables of section 5b (`ener.avi.ren`, `ener.nav.ren`, v0.9.0 R10.3). A new exception is added here and in the check's list (`UNIFORM_EXCEPTIONS`), never by loosening the check.
- Labelled parameters (user rule, 2026-10-13): every number in the parameter columns (D:G of the Mitigation sheet) is labelled: a label row above each block names the variable and each parameter column (looked up from the variable dictionary).
- One level of row groups (user rule, 2026-10-13): no nested row groups (outline level at most 1).
- Years in row 1 (user rule, 2026-10-13): on time-series calculation sheets the years sit in row 1 above each column block; no separate year label is needed.
- No hard-coded constants (user rule, 2026-10-13): no number is typed in a calculation sheet or written into its formulas (apart from 0 and 1, function codes and text lengths). Constants are looked up: named constants and assumptions on a constants sheet, input rows by name or label (not by typed row numbers), data on data sheets.
- Sign convention (user rule, 2026-10-13): subsidies are negative (a subsidy reduces net revenue: net = taxes + subsidies).
- Layout (user rules, 2026-10-13): short section bands (no explanations in the band; they go to the ReadMe); title of the calculation sheet = the module name; one row group per section with its summary row last, the only row shown rolled up, without decimals; default column width 10.14 (76 pixels); tabs grouped behind divider tabs (MAIN, INPUTS, REF, DATA); every input sheet (scenario inputs such as ScenarioDefinition, Settings) sits in INPUTS; bold only on summary and total rows (values only, never names).
- Excel names and encoding: see section 3b (rules 1-2; user-reported repair errors 2026-10-13/14).

## 3b. Building workbooks with code: Excel encoding and LAMBDA rules

Lessons from the distribution workbook ([`other/distribution/LESSONS_LEARNED.md`](../../other/distribution/LESSONS_LEARNED.md), the full account) and the mitigation prototype (repair errors in v0.2.4-v0.2.8). Every bug below opened without an error somewhere first (LibreOffice, a scalar test, one Excel build) and only failed in a specific case. Apply them to every workbook built by a script.

1. **Let Excel encode LAMBDA and newer functions.** In the file, every newer function needs the `_xlfn.` prefix (`LAMBDA`, `LET`, `XLOOKUP`, `MAXIFS`, `MINIFS`, `AGGREGATE`, `IFNA`, ...), and every LAMBDA/LET parameter the `_xlpm.` prefix where it is declared and wherever it is used. Writing this encoding by hand (openpyxl) is fragile: Excel's repair pass silently removes a formula or name with a small mistake ("Removed Records: Formula / Named range") and LibreOffice accepts it, so the checks pass. Rule: ship LAMBDA names and the formulas that call them as text, and install them with a macro through `Names.Add` and `Range.Formula2` (Excel then does the encoding). Where a newer function must be written into the file, a build check fails on any missing `_xlfn.` prefix.
2. **Names Excel cannot read.** No defined name, LAMBDA parameter or table name may read as a cell reference: A1 style (`y1`, `co2`) or a name beginning like one (`BCO2Key`), or R1C1 style (`r`, `c`, `R2C3`). Avoid function names as LAMBDA parameters (`now`, `base`, `switch`, `year`). A build check fails on each.
3. **One namespace.** Defined names, LAMBDA names and Excel Table names share one case-insensitive namespace: check them against each other at build time and fail on a collision.
4. **No silent error handling.** `On Error Resume Next` in an installing macro must record every error it skips and report them (sheet MacroCheck or equivalent); a macro that says "done" is not a test.
5. **Arrays.** `MIN`/`MAX` do not clamp element by element over an array argument (use `IF`); `INDEX(range, 0, X)` with an array `X` is not supported (use `MATCH`, `INDEX(range, row, 0)`, `CHOOSECOLS`). Test every array-callable formula with its real array shape, not a scalar stand-in.
6. **Check the pattern, not the instance.** After fixing a bug caused by a pattern, add a build-time scan for the pattern (as rules 1-3 do), not only a regression test for the one formula.
7. **Generated code round-trips.** When a script writes VBA string literals (long formulas), split the raw text into chunks first and escape each chunk (`"` to `""`) afterwards, and verify with a real parser that every generated string decodes back to the original text.
8. **Tables need unique column headers, compared case-insensitively** (`iso3` and `ISO3` clash): de-duplicate them at build time, after adding any column of your own, and give added columns names no source can carry (`FilterISO3`). Excel repairs a table with duplicate headers; openpyxl and LibreOffice do not notice. Enforced by `excel_lint.py` (section 3g).
9. **Design in Python, encoding in Excel.** Check every formula's design against an independent Python calculation (and legacy cached values) before encoding it; Python cannot test how Excel evaluates the encoded formula, so a test that runs in real Excel (a test sheet or a macro self-test) is still needed.

## 3c. Results: where they go and how differences are computed

User decision 2026-10-15. It applies to every result that legacy computes after its scenario blocks (blocks E, F, G) and to every new result.

1. **Results belong to the scenario.**
   - A number that depends on one scenario (with the baseline as reference at most) is a model quantity. It is computed in that scenario's column group on `Mitigation`, one formula per row, like every other row.
   - Output sheets only select, compare between scenarios and format: `MTOutputs` (results by output code in the legacy MTOutputs layout; rule 5 below), `StoredOutputs` (values of stored runs), `ScenarioCompare`, `Charts`. No output sheet computes a model quantity.
   - Legacy's results area (blocks E, F, G) is not rebuilt as a block. Its calculations are rebuilt as rows in the scenario sections, and its cross-scenario tables as output-sheet rows.
2. **Differences: computed in the model only where the model uses them.**
   - A difference against the baseline that feeds another calculation (fiscal effect, GDP effect, deadweight cost, price index, efficiency costs) is a scenario row:
     - `x.ref` is the scenario-1 value of the same year, from `ref_formula`. The lookup range ends at the current column, so the reference group must lie to the left.
     - `x.chg` = x - x.ref, and `x.pct` = x / x.ref - 1 where allowed (rule 3).
   - Every other difference, shown for reading only, is computed in the output sheets from the levels.
3. **Definitions of differences.**
   1. **% difference** = x / x.ref - 1, same year, **only for strictly positive quantities.** Signed quantities (subsidies, net revenue, balances, changes) get absolute differences only.
   2. **Prices:** price changes are price indices (pure price change), never ratios of unit values (average prices with each scenario's own quantities; issue I31).
   3. **Ratios and intensities** (CO2 per GDP, t/MWh, effective carbon rate, shares): computed from summed levels, never as averages of ratios or of percentages.
   4. **Periods** (cumulative or average over years): sum the levels first, then take the difference or the ratio. Never average yearly percentages.
   5. **Reference scenario:** scenario 1. A per-scenario reference (policy B against policy A) is a later option; its reference group must lie to the left (circularity guard of `ref_formula`).
4. **Large downstream modules** (air pollution, transport externalities) may sit on their own sheet. A time-series module sheet must have exactly the same column-group geometry as `Mitigation`: same first group column, group width, year row and scenario row. Copying a scenario group then works the same way on every sheet. The check tests that the geometries match. **Exception, single-year modules (user decision 2026-10-17):** a module analysed in one year (distribution: one analysis year to 2030, deciles across) uses its own, narrower group (code column, basket, deciles 1-10, spacer). It keeps the same order of groups, the same scenario-number row and the same LAMBDA group (group 2). Group *n* reads Mitigation group *n* through one offset row (group position x Mitigation group width + analysis year - base year + 1), and its lookup range covers at least the scenario capacity below.
5. **Section layout.**
   - The existing sections 1-16 of `Mitigation` keep their numbers.
   - A post-processing result goes into the existing section it belongs to. Small summaries become a memo at the end of the section; larger groups become a lettered sub-block (e.g. 12d, 16b).
   - New numbered sections exist only for results with no home: **17 Carbon pricing** and **18 Welfare and externalities**.
   - The sections follow dependency order: a section reads earlier sections, data rows, or the baseline through `.ref`. A memo may read rows further down when it is not circular (the section 2 price indices read after-tax prices in sections 5-8).
   - The plan: `mitigation/Results_Assessment_v<n>.md` section 6.
6. **Modules read `Mitigation` directly.** There is no hand-off block. (Inside the integrated prototype only. A free-standing module workbook reads Mitigation through its `FromMitigation` tab: section 9.)
   - A downstream module reads its inputs straight from the `Mitigation` rows of the same scenario column group, by output code, and reads the baseline through its own `.ref` rows.
   - Transformations that only the module needs (ratios to the baseline, unit conversions, its own layout) live on the module sheet.
   - `Mitigation` holds levels as rows with stable codes, ordered where useful like the module's input table (section 15 like the legacy air-pollution input).

7. **`MTOutputs` in the legacy layout (user 2026-10-29, v1.0.4).** The outputs tab keeps legacy MTOutputs' columns and their order: A Include?, B Country, C Scenario, D CPATIndicator, E CPATCode, F the legacy CPAT code (legacy's MTCode column, always N/A, repurposed), G Tab, H Variable, I Unit, J SubScenario, years K:AD; extra columns only right of the years (lookups, legacy code body and row, match). Columns are repurposed rather than added. Codes build themselves from the component columns: E = country, Tab, Variable, SubScenario (our codes); F = country, the legacy code body and the scenario. The rows are legacy MTOutputs' (latest legacy file), section by section in legacy order, one row per quantity in each scenario block; a row the prototype does not have stays, with Include? = No and the reason; legacy intermediates and junk rows are not added beyond what legacy lists. The mapping lives in `data_old/mvp_legacy_extracts/mtoutputs_map_465.csv` (match: exact, reordered, renamed, guess, none). Purpose: comparing the prototype with legacy row by row.

## 3d. Names, keywords and cell references

The LAMBDA repair errors (v0.2.4-v0.2.8; SCALE and SHARE in v0.3.6) all came from names. Rules for every defined name, LAMBDA name, LAMBDA parameter and Table name. The quick check enforces rules 1-5.

1. **Reserved names.** No name may equal a name in `mitigation/excel_reserved_names.txt` (case-insensitive):
   - Excel worksheet functions, including the newer ones;
   - reserved defined names (`Print_Area`, `Criteria`, `Database`, `Extract`, ...);
   - `TRUE` and `FALSE`;
   - names Excel 365 rejected in practice (`SCALE`, `SHARE`, 2026-10-15).

   Add a name to the file the day Excel rejects it. Exception, grandfathered: seven existing LAMBDA parameters that equal function names (`base`, `growth`, `price`, `rate`, `share`, `value`, `year`). Excel accepted them in the v0.3.7 test, but no new parameter may equal a function name.
2. **No cell-like names.**
   - A1 style: 1-3 letters then digits, up to XFD1048576 (`co2`, `pm2`, `x1`, `nh3`).
   - R1C1 style: `r`, `c`, `rc`, `r2`, `c3`, `r1c1`.
   - A name that begins like a cell reference (`BCO2Key`).
   - Pollutant and fuel codes such as `co2`, `pm2`, `so2`, `nh3`, `ch4` are therefore never names. They appear only as text inside codes (`mit.co2.pow.all`).
3. **One namespace.** Defined names, LAMBDA names and Table names are one case-insensitive namespace (3b.3). A LAMBDA name and a defined name differing only in case clash (`ETSSemi` / `ETSSEMI`, v0.1.07).
4. **Form of new names.**
   - LAMBDA names are upper case, at least two words joined (`SCALEBY`, `SHAREOF`, `FUELUSE`), letters only. Single common words are not used for new LAMBDAs: Excel adds functions with such names.
   - Parameters are lower case, at least three characters, letters and underscores only, no digits.
   - Defined names for data use CamelCase with a role suffix (`...Key`, `...Val`, `...Year`, `...Col`).
5. **No sheet names inside a LAMBDA body.** A body reads data through defined names only. Since v0.3.6 merged tabs, a sheet name in a body breaks when blocks move.
6. **Newer functions in the file.**
   - They carry `_xlfn.`; `FILTER`, `SORT`, `SORTBY` and `UNIQUE` carry `_xlfn._xlws.`; LAMBDA and LET parameters carry `_xlpm.`.
   - A function newer than the target Excel (2019 for the baseline group, 365 for the LAMBDA group) is not used in a plain formula.
7. **Keywords in formulas.**
   - No number other than 0, 1, function codes and text lengths (section 3).
   - No whole-column or whole-row references (`A:A`, `1:1`) in calculation formulas.
   - No volatile functions (`OFFSET`, `INDIRECT`, `TODAY`, `NOW`, `RAND`) in calculation formulas: they recalculate everything on every edit.
   - `INDEX/MATCH` with exact match (`0`) only.

## 3e. Copy-paste ability

The mitigation prototype is copy-pasteable in three directions. Every new row must keep all three, and the check tests them (drag test, LAMBDA group regression, scenario-copy test).

| Direction | Rule | What breaks it |
|---|---|---|
| **Across years** (drag right) | One plain formula per block from the base-year column + 1 to the last year. Year columns are relative. The previous year is the column to the left. The base year has its own formula (data). Rows with history and projection keep separate blocks (prices); in the LAMBDA group the row's LAMBDA holds that switch. | A year typed into a formula; a reference to a fixed year column; a look-ahead past the last year that reads a non-blank spacer |
| **Down a block** (copy down) | Rows of one block share one formula. Parameters come from the row's own D:G (`$D{r}`). References to a parallel block keep the same row order, so the same offset holds for every row. Single rows (totals, header rows, settings) are row-anchored (`$1`, `$5`, `$7`). | A row-specific constant; a parallel block in a different order; a total referenced without `$` |
| **Across scenarios** (copy a column group) | A scenario group references its own columns, the header rows (`$1` year, `$5` scenario number, itself a formula: the count of code-column headers from `$K$1` to its own, so a pasted group numbers itself), the parameter columns (`$D:$G`) and ScenarioDefinition through the scenario number. Scenario 1 is reached only through `ref_formula`, whose range starts at scenario 1's first column (`$K`) and ends at the current column. Module sheets have the same group geometry (3c rule 4). | An absolute column reference into another group; a reference to a group on the right (circular with the GDP feedback); a module sheet with a different geometry |

A row that cannot follow a rule (e.g. a data row) says so in its source column, and the check lists it as an exception.

**Scenario capacity (user rule 2026-10-17; 2026-10-20: two groups shipped, plenty of room).** The user can paste live scenarios to the right of the live group (group 2) by copy-paste. We ship two groups (baseline, one live policy scenario in LAMBDAs), but the whole workbook must work with at least the full set of scenarios 1-6 (groups 1-6; ranges reach group 7):
1. A group pasted into any free group to the right numbers itself, finds its inputs and works with no edit: groups 3-6 run scenarios 3-6.
2. ScenarioDefinition holds a scenario definition for every scenario number 1-6. A missing definition is an error, never a silent zero.
3. Every range that spans the groups (`ref_formula`, the lookups of module sheets, names, MTOutputs, checks, outline and column widths) reaches at least the last column of group 7. Nothing is sized to the shipped groups only.
4. Module sheets (distribution and others) follow the same capacity: Distribution group *n* reads Mitigation group *n* for every *n* up to 7.
5. The paste test (`check_paste_v<n>.py`) pastes group 2 into groups 3-6. It passes when there are no error values, the scenario numbers read 3-6, and the groups that match a stored scenario equal it. It runs at every release that touches the column groups.

**Full copy-pastability left to right (user rule 2026-10-16).**
1. Every cell of a scenario group, the code column, the scenario number and the header included, has the same relative (R1C1) formula in every group. Copying the baseline group (scenario 1) over a policy group, or a policy group onto the next free group (scenario 3 has its code column in `BC` and its years from `BD`; up to scenario 6, see Scenario capacity below), gives a working scenario with no edit. The quick check compares groups 1 and 2 cell by cell outside the LAMBDA cells of group 2.
2. **Differences against the baseline are formulas of the group itself**: `x - INDEX($K x:<this column> x, <this column>$10)`, where row 10 holds the position of scenario 1's column of the same year (`MATCH(year, $K$1:<this column>$1, 0)`). The range starts at the baseline's code column and ends at the current column, so the same formula gives 0 in the baseline and the difference against scenario 1 in every group to its right, wherever it is pasted. The baseline is always scenario 1, the leftmost group.
3. Nothing in a group is typed: the scenario number is a formula, and inputs come from ScenarioDefinition through it.

## 3f. Running several versions in one go (overnight runs)

For a chain of versions run without the user (e.g. v0.3.9-v0.3.18). The questions of the chain are answered in advance in its plan (`mitigation/Old/Plan_v3_9_to_v3_17.md`).

1. **One version per step**, in the plan's order. Each step:
   1. Bump the version (previous files to `Old/`).
   2. Build quick (`QUICK=1`, about 2 minutes) and run `check_quick` after the first structural change of the step. Fix before continuing: a half-way build catches row, name and copy errors early.
   3. Finish the step. Build quick and run `check_quick` again: the changed codes must be only the intended ones.
   4. Full build (about 2 minutes since v0.4.9), then `check_quick` on the full build.
   5. Regenerate the lists and the notes the step touches. Add the CAVEATS entry, version-log row and TODO update. Commit and push.
2. **No hangs.**
   - Every LibreOffice call runs under `timeout`.
   - Kill stray `soffice` processes before each build, by exact process name (`pkill -x soffice.bin`): `pkill -f soffice` also matches, and kills, the shell running the command (lesson of 2026-10-16).
   - Never run two LibreOffice jobs on one user profile. Parallel sessions are allowed only with their own profile each (`-env:UserInstallation`, as `lo_session_v<n>.py`), and never next to another job that uses the default profile (the conversions of the checks).
   - Long steps run in the background, with completion notices, not polling.
   - No Excel COM in the cloud.
   - A build or check that times out twice is reported and the step stops.
3. **Full check** (`check_v<n>`, about an hour) only when the user asks (at the plan's checkpoints), not every step. Every new row group adds its independent Python recomputation to `check_v<n>` in the same step.
4. **A failing step is never shipped half-done.** If it cannot be fixed within the step, revert its changes, record why in CAVEATS and TODO, and continue only with later steps that do not depend on it.
5. **A question not answered in the plan:** take the recommended default and record it in the CAVEATS entry as a decision to confirm. Do not stop the chain for it.
6. **Saving tokens:** print only check summaries and the tail of logs; do not re-read large files; reuse the generated lists.

## 3g. Excel repair prompts: lint every file before it ships (user rule 2026-10-20)

"We found a problem with some content ... Repaired Records: ..." keeps coming back because **Excel validates a
package more strictly than openpyxl and LibreOffice**: a file can build, open in LibreOffice and pass every check
here, and still be repaired by Excel. The cloud has no Excel, so the only defence is to test for every known cause
in the file itself.

1. **Every workbook written by code is linted before it is shipped or committed:**
   `python excel_ai/core/tools/excel_lint.py <file> ...` (exit code 1 on any problem; library: `excel_lint.lint(path)`).
   Builders call it on their output and fail the build on a problem. This applies to every builder in the repository
   (Excel-AI, Coded CPAT exports, data workbooks) and to the variants made from a built file.
2. **What it checks** (each a cause Excel has repaired in our files, or a documented Excel limit):
   - table column names: none blank, none equal case-insensitively (cause: `CPAT_Data_dummy.xlsx`, 2026-10-20);
     each header cell is text and equals its column name; the column count matches the range; tables do not overlap;
     the autoFilter range equals the table range;
   - table and defined names: valid characters, not cell-like (A1 or R1C1), not TRUE/FALSE, at most 255 characters,
     one case-insensitive namespace (section 3d);
   - defined-name comments at most 255 characters (cause: FUELUSE, v0.6.2, 2026-10-20); defined-name formulas at most
     8,192 characters;
   - cell formulas at most 8,192 characters; cell text at most 32,767 characters; in-cell list validations at most
     255 characters;
   - sheet names: at most 31 characters, none of `[]:*?/\`, no leading or trailing apostrophe, unique
     case-insensitively.
   The LAMBDA rules (sections 3b and 3d: `_xlfn.`/`_xlpm.` prefixes, reserved names) stay with the quick check of the
   prototype.
3. **When Excel repairs a file anyway:** ask for the repair log (the XML Excel offers to show). It names the package
   part (`/xl/tables/table4.xml`, `/xl/workbook.xml`, `/xl/worksheets/sheet3.xml`); unzip the file, read that part,
   find the cause, and **add a rule for it to `excel_lint.py` the same day**, with the file and date in section 2
   above, so that the cause can never ship again (the pattern, not the instance: section 3b.6). Then fix the builder,
   rebuild, lint, and log it in `CAVEATS.md`.
4. A file that has been repaired by Excel and saved is not the fix: the builder is.

## 3h. VBA modules embedded by the build (user rule 2026-10-22, after v0.7.1)

The build writes the VBA project itself (`vba_project_v<n>.py`). It references **only the Excel library and stdole**,
and the only macro test in the cloud runs in LibreOffice Basic, which is lax: it runs code Excel will not compile.

1. **Only Excel and VBA names.** No constant or type from another library: no `mso...` (Office), `ado...`, `fm...`,
   `Scripting.Dictionary` as a declared type. Use the value as a module constant (`MSO_TRUE = -1`, `MSO_LINE_DASH = 4`)
   or late binding (`CreateObject`, `As Object`). Found 2026-10-22: `msoTrue`, `msoLineDash`, `msoLineSolid` in
   StyleSeries (v0.6.7-v0.7.1, "Variable not defined"). Check: `check_quick` `vba_names` (every identifier declared, VBA,
   Excel or a listed xl/vb constant); add a new Excel constant to its list after checking it in the Excel object model.
2. **Declarations first.** Every module-level `Const`, `Dim` and `Type` sits above the first procedure (VBA compile
   error otherwise; found v0.6.5, the DataLinks constants). `Option Explicit` on every module.
3. **No silent errors** (3b.4): an `On Error Resume Next` covers one statement and is followed by `On Error GoTo 0`;
   a handler restores what the macro changed (calculation mode, ScreenUpdating, DisplayAlerts) and re-raises or
   reports. A macro that changes `Application.Calculation` restores the mode it found (v0.6.6: RunAll).
4. **No volatile state in cells for macros:** a value the macro needs (the workbook folder) is written by the macro,
   not computed by a volatile formula (`CELL("filename")`, removed v0.6.6).
5. **Generated strings round-trip** (3b.7): chunk, then escape, then parse back.
6. **Excel-only behaviour is listed as untested.** Charts, Power Query, `ListObjects`, `Queries`, `Formula2` and
   anything LibreOffice does not implement are reported in CAVEATS as "not run in Excel" until the user has run them;
   the first-run checklist (QuickStart) asks the user to run Debug > Compile VBAProject once per release.
7. **Power Query loads never sit on a model tab:** load into a staging sheet and copy by column name (v0.7.1
   `RefreshLink`), so the tab keeps its header row, formula columns and named ranges.

## 3i. Testing LAMBDAs and values without Excel (LibreOffice; lessons of v0.6.6-v0.7.0)

LibreOffice evaluates neither named LAMBDAs nor, reliably, a workbook on loading. Every check that reads values:

1. **Expands the LAMBDAs** (the bodies substituted into the calls) before LibreOffice recalculates, for the current
   file and for the earlier release a regression compares with (v0.7.0: the quick check compared v0.7.0 with an
   unexpanded v0.6.7 whose LAMBDA group read as errors).
2. **Every recalculation is two `calculateAll`** (`lo_session` `Session.calc`, used by the build's batch, the checks'
   `hard_recalc` and the value sessions): the recalculation on load gave wrong trailing averages (fpp, up to 31%),
   and one `calculateAll` after loading or after copying a definition left differences of 5e-5 to 2.4e-3 (stored
   results of the batch, fiscal impulse); `soffice --convert-to` is not used for values.
3. **Puts the file in automatic calculation first** when it ships in manual calculation (since v0.6.6): otherwise the
   formulas of an openpyxl copy, which has no cached values, stay uncalculated.
4. **Tests the LAMBDA group by its results:** group 2 (LAMBDAs) against the plain group's earlier release and the
   Python reference; a build step that copies or blanks "the LAMBDA group" is checked by the stored results (v0.6.6
   shipped empty stored definitions: `stored_complete`).
5. **Tests by scenario group number, not position:** a pasted group numbers itself from the group on its left, so a
   test pastes into the next free group (v0.7.0: tests that pasted into group 4 with an empty group 3).

## 3j. Lessons register: LAMBDA and VBA (every issue found, its norm and its check)

| Found | Issue | Norm | Check |
|---|---|---|---|
| distribution workbook | hand-written `_xlfn`/`_xlpm` encoding removed by Excel's repair | 3b.1, 3d.6 | quick check (prefixes); LAMBDAs installed by macro where possible |
| v0.2.4-v0.2.8 | names and LAMBDA parameters read as cells (`y1`, `co2`, `c`, `tco2_kwh`) | 3b.2, 3d.2 | quick check, `excel_lint.py` |
| v0.1.07 | LAMBDA and defined name differing only in case (`ETSSemi`/`ETSSEMI`) | 3b.3, 3d.3 | quick check, `excel_lint.py` |
| v2.x | `MAXIFS` without `_xlfn.` (found before shipping) | 3b.1, 3d.6 | quick check |
| v0.3.6 | LAMBDA names `SCALE`, `SHARE` rejected by Excel 365 | 3d.1, 3d.4 | `excel_reserved_names.txt`, quick check |
| v0.3.6, v0.5.3 (M12, M14) | LAMBDA-library texts naming merged-away sheets (`#REF!` when copied) | 3d.5 | full check section 3 (sheet names in LAMBDA texts) |
| v4.x | a LAMBDA name defined twice (`INTENSITY`); the later one silently won | 3d.3 | build assertion (no LAMBDA defined twice) |
| distribution | `MIN`/`MAX` over arrays, `INDEX(range, 0, X)` with an array X | 3b.5 | array-shape tests (distribution) |
| distribution | VBA string literals escaped before chunking | 3b.7, 3h.5 | parse-back test of generated code |
| v0.6.2 | defined-name comment over 255 characters (FUELUSE) | 3g | `excel_lint.py` |
| v0.6.5 | VBA module constants after the first procedure (compile error) | 3h.2 | `vba_names` (declarations); Excel compile by the user |
| v0.6.6 | build's batch copy blanked the live (LAMBDA) group: empty stored results | 3i.4 | quick check `stored_complete` |
| v0.6.6 | `CELL("filename")` volatile cell read by a macro | 3h.4 | review (no volatile functions: 3d.7) |
| v0.6.7-v0.7.1 | Office constants `msoTrue`, `msoLineDash`, `msoLineSolid` undefined ("Variable not defined") | 3h.1 | quick check `vba_names` |
| v0.7.0-v0.7.1 | LibreOffice: wrong values on load, errors up to 2.4e-3 after one `calculateAll` (stored results of IDs 3-5) | 3i.2-3i.3 | `Session.calc` = two `calculateAll`; full check stored results vs Python |
| v0.7.0 | regression against an unexpanded earlier release | 3i.1 | quick check (`recalc_values` expands) |
| v0.7.0 | tests pasting into group 4 with group 3 empty | 3i.5 | full check (exemption, leakage) |

Add a row in the task that finds a new issue (root `NORMS.md` section 6b).

## 4. Policy and parameter input norms (ScenarioDefinition)

**Where inputs live (user rule 2026-10-18, mitigation prototype v0.4.12).** The main inputs are on `ScenarioDefinition`. Policy inputs elsewhere (Settings, data tabs) are allowed, but they should mostly come from legacy (for example legacy `Manual inputs` switches) or from bug fixes, not extend the functionality. An prototype input that extends legacy (for example the ETS benchmarks by sector group, issue I21) is a departure: it needs a user decision, and the legacy `ScenarioDefinition` input it replaces must still work.

All new models take their policy and parameter inputs from a dedicated input tab/file built on the legacy MTInputs structure (the prototype's `ScenarioDefinition`). Master list of the inputs: tab Inputs of the codes map `excel_ai/CPAT-AI_CodesMap_v<version>.xlsx` (row, label, unit, name, legacy name, Name Manager names, Python key). Its sources: `data_old/mvp_legacy_extracts/mtinputs_465.csv` and the build's row template `excel_ai/core/tools/MTInputs_template.xlsx`, both written by `excel_ai/mitigation/extract/extract_inputs.py` from the legacy workbook (never edit them by hand).

- **Exact row structure (user rule 2026-10-28).** Every model's input sheet reproduces the rows of MTInputs of the **latest legacy CPAT** (today `CPAT 1.0pre_465`, rows 8-413) exactly, in the same order, **including blank rows and section-heading rows**. Never insert, delete or reorder rows; row numbers must match the legacy tab so references and Python mappings port 1:1. Inputs the prototype adds (that legacy does not have) go **below** the last legacy row, in blocks with a heading; each is recorded as a departure or an upgrade. When a new legacy file changes MTInputs, rerun `extract_inputs.py` and rebuild.
- **Colouring.** Parameters actually used by the module: green fill (`EBF1DE`) on B:H. All other parameters: light grey (`F2F2F2`) on B:H. Section-heading rows are bold, unfilled. Rows 1-3 carry the title (`00B050`) and section (`92D050`) bands.
- **Columns** (column structure of the legacy tab need not be replicated). Required, in this order:

| Col | Header |
|---|---|
| B | Parameters (parameter name) |
| C | unit |
| D | MT values - **placeholder, hidden** |
| E | "Dashboard" values - **placeholder, hidden** |
| F | Used for calculation |
| G | Defaults |
| H | NameOfParameter |

  Columns D and E carry the header text but are hidden and empty (for now). Other legacy columns (e.g. I, "Use Dashboard even if Defaults selected") are dropped. Column A may hold the legacy `X` flag.
- **Linking.** Module calculations reference the `Used for calculation` column (F) only; defaults feed it until Dashboard/MT columns are activated.
- **Lookup by name.** Read parameters with `INDEX(ScenarioDefinition!$F$8:$F$415, MATCH("<NameOfParameter>", ScenarioDefinition!$H$8:$H$415, 0))`, not by row reference.
- **Names (user rule 2026-10-28).** `NameOfParameter` (column H) is the name of every input in Excel and Python: Excel looks inputs up by it, and the Python input keys (`coded/cpat_model/dashboard_inputs.py`, `distribution_inputs.py`) are the same names. The set is complete: every input row has a name. Names are legacy column H as it is, with two exceptions: a legacy name that is wrong is a bug and is corrected (L137: no `D_` prefix, which in legacy names the Dashboard cell, not the MTInputs value; no spaces); a row legacy leaves without a name gets one (I87), built from its section and label (`FbCov<Sector>`, `ETSCov<Sector>`, `CBAMProc<Sector>`, `Fpr<Start|Final|Unit><Fuel><Sector>`). The legacy name is kept in the codes map. Inconsistencies of legacy names and values that are not wrong are issues and are replicated (I85 percentages typed as whole numbers, I86 spelling). A name is never reused for another input.

## 5. Versions, releases and documents (user rules 2026-10-22, v0.8.0; 2026-10-28, v0.8.4)

### 5a. File naming and the release layout (user rule 2026-10-28)

- **Main files carry their version.** Every version of a module workbook, the current one included, is in the module's `releases/` folder as `<Name>_v<version>.<ext>` (`<version>` = `0.<major>.<minor>`, section 5a Version numbers): `excel_ai/mitigation/releases/CPAT-AI-Mitigation-Prototype_v1.0.4.xlsm`, `excel_ai/distribution/releases/CPAT-AI-Distribution-Prototype_v<n>.xlsm`, `excel_ai/air_pollution/releases/`. The documents people read keep their current version where people look (user 2026-10-30): `excel_ai/bugs_and_legacy/Legacy_CPAT_Bugs_v<n>.docx` and `Tracking_Legacy_Bugs_v<n>.xlsx`; `excel_ai/CPAT-AI_CodesMap_v<n>.xlsx` and `CPAT-AI_Overview_v<n>.pptx`. The register documents, the tracker and the codes map carry the version of the mitigation prototype they were made with.
- **Older versions stay with their module** (user 2026-10-30): a module's workbooks in its `releases/`; the documents' older versions in `excel_ai/bugs_and_legacy/register/releases/` (the deck's in `excel_ai/mitigation/releases/`). Writing a new version moves the older ones there (`excel_ai/core/tools/release.py`, `publish`); every builder and document script uses it. The releases keep every version from v0.7.2 on (except the mitigation workbooks before 0.9.1, removed by user decision 2026-10-29).
- **`excel_ai/active_workbooks/`** (user 2026-10-30; replaced `permalink/` and `permalink_countryeditable/`) holds the permalinked copy of every module, `<Name>_latest.<ext>`: what people open and what other files and tools link to for data transfer (today mitigation, distribution and the air-pollution standalone; the distribution module reads the mitigation copy beside it). A user runs a module for a particular country there, on the local drive, and edits it. Nothing else gets a `_latest` copy.
- **Data and links of the active workbooks** (links done v1.0.3): each workbook refreshes its data tables by Power Query from the public repository (source "Dummy - GitHub (public repository)": `main/data/Public01/legacy_xlsx/CPAT_LegacyData.xlsx`), a local copy (`<repo>/data/Public01/legacy_xlsx/CPAT_LegacyData.xlsx`), or a separate data repository (its URL typed in the source table). A module's Update macro finds the source module's `_latest` file next to itself first, then in `active_workbooks/` one or two folders up (section 9.3). Builders publish the `_latest` copy (`excel_ai/core/tools/release.py`, `publish(link=True)`). Never commit a copy filled with real data (section 8).
- **Names.** `<Name>` in words joined by hyphens or underscores, no spaces, no dates; `_v<version>` last, before the extension. Scripts and notes have stable names (`build.py`, `check_full.py`, `check_quick.py`, `make_docs.py`, method chapters in `mitigation/docs/methods/`), never a version. A release is a git tag; the history keeps every earlier file. No `Old/` folders.
- **Version numbers.** Three parts, `0.<major>.<minor>` (e.g. `0.9.0`), until the first full release `1.0.0` (user 2026-10-29). Rebased 2026-10-29: Mitigation `X.Y` -> `0.X.Y` (9.0 -> 0.9.0, 1.07 -> 0.1.07, the early 0.Y -> 0.0.Y), Distribution `1.Y` -> `0.1.Y`; the released files were renamed, their contents keep the old numbers. Code that reads a version from a file name or `VERSION` compares all parts as integers (`excel_ai/core/tools/release.py`, `all_versions`). `VERSION` in `build.py` (also `mitigation/version.json` for the deck): the last part for fixes and small features, the middle part for structural or methodological change. `REGISTER_VERSION` (`issues_register.py`) equals it. A module with its own builder (distribution, air pollution) has its own `VERSION` and says in its version log which mitigation version it was built from.

### 5b. Version tables (user rule 2026-10-28)

Every workbook and every generated document keeps **one** version table, in the same columns:

| Column | Content |
|---|---|
| Version | `0.<major>.<minor>`, the version in the file name |
| Date | `YYYY-MM-DD` |
| Description | One or two sentences: what changed, with register codes (L, I, ...) where a bug or issue is involved |
| Max abs regression diff | Against the previous release (quick check): `0`, or the largest difference and why (workbooks; `n/a` for documents) |

- Where: a workbook in its version tab (mitigation: `Version Log, About, and Diff`; others: `Settings` or `ReadMe`); a generated document in its first lines (version, date, the prototype version) and, for the change history, `CAVEATS.md`; never in a methodology (section 7).
- Newest row last. Rows are not edited after the release, except to correct a mistake (say so in the row).
- The `CAVEATS.md` entry of the task and the version row agree.
- Documents written by hand (method chapters, NORMS, READMEs) carry no version table: git history and `CAVEATS.md` are their record.

### 5c. Documents, plans and other release rules

- **Documents, few and simple.** In `excel_ai/bugs_and_legacy/`: `Legacy_CPAT_Bugs_v<version>.docx` (the legacy bugs, with every cell-level fix plan; the register as JSON in `bugs_and_legacy/register/Legacy_CPAT_Register.json`) and the tracker `Tracking_Legacy_Bugs_v<version>.xlsx` (the master list of bugs and issues), at the top of `excel_ai/` the codes map `CPAT-AI_CodesMap_v<version>.xlsx` (codes and inputs) and the deck; in `core/` `BUGS.md`, `ISSUES.md`, a README. In `excel_ai/mitigation/`: the short **Documentation** (`docs/Documentation.md`, hand-written, about 5-20 pages: what it is, quick start, how each block works with its key equations, results, limits) and the **Methods** volume (`docs/methods/`, one chapter per block; equations and data tabs as appendices). `make_documentation.py` rebuilds them all. The documentation points to the register; it does not repeat bugs, issues or version history. Every release regenerates the deck so its counts match the register.
- **Plans and lists.** Open work in `excel_ai/core/TODO.md` (one list); one file per open plan in `excel_ai/core/plans/`; finished plans leave (their record: `CAVEATS.md`). Legacy material (legacy workbooks, fix-plan sources and tools, surveys of legacy, one-off extraction tools) in `excel_ai/bugs_and_legacy/`.
- **GDP timing rule (v0.6.2, I72, user 2026-10-20).** Revenue of year t changes GDP only from year t+1 (`gdp.lvl`(t+1) = 1 + `gdp.eff`(t), as legacy row 8776); the fiscal space reads revenue of year t only; no same-year GDP effect reaches same-year demand. Keep it in every change to the GDP block (`GDP_Method_v6_2.md` 2b).
- **Circular references (v0.6.0; v0.6.2).** A LibreOffice load computes a workbook with a circular reference without complaint; only a full recalculation (`calculateAll`) shows Err:522, so the quick check and the checks recalculate fully after loading. Rules: (1) no formula reads a later year (L67 is fixed with this year's growth, not next year's demand); (2) every range is exact: a range shifted by a row offset must not run past its block into other sections (v0.6.2: the price-block averages ran into section 11 and made the methane fee circular); (3) an average over several years reads one row, never a block area (v0.6.2: `fpn`/`fpp`); (4) the GDP fiscal space reads no fuel use: where legacy counts a revenue that depends on fuel use incl. power, use the stored scenario-1 activity (sheet BaselineCO2, refreshed by the build, with a check row), as v0.6.2 does for the methane fee (I47). Excel and LibreOffice treat every cell of a referenced range as a precedent. (5) No parameter cell (D:G), which acts in every year, reads a model year after the base year: store the scenario-1 value instead (v0.6.2: the methane calibration ghg.k read GHGYear). (6) A running range from the left (INDEX($A..:this year)) keeps the spacer test of the group on its left blank. Tests (quick check, v0.6.2): no formula reads a later year except the whitelist (mani: data; dsum, lvc: levelised input-driven costs); no parameter cell reads a later model row that is not data; the levelised cost reaches no fuel use, GDP or power quantity row; plus the full recalculation (Err:522).
- **No ETS goal-seek runs (user rule 2026-10-19).** Do not run the ETS goal seek (`ets_goalseek_v<n>.py`, the macro `SolveETS`/`SolveETSLive`, or any convergence test of it) in builds, checks or tasks, and skip the goal-seek parts of the full check. The user tests the goal seek (issue I30) separately; run it only when the user asks in so many words.
- **Build speed (user rules 2026-10-17): the full build as fast as possible; speed comes first, as the builds give no errors.** The full build of the mitigation prototype took about 70 minutes in v0.4.6 and takes about 2 minutes since v0.4.9. Keep it that way:
  1. **No ETS goal seek in the build.** The emulation of RunAllScenarios stores a definition with a new ETS at the workbook's own price estimate; the macro still goal-seeks in Excel.
  2. **Load once, recalculate in memory.** LibreOffice runs as UNO sessions (`lo_session_v<n>.py`): each session loads the recalculation copy once; each run writes its inputs, recalculates in memory and reads only the cells it needs. No save, reload or file conversion per run.
  3. **Parallel sessions.** The runs (baseline, definitions) are shared among 3 sessions, one spawned process each, on the 4 cores; Python merges the tabs meanwhile. More sessions do not help: the cores are the limit.
  4. **Recalculate only what is read.** The copy that LibreOffice recalculates leaves out what no stored result reads: the Distribution sheet. It is written from the workbook in memory (LAMBDA calls expanded, then restored), never by saving and reloading the workbook.
  5. **No per-row scans and no slow helpers in loops.** Hoist `ws.max_row` / `ws.max_column` out of loops (openpyxl scans every cell for them); copy formulas along a row with the column shifter (`shift_cols`), not openpyxl's Translator.
  6. **Every speed change keeps the output identical:** compare the new build with the previous one cell by cell (all sheets) and the stored results to 1e-12, before it ships.
  7. **Measure first.** The build prints the time of each stage; profile (cProfile) before optimising, and optimise the largest stage.
  8. **Checks the same way (v0.4.9).** The quick check and the paste test write their LAMBDA-expanded copy from the file's XML (seconds; no openpyxl load and save) and recalculate it in a LibreOffice session in a spawned process while Python runs the structure checks; error values come from LibreOffice's own query, not a scan of every cell. The paste test writes its paste into the XML (the column shifter: identical to openpyxl's Translator on all 574,168 pasted cells). Never paste with UNO (`copyRange` recalculates after each paste; with automatic calculation off the results are wrong). Quick check about 1.5 minutes (was 3.3), paste test about 3.5 (was 5).
- **Regression test on every increment.** Recalculate old and new versions in Excel and diff all values (baseline plus input shifts); differences must be zero or explained in the version log. Check sheets must stay at ~0 vs legacy CPAT.
- **Checks (user rule 2026-10-15): optimise for (a) it works and (b) speed.** After every change run only the quick check (`check_quick.py`, a few minutes: structure, names, literals, formula length, a recalculation with no error cells, the code protocol, the change of every output code against the last release in `releases/`). The full check (`check_full.py`, several hours with the macro tests) runs at a completed milestone or when the user asks. The paste test (`check_paste.py`) runs at every release.

## Excel files written by code (every project)

Every .xlsx/.xlsm a script writes, in any project, is checked with `python excel_ai/core/tools/excel_lint.py <file>` before it is shipped or committed, and the builder fails on a problem. Excel repairs files that openpyxl and LibreOffice accept; the causes found so far and the procedure when Excel still repairs a file are in [section](NORMS.md) section 3g.

## 6. Task completion: caveats log and bookkeeping

Applies to **every** task (Excel, Python, data, documentation). A task is not finished until it is logged. When a task is done:

1. **Add an entry to [`CAVEATS.md`](CAVEATS.md) (repo root).** This is the single record of completed work. Use the template at the top of that file and record:
   - **Task** - what was asked and what was done, with the task id or version (e.g. `v0.2.3`);
   - **Inputs** - files, sheets/ranges, data sources, specs and prior versions used;
   - **Outputs** - files created or changed (paths), version numbers, documents updated;
   - **Caveats** - placeholders, assumptions, known gaps, deferred items, regression differences that were explained rather than zero, decisions still open; anything the next person must know before building on the result.

   Newest entry at the bottom. Earlier entries may be edited to keep the log accurate (fix stale paths, mark a caveat resolved with the date and where it was resolved, correct a mistake), but the record of a task is not deleted. Keep entries short and point to the task spec, report or yaml notes for detail.
2. **Workbook version log** (Excel work: [section](NORMS.md) section 5). Add the version-log row (version, date, one-line description, max abs regression diff) in the workbook's `Settings`/`ReadMe` tab. The `CAVEATS.md` entry and the version-log row must agree.
3. **Bugs and issues.** Never replicate a legacy bug; replicate every legacy issue and track it ([section](NORMS.md) section 0). Every bug found and every issue met goes in the register, so that it shows in [`excel_ai/core/BUGS.md`](BUGS.md) or [`excel_ai/core/ISSUES.md`](ISSUES.md).
4. **Queue.** Tick the item in the project TODO ([`excel_ai/core/TODO.md`](TODO.md) or [`coded/TODO.md`](../../coded/TODO.md)). Follow-up work the task generated goes in as a new `TODO.md` item, not only as a caveat.
6. **No commit unless asked.** Leave changes in the working tree; the user decides what to commit.

`CAVEATS.md` summarises and points; detail stays where it is produced - the task spec, the workbook version log, and `other/distribution/LESSONS_LEARNED.md` for the LAMBDA/VBA workbook. The per-task conventions in `excel_ai/core/TODO.md` (builders via Excel COM, codes/source/confidence for every new input, `Settings` version-log row, `Check`-sheet regression) remain in force and are the operational version of section sections 3-5.


## 6b. Norms follow the lessons: update them in the same task (user rule 2026-10-22)

Every bug, repair prompt, compile error or false check that has a cause another file or task could repeat ends with a
norm, not only a fix. In the same task that fixes it:

1. **Name the class, not the instance:** what kind of mistake it was (e.g. "an Office-library constant in a project
   that references only Excel", not "msoTrue in StyleSeries").
2. **Add or sharpen the norm** in the project's NORMS (Excel: section; repository-wide: here), with the
   date and the version or file where it was found. If a norm already covered it, say why it was missed and sharpen
   the wording or the check.
3. **Add the check** that would have caught it (a build assertion, `check_quick`, `excel_lint.py`, a test): the
   pattern, not the one formula or line (section 3b.6). Show that the check fails on the old file.
4. **Look back:** search the current files for other instances of the class and fix them in the same task.
5. **Register it:** add a row to the lessons register of the project (Excel: section section 3j,
   LAMBDA and VBA) and name the norm in the task's `CAVEATS.md` entry ("Norm: ...").
6. **A user report counts the same as a failing check:** when the user finds a problem the checks did not, the norm
   and the check are part of the fix.

## 7. Methodology and version notes are always different documents

A **methodology document** describes the method as it is now: equations, inputs, conventions, results and open issues. It is written for a reader who has never seen an earlier version, so it contains no change history: no "v0.0.3 changes (vs v0.0.2)", no "was X, now Y", no version log, no "superseded" commentary and no per-version result columns.

Version and change history goes in **separate version notes**, never in the methodology:

| What | Where |
|---|---|
| What changed between versions, and why | The version notes next to the document (e.g. `VersionNotes_<name>.md`), the workbook's `Settings` / `ReadMe` version log, and the `CAVEATS.md` entry |
| Caveats and decisions still open | `CAVEATS.md` and the document's own "Open issues" section (current state only) |
| Superseded copies | The git history (release tags) |

When a task changes the method, rewrite the affected methodology text to describe the new state, and put the delta in the version notes and `CAVEATS.md`. A methodology that contains a version log or before/after comparisons is non-compliant: move that content out when you next touch the document.


## 8. Data: everything in `data/`, as editions; tidy is the source of truth; the legacy shell

**All data live in the root folder [`data/`](../../data/README.md)** (user 2026-10-20; rebuilt and organised in editions 2026-10-30), with the scripts that convert them:

| Item | What it holds |
|---|---|
| `data/editions.csv` | The registry of every data set (edition): name, type (`public-perturbed`, `full-real`), location, based on, legacy base, version, status, default |
| `data/<edition>/` (`Public01`) | One data set, the same structure in every edition: `EDITION.json` (manifest, checksums), `data_sources.csv` (the catalogue plus column `values`), `tidy/` (**the source of truth**, user 2026-10-30), `legacy_xlsx/CPAT_LegacyData.xlsx` (written from `tidy/`, never edited by hand), `legacy/CPAT 1.0pre_465_<edition>.xlsb` (the legacy shell with the edition's six proprietary tables), `inputs/` (inputs that depend on the data) |
| `data/catalog.csv` | The generic catalogue of every data table: tidy file, Excel tab, proprietary / non-proprietary, provenance, and the legacy "Data sources" columns (`data/scripts/build_catalog.py`) |
| `data/legacy/CPAT 1.0pre_465_Shell.xlsb` | The legacy model (below), its six proprietary tabs empty, every other tab filled |
| `data/inputs/` | Generic model inputs: scenario sets (`scenarios_excel_ai.csv`) |
| `data/scripts/`, `data/tests/` | Generic: the converter, `editions.py`, `legacy_csv.py`, the catalogue and manifest builders, the perturbation and legacy scripts; the tests run on every edition present |
| `.buildcache/legacy_csv/<edition>/` (git-ignored) | An edition's `tidy/` in the legacy CSV form the Excel-AI scripts read (`data/scripts/legacy_csv.py`, `legacy_dir()`); a build product. Scripts that write tables write there, then `legacy_csv.py --save` puts them into the edition's `tidy/` |

Rules:

- **Editions** (user 2026-10-30): one folder per data set, `<Type><NN>` (`Public01`; `Full01` lives in the private data repository and never here); same structure and file names in every edition; models switch by path (`--edition`, `CPAT_DATA_EDITION`, the default row of `editions.csv`). A new number is new data; `version` records smaller corrections. An edition that a released model links to is frozen; changes then go into the next number. Models print the edition and version on their outputs.
- **New data go in an edition's `tidy/`**, as tidy tables with a spec in `data/scripts/tidy_specs.py` (or `tidy_blocks.py`). No other formats of the same data are kept (user 2026-10-30). Project folders hold code, documents and generated workbooks, not data; code reads the data from `data/` by a path relative to the repository (never a copy).
- **One change, every form.** When an edition's `tidy/` changes, rewrite its `legacy_xlsx/` workbook in the same task, its legacy copy (`legacy_proprietary.py fill`) if a proprietary table changed, `data/catalog.csv` if a table was added, then its manifest (`build_edition.py`), run `python -m pytest data/tests`, and log it in `CAVEATS.md`.
- **Six proprietary tables** (user 2026-10-30): Balances, EnergyCons, Prices_dom, IO_GTAP, HHSurvey, Tran_Scatter. Every other table is non-proprietary; a table derived from a proprietary one is non-proprietary, with its derivation in the provenance column.
- **Public editions hold perturbed proprietary values** (user 2026-10-30): the Egypt rows of the proprietary tables, and Excel-AI's copies of them, multiplied by random factors within +-3% with their identities kept (`data/scripts/perturb_proprietary.py`); the factors are not stored. Column `values` of the edition's `data_sources.csv` says `public`, `perturbed`, `derived-real` (computed from the real data before the perturbation; to be rebuilt) or `real` (full editions only). This repository never holds a `full-real` edition or a table marked `real` (the data tests check it). `CPAT_LegacyData*.xlsx` is git-ignored except the editions' `legacy_xlsx/CPAT_LegacyData.xlsx`.
- **Exceptions:** test fixtures stay with their tests (`coded/cpat_testing/model/data_expected/`).
- **Archived:** the earlier folder (dummy pipeline, data workbooks in Python and CPAT format, `legacy_dummy/`, `mvp_legacy_extracts/`, distribution pipeline, air-pollution extracts) was renamed `data_old/` and removed on 2026-10-30; the user keeps the archive. The code was repointed to `data/` on 2026-10-30 (`CAVEATS.md`).

The legacy workbook and the team's reference files:

| File | What it is | Rule |
|---|---|---|
| `data/legacy/CPAT 1.0pre_465_Shell.xlsb` | **The latest legacy workbook** (user 2026-10-22; 62 of our bugs marked fixed by the CPAT team, checked in `excel_ai/bugs_and_legacy/fixes/check465/`), the only reference copy (user 2026-10-30: older versions and copies deleted), its six proprietary tabs empty (the shell). Each edition holds it filled with its own six tables (`data/<edition>/legacy/`, `data/scripts/legacy_proprietary.py fill`) | Read-only ground truth, except `legacy_proprietary.py`. Never edit or re-save it by hand; work on a copy in a scratch folder. Since v0.8.2 the register's cell references are 465 rows (`excel_ai/bugs_and_legacy/fixes/data/rowmap_456_465.json`); since v0.8.4 ScenarioDefinition has the 465 MTInputs rows |
| `excel_ai/bugs_and_legacy/reference/CPATMasterProcessesCodesAndDefaults.xlsx` | The CPAT team's master list of codes, processes and defaults | Read-only reference (may be inaccurate in places; an alignment exercise is planned) |
| (tracker) | The CPAT team's bug and issue tracker became the master list `excel_ai/bugs_and_legacy/Tracking_Legacy_Bugs_v<version>.xlsx` (v0.8.4, user 2026-10-28; was `excel_ai/bugs_and_legacy/Tracking issues.xlsx`) | **Editable** (user 2026-10-18): the team's tabs are kept as they are; tabs ReadMe, Bugs and Issues are written from the register by `make_tracker.py` at every release (the columns Date, CPAT Version and Issue raised by of tab Bugs are read back, so edits there stay) |

The earlier legacy workbooks 456 and 459 were removed on 2026-10-30 (user: keep only the latest); they remain in the git history. Tools that read them (the prototype's data extracts, the Methods, some bug-fix tools) need repointing to 465 (`CAVEATS.md`, 2026-10-30).

## 9. Modules: how they work (user 2026-10-29)

Distribution, air pollution (AP) and transport co-benefits (TCB) are **modules**: free-standing workbooks, each with its own builder, version and release, that exchange values with the mitigation prototype (the core) and with each other through files in `excel_ai/active_workbooks/`. This section is the one place for the module rules; sections 0-8 apply to every module as to the prototype. Plan and history: [`excel_ai/core/plans/Modules.md`](plans/Modules.md); prompts to build each module: [`excel_ai/core/prompts/`](prompts/README.md).

### 9.1 What a module is

| | Rule |
|---|---|
| Sources | `excel_ai/<module>/` (`distribution/`, `air_pollution/`, `transport_cobenefits/`): builder `build_<module>.py`, check `check_<module>.py`, VBA `.bas`, README, Python reference `<module>_ref.py`; data in `data/<module>/` (section 8) |
| Files | `excel_ai/CPAT-AI-<Module>-Prototype_v<version>.xlsm` (`Distribution`, `Air-Pollution`, `Transport-Cobenefits`); older versions in `excel_ai/<module>/releases/`; `<Name>_latest.xlsm` in **both** `excel_ai/active_workbooks/` and `excel_ai/active_workbooks/`, written by `excel_ai/core/tools/release.py` `publish(link=True)` (5a) |
| Version | Its own `VERSION` and version table (5b), which names the mitigation version it was built and checked with |
| Register | Its bugs and issues go in the one register (`excel_ai/bugs_and_legacy/register/issues_register.py`, field Module), with the same codes (section 0); no list of its own |
| Free-standing | After its inputs are filled, the module calculates with no link to another workbook: no external references in formulas, no Power Query left live, data tabs inside the workbook |

### 9.2 Encapsulation: inputs in, outputs out

Every module workbook has the same tab structure, in this order:

| Tab | Content | Rule |
|---|---|---|
| `Cover` | Contents (2.7), the **link table** (source file of each input tab, its path, saved time, scenario names read) and the buttons | The run order of the modules (9.4) is written on it |
| `From<Source>` | **Inputs from another workbook**, values only: `FromMitigation` (every module), `FromAirPollution` (TCB) | Same rows, codes and columns as the source block (9.3), filled by the update macro, shipped with the values of the build. The only place the module reads another workbook's numbers |
| `ScenarioDefinition` | The legacy MTInputs rows (section 4); the module's rows green, the rest grey | Module options that legacy does not have (for example a method switch) go below the last legacy row, with the default = legacy |
| Calculation sheet | The legacy sheet name (`Distribution`, `Air pollution`, `Transport`) | Reads only its `From<Source>` tabs, `ScenarioDefinition`, its data tabs and constants. Never another workbook, never a hard-coded copy of an input |
| `To<Consumer>` | **Outputs for other workbooks**: `ToMitigation` (AP, TCB), `ToTransportCB` (AP: VSL and earnings) | Plain copies of calculation rows (no calculation), one defined name each (`Out<Module>`: `OutAP`, `OutTCB`, `OutAPtoTCB`), in the layout and codes the consumer's `From<Module>` tab expects |
| Data tabs, `Check` | Legacy tables unchanged under the legacy dividers (1.5); the check summary | |

Column norms: **a time-series module (AP, TCB) has exactly the Mitigation column layout** (1.1: A-J descriptors, K code column, L..AE = 2022..2041, spacer, groups of 22 columns, years in row 1, scenario name and number in rows 4-5, groups 1-7, group 2 the LAMBDA group, differences against scenario 1 by `.ref`; 3c rule 4, 3e). Its `From`/`To` tabs use the same columns, so a row copies 1:1. A single-year module (Distribution) keeps its own group (1.1b) and reads `FromMitigation` through the offset row. Visual style (2), formulas and names (3, 3b-3d), copy-paste (3e) and lint (3g) apply unchanged.

### 9.3 Links between workbooks (at this stage: files in `excel_ai/active_workbooks/`)

1. **By file, not by formula.** A module's update macro (`UpdateFrom<Source>`, button on Cover) finds `<Source>_latest.xlsm` next to the module, then in `active_workbooks/` (one or two folders up), or the path or web address typed on Cover. If the file is open, its current values are used; otherwise it is opened read-only, without macros or recalculation, and closed. It copies values **by code**, checks that every row is the same variable (stops with a list of mismatches otherwise), writes the link table on Cover and recalculates. Power Query on the same files replaces the file search later (TODO M6); the copy-by-code contract stays.
2. **What each module reads and writes:**

| Module | Reads (source block in the source workbook) | Writes (its `To` tab) | Read by |
|---|---|---|---|
| Distribution | Mitigation section 19a (defined name `ExportDistn`) | Results by decile (MTOutputs codes `<iso>.distn.*`) | (reports) |
| Air pollution | Mitigation section 15 "Local air pollutants: outputs to the air pollution module" (emissions `aps.<pol>.<sec>`, fuel use, GDP, population, deflator) | `ToMitigation`: the rows of Mitigation tab `FromAirPollution` (value of averted PM2.5, concentration coefficients, unit costs); `ToTransportCB`: VSL, daily earnings | Mitigation; TCB |
| Transport co-benefits | Mitigation section 5b "Road transport: engineer model and outputs to the transport co-benefits module" (vehicle-km, freight vehicle-km, fuel economy, class splits, road share of each fuel, road and total fuel use), GDP, population; AP `ToTransportCB` | `ToMitigation`: the rows of Mitigation tab `FromTransportCB` (per-km costs `tran.acc.km`, `tran.con.km`, `tran.rdm.km`), plus $/l and welfare under legacy codes | Mitigation |

3. **The source block names the module.** A Mitigation section a module reads says so in its band ("... outputs to the ... module"); a row in it is never renamed or reordered without the module's builder and check in the same task. Sections 15 and 5b are read in place (no copies, user 2026-10-29); section 19 holds 19a only.
4. **Until a source module exists**, the consumer's `From<Module>` tab holds legacy 465 Egypt values, typed, with the legacy cell in the source column and an issue in the register ("typed until module X exists"); the tab keeps the layout the module will fill.
5. **Never commit a copy filled with real data** (sections 5a, 8): the active workbooks hold the public data of the build.

### 9.4 Scenarios and run order

- **One scenario at a time, no batch** (user 2026-10-22): set the live scenario in Mitigation (group 2), save it as `_latest`, update the module, read its results. The `From` tabs carry the groups of Mitigation (baseline and live scenario; capacity groups 1-7, 3e).
- **Run order:** Mitigation, then air pollution, then transport co-benefits (it reads AP), then Distribution; then, where Mitigation reads module outputs (welfare, Pigouvian taxes), update Mitigation's `From<Module>` tabs and recalculate. Each update copies values, so there is no circular reference between workbooks; the feedback is one explicit step.

### 9.5 Methods, modes and legacy

- **Legacy first** (section 0): the module reproduces the legacy sheet (465), bugs fixed and registered (L), issues replicated and registered (I).
- **A method switch is a mode** in `ScenarioDefinition` below the legacy rows (section 4), default = legacy. A mode that departs from legacy is an upgrade (U) or a departure by user decision (LD), registered as such (example: TCB `TcbMode` = `Legacy` | `Engineer`, issue I100).

### 9.6 Checks and release of a module

`check_<module>.py`, at every release: lint (3g); no formula reads outside the `From` tabs, `ScenarioDefinition`, data tabs and constants; no external links; every `From` tab equals its source block through the macro's row mapping; the `To` tab matches the consumer's `From` tab row by row; the Python reference reproduces legacy cached values with the fixes off and the workbook with the fixes on; paste test of the groups (3e); end to end (change Mitigation's live scenario, update, recalculate: the results move as the reference says). Then: README of the module, `CAVEATS.md` entry, TODO, register, publish to `releases/` and both permalink folders.
