"""Write an edition's manifest and table list: <edition>/EDITION.json and <edition>/data_sources.csv.

Every edition (data/editions.csv) has the same structure (data/README.md) and one manifest at its root:

    EDITION.json       the edition's row of data/editions.csv (type, based_on, legacy base, version, status), the
                       perturbation (public-perturbed editions), and the SHA-256 of every file of the edition
    data_sources.csv   data/catalog.csv plus the column values: what the values of each table are in this edition
                         real          the real values (full-real editions only)
                         public        public data, as published
                         perturbed     a proprietary table, or a copy of one, perturbed (perturb_proprietary.py)
                         derived-real  computed from the real data before the perturbation (model outputs, fits): to be
                                       rebuilt on the perturbed data

Models print the edition and version on their outputs, so a result says which data made it. The data tests fail on a
stale manifest, and on a full-real edition or a table marked real in this repository.

Run from the repository root after any change of an edition (and after build_catalog.py):
    python data/scripts/build_edition.py [--edition Public01]
"""
import argparse
import csv
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import editions as ED  # noqa: E402

FOLDERS = ['tidy', 'legacy_xlsx', 'legacy', 'inputs']

# public-perturbed: the tables perturbed (the six proprietary ones and Excel-AI's copies of them)
PERTURBED = {'energy_balances.csv', 'energy_consumption.csv', 'prices_domestic.csv', 'prices_domestic_corrections.csv',
             'hh_survey.csv', 'io_gtap.csv', 'tran_scatter.csv', 'xai_energy_balance.csv', 'xai_energy_use.csv',
             'xai_power_demand.csv'}
# Public01: tables computed from the real data before the perturbation (empty once rebuilt on the perturbed data)
DERIVED_REAL = {'Public01': {'xai_legacy_cached_baseline.csv', 'xai_legacy_engineer_reference.csv',
                             'xai_legacy_power_reference.csv', 'xai_legacy_transport_reference.csv',
                             'xai_legacy_mtoutputs_465.csv'}}
PERTURBATION = {'scripts': 'data/scripts/perturb_proprietary.py, data/scripts/legacy_proprietary.py fill',
                'delta': 0.03, 'factors_stored': False}


def values(edition, kind, row):
    if kind == 'full-real':
        return 'real'
    if row['tidy_file'] in PERTURBED or row['proprietary'] == 'proprietary':
        return 'perturbed'
    return 'derived-real' if row['tidy_file'] in DERIVED_REAL.get(edition, set()) else 'public'


def checksums(edition=None):
    root = ED.root(edition)
    files = {'data_sources.csv': os.path.join(root, 'data_sources.csv')}
    for folder in FOLDERS:
        for d, _dirs, names in os.walk(os.path.join(root, folder)):
            for n in names:
                p = os.path.join(d, n)
                files[os.path.relpath(p, root).replace(os.sep, '/')] = p
    out = {}
    for rel in sorted(files):
        with open(files[rel], 'rb') as f:
            out[rel] = hashlib.sha256(f.read()).hexdigest()
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--edition', default=None)
    args = p.parse_args()
    e, info, root = ED.name(args.edition), ED.info(args.edition), ED.root(args.edition)
    with open(os.path.join(ED.DATA, 'catalog.csv'), encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    head = list(rows[0]) + ['values']
    for r in rows:
        r['values'] = values(e, info['type'], r)
    with open(os.path.join(root, 'data_sources.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, head, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    man = {k: info[k] for k in ('edition', 'type', 'based_on', 'legacy_base', 'version', 'status', 'notes')}
    if info['type'] == 'public-perturbed':
        man['perturbation'] = {**PERTURBATION, 'date': info['version']}
    man['files'] = checksums(args.edition)
    with open(os.path.join(root, 'EDITION.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(man, f, indent=1, ensure_ascii=False)
        f.write('\n')
    n = {v: sum(r['values'] == v for r in rows) for v in ('real', 'public', 'perturbed', 'derived-real')}
    print(f"{e}: EDITION.json ({info['type']}, version {info['version']}, {len(man['files'])} files), "
          f'data_sources.csv {n}')


if __name__ == '__main__':
    main()
