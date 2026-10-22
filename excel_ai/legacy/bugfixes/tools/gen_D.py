# Cell-level fix plans, group D: L96-L106 (register v5.4); legacy file CPAT 1.0pre_456
import json,sys,pickle,os
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,S)
from q import fx as _fx
HI=pickle.load(open(os.path.join(S,'parts','mit_hi.pkl'),'rb'))  # Mitigation rows > 15000 (openpyxl, raw)
from openpyxl.utils import column_index_from_string as ci
import re
def fx(sheet,a):
    c,r=re.match(r'([A-Z]+)(\d+)',a).groups(); r=int(r)
    if sheet=='Mitigation' and r>15000:
        row=HI.get(r,()); i=ci(c)-1
        v=row[i] if i<len(row) else None
        return '' if v is None else v
    v=_fx(sheet,a)
    return '' if v is None else v
def bal(f):
    if not isinstance(f,str): return f
    d=0
    for ch in f:
        d+=(ch in '({')-(ch in ')}'); assert d>=0,f
    assert d==0,f; return f
def sub(sheet,a,*pairs):
    f=fx(sheet,a)
    for o,n in pairs:
        assert o in f,(a,o,f); f=f.replace(o,n)
    return bal(f)
def fix(sheet,cell,new,fill,policy,now=None):
    nw=now if now is not None else fx(sheet,cell)
    if not isinstance(nw,str): nw=repr(nw)
    pre='' if sheet=='Mitigation' else f"'{sheet}'!"
    return dict(cell=pre+cell,now=nw,new=bal(new),fill=fill,policy=policy)
def chk(sheet,a,val):
    assert fx(sheet,a)==val,(sheet,a,fx(sheet,a),val)
A=[]
def bug(id,pri,title,where,why,fixes,ref,effect,note=None,status='fix'):
    A.append(dict(id=id,pri=pri,title=title,where=where,why=why,fixes=fixes,ref=ref,effect=effect,note=note,status=status))
M='Mitigation'; MI='Manual inputs'
NOPOL='none (sheet has no policy copy)'
SHARED='none (shared row above 2173)'

# ---------------- L96
for a,v in [('C2199','Tax in nominal or real terms?'),('C2201','Exponential option or linear'),('E2201','`'),('K2197','Sector'),('M2197','Increment'),
            ('K2199','Road vehicles'),('M2201','=MTInputs!$F$245'),('E2385','Road'),('E2386','Industry'),('H2385','=LOWER(_Country_code&".mit.shp.lpg.all.")&C2173'),
            ('H2386','=LOWER(_Country_code&".mit.shp.ker.all.")&C2173'),('C8532','Exponential option or linear'),('K8528','Sector'),('E8716','Road'),('E8717','Industry')]:
    chk(M,a,v)
TYPO=['D5615','D5722','D6072','D6083']; TYPOP=['D11946','D12042','D12389','D12400']
for a in TYPO+TYPOP: chk(M,a,'Other oil pinducts')
L96=[fix(M,'K2197','Additional efficiency gain pa: sector','label only','type K8528 the same'),
     fix(M,'M2197','Additional efficiency increment (MTInputs F242:F245)','label only; M2198:M2201 read by the fuel rows as $M2198..$M2201','type M8528 the same'),
     fix(M,'C2201','','clear the duplicated label (its E2201 holds a stray "`" and is read by nothing)','clear C8532'),
     fix(M,'E2201','','clear the stray "`"','clear E8532'),
     fix(M,'E2385','All','label only (code shp.lpg.all)','type E8716 = All'),
     fix(M,'E2386','All','label only (code shp.ker.all)','type E8717 = All')]
L96+=[fix(M,a,'Other oil products','label only',f'type {p} the same') for a,p in zip(TYPO,TYPOP)]
bug('L96','Low','Fuel-use block: mislabelled parameter and fuel rows','Mitigation C2197:M2201, E2385:E2386, D5615/D5722/D6072/D6083 (+ policy copies)',
 'C2199:C2201 label the carbon-tax settings in E, and the additional-efficiency increments read by every fuel row ($M2198:$M2201 = MTInputs F242:F245) sit beside them under the bare headers K2197 "Sector" / M2197 "Increment"; C2201 repeats "Exponential option or linear" over a stray "`" in E2201. E2385/E2386 say Road/Industry on the all-sector LPG and kerosene shadow prices; D5615, D5722, D6072, D6083 read "Other oil pinducts".',
 L96,
 'Policy copies found by label search: K8528/M8528, C8532/E8532, E8716/E8717, D11946, D12042 (offset +6,320), D12389, D12400 (+6,317). No formula reads E2201, C2201, K2197, M2197, E2385 or E2386 as text.',
 'None on values (labels only). prototype: own labelled rows for additional efficiency, shadow prices by coverage sector, fuel names.',
 note='Relabelling the existing header row is the smallest fix; the prototype gives the increments rows of their own (to confirm if a move is wanted). The same typo is in 68 more output labels (Mitigation column E, rows 14808-15622): fix all with Find & Replace "pinducts" -> "products" on Mitigation (76 text cells, no formula contains the text).')

