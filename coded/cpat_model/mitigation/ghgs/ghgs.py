import pandas as pd

import cpat_model.constants as c
from config import DATA_PATH

GHGS_DATA_FILE_NAME = 'ghgs'

SOURCES_TO_LOAD = ['3.  Agriculture', '5.  Waste']
SOURCE_MAPPING = {
    '3.  Agriculture': c.AGR,
    '5.  Waste': c.WST
}

# [Post policy GDP]

def get_ghgs_data(
        selected_countries: list[str],
        ) -> dict[str, pd.DataFrame]:
    """
    Filtering for raw data taken from (v361)
    GHGs tab (2018-2022 years taken from CPAT Excel)

    'ISO' col renamed to 'CountryCode'
    'Source' and 'UNFCCC category' cols omitted

    Tables for all years stacked to one table

    Sources (categories) are in top level index
    Rest of the columns are in second level index

    returns a dict with filtered data, df dims (c, gas), t in the dataset
    """
    filtered_data = {}
    ghgs_raw: pd.DataFrame = (
        pd.read_csv(f'{DATA_PATH}/{GHGS_DATA_FILE_NAME}.csv', header=[0, 1], encoding='utf-8-sig')
        .drop(('Unnamed: 0_level_0', 'Country'), axis=1)
    )
    ghgs_raw = ghgs_raw[ghgs_raw[('Unnamed: 1_level_0', c.COUNTRY_CODE)].isin(selected_countries)]

    cols_to_keep = [
        ('Unnamed: 1_level_0', c.COUNTRY_CODE),
        ('Unnamed: 2_level_0', 'Year')
    ]
    for source in SOURCES_TO_LOAD:
        source_cols = [col for col in ghgs_raw.columns if col[0] == source]
        ghgs_by_source = ghgs_raw.loc[:, cols_to_keep + source_cols]
        ghgs_by_source.columns = ghgs_by_source.columns.get_level_values(1)

        ghgs_by_source = (
            ghgs_by_source
            .melt(
                id_vars=[c.COUNTRY_CODE, 'Year'],
                var_name=c.GAS,
                value_name='Value'
            )
        )
        ghgs_by_source = (
            ghgs_by_source
            .pivot_table(
                index=[c.COUNTRY_CODE, c.GAS],
                columns='Year',
                values='Value'
            )
        )
        ghgs_by_source.columns = ghgs_by_source.columns.astype(str)
        ghgs_by_source.columns.name = None

        filtered_data[SOURCE_MAPPING[source]] = ghgs_by_source.copy()

    return filtered_data
