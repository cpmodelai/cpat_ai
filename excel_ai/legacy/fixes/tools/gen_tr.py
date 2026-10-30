import pickle,json,re
F=pickle.load(open('f.pkl','rb'))
from openpyxl.utils import column_index_from_string as ci
def cur(a):
    c,r=re.match(r'([A-Z]+)(\d+)',a).groups(); v=F[int(r)][ci(c)-1]
    return v if isinstance(v,str) else repr(v)
def bal(f):
    d=0
    for ch in f:
        d+=(ch=='(')-(ch==')'); assert d>=0,f
    assert d==0,f; return f
def sub(a,*pairs):
    f=cur(a)
    for o,n in pairs:
        assert o in f,(a,o,f); f=f.replace(o,n)
    return bal(f)
def pol(fill,cell):
    rng=fill.split(" ")[0] if fill[0].isupper() and fill[1:2].isupper() or re.match(r"[A-Z]+\d",fill) else cell
    if ':' in rng:
        a,b=rng.split(':'); ca,ra=re.match(r'([A-Z]+)(\d+)',a).groups(); cb,rb=re.match(r'([A-Z]+)(\d+)',b).groups()
        return f'paste into {ca}{int(ra)+6331}:{cb}{int(rb)+6331} (+6,331)'
    c,r=re.match(r'([A-Z]+)(\d+)',rng).groups(); return f'paste into {c}{int(r)+6331} (+6,331)'
def fx(cell,new,fill,policy=None,now=None):
    return dict(cell=cell,now=now if now is not None else cur(cell),new=bal(new),fill=fill,policy=policy or pol(fill,cell))
B=[]
def bug(id,pri,sid,title,where,why,fixes,ref,effect,note=None):
    B.append(dict(id=id,pri=pri,title=f'{title} (survey {sid})',where=where,why=why,fixes=fixes,ref=ref,effect=effect,note=note,status='fix'))
EG='Egypt engineer baseline 2035 (legacy inputs, TrModel = Engineer): '
NONE='None in the Egypt engineer run (the policy or fuel is zero there).'
LD='MATCH($E$2089,$L$2033:$AE$2033,0)'
# ---- Medium
bug('L27','Medium','B3','Vehicle ownership calibration only scales up (and uses 2024)','Mitigation H4787:J4787, H4903:J4903',
 'J = MAX(1, actual/expected), so a country below its Gompertz curve (Egypt: actual 57.8 against 138.9) is never scaled down; H and I read column N (2024) although the data run to 2025.',
 [fx('H4787',f'= INDEX($L4783:$AE4783,{LD}) * EXP(-5.897 * EXP(INDEX($L4784:$AE4784,{LD}) * $T4323 / 1000))','single cell'),
  fx('I4787',f'= INDEX($L4761:$AE4761,{LD}) + INDEX($L4742:$AE4742,{LD})','single cell'),
  fx('J4787','= I4787 / H4787','single cell'),
  fx('H4903',f'= INDEX($L4899:$AE4899,{LD}) * EXP(-5.897 * EXP(INDEX($L4900:$AE4900,{LD}) * $U4323 / 1000))','single cell'),
  fx('I4903',f'= INDEX($L4886:$AE4886,{LD}) + INDEX($L4876:$AE4876,{LD})','single cell'),
  fx('J4903','= I4903 / H4903','single cell')],
 'E2089 ("Data available" = last year with passenger data, 2025) and the year row 2033, both legacy rows. The same calibration ratio applied in both directions.',
 EG+'gasoline -33.9%, diesel -37.9%, road electricity -52.4%, passenger EV sales share -2.6 points.')
