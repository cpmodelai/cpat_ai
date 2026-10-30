"""Decode cell formulas straight from the .xlsb (BIFF12 rgce -> text), for cells whose LibreOffice conversion lost
arguments (e.g. _xlfn.XLOOKUP, _xlfn.IFNA, LET). Usage: python3 dec.py Sheet A1,B2:C3 ...
Needs pyxlsb2 (pip install pyxlsb2) for the table of Excel function numbers only."""
import zipfile,struct,re,sys,json,pickle
from pyxlsb2.ptgs import function_names
from openpyxl.utils import get_column_letter as L, column_index_from_string as ci
import os; p=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..','..','data','legacy','CPAT 1.0pre_465_Shell.xlsb')
z=zipfile.ZipFile(p)
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
sheets=[];rids=[];names=[];xti=[]
for t,d in recs(z.read('xl/workbook.bin')):
    if t==156:
        o=8; rid,o=wstr(d,o); nm,o=wstr(d,o); sheets.append(nm); rids.append(rid)
    elif t==362:
        n=struct.unpack_from('<I',d,0)[0]
        for k in range(n): xti.append(struct.unpack_from('<iii',d,4+12*k))
    elif t==39:
        o=5; itab=struct.unpack_from('<i',d,o)[0]; o+=4; nm,o=wstr(d,o); names.append(nm)
rels=dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"',z.read('xl/_rels/workbook.bin.rels').decode()))
def qs(s): return "'"+s.replace("'","''")+"'" if re.search(r"[^A-Za-z0-9_.]",s) or re.match(r'\d',s) else s
def sheet3d(ix):
    e,f,l=xti[ix]
    if f<0: return f'[ext{e}]'
    return qs(sheets[f]) if f==l else qs(sheets[f]+':'+sheets[l])
def cref(row,col,rr,cr): return f"{'' if cr else '$'}{L(col+1)}{'' if rr else '$'}{row+1}"
def colf(c): return c&0x3fff, bool(c&0x4000), bool(c&0x8000)
def s14(x): return x-0x4000 if x&0x2000 else x
OPS={0x03:'+',0x04:'-',0x05:'*',0x06:'/',0x07:'^',0x08:'&',0x09:'<',0x0A:'<=',0x0B:'=',0x0C:'>=',0x0D:'>',0x0E:'<>',0x0F:' ',0x10:',',0x11:':'}
ERR={0x00:'#NULL!',0x07:'#DIV/0!',0x0F:'#VALUE!',0x17:'#REF!',0x1D:'#NAME?',0x24:'#NUM!',0x2A:'#N/A'}
def decode(r,crow,ccol):
    st=[];i=0;pend=[]
    def sp(types):
        s=''
        for t,n in list(pend):
            if t in types: s+=(' ' if t in (0,2,4,6) else '\n')*n; pend.remove((t,n))
        return s
    while i<len(r):
        pt=r[i]; i+=1
        base=pt if pt<0x20 else ((pt&0x1f)|0x20)
        if base in OPS:
            b=st.pop(); a=st.pop(); s=sp((0,1)); st.append(a+s+OPS[base]+b)
        elif base in (0x12,0x13):
            a=st.pop(); s=sp((0,1)); st.append(s+('+' if base==0x12 else '-')+a)
        elif base==0x14: st.append(st.pop()+sp((0,1))+'%')
        elif base==0x15:
            a=st.pop(); s0=sp((0,1)); s2=sp((2,3)); s4=sp((4,5)); st.append(s0+s2+'('+a+s4+')')
        elif base==0x16: st.append(sp((0,1)))
        elif base==0x17:
            n=struct.unpack_from('<H',r,i)[0]; s=r[i+2:i+2+2*n].decode('utf-16le'); i+=2+2*n
            st.append(sp((0,1))+'"'+s.replace('"','""')+'"')
        elif base==0x19:
            g=r[i]; i+=1
            if g&0x40:
                t=r[i]; n=r[i+1]; i+=2; pend.append((t,n))
            elif g&0x04:
                n=struct.unpack_from('<H',r,i)[0]; i+=2+2*(n+1)
            elif g&0x10:
                i+=2; a=st.pop(); s4=sp((4,5)); s2=sp((2,3)); s0=sp((0,1)); st.append(s0+'SUM'+s2+'('+a+s4+')')
            else: i+=2
        elif base==0x1C: st.append(sp((0,1))+ERR.get(r[i],'#ERR')); i+=1
        elif base==0x1D: st.append(sp((0,1))+('TRUE' if r[i] else 'FALSE')); i+=1
        elif base==0x1E: st.append(sp((0,1))+str(struct.unpack_from('<H',r,i)[0])); i+=2
        elif base==0x1F:
            v=struct.unpack_from('<d',r,i)[0]; i+=8; st.append(sp((0,1))+(repr(int(v)) if v==int(v) and abs(v)<1e15 else repr(v)))
        elif base==0x20: raise ValueError('array constant')
        elif base in (0x21,0x22):
            if base==0x21: argc=None; ift=struct.unpack_from('<H',r,i)[0]; i+=2
            else: argc=r[i]&0x7f; ift=struct.unpack_from('<H',r,i+1)[0]&0x7fff; i+=3
            if ift==255:
                args=[st.pop() for _ in range(argc-1)][::-1]; fn=st.pop()
            else:
                fd=function_names[ift]; fn=fd[0]
                n=argc if argc is not None else (fd[1] if len(fd)>1 else 0)   # fixed-arity entries without a count: NA(), PI(), NOW() ...
                args=[st.pop() for _ in range(n)][::-1] if n else []
            s4=sp((4,5)); s2=sp((2,3)); s0=sp((0,1))
            st.append(s0+fn.strip()+s2+'('+','.join(args)+s4+')')
        elif base==0x23:
            ix=struct.unpack_from('<I',r,i)[0]; i+=4; st.append(sp((0,1))+names[ix-1])
        elif base==0x24:
            row,c=struct.unpack_from('<iH',r,i); i+=6; col,cr,rr=colf(c); st.append(sp((0,1))+cref(row,col,rr,cr))
        elif base==0x25:
            r1,r2,c1,c2=struct.unpack_from('<iiHH',r,i); i+=12
            a,ca,ra=colf(c1); b,cb,rb=colf(c2); st.append(sp((0,1))+cref(r1,a,ra,ca)+':'+cref(r2,b,rb,cb))
        elif base in (0x26,0x27,0x28): i+=6
        elif base==0x29: i+=2
        elif base==0x2A: i+=6; st.append(sp((0,1))+'#REF!')
        elif base==0x2B: i+=12; st.append(sp((0,1))+'#REF!')
        elif base==0x2C:
            row,c=struct.unpack_from('<iH',r,i); i+=6; col,cr,rr=colf(c)
            rw=(crow+row)%1048576 if rr else row; cl=(ccol+col)%16384 if cr else col
            st.append(sp((0,1))+cref(rw,cl,rr,cr))
        elif base==0x2D:
            r1,r2,c1,c2=struct.unpack_from('<iiHH',r,i); i+=12
            a,ca,ra=colf(c1); b,cb,rb=colf(c2)
            R1=(crow+r1)%1048576 if ra else r1; R2=(crow+r2)%1048576 if rb else r2; A=(ccol+a)%16384 if ca else a; B=(ccol+b)%16384 if cb else b
            st.append(sp((0,1))+cref(R1,A,ra,ca)+':'+cref(R2,B,rb,cb))
        elif base==0x39:
            ix,ni=struct.unpack_from('<HI',r,i); i+=6; st.append(sp((0,1))+names[ni-1])
        elif base==0x3A:
            ix,row,c=struct.unpack_from('<HiH',r,i); i+=8; col,cr,rr=colf(c); st.append(sp((0,1))+sheet3d(ix)+'!'+cref(row,col,rr,cr))
        elif base==0x3B:
            ix,r1,r2,c1,c2=struct.unpack_from('<HiiHH',r,i); i+=14
            a,ca,ra=colf(c1); b,cb,rb=colf(c2); st.append(sp((0,1))+sheet3d(ix)+'!'+cref(r1,a,ra,ca)+':'+cref(r2,b,rb,cb))
        elif base in (0x3C,0x3D): i+=8 if base==0x3C else 14; st.append(sp((0,1))+'#REF!')
        elif base==0x18: raise ValueError('ptg 0x18')
        else: raise ValueError('ptg %x'%pt)
    assert len(st)==1,st
    return '='+sp((6,))+st[0]
