"""CPAT codes map for the mitigation prototype (v7.1): the legacy codes map updated for the prototype, with the code protocol.

Reads (read only):
  - the legacy codes map    ../legacy/workbooks/CPATMasterProcessesCodesAndDefaults.xlsx (CodesAndLookups sheets)
  - the legacy workbook     ../legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb (Mitigation codes G/H, MTOutputs)
  - the prototype                 CPAT-AI-Mitigation-Prototype-v7.1.xlsm (Mitigation code column, LiveOutputs, variable dictionary)
  - the crosswalk           <repo>/data/mvp_legacy_extracts/codes_crosswalk_v7_1.csv (prototype variable -> legacy code,
                            curated: every prototype variable whose quantity legacy codes differently)
Writes:
  - CPAT_CodesMap_v7_1.xlsx (sheets: Cover, Protocol, Positions, the vocabularies, Variables, Crosswalk, LiveOutputs,
    MVPOnly, Checks) and lints it (../excel_lint.py).

    python make_codes_map_v7_1.py

The protocol (sheet Protocol) is the rule set; Codes_Remediation_Plan_v7_1.md is the plan to bring the prototype onto it.
"""
import csv
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter as L

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
ORIG = os.path.join(HERE, '..', 'legacy', 'workbooks')
MASTER = os.path.join(ORIG, 'CPATMasterProcessesCodesAndDefaults.xlsx')
LEGACY = os.path.join(ORIG, 'CPAT 1.0pre_456_NoPropData.xlsb')
prototype = os.path.join(HERE, 'CPAT-AI-Mitigation-Prototype-v7.1.xlsm')
XWALK = os.path.join(ROOT, 'data', 'mvp_legacy_extracts', 'codes_crosswalk_v7_1.csv')
OUT = os.path.join(HERE, 'CPAT_CodesMap_v7_1.xlsx')
VERSION = '7.1'
DATE = '2026-10-21'

FONT = Font(name='Arial', size=10)
FONT_B = Font(name='Arial', size=10, bold=True)
FONT_T = Font(name='Arial', size=14, bold=True)
F_HEAD = PatternFill('solid', fgColor='D9D9D9')
F_CODE = PatternFill('solid', fgColor='DCE6F1')     # code cells (excel_ai/NORMS.md 2.x colours)
F_FLAG = PatternFill('solid', fgColor='FCE4D6')     # a deviation from legacy or from the protocol
WRAP = Alignment(wrap_text=True, vertical='top')

MODULES = ('mit', 'distn', 'air', 'ap', 'tra', 'dist', 'tran', 'emi')

