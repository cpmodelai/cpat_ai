"""Batch G (2026-10-29): the v0.9.0 plans (fixes_v0_9_0.json) whose entries described the new formula instead of
typing it, rewritten cell by cell from the 465 file (L176-L180, L185-L193, L195-L197, L199, L200, L202, L203, L215,
L219, L220, L222, L228, L229). Every "now" is read from the .xlsb (gen_F.cur) and every new formula is built by exact
text substitution of it where it can be; the script stops if a legacy text is not found and checks the brackets.
L224 (average vs marginal air-pollution damages) is a change of method, not a cell edit: its plan stays as written.

    python3 gen_G.py         (rewrites ../data/fixes_v0_9_0.json in place)
"""
import json
import os
import re

from openpyxl.utils import column_index_from_string as ci, get_column_letter as L

from xlsb465 import OFF, bal, cur, fx, paste, sub

HERE = os.path.dirname(os.path.abspath(__file__))
PLANS = os.path.join(HERE, '..', 'data', 'fixes_v0_9_0.json')
RES = 'none (results block, one copy only)'
SHARED = 'none (shared rows, one copy only)'
AP = "'Air pollution'!"


def cols(c0, c1):
    return [L(i) for i in range(ci(c0), ci(c1) + 1)]


REF = re.compile(r"(?<![A-Za-z_.])(\$?)([A-Z]{1,3})(\$?)(\d+)(?![\d(A-Za-z_])")


def shift(f, k):
    """A formula moved k columns right: relative column references shift (Excel's fill)."""
    return REF.sub(lambda m: m.group(0) if m.group(1) else
                   m.group(1) + L(ci(m.group(2)) + k) + m.group(3) + m.group(4), f)


def same_right(r, c0, c1, sheet='Mitigation'):
    """Check that a row is one formula filled right from c0 to c1."""
    first = cur(f'{c0}{r}', sheet)
    for c in cols(c0, c1)[1:]:
        got, exp = cur(f'{c}{r}', sheet), shift(first, ci(c) - ci(c0))
        assert got == exp, (sheet, f'{c}{r}', got, exp)


new = {}

# L176: the climate cost of other oil products is per barrel; the row says per GJ.
new['L176'] = [fx('L17704', sub('L17704', ('$G17680', '$G17680 / _conv_barrel_to_gj')), 'L17704:AE17704', RES)]

# L177: air-pollution cost of power: fuel use in GJ, not generation shares.
new['L177'] = [fx('L18090', '=(L17740*L$16850+L17743*L$16856+L17748*(L$16886+L$16868))*_conv_ktoe_to_gj/(L$17003*10^9)',
                  'L18090:AE18090 (L18102 =L18090 follows)', RES)]

# L178: coal and gas "other": each sector's cost weighted by its own use.
new['L178'] = [
    fx('L17750', sub('L17750', ('L17738 * L16911', 'L17738 * L16914'), ('L17740 * L16914', 'L17740 * L16911')),
       'L17750:AA17750 (AB:AE hold AA until L191)', RES),
    fx('L17751', sub('L17751', ('L17741 * L16917', 'L17741 * L16920'), ('L17743 * L16920', 'L17743 * L16917')),
       'L17751:AA17751 (AB:AE hold AA until L191)', RES)]

# L179: FFS benefits: each line takes the change in its own sector's fuel use.
new['L179'] = [fx(f'L{r}', sub(f'L{r}', (o, n)), f'L{r}:AE{r}', RES) for r, o, n in (
    (17767, '(L16911-L16850)', '(L16914-L16853)'), (17768, '(L16912-L16851)', '(L16913-L16852)'),
    (17769, '(L16914-L16853)', '(L16911-L16850)'), (17770, '(L16917-L16856)', '(L16920-L16859)'),
    (17772, '(L16920-L16859)', '(L16917-L16856)'))]

