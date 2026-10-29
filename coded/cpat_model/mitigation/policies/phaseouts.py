import pandas as pd
import numpy as np

from cpat_model.dashboard_inputs import EnergySectorReform
import cpat_model.constants as c

class Phaseouts:
    """
    'Phaseouts of existing policies (subsidies, taxes, and price controls)' from
    'Policies' section (v361)
    CPAT Excel: table start baseline: 1816, scenario: 6806

    No 'Phaseout factor - PPAs (engineer model)' implemented.
    """
    # Public attributes:
    phaseout_producer: pd.DataFrame
    phaseout_consumer: pd.DataFrame
    phaseout_subsidy_tax: pd.DataFrame

    def __init__(
            self,
            simulation_years: tuple[int, int],
            scenario_type: str,
            # Dashboard inputs:
            energy_sector_reform: EnergySectorReform,
            is_pc_phaseout_baseline: bool,
            ) -> None:
        self.__years = np.arange(simulation_years[0] - 1, simulation_years[1] + 1)
        self.__columns = self.__years.astype(str)

        self.phaseout_producer = self.__get_phaseout_producer(energy_sector_reform)
        self.phaseout_consumer = self.__get_phaseout_consumer(energy_sector_reform)
        self.phaseout_subsidy_tax = self.__get_phaseout_subsidy_tax(
            scenario_type, is_pc_phaseout_baseline, energy_sector_reform
        )


    def __get_phaseout_producer(
            self,
            energy_sector_reform: EnergySectorReform
            ) -> pd.DataFrame:
        """
        'Phaseout factor - fossil fuels (producer)' (v361)
        CPAT Excel: baseline 1817, scenario 6807

        Scenario specific
        returns dims <simulation_years[0] - 1, simulation_years[1]>
        """
        neagative_share = 1.0 - energy_sector_reform['ShareofProdSubPha']
        max_value = max(neagative_share, 1.0)

        phaseout_producer = pd.DataFrame(
            [np.full(len(self.__columns), max_value, dtype=float)],
            columns=self.__columns
        )

        if not energy_sector_reform['ProdSubPh']:
            return phaseout_producer

        decrease_each_year = (
            - energy_sector_reform['ShareofProdSubPha']
            / energy_sector_reform['FFSProdPhaseoutPeriod']
        )

        mask = self.__years > energy_sector_reform['YearProdSubPha']
        values = (
            1 + decrease_each_year * (self.__years[mask] - energy_sector_reform['YearProdSubPha'])
        )
        # for years > than ffs_start_prod:
        phaseout_producer = phaseout_producer.copy()   # pandas copy-on-write: .values is read-only
        phaseout_producer.iloc[0, mask] = np.maximum(values, neagative_share)

        return phaseout_producer


    def __get_phaseout_consumer(
            self,
            energy_sector_reform: EnergySectorReform
            ) -> pd.DataFrame:
        """
        'Phaseout factor - fossil fuels (consumer)' (v361)
        CPAT Excel: baseline 1818, scenario 6808

        Scenario specific
        returns dims <simulation_years[0] - 1, simulation_years[1]>
        """
        neagative_share = 1.0 - energy_sector_reform['ShareOfConsSubPha']
        max_value = max(neagative_share, 1.0)

        phaseout_consumer = pd.DataFrame(
            [np.full(len(self.__columns), max_value, dtype=float)],
            columns=self.__columns
        )

        if not energy_sector_reform['ConsSubPha']:
            return phaseout_consumer

        decrease_each_year = (
            - energy_sector_reform['ShareOfConsSubPha']
            / energy_sector_reform['FFPhaseOut']
        )

        mask = self.__years > energy_sector_reform['YearConsSubPha']
        values = (
            1 + decrease_each_year * (self.__years[mask] - energy_sector_reform['YearConsSubPha'])
        )
        # for years > than ffs_start_cons:
        phaseout_consumer = phaseout_consumer.copy()   # pandas copy-on-write: .values is read-only
        phaseout_consumer.iloc[0, mask] = np.maximum(values, neagative_share)

        return phaseout_consumer


    def __get_phaseout_subsidy_tax(
            self,
            scenario_type: str,
            is_pc_phaseout_baseline: bool, # TODO: input Dashboard!$V$76
            energy_sector_reform: EnergySectorReform
            ) -> pd.DataFrame:
        """
        'Phaseout factor - price controls (subsidy)' (v361)
        and
        'Phaseout factor - price controls (tax)' (v361)
        CPAT Excel: baseline 1820,1821, scenario 6810,6811

        Both have the same formulas in CPAT Excel

        Scenario specific
        returns dims <simulation_years[0] - 1, simulation_years[1]>
        """

        neagative_share = 1.0 - energy_sector_reform['ShareOfConsSubPha']
        max_value = max(neagative_share, 1.0)

        phaseout_subsidy_tax = pd.DataFrame(
            [np.full(len(self.__columns), max_value, dtype=float)],
            columns=self.__columns
        )

        baseline_condition = (scenario_type  != c.BASELINE) or is_pc_phaseout_baseline
        if not (energy_sector_reform['PrcContPha'] and baseline_condition):
            return phaseout_subsidy_tax

        decrease_each_year = (
            - energy_sector_reform['ShareOfConsSubPha']
            / energy_sector_reform['PrcControlPhaseout']
        )

        mask = self.__years > energy_sector_reform['YearPrcContPha']
        values = (
            1 + decrease_each_year * (self.__years[mask] - energy_sector_reform['YearPrcContPha'])
        )
        # for years > than pc_start:
        phaseout_subsidy_tax = phaseout_subsidy_tax.copy()   # pandas copy-on-write: .values is read-only
        phaseout_subsidy_tax.iloc[0, mask] = np.maximum(values, neagative_share)

        return phaseout_subsidy_tax
