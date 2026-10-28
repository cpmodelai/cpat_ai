"""Extract public Air Pollution reference tables from legacy CPAT 1.0pre_459.

Only the nine DATA_AIR_POLL tables are exported. The legacy workbook is opened
read-only; the Air pollution calculation sheet and all other workbook sheets
are excluded. The output preserves source row/column positions so stacked
legacy tables and header offsets remain traceable.

Run from the repository root:
    python data/scripts/extract_air_pollution_legacy.py
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
DEFAULT_SOURCE = (
    REPO_ROOT
    / "excel_ai"
    / "legacy"
    / "workbooks"
    / "CPAT 1.0pre_459_NoPropData.xlsb"
)
DEFAULT_OUTPUT = REPO_ROOT / "data" / "air_pollution" / "legacy_459"

SOURCE_SHEETS = (
    "WB",
    "GBD",
    "IHME",
    "ILO",
    "ExposureCoefs",
    "IF PP",
    "ConcMat",
    "Air_Data",
    "Air_meta",
)
OUTPUT_NAMES = {
    "WB": "wb.csv",
    "GBD": "gbd.csv",
    "IHME": "ihme.csv",
    "ILO": "ilo.csv",
    "ExposureCoefs": "exposure_coefs.csv",
    "IF PP": "if_pp.csv",
    "ConcMat": "conc_mat.csv",
    "Air_Data": "air_data.csv",
    "Air_meta": "air_meta.csv",
}


def trim_trailing_empty(values: list[object]) -> list[object]:
    while values and values[-1] is None:
        values.pop()
    return values


def read_sheet_rows(sheet) -> list[list[object]]:
    rows = [trim_trailing_empty([cell.v for cell in row]) for row in sheet.rows()]
    while rows and not rows[-1]:
        rows.pop()
    return rows


def verify_csv_rows(csv_path: Path, source_rows: list[list[object]], sheet_name: str) -> None:
    with csv_path.open("r", newline="", encoding="utf-8") as stream:
        actual_rows = list(csv.reader(stream))
    expected_rows = [
        ["" if value is None else str(value) for value in row]
        for row in source_rows
    ]
    if actual_rows != expected_rows:
        raise ValueError(f"Extracted CSV differs from source sheet {sheet_name!r}.")


def extract(source: Path, output_dir: Path) -> dict[str, tuple[int, int]]:
    try:
        from pyxlsb import open_workbook
    except ImportError as exc:
        raise RuntimeError("Install pyxlsb to extract the legacy .xlsb tables.") from exc

    if not source.is_file():
        raise FileNotFoundError(f"Legacy workbook not found: {source}")

    output_dir.mkdir(parents=True, exist_ok=True)
    dimensions: dict[str, tuple[int, int]] = {}
    with open_workbook(str(source)) as workbook:
        missing = sorted(set(SOURCE_SHEETS) - set(workbook.sheets))
        if missing:
            raise ValueError("Legacy workbook is missing AP data tab(s): " + ", ".join(missing))

        for sheet_name in SOURCE_SHEETS:
            with workbook.get_sheet(sheet_name) as sheet:
                rows = read_sheet_rows(sheet)

            max_columns = max((len(row) for row in rows), default=0)
            output_path = output_dir / OUTPUT_NAMES[sheet_name]
            with output_path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.writer(stream)
                writer.writerows(rows)
            verify_csv_rows(output_path, rows, sheet_name)
            dimensions[sheet_name] = (len(rows), max_columns)

    manifest_path = output_dir / "manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("Source workbook", "Source sheet", "Output CSV", "Rows", "Columns"))
        for sheet_name, (row_count, column_count) in dimensions.items():
            writer.writerow((source.name, sheet_name, OUTPUT_NAMES[sheet_name], row_count, column_count))

    return dimensions


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    dimensions = extract(args.source, args.out_dir)
    for sheet_name, (row_count, column_count) in dimensions.items():
        print(f"{sheet_name}: {row_count} rows x {column_count} columns")
    print(f"Wrote AP tables to {args.out_dir}")


if __name__ == "__main__":
    main()