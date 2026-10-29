"""Phase 3: the mitigation blocks built so far match Excel-AI's stored values for Egypt, code by code and year by year
(NORMS 7). Each block lists its variables (core/variables.csv names): every reference code of those variables
(scenarios 1 and 2) must be produced and match."""
import pandas as pd
import pytest

import cpat_model
from cpat_model.core.variables import PATH as VARIABLES_CSV
from cpat_model.inputs import read_scenario_set
from cpat_testing.compare.compare import compare, reference, summary


def section(first, last, without=()):
    """The variables of the Mitigation rows from `first` to `last` (sheet order), less `without`."""
    v = pd.read_csv(VARIABLES_CSV)
    i0, i1 = v.index[v['variable'] == first][0], v.index[v['variable'] == last][-1]
    return sorted(set(v.loc[i0:i1, 'variable']) - set(without))


DEFERRED_1 = ['airpol.mc', 'pig.ap', 'cc.code', 'pig.tr', 'pigx', 'xcpb', 'xpre', 'pig.fe0', 'pig.wsh',
              'pig.mu0', 'pig.rsh0', 'pig.kpl', 'pig.trb.acc', 'pig.trb.con', 'pig.trb.rdm', 'pig.phi', 'pig.efw', 'pig.vpm', 'pig.trk', 'pig.trg.acc', 'pig.trg.con', 'pig.trg.rdm']
