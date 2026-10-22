import sys,os
name=sys.argv[1]; cols=sys.argv[2].split(',') ; r0=int(sys.argv[3]); r1=int(sys.argv[4])
W=int(os.environ.get('W','160'))
F={};V={}
for fn,D in (('f_',F),('v_',V)):
    try:
        for line in open(fn+name+'.txt'):
            k,v=line.rstrip('\n').split('\t',1); D[k]=v
    except FileNotFoundError: pass
def fv(k):
    vv=V.get(k,'')
    try: return '%.6g'%float(vv)
    except: return vv[:24]
for r in range(r0,r1+1):
    out=[]
    for c in cols:
        k=f'{c}{r}'
        if k in F:
            s=F[k]
            if '=' in s[:6]: s=s[:W]+' =>'+fv(k)
            else: s=s[:W]
            out.append(f'{c}:{s}')
    if out: print(r,' | '.join(out))
