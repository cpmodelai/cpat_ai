# Group C: cell-level fix plans for legacy bugs L68-L73, L75-L77, L85, L86 (register v5.4); legacy file CPAT 1.0pre_456_NoPropData
import json,sys,os,re
D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D); sys.path.insert(0,os.path.dirname(D))
from qC import fm            # Mitigation, rows 1-17400 (rows > 15000 read from l456.xlsx)
from q import fx as fxs      # other sheets
def fx(a):
    if '!' in a:
        s,c=a.split('!'); return fxs(s,c)
    return fm(a)
def bal(f):
    d=0
    for ch in f:
        d+=(ch in '({')-(ch in ')}'); assert d>=0,f
    assert d==0,f; return f
def sub(a,*pairs):
    f=fx(a); assert isinstance(f,str),(a,f)
    for o,n in pairs:
        assert o in f,(a,o,f); f=f.replace(o,n)
    return bal(f)
def fix(cell,new,fill,policy,now=None):
    if now is None:
        now=fx(cell); now='' if now is None else now
    return dict(cell=cell,now=now,new=bal(new),fill=fill,policy=policy)
def pol(rng,off=6317):
    return 'paste into '+re.sub(r'(\d+)',lambda m:str(int(m.group(1))+off),rng)+f' (+{off:,})'
def spell(pc,*pairs,fill=None):
    """policy formula spelled out from the policy cell's own text (references cross the 6070 boundary)"""
    f=sub(pc,*pairs); r=re.match(r'([A-Z]+)(\d+)',pc)
    return f'type {pc}: {f}'+(f' and fill {fill}' if fill else '')
def full(cell):  # assert the row runs to AE
    c,r=re.match(r'([A-Z]+)(\d+)',cell).groups(); assert fx(f'AE{r}') not in (None,''),cell
A=[]
def bug(id,pri,title,where,why,fixes,ref,effect,note=None,status='fix'):
    A.append(dict(id=id,pri=pri,title=title,where=where,why=why,fixes=fixes,ref=ref,effect=effect,note=note,status=status))

# ---------- L68
assert fx('K8070') is None and fx('K8057')==0 and fx('L8057')=='=K8057+1'
bug('L68','Medium','GDP effects: the multiplier of lag 1 acts in the impulse year','Mitigation row 8070 (lag counter of cohort 1; later cohorts copy it: M8081 = L8070, N8092 = M8081, ...), policy row 14387',
 'The cohort blocks (rows 8069-8244) read the multiplier at the lag in row 8070 (MATCH(L8070,$K8057:$AE8057,0); row 8057 = lag 0, 1, 2, ... of Multipliers D:G). L8070 = K8070+1 = 1, so each cohort gets the lag-1 multiplier in its own (impulse) year, although lag 0 (Multipliers column D, 0 in every table) is the impulse year; the GDP effect runs one year early.',
 [fix('L8070',sub('L8070',('=K8070+1','=0')),'single cell (M8070:AE8070 = previous + 1 and the later cohorts\' lag rows, e.g. M8081 = L8070, follow)',pol('L8070'))],
 'Row 8057 (lags 0-20) = Multipliers row 61; lag 0 = Multipliers column D (0 in the global, income-group and country tables, e.g. D92:D99).',
 'The GDP effect of every impulse comes one year later (lag 0 in the impulse year). MVP v4.15 (lag 0 in the impulse year, multiplier 0).',
 note='Rows 8280-8287 / 14597-14604 (which turn the cohort sums 8267-8274 into the GDP-effect rows) are IFNA(0) in this NoPropData file (LD58), so the result can only be checked once they are restored. L69 (row 8071) reads the same lag row.')

