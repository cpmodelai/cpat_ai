"""Move legacy cell references from CPAT 1.0pre_456 to CPAT 1.0pre_465 (2026-10-23).

The row map (data/rowmap_456_465.json) aligns the rows of both files on their labels and codes. Only sheets Mitigation
and MTInputs moved; every other sheet keeps its rows. In 465 the policy block sits +6,316 rows below the baseline
everywhere (456: +6,331 above row ~5667, +6,317 below).

    python remap_465.py json  <fixes_*.json> ...     cell plans: cell, now, new, fill, policy, where, why, ref, note
    python remap_465.py py    <source.py> ...        every string literal of a Python source (comments untouched)
    python remap_465.py text  <file.md> ...          a Markdown or text file

Each mode rewrites the files in place and prints every reference it changed; rows deleted in 465 are left as they
are and reported. Effects and prototype notes are not touched in the JSON plans (they quote values and prototype rows).
"""
import io
import json
import os
import re
import sys
import tokenize

HERE = os.path.dirname(os.path.abspath(__file__))
MAP = json.load(open(os.path.join(HERE, '..', 'data', 'rowmap_456_465.json'), encoding='utf-8'))
LOG = []


def mrow(sheet, r):
    """465 row of a 456 row; None if deleted; unchanged for sheets that did not move or rows past the end."""
    m = MAP['sheets'].get(sheet)
    if m is None or r > m['last']:
        return r
    for a, b, off in m['runs']:
        if a <= r <= b:
            return r + off
    return None


SIZE = {'Manual inputs': 378, 'MTInputs': 415, 'CoC': 390}
REF = re.compile(r"((?:'[^']+'|\b[A-Za-z_][\w\.]*)!)?(\$?)\b([A-Z]{1,3})(\$?)(\d{1,5})\b(?![\w(])")


def remap_formula(f, sheet='Mitigation'):
    """Every A1 reference outside string literals."""
    def rep(m):
        sp, d1, c, d2, r = m.groups()
        tsh = sp[:-1].strip("'") if sp else sheet
        nr = mrow(tsh, int(r))
        if nr is None:
            LOG.append(f'deleted in 465: {tsh}!{c}{r}')
            return m.group(0)
        if nr != int(r):
            LOG.append(f'{tsh}!{c}{r} -> {c}{nr}')
        return (sp or '') + d1 + c + d2 + str(nr)
    return ''.join(p if p.startswith('"') else REF.sub(rep, p) for p in re.split(r'("[^"]*")', f))


OTHER = (r"(?:Power|Distribution|Dashboard|ECP|Transport\w*|CoC|Manual inputs|MTOutputs|GHGs|NDCs|Countries|"
         r"Multipliers|Prices_\w+|EF_\w+|Elasticities|ETS\+LTS|WEO|SSPs|CBAM|Balances|HHSurvey|ASPIRE|Air pollution|"
         r"Air_Data|Mapping|IO_GTAP|OilProductShares|UNPop|CalVal|SCC|GoalSeekCoal|EnergyCons|MTInputs|Mitigation)")
TOK = re.compile(r"(?P<off>\+6,?3(?:31|17)(?!\d))|(?P<sheet>'?" + OTHER + r"'?(?=[!\s]))|"
                 r"(?P<ref>(?<![\w.,^])(?:\$?[A-Z]{1,3}\$?)?\d{3,5}(?!\w|[.,]\d|%))")


