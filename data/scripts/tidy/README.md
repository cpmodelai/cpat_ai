# Tidy converter: legacy layout <-> tidy CSV

Two-way conversion between the data tabs of legacy CPAT (the layout Excel-AI is built from) and the tidy CSV tables Coded CPAT reads (user decision 2026-10-29; [`../../INTERFACE.md`](../../INTERFACE.md)).

| File | What it is |
|---|---|
| `tidy_convert.py` | The converter (commands `to-tidy`, `to-legacy`, `check`) |
| `tidy_specs.py` | What each legacy table becomes: keys, describing columns, which headers melt into a variable |
| `tidy_blocks.py` | The legacy tabs kept at their cell addresses, and their data blocks |

```bash
# from the repository root
python data/scripts/tidy/tidy_convert.py to-tidy   --legacy data/mvp_legacy_extracts --out data/tidy
python data/scripts/tidy/tidy_convert.py to-legacy --tidy data/tidy --xlsx legacy_style.xlsx    # pastes onto legacy CPAT
python data/scripts/tidy/tidy_convert.py to-legacy --tidy data/tidy --out legacy_csv/            # the files Excel-AI reads
python data/scripts/tidy/tidy_convert.py to-tidy   --legacy legacy_style.xlsx --out tidy_from_xlsx/
python data/scripts/tidy/tidy_convert.py check     --legacy data/mvp_legacy_extracts            # both round trips
pytest data/tests/test_tidy_roundtrip.py
```

**Exactness.** legacy CSV -> tidy -> legacy CSV gives back every cell as the same text. Through the legacy-style workbook, every value comes back to 16 significant digits (openpyxl writes 16) and whole numbers lose a trailing `.0`. The test also fails if the committed `data/tidy/` is stale.

**Tidy form.** One CSV per table, one observation per row, keys first (`country` = ISO3 upper case, `year`, `code`, ...), then `value` (or one column per variable where the legacy columns are different variables). Headers that are values of a dimension (years, fuels, sectors, GTAP sectors, price codes) become a column. What is not data (headers in their legacy form, country names, row order, rows repeated in legacy, the titles, labels and notes of the cells tabs) goes to `_layout/`, so the legacy form comes back exactly. `_manifest.csv` lists the tables.

**Adding data in tidy form.** A row with a new key (a new country) is written after the rows the layout knows, with the legacy case of the country key; its describing columns (country name) are left blank in the legacy table. A new column of a melted header (a new year) stops the conversion: the legacy table has no place for it.