# ---------------------------------------------------------------------------------------------------------------
# The protocol. Each rule: id, rule, legacy practice (what legacy does, counted on the 456 file), prototype v7.1 practice.
# Counts in {braces} are filled from the checks below.
# ---------------------------------------------------------------------------------------------------------------
PROTOCOL = [
    ('C0', 'Purpose and authority',
     'A CPAT code names one row of a model sheet: one quantity, for one set of members, in one scenario. Modules '
     '(Distribution, air pollution), LiveOutputs/MTOutputs, StoredOutputs, the Python model (coded) and the '
     'legacy team find a quantity by its code. This protocol is the rule for every code; this workbook holds the '
     'vocabularies (one sheet each) and the variable dictionary (sheet Variables) it refers to. A code is generated '
     'from the row\'s descriptors (variable, sector, fuel, other, model letter, scenario), never typed.',
     'The legacy codes map (CodesAndLookups) states the positions but not the rules; legacy follows them in its '
     'model rows and not elsewhere (rules below).',
     'The prototype generates codes from columns A (variable), C (sector), B (fuel), the variable dictionary (code end) '
     'and the scenario number (build_v7_1.code_formula).'),
    ('C1', 'Characters',
     'Lower case a-z, digits 0-9 and the underscore; tokens separated by a full stop; no spaces, capitals, hyphens or '
     'empty tokens (no trailing full stop). One exception: a pass-through row of a ScenarioDefinition (MTInputs) '
     'input uses the input\'s NameOfParameter verbatim as its variable (CamelCase), as legacy MTInputs and '
     'coded do (e.g. egy.mit.CPIntro.1).',
     'Mostly followed. Deviations: "All" in the em.* rows ({leg_upper} codes); empty tokens and trailing full stops '
     '({leg_empty} codes, e.g. egy.mit.fix.pow.coa.t.).',
     'Followed; {mvp_upper} pass-through codes use NameOfParameter (allowed).'),
    ('C2', 'Grammar of a model-row code',
     '<iso>.<tab>.<variable>[.<sector>][.<fuel>][.<other>].<scenario>\n'
     'Positions, left to right: 1 country, 2 module, 3 variable, then the dimension slots in this fixed order: '
     'sector, fuel, other (pollutant, vehicle class, technology, inventory category); the scenario number is '
     'always last. No model letter (C7). The order is the same for every variable, legacy or new (user decision '
     '2026-10-21: self-consistent codes). A slot the variable does not have is filled with all (C5). Every row of one variable uses the '
     'same template (the slots and their order), recorded in sheet Variables.',
     'The legacy codes map states Country.Tab.Variable.Sector.FuelType.Other.SubScenNo. The model rows follow it '
     '(ener.pow.coa.e, atp.rod.gso.e, ctx.pow.coa.a, cap.pow.coa.t); results blocks E-G, the MTOutputs rows and '
     'several sections put the fuel first (co2.coa.pow, em.pm2.coa.pow, atp.coa.pow.pct, rp.coa.wtd) or the pollutant '
     'before the members (em.pm2.coa.pow). One variable often has two templates (ctx.coa.pow and ctx.pow.coa.a).',
     'Sector before fuel throughout (code_formula). The template is the same for a whole variable. Deviations: '
     'members that are not sectors or fuels are written into the sector and fuel columns (C6).'),
    ('C3', 'Country (position 1) and module (position 2)',
     'Country: ISO 3166 alpha-3, lower case (sheet CountryCode). Module: the module that computes the row: mit '
     '(mitigation), distn (distribution), air (air pollution), tra (transport module, when built). Data keys '
     '(C9) have no country.',
     'The legacy table lists ap and dist, but legacy codes use air ({leg_air} codes) and distn ({leg_distn}). '
     'Some legacy rows have no country (emi.pow.bc.1, air.ef rows, ExposureCoefs) or a region (afr, wld) in '
     'position 1.',
     'mit and distn as legacy. The air-pollution results sit in Mitigation under variable ap (mit.ap.<sector>.<pollutant>), '
     'where legacy codes them em.<pollutant>.<sector> (sheet Crosswalk); the air module, when built, takes air.'),
    ('C4', 'Variable (position 3)',
     'The variable comes from sheet Variables. Reuse the legacy variable whenever legacy computes the same '
     'quantity; never a new name for a legacy quantity. 2 to 12 characters. A unit or measure variant joins the '
     'stem with an underscore (elec_gwh, gen_ktoe, gen_mwy). A qualifier that subdivides a variable may follow it '
     'after a full stop (rev.new, rev.exi, gdp.pre, fis.mul) only when it is registered with the variable in '
     'sheet Variables; a qualifier never equals a dimension code or a model letter.',
     'Underscore variants as the rule (elec_gwh, gen_mwy); unit tokens as separate positions elsewhere '
     '(exp.coa.usd, rev.tot.coa.usd, atp.coa.pow.pct); dotted variables (gdp.pre.lvl, inc.ela.adj, air.ef).',
     '{mvp_vars} variables, {mvp_common} with a legacy variable token; {xw_renamed} prototype variables compute a legacy '
     'quantity under a new name (sheet Crosswalk).'),
    ('C5', 'all, tot and left-out slots',
     'all: one value that applies to every member of the slot (the gasoline price is the same in every sector: '
     'rp.all.gso.a). tot: the sum or aggregate over the members (fuel use of road, all fuels: ener.rod.tot.e; '
     'nameplate capacity, all plants: cap.pow.tot). A slot the variable does not have may be filled with all '
     '(user decision 2026-10-21: the prototype keeps its fixed sector and fuel slots, gdp.usd.all.all, ssc.pow.all); '
     'legacy leaves it out (mit.cptraj.1, mit.co2cov.pow.1) and the legacy form is kept as an alias. A total is '
     'never written all. A sector group (ind, tra, bld, oth) in the '
     'sector slot is the aggregate of its subsectors; the sector slot holds one code, never a group and a '
     'subsector (co2.tra.rod is co2.rod).',
     'all for "applies to all" ({leg_all} codes) and tot for totals ({leg_tot} codes), as above; group and '
     'subsector together in co2.tra.rod.',
     'all for both meanings ({mvp_all} all, {mvp_tot} tot): totals (ener.rod.all.e for legacy ener.rod.tot.e) and '
     'padding of slots the variable does not have (gdp.usd.all.all, ssc.pow.all).'),
    ('C6', 'Vocabularies: one per slot, closed, disjoint',
     'Each slot takes codes from its own sheet only: sector (Sector), fuel (FuelType), other (Pollutant, '
     'VehicleClass, OtherMembers), model (Submodel), scenario (Scenario). A new member is added to its sheet '
     'before it is used. The vocabularies do not share codes (except all and tot), so a code parses even when '
     'a slot is left out. Electricity as a fuel is ecy (never ele, elc); oil as an aggregate fuel is oil.',
     'Fuel codes as the FuelType sheet; ele for electricity in {leg_ele} codes (dem.ele, pric.ele, csu.exi.ele); '
     'vehicle classes pass, fre/freight, motor; pollutants pm2, co2 used but not in the Pollutant sheet.',
     'Fuels and sectors as legacy, plus rail (ral, used by legacy but not in its Sector sheet). Members outside '
     'the vocabularies are written into the fuel or sector column: pollutants, ch4 sources, lags l1-l19, Kaya '
     'terms, revenue parts ({mvp_offvocab} codes; sheet MVPOnly); vehicle classes pas/fre/cyc/bus/lgt/pau and '
     'technologies ice/bev/phv/ev where legacy uses pass/fre/motor and ev.'),
    ('C7', 'Model letter',
     'No model letter (user decision 2026-10-21). Legacy\'s submodel letters (sheet Submodel: t engineer, '
     'e elasticity, s selected, b both, a all) are not part of a code; legacy codes that carry one are aliases '
     '(ener.rod.coa for legacy ener.rod.coa.e, cap.pow.coa for cap.pow.coa.t). Where two quantities differ only '
     'by the submodel, they are different variables (pe, engineer primary energy of power plants, beside ener). '
     'Single-letter tokens are not used.',
     'Followed in the model rows (ener.*.e, cap.pow.coa.t, atp.pow.coa.t, rp.pow.coa.a); s is used '
     '(ener.pow.coa.s, elec_gwh.tot.s) but missing from the Submodel sheet.',
     'Kept for fuel use, prices and taxes (.e, .a: 1,935 codes, to drop; dropping them makes no two codes '
     'equal); already dropped for the engineer power model ({mvp_noletter} variables); single letters used as '
     'qualifiers or members ({mvp_single} codes: fpr.s, etsb.t, ndc.x.all.u).'),
    ('C8', 'Scenario (last position)',
     'The scenario number (SubScenario; 1 = baseline), always the last token of a model-row code. The legacy '
     'MT scenario names (U1, P2) are not CPAT codes. A setting that is not per scenario has no scenario '
     'number only on a data or settings sheet.',
     'Followed in the model rows; inputs and settings in Mitigation have no number ({leg_noscen} codes).',
     'Every model row has the number.'),
    ('C9', 'Data keys (legacy data tabs)',
     'A data tab keeps the legacy table and its keys unchanged (paste compatibility, excel_ai/NORMS.md 1.6 '
     'rule 2): mit.<variable>.<fuel>.<sector>, no country and no scenario (Prices_dom mit.sp.coa.pow; EnergyCons '
     '<iso>.mit.enc.<fuel>; ECP <iso>.mit.ecr.<fuel>). Fuel before sector is the legacy data order; new data keys '
     'follow it. A model row that reads a data key shows the key in Input Code and its own code (C2) in Output '
     'Code.',
     'As stated (Prices_dom, EnergyCons, ECP, EF_GHG, EF_PM).',
     'As legacy (data tabs pasted unchanged).'),
    ('C10', 'Uniqueness',
     'A code appears once in the code column of a sheet. A quantity shown twice (a memo copy in a results '
     'section) reads the original row; if it needs a row of its own, it gets a distinct code.',
     '{leg_dup} output codes appear more than once in legacy Mitigation (the 456 file).',
     '{mvp_dup} codes appear twice in prototype Mitigation (section 11 repeats ener.<sector>.all.e; sheet Checks).'),
    ('C11', 'Legacy variable names, self-consistent codes',
     '(a) User decision 2026-10-21: a Mitigation row that replicates a legacy quantity carries legacy\'s variable '
     'name (sheet Variables), in the protocol\'s structure (C2-C7): the same slot order, no model letter, tot for '
     'totals, members from the vocabularies. Where legacy\'s whole code differs only in structure (fuel first, '
     'model letter, left-out slot), legacy\'s code is an alias, recorded in sheet Crosswalk, not copied (a legacy '
     'issue, tracked). (b) LiveOutputs (legacy MTOutputs) carries the protocol code and shows the MTOutputs code '
     'as an alias beside it. (c) A legacy code that is a bug (wrong label, empty token, duplicate) is an alias too; '
     'the prototype name follows the quantity. Example: legacy nox.tot holds N2O (label, value 28.5 Mt CO2e in 2022 for Egypt, part of total '
     'GHGs) and legacy\'s NOx row (-5.5 Mt CO2e, a cooling forcing) is coded oc.tot. (the organic-carbon code, no '
     'scenario): in the prototype N2O is n2o.tot and NOx is nox.tot. (d) A quantity legacy does not code follows the protocol.',
     '-',
     'Not yet: see sheet Crosswalk and Codes_Remediation_Plan_v7_1.md (incremental steps R0-R8).'),
]


