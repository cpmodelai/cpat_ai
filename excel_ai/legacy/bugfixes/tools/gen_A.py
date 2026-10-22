# Group A: cell-level fix plans for L51, L57, L60-L65, L78-L80 (legacy CPAT 1.0pre_456)
import json,sys,re,os
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,S)
from q import fx as _fx
def fx(a):
    sh,c=a.split('!') if '!' in a else ('Mitigation',a)
    v=_fx(sh,c); return v if isinstance(v,str) else ('' if v is None else repr(v))
def bal(f):
    d=0
    for ch in f:
        d+=(ch in '({')-(ch in ')}'); assert d>=0,f
    assert d==0,f; return f
def sub(a,*pairs):
    f=fx(a)
    for o,n in pairs:
        assert o in f,(a,o,f); f=f.replace(o,n)
    return bal(f)
def fix(cell,new,fill,policy,now=None):
    return dict(cell=cell,now=now if now is not None else fx(cell),new=bal(new),fill=fill,policy=policy)
P=6331
def pol(rng,off=P):
    return 'paste into '+re.sub(r'(\d+)',lambda m:str(int(m.group(1))+off),rng)+f' (+{off:,})'
NONE='none (shared row above 2173)'
A=[]
def bug(id,pri,title,where,why,fixes,ref,effect,note=None,status='fix'):
    A.append(dict(id=id,pri=pri,title=title,where=where,why=why,fixes=fixes,ref=ref,effect=effect,note=note,status=status))

# ---------- Medium
bug('L57','Medium','New ETS: the quick price estimate is linear in the semi-elasticity','Mitigation ETS block, row 1868 (QuickEstimateOfETSPrices, Q1868:AD1868)',
 'Q1868 = MAX(Q1860/Q1867,0): the needed relative change of covered emissions (row 1860, from rows 1858-1859) divided by the adjusted semi-elasticity (row 1867 = D1845 x effectiveness row 1866). Emissions respond log-linearly to the price, so the linear estimate misses the cap and is left to the VBA goal seek.',
 [fix('Q1868',sub('Q1868',('Q1860/Q1867','LN(1+Q1860)/Q1867')),'Q1868:AD1868',NONE)],
 'Row 1860 is the change relative to baseline (cap / baseline - 1); D1845 already divides by the volatility ratio D1843, so row 1867 = semi-elasticity x effectiveness x volatility adjustment, as in the MVP. Row 1871 = IFERROR(Q1868,0) catches a reduction of 100% or more (LN of 0 or less).',
 'New ETS scenarios: the quick estimate meets the cap (legacy relies on the VBA goal seek). MVP v1.02.',
 note='The VBA goal seek (ETSMaxIterations, ETSErrorTolerance) still runs from this estimate; no macro change needed.')
L79=[fix('L2323',sub('L2323',('MAX($G2404:$G2407)','IFERROR(SUMPRODUCT($G2404:$G2407,$F$1816:$F$1819)/SUM($F$1816:$F$1819),MAX($G2404:$G2407))')),'L2323:AE2323',
         'policy L8654:AE8654: '+sub('L8654',('MAX($G8735:$G8738)','IFERROR(SUMPRODUCT($G8735:$G8738,$F$1816:$F$1819)/SUM($F$1816:$F$1819),MAX($G8735:$G8738))'))+' (type, do not paste: the policy row reads $G8735, $C8504, $E8520)'),
     fix('L2325',sub('L2325',('MAX($G2409:$G2418)','IFERROR(SUMPRODUCT($G2409:$G2418,$F$1821:$F$1830)/SUM($F$1821:$F$1830),MAX($G2409:$G2418))')),'L2325:AE2325',
         'policy L8656:AE8656: '+sub('L8656',('MAX($G8740:$G8749)','IFERROR(SUMPRODUCT($G8740:$G8749,$F$1821:$F$1830)/SUM($F$1821:$F$1830),MAX($G8740:$G8749))'))+' (type, do not paste)')]
bug('L79','Medium','ETS: industry and transport priced as a whole when one subsector is covered','Mitigation rows 2323, 2325 (policy 8654, 8656); revenue rows 7790, 7792 follow',
 'L2323 (transport) and L2325 (industry) = MAX of the subsector coverage flags G2404:G2407 / G2409:G2418 x the auctioned permit price, so one covered subsector puts the full price on the whole sector; revenue rows 7790/7792 (= sector CO2 rows 7784/7786 x price rows 7779/7781 = L2323/L2325) then charge the whole sector, while the price estimate (K1815:K1831) counts covered subsectors only.',
 L79,
 'Weights F1816:F1819 and F1821:F1830 are the country baseline emissions by subsector (2025, column O of rows 1889-1903), the same rows that define coverage in E1815:E1836. Revenue rows 7789-7792 need no change: sector CO2 x (price x covered share) = price x covered CO2. Rows 2322 (power) and 2324 (residential) are single subsectors.',
 'Uncovered industry and transport subsectors no longer pay the full permit price; revenue on covered CO2 only. MVP: coverage, price and revenue by subsector (etsc, v1.07).',
 note='To confirm: the legacy price blocks are by fuel x sector (one industry price, one road price), so separate subsector prices as in the MVP need new price rows (structural). This plan applies the emission-weighted covered share of the sector instead (exact for revenue, average for the price signal). IFERROR keeps the MAX when the sector has no baseline emissions.')

