import zipfile,struct
from openpyxl.utils import get_column_letter as L
p='/home/user/CPAT-AI-Local/excel_ai/bugs_and_legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb'
z=zipfile.ZipFile(p); b=z.read('xl/workbook.bin')
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
sheets=[];xti=[];names=[]
def wstr(d,o):
    n=struct.unpack_from('<I',d,o)[0]; return d[o+4:o+4+2*n].decode('utf-16le'),o+4+2*n
for t,d in recs(b):
    if t==156:
        o=8; rid,o=wstr(d,o); nm,o=wstr(d,o); sheets.append(nm)
    elif t==362:
        n=struct.unpack_from('<I',d,0)[0]
        for k in range(n): xti.append(struct.unpack_from('<iii',d,4+12*k))
    elif t==39:
        o=4; o+=1; itab=struct.unpack_from('<i',d,o)[0]; o+=4
        nm,o=wstr(d,o); cce=struct.unpack_from('<I',d,o)[0]; o+=4
        names.append((nm,itab,d[o:o+cce]))
def sh(ix):
    e,f,l=xti[ix]
    if f<0: return f'ext{e}'
    return sheets[f] if f==l else sheets[f]+':'+sheets[l]
def dec(r):
    out=[];i=0
    while i<len(r):
        pt=r[i]
        base=pt&0x1f if pt>=0x20 else pt
        if pt in (0x3A,0x5A,0x7A):
            ix,row,col=struct.unpack_from('<HiH',r,i+1); out.append(f"{sh(ix)}!{L((col&0x3fff)+1)}{row+1}"); i+=9
        elif pt in (0x3B,0x5B,0x7B):
            ix,r1,r2,c1,c2=struct.unpack_from('<HiiHH',r,i+1); out.append(f"{sh(ix)}!{L((c1&0x3fff)+1)}{r1+1}:{L((c2&0x3fff)+1)}{r2+1}"); i+=15
        else:
            out.append(f'<complex {r[i:].hex()[:40]}>'); break
    return ' '.join(out)
with open('names.tsv','w') as f:
    for nm,itab,r in names:
        try: s=dec(r)
        except Exception as e: s='<err>'
        f.write(f'{nm}\t{itab}\t{s}\n')
print(len(names),len(sheets),len(xti))
