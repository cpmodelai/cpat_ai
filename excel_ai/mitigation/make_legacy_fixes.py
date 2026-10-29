"""Priorities, fixes and effects of the legacy bugs (read by register.py), and the deck counts (v8.4: LegacyBugFixes.md
retired; its content is in Legacy_CPAT_Bugs_v<version>.docx and the tracker).

The register holds every bug found in legacy CPAT while rebuilding it (L1-L24). This script writes the short list the
legacy team needs: priority, where the bug is, the fix, and the effect, highest priority first. Priorities:
High = changes the results of standard runs (Egypt); Medium = changes results in some runs or countries, or a reported
number; Low = latent (no effect in the Egypt runs) or cosmetic.

    python make_legacy_fixes.py
"""
import json
import os

import build as B
import issues_register as R

HERE = os.path.dirname(os.path.abspath(__file__))
PRIORITY = {'L1': 'High', 'L3': 'High', 'L13': 'High', 'L18': 'High', 'L19': 'High', 'L20': 'High', 'L24': 'High',
            'L2': 'Medium', 'L5': 'Medium', 'L6': 'Medium', 'L14': 'Medium', 'L15': 'Medium', 'L16': 'Medium',
            'L21': 'Medium', 'L22': 'Medium',
            'L42': 'Medium', 'L43': 'Medium', 'L44': 'Low', 'L45': 'Low', 'L46': 'Low', 'L47': 'Low', 'L48': 'Low',
            'L49': 'Medium', 'L50': 'Low', 'L51': 'Low',
            'L52': 'Medium', 'L53': 'High', 'L54': 'Medium', 'L55': 'Low', 'L56': 'Low', 'L57': 'Medium', 'L58': 'Medium', 'L59': 'Medium', 'L60': 'Low', 'L61': 'Low', 'L62': 'Low', 'L63': 'Low', 'L64': 'Low', 'L65': 'Low', 'L66': 'Low', 'L67': 'Medium',
            'L68': 'Medium', 'L69': 'Low', 'L70': 'Low', 'L71': 'Low', 'L72': 'Low', 'L73': 'Low', 'L75': 'Low',
            'L76': 'Low', 'L77': 'Medium', 'L78': 'Low', 'L79': 'Medium', 'L80': 'Low',             # v4.15
            'L81': 'Low', 'L82': 'Low', 'L83': 'Medium', 'L84': 'Low', 'L85': 'Low', 'L86': 'Low', 'L87': 'High',
            'L88': 'Medium', 'L89': 'Low',                                                        # v4.16
            'L90': 'Low', 'L91': 'Low', 'L92': 'Low', 'L93': 'Low', 'L94': 'Low',                 # v5.1: residential
            'L95': 'Low', 'L96': 'Low', 'L97': 'Low', 'L112': 'Medium', 'L113': 'Low', 'L114': 'Low', 'L115': 'Medium', 'L116': 'Low', 'L117': 'Low', 'L118': 'Medium', 'L119': 'Medium', 'L120': 'Low', 'L121': 'Low', 'L122': 'Medium', 'L123': 'Medium', 'L124': 'Low', 'L125': 'Low', 'L126': 'Medium', 'L127': 'Low', 'L128': 'Low', 'L129': 'Medium', 'L130': 'Low',
            'L107': 'Low', 'L108': 'Medium', 'L109': 'Low', 'L110': 'Low', 'L111': 'Low',   # v5.4
            'L98': 'Medium', 'L99': 'Medium', 'L100': 'Low', 'L101': 'Low', 'L102': 'Low', 'L103': 'Low', 'L104': 'Low', 'L105': 'Medium', 'L106': 'Low',   # v5.2                                             # v5.1: team tracker
            'L4': 'Low', 'L7': 'Low', 'L8': 'Low', 'L9': 'Low', 'L10': 'Low', 'L11': 'Low', 'L12': 'Low', 'L23': 'Low', 'L131': 'Low', 'L132': 'Low', 'L133': 'Low', 'L134': 'Low'}
