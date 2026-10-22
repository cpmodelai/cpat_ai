import pickle, sys
from openpyxl.utils import get_column_letter as L
F=pickle.load(open(sys.argv[1],'rb'))
cols=sys.argv[3] if len(sys.argv)>3 else "A:P"
c0,c1=[__import__('openpyxl').utils.column_index_from_string(c) for c in cols.split(':')]
for spec in sys.argv[2].split(','):
    a,b=(spec.split('-')+[spec])[:2]
    for r in range(int(a),int(b)+1):
        row=F[r]
        out=[f"{L(c)}={row[c-1]!r}" for c in range(c0,c1+1) if row[c-1] not in (None,'')]
        print(r,' | '.join(out))
