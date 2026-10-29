"""What each legacy table becomes in tidy form (read by tidy_convert.py).

Two kinds of legacy source (data/INTERFACE.md section 3):

TABLES  a legacy table (one header line, one row per record): file name -> spec
        tidy      name of the tidy table (<tidy>.csv)
        sheet     legacy tab name; header_row: 1-based row of the header on that tab in legacy CPAT (the legacy-style
                  workbook puts the table there, so it pastes onto legacy CPAT at the same address)
        keys      legacy columns that identify a row, renamed {legacy: tidy}; with country=(legacy column, case) the
                  column becomes `country`, ISO3 upper case in tidy, written back in the legacy case
        attrs     legacy columns that only describe a row (e.g. a country name): kept in the layout, not in tidy
        melt      None: the other columns stay columns (they are different variables), renamed by `rename`;
                  (name,): the other columns are values of one variable `name` (years, fuels, sectors, codes);
                  the tidy table gets the column `name` and a column `value`, one row per non-blank cell;
                  (name1, name2, sep): as above, the header split at `sep` into two variables
        skip      first-key values of rows that are not data (kept in the layout only)
        A row that repeats an earlier row exactly (legacy EF_PM repeats Taiwan) is kept in the layout only; a row that
        repeats a key with other values stops the conversion.
CELLS   a legacy tab with several tables at fixed addresses: file name -> spec with sheet, first_row and
        blocks (list of grids, see tidy_convert.py, `grid_*`); cells outside the blocks are layout.
"""

ISO = ('country', 'upper')            # shorthand: the key column is an ISO3 code in upper case