ORDER = {'High': 0, 'Medium': 1, 'Low': 2}
DECK = os.path.join(HERE, 'presentation', 'img', f'v{B.VERSION.replace(".", "")}_legacy.json')   # for the deck
SHORT = {  # one-line effect of each high-priority bug (deck)
    'L1': 'Services electricity demand follows the industry multiple: the largest single power-demand error',
    'L3': 'Income factor applied twice: the GDP elasticity drifts, error growing to 2040',
    'L13': 'Other oil products priced at the 0.01 floor: their fuel use rises tenfold by 2030',
    'L18': 'Non-energy methane flat: a methane fee on farming and waste does nothing',
    'L19': 'CO2 from flaring booked as methane',
    'L20': 'Population 185 million in 2041 instead of 147 million (UN)',
    'L24': 'GDP effect added to growth every year: +0.5% compounds to about +10% of GDP',
    'L53': 'Actual capacity factors never used: the studies value always applies, the override bounds never act',
    'L87': 'Regulation scenarios (energy efficiency, feebates, fuel economy) have no effect: share fixed at 0'}
FIX = {  # L11 onwards (the register records what the prototype did; this is what legacy should do), effect
    'L11': ('Remove the $G4291 x total term (or point it to the intended cell).',
            'None while G4291 stays empty; wrong dispatch if anything is typed there.'),
    'L12': ('Sum the nine generation types instead of multiplying by $X3008.', 'Reported total investment is 0.'),
    'L13': ('Take pass-through and margin of other oil products from the IMF price dataset, like the other oil '
            'products.', 'Retail price falls to the 0.01 floor with the oil price; fuel use rises tenfold by 2030 '
            '(Egypt).'),
    'L14': ('Apply (1 - pass-through) once in the first projected year.',
            'Taxes jump in the first projected year when pass-through is between 0 and 1 (none for Egypt: 0 or 1).'),
    'L15': ('Use the volatility inputs of the ETS+LTS table instead of the fixed 1.1.',
            'The ETS price effectiveness ignores the volatility inputs.'),
    'L16': ('Use the log form: price = LN(cap / baseline) / (semi-elasticity x effectiveness).',
            'The fast ETS price estimate is off for large cuts, so the goal seek starts far from the answer.'),
    'L18': ('Grow livestock, rice and waste methane with their drivers (income, population) and apply the abatement '
            'shares already computed in rows 6168, 6180, 6192.',
            'Non-energy methane is flat and a methane fee on agriculture and waste has no effect.'),
    'L19': ('Report the CO2 from flaring as CO2 in energy, not divided by the CH4 GWP in the CH4 row.',
            'Methane overstated and CO2 understated when the fee abates oil and gas methane.'),
    'L20': ('Use the UN WPP population of sheet UNPop (or fix the growth path).',
            'Egypt reaches 185 million in 2041 instead of 147 million; agriculture, waste and other GHGs too high '
            'after 2030.'),
    'L21': ('Use the waste curve of CH4Inputs for waste (row 6192 now = M6168, the livestock share).',
            'Waste methane is abated as if it were livestock.'),
    'L22': ('Add domestic navigation to the transport and total pollutant rows.', 'Pollutant totals miss navigation.'),
    'L23': ('Add services and food & forestry to the total of each pollutant.',
            'None for Egypt (they emit zero there); totals too low wherever they emit.'),
    'L24': ('Raise the GDP level by the effect: growth = (1 + g) x (1 + e(t-1)) / (1 + e(t-2)) - 1, not g + e.',
            'A steady effect of 0.5% compounds to about +10% of GDP after 20 years, in every run with endogenous '
            'GDP effects (the NoPropData file strips these rows).'),
    'L42': ('Use the standard form: (1 + g)^(eps_Y x income factor) x (1 + shock), the shock once, jet fuel with its '
            'own (oil) income elasticity.', 'Jet fuel x0.87 (2023) to x1.07 (2040) against the standard form.'),
    'L43': ('Point the income factor to row 2433 and add the additional-efficiency term.',
            'Other energy use flat with GDP: about -46 ktoe (2030) and -124 ktoe (2040) for Egypt.'),
    'L44': ('Read the other-oil-products price (row 5548).', 'None for Egypt today.'),
    'L45': ('Subtract the fossil change once, use the kerosene rows for kerosene, conserve the substituted energy.',
            'None while BiomassLeakage = No.'),
    'L46': ('Use the biofuel price, the shadow price through eps_F, the efficiency term and the road efficiency row.',
            'None for Egypt (no road biofuels).'),
    'L47': ('Use the shock row 2439.', 'None for Egypt (no self-generated renewables).'),
    'L48': ('Apply the income factor, start from the exempt share, and match the starred defaults.',
            'None (the initial exempt share is 0).'),
    'L49': ('Multiply the oil change in use by the share traded of row 742, as for gas and coal.',
            'Reported balance of payments only: the oil effect is about twice too large (Egypt 2030: 3.2 bn USD).'),
    'L50': ('Read the WEO current account (BCA), drop the one-column lag and check the sign of policy net imports.',
            'Reported balance of payments only (the % of GDP panel shows errors).'),
    'L51': ('Value the coal trade balance at the coal price (row 732), not the oil price (row 731).',
            'Reported energy trade balance only (Egypt: about 0.6 bn USD a year).'),
    'L52': ('Swap the branches of the ISERROR test (take the country value where it exists).',
            'Power: solar fixed O&M of Egypt 11.831 instead of 15 $/kW/y (other renewables: no country data).'),
    'L53': ('Search the installed capacity by FirstYearCalculations over all year columns (Power F:AC).',
            'Power: actual capacity factors where data exist (Egypt: all types with capacity), base capacities change.'),
    'L54': ('Test the hydro generation share (row 3846), not the year header.',
            'Power: hydro investment from NewInvHydYear (2030) unless hydro is above 50%.'),
    'L55': ('Search the country block (Power rows 110-294) before the regional block.', 'None for Egypt.'),
    'L56': ('Flag countries without CoC fixed data instead of using Sri Lanka.', 'None for Egypt.'),
    'L57': ('Estimate the ETS price in log form, LN(cap / baseline) / (semi-elasticity x effectiveness).',
            'New ETS scenarios: the quick estimate meets the cap (legacy relies on the VBA goal seek).'),
    'L58': ('Map subsectors without a GAINS match to the nearest GAINS subsector (services as residential, rail as '
            'road, industry as manufacturing).', 'Local pollutants of services, rail and industry no longer zero.'),
    'L59': ('Give a fuel without a GAINS factor the nearest GAINS match (LPG: natural gas of the same subsector; food & '
            'forestry: construction; else manufacturing).', 'Egypt 2022: NOx +11%, PM2.5 +5%, combustion CH4 +20%.'),
    'L60': ('VAT payment = (supply cost + taxes) x VAT rate x household share.', 'None for Egypt (VAT 0 on oil).'),
    'L61': ('Grow the EU ETS price with ExistingETSGrowth.', 'None for Egypt.'),
    'L62': ('Take the fuel coverage row, and the single-price flag, for transport diesel, LPG and kerosene.',
            'None for Egypt.'),
    'L63': ('Look the fuel coverage up in the whole ECP block (to row 425).', 'None for Egypt.'),
    'L64': ('Apply the industry ETS coverage to other oil products outside power.', 'None for Egypt.'),
    'L65': ('Use the ETS coverage of the year for the complementary carbon tax.', 'None for Egypt.'),
    'L66': ('Add the industrial additional efficiency to the fossil rows of other energy use.',
            'None while the input is 0.'),
    'L67': ('Size the investment need on next year\'s demand (row 4027), as its label says, estimated as this year\'s demand x (1 + growth from last year to this year): reading next year\'s demand itself would make the workbook circular through the GDP feedback once a revenue reads fuel use (the methane fee).',
            'Egypt (legacy inputs, v6.2 estimate): capacity 77.9 GW in 2030 and 109.6 GW in 2040 against legacy 75.2 and 107.3 (next year read directly: 77.3, 109.5); the need follows the 2023-2024 demand shock (4.3 GW in 2024, 0 in 2025).'),
    'L68': ('Apply multiplier(t - s) to the impulse of year s (lag 0 in the impulse year), as the multiplier notes '
            'define the lags.', 'The GDP effect of every impulse comes one year early.'),
    'L69': ('Match the first cohort\'s excise use on its own row (L14372, baseline L8056), not L$8113.',
            'The first year\'s revenue has no contractionary effect (Egypt about 3e-5 of GDP).'),
    'L70': ('Use the gas industry excise rate (row 2581) and gas industry use in row 7747.',
            'Gas industry excise revenue is wrong wherever coal and gas excises differ (none for Egypt).'),
    'L71': ('Multiply by _conv_ktoe_to_gj in rows 7791, 7805, 7859.', 'Biomass taxes, subsidies and VAT are 0.'),
    'L72': ('Read column R (the year) in rows 7657 and 7742.', 'Revenue of the year uses next year\'s rate.'),
    'L73': ('Divide by the industry gas total (6428) in row 7677; use power x kerosene coverage (R2265 x R2270) in row '
            '7704.', 'Coverage shares of gas industry and kerosene power are wrong (info rows).'),
    'L75': ('Index the excise report by the matched row instead of 759; take electricity from rev.new in the revenue '
            'by fuel report.', 'The excise report is all zeros; revenue by fuel mixes totals.'),
    'L76': ('Point CIT to the labour-tax or an own table (or the income group), WAGE to its own table, MATCH the country '
            'exactly (0), default unknown text to the income group.', 'Estimated multipliers: CIT 0, WAGE = GNFS, a '
            'missing country takes its neighbour\'s.'),
    'L77': ('Point rows 16383-16390 to the average-price rows of each fuel; test the baseline gas total in E16302; '
            'relabel "baseline = 100".', 'The reported price indices are of the wrong fuels.'),
    'L78': ('Hold the target auctioned share after the target year whatever the continuation (or offer a defined '
            'alternative).', 'An auctioned share drops to 0 (all free) after the target year.'),
    'L79': ('Price and charge the ETS by subsector coverage, not MAX over the sector.', 'Uncovered industry and '
            'transport subsectors pay the permit price; revenue on the whole sector\'s CO2.'),
    'L80': ('Leave the carbon-tax trajectory unscaled when the ETS applies (drop E2191 from row 2251).',
            'The carbon tax outside the ETS is cut by the volatility ratio.'),
    'L81': ('Use the factor of the same column in the fixed-subsidy rows (Q2214 for Q).',
            'A consumer subsidy phase-out starts and ends a year late.'),
    'L82': ('Point row 2547 to row 826 (gas producer subsidy).', 'Residential gas takes the oil producer subsidy.'),
    'L83': ('Project as base value x the factor of the year (J x O2213).', 'Electricity producer subsidies fall too '
            'fast (compounding) and a year late.'),
    'L84': ('Phase the electricity consumer subsidy with the consumer factor (row 2214); one option text.',
            'An electricity subsidy reform follows the price-control timing.'),
    'L85': ('Add the industry part: -(MIN(0, res) + MIN(0, ind)).', 'Reported electricity consumer subsidies wrong.'),
    'L86': ('Give the electricity producer subsidy a manual-input row.', 'Manual values ignored.'),
    'L87': ('Set the regulation share (C2371) to the scenario\'s adjustment of MTInputs rows 247-250 (F86:F89) and '
            'use row 251 for feebates.', 'Regulation scenarios have no effect at all.'),
    'L88': ('Add the regulation shadow price to the power shadow price (rows 3398 ff.).', 'Economy-wide regulations '
            'skip power.'),
    'L89': ('Read the shadow price of the row\'s own sector for coal.', 'Coal in road and services takes the '
            'residential shadow price (minor).'),
    'L90': ('Drop $C5593* in row 5593 (biomass gain = -sum of the equivalents).',
            'Biomass gain 5 times too small when leakage is on.'),
    'L91': ("Compute the leakage price change from the residential after-tax price (the row's own new policy).",
            'An exempt LPG still leaks to biomass.'),
    'L92': ('I1784 = IF(LEFT(H1784,3)="Yes",1,0); start rows 5568-5570 from L(total) x K1795.',
            'ExemptMostCook has no effect on fuel use or revenue.'),
    'L93': ('Use the sector rule IF(D2369=1,IF(OR(C2173=4,C2173=9),"Yes","No"),...) in rows 2259-2268.',
            'None (dead branch).'),
    'L94': ('One rule: MAX(MIN((t+1-YearPha)/ExemptPhaseoutPeriod,1),0) x ExemptPhaseout.',
            'Biomass, renewables and jet fuel phase in differently from the other fuels.'),
    'L98': ('Use =AND(Dashboard!$K$44,P53) in P54:X54.',
            'Industry feebate coverage follows the ETS switch on the Dashboard.'),
    'L99': ('Read Dashboard R30 in S11 and U11.',
            'Machinery and other manufacturing join the ETS with buildings, not industry.'),
    'L100': ('Extend both names to row 146.',
            'Manual electricity prices ignored.'),
    'L101': ('Read N279:N286 in F51:F58.',
            'Manual services income elasticities equal the industry ones.'),
    'L102': ('Type the inputs and read them directly.',
            'Manual non-energy elasticities ignored.'),
    'L103': ("Mitigation row 17668 = 'Manual inputs'!J237 (NSCC) / J240 (GSCC).",
            'Manual SCC entered on Manual inputs is ignored.'),
    'L104': ('Delete the name or point it at the methane fee input.',
            'None (unused name).'),
    'L105': ('Transpose H46:K46 and H47:K47.',
            'Industry feebate rates set on the Dashboard have no effect.'),
    'L106': ('Use rows 297 and 298 respectively.',
            'None (memo only).'),
    'L107': ('Add an MTInputs row (and Dashboard cell) for the start year of the additional RE subsidy and point E2736 at it.',
            'The two policies cannot be timed apart.'),
    'L108': ('Rows 7883-7887 = the subsidy by type (rows 3148-3152) x generation.',
            'Wrong total revenue whenever a renewable subsidy is set.'),
    'L109': ('Add the Low and Vhigh series to the Power tab, or map the options to the old series.',
            'Low and Vhigh options give errors.'),
    'L110': ('Use the carbon cost before VAT in the rebate, or count the VAT on the policy term in the VAT revenue.',
            'Revenue split inconsistent (total unchanged).'),
    'L111': ('Compute row 3660 from the excise in the price.',
            'Excise revenue overstated when AdditionalExcise is on.'),
    'L112': ('In rows 8693-8704 refer to the policy block ($D$8685, L$8691) instead of $D$2369 and L$2375.',
            'Regulations have no effect in the policy run even after the L87 fix.'),
    'L113': ('Test LEFT(switch,3)="Yes" in G261, row 3150 and F201, so Yes and Yes* both count as Yes.',
            'Choosing the default option ("Yes*") of PowerRebates, RenewableSubsidyHydro or AdditionalExcise switches the feature off.'),
    'L114': ('Deflate the nominal inputs (rows 2734-2735) by the CPI index before they enter row 2743, or relabel MTInputs 352-353 as real.',
            'Renewable subsidies too large in real terms in later years (nominal value read as real).'),
    'L115': ('Point row 2555 (and policy 8871) at the residential gas ETS row 1715.',
            'Residential gas price carries the LPG permit price wherever an existing ETS covers either fuel.'),
    'L116': ('Point H53 and H54 at rows 169 and 170.',
            'None today (equal values); wrong step-change elasticity for services gasoline and diesel when regional values differ.'),
    'L117': ('Read D$1220:D$1418 in D44, as E44:O44.',
            'None today (lag 0 is 0); the lag-0 transfers multiplier would come from the wrong country.'),
    'L119': ('Drop the adjustment, or apply it once and to all types (compare in the target year).', 'BAU targets before 2030 scaled twice; Fixed and Historical never adjusted.'),
    'L120': ('Use target / start-year emissions in rows 18482-18483, as 18484.', 'Conditional NDC line plotted as the inverse ratio.'),
    'L121': ('Return F18437 - F18440 x adj (the level), as the Fixed block.', 'None today (branch never runs); a cut would be read as a level.'),
    'L122': ('Add I18450 (LULUCF) instead of J18450 (non-CO2).', 'Intensity targets incl. LULUCF count non-CO2 twice and miss LULUCF.'),
    'L123': ('None: not reproduced in the .xlsb (G470 already reads the reference year).', 'None.'),
    'L124': ('Read N$826 (gas) in row 2547, as the other gas blocks (same cells as the L82 plan).', 'A gas producer subsidy misses residential gas, which takes the oil value instead.'),
    'L125': ('Multiply by liters per barrel in row 2685.', 'The oil producer subsidy is about 159 times too small for other oil products.'),
    'L126': ('Average the fuel prices over t-4 .. t (rows 3155-3163): L3155 =IF(...,L3072,AVERAGE($L3072:L3072)) for L:O, P3155 =IF(...,P3072,AVERAGE(L3072:P3072)) for P:AE.', 'Power costs read the next two years\' prices: a circular reference as soon as a price depends on quantities.'),
    'L127': ('Keep the levelised variable cost (rows 3439-3447) on input-driven costs only; if an ETS price becomes endogenous, levelise the announced price path instead of the solved one.', 'Latent: investment would read future quantities through the cost path.'),
    'L128': ('K6238 =K8024 and K6243 =K8029, filled K:AD; policy rows 12554, 12559 the same (+6,316).', 'Each year reports the next year\'s net revenue (USD and % of GDP).'),
    'L129': ('In rows 2785-2788, 2947-2951 and 7883-7886 drop the + L2743 term (L2745 already includes it); policy rows the same (+6,316).', 'With a baseline renewable subsidy (MTInputs 352) the subsidy cost is counted twice.'),
    'L131': ('Give each row its own code (e.g. gdp.pre.ln, gdp.pre.mn; sub.new.usd only on its own subtotal).', 'Lookups by code (MTOutputs, the data link) return the first row of a reused code.'),
    'L132': ('Write the codes in lower case and with a scenario number: em.pm2.all.<sector>, nox.tot.<n>.', 'Lookups of the protocol codes fail.'),
    'L133': ('Rename the N2O total n2o.tot and the NOx forcing row nox.tot.', 'A reader of the codes takes one gas for the other.'),
    'L134': ('Label the price-increase units USD/bbl (other oil products) and USD/GJ (biomass) in columns E and G of MTInputs rows 182-183.',
             'Labels only: no value changes; a user may type an increase in the wrong unit.'),
    'L130': ('F18456: apply the cut to the reference-year intensity F18453, as F18455 does.', 'Conditional and unconditional intensity targets are not comparable.'),
    'L118': ('Size the logit investment on row 4108 (need after manual investment), not row 4028.',
            'Over-investment whenever a type is set to Manual: logit investment comes on top of the manual capacity path.'),
    'L95': ('Put the efficiency increment on its own labelled row (or read M2198 directly); leave row 3719 to net exports.',
            'None on values (increment 0 by default); a reader of the row label takes the efficiency term for a trade term.'),
    'L96': ("Give the additional-efficiency increments their own labelled rows; label the LPG and kerosene shadow-price rows 'All'; correct the typo.",
            'None on values; formula audits misread the additional-efficiency term as a carbon-price setting.'),
    'L97': ("Delete the memo rows (or move them to a diagnostics area with the year's own growth M2446).",
            'None (dead calculation); would be wrong if anything used it.')}   # v5.1: L95-L97 from the team tracker


