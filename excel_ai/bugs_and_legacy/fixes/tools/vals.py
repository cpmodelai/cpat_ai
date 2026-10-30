import zipfile,struct,re,sys,pickle
from openpyxl.utils import get_column_letter as L
z=zipfile.ZipFile('legacy/legacy.xlsb')
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
sheets=[];rids=[]
for t,d in recs(z.read('xl/workbook.bin')):
    if t==156:
        o=8; rid,o=wstr(d,o); nm,o=wstr(d,o); sheets.append(nm); rids.append(rid)
rels=dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"',z.read('xl/_rels/workbook.bin.rels').decode()))
# shared strings
sst=[]
try:
    for t,d in recs(z.read('xl/sharedStrings.bin')):
        if t==19: s,_=wstr(d,1); sst.append(s)
except KeyError: pass
def rk(v):
    x=v>>2
    if v&2:
        x = x if x<2**29 else x-2**30
        val=float(x)
    else: val=struct.unpack('<d',struct.pack('<Q',(v&0xfffffffc)<<32))[0]
    return val/100 if v&1 else val
out={}
for sname in sys.argv[1:]:
    k=sheets.index(sname); d=z.read('xl/'+rels[rids[k]]); row=0; V={}
    for t,dd in recs(d):
        if t==0: row=struct.unpack_from('<I',dd,0)[0]
        elif t in (2,5,6,7,8,9,10,11,3,4):
            col=struct.unpack_from('<I',dd,0)[0]; key=f'{L(col+1)}{row+1}'
            if t==2: V[key]=rk(struct.unpack_from('<I',dd,8)[0])
            elif t in (5,9): V[key]=struct.unpack_from('<d',dd,8)[0]
            elif t==7: V[key]=sst[struct.unpack_from('<I',dd,8)[0]]
            elif t in (6,8): V[key]=wstr(dd,8)[0]
            elif t in (4,10): V[key]=bool(dd[8])
            elif t in (3,11): V[key]='#ERR%d'%dd[8]
    out[sname]=V
pickle.dump(out,open('cv.pkl','wb'))
print({k:len(v) for k,v in out.items()})
