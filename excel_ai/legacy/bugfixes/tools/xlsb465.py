"""Reading the 465 .xlsb for the plan generators (gen_F, gen_G): formulas (dec465.py) and constants, and the plan-entry
helpers (exact substitution, bracket check, policy paste)."""
import re
import struct

import dec465 as D

OFF = 6316                                      # policy block offset in 465 (README)

SST = [D.wstr(d, 1)[0] for t, d in D.recs(D.z.read('xl/sharedStrings.bin')) if t == 19]
_SHEETS = {}


def _rk(x):
    """BIFF12 RK number."""
    v = float(x >> 2) if x & 2 else struct.unpack('<d', struct.pack('<Q', (x & 0xFFFFFFFC) << 32))[0]
    if x & 2 and x & 0x80000000:
        v = float((x >> 2) - (1 << 30))
    return v / 100 if x & 1 else v


def _sheet(name):
    """(formula cells, shared formulas, constants) of a sheet, read once."""
    if name not in _SHEETS:
        cells, sh = D.sheetcells(name)
        const, row = {}, 0
        for t, d in D.recs(D.z.read('xl/' + D.rels[D.rids[D.sheets.index(name)]])):
            if t == 0:
                row = struct.unpack_from('<I', d, 0)[0]
            elif t in (2, 5, 6, 7):              # RK number, number, inline string, shared string
                col = struct.unpack_from('<I', d, 0)[0]
                const[(row, col)] = (_rk(struct.unpack_from('<I', d, 8)[0]) if t == 2 else
                                     struct.unpack_from('<d', d, 8)[0] if t == 5 else D.wstr(d, 8)[0] if t == 6
                                     else SST[struct.unpack_from('<I', d, 8)[0]])
        _SHEETS[name] = cells, sh, const
    return _SHEETS[name]


def cur(a, sheet='Mitigation'):
    """The formula of a cell, else its constant (text as typed)."""
    cells, sh, const = _sheet(sheet)
    f = D.formula(cells, sh, a)
    if f is not None:
        return f
    c, r = re.match(r'([A-Z]+)(\d+)$', a).groups()
    v = const.get((int(r) - 1, D.ci(c) - 1))
    assert v is not None, (sheet, a, 'empty')
    return v if isinstance(v, str) else repr(v)


def bal(f):
    d = 0
    for ch in f:
        d += (ch == '(') - (ch == ')')
        assert d >= 0, f
    assert d == 0, f
    return f


def sub(a, *pairs, sheet='Mitigation'):
    f = cur(a, sheet)
    for o, n in pairs:
        assert f.count(o) == 1, (a, o, f)
        f = f.replace(o, n)
    return bal(f) if f.startswith('=') else f


def fx(cell, new, fill='single cell', policy='none (shared rows, one copy only)', sheet='Mitigation'):
    now = cur(cell, sheet)
    assert new != now, (cell, 'no change')
    return dict(cell=cell if sheet == 'Mitigation' else f'{sheet}!{cell}', now=now, new=new, fill=fill, policy=policy)


def pol(a):
    """The policy-block copy of a baseline cell (+6,316 rows)."""
    c, r = re.match(r'([A-Z]+)(\d+)$', a).groups()
    return f'{c}{int(r) + OFF}'


def paste(a, rng=None):
    rng = rng or a
    first, *last = rng.split(':')
    tgt = pol(first) + (':' + pol(last[0]) if last else '')
    return f'{tgt}: paste the baseline cells (Paste Special, Formulas; +6,316 rows)'


def wrap_lower(a):
    f = cur(a)
    assert f.startswith('=LOWER(_Country_code)&'), (a, f)
    return '=LOWER(' + f[1:] + ')'


