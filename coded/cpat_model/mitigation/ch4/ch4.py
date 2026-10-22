import pandas as pd

import cpat_model.constants as c
from config import DATA_PATH

CH4_DATA_FILE_NAME = 'ch4_inputs'

RICE_CULTIVATION = 'Rice Cultivation'
LIVESTOCK = 'Livestock'
WASTE = 'TotalWaste'

NAME_TO_CODE_MAPPING = {
    RICE_CULTIVATION: c.RIC,
    LIVESTOCK: c.LIV,
    WASTE: c.WST
}

PRICE = 'price'
AVG_POW = 'avg_pow'

PRODUCTION = 'production'
PERCENT = 'percent'
PER_OTHER = 'per_other'
PER_AVG = 'per_avg'

PER_LIVESTOCK = 'per_livestock'
PER_RICE = 'per_rice'

# [Post policy GDP]

def get_ch4_data(
        selected_countries: list[str],
        simulation_years: tuple[int, int]
        ) -> dict[str, pd.DataFrame]:
    """
    Country filtering for raw data taken from (v361)
    CH4Inputs tab (2017-2029, years cut before 2017)

    Price is based on  G904 and H904

    countryname == Average is the only one with nans in CountryCode col!

    Average for per_rice in 'Rice Cultivation'
    and per_livestock in 'Livestock' were added in the DB,
    in order not to calculate it every time

    returns a dict with filtered data
    """
    data_filtered = {}
    start_year, end_year = simulation_years
    simulation_years = [str(year) for year in range(start_year, end_year + 1)]

    ch4_raw = (
        pd.read_csv(f'{DATA_PATH}/{CH4_DATA_FILE_NAME}.csv')
        .drop(columns=['countryname'])
        .set_index([c.COUNTRY_CODE, 'tier3'])
    )

    ch4_raw: pd.DataFrame = (
        ch4_raw[
            # NaN is for Average!
            (
                ch4_raw.index.get_level_values(c.COUNTRY_CODE).isin(selected_countries)
                | ch4_raw.index.get_level_values(c.COUNTRY_CODE).isna()
            )
            & ch4_raw.index.get_level_values('tier3').isin([RICE_CULTIVATION, LIVESTOCK, WASTE])
        ]
        .rename_axis(index={'tier3': c.FUEL_CODE})
        .rename(index=NAME_TO_CODE_MAPPING, level=c.FUEL_CODE)
    )

    # price
    liv_ric_price = (
        ch4_raw.loc[
            ~ch4_raw.index.get_level_values(c.FUEL_CODE).isin([c.WST])
        ]
        .loc[:, ['price_2022']].rename(columns={'price_2022': PRICE})
    )
    liv_ric_price_avg: pd.DataFrame = (
        liv_ric_price.loc[
            liv_ric_price.index.get_level_values(c.COUNTRY_CODE).isna()
        ]
        .droplevel(c.COUNTRY_CODE)
    )
    liv_ric_price = liv_ric_price.loc[~liv_ric_price.index.get_level_values(c.COUNTRY_CODE).isna()]

    # fill 0s with avg
    def fill_zeros(row):
        if row[PRICE] == 0:
            return liv_ric_price_avg.loc[row.name[1], PRICE]
        return row[PRICE]
    liv_ric_price[PRICE] = liv_ric_price.apply(fill_zeros, axis=1)

    # add missing countires and fill with avg
    data_countries = set(liv_ric_price.index.get_level_values(c.COUNTRY_CODE).unique())
    selected_countries = set(selected_countries)
    missing_countires = selected_countries - data_countries
    liv_ric_price = fill_missing_countires(missing_countires, liv_ric_price_avg, liv_ric_price)

    data_filtered[PRICE] = liv_ric_price.copy()

    # avg_pow
    avg_pow = ch4_raw.loc[:, ['avg_pow_a', 'avg_pow_b']]
    avg_pow_avg: pd.DataFrame = (
        avg_pow.loc[
            avg_pow.index.get_level_values(c.COUNTRY_CODE).isna()
        ]
        .droplevel(c.COUNTRY_CODE)
    )
    avg_pow = avg_pow.loc[~avg_pow.index.get_level_values(c.COUNTRY_CODE).isna()]

    # fill NaNs with avg
    # TODO: there are no cases like this in the DB
    # so it is not tested, if DB updated, have a look on it
    def fill_nas_from_avg(row):
        fuel_idx = row.name[1]  # Get the FUEL_CODE value
        for col in row.index:
            if pd.isna(row[col]):
                row[col] = avg_pow_avg.loc[fuel_idx, col]
        return row

    # # Apply the avg_pow row-wise
    avg_pow = avg_pow.apply(fill_nas_from_avg, axis=1)

    avg_pow = fill_missing_countires(missing_countires, avg_pow_avg, avg_pow)

    data_filtered[AVG_POW] = avg_pow.copy()


    # production
    production = (
        ch4_raw
        .loc[:, [f'{PRODUCTION}_2022']].rename(columns={f'{PRODUCTION}_2022': PRODUCTION})
        .fillna(0)
    )
    production_avg: pd.DataFrame = (
        production.loc[
            production.index.get_level_values(c.COUNTRY_CODE).isna()
        ]
        .droplevel(c.COUNTRY_CODE)
    )
    production = production.loc[~production.index.get_level_values(c.COUNTRY_CODE).isna()]
    production = fill_missing_countires(missing_countires, production_avg, production)
    data_filtered[PRODUCTION] = production

    # percent
    per = (
        ch4_raw.loc[
            ~ch4_raw.index.get_level_values(c.FUEL_CODE).isin([c.WST])
        ]
        .loc[:, [PER_RICE, PER_LIVESTOCK, PER_OTHER]]
    )
    per_other = (
        per[
            ~per.index.get_level_values(c.COUNTRY_CODE).isna()
            & per.index.get_level_values(c.FUEL_CODE).isin([c.LIV])
        ]
        [[PER_OTHER]]
        .droplevel(c.FUEL_CODE)
    )
    per_other = pd.concat(
        [
            per_other,
            pd.DataFrame({PER_OTHER: 0.0}, pd.Index(list(missing_countires), name=c.COUNTRY_CODE))
        ]
    ).sort_index()
    per = per[[PER_RICE, PER_LIVESTOCK]]
    def select_per(row):
        fuel_idx = row.name[1]
        if fuel_idx == c.RIC:
            return row[PER_RICE]
        elif fuel_idx == c.LIV:
            return row[PER_LIVESTOCK]
    per[PERCENT] = per.apply(select_per, axis=1)
    per = per[[PERCENT]]
    per_avg = per[per.index.get_level_values(c.COUNTRY_CODE).isna()].droplevel(c.COUNTRY_CODE)
    per = per[~per.index.get_level_values(c.COUNTRY_CODE).isna()]

    # missing countries fill with 0s
    per = fill_missing_countires(missing_countires, per_avg, per)
    per.loc[per.index.get_level_values(c.COUNTRY_CODE).isin(missing_countires), PERCENT] = 0.0


    data_filtered[PERCENT] = per
    data_filtered[PER_OTHER] = per_other
    data_filtered[PER_AVG] = per_avg

    return data_filtered


def fill_missing_countires(
        missing_countires: set[str],
        average_df: pd.DataFrame,
        countries_df: pd.DataFrame
        ) -> pd.DataFrame:
    if missing_countires:
        missing_countires_dfs = []
        for country in missing_countires:
            missing_country_df: pd.DataFrame = (
                average_df
                .reset_index()
                .assign(**{c.COUNTRY_CODE: country})
            )
            missing_country_df.set_index([c.COUNTRY_CODE, c.FUEL_CODE], inplace=True)
            missing_countires_dfs.append(missing_country_df.copy())
        countries_df = pd.concat([countries_df] + missing_countires_dfs).sort_index()

    return countries_df
