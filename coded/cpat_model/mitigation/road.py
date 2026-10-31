"""Block 5b, the road transport engineer model (Mitigation section 5b): vehicle stocks, purchases and retirements,
total cost of ownership (TCO), the choice between internal-combustion vehicles (ICEV) and battery EVs (BEV), fuel
economy, distance driven and fuel use, for passenger vehicles (new and used), freight vehicles, 2-3 wheelers and buses.

prepare  the data rows by year (country data, paths, vehicle prices) and the parameters (road_data; EQ-A3.5).
step     one year t: stock and ownership (EQ-A3.6), TCO and EV choice (EQ-A3.7), fuel economy, distance and
         fuel use (EQ-A3.8), results for the transport co-benefits module (EQ-A3.9).

The model runs whatever TrModel says. With TrModel = Elasticity (tr.sw = 0, as Egypt) fuel use of sections 5-8 stays
the elasticity model's and the results here go only to the transport co-benefits module (sections 17b and 18). With
TrModel = Engineer (tr.sw = 1) road gasoline, diesel, LPG, gas and biofuels take trkt and trbio (fuel_use.step, EQ-M3.2)
and road electricity demand after the base year takes trkte (power.step, EQ-M4.1); so step runs before them in the year.
Rows are named as Excel-AI's (variable.sector.fuel, sector = column C, fuel = column B); "" cells are NaN.

Vehicle classes: pas new passenger vehicles (cars and light vehicles), pau used passenger vehicles, fre freight,
cyc 2-3 wheelers (Excel-AI also calls them motor), bus buses (fuel use only).
"""
import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.core.rows import Rows
from cpat_model.mitigation import road_data
from cpat_model.mitigation.gdp import year_rows

PAS_FUELS = ['gso', 'die', 'lpg', 'nga']                 # ICE passenger fuels (and phv, plug-in hybrids)
FRE_FUELS = ['die', 'lpg', 'nga']


def prepare(state, db, inputs, settings, baseline):
    """EQ-A3.5: the data rows of section 5b by year and the parameters of the road model."""
    from cpat_model.mitigation.fuel_use import _road_biofuel
    countries, years = list(settings.countries), settings.years
    R = Rows(state, countries, years)
    par = road_data.params(db)
    biofuel = {name: _road_biofuel(state, db, settings, name) for name in ('bgs', 'bdi', 'obf')}
    rows, cps, ras = {}, [], []
    paths = road_data.path_rows(db, years)
    for i, iso in enumerate(countries):
        r = road_data.country_rows(db, iso, years)
        r.update(road_data.vehicle_prices(db, iso, years))
        rows[iso] = r
        cps.append(road_data.country_params(db, iso, settings, state, par, r,
                                            {n: biofuel[n][i] for n in biofuel}))
        ras.append(road_data.range_anxiety(db, iso, par))
    for key in rows[countries[0]]:
        R.put(key[0], np.array([rows[iso][key] for iso in countries]), key[1], key[2])
    for (var, s, f), values in paths.items():
        R.put(var, values, s, f)
    R.finish()
    state['_road'] = {'par': par, 'tryr': road_data.data_years(db),
                      'p': {key: np.array([cp[key] for cp in cps]) for key in cps[0]},
                      'ra': {c: np.array([ra[c] for ra in ras]) for c in ('pas', 'fre', 'cyc')}}


class _Year:
    """The rows of year index k by Excel-AI name 'variable.sector.fuel': x(name), x.prev(name), x.put(name, values)."""

    def __init__(self, R, k):
        self.R, self.k = R, k

    def __call__(self, name, kk=None):
        var, s, f = name.rsplit('.', 2)
        return self.R.at(var, self.k if kk is None else kk, s, f)

    def prev(self, name, first=np.nan):
        """The value of the year before; in the base year Excel-AI reads the code column (text: N() gives 0)."""
        return np.full(len(self.R.countries), first) if self.k == 0 else self(name, self.k - 1)

    def last(self, name, n):
        """The values of the last n years up to this one, (country, n)."""
        var, s, f = name.rsplit('.', 2)
        return self.R.of(var, s, f)[:, self.k - n + 1:self.k + 1]

    def put(self, name, values):
        var, s, f = name.rsplit('.', 2)
        return self.R.set(var, self.k, values, s, f)


def N(a):
    """Excel's N(): "" (NaN) -> 0."""
    return np.where(np.isnan(a), 0.0, a)


def isnum(a):
    """Excel's ISNUMBER: not "" (NaN)."""
    return ~np.isnan(a)


def pv(rate, nper, pmt):
    """-PV(rate, nper, pmt): present value of nper payments pmt at the end of each year (Excel's PV formula)."""
    return pmt * ((1 + rate) ** nper - 1) / rate / (1 + rate) ** nper


def annuity(value, rate, n):
    """Excel-AI's annuity of a value over n years: value / n / rate x (1 - 1 / (1 + rate)^n)."""
    return value / n / rate * (1 - 1 / (1 + rate) ** n)


def step(state, db, inputs, settings, baseline, t):
    """EQ-A3.6, EQ-A3.7, EQ-A3.8: the road engineer model in year t, before power (power demand reads trkte where
    TrModel = Engineer). It reads last year's electricity price, except in the base year, which runs after power
    (step_after_power)."""
    if t > settings.base_year:
        _run(state, inputs, settings, t)


def rerun(state, settings, t):
    """The years the road model reads this year's electricity price: the base year (rp, rppre) and the transport data
    years (rppre.ind.ecy of the freight and 2-3 wheeler BEV usage)."""
    return t == settings.base_year or t in state['_road']['tryr']


def step_after_power(state, db, inputs, settings, baseline, t):
    """The road engineer model again after power where it reads this year's electricity price (rerun). In Excel-AI
    that price does not depend on this year's power demand, so there is no circular reference: with TrModel = Engineer
    road electricity (trkte) of a data year after the base year then changes, and power runs once more
    (power.step_after_road)."""
    if rerun(state, settings, t):
        _run(state, inputs, settings, t)


def results(state, db, inputs, settings, baseline, t):
    """EQ-A3.9: the rows of section 5b that read this year's fuel use (after fuel_use.step)."""
    R = year_rows(state, settings)
    k = settings.years.index(t)
    with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
        _results(_Year(R, k), *state['_road']['results'])


def _run(state, inputs, settings, t):
    R = year_rows(state, settings)
    k = settings.years.index(t)
    x = _Year(R, k)
    with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
        _year(x, state, inputs, settings, k, t)


