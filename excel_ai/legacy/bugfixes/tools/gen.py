import pickle,json,re
F=pickle.load(open('f.pkl','rb'))
from openpyxl.utils import column_index_from_string as ci
def cur(a):
    c,r=re.match(r'([A-Z]+)(\d+)',a).groups(); v=F[int(r)][ci(c)-1]
    return v if isinstance(v,str) else repr(v)
def bal(f):
    d=0
    for ch in f:
        d+= (ch=='(')-(ch==')'); assert d>=0,f
    assert d==0,f; return f
def sub(a,*pairs):
    f=cur(a)
    for o,n in pairs:
        assert f.count(o)>=1,(a,o,f); f=f.replace(o,n)
    return bal(f)
def fix(cell,new,fill,policy,now=None):
    return dict(cell=cell,now=now if now is not None else cur(cell),new=bal(new),fill=fill,policy=policy)
B=[]
def bug(id,pri,title,where,why,fixes,ref,effect,note=None,status='fix'):
    B.append(dict(id=id,pri=pri,title=title,where=where,why=why,fixes=fixes,ref=ref,effect=effect,note=note,status=status))
P=6331
# ---------- High
key='MATCH(LOWER(_Country_code)&".lp",UNPop!$B$7:$B$243,0)'
un=lambda col:f'INDEX(UNPop!$E$7:$AJ$243,{key},MATCH({col}$415,UNPop!$E$6:$AJ$6,0))'
bug('L13','High','Other oil products: hardcoded pass-through 1 and margin 0','Mitigation price-parameter table, row 759 (oop.all)',
 'Row 759 holds typed constants: raw price-control coefficient M759 = 1 and margin O759 = 0, while every other oil product (rows 755-758) reads both from the IMF price dataset.',
 [fix('M759','=IFERROR(AVERAGE(INDEX(_prices_main,MATCH(_Country_code & FirstYearCalculations,_prices_country_years,0),MATCH(M$745 & "." & $G759,_prices_codes,0))),1)','single cell','none (above the scenario blocks)'),
  fix('O759','=IFERROR(AVERAGE(INDEX(_prices_main,MATCH(_Country_code & FirstYearCalculations, _prices_country_years,0),MATCH(O$745 & "." & $G759,_prices_codes,0))),0)','single cell','none (above the scenario blocks)')],
 'M758 and O758 (kerosene), the same formulas with $G758. IFERROR keeps the old constant if the dataset has no oop entry.',
 'Egypt: pass-through 0 and margin about 7.95 $/bbl from the dataset (as the prototype). The other-oil-products retail price no longer falls with the oil price to the floor, and the tenfold rise in their fuel use by 2030 goes away.')
bug('L20','High','Population growth path','Mitigation row 428 (feeds 429, 481, 2428, 6210 and the policy block)',
 'From 2026 the population row carries 2% a year, then 3% (2030) and 4% (2031 on, by repeating the last growth): Egypt 185.2 million in 2041. The legacy sheet UNPop (UN WPP 2024) gives 147.0 million.',
 [fix('P428','=O428*'+un('P')+'/'+un('O'),'P428:AE428 (2026-2041); K428:O428 stay as data','none (above the scenario blocks)')],
 'Sheet UNPop, row egy.lp (UN World Population Prospects 2024), already in legacy. Growth is chained on the 2025 WEO level so there is no break in 2026.',
 'Egypt population 2040: 178.1 to 132.4 million; 2041: 185.2 to 134.0 million. Rows 429, 481 and 2428 follow automatically, so agriculture, waste and per-capita GDP drivers fall after 2026.')
bug('L24','High','GDP effect added to GDP growth every year','Mitigation rows 2443 and 2446',
 'Post-policy growth = g + e (row 2446 = SUM(2444:2445)), so a steady GDP level effect e adds e to growth every year and compounds; row 2443 then chains on the pre-policy level.',
 [fix('L2446','=(1+L2444)*(1+L2445)/(1+K2445)-1','L2446:AE2446','paste into L8777:AE8777 (+6,331)'),
  fix('L2443','=L2442*(1+L2445)','L2443:AE2443','paste into L8774:AE8774 (+6,331)')],
 'Row 2445 is already the level effect lagged one year (= previous year of row 8288); the fix uses it as a level, as the label of 2443 ("GDP post-policy") says.',
 'No change on the NoPropData file (row 8288 is stripped to 0). With a steady effect of 0.5%, GDP is +0.5% instead of about +10% after 20 years.')
