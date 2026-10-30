"""Legacy 456 formulas with defined names restored.
CLI: python3 q.py "Sheet" ROWS COLS   e.g.  python3 q.py Mitigation 2590-2595 A:P   |  python3 q.py "Manual inputs" 54 P:X
Lib: from q import fx; fx('Mitigation','L2595')"""
import pickle,json,re,sys
from openpyxl.utils import get_column_letter as L, column_index_from_string as ci
_F=pickle.load(open(__file__.replace('q.py','f.pkl'),'rb'))
_O=pickle.load(open(__file__.replace('q.py','other.pkl'),'rb'))
_N=json.load(open(__file__.replace('q.py','cellnames.json')))
def raw(sheet,a):
    c,r=re.match(r'\$?([A-Z]+)\$?(\d+)',a).groups()
    if sheet=='Mitigation':
        r=int(r); return _F[r][ci(c)-1] if r in _F and ci(c)<=len(_F[r]) else None
    return _O[sheet].get(f'{c}{r}')
def fx(sheet,a):
    x=raw(sheet,a)
    if not isinstance(x,str): return x
    for n in _N.get(sheet,{}).get(a,[]):
        if '#NAME?' in x: x=x.replace('#NAME?',n,1)
    return x.replace('( ','(').replace(' )',')') if False else x
if __name__=='__main__':
    sheet=sys.argv[1]; c0,c1=[ci(x) for x in sys.argv[3].split(':')]
    for spec in sys.argv[2].split(','):
        a,b=(spec.split('-')+[spec])[:2]
        for r in range(int(a),int(b)+1):
            out=[f'{L(c)}={fx(sheet,L(c)+str(r))!r}' for c in range(c0,c1+1) if raw(sheet,L(c)+str(r)) not in (None,'')]
            print(r,' | '.join(out))
