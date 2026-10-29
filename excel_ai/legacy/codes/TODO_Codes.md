# TODO - Codes increment (CPAT code protocol): done in v0.7.2

Open items moved to [`excel_ai/plans/TODO.md`](../../plans/TODO.md) section 4. Record of the steps below; plan: [`Codes_Remediation_Plan_v0_7_1.md`](Codes_Remediation_Plan_v0_7_1.md).

## Steps (each: build, `check_codes`, quick check with 0 changed / 0 new / 0 gone through the rename map, one commit)

- ☑ (2026-10-22) **R0 - mechanism, empty map:** done: `build.py` (`load_renames`, `rn_stem`, `apply_renames` after `build_distribution`), `check_codes_v0_7_2.py` (cells through the map, codes, stems; `--values`: recalculated values against the release), `check_quick` maps the release's codes; empty map: 1,242,186 cells equal; dry run `gen` -> `gen_mwy`: cells explained, 272,860 values equal; reverted (status planned).
  - rename map `data/mvp_legacy_extracts/code_renames_v7_x.csv`;
  - the five write points (columns A-C, dictionary key, member pairs, output-sheet code literals, dictionary code end);
  - `check_codes_v7_x.py` (cell-by-cell against the last release, no recalculation);
  - the rename-aware regression in `check_quick`.

  Pass: the workbook equals the last release cell for cell. Then a dry run with `gen` -> `gen_mwy`, reverted.
- ☑ (2026-10-22) **R1 - model letters:** done (map row `codeend * -> ''`: 49 dictionary suffixes cleared; no new duplicate; cells explained, 272,860 values equal). every code end becomes `.` (1,935 codes lose `.e` or `.a`; no two codes become equal).
- ◐ (2026-10-22) **R2 - power model:** variables done (`gen` -> `gen_mwy`, `usd` -> `nid`, `reteff` -> `rec`, `ccp` -> `xac`; cells explained, values equal). The totals move to R7: renaming `captot` to `cap` with slots `pow.tot` makes a second dictionary key `cap` (its label and unit lookups would read the per-type row); R7 needs a total-row mechanism (dictionary key kept, code variable renamed).
  - `gen` -> `gen_mwy`, `usd` -> `nid`, `reteff` -> `rec`, `ccp` -> `xac`;
  - totals `captot`, `gtot`, `nimtot`, `usdtot` -> `<legacy var>.pow.tot`;
  - `pe` and `dem` keep their prototype names (without model letters, `ener` would make them equal to the elasticity rows).
