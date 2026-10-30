"""Batch F (2026-10-29): cell plans of the last legacy bugs without one (L129-L134, L137, L169), in the 465 file.

Every "now" is read from the .xlsb itself (formulas by dec465.py, constants from the cell records); every new formula
is built by exact text substitution of it, stops if the legacy text is not found and checks the brackets (as gen_A-E).
Output: ../data/fixes_other_mitigation_3.json. Needs pyxlsb2 (dec465.py).

    python3 gen_F.py
"""
import json
import os

from xlsb465 import OFF, bal, cur, fx, paste, pol, sub, wrap_lower

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data', 'fixes_other_mitigation_3.json')

plans = []

# ------------------------------------------------------------------ L129
fixes = []
for r in range(2785, 2789):                       # renewable subsidy by technology
    a = f'L{r}'
    fixes.append(fx(a, sub(a, ('=L2743+L2745', '=L2745')), f'L{r}:AE{r} (fill right only: the rows read the same '
                    'rows 2743/2745, so do not fill down)', paste(a, f'L{r}:AE{r}')))
for r in range(2947, 2952):                       # subsidy by technology, GWh basis
    a = f'L{r}'
    fixes.append(fx(a, sub(a, ('(L2743+L2745)*', 'L2745*')), f'L{r}:AE{r} (fill right only)', paste(a, f'L{r}:AE{r}')))
plans.append(dict(
    id='L129', pri='Medium', title='Baseline renewable subsidy counted twice',
    where='Mitigation rows 2785-2788 and 2947-2951 (policy 9101-9104, 9263-9267), against rows 2743, 2745',
    why='Row 2743 is the baseline renewable subsidy (-$E2734, MTInputs RenewableSubsidyBL) and row 2745 "New renewable '
        'electricity subsidy" is that baseline less the additional subsidy phased in (=L2743-IF(year>=start, $E2735 x '
        'phase)), so row 2745 already includes row 2743. Rows 2785-2788 (subsidy by wind, solar, hydro, other '
        'renewables) add L2743+L2745 and rows 2947-2951 multiply (L2743+L2745) by the generation share: the baseline '
        'subsidy is counted twice. Row 3143 ("New renewable energy subsidy") reads row 2745 alone, as it should. '
        'The register named rows 7883-7886 as the policy copies; in 465 they are 9101-9104 and 9263-9267 (7883-7886 '
        'are other rows that do not read 2743).',
    fixes=fixes,
    ref='Row 3143 (=L2745): the total new renewable subsidy read once.',
    effect='None for Egypt (no baseline renewable subsidy: E2734 = 0). With a baseline subsidy, the subsidy per '
           'technology (rows 2785-2788) and its cost (rows 2947-2951, and the power cost and fiscal rows they feed) '
           'fall by the baseline amount.',
    note='9 baseline rows x 20 years (L:AE), and the same 9 rows in the policy block. Each row is typed with its own '
         'row references (all read rows 2743/2745), so fill each row to the right, never down.',
    status='fix', prototype='Fixed (prototype: one renewable subsidy row rnsp = baseline + additional, counted once).'))

# ------------------------------------------------------------------ L130
plans.append(dict(
    id='L130', pri='Low', title='Intensity NDC: conditional and unconditional rows use different base years',
    where='Mitigation F18456:H18456 (NDC block, shared by both scenarios)',
    why='Row 18455 (unconditional target intensity) applies the cut to the baseline intensity of the NDC reference '
        'year (row 18453); row 18456 (conditional) applies it to the baseline intensity of the target year (row '
        '18454). An intensity target is a cut on the reference-year intensity, so the two targets are not comparable '
        'and the conditional one moves with the projected baseline.',
    fixes=[fx(f'{c}18456', sub(f'{c}18456', (f'{c}18454*', f'{c}18453*'))) for c in 'FGH'],
    ref='Row 18455 (unconditional): the same formula on row 18453.',
    effect='Only for countries with an intensity NDC and a conditional target (not Egypt). The conditional target '
           'intensity and target emissions (rows 18456, 18459, 18457, 18460) change.',
    note='Three cells (F excludes LULUCF, G includes it, H CO2 only), no fill.',
    status='fix', prototype='Fixed (prototype 14c: ndc.hi applies the cut to the reference-year intensity x target-year '
                            'GDP, for both).'))