bug('L18','High','Non-energy methane never changes','Mitigation rows 6172-6227',
 'Not reproduced in this file. Livestock, rice and waste production grow with income and population (rows 6212-6214), emissions apply (1 - abatement share) (rows 6217, 6220, 6226), and the reported inventory rows read them from 2024 (7572 = 7308, 7582 = 7309). Cached Egypt values: agriculture CH4 15.8 (2022) to 28.9 Mt CO2e (2040), waste 35.1 to 59.1.',
 [], 'n/a','None.', note='No cell to change for L18. Mark the register entry as "not reproduced in CPAT 1.0pre_456". A related defect that does exist is listed as N1 below.', status='none')
bug('L19','High','Flaring CO2 counted as methane','Mitigation rows 6156, 7561, 7608',
 'Row 6156 adds the flaring CO2 (row 6155) divided by the CH4 GWP ($I$1030) to the oil-and-gas CH4 row, so CO2 is reported as methane.',
 [fix('L6156','=L6154','L6156:AE6156','paste into L12473:AE12473 (+6,317)'),
  fix('L7561','=L6602+L6155','L7561:AE7561 (energy CO2 in the inventory table)','paste into L13878:AE13878 (+6,317)'),
  fix('L7608','=L6587+L7452*$B7562+L6155','L7608:AE7608 (power sector GHGs, where legacy books oil and gas extraction CH4, row 7223)','paste into L13925:AE13925 (+6,317)')],
 'Row 6155 is already in Mt CO2 (44/16 x flared CH4). Adding it to both 7561 and 7608 keeps legacy\'s own check in B7640 ("OK" when the by-sector and by-gas totals agree).',
 'None in the baseline (row 6155 = 0). With a methane fee on oil and gas, CH4 falls by the flared amount and CO2 rises by 44/16 of it; fee revenue (row 6157) is charged on methane only.')
# ---------- Medium
bug('L15','Medium','ETS: hardcoded relative price 1.1','Mitigation D1843',
 'Not reproduced in this file. D1843 = (1+E1811*$E$1812)/(1+D1813*$E$1812) reads the volatility (0.42), impact (0.5) and policy-risk (0.2) inputs; 1.1 is the result, not a constant.',
 [], 'n/a','None.', note='No cell to change. Mark the register entry as "not reproduced"; the prototype volatility adjustment (1/1.1) equals legacy.', status='none')
bug('L16','Medium','ETS quick estimate linear in the semi-elasticity','Mitigation row 1868',
 'The quick price estimate divides the reduction by the semi-elasticity. In the NoPropData file L1868:AE1868 hold stored zeros (formula stripped); in a full file they hold the linear quotient.',
 [fix('L1868','=IF(L1867=0,0,LN(1+L1860)/L1867)','L1868:AE1868','none (above the scenario blocks)')],
 'Row 1867 is the adjusted semi-elasticity (dlnE per $/t); row 1860 is the reduction left for the ETS as a share. Legacy\'s own note on rows 1875-1885 says "arguably exp/ln".',
 'Only the starting price of the ETS goal seek changes (closer to the solution for large cuts); converged results do not change.')
bug('L21','Medium','Waste abated with the livestock curve','Mitigation row 6206',
 'Waste reduction = M6182 (livestock share) although the waste curve inputs (rows 6200-6204) are computed.',
 [fix('L6206','=MAX(0,MIN(1,$L6202*L6204^$M6202))','L6206:AE6206','paste into L12523:AE12523 (+6,317)')],
 'Rows 6182 (livestock) and 6194 (rice): = MAX(0, MIN(1, $L curve x fee ^ $M curve)).',
 'None in the baseline (no methane fee). With a fee, waste CH4 follows its own abatement curve.')
