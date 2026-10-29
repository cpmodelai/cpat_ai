"""The order of the mitigation blocks (spec section 4.3). The only place the order is written.

Each block is a function: prepare and finish blocks take (state, db, inputs, settings, baseline); year blocks also
take t. They are added here as they are built (phase 3).
"""

from cpat_model import air_pollution, transport_cobenefits
from cpat_model.mitigation import emissions, fuel_use, gdp, header, policies, power, prices, totals

# Prepare (all years; nothing here reads a model quantity): the module values first (they feed the Pigouvian
# taxes), then 0 header, 1 policies, 2 prices, 3 power costs
PREPARE = [air_pollution.prepare, transport_cobenefits.prepare, header.prepare,
           policies.prepare, prices.prepare, power.prepare,
           fuel_use.prepare]

# One year t: 16 GDP level, 5b road, 5-8 fuel demand, 6b leakage, 3 power, 11 totals, 12 revenues, 13 CO2, 14 GHG,
# 15 local pollutants, then the module steps, then 16 GDP effect
YEAR = [gdp.start, power.step, fuel_use.step, totals.energy, prices.averages, emissions.co2, emissions.ghg,
        totals.revenues, emissions.kaya, gdp.effects, gdp.external, air_pollution.step, transport_cobenefits.step]

# Finish (all years): 17 indicators, 17b module inputs, 18 welfare, 19 exports
FINISH = [emissions.ndc]