# ---------------- L97
chk(M,'M5667','=(N2446)'); chk(M,'K5714','Price'); chk(M,'D5727','Fuel'); chk(M,'D5728','Average'); chk(M,'K5716','=J5716/J$5725'); chk(M,'J5725','=SUM(J5716:J5724)')
L97=[fix(M,'M5667','','clear D5667:AE5676 (elasticity memo table and the GDP row M5667:AE5667 = next year N2446..AF2446)','none (no policy copy: the policy iron & steel block 12019-12045 has no memo rows)'),
     fix(M,'L5714','','clear K5714:AE5714 (EF-weighted average price)','none (no policy copy)'),
     fix(M,'K5716','','clear I5715:K5724 and J5725 (EF, emissions, weights); keep B:H and L:AE of rows 5716-5725 (the iron & steel demand, read by row 6049 and others)','none (no policy copy)'),
     fix(M,'M5727','','clear D5727:AE5728 (demand and efficiency multiples)','none (no policy copy)')]
bug('L97','Low','Iron & steel memo rows unused; one reads next year\'s growth','Mitigation D5667:AE5676, K5714:AE5714, I5715:K5725, D5727:AE5728',
 'Row 5714 averages the iron & steel prices with emission weights (K5716:K5724 = J/J$5725, J = EF in I x base-year demand); rows 5727-5728 build demand and efficiency multiples from it and from the elasticity table 5668-5676; M5667 = (N2446) is next year\'s GDP growth. No cell on any sheet reads 5667-5676, 5714, I:K 5715-5725 or 5727-5728.',
 L97,'The live iron & steel demand rows 5716-5724 (columns L:AE) and their total L5725:AE5725 stay.',
 'None (dead calculation).',
 note='Alternative if the memo is kept as diagnostics: M5667 = (M2446), fill M5667:AE5667 (the year\'s own growth). Clearing follows the prototype (not built); to confirm.')

# ---------------- L98
L98=[fix(MI,'P54',sub(MI,'P54',('Dashboard!$R$30','Dashboard!$K$44')),'P54:X54 (copy across; the P53..X53 reference is relative)',NOPOL)]
bug('L98','Medium','Feebate inclusion of industry reads the ETS industry flag','Manual inputs P54:X54 (FeebateInclusion = H54:X54 -> MTInputs E66:E82)',
 "P54:X54 = AND(Dashboard!$R$30, P53): Dashboard R30 is the ETS industry switch; the feebate industry switch is Dashboard K44 (H44:J44 feed H54 and M54:O54).",
 L98,'Dashboard row 44 "Included?" (H power, J buildings, K industry) as read by H54 and M54:O54.',
 'Industry feebate coverage follows the Dashboard feebate switch K44 instead of the ETS switch R30. None for the shipped Egypt run unless R30 or K44 is changed (both feebate values 0).')

# ---------------- L99
L99=[fix(MI,c,sub(MI,c,('Dashboard!$Q$30','Dashboard!$R$30')),'single cell',NOPOL) for c in ('S11','U11')]
bug('L99','Medium','ETS inclusion of machinery and other manufacturing uses the buildings flag','Manual inputs S11, U11 (ETSInclusion = H11:X11)',
 'S11 (machinery) and U11 (other manufacturing) read Dashboard Q30 (buildings) while P11, Q11, R11, T11 read R30 (industry); Dashboard R31 counts P11:X11 as the industry subsectors.',
 L99,'Dashboard R30 = ETS "In?" for Industry, as in P11:R11 and T11.',
 'Machinery and other manufacturing join the ETS with industry, not buildings. Egypt default: Q30 FALSE, R30 TRUE, so mch and omn enter the ETS when it is on (ETS off by default).',
 note='V11:X11 (construction, fuel transformation, other energy use) also read Q30 although Dashboard R31 counts them under industry; register I52 treats this as a grouping choice: left unchanged (to confirm).')

# ---------------- L100
L100=[dict(cell='Name _manual_prices',now="='Manual inputs'!$G$59:$N$133",new="='Manual inputs'!$G$59:$N$146",fill='Name Manager: both copies (workbook scope and the sheet-scoped copy)',policy='none (defined name)'),
      dict(cell='Name _manual_codes',now="='Manual inputs'!$G$59:$G$133",new="='Manual inputs'!$G$59:$G$146",fill='Name Manager: both copies (workbook scope and the sheet-scoped copy)',policy='none (defined name)')]
