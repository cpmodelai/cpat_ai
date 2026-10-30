import pickle,json,re,sys
from openpyxl.utils import column_index_from_string as ci, get_column_letter as L
F=pickle.load(open('f.pkl','rb')); FO=pickle.load(open('fo.pkl','rb'))
CN=json.load(open('cellnames.json')); CV=pickle.load(open('cv.pkl','rb'))
def raw(a,sh='Mitigation'):
    if sh=='Mitigation':
        c,r=re.match(r'([A-Z]+)(\d+)',a).groups(); v=F[int(r)][ci(c)-1]
    else: v=FO[sh].get(a)
    return getattr(v,'text',v)
def cur(a,sh='Mitigation'):
    v=raw(a,sh)
    if not isinstance(v,str): return repr(v) if v is not None else None
    nm=CN.get(sh,{}).get(a,[])
    k=v.count('#NAME?')
    if k:
        assert k==len(nm),(sh,a,v,nm)
        for n in nm: v=v.replace('#NAME?',n,1)
    return v
def val(a,sh='Mitigation'): return CV[sh].get(a)
if __name__=='__main__':
    sh='Mitigation'; args=sys.argv[1:]
    if args[0] in FO or args[0]=='Mitigation': sh=args.pop(0)
    for spec in args[0].split(','):
        m=re.match(r'([A-Z]+):([A-Z]+)(\d+)(?:-(\d+))?$',spec)
        c0,c1,r0,r1=m.group(1),m.group(2),int(m.group(3)),int(m.group(4) or m.group(3))
        for r in range(r0,r1+1):
            out=[]
            for c in range(ci(c0),ci(c1)+1):
                a=f'{L(c)}{r}'; f=cur(a,sh)
                if f is not None: out.append(f'{a}={f} [{val(a,sh)}]' if isinstance(f,str) and f.startswith('=') else f'{a}={f}')
            print(r,' | '.join(out))
