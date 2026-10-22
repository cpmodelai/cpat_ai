# Local air pollutants: method (CPAT-AI-Mitigation-Prototype v6.4)

Equations: `Equations.md`; workbook formulas: `Formulas.md`.

The model computes emissions of seven local air pollutants from the fuel use of every subsector and of power generation: fine particulate matter (PM2.5), nitrogen oxides (NOx), sulphur dioxide (SO2), volatile organic compounds (VOC), black carbon (BC), organic carbon (OC) and carbon monoxide (CO). A memo converts them into CO2 equivalents (forcing). The emissions are also grouped into the sectors of the legacy air-pollution module, with primary organic matter and other PM2.5, its inputs. The pollutants are not part of the GHG totals. LiveOutputs reports total PM2.5, NOx, SO2, black carbon and the forcing for every scenario; the Charts sheet plots PM2.5 and SO2.

Units: emissions in kt; factors in t per ktoe; forcing in Mt CO2e (GWP100).

## 1. Data

| Sheet | Content | Source |
|---|---|---|
| EF_NonCO2 | Combustion emission factors by GAINS subsector, fuel and pollutant, base year and final, kt per PJ | Legacy sheet EF_PM (GAINS); also used for combustion CH4 |
| GWP_AP | GWP100 of the pollutants by GAINS region | Legacy GWP table of the pollutant forcing |
| Countries (column O) | GAINS region of every country (Egypt: `afr`) | Legacy Countries tab |

Each subsector takes the GAINS subsector of its CH4 factor: services use the residential factors, rail the road factors, and industry and other energy use the manufacturing factors (legacy bug L58). Power uses factors by generation type.

A fuel that its GAINS subsector has no factor for takes the nearest GAINS match (v4.12, legacy bug L59, user decision 2026-10-18; was issue I35; Inputs columns `efxs` to `eff`):

- LPG takes natural gas of the same GAINS subsector (both are gaseous fuels burnt in similar appliances; the only LPG factors in the data are for construction, i.e. off-road engines, with a CO factor about 300 times that of a gas stove);
- food & forestry takes construction (off-road machinery);
- biomass takes residential;
- any other fuel takes manufacturing (construction for manufacturing itself).

Egypt 2022: residential LPG (3,182 ktoe) takes residential gas, other mining diesel (3,819) and fuel transformation LPG (2,466; manufacturing gas) the manufacturing factors, food & forestry diesel (927) construction diesel. A pollutant missing for a fuel that the subsector does have factors for (for example organic carbon of manufacturing coal) stays 0: GAINS lists no zero factors.

## 2. Method

1. **Factor path**: the weight of the final factor rises linearly from 0 in the base year to 1 in 2039 (`EFEndYear`) and stays at 1, as for combustion CH4.
2. **Emissions**: for each subsector and pollutant, the sum over the eight fuels of fuel use x the weighted factor. Fuel use is the modelled one, so prices, policies and scenarios carry through. Power uses the same equation over the nine generation types.
3. **Totals**: transport, buildings and industry sum their subsectors, navigation included. A pollutant's total is the subsectors plus power.
4. **Forcing (memo)**: emissions x the region's GWP100 for BC, OC, NOx, SO2, VOC and CO, and their sum. Cooling pollutants (OC, SO2, NOx) have a negative GWP, so the net forcing can be negative: about -17.5 Mt CO2e for Egypt in 2022.
5. **Air-pollution module sectors**: coal power plants and gas power plants (fuel use of the type x the power factors); other power plants (power less coal and gas); ground level road (road); ground level other (residential, services, construction); other (rail, aviation, navigation, industry without construction, other energy use); food & forestry. The seven sectors add up to the pollutant's total.
6. **Primary organic matter (POM) and other PM2.5**, per sector: POM = 1.3 x organic carbon; other PM2.5 = MAX(0, PM2.5 - black carbon - POM).
7. **The module's input table (v3.12)**: the block takes the layout of the legacy input table (Mitigation rows 15859-15961):
   - one block per module sector (coal, gas and other power plants, ground level road, ground level other, other, food & forestry) and one for all sectors;
   - in each block the ten pollutants in legacy order: NOx, SO2, BC, POM, other PM2.5, VOC, CH4, CO, PM2.5, OC;
   - codes `aps.<pollutant>.<sector>`, in kt (legacy: tonnes).

   The air-pollution module reads these rows directly (NORMS 3c).