for a,v in [('G136','mit.sp.ecy.res'),('G146','mit.pros.ecy.all'),('G133','mit.rp.oop.all')]: chk(MI,a,v)
chk(M,'I828','=MATCH($G828,_manual_codes,0)'); chk(M,'G828','mit.pros.ecy.all'); chk(M,'G790','mit.sp.ecy.res')
bug('L100','Low','Manual domestic prices: the electricity rows are never read','Manual inputs G59:N146 (names _manual_prices, _manual_codes)',
 'Mitigation rows 765-829 look up _manual_codes / _manual_prices (I = MATCH($G,_manual_codes,0)); both names stop at row 133, so the electricity codes mit.sp/txo/rp.ecy.res/ind (Manual inputs 136-144, read by Mitigation 789-795) and mit.pros.ecy.all (146, Mitigation 828) are never found and the CPAT values are used.',
 L100,'Manual inputs G135:N135 repeats the header (Code, years), so the extended names keep the same columns; _manual_years (G59:N59) is unchanged.',
 'Manual electricity prices and producer subsidy are ignored; none for Egypt (prices not set to Manual).',
 note='Also fixes the cause of L86 (manual electricity producer subsidy, Mitigation I828).')

# ---------------- L101
chk('Elasticities','F58',"=IF(ISBLANK('Manual inputs'!M286),\"no data\",'Manual inputs'!M286)")
L101=[fix('Elasticities','F51',sub('Elasticities','F51',("'Manual inputs'!M279","'Manual inputs'!N279")),'F51:F58 (copy down: F52 -> N280 ... F58 -> N286)',NOPOL)]
bug('L101','Low','Manual services income elasticities read the industries column','Elasticities F51:F58 (Manual inputs N279:N286)',
 'F51:F58 (coal ... electricity, services) read Manual inputs M279:M286, the Industries column; Services is column N (N277 = "Services").',
 L101,'Manual inputs row 277: K Transport, L Residential, M Industries, N Services.',
 'Manual services income elasticities equal the industry ones (defaults all 0.5: no effect on Egypt).',
 note='Unrelated, seen in passing: Elasticities H53 = H173 and H54 = H174 while G53 = G169, G54 = G170 (gasoline/diesel services take the renewables/electricity column-H value); not part of L101, to confirm.')

# ---------------- L102
for a,v in [('K326','=IF($E$293="Manual",#REF!,0.9)'),('L326','=IF($E$293="Manual",#REF!,1)'),('M326','=IF($E$293="Manual",#REF!,1)'),('K327','=IF($E$293="Manual",#REF!,0.15)')]: chk(MI,a,v)
L102=[fix(MI,'K326','0.9','typed input','none'),fix(MI,'L326','1','typed input','none'),fix(MI,'M326','1','typed input','none'),fix(MI,'K327','0.15','typed input','none'),
      fix(M,'K366',"='Manual inputs'!K326",'single cell',SHARED),fix(M,'L366',"='Manual inputs'!L326",'single cell',SHARED),
      fix(M,'M366',"='Manual inputs'!M326",'single cell',SHARED),fix(M,'K367',"='Manual inputs'!K327",'single cell',SHARED)]
bug('L102','Low','Manual non-energy elasticities can never take effect','Manual inputs K326:M327; Mitigation K366:M367',
 'Manual inputs K326:M326, K327 = IF($E$293="Manual",#REF!,default) (E293 is empty), and Mitigation K366:M367 = IF($E$288="Manual",\'Manual inputs\'!K326, default) where E288 = MTInputs F261 (ElastIncAdjustment: Low/Base*/High), never "Manual".',
 L102,'Defaults 0.9 / 1 / 1 (population) and 0.15 (agriculture per capita income) as typed in the legacy fallbacks; L367:M367 stay "na".',
 'None on values (same defaults); manual non-energy elasticities typed on Manual inputs now take effect. prototype v5.2 (LegacyDiff 72).')

# ---------------- L103
chk(M,'D17683','Manual'); chk(M,'D17711','Manual'); chk(M,'L17711','=L17683'); chk(M,'AE17683','=AD17683*AD17683/AC17683')
chk(MI,'J236','=FirstYearCalculations'); chk(MI,'J237','=J240'); chk(MI,'AC240','=AB240*(1+$F$239)')
L103=[fix(M,'L17683',"='Manual inputs'!J237",'L17683:AE17683 (Manual inputs J:AC = 2022-2041; replaces the typed path L:AD and AE = AD*AD/AC)','none (single SCC block)'),
      fix(M,'L17711',"='Manual inputs'!J240",'L17711:AE17711','none (single SCC block)')]
