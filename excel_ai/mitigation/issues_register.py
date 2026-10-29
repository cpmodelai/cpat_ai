"""Register of bugs, known issues and potential upgrades of CPAT-AI-Mitigation-Prototype v0.4.7: the single source for the
Word register (make_bugfix_book.py -> documentation/CPAT-AI_BugsAndIssues_v0.6.4.docx) and the summary in the
Word documentation (make_docs.py). check_full.py tests that the IDs are unique and that every LegacyDiff row of
the types in LD_TYPES is included.

IDs: L = bug in legacy CPAT (fixed in the prototype unless stated), M = bug found and fixed in the prototype itself during
development, I = known issue or limitation of the prototype today, LD = simplification or feature not yet modelled (from the
workbook sheet LegacyDiff, row number), U = potential upgrade (priority High / Medium / Low).
"""
import build as B

REGISTER_VERSION = B.VERSION   # v0.8.4: the register documents carry the workbook version (user 2026-10-28)

BUGS = [  # key, title, legacy rows, what legacy does, what it should do, why it matters
    ('services', 'Services electricity demand grows with the industrial multiple after 2023', 'H3, row 3731',
     'The 2023 formula multiplies services demand by the services multiple (row 3713); from 2024 the copied formula '
     'points six rows up, to the industrial multiple (row 3707). Services have a higher GDP elasticity (1.1 against '
     '0.8) and a different price elasticity.',
     'Use the services multiple in every year, as in 2023 and as the label of row 3713 says.',
     'Services are about a quarter of Egypt\'s electricity demand, so this is the largest single effect.'),
    ('aee', 'Autonomous efficiency gains use the efficiency elasticity instead of the usage elasticity',
     'H1, rows 3691, 3697, 3703, 3709',
     'Efficiency multiple = 1 / (1 + alpha)^(1 + eps_F), with eps_F the "Price Elasticity" row 3677.',
     'Documentation equation (3.4.2.3) and the fuel equation use (1 + eps_U): 1 / (1 + alpha)^(1 + eps_U), with eps_U '
     'the usage ("Demand Elasticity") row 3676.',
     'Efficiency gains reduce demand slightly too much every year.'),
    ('income', 'Income factor on the GDP elasticity applied twice and anchored to 2023', 'H1, rows 3692-3710',
     'GDP term = (1 + g)^((eps_Y / $M3686) x M3686 x M2433). Row 3686 already holds the average elasticity x the '
     'income factor (row 2433), and $M fixes the denominator to 2023, so the effective elasticity is '
     'eps_Y x inc(t)^2 / inc(2023).',
     'eps_Y x inc(t): the income factor once, in the year of the calculation.',
     'The income factor falls from 1.03 to 0.95 by 2040, so the error grows over time.'),
    ('lt_alloc', 'Long-term storage cost allocation (33%) applied twice', 'J1, rows 3911 and 3912',
     'Row 3911 multiplies the long-term storage cost by the allocation share; row 3912 multiplies it again.',
     'Apply the 33% allocation once.',
     'No effect for Egypt (variable renewables stay below the 75% threshold); it matters for high-renewable '
     'scenarios.'),
    ('invcost', 'Investment spending uses the capital cost at time factor 1', 'L20, rows 4276-4284',
     'New investment (USD m) = nameplate MW x the capital cost column O of table A2, which is the cost before the '
     'capital-cost time factor.',
     'Use the capital cost of the year (table A13), as the levelised and amortised costs do.',
     'Investment spending on solar is overstated by up to 80% (2040, time factor 0.55), wind by up to 9%; it '
     'is reporting only (the investment decision uses the right cost).'),
    ('cmin', 'Investment logit normalised by the cheapest type, including types that may not be built',
     'L1/L4, rows 4046, 4073-4081',
     'The logit weight is EXP(-K x cost / cheapest cost), and the cheapest cost is taken over all nine types, '
     'including types whose new investment is not permitted (coal, nuclear, other renewables, biomass for Egypt).',
     'Normalise by the cheapest permitted type, so that a type that cannot be built does not change the shares of '
     'those that can.',
     'No effect in the Egypt baseline; in the carbon-tax run nuclear (not permitted) is the cheapest type from '
     '2024, which makes the investment logit steeper.'),
    ('retlag', 'Early coal retirement mixes nameplate and effective capacity', 'K4, row 3973',
     'The room for early coal retirement subtracts last year\'s non-coal retirements in nameplate MW from additions '
     'and demand growth in effective MW.',
     'Subtract effective retirements.',
     'Latent for Egypt (no coal). Too little early coal retirement where solar (low capacity factor) retires.'),
    ('coalret', 'Effective coal retirement is not capped like the nameplate retirement', 'K5/K6, rows 3994, 4009-4011',
     'Nameplate coal retirement is MIN(planned + early, capacity); the effective retirement uses planned + early '
     'without the cap.',
     'Effective retirement = nameplate retirement x capacity factor.',
     'Latent for Egypt. Where early retirement is large, capacity needed is overstated.'),
    ('rebate', 'Feebate rebate per kWh consumed is added to the cost per kWh generated', 'D6, rows 3407-3409',
     'The rebate is the average feebate per kWh generated divided by consumption/generation (x 1.22), and is then '
     'added to the cost per kWh generated of every type.',
     'Rebate per kWh generated, so the feebate is revenue-neutral at base-year shares.',
     'Latent for Egypt (no power feebate in the runs). Over-rebates by 22% when a power feebate is set.'),
    ('kcheck', 'Capacity needed is computed from last year\'s plan, not from actual capacity', 'K7, row 4024',
     'Effective capacity before retirements = last year\'s planned capacity (capacity after retirements + investment '
     'needed), whether or not the investment could be placed.',
     'Use the actual effective capacity of the year (capacity x capacity factor).',
     'Latent: it only matters when scale-up limits leave a deficit; then the model under-invests next year too.'),
]
SHORT = {'services': 'Services demand', 'aee': 'Efficiency exponent', 'income': 'Income factor',
         'lt_alloc': 'LT storage allocation', 'invcost': 'Investment spending', 'cmin': 'Investment logit',
         'retlag': 'Early-retirement units', 'coalret': 'Coal effective retirement', 'rebate': 'Feebate rebate',
         'kcheck': 'Capacity check'}
POWER_EXTRA = {'nextyear': 'L67 Capacity for next year\'s demand'}   # v0.4.14: power fixes registered in LEGACY
MINOR = [  # L11, L12 (kept for the effect report)
    ('Stray reference in dispatch', 'I1, rows 3773 and 3779',
     'Required generation from coal and gas is MAX(required - other generation, $G4291 x total), and G4291 is an '
     'unrelated, empty cell of table L21. Harmless while the cell is empty; not built in the prototype.'),
    ('Total nameplate investment row is zero', 'L19, row 4273',
     'The total multiplies by $X3008, an empty cell, instead of summing the types. Reporting only; the prototype sums.'),
]

LEGACY = [  # L11 onwards: id, title, where, what, status
    ('L11', 'Stray reference in dispatch', 'Mitigation rows 3773, 3779 (I1)',
     'Required generation from coal and gas is MAX(required - other generation, $G4291 x total); G4291 is an '
     'unrelated, empty cell of table L21.', 'Harmless while the cell is empty; not built in the prototype.'),
    ('L12', 'Total nameplate investment row is zero', 'Mitigation row 4273 (L19)',
     'The total multiplies by $X3008, an empty cell, instead of summing the types.', 'Reporting only; the prototype sums.'),
    ('L13', 'Other oil products: hardcoded pass-through 1 and margin 0', 'Mitigation price block (other oil products)',
     'With the hardcodes the retail price of other oil products falls with the oil price to the 0.01 floor and their '
     'fuel use rises tenfold by 2030 (Egypt).', 'Changed in the prototype (v0.0.10, user decision): pass-through and margin '
     'from the IMF dataset like the other oil products (LegacyDiff).'),
    ('L14', 'Pass-through applied twice in the first projected year', 'Mitigation txo rows (cs)',
     'With pass-through 0.5 or 0.8 the floating tax multiplies its last value by (1 - pass-through) a second time, so '
     'taxes jump in the first projected year.', 'Fixed in v0.4.10 (user rule: bugs are never replicated): the floating '
     'part is (1 - pass-through) x (last tax + fall in supply cost), applied once (txf; Methods, chapter Prices '
     'A10); no effect for Egypt (pass-through 0 or 1).'),
    ('L15', 'ETS: hardcoded relative price 1.1', 'Mitigation row 1843',
     'The ETS price effectiveness uses a fixed 1.1 instead of the volatility inputs of the ETS+LTS table.',
     'Replaced in the prototype by the volatility adjustment (v0.1.02); suggested to the legacy team (TODO).'),
    ('L16', 'ETS quick estimate linear in the semi-elasticity', 'Mitigation row 1868',
     'The fast estimate divides the reduction by the semi-elasticity (linear); the legacy note says "arguably exp/ln".',
     'prototype uses the log form LN(cap / baseline) / (semi-elasticity x effectiveness x volatility adjustment) (v0.1.02).'),
    ('L17', 'Version-log rows rewritten with the current version', 'prototype builders v0.0.3-v0.0.4 (not legacy)',
     'Earlier version-log rows showed the current version number.', 'Fixed in v0.0.5: each row has its own version.'),
    ('L18', 'Non-energy methane never changes', 'Mitigation rows 6158-6213 (livestock, rice, waste)',
     'Livestock, rice and waste CH4 are the inventory values divided by the GWP, constant over time; the abatement '
     'shares of the methane fee are computed (rows 6168, 6180, 6192) but not applied, so a methane fee on '
     'agriculture and waste has no effect.', 'Fixed in v0.2.8: the sources grow with income and population and the '
     'fee abates them along their curves (Methods, chapter Emissions).'),
    ('L19', 'Flaring CO2 counted as methane', 'Mitigation rows 6141-6142',
     'The CO2 from flaring the abated oil and gas methane is divided by the CH4 GWP and added to the CH4 row.',
     'Fixed in v0.2.8: reported as CO2 in energy (row ghg.flr).'),
    ('L20', 'Population growth path', 'Mitigation rows 481, 2428 (macro drivers)',
     'Population growth is 2% a year from 2027 and 3-4% from 2031, so Egypt reaches 185 million in 2041 against 147 '
     'million in the legacy sheet UNPop; it drives the agriculture, waste and other GHGs.',
     'Fixed in v0.2.8: population from UNPop (UN WPP).'),
    ('L21', 'Waste abated with the livestock curve', 'Mitigation row 6192',
     'The abatement share of waste equals that of livestock (=M6168) instead of the waste curve of CH4Inputs.',
     'Fixed in v0.2.8: every source uses its own curve.'),
    ('L22', 'Navigation missing from the local pollutant totals', 'Mitigation local pollutant totals (sections 13-14)',
     'The transport and total pollutant rows sum road, rail and aviation but leave out domestic navigation.',
     'Fixed in v0.2.9: navigation included (section 15).'),
    ('L23', 'Services and food & forestry missing from the pollutant totals', 'Mitigation rows 6690, 6792, ... '
     '(total emissions of each pollutant)', 'The total of each pollutant sums power, transport, residential, industry '
     'and other energy use but leaves out services and food & forestry, which the air-pollution sectors (ground '
     'level other, food & forestry) include. No effect on the legacy Egypt values (services and food & forestry '
     'emit zero there: legacy total = sum of its sectors), but it matters wherever they emit.',
     'Fixed in v0.3.0: totals = all subsectors + power.'),
    ('L24', 'GDP effect added to GDP growth every year', 'Mitigation rows 2443-2446, 8274',
     'The fiscal multipliers give the change of the GDP level; legacy adds that change to the growth rate every '
     'year, so a steady effect of 0.5% raises growth by 0.5 points a year and compounds (about +10% of GDP after 20 '
     'years instead of +0.5%). No effect on the NoPropData values (the GDP effect rows are stripped to 0).',
     'Fixed in v0.3.1: the GDP level is raised by the effect (growth from the ratio of level factors).'),
]
LEGACY = [x for x in LEGACY if x[0] != 'L17']           # L17 is an prototype bug: listed in MVP_BUGS

# v0.3.5: legacy bugs of the engineer road model (legacy survey ids B1-B23; switches of transport_model_ref.FIXES).
# The legacy Egypt run uses the elasticity road model, so these bugs change the engineer run only.
TR_TITLES = {
    'B1': 'Road: distance tax and 2-3 wheeler EV subsidy apply in the baseline', 'B2': 'Road: freight and 2-3 wheeler '
    'income growth read coal subsidies from 2038', 'B3': 'Road: vehicle ownership calibration only scales up (and '
    'uses 2024)', 'B3b': 'Road: freight-share cap and 2-3 wheeler peak use 2024', 'B4': 'Road: ownership of cars and '
    'trucks cannot fall', 'B6': 'Road: bus fuel scaled by the wrong rows', 'B6b': 'Road: bus share grossed up as '
    'x(1+share)', 'B7': 'Road: industry emission factors for road diesel and LPG', 'B8': 'Road: wrong elasticities and '
    'rows in freight and 2-3 wheeler distance', 'B8w': 'Road: freight discounted at the power-sector WACC',
    'B9': 'Road: negative PHEV sales share', 'B10': 'Road: charging-station subsidy ramp', 'B19': 'Road: new BEV '
    'maintenance at the ICEV rate', 'B20': 'Road: used ICEV and BEV depreciation over different periods',
    'B21': 'Road: freight distance output omits LPG and LNG trucks', 'B22': 'Road: wrong rows in average gas and EV '
    'fuel economy', 'B23': 'Road: PHEVs carry the full BEV range anxiety'}


def _tr_legacy():
    import transport_model_ref as T
    order = sorted(T.FIXES, key=lambda k: (int(''.join(c for c in k[1:] if c.isdigit())), k))
    out = []
    for i, k in enumerate(order):
        rows, desc = T.FIXES[k]
        what = desc.split('; fix')[0]
        out.append((f'L{25 + i}', TR_TITLES[k], f'Mitigation rows {rows} (engineer road model, survey {k})',
                    what[0].upper() + what[1:] + '.', 'Fixed in the prototype engineer road model (v0.3.5; '
                    'Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).'))
    return out


LEGACY = LEGACY + _tr_legacy()

