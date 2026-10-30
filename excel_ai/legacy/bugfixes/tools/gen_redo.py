# 2026-10-19: L48 and L50 redone from the .xlsb (dec_cells.py); L112 and new bugs L115-L117 added (user request).
import json,sys,os
sys.path.insert(0,os.path.dirname(__file__)); sys.argv=['x']
import dec_cells as d
C={}
def now(a,sh='Mitigation'):
    if sh not in C: C[sh]=d.raw_all(sh)
    return d.getf(*C[sh],a)
def sub(a,pairs,sh='Mitigation'):
    f=now(a,sh)
    for o,n in pairs: assert o in f,(a,o,f); f=f.replace(o,n)
    return f
fx=lambda cell,new,fill,policy,nw=None,sh='Mitigation':dict(cell=cell if sh=='Mitigation' else f"{sh}!{cell}",now=nw if nw is not None else now(cell,sh),new=new,fill=fill,policy=policy)
p='../data/fixes_other_mitigation.json'; A=json.load(open(os.path.join(os.path.dirname(__file__),p)))
for b in A:
    if b['id']=='L48':
        b['title']='Residential initially-exempt rows: no income factor; starred "Yes*" exemption test'
        b['where']='Mitigation rows 5546-5547, 5568-5570'
        b['why']=('The exemption split itself works: L5564:L5566 = IFNA(IF($L$1784=B,(1-$K$1795)*base, base), base) and L5568:L5570 = IFNA(IF($L$1784=B, $K$1795*base, 0), 0) '
                  '(text read from the .xlsb; the LibreOffice conversion had shown IFNA(0)). It is 0 in the Egypt run only because I1784 = 0 (ExemptMostCook off). '
                  'Two defects remain: the initially-exempt rows M5568:M5570 grow with (1+g)^eps_Y without the income factor M2433 (the not-exempt rows 5564-5566 have it), '
                  'and the AlwaysExemptResLPGKer test in rows 5546-5547 compares with "Yes" while the input list uses "Yes*"/"No*".')
        b['fixes']=[x for x in b['fixes'] if x['cell'] in ('M5568','M5569','M5570','L5546','L5547')]
        for x in b['fixes']: x['now']=now(x['cell'])
        b['note']='Redone from the .xlsb (2026-10-19): the earlier start-row edits of L5564:L5570 were built on converted text and are dropped (the split already exists). M5568:M5570 are also edited by L94 (exponent): apply both substitutions.'
        b['effect']='None in the default Egypt run (ExemptMostCook off; AlwaysExemptResLPGKer No). With ExemptMostCook on, the initially-exempt share grows like the rest; with "Yes*" the exemption applies.'
    if b['id']=='L50':
        b['why']=('(a) The WEO codes <iso>.bca_bp6 and <iso>.bca_gdp_bp6 are not on the WEO sheet (it has <iso>.BCA.A and <iso>.BCA_NGDPD.A), so J18197, J18206, J18213 are #N/A. '
                  '(b) Rows 18197, 18206 and 18213 read INDEX(WEO, ...) and the defined name WEO is empty; the data range is WEO_upd (WEO!C9:AU3333, same rows as WEO_codes). '
                  '(c) With the errors, the IFNA fallback of rows 18197 and 18206 (carry the previous column forward) leaves them empty. (Text read from the .xlsb; the conversion had shown =IFNA(K18197).) '
                  '(d) The "sign looks reversed" in rows 18215-18219 is a label error: rows 741-743 are a trade balance.')
        keep=[x for x in b['fixes'] if x['cell'].startswith('G') or x['cell'].startswith('D')]
        new=[fx('L18197',sub('L18197',[('INDEX(WEO,','INDEX(WEO_upd,')]),'L18197:AE18197 (array formula: edit L, copy across)','none (results block, one copy only)'),
             fx('L18206',sub('L18206',[('INDEX(WEO,','INDEX(WEO_upd,')]),'L18206:AE18206 (array formula: edit L, copy across)','none (results block, one copy only)'),
             fx('L18213',sub('L18213',[('INDEX(WEO,','INDEX(WEO_upd,')]),'L18213:AE18213 (array formula: edit L, copy across)','none (results block, one copy only)')]
        for x in keep: 
            if x['cell'].startswith('G'): x['now']=now(x['cell'])
        b['fixes']=[k for k in keep if k['cell'].startswith('G')]+new+[k for k in keep if k['cell'].startswith('D')]
        b['note']='Redone from the .xlsb (2026-10-19): rows 18197 and 18206 keep legacy\'s carry-forward (the previous column when the WEO year has no value); only the name and the codes change. WEO years beyond the data repeat the last value, as legacy intends.'
