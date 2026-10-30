"""Variants of the shipped CPAT-AI-Mitigation-Prototype v0.4.7 workbook without macros and/or without LAMBDAs.

Works on the file package (zip) of the shipped .xlsm, so charts, styles and every other part stay byte-identical:
- noMacros (.xlsx): drops the VBA project; the macro buttons stay as plain shapes (no macro assigned).
- noLambdas (.xlsm): every call of a named LAMBDA in a cell formula is replaced by the LAMBDA body with the
  arguments substituted (recursively), and the LAMBDA defined names are removed. Excel recalculates on open.
- noMacros_noLambdas (.xlsx): both.

Usage: python make_variants.py [source.xlsm]   (default: ../CPAT-AI-Mitigation-Prototype-v0.7.0.xlsm)
"""
import os as _os, sys as _sys  # the excel_ai code folders and data/scripts on the path (core/tools/xlpaths.py)
_xl = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_xl) != 'excel_ai':
    _xl = _os.path.dirname(_xl)
_sys.path.insert(0, _os.path.join(_xl, 'core', 'tools'))
import xlpaths  # noqa: E402,F401
import html
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'CPAT-AI-Mitigation-Prototype-v0.7.0.xlsm')
STEM = os.path.splitext(os.path.abspath(SRC))[0]
MAX_LEN = 8192                        # Excel limit on formula length (characters)

NAME_RE = re.compile(r'<definedName name="([^"]+)"[^>]*>([^<]*)</definedName>')
F_RE = re.compile(r'(<f(?:\s[^>]*)?>)(.*?)(</f>)', re.S)


def split_args(s):
    """Top-level comma split of a function's argument text (strings and brackets respected)."""
    args, cur, depth, q = [], '', 0, False
    for ch in s:
        if ch == '"':
            q = not q
        elif not q:
            if ch in '({':
                depth += 1
            elif ch in ')}':
                depth -= 1
            elif ch == ',' and depth == 0:
                args.append(cur)
                cur = ''
                continue
        cur += ch
    return args + [cur]


def read_lambdas(wb_xml):
    lam = {}
    for name, val in NAME_RE.findall(wb_xml):
        v = html.unescape(val)
        if v.startswith('_xlfn.LAMBDA('):
            parts = split_args(v[len('_xlfn.LAMBDA('):-1])
            lam[name] = ([p.replace('_xlpm.', '') for p in parts[:-1]], parts[-1])
    return lam


def make_expander(lam):
    call = re.compile(r'(?<![A-Za-z0-9_.!])(' + '|'.join(sorted(lam, key=len, reverse=True)) + r')\(')

    def expand(f):
        while True:
            m = call.search(f)
            if not m:
                return f
            depth, k, q = 1, m.end(), False
            while depth:
                ch = f[k]
                if ch == '"':
                    q = not q
                elif not q:
                    depth += (ch == '(') - (ch == ')')
                k += 1
            params, body = lam[m.group(1)]
            args = split_args(f[m.end():k - 1])
            assert len(args) == len(params), (m.group(1), f[:200])
            for prm, arg in zip(params, args):
                body = re.sub(rf'_xlpm\.{re.escape(prm)}(?![A-Za-z0-9_])', lambda _m, a=arg: f'({a})', body)
            f = f[:m.start()] + '(' + body + ')' + f[k:]
    return expand, call


def build(no_macros, no_lambdas, out):
    zin = zipfile.ZipFile(SRC)
    wb_xml = zin.read('xl/workbook.xml').decode('utf-8')
    lam = read_lambdas(wb_xml)
    expand, call = make_expander(lam)
    stats = {'cells': 0, 'longest': 0}
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            name, data = item.filename, zin.read(item.filename)
            if no_macros and name == 'xl/vbaProject.bin':
                continue
            if name.endswith('.xml') or name.endswith('.rels'):
                txt = data.decode('utf-8')
                if no_macros:
                    if name == '[Content_Types].xml':
                        txt = re.sub(r'<Default Extension="bin" ContentType="application/vnd\.ms-office\.vbaProject"/>',
                                     '', txt)
                        txt = txt.replace('application/vnd.ms-excel.sheet.macroEnabled.main+xml',
                                          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml')
                    elif name == 'xl/_rels/workbook.xml.rels':
                        txt = re.sub(r'<Relationship [^>]*vbaProject[^>]*/>', '', txt)
                    elif name.startswith('xl/drawings/'):
                        txt = re.sub(r' macro="[^"]*"', ' macro=""', txt)
                if no_lambdas:
                    if name == 'xl/workbook.xml':
                        txt = NAME_RE.sub(lambda m: '' if m.group(1) in lam else m.group(0), txt)
                        txt = re.sub(r'<calcPr([^>]*?)/>', lambda m: '<calcPr' + re.sub(
                            r'\sfullCalcOnLoad="[^"]*"', '', m.group(1)) + ' fullCalcOnLoad="1"/>', txt)
                    elif name.startswith('xl/worksheets/sheet'):
                        def sub(m):
                            f = html.unescape(m.group(2))
                            if not call.search(f):
                                return m.group(0)
                            g = expand(f)
                            stats['cells'] += 1
                            stats['longest'] = max(stats['longest'], len(g.replace('_xlfn.', '')))
                            return m.group(1) + html.escape(g, quote=False) + m.group(3)
                        txt = F_RE.sub(sub, txt)
                data = txt.encode('utf-8')
            zout.writestr(item, data)
    print(f'{os.path.basename(out)}: LAMBDA cells expanded {stats["cells"]}, longest formula {stats["longest"]} chars'
          if no_lambdas else os.path.basename(out))
    assert stats['longest'] <= MAX_LEN, 'expanded formula longer than Excel allows'


if __name__ == '__main__':
    build(True, False, STEM + '_noMacros.xlsx')
    build(False, True, STEM + '_noLambdas.xlsm')
    build(True, True, STEM + '_noMacros_noLambdas.xlsx')
