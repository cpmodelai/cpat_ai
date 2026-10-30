# decode raw xlsb formulas for selected Mitigation cells (group B helper)
import zipfile,struct,re,sys,json,pickle
from openpyxl.utils import get_column_letter as L, column_index_from_string as ci
S='/tmp/claude-0/-home-user-CPAT-AI/8ecef15a-59be-528a-8fc5-3dd56f80a940/scratchpad/lg'
z=zipfile.ZipFile(S+'/l456.xlsb')
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
for t,d in recs(z.read('xl/workbook.bin')):
    if t==156:
        o=8; rid,o=wstr(d,o); nm,o=wstr(d,o); sheets.append(nm); rids.append(rid)
    elif t==39:
        o=5; itab=struct.unpack_from('<i',d,o)[0]; o+=4; nm,o=wstr(d,o); names.append(nm)
xti=[]
for t,d in recs(z.read('xl/workbook.bin')):
    if t==362:
        n=struct.unpack_from('<I',d,0)[0]
        for k in range(n):
            sup,a,b=struct.unpack_from('<Iii',d,4+12*k); xti.append((sup,a,b))
rels=dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"',z.read('xl/_rels/workbook.bin.rels').decode()))
FN={0:'COUNT',1:'IF',2:'ISNA',3:'ISERROR',4:'SUM',5:'AVERAGE',6:'MIN',7:'MAX',8:'ROW',9:'COLUMN',15:'SIN',19:'PI',20:'SQRT',21:'EXP',24:'ABS',25:'INT',26:'SIGN',27:'ROUND',28:'LOOKUP',29:'INDEX',32:'LN',36:'AND',37:'OR',38:'NOT',39:'MOD',48:'TEXT',56:'PV',64:'MATCH',65:'DATE',74:'NOW',77:'ROWS',78:'COLUMNS',82:'SEARCH',100:'CHOOSE',101:'HLOOKUP',102:'VLOOKUP',105:'ISREF',109:'LOG',111:'CHAR',112:'LOWER',113:'UPPER',115:'LEFT',116:'RIGHT',117:'EXACT',118:'TRIM',119:'REPLACE',120:'SUBSTITUTE',124:'FIND',125:'CELL',127:'ISTEXT',128:'ISNUMBER',129:'ISBLANK',148:'INDIRECT',169:'COUNTA',183:'PRODUCT',190:'ISNONTEXT',197:'TRUNC',198:'ISLOGICAL',212:'ROUNDUP',213:'ROUNDDOWN',219:'ADDRESS',220:'DAYS360',221:'TODAY',227:'MEDIAN',228:'SUMPRODUCT',255:'UDF',269:'AVEDEV',336:'CONCATENATE',337:'POWER',342:'RADIANS',344:'SUBTOTAL',345:'SUMIF',346:'COUNTIF',347:'COUNTBLANK',358:'GETPIVOTDATA',359:'HYPERLINK',480:'IFERROR',481:'COUNTIFS',482:'SUMIFS',483:'AVERAGEIF',484:'AVERAGEIFS'}
FIXARGS={1:None,2:1,3:1,24:1,25:1,26:1,27:2,32:1,38:1,39:2,48:2,65:3,77:1,78:1,112:1,113:1,117:2,118:1,119:4,127:1,128:1,129:1,190:1,198:1,212:2,213:2,342:1,480:2,21:1,20:1,19:0,74:0,221:0,111:1}
def cref(r,c,colrel,rowrel):
    return ('' if colrel else '$')+L(c+1)+('' if rowrel else '$')+str(r+1)
