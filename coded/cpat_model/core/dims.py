"""Index sets of the model, as Excel-AI defines them (excel_ai/mitigation/build.py, dimensions block).

Letters of the equation list in brackets. Codes are those of the codes map.
"""

# Subsectors s (16): code, name, sector group, elasticity sector, EF sector, coal/gas price sector, feebate sector
SUBSECTORS = [
    ('rod', 'Road', 'tra', 'tra', 'rod', 'res', 'tra'),
    ('ral', 'Rail', 'tra', 'tra', 'rod', 'ind', 'tra'),
    ('avi', 'Domestic aviation', 'tra', 'tra', 'rod', 'ind', 'tra'),
    ('nav', 'Domestic navigation', 'tra', 'tra', 'rod', 'ind', 'tra'),
    ('res', 'Residential', 'bld', 'res', 'res', 'res', 'res'),
    ('foo', 'Food & forestry', 'bld', 'ind', 'res', 'ind', 'res'),
    ('srv', 'Services (public & private)', 'bld', 'srv', 'res', 'ind', 'res'),
    ('mch', 'Mining & chemicals', 'ind', 'ind', 'ind', 'ind', 'ind'),
    ('irn', 'Iron & steel', 'ind', 'ind', 'ind', 'ind', 'ind'),
    ('nfm', 'Other metals', 'ind', 'ind', 'ind', 'ind', 'ind'),
    ('mac', 'Machinery', 'ind', 'ind', 'ind', 'ind', 'ind'),
    ('cem', 'Cement', 'ind', 'ind', 'ind', 'ind', 'ind'),
    ('omn', 'Other manufacturing', 'ind', 'ind', 'ind', 'ind', 'ind'),
    ('cst', 'Construction', 'ind', 'ind', 'ind', 'ind', 'ind'),
    ('ftr', 'Fuel transformation', 'ind', 'ind', 'ind', 'ind', 'ind'),
    ('oen', 'Other energy use', 'oen', 'ind', 'ind', 'ind', 'ind'),
]
SECTORS = [s[0] for s in SUBSECTORS]                       # s
SECTOR_GROUP = {s[0]: s[2] for s in SUBSECTORS}            # S (tra, bld, ind, oen)
ELASTICITY_SECTOR = {s[0]: s[3] for s in SUBSECTORS}
EF_SECTOR = {s[0]: s[4] for s in SUBSECTORS}
GAS_COAL_PRICE_SECTOR = {s[0]: s[5] for s in SUBSECTORS}
FEEBATE_SECTOR = {s[0]: s[6] for s in SUBSECTORS}
COVERAGE_SECTORS = ['pow'] + SECTORS                      # e: the 17 ETS and coverage sectors

# Fuels f (9): code, name, elasticity fuel, AEEI fuel, price-sector rule, price unit
FUEL_TABLE = [
    ('coa', 'Coal', 'coa', 'coa', 'sub', 'USD/GJ'),
    ('nga', 'Natural gas', 'nga', 'nga', 'sub', 'USD/GJ'),
    ('gso', 'Gasoline', 'gso', 'oil', 'all', 'USD/liter'),
    ('die', 'Diesel', 'die', 'oil', 'all', 'USD/liter'),
    ('lpg', 'LPG', 'oil', 'oil', 'all', 'USD/liter'),
    ('ker', 'Kerosene', 'oil', 'oil', 'all', 'USD/liter'),
    ('jfu', 'Jet fuel', 'oil', 'oil', 'all', 'USD/liter'),
    ('oop', 'Other oil products', 'oil', 'oil', 'all', 'USD/bbl'),
    ('bio', 'Biomass', 'bio', 'bio', 'all', 'USD/GJ'),
]
FUELS = [f[0] for f in FUEL_TABLE]                         # f
PRICE_FUEL_OF = {'jfu': 'ker'}                             # jet fuel takes the kerosene price build-up (I19)

# Price fuels c (12): coal and gas by price sector, oil products and biomass for all sectors
PRICE_FUELS = ['coa.pow', 'coa.res', 'coa.ind', 'nga.pow', 'nga.res', 'nga.ind',
               'gso.all', 'die.all', 'lpg.all', 'ker.all', 'oop.all', 'bio.all']

# Generation types k (9) and the user and demand groups of electricity
GENERATION = ['coa', 'nga', 'oop', 'nuc', 'wnd', 'sol', 'hyd', 'ore', 'bio']
USERS = ['res', 'ind']                                     # u
DEMAND_GROUPS = ['tra', 'res', 'ind', 'srv']               # d

# Distribution
DECILES = list(range(1, 11))