# L180: diesel road line: diesel litres and the road damage.
new['L180'] = [fx('L17774', sub('L17774', ('+L17759)', '+L17759+L17761)'), ('_conv_ktoe_liter_gso', '_conv_ktoe_liter_die')),
                  'L17774:AE17774', RES)]

# L185: other oil products: household share = buildings use / total use (as gasoline row 17789 for transport).
new['L185'] = [fx('L17836', '=IFERROR(L16888 / L16885, 0)', 'L17836:AE17836 (AE was =AD17836)', RES)]

# L186: kerosene litres.
new['L186'] = [fx('L17831', sub('L17831', ('_conv_ktoe_liter_die', '_conv_ktoe_liter_ker')), 'L17831:AE17831', RES)]

# L187: electricity "other": M:AE take the L formulas.
new['L187'] = [fx(f'M{r}', shift(cur(f'L{r}'), 1), f'L{r}:AE{r} (fill the L formula right)', RES)
               for r in (17939, 17941, 17943)]

# L188: subsidies in % of GDP of the same year.
new['L188'] = [fx('L17950', sub('L17950', ('/K$16082', '/L$16082')), 'L17950:AE17951 (both rows)', RES)]

# L189: residential gas: dollars per GJ like every other cost row (AP rows 3997-3998 for industry gas).
new['L189'] = [fx('L17742', f"={AP}K4378*{AP}K$741*time_factor*(1+{AP}K$1713)/_conv_ktoe_to_gj",
                  'L17742:AA17742 (AB:AE hold AA until L191)', RES)]
assert cur('F4378', 'Air pollution') == 'Deaths per ktoe' and cur('E4378', 'Air pollution') == 'nga'

# L190: LPG cost of the year.
new['L190'] = [fx('L17746', sub('L17746', ("!$K$4314", '!K$4314')), 'L17746:AA17746 (AB:AE hold AA until L191)', RES)]

# L191: AP has 2038-2040 (columns AA:AC): link them; 2041 = 2040 (issue I112).
for r in range(17738, 17753):
    for c, p in (('AB', 'AA'), ('AC', 'AB'), ('AD', 'AC'), ('AE', 'AD')):
        assert cur(f'{c}{r}') == f'={p}{r}', (c, r)
same_right(17738, 'L', 'AA')
new['L191'] = [
    fx('AB17738', shift(cur('AA17738'), 1),
       'AA17738:AD17752 (fill each row\'s AA formula right to AD; apply L178, L189, L190, L192 first); AE stays =AD',
       RES),
    fx('AD17717', "=IFERROR('Air pollution'!AC3217,AC17717)", 'single cell; AE17717 stays =AD17717', RES)]

# L192: residential coal switch: share of the year's residential use (row 5562), not of a typed 9127.
new['L192'] = [fx('L17739', sub('L17739', ('L16282/9127', 'IFERROR(L16282/L$5562,0)')),
                  'L17739:AA17739 (AB:AE hold AA until L191)', RES)]

# L193: Transport margins of LPG (#DIV/0! when LPG has no class use): 0.
new['L193'] = []
for r in (188, 223, 235, 268, 303, 315):
    same_right(r, 'I', 'AB', 'Transport')
    new['L193'].append(fx(f'I{r}', '=IFERROR(' + cur(f'I{r}', 'Transport')[1:] + ',0)', f'I{r}:AB{r}',
                          'none (rows 268, 303, 315 are the policy copies, listed)' if r > 240 else
                          f'row {r + 80} listed (Transport policy rows)', sheet='Transport'))

# L195 / L196: Pigouvian phase-in.
new['L195'] = [fx('L146', shift(cur('O146'), -3), 'L146:N146', SHARED)]
new['L196'] = [fx('O146', sub('O146', ('/$E$145', '/MAX($E$145,1)')), 'O146:AE146 (with L195: L146:AE146)', SHARED)]