# ------------------------------------------------------------------ L169
plans.append(dict(
    id='L169', pri='Low', title='Intensity NDC: China CO2 hard-coded',
    where='Mitigation H18449',
    why='H18449 (CO2 emissions in the NDC reference year) returns 5665 for China instead of the data in row 889, '
        'which F18449 and G18449 read for their own gases.',
    fixes=[fx('H18449', sub('H18449', ('=IF(_Country_code="CHN",5665,IF(', '=IF('), ('"NA"))', '"NA")')))],
    ref='F18449, G18449: INDEX of rows 885 and 886 by the reference year.',
    effect='China only (an intensity NDC with CO2 cover); no effect for Egypt.',
    note='If 5665 was a deliberate correction of the China data, put it in the data (GHGs) instead.',
    status='fix', prototype='Fixed (v0.5.7): no hard-coded value; data or model (departure by design, user rule: data '
                            'not typed).'))

# ------------------------------------------------------------------ L131
cc = 'LOWER(_Country_code)&".mit.'
fixes = [fx('H466', sub('H466', ('.mit.gdp.pre.lvl.1"', '.mit.ln.gdppc"')))]
for r, tok in ((7736, 'rev.ctx.tot.usd'), (7737, 'rev.ctx.tot.pct'), (7756, 'rev.exc.tot.usd'),
               (7757, 'rev.exc.tot.pct'), (7999, 'rev.tot.tot.usd'), (8000, 'rev.tot.tot.pct')):
    old = 'sub.new.' + tok[-3:]
    fixes.append(fx(f'H{r}', sub(f'H{r}', (f'.mit.{old}.', f'.mit.{tok}.')), policy=paste(f'H{r}')))
for c in ('G17161', 'G17163'):
    fixes.append(fx(c, sub(c, ('.mit.sub.new.pct.', '.mit.rev.new.pct.')), policy='none (results block; G17163 is '
                    'the policy row)'))
for r, tok in ((7655, 'gso'), (7656, 'die'), (7657, 'lpg'), (7658, 'ker'), (7659, 'bio'), (7660, 'ecy')):
    fixes.append(fx(f'H{r}', sub(f'H{r}', ('.mit.rev.ctr.coa.', f'.mit.rev.ctr.{tok}.')), policy=paste(f'H{r}')))
