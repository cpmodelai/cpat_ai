"""1.2.2 (user 2026-10-31): the cooking-fuel table Mitigation reads instead of the household survey (HHSurvey) and
WHOCooking, which are distribution data.

Mitigation needs two things from them, both for residential cooking fuel (legacy Mitigation rows 1784-1795, K1795):
- the country's most-used cooking fuel (WHOCooking main_fuel, overall sample): the fuel that leaks to biomass and the
  fuel an exemption covers (CookFuel);
- for the initial exemption of the bottom deciles (MTInputs ExemptMostCook, ExemptCookDeciles): the share of the
  economy-wide spend on that fuel paid by each decile (ExemptCookShare = the sum over the exempt deciles).
  Share of decile d = budget share x consumption per head x population weight of decile d (overall sample, mean)
  over the same product for the whole-sample basket row (quant_cons 9999), as legacy K1795 and v0.9.0 R6.3 (I136).

Writes (the data edition, through the build cache of data/scripts/legacy_csv.py):
  cooking_fuel.csv   key, country, fuel, item, d1..d10
                     <ISO3>|main   the most-used cooking fuel in column fuel (blank if WHOCooking has it blank)
                     <ISO3>|<fuel> the decile shares of the spend on the fuel, for the fuels that can be exempted or leak
                                   (gas, LPG, kerosene: build.py LK_FUELS); rows only where the survey has the basket row
Every country of the edition's HHSurvey and WHOCooking. The values are derived from HHSurvey (proprietary): perturbed in a
public edition, real in a full one.

    python extract_cooking.py          # writes the cache file and saves the edition's tidy/
"""
import os as _os, sys as _sys  # the excel_ai code folders and data/scripts on the path (core/tools/xlpaths.py)
_xl = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_xl) != 'excel_ai':
    _xl = _os.path.dirname(_xl)
_sys.path.insert(0, _os.path.join(_xl, 'core', 'tools'))
import xlpaths  # noqa: E402,F401
from legacy_csv import legacy_dir, save_to_tidy  # noqa: E402  (data/<edition>/tidy/ in the legacy CSV form)
import csv
import os

DATA = legacy_dir()
FUELS = ['nga', 'lpg', 'ker']          # build.py LK_FUELS: the residential fuels that can be exempted or leak
BASKET_Q = '9999'                      # build.py BasketQ: the quantile code of the whole-sample basket row
HEAD = ['key', 'country', 'fuel', 'item'] + [f'd{d}' for d in range(1, 11)]
ITEM_MAIN = 'Most-used cooking fuel (WHOCooking main_fuel, overall sample)'
ITEM_SHARE = 'Share of the economy-wide spend on the fuel by decile (HHSurvey overall mean: budget share x consumption per head x population weight, over the basket row)'


def read(name):
    with open(os.path.join(DATA, name), encoding='utf-8', newline='') as f:
        return list(csv.reader(f))


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0                     # as the workbook's IFERROR(...,0) on a missing or text value


def rows():
    who = read('legacy_WHOCooking.csv')
    wh = who[0]
    out = []
    main = {r[wh.index('iso3')].upper(): r[wh.index('main_fuel')] for r in who[1:]
            if r[wh.index('code')].endswith('.distn.pcoff.ove')}
    hh = read('legacy_HHSurvey.csv')
    h = hh[0]
    by_code = {r[0]: r for r in hh[1:]}
    countries = sorted(set(main) | {r[h.index('iso3')].upper() for r in hh[1:]})
    for iso in countries:
        if iso in main:
            out.append([f'{iso}|main', iso, main[iso], ITEM_MAIN] + [''] * 10)
        bkt = by_code.get(f'{iso}.distn.bsh.bkt.ove.mean.{BASKET_Q}')
        if not bkt:
            continue
        for fu in FUELS:
            col = f'{fu}_share'
            if col not in h:
                continue
            spend = lambda r: num(r[h.index(col)]) * num(r[h.index('cons_pc_acrent')]) * num(r[h.index('popw')])
            tot = spend(bkt)
            if tot == 0:
                continue
            sh = []
            for d in range(1, 11):
                r = by_code.get(f'{iso}.distn.bsh.dec.ove.mean.{d}')
                sh.append(repr(spend(r) / tot) if r else '0')
            out.append([f'{iso}|{fu}', iso, fu, ITEM_SHARE] + sh)
    return out


def main():
    out = rows()
    with open(os.path.join(DATA, 'cooking_fuel.csv'), 'w', encoding='utf-8', newline='') as f:
        csv.writer(f, lineterminator='\n').writerows([HEAD] + out)
    print(f'cooking_fuel.csv: {len(out)} rows, {len({r[1] for r in out})} countries')
    save_to_tidy()


if __name__ == '__main__':
    main()
