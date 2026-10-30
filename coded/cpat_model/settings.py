"""Run settings: what Excel-AI holds on its Settings tab and the run itself chooses (spec section 6).

Scenario inputs are not here (they are the scenario set, cpat_model.inputs); inputs that Excel-AI reads from the
baseline column for every scenario are run settings (D16), filled from the scenario set by inputs.global_settings.
"""
from dataclasses import dataclass, field, replace
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


@dataclass
class Settings:
    database: str = 'dummy'                       # 'dummy': an edition of this repository; 'full': the private one
    data_path: Path | None = None                 # the tidy folder; default: data/<edition>/tidy, FULL_DATA_PATH (full)
    countries: tuple = ('EGY',)
    base_year: int = 2022                         # Excel-AI BASE_YEAR (t0)
    last_year: int = 2041                         # Excel-AI LAST_YEAR
    last_hist_price_year: int = 2024              # Excel-AI LAST_HIST (Settings C10, L)
    results_year: int = 2026                      # year of the real USD of money values (MTInputs ResultsYear)
    global_settings: dict = field(default_factory=dict)   # D16: from the baseline column of the scenario set
    base: object = None                           # the baseline inputs (Excel-AI SDBase: settings read from scenario 1)

    def with_globals(self, values, base=None):
        """D16: these settings with the global inputs of a scenario set (its baseline column) and its baseline inputs."""
        return replace(self, global_settings=values, base=base,
                       results_year=int(values.get('ResultsYear', self.results_year)),
                       last_hist_price_year=int(values.get('LastHistPriceYear', self.last_hist_price_year)))

    @property
    def years(self):
        return list(range(self.base_year, self.last_year + 1))

    def tidy_path(self):
        if self.data_path:
            return Path(self.data_path)
        if self.database == 'full':
            import os
            p = os.getenv('FULL_DATA_PATH')
            if not p:
                raise ValueError('FULL_DATA_PATH must point at the tidy folder of the full database')
            return Path(p)
        return REPO / 'data' / edition() / 'tidy'


def edition():
    """The data edition of this repository the run reads (data/editions.csv): CPAT_DATA_EDITION, else the default."""
    import csv
    import os
    if os.getenv('CPAT_DATA_EDITION'):
        return os.environ['CPAT_DATA_EDITION']
    with open(REPO / 'data' / 'editions.csv', encoding='utf-8') as f:
        return next(r['edition'] for r in csv.DictReader(f) if r['default'] == 'yes')


def edition_info(name=None):
    """The data edition's manifest fields shown on outputs: edition, type, version (data/<edition>/EDITION.json)."""
    import json
    name = name or edition()
    p = REPO / 'data' / name / 'EDITION.json'
    man = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
    return {'data_edition': name, 'data_type': man.get('type', ''), 'data_version': man.get('version', '')}
