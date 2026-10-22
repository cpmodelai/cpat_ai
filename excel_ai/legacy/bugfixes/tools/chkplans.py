import json,sys,re
from dec import *
import h   # labels and constants (not formulas) from the LibreOffice cache
C={}
def get(sh,a):
    if sh not in C: C[sh]=sheetcells(sh)
    return formula(*C[sh],a)
for f in sys.argv[1:]:
    d=json.load(open(f)); n=bad=0
    for b in d:
        for x in b['fixes']:
            cell=x['cell']; sh='Mitigation'
            if '!' in cell: sh,cell=cell.split('!'); sh=sh.strip("'")
            if not re.match(r'^[A-Z]+\d+$',cell): print('skip',b['id'],x['cell']); continue
            try: t=get(sh,cell)
            except Exception as e: t='ERR '+str(e)
            n+=1
            if t is None:
                try: t=h.cur(cell,sh)
                except Exception: t=None
                t='(empty)' if t is None else t
            if ' | ' in x['now']: t=t+' | '+x['now'].split(' | ',1)[1]   # several cells described in one entry
            if t!=x['now'] and not (x['now'] in ('(empty)',) and t=='(empty)'):
                bad+=1; print(b['id'],x['cell'],'\n  plan:',x['now'][:200],'\n  xlsb:',str(t)[:200])
    print(f,n,'cells',bad,'differ')