def _transport():
    """v3.5: PRIORITY and FIX of the engineer road-model bugs (L25+), from transport_model_ref: the fix text of
    FIXES and the Egypt effect of each fix alone in the engineer baseline, 2035. Medium = changes the Egypt engineer
    run (the legacy Egypt run itself uses the elasticity road model); Low = latent (policy or fuel zero in Egypt)."""
    import transport_model_ref as T
    inp = T.legacy_inputs('base')
    leg = T.summary(T.engine(inp, fix=frozenset()))[2035]
    keys = {lid: k for lid, k in zip([x[0] for x in R.LEGACY if int(x[0][1:]) >= 25],
                                     sorted(T.FIXES, key=lambda k: (int(''.join(c for c in k[1:] if c.isdigit())), k)))}
    pri, fix = {}, {}
    for lid, k in keys.items():
        new = T.summary(T.engine(inp, fix=frozenset([k])))[2035]
        d = {m: (new[m] / leg[m] - 1) * 100 for m in ('gso', 'die', 'ele') if leg[m]}
        dev = (new['ev_pass'] - leg['ev_pass']) * 100
        big = max([abs(v) for v in d.values()] + [abs(dev)]) >= 0.1
        pri[lid] = 'Medium' if big else 'Low'
        eff = ('Egypt engineer baseline 2035: gasoline {gso:+.1f}%, diesel {die:+.1f}%, road electricity {ele:+.1f}%, '
               'passenger EV sales share {ev:+.1f} points.'.format(ev=dev, **d) if big else
               'None in the Egypt engineer run (the policy or fuel is zero there).')
        fx = T.FIXES[k][1].split('; fix')[1].lstrip(': ').split('): ')[-1]
        fix[lid] = (fx[0].upper() + fx[1:] + '.', eff)
    return pri, fix


