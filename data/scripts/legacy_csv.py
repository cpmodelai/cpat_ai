"""The legacy-form CSV files Excel-AI's scripts read, written from an edition's tidy/ into a build cache.

    from legacy_csv import legacy_dir, save_to_tidy
    DATA = legacy_dir()        # .buildcache/legacy_csv/<edition>/ at the repository root, rewritten when tidy/ is newer

The edition: CPAT_DATA_EDITION, else the default of data/editions.csv (data/scripts/editions.py).

The cache holds every file of the specs (tidy_specs.py) under its legacy file name (legacy_Balances.csv, power_tech.csv,
ap459_gbd.csv, ...), cell for cell as the earlier data/mvp_legacy_extracts/ held them. It is a build product: never edit
it and never commit it (.gitignore: .buildcache/). A script that writes a table writes it into the cache, then calls
save_to_tidy(), which converts the cache back into the edition's tidy/ (the source of truth).

Command line, from the repository root:
    python data/scripts/legacy_csv.py              # (re)write the cache, print its path
    python data/scripts/legacy_csv.py --save       # the cache -> the edition's tidy/ (after a script wrote into it)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import editions as ED  # noqa: E402
import tidy_convert as tc  # noqa: E402

TIDY = ED.tidy()
CACHE = os.path.join(ED.REPO, '.buildcache', 'legacy_csv', ED.name())
STAMP = os.path.join(CACHE, '.written')


def _newest(path):
    return max(os.path.getmtime(os.path.join(d, f)) for d, _, fs in os.walk(path) for f in fs)


def legacy_dir(force=False):
    """The cache folder, rewritten from tidy/ when it is missing or older than tidy/."""
    if force or not os.path.exists(STAMP) or _newest(TIDY) > os.path.getmtime(STAMP):
        tables = tc.from_tidy(TIDY)
        for name, (head, rows) in tables.items():
            tc.write_csv(os.path.join(CACHE, name), head, rows)
        with open(STAMP, 'w', encoding='utf-8') as f:
            f.write(f'{len(tables)} files from {TIDY}\n')
    return CACHE


def save_to_tidy():
    """The cache (with the tables a script wrote) -> tidy/; then the cache is current again."""
    tc.to_tidy(tc.read_legacy(CACHE), TIDY)
    os.utime(STAMP)
    print(f'{TIDY} updated from the cache: rewrite the workbook (tidy_convert.py to-xlsx), build_edition.py, the data tests')


if __name__ == '__main__':
    if '--save' in sys.argv:
        save_to_tidy()
    else:
        print(legacy_dir(force=True))
