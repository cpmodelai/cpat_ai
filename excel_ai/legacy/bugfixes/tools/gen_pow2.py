"""Power-engineer plans for register bugs L52-L56, L67, L83, L84, L88, L95, L107-L111 (added 2026-10-19).
Every 'now' is the formula decoded from the .xlsb (dec.py) and checked against the LibreOffice text + recovered names
(h.py); every 'new' is an exact text substitution of it (brackets checked); every fill range is checked cell by cell
(same R1C1 pattern as the anchor). Output: partA_new.json (the 15 entries) and partA.json (merged with the 12 old)."""
import json, re, sys
from openpyxl.formula.translate import Translator
from openpyxl.utils import get_column_letter as L, column_index_from_string as ci
import dec, h

CELLS = {}
def xf(a, sh='Mitigation'):
    if sh not in CELLS: CELLS[sh] = dec.sheetcells(sh)
    return dec.formula(*CELLS[sh], a)

LOG = []
def cur(a, sh='Mitigation'):
    x = xf(a, sh)
    if x is None:
        v = h.cur(a, sh)
        assert v is not None, (sh, a)
        return v
    try: y = h.cur(a, sh)
    except AssertionError: y = None
    if y is not None: y = y.replace('FALSE()', 'FALSE').replace('TRUE()', 'TRUE')
    if x != y: LOG.append(f'{sh}!{a}: xlsb text differs from the LibreOffice text')
    return x

def bal(f):
    if not f.startswith('='): return f
    d = 0; q = False
    for ch in f:
        if ch == '"': q = not q
        if q: continue
        d += (ch == '(') - (ch == ')'); assert d >= 0, f
    assert d == 0, f
    return f

def sub(a, *pairs, sh='Mitigation'):
    f = cur(a, sh)
    for o, n in pairs:
        assert f.count(o) >= 1, (a, o, f); f = f.replace(o, n)
    return bal(f)

def rng_cells(r):
    a, b = r.split(':'); ca, ra = re.match(r'([A-Z]+)(\d+)', a).groups(); cb, rb = re.match(r'([A-Z]+)(\d+)', b).groups()
    return [f'{L(c)}{rr}' for rr in range(int(ra), int(rb) + 1) for c in range(ci(ca), ci(cb) + 1)]

def check_fill(anchor, rng, sh='Mitigation', multiline=False):
    """every cell of rng holds the anchor's formula in R1C1 terms (so a fill of the new formula is a pure edit)"""
    f0 = cur(anchor, sh)
    for c in rng_cells(rng):
        fc = cur(c, sh)
        if multiline:     # LET formulas: compare with the column letters of the year header and row numbers normalised
            n = lambda s, cell: re.sub(r'(?<![$A-Z])([A-Z]{1,2})\$201', '@$201', re.sub(r'\$B(\d+)', '$B#', s))
            assert n(fc, c) == n(f0, anchor), (c, fc[:80])
        else:
            t = Translator(f0, origin=anchor).translate_formula(c)
            assert t.replace(' ', '') == fc.replace(' ', ''), (sh, anchor, c, t, fc)

def pol(rng, off=6331):
    a, b = (rng.split(':') + [rng])[:2]
    ca, ra = re.match(r'([A-Z]+)(\d+)', a).groups(); cb, rb = re.match(r'([A-Z]+)(\d+)', b).groups()
    t = f'{ca}{int(ra) + off}' + (f':{cb}{int(rb) + off}' if b != a else '')
    return f'paste into {t} (+{off:,})'

def chk_pol(rng, off=6331):
    """the policy row holds the same formulas as the baseline row (shifted by off)"""
    for c in rng_cells(rng if ':' in rng else rng + ':' + rng):
        col, r = re.match(r'([A-Z]+)(\d+)', c).groups(); pc = f'{col}{int(r) + off}'
        f0, f1 = cur(c), cur(pc)
        if isinstance(f0, str) and f0.startswith('='): f0 = Translator(f0, origin=c).translate_formula(pc)
        assert f0.replace(' ', '') == (f1 or '').replace(' ', ''), (c, pc, f0, f1)

def fix(cell, new, fill, policy, now=None, sh='Mitigation', check=True):
    if check and ':' in fill.split(' ')[0] and sh == 'Mitigation' and now is None:
        check_fill(cell, fill.split(' ')[0])
    return dict(cell=cell if sh == 'Mitigation' else f'{sh}!{cell}', now=now if now is not None else cur(cell, sh),
                new=bal(new), fill=fill, policy=policy)

