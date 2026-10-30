import pickle,json,re
from openpyxl.utils import column_index_from_string as ci
R=pickle.load(open('orig/bop.pkl','rb'))
def cur(a):
    c,r=re.match(r'([A-Z]+)(\d+)',a).groups(); v=R[int(r)][ci(c)-1]
    return v if isinstance(v,str) else repr(v)
def bal(f):
    d=0
    for ch in f:
        d+=(ch=='(')-(ch==')'); assert d>=0,f
    assert d==0,f; return f
def sub(a,*p):
    f=cur(a)
    for o,n in p: assert o in f,(a,o,f); f=f.replace(o,n)
    return bal(f)
NP='none (results block, one copy only)'
def fx(cell,new,fill,now=None): return dict(cell=cell,now=now if now is not None else cur(cell),new=bal(new) if new.startswith('=') else new,fill=fill,policy=NP)
B=json.load(open('doc/partB.json'))
B=[b for b in B if b['id'] not in ('L49','L50')]
L49=dict(id='L49',pri='Medium',title='Balance of payments: oil without the share traded',where='Mitigation row 18181 (section 11, balance of payments)',
 why='The value of the change in oil net imports is change in use x price, while gas (row 18187, x $H741) and coal (row 18193, x $H743) multiply by the share traded of the trade-balance table (rows 741-743). Oil products have a share of 0.47 (H742), so the oil effect is about twice too large.',
 fixes=[fx('L18181',sub('L18181',('/10^9','/10^9*$H742')),'L18181:AE18181')],
 ref='Rows 18187 (gas) and 18193 (coal) of the same section; H742 = share traded of oil products.',
 effect='Reported balance of payments only: the oil line falls to 47% (Egypt 2028: -1.75 to -0.83 bn USD); rows 18200, 18203, 18207, 18218 follow.',note=None,status='fix')
L50=dict(id='L50',pri='Low',title='Balance of payments: current account #NAME?, column lag, label',where='Mitigation rows 18197, 18206, 18213, 18215-18219',
 why='(a) The WEO codes are <iso>.bca_bp6 and <iso>.bca_gdp_bp6, which the WEO sheet does not have (it has <iso>.BCA.A and <iso>.BCA_NGDPD.A), so J18197, J18206, J18213 are #N/A. (b) Row 18213 reads INDEX(WEO, ...) and the defined name WEO is empty (#NAME?); the data range is WEO_upd. (c) Rows 18197 and 18206 hold no lookup at all: each year repeats the previous column (=IFNA(K18197)), so they stay empty with a one-column lag. (d) The "sign looks reversed" in rows 18215-18219 is a label error: rows 741-743 are a trade balance (row 740 "Trade balance", negative = deficit), and policy = baseline - change in import value is correct for a balance; the labels say net imports.',
 fixes=[fx('G18197','=LOWER(_Country_code)&".bca.a"','single cell'),
        fx('G18213','=LOWER(_Country_code)&".bca.a"','single cell'),
        fx('G18206','=LOWER(_Country_code)&".bca_ngdpd.a"','single cell'),
        fx('L18213','=INDEX(WEO_upd,$J18213,MATCH(L$18212,WEO_years,0))','L18213:AE18213'),
        fx('L18197','=L18213','L18197:AE18197'),
        fx('L18206','=INDEX(WEO_upd,$J18206,MATCH(L$18205,WEO_years,0))','L18206:AE18206'),
        fx('D18215','Baseline (trade balance of oil, gas and coal, USD bln)','label'),
        fx('D18217','Baseline (trade balance of oil, gas and coal, % of GDP)','label'),
        fx('D18218','Policy (trade balance of oil, gas and coal, USD bln)','label'),
        fx('D18219','Policy (trade balance of oil, gas and coal, % of GDP)','label')],
 ref='Row 420 (GDP growth): INDEX(WEO_upd, row, MATCH(year, WEO_years, 0)) with codes <iso>.<WEO subject>.a; sheet WEO holds EGY.BCA.A (current account, USD bn) and EGY.BCA_NGDPD.A (% of GDP). Row 740 heads rows 741-743 as "Trade balance".',
 effect='Reported balance of payments only: the current-account panel (rows 18197-18210) shows values instead of errors; no other result changes. Note: WEO data run to the WEO horizon (2029/2031); later years return #N/A until extended.',note='WEO years beyond the data return #N/A; wrap in IFERROR(...,"") if a blank is preferred.',status='fix')
B.append(L49); B.append(L50)
order={'High':0,'Medium':1,'Low':2,'Low (new)':3}
B.sort(key=lambda b:(order.get(b['pri'],9),))
json.dump(B,open('doc/partB.json','w'),indent=1)
for b in (L49,L50):
    for f in b['fixes']: print(f['cell'],'|',f['now'][:70],'=>',f['new'][:90])
print(len(B),sum(len(b['fixes']) for b in B))