# ---------------------------------------------------------------------------------------------------------------
# Readers
# ---------------------------------------------------------------------------------------------------------------
def read_master():
    """The CodesAndLookups sheets of the legacy codes map: {sheet: [rows]} (blank rows dropped)."""
    wb = openpyxl.load_workbook(MASTER, read_only=True, data_only=True)
    out = {}
    for sn in ('CodesAndLookups', 'CountryCode', 'Tab', 'Variables', 'FuelType', 'UNFCCSector', 'Sector', 'Submodel',
               'Pollutant', 'Unit', 'Policy', 'Year'):
        name = sn if sn in wb.sheetnames else sn + '>>'
        rows = []
        for r in wb[name].iter_rows(values_only=True):
            if any(c is not None for c in r):
                rows.append(['' if c is None else c for c in r])
        out[sn] = rows
    return out


def read_legacy():
    """Legacy 456 file: Mitigation input/output codes by row and the MTOutputs codes."""
    from pyxlsb import open_workbook
    mit, mto = [], []
    with open_workbook(LEGACY) as wb:
        with wb.get_sheet('Mitigation') as sh:
            for i, row in enumerate(sh.rows(), 1):
                d = {c.c: c.v for c in row if c.v not in (None, '')}
                for col, kind in ((6, 'input'), (7, 'output')):
                    v = d.get(col)
                    if isinstance(v, str) and is_code(v):
                        mit.append({'row': i, 'kind': kind, 'fuel': str(d.get(1, '')), 'sector': str(d.get(2, '')),
                                    'desc': str(d.get(3, ''))[:120], 'unit': str(d.get(4, '')), 'code': v.strip()})
        with wb.get_sheet('MTOutputs') as sh:
            for i, row in enumerate(sh.rows(), 1):
                d = {c.c: c.v for c in row if c.v not in (None, '')}
                v = d.get(4)
                if isinstance(v, str) and is_code(v):
                    mto.append({'row': i, 'desc': str(d.get(3, ''))[:120], 'code': v.strip()})
    return mit, mto


def read_mvp():
    """prototype v7.1: Mitigation rows with a code, LiveOutputs codes, the variable dictionary."""
    wb = openpyxl.load_workbook(prototype, read_only=True, data_only=True)
    mit = []
    for i, r in enumerate(wb['Mitigation'].iter_rows(max_col=11, values_only=True), 1):
        if isinstance(r[10], str) and is_code(r[10]):
            mit.append({'row': i, 'var': s(r[0]), 'fuel': s(r[1]), 'sector': s(r[2]), 'desc': s(r[7])[:120],
                        'unit': s(r[8]), 'code': r[10]})
    live = []
    for i, r in enumerate(wb['LiveOutputs'].iter_rows(max_col=4, values_only=True), 1):
        if isinstance(r[0], str) and is_code(r[0]):
            live.append({'row': i, 'code': r[0], 'stem': s(r[1]), 'desc': s(r[2])[:120], 'unit': s(r[3])})
    vd = OrderedDict()
    for r in wb['Check, Variables, Lambdas'].iter_rows(min_row=5, max_col=11, values_only=True):
        if s(r[0]) == 'Variable':          # the LAMBDA table starts: the dictionary ends
            break
        if r[0] is not None:
            vd[s(r[0])] = {'label': s(r[1]), 'unit': s(r[2]), 'legacyref': s(r[5]), 'codeend': s(r[10])}
    return mit, live, vd


