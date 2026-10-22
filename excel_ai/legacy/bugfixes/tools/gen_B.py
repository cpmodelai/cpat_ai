# Group B: cell-level fix plans for legacy bugs L58 L59 L66 L81 L82 L87 L89 L90 L91 L92 L93 L94 (file CPAT 1.0pre_456_NoPropData.xlsb)
# 'now' = q.py text (LibreOffice xlsx) except where that text holds a mangled _xlfn.IFNA: then the formula decoded from the xlsb (parts/dec.py).
import json,sys,re,pickle
S='/tmp/claude-0/-home-user-CPAT-AI/8ecef15a-59be-528a-8fc5-3dd56f80a940/scratchpad/lg'
sys.path.insert(0,S); sys.path.insert(0,S+'/parts')
from q import fx as qfx
import dec
from openpyxl.utils import column_index_from_string as ci
ROWS=set(r-1 for r in list(range(1049,1665))+list(range(2255,2290))+list(range(2365,2420))+list(range(2440,2720))+list(range(5390,5600))+list(range(1780,1800))+[8702])
_cells,_shr=dec.raw_all('Mitigation',ROWS)
def dfx(a): return dec.getf(_cells,_shr,a)
def fx(a):
    q=qfx('Mitigation',a); d=dfx(a)
    if isinstance(q,str) and 'IFNA' in q: return d
    if isinstance(q,str) and d and q.replace(' ','')!=d.replace(' ',''): print('WARN differs',a,q,'|',d)
    return q if q is not None else ''
def bal(f):
    d=0
    for ch in f:
        d+=(ch in '({')-(ch in ')}'); assert d>=0,f
    assert d==0,f; return f
def sub(a,*pairs,base=None):
    f=base if base is not None else fx(a)
    for o,n in pairs:
        assert f.count(o)==1,(a,o,f); f=f.replace(o,n)
    return bal(f)
def fix(cell,new,fill,policy,now=None):
    return dict(cell=cell,now=now if now is not None else fx(cell),new=bal(new),fill=fill,policy=policy)
P=6331
def pol(rng,off=P):
    return 'paste into '+re.sub(r'(\d+)',lambda m:str(int(m.group(1))+off),rng)+f' (+{off:,})'
A=[]
def bug(id,pri,title,where,why,fixes,ref,effect,note=None,status='fix'):
    A.append(dict(id=id,pri=pri,title=title,where=where,why=why,fixes=fixes,ref=ref,effect=effect,note=note,status=status))
CONV=('The converted xlsx (q.py) shows these IFNA formulas mangled (e.g. "=_xlfn.IFNA(0)"); the "now" text here is decoded '
      'from the xlsb itself.')

# ------------------------------------------------------------------ L87 (High)
c2371=sub('C2371',('MATCH(C2370,','MATCH(" - "&C2370,')).replace('_xlfn.','')
I=[]
for r in range(2403,2420):
    f=fx(f'I{r}'); assert f.count(',0)')==1 and f'E${1982+r-2403},0)' in f,(r,f)
I_new=sub('I2403',(',0)','*$F$90,0)'))
bug('L87','High','Regulations never act: share 0 and the adjustments unused','Mitigation C2371 (policy C8702), I2403:I2419 (policy I8734:I8750); F86:F90 = MTInputs F247:F251',
 'C2371 (share of the regulation shadow price on the efficiency margin, used by K2403:K2419) is IFNA(INDEX($F$86:$F$90,MATCH(C2370,$C$86:$C$90,0)),0), but C86:C90 hold " - "&MTInputs!B247:B251, so the scenario name in C2370 never matches and the share is 0. The feebate rows I2403:I2419 never use F90 (MTInputs F251).',
 [fix('C2371',c2371,'single cell',pol('C2371')),
  fix('I2403',I_new,'I2403:I2419: select, Find/Replace ",0)" by "*$F$90,0)" (one hit per cell; each row keeps its own E$1982...E$1998)','I8734:I8750: same Find/Replace ($F$90 is a shared row)')],
 'The scenario names in Mitigation N223:AC223 equal MTInputs B247:B251 ("Energy efficiency regulations", "Vehicle fuel economy", "Residential efficiency regulations", "Industrial efficiency regulations", "Feebates"); K2403:K2419 already apply C2371 where the sector is covered (F2403:F2419).',
 'Regulation scenarios have no effect at all in legacy; after the fix they cut fuel use through the efficiency margin. prototype v4.16: regulation shadow price = shadow carbon price x adjustment x sector coverage; feebate share x SPPEffAdjFeebates.',
 note=CONV+' The q.py text "=_xlfn.IFNA(0)" behind the register wording is a conversion artefact: the lookup exists, the " - " prefix breaks it. The F90 factor on the feebate share follows the prototype (to confirm).')

