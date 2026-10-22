# Group E: cell-level fix plans for the distribution bugs D1-D9 (register v5.4 DIST_BUGS); legacy file CPAT 1.0pre_456
import json,sys,re,os
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,S)
from q import fx as qfx
from openpyxl.utils import get_column_letter as L, column_index_from_string as ci
D='Distribution'
def fx(a,sh=D):
    f=qfx(sh,a); return '' if f is None else f
def bal(f):
    d=0
    for ch in f:
        d+=(ch in '({')-(ch in ')}'); assert d>=0,f
    assert d==0,f; return f
def sub(a,*pairs,sh=D):
    f=fx(a,sh)
    for o,n in pairs:
        assert o in f,(a,o,f); f=f.replace(o,n,1)
    return bal(f)
def fix(cell,new,fill,policy='none (sheet Distribution)',now=None,sh=D):
    return dict(cell=f'{sh}!{cell}',now=now if now is not None else fx(cell,sh),new=bal(new),fill=fill,policy=policy)
COLS=[L(c) for c in range(ci('Q'),ci('Z')+1)]
def shift(f,dc):  # relative column shift of unanchored column letters (copy across)
    return re.sub(r'(?<![A-Za-z_$])([A-Z]{1,2})(\$?\d+)',lambda m:L(ci(m.group(1))+dc)+m.group(2) if not m.group(0).startswith('$') else m.group(0),f)
A=[]
def bug(id,pri,title,where,why,fixes,ref,effect,note=None,status='fix'):
    A.append(dict(id=id,pri=pri,title=title,where=where,why=why,fixes=fixes,ref=ref,effect=effect,note=note,status=status))

# ---------- D1
for c in COLS[1:]:
    p=L(ci(c)-1); assert fx(f'{c}2562')==f'=IF($Q$2552>={p}2561,MIN($Q$2552-{p}2561,10),0)',c
bug('D1','Low','Targeted transfer capped at 10 points, not the decile\'s population share','Distribution R2562:Z2562',
 'R2562:Z2562 give a decile MIN(targeted percentile - cumulative share of the deciles below, 10): the cap is 10 points instead of the decile\'s population share (row 2560, e.g. 10.56 for decile 2), so more than 100% of a decile can be targeted (105.6% of decile 2).',
 [fix('R2562',sub('R2562',(',10),',',R2560),')),'R2562:Z2562 (copy right)')],
 'Row 2560 is each decile\'s % of population (from the survey individuals, row 2572); row 2561 the cumulative share.',
 'Targeted transfer shares by decile; Egypt: the targeted transfer in deciles 1-4 moves by up to 0.13 points of consumption (all distribution fixes together). MVP v4.4.',
 'Q2562 (decile 1) is left as is: it gives 0 when the targeted percentile is below decile 1\'s share. The MVP caps every decile with MIN(MAX(percentile - cumulative below, 0), share); to confirm whether Q2562 should become =MIN($Q$2552,Q2560).')

# ---------- D2
assert fx('Q740')==9999 and fx('N740')=='Basket -->'
el=[]
for r0,r1 in ((743,750),(752,765)):
    for r in range(r0,r1+1):
        assert fx(f'P{r}')=='' and fx(f'P{r+58 if r<=750 else r+60}')==''
    el.append(fix(f'P{r0}',sub(f'Q{r0}',('{=','='),('}',''),(f'$L{r0}&Q$741',f'SUBSTITUTE($L{r0},".dec.",".bkt.")&$Q$740')),
                  f'P{r0}:P{r1} (column P is empty here; ordinary formula, no Ctrl+Shift+Enter)',now=''))
for r0,r1,e0 in ((801,808,743),(812,825,752)):
    el.append(fix(f'P{r0}',sub(f'Q{r0}',(f'^Q{e0}',f'^P{e0}')),f'P{r0}:P{r1} (copy down)',now=''))
