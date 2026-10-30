"""The legacy workbook and the six proprietary tables: the generic shell, and an edition's filled copy.

    python data/scripts/legacy_proprietary.py shell --from <filled legacy .xlsb>   # -> data/legacy/ (the shell)
    python data/scripts/legacy_proprietary.py fill [--edition Public01]             # -> <edition>/legacy/

The shell (data/legacy/CPAT 1.0pre_465_Shell.xlsb, generic) is the legacy model with the six proprietary tabs
(Balances, EnergyCons, Prices_dom, HHSurvey, IO_GTAP, Tran_Scatter) empty below their header rows: every other tab is
filled with the public legacy data. An edition's copy (<edition>/legacy/CPAT 1.0pre_465_<edition>.xlsb) is the shell
with the six tabs filled from the edition's tidy tables (the legacy form of data/scripts/tidy_convert.py), one row per
tidy row below the header, columns by the legacy header (Prices_dom: the codes of row 8; legacy columns the tidy table
has not, such as the Info columns, stay empty). So the person updating the data clears or fills six tables only.

The workbook is edited in its own format: the cell records of the six sheets are rewritten in the .xlsb (BIFF12)
stream, every other part of the file stays byte for byte. The sheets' binary row indexes (optional parts) are dropped,
as their offsets no longer hold, and the workbook is set to recalculate fully when Excel opens it (formula results
cached in the file are those of the previous data until Excel saves it). Check: the script reads the written file back
(pyxlsb) and compares every written cell.
"""
import os
import re
import shutil
import struct
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tidy_convert as tc  # noqa: E402

import editions as ED  # noqa: E402

CELL_TYPES = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
FORMULA = {8, 9, 10, 11}
BLANK, REAL, ISST = 1, 5, 7

# tab: (legacy file of the tidy table, 0-based header row)
TABS = {'Balances': ('legacy_Balances.csv', 12), 'EnergyCons': ('legacy_EnergyCons.csv', 0),
        'Prices_dom': ('prices_dom.csv', 7), 'HHSurvey': ('legacy_HHSurvey.csv', 0),
        'IO_GTAP': ('legacy_IO_GTAP.csv', 0), 'Tran_Scatter': ('legacy_Tran_Scatter.csv', 0)}


# ------------------------------------------------------------------------------------------------ BIFF12 records
def recs(b):
    i, out = 0, []
    while i < len(b):
        t = b[i]
        i += 1
        if t & 0x80:
            t = (t & 0x7f) | ((b[i] & 0x7f) << 7)
            i += 1
        sz = sh = 0
        for _ in range(4):
            x = b[i]
            i += 1
            sz |= (x & 0x7f) << sh
            sh += 7
            if not x & 0x80:
                break
        out.append((t, b[i:i + sz]))
        i += sz
    return out


def enc(t, d):
    h = bytes([t]) if t < 0x80 else bytes([(t & 0x7f) | 0x80, t >> 7])
    n, s = len(d), b''
    while True:
        s += bytes([(n & 0x7f) | (0x80 if n > 0x7f else 0)])
        n >>= 7
        if not n:
            break
    return h + s + d


def rk(x):
    v = float(x >> 2) if x & 2 else struct.unpack('<d', struct.pack('<Q', (x & 0xFFFFFFFC) << 32))[0]
    if x & 2 and x & 0x80000000:
        v = float((x >> 2) - (1 << 30))
    return v / 100 if x & 1 else v


def wstr(d, o):
    n = struct.unpack_from('<I', d, o)[0]
    return d[o + 4:o + 4 + 2 * n].decode('utf-16le')


def value(t, d, sst):
    """The constant of a cell record (None: blank, formula or other)."""
    if t == 2:
        return rk(struct.unpack_from('<I', d, 8)[0])
    if t == 5:
        return struct.unpack_from('<d', d, 8)[0]
    if t == 7:
        return sst[struct.unpack_from('<I', d, 8)[0]]
    if t == 6:
        return wstr(d, 8)
    return None


def cell(col, style, v, sst):
    h = struct.pack('<I', col) + style
    if v is None:
        return BLANK, h
    if isinstance(v, str):                               # a shared string, added to the table when new
        if v not in sst.index:
            sst.index[v] = len(sst)
            sst.append(v)
        return ISST, h + struct.pack('<I', sst.index[v])
    return REAL, h + struct.pack('<d', float(v))


