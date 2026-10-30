# convert formulas to R1C1-ish relative form to find structure changes along a row
import re,sys
from openpyxl.utils import column_index_from_string as ci, get_column_letter as L
F={};V={}
for line in open('f_Mitigation.txt'):
    k,v=line.rstrip('\n').split('\t',1); F[k]=v
for line in open('v_Mitigation.txt'):
    k,v=line.rstrip('\n').split('\t',1); V[k]=v
ref=re.compile(r"(\$?)([A-Z]{1,3})(\$?)(\d+)")
def rel(f,col,row):
    def sub(m):
        c=m.group(2); 
        try: cc=ci(c)
        except: return m.group(0)
        if cc>200: return m.group(0)
        cs = c if m.group(1) else f'C[{cc-col}]'
        rs = m.group(4) if m.group(3) else f'R[{int(m.group(4))-row}]'
        return cs+rs
    return ref.sub(sub,f)
r0,r1=int(sys.argv[1]),int(sys.argv[2])
cols=[L(i) for i in range(12,32)]  # L..AE
for r in range(r0,r1+1):
    d=F.get(f'D{r}',F.get(f'B{r}',''))[:60]
    segs=[];prev=None
    for c in cols:
        f=F.get(f'{c}{r}')
        if f is None: 
            key=None
        else:
            key=rel(f,ci(c),r)
        if key!=prev:
            segs.append((c,f)); prev=key
    if all(f is None for c,f in segs): continue
    if len(segs)>1 or True:
        print(f'{r} [{d}]')
        for c,f in segs:
            if f is None: print(f'   {c}+: (blank)')
            else:
                v=V.get(f'{c}{r}','')
                try: v='%.6g'%float(v)
                except: pass
                print(f'   {c}+: {f[:330]}  => {v[:20]}')