pat=re.compile(r'=IF\(AND\(\$I\$225="Yes", \$H(\d+)=\$I\$226, Q\$(\d+)<=\$I\$228\), 0,Q\$(\d+)\*Q\$(\d+)\*Q(\d+)\)$')
pat2=re.compile(r'=Q\$(\d+)\*Q\$(\d+)\*Q(\d+)$')
blocks={}
for r in range(1580,2188):
    if fx(f'G{r}')!='Basket': continue
    f=fx(f'Q{r}'); m=pat.match(f) or pat2.match(f)
    if not m:
        assert re.fullmatch(r'=(Q\d+\+)+Q\d+',f),(r,f); continue   # total rows (sums of the fixed rows)
    g=m.groups(); pr,fr,bs=g[-3:]
    if len(g)==5: assert int(g[0])==r
    blocks.setdefault((pr,fr),[]).append((r,int(bs),f))
fx2=[]
nb=0
for (pr,fr),rows in blocks.items():
    off={bs-r for r,bs,f in rows}; assert len(off)==1 and len(rows)==12,(pr,rows)
    r0,b0,f0=rows[0]; nb+=len(rows)
    fx2.append(fix(f'Q{r0}',f'=Q${pr}*P${fr}*Q{b0}',
        'copy to the other Basket rows of the block: '+', '.join(f'Q{r}' for r,_,_ in rows[1:])+' (the Deciles rows between them stay)',now=f0))
assert len(fx2)==22 and nb==264
bug('D2','Low','Basket uses decile 1\'s elasticity adjustment and exemption test','Distribution C.V (rows 1580-1792) and C.VI (rows 1825-2185), Basket rows, column Q (e.g. Q1607); elasticity rows 743-765, factors 801-825',
 'The Basket rows (G = "Basket") of the direct effects (e.g. Q1607 = IF(AND($I$225="Yes", $H1607=$I$226, Q$1579<=$I$228), 0, Q$772*Q$802*Q916)) sit in column Q, the column of decile 1, so they take decile 1\'s price-elasticity factor (Q$802) and the cooking-fuel exemption test of decile 1 (Q$1579 = 1). The indirect Basket rows (e.g. Q1825 = Q$782*Q$812*Q1214) take decile 1\'s factor too.',
 el+fx2,
 'HH_Elast holds a basket elasticity row per country (code <ISO>.distn.bkt.ove.mean.9999, e.g. EGY row 639; 9999 = Q740); the price changes (rows 771-795) are the same in every decile column, so Q$771 serves the basket.',
 'Basket (all-household) direct and indirect effects only; the decile rows are unchanged. With ExemptMostCook = No (Egypt default) only the elasticity factor changes. MVP v4.4.',
 'New helper column P: basket elasticities P743:P765 and basket factors P801:P825 (column P is empty in rows 740-830). 264 Basket cells in 22 blocks: total rows (e.g. 1796, 2189, 2217) sum them and need no change.')

# ---------- D3
bug('D3','Low','Current spending tests the ASPIRE flag of the targeted transfer','Distribution Q2633:Z2633',
 'Q2633 (per-capita current spending by decile) returns 0 when $I$212 or $I$213 is "No"; I213 is the ASPIRE flag of the targeted transfer type, not of the current spending type (I214).',
 [fix('Q2633',sub('Q2633',('IF(OR($I$212="No", $I$213="No"), 0, ',''),('_preT_tot", ASPIRECODES, 0))), 0)','_preT_tot", ASPIRECODES, 0)), 0)')),'Q2633:Z2633 (copy right)')],
 'The IFERROR(..., 0) already returns 0 when the ASPIRE programme of the current spending type ($Q$2549) is missing.',
 'None for Egypt by default (cash transfer: I213 = "n.a.", so the test passes). Differs when the targeted-transfer type has no ASPIRE data but current spending does, or the reverse. MVP v4.4.',
 'The MVP drops the flag (register: "no flag; the ASPIRE programme of the chosen type, 0 if absent"); the alternative is to replace $I$213 by $I$214. To confirm.')

# ---------- D4
d4=[]
for r in (2701,2702,2703,2705,2706,2707):
    f=fx(f'Q{r}'); m=re.fullmatch(r'=IF\(OR\(\$Q\$2553=0, \$Q\$2552=0\), 0, (.+)\)',f); assert m,f
    d4.append(fix(f'Q{r}','='+m.group(1),f'Q{r}:Z{r} (copy right)'))