TR_PRI, TR_FIX = _transport()
PRIORITY.update(TR_PRI)
FIX.update(TR_FIX)


CHECK465 = os.path.join(HERE, '..', 'legacy', 'bugfixes', 'check465', 'legacy465_check.json')   # v8.2: fixes the CPAT team made in 465


def legacy465(lid):
    """v8.2: the bug in legacy 465 (column "In legacy 465"): open, or the check of the CPAT team's fix."""
    chk = json.load(open(CHECK465, encoding='utf-8'))['bugs'] if os.path.exists(CHECK465) else {}
    return {'Confirmed fixed': 'Fixed', 'Fixed with caveats': 'Fixed with caveats',
            'Not fixed': 'Not fixed (marked fixed)'}.get(chk.get(lid, {}).get('status'), 'Open')


def mvp_status(lid):
    """v3.7: what the prototype does about the bug, in a word or two (column "In the prototype")."""
    st = {x[0]: x[4] for x in R.LEGACY}.get(lid, 'Fixed')
    if st.startswith('Kept'):
        return 'Kept as legacy'
    if st.startswith('Copied'):                       # v8.2: L134, labels copied from legacy, queued to fix
        return 'Copied (labels), to fix'
    if st.startswith(('Harmless', 'Not built')):
        return 'Not built'
    if 'engineer road model' in st:
        return 'Fixed (engineer road model)'
    return 'Fixed'