TABLES = {
    # ---- the four proprietary tables (and the file derived from them)
    'legacy_Balances.csv': dict(
        tidy='energy_balances', sheet='Balances', header_row=13, proprietary='yes',
        keys={'country_code': 'country', 'year': 'year', 'measure': 'unit', 'flow_code': 'flow'},
        country=('country_code', 'upper'), attrs=['country'], melt=('fuel',)),
    'legacy_EnergyCons.csv': dict(
        tidy='energy_consumption', sheet='EnergyCons', header_row=1, proprietary='derived',
        keys={'CPAT Code': 'code', 'Year': 'year'}, attrs=['CountryName', 'FuelType'], melt=('sector',)),
    'prices_dom.csv': dict(
        tidy='prices_domestic', sheet='Prices_dom', header_row=5, proprietary='yes',
        keys={'countrycode': 'country', 'year': 'year'}, country=('countrycode', 'upper'),
        attrs=['country_year', 'countrycode_weo', 'countryname'], melt=('code',)),
    'prices_dom_changes.csv': dict(
        tidy='prices_domestic_corrections', sheet='Prices_dom_changes', header_row=1, proprietary='derived',
        keys={'country_year': 'country_year', 'column': 'code'}, attrs=[], melt=None),
    'legacy_HHSurvey.csv': dict(
        tidy='hh_survey', sheet='HHSurvey', header_row=1, proprietary='yes',
        keys={'code': 'code'}, attrs=['iso3', 'year', 'sample', 'type', 'stat_type', 'quant_cons'], melt=('variable',)),
    'legacy_IO_GTAP.csv': dict(
        tidy='io_gtap', sheet='IO_GTAP', header_row=1, proprietary='yes',
        keys={'iso3': 'country', 'year': 'year', 'sector': 'series'}, country=('iso3', 'lower'), attrs=['dis'],
        melt=('gtap_sector',)),
    # ---- distribution
    'legacy_HH_Elast.csv': dict(
        tidy='hh_elasticities', sheet='HH_Elast', header_row=1,
        keys={'code': 'code'}, attrs=['iso3', 'year', 'sample', 'type', 'stat_type', 'quant_cons'], melt=('variable',)),
    'legacy_ASPIRE.csv': dict(
        tidy='aspire', sheet='ASPIRE', header_row=1,
        keys={'Series_Code': 'code'}, attrs=['Country Name', 'ISO-3 Country Code', 'Year', '(firstnm) indicator_name',
                                              '(firstnm) Sub_Topic5', '(firstnm) Sub_Topic6'],
        melt=None, rename={'(firstnm) Value': 'value'}),
    'legacy_WHOCooking.csv': dict(
        tidy='who_cooking', sheet='WHOCooking', header_row=1,
        keys={'code': 'code'}, attrs=['iso3', 'year', 'sample'], melt=None),
    'legacy_GDPRatios.csv': dict(
        tidy='gdp_ratios', sheet='GDPRatios', header_row=1,
        keys={'Country Code': 'country', 'Indicator Code': 'indicator'}, country=('Country Code', 'upper'),
        attrs=['Country Name', 'Indicator Name', 'Latest Year'], melt=('year',)),
    # ---- macro, population, GHG
    'legacy_WEO.csv': dict(
        tidy='weo', sheet='WEO', header_row=9,
        keys={'SERIES_CODE': 'series_code'}, attrs=['last year', 'countrycode', 'DATASET', 'COUNTRY', 'INDICATOR'],
        melt=('year',)),
    'legacy_UNPop.csv': dict(
        tidy='un_population', sheet='UNPop', header_row=6,
        keys={'ISO': 'country'}, country=('ISO', 'upper'), attrs=['', 'CPAT code', 'Population'], melt=('year',)),
    'legacy_SCC.csv': dict(
        tidy='scc', sheet='SCC', header_row=7,
        keys={'Code': 'code'}, attrs=['', 'ISO3', 'prtp', 'eta'], melt=None, rename={'Central': 'value'}),
    'legacy_CH4Inputs.csv': dict(
        tidy='ch4_inputs', sheet='CH4Inputs', header_row=1,
        keys={'cpat_ccode3': 'country', 'tier3': 'source'}, country=('cpat_ccode3', 'upper'), attrs=['countryname'],
        melt=None),
    'legacy_GoalSeekCoal.csv': dict(
        tidy='coal_implicit_price', sheet='GoalSeekCoal', header_row=7,
        keys={'Country': 'country_name'}, attrs=['RowNumber', 'Region'], melt=None,
        rename={'First Year of Calculations': 'first_year', 'Year 2030': 'year_2030'}),
    'legacy_NDCs.csv': dict(
        tidy='ndcs', sheet='NDCs', header_row=1,
        keys={'round': 'round', 'code': 'country'}, country=('code', 'upper'), attrs=['country'], melt=None),
    'legacy_GHGHist.csv': dict(
        tidy='ghg_history', sheet='GHGHist', header_row=1,
        keys={'iso': 'country'}, country=('iso', 'upper'), attrs=['country'], melt=('group', 'year', '|')),
    'legacy_EF_PM.csv': dict(
        tidy='ef_local_pollutants', sheet='EF_PM', header_row=2,
        keys={'Country-Series code': 'code'}, attrs=['Country Code', 'Subsector', 'Fuel', 'Pollutant'], melt=None,
        rename={'FE in': 'fe_in', 'FE fin': 'fe_fin'}),
    'legacy_EF_GHG.csv': dict(
        tidy='ef_ghg', sheet='EF_GHG', header_row=3, skip=['Code'],
        keys={'Code': 'code'}, attrs=['Region/country', 'Series name', 'Atribute 1', 'Atribute 2'], melt=None,
        rename={'FACTOR': 'value'}),
    'legacy_OilProductShares.csv': dict(
        tidy='oil_product_shares', sheet='OilProductShares', header_row=1,
        keys={'countrycode': 'country'}, country=('countrycode', 'upper'), attrs=['countryname', 'incomelevel', 'region'],
        melt=('variable',)),
    # ---- transport
    'legacy_Transport1.csv': dict(
        tidy='transport_country', sheet='Transport1', header_row=1,
        keys={'iso3': 'country', 'year': 'year'}, country=('iso3', 'upper'), attrs=['country'], melt=('variable',)),
    'legacy_Transport2.csv': dict(
        tidy='vehicle_prices', sheet='Transport2', header_row=1,
        keys={'cpat_ccode3': 'country', 'year': 'year'}, country=('cpat_ccode3', 'upper'), attrs=['countryname'],
        melt=('variable',)),
    # ---- global parameters (not country data)
    'transport_params.csv': dict(
        tidy='transport_params', sheet='TransportParams', header_row=1,
        keys={'key': 'key'}, attrs=[], melt=None),
    'transport_paths.csv': dict(
        tidy='transport_paths', sheet='TransportPaths', header_row=1,
        keys={'key': 'key'}, attrs=['unit', 'description', 'legacy_cell'], melt=('year',)),
    'fuel_units.csv': dict(tidy='fuel_units', sheet='FuelUnits', header_row=1, keys={'fuel': 'fuel'}, attrs=[], melt=None),
    'distn_catmap.csv': dict(tidy='distn_category_map', sheet='DistCatMap', header_row=1, keys={'gtap': 'gtap_sector'},
                             attrs=[], melt=None),
    'distn_programs.csv': dict(tidy='distn_programs', sheet='DistPrograms', header_row=1, keys={'key': 'key'}, attrs=[],
                               melt=None),
    'distn_gtapmap.csv': dict(tidy='distn_gtap_map', sheet='DistGtapMap', header_row=1, keys={'gtap': 'gtap_sector'},
                              attrs=[], melt=None),
    'distn_passthrough.csv': dict(tidy='distn_passthrough', sheet='DistPassthrough', header_row=1,
                                  keys={'cpat': 'sector'}, attrs=[], melt=None),
    '../range_anxiety_fit/range_anxiety_fit.csv': dict(
        tidy='range_anxiety_fit', sheet='RangeAnxietyFit', header_row=1, proprietary='derived',
        keys={'iso': 'country'}, country=('iso', 'upper'), attrs=['country'], melt=None),
}

# Layout-only files that travel with a table (not data): copied as they are.
LAYOUT_FILES = {'prices_dom_header.csv': 'prices_dom.csv'}

CELLS = {}     # filled from tidy_blocks.py (legacy tabs at their addresses)
try:
    from tidy_blocks import CELLS  # noqa: F401,E402
except ImportError:
    pass

_names = [s['tidy'] for s in TABLES.values()] + [s['tidy'] for s in CELLS.values()] +     [b['name'] for s in CELLS.values() for b in s.get('blocks', [])]
assert len(_names) == len(set(_names)), sorted({n for n in _names if _names.count(n) > 1})