def _year(x, state, inputs, settings, k, y):
    road = state['_road']
    par, p, ra = road['par'], road['p'], road['ra']
    c = xt.constant
    put, prev, nan = x.put, x.prev, np.nan
    g = lambda name: x(f'{name}.all.all')                      # an input row of the scenario
    life_own, life_pas, life_fre, life_cyc = (par['own_years|pass'], par['life|pass'], par['life|fre'],
                                              par['life|cyc'])                          # trp.life D-G
    life_used = life_pas - life_own
    yes_price = 0.0 if str(par['vkt_new_price']).lower() == 'no' else 1.0              # trp.vkt G

    # switches (rows 3539-3542)
    put('tr.sw.all.all', 1.0 if str(inputs['TrModel'])[:8].lower() == 'engineer' else 0.0)
    dk = put('tr.dk.all.all', 1.0 if y in road['tryr'] else 0.0) == 1                # a year with transport data
    col = put('tr.col.all.all', y - settings.base_year + 1)[0]
    pol = put('tr.pol.all.all', 1.0 if inputs.number > 1 else 0.0)

    # prices and macro (rows 3820-3836)
    prl = {f: put(f'trprl.rod.{f}', x(f'atp.rod.{f}') * p[f'gj|{f}']) for f in ('gso', 'die', 'lpg')}   # $/liter
    prl['nga'] = put('trprg.rod.nga', x('atp.rod.nga') / par['gas_l_per_gj'])
    countries = list(settings.countries)
    blank = np.full(len(countries), nan)                      # Excel-AI's ""
    dom = state['_prices']['domestic']
    vat = lambda pc: np.array([dom[iso][pc]['vr'] for iso in countries])               # VAT of a price code
    vat_rod = lambda f: np.array([state['_fuel'][iso][(f, 'rod')]['vat'] for iso in countries])
    floor = settings.global_settings.get('PriceFloor', inputs['PriceFloor'])
    pri = put('trpri.ind.nga', np.maximum(x('pbc.ind.nga') + (x('nce.rod.nga') + x('xcpd.rod.nga'))
                                          * (1 + vat('nga.ind')), floor))             # industry gas price $/GJ
    prn = {f: put(f'trprn.rod.{f}', prl[f] / (1 + vat_rod(f))) for f in ('die', 'lpg')}   # net of VAT
    prn['nga'] = put('trprm.fre.nga', pri / ((1 + vat('nga.ind')) * par['gas_l_per_gj']))
    pop = put('trpop.all.all', x('pop.all.all') / c('Thousand'))
    gpc = put('trgpc.all.all', x('gdp.pos.usd.all.all') * c('Million') / x('pop.all.all'))
    if k == 0:
        gdl = put('trgdl.all.all', state['macro.gdp_growth'].sel(country=countries, year=y - 1).values)   # WEO
    else:
        gdl = put('trgdl.all.all', x.R.at('gdp.pos.pct', k - 1))
    dmax, dmin, dlo, dhi = par['disc_max'], par['disc_min'], par['disc_inc_low'], par['disc_inc_high']
    disc = put('trdisc.all.all', np.minimum(dmax, np.maximum(dmin, dmax - (gpc - dlo) / (dhi - dlo) * (dmax - dmin))))

    # base-year data of the vehicle classes, from the transport data while there is data (rows 3839-3923)
    D = lambda v: np.where(dk, v, nan)
    own = {cl: x(f'trown.{cl}.all') for cl in ('pas', 'lgt', 'fre', 'cyc')}
    sps = put('trsps.pas.all', D(own['pas'] / (own['pas'] + own['lgt'])))
    fe = lambda name: x(f'trfe.{name}')
    mix = lambda a, b: a * sps + b * (1 - sps)                 # passenger cars and light vehicles
    fem = {f: put(f'trfem.pas.{f}', D(mix(fe(f'pas.{f}'), fe('lgt.ice')))) for f in ('gso', 'die')}
    for f in ('lpg', 'nga'):
        fem[f] = put(f'trfem2.pas.{f}', D(mix(fe(f'pas.{f}'), fe('lgt.ice') * fe(f'pas.{f}') / fe('pas.gso'))))
    phs = put('trphs.pas.phv', D(fe('pas.gso') / fe('pas.phv')))
    febm = put('trfebm.pas.bev', D(mix(fe('pas.bev'), x('trfeb.lgt.bev'))))
    pbc = lambda f: x(f'pbc.all.{f}')
    pkg = put('trpkg.pas.gso', D(pbc('gso') * p['gj|gso'] / fem['gso']))
    rp_res0 = np.array([state['_power'][iso]['users']['res']['rp2021'] for iso in countries])   # Inputs J221
    pke = put('trpke.pas.bev', D((rp_res0 if k == 0 else x('rppre.res.ecy', k - 1)) / febm))
    bvu = lambda pk_ev, pk_ice, cap, ela: D(np.where(pk_ev == 0, 1.0, np.minimum(cap, (pk_ev / pk_ice) ** ela)))
    bvup = put('trbvu.pas.bev', bvu(pke, pkg, par['bev_vkt_cap|pass'], p['ela_usage|gso']))
    vkm = put('trvkm.pas.all', D(mix(x('trvkd.pas.all'), x('trvkd.lgt.all'))))
    vkb = put('trvkb.pas.bev', D(vkm * bvup))
    evo = lambda name: x(f'trevo.{name}')
    evp = lambda name: x(f'trevp.{name}')
    evom = put('trevom.pas.ev', D(mix(evo('pas.ev'), evo('lgt.bev'))))
    phv = put('trphv.pas.phv', D((evo('pas.ev') - evo('pas.bev')) * phs * sps))
    bshl = lambda cl, f: p[f'bshl|{cl}|{f}']
    put('trvkg.pas.gso', D(fem['gso'] * (bshl('pas', 'gso') + bshl('lgt', 'gso')) * (1 - phv)))
    for f in ('die', 'lpg', 'nga'):
        put(f'trvkf.pas.{f}', D(fem[f] * (bshl('pas', f) + bshl('lgt', f))))
    put('trvkp.pas.phv', D(fe('pas.phv') * (bshl('pas', 'gso') + bshl('lgt', 'gso')) * phv))
    for f in PAS_FUELS:
        first = x('trvkg.pas.gso') if f == 'gso' else x(f'trvkf.pas.{f}')
        put(f'trvk0.pas.{f}', first if k == 0 else prev(f'trvk0.pas.{f}'))
    vk0 = sum(x(f'trvk0.pas.{f}') for f in PAS_FUELS)
    vsh = {f: put(f'trvsh.pas.{f}', D(x(f'trvk0.pas.{f}') / vk0 * (1 - evom))) for f in PAS_FUELS}
    evbm = mix(evo('pas.bev'), evo('lgt.bev'))
    phvs = put('trphvs.pas.phv', D(evom - evbm))
    evbm = put('trevbm.pas.bev', D(evbm))
    ownb = put('trownb.pas.ice', D((own['pas'] + own['lgt']) * (1 - evbm)))
    owne = put('trowne.pas.bev', D(own['pas'] + own['lgt'] - ownb))
    evpm = put('trevpm.pas.bev', D(mix(evp('pas.bev'), evp('lgt.bev'))))
    # freight
    for f in FRE_FUELS:
        put(f'trvkfr.fre.{f}', D(fe(f'fre.{f}') * bshl('fre', f)))
        put(f'trvkr0.fre.{f}', x(f'trvkfr.fre.{f}') if k == 0 else prev(f'trvkr0.fre.{f}'))
    r0 = sum(x(f'trvkr0.fre.{f}') for f in FRE_FUELS)
    vsf = {'die': put('trvsf1.fre.die', D(np.where(r0 == 0, 1.0, x('trvkr0.fre.die') / r0 * (1 - evo('fre.bev')))))}
    for f in ('lpg', 'nga'):
        vsf[f] = put(f'trvsf.fre.{f}', D(np.where(r0 == 0, 0.0, x(f'trvkr0.fre.{f}') / r0 * (1 - evo('fre.bev')))))
    ownf = put('trownf.fre.ice', D(own['fre'] * (1 - evo('fre.bev'))))
    ownfe = put('trownfe.fre.bev', D(own['fre'] - ownf))
    pkd = put('trpkd.fre.die', D(pbc('die') * p['gj|die'] / (1 + vat('die.all')) / fe('fre.die')))
    pkef = put('trpkef.fre.bev', D(x('rppre.ind.ecy') / x('trfeb.fre.bev')))
    bvuf = put('trbvu.fre.bev', bvu(pkef, pkd, par['bev_vkt_cap|fre'], p['ela_usage|die']))
    put('trvkbf.fre.bev', D(bvuf * x('trvkd.fre.all')))
    if k == 0:
        vkfd = put('trvkfd.fre.all', np.where(vsf['die'] == 0, x('trvkd.fre.all'),
                                              x('trvkfr.fre.die') / (vsf['die'] * own['fre'] * pop) * c('Million')))
        put('trvkfb.fre.bev', bvuf * vkfd)
    else:
        put('trvkfd.fre.all', D(prev('trvkfd.fre.all') * vkm / prev('trvkm.pas.all')))
        put('trvkfb.fre.bev', D(prev('trvkfb.fre.bev') * vkb / prev('trvkb.pas.bev')))
    # 2-3 wheelers
    ownc = put('trownc.cyc.ice', D(own['cyc'] * (1 - evo('cyc.bev'))))
    ownce = put('trownce.cyc.bev', D(own['cyc'] - ownc))
    pkc = put('trpkc.cyc.gso', D(pbc('gso') * p['gj|gso'] / fe('cyc.gso')))
    pkec = put('trpkec.cyc.bev', D(x('rppre.ind.ecy') / x('trfeb.cyc.bev')))
    bvuc = put('trbvu.cyc.bev', bvu(pkec, pkc, par['bev_vkt_cap|cyc'], p['ela_usage|gso']))
    put('trvkbc.cyc.bev', D(x('trvkd.cyc.all') * bvuc))
    # freight share of ownership and the 2-3 wheeler hump with income (beyond the data years)
    fre_ratio = own['fre'] / (own['pas'] + own['lgt'])
    nc0 = prev('trnc.fre.all')
    put('trnc.fre.all', np.where(dk, fre_ratio, nc0))
    inc_t, sh_t, peak, scale = par['fre_inc_target'], par['fre_share_target'], par['cyc_peak_inc'], par['cyc_scale']
    fsh = put('trfsh.fre.all', np.where(dk, fre_ratio,
                                        np.minimum(nc0, np.maximum(sh_t, nc0 - (nc0 - sh_t) * gpc / inc_t))))
    jc0 = prev('trjc.cyc.all')
    put('trjc.cyc.all', np.where(dk, (1 + (1 - gpc / peak) * scale) * own['cyc'], jc0))
    cyh = put('trcyh.cyc.all', np.where(dk, own['cyc'], (jc0 + jc0) / (gpc / peak + peak / gpc)))
    ush = put('trush.pas.all', np.where(dk, x('trusd.pas.all'), prev('trush.pas.all')))
    owny = put('trowny.pas.all', ush * life_pas + (1 - ush) * life_own)
    std = {'pas.ice': put('trstd.pas.ice', D(ownb)), 'pas.bev': put('trstd.pas.bev', D(owne)),
           'fre.ice': put('trstdf.fre.ice', D(ownf)), 'fre.bev': put('trstdf.fre.bev', D(ownfe)),
           'cyc.ice': put('trstdc.cyc.ice', D(ownc)), 'cyc.bev': put('trstdc.cyc.bev', D(ownce))}

    # the stock at the start of the year, retirements and vehicles kept (rows 3924-3955, 3980-3989)
    # (vehicles per thousand people; the stock is the data while there is data, else last year's closing stock)
    # class: opening stock row, data stock, its share in the class, closing row, life, average, retired, kept rows
    classes = {
        'pas.ice': ('tropn', 'pas.ice', 1 - ush, 'trclon', life_own, 'travn', 'trretn', 'traftn'),
        'pas.bev': ('tropn', 'pas.bev', 1 - ush, 'trclon', life_own, 'travn', 'trretn', 'traftn'),
        'pau.ice': ('tropu', 'pas.ice', ush, 'trclou', life_used, 'travu', 'trretu', 'traftu'),
        'pau.bev': ('tropu', 'pas.bev', ush, 'trclou', life_used, 'travu', 'trretu', 'traftu'),
        'fre.ice': ('tropf', 'fre.ice', 1.0, 'trclof', life_fre, 'travf', 'trretf', 'traftf'),
        'fre.bev': ('tropf', 'fre.bev', 1.0, 'trclof', life_fre, 'travf', 'trretf', 'traftf'),
        'cyc.ice': ('tropc', 'cyc.ice', 1.0, 'trcloc', life_cyc, 'travc', 'trretc', 'traftc'),
        'cyc.bev': ('tropc', 'cyc.bev', 1.0, 'trcloc', life_cyc, 'travc', 'trretc', 'traftc')}
    op, aft = {}, {}
    for key, (vop, sd, share, vclo, life, vav, vret, vaft) in classes.items():
        s0 = N(std[sd])
        op[key] = put(f'{vop}.{key}', np.where(s0 > 0, s0 * share, N(prev(f'{vclo}.{key}'))))
    for key, (vop, sd, share, vclo, life, vav, vret, vaft) in classes.items():
        av = put(f'{vav}.{key}', x.last(f'{vop}.{key}', int(min(life, col))).mean(axis=1))
        ret = put(f'{vret}.{key}', np.minimum(av / life, op[key]))
        aft[key] = put(f'{vaft}.{key}', op[key] - ret)
    stt = put('trstt.pas.all', op['pas.ice'] + op['pas.bev'] + op['pau.ice'] + op['pau.bev'])
    evst = put('trevst.pas.ev', np.where(stt == 0, 0.0, (op['pas.bev'] + op['pau.bev']) / stt))
    for cl, var in (('fre', 'trevsf'), ('cyc', 'trevsc')):
        tot = op[f'{cl}.bev'] + op[f'{cl}.ice']
        put(f'{var}.{cl}.bev', np.where(tot == 0, 0.0, op[f'{cl}.bev'] / tot))
    afts = put('trafts.pas.all', aft['pas.ice'] + aft['pas.bev'] + aft['pau.ice'] + aft['pau.bev'])
    aftsf = put('traftsf.fre.all', aft['fre.ice'] + aft['fre.bev'])
    aftsc = put('traftsc.cyc.all', aft['cyc.ice'] + aft['cyc.bev'])
    bevm = put('trbevm.all.bev', (op['pas.bev'] + op['pau.bev'] + op['fre.bev'] + op['cyc.bev']) * pop / c('Thousand'))

    # charging stations, charging mark-up, range anxiety (rows 3990-4000)
    css = np.where(y < g('TrCsStartYear'), 0.0, g('TrCsStartLevel') + (g('TrCsTargetLevel') - g('TrCsStartLevel'))
                   * np.minimum(1, (y - g('TrCsStartYear')) / np.maximum(1, g('TrCsTargetYear') - g('TrCsStartYear'))))
    css = put('trcss.all.all', css * pol)
    csc = put('trcsc.all.all', x('trcpp.all.all') * (1 - css))
    sta = put('trsta.all.all', np.where(dk, x('trchs.all.all'), prev('trsta.all.all') * (bevm / prev('trbevm.all.bev'))
                                        ** par['ch_el_stock'] * (csc / prev('trcsc.all.all')) ** par['ch_el_cost']))
    sat = par['ch_sat']
    mku = put('trmku.all.all', np.maximum(par['ch_cost_min'], par['ch_cost_max'] * (sat - evst) / (1 - sat))
              * par['ch_public'])
    rp = lambda u: x(f'rp.{u}.ecy') if k == 0 else x(f'rp.{u}.ecy', k - 1)          # last year's electricity price
    pev = {'res': put('trpev.res.ecy', rp('res') + mku), 'ind': put('trpev.ind.ecy', rp('ind') + mku)}
    for cl, decline in (('pas', 'pass'), ('fre', 'fre'), ('cyc', 'cyc')):
        ra0 = prev(f'trra.{cl}.bev')
        later = np.where(ra0 < 0, ra0, np.maximum(ra0 * (1 - par[f'ra_decline|{decline}'])
                                                  * (sta / prev('trsta.all.all')) ** par['ra_el_stations'], 0))
        put(f'trra.{cl}.bev', ra[cl] if col <= c('TrRALag') else later)

    # fuel economy of new vehicles and the feebate (rows 4003-4078)
    few = {f: put(f'trfew.pas.{f}', np.where(dk, vsh[f], prev(f'tricw.pas.{f}'))) for f in PAS_FUELS}
    few['phv'] = put('trfew.pas.phv', np.where(dk, phvs, prev('tricw.pas.phv')))
    phg = put('trphg.pas.phv', np.where(dk, phs, prev('trphg.pas.phv')))
    prl['phv'] = put('trpphv.pas.phv', phg * prl['gso'] + (1 - phg) * (pev['res'] * par['phev_l_per_kwh']))
    wavg = lambda vals, w: sum(vals[f] * w[f] for f in w) / sum(w.values())        # SUMPRODUCT / SUM
    pav = put('trpav.pas.all', wavg(prl, few))
    fb_year = lambda cl: g(f'TrFbYear{cl}')
    fbt = {cl: put(f'trfbt{cl[0].lower()}.{v}.all', (np.where(y >= fb_year(cl), g(f'TrFbRate{cl}'), 0.0)
                                                    + x('reg.rod.all') * 1) * pol)
           for cl, v in (('Pas', 'pas'), ('Fre', 'fre'), ('Cyc', 'cyc'))}
    ef = {f: p[f'ef|{f}'] for f in PAS_FUELS}
    ef['phv'] = ef['gso']
    efb = {'gso': ef['gso'] * p['efa|gso'], 'die': ef['die'] * p['efa|die'], 'lpg': ef['lpg'], 'nga': ef['nga'],
           'phv': ef['gso'] * p['efa|gso']}                         # fossil CO2 per liter (biofuel blend out)
    fbl = {f: put(f'trfbl.pas.{f}', fbt['Pas'] * efb[f]) for f in efb}
    gap, mod = par['fe_gap|pass'], p['aeei']

    def ratio(now, name):                                     # year-on-year ratio of a row ("" in the base year)
        return blank if k == 0 else now / x(name, k - 1)

    for f in PAS_FUELS:                                       # change of the fuel price with the feebate
        price_row = 'trprg.rod.nga' if f == 'nga' else f'trprl.rod.{f}'
        put(f'trfbr.pas.{f}', blank if k == 0 else (prl[f] + fbl[f]) / (prev(price_row) + prev(f'trfbl.pas.{f}')))
    put('trfbr5.pas.phv', blank if k == 0 else (pav + fbl['phv']) / (prev('trpav.pas.all') + prev('trfbl.pas.phv')))
    fn = {}
    for f in PAS_FUELS:
        fn[f] = put(f'trfn.pas.{f}', np.where(dk, fem[f] * (1 + gap), prev(f'trfn.pas.{f}') * x(f'trfbr.pas.{f}')
                                              ** abs(p['ela_eff|gso']) * (1 + mod)))
    fn['phv'] = put('trfnp.pas.phv', np.where(dk, fe('pas.phv') * (1 + gap), prev('trfnp.pas.phv')
                                              * x('trfbr5.pas.phv') ** abs(p['ela_eff|gso']) * (1 + mod)))
    fna = put('trfna.pas.all', wavg(fn, few))
    intn = {f: put(f'trint.pas.{f}', ef[f] * c('Million') / fn[f]) for f in fn}
    inta = put('trinta.pas.all', wavg(ef, few) / fna * c('Million'))
    n_own = int(min(col, life_own))
    feu = put('trfeu.pau.all', x.last('trfna.pas.all', n_own).mean(axis=1))
    intu = put('trintu.pau.all', x('trinta.pas.all', k - n_own + 1))
    feub = put('trfeub.pau.bev', x('trfen.pas.bev', k - n_own + 1))
    icl = put('tricl.pas.ice', 1 - evpm if k == 0 else prev('trshn.pas.ice'))
    if k:
        put('triclu.pau.ice', prev('trshu.pau.ice'))
        ints = put('trints.pas.all', ush * (prev('trintu.pau.all') * x('triclu.pau.ice'))
                   + (1 - ush) * (prev('trinta.pas.all') * icl))
    else:
        ints = put('trints.pas.all', blank)
    # freight
    fewf = {f: put(f'trfewf.fre.{f}', np.where(dk, vsf[f], prev(f'tricwf.fre.{f}'))) for f in FRE_FUELS}
    pavf = put('trpavf.fre.all', wavg(prn, fewf))
    fblf = {f: put(f'trfblf.fre.{f}', fbt['Fre'] * efb[f]) for f in FRE_FUELS}
    prn_name = {'die': 'trprn.rod.die', 'lpg': 'trprn.rod.lpg', 'nga': 'trprm.fre.nga'}
    fnf = {}
    for f in FRE_FUELS:
        put(f'trfbrf.fre.{f}', blank if k == 0
            else (prn[f] + fblf[f]) / (prev(prn_name[f]) + prev(f'trfblf.fre.{f}')))
        fnf[f] = put(f'trfnf.fre.{f}', np.where(dk, fe(f'fre.{f}') * (1 + par['fe_gap|fre']), prev(f'trfnf.fre.{f}')
                                                * x(f'trfbrf.fre.{f}') ** abs(p['ela_eff|die']) * (1 + mod)))
    fnaf = put('trfnaf.fre.all', wavg(fnf, fewf))
    intf = {f: put(f'trintf.fre.{f}', ef[f] * c('Million') / fnf[f]) for f in FRE_FUELS}
    intaf = put('trintaf.fre.all', wavg({f: ef[f] for f in FRE_FUELS}, fewf) / fnaf * c('Million'))
    iclf = put('triclf.fre.ice', 1 - N(evp('fre.bev')) if k == 0 else prev('trshfi.fre.ice'))
    intsf = put('trintsf.fre.all', blank if k == 0 else iclf * prev('trintaf.fre.all'))
    # 2-3 wheelers
    fblc = put('trfblc.cyc.gso', fbt['Cyc'] * efb['gso'])
    put('trfbrc.cyc.gso', blank if k == 0
        else (prl['gso'] + fblc) / (prev('trprl.rod.gso') + prev('trfblc.cyc.gso')))
    fnc = put('trfnc.cyc.gso', np.where(dk, fe('cyc.gso') * (1 + par['fe_gap|cyc']), prev('trfnc.cyc.gso')
                                        * x('trfbrc.cyc.gso') ** abs(p['ela_eff|gso']) * (1 + mod)))
    intc = put('trintc.cyc.gso', ef['gso'] * c('Million') / fnc)
    iclc = put('triclc.cyc.ice', 1 - N(evp('cyc.bev')) if k == 0 else prev('trshc.cyc.ice'))
    intsc = put('trintsc.cyc.gso', blank if k == 0 else iclc * prev('trintc.cyc.gso'))

    # distance tax, cost per km and distance driven (rows 4081-4123)
    dtx = {}
    for cl, v in (('Pas', 'trdtxp.pas.all'), ('Fre', 'trdtxf.fre.all'), ('Cyc', 'trdtxc.cyc.all')):
        y0, y1, x0, x1 = (g(f'TrDtYear{cl}'), g(f'TrDtTargetYear{cl}'), g(f'TrDtStart{cl}'), g(f'TrDtTarget{cl}'))
        dtx[cl] = put(v, np.where(y == y0, x0, np.minimum(x1, N(prev(v)) + (x1 - x0) / (y1 - y0))) * (y >= y0) * pol)
    for f in PAS_FUELS + ['phv']:
        ckm = put(f'trckm.pas.{f}', prl[f] / fn[f] + dtx['Pas'])
        put(f'trckr.pas.{f}', ratio(ckm, f'trckm.pas.{f}'))
    inc = {'pas': par['inc_el_vkt|pass'], 'fre': par['inc_el_vkt|fre'], 'cyc': par['inc_el_vkt|cyc']}
    grow = lambda cl: (1 + gdl) ** inc[cl]

    def driven(name, data, cost_ratio, ela, cl, lo=None, hi=None):  # distance driven: data, else last year's x response
        later = prev(name) * np.where(yes_price, cost_ratio, 1.0) ** ela * grow(cl)
        if lo is not None:
            later = np.maximum(lo, np.minimum(hi, later))
        return put(name, np.where(dk, data, later))

    ela_g, ela_d = p['ela_usage|gso'], p['ela_usage|die']
    vkn = {f: driven(f'trvkn.pas.{f}', vkm, x(f'trckr.pas.{f}'), ela_g, 'pas') for f in PAS_FUELS + ['phv']}
    vkna = put('trvkna.pas.all', wavg(vkn, few))
    for cl, u, d in (('pas', 'res', 'Pas'), ('fre', 'ind', 'Fre'), ('cyc', 'res', 'Cyc')):
        name = {'pas': 'trckbp.pas.bev', 'fre': 'trckbf.fre.bev', 'cyc': 'trckbc.cyc.bev'}[cl]
        put(name, pev[u] / x(f'trfen.{cl}.bev') + dtx[d])
        put(f'trckbr.{cl}.bev', ratio(x(name), name))
    vknb = driven('trvknb.pas.bev', vkb, x('trckbr.pas.bev'), ela_g, 'pas')
    vku = put('trvku.pau.all', vkna * (fna / feu) ** ela_g)
    vkub = put('trvkub.pau.bev', vknb * (x('trfen.pas.bev') / feub) ** ela_g)
    lo, hi = par['fre_vkt_min'], par['fre_vkt_max']
    vknf = {}
    for f in FRE_FUELS:
        put(f'trckf.fre.{f}', prn[f] / fnf[f] + dtx['Fre'])
        put(f'trckfr.fre.{f}', ratio(x(f'trckf.fre.{f}'), f'trckf.fre.{f}'))
        vknf[f] = driven(f'trvknf.fre.{f}', x('trvkd.fre.all'), x(f'trckfr.fre.{f}'), ela_d, 'fre', lo, hi)
    vknaf = put('trvknaf.fre.all', wavg(vknf, fewf))
    vknbf = driven('trvknbf.fre.bev', x('trvkbf.fre.bev'), x('trckbr.fre.bev'), ela_d, 'fre', lo, hi)
    put('trckc.cyc.gso', prl['gso'] / fnc + dtx['Cyc'])
    put('trckcr.cyc.gso', ratio(x('trckc.cyc.gso'), 'trckc.cyc.gso'))
    vkncg = driven('trvkncg.cyc.gso', x('trvkd.cyc.all'), x('trckcr.cyc.gso'), ela_g, 'cyc')
    vkncb = driven('trvkncb.cyc.bev', x('trvkbc.cyc.bev'), x('trckbr.cyc.bev'), ela_g, 'cyc')

    # discounted lifetime distance (rows 4126-4133)
    dkm = {'pas.ice': put('trdkmpasi.pas.ice', pv(disc, life_own, vkna)),
           'pas.bev': put('trdkmpasb.pas.bev', pv(disc, life_own, vknb)),
           'pau.ice': put('trdkmpaui.pau.ice', pv(disc, life_used, vku)),
           'pau.bev': put('trdkmpaub.pau.bev', pv(disc, life_used, vkub)),
           'fre.ice': put('trdkmfrei.fre.ice', pv(disc, life_fre, vknaf)),
           'fre.bev': put('trdkmfreb.fre.bev', pv(disc, life_fre, vknbf)),
           'cyc.ice': put('trdkmcyci.cyc.ice', pv(disc, life_cyc, vkncg)),
           'cyc.bev': put('trdkmcycb.cyc.bev', pv(disc, life_cyc, vkncb))}

    # feebate pivot and the vehicle taxes and subsidies (rows 4134-4152)
    def pivot(cl, v, intensity):                              # pivot point of the feebate (gCO2/km)
        lag = col <= c('TrPivotLag')
        avg = put(f'trpva{v}', blank if lag
                  else N(intensity) * N(intensity) / N(prev(intensity_name[cl])))
        man0 = N(prev(f'trpvm{v}'))
        man = np.where(y == fb_year(cl), g(f'TrFbPivot{cl}'),
                       np.where(y > fb_year(cl), np.maximum(0, man0 - g(f'TrFbPivotChg{cl}')), 0.0))
        man = put(f'trpvm{v}', blank if lag else man)
        return put(f'trpv{v}', avg if str(inputs[f'TrFbPivotType{cl}'])[:3].lower() == 'ave' else man)

    intensity_name = {'Pas': 'trints.pas.all', 'Fre': 'trintsf.fre.all', 'Cyc': 'trintsc.cyc.gso'}

    def fbv(name, intens, pvt, rate, km):                     # feebate on a vehicle ($): (gCO2/km - pivot) x rate x km
        return put(name, blank if k == 0 else (intens - N(pvt)) * rate / c('Million') * km)

    pvp = pivot('Pas', 'p.pas.all', ints)
    fbvpi = fbv('trfbvpi.pas.ice', inta, pvp, fbt['Pas'], dkm['pas.ice'])
    fbvpb = fbv('trfbvpb.pas.bev', 0, pvp, fbt['Pas'], dkm['pas.bev'])
    adv, cue, vatb, sub = {}, {}, {}, {}
    for cl, v, sc in (('Pas', 'p', 'pas'), ('Fre', 'f', 'fre'), ('Cyc', 'c', 'cyc')):
        base = (pol == 0) | (y < g(f'TrAdvYear{cl}'))                 # ad-valorem taxes: baseline or policy
        adv[(cl, 'ice')] = put(f'tradv{v}i.{sc}.ice', np.where(base, g(f'TrAdvIceBase{cl}'), g(f'TrAdvIcePol{cl}')))
        adv[(cl, 'bev')] = put(f'tradv{v}b.{sc}.bev', np.where(base, g(f'TrAdvBevBase{cl}'), g(f'TrAdvBevPol{cl}')))
        duty = p[f'tax_bev|{sc}'] * p[f'tax_imp|{sc}']               # BEV import duty x import share
        cue[cl] = put(f'trcue{v}.{sc}.bev', np.where((pol == 0) | (y < g(f'TrCustYear{cl}')), duty,
                                                     p[f'tax_bev|{sc}'] * g('TrCustPolFactor') * p[f'tax_imp|{sc}']))
        if cl != 'Fre':
            vatb[cl] = put(f'trvatb{v}.{sc}.bev', np.where((pol == 0) | (y < g(f'TrVatYear{cl}')), p[f'tax_vat|{sc}'],
                                                           p[f'tax_vat|{sc}'] * g('TrVatPolFactor')))
        name = f'trsub{v}.{sc}.bev'
        sub[cl] = put(name, np.where(y == g(f'TrSubYear{cl}'), -g(f'TrSubAmount{cl}'),
                                     np.where(y > g(f'TrSubYear{cl}'), np.minimum(0, N(prev(name)) - g(f'TrSubChg{cl}')),
                                              0.0)) * pol)

    # TCO of a new passenger ICEV and BEV, of a used one (rows 4153-4192)
    dep, ins, ins_f = par['dep1|pass'], par['ins|pass'], par['ins_factor']
    icev_tax = lambda cl: (1 + p[f'tax_ice|{cl}'] * p[f'tax_imp|{cl}'])                 # import duty
    vp = lambda name: x(f'trvp.{name}')
    insure = lambda price, rate, life: price * rate / disc * (1 - 1 / (1 + disc) ** (life + 1)) * ins_f
    resale = lambda price: price * (1 - (dep + (life_own - 1) / (life_pas - 1) * (1 - dep)))

    ppip = put('trppip.pas.ice', vp('pas.ice') * icev_tax('pas') * (1 + adv[('Pas', 'ice')]) * (1 + p['tax_vat|pas'])
               + N(fbvpi))
    dppin = put('trdppin.pas.ice', ppip * dep)
    anpin = put('tranpin.pas.ice', annuity(ppip - dppin, disc, life_pas - 1))
    svpin = put('trsvpin.pas.ice', np.minimum(0, -ppip * ((life_pas - life_own) / life_pas * (1 - dep))
                                              / (1 + disc) ** life_own))
    impin = put('trimpin.pas.ice', insure(ppip, ins, life_own) + par['maint_ice|pass'] * dkm['pas.ice'])
    fupin = put('trfupin.pas.ice', (pav / fna + dtx['Pas']) * dkm['pas.ice'])
    topin = put('trtopin.pas.ice', dppin + anpin + svpin + impin + fupin)
    pkpin = put('trpkpin.pas.ice', topin / dkm['pas.ice'])
    resp = put('trresp.pas.ice', resale(vp('pas.ice')))
    resgp = put('trresgp.pas.ice', resp * icev_tax('pas') * (1 + adv[('Pas', 'ice')]) * (1 + p['tax_vat|pas']) + 0)
    for f in PAS_FUELS:
        put(f'trtcf.pas.{f}', dkm['pas.ice'] * x(f'trckm.pas.{f}') + ((dppin + anpin + svpin) + impin)
            + N(fbvpi) * (intn[f] / inta))
    ppbp = put('trppbp.pas.bev', vp('pas.bev') * (1 + cue['Pas']) * (1 + vatb['Pas']) * (1 + adv[('Pas', 'bev')])
               + (sub['Pas'] + N(fbvpb)))
    dppbn = put('trdppbn.pas.bev', ppbp * dep)
    anpbn = put('tranpbn.pas.bev', annuity(ppbp - dppbn, disc, life_pas - 1))
    svpbn = put('trsvpbn.pas.bev', np.minimum(0, -ppbp * ((life_pas - life_own) / life_pas * (1 - dep))
                                              / (1 + disc) ** life_own))
    impbn = put('trimpbn.pas.bev', insure(ppbp, ins, life_own) + par['maint_ev|pass'] * dkm['pas.bev'])
    fupbn = put('trfupbn.pas.bev', (pev['res'] / x('trfen.pas.bev') + dtx['Pas']) * dkm['pas.bev'])
    topbn = put('trtopbn.pas.bev', dppbn + anpbn + svpbn + impbn + fupbn + x('trra.pas.bev'))
    pkpbn = put('trpkpbn.pas.bev', topbn / dkm['pas.bev'])
    # plug-in hybrids: one price basis, the BEV's (no PHEV price in the data): insurance on the BEV price, ICEV
    # maintenance per km and distance (bug M17, fixed in Excel-AI 0.9.2)
    imphv = put('trimphv.pas.phv', insure(ppbp, ins, life_own) + par['maint_ice|pass'] * dkm['pas.ice'])
    put('trtcfp.pas.phv', dkm['pas.ice'] * x('trckm.pas.phv') + ((dppbn + anpbn + svpbn) + imphv)
        + N(fbvpi) * (intn['phv'] / inta))
    resb = put('trresb.pas.bev', resale(vp('pas.bev')))
    resgb = put('trresgb.pas.bev', resb * (1 + cue['Pas']) * (1 + adv[('Pas', 'bev')]) * (1 + vatb['Pas']) + 0)
    fbvui = fbv('trfbvui.pau.ice', intu, pvp, fbt['Pas'], dkm['pau.ice'])
    fbvub = fbv('trfbvub.pau.bev', 0, pvp, fbt['Pas'], dkm['pau.bev'])
    ppui = put('trppui.pau.ice', resgp + N(fbvui))
    anpiu = put('tranpiu.pau.ice', annuity(ppui, disc, life_used - 1))
    impiu = put('trimpiu.pau.ice', insure(ppui, ins, life_used) + par['maint_ice|pass'] * dkm['pau.ice'])
    fupiu = put('trfupiu.pau.ice', (pav / feu + dtx['Pas']) * dkm['pau.ice'])
    topiu = put('trtopiu.pau.ice', anpiu + impiu + fupiu)
    pkpiu = put('trpkpiu.pau.ice', topiu / dkm['pau.ice'])
    ppub = put('trppub.pau.bev', resgb + N(fbvub) + sub['Pas'])
    rau = put('trrau.pau.bev', (x('trra.pas.bev') * ppub) / ppbp)
    anpbu = put('tranpbu.pau.bev', annuity(ppub, disc, life_used - 1))
    impbu = put('trimpbu.pau.bev', insure(ppub, ins, life_used) + par['maint_ev|pass'] * dkm['pau.bev'])
    fupbu = put('trfupbu.pau.bev', (pev['res'] / feub + dtx['Pas']) * dkm['pau.bev'])
    topbu = put('trtopbu.pau.bev', anpbu + impbu + fupbu + rau)
    pkpbu = put('trpkpbu.pau.bev', topbu / dkm['pau.bev'])

    # TCO of freight vehicles (rows 4193-4214)
    pvf = pivot('Fre', 'f.fre.all', intsf)
    fbvfi = fbv('trfbvfi.fre.ice', intaf, pvf, fbt['Fre'], dkm['fre.ice'])
    fbvfb = fbv('trfbvfb.fre.bev', 0, pvf, fbt['Fre'], dkm['fre.bev'])   # its own distance (bug M16, fixed in 0.9.2)
    dep_f, ins_fr = par['dep1|fre'], par['ins|fre']
    ppfi = put('trppfi.fre.ice', vp('fre.ice') * icev_tax('fre') * (1 + adv[('Fre', 'ice')]) * (1 + 0) + N(fbvfi))
    dpfin = put('trdpfin.fre.ice', ppfi * dep_f)
    anfin = put('tranfin.fre.ice', annuity(ppfi - dpfin, disc, life_fre - 1))
    imfin = put('trimfin.fre.ice', insure(ppfi, ins_fr, life_fre) + par['maint_ice|fre'] * dkm['fre.ice'])
    fufin = put('trfufin.fre.ice', (pavf / fnaf + dtx['Fre']) * dkm['fre.ice'])
    tofin = put('trtofin.fre.ice', dpfin + anfin + imfin + fufin)
    pkfin = put('trpkfin.fre.ice', tofin / dkm['fre.ice'])
    for f in FRE_FUELS:
        put(f'trtcff.fre.{f}', dkm['fre.ice'] * x(f'trckf.fre.{f}') + (dpfin + anfin + imfin)
            + N(fbvfi) * (intf[f] / intaf))
    ppfb = put('trppfb.fre.bev', vp('fre.bev') * (1 + cue['Fre']) * (1 + adv[('Fre', 'bev')]) * (1 + 0)
               + (N(fbvfb) + sub['Fre']))
    dpfbn = put('trdpfbn.fre.bev', ppfb * dep_f)
    anfbn = put('tranfbn.fre.bev', annuity(ppfb - dpfbn, disc, life_fre - 1))
    imfbn = put('trimfbn.fre.bev', insure(ppfb, ins_fr, life_fre) + par['maint_ev|fre'] * dkm['fre.bev'])
    fufbn = put('trfufbn.fre.bev', (pev['ind'] / x('trfen.fre.bev') + dtx['Fre']) * dkm['fre.bev'])
    tofbn = put('trtofbn.fre.bev', dpfbn + anfbn + imfbn + fufbn + x('trra.fre.bev'))
    pkfbn = put('trpkfbn.fre.bev', tofbn / dkm['fre.bev'])

    # TCO of 2-3 wheelers (rows 4215-4233)
    pvc = pivot('Cyc', 'c.cyc.all', intsc)
    fbvci = fbv('trfbvci.cyc.ice', intc, pvc, fbt['Cyc'], dkm['cyc.ice'])
    fbvcb = fbv('trfbvcb.cyc.bev', 0, pvc, fbt['Cyc'], dkm['cyc.bev'])
    dep_c, ins_c = par['dep1|cyc'], par['ins|cyc']
    ppci = put('trppci.cyc.ice', vp('cyc.ice') * icev_tax('cyc') * (1 + p['tax_vat|cyc']) * (1 + adv[('Cyc', 'ice')])
               + N(fbvci))
    dpcin = put('trdpcin.cyc.ice', ppci * dep_c)
    ancin = put('trancin.cyc.ice', annuity(ppci - dpcin, disc, life_cyc - 1))
    imcin = put('trimcin.cyc.ice', insure(ppci, ins_c, life_cyc) + par['maint_ice|cyc'] * dkm['cyc.ice'])
    fucin = put('trfucin.cyc.ice', (prl['gso'] / fnc + dtx['Cyc']) * dkm['cyc.ice'])
    tocin = put('trtocin.cyc.ice', dpcin + ancin + imcin + fucin)
    pkcin = put('trpkcin.cyc.ice', tocin / dkm['cyc.ice'])
    ppcb = put('trppcb.cyc.bev', vp('cyc.bev') * (1 + cue['Cyc']) * (1 + vatb['Cyc']) * (1 + adv[('Cyc', 'bev')])
               + (N(fbvcb) + sub['Cyc']))
    dpcbn = put('trdpcbn.cyc.bev', ppcb * dep_c)
    ancbn = put('trancbn.cyc.bev', annuity(ppcb - dpcbn, disc, life_cyc - 1))
    imcbn = put('trimcbn.cyc.bev', insure(ppcb, ins_c, life_cyc) + par['maint_ev|cyc'] * dkm['cyc.bev'])
    fucbn = put('trfucbn.cyc.bev', (pev['res'] / x('trfen.cyc.bev') + dtx['Cyc']) * dkm['cyc.bev'])
    tocbn = put('trtocbn.cyc.bev', dpcbn + ancbn + imcbn + fucbn + x('trra.cyc.bev'))
    pkcbn = put('trpkcbn.cyc.bev', tocbn / dkm['cyc.bev'])

    # vehicle ownership: Gompertz demand, partial adjustment, purchases (EQ-M5.1; rows 4236-4249)
    gomp = lambda b: np.exp(par['gomp_a'] * np.exp(gpc * b / c('Thousand')))
    b_pas, b_fre = par['own_gomp_b|pass'], par['own_gomp_b|fre']
    put('trjhp.pas.all', np.where(dk, (x('trsat.all.all') * (1 - fsh)) * gomp(b_pas), prev('trjhp.pas.all')))
    put('trjip.pas.all', np.where(dk, owne + ownb, prev('trjip.pas.all')))
    put('trjjp.pas.all', np.where(dk, x('trjip.pas.all') / x('trjhp.pas.all'), prev('trjjp.pas.all')))
    put('trjhf.fre.all', np.where(dk, (x('trsat.all.all') * fsh) * gomp(b_fre), prev('trjhf.fre.all')))
    put('trjif.fre.all', np.where(dk, ownfe + ownf, prev('trjif.fre.all')))
    put('trjjf.fre.all', np.where(dk, x('trjif.fre.all') / x('trjhf.fre.all'), prev('trjjf.fre.all')))
    satp = put('trsatp.pas.all', np.where(dk, x('trsat.all.all'), prev('trsatp.pas.all')))
    satq = put('trsatq.pas.all', satp * (1 - fsh))
    gtp = put('trgtp.pas.all', satq * gomp(b_pas) * N(prev('trjjp.pas.all')))

    def demand(name_dem, name_dmc, s_ice, s_bev, target, adj, grow_max, decline):
        data = N(s_ice) > 0
        d0 = N(prev(name_dmc))
        dem = put(name_dem, np.where(data, N(s_ice) + N(s_bev), adj * target + (1 - adj) * d0)) if name_dem else target
        return put(name_dmc, np.where(data, N(s_ice) + N(s_bev),
                                      np.maximum(d0 * (1 - decline), np.minimum(d0 * (1 + grow_max), dem))))

    odc = (c('TrOwnDecline'), c('TrOwnDecline'), par['own_max_decline|cyc'])            # trp.odc D-F
    dmcp = demand('trdemp.pas.all', 'trdmcp.pas.all', std['pas.ice'], std['pas.bev'], gtp, par['own_adj|pass'],
                  par['own_max_growth|pass'], odc[0])
    byt = put('trbyt.pas.all', dmcp - afts)
    bytn = put('trbytn.pas.all', byt * (1 - ush))
    bytu = put('trbytu.pau.all', byt - bytn)

    # EV choice: logit of the TCO per km, or the data's purchase shares while there is data (EQ-M5.2; rows 4250-4263)
    logit = lambda kk, ev, ice, avg: 1 / (1 + np.exp(-kk * (ev - ice) / avg))
    tcav = put('trtcav.pas.all', icl * pkpin + (1 - icl) * pkpbn)
    lgn = put('trlgn.pas.ice', logit(par['k|pass'], pkpbn, pkpin, tcav))
    lgnb = put('trlgnb.pas.bev', 1 - lgn)
    evac = put('trevac.pas.bev', D(evpm))
    shn = put('trshn.pas.ice', np.where(isnum(evac), 1 - evac, lgn))
    shnb = put('trshnb.pas.bev', 1 - shn)
    iclu = icl if k == 0 else x('triclu.pau.ice')
    tcau = put('trtcau.pau.all', iclu * pkpiu + (1 - iclu) * pkpbu)
    lgu = put('trlgu.pau.ice', logit(par['k|pass'], pkpbu, pkpiu, tcau))
    lgub = put('trlgub.pau.bev', 1 - lgu)
    shu = put('trshu.pau.ice', np.where(isnum(evac), 1 - evac, lgu))
    shub = put('trshub.pau.bev', 1 - shu)
    if k == 0:
        put('triclu.pau.ice', shu)
    evcc = put('trevcc.pas.ev', ush * lgub + (1 - ush) * lgnb)
    evsh = put('trevsh.pas.ev', np.where(N(evac) > 0, evac, evcc))
    trn = put('trtrn.pas.all', 1 / (ush * life_own + life_pas * (1 - ush)))
    # freight
    put('trsatf.fre.all', np.where(dk, x('trsat.all.all'), prev('trsatf.fre.all')))
    satg = put('trsatg.fre.all', x('trsatf.fre.all') * fsh)
    gtf = put('trgtf.fre.all', satg * gomp(b_fre) * N(prev('trjjf.fre.all')))
    dmcf = demand('trdemf.fre.all', 'trdmcf.fre.all', std['fre.ice'], std['fre.bev'], gtf, par['own_adj|fre'],
                  par['own_max_growth|fre'], odc[1])
    bytf = put('trbytf.fre.all', dmcf - aftsf)
    tcaf = put('trtcaf.fre.all', iclf * pkfin + (1 - iclf) * pkfbn)
    lgf = put('trlgf.fre.ice', logit(par['k|fre'], pkfbn, pkfin, tcaf))
    lgfb = put('trlgfb.fre.bev', 1 - lgf)
    evaf = put('trevaf.fre.bev', D(evp('fre.bev')))
    shfi = put('trshfi.fre.ice', np.where(isnum(evaf), 1 - evaf, lgf))
    shfb = put('trshfb.fre.bev', 1 - shfi)
    # 2-3 wheelers (demand: the hump with income, no partial adjustment)
    dmcc = demand(None, 'trdmcc.cyc.all', std['cyc.ice'], std['cyc.bev'], cyh, 1.0, par['own_max_growth|cyc'], odc[2])
    bytc = put('trbytc.cyc.all', dmcc - aftsc)
    tcac = put('trtcac.cyc.all', iclc * pkcin + (1 - iclc) * pkcbn)
    lgc = put('trlgc.cyc.ice', logit(par['k|cyc'], pkcbn, pkcin, tcac))
    lgcb = put('trlgcb.cyc.bev', 1 - lgc)
    evacc = put('trevacc.cyc.bev', D(evp('cyc.bev')))
    shc = put('trshc.cyc.ice', np.where(isnum(evacc), 1 - evacc, lgc))
    shcb = put('trshcb.cyc.bev', 1 - shc)

    # purchases, the gap to the data stock, closing stock (rows 3956-3979)
    buy_share = {'pas.ice': (shn, bytn), 'pas.bev': (shnb, bytn), 'pau.ice': (shu, bytu), 'pau.bev': (shub, bytu),
                 'fre.ice': (shfi, bytf), 'fre.bev': (shfb, bytf), 'cyc.ice': (shc, bytc), 'cyc.bev': (shcb, bytc)}
    buy_var = {'tropn': 'trbuyn', 'tropu': 'trbuyu', 'tropf': 'trbuyf', 'tropc': 'trbuyc'}
    plg_var = {'tropn': 'trplgn', 'tropu': 'trplgu', 'tropf': 'trplgf', 'tropc': 'trplgc'}
    clo = {}
    for key, (vop, sd, share, vclo, life, vav, vret, vaft) in classes.items():
        sh, total = buy_share[key]
        buy = put(f'{buy_var[vop]}.{key}', sh * total)
        s0 = N(std[sd])
        plg = put(f'{plg_var[vop]}.{key}', np.where(s0 > 0, s0 * share - aft[key] - buy, 0.0))
        clo[key] = put(f'{vclo}.{key}', aft[key] + buy + plg)

    # ICE fuel shares of the passenger stock: data, else the response to the TCO per fuel (rows 4264-4311)
    new_bev = clo['pas.bev'] + clo['pau.bev']
    nwbn = put('trnwbn.pas.bev', np.where(new_bev == 0, 0.0, (clo['pas.bev'] - aft['pas.bev']) / new_bev))
    nwbu = put('trnwbu.pau.bev', np.where(new_bev == 0, 0.0, (clo['pau.bev'] - aft['pau.bev']) / new_bev))
    ics = {f: put(f'trics.pas.{f}', D(vsh[f])) for f in PAS_FUELS}
    ics['phv'] = put('trics.pas.phv', D(phvs))
    tcf_name = lambda f: 'trtcfp.pas.phv' if f == 'phv' else f'trtcf.pas.{f}'
    tcr = {f: put(f'trtcr.pas.{f}', ratio(x(tcf_name(f)), tcf_name(f))) for f in PAS_FUELS + ['phv']}
    icdp = put('tricdp.pas.phv', D(np.maximum(0, evp('pas.ev') - evp('pas.bev')) * sps))
    ics4 = sum(ics[f] for f in PAS_FUELS)
    icd = {f: put(f'tricd.pas.{f}', D(ics[f] / ics4 * (1 - evac - icdp))) for f in PAS_FUELS}
    icd['phv'] = icdp
    icp = _ice_shares(x, k, 'trcrs.pas', 'tricp.pas', icd, tcr, PAS_FUELS + ['phv'], par)
    icp_sum = sum(icp.values())
    icn = {f: put(f'tricn.pas.{f}', np.where(isnum(ics[f]), icp[f], icp[f] / icp_sum * (1 - evsh))) for f in icp}
    ico = {f: put(f'trico.pas.{f}', np.where(isnum(ics[f]), ics[f], N(prev(f'trico.pas.{f}')) * (owny - 1) / owny
                                             + icn[f] / owny)) for f in icp}
    ico_sum = sum(ico.values())
    icw = {f: put(f'tricw.pas.{f}', ico[f] / (ico_sum + evst)) for f in ico}
    veh = {f: put(f'trveh.pas.{f}', (stt * icw[f]) * pop / c('Thousand')) for f in icw}
    vehb = put('trvehb.pas.bev', new_bev * pop / c('Thousand'))
    # freight
    put('trnwf.fre.bev', np.where(clo['fre.bev'] == 0, 0.0, (clo['fre.bev'] - aft['fre.bev']) / clo['fre.bev']))
    icsf = {f: put(f'tricsf.fre.{f}', D(vsf[f])) for f in FRE_FUELS}
    tcrf = {f: put(f'trtcrf.fre.{f}', ratio(x(f'trtcff.fre.{f}'), f'trtcff.fre.{f}')) for f in FRE_FUELS}
    icpf = _ice_shares(x, k, 'trcrsf.fre', 'tricpf.fre', icsf, tcrf, FRE_FUELS, par)
    icpf_sum = sum(icpf.values())
    icnf = {f: put(f'tricnf.fre.{f}', np.where(isnum(icsf[f]), icpf[f], icpf[f] / icpf_sum * (1 - shfb)))
            for f in FRE_FUELS}
    icof = {f: put(f'tricof.fre.{f}', np.where(isnum(icsf[f]), icsf[f], N(prev(f'tricof.fre.{f}')) * (life_fre - 1)
                                               / life_fre + icnf[f] / life_fre)) for f in FRE_FUELS}
    icof_sum = sum(icof.values())
    icwf = {f: put(f'tricwf.fre.{f}', icof[f] / (icof_sum + x('trevsf.fre.bev'))) for f in FRE_FUELS}
    vehf = {f: put(f'trvehf.fre.{f}', ((clo['fre.ice'] + clo['fre.bev']) * icwf[f]) * pop / c('Thousand'))
            for f in FRE_FUELS}
    vehfb = put('trvehfb.fre.bev', clo['fre.bev'] * pop / c('Thousand'))
    # 2-3 wheelers
    put('trnwc.cyc.bev', np.where(clo['cyc.bev'] == 0, 0.0, (clo['cyc.bev'] - aft['cyc.bev']) / clo['cyc.bev']))
    vehc = put('trvehc.cyc.ice', clo['cyc.ice'] * pop / c('Thousand'))
    vehcb = put('trvehc.cyc.bev', clo['cyc.bev'] * pop / c('Thousand'))

    road_use = _fuel_use(x, k, par, p, prl, prn, pev, dtx, fn, fnf, fnc, trn, veh, vehb, vehf, vehfb, vehc, vehcb,
                         gpc, nwbn, nwbu, phg, life_fre, life_cyc, c)
    state['_road']['results'] = (dk, evac, evcc, lgfb, evaf, lgcb, evacc, road_use)   # for results(), after fuel use