# v0.3.7: legacy bugs of the fuel-use equations (Reviews_and_Surveys.md (section Sector_Equations_Survey), proposed ids L42-L48)
LEGACY += [
    ('L42', 'Domestic aviation: GDP growth and shock swapped', 'Mitigation rows 5483-5492',
     'GDP growth enters with elasticity 1 while the shock carries eps_Y x income factor; coal and gas get the shock '
     'twice; jet fuel takes the diesel income elasticity.', 'Fixed in v0.3.11: jet fuel in the prototype with the standard form '
     '(shock once) and the transport oil income elasticity.'),
    ('L43', 'Other energy use: no GDP growth', 'Mitigation rows 6063-6071',
     'The income factor points to the blank row 2440, so other energy use never grows with GDP; rows 6063-6070 have no '
     'additional-efficiency term.', 'Fixed in the prototype: other energy use grows with GDP (oil, industry elasticities).'),
    ('L44', 'Residential other oil products priced at the biomass price', 'Mitigation row 5559',
     'The price term reads row 5549 (biomass) instead of 5548.', 'Fixed in the prototype: own price.'),
    ('L45', 'Residential leakage to biomass inconsistent', 'Mitigation rows 5574-5593',
     'Sign and cumulation differ between rows 5564 and 5554; kerosene uses the LPG price and share rows (5587, 5588); '
     'duplicate kerosene change rows.', 'Fixed in v0.5.1 (feature built, section 6b): one row set per fuel with its own '
     'price and share; fuel use = elasticity model + cumulative change computed on last year\'s actual use; one '
     'switch (BiomassLeakage, Settings C59).'),
    ('L46', 'Road other biofuels: wrong price and terms', 'Mitigation row 5406',
     'Uses the bioethanol price, applies the shadow price through eps_U, has an efficiency term equal to 1 and uses '
     'M2259 (coal exemption phase-out) as additional efficiency.', 'Fixed (v0.9.0, R10.3): other road biofuels of the '
     'elasticity road model built as legacy 465 (the road biomass price, the shadow price in the efficiency term, oil '
     'elasticities and AEEI; issue I143); not reproduced in legacy 465. None in Egypt.'),
    ('L47', 'Self-generated renewables in aviation and navigation take the shock from wrong rows',
     'Mitigation rows 5491, 5516', 'The "shock" is row 2512 (coal industry new excise) or row 2473 (blank).',
     'Fixed (v0.9.0, R10.6): self-generated renewables of aviation and navigation built with the shock row like every '
     'fuel row (issue I144); not reproduced in legacy 465. None in Egypt.'),
    ('L48', 'Residential initially-exempt rows: no income factor; starred "Yes*" exemption test', 'Mitigation rows 5546-5547, 5568-5570',
     'The initially-exempt rows M5568:M5570 grow without the income factor M2433; the AlwaysExemptResLPGKer test misses the starred defaults. '
     'The split itself works in the .xlsb (L5564:L5570 = IFNA(IF($L$1784=B, ... $K$1795 ...))); it is 0 in Egypt because ExemptMostCook is off (v0.5.5 check from the .xlsb; the LibreOffice conversion had shown IFNA(0)).',
     'Fixed: the initially-exempt split is built with the income factor (v0.5.6, section 6b lkx; v0.9.0 R6 as legacy 465, '
     'LegacyDiff 67; legacy 465 M5568 has the income factor); the starred AlwaysExemptResLPGKer test is fixed in v0.5.1 '
     '(LEFT(x,3)="Yes", rows exf).'),
    ('L49', 'Balance of payments: oil without the share traded', 'Mitigation rows 18162-18166, 742',
     'The value of the change in net imports of oil is the change in use x the price, while gas (and coal) apply the '
     'share traded of rows 741-743 (oil products 0.47), so the oil effect is about twice too large (Egypt 2030: '
     '3.2 bn USD).', 'Fixed in v0.3.16: every fuel group applies its share (section 16b).'),
    ('L50', 'Balance of payments: current account #NAME?, column lag, sign', 'Mitigation rows 18180-18198',
     'The pre-policy current account (WEO BCA) is #NAME?, so the whole % of GDP panel errors (v0.5.5: the rows do look '
     'up INDEX(WEO,...); the cell plan L50 was built from texts the LibreOffice conversion truncated and is to be '
     'redone); the policy rows lag one '
     'column; the sign of policy net imports looks reversed.', 'Fixed (v0.9.0, R11): current account in section 16b from '
     'the corrected WEO values typed for Egypt (EGY.BCA.A, EGY.BCA_NGDPD.A; held at 2031 by legacy\'s own rule; other '
     'countries 0, issue I148); the column lag not replicated (16b xtb, since v0.3.16).'),
    ('L51', 'Energy trade balance of coal valued at the oil price', 'Mitigation row 743',
     'The coal trade balance multiplies coal net imports by the crude oil price per GJ (row 731) instead of the coal '
     'price (row 732); Egypt 2022: -1.4 bn USD instead of about -0.5.',
     'Fixed in v0.4.6: coal at the coal price (data step Inputs_macro, from Balances and the international prices).'),
    ('L52', 'Renewables take the world power parameters, never the country ones', 'Mitigation rows 2981-2985 P:T',
     'The fallback IF(ISERROR(country), country, IF(ISERROR(world), ...)) is inverted, so wind, solar, hydro, other '
     'renewables and biomass always take the world efficiency, fixed and variable O&M, WACC and lifetime (Egypt: solar '
     'fixed O&M 15 instead of the country 11.831 $/kW/y).',
     'Fixed in v0.4.10: every type takes the country value where it exists, else the world value (Egypt: solar fixed O&M '
     '11.831 $/kW/y).'),
    ('L53', 'Actual capacity factors are never used', 'Mitigation rows 2999-3007 N, Q, W',
     'The installed-capacity lookup searches the years 2000-2019 (Power F:Y) for 2022 (column AB), so it is #N/A, the '
     'actual capacity factor is 0 and the studies value is always used; the CFOverride bounds never act.',
     'Fixed in v0.4.10: installed capacity of the base year from Power rows 358-1635 (all year columns); the actual '
     'capacity factor (output / capacity) is used inside the CFOverride bounds, else the studies value (Egypt: gas 0.385, '
     'wind 0.436, solar 0.347, hydro 0.592; base-year gas capacity 52 GW instead of 35).'),
    ('L54', 'Hydro investment always starts in the first year', 'Mitigation row 4067 H',
     'IF($L$3827>50%, FirstYearCalculations, NewInvHydYear) tests a year header (2022 > 0.5) instead of a share, so hydro '
     'can invest from 2022 instead of 2030.', 'Fixed in v0.4.10: the base year only when the hydro generation share is '
     'above HydInvShare (50%), else NewInvHydYear (Egypt: 2030).'),
    ('L55', 'China, Japan and Korea take regional power data', 'Mitigation rows 2977-2985 K (Power A25:A356)',
     'The country lookup searches the regional block (rows 42-109) first, whose codes chn.mpp.*, jpn.mpp.*, kor.mpp.* '
     'equal the country codes, so the regional rows replace the country rows.', 'Fixed in v0.4.10: the country rows are '
     'looked up in the country block (Power rows 112-294) first; no effect for Egypt.'),
    ('L56', 'Countries without CoC risk data get Sri Lanka\'s WACC parameters', 'CoC rows 202-390 D:V',
     'The WACC calculator falls back to row 172 (Sri Lanka) for countries without fixed data, silently.',
     'Fixed in v0.4.10: such countries take the default WACC (as countries missing from CoC), flagged on Inputs '
     '(PsCoCData); no effect for Egypt.'),
    ('L57', 'New ETS: the quick price estimate is linear in the semi-elasticity', 'Mitigation ETS block (quick '
     'estimate, override row)', 'The cap is a relative change of covered emissions, which respond log-linearly to the '
     'price; the linear quick estimate misses the cap (legacy note: "arguably exp/ln") and leaves it to the VBA goal '
     'seek.', 'Fixed (v0.1.02; bug by user decision 2026-10-18, was LegacyDiff row 6): the fast estimate in log form, '
     'LN(cap / baseline) / (semi-elasticity x effectiveness x volatility adjustment); the build stores it (no goal '
     'seek).'),
    ('L58', 'Local pollutants: subsectors without a GAINS match get zero factors', 'Mitigation rows 15885-16685 '
     '(GAINS factor lookups)', 'The GAINS factors are looked up by subsector; services, rail, industry and other energy '
     'use have no GAINS match and silently get 0, although they burn fuel.', 'Fixed (v0.2.9; bug by user decision '
     '2026-10-18, was issue I27 and LegacyDiff row 49): each subsector takes the GAINS subsector of its CH4 factor '
     '(services as residential, rail as road, industry as manufacturing).'),
    ('L59', 'Local pollutants and combustion CH4: fuels without a GAINS factor emit nothing', 'Mitigation rows '
     '15885-16685 (GAINS factor lookups; sheet EF_PM)', 'A fuel that its GAINS subsector has no factor for gets 0, '
     'although it burns: Egypt 2022 residential LPG (3,182 ktoe), other mining diesel (3,819), food & forestry diesel '
     '(927), fuel transformation LPG (2,466); food & forestry shows about 1 t of NOx (legacy row 15924).', 'Fixed '
     '(v0.4.12; bug by user decision 2026-10-18, was issue I35): the nearest GAINS match (LPG: natural gas of the same '
     'GAINS subsector; food & forestry: construction, off-road machinery; biomass: residential; else manufacturing). '
     'A fuel the subsector has factors for keeps a missing pollutant at 0 (GAINS omits zero factors).'),
    ('L60', 'VAT payment on oil products divided by the full VAT rate', 'Mitigation rows 2595, 2618, 2641, 2664 (VAT '
     'payment)', 'The retail price of gasoline, diesel, LPG and kerosene carries VAT x household share (rows 797-816), '
     'but the VAT payment is retail price / (1 + VAT rate) x VAT rate x share, so VAT is understated where the share '
     'is below 1 and the excise residual absorbs the gap.', 'Fixed (v0.4.12): VAT = (supply cost + taxes) x rate x '
     'share, consistent with the retail price.'),
    ('L61', 'EU ETS price grows with the carbon-tax growth', 'Mitigation row 1695 (from the column after the last data '
     'year)', 'After the last data year the EU ETS price grows with ExistingCTGrowth (MTInputs 214) instead of '
     'ExistingETSGrowth (209).', 'Fixed (v0.4.12): ETS prices grow with ExistingETSGrowth, carbon tax rates with '
     'ExistingCTGrowth.'),
    ('L62', 'Existing carbon tax on transport diesel, LPG and kerosene uses the rate row as coverage', 'Mitigation '
     'rows 1760-1762', 'The fuel coverage is looked up with INDEX over rows 1732-1749 by fuel code, which finds the fuel '
     'rate row (1732-1734) before the coverage row (1745-1747): the tax becomes rate x rate x sector coverage; the '
     'single-price flag is ignored.', 'Fixed (v0.4.12): every fuel takes rate x sector coverage x fuel coverage, the '
     'fuel rate only where the country has one and no single price.'),
    ('L63', 'Existing carbon tax fuel coverage: lookup range cut short', 'Mitigation J1741-J1749 (ECP!E133:E403)',
     'The fuel coverage block of sheet ECP runs to row 425, the lookup stops at 403: part of Ukraine, Uruguay and the '
     'United Kingdom get no fuel coverage, so no existing carbon tax.', 'Fixed (v0.4.12): each scheme is looked up in '
     'its whole block (Inputs_ecp columns K:L).'),
    ('L64', 'No existing ETS on other oil products outside power', 'Mitigation rows 1711-1723', 'The ETS block has '
     'other oil products for power only (row 1717); the all-sector price of other oil products gets no existing ETS, '
     'while the carbon tax block applies industry coverage to it (row 1758).', 'Fixed (v0.4.12): other oil products '
     'take the industry coverage of both schemes.'),
    ('L65', 'Carbon tax complementary to an existing ETS: last year\'s ETS coverage', 'Mitigation rows 2270-2288',
     'With CTaxComplimentaryToETS = Yes the new tax covers 1 - the national ETS sector coverage of the previous year '
     '(column one to the left).', 'Fixed (v0.4.12): the coverage of the year (the same from 2026, coverage being held '
     'after the last data year).'),
    ('L66', 'Other energy use: no additional policy efficiency gains on fossil fuels', 'Mitigation rows of other energy '
     'use (fossil fuels; renewables use $M2201)', 'The additional policy-induced efficiency gain of industry (MTInputs '
     '245, row 2201) enters every industrial subsector and the renewables row of other energy use, but not its fossil '
     'rows.', 'Fixed (v0.4.13): other energy use takes the industrial gain on every fuel.'),
    ('L67', 'Power: capacity bought for this year\'s demand, although it comes online next year', 'Mitigation rows '
     '4022-4031 (K7)', 'New capacity bought in a year produces from the next year, but the investment need is sized '
     'on this year\'s demand: row 4027 is labelled "Next Year Demand" and row 4031 "Actual effective generation in '
     'next year (should be the same)", yet row 4027 reads this year\'s demand. The system enters every year one year '
     'of demand growth short (Egypt about 4% a year), and existing plants, mostly gas, run harder to cover it.',
     'Fixed (v0.4.14; bug by user decision 2026-10-18, was issue I8). v0.6.2 (user 2026-10-20): next year\'s required '
     'generation is estimated as this year\'s x (1 + growth from last year to this year), so neither legacy nor the '
     'prototype reads a later year and the GDP feedback (last year\'s effect) cannot loop; legacy kept as a switch in '
     'power_model_ref only.'),
    # v0.4.15 (survey of the revenue, GDP, multiplier, average price and ETS blocks; row numbers baseline, policy +6317)
    ('L68', 'GDP effects: the multiplier of lag 1 acts in the impulse year', 'Mitigation rows 8253-8274 (policy '
     '14569-14590)', 'The effect in year t sums impulse(s) x multiplier(t - s + 1): an impulse already gets the lag-1 '
     'multiplier in its own year, although the multiplier notes (Manual inputs D269, Multipliers) define lag 1 as one '
     'year after implementation. The GDP effect runs one year early.', 'Fixed (v0.4.15): lag 0 in the impulse year '
     '(multiplier 0), lag 1 the year after.'),
    ('L69', 'GDP effects: the first cohort\'s excise drag is lost', 'Mitigation row 8057 (policy 14373)', 'The '
     'excise (revenue) use of the first cohort looks up L$8113, a baseline-block cell (0), instead of the cohort\'s '
     'own row (L14372); the contractionary effect of the first year\'s revenue is dropped (Egypt about 3e-5 of GDP).',
     'Fixed: every cohort counts its revenue use (share -1).'),
    ('L70', 'Revenue: industry gas excise uses the coal rate and coal use', 'Mitigation row 7747 (policy 14063)',
     'The additional excise of gas in industry is the coal industry tax (R2512) x coal industry use (R6422).',
     'Fixed: each subsector and fuel takes its own excise and use (rex, v0.4.15).'),
    ('L71', 'Revenue: biomass taxes, subsidies and VAT divided by the unit conversion', 'Mitigation rows 7791, 7805, '
     '7859', 'Biomass existing taxes, subsidies and VAT divide by _conv_ktoe_to_gj instead of multiplying, so they are '
     'about 0 (2.7e-11).', 'Fixed: fuel use x PJ/ktoe x rate for every fuel.'),
    ('L72', 'Revenue: next-year references', 'Mitigation rows 7657, 7742', 'The LPG price-control row reads S$738 '
     '(next year) and the coal power excise S2466 (next year) instead of column R.', 'Fixed: the year\'s own column.'),
    ('L73', 'Revenue: wrong coverage shares', 'Mitigation rows 7677 (policy 13993), 7704', 'Gas industry coverage '
     'divides by R6027 instead of the industry gas total (6428); kerosene power coverage multiplies power by domestic '
     'shipping (R2270 x R2273).', 'Fixed: coverage by subsector and fuel (ctxnew, covct).'),
    ('L75', 'Revenue reports: hard-coded row and mixed totals', 'Mitigation rows 17145-17149, 17175, 17186', 'The '
     '"additional revenues from excises" report indexes a hard-coded 759 (all zeros); "revenue by fuel source" takes '
     'electricity from the total (rev.tot) while the fuel rows are carbon tax revenue (rev.new).', 'Fixed: 12d and 12e '
     'read the revenue rows (v0.3.13, v0.4.15).'),
    ('L76', 'Multipliers: empty CIT table, WAGE on the GNFS table, approximate country match, default to Estimated',
     'Multipliers rows 19-22, 38-45, 1624-1822', 'With MultipliersSource = Estimated, CIT lags 1+ read the empty rows '
     '1624-1822 (so 0), WAGE reads the public consumption (GNFS) table, the country row is found by approximate MATCH '
     '(a code missing from the sorted list takes its neighbour), and any unknown source text means Estimated.',
     'Fixed (v0.4.15): CIT and WAGE take the income group, exact match with the income group as fallback, unknown text '
     'the income group.'),
    ('L77', 'Average prices: index rows point at the wrong rows, gas test on the policy total', 'Mitigation rows '
     '16302, 16374-16390', 'The "indexed vs 2022" rows read rows 16316-16323 (electricity industry, electricity '
     'residential, coal industry, ...) under the labels electricity, coal, gas, oil, ...; E16302 tests the policy gas '
     'total instead of the baseline one; labels say 2022 = 100 where baseline = 100.', 'Fixed (v0.4.15): pav.leg and '
     'pav.lidx per fuel against scenario 1.'),
    ('L78', 'ETS: auctioned share drops to 0 after the target year unless "Constant"', 'Mitigation row 1863 (MTInputs '
     'row 92)', 'With D_ETSAuctCont other than Constant the auctioned share becomes 0 after the target year (all '
     'permits free), whatever the target share.', 'Fixed (v0.4.15): the target share is held after the target year.'),
    ('L79', 'ETS: industry and transport priced as a whole when one subsector is covered', 'Mitigation rows 2322-2325 '
     '(policy 8638-8641), 7775-7778', 'The auctioned price of industry and transport takes MAX over the subsector '
     'coverage flags, and the revenue is charged on the whole sector\'s CO2: uncovered subsectors pay, while the '
     'price estimate counts covered subsectors only.', 'Fixed: coverage, price and revenue by subsector (etsc, v0.1.07).'),
    ('L80', 'ETS: the carbon-tax trajectory rescaled when the ETS is on', 'Mitigation rows 2191, 2251', 'E2191 = 1 / '
     'the volatility ratio multiplies the carbon-tax trajectory (row 2251) when the new ETS is applied.', 'Fixed: the '
     'carbon tax path is the MTInputs path; the volatility adjustment acts on the ETS price only.'),
    # v0.4.16 (survey of the subsidy, price-control, producer-subsidy and regulation rows; baseline rows, policy +6331)
    ('L81', 'Consumer subsidy phase-out: the fixed subsidy takes last year\'s factor', 'Mitigation rows 2460, 2483, '
     '2506, ... 2598, ... 2713 (fixed portion of subsidy, each price block)', 'The projected fixed subsidy is the base '
     'value x the consumer factor of the previous column (P2214 for Q), while the floating and producer rows use the '
     'year\'s own factor: the consumer phase-out lags a year.', 'Fixed (v0.4.16): every wedge takes the factor of its '
     'year.'),
    ('L82', 'Residential gas producer subsidy reads the oil row', 'Mitigation row 2547', 'The producer subsidy of the '
     'residential gas block reads row 827 (oil, $/liter) instead of 826 (gas, $/GJ).', 'Fixed (v0.4.16): producer '
     'subsidies by fuel (pros, psf); v0.9.0 (R7): in the supply cost as legacy (issue I49).'),
    ('L83', 'Electricity producer subsidy compounds the factor and lags a year', 'Mitigation rows 3592, 3601, 3630',
     'The projection is the previous value x the previous factor (N3601 x N2213), so the factors multiply year on '
     'year and lag.', 'Fixed (v0.4.16): base value x the factor of the year (fiscal line rpsu); v0.9.0 (R7.6-R7.9): the '
     'electricity producer subsidy per kWh (pseu) and residual (pser) x psf.ecy as legacy 465, passed through in the '
     'price before policies.'),
    ('L84', 'Electricity consumer subsidy phased with the price-control factor; option text mismatch', 'Mitigation '
     'rows 3606, 3635; MTInputs row 138', 'The electricity consumer subsidy (PowerSubsidyExemptInclude = Include) is '
     'phased with the price-control factor (row 2216), not the consumer factor (2214); the unit says Exempt/Include* '
     'while the value is DoNotPhaseOut*.', 'Fixed (v0.9.0, R9.2): the consumer subsidy phase-out csd uses the consumer '
     'factor when PowerSubsidyExemptInclude = Include (read per scenario), as legacy 465 O3606.'),
    ('L85', 'Electricity consumer subsidy info row subtracts industry', 'Mitigation row 7806', 'The info row is '
     '-(MIN(0, res) - MIN(0, ind)) instead of -(MIN(0, res) + MIN(0, ind)).', 'Not applicable (info row; the prototype '
     'subsidy gap rgap sums both groups).'),
    ('L86', 'No manual override for the electricity producer subsidy', 'Mitigation I828', 'The manual-input row of '
     'the electricity producer subsidy is #N/A, so a manual value is ignored.', 'Fixed (v0.9.0, R8.1-R8.2): the manual '
     'price table (Inputs_prices MPU) covers Manual inputs rows 60-146, the electricity producer subsidy included.'),
    ('L87', 'Regulations never act: share 0 and the adjustments unused', 'Mitigation C2371, F86:F90 (MTInputs rows '
     '247-251)', 'The share of the regulation shadow price on the efficiency margin, C2371 = IFNA(INDEX($F$86:$F$90, '
     'MATCH(C2370,$C$86:$C$90,0)),0), is 0: C86:C90 hold " - " plus the scenario name, so the MATCH never hits '
     '(v0.5.5: text read from the .xlsb; the LibreOffice conversion had shown IFNA(0)). The efficiency '
     'adjustments of MTInputs rows 247-251 are read into F86:F90 but referenced nowhere: the regulation scenarios '
     '(energy efficiency, vehicle fuel economy, residential, industrial) change no fuel use or vehicle choice.',
     'Fixed (v0.4.16): regulation shadow price = shadow carbon price x the scenario\'s adjustment x sector coverage.'),
    ('L88', 'Regulations never reach power', 'Mitigation rows 3398 ff.', 'The power shadow price reads the feebate and '
     'ETS rows (2354) only, though the energy efficiency regulation scenario covers power.', 'Fixed (v0.4.16): shpx.pow '
     'includes reg.pow.'),
    ('L89', 'Coal in road, residential and services reads the residential coal shadow price', 'Mitigation rows 5396, '
     '5553, 5634', 'The coal rows of road, residential and services read row 2378 (coal, residential) whatever the '
     'sector.', 'Fixed: shadow prices by coverage sector x EF (shp).'),
    ('L90', 'Residential leakage breaks the useful-energy balance', 'Mitigation row 5593',
     'The biomass gain is -dF x e_m (the equivalent biomass is multiplied by BioEff again); conserving cooking energy needs -dF x e_m / e_b, so the gain is 5 times too small.',
     'Fixed in v0.5.1 (lkb = -lkd x e_m / e_b).'),   # v0.5.1 (residential leakage survey)
    ('L91', 'Exempt residential fuel still leaks to biomass', 'Mitigation rows 5580, 5586 (against 5546-5547)',
     'The leakage price change is taken from M2652 / M2675 even when AlwaysExemptResLPGKer removes the new policy from the residential price.',
     "Fixed in v0.5.1 (lkt reads the row's own new policy nce)."),   # v0.5.1 (residential leakage survey)
    ('L92', 'ExemptMostCook never reaches Mitigation', 'Mitigation I1784, K1795, rows 5568-5570',
     'Not reproduced in the .xlsb (v0.5.5 check): I1784 = IF(AND(H1784="Yes",ISNUMBER(MATCH(L1784,...))),1,0) with H1784 = MTInputs F312 (ExemptMostCook), and K1795 feeds L5564:L5570; the "typed 0" came from the LibreOffice conversion. The exempt share is 0 in Egypt because ExemptMostCook is off. Kept as an entry for traceability; no fix needed.',
     'Not built (D8; LegacyDiff 67).'),   # v0.5.1 (residential leakage survey)
    ('L93', 'Fuel coverage rows test text labels and contain #REF!', 'Mitigation rows 2259-2268 (column E)',
     'The rows test D2312-D2320 / D2367 (text labels) and #REF!; the branch is never taken.',
     'Not built (coverage by switch).'),   # v0.5.1 (residential leakage survey)
    ('L94', 'Exemption phase-in rules differ between rows', 'Mitigation rows 2259-2265, 2270-2288 against 2266-2268, 5568-5570',
     'The first group uses YearPha with the ExemptPhaseout switch; the second counts from CPIntro (row 2258) and ignores the switch.',
     'Not built (LegacyDiff 67).'),   # v0.5.1 (residential leakage survey)
    ('L95', 'Power demand: efficiency increment sits on the net-exports row', "Mitigation row 3719 (D3719 = D3742 'Net Exports (Imports negative)', F:J net-export data egy.mit.nxp.ecy; L3719 'Additional Efficiency Improvements - Power demand', M3719 = M2198 = MTInputs F242); read as $M3719 in rows 3691, 3697, 3703, 3709",
     'One row carries two things: net-exports data (columns D-J) and the power-demand efficiency increment (L:M). The demand formulas read $M3719 as the efficiency term, so the row label misleads.',
     'Fixed in the prototype (v0.5.1 register; the power-demand efficiency term has its own labelled row, AdditionalEfficiencyPower).'),   # v0.5.1: from the team tracker (Mit+Disn_DeepDive #6)
    ('L96', 'Fuel-use block: mislabelled parameter and fuel rows', "Mitigation C2199:C2201 ('Tax in nominal or real terms?', 'Exponential option or linear' twice) beside K2199:M2201 (road, residential, industrial additional efficiency, MTInputs F243-F245); E2385 (LPG 'Road'), E2386 (kerosene 'Industry') on all-sector rows (codes shp.lpg.all, shp.ker.all); D5615, D5711, D6058, D6069 'Other oil pinducts'",
     'Column C of rows 2199-2201 labels the carbon-tax settings of column E, while every fuel row reads K:M of the same rows as the additional-efficiency term; the sector labels of the LPG and kerosene shadow prices do not match their all-sector codes; a typo in four rows.',
     'Fixed in the prototype (v0.5.1 register; own labels: additional efficiency, shadow prices by coverage sector, fuel names).'),   # v0.5.1: from the team tracker (Mit+Disn_DeepDive #7, #8, #11)
    ('L97', "Iron & steel memo rows unused; one reads next year's growth", 'Mitigation rows 5667-5676, 5703, 5727-5728 (iron & steel block; M5667 = N2446)',
     "An EF-weighted average price (5703), an elasticity table (5668-5676) and 'Fuel'/'Average' demand and efficiency multiples (5727-5728) are computed but referenced nowhere; M5667 takes next year's GDP growth (N2446).",
     'Not built in the prototype (dead memo rows).'),   # v0.5.1: from the team tracker (Mit+Disn_DeepDive #10)
    ('L98', 'Feebate inclusion of industry reads the ETS industry flag', 'Manual inputs P54:X54 (name FeebateInclusion -> MTInputs E66:E82)',
     'P54:X54 = AND(Dashboard!$R$30, P53): the ETS industry flag, not the feebate flag K44.',
     'Not applicable in the prototype (feebate coverage typed per scenario, MTInputs rows 66-82).'),   # v0.5.2 (Manual inputs survey)
    ('L99', 'ETS inclusion of machinery and other manufacturing uses the buildings flag', 'Manual inputs S11, U11 (name ETSInclusion)',
     'S11 and U11 read Dashboard Q30 (buildings) while mch, irn, nfm, cem read R30 (industry).',
     'Not applicable in the prototype (ETS coverage typed per scenario, MTInputs rows 99-115).'),   # v0.5.2 (Manual inputs survey)
    ('L100', 'Manual domestic prices: the electricity rows are never read', 'Manual inputs G59:N146 (names _manual_prices, _manual_codes)',
     '_manual_prices (G59:N133) and _manual_codes (G59:G133) stop at row 133, so the electricity prices and producer subsidy (rows 136-146) are never read (the cause of L86).',
     'Fixed (v0.9.0, R8.1-R8.2): manual domestic prices read for rows 60-146 (Inputs_prices MPU), electricity '
     'included.'),   # v0.5.2 (Manual inputs survey)
    ('L101', 'Manual services income elasticities read the industries column', 'Elasticities F51:F58 (Manual inputs rows 279-286)',
     'F51:F58 (services) read Manual inputs column M (industries) instead of N; the price and efficiency rows are right.',
     'Fixed (v0.9.0, R8.3-R8.4): manual elasticities read (Inputs_ela columns I:M); services read column N.'),   # v0.5.2 (Manual inputs survey)
    ('L102', 'Manual non-energy elasticities can never take effect', 'Manual inputs K326:K327; Mitigation K366:M367',
     'K326:K327 are IF($E$293="Manual",#REF!,...) and Mitigation K366:M367 test E288 (MTInputs ElastIncAdjustment), which never equals "Manual".',
     'Fixed in v0.5.2 (typed inputs on Manual inputs K325:M327, read directly; same values; LegacyDiff 72).'),   # v0.5.2 (Manual inputs survey)
    ('L103', 'Manual SCC reads a path typed on Mitigation, not the Manual inputs block', 'Manual inputs rows 234-240; Mitigation row 17668',
     'The SCC block of Manual inputs is read by nothing; the Manual option of NSCCSource / GSCCSource takes the path typed on Mitigation row 17668.',
     'Fixed in v0.5.2 (scc.man reads Manual inputs row 237 by year; names SCCManVal, SCCManYear). No effect on the shipped scenarios (SCC source Target).'),   # v0.5.2 (Manual inputs survey)
    ('L104', 'Name CH4Feebate points to an empty cell', 'Manual inputs J217 (name CH4Feebate)',
     'The defined name CH4Feebate points to J217, which is empty (the methane block ends at row 200).',
     'Not applicable in the prototype (name not used).'),   # v0.5.2 (Manual inputs survey)
    ('L105', 'Dashboard industry feebate rates are lost', 'MTInputs E56:E64 (Dashboard H46:K47)',
     'E56:E58 and E61:E63 transpose Dashboard H46:J46 and H47:J47; E59 and E64 (industry) are empty, so the Dashboard industry feebate rates K46 / K47 never reach MTInputs.',
     'Not applicable in the prototype (feebate rates typed per scenario on MTInputs).'),   # v0.5.2 (Manual inputs survey)
    ('L106', 'Manual inputs memo swaps the renewables and electricity price elasticities', 'Manual inputs K315:N316',
     'The memo totals of renewables and electricity use the price elasticity rows 298 and 297 the wrong way round.',
     'Fixed in the placed memo (display only).'),   # v0.5.2 (Manual inputs survey)
    ('L107', 'Renewable subsidy: start year of the additional subsidy reuses the consumer-subsidy phase-out year', 'Mitigation E2736 (policy E9052) = row 270 = MTInputs F132 (YearConsSubPha)',
     'The additional renewable subsidy (MTInputs 353) starts in the year the consumer fuel subsidies start to be phased out; it has no start-year input of its own.',
     'Fixed (v0.5.4): own input RenSubsidyAddStartYear (MTInputs row 482, default 2027 = the default of row 132); rows rnsp, rns.'),   # v0.5.4 (power features)
    ('L108', 'Cost of renewable subsidies counts the base subsidy twice, ignores the hydro switch and omits biomass', 'Mitigation rows 7883-7889 (policy +6316)',
     'Rows 7883-7886 = (row 2743 + row 2745) x generation, but row 2745 already equals row 2743 minus the additional subsidy, so the base subsidy enters twice; hydro (7885) ignores RenewableSubsidyHydro; biomass has no row; 7889 enters total revenue (row 8009).',
     'Fixed (v0.5.4): revenue = subsidy x generation by type (row prrns), hydro by its switch, biomass included; in rsub.pow and rpol.ren.'),   # v0.5.4 (power features)
    ('L109', 'Capex decline options Low and Vhigh have no wind and solar series', 'Mitigation rows 3038-3046; Power rows 303-330',
     'RenewableCostDeclineRate Low gives codes wld.ctf.low.wnd/sol and Vhigh wld.ctf.vhg.wnd/sol/ore, which the Power tab does not hold (only oldlow, oldvhg); the MATCH fails and the INDEX errors.',
     'Fixed (v0.5.4): the older series of the same option (wind, solar) or Medium (other renewables, Vhigh), Inputs_ppath tcf|<type>|<option>. User to confirm the fallback.'),   # v0.5.4 (power features)
    ('L110', 'Power revenue rebate counts VAT that was never collected', 'Mitigation rows 3615, 3644, 3663, 7874, 7735 (policy +6316 / +6316)',
     'The rebate includes VAT (carbon cost x pass-through x (1 + VAT)) and enters total revenue through row 7735, while the VAT on the carbon cost is never counted as revenue.',
     "Fixed (v0.5.4): the rebate returns the carbon cost passed through (row rreb, without VAT) and the VAT on it is not collected (rnvat); the total change equals legacy's."),   # v0.5.4 (power features)
    ('L111', 'Manual electricity excise revenue counts the whole excise, also where the price does not include it', 'Mitigation rows 3602, 3631, 3660, 7871, 7748',
     'The revenue memo 3660 (and 7748) = manual excise x consumption in every year, while the price includes only the change since the last historical year x pass-through.',
     'Fixed (v0.5.4): excise revenue = the excise in the price x consumption (rows pex, rpex, rexm).'),   # v0.5.4 (power features)
    ('L112', 'Policy copies of the shadow-price rows read the baseline carbon price in the regulation term', 'Mitigation rows 8693-8704 (policy copies of 2377-2388)', 'The policy copies keep $D$2369 and L$2375 (absolute rows of the baseline block), so their regulation term reads the baseline carbon price (0) instead of the policy run\'s; once L87 is fixed, regulations still do nothing in the policy run. Found by the v0.5.5 cell plans (text read from the .xlsb); to confirm in Excel.', 'Not replicated: the prototype\'s regulation shadow price is per scenario group (reg rows, v0.4.16).'),   # v0.5.5
    ('L113', 'Power switches tested for the exact "Yes" (was issue I58)', 'Mitigation G261 (PowerRebates), row 3150 (RenewableSubsidyHydro), F201 (AdditionalExcise)', 'The switches test ="Yes", so the starred default "Yes*" of the MTInputs dropdowns counts as No: choosing the default option switches the feature off. Reclassified as a bug by the user (2026-10-19), as the PPA switch.', 'Fixed (v0.5.4): the prototype accepts Yes or Yes* (LEFT 3).'),   # user 2026-10-19
    ('L114', 'Renewable subsidies: nominal inputs used as real (was issue I55)', 'Mitigation rows 2734-2735, 2743, 2745 (MTInputs 352-353)', 'MTInputs 352-353 are labelled $/kWh nominal but enter the real cost and revenue without deflation (row 2743 = -E2734). A formula that contradicts its label: reclassified as a bug by the user (2026-10-19).', 'Fixed (v0.5.6): the inputs are converted to real with the CPI factor of the year (row rnsp).'),   # user 2026-10-19
    ('L115', 'Residential gas: current ETS price reads the LPG transport row', 'Mitigation row 2555 (policy 8871)', 'Row 2555 (nga res, current ETS permit price) = K$1720 (LPG, transport/industry) instead of K$1715 (natural gas, residential); the other blocks read their own row. Found 2026-10-19 while planning L64/L65.', 'Fixed by design: the prototype reads the existing ETS price by fuel and sector (section 2).'),   # 2026-10-19
    ('L116', 'Services gasoline and diesel income elasticities: step-change column reads the wrong rows', 'Elasticities H53, H54', 'H53 = H173 (renewables, services) and H54 = H174 (electricity, services) instead of H169 and H170 (gasoline, diesel, services); every other row reads its own. No effect today (all 0.13).', 'Not built: the prototype reads the income elasticities by code from the data step.'),   # 2026-10-19
    ('L117', 'Transfers multiplier (TRNS): estimated lag-0 table read two rows off', 'Multipliers D44', 'D44 reads INDEX(D$1218:D$1418, ...) while E44:O44 read $1220:$1418 (rows 1218-1219 are titles). No effect today (lag 0 is 0 for every country).', 'Not replicated: the prototype reads the multiplier table by country code.'),   # 2026-10-19
    ('L118', 'Manual power investment: the need net of manual investment is never used', 'Mitigation row 4108', 'Row 4108 (needed effective investment after manual investment) is computed but the logit investment (rows 4110-4118) reads row 4028, so logit investment comes on top of the manual one (over-investment). Found by the power plan survey (item 8).', 'Fixed (v0.5.6, P3): rows needm, first and deficit use the need net of manual investment.'),   # v0.5.6
    ('L119', 'NDC year adjustment applied twice for BAU targets and never for Fixed or Historical', 'Mitigation rows 18399, 18407-18412, 18426-18428, 18443-18445', 'F18399 = IF(target year < 2030, (2030 - base)/(target year - base), 1) is at least 1, so the "<1" branches of the Fixed and Historical blocks (rows 18426-18428, 18443-18445) never run, while the BAU block multiplies both the reduction (18407) and the level (18410: BAU x (1 - reduction x adj) x adj) by it: a 2025 BAU target is scaled up twice and the other types not at all. Found by the item 8 plan (v0.5.7).', 'Fixed (v0.5.7, NDC comparison 14c): the prototype compares every NDC in its own target year (each year is modelled), so no adjustment is needed.'),   # v0.5.7
    ('L120', 'NDC index rows: unconditional and conditional ratios inverted against the average', 'Mitigation rows 18482-18484', 'Rows 18482-18483 divide the start-year emissions by the target (G18431/F18479) while row 18484 divides the target by the start-year emissions; the chart rows 18494-18495 read 18484 for the unconditional line and 18483 (inverted) for the conditional one. Found by the item 8 plan (v0.5.7).', 'Fixed (v0.5.7, NDC comparison 14c): ndc.idx = target / base-year GHGs incl. LULUCF for both.'),   # v0.5.7
    ('L121', 'Historical NDC: the target "level" is the emissions cut', 'Mitigation rows 18443-18445', 'Rows 18443-18445 return the cut (F18440 x adj) when adj < 1 and the level otherwise; harmless today only because adj < 1 never happens (L119). Found by the item 8 plan (v0.5.7).', 'Fixed (v0.5.7, NDC comparison 14c): level = reference-year emissions x (1 - reduction).'),   # v0.5.7
    ('L122', 'Intensity NDC incl. LULUCF adds a blank cell instead of LULUCF emissions', 'Mitigation rows 18461-18462', 'The excludes-LULUCF branch adds $J$18450 where the LULUCF emissions are in column I (I18450 = G - F). J18450 is not blank: it holds the non-CO2 emissions (F - H, 254.9 Mt for Egypt), so non-CO2 is counted twice and LULUCF is missed (cell plan 2026-10-20 corrected the register). Found by the item 8 plan (v0.5.7).', 'Fixed (v0.5.7, NDC comparison 14c): the reduction is computed on the NDC basis and applied to the BAU incl. LULUCF, as for the other types.'),   # v0.5.7
    ('L123', 'Intensity NDC: reference-year GDP read from a fixed cell', 'Mitigation row 18451', 'Not reproduced in the .xlsb (cell plan 2026-10-20): G469 = _NDC_Year, so G470 is the WEO real GDP of the reference year and F18466 = G470 is right; the fixed-cell reading came from the LibreOffice conversion. Only gap: reference years before 2000 find no GDP (#VALUE! or N/A; the prototype also gives N/A). Kept for the record. Found by the item 8 plan (v0.5.7).', 'Fixed (v0.5.7, NDC comparison 14c): ndc.gdp.ref looks the reference year up (WEO real GDP; N/A when the year is not in the data).'),   # v0.5.7
    ('L124', 'Producer subsidy: the residential gas block reads the oil subsidy', 'Mitigation row 2547 (N2547)', 'The "in which: producer-side subsidies" row of the gas | residential block reads N$827 (oil, $/liter) where the other gas blocks read N$826 (gas, $/GJ). Found by I49 (v0.6.1). The same cells as L82 (fix plan L82 covers it).', 'Fixed (v0.6.1, I49): every block reads the per-unit subsidy of its own fuel by its international price position (psp).'),   # v0.6.1
    ('L125', 'Producer subsidy: other oil products add a per-liter value to a per-barrel price', 'Mitigation row 2685 (N2685)', 'The other-oil-products block ($/bbl) adds the oil subsidy per liter (row 827) unconverted, about 159 times too small. Found by I49 (v0.6.1).', 'Fixed (v0.6.1, I49): x liters per barrel (LitersPerBbl) for a barrel-priced block.'),   # v0.6.1
    ('L126', 'Power: fuel price for power averages later years', 'Mitigation rows 3155-3163 (A18)', 'The fuel price for power is a centred 5-year average, AVERAGE(t-2 .. t+2) of the fuel prices (rows 3072-3080), so this year\'s power costs read the next two years. Safe only while those prices depend on inputs alone: any quantity-dependent price (an endogenous ETS price, a supply-cost feedback) closes a circular reference through the GDP feedback. Found by the circular-reference review (v0.6.2, user 2026-10-20).', 'Fixed (v0.6.2): trailing average t-4 .. t (fpp over the row fpn; AVERAGEIFS on the year row keeps the scenario\'s own years); legacy 465 has the same fix for coal, gas and oil, not for biomass (row 3163). Price changes reach power costs about two years later than in legacy 456 (465: biomass only).'),   # v0.6.2
    ('L127', 'Power: levelised variable cost reads the variable cost to 2041', 'Mitigation rows 3439-3447 (D9)', 'Investment choices use the variable cost levelised from the year to the end of the horizon (perfect foresight of the cost path). Safe only while that cost is built from inputs alone (prices before new policies, announced policy rates); a variable cost that reads quantities would close a circular reference. Latent today. Found by the circular-reference review (v0.6.2, user 2026-10-20).', 'Fixed (v0.6.2) as a rule with a test: the levelised cost reads only input-driven costs (tvc: fuel price for power, variable O&M, policy rates, shadow price, rebate); the quick check tests that no other row reads a later year and that tvc reaches no fuel use, GDP or power quantity row.'),   # v0.6.2
    ('L128', 'Net revenue report rows read the next year', 'Mitigation rows 6238, 6243 (policy 12554, 12559)', 'The net revenue rows (USD and % of GDP) read the next column of rows 8024 and 8029 (K6238 = L8024 ... AD6238 = AE8024), so each year shows the next year\'s net revenue. Report only (rows 6239, 6244 read them). Found by the read-of-later-years scan of legacy (v0.6.2, user 2026-10-20).', 'Not in the prototype (its revenue rows read the same year; reporting rebuilt). Legacy fix: K6238 =K8024 and K6243 =K8029, filled K:AD.'),   # v0.6.2
    ('L129', 'Baseline renewable subsidy counted twice', 'Mitigation rows 2785-2788, 2947-2951, 7883-7886 (against 2743, 2745)', 'The rows add L2743 + L2745, but L2745 already includes L2743, so the baseline renewable subsidy is counted twice. Only when MTInputs row 352 (RenewableSubsidyBL) is not zero; 0 for Egypt. Found by the cell plans (user 2026-10-20: a bug).', 'Fixed (prototype: one renewable subsidy row rnsp = baseline + additional, counted once).'),   # v0.6.3
    ('L130', 'Intensity NDC: conditional and unconditional rows use different base years', 'Mitigation rows 18455-18456', 'F18456 (conditional) applies the cut to the target-year BAU intensity (F18454); F18455 (unconditional) applies it to the reference-year intensity (F18453). Found by the cell plans (user 2026-10-20: a bug).', 'Fixed (prototype 14c: ndc.hi applies the cut to the reference-year intensity x target-year GDP, for both).'),   # v0.6.3
    ('L131', 'Codes: one output code on rows with different contents', 'Mitigation rows 466, 2442, 16170 (gdp.pre.lvl); 7722, 7742, 7985 (sub.new.usd); 7638-13962 (rev.ctr.coa)', 'Legacy reuses a code for other quantities: gdp.pre.lvl for ln(GDP pc), GDP in $mn and in bn US$; sub.new.usd for revenue subtotals; rev.ctr.coa for the gasoline to electricity rows. A lookup by code finds the first row only. Found by the codes crosswalk (v0.7.1).', 'Fixed (v0.7.2, codes R7): every prototype code is unique (check_codes; the 18 copy rows carry no code).'),   # v0.7.2
    ('L132', 'Codes: capitals and empty tokens', 'Mitigation rows 7606, 13922 (oc.tot.); em.pm2.All.<sector> rows', 'Legacy codes mix capitals (All) into the lower-case protocol and end with an empty token (oc.tot., no scenario number), so a lookup of the protocol code fails. Found by the codes crosswalk (v0.7.1).', 'Fixed (v0.7.2): prototype codes are lower case with no empty token (code formula; check_codes).'),   # v0.7.2
    ('L133', 'Codes: nox.tot holds N2O, oc.tot. holds NOx', 'Mitigation rows 7606, 13922 and the GHG total rows (nox.tot)', 'The N2O total in CO2e carries the code nox.tot and the NOx forcing row the code oc.tot. (labels: Nitrous oxide; Nitrogen oxides): a reader of the codes takes one gas for the other. Found by the codes crosswalk (v0.7.1).', 'Fixed (v0.7.2, codes R5): n2o.tot and nox.tot carry their own gas.'),   # v0.7.2
    ('L134', 'Price-increase units: other oil products "$/bbn", default "$/liter" for other oil products and biomass',
     'MTInputs rows 182-183 (columns E and G); Mitigation I177, I180',
     'The unit labels of the price-increase inputs read "$/bbn" (for $/bbl) for other oil products, and the default '
     'column says "$/liter" for other oil products and biomass, whose prices are per barrel and per GJ. No formula '
     'reads the labels (Mitigation rows 168-180 use the amounts in G and H only), so no value changes; a user typing an '
     'increase per liter for these fuels gets a wrong price path. Found by the tracker leads (2026-10-23).',
     'Fixed (v0.8.3): the prototype\'s ScenarioDefinition rows 182-183 read $/bbl and $/GJ, defaults included.'),   # v0.8.3
]

