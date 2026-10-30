import pickle,sys
from openpyxl.formula.translate import Translator
from openpyxl.utils import get_column_letter as L
F=pickle.load(open('f.pkl','rb'))
def f(r,c):
    v=F[r][c-1]; return getattr(v,'text',v)
pol='-p' in sys.argv
for spec in sys.argv[1].split(','):
    a,b=(spec.split('-')+[spec])[:2]
    for r in range(int(a),int(b)+1):
      for off in ((0,6331) if pol else (0,)):
        rr=r+off
        lab=' '.join(str(f(rr,c)) for c in (2,3,4) if f(rr,c) not in (None,''))[:70]
        norms={}
        for c in range(11,32):
            x=f(rr,c)
            if x in (None,''): continue
            if not isinstance(x,str) or not x.startswith('='): norms.setdefault(repr(x),[]).append(L(c)); continue
            try: n=Translator(x,origin=f"{L(c)}{rr}").translate_formula(f"M{r}")
            except Exception: n='?'+x
            norms.setdefault(n,[]).append(L(c))
        g=' || '.join(f"[{v[0]}..{v[-1]}] {k}" for k,v in norms.items())
        print(f"{rr} {lab} :: {g}"[:900])
