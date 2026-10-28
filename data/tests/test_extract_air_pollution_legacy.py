"""Verify Air Pollution CSV extracts preserve the legacy source tables."""

import csv
import importlib.util
import os
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO_ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import extract_air_pollution_legacy as ap  # noqa: E402


@pytest.fixture(scope="module")
def extracted(tmp_path_factory):
    pytest.importorskip("pyxlsb")
    if not ap.DEFAULT_SOURCE.is_file():
        pytest.skip("legacy 1.0pre_459 NoPropData workbook is not present")
    output_dir = tmp_path_factory.mktemp("air_pollution_legacy")
    dimensions = ap.extract(ap.DEFAULT_SOURCE, output_dir)
    return output_dir, dimensions


def test_air_pollution_csvs_match_legacy_tables(extracted):
    pyxlsb = pytest.importorskip("pyxlsb")
    output_dir, dimensions = extracted

    with pyxlsb.open_workbook(str(ap.DEFAULT_SOURCE)) as workbook:
        assert set(ap.SOURCE_SHEETS).issubset(workbook.sheets)
        for sheet_name in ap.SOURCE_SHEETS:
            with workbook.get_sheet(sheet_name) as sheet:
                source_rows = ap.read_sheet_rows(sheet)

            csv_path = output_dir / ap.OUTPUT_NAMES[sheet_name]
            with csv_path.open(encoding="utf-8", newline="") as stream:
                extracted_rows = list(csv.reader(stream))

            expected_rows = [
                ["" if value is None else str(value) for value in row]
                for row in source_rows
            ]
            assert extracted_rows == expected_rows, sheet_name
            with (ap.DEFAULT_OUTPUT / ap.OUTPUT_NAMES[sheet_name]).open(encoding="utf-8", newline="") as stream:
                assert list(csv.reader(stream)) == expected_rows, sheet_name
            assert dimensions[sheet_name] == (
                len(source_rows),
                max((len(row) for row in source_rows), default=0),
            )


def test_manifest_lists_all_air_pollution_tables(extracted):
    output_dir, dimensions = extracted
    with (output_dir / "manifest.csv").open(encoding="utf-8", newline="") as stream:
        manifest = list(csv.DictReader(stream))

    assert [row["Source sheet"] for row in manifest] == list(ap.SOURCE_SHEETS)
    assert len(manifest) == len(dimensions) == 9


def test_recovered_air_pollution_builder(tmp_path, monkeypatch):
    openpyxl = pytest.importorskip("openpyxl")
    builder_path = ap.REPO_ROOT / "excel_ai" / "air_pollution" / "build_workbook.py"
    spec = importlib.util.spec_from_file_location("ap_recovery_builder", builder_path)
    assert spec is not None and spec.loader is not None
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    output = tmp_path / "air_pollution_smoke.xlsx"
    monkeypatch.setattr(builder, "OUTPUT", output)
    assert builder.build_workbook() == output
    assert len(builder.input_codes()) == 80
    workbook = openpyxl.load_workbook(output)
    assert len(workbook.sheetnames) == 13
    assert set(ap.SOURCE_SHEETS).issubset(workbook.sheetnames)
    assert not workbook._external_links
    workbook.close()