# v0.4.15: the distribution module (legacy sheet Distribution; Methods, chapter Distribution sections 3-5). Bugs are fixed
# in the prototype (v0.4.4); the issues are replicated (I76-I80) or not modelled yet (I81-I84).
DIST_BUGS = [  # id, title, where, what legacy does, status
    ('L138', 'Targeted transfer capped at 10 points, not the decile\'s population share', 'Distribution R2562:Z2562',
     'The targeted share of a decile is capped at 10 percentage points instead of its population share: 105.6% of '
     'decile 2 receives the transfer.', 'Fixed (v0.4.4): capped at the decile\'s population share.'),
    ('L139', 'Basket uses decile 1\'s elasticity adjustment and exemption test', 'Distribution C.V, C.VI (e.g. Q1607)',
     'The all-household basket takes the elasticity adjustment and the exemption test of decile 1.',
     'Fixed (v0.4.4): the basket elasticity, never exempt.'),
    ('L140', 'Current spending tests the ASPIRE flag of the targeted transfer', 'Distribution Q2633', 'Current spending '
     'reads the ASPIRE flag of the targeted transfer (I213) instead of its own (I214).', 'Fixed (v0.4.4): no flag; the '
     'ASPIRE programme of the chosen type, 0 if absent.'),
    ('L141', 'Public investment and current spending vanish with the transfer settings', 'Distribution rows 2701-2707',
     'Public investment and current spending are 0 when the transfer coverage or percentile is 0.', 'Fixed (v0.4.4): '
     'independent of the transfer settings.'),
    ('L142', 'Targeted exemption capped by all revenue; urban and rural not per capita', 'Distribution Q2749', 'The '
     'targeted exemption is capped by all carbon-pricing revenue (I154) instead of the PIT share (I163); urban and rural '
     'values are not per capita.', 'Fixed (v0.4.4): capped by the PIT revenue; per capita in every sample.'),
    ('L143', 'Urban and rural compensation shares on overall weights', 'Distribution Q3259, Q3263', 'The urban and rural '
     'compensation shares divide by overall consumption weights (they sum to 52 and 47).', 'Fixed (v0.4.4): each '
     'sample\'s own weights, each summing to 100.'),
    ('L144', 'Deadweight loss in mixed units', 'Distribution rows 859-883', 'The deadweight loss is a price fraction '
     'subtracted from a % of consumption.', 'Fixed (v0.4.4): DWLTri x (1 - factor) x the effect, in the same units.'),
    ('L145', 'Analysis year and statistic read MTInputs column D', 'MTOutputs rows 1001-1002', 'dist.year and dist.stat '
     'read MTInputs column D, which is 0 in dashboard mode.', 'Fixed (v0.4.4): the analysis year and statistic of the '
     'scenario group.'),
    ('L146', 'Rural rows labelled Urban; fuel code oil vs oop', "Distribution H2417, H2422 (456 numbering; DeepDive cites 2416, 2421): '... - Urban Sample' on rows computed from the rural rows 2402, 2407, 2412; C.II row 746 code 'oil' against price rows 774 and 804 'oop'",
     'Post-CP consumption rows of the rural sample carry the urban label; the elasticity and price rows of other oil products use different codes and are paired by row position only.',
     'Fixed in the prototype (v0.5.1 register; own labels, rural and urban rows by key; one code oop paired by code).'),   # v0.5.1: from the team tracker (Mit+Disn_DeepDive Dist 1, Dist 2)
    ('L147', 'ASPIRE transfer pays out more than the revenue', 'Distribution row 2629 (-> 2697-2699)', 'Per capita = scale x benefit x [decile targeted], with the scale computed over actual receivers: partly targeted deciles get the full benefit, leakage deciles none; 125-129% of the funds are paid out for Egypt.', 'Fixed (v0.6.0): transfer = revenue x benefit x share receiving / sum over deciles (payout = revenue).'),   # v0.6.0
    ('L148', 'ASPIRE program without country data: the transfer vanishes', 'Distribution row 2617, I213', 'A program with no data gives a zero scale, so the transfer share of revenue silently disappears (no IFERROR).', 'Fixed (v0.6.0): cash used and the settings check says so.'),   # v0.6.0
    ('L149', 'ASPIRE branch skips the median flag and the zero-coverage test', 'Distribution row 2697', 'Parenthesisation: the ASPIRE branch is outside the flag and the coverage/percentile test.', 'Fixed (v0.6.0): one formula for every targeting mode.'),   # v0.6.0
    ('L150', 'Public investment and current spending use the targeted-transfer median flag', 'Distribution rows 2701-2707', 'Under the median statistic, public investment for deciles 5-10 is zeroed by the transfer flag.', 'Fixed (v0.6.0): the flag applies to the targeted transfer only.'),   # v0.6.0
    ('L151', 'Poverty targeting: share receiving ignores targeting, coverage and leakage', 'Distribution row 2679', 'The share receiving is the share below the line, while the amounts use receivers x poor.', 'Fixed (v0.6.0): share receiving = receiving x below the line.'),   # v0.6.0
    ('L152', 'Poverty targeting: urban and rural pay out about half of the funds', 'Distribution rows 2650-2674', 'Sample poverty shares x the overall receiving share x the overall amount: urban plus rural recipients are about 52% of the overall ones.', 'Fixed (v0.6.0): urban and rural per capita = the overall per capita (issue I78).'),   # v0.6.0
    ('L153', 'Poverty share x 10 assumes deciles of 10%', 'Distribution row 2649', 'Decile 2 gives 111% (capped at 100 by MIN).', 'Kept with the cap (data limitation; noted).'),   # v0.6.0
    ('L154', 'ASPIRE values converted without a PPP factor', 'Distribution row 2618, I220-I223', 'PPP $ per day become "real LCU" by a deflator ratio only; the data year is unused. Displays only (the scale cancels).', 'Fixed (v0.6.0): rows labelled PPP $ per day; no conversion.'),   # v0.6.0
    ('L155', 'Horizontal p25/p75 effects inflated', 'Distribution rows 3188-3206', 'Effect x (1 + effect / other effect): Egypt decile 1 p75 -3.09 becomes -6.77.', 'Fixed (v0.6.0): effect = price factors x the budget shares of the percentile x loss scale.'),   # v0.6.0
    ('L156', 'Horizontal "chosen statistic" recycling divides by median consumption', 'Distribution rows 3193, 3201, 3209', 'Hard-coded .median.', 'Fixed (v0.6.0): the recycling row of the chosen statistic.'),   # v0.6.0
    ('L157', 'Decile brackets always divided by 1000', 'Distribution row 2774', 'Relative reference instead of $G$2771.', 'Fixed (v0.6.0): no scaling; brackets in local currency.'),   # v0.6.0
    ('L158', 'Decile bracket labels unusable', 'Distribution rows 2775-2784', 'Appends "0" when not in thousands; one significant digit gives "10k-10k"; survey-year values.', 'Fixed (v0.6.0): real local currency of the analysis year (survey value x consumption adjustment), full numbers.'),   # v0.6.0
    ('L159', 'Sector table "ordered by demand" sorts each column independently', 'Distribution rows 3300-3310', 'LARGE per column: output and exports do not belong to the sector named.', 'Fixed (v0.6.0): one rank per sector; values read by rank.'),   # v0.6.0
    ('L160', 'Ordered sector tables show 11 of 12 sectors', 'Distribution rows 3300-3323', '11 rows for 12 sectors.', 'Fixed (v0.6.0): every sector listed.'),   # v0.6.0
    ('L161', 'Chemicals and power missing from the CPAT-sector table', 'Distribution rows 3285-3296', 'The most affected sector (chemicals) drops out of the CPAT-sector charts and shares.', 'Fixed (v0.6.0): 14 sectors, chemicals and power included.'),   # v0.6.0
    ('L162', 'Chart 19 labels ranked separately from their values; ties', 'Distribution row 3313', 'Labels ranked by one column, values by another; MATCH on equal values returns the first sector twice.', 'Fixed (v0.6.0): one ranking; ties broken by order.'),   # v0.6.0
    ('L163', 'Pass-through coefficients one row off', 'Distribution G659:BR659', 'Every sector gets the coefficient of the next row; power has none.', "Fixed (v0.6.0): coefficient of the sector's own row; power 1."),   # v0.6.0
    ('L164', 'MTOutputs outpriin labels do not match their values', 'MTOutputs K1048:L1058', "Fixed labels read the sorted rows (outpriin.avi = iron and steel's value).", 'Fixed (v0.6.0): outpriin by sector code.'),   # v0.6.0
    ('L165', 'MTOutputs codes without a dot', 'MTOutputs E1006, E1013', 'egydistn.cts..., egydistn.rec...', 'Not replicated: the prototype writes the right codes.'),   # v0.6.0
    ('L166', 'MTOutputs ppic.fuel empty', 'MTOutputs K1046', 'Blank cell.', 'Fixed (v0.6.0): the fuel transformation sector is read (0).'),   # v0.6.0
    ('L167', 'Lorenz equality line in 10% steps', 'Distribution rows 2455-2457, 3109', 'The x-axis is the actual cumulative population share.', 'Fixed (v0.6.0): equality line = cumulative population share.'),   # v0.6.0
    ('L168', 'Absolute overall rows carry wrong codes', 'Distribution L3036:L3043', 'Codes bsh.ely.dec.rur... on overall rows (labels only).', 'Not replicated: the prototype builds codes from the row ids.'),   # v0.6.0
]
DIST_ISSUES = [  # id, title, description, status
    ('I76', 'Spending in the base year', 'Fuel spending is taken in the base year (legacy: the first calculation year), '
     'with the price changes of the analysis year.', 'Replicated'),
    ('I77', 'GTAP values converted with the local GDP deflator', 'The GTAP input-output values are converted with the '
     'local GDP deflator (legacy I244).', 'Replicated'),
    ('I96', 'Elasticities always overall, mean', 'The data have no other statistics or samples.', 'Replicated'),
    ('I78', 'Recycled amounts per capita from the overall sample', 'Applied to urban and rural consumption alike.',
     'Replicated'),
    ('I79', 'Gini from a fitted Lorenz curve', 'The Gini comes from the fitted curve, not the trapezoid rule.',
     'Replicated'),
    ('I80', 'Carbon-pricing revenue stands for the revenue to recycle', 'Revenue from new policies (rnew: carbon tax, '
     'VAT on it, auctioned ETS) is the revenue recycled, as legacy\'s carbon-pricing revenue.', 'Replicated'),
    ('I81', 'ASPIRE-targeted transfers (TransferType other than Cash)', 'Modelled v0.6.0: the transfer follows the '
     'program\'s incidence by quintile (legacy rows 2617-2629; bugs L147-L149 fixed).', 'Replicated (v0.6.0)'),
    ('I82', 'Poverty-line targeting (TargetBelow, with Cash only)', 'Modelled v0.6.0: the transfer weights each decile by '
     'its share below the line (HHSurvey pct_belowpl_*, mean as legacy; bugs L151-L153).', 'Replicated (v0.6.0)'),
    ('I83', 'Pass-through switch wired into the production-sector prices only', 'PassthroughDist scales the sector '
     'price changes (legacy D.VI, bug L163 fixed), not the household effects, as legacy.', 'Replicated (v0.6.0)'),
    ('I84', 'Median statistic: the targeted transfer only reaches deciles where more than half receive', 'Modelled '
     'v0.6.0 (legacy row 2685): the money not paid is not redistributed, as legacy.', 'Replicated (v0.6.0)'),
]

