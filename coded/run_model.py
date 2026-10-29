from types import SimpleNamespace

import config

from cpat_model.dashboard_inputs import DashboardInputs
from cpat_model.data_read.input_data import InputData
from cpat_model.distribution_inputs import DistributionInputs
from cpat_model.scenario_results import ScenarioResults

from cpat_model.mitigation.gdp.gdp import GDP
from cpat_model.mitigation.policies.phaseouts import Phaseouts
from cpat_model.mitigation.policies.policies import Policies
from cpat_model.mitigation.policies.shadow_prices import ShadowPrices
from cpat_model.mitigation.carbon_pricing.existing_ct import ExistingCT
from cpat_model.mitigation.carbon_pricing.existing_ets import ExistingETS
from cpat_model.mitigation.efs.co2 import EFsCO2
from cpat_model.mitigation.elasticities.elasticities import Elasticities

from cpat_model.mitigation.prices.domestic_prices import DomPrices
from cpat_model.mitigation.prices.international_prices import IntPrices
from cpat_model.mitigation.prices.prices import EnergyPrices

from cpat_model.mitigation.energy_consumption.ec import EC
from cpat_model.mitigation.emissions.em import CO2Emissions

from cpat_model.mitigation.power.power import Power

from cpat_model.distribution.distribution import Distribution
from cpat_model.distribution import price_changes as distn_price_changes

import cpat_model.constants as c


def run_model():
    selected_countries = ['USA', 'EGY']
    last_simulation_year = 2030

    base_year = 2022
    simulation_years = (base_year, last_simulation_year)
    input_data = InputData(
        simulation_years, selected_countries
    )

    # Distribution module is single-year/single-country; defaults to
    # analysing the last simulated year. See excel_ai/distribution/README.md and
    # other/more/CPAT_Distribution_Module_Pseudocode.docx.
    distribution_inputs = DistributionInputs({'YearDistn': last_simulation_year})

    # Collects every scenario's finished component outputs so Distribution
    # can compare a policy scenario against the baseline scenario once all
    # scenarios have been run (see cpat_model.scenario_results.ScenarioResults).
    scenario_results: dict[str, ScenarioResults] = {}

    for scenario_name, dashboard_inputs in config.SCENARIOS.items():

        di = DashboardInputs(dashboard_inputs)

        elasticities = Elasticities(selected_countries, di.d, input_data)
        gdp = GDP(simulation_years, di.d, input_data)
        efs_co2 = EFsCO2(selected_countries, input_data, di.d['EmissionsFactCO2'])
        policies = Policies(
            simulation_years, selected_countries, di.d['ScenarioSelected'],
            input_data, di.d, gdp.deflator
        )
        phaseouts = Phaseouts(
            simulation_years, di.d['ScenarioSelected'],
            di.d['energy_sector_reform'], di.d['PrcContPhaBaseline']
        )
        existing_ct = ExistingCT(
            selected_countries, simulation_years, input_data,
            di.d['ExistingCTApply'], di.d['ExistingCTGrowth']
        )
        existing_ets = ExistingETS(
            selected_countries, simulation_years, input_data,
            di.d['ExistingETSApply'], di.d['ExistingETSGrowth']
        )

        dom_prices = DomPrices(
            selected_countries, simulation_years, input_data, di.d['GovPriceControls']
        )
        int_prices = IntPrices(
            simulation_years, selected_countries, input_data, di.d, gdp.deflator
        )
        energy_prices = EnergyPrices(
            simulation_years, di.d['ScenarioSelected'], selected_countries, gdp, dom_prices, phaseouts,
            existing_ct, existing_ets, efs_co2, int_prices, input_data, di.d
        )

        shadow_prices = ShadowPrices(di.d, policies, efs_co2.ef_tco2_per_volume_unit)
        ec = EC(simulation_years, input_data, elasticities, shadow_prices)

        power = Power(
            simulation_years, selected_countries, di.d,
            energy_prices.ele_prices['rp'], policies.cp_trajectory, input_data
        )
        em = CO2Emissions(ec.ec_fossil_fuels_by_sector, efs_co2)

        for year in range(simulation_years[0], simulation_years[1] + 1):
            policies.calculate_policies_year(year, existing_ets.existing_ets_s_nat, di.d)
            energy_prices.calculate_prices_year(
                year, di.d['ScenarioSelected'], policies, efs_co2,
                dom_prices, phaseouts
            )
            power.calculate_power_year(
                year, input_data,
                gdp.d_gdp_at_const_prices, elasticities, di.d,
                energy_prices, policies.p_cov_s, int_prices.uranium_fuel_cost
            )
            shadow_prices.calculate_year(year, energy_prices.pbc)
            ec.calculate_ec_year(
                year, gdp.d_gdp_at_const_prices,
                energy_prices, policies.p_cov_s, elasticities, input_data.lcoe_tmp,
                di.d, policies.exogenous_shock_on_ec,
                shadow_prices
            )
            em.calculate_em_year(year, ec.ec_fossil_fuels_by_sector)

        # energy_prices.rp.to_csv(f'rp_{scenario_name}.csv')
        # em.em.to_csv(f'em_{scenario_name}.csv')
        # power.generation.g.to_csv(f'power_generation_{scenario_name}.csv')

        scenario_results[scenario_name] = ScenarioResults(
            scenario_name=scenario_name,
            dashboard_inputs_d=di.d,
            gdp=gdp,
            policies=policies,
            energy_prices=energy_prices,
            ec=ec,
            em=em,
            power=power,
        )

    distributions = run_distribution(
        scenario_results, selected_countries, input_data, distribution_inputs
    )
    return scenario_results, distributions