bug('L28','Medium','B3b','Freight-share cap and 2-3 wheeler peak use 2024','Mitigation J2168 (new helper), L2168:AE2168, J2169 (above the scenario blocks)',
 'The freight-share cap reads $N2168 and the 2-3 wheeler peak J2169 reads N444 and N2129: column N (2024) is hardcoded although data run to 2025.',
 [fx('J2168',f'=INDEX($L2108:$AE2108,{LD}) / (INDEX($L2036:$AE2036,{LD}) + INDEX($L2037:$AE2037,{LD}))','single cell (empty today; helper = freight share at the last data year)','none (above the scenario blocks)',now='(empty)'),
  fx('L2168',sub('L2168',('$N2168','$J2168')),'L2168:AE2168','none (above the scenario blocks)'),
  fx('J2169',f'=(1 + (1-INDEX($L444:$AE444,{LD})/H2169) * I2169) * INDEX($L2129:$AE2129,{LD})','single cell','none (above the scenario blocks)')],
 'E2089 (last data year). A helper in J2168 avoids L2168:AE2168 pointing into its own row.',
 EG+'road electricity -0.6%, passenger EV sales share -0.1 points.')
bug('L30','Medium','B6','Bus fuel scaled by the wrong rows','Mitigation rows 5310-5314, 5318',
 'Rows 5310-5313 (labelled gasoline, diesel, LPG, gas passenger fuel use) read rows 5191-5194 (LPG, gas, PHEV VKT and a blank row); 5314 (labelled passenger electricity) reads BEV vehicles (5219). Row 5318 adds base bus energy in liters and kWh.',
 [fx('L5310','=L5195/$E5310*10^9','L5310:AE5310'),fx('L5311','=L5196/$E5311*10^9','L5311:AE5311'),
  fx('L5312','=L5197/$E5312*10^9','L5312:AE5312'),fx('L5313','=L5198/$E5313*10^9','L5313:AE5313'),
  fx('L5314','=L5223*10^3/_conv_ktoe_to_gwh','L5314:AE5314'),
  fx('L5318','= SUM($L5306:$L5309)*_conv_ktoe_to_gwh/10^3 * L5314 / SUM($L5310:$L5314)','L5318:AE5318')],
 'Column D of rows 5310-5314 already names the intended rows (=D5195 ... =D5198, =D5223); column F says ktoe. Rows 5195-5198 are passenger fuel use in bln liters, 5223 passenger electricity in bln kWh.',
 EG+'diesel -0.3%, road electricity -16.8%.')
bug('L31','Medium','B6b','Bus share grossed up as x(1+share)','Mitigation O5171:O5173',
 'The bus share of fuel use (column M) is added to the bottom-up use as x(1 + share); a share of the total needs /(1 - share).',
 [fx(f'O{r}',sub(f'O{r}',(f'(1 + M{r})',f'/ (1 - M{r})'),('* 10^9 * /','* 10^9 /')),'single cell') for r in (5171,5172,5173)],
 'Column header M5169 "Share for buses" (a share of the total).',EG+'road electricity -0.3%.')
bug('L33','Medium','B8','Wrong elasticities and rows in freight and 2-3 wheeler distance','Mitigation rows 5232, 5261, 5295 (and L4646, see L34)',
 'LPG freight VKT reads row 5126 instead of the freight VKT row 5230; BEV freight VKT uses the 2-3 wheeler income elasticity $L4330; BEV 2-3 wheeler VKT uses the cost ratio M5292 twice and no income term.',
 [fx('L5232',sub('L5232',('L5126','L5230')),'L5232:AE5232'),
  fx('L5261',sub('L5261',('$L4330','$K4330')),'L5261:AE5261'),
  fx('L5295',sub('L5295',('L5292 ^ $L4330','L5158 ^ $L4330')),'L5295:AE5295')],
 'Sibling rows 5231/5233 (base row 5230), 5231 ($K4330 for freight) and 5273 (2-3 wheeler gasoline: income term M5158 ^ $L4330).',EG+'diesel -0.2%, road electricity +4.0%.')
fr=[fx('L4646',sub('L4646',('$K4329','L4531')),'L4646 only (M4646:AE4646 already read row 4531)')]
for r in (4628,4630,4648,4670,4672):
    fr.append(fx(f'L{r}',sub(f'L{r}',('$K4329','L4531')),f'L{r}:AE{r}'))