MVP_BUGS = [  # id, title, found / fixed in, what happened, fix
    ('M1', 'Version-log rows rewritten with the current version', 'v0.0.3-v0.0.4 / v0.0.5',
     'The builders wrote earlier version-log rows with the current version number.',
     'Each row has its own version; old workbooks left as shipped.'),
    ('M2', 'Power: VAT left out on the policy term', 'v0.1.05 / v0.1.06',
     'The end-user price added the policy cost without VAT; legacy row 3614 charges VAT.',
     'VAT on the policy term as legacy (no effect for Egypt, VAT 0).'),
    ('M3', 'Power: long-term storage allocation left out', 'v0.1.05 / v0.1.06',
     'The legacy note "incomplete" was read as "not applied".', 'The 33% allocation is applied once.'),
    ('M4', 'Power: VRE share without other renewables', 'v0.1.05 / v0.1.06',
     'Legacy row 3851 also counts other renewables.', 'Follows legacy (other renewables 0 for Egypt).'),
    ('M5', 'Defined name clashed with a LAMBDA name', 'v0.1.07 build / v0.1.07',
     'The defined name ETSSemi equals the LAMBDA ETSSEMI ignoring case and gave #NAME?; the ETS goal seek stopped '
     'converging.', 'Renamed SemiEl; the builder asserts that no defined name equals a LAMBDA name.'),
    ('M6', 'Power ETS revenue valued at the tax-equivalent price', 'v0.1.05 / v0.1.09',
     'Power new-policy revenue (ccpav x consumption) valued the ETS at the tax-equivalent price, about 10% high at '
     'Medium volatility.', 'Revenue by generation type (prnew) with the ETS at the permit price; rcarb kept as a memo.'),
    ('M7', 'Stale texts in the workbook and notes', 'v0.1.08 / v0.1.09',
     'Section 12 and 13 notes said power was not included; PowerPaths said interim data; data sheets named old '
     'extractors; method notes described earlier versions.', 'Texts updated; the check now scans the workbook texts '
     'for stale statements and missing file references.'),
    ('M8', 'LegacyDiff rows out of date', 'v0.1.09 / v0.2.2',
     'Existing carbon pricing was still listed as "Not modelled"; the formula-structure row described the LAMBDA '
     'right column of v0.1.07.', 'Rows updated; the check scans for these phrases.'),
    ('M9', 'Legacy comparison note from v0.1.01', 'v0.1.02-v0.1.09 / v0.2.2',
     'legacy_comparison described the v0.1.01 baseline and its script wrote a different file name.',
     'Re-run on v0.2.2 (legacy_comparison_v6_4.md).'),
    ('M10', 'Total rows labelled "All subsectors"', 'v0.1.09 / v0.2.3',
     'Since v0.1.09 the totals (fuel use, CO2, revenues) include power, but the label of the sector code all still said '
     '"All subsectors".', 'Label "All sectors".'),
    ('M11', 'Macros read 19 year columns', 'v0.2.3 build / v0.2.3',
     'The VBA module had the number of years (NYEARS = 19, 2022-2040) as a constant; with the horizon to 2041 the batch '
     'run and CheckBatchRun would have stored and compared one year too few (found by the check).',
     'NYEARS = 20; the builder now asserts that it equals the number of model years.'),
    ('M12', 'Sheet Lambdas: formula texts named merged sheets', 'v0.3.6 / v0.3.13',
     'The tab merge of v0.3.6 re-pointed every formula but not the formula texts of sheet Lambdas (column F), so the '
     'rows reading the power and price inputs named Inputs_power / Inputs_prices, which no longer exist; copied into '
     'Mitigation they gave #REF! (found by the full check, variant B).',
     'merge_tabs re-points the texts too; the full check copies them over every row (variant B).'),
    ('M13', 'Road vehicle feebate counted the carbon price twice', 'v0.3.5 / v0.4.16', 'The vehicle feebate rate of the '
     'engineer road model added the carbon price x road feebate share in every policy scenario, although the carbon '
     'tax is in the fuel price already (legacy adds the shadow carbon price, 0 under explicit pricing).',
     'The road regulation shadow price (reg.rod) replaces it; 0 under explicit pricing.'),
    ('M14', 'LAMBDA library texts named a merged-away sheet', 'v0.4.2 / v0.5.3', 'The 21 LAMBDA-library texts of the power pollutant rows (sheet Lambdas, column C) still named the sheet Inputs_power: the v0.3.13 fix (M12) re-pointed the texts only on sheets that stay in place, and Lambdas is an appended block since v0.4.2; pasted, they gave #NAME?.', 'merge_tabs re-points the Lambdas texts of an appended block too (host Mitigation); the full check lists any text naming a merged-away sheet.'),
]