# ------------------------------------------------------------------ L58, L59 (Medium): GAINS EF tables, rows 1052-1662 (8 pollutant blocks)
F=pickle.load(open(S+'/f.pkl','rb'))
data=[r for r in range(1049,1664) if F[r][4]=='ton/ktoe' and F[r][2]!='oen']
rng=[];s=data[0];p=s
for r in data[1:]:
    if r!=p+1: rng.append((s,p)); s=r
    p=r
rng.append((s,p))
RNG=', '.join(f'{a}:{b}' for a,b in rng)
for r in data: assert (dfx(f'F{r}') or '').startswith('=_xlfn.IFNA(_xlfn.IFNA(MATCH(_Country_code'),r
assert all(F[r][9] in (None,'') for r in range(1049,1664))
MAP='IF($C1052="srv","res",IF($C1052="ral","rod",$C1052))'
J58='='+MAP+'&MID($G1052,LEN($C1052)+1,99)'
J59=('=IF(COUNTIF(EF_PM!$A$3:$A$39323,"*.mit.ef."&'+MAP+'&"."&$D1052&".*")>0,'+MAP+'&"."&$D1052,'
     'IF($D1052="lpg",'+MAP+'&".nga",IF($C1052="foo","cst."&$D1052,IF($D1052="bio","res.bio",IF($C1052="mnf","cst","mnf")&"."&$D1052))))'
     '&MID($G1052,LEN($C1052)+LEN($D1052)+2,99)')
f0=dfx('F1052')
Jl='IFNA(IFNA(MATCH(_Country_code&".mit.ef."&$J1052,EF_PM!$A$3:$A$39323,0),MATCH(_region_code&".mit.ef."&$J1052,EF_PM!$A$3:$A$39323,0)),MATCH("wld.mit.ef."&$J1052,EF_PM!$A$3:$A$39323,0))'
F_new=('=IFNA('+f0[1:]+','+Jl+')').replace('_xlfn.','')
bug('L58','Medium','Local pollutants: subsectors without a GAINS match get zero factors','Mitigation EF tables rows 1052-1662 (8 blocks: PM2.5 1049, NOx 1126, SO2 1203, VOC 1280, BC 1357, OC 1434, CH4 1511, CO 1587), columns F and J; emissions rows 6607 ff. read them through Em_fact (I1052:AE1663)',
 'F1052 matches country, region, then world GAINS codes "<sub>.<fuel>.<pollutant>" (G1052) in EF_PM!A. GAINS has no "srv" or "ral" subsector, so F is #N/A and the EF (L, AC: IFNA(...,0)) is 0 for services (e.g. rows 1083-1090) and rail diesel (1063). Industry is already mapped to mnf/omn in the emission rows and other energy use takes the MAX (rows 1117 ff.).',
 [fix('J1052',J58,'J of every non-oen data row of the 8 blocks: '+RNG,'none (shared rows above 2173)',now=''),
  fix('F1052',F_new,'F of the same rows ('+RNG+'): copy F1052 down/paste','none (shared rows above 2173)')],
 'Column J is empty in rows 1049-1663 (Em_fact reads the year columns by MATCH on row 1051, so J is not picked up). Mapping as the prototype CH4 subsector (CH4_SUB): services -> residential, rail -> road; G (input/output code, H) stays.',
 'Local pollutants of services and rail no longer zero. prototype v2.9 (each subsector takes the GAINS subsector of its CH4 factor).',
 note='In the NoPropData file the emission rows (e.g. L6607 = IFNA(L6350*INDEX(Em_fact,$J6607,L6605),0)) and the EF values are #NAME?/stripped, so check the result in the full file. '+CONV+' Apply before L59.')