def sheetcells(sname):
    d=z.read('xl/'+rels[rids[sheets.index(sname)]]); row=0; shr=[]; cells={}
    for t,dd in recs(d):
        if t==0: row=struct.unpack_from('<I',dd,0)[0]
        elif t in (8,9,10,11):
            col=struct.unpack_from('<I',dd,0)[0]; o=8
            if t==8: n=struct.unpack_from('<I',dd,o)[0]; o+=4+2*n
            elif t==9: o+=8
            else: o+=1
            o+=2; cce=struct.unpack_from('<I',dd,o)[0]; cells[(row,col)]=dd[o+4:o+4+cce]
        elif t==427:
            r1,r2,c1,c2=struct.unpack_from('<iiii',dd,0); cce=struct.unpack_from('<I',dd,16)[0]; shr.append((r1,r2,c1,c2,dd[20:20+cce]))
        elif t==426:
            r1,r2,c1,c2=struct.unpack_from('<iiii',dd,0); o=17; cce=struct.unpack_from('<I',dd,o)[0]; shr.append((r1,r2,c1,c2,dd[o+4:o+4+cce]))
    SH={}
    for r1,r2,c1,c2,srg in shr:
        for rr in range(r1,r2+1):
            for cc in range(c1,c2+1): SH.setdefault((rr,cc),[]).append((r1,c1,srg))
    return cells,SH
def formula(cells,SH,a):
    c,r=re.match(r'([A-Z]+)(\d+)',a).groups(); key=(int(r)-1,ci(c)-1)
    rg=cells.get(key)
    if rg is None: return None
    if rg and rg[0]==0x01:
        ar=struct.unpack_from('<i',rg,1)[0]; cands=SH.get(key,[])
        m=[x for x in cands if x[0]==ar] or cands
        rg=m[0][2]
    return decode(rg,*key)
if __name__=='__main__':
    cells,SH=sheetcells(sys.argv[1])
    for spec in sys.argv[2].split(','):
        m=re.match(r'([A-Z]+)(\d+)(?::([A-Z]+)(\d+))?$',spec)
        c0,r0=m.group(1),int(m.group(2)); c1,r1=(m.group(3) or c0),int(m.group(4) or r0)
        for r in range(r0,r1+1):
            for c in range(ci(c0),ci(c1)+1):
                a=f'{L(c)}{r}'
                try: print(a,formula(cells,SH,a))
                except Exception as e: print(a,'ERR',e)