ISSUES = [  # id, title, description, where it is documented
    ('I1', 'Not yet run in Excel', 'The workbook and its VBA project were generated and tested without Excel '
     '(LibreOffice). Open it, enable macros and run CheckBatchRun once; if Excel rejects the VBA project, import '
     'CPATScenarios.bas.', 'TODO; Methods, chapter Macro and results'),
    ('I2', 'Excel versions', '2022-2040 need Excel 2019 or later (MINIFS, AGGREGATE); the last year 2041 is the '
     'LAMBDA year and needs Excel 365.', 'README; NORMS (LAMBDA year)'),
    ('I3', 'New sector | fuel pairs need a label', 'A new pair on Mitigation needs a row in the member-label table on '
     'Mapping, or its description shows #N/A (20 spare rows in the defined name).', 'CAVEATS v0.1.08'),
    ('I89', 'Price vintage: data prices end in 2022 (legacy 465: 2024)', 'The last historical price year is 2022 (Settings C10, '
     'v0.3.7), as legacy 456, whose prices stay near their 2022 USD level; legacy 465 uses 2024 (v0.9.0 check: the '
     'electricity tax and price-chain residual are those of 2022 in the prototype). The IMF dataset also holds 2023-2024, when Egypt '
     'prices fell sharply in USD after the devaluation (gasoline 0.60 to 0.34 $/l); with C10 = 2024, fuel use and '
     'electricity demand jump in 2023 and the gap to legacy fuel use grows from 17% to 46%. Demand responds to real '
     'USD prices, as legacy.', 'legacy_comparison_v6_4.md; Methods, chapter Prices A7'),
    ('I5', 'Totals include power since v0.1.09', 'Fuel use and revenue totals of v0.1.09 and later include power and are '
     'not comparable with v0.1.08 and earlier outputs.', 'CAVEATS v0.1.09'),
    ('I6', 'Electricity subsidy gap is signed', 'Subsidies are negative (v0.2.4): the gap is negative when the tariff is '
     'below the modelled supply cost and positive when it is above; fuel subsidies count the negative part of the '
     'existing taxes only.', 'Methods, chapter Power 3.9'),
    ('I9', 'The LAMBDA year 2041 needs LAMBDA support', 'Every calculated cell of 2041 calls its named LAMBDA. '
     'Without LAMBDA support (Excel before 365, LibreOffice) 2041 shows errors, and so does its column in MTOutputs.',
     'ReadMe (LAMBDAs, year 2041); NORMS'),
    ('I10', 'Without LAMBDA support the power model looks ahead without 2041', 'The levelised variable cost (D9) uses '
     'last year\'s cost for 2041 (tvcx), and the moving average of fuel prices for power leaves 2041 out of 2039-2040. '
     'Power results 2022-2040 then differ slightly from Excel 365 (the check reports the size); stored results are '
     'the Excel 365 values.', 'check report section 1; Methods, chapter Power'),
    ('I11', 'Changing the last historical price year', 'Prices have separate history and projection blocks; changing '
     'Settings C10 needs the blocks re-dragged (or the LAMBDA of the row, sheet Lambdas, copied left over the row).', 'README'),
    ('I12', 'Values after 2030', 'Not a legacy target; the legacy CPI is held flat after 2031.', 'LegacyDiff'),
    ('I90', 'Data for other countries: proprietary tables are Egypt only', 'The model is country-generic (Settings C4) and every public '
     'table holds all countries, but the legacy proprietary tables (Balances, EnergyCons, EF_PM, IO_GTAP, HHSurvey, ASPIRE, WHOCooking) of the '
     'NoPropData file hold Egypt only. Next: paste the full tables (full legacy file or the CPAT data pipeline), rebuild BaselineCO2 for scenario 1, '
     'test a second country end to end (was a TODO item; user 2026-10-19).', 'README'),
    ('I14', 'Distance to the legacy cached baseline', 'The prototype baseline differs from the cached legacy run, mainly '
     'through the fuel-use shock (I92), jet fuel (I19), the electricity price data (I99) and the fixed legacy bugs.',
     'legacy_comparison_v6_4.md'),
    ('I15', 'Subsidy rows changed sign in v0.2.4', 'esub, esubpu, rsub, prsub, sgap and rgap are negative from v0.2.4 (net '
     'existing revenue rnet = rtx + rsub, unchanged in value). Outputs stored with v0.2.3 or earlier have the opposite '
     'sign in these rows.', 'CAVEATS v0.2.4; NORMS'),
    ('I16', 'A new block needs its label row', 'Every block of rows on Mitigation has a label row above it (D:G '
     'parameter names from Variables G:J). Copy the label row with the block; a new variable needs its labels in '
     'Variables G:J.', 'ReadMe (Layout and roll-up)'),
    ('I91', 'Egypt GHG inventory: energy CH4 breaks after 2021', 'Sheet GHGs (legacy data) gives energy CH4 of 21.9 '
     'Mt CO2e in 2021 and 1.9-2.0 in 2022-2024, while the fugitive-emissions memo alone is 20.3 in 2023: the years come '
     'from different sources. Section 14 calibrates to the last inventory year (2024, as legacy), so energy CH4 and '
     'the fuel-supply methane may be understated by about 19 Mt CO2e.', 'Methods, chapter Emissions (Data); CAVEATS v0.2.8'),
    ('I18', 'GHG totals use energy CO2 without inventory adjustment (resolved v0.3.2)', 'Energy CO2 in section 14 was '
     'section 13 (IIASA EFs, no adjustment to the inventory) plus flaring: 225 Mt in 2022 against 252 Mt in the '
     'inventory. v0.3.2: every CO2 EF is calibrated to the inventory of GHGYear (Settings EFCalib), so 2024 matches; '
     '2022 stays below the 2022 inventory because of the 2021-2022 inventory break (I91).',
     'Methods, chapter Emissions; CAVEATS v0.3.2'),
    # v0.3.7: every major departure from legacy (other than a bug fix) and every major open problem is an issue
    ('I19', 'Jet fuel (replicated v0.3.11)', 'Legacy domestic aviation burns jet fuel (707 ktoe in 2022). Since v0.3.11 the prototype '
     'has the fuel jfu (aviation only, kerosene price build-up, legacy EF row 1011, kerosene carbon-tax coverage '
     'switch); the legacy comparison includes it.', 'Reviews_and_Surveys.md (section Sector_Equations_Survey) D1; CAVEATS v0.3.11'),
    ('I99', 'Electricity price data differ from legacy', 'The corrected Egypt block supplied by the user (2026-10-09) '
     'gives residential 0.054, 0.048, 0.043 $/kWh nominal for 2022-2024; the legacy vintage has 0.097 in 2022. '
     'Electricity prices, power demand and the subsidy gap differ from legacy.', 'Methods, chapter Power; '
     'LegacyDiff'),
    ('I21', 'ETS: one auctioned share for every sector (replicated v0.4.15)', 'Legacy allocates by one auctioned share '
     'path (MTInputs rows 90-92, default 0: everything allocated free), the same for every sector. The prototype had '
     'benchmarks by sector group typed on Constants (v0.1.02), so an MTInputs auctioned share had no effect; since v0.4.15 '
     'the benchmarks are 1 - the MTInputs share of the scenario (user 2026-10-18), as legacy. Benchmarks by sector '
     '(output-based) come later.', 'Methods, chapter ETS; Methods, chapter ETS; LegacyDiff'),
    ('I92', 'Fuel-use shock of 2023-2024 (replicated v0.3.11)', 'Every legacy fuel row multiplies by (1 + shock), row 2439 = '
     'row 483 ("Covid factor"): -20.8% in 2023, +9.2% in 2024, so fuel use is 13.5% lower from 2024 on. Replicated in '
     'v0.3.11 for fuels (header row 11) and power demand, switch Settings C19 on. Open questions kept: the label "Covid '
     'factor" does not fit 2023, legacy documents the effect as "Small", and the source of the two values is unknown.',
     'Reviews_and_Surveys.md (section Sector_Equations_Survey) D2; LegacyDiff'),
    ('I25', 'Industrial process emissions below legacy, not explained', 'Both follow increases in industrial energy '
     'CO2, yet the prototype is 57.2 against 66.5 Mt CO2e in 2024 and 94.9 against 119.2 in 2040.',
     'legacy_comparison_v6_4.md; CAVEATS v0.2.8'),
    ('I26', 'GHG defaults not yet checked against legacy', 'Oil, gas and coal production held at the base year (fuel '
     'supply methane) and energy N2O moving with energy CO2 were applied as defaults in v0.2.8; their legacy '
     'counterparts are not yet checked.', 'Methods, chapter Emissions; CAVEATS v0.2.8'),
    ('I28', 'Engineer road model: calibration open', 'Off by default (TrModel = Elasticity, as the legacy Egypt run). '
     'Range anxiety is legacy\'s stored values (Egypt 2025 passenger EV share 0.09% against 0.15% actual); the '
     'ownership decline limit (10% a year) is a placeholder.', 'Methods, chapter Transport'),
    ('I29', 'Excel repair prompt (resolved v0.3.7)', 'Excel 365 removed the cell formulas calling the LAMBDAs SCALE and '
     'SHARE (found by bisection with the repair log); renamed SCALEBY and SHAREOF in v0.3.7. The quick check opens the '
     'file in Excel where Excel is installed.', 'CAVEATS v0.3.6 (variants entry); check_quick.py'),
    ('I30', 'ETS goal seek short of the cap in definition 5', 'With all permits allocated free (benchmarks 1.0, the '
     'legacy default) the ETS works at half effectiveness, so definition 5 (cap -5% in 2027 to -20% in 2035) needs '
     'about 134 $/t in 2030 and 230 $/t in 2035. The goal seek then oscillates between years: after 20 iterations '
     'covered emissions are 3.7% above the cap (2033) or below it (2041); worst gap 6.2% in the stored results.',
     'ets_goalseek.py; CAVEATS v0.3.7'),
    ('I32', 'Energy CO2 calibration to the inventory: as legacy since v0.4.11', 'Legacy row 7520 ("Adjust EFs to match '
     'energy-related CO2 to UNFCCC inventories?", Yes* by default) multiplies every CO2 EF by the inventory energy CO2 '
     'of the year before the base year over the estimate from the base-year energy balance (Egypt: 2021 inventory '
     'against 2022, 0.930), so CO2 is about 7% below uncalibrated EFs in every sector. The inventory has a break between '
     '2021 and 2022 (I17: 211 to 252 Mt), which legacy carries into the factor. v0.4.11 replicates legacy (user '
     '2026-10-18: go with legacy); before, the prototype calibrated in 2024 and kept the switch off (user decisions v0.3.2, '
     'v0.3.4).', 'Methods, chapter Macro and results; Methods, chapter Emissions; CAVEATS v0.4.11'),
    ('I33', 'Data step overwrites the corrected Egypt prices', 'extract_data rewrites every data file from its sources; '
     'prices_dom.csv then loses the corrected Egypt block (update_prices_egypt must run after it), and the files come '
     'out with CRLF line ends. v0.3.11 kept only the jet-fuel rows of its run.', 'CAVEATS v0.3.11'),
    ('I31', 'Average prices mix price and composition changes', 'Legacy F5b-c averages the after-tax price of each '
     'fuel over sectors with each scenario\'s own consumption of the year (a unit value) and reports the policy / '
     'baseline ratio and an index 2022 = 100 as price changes (Egypt 2030: gas +71%, oil +104%). A shift of '
     'consumption between sectors with different prices moves the "price change" with no price moving. Survey v0.4.15: '
     'coal and gas are averaged over power generation, residential and the 8 industry subsectors with baseline '
     'quantities (a Laspeyres index), electricity with each scenario\'s own consumption, oil products are single '
     'prices. v0.4.15 replicates legacy as the default (Settings C54 Legacy*; pav.leg, pav.lidx, pav.idx), the prototype\'s '
     'Laspeyres index over all final uses as the option.', 'Reviews_and_Surveys.md (section Downstream_Survey) F5; PriceProjection_Method'),
    ('I34', 'CH4 of the air-pollution input table: methane sources by convention', 'Legacy rows 7283-7307 feed the '
     'air-pollution module CH4 by sector: oil and gas extraction methane under "other", agriculture and waste methane '
     'under "food & forestry" (waste is not food or forestry), no combustion CH4 (no factors in legacy). v0.3.12 '
     'replicates the allocation and adds the combustion CH4 of each sector (GAINS factors, section 14), with all '
     'fossil fuel supply methane (extraction, downstream gas, coal mining, biomass) under "other".',
     'Methods, chapter Emissions; CAVEATS v0.3.12'),
    ('I36', 'Effective carbon rate counts VAT and subsidies', 'Legacy\'s effective carbon rate (row 16647) and total '
     'carbon price (F5d) divide revenue net of subsidies, VAT included, by CO2; the OECD effective carbon rate counts '
     'carbon taxes, fuel excises and permit prices only. The prototype replicates the legacy definition (section 17, v0.3.15) '
     'and says so in the note; Egypt has negative rates (subsidies exceed taxes).', 'Methods, chapter Macro and results; '
     'CAVEATS v0.3.15'),
    ('I93', 'Primary energy of renewables: efficiencies not exactly 1', 'Legacy power data give wind, solar and hydro '
     'efficiencies of 1.004, 1.026 and 0.937, so their primary energy (generation / efficiency) differs from the '
     'physical energy content convention (1); solar shows more output than input. It enters total primary energy '
     'supply (Kaya, v0.3.18) and the power fuel totals; about 0.1% of TPES for Egypt.', 'Methods, chapter Macro and results'),
    ('I94', 'Legacy\'s stored run: wind and solar capex time factors 2039-2041 differ from its Power tab', 'Legacy '
     'Mitigation reads the capital cost time factors of wind and solar from the Power tab; its cached values for '
     '2039-2041 (wind 0.920, 0.915, 0.909) disagree with the cached Power cells they reference (0.923, 0.920, 0.918), '
     'apparently a stale cache in the distributed file. Since v0.4.7 the prototype computes the factors from the Power tab by '
     'formula, so its power results (new capacity and investment of solar, wind and gas, then power fuel use and emissions) depart from '
     'legacy\'s stored run from 2039; nothing changes before 2039.', 'Methods, chapter Data tabs; CAVEATS v0.4.7'),
    ('I39', 'VAT on oil products charged on the household share only (replicated v0.4.12)', 'Legacy multiplies the VAT '
     'rate of gasoline, diesel, LPG and kerosene by the household share of the product (sheet OilProductShares; Egypt: '
     'gasoline 1, diesel 0.03, LPG 0.99, kerosene 0.39), on the view that firms reclaim VAT. The share is one value for '
     'all sectors, so household diesel is under-taxed and firms\' gasoline over-taxed; road diesel of households is '
     'small, so the effect is mainly on gasoline. Replicated in v0.4.12 (LD5; user 2026-10-18: an issue, not a bug).',
     'Methods, chapter Prices 5; LegacyDiff'),
    ('I41', 'GDP effects: the impulse is the change in revenue over this year\'s GDP (replicated v0.4.15)', 'Legacy '
     'row 14341 takes the yearly change of the revenue gain in USD over the current GDP, not the change of the gain as '
     'a share of GDP: with GDP growing, a constant share of GDP keeps giving impulses (Egypt: impulses sum to 4.9% of '
     'GDP against a final fiscal space of 3.5%). Replicated in v0.4.15 (user 2026-10-18: replicate legacy, note issues).',
     'Methods, chapter Macro and results; LegacyDiff'),
    ('I42', 'GDP effects: impulses only from GDPStartYear (replicated v0.4.15)', 'Legacy cohorts start in GDPStartYear '
     '(MTInputs row 236, Egypt 2025): revenue gained before it never acts on GDP, and the first cohort holds only the '
     'change of that year. Replicated in v0.4.15 (impulse 0 before GDPStartYear).', 'Methods, chapter Macro and results'),
    ('I43', 'GDP effects: revenue uses 0 before the carbon price starts (not replicated)', 'Legacy rows 96-100 set '
     'the revenue-use shares to 0 before CPIntro, so an impulse of those years counts only as an excise drag. The '
     'prototype applies the shares in every year (per-cohort shares would need one share row per cohort). Tiny for Egypt '
     '(the revenue gain before CPIntro is nearly 0).', 'Methods, chapter Macro and results'),
    ('I44', 'Multipliers: the income-group spread added to manual and country multipliers (replicated v0.4.15)',
     'Legacy Low / High (FmAdj) adds -/+ the standard deviation of the income group to every source, also to manual '
     'and country-estimated multipliers. Replicated in v0.4.15 (Inputs_mult est and man columns).', 'Methods, chapter Macro and results'),
    ('I45', 'Multipliers: excise estimates from the "Excise tax" table (replicated v0.4.15)', 'Legacy maps the energy '
     'excise instrument (EXC) to the "Excise tax" country table (rows 614-812); the "Fuel tax" table (rows 210-408) is '
     'never used. Replicated in v0.4.15.', 'Methods, chapter Macro and results'),
    ('I46', 'Revenue by policy: transport and renewable subsidies not modelled', 'Legacy total revenue (row 8012) '
     'includes the transport revenues of the engineer road model (customs and VAT on vehicles, feebates, vehicle and '
     'charging subsidies, distance tax; rows 7899-7985) and the renewable subsidy cost (from the elasticity power '
     'model even where the engineer model is used, rows 7882-7890). The prototype 12e block has both rows at 0 (road '
     'engineer revenues parked; no renewable subsidy policy). Egypt: transport +0.04 bn in 2030 against baseline.',
     'LegacyDiff 37'),
    ('I47', 'GDP effects: methane fee in the fiscal space on the scenario\'s own activity', 'Legacy counts the methane fee in total '
     'revenue (row 8010) and so in the fiscal space, on the scenario\'s own activity; the prototype does the same since v0.9.0 (user 2026-10-29). Before (v0.6.2-v0.8.5), the prototype counted it with the '
     'stored scenario-1 activity of downstream gas and biomass use (v0.6.2, user decision 2026-10-20: no vulnerability '
     'to circular references through the GDP feedback). Differs from legacy only when a policy changes gas or biomass '
     'use and a methane fee applies. None for Egypt (no methane fee in the scenarios).',
     'Methods, chapter Macro and results; LegacyDiff 55'),
    ('I48', 'Price-control phase-out uses the consumer subsidy share (replicated v0.4.16)', 'Legacy rows 2216-2217 take '
     'the floor and slope of the price-control factor from the consumer subsidy share (I2201): there is no '
     'price-control share, and a baseline price-control phase-out (share 0) has no effect. The phase-out also scales a '
     'floating tax, not only a floating subsidy. Replicated in v0.4.16 (po.sh.pc).', 'Methods, chapter Prices 6'),
    ('I49', 'Producer subsidies spread over world or domestic demand, in the supply cost (replicated v0.9.0)', 'Legacy '
     'spreads a producer subsidy over world demand (oil) or half world, half domestic demand (coal, gas), and over '
     'domestic use (biomass): the per-unit subsidy is then near zero for oil, coal and gas, and enters the supply cost '
     '(the pass-through share reaches retail; the price controls absorb the rest). The prototype does the same since '
     'v0.9.0 (R7: psu x psf, block row psp in the supply cost; fiscal line rpsu); electricity producer subsidies enter '
     'the power price before policies (pseu, R7.5-R7.9). None for Egypt (data 0).',
     'Methods, chapter Prices 6'),
    ('I54', 'PPAs: phase-out switch only on the exact text "Yes*"; share to phase out typed 1', 'Q2190 = IF(Q2189 = "Yes*", 1, 0): a plain "Yes" means no phase-out; the share of PPAs to phase out is typed 1 (Mitigation Q2190, Q2193, row 2218). Replicated with Yes or Yes* (LEFT 3), share 1.', 'Methods, chapter Power; LegacyDiff 75'),   # v0.5.4
    ('I55', 'Renewable subsidies: nominal inputs used as real', 'MTInputs 352-353 are labelled $/kWh nominal and enter the real cost and revenue without deflation (Mitigation row 2743). Replicated (rows rnsp, rns).', 'Methods, chapter Power; LegacyDiff 76'),   # v0.5.4
    ('I56', 'Electricity excise: base-year grid intensity of the energy balance', "The excise per kWh = CO2 of the fuel input to power / power output of the base-year balance x carbon price, the same intensity in every year and scenario (Mitigation C2253, row 2253). Replicated (row exs, PwGInt) with the prototype's calibrated power EFs.", 'Methods, chapter Power; LegacyDiff 77'),   # v0.5.4
    ('I57', 'Final deficit to gas: a typed switch outside MTInputs', 'The switch is a typed cell (Mitigation E4248, No), global. Replicated as a global switch on Settings C45 (PwDeficitGas, default No).', 'Methods, chapter Power; LegacyDiff 78'),   # v0.5.4
    ('I58', 'Power switches tested for the exact "Yes"', 'PowerRebates (G261), RenewableSubsidyHydro (row 3150) and AdditionalExcise (F201) count a starred "Yes*" as No. The prototype accepts Yes or Yes* (LEFT 3), as I54 and the other prototype switches.', 'Methods, chapter Power; LegacyDiff 77'),   # v0.5.4
    ('I59', 'Electricity fuel price reform not applied to electricity prices (not replicated yet)', 'Legacy adds the electricity fuel price reform (MTInputs 148/162) to the excise (row 216); the prototype computes fpr.ecy but does not apply it to the electricity price.', 'Methods, chapter Power'),   # v0.5.4
    ('I60', 'End-user electricity price not floored at MinPostSubsidyPowerPrice (not replicated yet)', 'Legacy floors the end-user electricity price at MinPostSubsidyPowerPrice (rows 3617, 3646); the prototype has no floor (MinPostSubsidyPowerPrice is read per scenario since v0.5.4 but used only where legacy uses it in the cost side).', 'Methods, chapter Power'),   # v0.5.4
    ('I61', 'Engineer road model: follow-ups parked', 'The engineer road model (v0.3.5) replicates legacy with its bugs fixed (L25-L41), '
     'but its follow-ups are parked (user 2026-10-18: too many issues, not to be fixed now): review of the engineer run in Excel (TrModel), '
     'a goal seek to re-solve range anxiety for the corrected model (LD63; Egypt 2025 passenger EV sales share 0.09% vs 0.15% actual), '
     'the elasticity branch of road biofuels (LD62) and vehicle revenues in 12b. The default run uses the elasticity road model, as legacy.',
     'Methods, chapter Transport; TODO'),   # user 2026-10-19
    ('I62', 'Fuel use: no partial-adjustment model', 'Fuel use responds to prices and income with constant long-run elasticities, '
     'as legacy, with no partial (lagged) adjustment, so the full response comes in the year of the price change. Parked by the user '
     '(2026-10-09); was upgrade U12.', 'Methods, chapter Prices; TODO'),   # user 2026-10-19
    ('I63', 'Demand responds to real USD prices, not real local-currency prices', 'As legacy, fuel and electricity demand respond '
     'to prices in real USD. Under a devaluation the two diverge (Egypt gasoline 2022-2024: about -15% in real EGP against -42% in '
     'real USD), so demand responds to a price fall households do not see. Parked by the user (2026-10-09); related to I89 and U3.',
     'Methods, chapter Prices; TODO'),   # user 2026-10-19
    ('I98', 'Combustion emission factors: GAINS base and final factors only', 'Legacy 465 builds every combustion '
     'emission factor (local pollutants; the prototype also combustion CH4) as a line from the GAINS base factor (sheet '
     'EF_PM, FE in) in the base year to the final factor of switch EFSel in 2039 (Constant: FE in; Variable: FE fin; '
     'Average, the default: their mean), extrapolated after 2039 (Mitigation rows 1052-1663, columns L, AC, AD-AE). The '
     'yearly GAINS paths are not used. Until v0.8.4 the prototype ended at FE fin and stayed flat (data bug DB1, which '
     'wrongly said legacy reads zero paths); v0.8.5 aligns it with legacy (EFFinShare, EFWEIGHT, NONCO2).',
     'Methods, chapter Emissions'),
    ('I97', 'Blank VAT cells in the IMF price dataset', 'Some VAT cells of the IMF price dataset are blank; legacy '
     'reads a blank as 0 (bug L170, with its cell plan). The prototype fixes the bug: a blank takes the general VAT '
     'rate (VAT_WEO) for residential coal and gas and the oil products, 0 for power, industry and biomass. The data '
     'problem stays: which blanks are missing values.', 'Legacy_CPAT_Bugs (L170); Methods, chapter Prices'),
    ('L169', 'Intensity NDC: China CO2 hard-coded', "Legacy row 18449 H uses 5665 (Mt CO2) for China instead of the data (row 889). The prototype reads sheet GHGHist (or the model where the reference year is modelled); China's latest NDC is a Historical target (ref 2024, modelled), so the value is not used.", 'Methods, chapter Emissions'),   # v0.5.7
    ('I95', 'NDC reference years outside the data', 'Historical emissions (sheet GHGHist, legacy GHGs rows 954-1189) cover 1990, 2000, 2005, 2007, 2010, 2013, 2014 and 2017 (CO2 to 2020); real GDP (WEO) starts later. A Historical or Intensity NDC with another reference year, or an Intensity NDC with an early reference year (India 2005), gives N/A (legacy #N/A or a wrong cell, L123). Data to extend when the NDC module is used.', 'Methods, chapter Emissions'),   # v0.5.7
    ('I69', 'Air-pollution co-benefits (health, mortality) not built', 'Legacy computes air-pollution mortality and its valuation from fuel use (sheets AP and the Mitigation co-benefit rows). The prototype keeps local pollutant emissions (section 15) only. Dropped by the user (2026-10-20); the plan stays for reference.', 'excel_ai/plans/Air_pollution.md'),   # v0.6.1
    ('I70', 'Transport externalities (congestion, accidents, road damage) not built', 'Legacy values the transport externalities of road fuel use and vehicle-km. Not in the prototype. Dropped by the user (2026-10-20); the plan stays for reference.', 'excel_ai/plans/Transport_cobenefits.md'),   # v0.6.1
    ('I71', 'Fuel use grows with total GDP: population gets the income elasticity', 'Legacy updates fuel use each year with GDP growth raised to the income elasticity (x the income factor), next to the price and efficiency terms (CPAT equation 3.3.3; legacy row 2433). Total GDP growth mixes per-capita income growth with population growth, so population growth acts through the income elasticity (typically below 1) instead of an exponent of about 1, and its effect is entangled with the price elasticities in the same multiplicative update. Replicated as legacy. High priority (user 2026-10-20).', 'Equations.md E53-E56; Methods, chapter Prices'),   # v0.6.2
    ('I72', 'GDP feedback timing: same-year effects must never reach same-year demand', 'Legacy and the prototype let revenue of year t move GDP only from year t+1 (legacy row 8761 reads the previous column; prototype gdp.lvl = 1 + last year\'s gdp.eff), and the fiscal space reads revenue of year t only. This lag is what keeps the model free of circular references whatever the revenue lines read; it is not stated anywhere. Recommendation to the CPAT team: make it an explicit rule of the method and keep it when the GDP block changes. Replicated.', 'Methods, chapter Macro and results; NORMS (circular references)'),   # v0.6.2
    ('I73', 'Scenario-1 lookups must end at the current column', 'Lookups of the scenario-1 value of the same year (INDEX over a row, MATCH on the year) must not range over later columns: in a recalculation that evaluates the range, a lookup over the whole row reads its own scenario\'s later years and closes a circular reference (the prototype had one such row, ener.ref, fixed in v0.6.2; all others end at the current column). Recommendation to the CPAT team: check the legacy lookups the same way.', 'NORMS (circular references)'),   # v0.6.2
    ('I74', 'Methane calibration bases must be data or base-year values', 'Source allocations and intensities of the methane fee must be calibrated on data or base-year activity, never on a later model year: legacy read GHGYear (2024) activity in the earlier years, a read of later years that becomes circular as soon as the fee revenue feeds the GDP effects. The prototype uses data activity since v0.6.0 and, for the fiscal space, the stored scenario-1 gas and biomass activity (I47). Recommendation to the CPAT team.', 'Methods, chapter Emissions'),   # v0.6.2
    ('I75', 'Legacy code inconsistencies (CPAT code protocol)', 'Legacy codes do not follow one protocol: variable names differ by module (trevst vs stockcalc), slots differ in order (fuel.sector and sector.fuel), totals are written all or tot, model letters (.e, .a, .t) end some codes. The prototype follows the protocol from v0.7.2 (codes R0-R9: legacy variable names, sector before fuel, tot for totals, no model letters); legacy codes that differ are aliases in the crosswalk.', 'Codes_Remediation_Plan_v0_7_1.md; codes_crosswalk_v0_7_1.csv; code_renames_v0_7_2.csv'),   # v0.7.2
    ('I66', 'Fuel production for supply methane held at the base year (not replicated)', 'Legacy grows crude oil, natural gas and coal production (rows 6132-6135) from 2024 with the producer-price response to the methane fee (rows 6123-6130: price increase x pass-through, Manual inputs J190:J194 elasticities) and the growth of world demand of the global demand scenario (Prices_int rows 323-333, lagged one year). The prototype holds production at the base year (rows ch4.act og, cm). Found 2026-10-19 checking I26.', 'Methods, chapter Emissions'),   # v0.5.6
    ('I52', 'ETS inclusion: construction, fuel transformation and other energy use follow the buildings flag', 'Manual inputs V11:X11 read Dashboard Q30 (buildings) for construction, fuel transformation and other energy use: a grouping choice. The prototype types ETS coverage per scenario (MTInputs rows 99-115).', 'Manual inputs survey (v0.5.2)'),
    ('I53', 'Manual domestic prices switch on only with a 2021 value', 'A manual price row is "Manual" only if its 2021 value is filled (Mitigation F765:F829 test K$764); years without a value fall back to the data year by year. Could be a bug (intent unclear). Replicated since v0.9.0 (R8.1-R8.2, Inputs_prices MPU; I139).', 'Manual inputs survey (v0.5.2)'),
    ('I50', 'Residential LPG and kerosene always exempted: all new policy removed (replicated v0.5.1)', 'AlwaysExemptResLPGKer (MTInputs 268, per scenario) removes the carbon tax, the ETS and the new excise with their VAT from the residential LPG and kerosene price (legacy rows 5546-5547); the shadow price is kept, and ETS-covered emissions still count the fuels.', 'Methods, chapter Prices 5; LegacyDiff 66'),
    ('I51', 'Residential leakage: the fossil change is efficiency-weighted (replicated v0.5.1)', 'dF = -F x e_m x p, as legacy (p read as a share of useful energy). The alternative dF = -F x p is equally defensible (Egypt, $20 scenario, 2027: about -45 ktoe LPG and +127 ktoe biomass instead of -25 and +71).', 'Equations.md 4a; LegacyDiff 65'),
    ('I40', 'Road biofuels: feebate CO2 per liter scaled by the fossil share (replicated v0.4.12)', 'Legacy scales the '
     'CO2 per liter of gasoline and diesel in the vehicle feebate by the fossil share of road gasoline + bioethanol and '
     'diesel + biodiesel (E2146:E2147), as if the model\'s liters were blends; but road gasoline and diesel exclude '
     'the biofuels, which follow them as separate rows (5436-5438). Where biofuels are blended the feebate per liter '
     'is lower than the CO2 of the fossil liter. Replicated in v0.4.12 (LD62; user 2026-10-18). None for Egypt.',
     'Methods, chapter Transport; LegacyDiff'),
]