def pf(cell, new, fill, off=6331, **k):
    r = fill.split(' ')[0]; chk_pol(r, off)
    return fix(cell, new, fill, pol(r, off), **k)

B = []
def bug(id, pri, title, where, why, fixes, ref, effect, note=None, status='fix'):
    B.append(dict(id=id, pri=pri, title=title, where=where, why=why, fixes=fixes, ref=ref, effect=effect, note=note,
                  status=status))

SHARED = 'none (above the scenario blocks)'
# ---------------------------------------------------------------- High
bug('L53', 'High', 'Actual capacity factors are never used', 'Mitigation A4, rows 2999-3007 (N; Q and W follow)',
    'The installed-capacity lookup N2999 searches the year header Power!F357:Y357 (2000-2019) for FirstYearCalculations '
    '(2022, column AB), so it is #N/A in every row; Q (actual capacity factor) is then 0 and W always takes the studies '
    'value R, and the CFOverride bounds S:T never act.',
    [pf('N2999', sub('N2999', ('Power!$F$358:$Y$1635', 'Power!$F$358:$AC$1635'), ('Power!$F$357:$Y$357', 'Power!$F$357:$AC$357')),
        'N2999:N3007')],
    'Power tab rows 357-1635 (installed capacity by country and type, years 2000-2023 in F:AC). Q2999 = IFERROR(M2999/N2999,0) '
    'and W2999 = IF(AND(Q<T,Q>S),Q,R) then work as written.',
    'Egypt base year (prototype v4.10, same Power data): actual capacity factors gas 0.385 (studies 0.566), wind 0.436 (0.30), '
    'solar 0.347 (0.18), hydro 0.592 (0.432); oil stays at the studies 0.134 (actual 1.59 is above CFOverrideIfAbove). '
    'Base-year gas capacity (Y3000) 52.0 GW instead of 35.4 GW. Changes capacities, dispatch and investment in every year.')

# ---------------------------------------------------------------- Medium
p52 = []
for c in 'P':
    a = f'{c}2981'; f = cur(a); pc = f'Power!{"G"}$25:{"G"}$356'
    new = sub(a, (f'ISERROR(INDEX({pc},$K2981))', f'INDEX({pc},$K2981)>0'), (f'ISERROR(INDEX({pc},$L2981))', f'INDEX({pc},$L2981)>0'))
    p52.append(pf(a, new, 'P2981:T2985'))
p52[0]['fill'] = 'P2981:T2985 (25 cells, one pattern: copy P2981 and paste into P2981:T2985)'
bug('L52', 'Medium', 'Renewables take the world power parameters, never the country ones', 'Mitigation A2, rows 2981-2985 P:T',
    'Wind, solar, hydro, other renewables and biomass test IF(ISERROR(country), country, IF(ISERROR(world), world, ...)): '
    'the branches are inverted, so a valid country value is never taken and the world value (column M) always is. The '
    'four other types (rows 2977-2980) use IF(country>0, country, IF(world>0, world, ...)).',
    p52,
    'Rows 2977-2980, columns N:T of the same table (country value where > 0, else world). K2981:K2985 already fall back to '
    'the world row when the country has no row.',
    'Egypt: only solar has a country row (Power row 230): fixed O&M (Q2982) 11.831 instead of 15 $/kW/y; the studies WACC '
    '(S2982) 0.13 instead of 0.075, used only by the WACC source that takes the studies values (Egypt: Tech, so no '
    'effect); efficiency, '
    'variable O&M and lifetime are blank or 0 in the country row and stay at the world values.',
    note='P2981:T2985 are single-cell array formulas in the file (entered with Ctrl+Shift+Enter). Each INDEX returns one '
         'value, so the new formula can be entered normally or as an array formula; the result is the same.')
