"""The legacy tabs kept at their cell addresses, and the data blocks of each that become tidy tables (tidy_specs.py).

A block is a grid: data cells in rows r0..r1 and columns c0..c1 (minus the key columns); each data cell gets the
row keys from the key columns of its row and the column label from `label_row`. Cells outside every block (titles,
notes, labels) stay in the layout (`_layout/<tidy>.cells.csv`) and come back unchanged.
"""

# The blocks were mapped from the legacy tabs and checked (row keys unique, labels unique, no overlap, no key or
# label cell used as data): 183 blocks hold 225,936 of the 232,465 numeric cells; the rest are keys, labels and 60
# non-data numbers (column index rows, a year row read by its own header). Extras: labels={col: name} names a column
# whose legacy header is blank or repeated; key_cols=[] marks a one-row block.
BLOCKS = {
  'legacy_Countries_cells.csv': [
    # countries_seq: A6:B261, keys C,D, labels row 5
    dict(name='countries_seq', rows=(6, 261), cols=(1, 2), key_cols=[3, 4], label_row=5, keys=['name', 'code'], label='variable', desc='Economy list (World Bank June 2018 classification, plus World and memo aggregates in rows 229-261; code OEU appears twice, rows 235 and 259, so the name is part of the key): sequence number (CtryNames C6:C227, CtryCodes D6:D227)', unit='', labels={1: 'seq'}),
    # countries_attributes: E6:X261, keys C,D, labels row 5
    dict(name='countries_attributes', rows=(6, 261), cols=(5, 24), key_cols=[3, 4], label_row=5, keys=['name', 'code'], label='variable', desc='Economy attributes by code: alpha-2, WB region (CtryRegions F), income group, income code (CtryIncome H), lending category, GAINS region (RegVal O), euro use (CtryEuro P), IFS and WEO codes, crude market, IEA, Enerdata codes, VSL grouping', unit='', labels={8: 'Income code', 11: 'Name (K)', 12: 'Name (L)', 13: 'Code (M)'}),
    # countries_region_seq: A264:B309, keys C,D, labels row 5
    dict(name='countries_region_seq', rows=(264, 309), cols=(1, 2), key_cols=[3, 4], label_row=5, keys=['name', 'code'], label='variable', desc='World Bank aggregates (regions and groups): sequence number (RegNames C264:C309, RegCodes D)', unit='', labels={1: 'seq'}),
    # countries_region_attributes: K264:U309, keys C,D, labels row 5
    dict(name='countries_region_attributes', rows=(264, 309), cols=(11, 21), key_cols=[3, 4], label_row=5, keys=['name', 'code'], label='variable', desc='World Bank aggregates: name variants (K-M) and IEA country (U)', unit='', labels={11: 'Name (K)', 12: 'Name (L)', 13: 'Code (M)'}),
    # countries_iea_regions: C320:C346, keys B, labels row 319
    dict(name='countries_iea_regions', rows=(320, 346), cols=(3, 3), key_cols=[2], label_row=319, keys=['code'], label='variable', desc='IEA regions: name by code', unit=''),
  ],
  'legacy_Elasticities_cells.csv': [
    # ela_source_options: I5:I6, keys H, labels row 4
    dict(name='ela_source_options', rows=(5, 6), cols=(9, 9), key_cols=[8], label_row=4, keys=['option'], label='variable', desc='Elasticity source options and their numeric code', unit='', labels={9: 'code'}),
    # ela_fuel_codes: C5:C14, keys B, labels row 4
    dict(name='ela_fuel_codes', rows=(5, 14), cols=(3, 3), key_cols=[2], label_row=4, keys=['fuel'], label='variable', desc='Fuel names and codes', unit='', labels={3: 'code'}),
    # ela_type_sector_codes: F5:F13, keys E, labels row 4
    dict(name='ela_type_sector_codes', rows=(5, 13), cols=(6, 6), key_cols=[5], label_row=4, keys=['name'], label='variable', desc='Elasticity types (rows 5-7) and sectors (rows 10-13) with codes', unit='', labels={6: 'code'}),
    # ela_settings: C19:F22, keys B, labels row 18
    dict(name='ela_settings', rows=(19, 22), cols=(3, 6), key_cols=[2], label_row=18, keys=['setting'], label='variable', desc='User-specified elasticity settings (source, GDP adjustment, adjustments) and their codes', unit=''),
    # ela_income_global: C27:H58, keys B, labels row 26
    dict(name='ela_income_global', rows=(27, 58), cols=(3, 8), key_cols=[2], label_row=26, keys=['item'], label='variable', desc='Income elasticities used in calculations: elasticity, adjustment, manual, simple, standard deviation', unit='1'),
    # ela_price_usage_global: C62:H93, keys B, labels row 61
    dict(name='ela_price_usage_global', rows=(62, 93), cols=(3, 8), key_cols=[2], label_row=61, keys=['item'], label='variable', desc='Own-price elasticities, usage/intensive margin: elasticity, adjustment, manual, simple, standard deviation', unit='1'),
    # ela_price_efficiency_global: C96:H127, keys B, labels row 95
    dict(name='ela_price_efficiency_global', rows=(96, 127), cols=(3, 8), key_cols=[2], label_row=95, keys=['item'], label='variable', desc='Own-price elasticities, extensive and efficiency margin: elasticity, adjustment, manual, simple, std. dev.', unit='1'),
    # ela_cross_price_global: C131:H133, keys B, labels row 130
    dict(name='ela_cross_price_global', rows=(131, 133), cols=(3, 8), key_cols=[2], label_row=130, keys=['item'], label='variable', desc='Cross-price elasticities: elasticity, adjustment, manual, simple, standard deviation', unit='1'),
    # ela_income_selected: G143:H174, keys C,D,E,F, labels row 142
    dict(name='ela_income_selected', rows=(143, 174), cols=(7, 8), key_cols=[3, 4, 5, 6], label_row=142, keys=['type', 'fuel', 'sector', 'code'], label='variable', desc='Income elasticity used for the selected country (G, legacy formula result) and its standard deviation', unit='1'),
    # ela_income_by_country: I143:IA174, keys C,D,E,F, labels row 139
    dict(name='ela_income_by_country', rows=(143, 174), cols=(9, 235), key_cols=[3, 4, 5, 6], label_row=139, keys=['type', 'fuel', 'sector', 'code'], label='country', desc="Country-specific income elasticities ('Simple' option): generic (NA), income-group (Lower..High) and one column per country code (ElaAll / ElaCtry row 139)", unit='1'),
    # ela_price_selected: G178:H246, keys C,D,E,F, labels row 176
    dict(name='ela_price_selected', rows=(178, 246), cols=(7, 8), key_cols=[3, 4, 5, 6], label_row=176, keys=['type', 'fuel', 'sector', 'code'], label='variable', desc='Own-price (usage, efficiency) and cross-price elasticities used for the selected country and standard error', unit='1'),
    # ela_price_by_country: I178:IA246, keys C,D,E,F, labels row 139
    dict(name='ela_price_by_country', rows=(178, 246), cols=(9, 235), key_cols=[3, 4, 5, 6], label_row=139, keys=['type', 'fuel', 'sector', 'code'], label='country', desc='Country-specific own-price (usage rows 178-209, efficiency 211-242) and cross-price (244-246) elasticities by country code (labels from row 139; rows 176-177 repeat the region / income rows)', unit='1'),
    # ela_efficiency_selected: G256:G282, keys C,D,E,F, labels row 254
    dict(name='ela_efficiency_selected', rows=(256, 282), cols=(7, 7), key_cols=[3, 4, 5, 6], label_row=254, keys=['type', 'fuel', 'sector', 'code'], label='variable', desc='Autonomous efficiency improvement used for the selected country', unit='1/year'),
    # ela_efficiency_by_country: H256:HZ282, keys C,D,E,F, labels row 251
    dict(name='ela_efficiency_by_country', rows=(256, 282), cols=(8, 234), key_cols=[3, 4, 5, 6], label_row=251, keys=['type', 'fuel', 'sector', 'code'], label='country', desc='Annual autonomous efficiency improvements by sector and fuel: generic (NA), income group, one column per country code (row 251)', unit='1/year'),
    # ela_power_selected: G293:G321, keys C,D,E,F, labels row 290
    dict(name='ela_power_selected', rows=(293, 321), cols=(7, 7), key_cols=[3, 4, 5, 6], label_row=290, keys=['type', 'fuel', 'sector', 'code'], label='variable', desc='Elasticity-based power parameters used for the selected country', unit=''),
    # ela_power_by_country: H293:HZ321, keys C,D,E,F, labels row 287
    dict(name='ela_power_by_country', rows=(293, 321), cols=(8, 234), key_cols=[3, 4, 5, 6], label_row=287, keys=['type', 'fuel', 'sector', 'code'], label='country', desc='Elasticity-based power parameters (generation productivity gains, transmission cost, non-fuel cost shares, conditional price elasticities) by country code (row 287)', unit=''),
  ],
  'legacy_Prices_int_cells.csv': [
    # pint_wb: L13:AV17, keys E,G, labels row 11
    dict(name='pint_wb', rows=(13, 17), cols=(12, 48), key_cols=[5, 7], label_row=11, keys=['commodity', 'unit'], label='year', desc='World Bank Commodity Price Forecasts (Pink Sheet, Oct 2024), nominal USD', unit='per row (column G)'),
    # pint_imf_series: G24:K29, keys E,F, labels row 23
    dict(name='pint_imf_series', rows=(24, 29), cols=(7, 11), key_cols=[5, 6], label_row=23, keys=['group_code', 'subject_code'], label='variable', desc='IMF WEO commodity series metadata: group name, descriptor, units, scale, notes', unit=''),
    # pint_imf: L24:AR31, keys E,F, labels row 23
    dict(name='pint_imf', rows=(24, 31), cols=(12, 44), key_cols=[5, 6], label_row=23, keys=['group_code', 'subject_code'], label='year', desc='IMF WEO (April 2026) commodity prices by subject code; row 31 = average coal', unit='USD (see pint_imf_series)'),
    # pint_iea: L37:BA43, keys H,I,K, labels row 36
    dict(name='pint_iea', rows=(37, 43), cols=(12, 53), key_cols=[8, 9, 11], label_row=36, keys=['commodity', 'unit', 'wb_commodity'], label='year', desc='IEA WEO 2024 prices (STEPS), with the US CPI (row 43)', unit='per row (column I)'),
    # pint_eia_short_ton: I47:I47, keys H, labels row 46
    dict(name='pint_eia_short_ton', rows=(47, 47), cols=(9, 9), key_cols=[8], label_row=46, keys=['item'], label='variable', desc='EIA: short ton to metric ton conversion', unit='factor', labels={9: 'value'}),
    # pint_eia: L50:BK56, keys H,I, labels row 49
    dict(name='pint_eia', rows=(50, 56), cols=(12, 63), key_cols=[8, 9], label_row=49, keys=['commodity', 'unit'], label='year', desc='EIA International Energy Outlook 2023 prices; row 56 = delivered coal supply price ($nom/short ton)', unit='per row (column I)'),
    # pint_regional_assumptions: H62:I281, keys G, labels row 61
    dict(name='pint_regional_assumptions', rows=(62, 281), cols=(8, 9), key_cols=[7], label_row=61, keys=['country'], label='variable', desc='Regional assumptions by country name: baseline taxes ad-valorem or fixed; natural gas market', unit=''),
    # pint_regional_fuel: H285:Q312, keys F,G, labels row 284
    dict(name='pint_regional_fuel', rows=(285, 312), cols=(8, 17), key_cols=[6, 7], label_row=284, keys=['region', 'fuel'], label='year', desc='Values by World Bank region and oil product, 2016-2025 (untitled in legacy)', unit=''),
    # pint_ej_mtoe: J320:J320, keys I, labels row 319
    dict(name='pint_ej_mtoe', rows=(320, 320), cols=(10, 10), key_cols=[9], label_row=319, keys=['item'], label='variable', desc='Conversion EJ to MTOE', unit='MTOE/EJ', labels={10: 'value'}),
    # pint_world_demand: I323:AO333, keys D,E,F,G,H, labels row 322
    dict(name='pint_world_demand', rows=(323, 333), cols=(9, 41), key_cols=[4, 5, 6, 7, 8], label_row=322, keys=['scenario_no', 'scenario', 'fuel', 'unit', 'indicator'], label='year', desc='Global fuel demand / production by IEA scenario (WDData A323:BZ333)', unit='MTOE'),
  ],
  'legacy_Power_cells.csv': [
    # power_misc_parameters: E20:G23, keys B,D, labels row 19
    dict(name='power_misc_parameters', rows=(20, 23), cols=(5, 7), key_cols=[2, 4], label_row=19, keys=['quantity', 'sector'], label='variable', desc='Miscellaneous power parameters: source, unit, value (T&D cost, nuclear fuel cost, average WACC)', unit='per row (F)'),
    # power_re_scaleup_rates: J20:J23, keys I, labels row 19
    dict(name='power_re_scaleup_rates', rows=(20, 23), cols=(10, 10), key_cols=[9], label_row=19, keys=['category'], label='variable', desc='Assumptions for max RE scale-up rates by category (PowScRate J20:J23, PowScCat I20:I23)', unit='1/year', labels={10: 'rate'}),
    # power_wacc_by_income: N20:N23, keys M, labels row 19
    dict(name='power_wacc_by_income', rows=(20, 23), cols=(14, 14), key_cols=[13], label_row=19, keys=['income_level'], label='variable', desc='User-set WACC assumption by income level', unit='1'),
    # power_mpp_world: E28:L39, keys A,B,C,D, labels row 27
    dict(name='power_mpp_world', rows=(28, 39), cols=(5, 12), key_cols=[1, 2, 3, 4], label_row=27, keys=['code', 'item', 'region', 'technology'], label='variable', desc='Main technoeconomic parameters, global level (PowA/PowE..PowK rows 25-356)', unit='per column name'),
    # power_mpp_world_old: U28:AA39, keys Q,R,S,T, labels row 27
    dict(name='power_mpp_world_old', rows=(28, 39), cols=(21, 27), key_cols=[17, 18, 19, 20], label_row=27, keys=['code', 'item', 'region', 'technology'], label='variable', desc='Main technoeconomic parameters, global level, OLD DATA copy', unit='per column name'),
    # power_mpp_region: E42:L109, keys A,B,C,D, labels row 41
    dict(name='power_mpp_region', rows=(42, 109), cols=(5, 12), key_cols=[1, 2, 3, 4], label_row=41, keys=['code', 'item', 'region', 'technology'], label='variable', desc='Main technoeconomic parameters, regional level (column L: notes / values without header)', unit='per column name', labels={12: 'note (L)'}),
    # power_mpp_region_old: U42:AB109, keys Q,R,S,T, labels row 41
    dict(name='power_mpp_region_old', rows=(42, 109), cols=(21, 28), key_cols=[17, 18, 19, 20], label_row=41, keys=['code', 'item', 'region', 'technology'], label='variable', desc='Main technoeconomic parameters, regional level, OLD DATA copy (column AB: notes / values without header)', unit='per column name', labels={28: 'note (AB)'}),
    # power_mpp_country: E112:K294, keys A,B,C,D, labels row 111
    dict(name='power_mpp_country', rows=(112, 294), cols=(5, 11), key_cols=[1, 2, 3, 4], label_row=111, keys=['code', 'item', 'region', 'technology'], label='variable', desc='Main technoeconomic parameters, country level (PowACtry A112:A294)', unit='per column name'),
    # power_mpp_country_old: U112:Z294, keys Q,R,S,T, labels row 111
    dict(name='power_mpp_country_old', rows=(112, 294), cols=(21, 26), key_cols=[17, 18, 19, 20], label_row=111, keys=['code', 'item', 'region', 'technology'], label='variable', desc='Main technoeconomic parameters, country level, OLD DATA copy', unit='per column name'),
    # power_capex_time_factor: F303:BD317, keys A,B,C,D,E, labels row 302
    dict(name='power_capex_time_factor', rows=(303, 317), cols=(6, 56), key_cols=[1, 2, 3, 4, 5], label_row=302, keys=['code', 'item', 'region', 'scenario', 'technology'], label='year', desc='Evolution of capex: capex time factor by decline scenario and technology, rows 303-317 (PowCtf F25:BD597, PowCtfYr row 302)', unit='factor (base = 1)'),
    # power_capex_time_factor_2: F318:BD330, keys A,B,C,D,E, labels row 302
    dict(name='power_capex_time_factor_2', rows=(318, 330), cols=(6, 56), key_cols=[1, 2, 3, 4, 5], label_row=302, keys=['code', 'item', 'region', 'scenario', 'technology'], label='year', desc='Capex time factor, rows 318-330 (split because row 318 repeats the key wld.ctf.med.ore of row 316 with the same values; MATCH on PowA finds row 316)', unit='factor (base = 1)'),
    # power_capex_time_factor_side: BW304:CX308, keys BV, labels row 303
    dict(name='power_capex_time_factor_side', rows=(304, 308), cols=(75, 102), key_cols=[74], label_row=303, keys=['technology_name'], label='year', desc='Side table: capex factor path 2023-2050 by technology name (utility / rooftop PV, wind, battery)', unit='factor'),
    # power_capex_change_avg: F333:G340, keys D,E, labels row 332
    dict(name='power_capex_change_avg', rows=(333, 340), cols=(6, 7), key_cols=[4, 5], label_row=332, keys=['category', 'technology'], label='variable', desc='Yearly change in wind and solar capex: historical and forward-projection averages', unit='1/year'),
    # power_capex_change: H333:BD340, keys D,E, labels row 302
    dict(name='power_capex_change', rows=(333, 340), cols=(8, 56), key_cols=[4, 5], label_row=302, keys=['category', 'technology'], label='year', desc='Yearly change in wind and solar capex by year (no header in legacy row 332; labels assumed from the year row 302 of the capex factors, H = 2002 .. BD = 2050)', unit='1/year'),
    # power_capex_change_avg_old: BJ334:BK339, keys BH,BI, labels row 332
    dict(name='power_capex_change_avg_old', rows=(334, 339), cols=(62, 63), key_cols=[60, 61], label_row=332, keys=['category', 'technology'], label='variable', desc='OLD copy: historical and forward-projection averages of the yearly change in wind and solar capex (no legacy header)', unit='1/year', labels={62: 'Hist Avg', 63: 'Forward projection avg'}),
    # power_capex_change_old: BL334:DH339, keys BH,BI, labels row 332
    dict(name='power_capex_change_old', rows=(334, 339), cols=(64, 112), key_cols=[60, 61], label_row=332, keys=['category', 'technology'], label='year', desc='OLD copy of the yearly change in wind and solar capex by year (no legacy header; labels as power_capex_change, BL = 2002 .. DH = 2050)', unit='1/year', labels={64: '2002', 65: '2003', 66: '2004', 67: '2005', 68: '2006', 69: '2007', 70: '2008', 71: '2009', 72: '2010', 73: '2011', 74: '2012', 75: '2013', 76: '2014', 77: '2015', 78: '2016', 79: '2017', 80: '2018', 81: '2019', 82: '2020', 83: '2021', 84: '2022', 85: '2023', 86: '2024', 87: '2025', 88: '2026', 89: '2027', 90: '2028', 91: '2029', 92: '2030', 93: '2031', 94: '2032', 95: '2033', 96: '2034', 97: '2035', 98: '2036', 99: '2037', 100: '2038', 101: '2039', 102: '2040', 103: '2041', 104: '2042', 105: '2043', 106: '2044', 107: '2045', 108: '2046', 109: '2047', 110: '2048', 111: '2049', 112: '2050'}),
    # power_decom_transmission: E346:F354, keys A,B,C,D, labels row 345
    dict(name='power_decom_transmission', rows=(346, 354), cols=(5, 6), key_cols=[1, 2, 3, 4], label_row=345, keys=['code', 'item', 'region', 'technology'], label='variable', desc='Decommissioning and transmission costs by technology (world)', unit='share of capex'),
    # power_installed_capacity: F358:AC1635, keys C,D,E, labels row 357
    dict(name='power_installed_capacity', rows=(358, 1635), cols=(6, 29), key_cols=[3, 4, 5], label_row=357, keys=['code', 'country', 'technology'], label='year', desc='Installed capacity per country and technology 2000-2023 (PowIC F358:AC1635, PowICKey C)', unit='MW'),
    # power_coal_retirement: F1639:AT1746, keys D,E, labels row 1638
    dict(name='power_coal_retirement', rows=(1639, 1746), cols=(6, 46), key_cols=[4, 5], label_row=1638, keys=['country', 'country_name'], label='year', desc='Planned retirement of coal power plants (Global Coal Plant Tracker)', unit='MW'),
    # power_coal_retirement_avg_flag: F1750:F1857, keys D,E, labels row 1749
    dict(name='power_coal_retirement_avg_flag', rows=(1750, 1857), cols=(6, 6), key_cols=[4, 5], label_row=1749, keys=['country', 'country_name'], label='variable', desc='Averaged coal retirement data: data-available flag (PowPrFlag F1750:F1857)', unit=''),
    # power_coal_retirement_avg: G1750:AT1857, keys D,E, labels row 1749
    dict(name='power_coal_retirement_avg', rows=(1750, 1857), cols=(7, 46), key_cols=[4, 5], label_row=1749, keys=['country', 'country_name'], label='year', desc='Averaged coal retirement data used in the model (PowPr G1750:BD1857, PowPrKey D)', unit='MW'),
    # power_storage_eur: F1884:BD1895, keys C,D,E, labels row 1883
    dict(name='power_storage_eur', rows=(1884, 1895), cols=(6, 56), key_cols=[3, 4, 5], label_row=1883, keys=['technology', 'parameter', 'unit'], label='year', desc='Battery storage, battery interface and water electrolysis cost paths, EUR (PowBatYr row 1883)', unit='per row (E)'),
    # power_storage_conversion: D1896:D1898, keys C, labels row 1883
    dict(name='power_storage_conversion', rows=(1896, 1898), cols=(4, 4), key_cols=[3], label_row=1883, keys=['item'], label='variable', desc='Storage conversion factors: EUR 2015->2021, EUR->USD 2021, H2/E', unit='factor', labels={4: 'value'}),
    # power_storage_usd: F1899:BD1914, keys C,D,E, labels row 1898
    dict(name='power_storage_usd', rows=(1899, 1914), cols=(6, 56), key_cols=[3, 4, 5], label_row=1898, keys=['technology', 'parameter', 'unit'], label='year', desc='Battery storage, battery interface, water electrolysis and storage tank cost paths, USD (rows 1899-1911 read by Inputs_ppath)', unit='per row (E)'),
    # power_min_growth_rate: H1919:H1919, keys G, labels row 1918
    dict(name='power_min_growth_rate', rows=(1919, 1919), cols=(8, 8), key_cols=[7], label_row=1918, keys=['item'], label='variable', desc='Minimum growth rate for the MW capacity growth table', unit='1/year', labels={8: 'value'}),
    # power_re_growth: D1922:J2335, keys A,B,C, labels row 1921
    dict(name='power_re_growth', rows=(1922, 2335), cols=(4, 10), key_cols=[1, 2, 3], label_row=1921, keys=['code', 'country', 'technology'], label='variable', desc='Maximum and average MW capacity growth of solar and wind by country (Energy GP calculation)', unit='MW, 1/year'),
    # power_re_max_scaleup: C2349:C2570, keys A,B, labels row 2348
    dict(name='power_re_max_scaleup', rows=(2349, 2570), cols=(3, 3), key_cols=[1, 2], label_row=2348, keys=['country_name', 'country'], label='variable', desc='Historical country max RE scale-up (solar/wind max investment; PowScB B2349:B2570, PowScC C)', unit='1/year'),
    # power_re_gen_share_limit: E2573:Z4792, keys A,B,C,D, labels row 2572
    dict(name='power_re_gen_share_limit', rows=(2573, 4792), cols=(5, 26), key_cols=[1, 2, 3, 4], label_row=2572, keys=['code', 'country', 'technology', 'carbon_price_level'], label='year', desc='Generation share addition limit by country, technology and carbon price level, 2019-2040', unit='share'),
    # power_wacc_previous: B4797:C4985, keys A, labels row 4796
    dict(name='power_wacc_previous', rows=(4797, 4985), cols=(2, 3), key_cols=[1], label_row=4796, keys=['country_name'], label='variable', desc='(Previous) WACC data: region and default WACC by country', unit='1'),
  ],
  'legacy_CoC_cells.csv': [
    # coc_as_of_date: B18:B18, keys A, labels row 17
    dict(name='coc_as_of_date', rows=(18, 18), cols=(2, 2), key_cols=[1], label_row=17, keys=['item'], label='variable', desc='As-of date of the CoC data', unit='year', labels={2: 'value'}),
    # coc_us_rates: B24:F36, keys A, labels row 23
    dict(name='coc_us_rates', rows=(24, 36), cols=(2, 6), key_cols=[1], label_row=23, keys=['year'], label='variable', desc='US market yield (10y), real risk-free rate, US GDP deflator (WEO), 10-year average inflation by year', unit=''),
    # coc_country_parameters: C41:J198, keys A,B, labels row 40
    dict(name='coc_country_parameters', rows=(41, 198), cols=(3, 10), key_cols=[1, 2], label_row=40, keys=['country_name', 'code'], label='variable', desc='Fixed CoC data by country: region, default spread, equity and country risk premia, tax rate, beta, equity weight, lender margin (row 198 = Default)', unit='1'),
    # coc_rating: C202:C390, keys A,B, labels row 201
    dict(name='coc_rating', rows=(202, 390), cols=(3, 3), key_cols=[1, 2], label_row=201, keys=['country_name', 'code'], label='variable', desc='S&P rating by country (CoCC C202:C390)', unit=''),
    # coc_real_wacc: D202:V390, keys A,B, labels row 201
    dict(name='coc_real_wacc', rows=(202, 390), cols=(4, 22), key_cols=[1, 2], label_row=201, keys=['country_name', 'code'], label='year', desc='Real WACC by country, 2022-2040 (CoCD D202:D390 = 2022)', unit='1'),
    # coc_tech_adjustment: Y203:AB211, keys X, labels row 202
    dict(name='coc_tech_adjustment', rows=(203, 211), cols=(25, 28), key_cols=[24], label_row=202, keys=['technology'], label='income_group', desc='WACC technology adjustment (Hatt) by technology and income group (CoCAdj Y203:AB211)', unit='1'),
  ],
  'legacy_GHGs_cells.csv': [
    # ghg_inventory_category: G8:G947, keys C,D,E, labels row 7
    dict(name='ghg_inventory_category', rows=(8, 947), cols=(7, 7), key_cols=[3, 4, 5], label_row=7, keys=['country_name', 'iso', 'year'], label='variable', desc='UNFCCC category (AI / NAI) of each inventory row', unit=''),
    # ghg_inventory_energy: H8:L947, keys C,D,E, labels row 7
    dict(name='ghg_inventory_energy', rows=(8, 947), cols=(8, 12), key_cols=[3, 4, 5], label_row=7, keys=['country_name', 'iso', 'year'], label='gas', desc='GHG inventory by gas, sector group "energy" (legacy row 6 group header; GHGVal H8:AZ947)', unit='MtCO2e'),
    # ghg_inventory_ippu: M8:Q947, keys C,D,E, labels row 7
    dict(name='ghg_inventory_ippu', rows=(8, 947), cols=(13, 17), key_cols=[3, 4, 5], label_row=7, keys=['country_name', 'iso', 'year'], label='gas', desc='GHG inventory by gas, sector group "ippu" (legacy row 6 group header; GHGVal H8:AZ947)', unit='MtCO2e'),
    # ghg_inventory_agriculture: R8:V947, keys C,D,E, labels row 7
    dict(name='ghg_inventory_agriculture', rows=(8, 947), cols=(18, 22), key_cols=[3, 4, 5], label_row=7, keys=['country_name', 'iso', 'year'], label='gas', desc='GHG inventory by gas, sector group "agriculture" (legacy row 6 group header; GHGVal H8:AZ947)', unit='MtCO2e'),
    # ghg_inventory_lulucf: W8:AA947, keys C,D,E, labels row 7
    dict(name='ghg_inventory_lulucf', rows=(8, 947), cols=(23, 27), key_cols=[3, 4, 5], label_row=7, keys=['country_name', 'iso', 'year'], label='gas', desc='GHG inventory by gas, sector group "lulucf" (legacy row 6 group header; GHGVal H8:AZ947)', unit='MtCO2e'),
    # ghg_inventory_waste: AB8:AF947, keys C,D,E, labels row 7
    dict(name='ghg_inventory_waste', rows=(8, 947), cols=(28, 32), key_cols=[3, 4, 5], label_row=7, keys=['country_name', 'iso', 'year'], label='gas', desc='GHG inventory by gas, sector group "waste" (legacy row 6 group header; GHGVal H8:AZ947)', unit='MtCO2e'),
    # ghg_inventory_other: AG8:AK947, keys C,D,E, labels row 7
    dict(name='ghg_inventory_other', rows=(8, 947), cols=(33, 37), key_cols=[3, 4, 5], label_row=7, keys=['country_name', 'iso', 'year'], label='gas', desc='GHG inventory by gas, sector group "other" (legacy row 6 group header; GHGVal H8:AZ947)', unit='MtCO2e'),
    # ghg_inventory_total_incl_lucf: AL8:AP947, keys C,D,E, labels row 7
    dict(name='ghg_inventory_total_incl_lucf', rows=(8, 947), cols=(38, 42), key_cols=[3, 4, 5], label_row=7, keys=['country_name', 'iso', 'year'], label='gas', desc='GHG inventory by gas, sector group "total_incl_lucf" (legacy row 6 group header; GHGVal H8:AZ947)', unit='MtCO2e'),
    # ghg_inventory_total_excl_lucf: AQ8:AU947, keys C,D,E, labels row 7
    dict(name='ghg_inventory_total_excl_lucf', rows=(8, 947), cols=(43, 47), key_cols=[3, 4, 5], label_row=7, keys=['country_name', 'iso', 'year'], label='gas', desc='GHG inventory by gas, sector group "total_excl_lucf" (legacy row 6 group header; GHGVal H8:AZ947)', unit='MtCO2e'),
    # ghg_inventory_memo_fugitive: AV8:AZ947, keys C,D,E, labels row 7
    dict(name='ghg_inventory_memo_fugitive', rows=(8, 947), cols=(48, 52), key_cols=[3, 4, 5], label_row=7, keys=['country_name', 'iso', 'year'], label='gas', desc='GHG inventory by gas, sector group "memo_fugitive" (legacy row 6 group header; GHGVal H8:AZ947)', unit='MtCO2e'),
    # ghg_hist_category: G955:G1189, keys C,D, labels row 954
    dict(name='ghg_hist_category', rows=(955, 1189), cols=(7, 7), key_cols=[3, 4], label_row=954, keys=['country_name', 'iso'], label='variable', desc='UNFCCC category of each historical row', unit=''),
    # ghg_hist_ghg_excl_lulucf: H955:O1189, keys C,D, labels row 954
    dict(name='ghg_hist_ghg_excl_lulucf', rows=(955, 1189), cols=(8, 15), key_cols=[3, 4], label_row=954, keys=['country_name', 'iso'], label='year', desc='Historical GHGs excluding LULUCF (GHHTab)', unit='MtCO2e'),
    # ghg_hist_ghg_incl_lulucf: P955:W1189, keys C,D, labels row 954
    dict(name='ghg_hist_ghg_incl_lulucf', rows=(955, 1189), cols=(16, 23), key_cols=[3, 4], label_row=954, keys=['country_name', 'iso'], label='year', desc='Historical GHGs including LULUCF', unit='MtCO2e'),
    # ghg_hist_co2_excl_lulucf: X955:AJ1189, keys C,D, labels row 954
    dict(name='ghg_hist_co2_excl_lulucf', rows=(955, 1189), cols=(24, 36), key_cols=[3, 4], label_row=954, keys=['country_name', 'iso'], label='year', desc='Historical CO2 excluding LULUCF', unit='MtCO2'),
    # ghg_hist_energy_co2: AK955:AU1189, keys C,D, labels row 954
    dict(name='ghg_hist_energy_co2', rows=(955, 1189), cols=(37, 47), key_cols=[3, 4], label_row=954, keys=['country_name', 'iso'], label='year', desc='Historical energy CO2', unit='MtCO2'),
    # ghg_adjustment_egypt: D1196:F1198, keys C, labels row 1195
    dict(name='ghg_adjustment_egypt', rows=(1196, 1198), cols=(4, 6), key_cols=[3], label_row=1195, keys=['item'], label='variable', desc='GHG adjustments (Egypt): modelled vs historical energy CO2 and difference', unit='MtCO2 / share'),
    # ghg_shock_eu_flag: A1202:A1388, keys B, labels row 1201
    dict(name='ghg_shock_eu_flag', rows=(1202, 1388), cols=(1, 1), key_cols=[2], label_row=1201, keys=['code'], label='variable', desc='EU member flag', unit='0/1'),
    # ghg_shock_info: C1202:F1388, keys B, labels row 1201
    dict(name='ghg_shock_info', rows=(1202, 1388), cols=(3, 6), key_cols=[2], label_row=1201, keys=['code'], label='variable', desc='Energy CO2 targets: region, country, 2023 emissions, 2024 vs 2023 change', unit='MtCO2 / share'),
    # ghg_shock: G1202:H1388, keys B, labels row 1201
    dict(name='ghg_shock', rows=(1202, 1388), cols=(7, 8), key_cols=[2], label_row=1201, keys=['code'], label='year', desc='Exogenous energy CO2 adjustments 2023-2024 of the power model (GHGShock G1202:H1388)', unit='share'),
    # ghg_shock_notes: I1202:K1388, keys B, labels row 1201
    dict(name='ghg_shock_notes', rows=(1202, 1388), cols=(9, 11), key_cols=[2], label_row=1201, keys=['code'], label='variable', desc='Notes, sequence number and GHG MATCH row of the shock rows', unit=''),
    # ghg_eu_quarterly: D1409:N1436, keys B,C, labels row 1408
    dict(name='ghg_eu_quarterly', rows=(1409, 1436), cols=(4, 14), key_cols=[2, 3], label_row=1408, keys=['code', 'name'], label='variable', desc='EU air emissions accounts (Eurostat), quarterly 2023-Q1..2024-Q3, Q1-Q3 totals and 2024 vs 2023 (row 1409 = EU27, no code)', unit='thousand tonnes / share'),
    # ghg_noneu_cpat_region: C1446:C1470, keys D,E,F,G, labels row 1445
    dict(name='ghg_noneu_cpat_region', rows=(1446, 1470), cols=(3, 3), key_cols=[4, 5, 6, 7], label_row=1445, keys=['object_id', 'country', 'iso2', 'iso3'], label='variable', desc='Non-EU quarterly estimates: CPAT region of the row', unit=''),
    # ghg_noneu_series: H1446:N1470, keys D,E,F,G, labels row 1445
    dict(name='ghg_noneu_series', rows=(1446, 1470), cols=(8, 14), key_cols=[4, 5, 6, 7], label_row=1445, keys=['object_id', 'country', 'iso2', 'iso3'], label='variable', desc='Non-EU quarterly estimates: series metadata (indicator, code, unit, source, industry, gas, scale)', unit=''),
    # ghg_noneu_quarterly: O1446:Y1470, keys D,E,F,G, labels row 1445
    dict(name='ghg_noneu_quarterly', rows=(1446, 1470), cols=(15, 25), key_cols=[4, 5, 6, 7], label_row=1445, keys=['object_id', 'country', 'iso2', 'iso3'], label='variable', desc='Non-EU quarterly CO2 2023Q1-2024Q2, Q1-Q2 totals and 2024 vs 2023', unit='Mt CO2 / share'),
    # ghg_carbon_monitor: D1480:E1488, keys C, labels row 1479
    dict(name='ghg_carbon_monitor', rows=(1480, 1488), cols=(4, 5), key_cols=[3], label_row=1479, keys=['country'], label='variable', desc='Carbon Monitor emission changes 2024 vs 2023 and 2023 vs 2022', unit='share'),
  ],
  'legacy_ECP_cells.csv': [
    # ecp_general_information: D11:L66, keys B,C, labels row 10
    dict(name='ecp_general_information', rows=(11, 66), cols=(4, 12), key_cols=[2, 3], label_row=10, keys=['country_name', 'country'], label='variable', desc='General information per initiative: carbon tax yes/no, single price, ETS yes/no, allocation, EU ETS, comments (ECPInfoCode C11:C66, ECPInfoSgl E, ECPInfoEU K)', unit='', labels={4: 'Carbon tax (Yes/No)', 6: 'ETS (Yes/No)'}),
    # ecp_tax_rate: F70:P132, keys B,C,D,E, labels row 69
    dict(name='ecp_tax_rate', rows=(70, 132), cols=(6, 16), key_cols=[2, 3, 4, 5], label_row=69, keys=['country_name', 'country', 'sector_fuel', 'code'], label='year', desc='Carbon tax rates by country and fuel (ECPAllVal F1:P3000, ECPAllKey E)', unit='$/tCO2 nominal'),
    # ecp_tax_fuel_coverage: F138:P425, keys B,C,D,E, labels row 137
    dict(name='ecp_tax_fuel_coverage', rows=(138, 425), cols=(6, 16), key_cols=[2, 3, 4, 5], label_row=137, keys=['country_name', 'country', 'sector_fuel', 'code'], label='year', desc='Fuel coverage of carbon taxes (ECPAllVal F1:P3000, ECPAllKey E)', unit='share'),
    # ecp_tax_sector_coverage: F430:P557, keys B,C,D,E, labels row 429
    dict(name='ecp_tax_sector_coverage', rows=(430, 557), cols=(6, 16), key_cols=[2, 3, 4, 5], label_row=429, keys=['country_name', 'country', 'sector_fuel', 'code'], label='year', desc='Sectoral coverage of carbon taxes (ECPAllVal F1:P3000, ECPAllKey E)', unit='share'),
    # ecp_tax_revenue: F562:P594, keys B,C,D,E, labels row 561
    dict(name='ecp_tax_revenue', rows=(562, 594), cols=(6, 16), key_cols=[2, 3, 4, 5], label_row=561, keys=['country_name', 'country', 'sector_fuel', 'code'], label='year', desc='Carbon tax revenues collected (ECPAllVal F1:P3000, ECPAllKey E)', unit='mln USD nominal'),
    # ecp_ets_price_national: F602:P614, keys B,C,D,E, labels row 600
    dict(name='ecp_ets_price_national', rows=(602, 614), cols=(6, 16), key_cols=[2, 3, 4, 5], label_row=600, keys=['country_name', 'country', 'sector_fuel', 'code'], label='year', desc='ETS permit price, national ETS (ECPAllVal F1:P3000, ECPAllKey E)', unit='$/tCO2 nominal'),
    # ecp_ets_price_regional: F616:P617, keys B,C,D,E, labels row 600
    dict(name='ecp_ets_price_regional', rows=(616, 617), cols=(6, 16), key_cols=[2, 3, 4, 5], label_row=600, keys=['country_name', 'country', 'sector_fuel', 'code'], label='year', desc='ETS permit price, regional ETS (ECPAllVal F1:P3000, ECPAllKey E)', unit='$/tCO2 nominal'),
    # ecp_ets_fuel_coverage_national: F621:P737, keys B,C,D,E, labels row 619
    dict(name='ecp_ets_fuel_coverage_national', rows=(621, 737), cols=(6, 16), key_cols=[2, 3, 4, 5], label_row=619, keys=['country_name', 'country', 'sector_fuel', 'code'], label='year', desc='Fuel coverage of national ETS (ECPAllVal F1:P3000, ECPAllKey E)', unit='share'),
    # ecp_ets_fuel_coverage_regional: F739:P1037, keys B,C,D,E, labels row 619
    dict(name='ecp_ets_fuel_coverage_regional', rows=(739, 1037), cols=(6, 16), key_cols=[2, 3, 4, 5], label_row=619, keys=['country_name', 'country', 'sector_fuel', 'code'], label='year', desc='Fuel coverage of regional ETS (EU ETS by member) (ECPAllVal F1:P3000, ECPAllKey E)', unit='share'),
    # ecp_ets_sector_coverage_national: F1042:P1093, keys B,C,D,E, labels row 1040
    dict(name='ecp_ets_sector_coverage_national', rows=(1042, 1093), cols=(6, 16), key_cols=[2, 3, 4, 5], label_row=1040, keys=['country_name', 'country', 'sector_fuel', 'code'], label='year', desc='Sector coverage of national ETS (ECPAllVal F1:P3000, ECPAllKey E)', unit='share'),
    # ecp_ets_sector_coverage_regional: F1095:P1224, keys B,C,D,E, labels row 1040
    dict(name='ecp_ets_sector_coverage_regional', rows=(1095, 1224), cols=(6, 16), key_cols=[2, 3, 4, 5], label_row=1040, keys=['country_name', 'country', 'sector_fuel', 'code'], label='year', desc='Sector coverage of regional ETS (ECPAllVal F1:P3000, ECPAllKey E)', unit='share'),
    # ecp_ets_revenue_national: F1228:P1240, keys B,C,D,E, labels row 1226
    dict(name='ecp_ets_revenue_national', rows=(1228, 1240), cols=(6, 16), key_cols=[2, 3, 4, 5], label_row=1226, keys=['country_name', 'country', 'sector_fuel', 'code'], label='year', desc='ETS revenues collected, national ETS (ECPAllVal F1:P3000, ECPAllKey E)', unit='mln USD nominal'),
    # ecp_ets_revenue_regional: F1242:P1275, keys B,C,D,E, labels row 1226
    dict(name='ecp_ets_revenue_regional', rows=(1242, 1275), cols=(6, 16), key_cols=[2, 3, 4, 5], label_row=1226, keys=['country_name', 'country', 'sector_fuel', 'code'], label='year', desc='ETS revenues collected, regional ETS (ECPAllVal F1:P3000, ECPAllKey E)', unit='mln USD nominal'),
    # ecp_ets_free_allocation_national: F1278:P1290, keys B,C,D,E, labels row 1277
    dict(name='ecp_ets_free_allocation_national', rows=(1278, 1290), cols=(6, 16), key_cols=[2, 3, 4, 5], label_row=1277, keys=['country_name', 'country', 'sector_fuel', 'code'], label='year', desc='Share of free allocations, national ETS (ECPAllVal F1:P3000, ECPAllKey E)', unit='share'),
    # ecp_ets_free_allocation_regional: F1292:P1392, keys B,C,D,E, labels row 1277
    dict(name='ecp_ets_free_allocation_regional', rows=(1292, 1392), cols=(6, 16), key_cols=[2, 3, 4, 5], label_row=1277, keys=['country_name', 'country', 'sector_fuel', 'code'], label='year', desc='Share of free allocations, regional ETS (ECPAllVal F1:P3000, ECPAllKey E)', unit='share'),
  ],
  'legacy_ETS+LTS_cells.csv': [
    # ets_assumptions: E6:H9, keys A, labels row 5
    dict(name='ets_assumptions', rows=(6, 9), cols=(5, 8), key_cols=[1], label_row=5, keys=['assumption'], label='case', desc='ETS assumptions by case (price volatility, abatement cost increase, policy change volatility, relative abatement cost)', unit='1'),
    # ets_ctax_policy_risk: C11:C11, keys A, labels row 10
    dict(name='ets_ctax_policy_risk', rows=(11, 11), cols=(3, 3), key_cols=[1], label_row=10, keys=['item'], label='variable', desc='Carbon tax policy risk setting', unit='', labels={3: 'value'}),
    # ets_relative_effectiveness: A14:B14, keys -, labels row 13
    dict(name='ets_relative_effectiveness', rows=(14, 14), cols=(1, 2), key_cols=[], label_row=13, keys=[], label='variable', desc='Relative effectiveness (auctioning, output-based)', unit='1'),
    # ets_fuel_codes: C19:C26, keys B, labels row 18
    dict(name='ets_fuel_codes', rows=(19, 26), cols=(3, 3), key_cols=[2], label_row=18, keys=['fuel'], label='variable', desc='Fuel codes', unit=''),
    # ets_unit_codes: C30:C36, keys B, labels row 29
    dict(name='ets_unit_codes', rows=(30, 36), cols=(3, 3), key_cols=[2], label_row=29, keys=['unit'], label='variable', desc='Fuel unit codes', unit=''),
    # ets_fuel_units: C39:E46, keys B, labels row 38
    dict(name='ets_fuel_units', rows=(39, 46), cols=(3, 5), key_cols=[2], label_row=38, keys=['fuel'], label='variable', desc='Price units per fuel', unit='', labels={3: 'unit_1', 4: 'unit_2', 5: 'unit_3'}),
    # ets_emission_factors: C49:D73, keys B, labels row 48
    dict(name='ets_emission_factors', rows=(49, 73), cols=(3, 4), key_cols=[2], label_row=48, keys=['code'], label='variable', desc='CO2 emission factors by fuel.unit code', unit='tCO2 per unit (column D)'),
    # ets_cap_calculator: O30:O34, keys K, labels row 38
    dict(name='ets_cap_calculator', rows=(30, 34), cols=(15, 15), key_cols=[11], label_row=38, keys=['item'], label='variable', desc='Cap relative to baseline calculator', unit='', labels={15: 'value'}),
    # ets_semi_el_raw_1: P17:S37, keys T, labels row 40
    dict(name='ets_semi_el_raw_1', rows=(17, 37), cols=(16, 19), key_cols=[20], label_row=40, keys=['country'], label='sector', desc='Semi-elasticities by sector (raw), part above the header row 40 (country names in O are not keys: O30:O34 hold the cap calculator)', unit='1/($/tCO2)'),
    # ets_semi_el_floor_1: U17:X37, keys T, labels row 40
    dict(name='ets_semi_el_floor_1', rows=(17, 37), cols=(21, 24), key_cols=[20], label_row=40, keys=['country'], label='sector', desc='Semi-elasticities by sector with the minimum applied, part above row 40', unit='1/($/tCO2)'),
    # ets_semi_el_raw_2: P41:S131, keys O,T, labels row 40
    dict(name='ets_semi_el_raw_2', rows=(41, 131), cols=(16, 19), key_cols=[15, 20], label_row=40, keys=['country_name', 'country'], label='sector', desc='Semi-elasticities by sector (raw), rows 41-131', unit='1/($/tCO2)'),
    # ets_semi_el_floor_2: U41:X131, keys O,T, labels row 40
    dict(name='ets_semi_el_floor_2', rows=(41, 131), cols=(21, 24), key_cols=[15, 20], label_row=40, keys=['country_name', 'country'], label='sector', desc='Semi-elasticities by sector with the minimum applied, rows 41-131', unit='1/($/tCO2)'),
    # ets_min_semi_elasticity: D76:D76, keys B, labels row 75
    dict(name='ets_min_semi_elasticity', rows=(76, 76), cols=(4, 4), key_cols=[2], label_row=75, keys=['item'], label='variable', desc='Minimum semi-elasticity', unit='1/($/tCO2)', labels={4: 'value'}),
    # ets_semi_el_minima: D79:G79, keys B, labels row 80
    dict(name='ets_semi_el_minima', rows=(79, 79), cols=(4, 7), key_cols=[2], label_row=80, keys=['item'], label='sector', desc='Minima of the semi-elasticities by sector', unit='1/($/tCO2)'),
    # ets_semi_elasticities: D82:H256, keys B,C, labels row 81
    dict(name='ets_semi_elasticities', rows=(82, 256), cols=(4, 8), key_cols=[2, 3], label_row=81, keys=['country_name', 'country'], label='sector', desc='Semi-elasticities of emissions to the carbon price by country and sector (ETSSemiKey C82:C400, ETSSemiVal D82:G400)', unit='1/($/tCO2)'),
    # ets_mitigation_investment: C261:H302, keys A,B, labels row 260
    dict(name='ets_mitigation_investment', rows=(261, 302), cols=(3, 8), key_cols=[1, 2], label_row=260, keys=['country', 'country_name'], label='variable', desc='Mitigation investment needs (constant 2020 USD bn) and share of GDP', unit='$2020 bn / share'),
  ],
  'legacy_Multipliers_cells.csv': [
    # mult_source_selected: C18:C18, keys B, labels row 17
    dict(name='mult_source_selected', rows=(18, 18), cols=(3, 3), key_cols=[2], label_row=17, keys=['item'], label='variable', desc='Multiplier source selected', unit='', labels={3: 'value'}),
    # mult_settings: C19:E22, keys B, labels row 17
    dict(name='mult_settings', rows=(19, 22), cols=(3, 5), key_cols=[2], label_row=17, keys=['item'], label='variable', desc='Multiplier selection: country, source, category, range with their indices', unit='', labels={3: 'value', 4: 'index', 5: 'index_2'}),
    # mult_manual_used: D26:S33, keys B,C, labels row 25
    dict(name='mult_manual_used', rows=(26, 33), cols=(4, 19), key_cols=[2, 3], label_row=25, keys=['instrument', 'instrument_name'], label='lag', desc='Manual multiplier (used) by instrument and lag (years)', unit='1'),
    # mult_base: D38:S45, keys B,C, labels row 37
    dict(name='mult_base', rows=(38, 45), cols=(4, 19), key_cols=[2, 3], label_row=37, keys=['instrument', 'instrument_name'], label='lag', desc='Base multiplier by instrument and lag (years)', unit='1'),
    # mult_plus_adjustment: D50:S57, keys B,C, labels row 49
    dict(name='mult_plus_adjustment', rows=(50, 57), cols=(4, 19), key_cols=[2, 3], label_row=49, keys=['instrument', 'instrument_name'], label='lag', desc='Plus adjustment by instrument and lag (years)', unit='1'),
    # mult_fiscal_used: D62:S69, keys B,C, labels row 61
    dict(name='mult_fiscal_used', rows=(62, 69), cols=(4, 19), key_cols=[2, 3], label_row=61, keys=['instrument', 'instrument_name'], label='lag', desc='Fiscal multipliers used (effect of revenue / expenditure) by instrument and lag (years)', unit='1'),
    # mult_manual_source: D76:S83, keys B,C, labels row 75
    dict(name='mult_manual_source', rows=(76, 83), cols=(4, 19), key_cols=[2, 3], label_row=75, keys=['instrument', 'instrument_name'], label='lag', desc="Source data from 'Manual inputs' by instrument and lag (years)", unit='1'),
    # mult_mfmod_median_global: D92:O99, keys B,C, labels row 91
    dict(name='mult_mfmod_median_global', rows=(92, 99), cols=(4, 15), key_cols=[2, 3], label_row=91, keys=['instrument', 'instrument_name'], label='lag', desc='MFMOD median, global by instrument and lag (years)', unit='1'),
    # mult_mfmod_median_hic: D103:O110, keys B,C, labels row 102
    dict(name='mult_mfmod_median_hic', rows=(103, 110), cols=(4, 15), key_cols=[2, 3], label_row=102, keys=['instrument', 'instrument_name'], label='lag', desc='MFMOD median, HIC by instrument and lag (years)', unit='1'),
    # mult_mfmod_median_umic: D115:O122, keys B,C, labels row 114
    dict(name='mult_mfmod_median_umic', rows=(115, 122), cols=(4, 15), key_cols=[2, 3], label_row=114, keys=['instrument', 'instrument_name'], label='lag', desc='MFMOD median, UMIC by instrument and lag (years)', unit='1'),
    # mult_mfmod_median_lmic: D126:O133, keys B,C, labels row 125
    dict(name='mult_mfmod_median_lmic', rows=(126, 133), cols=(4, 15), key_cols=[2, 3], label_row=125, keys=['instrument', 'instrument_name'], label='lag', desc='MFMOD median, LMIC by instrument and lag (years)', unit='1'),
    # mult_mfmod_median_lic: D137:O144, keys B,C, labels row 136
    dict(name='mult_mfmod_median_lic', rows=(137, 144), cols=(4, 15), key_cols=[2, 3], label_row=136, keys=['instrument', 'instrument_name'], label='lag', desc='MFMOD median, LIC by instrument and lag (years)', unit='1'),
    # mult_mfmod_sd_global: D151:O158, keys B,C, labels row 150
    dict(name='mult_mfmod_sd_global', rows=(151, 158), cols=(4, 15), key_cols=[2, 3], label_row=150, keys=['instrument', 'instrument_name'], label='lag', desc='MFMOD standard deviation, global by instrument and lag (years)', unit='1'),
    # mult_mfmod_sd_hic: D162:O169, keys B,C, labels row 161
    dict(name='mult_mfmod_sd_hic', rows=(162, 169), cols=(4, 15), key_cols=[2, 3], label_row=161, keys=['instrument', 'instrument_name'], label='lag', desc='MFMOD standard deviation, HIC by instrument and lag (years)', unit='1'),
    # mult_mfmod_sd_umic: D174:O181, keys B,C, labels row 173
    dict(name='mult_mfmod_sd_umic', rows=(174, 181), cols=(4, 15), key_cols=[2, 3], label_row=173, keys=['instrument', 'instrument_name'], label='lag', desc='MFMOD standard deviation, UMIC by instrument and lag (years)', unit='1'),
    # mult_mfmod_sd_lmic: D185:O192, keys B,C, labels row 184
    dict(name='mult_mfmod_sd_lmic', rows=(185, 192), cols=(4, 15), key_cols=[2, 3], label_row=184, keys=['instrument', 'instrument_name'], label='lag', desc='MFMOD standard deviation, LMIC by instrument and lag (years)', unit='1'),
    # mult_mfmod_sd_lic: D196:O203, keys B,C, labels row 195
    dict(name='mult_mfmod_sd_lic', rows=(196, 203), cols=(4, 15), key_cols=[2, 3], label_row=195, keys=['instrument', 'instrument_name'], label='lag', desc='MFMOD standard deviation, LIC by instrument and lag (years)', unit='1'),
    # mult_estimated_fuel_tax: D210:O408, keys B,C, labels row 209
    dict(name='mult_estimated_fuel_tax', rows=(210, 408), cols=(4, 15), key_cols=[2, 3], label_row=209, keys=['n', 'country'], label='lag', desc='Estimated country multipliers, fuel tax, by lag (MultC C1:C1700, MultD D1:O1700)', unit='1'),
    # mult_estimated_labor_tax: D412:O610, keys B,C, labels row 411
    dict(name='mult_estimated_labor_tax', rows=(412, 610), cols=(4, 15), key_cols=[2, 3], label_row=411, keys=['n', 'country'], label='lag', desc='Estimated country multipliers, labor tax, by lag (MultC C1:C1700, MultD D1:O1700)', unit='1'),
    # mult_estimated_excise_tax: D614:O812, keys B,C, labels row 613
    dict(name='mult_estimated_excise_tax', rows=(614, 812), cols=(4, 15), key_cols=[2, 3], label_row=613, keys=['n', 'country'], label='lag', desc='Estimated country multipliers, excise tax, by lag (MultC C1:C1700, MultD D1:O1700)', unit='1'),
    # mult_estimated_public_investment: D816:O1014, keys B,C, labels row 815
    dict(name='mult_estimated_public_investment', rows=(816, 1014), cols=(4, 15), key_cols=[2, 3], label_row=815, keys=['n', 'country'], label='lag', desc='Estimated country multipliers, public investment, by lag (MultC C1:C1700, MultD D1:O1700)', unit='1'),
    # mult_estimated_public_consumption: D1018:O1216, keys B,C, labels row 1017
    dict(name='mult_estimated_public_consumption', rows=(1018, 1216), cols=(4, 15), key_cols=[2, 3], label_row=1017, keys=['n', 'country'], label='lag', desc='Estimated country multipliers, public consumption, by lag (MultC C1:C1700, MultD D1:O1700)', unit='1'),
    # mult_estimated_transfers: D1220:O1418, keys B,C, labels row 1219
    dict(name='mult_estimated_transfers', rows=(1220, 1418), cols=(4, 15), key_cols=[2, 3], label_row=1219, keys=['n', 'country'], label='lag', desc='Estimated country multipliers, transfers, by lag (MultC C1:C1700, MultD D1:O1700)', unit='1'),
    # mult_estimated_vat: D1422:O1621, keys B,C, labels row 1421
    dict(name='mult_estimated_vat', rows=(1422, 1621), cols=(4, 15), key_cols=[2, 3], label_row=1421, keys=['n', 'country'], label='lag', desc='Estimated country multipliers, vat, by lag (MultC C1:C1700, MultD D1:O1700)', unit='1'),
  ],
  'legacy_Transport3_cells.csv': [
    # transport3_range_anxiety: B5:T191, keys A,U, labels row 4
    dict(name='transport3_range_anxiety', rows=(5, 191), cols=(2, 20), key_cols=[1, 21], label_row=4, keys=['country_name', 'country_name_u'], label='variable', desc='Stored range-anxiety calibration per country (actual vs calculated EV share, 2030/2035, difference, range anxiety $/vehicle) for passenger, freight, 2-3 wheelers (RAKey A5:A700; RAPas H, RAFre N, RACyc T). Legacy header rows 1-2 are not in the extract: labels given here.', unit='$/vehicle (range anxiety), share', labels={2: 'B (no header)', 3: 'passenger|actual', 4: 'passenger|calculation', 5: 'passenger|2030', 6: 'passenger|2035', 7: 'passenger|difference', 8: 'passenger|range_anxiety', 9: 'freight|actual', 10: 'freight|calculation', 11: 'freight|2030', 12: 'freight|2035', 13: 'freight|difference', 14: 'freight|range_anxiety', 15: 'two_three_wheeler|actual', 16: 'two_three_wheeler|calculation', 17: 'two_three_wheeler|2030', 18: 'two_three_wheeler|2035', 19: 'two_three_wheeler|difference', 20: 'two_three_wheeler|range_anxiety'}),
    # transport3_range_anxiety_repeat: B192:T203, keys A,U, labels row 4
    dict(name='transport3_range_anxiety_repeat', rows=(192, 203), cols=(2, 20), key_cols=[1, 21], label_row=4, keys=['country_name', 'country_name_u'], label='variable', desc='Second set of rows for 12 countries already in rows 180-191 (differ in column B only; MATCH on RAKey finds the first)', unit='$/vehicle (range anxiety), share', labels={2: 'B (no header)', 3: 'passenger|actual', 4: 'passenger|calculation', 5: 'passenger|2030', 6: 'passenger|2035', 7: 'passenger|difference', 8: 'passenger|range_anxiety', 9: 'freight|actual', 10: 'freight|calculation', 11: 'freight|2030', 12: 'freight|2035', 13: 'freight|difference', 14: 'freight|range_anxiety', 15: 'two_three_wheeler|actual', 16: 'two_three_wheeler|calculation', 17: 'two_three_wheeler|2030', 18: 'two_three_wheeler|2035', 19: 'two_three_wheeler|difference', 20: 'two_three_wheeler|range_anxiety'}),
  ],
  'legacy_ManualInputs_cells.csv': [
    # mi_ets_settings: E7:E12, keys D, labels row 6
    dict(name='mi_ets_settings', rows=(7, 12), cols=(5, 5), key_cols=[4], label_row=6, keys=['parameter'], label='variable', desc='Advanced ETS parameters: volatility, C-tax risk, max iterations, start fresh/continue, max error', unit='', labels={5: 'value'}),
    # mi_ets_price_override: I15:AC15, keys B, labels row 14
    dict(name='mi_ets_price_override', rows=(15, 15), cols=(9, 29), key_cols=[2], label_row=14, keys=['item'], label='year', desc='Override for the ETS price (2025 onwards), real 2026 (AC14 reads "2041 (projection)")', unit='$/tCO2 real 2026', labels={29: '2041'}),
    # mi_process_emission_factors: H30:AE37, keys D,E,F,G, labels row 29
    dict(name='mi_process_emission_factors', rows=(30, 37), cols=(8, 31), key_cols=[4, 5, 6, 7], label_row=29, keys=['product', 'unit', 'cn_codes', 'route'], label='variable', desc='Process emissions (CBAM goods): scope 1/2 emission factors, EF inputs, EU defaults, notes', unit='tCO2e/t'),
    # mi_process_half_elasticity: E40:F47, keys D, labels row 39
    dict(name='mi_process_half_elasticity', rows=(40, 47), cols=(5, 6), key_cols=[4], label_row=39, keys=['process'], label='variable', desc='Process emissions half elasticity and emission reduction at $100', unit=''),
    # mi_prices_coal: I60:N75, keys B,C,D,E,G, labels row 59
    dict(name='mi_prices_coal', rows=(60, 75), cols=(9, 14), key_cols=[2, 3, 4, 5, 7], label_row=59, keys=['sector', 'fuel', 'variable', 'unit', 'code'], label='year', desc='Manual domestic energy prices and taxes, coal (ManPrKey G59:G146, ManPrVal I59:N146)', unit='per row (E)'),
    # mi_prices_natural_gas: I78:N93, keys B,C,D,E,G, labels row 77
    dict(name='mi_prices_natural_gas', rows=(78, 93), cols=(9, 14), key_cols=[2, 3, 4, 5, 7], label_row=77, keys=['sector', 'fuel', 'variable', 'unit', 'code'], label='year', desc='Manual domestic energy prices and taxes, natural gas (ManPrKey G59:G146, ManPrVal I59:N146)', unit='per row (E)'),
    # mi_prices_gasoline: I96:N99, keys B,C,D,E,G, labels row 95
    dict(name='mi_prices_gasoline', rows=(96, 99), cols=(9, 14), key_cols=[2, 3, 4, 5, 7], label_row=95, keys=['sector', 'fuel', 'variable', 'unit', 'code'], label='year', desc='Manual domestic energy prices and taxes, gasoline (ManPrKey G59:G146, ManPrVal I59:N146)', unit='per row (E)'),
    # mi_prices_diesel: I102:N105, keys B,C,D,E,G, labels row 101
    dict(name='mi_prices_diesel', rows=(102, 105), cols=(9, 14), key_cols=[2, 3, 4, 5, 7], label_row=101, keys=['sector', 'fuel', 'variable', 'unit', 'code'], label='year', desc='Manual domestic energy prices and taxes, diesel (ManPrKey G59:G146, ManPrVal I59:N146)', unit='per row (E)'),
    # mi_prices_lpg: I108:N111, keys B,C,D,E,G, labels row 107
    dict(name='mi_prices_lpg', rows=(108, 111), cols=(9, 14), key_cols=[2, 3, 4, 5, 7], label_row=107, keys=['sector', 'fuel', 'variable', 'unit', 'code'], label='year', desc='Manual domestic energy prices and taxes, lpg (ManPrKey G59:G146, ManPrVal I59:N146)', unit='per row (E)'),
    # mi_prices_kerosene: I114:N117, keys B,C,D,E,G, labels row 113
    dict(name='mi_prices_kerosene', rows=(114, 117), cols=(9, 14), key_cols=[2, 3, 4, 5, 7], label_row=113, keys=['sector', 'fuel', 'variable', 'unit', 'code'], label='year', desc='Manual domestic energy prices and taxes, kerosene (ManPrKey G59:G146, ManPrVal I59:N146)', unit='per row (E)'),
    # mi_prices_biomass: I120:N125, keys B,C,D,E,G, labels row 119
    dict(name='mi_prices_biomass', rows=(120, 125), cols=(9, 14), key_cols=[2, 3, 4, 5, 7], label_row=119, keys=['sector', 'fuel', 'variable', 'unit', 'code'], label='year', desc='Manual domestic energy prices and taxes, biomass (ManPrKey G59:G146, ManPrVal I59:N146)', unit='per row (E)'),
    # mi_prices_oil: I128:N133, keys B,C,D,E,G, labels row 127
    dict(name='mi_prices_oil', rows=(128, 133), cols=(9, 14), key_cols=[2, 3, 4, 5, 7], label_row=127, keys=['sector', 'fuel', 'variable', 'unit', 'code'], label='year', desc='Manual domestic energy prices and taxes, oil (ManPrKey G59:G146, ManPrVal I59:N146)', unit='per row (E)'),
    # mi_prices_electricity: I136:N146, keys B,C,D,E,G, labels row 135
    dict(name='mi_prices_electricity', rows=(136, 146), cols=(9, 14), key_cols=[2, 3, 4, 5, 7], label_row=135, keys=['sector', 'fuel', 'variable', 'unit', 'code'], label='year', desc='Manual domestic energy prices and taxes, electricity (ManPrKey G59:G146, ManPrVal I59:N146)', unit='per row (E)'),
    # mi_excise_reform: J150:BU163, keys B,C,D,E,G, labels row 149
    dict(name='mi_excise_reform', rows=(150, 163), cols=(10, 73), key_cols=[2, 3, 4, 5, 7], label_row=149, keys=['fuel', 'sector', 'variable', 'unit', 'code'], label='year', desc='Additional excise tax (ManExcKey G150:G163, ManExcVal J150:AF163)', unit='per row (E), real 2026'),
    # mi_price_controls: J167:J180, keys B,C,D,G, labels row 166
    dict(name='mi_price_controls', rows=(167, 180), cols=(10, 10), key_cols=[2, 3, 4, 7], label_row=166, keys=['fuel', 'sector', 'variable', 'code'], label='variable', desc='Retail price control pass-through by code (PCtrlKey G167:G180, PCtrlVal J)', unit='share', labels={10: 'pass_through'}),
    # mi_methane_fee: J185:L200, keys C,F, labels row 184
    dict(name='mi_methane_fee', rows=(185, 200), cols=(10, 12), key_cols=[3, 6], label_row=184, keys=['parameter', 'unit'], label='variable', desc='Methane fee inputs: intensity reduction, demand elasticity, pass-through, fee scope by source (J196:J200)', unit='', labels={10: 'value', 12: 'note'}),
    # mi_passthrough: F207:BU215, keys D,E, labels row 205
    dict(name='mi_passthrough', rows=(207, 215), cols=(6, 73), key_cols=[4, 5], label_row=205, keys=['fuel', 'fuel_code'], label='gtap_sector', desc='Market-induced imperfect pass-through coefficients by fuel and GTAP sector (row 205; the CPAT sector of row 206 repeats, so it stays in the layout; BS-BU are #N/A in both header rows)', unit='share', labels={71: 'BS (#N/A)', 72: 'BT (#N/A)', 73: 'BU (#N/A)'}),
    # mi_intl_prices: J221:AF225, keys D,E, labels row 220
    dict(name='mi_intl_prices', rows=(221, 225), cols=(10, 32), key_cols=[4, 5], label_row=220, keys=['commodity', 'unit'], label='year', desc='Manual international energy price forecasts (PIntManVal J221:AF225)', unit='per row (E)'),
    # mi_gdp_forecast: J231:BU231, keys D,E, labels row 230
    dict(name='mi_gdp_forecast', rows=(231, 231), cols=(10, 73), key_cols=[4, 5], label_row=230, keys=['item', 'unit'], label='year', desc='Manual GDP forecasts', unit='% change'),
    # mi_scc: J237:AF240, keys D,E, labels row 236
    dict(name='mi_scc', rows=(237, 240), cols=(10, 32), key_cols=[4, 5], label_row=236, keys=['item', 'unit'], label='year', desc='Social cost of carbon, national (row 237, SCCManVal) and global (row 240)', unit='$/tCO2'),
    # mi_scc_global_parameters: F238:F239, keys D, labels row 236
    dict(name='mi_scc_global_parameters', rows=(238, 239), cols=(6, 6), key_cols=[4], label_row=236, keys=['item'], label='variable', desc='Global SCC level (2018 US$/t) and real growth rate', unit='', labels={6: 'value'}),
    # mi_pm25_apportionment: F247:F254, keys D, labels row 246
    dict(name='mi_pm25_apportionment', rows=(247, 254), cols=(6, 6), key_cols=[4], label_row=246, keys=['source'], label='variable', desc='PM2.5 source apportionment (contribution by source)', unit='share'),
    # mi_multipliers: J261:U268, keys D,E, labels row 260
    dict(name='mi_multipliers', rows=(261, 268), cols=(10, 21), key_cols=[4, 5], label_row=260, keys=['instrument', 'instrument_name'], label='lag', desc='Manual fiscal multipliers by instrument and lag (MultMan J261:U268)', unit='1'),
    # mi_income_elasticities: K279:N286, keys D,H, labels row 277
    dict(name='mi_income_elasticities', rows=(279, 286), cols=(11, 14), key_cols=[4, 8], label_row=277, keys=['item', 'code'], label='sector', desc='Manual income elasticities of demand by fuel and sector', unit='1'),
    # mi_price_elasticities: K291:N307, keys D,H, labels row 289
    dict(name='mi_price_elasticities', rows=(291, 307), cols=(11, 14), key_cols=[4, 8], label_row=289, keys=['item', 'code'], label='sector', desc='Manual own-price elasticities (usage rows 291-298, efficiency rows 300-307) by fuel and sector', unit='1'),
    # mi_price_elasticities_total: K309:N316, keys D, labels row 289
    dict(name='mi_price_elasticities_total', rows=(309, 316), cols=(11, 14), key_cols=[4], label_row=289, keys=['item'], label='sector', desc='Memo: implied total demand elasticities by fuel and sector', unit='1'),
    # mi_substitution_elasticities: K319:N321, keys D,H, labels row 318
    dict(name='mi_substitution_elasticities', rows=(319, 321), cols=(11, 14), key_cols=[4, 8], label_row=318, keys=['item', 'code'], label='sector', desc='Manual substitution elasticities', unit='1'),
    # mi_nonenergy_elasticities: K326:M327, keys D, labels row 325
    dict(name='mi_nonenergy_elasticities', rows=(326, 327), cols=(11, 13), key_cols=[4], label_row=325, keys=['item'], label='sector', desc='Population and per-capita income elasticities of non-energy GHGs (GhgElCat K325:M325, GhgElPop, GhgElInc)', unit='1'),
    # mi_additional_mitigation: J335:AA340, keys D,E, labels row 334
    dict(name='mi_additional_mitigation', rows=(335, 340), cols=(10, 27), key_cols=[4, 5], label_row=334, keys=['sector', 'unit'], label='year', desc='Additional mitigation effort (non-energy) by GHG-emitting sector', unit='%'),
    # mi_capacity_baseline_used: F349:F357, keys C,D,E,G, labels row 348
    dict(name='mi_capacity_baseline_used', rows=(349, 357), cols=(6, 6), key_cols=[3, 4, 5, 7], label_row=348, keys=['scenario', 'technology', 'technology_name', 'code'], label='variable', desc='Manual capacity, baseline: whether used', unit=''),
    # mi_capacity_baseline: J349:AO357, keys C,D,E,G, labels row 348
    dict(name='mi_capacity_baseline', rows=(349, 357), cols=(10, 41), key_cols=[3, 4, 5, 7], label_row=348, keys=['scenario', 'technology', 'technology_name', 'code'], label='year', desc='Manual new investment in power capacity, baseline (ManCapVal J349:AO371)', unit='MW'),
    # mi_capacity_policy_used: F363:F371, keys C,D,E,G, labels row 362
    dict(name='mi_capacity_policy_used', rows=(363, 371), cols=(6, 6), key_cols=[3, 4, 5, 7], label_row=362, keys=['scenario', 'technology', 'technology_name', 'code'], label='variable', desc='Manual capacity, policy scenario: whether used', unit=''),
    # mi_capacity_policy: J363:AO371, keys C,D,E,G, labels row 362
    dict(name='mi_capacity_policy', rows=(363, 371), cols=(10, 41), key_cols=[3, 4, 5, 7], label_row=362, keys=['scenario', 'technology', 'technology_name', 'code'], label='year', desc='Manual new investment in power capacity, policy scenario', unit='MW'),
    # mi_ev_fuel_economy: J375:AC377, keys D,F, labels row 374
    dict(name='mi_ev_fuel_economy', rows=(375, 377), cols=(10, 29), key_cols=[4, 6], label_row=374, keys=['vehicle', 'unit'], label='year', desc='Fuel economy of new EVs (BEVFEVal J375:AC377, BEVFELab D375:D377)', unit='km per kWh'),
    # mi_ev_fuel_economy_growth: K378:T378, keys -, labels row 374
    dict(name='mi_ev_fuel_economy_growth', rows=(378, 378), cols=(11, 20), key_cols=[], label_row=374, keys=[], label='year', desc='Row 378: annual growth factor of the EV fuel economy (no row label in legacy)', unit='factor'),
  ],
}