bug('L22','Medium','Navigation missing from the local pollutant totals','Mitigation pollutant blocks (sections 13-14)',
 'Each pollutant block has transport rows rod gso/die/lpg/ker/nga, ral die and avi jfu, but no navigation row, so navigation never enters the transport, "Other" or total rows. This cannot be fixed by editing an existing cell.',
 [], 'The "ral die" row of the same block (e.g. 6822 for SO2) for the formula; navigation fuel use is rows 5508-5515.',
 'Adds navigation emissions (Egypt navigation: about 291 ktoe of other oil products in 2022).',
 note='Steps, in the 8 pollutant blocks (PM2.5 6604, NOx 6706, SO2 6808, VOC 6910, BC 7012, OC 7114, CH4 7216, CO 7323) of the baseline and of the policy block (+6,317): (1) select the "avi jfu" row (6619, 6721, 6823, 6925, 7027, 7129, 7232, 7338) and insert one row above it, so the transport SUM ranges and the totals expand by themselves; (2) in the new row type B = "nav", C = "oop" and copy the year formula of the "ral die" row directly above; (3) add the new cell to the "Other" (oth) air-pollution row of the block (6700, 6802, 6904, 7006, 7108, 7210, 7419; CH4: no such row). Do all baseline blocks first, then the policy blocks, and check that BaselineFirstRow/PolicyScenarioFirstRow moved with them. In the NoPropData file every emission row holds 0 (GAINS factors stripped), so check the copied formula in the full file.', status='struct')
avi=[]
for r,fu in [(5483,'coa'),(5484,'nga'),(5485,'gso'),(5486,'die'),(5487,'oil'),(5488,'oil'),(5489,'oil'),(5490,'bio'),(5492,'jfu')]:
    pairs=[('((1+M2439)^(','((1+M2446)^('),('*(1+M2446)*','*(1+M2439)*')]
    if r in (5483,5484): pairs.append((')*(1+M2439)\x00',''))
    f=cur(f'M{r}')
    f=f.replace('((1+M2439)^(','((1+M2446)^(',1); assert '((1+M2446)^(' in f
    assert '*(1+M2446)*' in f; f=f.replace('*(1+M2446)*','*(1+M2439)*',1)
    if r in (5483,5484):
        assert f.endswith(')*(1+M2439)'); f=f[:-len('*(1+M2439)')]
    if r==5492: assert '_el_inc_die_rod' in f; f=f.replace('_el_inc_die_rod','_el_inc_oil_rod')
    avi.append(fix(f'M{r}',f,f'M{r}:AE{r}',f'paste into M{r+P}:AE{r+P} (+6,331)'))
bug('L42','Medium','Domestic aviation: GDP growth and shock swapped','Mitigation rows 5483-5490, 5492 (5491: see L47)',
 'Aviation rows raise the shock (1+M2439) to eps_Y x income factor and multiply by (1+M2446) with elasticity 1; coal and gas multiply by (1+M2439) a second time; jet fuel uses the diesel income elasticity _el_inc_die_rod.',
 avi,'Standard row 5399 (road diesel): L x (1+M2446)^(eps_Y x M2433) x (1+M2439) x price terms. Jet fuel takes the oil income elasticity, as its other elasticities (_el_dem_oil_rod, _el_eff_oil_rod) already do.',
 'Egypt jet fuel (707 ktoe in 2022) x0.90 in 2023, x0.82 in 2030, x0.68 in 2040 against legacy (the shock now enters in full and GDP with eps_Y x income factor). Other aviation fuels are 0 for Egypt.')
oen=[]
for r in range(6077,6086):
    f=cur(f'M{r}'); assert 'M2440)' in f; f=f.replace('M2440)','M2433)')
    if r<6085:
        assert f.count('_ind))^')==1; f=f.replace('_ind))^','_ind+$M2201))^')
    oen.append(fix(f'M{r}',f,f'M{r}:AE{r}',f'policy row {r+6317}: same edit with M8764 for M2433 and $M8532 for $M2201 (do not paste: this block is +6,317 but its drivers are +6,331)'))