def decode(rg,cr,cc,extra=b''):
    st=[];i=0
    while i<len(rg):
        pt=rg[i]; i+=1
        base=pt if pt<0x20 else ((pt&0x1f)|0x20)
        ops={0x03:'+',0x04:'-',0x05:'*',0x06:'/',0x07:'^',0x08:'&',0x09:'<',0x0A:'<=',0x0B:'=',0x0C:'>=',0x0D:'>',0x0E:'<>',0x0F:' ',0x10:',',0x11:':'}
        if pt in ops:
            b=st.pop();a=st.pop();st.append(a+ops[pt]+b);continue
        if pt==0x12: st.append('+'+st.pop());continue
        if pt==0x13: st.append('-'+st.pop());continue
        if pt==0x14: st.append(st.pop()+'%');continue
        if pt==0x15: st.append('('+st.pop()+')');continue
        if pt==0x16: st.append('');continue
        if pt==0x17:
            n=struct.unpack_from('<H',rg,i)[0]; s=rg[i+2:i+2+2*n].decode('utf-16le'); i+=2+2*n; st.append('"'+s+'"');continue
        if pt==0x18:
            e=rg[i];i+=1
            if e==0x19: i+=12; st.append('?list');continue
            st.append('?ext');return 'ERR'+str(st)
        if pt==0x19:
            sub=rg[i];i+=1
            if sub&0x04:
                n=struct.unpack_from('<H',rg,i)[0]; i+=2+2*(n+1)
            else: i+=2
            if sub&0x10: st.append('SUM('+st.pop()+')')
            continue
        if pt==0x1C: st.append({0:'#NULL!',7:'#DIV/0!',15:'#VALUE!',23:'#REF!',29:'#NAME?',36:'#NUM!',42:'#N/A'}.get(rg[i],'#ERR'));i+=1;continue
        if pt==0x1D: st.append('TRUE' if rg[i] else 'FALSE');i+=1;continue
        if pt==0x1E: st.append(str(struct.unpack_from('<H',rg,i)[0]));i+=2;continue
        if pt==0x1F: v=struct.unpack_from('<d',rg,i)[0];i+=8;st.append(repr(v).rstrip('0').rstrip('.') if '.' in repr(v) else repr(v));continue
        if base==0x20: i+=14; st.append('{array}');continue
        if base==0x21:
            f=struct.unpack_from('<H',rg,i)[0];i+=2;n=FIXARGS.get(f,1)
            args=[st.pop() for _ in range(n)][::-1] if n else []
            st.append(FN.get(f,'F%d'%f)+'('+','.join(args)+')');continue
        if base==0x22:
            n=rg[i];f=struct.unpack_from('<H',rg,i+1)[0]&0x7fff;i+=3
            args=[st.pop() for _ in range(n)][::-1]
            if f==255: st.append(args[0]+'('+','.join(args[1:])+')')
            else: st.append(FN.get(f,'F%d'%f)+'('+','.join(args)+')')
            continue
        if base==0x23:
            ix=struct.unpack_from('<I',rg,i)[0];i+=4;st.append(names[ix-1] if 0<ix<=len(names) else '?n%d'%ix);continue
        if base==0x24:
            r,c=struct.unpack_from('<IH',rg,i);i+=6;st.append(cref(r,c&0x3fff,c&0x4000,c&0x8000));continue
        if base==0x25:
            r1,r2,c1,c2=struct.unpack_from('<IIHH',rg,i);i+=12
            st.append(cref(r1,c1&0x3fff,c1&0x4000,c1&0x8000)+':'+cref(r2,c2&0x3fff,c2&0x4000,c2&0x8000));continue
        if base==0x26 or base==0x27 or base==0x28: i+=6; continue  # mem tokens: skip header (subexpr follows)
        if base==0x29: i+=2; continue
        if base==0x2A: i+=6; st.append('#REF!');continue
        if base==0x2B: i+=12; st.append('#REF!');continue
        if base==0x2C:
            r,c=struct.unpack_from('<iH',rg,i);i+=6
            rr=(cr+r)%1048576 if c&0x8000 else r; ccc=(cc+((c&0x3fff)^0x2000)-0x2000)%16384 if c&0x4000 else c&0x3fff
            st.append(cref(rr,ccc,c&0x4000,c&0x8000));continue
        if base==0x2D:
            r1,r2,c1,c2=struct.unpack_from('<iiHH',rg,i);i+=12
            def one(r,c):
                rr=(cr+r)%1048576 if c&0x8000 else r; ccc=(cc+((c&0x3fff)^0x2000)-0x2000)%16384 if c&0x4000 else c&0x3fff
                return cref(rr,ccc,c&0x4000,c&0x8000)
            st.append(one(r1,c1)+':'+one(r2,c2));continue
        if base==0x39:
            x,ix=struct.unpack_from('<HI',rg,i);i+=6;st.append('?nameX%d'%ix if ix>len(names) else names[ix-1]);continue
        if base==0x3A:
            x,r,c=struct.unpack_from('<HIH',rg,i);i+=8;sn=sheets[xti[x][1]] if x<len(xti) and 0<=xti[x][1]<len(sheets) else '?'
            st.append(sn+'!'+cref(r,c&0x3fff,c&0x4000,c&0x8000));continue
        if base==0x3B:
            x,r1,r2,c1,c2=struct.unpack_from('<HIIHH',rg,i);i+=14;sn=sheets[xti[x][1]] if x<len(xti) and 0<=xti[x][1]<len(sheets) else '?'
            st.append(sn+'!'+cref(r1,c1&0x3fff,c1&0x4000,c1&0x8000)+':'+cref(r2,c2&0x3fff,c2&0x4000,c2&0x8000));continue
        if base in (0x3C,0x3D): i+=8 if base==0x3C else 14; st.append('#REF!');continue
        return 'ERRptg%x %s'%(pt,st)
    return '='+(st[-1] if st else '')