# ---------- L69
full('L8071')
bug('L69','Low','GDP effects: the first cohort\'s excise drag is lost','Mitigation row 8071 (policy 14388)',
 'L8071 (excise, cohort 1) matches the lag L$8127, an empty cell of the cohort-6 block, instead of the cohort\'s own lag row L8070 like rows 8072-8078; the policy copy L14388 also reads L$8127. The MATCH fails, so the first cohort\'s excise revenue use has no GDP effect.',
 [fix('L8071',sub('L8071',('MATCH(L$8127,','MATCH(L8070,')),'L8071:AE8071',pol('L8071:AE8071')+': gives MATCH(L14387, ...) as in L14389')],
 'Rows 8072-8078 (e.g. L8072: MATCH(L8070,$K8057:$AE8057,0)); policy L14389.',
 'The first year\'s revenue gets its contractionary excise effect (Egypt about 3e-5 of GDP). MVP: every cohort counts its revenue use (share -1).',
 note='MATCH on the empty L$8127 returns #N/A in every column, so row 8267 (EXC total) may be #N/A, not only cohort 1: to confirm on recalculation (rows 8280+ are IFNA(0) in this file).')

# ---------- L70
full('L7761')
bug('L70','Low','Revenue: industry gas excise uses the coal rate and coal use','Mitigation row 7761 (policy 14078)',
 'Additional excise revenue of gas in industry: L7761 = L2512 (coal industry new excise) x L6442 (gas industry use); M7761:AE7761 = coal rate x M6436 (coal industry use).',
 [fix('L7761',sub('L7761',('L2512','L2581')),'L7761:AE7761 (M:AE now read row 6436, coal)',
      spell('L14078',('L8843','L8912'),fill='L14078:AE14078 (rate rows +6,331, use rows +6,317; a pasted copy would point at row 8898)'))],
 'Row 2581 = "nga ind - in which: new excise tax" ($/GJ, code mit.ntx.ind.nga); row 6442 = natural gas, industry (ktoe); policy 8912 and 12759.',
 'Gas industry excise revenue right wherever coal and gas excises (or uses) differ; none for Egypt (no new excise). MVP: rex per subsector and fuel (v4.15).')

# ---------- L71
L71=[]
for r,pr in ((7805,14122),(7819,14136),(7873,14190)):
    full(f'L{r}')
    L71.append(fix(f'L{r}',sub(f'L{r}',('/_conv_ktoe_to_gj/10^9','*_conv_ktoe_to_gj/10^9')),f'L{r}:AE{r}',
                   spell(f'L{pr}',('/_conv_ktoe_to_gj/10^9','*_conv_ktoe_to_gj/10^9'),fill=f'L{pr}:AE{pr} (or Find/Replace on the row)')))
bug('L71','Low','Revenue: biomass taxes, subsidies and VAT divided by the unit conversion','Mitigation rows 7805, 7819, 7873 (policy 14122, 14136, 14190)',
 'Biomass existing taxes (7805), consumer subsidies (7819) and VAT (7873) = use (ktoe) x rate ($/GJ) / _conv_ktoe_to_gj (41,868 GJ/ktoe) / 10^9, so about 0; the coal and gas rows (7798, 7812) multiply.',
 L71,'Rows 7798 and 7812 (coal): ... *_conv_ktoe_to_gj/10^9; _conv_ktoe_to_gj = Mitigation E1035.',
 'Biomass taxes, subsidies and VAT are no longer 0 (they enter rev.exi, csu.exi and total revenue via rows 7807, 7821, 7875, 8008). MVP: use x PJ/ktoe x rate for every fuel.')

# ---------- L72
full('L7671'); full('M7756')
bug('L72','Low','Revenue: next-year references','Mitigation rows 7671 (policy 13988), 7756 (policy 14073)',
 'LPG price-control revenue L7671 uses the price change M$738-K$738 (next year minus last year) where the other fuels (7666-7672) use L$73x-K$73x. Coal power new excise M7756:AE7756 = N2466 (next year\'s rate) x M6433 (L7756 is right).',
 [fix('L7671',sub('L7671',('(M$738-K$738)','(L$738-K$738)')),'L7671:AE7671',
      spell('L13988',('(M$738-K$738)','(L$738-K$738)'),fill='L13988:AE13988')),
  fix('M7756',sub('M7756',('=N2466','=M2466')),'M7756:AE7756 (= copy L7756 right)',
      spell('M14073',('=N8797','=M8797'),fill='M14073:AE14073 (= copy L14073 right)'))],
 'Row 7670 (diesel: L$736-K$736) and L7756 / L14073 (=L2466 / =L8797).',
 'Revenue of the year uses the year\'s rate and price change. None for Egypt\'s default run where these rates are 0 or flat. MVP: the year\'s own column.',
 note='K7756 (=O2466/_conv_ktoe_to_gj) and K14073 are stray cells with no role; leave or clear.')