plans.append(dict(
    id='L131', pri='Low', title='Codes: one output code on rows with different contents',
    where='Mitigation H466, H2442 (gdp.pre.lvl); H7736:H7737, H7756:H7757, H7999:H8000 and policy copies (sub.new); '
          'H7652:H7660 and policy (rev.ctr.coa); readers G17161, G17163',
    why='Legacy reuses a code for other quantities, and a lookup by code (MATCH on $H$2173:$H$14755, the results '
        'block) finds the first row only. (1) gdp.pre.lvl.1 is ln(GDP per capita) in H466 and GDP in $mn in H2442 '
        '(MTOutputs already calls row 466 egy.mit.ln.gdppc, E33). (2) sub.new.usd/pct is on three subtotals: '
        'carbon-price revenue by fuel (7736/7737), additional excise (7756/7757) and total revenue by fuel '
        '(7999/8000). (3) rev.ctr.coa.usd is on the coal row and also on gasoline, diesel, LPG, kerosene, biomass '
        'and electricity (7655-7660). Effect on values: results row 17161 "Revenues - baseline, % GDP" looks up '
        'sub.new.pct.1 and finds row 7737 (carbon-price revenue only, 0 in the baseline), while its US$ partner '
        '17160 reads the total revenue (rev.new.usd, row 8012); the same for the policy rows 17163 (finds 14053) and '
        '17162. Egypt, Carbon tax: 17163 shows 0.0015% of GDP in 2040 where the total is -0.0215%, so 17165 '
        '("Additional revenues ... % GDP") is 0.0015 where it should be 0.0029.',
    fixes=fixes,
    ref='Rows 8012/8013 (Total revenues, rev.new.usd/pct): the totals that results rows 17160 and 17162 read; '
        'MTOutputs E33 (egy.mit.ln.gdppc).',
    effect='Results rows 17161, 17163 and 17165 (revenues in % of GDP) become the total revenue, consistent with the '
           'US$ rows 17160, 17162 and 17164. The other renames change no value (no formula reads those codes); a '
           'reader of the codes by name (MTOutputs, the data link) finds the right row.',
    note='The copies H8355 (=H7999) and H14671 (=H14315) follow. New codes checked absent from the file. A scan of '
         'column H finds 890 codes on more than one row; most are copy rows or the same quantity shown twice '
         '(e.g. sections 11-12 repeat earlier rows). This plan fixes the reuses the register names, the ones with a '
         'reader or a different quantity; give copy rows no code (as the prototype does) when the code list is '
         'cleaned up as a whole. Not fixed here: the ctxnew.<fuel>.<sector> codes of the implied carbon price '
         '(rows 2308-2320) repeat in rows 2330-2342 and 2354-2366 (no reader finds them by code).',
    status='fix', prototype='Fixed (v0.7.2, codes R7): every prototype code is unique (check_codes; the 18 copy rows '
                            'carry no code).'))

# ------------------------------------------------------------------ L132
fixes = []
for a0, a1 in ((6668, 6678), (6770, 6780), (6872, 6882), (6974, 6984), (7076, 7086), (7178, 7188), (7283, 7295),
               (7387, 7397)):
    for r in range(a0, a1 + 1):                    # every cell is typed with its own pollutant anchor
        wrap_lower(f'H{r}')
    fixes.append(fx(f'H{a0}', wrap_lower(f'H{a0}'),
                    f'each cell of H{a0}:H{a1} the same way: wrap its own formula in LOWER( ) (do not fill down: the '
                    'pollutant anchor is relative)', f'H{a0 + OFF}:H{a1 + OFF}: the same edit (or paste the baseline '
                    'cells: +6,316 rows)'))
for r, old in ((2320, 'C2175'), (3643, 'C2186'), (3644, 'C2186')):
    fixes.append(fx(f'H{r}', sub(f'H{r}', (old, 'C2173')), policy=paste(f'H{r}')))
for a0, old, tok in ((3315, 'C2184', 'ltc'), (3474, 'C2033', 'gnb')):
    for r in range(a0, a0 + 9):
        assert cur(f'G{r}') == cur(f'G{a0}')
    fixes.append(fx(f'G{a0}', tok, f'G{a0}:G{a0 + 8} (constant)', f'G{a0 + OFF}:G{a0 + 8 + OFF}: the same constant'))
    for r in range(a0, a0 + 9):
        fixes.append(fx(f'H{r}', sub(f'H{r}', (old, 'C2173')), policy=paste(f'H{r}')))
for r in range(3225, 3234):                       # copies of rows 3282-3290 (=L3282): no code
    fixes.append(fx(f'H{r}', '(clear: copy row, no code)', policy=f'H{r + OFF}: clear'))
fixes += [fx('G7589', 'n2o', policy='G13905: the same constant'),
          fx('H7589', sub('H7589', ('C2174', 'C2173')), policy=paste('H7589')),
          fx('F7590', 'fug', policy='F13906: the same constant'),
          fx('H7590', sub('H7590', ('C2186', 'C2173')), policy=paste('H7590')),
          fx('G17215', '(clear: difference row, no code)', policy='none (results block)'),
          fx('H17215', '(clear)', policy='none (results block)')]