bug('L34','Medium','B8w','Freight discounted at the power-sector WACC','Mitigation rows 4628, 4630, 4646, 4648, 4670, 4672',
 'Freight TCO rows discount at $K4329 = AVERAGE(I2988:I2996), the power-sector cost of capital; passenger rows use the consumer discount rate row 4531, and freight depreciation 4646 already switches to it from 2023.',
 fr,'Passenger rows (e.g. 4573, 4598) and M4646:AE4646, which use the year\'s consumer discount rate (row 4531).',EG+'diesel +0.2%, road electricity -1.0%.')
bug('L35','Medium','B9','Negative PHEV sales share','Mitigation rows 4846-4850',
 'PHEV share = passenger PHEV+BEV share (4845) minus the blended passenger/light BEV share (4805): negative for Egypt (-0.07% in 2022).',
 [fx('L4850','=MAX(0,L2063-L2065)*L2038','L4850:O4850 (data years)'),
  fx('P4850',sub('P4850',('P4845 - P4805','MAX(0,P2063-P2065)*P2038')),'P4850:AE4850 (only the data branch changes)'),
  *[fx(f'L{r}',sub(f'L{r}',(f'(1 - L4845)','(1 - L4805 - L4850)')),f'L{r}:O{r}') for r in (4846,4847,4848,4849)]],
 'Rows 2063 (PHEV+BEV passenger share), 2065 (BEV passenger share) and 2038 (passenger share of passenger/light).',EG+'diesel +0.1%, road electricity +0.2%.')
bug('L37','Medium','B19','New BEV maintenance at the ICEV rate','Mitigation row 4573',
 'BEV insurance and maintenance uses $J4327 (ICEV maintenance) instead of $J4328 (EV maintenance).',
 [fx('L4573',sub('L4573',('$J4327','$J4328')),'L4573:AE4573')],'Parameter table: J4327 ICEV, J4328 EV maintenance.',EG+'gasoline -0.1%, road electricity +1.2%, passenger EV sales share +0.5 points.')
bug('L38','Medium','B20','Used ICEV and BEV depreciation over different periods','Mitigation row 4598',
 'Used ICEV depreciation is an annuity over $J4322-1 (6) years, the used BEV over 12 ($J4323-1).',
 [fx('L4598',sub('L4598',('$J4322','$J4323')),'L4598:AE4598')],'Row 4600 (used ICEV insurance) and the used BEV rows, which use $J4323 ("Used vehicle useful life").',
 EG+'gasoline +5.1%, diesel +3.1%, road electricity -50.7%, passenger EV sales share -10.0 points.')
# ---- Low
bug('L25','Low','B1','Distance tax and 2-3 wheeler EV subsidy apply in the baseline','Mitigation rows 4451, 4720',
 'The scenario test is ($C2227 > 1); C2227 is the text "res" and text > number is TRUE, so both policies are on in the baseline.',
 [fx('L4451',sub('L4451',('$C2227','$C2173')),'L4451:AE4451'),fx('L4720',sub('L4720',('$C2227','$C2173')),'L4720:AE4720')],
 'C2173 = scenario number (used by e.g. row 4343, IF($C2173 = 1, 0, ...)).',NONE)
bug('L26','Low','B2','Freight and 2-3 wheeler income growth read coal subsidies from 2038','Mitigation row 4487 (4501 follows)',
 'L4487:AA4487 = row 4463 (lagged GDP growth); AB4487:AE4487 = row 2455 (coal producer-side subsidies).',
 [fx('AB4487','=AB4463','AB4487:AE4487')],'L4487:AA4487 (= the same column of row 4463).',NONE)