# v0.3.7: severity and status of each issue (excel_ai/BUGS.md, ISSUES.md). Major = changes results against
# legacy or blocks use; status: Open (action needed), Accepted (a decided departure or limitation), Resolved.
# v0.3.7 (user rule 2026-10-15): bugs are never replicated, issues are replicated (the prototype matches legacy) and tracked.
# Legacy side of each issue: 'replicated' (the prototype does what legacy does), 'not replicated' (a departure from legacy
# that is not a bug fix: an exception, kept only by user decision, else queued to replicate), 'mvp' (the prototype's own
# issue, no legacy counterpart). Lists: excel_ai/ISSUES.md, BUGS.md.
ISSUE_LEGACY = {
    'I1': 'mvp', 'I2': 'mvp', 'I3': 'mvp', 'I89': 'replicated', 'I5': 'mvp', 'I6': 'not replicated',
'I9': 'mvp', 'I10': 'mvp', 'I11': 'mvp', 'I12': 'mvp', 'I90': 'mvp',
    'I14': 'not replicated', 'I15': 'mvp', 'I16': 'mvp', 'I91': 'replicated', 'I18': 'replicated',
    'I19': 'replicated', 'I99': 'not replicated', 'I21': 'replicated', 'I92': 'replicated',
'I25': 'replicated', 'I26': 'replicated',
    'I28': 'replicated', 'I29': 'mvp', 'I30': 'mvp', 'I31': 'replicated',
    'I32': 'replicated', 'I33': 'mvp', 'I34': 'replicated', 'I36': 'replicated', 'I93': 'replicated',
    'I94': 'replicated', 'I39': 'replicated', 'I40': 'replicated', 'I41': 'replicated', 'I42': 'replicated',
    'I43': 'replicated', 'I44': 'replicated', 'I45': 'replicated', 'I46': 'replicated', 'I47': 'not replicated',
    'I48': 'replicated', 'I49': 'replicated', 'I50': 'replicated', 'I51': 'replicated', 'I52': 'not replicated', 'I53': 'not replicated', 'I54': 'replicated', 'I55': 'replicated', 'I56': 'replicated', 'I57': 'replicated', 'I58': 'not replicated', 'I59': 'replicated', 'I60': 'replicated', 'I61': 'replicated', 'I62': 'replicated', 'I63': 'replicated', 'I98': 'not replicated', 'I97': 'not replicated', 'I66': 'replicated', 'L169': 'not replicated', 'I95': 'replicated', 'I69': 'not replicated', 'I70': 'not replicated', 'I71': 'replicated', 'I72': 'replicated', 'I73': 'mvp', 'I74': 'mvp', 'I75': 'not replicated'}
LD_REPLICATED = {64}   # LegacyDiff rows of a departure type that in fact keep legacy (64: kept as legacy; 36 relabelled Same in v0.4.15)
BUGS_REPLICATED = set()   # legacy bugs the prototype still copies (status "Kept as legacy"): none since v0.4.10 (rule 2026-10-15)

ISSUE_STATUS = {  # id: (severity, status, next step to stay close to legacy or to close the issue)
    'I1': ('Major', 'Open', 'Review in Excel 365 (TODO).'),
    'I2': ('Minor', 'Accepted', ''), 'I3': ('Minor', 'Accepted', ''),
    'I89': ('Major', 'Accepted', 'Decided 2026-10-15: 2022 as legacy.'),
    'I5': ('Minor', 'Accepted', ''), 'I6': ('Minor', 'Accepted', 'Exception by decision (v0.2.4): sign convention only, values as legacy.'),
'I9': ('Minor', 'Accepted', ''), 'I10': ('Minor', 'Accepted', ''),
    'I11': ('Minor', 'Accepted', ''), 'I12': ('Minor', 'Accepted', ''),
    'I90': ('Major', 'Open', 'Data for other countries (TODO).'),
    'I14': ('Major', 'Accepted', 'v0.5.7: I25 closed (v0.5.6); the remaining distance is the documented data and bug-fix differences (legacy_comparison, LegacyDiff).'),
    'I15': ('Minor', 'Accepted', ''), 'I16': ('Minor', 'Accepted', ''),
    'I91': ('Major', 'Accepted', 'Decided 2026-10-15: calibrate to 2024 as legacy.'),
    'I18': ('Minor', 'Resolved', 'v0.3.2 (switch, off by default as legacy since v0.3.4).'),
    'I19': ('Major', 'Resolved', 'v0.3.11.'),
    'I99': ('Major', 'Accepted', 'Exception by user decision (corrected data, 2026-10-09).'),
    'I21': ('Major', 'Accepted', 'v0.4.15 (user 2026-10-18): benchmarks = 1 - the MTInputs auctioned share (rows 90-91, '
                                 'one share for all sectors, as legacy); benchmarks by sector later.'),
    'I92': ('Major', 'Accepted', 'Replicated v0.3.11; source of the values to trace.'),
    'I25': ('Major', 'Resolved', 'Traced (v0.5.6): legacy process emissions = 2023 inventory x the year-on-year growth of industrial energy CO2 (row 6576; 2024: +16.8%, the rebound after the 2023 demand shock, so 56.9 -> 66.5). The prototype floored that growth at 0 (a departure: removed in v0.5.6, as legacy). The remaining gap is the industrial energy CO2 path, part of the fuel-use gap (I14).'),
    'I26': ('Minor', 'Resolved', 'Checked (v0.5.6): energy N2O moves with energy CO2 as legacy (row 7549 = previous x CO2 ratio). Production for fuel-supply methane differs: now issue I66.'),
    'L169': ('Minor', 'Accepted', 'v0.5.7: no hard-coded value; data or model (departure by design, user rule: data not typed).'),
    'I95': ('Minor', 'Open', 'v0.5.7: GDP solved (WEO NGDP_R, 2000-2040). v0.6.1: reference years 2021-2024 read the GHGs inventory (rows ndc.hc, ndc.hv), 2022 onwards the model. Still open: historical GHGs 2018-2020 (GHGHist ends 2017, CO2 2020): data request.'),
    'I69': ('Major', 'Dropped', 'Module dropped by the user (2026-10-20); plan kept for reference.'),
    'I70': ('Major', 'Dropped', 'Module dropped by the user (2026-10-20); plan kept for reference.'),
    'I71': ('Major', 'Accepted', 'Legacy issue, not a bug: high priority for the CPAT team, not for the prototype (user 2026-10-20); replicated as legacy. Recommendation: split the driver: fuel use x (1 + population growth)^1 x (1 + per-capita income growth)^income elasticity, keeping the price and efficiency terms separate; switch off = legacy.'),
    'I72': ('Major', 'Resolved', 'Stated as a rule (user 2026-10-20): Methods, chapter Macro and results section Timing rule and NORMS (circular references): revenue of year t moves GDP only from year t+1, the fiscal space reads revenue of year t only, and no same-year GDP effect reaches same-year demand. Recommendation to the CPAT team: state it in the legacy method too.'),
    'I73': ('Major', 'Resolved', 'Legacy checked (v0.6.2 scan of every Mitigation formula for reads of later years): no scenario-1 lookup over whole rows (the policy block reads the baseline block in the same column); the cost breakdown (rows 3509-3517) reads the user\'s CostBreakdownYear, a report only; the net revenue report rows read the next year: legacy bug L128. prototype: every lookup ends at the current column (ener.ref fixed in v0.6.2); the quick check tests reads of later years.'),
    'I74': ('Major', 'Resolved', 'Legacy checked: no bug. The source allocation uses energy-balance data (row 894) and the energy CH4 calibration (row 7548) uses the first two years and applies the factor from the third (it reads only earlier years). The prototype calibrated on GHGYear (2024) in every year (its own design) and now reads stored scenario-1 values; the fiscal space uses the stored scenario-1 activity (I47).'),
    'I75': ('Minor', 'Resolved', 'v0.7.2 (codes R0-R9): the prototype codes follow the protocol; legacy codes that differ are aliases (crosswalk, LiveOutputs alias column). Open review rows: excel_ai/plans/TODO_Codes.md.'),
    'I66': ('Major', 'Resolved', 'Replicated in v0.5.6: rows ch4.wd, ch4.fk, ch4.pi, ch4.prd (inventory-year activity = base production, to avoid a loop; legacy holds 2022-2023 at the base anyway). Note: legacy CHOOSE reads the Net Zero row for the third and fourth demand scenarios.'),
    'I28': ('Minor', 'Dropped', 'Parked, then dropped by the user (2026-10-20).'),
    'I29': ('Minor', 'Resolved', 'v0.3.7: LAMBDAs renamed; confirm in Excel (quick check on Windows).'),
    'I31': ('Major', 'Accepted', 'v0.4.15 (user 2026-10-18): legacy averages are the default (pav.leg, pav.lidx, pav.idx; '
                                 'Settings C54 Legacy*), the Laspeyres index kept as an option.'),
    'I32': ('Major', 'Accepted', 'Replicated in v0.4.11 (user 2026-10-18: go with legacy); the inventory break (I91) stays in the factor, as legacy.'),
    'I33': ('Minor', 'Resolved', 'v0.5.7: extract_data writes LF line ends and runs update_prices_egypt after the price extraction, so the corrected Egypt block is kept.'),
    'I34': ('Minor', 'Accepted', 'As legacy (v0.3.12); to confirm: combustion CH4 added, all fuel supply methane under other.'),
    'I36': ('Minor', 'Accepted', 'As legacy (v0.3.15); an OECD-style rate (carbon taxes, excises, permits) could be added as a memo.'),
    'I93': ('Minor', 'Accepted', 'As legacy (v0.3.18); set the renewable efficiencies to 1 if the data are confirmed.'),
    'I94': ('Minor', 'Accepted', 'v0.4.7: the formula follows the Power tab; recheck against a fresh legacy run.'),
    'I39': ('Minor', 'Accepted', 'Replicated v0.4.12 (user 2026-10-18); a share by sector would need data by sector.'),
    'I40': ('Minor', 'Accepted', 'Replicated v0.4.12 (user 2026-10-18); revisit if road fuels are modelled as blends.'),
    'I41': ('Major', 'Accepted', 'Replicated v0.4.15 (user 2026-10-18); the prototype form (change of the GDP share) is one line.'),
    'I42': ('Minor', 'Accepted', 'Replicated v0.4.15.'),
    'I43': ('Minor', 'Resolved', 'Replicated v0.5.7: rows fis.impp and fis.lagp (impulse 0 before CPIntro) feed every revenue use but the excise drag, as legacy rows 96-100.'),
    'I44': ('Minor', 'Accepted', 'Replicated v0.4.15.'), 'I45': ('Minor', 'Accepted', 'Replicated v0.4.15.'),
    'I46': ('Major', 'Resolved', 'Renewable subsidies: in the power model since v0.5.4 (prrns), counted in rsub, rtot and block 12e row rpol.ren, as legacy rows 7882-7890. Transport revenues: dropped with the engineer road model (I61, user 2026-10-20); row rpol.trs stays 0.'),
    'I47': ('Minor', 'Accepted', 'v0.6.2 (user 2026-10-20: as close to legacy as possible with no vulnerability to circular references): the fee revenue is in the fiscal space (fis.rev + ch4.revf). ch4.revf is the legacy fee revenue with the stored scenario-1 activity of downstream gas and biomass use (sheet BaselineCO2 rows dg, bm, refreshed by the build; check row ch4bs.chk = 0 in scenario 1); fee, abatement and the other sources are the scenario\'s own. So the fiscal space reads no fuel use, and no later change to the power or demand blocks can close a loop through it. Reported revenue (rmf, rtot, 12e) keeps the own activity. The v0.6.0-v0.6.1 loop came from price-block average ranges that ran into section 11 (fixed v0.6.2), not from the L67 fix. No effect in the shipped scenarios (no methane fee).'),
    'I48': ('Minor', 'Accepted', 'Replicated v0.4.16; a price-control share would need an MTInputs row.'),
    'I50': ('Minor', 'Accepted', 'None (as legacy).'),
    'I54': ('Minor', 'Accepted', 'None (user decision 2026-10-18).'),
    'I55': ('Minor', 'Resolved', 'Reclassified as legacy bug L114 (user 2026-10-19).'),
    'I56': ('Minor', 'Accepted', 'Decided (user 2026-10-19): legacy kept (base-year intensity); the yearly intensity would be an upgrade.'),
    'I57': ('Minor', 'Accepted', 'None (user decision: Settings, as legacy).'),
    'I58': ('Minor', 'Resolved', 'Reclassified as legacy bug L113 (user 2026-10-19).'),
    'I59': ('Minor', 'Resolved', 'Replicated in v0.5.6: the electricity fuel price reform path enters the excise of policy scenarios (row entx).'),
    'I60': ('Minor', 'Resolved', 'Replicated in v0.5.6: end-user electricity prices floored at MinPostSubsidyPowerPrice (row rp).'),
    'I61': ('Major', 'Dropped', 'Parked, then dropped by the user (2026-10-20).'),
    'I62': ('Major', 'Accepted', 'Legacy issue, not a bug: high priority for the CPAT team, not for the prototype (user 2026-10-20); replicated as legacy. Recommendation: add a partial-adjustment option: fuel use moves a share of the way to its long-run level each year (short-run and long-run elasticities), as an upgrade over legacy, switch off = legacy.'),
    'I98': ('Major', 'Open', 'prototype fill kept (user 2026-10-19). Data request: a legacy file with the GAINS combustion factor paths (high priority, user 2026-10-19).'),
    'I97': ('Major', 'Open', 'prototype fill kept (user 2026-10-19). Data request: raise the blank VAT cells with the data team (high priority, user 2026-10-19); the prototype fill stays until then.'),
    'I63': ('Major', 'Dropped', 'Parked, then dropped by the user (2026-10-20).'),
    'I52': ('Minor', 'Accepted', 'Conditional: nothing to replicate now (the prototype types ETS coverage per sector). Decided (user 2026-10-19): replicate the legacy grouping when ETS coverage by Dashboard groups is built.'),
    'I53': ('Minor', 'Accepted', 'Conditional: nothing to replicate now (the prototype does not build manual domestic prices). Decided (user 2026-10-19): an issue; replicate legacy when manual domestic prices are built; ask the CPAT team about the intent.'),
    'I51': ('Minor', 'Accepted', 'Decided (user 2026-10-19): keep the efficiency weighting, as legacy.'),
    'I49': ('Minor', 'Resolved', 'v0.6.1: replicated: rows psd (demand: world oil; half world, half domestic coal and gas; domestic biomass), psu (existing subsidy per unit, held after the last price year) and block row psp ($/GJ) in the supply cost, as legacy rows 825-829, 2455-2708; legacy bugs L124, L125 fixed. v0.6.2 (user 2026-10-20: reforms separate from the before-tax build-up): the phase-out is the wedge ppsw = psr (= -psu x (1 - psf)) per GJ x pass-through, subsector line psw beside csw and pcw, VAT on it in rsr. Legacy puts it in the supply cost, where the price controls absorb (1 - pass-through) of it, so results equal legacy except where the excise floor binds. Electricity producer subsidies stay with the power model. Egypt: no data (0).'),
    'I30': ('Minor', 'Open', 'Tested separately by the user (2026-10-19); no goal-seek runs in builds or checks (NORMS 5). Last full check (v0.5.3): worst gap 0.0265 after 20 iterations.'),
}

UPGRADES = [  # id, title, description, priority
    ('U1', 'Review in Excel 365', 'The user runs the checklist (ExcelReview_Checklist.md) on Windows: CheckBatchRun, '
     'the batch run, ScenarioCompare, no repair prompt and no circular-reference warning (I1).', 'High'),
    ('U2', 'Numerical check against legacy CPAT for Egypt', 'Explain the distance to the legacy run (I14) '
     'sector by sector, on the latest legacy file (465; was 459).', 'High'),
    ('U4', 'Report the legacy bugs to the CPAT team', 'Send the register (L1-L128, D1-D31) and the cell-level fix '
     'plans; legacy issues for the team, high priority for them: I62 (partial adjustment), I71 (population takes the '
     'income elasticity), I72-I74 (circularity).', 'High'),
    ('U5', 'Copy-paste stress test', 'Add a fuel, a subsector and a scenario by dragging; fix what breaks.', 'Medium'),
    ('U6', 'Other gases, local pollutants and process emissions', 'CH4 and N2O done (v0.2.8), local pollutants (v0.2.9); inventory-adjusted EFs and process CO2 remain.',
     'Medium'),
    ('U7', 'Regulations as shadow prices', 'Fill the regulation rows (placeholder 0) and their efficiency-margin '
     'adjustments (MTInputs 247-250).', 'Medium'),
    ('U10', 'Data for more countries', 'Energy balances, GDP and EFs beyond Egypt (I90).', 'Medium'),
    ('U13', 'Planned retirement data for Egypt', 'Enter PowerPaths pret|<type> where plans exist.', 'Low'),
    ('U14', 'Python port', 'The check script already recomputes every value in Python.', 'Low'),
]

IMPROVEMENTS = [
    'One plain formula per block for 2022-2040, at most 100 characters, no LAMBDA support needed; the last year 2041 '
    'calls the named LAMBDA of every calculated row (sheet Lambdas lists them).',
    'Fuel prices for power and the levelised-cost window as legacy (moving average, horizon 2041).',
    'The second investment round (legacy tables L11-L17, about 60 rows) is one row: permit x MAX(0, MIN(space, '
    'deficit - space of cheaper types)); coal and gas dispatch (legacy I2, 19 rows) is five rows.',
    'Amortised and levelised fixed costs are one row per type each, with constants derived once in Inputs_power.',
    'Electricity prices are telescoped, so components held at their last historical value drop out.',
    'Power is part of the main thread: fuel use, revenues and CO2 enter the totals, and a new ETS that covers power '
    'sees power emissions.',
    'Every number is checked: a Python reference reproduces 208 legacy rows of the baseline and the carbon-tax run to '
    '1e-13 with the bugs switched on, and the workbook equals the reference with the bugs fixed.',
]

LD_TYPES = ('Not yet', 'Simplification', 'To check (bucket 5)')


def legacy_diff_items():
    """LegacyDiff rows of the types in LD_TYPES: (id, title, legacy, this model, effect, type)."""
    return [(f'LD{k}', d[0], d[1], d[2], d[4], d[5]) for k, d in enumerate(B.LEGACY_DIFFS, 1) if d[5] in LD_TYPES]


def items():
    """Every register item as (id, title, category)."""
    out = [(f'L{i + 1}', t, 'Legacy bug') for i, (_k, t, *_r) in enumerate(BUGS)]
    out += [(i, t, 'Legacy bug') for i, t, *_r in LEGACY]
    out += [(i, t, 'prototype bug (fixed)') for i, t, *_r in MVP_BUGS]
    out += [(i, t, 'Known issue') for i, t, *_r in ISSUES]
    out += [(i, t, 'Simplification / not yet') for i, t, *_r in legacy_diff_items()]
    out += [(i, t, 'Upgrade') for i, t, *_r in UPGRADES]
    return out