# ---------- L73
full('L7691'); full('L7718')
bug('L73','Low','Revenue: wrong coverage shares','Mitigation rows 7691 (policy 14008), 7718 (policy 14035)',
 'Gas industry coverage L7691 divides by L6041 (energy-balance gas total of industry) where the other fuels divide by their row-64xx industry total (e.g. 7703 / L6448); kerosene power coverage L7718 = L2270 (power) x L2273 (domestic shipping) where the other fuels use fuel x power (e.g. 7712 = L2264*L2270).',
 [fix('L7691',sub('L7691',('IF(L6041=0','IF(L6442=0'),('/L6041)','/L6442)')),'L7691:AE7691',
      spell('L14008',('IF(L12358=0','IF(L12759=0'),('/L12358)','/L12759)'),fill='L14008:AE14008')),
  fix('L7718',sub('L7718',('=L2270*L2273','=L2265*L2270')),'L7718:AE7718',
      spell('L14035',('=L8601*L8604','=L8596*L8601'),fill='L14035:AE14035'))],
 'Row 2265 = kerosene coverage (fuel), row 2270 = power (sector); row 6442 = natural gas, industry; rows 7712 and 7703 as patterns.',
 'Kerosene power coverage (info row, feeds the kerosene average 7717) right; the gas industry change is cosmetic (row 6442 = L6041 in every column, so no value change). MVP: coverage by subsector and fuel.',
 note='Row 7691 does not reproduce as a value error in this file (6442 = 6041); the edit only aligns it with the other fuels.')

# ---------- L75
code=lambda k,s: f'LOWER(_Country_code)&".mit.{k}."&{s}'
def idx(k,s): return f'INDEX(L$2173:L$14770,MATCH({code(k,s)},$H$2173:$H$14770,0),0)'
assert fx('G17160') is None and 'MATCH($G17160' in fx('J17160')
n17163=f'={idx("csu.exi.usd","$E$16792")}-{idx("csu.exi.usd","1")}'
n17160=f'={idx("rev.exi.usd","$E$16792")}-{idx("rev.exi.usd","1")}-L17163'
for k in ('rev.exi.usd','csu.exi.usd','sub.new.usd','rev.new.elec.usd','rev.new.lpk.usd'):
    assert any(isinstance(fx(f'H{r}'),str) and f'.mit.{k}."' in fx(f'H{r}') for r in range(7740,7830)),k
bug('L75','Low','Revenue reports: hard-coded row and mixed totals','Mitigation rows 17160-17164, 17190, 17201',
 'In this file the excise report (17160-17163) has no hard-coded 759: J = MATCH($G...) on an empty column G, and the codes in H (mit.rev.blt/ct/rta/sr.pct) exist nowhere in the calculation block, so the rows are #N/A. In the revenue-by-fuel report, electricity (L17190 = L17216, L17201 = L17227) is the total electricity revenue (rev.tot.ecy) while the other fuel rows read the new-policy revenue (rev.new.<fuel>).',
 [fix('L17160',n17160,'L17160:AE17160','none (report block)'),
  fix('G17161','='+code('sub.new.usd','C17161'),'single cell (J17161 and L17161:AE17161 then match it)','none (report block)'),
  fix('L17162','=0','L17162:AE17162 (not modelled)','none (report block)'),
  fix('L17163',n17163,'L17163:AE17163','none (report block)'),
  fix('G17190','='+code('rev.new.elec.usd','C17190'),'single cell; then type H17190 =G17190 and J17190 =MATCH($G17190,$H$2173:$H$14770,0) as in row 17189','none (report block)'),
  fix('L17190','=INDEX(L$2173:L$14770,$J17190,0)','L17190:AE17190 (as L17189)','none (report block)'),
  fix('G17201',sub('G17200',('rev.new.lpk.usd','rev.new.elec.usd'),('C17200','C17201')),'copy G17200:AE17200 to G17201:AE17201, then edit G17201 as shown','none (report block)'),
  fix('L17201',sub('L17200',('$C17200','$C17201'),('$J17200','$J17201')).strip('{}'),'L17201:AE17201 (comes with the copy of row 17200)','none (report block)')],
 'Codes in the calculation block: rev.exi.usd (row 7807 / 14124), csu.exi.usd (7821 / 14138), sub.new.usd (7750 / 14067), rev.new.elec.usd (7749 / 14066); $E$16792 = ScenarioNum, 1 = baseline as in C17152.',
 'The excise report shows the change in existing taxes (net of the subsidy change), the new-policy revenue and the subsidy saving instead of #N/A; revenue by fuel takes electricity\'s new-policy revenue like the other fuels. MVP: 12d and 12e read the revenue rows.',
 note='To confirm: the split of 17160-17163 is ours (the MVP has no such report): 17160 = change in rev.exi minus change in consumer subsidies, 17161 = new-policy revenue (sub.new), 17162 = 0 (tax evasion not modelled), 17163 = change in consumer subsidies (csu.exi). Totals 17164 = SUM unchanged.')