bug('L59','Medium','Local pollutants and combustion CH4: fuels without a GAINS factor emit nothing','Mitigation EF tables rows 1052-1662, helper column J (after L58); sheet EF_PM',
 'A subsector-fuel pair that GAINS does not cover (Egypt EF_PM: res has only nga and bio, foo no diesel, omn no diesel, mnf no LPG, pow no coal) finds no code in F, so all its pollutants and its combustion CH4 (block 1511) are 0, although the fuel burns (row 15939: food & forestry NOx about 1 t).',
 [fix('J1052',J59,'J of the same rows as L58 ('+RNG+')','none (shared rows above 2173)',now=J58)],
 'prototype ef_fallback: LPG takes natural gas of the same (mapped) subsector; food & forestry takes construction; biomass takes residential; else manufacturing (construction for manufacturing itself). The COUNTIF keeps a missing pollutant of a covered fuel at 0 (GAINS omits zero factors), as the prototype. F1052 (L58) already looks the J code up.',
 'Egypt 2022: NOx +11%, PM2.5 +5%, combustion CH4 +20% (prototype v4.12).',
 note='Apply after L58 ("now" is L58\'s J). The COUNTIF tests any country/region/world code for the pair (prototype tests the country GAINS set): to confirm.')

# ------------------------------------------------------------------ L66 (Low)
bug('L66','Low','Other energy use: no additional policy efficiency gains on fossil fuels','Mitigation M6077:AE6084 (policy M12394:AE12401, +6,317)',
 'Rows 6077-6084 (coal ... biomass) divide by (1+_eff_imp_<fuel>_ind) without $M2201 (MTInputs F245, industrial additional efficiency); only the renewables row 6085 and the industry rows add it.',
 [],'Plan L43 (fixes_other_mitigation) already edits the same cells: "_ind))^" -> "_ind+$M2201))^" in M6077:AE6084 and "+$M8532" in the policy rows 12394-12401 (do not paste: +6,317 block with +6,331 drivers).',
 'None while the input is 0. prototype v4.13 (other energy use takes the industrial gain on every fuel).',
 note='No separate edit: applying L43 fixes L66 (same cells, same term).')

# ------------------------------------------------------------------ L81 (Low)
L81=[]
for r in (2460,2483,2506,2529,2552,2575,2598,2621,2644,2667,2690,2713):
    assert fx(f'P{r}').replace(' ','')==f'=$J{r}*O2214', r
    L81.append(fix(f'O{r}',sub(f'O{r}',('N2214','O2214')),f'O{r}:AE{r}',pol(f'O{r}:AE{r}')))
bug('L81','Low','Consumer subsidy phase-out: the fixed subsidy takes last year\'s factor','Mitigation O:AE of the 12 "fixed portion of subsidy" rows 2460, 2483, ..., 2713 (policy +6,331)',
 'O2460 = $J2460 * N2214 (P = O2214, ...): the fixed subsidy uses the consumer phase-out factor of the previous column, while the floating rows (e.g. O2461: O2216/O2217) and the producer rows (O2455: O2213) use the year\'s own factor.',
 L81,'Row 2214 = consumer subsidy phase-out factor; J = 2024 value of the row.',
 'A consumer subsidy phase-out no longer starts and ends a year late. prototype v4.16 (every wedge takes the factor of its year).')

# ------------------------------------------------------------------ L82 (Low)
bug('L82','Low','Residential gas producer subsidy reads the oil row','Mitigation K2547:N2547 (policy K8878:N8878)',
 'The producer-subsidy row of the residential gas block reads K$827 (oil, $/liter) in the data years; the other gas blocks read K$826 (e.g. K2524, K2570). O:AE (= $J2548 * O2213, J2548 = N2547) carry it into the projection.',
 [fix('K2547',sub('K2547',('K$827','K$826')),'K2547:N2547',pol('K2547:N2547'))],
 'Row 826 = producer-side subsidy, natural gas ($/GJ); rows 2524 and 2570 (industry and power gas) already read it.',
 'Residential gas no longer takes the oil producer subsidy. prototype v4.16 (producer subsidies by fuel; no price effect in the prototype, issue I49).')