plans.append(dict(
    id='L132', pri='Low', title='Codes: capitals and empty tokens',
    where='Mitigation H6668:H7397 (8 pollutant blocks, 90 cells) and policy H12984:H13713; 67 codes with an empty '
          'scenario token (H2320, H3225:H3233, H3315:H3323, H3474:H3482, H3643:H3644, H7589:H7590, H7620, G17215 and '
          'policy copies)',
    why='(1) Capitals: the code formulas of the "All" rows of the local-pollutant blocks join the label in column D '
        '("All") into the code, so the code reads em.pm2.All.pow.1 against the lower-case protocol (180 codes). '
        '(2) Empty tokens: 67 codes end with "." because their scenario number points to a blank cell (C2175, '
        'C2184, C2033, C2186, C2174, C2165, C$1678; policy C8491, C8500, C8349, C8502, C8490, C8481, C$1678) '
        'instead of C2173 (policy C8489). A lookup of the protocol code fails: results row 16236 (current carbon tax '
        'on industrial electricity, ctx.ind.ecy.t.1) finds nothing and IFNA returns 0. Adding the number alone '
        'would make some codes equal to another row\'s: rows 3315-3323 (levelised transmission costs) would take '
        'fix.pow.<type>.t.1 of rows 3247-3255 (levelised fixed costs), rows 3474-3482 (generation costs before '
        'storage and carbon tax) gnc of rows 3486-3494, row 7589 (fugitive N2O) the CH4 code of row 7588 (its gas '
        'token is ch4), row 7590 (fugitive total) the total of row 7586. Those rows get their own variable token; '
        'rows 3225-3233 are copies of rows 3282-3290 (=L3282) and lose their code.',
    fixes=fixes,
    ref='Row 3646 (rp.ind.ecy.t.1: the same block with C2173); the code formulas of the other blocks.',
    effect='Codes only, except results row 16236, which then finds row 3643 instead of nothing (IFNA 0); row 3643 is '
           'the new policy\'s carbon cost, not the current carbon tax the row is labelled with, so L230 replaces that '
           'lookup. Excel\'s MATCH ignores case, so lower-casing changes no lookup in the workbook (the Air pollution '
           'readers build the same codes with "All").',
    note='Row 7620 (NOx forcing, oc.tot.) is fixed by L133. H2320 then shares ctxnew.oop.pow.1 with rows 2342 and '
         '2366, like the rest of its block (see L131). Policy cells: pasting a baseline cell gives the policy formula '
         '(C2173 becomes C8489; the blank references of the policy copies are the baseline ones +6,316). '
         'Results rows 16250 and 16251 look up '
         'ets.ind.ecy.t.1 and ets.res.ecy.t.1, which no row of the model carries: bug L230. '
         'New tokens ltc (levelised transmission cost) and gnb (generation cost before storage and carbon tax) are '
         'proposals; checked absent from the file.',
    status='fix', prototype='Fixed (v0.7.2): prototype codes are lower case with no empty token (code formula; '
                            'check_codes).'))

# ------------------------------------------------------------------ L133
plans.append(dict(
    id='L133', pri='Low', title='Codes: nox.tot holds N2O, oc.tot. holds NOx',
    where='Mitigation H7614, H7620 (policy H13930, H13936); readers G18242, G18247 (MTOutputs E84, E89)',
    why='Row 7614 "Nitrous oxide (N2O)" carries the code nox.tot and row 7620 "Nitrogen oxides (NOx, exc. N2O)" '
        'carries oc.tot., organic carbon\'s code with a blank scenario number (C2165). A reader of the codes takes '
        'one gas for the other. The results rows 18242/18247 (N2O) look up nox.tot and MTOutputs E84/E89 publish '
        'it as the N2O output.',
    fixes=[fx('H7614', sub('H7614', ('.mit.nox.tot.', '.mit.n2o.tot.')), policy=paste('H7614')),
           fx('H7620', sub('H7620', ('.mit.oc.tot."&C2165', '.mit.nox.tot."&C2173')), policy=paste('H7620')),
           fx('G18242', sub('G18242', ('.mit.nox.tot.', '.mit.n2o.tot.'))),
           fx('G18247', sub('G18247', ('.mit.nox.tot.', '.mit.n2o.tot.')), policy='none (results block; the policy '
              'row)')],
    ref='Rows 7612-7622: the other gases carry their own token (co2.tot, ch4.tot, bc.tot, oc.tot on row 7621).',
    effect='Codes only: rows 18242/18247 still find the N2O rows, so no value changes. MTOutputs E84/E89 '
           '(=Mitigation!G18242/G18247) and the copy H8339 (=H7614) follow: the published N2O code becomes '
           'egy.mit.n2o.tot.<n>; tell the users of MTOutputs.',
    note='n2o.tot is new in the file (checked); nox.tot is then only the NOx row.',
    status='fix', prototype='Fixed (v0.7.2, codes R5): n2o.tot and nox.tot carry their own gas.'))