bug('L43','Medium','Other energy use: no GDP growth','Mitigation rows 6077-6085 (policy 12394-12402)',
 'The income-factor reference is M2440, a blank row, so (1+g)^(eps_Y x 0) = 1: other energy use never grows with GDP. Rows 6077-6084 also lack the additional-efficiency term $M2201 that row 6085 and all industry rows have.',
 oen,'Industry row 5691 (mining & chemicals coal): (1+M2446)^(eps_Y x M2433) and /(1+_eff_imp_... + $M2201). Quickest: select M6077:AE6085, Ctrl+H, replace "2440)" with "2433)"; then select M6077:AE6084 and replace "_ind))^" with "_ind+$M2201))^". Policy: select M12394:AE12402, replace "8771)" with "8764)"; then M12394:AE12401, replace "_ind))^" with "_ind+$M8532))^".',
 'Egypt other energy use (mostly other oil products, 101 ktoe in 2022): about +46 ktoe in 2030 and +124 ktoe in 2040.')
cs=[]
for r in [2461,2484,2507,2530,2553,2576,2599,2622,2645,2668,2691,2714]:
    f=cur(f'O{r}')
    m=re.search(r'\(\$J(\d+) - O(\d+) \+ \$J(\d+)\) \* \(1 - \$J(\d+)\)',f); assert m,f
    old=m.group(0); new=f'($J{m.group(3)} + ($J{m.group(1)} - O{m.group(2)}) * (1 - $J{m.group(4)}))'
    assert f.count(old)==2; f=f.replace(old,new)
    cs.append(fix(f'O{r}',f,f'O{r}:AE{r}',f'paste into O{r+P}:AE{r+P} (+6,331)'))
bug('L14','Medium','Pass-through applied twice in the first projected year','Mitigation floating subsidy/tax rows (code cs), 12 fuel blocks',
 'The base value $J (= the 2024 value) already carries (1 - pass-through) from the history formula (columns K:N); the projection multiplies (2024 price - price + $J) by (1 - pass-through) again, so the floating subsidy jumps in the first projected year when pass-through is between 0 and 1.',
 cs,'History formula of the same rows (K:N): (excise - other parts) x (1 - $J pass-through), applied once.',
 'None for Egypt (bucketed pass-through 0 or 1). With pass-through 0.5 or 0.8 (Manual price controls, other countries), no jump in 2025.')
# ---------- Low
tot=[]
for r,res in [(6704,6622),(6806,6724),(6908,6826),(7010,6928),(7112,7030),(7214,7132),(7423,7341)]:
    f=sub(f'L{r}',(f'L{res}:L{res+5}',f'L{res}:L{res+21}'))
    tot.append(fix(f'L{r}',f,f'L{r}:AE{r}',f'paste into L{r+6317}:AE{r+6317} (+6,317)'))
bug('L23','Low','Services and food & forestry missing from the pollutant totals','Mitigation total row of each pollutant: 6704, 6806, 6908, 7010, 7112, 7214, 7423',
 'Each total sums residential (6 rows) but skips the 16 services and food & forestry rows directly below them.',
 tot,'The buildings subtotal of the same block (e.g. 6889 = SUM(6826:6847) for SO2) and the CH4 total 7321, which already include them.',
 'None for Egypt (services and food & forestry emit 0 in the file); correct totals wherever they emit.')
bug('L44','Low','Residential other oil products priced at the biomass price','Mitigation row 5559',
 'The price terms read row 5549 (biomass) instead of 5548 (other oil products).',
 [fix('M5559',sub('M5559',('M5549','M5548'),('L5549','L5548')),'M5559:AE5559','paste into M11890:AE11890 (+6,331)')],
 'Row 5555 (residential gasoline) reads its own price row 5544.','None for Egypt (residential other oil products = 0).')