bug('L54', 'Medium', 'Hydro investment always starts in the first year', 'Mitigation L3, row 4067 H',
    'H4067 = IF($L$3827>50%, FirstYearCalculations, NewInvHydYear): L3827 is the year header of table I5 (2022), so the '
    'test is always true and hydro may invest from the base year instead of from NewInvHydYear.',
    [fix('H4067', sub('H4067', ('$L$3827', '$M3005/SUM($M2999:$M3007)')), 'H4067 (single cell)', pol('H4067'))],
    'The intended test is the base-year hydro share of generation (row 3846, L3846 = 6.7% for Egypt). The new formula '
    'takes it from table A4 (base-year power output, MWy), which equals L3846 and is data only, so no circularity; '
    'relative rows let the paste into the policy block read its own copy (rows 9330-9338).',
    'Egypt (hydro share 6.7% < 50%): hydro may invest only from NewInvHydYear = 2030. The legacy run invests in hydro in '
    '2022-2029 (row 4257, new effective investment: 677 MWavg in total in the baseline, 1,015 MWavg in the carbon-tax '
    'run, policy row 10588); this goes to the other permitted types.')
chk_pol('H4067')
bug('L67', 'Medium', "Capacity bought for this year's demand, although it comes online next year", 'Mitigation K7, rows 4022-4031',
    'New capacity bought in a year produces from the next year, but the need (row 4028 = MAX(row 4027 - row 4026, 0)) uses '
    'row 4027 "Next Year Demand" = L3752, this year\'s required generation; row 4031 "Actual effective generation in next '
    'year (should be the same)" shows the gap. The system enters every year one year of demand growth short.',
    [pf('L4027', sub('L4027', ('L3752', 'M3752')), 'L4027:AE4027')],
    'Row label of 4027. Next year\'s demand depends only on this year\'s prices (rows 3688-3689 read the previous column), so '
    'there is no circularity. AE4027 then reads AF3752, which already = AE3752 (2041: this year\'s demand, as in the prototype).',
    'Egypt (legacy inputs, prototype v4.14): capacity +3% by 2030, gas generation -3%, wind and solar generation +4%.')
bug('L83', 'Medium', 'Electricity producer subsidy compounds the factor and lags a year', 'Mitigation G1/G2, rows 3592, 3601, 3630',
    'From 2025 (column O) the projection is last year\'s value x last year\'s phase-out factor (O3601 = N3601 * N2213), so '
    'the factors multiply year on year and act a year late; row 3630 uses the base value $J3630 but last year\'s factor.',
    [pf('O3601', sub('O3601', ('N3601 * N2213', '$J3601 * O2213')), 'O3601:AE3601'),
     pf('O3630', sub('O3630', ('*  N2213', '*  O2213')), 'O3630:AE3630'),
     pf('O3592', sub('O3592', ('N3592 * N2213', '$N3592 * O2213')), 'O3592:AE3592')],
    'Row 2213 = share of the original producer subsidy kept in the year. J3601 and J3630 hold the last historical value '
    '(2024, column N); row 3592 has no J cell, so its base is $N3592.',
    'None in the shipped Egypt runs (row 2213 = 1 in every year of both blocks). With a producer-subsidy phase-out (e.g. '
    'to 0 over 5 years) the legacy subsidy falls as the product of the factors and a year late; after the fix it follows '
    'the factor of the year (Egypt base: residential -0.097, industrial -0.021 $/kWh).')
bug('L88', 'Medium', 'Regulations never reach power', 'Mitigation D6, rows 3398-3400',
    'The power shadow price per kWh reads only the feebate/ETS shadow price of power fuels (rows 2354, 2357, 2366). The '
    'regulation shadow price (general carbon price x EF when the policy is shadow pricing, D2369 = 1) is added for '
    'the fuel rows in 2377-2388 but never for power, although the energy efficiency regulation scenario covers power '
    '(F2403 = 1).',
    [pf('L3398', sub('L3398', ('L2354', '(L2354+$F2403*IF($D2369,L2375*$I2354,0))')), 'L3398:AE3398'),
     pf('L3399', sub('L3399', ('L2357', '(L2357+$F2403*IF($D2369,L2375*$I2357,0))')), 'L3399:AE3399'),
     pf('L3400', sub('L3400', ('L2366', '(L2366+$F2403*IF($D2369,L2375*$I2366,0))')), 'L3400:AE3400')],
    'Rows 2377 and 2380 (coal and gas power: IF($D$2369, L$2375 x EF, 0) + row 2354/2357). Row 2403 F = 1 when the '
    'shadow-pricing scenario covers power. I2354, I2357, I2366 = EF of coal, gas and oil in power.',
    'None in the shipped Egypt runs (explicit carbon tax, D2369 = 0). In a regulation scenario covering power, dispatch '
    'and investment see the shadow carbon price (the carbon-tax path) x EF. To measure: run "Energy efficiency '
    'regulations" before and after and compare rows 3412-3420 and the generation mix (rows 3828-3836).',
    note='Not via rows 2377/2380: their policy copies (8708-8719) keep the absolute references $D$2369 and L$2375, so in '
         'the policy block their regulation term reads the baseline general carbon price (L2375, 0 in the file); the '
         'new formulas use relative rows so the policy paste reads rows 8700, 8706 and 8734. The prototype also '
         'multiplies by the scenario\'s efficiency adjustment (0.7, Mitigation F86:F89); legacy\'s share C2371 is 0 '
         '(see L87), so it is left out here as in rows 2377-2388.')
