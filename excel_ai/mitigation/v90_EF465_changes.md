# v9.0 group EF465: non-CO2 combustion emission factors as legacy 465 (changes for the integrator)

Problem (2026-10-29): the prototype's local-pollutant and combustion-CH4 factors (Inputs `ch4s`..`ap1_co`, `nc_ef`,
`ef_fallback`, `CH4_SUB`; EF_PM read through NCKey/NCIn/NCFin) were Egypt-only GAINS factors with our own subsector
mapping (L58) and nearest-match fallback (L59). Legacy 465 (Mitigation rows 1052-1663) looks them up differently, so
e.g. food & forestry diesel black carbon was 2.51 t/ktoe (construction fallback) against legacy 0.0043836 t/ktoe and
section 15 food & forestry BC 2,199 t against legacy 3.8 t.

## What changed
- **Data:** `extract_legacy_tables.py` writes `data/mvp_legacy_extracts/legacy_EF_PM.csv` whole (39,322 rows: all
  countries and the World Bank regions eas, eca, ecs, lcn, mea, nac, sas, ssf, legacy order; was Egypt's 229 rows).
  `EGYPT_ONLY` no longer lists EF_PM; `python3 extract_legacy_tables.py efpm` re-extracts this table only. The legacy
  lookup range `EF_PM!$A$3:$A$39323` covers every data row. EF_PM has no `wld` rows (the world step never matches,
  as in legacy).
- **New data step `Inputs_nc`** (merged into Inputs, last block; names `NCEfKey`, `NCEfIn`, `NCEfFin`): one row per
  legacy EF code `<sub>.<fuel>.<pollutant>` of legacy rows 1052-1663 (pollutants pm2, nox, so2, voc, bc, oc, ch4, co;
  subsectors pow, rod, ral, avi, res, cst, srv, mnf, omn, foo, oen with legacy's fuels) plus navigation (`nav` die,
  oop). Columns as the CO2 table of Inputs_ef: code of the country (`CodePrefix&"ef."`), of its region (`CtryReg`, Settings
  C43 = legacy `_region_code`, Egypt `mea`), of the world; the code used (first that exists, legacy F); FE in and FE
  fin x EFtPerKtoe (legacy L and I; IFERROR -> 0 as legacy IFNA). `oen` rows: `MAXIFS` of the same fuel over the
  other subsectors of the pollutant block, power included (legacy rows 1117-1124 `MAX(IF($D1052:$D1114=...))`).
- **Inputs:** `ch4s` = legacy EF subsector code of the subsector (`CH4_SUB`: srv -> srv, ral -> ral, oen -> oen; mch,
  irn, nfm, mac, cem, ftr -> mnf as legacy rows 6388-6395; nav -> nav), `ch4f` = fuel (aviation kerosene -> jfu);
  `ch4a`, `ch4b`, `ap0_*`, `ap1_*` read `Inputs_nc` by key. Columns `efxs`, `efxf`, `efok`, `efs`, `eff` removed
  (later Inputs columns move 5 to the left; all references go through `IC`). `ef_fallback` removed.
- **Inputs_power** `ap0_*/ap1_*` and the power CH4 parameters (`ch4.pw.*`, section 14) read the same table (`pow`).
- `nc_ef()` builds `IFERROR(INDEX(NCEfIn|NCEfFin,MATCH(sub&"."&fuel&".pol",NCEfKey,0)),0)`.
- Base/final line with EFSel as before (issue I98, unchanged).
- **check_full.py:** `_nc_table()` recomputes the same table in Python from `legacy_EF_PM.csv` (country, World Bank
  region from `legacy_Countries_cells.csv`, world; oen max); `NC_ALL`/`NC_EF` come from it; `nc_sub` is the plain
  `CH4_SUB` mapping. `ef_nonco2.csv` (extract_ghg.py, Egypt only) is no longer read by check_full (kept as is).
- Methods docs: `docs/methods/Emissions.md` (data rows, factor section, results, differences), `Data_tabs.md`
  (Inputs_nc). Variables-table texts of `ch4` and `ap` updated (legacy rows 1052-1663, 6591-7409; 7203-7307 for CH4).

## Where the 465 chain finds no factor
465 gives 0 (kept): pow.bio, rod.ker, res.oop, cst.coa/nga/oop/bio, srv.coa, omn.coa, foo.coa (all pollutants), and
single pollutants GAINS omits (e.g. so2, voc, oc of LPG in mnf/omn/foo/srv; oc and so2 of res.lpg). Pairs outside the
legacy table (rod.oop, ral other than diesel, res.gso/die, jfu outside aviation) also 0, as legacy. **None of these
burns fuel in Egypt** (prototype Balances 2022), so the L59 nearest-match fallback is not kept anywhere.

## Register / tracker updates
- **L58** (subsectors without a GAINS match): status "Fixed by the CPAT team in 465: legacy 465 has EF codes for
  services, rail, construction, other manufacturing, food & forestry and other energy, and maps mining & chemicals,
  iron & steel, other metals, machinery, cement and fuel transformation to manufacturing (rows 6388-6395); the
  prototype follows 465 (v9.0, EF465). Navigation is still missing in 465 (bug L22, our fix kept: GAINS nav factors)."
- **L59** (fuels without a GAINS factor): "Fixed by the CPAT team in 465: each factor is the country's, else its World
  Bank region's, else the world's (rows 1052-1663 F); Egypt's residential and fuel-transformation LPG, other-mining
  diesel and food & forestry diesel take the Middle East & North Africa factors. The prototype follows 465 (v9.0,
  EF465); our nearest-match fallback is retired (where the 465 chain still gives 0, no fuel is burnt in Egypt)."
  Bug-report wording / Fix column: "Fixed by the CPAT team in 465 (country, region, world lookup)". The Location
  "Mitigation rows 15885-16685" should read "Mitigation rows 1052-1663 (465)".
- **New issue (proposed I147; number to confirm)**, Mitigation, Minor, Replicated: "Other energy use takes the largest
  emission factor of each fuel across all other subsectors" -- Location: Mitigation rows 1117-1124 and the oen rows of
  every pollutant block (legacy note "The EF of this sector is equal to the max across other sectors"); power
  included; CH4 rows blank in legacy. Prototype: Inputs_nc oen rows (`MAXIFS`). Caveat: legacy takes the maximum year
  by year; the prototype takes the maximum of the base and of the final factor and the line between them: identical
  where one subsector holds the maximum (Egypt: oen burns only other oil products, linear in legacy: exact); differs
  for gasoline and biomass PM2.5/BC/OC (up to 0.32 t/ktoe mid-path) where oen burns none in Egypt.
- **I34** (CH4 of the air-pollution table): note "Legacy 465 rows 1514-1586 (CH4 factors) have the F and I lookups
  but no L/AC values, so legacy combustion CH4 is 0; the prototype fills them with the same 465 chain (v9.0)".
- **I98** unchanged.
- SEE_ALSO: add `'I147': ['L58', 'L59']` if the integrator wants the cross-reference.

## LegacyDiff rows
- **'Local pollutants: factor mapping (v2.9)'** (LD49): replace with: Legacy: "465: factors by legacy EF code
  (country, else World Bank region, else world; mnf = mch, irn, nfm, mac, cem, ftr; other energy the maximum of the
  other subsectors; no factor -> 0)". Prototype: "The same (v9.0, EF465; table Inputs_nc)". Reason: "Bugs L58 and L59
  fixed by the CPAT team in 465". Effect: "None for Egypt in 2022 (all sectors equal legacy but navigation, L22)".
  Type: "Same".
- **'Local pollutants: navigation (v2.9)'** (L22): unchanged; navigation takes its own GAINS factors (`nav`, country
  else region), the only remaining 2022 difference in the module table.
- 'GHGs: combustion CH4' wording, if a LegacyDiff row mentions the L59 fallback for CH4: "factors as legacy 465
  (legacy has the lookups but blank CH4 factors, I34)".

## Results (Egypt, scenario 1; section 15 vs legacy 465 rows 15844-16053, tonnes)
2022: **every module sector and pollutant equals legacy** (cpp 0; gpp NOx 96,931; opp SO2 154,644; rod NOx 557,470;
gro NOx 16,486 / SO2 1,713 / BC 4,794; foo NOx 5,498 / SO2 3,299 / BC 3.8 / PM2.5 6.9; before: foo BC 2,199, NOx
40,311, SO2 776) **except**:
- `oth`: + navigation (bug L22, our fix; 271 ktoe of other oil products): NOx 119,598 vs 104,831 (+14,767 = nav),
  SO2 130,064 vs 116,377 (+13,687), BC 756 vs 131 (+625), PM2.5 2,613 vs 1,121 (+1,492), OC 479 vs 81 (+398), VOC
  4,347 vs 4,006 (+341), CO 39,237 vs 36,396 (+2,840). By subsector (ral, avi, mnf, omn, oen) equal to legacy.
- CH4 (all sectors): combustion CH4 and all supply methane in the prototype, legacy combustion 0 (I34): gpp 56,706 t
  (legacy 0), rod 28,759, gro 41,830 (was 67,720: residential LPG no longer takes the gas factor), oth 89,584 (legacy
  64,002), foo 1,970,674 (legacy 1,871,853).
- Modelled ambient PM2.5 (17b) 2022: 33.06 ug/m3 (was 115.6) against legacy AP 981 30.17; the 2.89 difference is
  navigation's (sum of nav emissions x the `oth` coefficients = 2.89).
2030: the factors follow the same line; sectors differ from legacy by the modelled fuel use, not the factors: gpp 0.879
of legacy for every pollutant, opp 0.622, rod 0.70-0.77, gro 0.70 (NOx) to 1.0, foo 0.584, mnf 0.84-0.92, omn 0.60-0.92.
These are outside this group (fuel-use paths, power and transport models).

## Quick check
PASS (no error values; formulas <= 100 characters; lint 0). Output codes vs the pre-change build: 260 codes change,
none new or gone: `em.*` (section 15 and subsector rows), `aps.*`, combustion CH4 (`ch4.c.bld/ind/tot`: 2022 bld 67.9
-> 41.9 kt, total 181.9 -> 151.6 kt), `ghg.enrp.enr.all` (198.55 -> 197.95 Mt CO2e in 2022: energy CH4 equals the
inventory in GHGYear and moves after it with modelled combustion + supply CH4, whose mix changed), forcing (`apf.tot.tot` 2022 -17.75 -> -18.35;
bc 11.55 -> 10.79, nox -6.03 -> -5.77, so2 -25.94 -> -26.10), modelled PM2.5 (`air.con.pm2.*`: foo 85.3 -> 2.74,
total 115.6 -> 33.06) and the scenario-2 welfare (`wel.air.usd` 2030 3.76 -> 0.72 USD bn, `wel.tot` 8.25 -> 5.21,
`wel.pct.tot` 0.0107 -> 0.0068).

## New inputs
None (no MTInputs / ScenarioDefinition / Settings input; MT_LAST unchanged). New sheet block Inputs_nc (data step,
merged into Inputs as its last block; `tabs.json` updated by the build).

## Version-log sentence
"v9.0 (EF465): local-pollutant and combustion-CH4 factors as legacy 465 rows 1052-1663 (table Inputs_nc: legacy EF
code, country else World Bank region else world, other energy the maximum of the other subsectors, issue I147); EF_PM
holds all countries and regions; bugs L58 and L59 fixed by the CPAT team in 465 (our fallback retired); section 15
equals legacy in 2022 except navigation (L22) and CH4 (I34); modelled PM2.5 2022 33.06 against 30.17 (navigation)."

## Caveats (CAVEATS.md)
- The oen maximum is taken on the base and final factors, not year by year (exact for Egypt).
- `ef_nonco2.csv` (extract_ghg.py) is now unused by the checks; it still holds Egypt's rows only.
- The full check (`check_full.py`) was not run (quick check only); `_nc_table()` was checked against the legacy
  cached factors (e.g. foo.die.bc 0.0043836, oen.oop.pm2 0.367915 t/ktoe) and section 15 2022 equals legacy.
- The workbook grows by the all-country EF_PM (39k rows; quick file 12.5 MB).