# ------------------------------------------------------------------ L134
plans.append(dict(
    id='L134', pri='Low',
    title='Price-increase units: other oil products "$/bbn", default "$/liter" for other oil products and biomass',
    where='Dashboard T38; MTInputs G182, G183 (E182:F183 and Mitigation I177, I180 follow)',
    why='MTInputs E178:E183 is the array =TRANSPOSE(Dashboard!$H$38:$U$38), so the "$/bbn" of E182 is typed on the '
        'Dashboard (T38). The default column G types "$/liter" for other oil products (G182) and biomass (G183), '
        'whose prices are per barrel and per GJ (the Dashboard says $/GJ for biomass, U38). F picks E or G, and '
        'Mitigation I177 and I180 show F182 and F183.',
    fixes=[fx('T38', '$/bbl', policy='none', sheet='Dashboard'),
           fx('G182', '$/bbl', policy='none', sheet='MTInputs'),
           fx('G183', '$/GJ', policy='none', sheet='MTInputs')],
    ref='Dashboard H38:S38 and U38 (the units of the other fuels).',
    effect='Labels only: no formula reads them for a value. A user who sets the defaults no longer sees a per-liter '
           'unit for these two fuels.',
    note='Constants; nothing to fill.',
    status='fix', prototype='Fixed (v0.8.3): the prototype\'s ScenarioDefinition rows 182-183 read $/bbl and $/GJ, '
                            'defaults included.'))

# ------------------------------------------------------------------ L137
rows = list(range(53, 55)) + list(range(56, 60)) + list(range(61, 65)) + list(range(84, 94)) + list(range(95, 98))
fixes = []
for r in rows:
    old = cur(f'H{r}', 'MTInputs')
    assert old.startswith('D_'), (r, old)
    fixes.append(fx(f'H{r}', old[2:], policy='none', sheet='MTInputs'))
assert cur('H343', 'MTInputs') == 'ElasticityModel '
fixes.append(fx('H343', 'ElasticityModel', policy='none', sheet='MTInputs'))
plans.append(dict(
    id='L137', pri='Low', title='MTInputs NameOfParameter: Dashboard names on 23 inputs, a trailing space on one',
    where='MTInputs H53:H64, H84:H97 (23 D_ names), H343',
    why='Column H names each input. 23 feebate and ETS inputs carry the names of their Dashboard cells (D_FeebateIntro '
        '= Dashboard!D31, ...), where every other input carries its own name (D_<name> is the Dashboard cell, <name> '
        'the MTInputs value). H343 reads "ElasticityModel " with a trailing space (the defined name is '
        'ElasticityModel). A lookup by name finds the Dashboard cell or nothing.',
    fixes=fixes,
    ref='MTInputs H342 (CostBreakdownYear), H344 (kDispatch): the input\'s own name.',
    effect='Text only: no formula and no macro of the workbook reads column H (checked: formulas of every sheet and '
           'the VBA project). The multi-run tool and any outside reader of NameOfParameter find the inputs by their '
           'own names.',
    note='Rename only the text in column H; the Dashboard defined names D_* stay as they are.',
    status='fix', prototype='Fixed (v0.8.4): the prototype names drop the D_ prefix (FeebateIntro, NewETS, ETSIntro, '
                            '...) and the space; the legacy name is kept in the codes map (tab Inputs).'))

