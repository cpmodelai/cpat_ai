import pickle,sys
from openpyxl.formula.translate import Translator
from openpyxl.utils import get_column_letter as L
F=pickle.load(open('f.pkl','rb'))
def norm(r,target):
    out=[]
    for c in range(12,32):
        x=getattr(F[r][c-1],'text',F[r][c-1])   # array formulas (CSE cells) compare by text
        if isinstance(x,str) and x.startswith('='):
            try: x=Translator(x,origin=f"{L(c)}{r}").translate_formula(f"{L(c)}{target}")
            except Exception: pass
        out.append(x)
    return out
rows=[int(x) for x in sys.argv[1].split(',')]
for r in rows:
    b=norm(r,r); found=[]
    for off in range(6290,6345):
        if norm(r+off,r)==b and any(v not in (None,'') for v in b): found.append(off)
    print(r, str(F[r][3])[:40], 'policy offset', found, 'cols', [L(c) for c in range(12,32) if F[r][c-1] not in (None,'')][:1])