def remap_prose(t, sheet='Mitigation'):
    """Row numbers in prose: cell references, 'row(s) n, m-k', '(policy n)', bare numbers 1000-19219 (rows of
    Mitigation unless a sheet name stands just before), and the +6,331 / +6,317 offsets (now +6,316)."""
    out, pos, ctx, ctxpos = [], 0, sheet, -99
    for m in TOK.finditer(t):
        out.append(t[pos:m.start()])
        pos, s = m.end(), m.group(0)
        if m.group('sheet'):
            ctx, ctxpos = s.strip("'"), m.end()
            out.append(s)
            continue
        if m.group('off'):
            out.append('+6,316' if ',' in s else '+6316')
            continue
        mm = re.match(r'(\$?[A-Z]{1,3}\$?)?(\d+)', s)
        col, num = mm.group(1) or '', int(mm.group(2))
        cur = ctx if m.start() - ctxpos < 40 else sheet
        if cur in SIZE and num > SIZE[cur]:
            cur = 'Mitigation'
        if cur not in MAP['sheets']:
            out.append(s)
            continue
        if not col and not (1000 <= num <= MAP['sheets']['Mitigation']['last'] or (cur == 'MTInputs' and num >= 300)):
            out.append(s)
            continue
        if not col and 1900 <= num <= 2100 and re.search(r'(year|in|to|from|since|until|by)\s*$',
                                                        t[max(0, m.start() - 12):m.start()]):
            out.append(s)                                   # a year
            continue
        nr = mrow(cur, num)
        if nr is None:
            LOG.append(f'deleted in 465: {cur} {s}')
            out.append(s)
            continue
        if nr != num:
            LOG.append(f'{cur} {s} -> {col}{nr}')
        out.append(col + str(nr))
    out.append(t[pos:])
    return ''.join(out)


def is_formula(s):
    return s.strip().startswith(('=', '{'))


def do_json(path):
    plans = json.load(open(path, encoding='utf-8'))
    for b in plans:
        for k in ('where', 'why', 'ref', 'note'):
            if isinstance(b.get(k), str):
                b[k] = remap_prose(b[k])
        for f in b.get('fixes', []):
            cell = f['cell']
            sheet = cell.split('!')[0].strip("'") if '!' in cell else 'Mitigation'
            if re.match(r"('?[^!]+'?!)?[A-Z]+\d+$", cell):
                a = cell.split('!')[-1]
                c, r = re.match(r'([A-Z]+)(\d+)', a).groups()
                nr = mrow(sheet, int(r))
                if nr and nr != int(r):
                    f['cell'] = cell[:len(cell) - len(a)] + c + str(nr)
            for k in ('now', 'new'):
                v = f.get(k) or ''
                f[k] = remap_formula(v, sheet) if is_formula(v) else remap_prose(v, sheet)
            for k in ('fill', 'policy'):
                if f.get(k):
                    f[k] = remap_prose(f[k], sheet)
    json.dump(plans, open(path, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    open(path, 'a', encoding='utf-8').write('\n')


def do_py(path):
    src = open(path, encoding='utf-8').read()
    lines = src.splitlines(keepends=True)
    starts = [0]
    for ln in lines:
        starts.append(starts[-1] + len(ln))
    edits = []
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type != tokenize.STRING:
            continue
        a = starts[tok.start[0] - 1] + tok.start[1]
        b = starts[tok.end[0] - 1] + tok.end[1]
        s = src[a:b]
        m = re.match(r"([rRbBuUfF]*)('''|\"\"\"|'|\")", s)
        pre, q = m.group(1), m.group(2)
        inner = s[len(pre) + len(q):-len(q)]
        new = remap_prose(inner)
        if new != inner:
            edits.append((a, b, pre + q + new + q))
    for a, b, s in reversed(edits):
        src = src[:a] + s + src[b:]
    open(path, 'w', encoding='utf-8').write(src)


def do_text(path):
    s = open(path, encoding='utf-8').read()
    open(path, 'w', encoding='utf-8').write(remap_prose(s))


if __name__ == '__main__':
    mode, files = sys.argv[1], sys.argv[2:]
    for p in files:
        LOG.clear()
        {'json': do_json, 'py': do_py, 'text': do_text}[mode](p)
        print(f'== {p}: {len(LOG)} references')
        for x in LOG:
            print('  ', x)