# L197: CBAM process-emission lookup: a real formula, and unique codes for the fuel rows.
assert cur('L1905') == '=@INDEX(L$2170:L$14547,$J1905)'
new['L197'] = [fx('L1905', '=INDEX(L$2173:L$14755,$J1905)', 'L1905:AE1909', 'rows 1939-1943: J1939 =MATCH($G1939,'
                  '$H$2173:$H$14755,0) filled to J1943, and L1939 =INDEX(L$2173:L$14755,$J1939) filled to AE1943')]
for r in range(5996, 6002):
    new['L197'].append(fx(f'H{r}', sub(f'H{r}', ('.mit.cpe.', '.mit.cfe.') if r < 6001 else ('.mit.emis.', '.mit.cfe.')),
                          policy=paste(f'H{r}')))

# L199: CBAM prices: the scenario's carbon price, auctioned ETS price and shadow price, not typed 0.
new['L199'] = []
for r, src, txt in ((5869, 'L2251', '=L2727'), (5870, 'L2252', '=L2322'), (5871, 'L2009', '=L2346')):
    assert cur(f'K{r}') == txt and cur(f'L{r}') == '0.0', r
    new['L199'].append(fx(f'L{r}', f'={src}', f'L{r}:AE{r}', paste(f'L{r}', f'L{r}:AE{r}')))
    new['L199'].append(fx(f'K{r}', '(clear: the text of the intended link)', policy=f'K{r + OFF}: clear'))

# L200: CBAM fuel abatement at the carbon price (as rows 5985-5992), anchored parameter.
new['L200'] = []
for r in range(5974, 5982):
    old = cur(f'L{r}')
    k = r - 5974 + 5921
    n = re.sub(r'\(L5872\)', f'($F{k}*L5869+$G{k}*L5870)', old).replace(f'-(E{r})', f'-($E{r})')
    assert n != old
    new['L200'].append(fx(f'L{r}', bal(n), f'L{r}:AE{r} (replaces M:AE, incl. the drifting E5981 of M5981:AE5981)',
                          paste(f'L{r}', f'L{r}:AE{r}')))

# L202: post-policy process emissions: the L formulas filled right; the total row summed.
new['L202'] = [fx(f'M{r}', shift(cur(f'L{r}'), 1), f'L{r}:AE{r} (fill the L formula right)',
                  paste(f'L{r}', f'L{r}:AE{r}')) for r in (5996, 5997, 5998, 6000)]
new['L202'].append(dict(cell='L6012', now='(empty)', new='=SUM(L6007:L6011)', fill='L6012:AE6012',
                        policy=paste('L6012', 'L6012:AE6012')))

# L203: efficient-price display rows.
new['L203'] = [fx(f'L{r}', '=IFERROR(' + cur(f'L{r}')[1:] + ',"n.a.")', f'L{r}:AE{r}', RES) for r in (18096, 18108)]
for r, src in zip(range(18152, 18157), (18101, 18102, 18103, 18104, 18100)):
    k = cur(f'K{r}').replace('$AD', '$AE')
    n = re.sub(r'\$L(\$?)\d+:\$AE(\$?)\d+', lambda m: f'$L{m.group(1)}{src}:$AE{m.group(2)}{src}', k, count=1)
    new['L203'].append(fx(f'L{r}', n, policy=RES))
new['L203'].append(fx('L18157', sub('L18157', ('L18145:L18148)-L18149', 'L18152:L18155)-L18156')), policy=RES))
for r in range(18128, 18157):
    for c in ('K', 'L'):
        try:
            f = cur(f'{c}{r}')
        except AssertionError:
            continue
        if '$AD' in f and not (c == 'L' and 18152 <= r <= 18156):
            new['L203'].append(fx(f'{c}{r}', f.replace('$AD', '$AE'), policy=RES))

# L215: gas import bill at the $/GJ gas price (row 733, as the trade balance row 741).
new['L215'] = [fx('L18172', sub('L18172', ('*L709/', '*L733/')), 'L18172:AE18172', RES)]