def load(sname,want):
    k=sheets.index(sname); fn='xl/'+rels[rids[k]]
    d=z.read(fn); row=0; shr=[]; cells={}
    for t,dd in recs(d):
        if t==0: row=struct.unpack_from('<I',dd,0)[0]
        elif t in (8,9,10,11):
            col=struct.unpack_from('<I',dd,0)[0]
            if (row,col) in want:
                o=8
                if t==8: n=struct.unpack_from('<I',dd,o)[0]; o+=4+2*n
                elif t==9: o+=8
                else: o+=1
                o+=2; cce=struct.unpack_from('<I',dd,o)[0]; cells[(row,col)]=dd[o+4:o+4+cce]
        elif t==427:
            r1,r2,c1,c2=struct.unpack_from('<iiii',dd,0); cce=struct.unpack_from('<I',dd,16)[0]; shr.append((r1,r2,c1,c2,dd[20:20+cce],r1,c1,0))
        elif t==426:
            r1,r2,c1,c2=struct.unpack_from('<iiii',dd,0); cce=struct.unpack_from('<I',dd,17)[0]; shr.append((r1,r2,c1,c2,dd[21:21+cce],r1,c1,1))
    out={}
    for (r,c),rg in cells.items():
        arr=False
        if rg and rg[0]==0x01:
            for r1,r2,c1,c2,srg,mr,mc,isarr in shr:
                if r1<=r<=r2 and c1<=c<=c2: rg=srg; arr=isarr; break
        f=decode(rg,r,c)
        out[f'{L(c+1)}{r+1}']=('{'+f+'}' if arr else f)
    return out
if __name__=='__main__':
    sname=sys.argv[1]; cells=sys.argv[2:]
    want=set()
    for a in cells:
        c,r=re.match(r'([A-Z]+)(\d+)',a).groups(); want.add((int(r)-1,ci(c)-1))
    for k,v in sorted(load(sname,want).items(),key=lambda kv:(int(re.sub(r'[A-Z]','',kv[0])),kv[0])): print(k,v)

_RAW=None
def raw_all(sname='Mitigation',rows=None):
    """one pass: raw rgce of every formula cell (optionally only rows in `rows`), plus shared/array records"""
    k=sheets.index(sname); fn='xl/'+rels[rids[k]]
    d=z.read(fn); row=0; shr=[]; cells={}
    for t,dd in recs(d):
        if t==0: row=struct.unpack_from('<I',dd,0)[0]
        elif t in (8,9,10,11):
            if rows is not None and row not in rows: continue
            col=struct.unpack_from('<I',dd,0)[0]; o=8
            if t==8: n=struct.unpack_from('<I',dd,o)[0]; o+=4+2*n
            elif t==9: o+=8
            else: o+=1
            o+=2; cce=struct.unpack_from('<I',dd,o)[0]; cells[(row,col)]=dd[o+4:o+4+cce]
        elif t==427:
            r1,r2,c1,c2=struct.unpack_from('<iiii',dd,0); cce=struct.unpack_from('<I',dd,16)[0]; shr.append((r1,r2,c1,c2,dd[20:20+cce],0))
        elif t==426:
            r1,r2,c1,c2=struct.unpack_from('<iiii',dd,0); cce=struct.unpack_from('<I',dd,17)[0]; shr.append((r1,r2,c1,c2,dd[21:21+cce],1))
    return cells,shr
def getf(cells,shr,a):
    c,r=re.match(r'([A-Z]+)(\d+)',a).groups(); r=int(r)-1; c=ci(c)-1
    rg=cells.get((r,c))
    if rg is None: return None
    arr=False
    if rg and rg[0]==0x01:
        for r1,r2,c1,c2,srg,isarr in shr:
            if r1<=r<=r2 and c1<=c<=c2: rg=srg; arr=isarr; break
    f=decode(rg,r,c)
    return '{'+f+'}' if arr else f
