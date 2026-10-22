import pandas as pd

import cpat_model.constants as c

from cpat_model.mitigation.aggregations.total_energy_consumption import get_ec_sg_f, get_ec_f_totals
from cpat_model.mitigation.aggregations.total_emissions import get_em_sg_f, get_em_f_totals

from cpat_model.mitigation.fiscal_revenues.r_fuel_revenues import (
    get_cov_em, get_cov_em_by_fuel,
    get_cp_trajectory,
    get_r_by_fuel, get_r_fuel_revenues
)

from cpat_model.mitigation.fiscal_revenues.r_existing_taxes import (
   get_r_existing_taxes, get_r_existing_taxes_by_fuel
)

from cpat_model.mitigation.fiscal_revenues.r_vat import get_r_vat, get_r_vat_by_fuel

from cpat_model.mitigation.fiscal_revenues.r_losses import (
    get_domestic_demand, get_global_demand, get_subsidized_demand,
    get_per_unit_subsidies, get_r_losses_by_fuel, get_r_losses
)

from cpat_model.mitigation.fiscal_revenues.r_methane_fee import get_r_methane_fee

from cpat_model.mitigation.fiscal_revenues.revenues import (
    get_total_revenues_change, get_total_revenues_additional,
    get_total_revenues_per_gdp, get_total_revenues
)

from cpat_model.mitigation.fiscal_revenues.revenues_allocated import (
    get_revenues_allocation, get_revenues_allocated
)

from cpat_model.mitigation.gdp.gdp import (
    get_gdp_data_country_filtered,
    get_population, get_population_growth, get_gdp_per_capita, get_gdp_growth_per_capita,
    get_ngdp_and_enda, get_ngdp_rpch, get_ngdp_rpch_projection,
    get_ngdp_d, get_ngdp_d_projection, get_deflator, get_real_baseline_gdp
)

from cpat_model.mitigation.ch4.ch4 import (
    get_ch4_data, PRODUCTION, PRICE, PERCENT, PER_OTHER, PER_AVG, AVG_POW
)

from cpat_model.mitigation.ghgs.ghgs import get_ghgs_data

from cpat_model.mitigation.methan_fee.mf import (
    get_mf_price_trajectory, get_mf, get_mf_non_fossil, get_em_allocation_adjusted,
    get_em_allocation_avg_adjusted, get_em_allocation_used, get_methane_em_by_source,
    get_methane_em_intensity_by_source, get_ef_ch4_baseline, get_ef_ch4_baseline_reduction,
    get_ef_ch4_after_abatement, get_mf_agr, get_d_producer_prices,
    get_agr_production, get_em_ch4_agr,
    get_r_agr, get_r_agriculture
)
from cpat_model.mitigation.methan_fee.mf_wst import (
    get_methane_em_by_source_wst, get_methane_em_intensity_by_source_wst, get_ef_ch4_baseline_wst,
    get_ef_ch4_after_abatement_wst, get_wst_production, get_em_ch4_wst, get_mf_wst,
    get_r_wst
)


from cpat_model.mitigation.policies.policies import (
    get_p_cov_s, get_p_cov_f,
    get_apply_tax_s, get_apply_tax_f,
)

from cpat_model.mitigation.carbon_pricing.existing_ets import (get_existing_ets_s)

# [Post policy GDP]

ec = pd.DataFrame()
em = pd.DataFrame()
vat = pd.DataFrame()
fao = pd.DataFrame()
cs = pd.DataFrame()
xct = pd.DataFrame()
xetsp = pd.DataFrame()
ps = pd.DataFrame()

scenario_type = ''

# ignore no all params for fncs
# pylint: disable=E1120


# CALC ONLY ONCE (either no t, ro all t can be calc at the beginning):
apply_tax_f = get_apply_tax_f() # no t
apply_tax_s = get_apply_tax_s() # no t

existing_ets = get_existing_ets_s() # all t

cp_trajectory = get_cp_trajectory() # all t

global_demand = get_global_demand() # all t

revenues_allocation = get_revenues_allocation() # all t

### gdp indicators:
(
    gdp_data_country_filtered,
    countries_in_data,
    ngdp_d_world
) = get_gdp_data_country_filtered()
#
population = get_population(gdp_data_country_filtered)
population_growth = get_population_growth(population)
# for real_baseline_gdp
ngdp, enda = get_ngdp_and_enda(gdp_data_country_filtered, countries_in_data)
ngdp_rpch = get_ngdp_rpch(gdp_data_country_filtered, countries_in_data)
ngdp_rpch = get_ngdp_rpch_projection(ngdp_rpch)
ngdp_d = get_ngdp_d(gdp_data_country_filtered, countries_in_data)
ngdp_d = get_ngdp_d_projection(ngdp_d)
deflator = get_deflator(ngdp_d)
real_baseline_gdp = get_real_baseline_gdp(ngdp, enda, ngdp_rpch, deflator)

### ch4
ch4_data = get_ch4_data()
### ghgs data
ghgs_data = get_ghgs_data()