# L219: the check column of the foo and srv rows reads a label row and a year row: no matching row, clear.
new['L219'] = [fx(c, '(clear: no food & forestry or services row in 18735-18742)', policy=RES) for c in ('J18747', 'J18748')]

# L220: cross-price defaults are the simple cross-price elasticities.
new['L220'] = [fx(f'L{r}', f'=Elasticities!G{r - 188}', policy='none', sheet='Manual inputs') for r in (319, 320, 321)]

# L222: the scenario-2 cost breakdown tests its own block's scenario name.
new['L222'] = [fx('T9825', sub('T9825', ('B$2173', 'B$8489')), 'single cell (the baseline T3509 tests B$2173, '
                  'correct)', 'this is the policy copy'),
               fx('P9824', sub('P9824', ('B$2173', 'B$8489')), 'single cell', 'this is the policy copy')]

# L228 / L229: LNG and Europe gas price rows swapped.
new['L228'] = [fx('K644', sub('K644', ('$H15:$BZ15', '$H17:$BZ17')), 'K644:P644 (Q:AE extend P)', SHARED),
               fx('K646', sub('K646', ('$H17:$BZ17', '$H15:$BZ15')), 'K646:P646 (Q:AE extend P)', SHARED)]
new['L229'] = [fx('K652', sub('K652', ('$M39:$BZ39', '$M41:$BZ41')), 'K652:AE652', SHARED),
               fx('K654', sub('K654', ('$M41:$BZ41', '$M39:$BZ39')), 'K654:AE654', SHARED)]

# Plans whose "now" was abbreviated or had its spaces removed: the exact 465 text (L173's "now" is the formula after
# L171, on purpose: its ref says so).
new['L184'] = [fx('L17814', '=L811', 'L17814:AE17814 (as the kerosene row 17825 =L816)', RES)]
new['L216'] = [fx('H18756', sub('H18756', ('=L18731/', '=L18730/')), policy=RES)]
new['L226'] = [fx('M4637', sub('M4637', ('* M4628', '* M4630')), 'M4637:AE4637', paste('M4637', 'M4637:AE4637'))]
new['L227'] = [fx('L4555', '=L4509*L4456+SUM(L4565:L4567)+(L4562*$J4326)/L4531*(1-(1/(1+L4531)^($J4322+1)))*0.5'
                  '+$J4327*L4509+L4520*L4396/L4397', 'L4555:AE4555', paste('L4555', 'L4555:AE4555'))]

# Plans written as one entry for several cells: one entry per cell.
new['L221'] = [fx(f'H{r}', f'=H{s}', policy='none', sheet='Elasticities')
               for r, s in ((29, 145), (30, 146), (37, 153), (38, 154), (45, 161), (46, 162))]
new['L225'] = [fx(f'L{r}', sub(f'L{r}', ('*$E$17956', '*L$17787')), f'L{r}:AE{r}',
                  'none: the block is computed for the live scenario only (I120)')
               for r in (17969, 17984, 17996, 18008, 18032, 18068, 18104)]

plans = json.load(open(PLANS, encoding='utf-8'))
done = set()
for b in plans:
    if b['id'] in new:
        b['fixes'] = new[b['id']]
        b['note'] = ((b.get('note') or '') + ' Cells written out from the 465 file on 2026-10-29 (tools/gen_G.py).'
                     ).strip()
        done.add(b['id'])
assert done == set(new), set(new) - done
json.dump(plans, open(PLANS, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
left = [(b['id'], f['cell']) for b in plans for f in b['fixes'] if not f['new'].startswith(('=', '('))]
print('rewrote', len(done), 'plans,', sum(len(v) for v in new.values()), 'entries; described entries left:', left)
for k in sorted(new, key=lambda c: int(c[1:])):
    for e in new[k][:2]:
        print(k, e['cell'], '|', e['now'][:60], '=>', e['new'][:90])