bug('L45','Low','Residential leakage to biomass inconsistent','Mitigation rows 5554-5593',
 '(a) The not-exempt rows subtract the (negative) fossil change, so they rise, and the totals add the changes back cumulatively: fossil use is not reduced. (b) Kerosene uses the LPG price base (L5546 in 5587) and the LPG share (M5582 in 5588), and has two "Change in kerosene" rows. (c) The fossil change is multiplied by the fossil efficiency and the biomass gain by the biomass efficiency again, so energy is not conserved.',
 [fix('M5564',sub('M5564',('-M5577','+M5577')),'M5564:AE5564','paste +6,331'),
  fix('M5565',sub('M5565',('-M5583','+M5583')),'M5565:AE5565','paste +6,331'),
  fix('M5566',sub('M5566',('-M5588','+M5588')),'M5566:AE5566','paste +6,331'),
  fix('M5554','=M5564+M5568','M5554:AE5554','paste +6,331'),
  fix('M5557','=M5565+M5569','M5557:AE5557','paste +6,331'),
  fix('M5558','=M5566+M5570','M5558:AE5558','paste +6,331'),
  fix('M5577','=-L5564*M5576*$E$1785','M5577:AE5577','paste +6,331'),
  fix('M5583','=-L5565*M5582*$E$1785','M5583:AE5583','paste +6,331'),
  fix('M5587','=1+(M5586-L5586)/L5547','M5587:AE5587','paste +6,331'),
  fix('M5588','=-L5566*M5589*$E$1785','M5588:AE5588','paste +6,331'),
  fix('M5590','=M5588','M5590:AE5590','paste +6,331'),
  fix('M5593','=-(M5578+M5584+M5591)','M5593:AE5593','paste +6,331')],
 'Labels of the block: "Change in X" is a change in fuel; "Equivalent Biomass" (rows 5578, 5584, 5591, already = change x fossil efficiency / biomass efficiency) is the biomass that replaces it. Biomass total 5560 keeps its cumulative SUM; the fossil rows carry the reduction forward themselves.',
 'None while BiomassLeakage = No (E1785 = 0, Egypt). With leakage on, fossil cooking fuel falls and biomass rises by the same useful energy.')
bug('L46','Low','Road other biofuels: wrong price and terms','Mitigation rows 5392 and 5406',
 'Row 5406 uses the bioethanol price (5390) because the other-biofuels price row 5392 is empty, puts the shadow price through eps_U, has an efficiency term (M5390/M5390)^eps_F that is always 1, and uses $M2259 (coal exemption phase-out) as additional efficiency.',
 [fix('L5392','=(L2720)+L2721*L2271','L5392:AE5392 (empty today)','paste into L11723:AE11723 (+6,331)',now='(empty)'),
  fix('M5406','=L5406*((1+M2446)^(_el_inc_oil_rod*M2433))*(1+M2439)*((M5392/L5392)^_el_dem_oil_rod)*((((M5392+M2388*M2404)/(L5392+L2388*L2404))^(_el_eff_oil_rod))/(1+_eff_imp_oil_rod+$M2199))^(1+_el_dem_oil_rod)','M5406:AE5406','paste into M11737:AE11737 (+6,331)')],
 'Row 5389 (road biomass price: = (M2720)+M2721*M2271) for the price; standard row 5399 for the form, with the biomass shadow price row 2388 and road additional efficiency $M2199. The elasticity names are those legacy already uses in 5406.',
 'None for Egypt (no road other biofuels).')
bug('L47','Low','Self-generated renewables in aviation and navigation take the shock from wrong rows','Mitigation rows 5491, 5516',
 'Row 5491 multiplies by (1+M2512) (coal industry new excise) and row 5516 by (1+M2473) (blank row) instead of the shock row 2439. Row 5491 also has the aviation swap of L42.',
 [fix('M5491',sub('M5491',('((1+M2439)^(','((1+M2446)^('),('*(1+M2512)*','*(1+M2439)*')),'M5491:AE5491','paste into M11822:AE11822 (+6,331)'),
  fix('M5516',sub('M5516',('*(1+M2473)*','*(1+M2439)*')),'M5516:AE5516','paste into M11847:AE11847 (+6,331)')],
 'Row 5407 (road self-generated renewables).','None for Egypt (no self-generated renewables in these sectors).')
ex=[]
for r,tot_,fu in [(5568,5554,'nga'),(5569,5557,'oil'),(5570,5558,'oil')]:
    ex.append(fix(f'L{r}',f'=L{tot_}*IF($L$1784=$B{r},$K$1795,0)',f'single cell L{r}',f'paste into L{r+P} (+6,331)'))
for r,tot_,init in [(5564,5554,5568),(5565,5557,5569),(5566,5558,5570)]:
    ex.append(fix(f'L{r}',f'=L{tot_}-L{init}',f'single cell L{r}',f'paste into L{r+P} (+6,331)'))