bug('D4','Low','Public investment and current spending vanish with the transfer settings','Distribution rows 2701-2703, 2705-2707',
 'The chart rows of public investment (2701-2703) and current spending (2705-2707) are wrapped in IF(OR($Q$2553=0, $Q$2552=0), 0, ...): they are 0 whenever the targeted-transfer coverage (Q2553) or percentile (Q2552) is 0.',
 d4,'Rows 2610-2612 (public investment per capita) and 2645 (current spending per capita) do not depend on the transfer settings.',
 'None when coverage and percentile are positive (Egypt default). Otherwise public investment and current spending gains now show. MVP v4.4.',
 'The median flags (rows 2685-2687) still read row 2679, which is 0 when coverage or percentile is 0: with the median statistic these rows stay 0 (legacy behaviour kept).')

# ---------- D5
d5=[fix('Q2749',sub('Q2749',('<$I$154','<$I$163'),('MAX($I$154-','MAX($I$163-')),'single cell (Q differs from R:Z)'),
    fix('R2749',sub('R2749',('<$I$154','<$I$163'),('MAX($I$154-','MAX($I$163-')),'R2749:Z2749 (copy right)')]
for r,u in ((2764,2728),(2765,2729)):
    d5.append(fix(f'Q{r}',sub(f'Q{r}',(f'Q$2760*Q{u}/Q2727','Q$2760')),f'Q{r}:Z{r} (copy right)'))
bug('D5','Low','Targeted exemption capped by all revenue; urban and rural not per capita','Distribution Q2749:Z2749, Q2764:Z2765',
 'Q2749:Z2749 cap the cumulative targeted PIT exemption by all carbon-pricing revenue ($I$154) instead of the share recycled through PIT ($I$163, the cap used by the checks in P2743 and P2754). Q2764:Z2765 multiply the per-capita exemption (Q2760 = Q2751/Q2727) by urban or rural individuals / overall individuals, so the urban and rural values are no longer per capita.',
 d5,'I163 = I154 x EXPLabortax; the personal-allowance and proportional rows (2758-2759) are already used per capita in every sample.',
 'None for Egypt by default (PIT type Personal Allowance). With Targeted Exemption the PIT gain is capped at the PIT revenue and urban/rural gains are per capita. MVP v4.4.')

# ---------- D6
d6=[fix('Q3259',sub('Q3259',('$Q$3254:$Z$3254','$Q$3258:$Z$3258')),'Q3259:Z3259 (copy right)'),
    fix('Q3263',sub('Q3263',('$Q$3254:$Z$3254','$Q$3262:$Z$3262')),'Q3263:Z3263 (copy right)')]
bug('D6','Low','Urban and rural compensation shares on overall weights','Distribution Q3259:Z3259, Q3263:Z3263',
 'The urban (3259) and rural (3263) shares of revenue needed to compensate each decile divide by SUMPRODUCT(sample effect, overall consumption shares $Q$3254:$Z$3254) while the numerator uses the sample\'s own shares (3258, 3262), so they sum to about 52 and 47 instead of 100.',
 d6,'Rows 3258 and 3262 are the urban and rural consumption shares; the overall row 3255 uses its own row 3254.',
 'Urban and rural compensation shares (and cumulative rows 3269-3271) each sum to 100; the largest change in Egypt among the distribution fixes. MVP v4.4.')

# ---------- D7
d7=[fix('Q859',sub('Q859',('*Q771','')),'Q859:Z866 (copy right and down)'),
    fix('Q870',sub('Q870',('*Q782','')),'Q870:Z883 (copy right and down; row 883, tpu, is empty today and is filled too)')]
for r in list(range(859,867))+list(range(870,883)):
    for c in COLS: assert fx(f'{c}{r}')==f'=IF(DWLs="Yes", 0.5*(1-$I$145)*{c}{r-88 if r<867 else r-88}, 0)',(c,r)
assert fx('Q883')==''
ep=re.compile(r'\*([Q-Z])(8[3-5]\d)-\1(8[5-8]\d)\*\(\1\d+>0\)')
eff=[]
for r in range(2826,3016):
    if not ep.search(str(fx(f'Q{r}'))): continue
    for c in COLS: assert ep.search(fx(f'{c}{r}')),(c,r)
    eff.append(r)