# ---------- L76
M='Multipliers!'
L76=[fix(M+'D19',sub(M+'D19',('C210:C408)','C210:C408,0)')),'single cell','none (sheet Multipliers)'),
     fix(M+'D20',sub(M+'D20',('IF(C20="Estimated",4,4)','IF(C20="Estimated",4,2)')),'single cell','none (sheet Multipliers)'),
     fix(M+'D21',sub(M+'D21',('IF(D20=4,6,','IF(AND(D20=4,ISNUMBER(D19)),6,')),'single cell','none (sheet Multipliers)'),
     fix(M+'D40',sub(M+'D40',('INDEX(D$412:D$610,$D$19)','CHOOSE($E$21,D94,D105,D117,D128,D139)')),'single cell (array formula: Ctrl+Shift+Enter)','none (sheet Multipliers)'),
     fix(M+'E40',sub(M+'E40',('INDEX(E$1624:E$1822,$D$19)','CHOOSE($E$21,E94,E105,E117,E128,E139)')),'E40:O40 (array formulas, one cell at a time, or copy E40 right; P40:S40 = O40 stay)','none (sheet Multipliers)'),
     fix(M+'D45',sub(M+'D45',('INDEX(D$1018:D$1216,$D$19)','CHOOSE($E$21,D99,D110,D122,D133,D144)')),'D45:O45 (array formulas, copy D45 right)','none (sheet Multipliers)')]
for c in 'FGHIJKLMNO':
    assert f'INDEX({c}$1624:{c}$1822,$D$19)' in fx(f'{M}{c}40') and f'INDEX({c}$1018:{c}$1216,$D$19)' in fx(f'{M}{c}45')
bug('L76','Low','Multipliers: empty CIT table, WAGE on the GNFS table, approximate country match, default to Estimated','Multipliers rows 19-21, 40, 45 (tables 412-610, 1018-1216, 1624-1822)',
 'With MultipliersSource = Estimated (D21 = 6), CIT lag 0 reads the labour-tax table (D$412:D$610) and lags 1+ the empty rows 1624-1822 (so 0); WAGE (row 45) reads the public-consumption (GNFS) table 1018-1216; D19 = MATCH(C19,C210:C408) is approximate, so a code missing from the sorted list takes its neighbour; D20 maps any unknown text to 4 (Estimated).',
 L76,'Income-group tables: CIT rows 94 (global), 105 (HIC), 117 (UMIC), 128 (LMIC), 139 (LIC); WAGE rows 99, 110, 122, 133, 144; E21 = 1 (global) or the income group 2-5, as used by the "Plus adjustment" rows 50-57.',
 'Estimated multipliers: CIT and WAGE take the income-group values, a country missing from the estimated tables falls back to its income group, unknown text means the income group. None for Egypt by default (MultipliersSource = Income-grp*). MVP v4.15.',
 note='Seen while checking, not in the register: TRNS row 44 column D reads D$1218:D$1418 (title rows; E:O read $1220:$1418), so lag 0 of TRNS is off by two rows (lag 0 is 0 in every table, so no value effect).')

