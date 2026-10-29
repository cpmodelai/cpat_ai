"""Run settings: what Excel-AI holds on its Settings tab and the run itself chooses (spec section 6).

Scenario inputs are not here (they are the scenario set, cpat_model.inputs); inputs that Excel-AI reads from the
baseline column for every scenario are run settings (D16), filled from the scenario set by inputs.global_settings.
"""
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


@dataclass
class Settings:
    database: str = 'dummy'                       # 'dummy' (this repository) or 'full' (private repository)
    data_path: Path | None = None                 # the tidy folder; default: data/tidy (dummy), FULL_DATA_PATH (full)
    countries: tuple = ('EGY',)
    base_year: int = 2022                         # Excel-AI BASE_YEAR (t0)
    last_year: int = 2041                         # Excel-AI LAST_YEAR
    last_hist_price_year: int = 2024              # Excel-AI LAST_HIST (Settings C10, L)
    results_year: int = 2022                      # year of the real USD of money values (R)
    global_settings: dict = field(default_factory=dict)   # D16: from the baseline column of the scenario set

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
        return REPO / 'data' / 'tidy'