r108 = [(7897, 3148, 6308, 'Wind'), (7898, 3149, 6309, 'Solar'), (7899, 3150, 6310, 'Hydro'), (7900, 3151, 6311, 'Other renewables')]
f108 = []
for r, s, g, lab in r108:
    new = sub(f'L{r}', ('(L2743+L2745)', f'L{s}'), (f'L{r - 7897 + 6308 if r < 7900 else 6312}*', f'L{g}*'))
    f108.append(fix(f'L{r}', new, f'L{r}:AE{r}',
                    f'type =L{s + 6331}*L{g + 6317}*_conv_ktoe_to_gwh/1000 into L{r + 6317}, fill L{r + 6317}:AE{r + 6317}'))
f108.append(fix('L7901', '=L3152*L6312*_conv_ktoe_to_gwh/1000', 'L7901:AE7901 (empty today)',
                'type =L9483*L12629*_conv_ktoe_to_gwh/1000 into L14218, fill L14218:AE14218', now='(empty)', check=False))
f108.append(fix('D7901', 'Biomass', 'D7901 (label; also E7901 = copy of E7900)', 'D14218 = Biomass, E14218 = copy of E14217',
                now='(empty)', check=False))
f108.append(fix('L7903', sub('L7903', ('L7897:L7900', 'L7897:L7901')), 'L7903:AE7903', pol('L7903:AE7903', 6317)))
for r, *_ in r108 + [(7903,)]:
    check_fill(f'L{r}', f'L{r}:AE{r}')
bug('L108', 'Medium', 'Cost of renewable subsidies counts the base subsidy twice, ignores the hydro switch and omits biomass',
    'Mitigation revenue block, rows 7897-7903 (policy 14214-14220)',
    'Rows 7897-7900 = (row 2743 + row 2745) x generation, but row 2745 already = row 2743 minus the additional subsidy, so '
    'the base subsidy enters twice; hydro (7899) ignores RenewableSubsidyHydro; the "Other renewables" row 7900 reads '
    'biomass generation (row 6312, not 6311); biomass has no row. Row 7903 enters total revenue (row 8023).',
    f108,
    'Table A17 (rows 3148-3152 = new subsidy per kWh by type, hydro only if RenewableSubsidyHydro = "Yes"), the same rows '
    'the engineer revenue memo 3665-3669 uses; generation by type rows 6308-6312.',
    'None in the shipped Egypt runs (no renewable subsidy: E2734 = E2735 = 0). With a subsidy, the cost falls by the '
    'double-counted base part and changes by the hydro switch and biomass.',
    note='Policy block: do not paste. Rows 14214-14220 sit at +6,317 but read the power rows at +6,331 (L14214 = '
         '(L9074+L9076)*L12625*...), so a paste of the baseline row would point 14 rows off; type the policy formulas '
         'given. The elasticity-model memo rows 2947-2951 (shown by 7890-7894 only when the elasticity model is chosen) '
         'carry the same (L2743+L2745); change them the same way if that memo is used.')

# ---------------------------------------------------------------- Low
k55 = fix('K2977', sub('K2977', ('MATCH(G2977,Power!$A$25:$A$356,0)', 'MATCH(G2977,Power!$A$112:$A$294,0)+87')),
          'K2977:K2985', pol('K2977:K2985'))