class SST(list):
    """The shared strings: the file's, then the ones this script adds."""

    def __init__(self, data):
        self.recs = recs(data)
        super().__init__(wstr(d, 1) for t, d in self.recs if t == 19)
        self.n0 = len(self)
        self.index = {}
        for i, v in enumerate(self):
            self.index.setdefault(v, i)

    def data(self):
        out = []
        for t, d in self.recs:
            if t == 159:                                 # BrtBeginSst: total and unique counts
                tot, uniq = struct.unpack_from('<ii', d, 0)
                d = struct.pack('<ii', tot + len(self) - self.n0, uniq + len(self) - self.n0) + d[8:]
            if t == 160:                                 # BrtEndSst: the new strings go before it
                out += [enc(19, b'\x00' + struct.pack('<I', len(v)) + v.encode('utf-16le')) for v in self[self.n0:]]
            out.append(enc(t, d))
        return b''.join(out)


class Sheet:
    """The records of a sheet part, with the sheet data as rows of cells that can be changed."""

    def __init__(self, data, sst):
        self.recs, self.sst = recs(data), sst
        a = next(i for i, (t, _d) in enumerate(self.recs) if t == 145)
        b = next(i for i, (t, _d) in enumerate(self.recs) if t == 146)
        self.head, self.tail = self.recs[:a + 1], self.recs[b:]
        self.rows = {}                                   # row -> [row header data, {col: (t, d)}, [other records]]
        cur = None
        for t, d in self.recs[a + 1:b]:
            if t == 0:
                cur = [d, {}, []]
                self.rows[struct.unpack_from('<I', d, 0)[0]] = cur
            elif t in CELL_TYPES:
                cur[1][struct.unpack_from('<I', d, 0)[0]] = (t, d)
            else:
                cur[2].append((t, d))
        self.template = next(iter(self.rows.values()))[0]

    def get(self, r, c):
        t, d = self.rows.get(r, [None, {}, None])[1].get(c, (None, None))
        return (value(t, d, self.sst), t) if t else (None, None)

    def set(self, r, c, v):
        if r not in self.rows:
            self.rows[r] = [struct.pack('<I', r) + self.template[4:13] + struct.pack('<I', 0), {}, []]
        cells = self.rows[r][1]
        t, d = cells.get(c, (None, None))
        if t in FORMULA:
            return False
        style = d[4:8] if d else b'\x00\x00\x00\x00'
        if v is None and t is None:
            return True
        cells[c] = cell(c, style, v, self.sst)
        return True

    def data(self):
        out = [enc(t, d) for t, d in self.head]
        for r in sorted(self.rows):
            hdr, cells, other = self.rows[r]
            cols = sorted(cells)
            spans = sorted({c // 1024 for c in cols})
            # BrtRowHdr: rw, ixfe, miyRw, flags (13 bytes), then the column spans (one per block of 1024 columns): the
            # row's own spans, widened where its cells now reach further
            have = {}
            for k in range(struct.unpack_from('<I', hdr, 13)[0]):
                a, b = struct.unpack_from('<II', hdr, 17 + 8 * k)
                have[a // 1024] = (a, b)
            for s in spans:
                c0 = min(c for c in cols if c // 1024 == s)
                c1 = max(c for c in cols if c // 1024 == s)
                a, b = have.get(s, (c0, c1))
                have[s] = (min(a, c0), max(b, c1))
            out.append(enc(0, hdr[:13] + struct.pack('<I', len(have)) + b''.join(
                struct.pack('<II', *have[s]) for s in sorted(have))))
            out += [enc(*cells[c]) for c in cols] + [enc(t, d) for t, d in other]
        tail = [enc(t, d) for t, d in self.tail]
        rws = sorted(r for r, x in self.rows.items() if x[1])
        cls = sorted({c for x in self.rows.values() for c in x[1]})
        body = b''.join(out) + b''.join(tail)
        return self._dim(body, rws, cls)

    @staticmethod
    def _dim(body, rws, cls):
        """BrtWsDim (148): the used range."""
        out, done = [], False
        for t, d in recs(body):
            if t == 148 and not done and rws:             # widened to the cells, never narrowed
                r0, r1, c0, c1 = struct.unpack_from('<iiii', d, 0)
                d = struct.pack('<iiii', min(r0, rws[0]), max(r1, rws[-1]), min(c0, cls[0]), max(c1, cls[-1]))
                done = True
            out.append(enc(t, d))
        return b''.join(out)


# ------------------------------------------------------------------------------------------------ the tabs
def as_value(s):
    v = tc.cell_value(s)
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else v


def label(v):
    return str(int(v)) if isinstance(v, float) and v == int(v) else v       # a year header 2000.0 is '2000'


def header(sh, hr):
    return {label(sh.get(hr, c)[0]): c for c in sh.rows.get(hr, [None, {}])[1] if sh.get(hr, c)[0] not in (None, '')}


def clear(sh, hr):
    """Every constant below the header row (values and labels; formulas and formats stay)."""
    n = 0
    for r in [x for x in sh.rows if x > hr]:
        for c in list(sh.rows[r][1]):
            if sh.get(r, c)[1] not in (None, BLANK) and sh.get(r, c)[1] not in FORMULA:
                sh.set(r, c, None)
                n += 1
    return n


def fill(sh, tab, hr, table, written):
    cols = header(sh, hr)
    head, rows = table
    missing = [h for h in head if h not in cols]
    if missing:
        sys.exit(f'{tab}: legacy header lacks {missing[:5]}')
    clear(sh, hr)
    for i, r in enumerate(rows, hr + 1):
        for name, v in zip(head, r):
            x = as_value(v) if v != '' else None
            sh.set(i, cols[name], x)
            written.append((tab, i, cols[name], x))
    return len(rows)


def rewrite(src, dst, edit):
    """Copy src to dst with the six sheets changed by edit(tab, sheet) -> message; returns the written cells."""
    z = zipfile.ZipFile(src)
    sst = SST(z.read('xl/sharedStrings.bin'))
    wbrecs = recs(z.read('xl/workbook.bin'))
    names, rids = [], []
    for t, d in wbrecs:
        if t == 156:
            o = 8
            rid = wstr(d, o)
            o += 4 + 2 * len(rid)
            names.append(wstr(d, o))
            rids.append(rid)
    rels = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', z.read('xl/_rels/workbook.bin.rels').decode()))
    new_parts, drop, written = {}, set(), []
    for tab in TABS:
        part = 'xl/' + rels[rids[names.index(tab)]]
        sh = Sheet(z.read(part), sst)
        print(f'{tab}: {edit(tab, sh, written)}')
        new_parts[part] = sh.data()
        relp = part.replace('worksheets/', 'worksheets/_rels/') + '.rels'
        rx = z.read(relp).decode()
        drop |= {'xl/worksheets/' + i for i in re.findall(r'Target="(binaryIndex\d+\.bin)"', rx)}
        new_parts[relp] = re.sub(r'<Relationship [^>]*Target="binaryIndex\d+\.bin"[^>]*/>', '', rx).encode()
    ct = z.read('[Content_Types].xml').decode()
    for p in drop:
        ct = re.sub(rf'<Override PartName="/{re.escape(p)}"[^>]*/>', '', ct)
    new_parts['[Content_Types].xml'] = ct.encode()
    wb = []
    for t, d in wbrecs:                                    # BrtCalcProp: fFullCalcOnLoad
        if t == 157:
            d = d[:24] + struct.pack('<H', struct.unpack_from('<H', d, 24)[0] | 1) + d[26:]
        wb.append(enc(t, d))
    new_parts['xl/workbook.bin'] = b''.join(wb)
    new_parts['xl/sharedStrings.bin'] = sst.data()
    tmp = tempfile.NamedTemporaryFile(suffix='.xlsb', delete=False).name
    with zipfile.ZipFile(tmp, 'w') as out:
        for info in z.infolist():
            if info.filename not in drop:
                out.writestr(info, new_parts.get(info.filename, z.read(info.filename)),
                             compress_type=info.compress_type)
    z.close()
    verify(tmp, written)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(tmp, dst)
    os.chmod(dst, 0o644)
    print(f'written: {os.path.relpath(dst)} (binary row indexes dropped; full recalculation on open)')


def main():
    import argparse
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('shell')
    a.add_argument('--from', dest='src', required=True, help='a filled legacy workbook (.xlsb)')
    b = sub.add_parser('fill')
    b.add_argument('--edition', default=None)
    args = p.parse_args()
    if args.cmd == 'shell':
        rewrite(args.src, ED.SHELL, lambda tab, sh, w: f'{clear(sh, TABS[tab][1])} constants cleared')
    else:
        tables = tc.from_tidy(ED.tidy(args.edition))
        rewrite(ED.SHELL, ED.legacy_filled(args.edition),
                lambda tab, sh, w: f'{fill(sh, tab, TABS[tab][1], tables[TABS[tab][0]], w)} rows from tidy')


def verify(path, written):
    from pyxlsb import open_workbook
    if not written:
        return
    want = {}
    for tab, r, c, v in written:
        want.setdefault(tab, {})[(r, c)] = v
    with open_workbook(path) as wb:
        for tab, cells in want.items():
            with wb.get_sheet(tab) as sh:
                got = {(c.r, c.c): c.v for row in sh.rows() for c in row if (c.r, c.c) in cells}
            bad = [(k, v, got.get(k)) for k, v in cells.items()
                   if not (got.get(k) == v or (isinstance(v, float) and isinstance(got.get(k), float)
                                               and abs(got[k] - v) <= 1e-12 * max(1, abs(v))))]
            if bad:
                sys.exit(f'{tab}: {len(bad)} cells read back differently, e.g. {bad[:3]}')
    print(f'read back: {len(written)} written cells equal')


if __name__ == '__main__':
    main()