# ---------- Low
bug('L51','Low','Energy trade balance of coal valued at the oil price','Mitigation row 743 (K743:AE743)',
 'K743 = -(G504+E504) x conversion x K731, and row 731 is the crude oil price per GJ; the coal price per GJ is row 732. Egypt 2022: -1.4 bn USD instead of about -0.5.',
 [fix('K743',sub('K743',('*K731','*K732')),'K743:AE743',NONE)],
 'Row 732 = coal forecast, international, $/GJ real (K728/$G728); rows 741-742 use the gas (733) and oil (731) prices.',
 'Reported energy trade balance only (Egypt: about 0.6 bn USD a year). MVP v4.6.')
L60=[]
for r,rp,vr,sh in ((2595,2589,2594,2611),(2618,2612,2617,2634),(2641,2635,2640,2657),(2664,2658,2663,2680)):
    L60.append(fix(f'K{r}',sub(f'K{r}',(f'(1 + K{vr})',f'(1 + K{vr} * K{sh})')),f'K{r}:N{r} (O:AE already = (sp + taxes) x rate x share)',pol(f'K{r}:N{r}')))
bug('L60','Low','VAT payment on oil products divided by the full VAT rate','Mitigation K2595:N2595, K2618:N2618, K2641:N2641, K2664:N2664 (policy +6,331)',
 'The retail price carries VAT x household share (row 797 = (sp + txo) x (1 + K800 x K801), same for 802, 807, 812), but in the data years K:N the VAT payment is retail / (1 + rate) x rate x share (K2595), so VAT is understated where the share is below 1 and the excise residual (K2596 = rp - sp - VAT) absorbs the gap. From O the row is already (txo + sp) x rate x share.',
 L60,
 'Rows 2611, 2634, 2657, 2680 = household shares (rows 801, 806, 811, 816). retail / (1 + rate x share) = sp + taxes, so the new K:N equals (supply cost + taxes) x rate x share without a circular reference to row 2596.',
 'None for Egypt (VAT 0 on oil). MVP v4.12.')
bug('L61','Low','EU ETS price grows with the carbon-tax growth','Mitigation P1695:AE1695',
 'After the last data year (O = 2025) P1695 = O1695 x (1 + ExistingCTGrowth) x $C$1677; ExistingCTGrowth is MTInputs F214 (carbon tax), the ETS growth input is ExistingETSGrowth (MTInputs F209).',
 [fix('P1695',sub('P1695',('ExistingCTGrowth','ExistingETSGrowth')),'P1695:AE1695',NONE)],
 'Defined name ExistingETSGrowth = MTInputs!F209 (Dashboard Q149). The carbon tax rows 1727-1736 keep ExistingCTGrowth.',
 'None for Egypt. MVP v4.12.',
 note='The national ETS price row 1680 shows {=IFNA(0)} in all years in the converted file (no growth formula visible); check it in Excel and apply ExistingETSGrowth there too if it grows with ExistingCTGrowth.')
L62=[]
for r,rate,cov in ((1760,1732,1745),(1761,1733,1746),(1762,1734,1747)):
    k=fx(f'K{r}'); new=k
    for o,n in ((f'K$1727',f'L$1727'),(f',K{rate},',f',L{rate},'),('*K$1740*',f'*L$1740*'),(f'*K{cov}',f'*L{cov}')):
        assert o in new,(r,o); new=new.replace(o,n)
    assert '$K$81' in new and '$J'+str(rate) in new
    L62.append(fix(f'L{r}',new,f'L{r}:AE{r} (= K{r} copied across)',NONE))
bug('L62','Low','Existing carbon tax on transport diesel, LPG and kerosene uses the rate row as coverage','Mitigation L1760:AE1762',
 'From L, rows 1760-1762 = single rate x EF x INDEX(rows 1732:1749, MATCH(sector code)) x INDEX(rows 1732:1749, MATCH(fuel code)); the fuel-code MATCH finds the fuel rate row (1732-1734) before the coverage row (1745-1747), so the tax is rate x rate x sector coverage, and the single-price flag $K$81 and the fuel rate are ignored. K1760:K1762 hold the correct form.',
 L62,
 'K1760:K1762 and rows 1759, 1763 (all years): IF(single price, single rate, fuel rate if any) x EF x transport coverage (row 1740) x fuel coverage (rows 1745-1747).',
 'None for Egypt. MVP v4.12.')