for r,fu in [(5568,'nga'),(5569,'oil'),(5570,'oil')]:
    ex.append(fix(f'M{r}',sub(f'M{r}',(f'((1+M2446)^_el_inc_{fu}_res)',f'((1+M2446)^(_el_inc_{fu}_res*M2433))')),f'M{r}:AE{r}',f'paste +6,331'))
for r in (5546,5547):
    ex.append(fix(f'L{r}',sub(f'L{r}',('IF(AlwaysExemptResLPGKer="Yes"','IF(LEFT(AlwaysExemptResLPGKer,3)="Yes"')),f'L{r}:AE{r}',f'paste into L{r+P}:AE{r+P} (+6,331)'))
bug('L48','Low','Residential initially-exempt rows are dead code','Mitigation rows 5546-5547, 5564-5570',
 'The initially-exempt rows start from a hard 0 (L5568:L5570 = IFNA(0)), so the exemption split never happens; they also lack the income factor M2433; and the AlwaysExemptResLPGKer test compares with "Yes" while the input list uses "Yes*"/"No*".',
 ex,'The exempt share is legacy\'s own row 1795 ("Exempted ... proportion", most-used cooking fuel L1784). Income factor as in the not-exempt rows 5564-5566.',
 'None for Egypt (exemption off: K1795 = 0, MTInputs F268 = "No*").')
# ---------- new findings
bug('N1','Low (new)','Methane intensity decline of agriculture and waste computed but not applied','Mitigation rows 6217, 6220, 6226',
 'Rows 6173, 6185, 6197 ("CH4 emissions factor, baseline") fall by Manual inputs J187 (0.47%/y, agriculture) and J188 (0.5%/y, waste) but no emission row uses them.',
 [fix('N6217','= $M6217 * N6212 / $M6212 * N6173 / $M6173 * (1-N6182)','N6217:AE6217','paste into N12534:AE12534 (+6,317)'),
  fix('N6220','= $M6220 * N6213 / $M6213 * N6185 / $M6185 * (1-N6194)','N6220:AE6220','paste into N12537:AE12537 (+6,317)'),
  fix('N6226','= $M6226 * N6214 / $M6214 * N6197 / $M6197 * (1-N6206)','N6226:AE6226','paste into N12543:AE12543 (+6,317)')],
 'Labels of rows 6173/6185/6197 and Manual inputs C187/C188 ("Reduction in intensity due to autonomous technological improvement").',
 'Egypt 2040: agriculture CH4 about -7.7%, waste about -8.2%.',note='Not in the register; found while checking L18. Confirm it is intended before applying.')
bug('N2','Low (new)','Other oil products: new ETS left out of the new-policy total, VAT factor on a blank row','Mitigation row 2698',
 'Row 2698 = (2694+2696) x (1 + VAT x M2703): the new ETS (2695) is missing, unlike every other fuel (e.g. kerosene 2675 = 2671+2672+2673), and M2703 is a blank row (the oop block has no "portion used for residential" row), so VAT on the new policy is dropped.',
 [fix('K2698','=(K2694+K2695+K2696)*(1+K2686)','K2698:AE2698','paste into K9029:AE9029 (+6,331)')],
 'Row 2675 (kerosene) and 2721 (biomass). The oop VAT payment row 2687 applies VAT in full, so (1 + K2686) is consistent.',
 'None in the baseline; under a new ETS covering other oil products their price now carries the permit price.',note='Not in the register; confirm before applying.')
json.dump(B,open('doc/partB.json','w'),indent=1)
print(len(B),'bugs',sum(len(b['fixes']) for b in B),'cells')
# ---- fix L42 effect wording
for b in B:
    if b['id']=='L42': b['effect']='Egypt jet fuel (707 ktoe in 2022): the 2023-2024 shock now enters in full (-20.8%, +9.2%) and GDP growth with eps_Y x income factor; the repo survey (Sector_Equations_Survey) puts the standard form at x0.90 (2023), x0.82 (2030) and x0.68 (2040) of legacy. Other aviation fuels are 0 for Egypt.'
