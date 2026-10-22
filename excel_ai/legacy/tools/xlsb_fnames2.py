import zipfile,struct,re,sys,json
from openpyxl.utils import get_column_letter as L
p='/home/user/CPAT-AI-Local/excel_ai/legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb'
z=zipfile.ZipFile(p)
exec(open('names.py').read().split("def sh(ix)")[0].split("z=zipfile.ZipFile(p)")[1].replace("b=z.read","b=z.read",1)) if False else None
b=z.read('xl/workbook.bin')
def recs(b):
    i=0
    while i<len(b):
        t=b[i]; i+=1
        if t&0x80: t=(t&0x7f)|((b[i]&0x7f)<<7); i+=1
        sz=0;sh=0
        for _ in range(4):
            x=b[i]; i+=1; sz|=(x&0x7f)<<sh; sh+=7
            if not x&0x80: break
        yield t,b[i:i+sz]; i+=sz
def wstr(d,o):
    n=struct.unpack_from('<I',d,o)[0]; return d[o+4:o+4+2*n].decode('utf-16le'),o+4+2*n
sheets=[];rids=[];names=[]
for t,d in recs(b):
    if t==156:
        o=8; rid,o=wstr(d,o); nm,o=wstr(d,o); sheets.append(nm); rids.append(rid)
    elif t==39:
        o=5; itab=struct.unpack_from('<i',d,o)[0]; o+=4; nm,o=wstr(d,o); names.append((nm,itab))
rels=dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"',z.read('xl/_rels/workbook.bin.rels').decode()))
SZ={0x01:4,0x02:4,0x17:None,0x19:None,0x1C:1,0x1D:1,0x1E:2,0x1F:8,0x20:14,0x21:2,0x22:3,0x23:4,0x24:6,0x25:12,0x26:6,0x27:6,0x28:6,0x29:2,0x2A:6,0x2B:12,0x2C:6,0x2D:12,0x39:6,0x3A:8,0x3B:14,0x3C:8,0x3D:14}
def ptgnames(r):
    out=[];i=0
    while i<len(r):
        pt=r[i]; i+=1
        if 0x03<=pt<=0x16: continue
        base=pt if pt<0x20 else ((pt&0x1f)|0x20)
        if base==0x17:
            n=struct.unpack_from('<H',r,i)[0]; i+=2+2*n; continue
        if base==0x19:
            sub=r[i]; i+=1
            if sub&0x04:
                n=struct.unpack_from('<H',r,i)[0]; i+=2+2*(n+1)
            else: i+=2
            continue
        if base==0x18:
            e=r[i]; i+=1
            if e==0x19: i+=12; continue
            return out+['?ext%x'%e]
        if base not in SZ: return out+['?ptg%x'%pt]
        if base==0x23:
            ix=struct.unpack_from('<I',r,i)[0]; out.append(names[ix-1][0] if 0<ix<=len(names) else f'?n{ix}')
        if base==0x39:
            ix=struct.unpack_from('<I',r,i+2)[0]; out.append(f'X{ix}')
        i+=SZ[base]
    return out
want=sys.argv[1:]
res={}
for sname in want:
    k=sheets.index(sname); fn='xl/'+rels[rids[k]]
    d=z.read(fn); row=0; shr=[]; cells={}
    for t,dd in recs(d):
        if t==0: row=struct.unpack_from('<I',dd,0)[0]
        elif t in (8,9,10,11):
            col=struct.unpack_from('<I',dd,0)[0]; o=8
            if t==8: n=struct.unpack_from('<I',dd,o)[0]; o+=4+2*n
            elif t==9: o+=8
            else: o+=1
            o+=2; cce=struct.unpack_from('<I',dd,o)[0]; rg=dd[o+4:o+4+cce]
            cells[(row,col)]=rg
        elif t==427:
            r1,r2,c1,c2=struct.unpack_from('<iiii',dd,0); cce=struct.unpack_from('<I',dd,16)[0]
            shr.append((r1,r2,c1,c2,dd[20:20+cce]))
        elif t==426:
            r1,r2,c1,c2=struct.unpack_from('<iiii',dd,0); o=16+1; cce=struct.unpack_from('<I',dd,o)[0]
            shr.append((r1,r2,c1,c2,dd[o+4:o+4+cce]))
    SH={}
    for r1,r2,c1,c2,srg in shr:
        for rr in range(r1,r2+1):
            for cc in range(c1,c2+1): SH.setdefault((rr,cc),srg)
    out={}
    for (r,c),rg in cells.items():
        if rg and rg[0]==0x01:
            rg=SH.get((r,c),rg)
        try: nm=ptgnames(rg)
        except Exception as e: nm=['?err']
        if nm: out[f'{L(c+1)}{r+1}']=nm
    res[sname]=out
    print(sname,len(cells),len(out),len(shr))
json.dump(res,open('cellnames.json','w'))