def bugs():
    """(id, title, where, what legacy does, fix, effect) for every legacy bug of the register."""
    out = []
    for i, (_k, title, where, what, fix, effect) in enumerate(R.BUGS, 1):
        out.append((f'L{i}', title, f'Mitigation {where}', what, fix, effect))
    for lid, title, where, what, status in R.LEGACY:
        fix, effect = FIX[lid]
        out.append((lid, title, where, what, fix, f'{effect} prototype: {status}'))
    return out


def main():
    rows = sorted(bugs(), key=lambda b: (ORDER[PRIORITY[b[0]]], int(b[0][1:])))
    missing = [b[0] for b in rows if b[0] not in PRIORITY]
    assert not missing, missing
    n = {p: sum(PRIORITY[b[0]] == p for b in rows) for p in ORDER}
    lines = [f'# Legacy CPAT: bug fixes needed (CPAT-AI-Mitigation-Prototype v{B.VERSION})', '',
             'Rebuilding the legacy CPAT mitigation sheet found these bugs in legacy CPAT itself. The prototype fixes or '
             'documents each of them; **legacy CPAT still needs the fixes** unless column "In legacy 465" says Fixed. '
             'File: `CPAT 1.0pre_465 - No Prop Data.xlsb` (the bugs were found in 456; rows moved to 465), sheet '
             'Mitigation unless stated. Generated from the register (`issues_register.py`) by `make_legacy_fixes.py`; '
             'the full register, with the check of each fix in 465, is `CPAT-AI_BugsAndIssues_latest.docx`.',
             '', f'**{len(rows)} bugs: {n["High"]} high, {n["Medium"]} medium, {n["Low"]} low priority.** High = '
             'changes the results of standard runs (Egypt); medium = changes results in some runs or countries, or a '
             'reported number; low = latent (no effect in the Egypt runs) or reporting only. (L17 turned out to be a bug of '
             'the prototype, not of legacy, and is not listed.)', '',
             '| ID | Priority | In legacy 465 | Bug | Where in legacy | Fix | In the prototype |',
             '|---|---|---|---|---|---|---|']
    for lid, title, where, _what, fix, _eff in rows:
        lines.append(f'| {lid} | {PRIORITY[lid]} | {legacy465(lid)} | {title} | {where} | {fix} | {mvp_status(lid)} |')
    lines += ['', '## Details', '']
    for lid, title, where, what, fix, eff in rows:
        lines += [f'**{lid} ({PRIORITY[lid]}; in legacy 465: {legacy465(lid).lower()}). {title}.** {where}.', '',
                  f'- Legacy: {what}', f'- Fix: {fix}', f'- Effect: {eff}', '']
    with open(DECK, 'w', encoding='utf-8') as f:
        json.dump({'counts': n, 'total': len(rows),
                   'high': [{'id': b[0], 'effect': SHORT[b[0]]} for b in rows if PRIORITY[b[0]] == 'High']}, f, indent=1)
    print(f'wrote {DECK}: {len(rows)} bugs ({n})')
    return rows


if __name__ == '__main__':
    main()