def country_view(input_data, country: str) -> SimpleNamespace:
    """
    The Distribution tables of InputData restricted to one country (Distribution
    works on one country at a time and expects single-country tables; some data
    tables, e.g. HH_Elast and GDPRatios, hold several countries).
    """
    view = {}
    for name in [a for a in vars(input_data) if a.startswith('distn_')]:
        df = getattr(input_data, name)
        if c.COUNTRY_CODE in df.columns:
            df = df[df[c.COUNTRY_CODE] == country].reset_index(drop=True)
        view[name] = df
    return SimpleNamespace(**view)


def run_distribution(scenario_results, selected_countries, input_data, distribution_inputs):
    """
    Distributional analysis: compare each policy scenario against the baseline
    scenario for the configured analysis year, for every selected country that
    has household survey data (the Distribution data tables; Egypt so far).
    See excel_ai/distribution/README.md and
    other/more/CPAT_Distribution_Module_Pseudocode.docx.
    """
    baseline_name = next(
        (
            name for name, results in scenario_results.items()
            if results.dashboard_inputs_d['ScenarioSelected'] == c.BASELINE
        ),
        None
    )
    if baseline_name is None:
        raise RuntimeError(
            "No scenario with ScenarioSelected == c.BASELINE found in config.SCENARIOS; "
            "the Distribution module needs a baseline run to compare policy scenarios against."
        )
    baseline = scenario_results[baseline_name]
    with_survey = set(input_data.distn_hh_survey[c.COUNTRY_CODE])
    countries = [country for country in selected_countries if country in with_survey]

    # Distribution operates on one country at a time (see distribution.py's
    # class docstring); loop over every country for each policy scenario.
    distributions: dict[tuple[str, str], Distribution] = {}
    for scenario_name, policy in scenario_results.items():
        if scenario_name == baseline_name:
            continue
        for country in countries:
            price_change_direct = distn_price_changes.derive_price_change_direct_from_scenarios(
                country, baseline, policy, distribution_inputs.d['YearDistn']
            )
            # only the 8 priced fuels feed Distribution's constructor; the
            # biomass fuels it adds internally have no Mitigation-side price
            price_change_direct_priced = price_change_direct.drop(c.COOKING_BIOMASS_FUELS)
            cp_revenue = distn_price_changes.derive_cp_revenue_from_scenarios(
                country, policy, distribution_inputs.d['YearDistn']
            )
            # TODO: national_totals=None falls back to the household survey's own
            # implied population/consumption totals (see rebasing.py module
            # docstring) rather than a national-accounts figure; wire one up once
            # GDP exposes a real-terms household consumption series.
            national_totals = None

            distributions[(scenario_name, country)] = Distribution(
                distribution_inputs.d, country, country_view(input_data, country),
                price_change_direct_priced, cp_revenue, national_totals
            )

    return distributions


if __name__ == '__main__':
    run_model()