chk_pol('K2977:K2985')
bug('L55', 'Low', 'China, Japan and Korea take regional power data', 'Mitigation A2, rows 2977-2985 K',
    'K2977 = IFERROR(MATCH(<iso>.mpp.<type>, Power!A25:A356, 0), world row). The regional block (Power rows 42-109) comes '
    'first and its codes chn.mpp.*, jpn.mpp.*, kor.mpp.* equal the country codes of China, Japan and Korea, so their '
    'regional rows are found instead of the country rows (Power rows 112-294).',
    [k55],
    'Power tab: country block A112:A294 (header row 111); +87 converts the position in that block to the position in '
    'A25:A356 that the INDEX formulas in N:T use. The world fallback L2977 is unchanged.',
    'None for Egypt (no regional row with its code). China, Japan, Korea: the country parameters replace the regional ones.')
d202 = cur('D202', 'CoC')
fb = [(f',${c}$172)', ',NA())') for c in 'HFDGIJ']
new202 = sub('D202', *fb, sh='CoC')
check_fill('D202', 'D202:M390', sh='CoC', multiline=True)
for c in rng_cells('D202:M390'):
    t = cur(c, 'CoC'); assert all(t.count(o) == 1 for o, _ in fb), c
bug('L56', 'Low', "Countries without CoC risk data get Sri Lanka's WACC parameters", 'CoC rows 202-390 D:M (N:V copy M)',
    'The real-WACC calculator (a LET formula) looks up each country\'s beta, equity risk premium, default spread, tax, '
    'equity weight and liquidity margin in rows 41-197 with XLOOKUP(..., if_not_found = $X$172), and row 172 is Sri '
    'Lanka. 47 countries of rows 202-390 have no row there (e.g. Afghanistan, Algeria, Iran, Myanmar, Nepal, Yemen, '
    'Zimbabwe) and silently get Sri Lanka\'s parameters (17.8% real WACC in 2022).',
    [fix('D202', new202, 'CoC!D202:M390 (one pattern; easiest with Find and Replace limited to CoC!D202:M390: each ",$X$172)" '
         'by ",NA())" for X = H, F, D, G, I, J)', 'none (CoC sheet, one copy)', sh='CoC', check=False)],
    'Mitigation I2988:I2996 and AB2988:AB2996 already read CoC!D202:D390 inside IFERROR(..., 0.075), the default used for '
    'countries missing from CoC; with #N/A in the row they take it.',
    'None for Egypt (own row, 9.9% in 2022). The 47 countries take the 7.5% default (plus the technology premium with '
    'WACCSource = Tech) instead of Sri Lanka\'s 17.8%.',
    note='The cell text spans several lines (Alt+Enter). The #N/A of a country without data is itself the flag; the prototype '
         'also flags it on its Inputs sheet (PsCoCData).')
bug('L84', 'Low', 'Electricity consumer subsidy phased with the price-control factor; option text mismatch',
    'Mitigation G1/G2, rows 3606, 3635; MTInputs C138',
    'With PowerSubsidyExemptInclude = "Include" the electricity consumer subsidy is multiplied by row 2216 (price-control '
    'phase-out factor) instead of row 2214 (consumer-subsidy phase-out factor). The unit text of MTInputs C138 says '
    '"Exempt/Include*" while the options (Dashboard L54) are "DoNotPhaseOut*" and "Include".',
    [pf('O3606', sub('O3606', ('*O2216', '*O2214')), 'O3606:AE3606'),
     pf('O3635', sub('O3635', ('*O2216', '*O2214')), 'O3635:AE3635'),
     fix('C138', 'DoNotPhaseOut*/Include', 'MTInputs!C138 (label)', 'none (MTInputs)', sh='MTInputs', check=False)],
    'Row 2214 (consumer factor, from YearConsSubPha and FFPhaseOut) as for the fuel consumer subsidies.',
    'None in the shipped Egypt runs (DoNotPhaseOut*, and J3606 = J3635 = 0: no consumer subsidy on electricity).')
eff = []
for r, rng in [(3691, 'M3691:AE3691'), (3697, 'M3697:AE3697'), (3703, 'M3703:AE3703'), (3709, 'M3709:AE3709'),
               (2823, 'P2823:AE2823'), (2827, 'M2827:AE2827'), (2828, 'M2828:AE2828'), (2834, 'M2834:AE2834'),
               (2836, 'M2836:AE2836')]:
    a = rng.split(':')[0]
    eff.append(pf(a, sub(a, ('$M3719', '$M2198')), rng))