8. **CH4 in the table, as legacy (issue I34)**:
   - coal, gas and other power plants: combustion CH4 of the generation types (section 14);
   - road, ground level other: combustion CH4 of their subsectors (`ch4` rows of sections 5-8);
   - other: combustion CH4 of its subsectors plus fossil fuel supply methane (`ch4.sup`; legacy has oil and gas extraction only);
   - food & forestry: combustion CH4 plus agriculture (livestock, rice) and waste methane, as legacy.

   Legacy has no combustion CH4 factors, so its combustion part is zero. CH4 here is uncalibrated: it is not scaled to the inventory (`ghg.k`).

## 3. Results for Egypt (scenario 1)

v4.12 (with the nearest GAINS factors, bug L59): PM2.5 is 95.6 kt in 2022 and 94.8 kt in 2040; NOx 886 kt in 2022. The check recomputes all rows of the block in Python for scenarios 1 and 2.

The module's input table in 2022 (kt): NOx 886, SO2 317, BC 33.2, POM 48.3, other PM2.5 14.1, VOC 377, CH4 2,150, CO 2,473, PM2.5 95.6, OC 37.2. Sectors without the fuels of bug L59 match the legacy input table (rows 15861-15948, in tonnes): gas power plants' NOx is 104,502 t and road NOx 569,560 t in both. Before v4.12 (fuels without a factor at 0, as legacy) the totals were NOx 801, SO2 300, PM2.5 90.8: the fix adds residential LPG (as gas), mining and food & forestry diesel and fuel transformation LPG. CH4 is above legacy's 1,936 kt also because the prototype adds combustion CH4 and all fuel-supply methane, while legacy has extraction only (I34).

Forcing in 2022: total -18.6 Mt CO2e (v4.11: -17.5; legacy cached -16.3); black carbon 11.9, CO 4.9, VOC 2.3, organic carbon -4.5, NOx -6.3, SO2 -27.0. The legacy values differ by the fuels of bug L59, and by 2040 also because fuel use and the factor paths differ.

## 4. Differences with legacy CPAT (sheet LegacyDiff)

- Legacy omits navigation from the pollutant totals (bug L22). It is included here.
- Legacy leaves services and food & forestry out of each pollutant's total (bug L23), although its air-pollution sectors include them. Here the total is the sum of the sectors.
- Legacy gives fuels with no GAINS factor zero emissions (legacy bug L59, user decision 2026-10-18; was issue I35). Egypt 2022: residential LPG, mining diesel, food & forestry diesel and fuel transformation LPG, about 10 Mtoe in all; food & forestry shows about 1 t of NOx in legacy (row 15939). Here they take the nearest GAINS match (section 1).
- Legacy gives a zero factor to subsectors with no GAINS match (legacy bug L58, user decision 2026-10-18; was issue I27). Here every subsector is mapped to a GAINS subsector.
- Food & forestry is split into food and forestry/agriculture as legacy (v4.11, LD53): the food share of each fuel is info_food over the four info_ flows of the processed Balances (legacy rows 501-504, 1666-1673); rows apfd (food fuel use) and ap.<pollutant>.fod / .fag (memo rows, not in the totals). The share is 0 for Egypt.
- Legacy has no ammonia (NH3) from fuel combustion, so neither does the prototype.
- Legacy reads factor paths by year, which are proprietary and empty in the NoPropData file. The prototype draws a linear path between the base and final factors (simplification, as for CH4).
- Not built yet: the air-pollution (health) module that would use these sectors.
