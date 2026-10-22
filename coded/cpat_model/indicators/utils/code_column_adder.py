import pandas as pd

from cpat_model.indicators.utils.decorators import with_indicators_schema

class CodeColumnAdder:

    @staticmethod
    @with_indicators_schema(unit='ktoe', header_key='dec')
    def mit_ener_s_f_e(
        df: pd.DataFrame,
        suffix: str
        ) -> pd.DataFrame:

        df['CPATCode'] = [
            f'{c.lower()}.mit.ener.{s}.{f}.e.{suffix}'
            for c, s, f in zip(
                df.index.get_level_values('CountryCode'),
                df.index.get_level_values('SectorCode'),
                df.index.get_level_values('FuelCode')
                )
            ]
        return df

    @staticmethod
    @with_indicators_schema(unit='ktoe', header_key='dec')
    def mit_ener_s_tot_e(
        df: pd.DataFrame,
        suffix: str
        ) -> pd.DataFrame:

        df['CPATCode'] = [
            f'{c.lower()}.mit.ener.{s}.tot.e.{suffix}'
            for c, s in zip(
                df.index.get_level_values('CountryCode'),
                df.index.get_level_values('SectorCode')
                )
            ]
        return df

    @staticmethod
    @with_indicators_schema(unit='ktoe', header_key='dec')
    def mit_ener_pow_f_e(
        df: pd.DataFrame,
        suffix: str
        ) -> pd.DataFrame:

        df['CPATCode'] = [
            f'{c.lower()}.mit.ener.pow.{f}.e.{suffix}'
            for c, f in zip(
                df.index.get_level_values('CountryCode'),
                df.index.get_level_values('FuelCode')
                )
            ]
        return df

    @staticmethod
    @with_indicators_schema(unit='ktoe', header_key='ec')
    def mit_ener_con_f(
        df: pd.DataFrame,
        suffix: str
        ) -> pd.DataFrame:

        df['CPATCode'] = [
            f'{c.lower()}.mit.ener.con.{f}.{suffix}'
            for c, f in zip(
                df.index.get_level_values('CountryCode'),
                df.index.get_level_values('FuelCode')
                )
            ]
        return df

    @staticmethod
    @with_indicators_schema(unit='ktoe', header_key='ec')
    def mit_ener_con_tot(
        df: pd.DataFrame,
        suffix: str
        ) -> pd.DataFrame:

        df['CPATCode'] = (
            df.index
            .get_level_values('CountryCode')
            .map(lambda x: f'{x.lower()}.mit.ener.con.tot.{suffix}')
        )
        return df

    @staticmethod
    @with_indicators_schema(unit='ktoe', header_key='ec')
    def mit_ener_tot_tot(
        df: pd.DataFrame,
        suffix: str
        ) -> pd.DataFrame:

        df['CPATCode'] = (
            df.index
            .get_level_values('CountryCode')
            .map(lambda x: f'{x.lower()}.mit.ener.tot.tot.{suffix}')
        )
        return df

    @staticmethod
    @with_indicators_schema(unit='ktoe', header_key='ec')
    def mit_ener_f_s_aggr(
        df: pd.DataFrame,
        suffix: str
        ) -> pd.DataFrame:

        df['CPATCode'] = [
            f'{c.lower()}.mit.ener.{f}.{s}.{suffix}'
            for c, s, f in zip(
                df.index.get_level_values('CountryCode'),
                df.index.get_level_values('SectorCode'),
                df.index.get_level_values('FuelCode')
                )
            ]

        return df

    @staticmethod
    @with_indicators_schema(unit='twh', header_key='ec')
    def mit_elec_twh_f(
        df: pd.DataFrame,
        suffix: str
        ) -> pd.DataFrame:

        df['CPATCode'] = [
            f'{c.lower()}.mit.elec.twh.{f}.{suffix}'
            for c, f in zip(
                df.index.get_level_values('CountryCode'),
                df.index.get_level_values('FuelCode')
                )
            ]

        return df

    @staticmethod
    @with_indicators_schema(unit='twh', header_key='ec')
    def mit_elec_twh_tot(
        df: pd.DataFrame,
        suffix: str
        ) -> pd.DataFrame:

        df['CPATCode'] = (
            df.index
            .get_level_values('CountryCode')
            .map(lambda x: f'{x.lower()}.mit.elec.twh.tot.{suffix}')
        )
        return df

    @staticmethod
    @with_indicators_schema(unit='ktoe', header_key='ec')
    def mit_ener_tot_f_e(
        df: pd.DataFrame,
        suffix: str
        ) -> pd.DataFrame:

        df['CPATCode'] = [
            f'{c.lower()}.mit.ener.tot.{f}.e.{suffix}'
            for c, f in zip(
                df.index.get_level_values('CountryCode'),
                df.index.get_level_values('FuelCode')
                )
            ]
        return df

    @staticmethod
    @with_indicators_schema(unit='ktoe', header_key='p') #TODO: p or ec?
    def mit_rp_s_f_a(
        df: pd.DataFrame,
        suffix: str
        ) -> pd.DataFrame:

        df['CPATCode'] = [
            f'{c.lower()}.mit.rp.all.{f}.a.{suffix}'
            for c, f in zip(
                df.index.get_level_values('CountryCode'),
                df.index.get_level_values('FuelCode')
                )
            ]
        return df
    
    @staticmethod
    @with_indicators_schema(unit='mtCO2', header_key='em')
    def mit_co2_f(
        df: pd.DataFrame,
        suffix: str
        ) -> pd.DataFrame:

        df['CPATCode'] = [
            f'{c.lower()}.mit.co2.{f}.{suffix}'
            for c, f in zip(
                df.index.get_level_values('CountryCode'),
                df.index.get_level_values('FuelCode')
                )
            ]
        return df
    
    @staticmethod
    @with_indicators_schema(unit='mtCO2', header_key='em')
    def mit_co2_s(
        df: pd.DataFrame,
        suffix: str
        ) -> pd.DataFrame:

        df['CPATCode'] = [
            f'{c.lower()}.mit.co2.{s}.{suffix}'
            for c, s in zip(
                df.index.get_level_values('CountryCode'),
                df.index.get_level_values('SectorCode')
                )
            ]
        return df

    
    @staticmethod
    @with_indicators_schema(unit='mtCO2', header_key='em')
    def mit_co2_enr_tot(
        df: pd.DataFrame,
        suffix: str
        ) -> pd.DataFrame:

        df['CPATCode'] = (
            df.index
            .get_level_values('CountryCode')
            .map(lambda c: f'{c.lower()}.mit.co2.enr.tot.{suffix}')
        )
        return df
    