# ---------- L77
L77=[fix('E16317',sub('E16317',('$L$16313','$L$16309')),'single cell','none (report block)')]
for i,r in enumerate(range(16398,16406)):
    s=16345+i; full(f'L{r}')
    L77.append(fix(f'L{r}',f'=L{s}/$L{s}*100',f'L{r}:AE{r}','none (report block)'))
L77.append(fix('B16387',sub('B16387',('("&FirstYearCalculations&"=100)','(baseline = 100)')),'single cell (label of rows 16389-16396)','none (report block)'))
bug('L77','Medium','Average prices: index rows point at the wrong rows, gas test on the policy total','Mitigation rows 16317, 16387, 16398-16405',
 'Rows 16398-16405 ("indexed vs. FirstYearCalculations", labels electricity, coal, gas, oil, gasoline, diesel, LPG, kerosene) read rows 16331-16338 (electricity industry, electricity residential, coal industry, gas industry, coal residential, ...). E16317 ("natural gas absent in baseline") tests L16313, the policy gas total, where E16316 tests the baseline coal total. B16387 labels rows 16389-16396 "(2022=100)" although they are 100 + % change against the baseline.',
 L77,'Rows 16345-16352: scenario average price by fuel (electricity, coal, gas, oil, gasoline, diesel, LPG, kerosene), weighted by consumption; L16309 = baseline gas in the three sectors.',
 'The reported price indices are of the right fuels; the gas-absent switch follows the baseline. MVP v4.15 (pav.leg, pav.lidx per fuel against scenario 1).',
 note='C16395 and C16404 are a hard-coded 2 (the other rows =$E$16792); labels only.')

# ---------- L85
full('L7820')
bug('L85','Low','Electricity consumer subsidy info row subtracts industry','Mitigation row 7820 (policy 14137)',
 'L7820 = -(MIN(0, L6330*L3606) - MIN(0, L6331*L3635))/1000: the industry part (6331 x 3635) is subtracted instead of added.',
 [fix('L7820',sub('L7820',(')-MIN(0, L6331',')+MIN(0, L6331')),'L7820:AE7820',
      spell('L14137',(')-MIN(0, L12648',')+MIN(0, L12648'),fill='L14137:AE14137'))],
 'Row 7806 (existing electricity taxes): L6330*(...) + L6331*(...), both groups added.',
 'Reported electricity consumer subsidies (csu.exi, row 7821) right. MVP: not applicable (info row; rgap sums both groups).')

# ---------- L86
bug('L86','Low','No manual override for the electricity producer subsidy','Mitigation I828 (F828, K828:AE828); Manual inputs row 146; names _manual_codes, _manual_prices',
 'I828 = MATCH("mit.pros.ecy.all", _manual_codes, 0) is #N/A: the manual row exists (Manual inputs G146, USD bln) but _manual_codes = G59:G133 and _manual_prices = G59:N133 stop above the electricity block (rows 135-146), so F828 stays "CPAT" and a manual value is ignored.',
 [fix('Name _manual_codes','Manual inputs!$G$59:$G$146','both definitions (workbook level and the sheet-level copy, sheet 17), Name Manager','none',now="Manual inputs!G59:G133"),
  fix('Name _manual_prices','Manual inputs!$G$59:$N$146','both definitions, Name Manager','none',now="Manual inputs!G59:N133")],
 'Manual inputs G146 = mit.pros.ecy.all (Electricity, Producer-side subsidy, USD bln), same layout as G125 (mit.pros.bio.all); I828 and K828 need no edit.',
 'A manual electricity producer subsidy is used when EnergyPricesManualSwitch = Yes. MVP: not built (manual inputs to come).',
 note='To confirm: the extension also brings the manual electricity prices (Manual inputs 136-144: mit.sp/vatrate/txo/rp.ecy.res/ind, read by Mitigation rows 789-791 and others) into the lookup, which are also ignored today.',status='struct')

json.dump(A,open(os.path.join(D,'part_C.json'),'w'),indent=1)
for b in A: print(b['id'],len(b['fixes']),b['status'])
