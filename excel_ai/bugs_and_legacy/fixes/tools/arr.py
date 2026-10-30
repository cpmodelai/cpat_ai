import zipfile,struct,re,sys,json
from openpyxl.utils import get_column_letter as L
p='/home/user/CPAT-AI/excel_ai/bugs_and_legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb'
z=zipfile.ZipFile(p)
src=open('fnames.py').read(); exec(src[src.index('def recs'):src.index('sheets=[];rids=[];names=[]')])
b=z.read('xl/workbook.bin')
sheets=[];rids=[]
for t,d in recs(b):
    if t==156:
        o=8; rid,o=wstr(d,o); nm,o=wstr(d,o); sheets.append(nm); rids.append(rid)
rels=dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"',z.read('xl/_rels/workbook.bin.rels').decode()))
out={}
for s in sys.argv[1:]:
    d=z.read('xl/'+rels[rids[sheets.index(s)]]); A=[]
    for t,dd in recs(d):
        if t==426:
            r1,r2,c1,c2=struct.unpack_from('<iiii',dd,0); A.append(f'{L(c1+1)}{r1+1}:{L(c2+1)}{r2+1}')
    out[s]=A; print(s,len(A))
json.dump(out,open('arrays.json','w'))