bug('L29','Low','B4','Ownership of cars and trucks cannot fall','Mitigation T4328, U4328',
 'The maximum annual decrease of ownership is 0 for passenger and freight (Dashboard L555), so ownership never falls; 2-3 wheelers have 10% (V4328 = Dashboard L556).',
 [fx('T4328','=$V4328','single cell'),fx('U4328','=$V4328','single cell')],'V4328 (2-3 wheelers, 10%).',NONE)
bug('L32','Low','B7','Industry emission factors for road diesel and LPG','Mitigation G4376-G4378, G4419-G4421',
 'The defined names in these cells point to the wrong rows of the EF table: _ef_co2_ker_ind_lit = O1004 (diesel industry), _ef_co2_jet_avi_lit = O1005 (LPG industry), _ef_co2_die_pow_lit = O995 (gas residential, per GJ).',
 [fx('G4376','=$O$990*$E$2147','single cell'),fx('G4377','=$O$991','single cell'),fx('G4378','=$O$988/26','single cell'),
  fx('G4419','=$O$990*$E$2147','single cell'),fx('G4420','=$O$991','single cell'),fx('G4421','=$O$988/26','single cell')],
 'Road rows of the EF table: O990 diesel road, O991 LPG road, O988 natural gas road; G4375 (gasoline) already uses the road row (O989). Rows 5196-5198 and 5243-5245 take these cells.',
 'Diesel road EF 0.002679 to 0.002641 t/l (-1.4%); LPG and gas unchanged in value. '+NONE)
bug('L36','Low','B10','Charging-station subsidy ramp','Mitigation row 4343; Dashboard C95:C98 labels',
 'The ramp adds a step every year from the first column (also before the start year) and is only capped at 1, not at the target level after the target year. The Dashboard labels of rows 95-98 do not match how the inputs are used (values: G97 = 2026, G98 = 2035 are the years).',
 [fx('L4343','= IF( $C2173 = 1, 0, IF( L4334 < $P4317, 0, IF( L4334 >= $P4318, $P4316, $P4315 + ($P4316 - $P4315) * (L4334 - $P4317) / ($P4318 - $P4317))))','L4343:AE4343')],
 'P4315 start level, P4316 target level, P4317 start year, P4318 target year (as the formula and the default values use them).',NONE,
 note='Also relabel Dashboard C95 "start level", C96 "target level", C97 "start year", C98 "target year" (the M4315:M4318 labels read from there).')
bug('L39','Low','B21','Freight distance output omits LPG and LNG trucks','Mitigation row 5267',
 'All-freight VKT sums SUM(5239:5239) (diesel only) plus BEV.',
 [fx('L5267',sub('L5267',('L5239:L5239','L5239:L5241')),'L5267:AE5267')],'Rows 5239-5241 (diesel, LPG, gas freight VKT).',NONE)
bug('L40','Low','B22','Wrong rows in average gas and EV fuel economy','Mitigation rows 5368, 5373',
 'Average gas fuel economy weights freight by LPG freight fuel (5244) instead of LNG (5245); the EV fallback tests diesel use (5326) instead of electricity (5330).',
 [fx('L5368',sub('L5368',('L5244','L5245')),'L5368:AE5368'),fx('L5373',sub('L5373',('L5326 = 0','L5330 = 0')),'L5373:AE5373')],
 'Row 5324 (gas = 5198 + 5245 + 5317) and row 5330 (electricity, all).',NONE)
bug('L41','Low','B23','PHEVs carry the full BEV range anxiety','Mitigation row 4555',
 'PHEV TCO adds row 4579 (BEV range anxiety, about 100,000 $/vehicle), so PHEV sales vanish.',
 [fx('L4555',sub('L4555',(' + L4579','')),'L4555:AE4555')],'Rows 4551-4554 (ICE TCOs, no range anxiety). User decision 2026-10-14: PHEVs refuel with gasoline.',NONE)
json.dump(B,open('doc/partT.json','w'),indent=1)
print(len(B),sum(len(b['fixes']) for b in B))
for b in B:
    for f in b['fixes']: print(f['cell'],'|',f['new'][:150])
