# Standalone Distribution module (Egypt)

`CPAT_Distribution_Standalone_Egypt.xlsx` is a standalone rebuild of the household
distributional/incidence module from `excel_ai/original/CPAT 1.0pre_456_NoPropData.xlsb`
(sheet "Distribution"), scoped to Egypt only. See the workbook's own **ReadMe** tab for
scope, structure and verification notes.

## Pipeline

```
extract_egypt.py   reads the source .xlsb (pyxlsb) + data/distribution/data_tabular,
                    filters everything to Egypt, and writes egypt_data.pkl

build_workbook.py   reads egypt_data.pkl and writes:
                      - CPAT_Distribution_Standalone_Egypt.xlsx (data tabs, Distribution_
                        Inputs, Distribution_Outputs, ReadMe -- all labels/structure/
                        styling, but with formula cells and the LAMBDA library left BLANK)
                      - RebuildDistributionModule.bas (a VBA macro that adds the LAMBDA
                        names and writes every formula cell via Excel's own object model)

reference_calc.py   a pure-Python re-implementation of the same LAMBDA logic, used to
                    validate the design against the source workbook's cached Egypt values
                    before it was encoded as Excel formulas. Not part of the shipped
                    workbook; kept for anyone who wants to re-verify or extend the model.
```

### Why the .bas file

Excel's .xlsx format requires every "future function" (LAMBDA, LET, XLOOKUP, HSTACK,
SCAN, MAKEARRAY -- anything added after the OOXML spec froze) to be written internally
with an `_xlfn.` prefix, and every LAMBDA/LET parameter name to carry an `_xlpm.` prefix,
in both its declaration and every reference to it. Getting this byte-for-byte right by
hand-writing XML (via openpyxl) proved unreliable across Excel versions/builds -- Excel
would silently strip the offending names/formulas and show a "needs repair" prompt.
Shipping the workbook with everything left blank, plus a macro that recreates the LAMBDA
names and formulas through Excel's own `Names.Add` / `Range.Formula2` API, sidesteps the
encoding problem entirely: Excel does its own internal encoding, guaranteed correct.

To use: open the .xlsx, Alt+F11, Insert > Module, paste in `RebuildDistributionModule.bas`,
then run `RebuildDistributionModule` (F5). It defines all 39 named LAMBDA functions plus
the plain named ranges, then writes all ~1,400 formula cells in Distribution_Inputs and
Distribution_Outputs, then forces a full recalculation.

Re-run with:

```
python3 extract_egypt.py     # needs excel_ai/original/CPAT 1.0pre_456_NoPropData.xlsb
python3 build_workbook.py    # needs egypt_data.pkl
```

`egypt_data.pkl` is checked in so `build_workbook.py` can be re-run (e.g. to tweak
formatting or add sections) without re-reading the large source `.xlsb`.

## Versions

- **v0.5 (2026-10-17):** `NET_EFFECT` gives the basket (decile 0) as total recycled / total consumption, so the three `#VALUE!` cells (Distribution_Outputs P1408, P1411, P1414) are gone. Cause: recycled amounts exist per decile only, and `ASPIRE_PC` with decile 0 asked for `CHOOSECOLS(row, 0)`. `CPAT_Distribution_Standalone_Egypt_v0.5.xlsx` is v0.4 with that one name changed (and full recalculation on open); `build_workbook.py` and `RebuildDistributionModule.bas` carry the same change. Python check (`reference_calc.py` logic): basket net effect Overall -0.052, Urban -2.29, Rural -2.58 (% of consumption; negative = net gain). Urban and Rural use the Overall recycled amounts over their own consumption, a prototype simplification kept from v0.4.