# ---------------------------------------------------------------- v0.8.4 (user 2026-10-28): one register for every module
# Codes by kind, the same in every module (NORMS 0; v0.8.5, user 2026-10-29): L legacy bug (fix = formulas, with a cell
# plan), M prototype bug, I issue (replicated, or a departure by user decision; priority Very high / Extremely high for
# data problems), LD LegacyDiff departure, U upgrade. The kinds DB (data bug) and DI (data issue) of v0.8.4 are retired.
# Renumbered (former codes kept in FORMER, every step listed): v0.8.4: distribution bugs D1-D31 -> L138-L168, the
# cell-plan finds N1, N2 -> L135, L136, distribution issues DI1-DI10 -> I76-I84 and DI8, I67 -> L169; v0.8.5: data
# issues DI1-DI8 -> I89-I96; data bug DB2 -> bug L170 (cell plan) and issue I97 (very high); DB1 -> issue I98
# (extremely high; the prototype aligned with legacy); DB3 -> issue I99 (departure by user decision).
FORMER = {'L135': 'N1', 'L136': 'N2', 'L169': 'I67',
          'I89': 'DI1 < I4', 'I90': 'DI2 < I13', 'I91': 'DI3 < I17', 'I92': 'DI4 < I22', 'I93': 'DI5 < I37',
          'I94': 'DI6 < I38', 'I95': 'DI7 < I68', 'I96': 'DI8 < distribution DI3',
          'I97': 'DB2 < I65', 'L170': 'DB2 < I65', 'I98': 'DB1 < I64', 'I99': 'DB3 < I20'}
FORMER.update({f'L{137 + n}': f'D{n}' for n in range(1, 32)})
FORMER.update({f'I{76 + i}': f'distribution DI{n}' for i, n in enumerate([1, 2, 4, 5, 6, 7, 8, 9, 10])})
DATA_ISSUES = {f'I{n}' for n in range(89, 100)}   # v0.8.5: the former data issues and data bugs (area: data)

INPUT_BUGS = [  # id, title, where, what legacy does, status in the prototype (module: Inputs, ScenarioDefinition)
    ('L137', 'MTInputs NameOfParameter: Dashboard names on 23 inputs, a trailing space on one',
     'MTInputs column H, rows 53-64 and 84-97 (D_ names), row 343 (ElasticityModel)',
     'Column H names 23 feebate and ETS inputs with the names of their Dashboard cells (D_FeebateIntro, '
     'D_Feb_Level_Start_Pow, D_NewETS, D_ETSIntro, ...): everywhere else D_<name> is the Dashboard cell and <name> the '
     'MTInputs value (213 of the 272 inputs have a D_ twin on the Dashboard). Row 343 reads "ElasticityModel " with a '
     'trailing space (Name Manager: ElasticityModel). A lookup by name finds the wrong cell or none.',
     'Fixed (v0.8.4): the prototype names drop the D_ prefix (FeebateIntro, NewETS, ETSIntro, ...) and the space; the '
     'legacy name is kept in the codes map (tab Inputs).')]

ISSUES += [
    ('I85', 'Percentages typed as whole numbers on 8 inputs', 'MTInputs rows 197-201 and 203-205 (revenue use '
     'EXPLabortax, EXPCIT, EXPCapex, EXPGoodsandserv, EXPTransfers; TargettedPercentile, CoverageRate, LeakageRate) '
     'hold 30 for 30%; every other percentage input holds a fraction (0.3). Replicated: the prototype keeps legacy\'s '
     'values and divides where legacy divides; the Python port keeps the same convention.',
     'Codes map, tab Inputs'),
    ('I86', 'Input names: spelling not uniform', 'Column H spells ShareofProdSubPha and ShareofConsSubPhaBA beside '
     'ShareOfConsSubPha and ShareOfProdSubPhaBA, FFPhaseOut for the consumer phase-out period, NDCTargetYear where '
     'the Name Manager has NDCtargetyear, and three cells carry a second name (Simple_CPATDefaultsOrUserDefined, '
     'EnergyPricesManualSwitch for DomPrTax, EngineerModeProportionOfCovidFactor). Replicated: the column H names are '
     'kept as they are (only bug L137 is corrected).', 'Codes map, tab Inputs'),
    ('I87', 'Inputs without a name', 'MTInputs rows 11, 12, 14, 15 (scenario identification), 66-82 (feebate sector '
     'coverage), 99-115 (ETS sector coverage), 117-121 (CBAM process goods) and 140-183 (fuel price reform) have no '
     'NameOfParameter, so they can be found only by row or by heading and label. Not replicated by user decision '
     '(2026-10-28: a complete set of names): the prototype names them (FbCovPow, ETSCovPow, CBAMProcMch, FprIntro, '
     'FprStartCoaPow, ...); values and rows as legacy.', 'Codes map, tab Inputs'),
    ('I88', 'One Dashboard cell feeds two inputs', 'D_ETSIntro and D_FeebateIntro both point to Dashboard D31 '
     '(D_ETSOutro and D_FeebateOutro to D32), D_ResSubstLPGEff and D_LPGEff to L147 (also kerosene, biomass, natural '
     'gas), D_PhaseOutCoalAndGasPPAs and its baseline twin to Q55: the Dashboard sets both MTInputs rows at once '
     '(their defaults differ: ETS 2026, feebates 2027). Replicated: ScenarioDefinition keeps the two rows, as MTInputs.',
     'Codes map, tab Inputs')]
ISSUE_LEGACY.update({'I85': 'replicated', 'I86': 'replicated', 'I87': 'not replicated', 'I88': 'replicated'})
ISSUE_STATUS.update({
    'I85': ('Minor', 'Accepted', 'Replicated (user 2026-10-28: the inconsistency is an issue).'),
    'I86': ('Minor', 'Accepted', 'Replicated.'),
    'I87': ('Minor', 'Accepted', 'Departure by user decision (2026-10-28); names in the codes map.'),
    'I88': ('Minor', 'Accepted', 'Replicated.')})

# v0.8.5 (user 2026-10-29): the data problems as issues, with their priority and plan
ISSUE_STATUS.update({
    'I97': ('Very high', 'Open', 'Plan: the data team says which blank VAT cells of the IMF price dataset are missing '
            'values and which are true zeros, and fills the dataset. Legacy: apply the cell plan of bug L170 (a blank '
            'reads the general VAT rate for the household fuels); the prototype has that fix. No effect for Egypt.'),
    'I98': ('Extremely high', 'Open', 'The prototype now does exactly what legacy 465 does (v0.8.5). Plan: get the GAINS '
            'factor paths by year (proprietary) or confirm that the base and final factors are the intended data; '
            'check the 2040-2041 extrapolation and the EFSel average with the CPAT team.'),
    'I99': ('Major', 'Accepted', 'Departure by user decision (2026-10-29: the prototype keeps the corrected Egypt '
            'prices). Plan: send the corrected block to the CPAT data team for the legacy Prices_dom table; when legacy '
            'carries it, the two read the same data and LD4, LD33 close.')})
ISSUE_LEGACY.update({'I97': 'not replicated', 'I98': 'replicated', 'I99': 'not replicated'})

# v0.8.5 (user 2026-10-29): transport co-benefits self-consistency, checked before the build of R1-R2
ISSUES += [
    ('I100', 'Transport co-benefits use the engineer road model whatever TrModel', 'Legacy computes accidents, '
     'congestion and road damage (Transport sheet, Mitigation block E rows 15724-15823) from the engineer road model\'s '
     'vehicle-km, freight vehicle-km, fuel economy and passenger/freight splits, even when TrModel = Elasticity (the '
     'default), while the road share of each fuel follows TrModel. The welfare change is then not consistent with the '
     'fuel use modelled: Egypt 2031, engineer vehicle-km -8.6% against road gasoline -12.9% and diesel -14.3% in the '
     'elasticity model. Replicated: the prototype computes section 5b in every scenario and reads it, as legacy.',
     'excel_ai/plans/Transport_cobenefits.md (section 1.3, issue I-a)')]
ISSUE_LEGACY.update({'I100': 'replicated'})
ISSUE_STATUS.update({'I100': ('Major', 'Accepted', 'Replicated (user 2026-10-29: match legacy). Plan for legacy: take '
                              'vehicle-km from the switched road fuel use when TrModel = Elasticity.')})

# v0.9.0 (user 2026-10-29): I47 reverted to legacy (the methane fee in the fiscal space on the scenario's own activity)
ISSUE_LEGACY.update({'I47': 'replicated'})
ISSUE_STATUS.update({'I47': ('Minor', 'Accepted', 'Replicated since v0.9.0 (user 2026-10-29): the fiscal space counts the '
                             'methane fee on the scenario\'s own activity, as legacy rows 8018-8025 (fis.rev + ch4.rev). '
                             'Every reference is to the same year and the GDP feedback lags one year, so there is no '
                             'circular reference (checked by a full recalculation). v0.6.2-v0.8.5 used the stored scenario-1 '
                             'gas and biomass activity (ch4.revf, now a memo row).')})

# v0.9.0 (user 2026-10-29): issues found while preparing the equations addendum (R1-R13 and the reverts to legacy),
# I101-I146. Snippet to append to issues_register.py (not imported yet). Legacy rows: legacy 465, sheet Mitigation
# unless stated (L = 2022 ... AE = 2041; scenario 2 = row + 6316). Bugs L171-L222: legacy/bugfixes/data/fixes_v0_9_0.json.
_NA = 'excel_ai/mitigation/Equations_addendum_notes.md (section A)'
_NB = 'excel_ai/mitigation/Equations_addendum_notes.md (section B)'
_NC = 'excel_ai/mitigation/Equations_addendum_notes.md (section C)'
_ND = 'excel_ai/mitigation/Equations_addendum_notes.md (section D)'
_NE = 'excel_ai/mitigation/Equations_addendum_notes.md (section E)'

ISSUES += [
    # A. Reverts to legacy and R13
    ('I101', 'Coal and gas margins read at a typed year (2024)', 'O747:O752 read the coal and gas margins at '
     '_Country_code & 2024 (typed), while the oil-product margins (O755:O758), the production cost and the '
     'domestic-production share read FirstYearCalculations. Replicated (user decision R13): Inputs_prices column mary '
     '= 2024 for coal and gas, the base year otherwise.', _NA),
    ('I102', 'Fuel price reform: strict target test; Percentage rate from the first-year step', 'Rows 167-180: the test '
     'is t < target (strict), and the Percentage rate K for a zero start price uses (H/(G+J))^(1/n) - 1 (growth from '
     'the first-year step). With the L171 fix the strict test has no effect. No effect for Egypt (no fuel price '
     'reform). Replicated.', _NA),
    ('I103', 'Feebates held at the target rate whatever ExtendCarbonPriceBeyondOutro', 'Rows 2001-2004 '
     '(IF(t>J1977,$J,...)): feebates stay constant at the target rate after the target year whatever '
     'ExtendCarbonPriceBeyondOutro says. No effect for Egypt (no feebates). Replicated (user decision LD10).', _NA),
    # B. R1 inputs from air pollution and transport co-benefits; R2 social costs and benefits
    ('I104', 'Air-pollution unit costs are average, not marginal, damages', 'The unit costs per fuel (F10 rows '
     '17738-17749 from the Air pollution sheet) use baseline deaths per ug/m3 (plan AP I-b): sum of cost x change in '
     'use = 0.322 bn in 2030 against legacy wel.air 0.057 bn (5.7 times). Kept as legacy for social costs, subsidies, '
     'FFS and efficient prices; the welfare uses v_PM (R1.4).', _NB),
    ('I105', 'wel.air linearised on one legacy policy run', 'The prototype types v_PM = legacy wel.air / change in '
     'PM2.5 of one policy run (AP 3217 / (AP 981 - AP 1814)); 2023-2026 come from a change of about 1.5e-4 ug/m3, so '
     'they are noisy (0.196-0.291). O3 deaths and YLD scale with PM2.5; household air pollution does not respond.',
     _NB),
    ('I106', 'Typed Egypt values freeze the AP and VSL options of the cached run', 'The air-pollution and VSL options '
     'of the cached legacy run (SourceAppSel = Manual-FASST in MTInputs F322 and Dashboard F429, VSL Transfer from '
     'Group, 3% discount, cessation lag Yes) are frozen in the typed tables T1-T4; ScenarioDefinition rows 322-336 stay '
     'grey (inert). Other countries need their own typed values (R1 issue of the plan).', _NB),
    ('I107', 'FFS lines: diesel valued at oil-product costs; global SCC; separate welfare', 'F10 rows 17767-17784: the '
     'FFS lines value diesel in industry, power and "other" at the oil-product climate and air-pollution costs; the '
     'gasoline and diesel road lines take the transport sector; FFS uses the global SCC; the FFS welfare is a separate '
     'measure, not in wel.usd. Replicated.', _NB),
    ('I108', 'Electricity externalities blank in the subsidy block', 'F10 rows 17920-17946: the electricity lines have '
     'no externalities, so the implicit electricity subsidy is the VAT gap only. Replicated.', _NB),
    ('I109', 'Subsidy-block VAT: general rate, household share only', 'The subsidy block applies the general VAT rate '
     '(the fuel-specific VAT rows 17790, 17802, 17813, 17824, 17835, 17855, 17892, 17929 are read but unused), on the '
     'household share only; none on industry and power. Replicated.', _NB),
    ('I110', 'Subsidies computed for scenario 1 only', 'Legacy computes the subsidies (rows 17786-17951) and the .1 '
     'unit costs for scenario 1 only. The prototype computes them in every scenario group (group 1 = legacy).', _NB),
    ('I111', 'Transport co-benefits: scenario-1 margins, fixed per-km costs, rectangle welfare', 'Vehicle-km from the '
     'engineer model whatever TrModel (I100); margins from scenario 1 (plan T I111); per-km costs '
     'scenario-independent, congestion not responding to policy (T I-b); the welfare is a rectangle, road damage only '
     'for freight, 0.12 USD/km not deflated (T I-d, I-h). Replicated.', _NB),
    ('I112', 'Air pollution horizon 2040: 2041 = 2040', 'The Air pollution sheet stops at 2040 (K..AC); the '
     'AP-derived typed values take 2041 = 2040 (plan AP I-o). Replicated.', _NB),
    # C. R3 Pigouvian taxes; R4 CBAM process emissions
    ('I113', 'Pigouvian netting: top-up over existing taxes; climate charged twice', 'With AddEfficientTaxes on, the '
     'whole new excise of the block (reform + manual excise + Pigouvian) becomes MIN(R, MAX(0, R - SUM(existing fixed '
     'tax, fixed subsidy, floating part, existing carbon tax, existing ETS))) (rows 8782-9012 O:AE): never below 0, '
     'never above R. The new carbon tax and ETS are not netted, so with ClimateEffTax = Yes* and a carbon tax the '
     'climate damage is charged twice. No effect for Egypt by default (AddEfficientTaxes No*). Replicated.', _NC),
    ('I114', 'Pigouvian phase-in anchored on CPIntro; applied in policy scenarios only', 'Row 146: the phase-in starts '
     'at CPIntro (carbon tax start), linear over AddEfficientTaxesPhaseInYears; computed in every scenario, applied '
     'only in policy scenarios ($C>1); ntx rows typed 0 for 2022-2024. Replicated.', _NC),
    ('I115', 'Pigouvian and efficient prices use different externality vintages', 'The Pigouvian tax (rows 128-133) '
     'uses baseline externalities (Transport mf.1, air pollution .1); the efficient prices (17965-17982) use transport '
     'mf.2 and air pollution .1. Replicated.', _NC),
    ('I116', 'Climate damage per unit: national SCC x generic EF', 'Rows 136-142 = 17678-17684: national SCC x a '
     'generic EF (IIASA average across 2-3 sectors, base-year column L, not the calibrated EF[f,s], not '
     'inventory-adjusted); the CO2-equivalent rows multiply by the global SCC (17959) and divide by the national '
     'damage. Replicated.', _NC),
    ('I117', 'One Pigouvian for all other oil products, at the power-plant AP cost', 'Row 123 ("Power") uses the oil '
     'power-plant air-pollution cost for every oop use; the industrial oop cost (17749, 23.4 $/GJ in 2022) is unused. '
     'Replicated.', _NC),
    ('I118', 'Road damage only for diesel', 'Row 132 and 17967 are empty ("No road damage externalities for '
     'gasoline"). Replicated.', _NC),
    ('I119', 'Electricity Pigouvian tax always 0', 'Rows 124-125 hold a formula only in K (2021) (=IFERROR(L18102,0), '
     '=IFERROR(L18090,0)); L:AE are blank, so L159:AE160 = 0 (checked in the cached run). Filling them would tax '
     'power-plant air pollution twice (already in the coal, gas and oil-for-power Pigouvian, rows 148, 151, 158). '
     'Proposed as bug Lnew-R1R2-18, classified as an issue. No effect by default (AddEfficientTaxes No*). Replicated '
     '(0); K124:K125 are dead cells.', _NC),
    ('I120', 'Efficient prices: VAT on consumer fuels only, 2022 rate, scenario-1 supply cost', 'Rows 17955-18123: '
     'potential VAT only on consumer fuels (oil products, residential coal, gas, electricity), typed 0 for industry and '
     'power; the general VAT rate of 2022 for all years ($E$17956 = L726, label "2018"); supply cost of scenario 1, '
     'retail price of the live scenario; computed for the live scenario only; no oop, no biomass. Replicated (the '
     'prototype computes it per scenario group).', _NC),
    ('I121', 'Electricity AP cost per kWh assumes a fixed 31% thermal efficiency', 'Row 18090 = generation-share-'
     'weighted fuel cost ($/GJ of fuel) x _conv_ktoe_to_gwh/1000 = 0.01163 GJ/kWh, i.e. a fixed 31% thermal '
     'efficiency, with the baseline generation mix in every scenario. Replicated in the efficient prices (R3.15).',
     _NC),
    ('I122', 'Exact switch texts; dead code cells I2202:I2203', 'F144 "Yes*", F200 "Yes", F17955 "No", I2203 "Yes*" '
     'are tested as exact texts that match their dropdowns; the prototype uses LEFT(x,3)="Yes" (L113 rule). '
     'I2202:I2203 (code for VAT optimal taxation) are dead. Replicated.', _NC),
    ('I123', 'CBAM block: Egypt only, no output read anywhere', 'Rows 5867-6022: typed 2024 production and prices '
     '(IF(_Country_code="EGY",...)), master switch Dashboard G20 (Manual inputs row 22), switch of the live scenario '
     'read by both blocks (shared rows 1832-1836); abatement uses the auctioned ETS price; product fuel CO2 is also in '
     'the energy model (memo rows only); no output is read by revenue, GHG totals, the ETS cap or MTOutputs. No effect '
     'for Egypt (CBAM off). Replicated; the link to totals is decision D-R4.', _NC),
    # D. R5 green public investment; R11 current account; R12 GVA and emissions intensity
    ('I124', 'Green investment: cumulative need uses 35 years, the phase-out 34', 'H6250 =H6227*(2060-2025): 35 years '
     'hard-coded, while the phase-out spans D6222 - D6221 = 34 years and reaches 0 in 2059. Replicated (35; step '
     '1/34).', _ND),
    ('I125', 'Green investment section stops at 2040', 'Section 10 (rows 6215-6267) covers K:AD (2021-2040), as the '
     'revenue allocation rows 2178-2184; 2041 is blank. Replicated (2041 blank).', _ND),
    ('I126', 'Green public investment is report only; constants typed in Mitigation', 'No cell outside section 10 '
     'reads it: it changes neither emissions nor GDP; its five parameters are typed in Mitigation D6219-D6224, not '
     'MTInputs. Replicated; constants on Settings, labelled legacy hard-coded.', _ND),
    ('I127', 'Green investment: #N/A for countries outside the CCDR list', 'Countries outside the CCDR list (ETS+LTS '
     'rows 261-302, 42 rows) get #N/A in D6218 and every row of section 10. Egypt is in the list. Replicated '
     '(IFERROR would be a departure).', _ND),
    ('I128', 'Green investment: annual GDP shares summed against a discounted ratio', 'The cumulative green investment '
     'sums annual GDP shares of different years against a cumulative ratio of discounted CCDR GDP; the net revenue '
     'includes base erosion (rev.new.usd, I41). Replicated.', _ND),
    ('I129', 'Current account % GDP: GDP implied by CA / CA%', 'The % of GDP effects (rows 18192-18194) divide by '
     'the GDP implied by the current account and its % of GDP (row 18192); this fails when the current account is 0. '
     'Replicated.', _ND),
    ('I130', 'Current account in current prices: no hold rule after the data', 'Row 18198 has no hold rule: 0 for '
     '2032-2040 (blank WEO cells), AE = AD; the USD row 18182 tests the % row (J18191) for non-zero. Replicated.', _ND),
    ('I131', 'GVA shares floored at 1% for the chart', 'L18747:L18756 floor the GVA shares at 1% (sum 1.0032) and '
     'pass them to MTOutputs. Replicated.', _ND),
    ('I132', '"GVA" is GTAP gross output; 2014 IO inflated by a fixed CPI index', 'The GVA is the GTAP OUTPUT column '
     '(gross output), so intensities are per USD of output; the 2014 IO values are inflated by the fixed 2014 CPI '
     'index $G$15631; label "thousands US$" but the values are USD m. Replicated (typed values).', _ND),
    ('I133', 'Cumulative table: direct emissions only; repeated MTOutputs codes', 'The cumulative table uses direct '
     'emissions only (H18762:H18771) next to total intensities; MTOutputs codes repeat (emin.cem in rows 124 and 138) '
     'and construction is cst (132) and con (140). Replicated.', _ND),
    ('I134', 'GTAP mapping: coal mining to food, crude to fuel transformation, gas to power', 'Mapping column R sends '
     'GTAP coa (coal mining) to foo, oil (crude extraction) to ftr, nga to pow. Replicated (typed GVA).', _ND),
    # E. R6-R10
    ('I135', 'Initially exempt demand mutes the usage response to every price change', 'Rows 5568-5570 raise the '
     'after-tax price ratio to eU x phase, phase = 0 before the phase-out, in every scenario including scenario 1 '
     '(baseline world-price moves too). The prototype already does this (lkx). Replicated.', _NE),
    ('I136', 'Exempt share denominator: basket spend, not the sum of deciles', 'K1793 = basket budget share x total '
     'consumption is the economy-wide spend; with mean budget shares the ten decile parts do not sum to 1 (Egypt LPG: '
     'sum of deciles / basket = 0.822). Egypt, 4 deciles, LPG: legacy 27.26%, prototype before v0.9.0 33.16% (sum of '
     'deciles). Replicated in v0.9.0 (Settings C83, R6.3).', _NE),
    ('I137', 'Most-used cooking fuel defaults to LPG when the WHO code is missing', 'L1784 IFNA(...,"lpg"): the '
     'most-used cooking fuel is "lpg" when the WHOCooking code is missing; the prototype before v0.9.0 gave "" (Settings '
     'C65; affects leakage too). Replicated in v0.9.0 (R6.1).', _NE),
    ('I138', 'Leakage to biomass on the not-exempt use only', 'Rows 5577, 5583, 5588 (5577 = -L5564 x share ...): '
     'the leakage is computed on the not-exempt use only. Replicated (R6.7).', _NE),
    ('I139', 'Manual price rows switch on only with a 2021 value; years 2021-2026 only', 'F765:F829 (I53 known): a '
     'manual price row is used only if it has a 2021 value; manual years are 2021-2026 only. Replicated (R8.1).', _NE),
    ('I140', 'Blank manual elasticity gives "no data" and an error', 'A blank manual elasticity gives "no data" and an '
     'error in the elasticity (Elasticities F column). Replicated as #N/A plus a check, not a silent fallback.', _NE),
    ('I141', 'Methane intensity decline: rates borrowed across sources, decline from 2024', 'Biomass and downstream '
     'gas use the oil-and-gas rate J185 (rows 6078, 6079); coal J186 = 0; agriculture J187 = 0.4719%/y; waste J188 = '
     '0.5%/y. Decline from 2024 (index 1 in 2023). Replicated (R8.6).', _NE),
    ('I142', 'Power cost breakdown: no shadow-price column, floor ignored', 'E5 cost breakdown (rows 3508-3517) has no '
     'shadow-price (D6) column and ignores the MinPostSubsidyPowerPrice floor; checksum S shows the gap (0 for Egypt in '
     'both scenarios). Replicated; the checksum kept.', _NE),
    ('I143', 'Road other biofuels use oil elasticities and oil AEEI', 'Row 5406: road other biofuels (elasticity '
     'model) use the oil elasticities and the oil AEEI with the biomass price. Replicated (R10.3).', _NE),
    ('I144', 'Self-generated renewables priced at the solar investment cost, no policy', 'Rows 2805-2806, 5480, 5505: '
     'self-generated renewables in aviation and navigation are priced at the solar levelised investment cost (row '
     '3468), carry no new policy (nce typed 0) and no shadow price, with the transport ("rod") renewables '
     'elasticities. Egypt use 0. Replicated (R10.5-R10.6).', _NE),
    ('I145', 'Range anxiety: negative values held; one-year fit', 'Rows 4354-4356 IF(N<0,N,...): range anxiety may be '
     'negative and a negative start value is then held; the fit uses one year (Transport3 A1 = 2025); the freight '
     'residual is scaled x 10 (no effect on the root); a missing country gets the average of the stored table. '
     'Replicated (R10.9).', _NE),
    ('I146', 'Electricity producer subsidy per kWh floored at -0.3 $/kWh', 'H3590:H3591 floor the electricity producer '
     'subsidy per kWh at -0.3 $/kWh; the part above the floor is a residual (3592) outside prices; allocation by the '
     'pre-tax gap x consumption (3588). Replicated (R7.5-R7.7).', _NE)]