eff.append(fix('L3719', '(clear L3719:M3719)', 'L3719:M3719', 'clear L10050:M10050', now="Additional Efficiency "
               "Improvements - Power demand | M3719: " + cur('M3719'), check=False))
bug('L95', 'Low', 'Power demand: efficiency increment sits on the net-exports row', 'Mitigation H2, row 3719 L:M',
    'Row 3719 carries two things: net-export data (D3719 = "Net Exports (Imports negative)", F:J) and, in the side table '
    '"Other Parameters", the power-demand efficiency increment (L3719 label, M3719 = M2198 = MTInputs F242). Nine demand '
    'rows of the engineer (H1) and elasticity (2823-2836) power models read it as $M3719, so the row reads as a trade term.',
    eff,
    'Row 2198 (table K2197:M2201, "Power" increment) already holds the value; rows 2199-2201 serve road, residential and '
    'industry the same way.',
    'None on values (the reference moves to the cell M3719 copies; F242 = 0 by default).',
    note='L2 changes the same cells M3691, M3697, M3703, M3709 ($F3677 -> $F3676); the two substitutions are independent, '
         'apply them in either order. Clearing L3719:M3719 is optional (cosmetic) once nothing reads M3719.')
e2736 = fix('E2736', '=RenSubsidyAddStartYear', 'E2736 (single cell)', 'paste into E9067 (+6,331)')
chk_pol('E2736')
bug('L107', 'Low', 'Renewable subsidy: start year of the additional subsidy reuses the consumer-subsidy phase-out year',
    'Mitigation E2736 (policy E9067), row 270; MTInputs (new row)',
    'E2736 "Year to add additional RE subsidy" = row 270 of the scenario = MTInputs F132 (YearConsSubPha), the year the '
    'consumer fuel subsidies start to be phased out; the additional renewable subsidy (MTInputs 355) has no start year '
    'of its own, and the label of row 276 says it starts in CPIntro.',
    [e2736,
     fix('D276', sub('D276', ('&CPIntro', '&RenSubsidyAddStartYear')), 'D276 (single cell, label)', SHARED)],
    'MTInputs rows 354-357 (renewable subsidy inputs) and the layout of each MTInputs row (D = scenario value, E = '
    'Dashboard, F = value used, G = default, H = name).',
    'None in the shipped runs (additional subsidy 0; the default start year 2027 equals today\'s YearConsSubPha). After '
    'the fix the two policies can be timed apart.',
    note='Do first (otherwise E2736 shows #NAME?): append MTInputs row 416 after the last input row (415), copying row '
         '356: B416 "New renewable energy subsidy, start year", C416 "year", D416 =INDEX($N416:$XAA416,1,_ScenarioToRun), '
         'E416 =Dashboard!$R$6 (a free cell next to the renewable-subsidy inputs P6:Q6; type 2027 there), F416 '
         '=IF(MTAct,D416,IF(CPATDefaultsOrUserDefined="Default",IF(I416="Y",E416,G416),E416)), G416 2027, H416 '
         'RenSubsidyAddStartYear, I416 "Y"; give scenario columns N416:XAA416 the values of N132:XAA132 where set; define '
         'the name RenSubsidyAddStartYear = MTInputs!$F$416 (workbook scope). Appending (not inserting) keeps every '
         'existing MTInputs row number. The prototype has the same input (MTInputs row 482, default 2027).',
    status='needs input row')
i109 = fix('I3042', sub('I3042', ('),0)', '),IFERROR(MATCH(SUBSTITUTE(E3042,"ctf.","ctf.old"),Power!$A$25:$A$356,0),'
                                   'MATCH("wld.ctf.med."&B3042,Power!$A$25:$A$356,0)))')), 'I3042:I3046', pol('I3042:I3046'))
