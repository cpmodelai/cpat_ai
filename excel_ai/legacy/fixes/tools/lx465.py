"""Legacy 465 (excel_ai/legacy/workbooks, read-only): formulas (defined names kept) and cached values together.
Usage: python3 lx465.py "Sheet" 1825-1840[,6210-6220] [A:L]     (default A:L; Mitigation L = 2022 ... AE = 2041, K = 2021)
Each non-empty cell prints as  COL: formula => cached value  (or the constant)."""
import sys,os,pickle,re
sys.argv_save=sys.argv; sys.argv=[sys.argv[0]]
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
import dec465 as D
sys.argv=sys.argv_save
from openpyxl.utils import get_column_letter as L, column_index_from_string as ci
from pyxlsb import open_workbook
CACHE=os.environ.get('LX465_CACHE','/tmp')
def values(sheet):
    fn=os.path.join(CACHE,'vals_'+re.sub(r'\W','_',sheet)+'.pkl')
    if os.path.exists(fn): return pickle.load(open(fn,'rb'))
    V={}
    with open_workbook(D.p) as wb:
        with wb.get_sheet(sheet) as sh:
            for row in sh.rows():
                for c in row:
                    if c.v is not None: V[(c.r+1,c.c+1)]=c.v
    pickle.dump(V,open(fn,'wb')); return V
if __name__=='__main__':
    sheet=sys.argv[1]; cols=sys.argv[3] if len(sys.argv)>3 else 'A:L'
    c0,c1=[ci(c) for c in cols.split(':')]
    V=values(sheet); cells,SH=D.sheetcells(sheet)
    for spec in sys.argv[2].split(','):
        a,b=(spec.split('-')+[spec])[:2]
        for r in range(int(a),int(b)+1):
            out=[]
            for c in range(c0,c1+1):
                try: f=D.formula(cells,SH,f'{L(c)}{r}')
                except Exception as e: f='ERR'
                v=V.get((r,c))
                if f is None and v is None: continue
                out.append(f'{L(c)}: {f} => {v!r}' if f else f'{L(c)}: {v!r}')
            if out: print(r,' | '.join(out))