def prow(f):
    if f['policy'] in ('paste +6,331','paste +6,317'):
        off=int(f['policy'][-5:].replace(',',''))
        c=re.match(r'([A-Z]+)(\d+)',f['cell']); rng=f['fill'].split(' ')[0]
        if ':' in rng:
            a,bb=rng.split(':'); ca,ra=re.match(r'([A-Z]+)(\d+)',a).groups(); cb,rb=re.match(r'([A-Z]+)(\d+)',bb).groups()
            f['policy']=f'paste into {ca}{int(ra)+off}:{cb}{int(rb)+off} (+{off:,})'
for b in B:
    for f in b['fixes']: prow(f)
json.dump(B,open('doc/partB.json','w'),indent=1)
A=[]; B=A
def pol(cell,fill): 
    a,bb=fill.split(':'); ca,ra=re.match(r'([A-Z]+)(\d+)',a).groups(); cb,rb=re.match(r'([A-Z]+)(\d+)',bb).groups()
    return f'paste into {ca}{int(ra)+P}:{cb}{int(rb)+P} (+6,331)'
def pf(cell,new,fill): return fix(cell,new,fill,pol(cell,fill))
bug('L1','High','Services electricity demand grows with the industrial multiple after 2023','Mitigation H3, row 3731',
 'M3731 (2023) uses the services multiple (row 3713); from N3731 the copied formula points six rows up, to the industrial multiple (row 3707).',
 [pf('N3731','=M3731*N3713','N3731:AE3731')],'M3731 (2023) = L3731*M3713. Already scripted: bugfix_procedure/FixL1_ServicesElectricity.bas.',
 '2040 services demand +29% (baseline) and +15% (carbon tax); total demand +7.7%. Excel test run of the macro: 2041 services +30.8% (baseline), +16.1% (policy).')
inc=[]
for r,c in [(3692,'F'),(3698,'G'),(3704,'H'),(3710,'I')]:
    inc.append(pf(f'M{r}',sub(f'M{r}',(f'((${c}3675/$M3686)*M3686*M2433)',f'(${c}3675*M2433)')),f'M{r}:AE{r}'))
bug('L3','High','Income factor on the GDP elasticity applied twice and anchored to 2023','Mitigation H1, rows 3692, 3698, 3704, 3710',
 'Exponent = (eps_Y / $M3686) x M3686 x M2433, and M3686 already = average elasticity x M2433, so the effective elasticity is eps_Y x inc(t)^2 / inc(2023).',
 inc,'Legacy fuel rows (e.g. 5399): (1+g)^(eps_Y x M2433), the income factor once. Row 3686 is then read by nothing; leave it as a memo row.',
 '2040 demand +3.2% (baseline) and +3.7% (carbon tax).')
aee=[]
for r,c in [(3691,'F'),(3697,'G'),(3703,'H'),(3709,'I')]:
    aee.append(pf(f'M{r}',sub(f'M{r}',(f'^(1+${c}3677)',f'^(1+${c}3676)')),f'M{r}:AE{r}'))
bug('L2','Medium','Autonomous efficiency gains use the price elasticity instead of the usage elasticity','Mitigation H1, rows 3691, 3697, 3703, 3709',
 'Efficiency multiple = 1/(1+alpha+add)^(1+eps_F) with eps_F = row 3677 ("Price Elasticity").',
 aee,'Documentation equation 3.4.2.3 and the fuel rows: exponent (1 + eps_U), eps_U = row 3676 ("Demand Elasticity").','2040 demand +0.9%.')
usd=[pf('L4276','=L3099*L4264/1000','L4276:AE4284')]
usd[0]['fill']='L4276:AE4276, then fill L4276:AE4276 down to row 4284 (rows 3099-3107 line up with 4264-4272)'
usd[0]['policy']='paste into L10607:AE10615 (+6,331)'
bug('L5','Medium','Investment spending uses the capital cost at time factor 1','Mitigation L20, rows 4276-4284',
 'New investment (USD m) = $O2977 (base capital cost of table A2) x nameplate MW, ignoring the capital-cost time factor.',
 usd,'Table A13 (rows 3099-3107 = capital cost x time factor), which the weighted-capex row 3181 already uses.',
 '2040 total (row 4285) -18% (baseline) and -23% (carbon tax). Reporting only.')
