import cpat_model.constants as c

# [Post policy GDP]

# Income and population elasticities for non-energy emissions
# Manual inputs!273:275 (v361)
POPULATION_ELASTICITIES = {
    c.AGR: 0.9,
    c.WST: 1.0,
    'oth': 1.0 # other
}
PER_CAPITA_INCOME_ELASTICITIES = {c.AGR: 0.15}

# Elasticity of demand w/r/price - agriculture, average
ELASTICITY_DEMAND_AGR = -0.5 # Manual inputs'!$J$141 (v361)

# Pass-through of carbon price/methane fee to consumers
PASS_THROUGH_MAETHAN_FEE = 1.0 # Manual inputs'!$J$143 (v361)

# Methane fee applies to agriculture
IS_METHAN_FEE_AGR = True # Manual inputs'!$J$147 (v361)

# Methane fee applies to waste
IS_METHAN_FEE_WST = True # Manual inputs'!$J$148 (v361)

# Methane - non-fossil fuel
METHANE_NON_FOSSIL = 27.2 # Mitigation $I$1009 (v361)

# Reduction in intensity due to autonomous technological improvement - agriculture
REDUCTION_IN_INTENSITY_AGR = 0.471896530177661 / 100 # Manual inputs'!$J$135 (v361)

# Reduction in intensity due to autonomous technological improvement - waste
REDUCTION_IN_INTENSITY_WST = 0.5 / 100 # Manual inputs'!$J$136 (v361)