### mf agr
mf_price_trajectory = get_mf_price_trajectory()
mf = get_mf(mf_price_trajectory, cp_trajectory)
mf_non_fossil = get_mf_non_fossil(mf)
em_allocation_adjusted = get_em_allocation_adjusted(ch4_data[PERCENT], ch4_data[PER_OTHER])
em_allocation_avg_adjusted = get_em_allocation_avg_adjusted(ch4_data[PRODUCTION], ch4_data[PER_AVG])
em_allocation_used = get_em_allocation_used(em_allocation_adjusted, em_allocation_avg_adjusted)
methane_em_by_source = get_methane_em_by_source(em_allocation_used, ghgs_data[c.AGR])
methane_em_intensity_by_source = get_methane_em_intensity_by_source(
    methane_em_by_source, ch4_data[PRODUCTION]
)
ef_ch4_baseline = get_ef_ch4_baseline(methane_em_intensity_by_source)
ef_ch4_baseline_reduction = get_ef_ch4_baseline_reduction(mf_non_fossil, ch4_data[AVG_POW])
ef_ch4_after_abatement = get_ef_ch4_after_abatement(ef_ch4_baseline, ef_ch4_baseline_reduction)
mf_agr = get_mf_agr(ef_ch4_after_abatement, mf_non_fossil)
d_producer_prices = get_d_producer_prices(mf_agr, ch4_data[PRICE])

### mf wst
methane_em_by_source_wst = get_methane_em_by_source_wst(ghgs_data[c.WST])
methane_em_intensity_by_source_wst = get_methane_em_intensity_by_source_wst(
    methane_em_by_source_wst, ch4_data[PRODUCTION]
)
ef_ch4_baseline_wst = get_ef_ch4_baseline_wst(methane_em_intensity_by_source_wst)
ef_ch4_after_abatement_wst = get_ef_ch4_after_abatement_wst(
    ef_ch4_baseline_wst, ef_ch4_baseline_reduction
)
wst_production = get_wst_production(ch4_data[PRODUCTION], population_growth)
em_ch4_wst = get_em_ch4_wst(wst_production, ef_ch4_after_abatement_wst)
mf_wst = get_mf_wst(ef_ch4_after_abatement_wst, mf_non_fossil)
r_wst = get_r_wst(mf_wst, em_ch4_wst)

for year in range(2020, 2050 + 1):
    # each t for this 4 could be stored, for end results:
    ec_sg_f = get_ec_sg_f(ec)
    ec_f_totals = get_ec_f_totals(ec_sg_f)

    em_sg_f = get_em_sg_f(em)
    em_f_totals = get_em_f_totals(ec_sg_f)

    # r_by_fuel
    p_cov_f = get_p_cov_f(apply_tax_f)
    p_cov_s = get_p_cov_s(apply_tax_s, existing_ets)

    cov_em = get_cov_em(p_cov_f, p_cov_s, ec_sg_f, ec)
    cov_em_by_fuel = get_cov_em_by_fuel(cov_em, em_sg_f, em_f_totals)

    r_by_fuel = get_r_by_fuel(em_f_totals, cov_em,cp_trajectory)
    r_fuel_revenues = get_r_fuel_revenues(r_by_fuel)

    # r_additional_excise

    # r_existing_taxes
    r_existing_taxes_by_fuel = get_r_existing_taxes_by_fuel(ec_sg_f, ec, fao, cs, xct, xetsp)
    r_existing_taxes = get_r_existing_taxes(r_existing_taxes_by_fuel)

    # r_vat_by_fuel
    r_vat_by_fuel = get_r_vat_by_fuel(ec_sg_f, ec, vat)
    r_vat = get_r_vat(r_vat_by_fuel)

    # r_losses
    global_demand = get_global_demand()
    domestic_demand = get_domestic_demand(ec_f_totals)

    subsidized_demand = get_subsidized_demand(global_demand, domestic_demand)
    per_unit_subsidies = get_per_unit_subsidies(ps)

    r_losses_by_fuel = get_r_losses_by_fuel(subsidized_demand, per_unit_subsidies)
    r_losses = get_r_losses(r_losses_by_fuel)

    # gdp indicators
    gdp_per_capita = get_gdp_per_capita(population) # TODO get gdp_pre_policy and gdp_post_policy
    gdp_growth_per_capita = get_gdp_growth_per_capita(gdp_per_capita)

    # mf agr
    # TODO: put agr_production into structure so we hold all t
    agr_production = get_agr_production(
        agr_production, ch4_data[PRODUCTION], population_growth,
        gdp_growth_per_capita, d_producer_prices
    )
    em_ch4_agr = get_em_ch4_agr(agr_production, ef_ch4_after_abatement.loc[:, [str(year)]])
    r_agr = get_r_agr(em_ch4_agr, mf_non_fossil.loc[:, [str(year)]])
    r_agriculture = get_r_agriculture(r_agr)

    # mf_total
    r_methane_fee = get_r_methane_fee(r_agriculture, r_wst)

    # total revenues
    total_revenues = get_total_revenues(r_fuel_revenues, r_existing_taxes, r_vat, r_losses, r_methane_fee)
    total_revenues_per_gdp = get_total_revenues_per_gdp(total_revenues, real_baseline_gdp)

    if scenario_type == c.BASELINE:
        total_revenues_per_gdp_baseline = total_revenues_per_gdp.copy()
        total_revenues_additional = get_total_revenues_additional(scenario_type,
                                                                  total_revenues_per_gdp_baseline)
    else:
        # TODO: add sanity assertion if total_revenues_per_gdp_baseline exists (it should)
        total_revenues_additional = get_total_revenues_additional(scenario_type,
                                                                  total_revenues_per_gdp_baseline,
                                                                  total_revenues_per_gdp)
    total_revenues_change = get_total_revenues_change(total_revenues_additional)

    # revenues allocated
    revenues_allocated = get_revenues_allocated(revenues_allocation, total_revenues_change)
