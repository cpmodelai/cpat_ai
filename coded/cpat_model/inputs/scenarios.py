"""A scenario set: the rows of legacy MTInputs and Excel-AI's additions, keyed by NameOfParameter (D5).

File form (data/inputs/scenarios_<name>.csv): columns `row, name, label, unit`, then one column per scenario
number (1 = baseline). Two records come first: `_ScenarioName` and `_Countries` (ISO3 codes separated by spaces, or
`all`). Values are the text of the input cells, in legacy units (I85).
"""
import csv
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[3] / 'data' / 'inputs' / 'scenarios_excel_ai.csv'

# Inputs Excel-AI reads from the baseline column for every scenario: run settings (D16)
GLOBAL_INPUTS = ['ResultsYear', 'LastHistPriceYear', 'SCCTargetConsistentCP', 'SCCRise', 'SCCTargetYear',
                 'SCCEpaBaseYear', 'NSCCSource', 'GSCCSource', 'NSCCDiscountRate', 'NSCCMargUtilofCons',
                 'ETSOBREffectiveness', 'DomPrTax', 'GlobalEnergyDemand', 'PassLo', 'PassMid', 'PassHi',
                 'GovPriceControls', 'BiomassLeakage', 'BiomassNormal', 'NatGasEff', 'LPGEff', 'KerEff', 'BioEff']

# Python inputs below the Excel-AI rows (added to Excel-AI at its next release): name, label, unit, default
PYTHON_ROWS = [('ModelForm', 'Form of the demand equations (D4): CPAT, CPAT partial adjustment, CES partial '
                'adjustment, CDPM-FTT', 'option', 'CPAT')]


def number(text):
    """An input cell as a number where it is one, else the text (blank -> None)."""
    if text in ('', None):
        return None
    try:
        return float(text)
    except ValueError:
        return text


class Inputs:
    """The inputs of one scenario: inputs['CPLevelTarget'] -> 50.0; an unknown name is an error."""

    def __init__(self, number_, values, name, countries):
        self.number, self.values, self.name, self.countries = number_, values, name, countries

    def __getitem__(self, key):
        if key not in self.values:
            raise KeyError(f'{key} is not an input (NameOfParameter) of the scenario set')
        return number(self.values[key])

    def text(self, key):
        return self.values[key]


class ScenarioSet:
    def __init__(self, rows, scenario_cols):
        self.rows, self.cols = rows, scenario_cols
        self._check()

    def _check(self):
        names = [r['name'] for r in self.rows if r['name'] and not r['name'].startswith('_')]
        dup = {n for n in names if names.count(n) > 1}
        assert not dup, f'NameOfParameter repeated: {sorted(dup)}'
        assert self.cols and self.cols[0] == '1', 'scenario 1 (the baseline) must come first'

    def numbers(self):
        return [int(c) for c in self.cols]

    def inputs(self, n):
        col = str(n)
        meta = {r['name']: r[col] for r in self.rows if r['name'].startswith('_')}
        values = {r['name']: r[col] for r in self.rows if r['name'] and not r['name'].startswith('_')}
        countries = meta.get('_Countries', 'all').split()
        return Inputs(n, values, meta.get('_ScenarioName', ''), countries)

    def global_settings(self):
        """D16: the baseline values of the inputs read for every scenario; warn where another scenario differs."""
        base = self.inputs(1)
        out = {}
        for name in GLOBAL_INPUTS:
            if name in base.values:
                out[name] = base[name]
                for n in self.numbers()[1:]:
                    if self.inputs(n).values.get(name) != base.values[name]:
                        print(f'warning: {name} differs in scenario {n}; the baseline value is used (as Excel-AI)')
        return out


def read_scenario_set(path=DEFAULT):
    with open(path, encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        cols = [c for c in reader.fieldnames if c.isdigit()]
    return ScenarioSet(rows, cols)
