from typing import Dict, Optional
import pandas as pd


class MitIndicatorsCommon:
    def _extend_indexrs(
            self,
            df: pd.DataFrame,
            column_name: str, 
            aggr: str
            ) -> pd.DataFrame:
        assert (
            column_name in ['SectorCode', 'FuelCode']
        ), f"Error: Column: {column_name} is not one of: 'SectorCode' or 'FuelCode'."
        assert (
            aggr in ['ren', 'rnw', 'tot']
        ), f"Error: Group: {aggr} is not one of the defined ones."
        return (
            df
            .assign(**{column_name: aggr})
            .set_index(column_name, append=True)
        )

    def _map_to_group(
            self,
            code: str,
            mapping: Dict[str, str]
            ) -> Optional[str]:
        if code in mapping:
            return mapping[code]
        else:
            return pd.NA