- ◐ (2026-10-22) **R3 - prices and policies:** the seven with evidence done (`psp` -> `ps`, `pets` -> `etsnew`, `rpb` -> `pbc`, `txfx` -> `fadtx`, `txfl` -> `cs`, `incf` -> `inc.ela.adj`, `cpi` -> `tcp`; values equal). Open: the other price rows of the Crosswalk after their review.
  - `psp` -> `ps`, `pets` -> `etsnew`, `rpb` -> `pbc`, `txfx` -> `fadtx`, `txfl` -> `cs`, `incf` -> `inc.ela.adj`, `cpi` -> `tcp`;
  - `shp`, `pros` keep the sector-first order (legacy's fuel-first codes are aliases).
- ☑ (2026-10-22) **R4 - transport (road engineer model):** done (22 `codevar` rows, 18 row-slot rows, members `pas` -> `pass`, `cyc` -> `motor`; cells explained, 272,860 values equal, the 6,716 codes the workbook computes equal the map's). Mechanism added: Mitigation columns B and C stay internal (they key MTRowKey, CovKey, ConstKey, the Inputs lookups and the LAMBDAs' SecFuel/SecSub); the code reads the code variable (Variables column L, `VarCode`), the pair's code slots (Mapping column G, `MemSlot`) and, for single rows, a row code (Mapping columns I-J, `RowKey`/`RowCode`; a map row `V|C|B` replaces the whole code body). Descriptions (column H) keep the internal members.
  - `trevst`… -> `stockcalc`, `trevcc`… -> `shrcalc`, `trevsh`… -> `shract`;
  - `trkm*` -> `pass`/`fre`/`motor`/`all.vkt`, `trvht*` -> `*.own`, `traf*` -> `fecon`, `trkt` -> `tot.rod`;
  - members `pas` -> `pass`, `cyc` -> `motor`.
- ◐ (2026-10-22) **R5 - emissions:** done for the evidenced rows: `ap.<sec>.<pol>` -> `em.<sec>.all.<pol>`, `ap.all.<pol>` -> `em.all.<pol>`, `aps` -> `em`, combustion `ch4.<sec>.<fuel>` -> `em.<sec>.<fuel>.ch4`, `apf.all.<pol>` -> `<pol>.tot` (incl. `nox`), `ghg.all.<gas>` -> `<gas>.tot`; cells explained, 272,860 values equal, codes computed equal the map's. Open: `aps.all.<pol>` keeps its code (it would equal `ap.all.<pol>` -> R7 duplicates); `ch4.em.all.<src>` -> `em.<src>.<sector>.ch4` (legacy sector per source, only `og` -> `ext` evidenced); `co2.sec.*` (subsector-to-group map under review); `apf.all.all` -> `gwp100.tot` (review).
  - `ap`/`aps` -> `em`;
  - `apf.all.<pol>` -> `<pol>.tot`;
  - `ghg.all.n2o` -> `n2o.tot`, `apf.all.nox` -> `nox.tot` (legacy `nox.tot` holds N2O and `oc.tot.` holds NOx: aliases, and a legacy bug);
  - `ghg.all.<gas>` -> `<gas>.tot`;
  - `co2.sec.*` -> `co2` in the protocol structure.
- ◐ (2026-10-22) **R6 - fiscal and welfare:** done for the evidenced rows: `rfu.all.<fuel>` -> `rev.usd.tot.<fuel>`, `rtot.all.all` -> `rev.usd.tot`, `rsr.all.all` -> `rev.sr.usd`, `wel.all.cli/usd/pct/eff` -> `wel.cli.pct`/`wel.tot`/`wel.pct.tot`/`wel.eco.dwl.pct`, `gdpg.all.all` -> `gdp.pct.tot`; values equal. Open (crosswalk review): `rnew`, `rsub`, `rmf`, `rtx`, `rnet`, `rvt`, `rbe`, `gdp.*`, `gdpg.<use>`, `scc`, `rsr.<sec>.<fuel>`, `rfu.pow.ecy`.
  - `rtot`, `rnet`, `rfu`, `rsub`, `rmf`, `rpct` -> `rev.*`;
  - `gdp.*`, `wel.*`, `scc.*` sub-codes as legacy.
- ☑ (2026-10-22) **R7 - totals and duplicates:** done: 150 total rows (an explicit SUM/SUMIF/SUMIFS in the year formula) write `tot` for `all` (e.g. `ener.rod.tot`, `ener.tot.coa`, `co2.pow.tot`); power totals `captot`/`gtot`/`nimtot`/`usdtot` -> `cap`/`gen_mwy`/`nim`/`nid` `.pow.tot` (code variable); the 18 rows repeating an earlier row's variable, sector and fuel (section 11 copies, `ener.oen.all` of section 8, `eldem.oen.ecy`) carry no code: 0 duplicates, values equal, LiveOutputs stems found. Open: totals written another way (not an explicit sum), found per variable in the crosswalk review.
  - `all` -> `tot` on total rows (about 150 explicit sums, plus totals written another way);
  - the section 11 copies drop their own code (17 duplicate codes);
  - the LAMBDA text matches (`FUELSPEND`, `FUELQTY`, `BLOCKQTY`) unaffected.
- ◐ (2026-10-22) **R8 - output sheets:** done: LiveOutputs, StoredOutputs and ScenarioCompare carry the protocol stems (`rn_stem`); LiveOutputs column AB "Code stem v0.7.1 (alias)" holds the v0.7.1 stem of the 47 renamed stems; macro `UpgradeStoredCodes` (run first by every store and by CheckBatch, public too) renames v0.7.1 stems in StoredOutputs and their output codes (tested in LibreOffice: 235 v0.7.1 rows of 615 renamed, all 615 then protocol stems). Open: the legacy MTOutputs code as a second alias (C11b), once the crosswalk names a legacy code for each indicator.
  - LiveOutputs, StoredOutputs and ScenarioCompare carry the protocol codes, with the legacy MTOutputs code in an alias column;
  - the macro accepts the old prototype codes for one release.
- ◐ (2026-10-22) **R9 - outside the workbook:** done: `check_full` (expected codes, stored stems and the regression through the map: `RS`, `RC`), `legacy_compare` (prototype values found by the v0.7.1 code), register (issue I75; legacy bugs L131 reused codes, L132 capitals and empty tokens, L133 `nox.tot`/`oc.tot.`), protocol checks C1, C5, C7, C10 in `check_quick` (PASS on the quick build). The code formula reads `VCode` and the pair slots `MSlot`, or (512 rows the map codes on its own) `RowKey`/`RowCode` on Mapping I-J: at most 96 characters; full recalculation 31.8 s (v0.7.1 30.5 s; a 6,700-row code table took 51 s). `ap.all.<pol>` -> `em.tot.<pol>` (C5: a total, the crosswalk had `all`). Open: C6 (closed vocabularies per slot: the prototype members `vkt`, `own`, `pit`... are not in the sheets yet); `coded` `ele` -> `ecy` (changes the shared data CSVs too: 214 rows in energy_consumption alone; with the Coded CPAT owner); then once: full build, full check, paste test, Word documents, deck.
  - `check_v7`, `legacy_compare`, `check_links`, the Python references;
  - `coded` `ele` -> `ecy` and the shared codes;
  - register: legacy code inconsistencies (issue); duplicated codes, capitals, empty tokens, `nox.tot` / `oc.tot.` (legacy bugs);
  - protocol checks (C1, C5, C6, C7, C10) in `check_quick`;
  - then once: full check, paste test, Word documents, deck.

## Not in this increment

- The NOx forcing value differs from legacy (prototype `apf.all.nox` -6.3 against legacy -5.5 Mt CO2e, Egypt 2022): a value question, not a code one; register it separately if it is not already explained.