# ------------------------------------------------------------------ L89 (Low)
m=fx('M5396'); assert 'M2378*M2404' in m and 'L2378*L2404' in m
bug('L89','Low','Coal in road reads the residential coal shadow price','Mitigation M5396:AE5396 (policy M11727:AE11727)',
 'The efficiency term of road coal (M5396) adds M2378*M2404, the coal shadow price of the residential sector (2378 = reg. term + L2355 = $I2355 x residential price L2348); there is no road coal row. Residential coal (5553) reads 2378 rightly; services coal (5634) reads 2378 as services gas reads 2381.',
 [fix('M5396',sub('M5396',('M2378*M2404','(M2378+$I2355*(M2347-M2348))*M2404'),('L2378*L2404','(L2378+$I2355*(L2347-L2348))*L2404')),'M5396:AE5396',pol('M5396:AE5396'))],
 'Rows 2346-2349 are the feebate/ETS prices by sector (pow, rod, res, ind); 2355 = coal EF x residential price, so swapping L2348 for the transport price L2347 gives the road coal shadow price (regulation term unchanged).',
 'Coal in road takes the transport shadow price (minor; Egypt road coal 0). prototype: shadow prices by coverage sector x EF.',
 note='Services (5634) left on the residential price: the prototype feebate sector of services is residential (to confirm).')

# ------------------------------------------------------------------ L90 (Low)
bug('L90','Low','Residential leakage breaks the useful-energy balance','Mitigation M5593:AE5593 (policy M11924:AE11924)',
 'M5593 = -$C5593*(M5578+M5584+M5591)*$E$1785: the equivalent biomass rows (5578 = change x e_fuel / e_bio) are multiplied by BioEff ($C5593) again, so the biomass gain is about 5 times too small.',
 [fix('M5593',sub('M5593',('-$C5593*(','-(')),'M5593:AE5593',pol('M5593:AE5593'))],
 'Equivalent biomass rows 5578, 5584, 5591 already carry the efficiency ratio.',
 'Biomass gain no longer 5 times too small when leakage is on. prototype v5.1 (lkb = -lkd x e_m / e_b).',
 note='Plan L45 (fixes_other_mitigation) rewrites the same cell as =-(M5578+M5584+M5591) (also drops the second $E$1785): if L45 is applied, nothing more to do.')

# ------------------------------------------------------------------ L91 (Low)
bug('L91','Low','Exempt residential fuel still leaks to biomass','Mitigation M5580:AE5580, M5586:AE5586 (policy +6,331)',
 'The leakage tax rows read the new policy of the LPG and kerosene price blocks (M5580 = M2652*M2275, M5586 = M2675*M2275) even when AlwaysExemptResLPGKer removes it from the residential price (5546-5547).',
 [fix('M5580','=IF(LEFT(AlwaysExemptResLPGKer,3)="Yes",0,M2652*M2275)','M5580:AE5580',pol('M5580:AE5580')),
  fix('M5586','=IF(LEFT(AlwaysExemptResLPGKer,3)="Yes",0,M2675*M2275)','M5586:AE5586',pol('M5586:AE5586'))],
 'Same exemption term as the after-tax prices L5546:AE5547; LEFT(...,3) because the input values are "Yes*"/"No*" (plan L48 makes 5546-5547 test it the same way).',
 'An exempt LPG or kerosene no longer leaks to biomass. prototype v5.1 (lkt reads the row\'s own new policy).')