bug('L63','Low','Existing carbon tax fuel coverage: lookup range cut short','Mitigation J1741:J1749',
 'J1741 = MATCH(G1741, ECP!$E$133:$E$403, 0), but the fuel coverage block of ECP runs from row 138 to 425 (header row 136): Ukraine (from ker), Uruguay and the United Kingdom are not found, so no fuel coverage and no existing carbon tax.',
 [fix(f'J{r}',sub(f'J{r}',('ECP!$E$133:$E$403','ECP!$E$133:$E$425')),'single cell (J1741:J1749 each, or fill J1741 down)',NONE) for r in range(1741,1750)],
 'ECP rows 136-425 "Fuel coverage: carbon taxes" (last row gbr.mit.ecf.bio); the sectoral block starts at 428.',
 'None for Egypt. MVP v4.12.',
 note='K1741:O1749 show as {=IFNA(0)} in the converted file: if their INDEX on ECP stops at row 403 (e.g. ECP!$F$133:$P$403), extend it to row 425 as well.')
bug('L64','Low','No existing ETS on other oil products outside power','Mitigation K1717:AE1717',
 'Row 1717 (oop, pow) = EF x (national price x fuel coverage 1687 x POWER coverage 1681 + EU price x 1702 x POWER coverage 1696) and is the only oil-products ETS row; it feeds the all-sector oil-products price (row 2693 = K$1717, policy 9024), while the carbon tax row 1758 applies the industry coverage (K1739).',
 [fix('K1717',sub('K1717',('*K1681)','*K1683)'),('*K1696)','*K1698)')),'K1717:AE1717 (single-cell array formulas: edit K, copy across)',NONE)],
 'Rows 1683 and 1698 = national and EU ETS industry coverage, as rows 1713 and 1716; row 1717 has no other reader than 2693/9024.',
 'None for Egypt. MVP v4.12.',
 note='To confirm: the EF stays the power one (G1717 = mit.ef.oop.pow); set C1717 = "all" to take the all-sector EF as row 1758 does.')
L65=[]
for r in list(range(2270,2286))+[2287,2288]:
    L65.append(fix(f'L{r}',sub(f'L{r}',('INDEX(K$1681:K$1684','INDEX(L$1681:L$1684')),f'L{r}:AE{r} (single-cell array formula, copy across)',
        f'policy L{r+P}:AE{r+P}: '+sub(f'L{r+P}',('INDEX(K$1681:K$1684','INDEX(L$1681:L$1684'))+' (type, do not paste: $C8504)'))
bug('L65','Low','Carbon tax complementary to an existing ETS: last year\'s ETS coverage','Mitigation L2270:AE2285, L2287:AE2288 (policy L8601:AE8616, L8618:AE8619)',
 'With CTaxComplimentaryToETS = "Yes" each coverage cell is 1 - INDEX(K$1681:K$1684, $J): column K in column L, i.e. the national ETS sector coverage of the previous year.',
 L65,
 'Rows 1681-1684 = national ETS sector coverage by year (held after 2025, so only 2022-2026 change).',
 'None for Egypt. MVP v4.12.',
 note='Row 2286 (oen) has no complementary branch and is left as is.')
bug('L78','Low','ETS: auctioned share drops to 0 after the target year unless "Constant"','Mitigation Q1863:AD1863 (MTInputs row 92)',
 'Q1863 = start share + slope until the target year $D$1805, then IF($D$1808 = "Constant", previous year, 0): any other continuation (MTInputs F92, D_ETSAuctCont) makes all permits free after the target year.',
 [fix('Q1863',sub('Q1863',('IF($D$1808="Constant",P1863,0)','P1863')),'Q1863:AD1863',NONE)],
 'D1806/D1807 = auctioned share in the start/target year (MTInputs F90/F91); the target-year value is held, as the MVP.',
 'An auctioned share no longer drops to 0 (all free) after the target year. MVP v4.15.',
 note='MTInputs row 92 (D_ETSAuctCont, Dashboard I33) no longer acts; relabel it or drop it from the Dashboard.')
bug('L80','Low','ETS: the carbon-tax trajectory rescaled when the ETS is on','Mitigation L2251:AE2251 (policy L8582:AE8582)',
 'L2251 = CHOOSE($E2200, ...) x IF($E2189 = "Yes", $E2191, 1), and E2191 = 1 / D1843 (volatility ratio), so the carbon-tax path is scaled whenever the new ETS applies.',
 [fix('L2251',sub('L2251',('*(IF($E2189="Yes",$E2191,1))','')),'L2251:AE2251',pol('L2251:AE2251'))],
 'Rows 2248-2250 are the MTInputs carbon-price paths; the volatility adjustment stays in the ETS price (D1845 / D1843).',
 'The carbon tax outside the ETS is no longer cut by the volatility ratio. MVP: the carbon tax path is the MTInputs path.',
 note='Rows 7732-7735 (policy 14049-14052) still multiply by $E2191 when the scenario is "ETS"; not part of this bug.')
order=['L51','L57','L60','L61','L62','L63','L64','L65','L78','L79','L80']
A.sort(key=lambda b:order.index(b['id']))
json.dump(A,open(os.path.join(S,'parts','part_A.json'),'w'),indent=1)
for b in A: print(b['id'],len(b['fixes']),b['status'])
