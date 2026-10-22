import pandas as pd

MAPPINGS_PATH = 'cpat_shiny/mappings.xlsx'

df = pd.read_excel(MAPPINGS_PATH, sheet_name='Countries')
ALL_COUNTRIES = df.set_index('CountryCode')['Country'].to_dict()

regions_df = pd.read_excel(MAPPINGS_PATH, sheet_name='Regions')
country_to_region_df = pd.read_excel(MAPPINGS_PATH, sheet_name='Country to Region')
COUNTRY_TO_REGION = (
    country_to_region_df
    .merge(regions_df, on='Region')
    .set_index('CountryCode')['RegionCode']
    .to_dict()
)

# Country to IFS codes
COUNTRY_TO_IFS_CODE = (
    pd.read_excel(MAPPINGS_PATH, sheet_name='Country to IFS codes')
)

# Used only for elasticities, based on Elasticities tab, does not match Countries tab mapping
# HIC High income, LIC Low income, LMIC Lower middle income, UMIC Upper middle income
COUNTRY_TO_INCOME_GROUP = (
    pd.read_excel(MAPPINGS_PATH, sheet_name='Income Groups')
    .set_index('CountryCode')['Income group']
    .to_dict()
)

ALL_FUELS = {
    'coa': 'Coal',
    'nga': 'Natural Gas',
    'gso': 'Gasoline',
    'die': 'Diesel',
    'lpg': 'LPG',
    'ker': 'Kerosene',
    'oop': 'Other oil products'
    # Fuels not included in the policies:
    # 'bio': Biomass, 'jfu': Jetfuel, 'ore': Other Renewables, 'hyd': Hydro,
    # 'nuc': Nuclear, 'sol': Solar, 'wnd': Wind, 'ele': Electricity
}

ALL_SECTORS = {
    'pow': 'Power',
    'rod': 'Road',
    'ral': 'Rail',
    'avi': 'Domestic aviation',
    'nav': 'Domestic shipping',
    'res': 'Residential',
    'oen': 'Other energy use',
    'foo': 'Food & forestry',
    'srv': 'Services (private & public)',
    'mch': 'Mining & chemicals',
    'irn': 'Iron & steel',
    'nfm': 'Other metals',
    'mac': 'Machinery',
    'cem': 'Cement',
    'omn': 'Other manufacturing',
    'cst': 'Construction',
    'ftr': 'Fuel transformation & transportation'
    # Sectors not included in the policies:
    # ['elec' 'wav' 'neu']
}

CT_AFTER_TARGET_YEAR = {
    "lin": "Linear projection",
    "cst": "Target CT value"
}

ALL_INDICATORS = {
    'ec': 'Energy consumption',
    'dec': 'Disaggregated energy consumption (Policy)',
    'p': 'Energy prices',
    'em': 'Emissions'
}

CPAT_VARIABLES = {
    'ec': 'Energy consumption',
    'em': 'CO2 Emissions',
    'p': 'Retail prices',
    'txo': 'Excise and other taxes',
    'cs': 'Consumer-side subsidy',
    'ps': 'Producer-side subsidy',
    'sp': 'Supply Price'
}

# SCENARIOS_TABLE TODO add schema here
SCENARIOS_COL_TYPES = {
    'Tuple': ['SelectedCountries', 'SelectedSectors', 'SelectedFuels'],
    'str': ['ScenarioName', 'CTLinearProjection', 'IntPricesSource'],
    'int': ['CTintroYear', 'CTtargetYear', 'CTintroValue', 'CTtargetValue']
}
SCENARIOS_COLUMNS = [col for l in SCENARIOS_COL_TYPES.values() for col in l]

# price source selection
PRICES_SELECTION = {
    'AVG': 'AVG',
    'EIA': 'EIA',
    'IEA': 'IEA',
    'IMF': 'IMF',
    'IMF-IEA': 'IMF-IEA',
    'IMF-WB': 'IMF-WB',
    'WB': 'WB',
}

ALL_DOCUMENTATION = {
    'mitigation': 'Mitigation',
    'gdp_prices': 'GDP and international prices'
}

AIR_POLLUTION_VARIABLES = {
    'emissions': 'Local pollutant emissions',
    'conc_mat': 'Concentration Matricies',
    'pollution': 'PM2.5 Concentrations',
    'health_burden': 'Health burden',
    'wdl': 'Working days lost',
    'wdl_value': 'Working days lost value',
    'yld_value': 'YLD value',
    'mortality_value' : 'Mortality value',
    'mortality_as_gdp_share': 'Mortality value as GDP share',
    'vsl': 'Value of statistical life',
    'health_expenditure': 'Health expenditure'
}

AP_SECTORS = {
    'cpp': 'Coal Power Plants',
    'gpp': 'Gas Power Plants',
    'opp': 'Other Power Plants',
    'gro': 'Residential, services and construction',
    'rod': 'Road transport',
    'oth': 'Industries and other energy',
    'foo': 'Food & forestry'
}

AP_INDICATORS = {
    'conc_pm': 'PM2.5 concentrations',
    'cad': 'Cumulative averted deaths',
    'ada': 'Averted deaths by age', 
    'morbidity': 'Averted YLL and YLD',
    'externalities': 'Externalities by sector and fuel',
    'gdp_loss': 'GDP loss due to pollution',
    'sav': 'Health expenditure savings',
    'dthktoe': 'Deaths per ktoe by sector and fuel'
}