CELL_HEADER = ['row', 'col', 'value']

CELLS = {
    'legacy_Countries_cells.csv': dict(tidy='countries_tab', sheet='Countries', first_row=3, header=CELL_HEADER, blocks=[]),
    'legacy_Elasticities_cells.csv': dict(tidy='elasticities_tab', sheet='Elasticities', first_row=3, header=CELL_HEADER, blocks=[]),
    'legacy_Prices_int_cells.csv': dict(tidy='prices_int_tab', sheet='Prices_int', first_row=3, header=CELL_HEADER, blocks=[]),
    'legacy_Power_cells.csv': dict(tidy='power_tab', sheet='Power', first_row=3, header=CELL_HEADER, blocks=[]),
    'legacy_CoC_cells.csv': dict(tidy='coc_tab', sheet='CoC', first_row=3, header=CELL_HEADER, blocks=[]),
    'legacy_GHGs_cells.csv': dict(tidy='ghgs_tab', sheet='GHGs', first_row=3, header=CELL_HEADER, blocks=[]),
    'legacy_ECP_cells.csv': dict(tidy='ecp_tab', sheet='ECP', first_row=3, header=CELL_HEADER, blocks=[]),
    'legacy_ETS+LTS_cells.csv': dict(tidy='ets_lts_tab', sheet='ETS+LTS', first_row=3, header=CELL_HEADER, blocks=[]),
    'legacy_Multipliers_cells.csv': dict(tidy='multipliers_tab', sheet='Multipliers', first_row=3, header=CELL_HEADER, blocks=[]),
    'legacy_Transport3_cells.csv': dict(tidy='transport3_tab', sheet='Transport3', first_row=5, header=CELL_HEADER, blocks=[]),
    'legacy_ManualInputs_cells.csv': dict(tidy='manual_inputs_tab', sheet='Manual inputs', first_row=3,
                                          header=CELL_HEADER + ['formula'], blocks=[]),
}

for _file, _spec in CELLS.items():
    _spec['blocks'] = BLOCKS.get(_file, [])