def _ice_shares(x, k, crs_row, icp_row, data, tcr, fuels, par):
    """Fuel shares of new ICE vehicles: the data, else last year's shares x (own TCO ratio)^own elasticity x
    (TCO ratio of the other fuels, weighted by last year's shares)^cross elasticity."""
    put, prev = x.put, x.prev
    icp = {}
    for f in fuels:
        if k == 0:
            crs = put(f'{crs_row}.{f}', np.full(len(x.R.countries), np.nan))
        else:
            p0 = {g: prev(f'{icp_row}.{g}') for g in fuels}
            num = sum(p0[g] * N(tcr[g]) for g in fuels) - p0[f] * tcr[f]
            den = sum(p0.values()) - p0[f]
            crs = put(f'{crs_row}.{f}', np.where(den == 0, np.nan, num / den))     # IFERROR(..., "")
        p0f = N(prev(f'{icp_row}.{f}'))
        icp[f] = put(f'{icp_row}.{f}', np.where(isnum(data[f]), data[f], np.where(
            isnum(crs), p0f * tcr[f] ** par['own_price_el'] * crs ** par['cross_price_el'], p0f)))
    return icp


def _fuel_use(x, k, par, p, prl, prn, pev, dtx, fn, fnf, fnc, trn, veh, vehb, vehf, vehfb, vehc, vehcb,
              gpc, nwbn, nwbu, phg, life_fre, life_cyc, c):
    """EQ-A3.8: fuel economy of the stock, distance per vehicle, fuel use by vehicle class (billion liters), the
    calibration to the base-year energy balance, CO2, electricity (rows 4363-4522)."""
    put, prev = x.put, x.prev
    nan = np.full(len(x.R.countries), np.nan)
    ratio = lambda name: nan if k == 0 else x(name) / x(name, k - 1)
    ela_g, ela_d = p['ela_usage|gso'], p['ela_usage|die']
    inc_p, inc_f, inc_c = par['inc_el_vkt|pass'], par['inc_el_vkt|fre'], par['inc_el_vkt|cyc']
    gpcr = put('trgpcr.all.all', nan if k == 0 else gpc / x('trgpc.all.all', k - 1))
    vkm, vkfd, vkdc = x('trvkm.pas.all'), x('trvkfd.fre.all'), x('trvkd.cyc.all')

    def stock_fe(old, new, data, now_new, turnover):          # stock fuel economy: data, else turnover-weighted
        fso = put(old, np.where(isnum(data), data, N(prev(new))))
        fsc = put(new, np.where(isnum(data), data, now_new * turnover + fso * (1 - turnover)))
        return fso, fsc

    def per_vehicle(name, data, factor, cost_ratio, ela, inc):  # distance per vehicle: data x factor, else response
        return put(name, np.where(isnum(data), data * factor, N(prev(name)) * cost_ratio ** ela * gpcr ** inc))

    # passenger vehicles, before calibration
    fem = {'gso': x('trfem.pas.gso'), 'die': x('trfem.pas.die'), 'lpg': x('trfem2.pas.lpg'),
           'nga': x('trfem2.pas.nga'), 'phv': x('trfe.pas.phv')}
    fso, fsc = {}, {}
    for f in ('gso', 'die', 'lpg', 'nga', 'phv'):
        old, new = ('trfsop.pas.phv', 'trfscp.pas.phv') if f == 'phv' else (f'trfso.pas.{f}', f'trfsc.pas.{f}')
        fso[f], fsc[f] = stock_fe(old, new, fem[f], fn[f], trn)
    for f in fso:
        put(f'trcks.pas.{f}', prl[f] / fso[f] + dtx['Pas'])
        put(f'trcksr.pas.{f}', ratio(f'trcks.pas.{f}'))
    for f in fso:
        vku0 = per_vehicle(f'trvku0.pas.{f}', vkm, 1, x(f'trcksr.pas.{f}'), ela_g, inc_p)
        put(f'trbkm0.pas.{f}', veh[f] * vku0 / c('Thousand'))
    fu0 = {'gso': put('trfu0g.pas.gso', x('trbkm0.pas.gso') / fsc['gso'] + x('trbkm0.pas.phv') / fsc['phv'])}
    for f in ('die', 'lpg', 'nga'):
        fu0[f] = put(f'trfu0.pas.{f}', x(f'trbkm0.pas.{f}') / fsc[f])
    # freight
    fsof, fscf = {}, {}
    for f in FRE_FUELS:
        fsof[f], fscf[f] = stock_fe(f'trfsof.fre.{f}', f'trfscf.fre.{f}', x(f'trfe.fre.{f}'), fnf[f], 1 / life_fre)
    for f in FRE_FUELS:
        put(f'trcksf.fre.{f}', prn[f] / fsof[f] + dtx['Fre'])
        put(f'trcksfr.fre.{f}', ratio(f'trcksf.fre.{f}'))
    for f in FRE_FUELS:
        vku0 = per_vehicle(f'trvku0f.fre.{f}', vkfd, 1, x(f'trcksfr.fre.{f}'), ela_d, inc_f)
        put(f'trbkm0f.fre.{f}', vehf[f] * vku0 / c('Thousand'))
    # 2-3 wheelers
    fsoc, fscc = stock_fe('trfsoc.cyc.gso', 'trfscc.cyc.gso', x('trfe.cyc.gso'), fnc, 1 / life_cyc)
    put('trcksc.cyc.gso', prl['gso'] / fsoc + dtx['Cyc'])
    put('trckscr.cyc.gso', ratio('trcksc.cyc.gso'))
    vku0c = per_vehicle('trvku0c.cyc.gso', vkdc, 1, x('trckscr.cyc.gso'), ela_g, inc_c)
    put('trbkm0c.cyc.gso', vehc * vku0c / c('Thousand'))
    fu0c = put('trfu0c.cyc.gso', x('trbkm0c.cyc.gso') / fscc)
    fu0f = {f: put(f'trfu0f.fre.{f}', x(f'trbkm0f.fre.{f}') / fscf[f]) for f in FRE_FUELS}

    # calibration of distance to the base-year fuel use (held after the base year; rows 4429-4441)
    lpk = {f: p[f'lpk|{f}'] for f in ('gso', 'die', 'lpg', 'nga')}
    bus_share = {'gso': 0.0, 'die': p['bsh|bus|die'], 'lpg': p['bsh|bus|lpg'], 'nga': p['bsh|bus|nga']}
    for f in ('gso', 'die', 'lpg', 'nga'):
        if k == 0:
            liters = fu0['gso'] + fu0c if f == 'gso' else fu0[f] + fu0f[f]
            bu = put(f'trbu.rod.{f}', liters / lpk[f] * c('Billion') / (1 - bus_share[f]))
            put(f'trcq.rod.{f}', np.where((bu == 0) | (p[f'eb|{f}'] == 0), 1.0, p[f'eb|{f}'] / bu))
        else:
            put(f'trbu.rod.{f}', prev(f'trbu.rod.{f}'))
            put(f'trcq.rod.{f}', prev(f'trcq.rod.{f}'))
    cq = {f: x(f'trcq.rod.{f}') for f in ('gso', 'die', 'lpg', 'nga')}
    if k == 0:
        dfp = put('trdfp.pas.all', sum(fu0[f] * cq[f] for f in fu0) / sum(fu0.values()))
        dff = put('trdff.fre.all', sum(fu0f[f] * cq[f] for f in FRE_FUELS) / sum(fu0f.values()))
        dfc = put('trdfc.cyc.all', cq['gso'])
    else:
        dfp, dff, dfc = (put(n, prev(n)) for n in ('trdfp.pas.all', 'trdff.fre.all', 'trdfc.cyc.all'))

    # passenger vehicles, calibrated: distance, fuel use (EQ-M5.3), CO2, BEV electricity (rows 4444-4471)
    bkm = {}
    for f in fso:
        vkc = per_vehicle(f'trvkc.pas.{f}', vkm, dfp, x(f'trcksr.pas.{f}'), ela_g, inc_p)
        bkm[f] = put(f'trbkm.pas.{f}', veh[f] * vkc / c('Thousand'))
    fup = {'gso': put('trfup.pas.gso', bkm['gso'] / fsc['gso'] + bkm['phv'] / fsc['phv'])}
    for f in ('die', 'lpg', 'nga'):
        fup[f] = put(f'trfup.pas.{f}', bkm[f] / fsc[f])
    co2p = put('trco2p.pas.all', sum(fup[f] * p[f'ef|{f}'] for f in fup) * c('Thousand'))
    fen, feub = x('trfen.pas.bev'), x('trfeub.pau.bev')
    nw = nwbn + nwbu
    febn = put('trfebn.pas.bev', np.where(nw == 0, (fen + feub) / 2, (fen * nwbn + feub * nwbu) / nw))
    febs0 = N(prev('trfebs.pas.bev'))
    febo = put('trfebo.pas.bev', np.where(febs0 > 0, prev('trfebs.pas.bev'), febn))
    febs = put('trfebs.pas.bev', nw * febn + (1 - nw) * febo)
    put('trckb2.pas.bev', pev['res'] / febo + dtx['Pas'])
    put('trckb2r.pas.bev', ratio('trckb2.pas.bev'))
    vkcb = per_vehicle('trvkcb.pas.bev', x('trvkb.pas.bev'), dfp, x('trckb2r.pas.bev'), ela_g, inc_p)
    bkmb = put('trbkmb.pas.bev', vkcb * vehb / c('Thousand'))
    elph = put('trelph.pas.phv', bkm['phv'] / febs * (1 - phg))
    elp = put('trelp.pas.ecy', (bkmb / febs) + elph)
    bkmt = put('trbkmt.pas.all', sum(bkm.values()) + bkmb)
    put('trintp.pas.all', co2p / bkmt * c('Thousand'))
    # freight (rows 4472-4492)
    bkmf = {}
    for f in FRE_FUELS:
        vkcf = per_vehicle(f'trvkcf.fre.{f}', vkfd, dff, x(f'trcksfr.fre.{f}'), ela_d, inc_f)
        bkmf[f] = put(f'trbkmf.fre.{f}', vehf[f] * vkcf / c('Thousand'))
    fuf = {f: put(f'trfuf.fre.{f}', bkmf[f] / fscf[f]) for f in FRE_FUELS}
    co2f = put('trco2f.fre.all', sum(fuf[f] * p[f'ef|{f}'] for f in FRE_FUELS) * c('Thousand'))
    fenf = x('trfen.fre.bev')
    febsf0 = N(prev('trfebsf.fre.bev'))
    febof = put('trfebof.fre.bev', np.where(febsf0 > 0, prev('trfebsf.fre.bev'), fenf))
    nwf = x('trnwf.fre.bev')
    febsf = put('trfebsf.fre.bev', nwf * fenf + (1 - nwf) * febof)
    put('trckbf2.fre.bev', pev['ind'] / febof + dtx['Fre'])
    put('trckbf2r.fre.bev', ratio('trckbf2.fre.bev'))
    vkcbf = per_vehicle('trvkcbf.fre.bev', x('trvkfb.fre.bev'), dff, x('trckbf2r.fre.bev'), ela_d, inc_f)
    bkmbf = put('trbkmbf.fre.bev', vkcbf * vehfb / c('Thousand'))
    elf = put('trelf.fre.ecy', bkmbf / febsf)
    bkmtf = put('trbkmtf.fre.all', sum(bkmf.values()) + bkmbf)
    put('trintf2.fre.all', np.where(bkmtf == 0, p['ef|die'] / fsof['die'] * c('Million'), co2f / bkmtf * c('Thousand')))
    # 2-3 wheelers (rows 4493-4505)
    vkcc = per_vehicle('trvkcc.cyc.gso', vkdc, dfc, x('trckscr.cyc.gso'), ela_g, inc_c)
    bkmc = put('trbkmc.cyc.gso', vehc * vkcc / c('Thousand'))
    fuc = put('trfuc.cyc.gso', bkmc / fscc)
    co2c = put('trco2c.cyc.all', fuc * (p['ef|gso'] * c('Thousand')))
    fenc = x('trfen.cyc.bev')
    febsc0 = N(prev('trfebsc.cyc.bev'))
    feboc = put('trfeboc.cyc.bev', np.where(febsc0 > 0, prev('trfebsc.cyc.bev'), fenc))
    nwc = x('trnwc.cyc.bev')
    febsc = put('trfebsc.cyc.bev', nwc * fenc + (1 - nwc) * feboc)
    put('trckbc2.cyc.bev', pev['res'] / feboc + dtx['Cyc'])
    put('trckbc2r.cyc.bev', ratio('trckbc2.cyc.bev'))
    vkcbc = per_vehicle('trvkcbc.cyc.bev', x('trvkbc.cyc.bev'), dfc, x('trckbc2r.cyc.bev'), ela_g, inc_c)
    bkmbc = put('trbkmbc.cyc.bev', vkcbc * vehcb / c('Thousand'))
    elc = put('trelc.cyc.ecy', bkmbc / febsc)
    bkmtc = put('trbkmtc.cyc.all', bkmc + bkmbc)
    put('trintc2.cyc.all', co2c / bkmtc * c('Thousand'))

    # buses: base-year bus fuel use moved with passenger fuel use (rows 4509-4522)
    busp = {f: put(f'trbusp.pas.{f}', fup[f] / lpk[f] * c('Billion') * 1) for f in fup}
    buse = put('trbuse.pas.ecy', elp * c('Thousand') / p['ktoe_gwh'] * 1)
    bus0 = put('trbus0.pas.all', sum(busp.values()) + buse if k == 0 else prev('trbus0.pas.all'))
    busf = {f: put(f'trbusf.bus.{f}', p[f'bus|{f}'] * lpk[f] / c('Billion') * sum(busp.values()) / bus0)
            for f in FRE_FUELS}
    # all base-year bus energy electrifies with the passenger electricity share (as legacy)
    bus_all = p['bus|die'] + p['bus|lpg'] + p['bus|nga'] + p['bus|ecy']
    busel = put('trbusel.bus.ecy', bus_all * p['ktoe_gwh'] / c('Thousand') * buse / bus0)

    # totals, the calibration to the energy balance, results by vehicle class (rows 4525-4573)
    fua = put('trfua.all.gso', fup['gso'] + fuc)
    fub = {f: put(f'trfub.all.{f}', fup[f] + fuf[f] + busf[f]) for f in FRE_FUELS}
    fuel_all = {'gso': fua, **fub}
    elt = put('trelt.all.ecy', (busel + elc) + elf + elp)
    for f in ('gso', 'die', 'lpg', 'nga'):
        if k == 0:
            eb = p[f'eb|{f}']
            put(f'trcf2.all.{f}', np.where((fuel_all[f] == 0) | (eb == 0), 1.0,
                                           eb / (fuel_all[f] / lpk[f] * c('Billion'))))
        else:
            put(f'trcf2.all.{f}', prev(f'trcf2.all.{f}'))
    if k == 0:
        no = str(par['recon_ele'])[:2].lower() == 'no'
        put('trcf2e.all.ecy', np.where((elt == 0) | (p['eb2|ecy'] == 0) | no, 1.0,
                                       p['eb2|ecy'] / (elt / p['ktoe_gwh'] * c('Thousand'))))
    else:
        put('trcf2e.all.ecy', prev('trcf2e.all.ecy'))
    cf2 = {f: x(f'trcf2.all.{f}') for f in ('gso', 'die', 'lpg', 'nga')}
    cf2e = x('trcf2e.all.ecy')
    kt = {f: put(f'trkt.rod.{f}', fuel_all[f] / lpk[f] * c('Billion') * cf2[f]) for f in fuel_all}
    bgs_obf, bdi = p['eb2|bgs'] + p['eb2|obf'], p['eb2|bdi']
    bio = put('trbio.rod.bio', np.where(p['eb|gso'] == 0, bgs_obf, bgs_obf * kt['gso'] / p['eb|gso'])
              + np.where(p['eb|die'] == 0, bdi, bdi * kt['die'] / p['eb|die']))
    kte = put('trkte.rod.ecy', elt * c('Thousand') / p['ktoe_gwh'] * cf2e)
    kmp = put('trkmp.pas.all', bkmt * cf2['gso'])
    kmf = put('trkmf.fre.all', bkmtf * cf2['die'])
    kmc = put('trkmc.cyc.all', bkmtc * cf2['gso'])
    put('trkmt.all.all', kmp + kmf + kmc)
    for f in fup:
        put(f'trfcp.pas.{f}', fup[f] * cf2[f])
    put('trfcep.pas.ecy', elp * cf2e)
    put('trfcef.fre.ecy', elf * cf2e)
    put('trfcec.cyc.ecy', elc * cf2e)
    for f in FRE_FUELS:
        put(f'trfcf.fre.{f}', fuf[f] * cf2[f])
    put('trfcc.cyc.gso', fuc * cf2['gso'])
    # average fuel economy of the stock (weights without fuel use: Excel-AI TrFEW*)
    w_gso, w_half, w_evp, w_evo = c('TrFEWGso'), c('TrFEWHalf'), c('TrFEWEvP'), c('TrFEWEvO')
    put('trafg.all.gso', np.where(fua == 0, fso['gso'] * w_gso + fsoc * (1 - w_gso),
                                  (fso['gso'] * fup['gso'] + fsoc * fuc) / (fup['gso'] + fuc)))
    for f in FRE_FUELS:
        put(f'trafo.all.{f}', np.where(fub[f] == 0, fso[f] * w_half + fsof[f] * (1 - w_half),
                                       (fso[f] * fup[f] + fsof[f] * fuf[f]) / (fup[f] + fuf[f])))
    afen = put('trafen.all.ecy', febo * elp + febof * elf + feboc * elc)
    put('trafe.all.ecy', np.where(elt == 0, febo * w_evp + (febof + feboc) * w_evo, afen / (elp + elf + elc)))
    vht = put('trvht.pas.all', sum(veh.values()) + vehb)
    vhtf = put('trvhtf.fre.all', sum(vehf.values()) + vehfb)
    vhtc = put('trvhtc.cyc.all', vehc + vehcb)
    put('trvhta.all.all', vht + vhtf + vhtc)
    return sum(kt.values()) + bio + kte                       # road fuel use of the engineer model (ktoe)


def _results(x, dk, evac, evcc, lgfb, evaf, lgcb, evacc, road_use):
    """EQ-A3.9: range-anxiety fit targets, fuel use read by the transport co-benefits module (rows 4576-4616)."""
    put = x.put
    D = lambda v: np.where(dk, v, np.nan)
    put('trrafp.pas.ev', D(evcc - evac))
    put('trraff.fre.ev', D(lgfb - evaf))
    put('trrafc.cyc.ev', D(lgcb - evacc))
    for f in ('gso', 'die', 'lpg', 'nga', 'ecy'):
        src = (lambda s: x(f'eldem.{s}.ecy')) if f == 'ecy' else (lambda s: x(f'ener.{s}.{f}'))
        rod, total = put(f'trq.rod.{f}', src('rod')), put(f'trq.all.{f}', src('all'))
        put(f'tran.rsh.rod.{f}', np.where(total == 0, 0.0, rod / total))
    put('trsum.rod.all', road_use)