# ------------------------------------------------------------------ L92 (Low)
bug('L92','Low','ExemptMostCook never reaches Mitigation','Mitigation I1784, K1795, L5564:L5570',
 'Does not reproduce in the 456 file: I1784 = IF(AND(H1784="Yes",ISNUMBER(MATCH(L1784,{"lpg","nga","ker"},0))),1,0) with H1784 = MTInputs!F312 (ExemptMostCook), K1795 = exempt share x I1784, and the xlsb formulas L5568:L5570 = IFNA(IF($L$1784=B5568,$K$1795*L5554,0),0), L5564:L5566 = IFNA(IF($L$1784=B5564,(1-$K$1795)*L5554,L5554),L5554) split base-year demand with it.',
 [],'The register (typed 0 in I1784, K1795 unused) matches an older file or the LibreOffice conversion, which shows L5564:L5570, K1790, G1788, L1784 as "=_xlfn.IFNA(...)" constants.',
 'None in this file.',
 note=CONV+' Plan L48 (fixes_other_mitigation) was built on that converted text; its L5564:L5570 formulas are equivalent to the xlsb ones. The ExemptMostCook values are "Yes"/"No" (MTInputs G312 "No", no star), so I1784 needs no LEFT: to confirm.',status='none')

# ------------------------------------------------------------------ L93 (Low)
L93=[]
for r,d in zip(range(2259,2269),[2312,2313,2314,2315,2316,2317,2318,2319,2320,2367]):
    L93.append(fix(f'E{r}',sub(f'E{r}',(f'IF(D{d}=1,','IF(D2369=1,'),('OR(#REF!=4,#REF!=9)','OR(C2173=4,C2173=9)')),
                   'single cell, array formula (Ctrl+Shift+Enter); type each cell, do not fill down (D2369 and C2173 must stay)',pol(f'E{r}')))
bug('L93','Low','Fuel coverage rows test text labels and contain #REF!','Mitigation E2259:E2268 (policy E8590:E8599)',
 'E2259 = {IF(D2312=1,IF(OR(#REF!=4,#REF!=9),"Yes","No"),INDEX(...))}: D2312:D2320 and D2367 are fuel labels ("Coal", ...), never 1, and the scenario test is #REF!, so the shadow-pricing branch is never taken.',
 L93,'The sector rows use the same rule with live references: E2270 = {IF(D2369=1,IF(OR(C2173=4,C2173=9),"Yes","No"),INDEX($D$223:$AG$257,F2270,F2258))} (D2369 = 1 for shadow pricing).',
 'None (dead branch); under shadow pricing the fuels follow the sector rule. prototype: not built (coverage by switch).',
 note='Copying E2259:E2268 to E8590:E8599 moves D2369 to D8700 and C2173 to C8504, the policy block\'s own cells.')

# ------------------------------------------------------------------ L94 (Low)
L94=[fix(f'L{r}',sub(f'L{r}',('$E2265',f'$E{r}'),base=fx('L2265')),f'L{r}:AE{r}',pol(f'L{r}:AE{r}')) for r in (2266,2267,2268)]
for r in (5568,5569,5570):
    L94.append(fix(f'M{r}',sub(f'M{r}',('MIN(M2258/ExemptPhaseoutPeriod,1)','IF(ExemptPhaseout,MAX(MIN((M2257+1-YearPha)/ExemptPhaseoutPeriod,1),0),0)')),f'M{r}:AE{r}',pol(f'M{r}:AE{r}')))
bug('L94','Low','Exemption phase-in rules differ between rows','Mitigation L2266:AE2268 and M5568:AE5570 (policy +6,331)',
 'Rows 2259-2265 and 2270-2288 phase an exemption in with IF(ExemptPhaseout,MAX(MIN((t+1-YearPha)/ExemptPhaseoutPeriod,1),0),0) and test $C2173>1; biomass, renewables and jet fuel (2266-2268) and the exempt residential demand (5568-5570, MIN(M2258/ExemptPhaseoutPeriod,1)) count from CPIntro (row 2258) and ignore the switch.',
 L94,'L2265 (kerosene) is the rule of the first group; M2257 is the year header of rows 2259-2288.',
 'Biomass, renewables, jet fuel and the exempt residential demand phase in like the other fuels. prototype: not built (LegacyDiff 67).',
 note='Rows 2266-2268 lose their own "No"/number handling (as rows 2259-2265). M5568:M5570 are also edited by plan L48 (income factor M2433): if L48 is applied first, make only the exponent substitution shown here. One rule as the register; to confirm.')

json.dump(A,open(S+'/parts/part_B.json','w'),indent=1)
for b in A: print(b['id'],b['status'],len(b['fixes']))
