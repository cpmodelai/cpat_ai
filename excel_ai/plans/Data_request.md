# Data request

Four items need data from the CPAT data team. Nothing is built until the data arrive. Until then the workbook keeps the fills described in the register (`issues_register.py`). Send one file per item, in the legacy layout. The data steps then load it unchanged.

| Issue | Priority | What we need | Format | Where it goes |
|---|---|---|---|---|
| I64 | High | GAINS combustion emission-factor paths by year: CH4, N2O and local pollutants, by fuel and sector, for every country. The NoPropData legacy file has zeros in these rows because the data are proprietary. | The legacy CPAT file with the proprietary tables, or sheet `EF_PM` of it (same columns as legacy) | Sheet `EF_PM` (legacy table, loaded by `extract_legacy_tables.py`). The prototype then reads the paths instead of the linear fill to EFEndYear (LegacyDiff LD47). |
| I65 | High | The blank VAT cells of the IMF price dataset: which are missing values and which are true zeros. | The corrected price dataset (legacy `Prices_dom` layout), or a list of country, fuel, sector and VAT rate | `data/` price files through `extract_data.py` (sheet `Prices_dom`). The prototype fill (general VAT rate for residential coal and gas and for oil products; LegacyDiff LD3) is then dropped. |
| I13 | Medium | The proprietary tables for all countries: Balances, EnergyCons, EF_PM, IO_GTAP, HHSurvey, ASPIRE, WHOCooking. The NoPropData file holds Egypt only. | The full legacy CPAT file, or the CPAT data pipeline output | The legacy data tabs of the same names (`extract_legacy_tables.py`). Then rebuild BaselineCO2 for scenario 1 and test a second country end to end. |
| I68 | Low | Historical GHG emissions 2018-2020 by country: GHGs excluding and including LULUCF, and CO2. Also any NDC reference year after 2017 that the inventory (2021-2024) does not cover. | Legacy `GHGs` rows 954-1189 layout with the extra year columns | Sheet `GHGHist`. NDC reference years 2018-2020 then stop returning N/A. |

Contacts and status are tracked in the team tracker (`legacy/workbooks/Tracking issues.xlsx`, tabs BUGS and ISSUES-OTHER).