bug('L6','Medium','Investment logit normalised by the cheapest type, including types that may not be built','Mitigation L1/L4, rows 4045-4046',
 'The logit weight is EXP(-K x cost / cheapest cost), with the cheapest taken over all nine types, including types not permitted (L3, rows 4061-4069).',
 [pf('L4046','=IFERROR(AGGREGATE(15,6,L4035:L4043/(L4061:L4069=1),1),MIN(L4035:L4043))','L4046:AE4046'),
  pf('L4045','=MATCH(L4046,L4035:L4043,0)','L4045:AE4045')],
 'The permitted flags of table L3 (rows 4061-4069), already multiplied into rows 4073-4081. Change 4046 first, then 4045 (no circularity).',
 'No change in the baseline; carbon-tax run 2040 demand -0.07%, investment +0.3%.')
bug('L4','Low','Long-term storage cost allocation (33%) applied twice','Mitigation J1, row 3911',
 'Row 3911 multiplies by $E3876 (33%) and row 3912 multiplies by $E3876 again.',
 [pf('L3911','=L3909*L3906','L3911:AE3911')],'Example table on the same row, F3911:J3911 (= F3909*F3906); total row 3912 applies $E3876 once.',
 'None for Egypt (variable renewables below the long-term storage threshold).')
bug('L7','Low','Early coal retirement mixes nameplate and effective capacity','Mitigation K4, row 3973',
 'Row 3973 subtracts last year\'s non-coal retirement in nameplate MW (row 4004) from additions and demand growth in effective MW.',
 [pf('M3973','=SUM(L4012:L4019)','M3973:AE3973')],'Rows 4012-4019 (non-coal effective retirements, table K6). L3973 stays 0.','None for Egypt (no coal).')
bug('L8','Low','Effective coal retirement is not capped like the nameplate retirement','Mitigation K5/K6, row 4011',
 'Nameplate coal retirement (3994) is MIN(planned + early, capacity); the effective retirement (4011 = 4009 + 4010) is not capped.',
 [pf('L4011','=L3994*$W2999','L4011:AE4011')],'Rows 4012-4019 = nameplate x capacity factor. Rows 4009-4010 stay as memo rows.','None for Egypt.')
bug('L9','Low','Feebate rebate per kWh consumed added to the cost per kWh generated','Mitigation D6, row 3409',
 'Rebate = -(row 3408) = -(cost per kWh generated / consumption-generation ratio 0.82), i.e. x1.22, but it is added to costs per kWh generated (rows 3412-3420).',
 [pf('M3409','=-M3407','M3409:AE3409')],'Rows 3412-3420 add the rebate to a cost per kWh generated, so the rebate must be per kWh generated (row 3407). Row 3408 becomes a memo row.',
 'None unless a power feebate is set (then the over-rebate of 22% goes).')
bug('L10','Low','Capacity needed is computed from last year\'s plan, not from actual capacity','Mitigation K7, row 4024',
 'M4024 = L4030 (last year\'s planned capacity), whether or not the investment could be placed.',
 [pf('M4024','=M3753','M4024:AE4024')],'L4024 (base year) is actual effective capacity, SUMPRODUCT(capacity, capacity factor) = row 3753.',
 'None in the Egypt runs; matters only when scale-up limits leave a deficit.')
bug('L11','Low','Stray reference in dispatch','Mitigation I1, rows 3773, 3779',
 'Required generation = MAX(required - other, $G4291 x total); G4291 is an empty, unrelated cell of table L21.',
 [pf('L3773','=MAX(L3780-L3772,0)','L3773:AE3773'),pf('L3779','=MAX(L3780-L3778,0)','L3779:AE3779')],
 'Row meaning ("required generation", never negative).','None while G4291 is empty.')
bug('L12','Low','Total nameplate investment row is zero','Mitigation L19, row 4273',
 'The total multiplies by $X3008, an empty cell, instead of summing the types.',
 [pf('L4273','=SUM(L4264:L4272)','L4273:AE4273')],'Total rows 4285 and 4003 of the same section.','Row goes from 0 to the sum of the nine types. Nothing reads it.')
json.dump(A,open('doc/partA.json','w'),indent=1)
print('A',len(A),sum(len(b['fixes']) for b in A))