# ------------------------------------------------------------------ L230 (found 2026-10-29 while planning L132)
KWH = {'coa': ('_conv_kWh_to_GJ', 3061, 3452), 'nga': ('_conv_kWh_to_GJ', 3062, 3453),
       'oop': ('(_conv_kWh_to_GJ/_conv_barrel_to_gj)', 3063, 3454)}      # as rows 3385-3387 (oil per barrel)


def per_kwh(rows):
    """Current carbon price of the power fuels per kWh consumed, as rows 3385-3395 do for the new policy."""
    return '=(' + '+'.join(f'L${r}*{c}/L${e}*L${g}' for r, (c, e, g) in zip(rows, KWH.values())) + ')/$J$3395'


for r, lab in ((2462, 'current carbon tax'), (2531, 'current carbon tax'), (2692, 'current carbon tax'),
               (2463, 'current ETS'), (2532, 'current ETS'), (2693, 'current ETS')):
    assert lab in cur(f'D{r}'), (r, cur(f'D{r}'))
assert cur('L3387') == '=L3090*(_conv_kWh_to_GJ/_conv_barrel_to_gj)/L3063' and cur('J3395') == '=1/I3723'
fixes = []
for r, src in ((16236, (2462, 2531, 2692)), (16237, (2462, 2531, 2692)), (16250, (2463, 2532, 2693)),
               (16251, (2463, 2532, 2693))):
    fixes.append(fx(f'L{r}', bal(per_kwh(src)), f'L{r}:AE{r}', 'none (results block; the rows are scenario 1)'))
    fixes.append(fx(f'J{r}', '(clear: the row no longer looks up a code)', policy='none (results block)'))
plans.append(dict(
    id='L230', pri='Low', title='Electricity: current carbon tax and ETS outputs never see the existing carbon price',
    where='Mitigation L16236:AE16237 (current carbon tax, electricity), L16250:AE16251 (current ETS, electricity); '
          'published by MTOutputs K229:K230, K242:K243 and rows 16702-16703',
    why='The results rows for the current (existing) carbon tax and ETS on electricity look up a power-price row by '
        'code. Rows 16236/16237 (current carbon tax) find ctx.ind.ecy.t / ctx.res.ecy.t, the rows "Policy (usually '
        'carbon price)" 3643/3614, which carry the new policy\'s carbon cost (row 3395, from the "total new policy" '
        'rows 2468, 2537, 2698): 0 in scenario 1 by construction. Rows 16250/16251 (current ETS) look up '
        'ets.ind.ecy.t.1 / ets.res.ecy.t.1, which no row carries (IFNA 0). The existing carbon tax and ETS of the '
        'power fuels (rows 2462-2463 coal, 2531-2532 gas, 2692-2693 oil) never reach these outputs, so a country '
        'with a carbon tax or ETS on power reports 0 for electricity.',
    fixes=fixes,
    ref='Rows 3385-3395: the new policy\'s carbon cost per kWh consumed (fuel cost per GJ / efficiency x generation '
        'share, / transmission factor J3395); the same chain on the existing carbon price rows.',
    effect='None for Egypt (no existing carbon tax or ETS on power). Elsewhere the current carbon tax and ETS on '
           'electricity (results 16236-16251, MTOutputs K229:K230 and K242:K243, rows 16702-16703) show the '
           'existing carbon price per kWh instead of 0. Industry and residential get the same value: the price is '
           'upstream, before pass-through and VAT.',
    note='Found 2026-10-29 while planning L132 (the empty code token of row 3643). The G codes of the four rows stay '
         '(MTOutputs names them); only the lookup goes.',
    status='fix', prototype='Not built in the prototype (it has no current-carbon-price output for electricity): '
                            'nothing replicated.'))

json.dump(plans, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote', os.path.normpath(OUT), len(plans), 'bugs', sum(len(p['fixes']) for p in plans), 'cell entries')
for p in plans:
    for f in p['fixes'][:3]:
        print(p['id'], f['cell'], '|', f['now'][:70], '=>', f['new'][:80])
