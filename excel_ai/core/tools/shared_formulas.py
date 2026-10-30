"""Shared formulas in the workbooks Excel-AI writes (user 2026-10-30: smaller files, faster to open).

openpyxl writes every formula in full. Excel stores a run of cells that hold the same formula in relative terms
(what a fill or a copy-paste gives) once: the first cell holds the formula with t="shared", the range and an index
si; the other cells of the range hold only <f t="shared" si="n"/>, and Excel shifts the first cell's formula to each
of them, as a fill would. The results do not change.

share(xml) turns each run of adjacent cells of a row whose formulas are the first one's shifted (openpyxl's
Translator, the same shift as a fill) into one shared formula; unshare(xml) writes every formula in full again, for
the scripts that edit formulas in the XML (lo_session.expanded_zip, make_variants.py). Only plain formulas are shared
(no array formulas); a cell is shared only when the shift gives exactly its formula, so the round trip is exact.
A formula that names another sheet (Sheet!A1, 'My sheet'!A1) is never shared: Excel 365 removed every such shared
formula on open ("Removed Records: Shared formula from /xl/worksheets/sheetN.xml", user test 2026-10-30), and only
the sheets with them were repaired.

    import shared_formulas as SF
    SF.share_file(path)                 # in place; returns (formulas, shared groups, cells written as references)
"""
import html
import os
import re
import shutil
import zipfile

from openpyxl.formula.translate import Translator

ROW = re.compile(r'(<row\b[^>]*>)(.*?)(</row>)', re.S)
CELL = re.compile(r'<c r="([A-Z]+)(\d+)"((?:\s[^>]*?)?)(?<!/)>(.*?)</c>', re.S)
PLAIN_F = re.compile(r'^<f>(.*?)</f>', re.S)                     # a formula without attributes, first in the cell
ANY_F = re.compile(r'<f(\s[^>]*)?(?:/>|>(.*?)</f>)', re.S)
MIN_RUN = 2


def _col(letters):
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n


def _esc(s):
    return html.escape(s, quote=False)


def share(xml, keep=None):
    """The sheet XML with each run of shiftable formulas along a row written as one shared formula. keep(formula):
    False leaves the formula unshared (tests)."""
    si = [max((int(x) for x in re.findall(r'<f[^>]*\bsi="(\d+)"', xml)), default=-1) + 1]
    stats = [0, 0, 0]                                            # formulas, groups, cells written as references

    def row(m):
        cells = list(CELL.finditer(m.group(2)))
        if not cells:
            return m.group(0)
        info = []
        for c in cells:
            f = PLAIN_F.match(c.group(4))
            info.append((c.group(1), int(c.group(2)), html.unescape(f.group(1)) if f else None))
        stats[0] += sum(1 for _c, _r, f in info if f is not None)
        new, i, n = {}, 0, len(info)                            # cell index -> its new XML
        while i < n:
            col, r, f = info[i]
            j = i + 1
            if f is not None and ('!' in f or (keep is not None and not keep(f))):
                f = None                                         # a sheet reference: Excel rejects it shared
            if f is not None:
                tr = Translator('=' + f, origin=f'{col}{r}')
                while j < n and info[j][2] is not None and _col(info[j][0]) == _col(info[j - 1][0]) + 1:
                    try:
                        if tr.translate_formula(f'{info[j][0]}{r}') != '=' + info[j][2]:
                            break
                    except Exception:                            # a reference that cannot shift: not shared
                        break
                    j += 1
            if f is None or j - i < MIN_RUN:
                i += 1
                continue
            k = si[0]
            si[0] += 1
            stats[1] += 1
            stats[2] += j - i - 1
            for t in range(i, j):
                c = cells[t]
                fx = (f'<f t="shared" ref="{col}{r}:{info[j - 1][0]}{r}" si="{k}">{_esc(f)}</f>' if t == i
                      else f'<f t="shared" si="{k}"/>')
                new[t] = (f'<c r="{c.group(1)}{c.group(2)}"{c.group(3)}>' + fx
                          + c.group(4)[PLAIN_F.match(c.group(4)).end():] + '</c>')
            i = j
        if not new:
            return m.group(0)
        body, pos, text = [], 0, m.group(2)
        for t, c in enumerate(cells):
            if t in new:
                body.append(text[pos:c.start()])
                body.append(new[t])
                pos = c.end()
        body.append(text[pos:])
        return m.group(1) + ''.join(body) + m.group(3)

    xml = ROW.sub(row, xml)
    return xml, tuple(stats)


def unshare(xml):
    """The sheet XML with every shared formula written in full in each of its cells."""
    if 't="shared"' not in xml:
        return xml
    master = {}
    for c in CELL.finditer(xml):
        for f in ANY_F.finditer(c.group(4)):
            a = f.group(1) or ''
            if 't="shared"' in a and 'ref="' in a and f.group(2) is not None:
                k = re.search(r'\bsi="(\d+)"', a).group(1)
                master[k] = Translator('=' + html.unescape(f.group(2)), origin=f'{c.group(1)}{c.group(2)}')

    def cell(c):
        def fx(f):
            a = f.group(1) or ''
            if 't="shared"' not in a:
                return f.group(0)
            k = re.search(r'\bsi="(\d+)"', a).group(1)
            return '<f>' + _esc(master[k].translate_formula(f'{c.group(1)}{c.group(2)}')[1:]) + '</f>'
        inner = ANY_F.sub(fx, c.group(4), count=1)
        return f'<c r="{c.group(1)}{c.group(2)}"{c.group(3)}>{inner}</c>'
    return CELL.sub(cell, xml)


def share_file(path, keep=None):
    """Share the formulas of every worksheet of the workbook at path, in place. Returns (formulas, groups, cells
    written as references to their group's first cell)."""
    tot = [0, 0, 0]
    tmp = path + '.share.tmp'
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.startswith('xl/worksheets/sheet') and item.filename.endswith('.xml'):
                xml, st = share(data.decode('utf-8'), keep)
                tot = [a + b for a, b in zip(tot, st)]
                data = xml.encode('utf-8')
            zout.writestr(item, data)
    shutil.move(tmp, path)
    return tuple(tot)


if __name__ == '__main__':
    import sys
    for p in sys.argv[1:]:
        before = os.path.getsize(p)
        n, g, refs = share_file(p)
        print(f'{p}: {n} formulas, {g} shared groups, {refs} cells now reference their group; '
              f'{before / 1e6:.1f} MB -> {os.path.getsize(p) / 1e6:.1f} MB')