def read_crosswalk():
    with open(XWALK, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def s(x):
    return '' if x is None else str(x)


CODE_RE = re.compile(r'^[A-Za-z0-9_]+(\.[A-Za-z0-9_]*)+$')


def is_code(v):
    v = v.strip()
    return bool(CODE_RE.match(v)) and (v.split('.')[1] in MODULES or v.split('.')[0] in MODULES)


def stem(code):
    """Code without country and scenario number: egy.mit.ener.rod.coa.e.1 -> mit.ener.rod.coa.e."""
    t = code.split('.')
    if len(t) > 1 and len(t[0]) == 3 and t[0] not in MODULES and t[1] in MODULES:
        t = t[1:]
    if t and t[-1].isdigit():
        t = t[:-1]
    return '.'.join(t)


def var_token(code):
    t = stem(code).split('.')
    return t[1] if len(t) > 1 and t[0] in MODULES else t[0]


# ---------------------------------------------------------------------------------------------------------------
# Additions to the legacy vocabularies: codes legacy uses but its codes map does not list, and the prototype's members.
# (code, description, status, note). Status: legacy-unlisted = used in legacy codes, missing from the legacy sheet;
# mvp-new = prototype member with no legacy code (allowed, protocol C6); mvp-rename = prototype member for a legacy code (fix).
# ---------------------------------------------------------------------------------------------------------------
ADD_FUEL = [
    ('oil', 'Oil products, aggregate (gso, die, lpg, ker, jfu, oop)', 'legacy-unlisted', 'pros.oil.all, psu.exi.oil, co2.oil'),
    ('ele', 'Electricity (non-standard)', 'legacy-unlisted', 'Use ecy (C6). Legacy dem.ele, pric.ele, csu.exi.ele; '
     'coded FuelCode ele'),
    ('fos', 'Fossil fuels, aggregate', 'legacy-unlisted', 'ener.tot.fos.e'),
    ('ice', 'Internal combustion vehicle (technology)', 'mvp-new', 'Road engineer model; slot other (C6), not fuel'),
    ('bev', 'Battery electric vehicle (technology)', 'mvp-new', 'Slot other; legacy codes the EV as ev'),
    ('phv', 'Plug-in hybrid vehicle (technology)', 'mvp-new', 'Slot other'),
    ('ev', 'Electric vehicle (technology)', 'legacy-unlisted', 'stockcalc.ev.pass, shrcalc.ev.pass'),
]
ADD_SECTOR = [
    ('ral', 'Rail', 'legacy-unlisted', 'Legacy air.ef.ral.die.pm2, co2.tra.ral; transport group tra'),
    ('mnf', 'Manufacturing (air-pollution group)', 'legacy-unlisted', 'air.ef.mnf.coa.pm2, em.*.All.mnf'),
    ('tot', 'Total over the members', 'legacy-unlisted', 'C5: aggregate; distinct from all'),
]
VEHICLE = [  # code, description, legacy code, status
    ('pass', 'Passenger and light vehicles', 'pass', 'legacy'),
    ('fre', 'Freight vehicles', 'fre (ener.rod.die.fre); freight in stockcalc.ev.freight', 'legacy (two spellings)'),
    ('motor', '2-3 wheelers', 'motor', 'legacy'),
    ('pas', 'Passenger and light vehicles (prototype)', 'pass', 'mvp-rename: use pass'),
    ('cyc', '2-3 wheelers (prototype)', 'motor', 'mvp-rename: use motor'),
    ('pau', 'Used passenger and light vehicles (prototype)', '-', 'mvp-new'),
    ('lgt', 'Light vehicles (prototype)', '-', 'mvp-new'),
    ('bus', 'Buses (prototype)', '-', 'mvp-new'),
]
ADD_POLLUTANT = [
    ('pm2', 'Fine particulate matter (PM2.5)', 'legacy-unlisted', 'air.ef.*.pm2, em.pm2.*'),
    ('co2', 'Carbon dioxide', 'legacy-unlisted', 'ghg.enr.co2'),
    ('n2o', 'Nitrous oxide', 'legacy-unlisted', 'Legacy labels N2O as nox in mit.nox.tot (a legacy bug: nox is NOx)'),
    ('fga', 'F-gases (PFCs, HFCs, SF6, NF3)', 'legacy-unlisted', 'mit.fga.tot'),
    ('pom', 'Primary organic matter', 'legacy-unlisted', 'em.pom.cpp'),
    ('opm', 'Other primary PM2.5 (prototype)', 'mvp-new', 'aps.cpp.opm'),
]
ADD_MODEL = [('s', 'Selected model (the model chosen by the power-model switch)', 'legacy-unlisted',
              'ener.pow.coa.s, elec_gwh.tot.s')]
ADD_TAB = [  # code, module, status, note
    ('air', 'Air pollution', 'legacy-unlisted', 'Legacy codes use air (the legacy sheet says ap): use air'),
    ('distn', 'Distribution', 'legacy-unlisted', 'Legacy codes use distn (the legacy sheet says dist): use distn'),
    ('emi', '(none: row label)', 'legacy-unlisted', 'emi.pow.bc.1 has no country; a legacy issue'),
]


# ---------------------------------------------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------------------------------------------
def token_sets(master):
    fuels = {str(r[0]) for r in master['FuelType'][1:] if r[0]} | {a[0] for a in ADD_FUEL}
    sectors = {str(r[1]) for r in master['Sector'][1:] if r[1]} | {str(r[3]) for r in master['Sector'][1:] if r[3]} | \
        {a[0] for a in ADD_SECTOR} | {'all'}
    pols = {str(r[1]) for r in master['Pollutant'][1:] if r[1]} | {a[0] for a in ADD_POLLUTANT}
    models = {str(r[0]) for r in master['Submodel'][1:] if r[0]} | {a[0] for a in ADD_MODEL}
    return fuels, sectors, pols, models


def mvp_template(row):
    """Template of an prototype row: its code with the member tokens of columns C and B replaced by {sector}, {fuel}."""
    t = stem(row['code']).split('.')
    out = []
    for i, tok in enumerate(t):
        if i >= 2 and tok == row['sector'] and '{sector}' not in out:
            out.append('{sector}')
        elif i >= 2 and tok == row['fuel'] and '{fuel}' not in out:
            out.append('{fuel}')
        else:
            out.append(tok)
    return '.'.join(out)


def legacy_template(code, fuels, sectors, pols, models):
    """Template of a legacy code by vocabulary: sector, fuel, pollutant and model tokens become slots."""
    t = stem(code).split('.')
    head = 2 if t[0] in MODULES else 1
    out = t[:head]
    for tok in t[head:]:
        if tok in ('all', 'tot', 'All'):
            out.append(tok)
        elif tok in sectors and tok not in fuels:
            out.append('{sector}')
        elif tok in fuels and tok not in sectors:
            out.append('{fuel}')
        elif tok in pols:
            out.append('{pollutant}')
        elif tok in models and tok == t[-1]:
            out.append('{model:' + tok + '}')
        else:
            out.append(tok)
    return '.'.join(out)


def checks(leg_mit, leg_mto, mvp_mit, live):
    """Counts for the protocol rules (C1, C3, C5-C8, C10) on legacy (456) and prototype (v7.1)."""
    lo = [r['code'] for r in leg_mit if r['kind'] == 'output']
    la = [r['code'] for r in leg_mit]
    mc = [r['code'] for r in mvp_mit]
    lc = [r['code'] for r in live]
    tok = lambda codes: Counter(x for c in codes for x in stem(c).split('.'))
    lt, mt = tok(la), tok(mc)
    dup = lambda codes: sorted(k for k, n in Counter(codes).items() if n > 1)
    single = [c for c in mc if any(len(x) == 1 and not x.isdigit() and i < len(stem(c).split('.')) - 1
                                   for i, x in enumerate(stem(c).split('.')[2:], 2))]
    return {
        'leg_upper': sum(1 for c in la if re.search(r'[A-Z]', stem(c))),
        'leg_empty': sum(1 for c in la if '..' in c or c.endswith('.')),
        'leg_air': sum(1 for c in la + [r['code'] for r in leg_mto] if '.air.' in '.' + c),
        'leg_distn': sum(1 for c in la + [r['code'] for r in leg_mto] if '.distn.' in '.' + c),
        'leg_all': lt['all'], 'leg_tot': lt['tot'], 'leg_ele': lt['ele'],
        'leg_noscen': sum(1 for c in la if not c.split('.')[-1].isdigit()),
        'leg_dup': len(dup(lo)), 'leg_dup_list': dup(lo),
        'mvp_upper': sum(1 for c in mc if re.search(r'[A-Z]', c)),
        'mvp_all': mt['all'], 'mvp_tot': mt['tot'],
        'mvp_single': len(single), 'mvp_dup': len(dup(mc)), 'mvp_dup_list': dup(mc),
    }


# ---------------------------------------------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------------------------------------------
def sheet(wb, name, title, note, header, rows, widths=None, code_cols=(), flag=None):
    """One table sheet: title (row 1), note (row 2), header (row 4), data from row 5; frozen, filtered."""
    ws = wb.create_sheet(name)
    ws['A1'] = title
    ws['A1'].font = FONT_T
    ws['A2'] = note
    ws['A2'].font = FONT
    for j, h in enumerate(header, 1):
        c = ws.cell(4, j, h)
        c.font, c.fill, c.alignment = FONT_B, F_HEAD, WRAP
    for i, r in enumerate(rows, 5):
        bad = flag(r) if flag else False
        for j, v in enumerate(r, 1):
            c = ws.cell(i, j, v)
            c.font = FONT
            if j in code_cols:
                c.fill = F_CODE
            if bad and j == 1:
                c.fill = F_FLAG
    for j, w in enumerate(widths or [], 1):
        ws.column_dimensions[L(j)].width = w
    ws.freeze_panes = 'B5'
    if rows:
        ws.auto_filter.ref = f'A4:{L(len(header))}{4 + len(rows)}'
    return ws


def usage(codes, token):
    return sum(1 for c in codes if token in stem(c).split('.')[1:])


def build():
    master = read_master()
    leg_mit, leg_mto = read_legacy()
    mvp_mit, live, vd = read_mvp()
    xw = read_crosswalk()
    fuels, sectors, pols, models = token_sets(master)
    k = checks(leg_mit, leg_mto, mvp_mit, live)
    la = [r['code'] for r in leg_mit]
    mc = [r['code'] for r in mvp_mit]
    lvars = {var_token(c) for c in la}
    mvars = OrderedDict()
    for r in mvp_mit:
        mvars.setdefault(r['var'] or var_token(r['code']), []).append(r)
    k['mvp_vars'] = len(mvars)
    k['mvp_common'] = sum(1 for v in mvars if v.split('.')[0] in lvars)
    k['xw_renamed'] = len({x['mvp_var'] for x in xw if x['match_type'].startswith('renamed')})
    k['mvp_offvocab'] = sum(1 for r in mvp_mit if (r['fuel'] and r['fuel'] not in fuels | {'all'})
                            or (r['sector'] and r['sector'] not in sectors))
    k['mvp_noletter'] = len({x['mvp_var'] for x in xw if 'model letter' in x['variance']})

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Cover'
    cover = [
        ('CPAT codes map - mitigation prototype v' + VERSION, FONT_T),
        (f'Built {DATE} by make_codes_map_v7_1.py from the legacy codes map (CPATMasterProcessesCodesAndDefaults.xlsx, '
         'CodesAndLookups), the legacy workbook (CPAT 1.0pre_456_NoPropData.xlsb) and CPAT-AI-Mitigation-Prototype-v7.1.xlsm. '
         'Do not edit: change the script or the crosswalk (data/mvp_legacy_extracts/codes_crosswalk_v7_1.csv).', FONT),
        ('', FONT),
        ('Sheets', FONT_B),
        ('Protocol - the rules for every CPAT code (C0-C11): what the rule is, what legacy does, what the prototype does.', FONT),
        ('Positions - the legacy positions table (CodesAndLookups) with the protocol slot of each dimension.', FONT),
        ('Tab, FuelType, Sector, VehicleClass, Submodel, Pollutant, UNFCCSector, Unit, Scenario, CountryCode - the '
         'vocabularies: the legacy sheet, with the codes legacy uses but does not list and the prototype\'s members, and '
         'the number of legacy and prototype codes that use each code.', FONT),
        ('Variables - the legacy variable dictionary, with the prototype variable(s) for each legacy variable.', FONT),
        ('Crosswalk - every prototype variable that computes a legacy quantity under a different code: the legacy code, '
         'the kind of difference, and the code the prototype should carry (the fix).', FONT),
        ('LiveOutputs - every LiveOutputs (MTOutputs) code of the prototype and the legacy MTOutputs code of the same '
         'quantity, where there is one.', FONT),
        ('MVPOnly - prototype variables with no legacy counterpart, with the protocol rules each one breaks.', FONT),
        ('Checks - the protocol checks on legacy and on the prototype (duplicates, characters, slots).', FONT),
        ('', FONT),
        ('Remediation plan: Codes_Remediation_Plan_v7_1.md (next to this file). Fill colours: blue = code, '
         'orange = a deviation from legacy or from the protocol.', FONT),
    ]
    for i, (t, f) in enumerate(cover, 1):
        ws.cell(i, 1, t).font = f
    ws.column_dimensions['A'].width = 160

    # Protocol (inline)
    rows = [(rid, name, rule, legacy.format(**k), mvp.format(**k)) for rid, name, rule, legacy, mvp in PROTOCOL]
    ws = sheet(wb, 'Protocol', 'CPAT code protocol',
               'The rule set for every CPAT code. Legacy practice counted on the 456 file; prototype practice on v7.1. '
               'Examples drop the country and scenario where they do not matter.',
               ['Rule', 'Topic', 'Rule', 'Legacy practice', 'prototype v7.1 practice'], rows, [6, 22, 90, 60, 60])
    for row in ws.iter_rows(min_row=5):
        for c in row:
            c.alignment = WRAP

    # Positions
    pos = [r[1:8] for r in master['CodesAndLookups'] if len(r) > 7 and r[2] and r[2] not in ('CodeName',)][:14]
    slot = {'CountryCode': 'position 1 (C3)', 'Tab': 'position 2 (C3)', 'Variable': 'position 3 (C4)',
            'Unit': 'in the variable (C4: underscore variant)', 'SectorGrouping': 'sector slot (C2, C5)',
            'Sector': 'sector slot (C2)', 'FuelType': 'fuel slot (C2)', 'Submodel': 'model slot (C7)',
            'Subscenario': 'last position (C8)', 'MTScenario': 'not a CPAT code (C8)', 'Pollutant': 'other slot (C2, C6)',
            'Diseases': 'other slot (air module)', 'Air pollution risks': 'other slot (air module)',
            'Age ranges': 'other slot (air module)', 'Year': 'not in codes'}
    rows = [[*(s(x) for x in r[:6]), slot.get(s(r[1]), '')] for r in pos]
    rows.append(['', 'VehicleClass', 'Categorization', 'Used in transport codes (legacy pass/fre/motor)', 'CPAT code (lower)',
                 'e.g. pass', 'other slot (C2, C6)'])
    sheet(wb, 'Positions', 'Code positions',
          'Legacy CodesAndLookups (Country.Tab.Variable.Sector.FuelType.Other.SubScenNo) and the protocol slot of '
          'each dimension. Legacy text kept as it is.',
          ['Link in legacy file', 'Dimension', 'Type', 'In CPAT code? Position (legacy)', 'Format (legacy)',
           'Example (legacy)', 'Protocol slot'], rows, [18, 18, 14, 50, 28, 40, 34])

    # Vocabularies
    def vocab(name, title, legacy_rows, code_col, adds, extra_hdr=()):
        hdr = list(map(s, legacy_rows[0])) + ['Status', 'Note', 'Legacy codes using it', 'prototype codes using it']
        rows = []
        for r in legacy_rows[1:]:
            code = s(r[code_col])
            rows.append([*map(s, r), 'legacy', '', usage(la, code) if code else '', usage(mc, code) if code else ''])
        for code, desc, status, note in adds:
            base = [''] * len(legacy_rows[0])
            base[code_col] = code
            base[(code_col + 1) % len(base)] = desc
            rows.append([*base, status, note, usage(la, code), usage(mc, code)])
        n = len(legacy_rows[0])
        return sheet(wb, name, title, 'Legacy sheet first (as it is), then the codes legacy uses but does not list '
                     'and the prototype\'s members (Status). Counts: codes containing the code as a token after the module.',
                     hdr, rows, [14] + [24] * (n - 1) + [16, 60, 12, 12], code_cols=(code_col + 1,),
                     flag=lambda r: r[n] not in ('legacy', 'legacy-unlisted', 'mvp-new'))
    vocab('Tab', 'Modules (position 2)', master['Tab'], 0, ADD_TAB)
    vocab('FuelType', 'Fuels (fuel slot)', master['FuelType'], 0, ADD_FUEL)
    sec = master['Sector']
    vocab('Sector', 'Sectors and sector groups (sector slot)', sec, 3, ADD_SECTOR)
    sheet(wb, 'VehicleClass', 'Vehicle classes (other slot)',
          'Not in the legacy codes map. Legacy transport rows use pass, fre (freight in the EV rows) and motor; '
          'the prototype road engineer model uses its own codes (orange: rename to the legacy code).',
          ['Code', 'Description', 'Legacy code', 'Status', 'prototype codes using it'],
          [[c, d, lg, st, usage(mc, c)] for c, d, lg, st in VEHICLE], [10, 40, 50, 30, 14], code_cols=(1,),
          flag=lambda r: r[3].startswith('mvp-rename'))
    vocab('Submodel', 'Model letters (model slot)', master['Submodel'], 0, ADD_MODEL)
    vocab('Pollutant', 'Pollutants (other slot)', master['Pollutant'], 1, ADD_POLLUTANT)
    vocab('UNFCCSector', 'Inventory categories (other slot of ghg)', master['UNFCCSector'], 1, [])
    vocab('Unit', 'Units (in the variable, C4)', master['Unit'], 0, [])
    pol = master['Policy']
    sheet(wb, 'Scenario', 'Scenario numbers (last position)',
          'Legacy Policy sheet as it is. In the prototype the number is the scenario column of ScenarioDefinition '
          '(1 = baseline); the policy of a scenario is set by its inputs, not by its number.',
          list(map(s, pol[0])), [list(map(s, r)) for r in pol[1:]], [30, 40, 10])
    cc = master['CountryCode']
    sheet(wb, 'CountryCode', 'Countries (position 1, lower case)', 'Legacy sheet as it is; codes are written in '
          'lower case (egy).', list(map(s, cc[0])), [list(map(s, r)) for r in cc[1:]], [10, 10, 30, 28, 10, 10, 20, 10],
          code_cols=(1,))

    # Variables: legacy dictionary + the prototype variable(s) for each legacy variable
    by_leg = defaultdict(list)
    for x in xw:
        for lv in x['legacy_var'].split('|'):
            by_leg[lv].append(x)
    var_rows = []
    for r in master['Variables'][1:]:
        code = s(r[0]).strip()
        lv = code.split('.')[0]
        m = [x for x in by_leg.get(code, []) + (by_leg.get(lv, []) if lv != code else [])]
        same = lv in {v.split('.')[0] for v in mvars}
        mvp = ', '.join(dict.fromkeys(x['mvp_var'] for x in m)) or (lv if same else '')
        st = 'same code' if same and not m else (', '.join(dict.fromkeys(x['match_type'] for x in m)) or 'not in prototype')
        var_rows.append([code, s(r[1]), s(r[2]), s(r[3]), s(r[6]), s(r[7]), mvp, st])
    sheet(wb, 'Variables', 'Variable dictionary (position 3)',
          'Legacy Variables sheet (code, name, example output code, section, module, section name) with the prototype '
          'variable(s) for each legacy variable (from sheet Crosswalk). New variables go here before use (C4).',
          ['Code', 'Variable name', 'Current output code (legacy)', 'Section', 'Module', 'Section name', 'prototype variable(s)',
           'prototype status'], var_rows, [14, 50, 40, 8, 40, 22, 30, 24], code_cols=(1, 3),
          flag=lambda r: r[7] not in ('same code', 'not in prototype'))

    # Crosswalk
    cols = ['mvp_var', 'mvp_example', 'mvp_rows', 'legacy_var', 'legacy_example', 'legacy_rows', 'match_type',
            'variance', 'fix_code', 'review', 'evidence']
    sheet(wb, 'Crosswalk', 'Crosswalk: prototype codes that differ from legacy',
          'One row per prototype variable (or pattern) that computes a legacy quantity under a different code. Fix: the code '
          'the prototype should carry (C11: legacy variable name in the protocol structure); the legacy code is its alias. '
          'Review = yes: a person settles the row before its step (partial or unsure match, or no mechanical fix). Source: data/mvp_legacy_extracts/codes_crosswalk_v7_1.csv.',
          ['prototype variable', 'prototype example code', 'prototype rows', 'Legacy variable', 'Legacy example code', 'Legacy rows (456)',
           'Match', 'Difference', 'Fix: code for the prototype (protocol)', 'Review', 'Evidence'],
          [[x[c] for c in cols] for x in xw], [12, 30, 12, 14, 34, 14, 16, 30, 34, 8, 70], code_cols=(2, 5, 9),
          flag=lambda r: r[6] not in ('not_built',))

    # LiveOutputs vs MTOutputs
    mto = {stem(r['code']): r for r in leg_mto}
    xmap, xvar = {}, {}
    for x in xw:
        if x['mvp_example'] and x['fix_code']:
            xmap[stem(x['mvp_example'])] = x
            xvar.setdefault(var_token(x['mvp_example']), x)
    lrows = []
    for r in live:
        st = stem(r['code'])
        if st in mto:
            lrows.append([r['code'], r['desc'], mto[st]['code'], 'same as MTOutputs'])
        elif st in xmap:
            lrows.append([r['code'], r['desc'], xmap[st]['fix_code'], 'rename (Crosswalk)'])
        elif var_token(r['code']) in xvar:
            x = xvar[var_token(r['code'])]
            lrows.append([r['code'], r['desc'], x['fix_code'], f"rename by variable (Crosswalk: {x['legacy_var']})"])
        else:
            lrows.append([r['code'], r['desc'], '', 'no MTOutputs code (prototype output)'])
    sheet(wb, 'LiveOutputs', 'LiveOutputs (MTOutputs) codes against legacy MTOutputs',
          'LiveOutputs replicates legacy MTOutputs; C11b: where MTOutputs has the quantity, LiveOutputs carries the '
          'MTOutputs code. Legacy country (egy) and scenario numbers kept as they are.',
          ['prototype LiveOutputs code', 'Description', 'Legacy MTOutputs code', 'Status'], lrows, [40, 70, 40, 30],
          code_cols=(1, 3), flag=lambda r: r[3].startswith('rename'))

    # prototype-only variables and the protocol rules they break
    xvars = {x['mvp_var'] for x in xw}
    orows = []
    for v, rs in mvars.items():
        if v.split('.')[0] in lvars or v in xvars:
            continue
        issues = []
        codes = [r['code'] for r in rs]
        if any(re.search(r'[A-Z]', c) for c in codes):
            issues.append('C1 capitals (allowed if NameOfParameter)')
        if any('.all.' in '.' + stem(c) + '.' and r['sector'] == 'all' and r['fuel'] == 'all' for c, r in zip(codes, rs)):
            issues.append('C5 padding all.all')
        if any((r['fuel'] and r['fuel'] not in fuels | {'all'}) or (r['sector'] and r['sector'] not in sectors) for r in rs):
            issues.append('C6 member outside the vocabularies')
        if any(len(x) == 1 and not x.isdigit() for c in codes for x in stem(c).split('.')[2:-1]):
            issues.append('C7 single-letter token')
        orows.append([v, len(rs), codes[0], mvp_template(rs[0]), rs[0]['desc'], vd.get(v, {}).get('legacyref', ''),
                      '; '.join(issues)])
    sheet(wb, 'MVPOnly', 'prototype variables with no legacy code',
          'prototype variables whose quantity legacy does not code (or codes in a row without a code). They follow the '
          'protocol (C11d); the last column lists the rules each breaks today.',
          ['prototype variable', 'Rows', 'Example code', 'Template', 'Description', 'Legacy reference (prototype dictionary)',
           'Protocol issues'], orows, [14, 6, 34, 34, 60, 40, 50], code_cols=(3,), flag=lambda r: bool(r[6]))

    # Checks
    crow = [
        ['C10', 'Duplicated output codes, legacy Mitigation (456)', k['leg_dup'], ', '.join(k['leg_dup_list'][:40])],
        ['C10', 'Duplicated codes, prototype Mitigation (v7.1)', k['mvp_dup'], ', '.join(k['mvp_dup_list'])],
        ['C1', 'Legacy codes with capitals', k['leg_upper'], 'em.<pollutant>.All.<sector>'],
        ['C1', 'Legacy codes with an empty token or trailing full stop', k['leg_empty'], 'e.g. fix.pow.coa.t.'],
        ['C1', 'prototype codes with capitals (NameOfParameter pass-throughs)', k['mvp_upper'], 'allowed'],
        ['C3', 'Legacy codes with module air', k['leg_air'], 'legacy sheet says ap'],
        ['C5', 'Token all: legacy / prototype', f"{k['leg_all']} / {k['mvp_all']}", 'prototype pads left-out slots with all'],
        ['C5', 'Token tot: legacy / prototype', f"{k['leg_tot']} / {k['mvp_tot']}", 'prototype writes totals as all'],
        ['C6', 'Legacy codes with ele (electricity) instead of ecy', k['leg_ele'], ''],
        ['C6', 'prototype Mitigation rows with a member outside the vocabularies', k['mvp_offvocab'], 'sheet MVPOnly'],
        ['C7', 'prototype codes with a single-letter token before the end', k['mvp_single'], 'fpr.s, etsb.t, ndc.x.all.u'],
        ['C8', 'Legacy Mitigation codes without a scenario number', k['leg_noscen'], 'inputs and settings'],
        ['C4', 'prototype variables / with a legacy variable token / renamed legacy quantities',
         f"{k['mvp_vars']} / {k['mvp_common']} / {k['xw_renamed']}", 'sheet Crosswalk'],
    ]
    sheet(wb, 'Checks', 'Protocol checks', 'Counted by make_codes_map_v7_1.py on the 456 file and on v7.1.',
          ['Rule', 'Check', 'Count', 'Detail'], crow, [6, 60, 14, 120])
    for w in wb.worksheets:
        w.sheet_view.zoomScale = 85
    wb.save(OUT)
    return k


if __name__ == '__main__':
    k = build()
    sys.path.insert(0, os.path.join(HERE, '..', 'shared'))
    import excel_lint
    problems = excel_lint.lint(OUT)
    print(OUT)
    print('lint:', 'clean' if not problems else problems)
    print({a: b for a, b in k.items() if not a.endswith('_list')})
    sys.exit(1 if problems else 0)
