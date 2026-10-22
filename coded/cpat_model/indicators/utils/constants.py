"""
This module contains constant values used for indicators module.

Constants:
    INDICATORS_HEADERS: Dict where .values() returns all of headers for all indicators.
    ... TODO
"""

from cpat_shiny.mapping import ALL_INDICATORS

INDICATORS_HEADERS = ALL_INDICATORS

# aggregations for sectors
SECTORS_AGG = {
    'tra': ['rod', 'ral', 'avi', 'nav'],
    'res': ['res', 'foo', 'srv'], # bld
    'ind': ['mch', 'irn', 'nfm', 'mac', 'cem', 'omn', 'cst', 'ftr'],
    'oen': ['oen'],
    'pow': ['pow']
}
# TODO unify this -> here res -> bld like it should be differenciated
SECTORS_AGG_TMP = {
    'tra': ['rod', 'ral', 'avi', 'nav'],
    'bld': ['res', 'foo', 'srv'],
    'ind': ['mch', 'irn', 'nfm', 'mac', 'cem', 'omn', 'cst', 'ftr'],
    'oen': ['oen'],
    'pow': ['pow']
}
SECTOR_GROUPS = list(SECTORS_AGG_TMP.keys())
ALL_SECTORS_FROM_AGG = [value for values in SECTORS_AGG.values() for value in values]
REVERSE_SECTORS_AGG = {v: k for k, values in SECTORS_AGG.items() for v in values}

# used for mit.ener.{sector}.{fuel}.e
TRA_BLD_IND_SECTORS = SECTORS_AGG['tra'] + SECTORS_AGG['res'] + SECTORS_AGG['ind']
FOSSIL_FUELS = ['coa', 'nga', 'gso', 'die', 'lpg', 'ker', 'oop']
FOSSIL_FUELS_SORTED = sorted(FOSSIL_FUELS)
# FOSSIL_FUELS = ['coa', 'die', 'gso', 'ker', 'lpg', 'nga', 'oop']
FOSSIL_FUELS_AND_BIO = FOSSIL_FUELS +  ['bio']

# Non-biomass renewable
RNW_AGG = {
    'rnw': ['wnd', 'sol', 'hyd', 'ore']
}

# renewable + nuclear
REN_AGG = {
    'ren': ['wnd', 'sol', 'hyd', 'ore', 'nuc']
}
REVERSE_REN_AGG = {f: 'ren' for f in REN_AGG['ren']}
SECTORS_FOR_REN_AGG = SECTORS_AGG['res'] + SECTORS_AGG['ind']

# fuels for pow and elec aggregations
POW_ELEC_FUELS = ['coa', 'nga', 'oop', 'nuc', 'wnd', 'sol', 'hyd', 'ore', 'bio']

# conversion factors # TODO: unify with cpat_model/constants
KTOE_TO_GWH = 11.63
GWH_TO_TWH = 0.001