chk_pol('I3042:I3046')
bug('L109', 'Low', 'Capex decline options Low and Vhigh have no wind and solar series', 'Mitigation A7, rows 3042-3046 I',
    'RenewableCostDeclineRate Low builds the codes wld.ctf.low.wnd / .sol and Vhigh wld.ctf.vhg.wnd / .sol / .ore, which '
    'the Power tab (rows 303-330) does not hold (it has oldlow / oldvhg for wind and solar, and med.ore twice, rows 316 '
    'and 318). I3042 = IFERROR(MATCH(...),0) then gives 0 and INDEX(Power!F25:BE597, 0, year) in L3042:AE3046 errors.',
    [i109],
    'Power rows 323-330 (wld.ctf.oldlow/oldvhg.sol/wnd) and 316 (wld.ctf.med.ore). The prototype uses the same fallback '
    '(Inputs_ppath tcf|<type>|<option>): the older series of the same option for wind and solar, else Medium.',
    'None for Egypt (Medium*). With Low or Vhigh, the capex time factors of wind, solar (and other renewables under '
    'Vhigh) become the older series (Medium for other renewables) instead of errors.',
    note='The fallback is a choice: the user is to confirm it (the alternative is to add the missing series to the Power '
         'tab). Power row 318 is a second wld.ctf.med.ore, probably meant to be wld.ctf.vhg.ore.')
bug('L110', 'Low', 'Power revenue rebate counts VAT that was never collected', 'Mitigation G4, row 3663 (feeds 7888, 7749)',
    'The rebate per kWh (rows 3615, 3644) = rebate switch x carbon cost x pass-through x (1 + VAT), and row 3663 '
    'multiplies it by consumption into fiscal revenue (7888, then 7749 in the carbon-tax revenue). The VAT part of the '
    'carbon cost passed through is never collected (the VAT revenue row 3659 counts only the VAT on the price before '
    'policy), so the rebate returns VAT the government never had.',
    [pf('L3663', sub('L3663', ('L3615*L3621', 'L3615/(1+L3611)*L3621'), ('L3644*L3650', 'L3644/(1+L3640)*L3650')),
        'L3663:AE3663')],
    'Rows 3611 and 3640 (VAT rates). The price rows 3614-3617 are unchanged: users still see the carbon cost and its VAT '
    'removed; only the fiscal rebate excludes the VAT.',
    'None in the shipped Egypt runs (rebate off, J3595 = 0). With PowerRebates on, the rebate revenue falls by the VAT '
    'share: residential x 1/1.149 (VAT 14.9%), industrial unchanged (VAT 0).')
bug('L111', 'Low', 'Manual electricity excise revenue counts the whole excise, also where the price does not include it',
    'Mitigation G4, row 3660 (feeds 7885, 7762)',
    'Row 3660 = manual excise (rows 3602, 3631) x consumption in every year. The price includes the excise only through '
    'the change of the sum of components since the last historical year (2024, column N) times the pass-through (rows '
    '3607 and 3610), and not at all up to 2024, where the price is data.',
    [pf('L3660', sub('L3660', ('=(L3602*L3621+L3631*L3650)/1000',
                                '=IF(L3594>$I3600,((L3602-$N3602)*L3621+(L3631-$N3631)*L3650)*L3596/1000,0)')),
        'L3660:AE3660')],
    'Row 3594 (year), I3600 (last historical year, 2024), N3602 / N3631 (excise in 2024), row 3596 (pass-through, the '
    'same for both groups).',
    'None in the shipped Egypt runs (AdditionalExcise off, D199 = 0). With a manual excise, the revenue memo (and row '
    '7762, the excise revenue by fuel) counts only the excise in the price: 0 up to 2024, then pass-through x the change '
    'since 2024.')

order = ['L53', 'L52', 'L54', 'L67', 'L83', 'L88', 'L108', 'L55', 'L56', 'L84', 'L95', 'L107', 'L109', 'L110', 'L111']
B.sort(key=lambda b: order.index(b['id']))
json.dump(B, open('partA_new.json', 'w'), indent=1, ensure_ascii=False)
old = json.load(open('/home/user/CPAT-AI/legacy_bugfix_plans/data/fixes_power_engineer.json'))
old = [b for b in old if b['id'] not in order]          # rerun on the merged file: keep L1-L12 only
pri = {'High': 0, 'Medium': 1, 'Low': 2}
allb = old + B
seq = {b['id']: i for i, b in enumerate(allb)}
allb.sort(key=lambda b: (pri[b['pri']], seq[b['id']]))
json.dump(allb, open('partA.json', 'w'), indent=1, ensure_ascii=False)
print(len(B), 'new bugs,', sum(len(b['fixes']) for b in B), 'cell rows;', len(allb), 'total,', sum(len(b['fixes']) for b in allb))
print('\n'.join(sorted(set(LOG))))