ISSUE_LEGACY.update({f'I{n}': 'replicated' for n in range(101, 147)})
ISSUE_LEGACY.update({'I105': 'not replicated', 'I106': 'not replicated', 'I110': 'not replicated'})
ISSUE_STATUS.update({
    'I101': ('Major', 'Accepted', 'Replicated (user decision R13): margin year 2024 for coal and gas (MARGIN_YEAR).'),
    'I102': ('Minor', 'Accepted', 'Replicated (FPRPATH helper rows); no effect once L171 is fixed.'),
    'I103': ('Minor', 'Accepted', 'Replicated (user decision LD10): feebates flat after the target year.'),
    'I104': ('Major', 'Accepted', 'Replicated for unit costs; welfare from v_PM (Equations_addendum R1.4, R2.5).'),
    'I105': ('Major', 'Accepted', 'Prototype approximation; recompute v_PM from an AP module run for other policies.'),
    'I106': ('Major', 'Accepted', 'Typed Egypt values; other countries need their own module run (R1 issue).'),
    'I107': ('Minor', 'Accepted', 'Replicated (Equations_addendum R2.9-R2.10).'),
    'I108': ('Minor', 'Accepted', 'Replicated (Equations_addendum R2.11: ext_ecy = 0).'),
    'I109': ('Minor', 'Accepted', 'Replicated (Equations_addendum R2.11).'),
    'I110': ('Minor', 'Accepted', 'Departure: every scenario group computed; group 1 equals legacy.'),
    'I111': ('Major', 'Accepted', 'Replicated; pending user decisions B-c, B-d, B-e of the transport plan.'),
    'I112': ('Minor', 'Accepted', 'Replicated: 2041 = 2040 in the typed AP values.'),
    'I113': ('Major', 'Accepted', 'Replicated (Equations_addendum R3.9).'),
    'I114': ('Minor', 'Accepted', 'Replicated (Equations_addendum R3.1, R3.9).'),
    'I115': ('Minor', 'Accepted', 'Replicated (Equations_addendum R3.5, R3.14).'),
    'I116': ('Minor', 'Accepted', 'Replicated (Equations_addendum R3.2-R3.3).'),
    'I117': ('Minor', 'Accepted', 'Replicated (Equations_addendum R3.4).'),
    'I118': ('Minor', 'Accepted', 'Replicated (Equations_addendum R3.5).'),
    'I119': ('Minor', 'Accepted', 'Replicated 0; user to decide: keep 0, or fill and drop the AP term of the power fuels.'),
    'I120': ('Minor', 'Accepted', 'Replicated (Equations_addendum R3.16); the prototype computes every scenario group.'),
    'I121': ('Minor', 'Accepted', 'Replicated in the efficient prices (Equations_addendum R3.15).'),
    'I122': ('Minor', 'Accepted', 'Replicated values; the prototype tests LEFT(x,3)="Yes" (L113 rule).'),
    'I123': ('Major', 'Accepted', 'Replicated; link to revenue, GHG and ETS totals by decision D-R4.'),
    'I124': ('Minor', 'Accepted', 'Replicated (Equations_addendum R5.10).'),
    'I125': ('Minor', 'Accepted', 'Replicated: 2041 blank (Equations_addendum R5).'),
    'I126': ('Minor', 'Accepted', 'Replicated; constants on Settings labelled legacy hard-coded.'),
    'I127': ('Major', 'Accepted', 'Replicated (#N/A outside the CCDR list); IFERROR would be a departure.'),
    'I128': ('Minor', 'Accepted', 'Replicated (Equations_addendum R5.18).'),
    'I129': ('Minor', 'Accepted', 'Replicated (Equations_addendum R11.6).'),
    'I130': ('Minor', 'Accepted', 'Replicated (Equations_addendum R11.9).'),
    'I131': ('Minor', 'Accepted', 'Replicated (Equations_addendum R12.7).'),
    'I132': ('Minor', 'Accepted', 'Replicated (typed GVA, Equations_addendum R12.1).'),
    'I133': ('Minor', 'Accepted', 'Replicated (Equations_addendum R12.9).'),
    'I134': ('Minor', 'Accepted', 'Replicated (typed GVA).'),
    'I135': ('Minor', 'Accepted', 'Replicated (prototype lkx, unchanged).'),
    'I136': ('Major', 'Accepted', 'Replicate in v0.9.0: Settings C83 basket denominator (Equations_addendum R6.3).'),
    'I137': ('Minor', 'Accepted', 'Replicate in v0.9.0: Settings C65 fallback "lpg" (Equations_addendum R6.1).'),
    'I138': ('Minor', 'Accepted', 'Replicate in v0.9.0: lkd on the not-exempt use (Equations_addendum R6.7).'),
    'I139': ('Minor', 'Accepted', 'Replicated (Equations_addendum R8.1; I53).'),
    'I140': ('Minor', 'Accepted', 'Replicated as #N/A plus a check (Equations_addendum R8.5).'),
    'I141': ('Minor', 'Accepted', 'Replicated (Equations_addendum R8.6).'),
    'I142': ('Minor', 'Accepted', 'Replicated; checksum kept (Equations_addendum R9.12).'),
    'I143': ('Minor', 'Accepted', 'Replicated (Equations_addendum R10.3).'),
    'I144': ('Minor', 'Accepted', 'Replicated (Equations_addendum R10.5-R10.6).'),
    'I145': ('Minor', 'Accepted', 'Replicated (Equations_addendum R10.8-R10.9).'),
    'I146': ('Minor', 'Accepted', 'Replicated (Equations_addendum R7.6-R7.7).')})

# v0.9.0 (2026-10-29): status after the build of R1-R3, R6-R11 (integrator notes v90_*_changes.md, applied and deleted;
# record in CAVEATS.md). R4, R5, R12 deferred by the user (branch wip-r4-r5-r12): their issues are not built yet.
_DEFERRED = 'Not built: deferred by the user (2026-10-29; legacy work in progress)'
ISSUE_LEGACY.update({c: _DEFERRED for c in ('I123', 'I124', 'I125', 'I126', 'I127', 'I128', 'I131', 'I132', 'I133',
                                            'I134')})
ISSUE_LEGACY.update({'I53': 'replicated', 'I89': 'not replicated'})
ISSUE_STATUS.update({
    'I49': ('Minor', 'Resolved', 'Replicated as legacy (v0.9.0, R7): the phase-out in the supply cost (psu x psf, block '
            'row psp), the price controls absorb (1 - pass-through); the v0.6.2 wedge rows (psw, ppsw, psr) removed. '
            'Electricity producer subsidies built (R7.5-R7.9; I146). Egypt: no data (0).'),
    'I53': ('Minor', 'Accepted', 'Replicated (v0.9.0, R8.1-R8.2; I139): a manual row switches on with a 2021 value; manual '
            'years 2021-2026. Ask the CPAT team about the intent.'),
    'I61': ('Major', 'Accepted', 'v0.9.0: the range-anxiety goal seek (ra_goalseek.py, LegacyDiff 63) and the elasticity '
            'branch of road biofuels (R10, LegacyDiff 62) are built; the review of the engineer run in Excel and the '
            'vehicle revenues in 12b stay parked.'),
    'I89': ('Major', 'Accepted', 'Kept at 2022 by user decision (2026-10-15), although legacy 465 uses 2024 (v0.9.0 '
            'check): a departure; the electricity tax and price-chain residual are those of 2022 (res txe +0.0021, '
            'ores -0.063 $/kWh; legacy 2024: -0.0551, -0.0205).'),
    'I119': ('Minor', 'Accepted', 'Replicated 0 (v0.9.0, R3.12: electricity entx unchanged); filling it would tax '
             'power-plant air pollution twice.'),
    'I136': ('Major', 'Accepted', 'Replicated (v0.9.0, R6.3): Settings C83 basket denominator; Egypt 4 deciles LPG '
             '0.27259 = legacy 0.2726.'),
    'I137': ('Minor', 'Accepted', 'Replicated (v0.9.0, R6.1): Settings C65 fallback "lpg".'),
    'I138': ('Minor', 'Accepted', 'Replicated (v0.9.0, R6.7): lkd on the not-exempt use.')})
ISSUE_STATUS.update({c: (ISSUE_STATUS[c][0], 'Open', 'Not built: R4, R5, R12 deferred by the user (2026-10-29); '
                         'replicate when built (' + ISSUE_STATUS[c][2] + ')')
                     for c in ('I123', 'I124', 'I125', 'I126', 'I127', 'I128', 'I131', 'I132', 'I133', 'I134')})

ISSUES += [
    ('I147', 'Food & forestry local pollutants far above the legacy air-pollution input', 'The modelled PM2.5 of '
     'section 17b (coefficients x section-15 emissions, R1.5) matches legacy for power and road (AP 975-977, 2022) but '
     'food & forestry gives 85.3 ug/m3 against 2.74 in legacy: the prototype\'s section-15 food & forestry emissions '
     'are far above the legacy AP input (BC 2,199 t against 3.8 t; NOx 40 kt against 5.5 kt; SO2 0.78 kt against 3.3 '
     'kt); total 115.6 against 30.2 ug/m3. The food & forestry change drives wel.air (Egypt $20 tax, 2030: 3.76 bn). '
     'Cause not found yet (section 15 food & forestry block, LegacyDiff 53, against the legacy E3 rows).',
     'CAVEATS.md 2026-10-29 (v0.9.0 R1-R3)'),
    ('I148', 'Current account data typed for Egypt only', 'Legacy reads the current account from WEO codes that no '
     'longer exist (L50); the prototype types the corrected Egypt values (EGY.BCA.A, EGY.BCA_NGDPD.A, 2022-2041, '
     'held at 2031 as legacy) on Inputs (block Inputs_macro); other countries read 0, so their current-account rows '
     'are 0 (bca.y and bca.dp give 0 where legacy would give #DIV/0!).', 'CAVEATS.md 2026-10-29 (v0.9.0 R11)')]
DATA_ISSUES.add('I148')
ISSUE_LEGACY.update({'I147': 'Open: cause not found (prototype or legacy)', 'I148': 'replicated'})
ISSUE_STATUS.update({
    'I147': ('Major', 'Open', 'Reconcile the section-15 food & forestry emissions with the legacy AP input (a bug of '
             'the prototype or of legacy, or a data difference); read wel.air with this caveat until then.'),
    'I148': ('Extremely high', 'Open', 'No cell plan possible (the data are missing): Egypt typed, as legacy\'s '
             'corrected values. Plan: the data team adds the current account (BCA, BCA_NGDPD) to the WEO table for '
             'every country; then read it instead of the typed values.')})

# v0.9.0 (user 2026-10-29): the last historical price year is 2024, as legacy 456 and 465 (I89 closed)
ISSUE_LEGACY.update({'I89': 'replicated'})
ISSUE_STATUS.update({'I89': ('Major', 'Closed', 'v0.9.0 (user 2026-10-29): the last historical price year is 2024, as '
                             'legacy (price data through 2024, projection from 2025). v0.3.7-v0.8.5 held 2022, to stay close '
                             'to the legacy cached run of an older price vintage (2026-10-09 comparison).')})

# v0.9.0 (EF465, 2026-10-29): combustion emission factors as legacy 465 (table Inputs_nc)
_EF465_L = {
    'L58': 'Fixed by the CPAT team in 465: legacy 465 has EF codes for services, rail, construction, other '
           'manufacturing, food & forestry and other energy, and maps mining & chemicals, iron & steel, other metals, '
           'machinery, cement and fuel transformation to manufacturing (rows 6388-6395); the prototype follows 465 '
           '(v0.9.0, table Inputs_nc). Navigation is still missing in 465 (bug L22, our fix kept).',
    'L59': 'Fixed by the CPAT team in 465: each factor is the country\'s, else its World Bank region\'s, else the '
           'world\'s (rows 1052-1663 F); the prototype follows 465 (v0.9.0) and retires its nearest-match fallback '
           '(where the 465 chain gives 0, no fuel is burnt in Egypt).'}
LEGACY = [(c, t, ('Mitigation rows 1052-1663 (465)' if c in _EF465_L else w), d, _EF465_L.get(c, st))
          for c, t, w, d, st in LEGACY]
ISSUES += [
    ('I149', 'Other energy use takes the largest emission factor of each fuel across the other subsectors',
     'Legacy 465 rows 1117-1124 and the oen rows of every pollutant block (note "The EF of this sector is equal to the '
     'max across other sectors"), power included; CH4 rows blank in legacy. Replicated (Inputs_nc oen rows, MAXIFS). '
     'Legacy takes the maximum year by year, the prototype on the base and final factors and the line between: exact '
     'for Egypt (other energy burns only other oil products).', 'CAVEATS.md (2026-10-29, EF465)')]
ISSUE_LEGACY.update({'I147': 'replicated', 'I149': 'replicated'})
ISSUE_STATUS.update({
    'I147': ('Major', 'Closed', 'Resolved in v0.9.0 (EF465): the cause was the emission factors (our L58/L59 fallback gave '
             'food & forestry diesel the construction factor, 2.51 t BC/ktoe against legacy 465\'s regional 0.0044); '
             'with the 465 lookup section 15 equals legacy in 2022 (food & forestry BC 3.8 t) and modelled PM2.5 is '
             '33.06 against 30.17 ug/m3 (the difference: navigation, L22).'),
    'I149': ('Minor', 'Accepted', 'Replicated.')})

# v0.9.0 (user 2026-10-29): legacy prices (I99): legacy 465 already carries the corrected Egypt block
ISSUES += [
    ('I150', 'Spot coal and gas prices of Egypt hold a year and 0 in legacy 465', 'Legacy 465 Prices_dom EGY2021-2024 '
     'mit.spot.coa = 2024 and mit.spot.nga = 0 (the prototype data: 4.75-10.49 and 7.51-28.06 $/GJ). Read only with '
     'the spot-price option for power (SpotPow / UseSpotFuelPricesInEngineerModel, default No): no effect by default.',
     'Prices_dom; CAVEATS.md (2026-10-29)')]
DATA_ISSUES.add('I150')
ISSUE_LEGACY.update({'I99': 'replicated', 'I150': 'not replicated'})
ISSUE_STATUS.update({
    'I99': ('Major', 'Closed', 'v0.9.0 (user 2026-10-29: legacy prices): legacy 465 Prices_dom already holds the corrected '
            'Egypt block; the prototype data equal it cell by cell except the spot coal and gas cells (I150). LD4 and '
            'LD33 are Same.'),
    'I150': ('Minor', 'Open', 'The CPAT data team fills the spot cells; the prototype keeps the module values (no '
             'effect unless the spot option is chosen).')})

# v0.9.0 (user 2026-10-29): combustion CH4 in legacy is a bug with a cell plan (L223); I34 keeps the source allocation
ISSUE_STATUS.update({'I34': ('Minor', 'Accepted', 'Replicated: the allocation of methane sources in the air-pollution '
                             'table. The missing combustion CH4 factors are legacy bug L223 (cell plan), fixed in the '
                             'prototype.')})

# v0.9.0 PIGAP (user 2026-10-29): Pigouvian proxy (I151), air-pollution unit costs a bug (L224, was I104), module tabs
ISSUES += [
    ('I151', 'Pigouvian road-transport component: base-year value x growth of the per-km costs',
     'Legacy\'s Pigouvian tax uses scenario 1\'s transport externalities per litre (mf.1, Transport 322-344), which follow '
     'scenario 1\'s road model. The prototype, live and acyclic in every scenario group, takes base-year fuel economy, '
     'passenger/freight split (Transport1 fuel shares), driving share and road share, x the growth of the typed per-km '
     'costs. Egypt against legacy 465 mf.1: gasoline -5.0% (2030), -9.2% (2040); diesel +6.7%, +3.9%.',
     'CAVEATS.md (2026-10-29, PIGAP)')]
ISSUE_LEGACY.update({'I151': 'not replicated', 'I104': 'not replicated'})
ISSUE_STATUS.update({
    'I151': ('Major', 'Accepted', 'Departure by user decision (2026-10-29: dynamic, copy-pastable, no stored scenario-1 '
             'values).'),
    'I104': ('Major', 'Closed', 'A legacy bug (user 2026-10-29): L224, fixed with marginal damages.'),
    'I106': ('Minor', 'Accepted', 'Typed Egypt values on the module tabs FromAirPollution and FromTransportCB (other '
             'countries read 0) until the modules write them.'),
    'I118': ('Minor', 'Accepted', 'Transport part of the Pigouvian tax: the I151 proxy (no stored scenario-1 values).')})