BUILT = {
    '3.1 header': ['infl', 'defl', 'gdp.usd', 'gdp.lcu', 'xr', 'gdp.base'],
    '3.2 policies': section('CPIntro', 'cptraj', DEFERRED_1),
    '3.3 prices': ['IntEnerPricForeSource', 'IntEnerPricForecastAdjustment', 'gp.src', 'gp.adj', 'gpn', 'gp', 'gpi',
                   'spf', 'esubpu', 'ps', 'sp', 'txf', 'txo', 'fadtx', 'cs', 'etx', 'esub', 'vat', 'pbc', 'pcsw', 'ppcw'],
    '3.4 power costs': ['cfu', 'nuu', 'wsel', 'wfx', 'wac', 'dlf', 'dlfr', 'kwh', 'cap0', 'invs', 'perm', 'start', 'scat',
                        'scv', 'rate', 'rr', 'erf', 'spot', 'ctf', 'stm', 'ltu', 'ppa', 'rnsp', 'rns', 'rbs', 'exs', 'tcf',
                        'cbat', 'cint', 'obat', 'elcx', 'eltk', 'elof', 'elov', 'cel', 'incp', 'inc.ela.adj', 'shock',
                        'cax', 'cics', 'cicl', 'cic', 'fpn', 'fpp', 'xck', 'vbc', 'xac', 'shk', 'reb', 'tvc', 'tvcx', 'dsum',
                        'lvc', 'fce', 'cik', 'swd', 'cph', 'pcbcap', 'pcbom', 'pcbfu', 'pcbcp', 'pcbrns', 'pcbct', 'entxd',
                        'entx', 'pret', 'permit', 'ntxg', 'ntxb'],
    '3.7a fuel prices by subsector': ['ctxnew', 'ets', 'ntx', 'nce', 'xcp', 'xcpd', 'csw', 'pcw', 'atp', 'shp', 'aef'],
    # the year loop
    '3.8 power year step': ['caxav', 'stoav', 'fix', 'lfx', 'gnc', 'gncav', 'ccpav', 'tic', 'swi', 'cur', 'sys', 'pcbchk',
                            'cons', 'sc', 'rppre', 'pex', 'rp', 'sgap', 'rcarb', 'rexs', 'rexm', 'rvat', 'rnvat', 'rreb',
                            'rpex', 'rgap', 'rpnv', 'txg', 'txe', 'scl', 'psegap', 'psegs', 'psesh', 'pseu', 'pser', 'csd',
                            'ores', 'spe', 'pdem', 'aeef', 'mult', 'dem', 'demg', 'demtot', 'req', 'reqcg', 'vcmin', 'rem',
                            'gmx', 'gmin', 'lgd', 'glg', 'ppr', 'gen_mwy', 'dgen', 'shr', 'pe', 'vre', 'msc', 'cap',
                            'effcap', 'ret', 'rec', 'egrow', 'ecmin', 'ecshr', 'early', 'kafter', 'need', 'mancap', 'mani',
                            'needm', 'cmin', 'deficit', 'maxinv', 'lgi', 'pni', 'first', 'space', 'second', 'dgas', 'nei',
                            'nim', 'nid', 'phi', 'prtx', 'prsub', 'prxc', 'prnew', 'prxl', 'prrns', 'pet'],
    '3.7b fuel use by subsector': ['enel', 'ener', 'eldem', 'co2', 'ch4', 'rtx', 'rsub', 'rnew', 'rxcp', 'rsr', 'rex', 'rvt', 'trbe', 'trbea', 'trpren', 'trrena',
                                   'lkt', 'lkp', 'lkd', 'lkb', 'lkxp', 'lkxe', 'lkxr', 'lkx', 'lkxa', 'lkz', 'lkc', 'lkcb'],
    '3.3b price averages': ['pnq', 'pctx', 'etsnew', 'pntx', 'pxcd', 'pvatn', 'pnce', 'rpn', 'pav.sp', 'pav.q', 'pav.uv',
                            'pav.spr', 'pav.las', 'pav.sp0', 'pav.time', 'pav.mix', 'pav.leg', 'pav.lidx', 'pav.idx',
                            'pavl.qr', 'pavl.qi', 'pavl.qp', 'pavl.pp', 'rpe'],
    '3.9a energy totals': ['echg', 'epct', 'ener.chk', 'ener.ref', 'ener.pct'],
    '3.9b revenue totals': ['rmf', 'rpsu', 'rnet', 'rtot.ref', 'rev.chk', 'rfu', 'rfg', 'rfu.chk', 'rbe', 'rpct', 'gdpn',
                            'rpol', 'rpol.chk', 'rtot', 'rtot.chg', 'covct'],
    '3.10 CO2, other GHGs, NDC': ['co2.ref', 'co2.pct', 'co2.sec', 'co2.ets', 'co2.cap', 'co2.gap', 'ets.lr', 'ets.next',
                                 'bco2.chk', 'co2.chk', 'cchg', 'co2.grid', 'kaya', 'kidx', 'co2.chg', 'pop', 'pop.g',
                                 'gdppc.g', 'ghg.h', 'ghg.m', 'ghg.gi', 'ghg.dr', 'ch4.wd', 'ch4.fk', 'ch4.pi',
                                 'ch4.prd', 'ch4.act', 'ch4.abt', 'ch4.int', 'ch4.em', 'ch4.c', 'ch4.sup', 'ghg.k',
                                 'ghg.flr', 'ghg', 'ghg.inc', 'ghg.ref', 'ghg.pct', 'ch4.rev', 'ch4.emf', 'ch4.revf',
                                 'ch4bs.chk', 'gchg', 'ghg.chg', 'ndc.key', 'ndc.typ', 'ndc.k', 'ndc.ty', 'ndc.alt',
                                 'ndc.ref', 'ndc.x', 'ndc.lu', 'ndc.gas', 'ndc.co2', 'ndc.bs', 'ndc.bty', 'ndc.bi',
                                 'ndc.hk', 'ndc.hh', 'ndc.hc', 'ndc.hv', 'ndc.h', 'ndc.gdp', 'ndc.hi', 'ndc.f', 'ndc.lv',
                                 'ndc.r', 'ndc.lvl', 'ndc.idx', 'ndc.bau', 'ndc.red', 'ndc.gap', 'ndc.over'],
    '3.10b local air pollutants': ['ap.w', 'apfd', 'ap', 'apf', 'aps', 'apen', 'apco2', 'ghg.enrp'],
    '3.12a carbon pricing indicators': ['tcp', 'cpeff', 'cov.ct', 'cov.ets', 'cov.all', 'ecr'],
    '3.11 GDP effects': ['gdp.pos.pct', 'fis.rev', 'fis.ref', 'fis.sp', 'fis.imp', 'fis.lag', 'fis.impp', 'fis.lagp',
                         'fis.grp', 'fis.key', 'fis.eff', 'gdp.lvl', 'gdp.pos.usd', 'gdpg', 'gdpy', 'gdp.chg.usd',
                         'gdp.eff', 'EXPLabortax', 'EXPCIT', 'EXPCapex', 'EXPGoodsandserv', 'EXPTransfers',
                         'MultipliersSource', 'GDPStartYear', 'FmAdj', 'GDPEndogenous'],
    '3.11b external balance': ['xnim', 'xnim.pct', 'xtb', 'xtb.pct', 'xtbp', 'bca', 'bca.d', 'bca.dp', 'bca.gdp', 'bca.n',
                               'bca.p', 'bca.pp', 'bca.r', 'bca.y'],
}


@pytest.fixture(scope='module')
def results():
    return cpat_model.run(read_scenario_set()).by_code('EGY')


@pytest.mark.parametrize('block', BUILT)
def test_block_matches_excel_ai(results, block):
    ref = reference()
    v = pd.read_csv(VARIABLES_CSV)
    stems = set(BUILT[block])
    codes = {c[:-2] for c, var in zip(v['code'], v['variable']) if var in stems}          # without the scenario
    expected = [c for c in ref.index if c[:-2] in codes and c[-1] in '12'
                and ref.loc[c].notna().any()]           # rows with parameters only (no year values) are not results
    missing = sorted(set(expected) - set(results.index))
    assert not missing, missing[:20]
    report = compare(results.loc[expected], ref=ref)
    assert report['first_bad'].isna().all(), summary(report[report['first_bad'].notna()])