bug('L103','Low','Manual SCC reads a path typed on Mitigation, not the Manual inputs block','Manual inputs rows 234-240; Mitigation rows 17683, 17711',
 'NSCC "Manual" (CHOOSE($G$17674,...,L17683,...) in row 17685) takes the typed path L17683:AD17683 (80.8 in 2022 rising) and GSCC "Manual" (row 17711 = L17683, chosen in row 17713) reuses it; the Manual inputs SCC block (NSCC row 237, GSCC row 240) is read by nothing.',
 L103,'Mitigation L17680 and Manual inputs J236 are both FirstYearCalculations, so Mitigation L:AE match Manual inputs J:AC. Manual inputs J237 = J240 by default (NSCC = GSCC).',
 'Manual SCC entered on Manual inputs is ignored; none for the shipped scenarios and Egypt (SCC source Target).',
 note='The typed values on row 17683 are lost; if they are wanted as the manual default, type them into Manual inputs J237:AC237 first (to confirm). prototype reads row 237 only (scc.man); using J240 for GSCC follows the register.')

# ---------------- L104
L104=[dict(cell='Name CH4Feebate',now="='Manual inputs'!$J$217",new='(delete the name)',fill='Name Manager',policy='none (defined name)')]
assert fx(MI,'J217')==''
bug('L104','Low','Name CH4Feebate points to an empty cell','Manual inputs J217 (name CH4Feebate)',
 'CH4Feebate refers to Manual inputs J217, an empty cell between the pass-through table (rows 205-215) and the energy price block (218); no formula in the workbook uses the name. The methane fee inputs are MTInputs rows 185-189 (CTforMethane = F185) and Manual inputs rows 185-200.',
 L104,'No reference to CH4Feebate found in any sheet formula.',
 'None (unused name).',note='Deleting follows the prototype (name not used); re-pointing it would need a choice of methane fee input (to confirm).',status='struct')

# ---------------- L105
chk('MTInputs','E56','{=TRANSPOSE(Dashboard!H$46:$J46)}'); chk('MTInputs','E61','{=TRANSPOSE(Dashboard!H$47:$J47)}')
chk('MTInputs','H59','D_Feb_Level_Start_Ind'); chk('MTInputs','H64','D_Feb_Level_Target_Ind'); chk('Dashboard','K43','Industry')
L105=[fix('MTInputs','E56',sub('MTInputs','E56',('$J46','$K46')),'array over E56:E59: select E56:E59 (was E56:E58), enter, Ctrl+Shift+Enter',NOPOL),
      fix('MTInputs','E61',sub('MTInputs','E61',('$J47','$K47')),'array over E61:E64: select E61:E64 (was E61:E63), enter, Ctrl+Shift+Enter',NOPOL)]
bug('L105','Medium','Dashboard industry feebate rates are lost','MTInputs E56:E64 (Dashboard H46:K47)',
 'E56:E58 = {TRANSPOSE(Dashboard!H$46:$J46)} and E61:E63 = {TRANSPOSE(Dashboard!H$47:$J47)} cover power, transport, buildings; E59 and E64 (industry, D_Feb_Level_Start_Ind / D_Feb_Level_Target_Ind) are empty, so Dashboard K46 / K47 never reach F59 / F64.',
 L105,'Dashboard H43:K43 = Power, Transport, Buildings, Industry; MTInputs rows 56-59 and 61-64 are in the same order.',
 'Industry feebate rates set on the Dashboard take effect (user-defined path); none for Egypt (all rates 0).')

# ---------------- L106
chk(MI,'K315','=K298+K306+(K298*K306)'); chk(MI,'K316','=K297+K307+(K297*K307)')
L106=[fix(MI,'K315',sub(MI,'K315',('K298+','K297+'),('(K298*','(K297*')),'K315:N315',NOPOL),
      fix(MI,'K316',sub(MI,'K316',('K297+','K298+'),('(K297*','(K298*')),'K316:N316',NOPOL)]
bug('L106','Low','Manual inputs memo swaps the renewables and electricity price elasticities','Manual inputs K315:N316',
 'The memo total elasticity of renewables (row 315) adds the electricity price elasticity (row 298) to the renewables efficiency elasticity (306); electricity (316) uses the renewables row 297 with 307.',
 L106,'Rows 297 (el_dem_ren) and 298 (el_dem_ecy); the other memo rows 309-314 pair row n with n+9.',
 'None (memo only, read by nothing). prototype: fixed in the placed memo.')

out=os.path.join(S,'parts','part_D.json')
json.dump(A,open(out,'w'),indent=1,ensure_ascii=False)
for b in A: print(b['id'],len(b['fixes']),b['status'])