json.dump(A,open(os.path.join(os.path.dirname(__file__),p),'w'),indent=1)
p='../data/fixes_other_mitigation_2.json'; B=json.load(open(os.path.join(os.path.dirname(__file__),p)))
B=[b for b in B if b['id'] not in ('L112','L115','L116','L117')]
B.append(dict(id='L112',pri='Medium',title='Policy copies of the shadow-price rows read the baseline carbon price in the regulation term',where='Mitigation rows 8708-8719 (policy copies of 2377-2388)',
 why='The policy copies keep the absolute baseline references $D$2369 (shadow pricing on/off) and L$2375 (general carbon price), so in the policy run the regulation term reads the baseline price (0). Once L87 is fixed, regulations still do nothing in the policy run.',
 fixes=[fx('L8708',sub('L8708',[('$D$2369','$D$8700'),('L$2375','L$8706')]),'L8708:AE8719 (the 12 rows share the pattern: edit L8708, copy down and across; check that the EF code ($G86xx) of each row is kept)','is the policy block itself (rows 8708-8719)')],
 ref='D8700 and row 8706 are the policy copies of D2369 and row 2375 (+6,331). The baseline rows 2377-2388 are right.',
 effect='Regulations act in the policy run once L87 is fixed. None by default (explicit pricing).',note='Apply together with L87 (user 2026-10-19). Registered in v0.5.5 (main).',status='fix'))
B.append(dict(id='L115',pri='Medium',title='Residential gas: current ETS price reads the LPG transport row',where='Mitigation row 2555 (policy 8886)',
 why='Row 2555 ("nga res - in which: current ETS permit price") = K$1720, the effective permit price of LPG in transport/industry; the residential gas row of the ETS table is 1715 (the other blocks read their own row: 2486 = 1712, 2509 = 1713, 2532 = 1714, 2578 = 1716).',
 fixes=[fx('K2555','=K$1715','K2555:AE2555','policy K8886:AE8886: =K$1715 (type, do not paste: row 1715 is shared, above the scenario blocks)')],
 ref='Rows 2486, 2509, 2532, 2578 of the same price blocks; ETS table rows 1711-1723 (C column = sector).',
 effect='Residential gas price includes the LPG permit price instead of its own wherever an existing ETS covers either fuel; none for Egypt (no existing ETS). Found 2026-10-19 while planning L64/L65.',note=None,status='fix'))
B.append(dict(id='L116',pri='Low',title='Services gasoline and diesel income elasticities: step-change column reads the renewables and electricity rows',where='Elasticities H53, H54',
 why='In the services block of Elasticities, G53 = G169 and G54 = G170 (gasoline, diesel), but H53 = H173 (renewables, services) and H54 = H174 (electricity, services); every other row reads its own row (H51 = H167, H52 = H168, H55 = H171, H56 = H172).',
 fixes=[fx('H53','=H169','single cell','none (sheet Elasticities)',sh='Elasticities'),fx('H54','=H170','single cell','none (sheet Elasticities)',sh='Elasticities')],
 ref='Rows 51-56 against 167-174 of the same sheet.',effect='None today (H169, H170, H173, H174 are all 0.13); matters when the regional values differ.',note=None,status='fix'))
B.append(dict(id='L117',pri='Low',title='Transfers multiplier (TRNS): estimated lag-0 table read two rows off',where='Multipliers D44',
 why='D44 reads INDEX(D$1218:D$1418,$D$19) while E44 (and the other lags) read $1220:$1418; rows 1218-1219 are title rows, so lag 0 takes the country two rows up.',
 fixes=[fx('D44',sub('D44',[('D$1218:D$1418','D$1220:D$1418')],sh='Multipliers'),'single cell (array formula: Ctrl+Shift+Enter)','none (sheet Multipliers)',sh='Multipliers')],
 ref='E44:O44 (same row, other lags).',effect='None today (lag 0 of the estimated transfers table is 0 for every country).',note=None,status='fix'))
pr={'High':0,'Medium':1,'Low':2}; B.sort(key=lambda b:(pr.get(b['pri'],3),int(b['id'][1:])))
json.dump(B,open(os.path.join(os.path.dirname(__file__),p),'w'),indent=1)
print('ok',len(A),len(B))