grp=[]
for r in eff:
    if grp and r==grp[-1][-1]+1: grp[-1].append(r)
    else: grp.append([r])
for g in grp:
    f=fx(f'Q{g[0]}'); arr=f.startswith('{')
    eff_new=ep.sub(lambda m:f'*({m.group(1)}{m.group(2)}+{m.group(1)}{m.group(3)})',f,count=1)
    d7.append(fix(f'Q{g[0]}',eff_new,f'Q{g[0]}:Z{g[-1]} (copy right and down'+('; array formulas: enter each cell with Ctrl+Shift+Enter, or as ordinary formulas)' if arr else ')')))
assert [g[0] for g in grp]==[2828,2846,2920,2930,2989,2999],[g[0] for g in grp]
bug('D7','Low','Deadweight loss in mixed units','Distribution rows 859-883 (DWL factors) and the effect rows 2828-2835, 2846-2859, 2920-2927, 2930-2943, 2989-2996, 2999-3012',
 'Rows 859-882 = IF(DWLs="Yes", 0.5*(1-$I$145)*price change, 0), a fraction of the price, and the effect rows subtract it from the effect in % of consumption (Q2828 = effect*(-1)*Q830 - Q859*(Q2799>0)); the transport row 883 is empty.',
 d7,'Row 830-854 = behavioural factor ($I$145 when InferredDist); DWLTri = 0.5 (the triangle). The MVP loss = effect x (factor + DWLTri x (1 - factor)).',
 'None by default (DWLs = No). With DWLs on, the deadweight loss is 0.5 x (1 - factor) x the effect in % of consumption. MVP v4.4.',
 'The (budget share > 0) test is dropped: the effect is already 0 without spending.')

# ---------- D8
bug('D8','Low','Analysis year and statistic read MTInputs column D','MTOutputs K1001:K1002',
 'K1001 (dist.year) = MTInputs!$D$304 and K1002 (dist.stat) = MTInputs!$D$319: column D is the MT scenario column, 0 in dashboard mode; the Distribution sheet uses the active values YearDistn (MTInputs!F304) and QuantilesStatistic (F319).',
 [fix('K1001','=YearDistn','single cell',sh='MTOutputs'),fix('K1002','=QuantilesStatistic','single cell',sh='MTOutputs')],
 'Distribution I133 (=YearDistn) and I138 (=QuantilesStatistic).',
 'MT outputs dist.year and dist.stat show the analysis year and statistic actually used, also in dashboard mode. MVP v4.4.')

# ---------- D9
assert fx('H2417')==fx('H2416') and fx('H2422')==fx('H2421') and fx('Q2417')=='=Q2402-Q2407' and fx('Q2422')=='=Q2402-Q2407+Q2412'
assert fx('H746')=='oil' and fx('G746')=='=$H746&"_elasticity"' and fx('H774')=='oop' and fx('H804')=='oop'
bug('D9','Low','Rural rows labelled Urban; fuel code oil vs oop',"Distribution H2417, H2422; C.II row 746",
 'H2417 and H2422 read "... - Urban Sample" on rows computed from the rural rows (Q2417 = Q2402-Q2407, Q2422 = Q2402-Q2407+Q2412). The elasticity row 746 has code "oil" while its price rows 774 and 804 have "oop"; they are paired by row position only.',
 [fix('H2417',fx('H2417').replace('Urban Sample','Rural Sample'),'label'),
  fix('H2422',fx('H2422').replace('Urban Sample','Rural Sample'),'label'),
  fix('G746','oil_elasticity','constant (the HH_Elast column header, PELCategories), as G752:G765'),
  fix('H746','oop','constant, after G746')],
 'HH_Elast column M is "oil_elasticity"; rows 774 and 804 carry "oop".',
 'None (labels and codes only; the values are unchanged).',
 'G746 must become a constant before H746 changes, or K746 (MATCH of G746 in PELCategories) fails. The MVP pairs rural and urban rows and the oil rows by key; legacy keeps pairing by position.')

out=os.path.join(S,'parts','part_E.json')
json.dump(A,open(out,'w'),indent=1)
print(len(A),sum(len(b['fixes']) for b in A))
for b in A: print(b['id'],len(b['fixes']),b['status'])
