import openpyxl,sys,pickle
wb=openpyxl.load_workbook(sys.argv[1],read_only=True,data_only=False)
out={}
for s in sys.argv[2:]:
    ws=wb[s]; d={}
    for row in ws.iter_rows():
        for c in row:
            if c.value is not None and hasattr(c,'coordinate'): d[c.coordinate]=c.value
    out[s]=d; print(s,len(d))
pickle.dump(out,open('fo.pkl','wb'))
