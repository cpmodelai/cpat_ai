# v9.0 PIGAP: Pigouvian tax without stored scenario-1 values, module tabs, marginal air-pollution damages

Group PIGAP (user decisions 2026-10-29, points 1-3). Builder: `excel_ai/mitigation/build.py` (quick build and quick
check PASS). Egypt values: the prototype's quick build (scenario 1 = baseline, group 2 = the live policy scenario);
legacy = l465 cached Egypt run.

## What changed in build.py

1. **Pigouvian tax, live and acyclic (point 1).** `R3_STORE`, `PIG_STORE`, the three BaselineCO2 rows (`apcr`,
   `trgso`, `trdie`), their `fast_batch`/`write_bco2` code and the 17b rows `pig.trs.*` are removed. New section-1 rows
   (sub-heading "Pigouvian tax: road transport externalities per litre ..."), inputs only:
   - `pig.trk` (Transport1 row of country|BaseYr); `pig.fe0.pas.gso`, `pig.fe0.pas.die` (passenger and light fuel
     economy, ownership-weighted, as legacy trfem); `pig.wsh.rod.gso` = 1 - cycle share, `pig.wsh.rod.die` =
     1 - freight / (1 - bus) (Transport1 fuel shares by vehicle type); `pig.fe0.all.gso|die` = w x FE pas + (1 - w) x
     FE cycle|freight; `pig.mu0.rod.*` (R1.8 with w, road elasticities from Inputs); `pig.rsh0.rod.*` (base-year road
     use / use of all subsectors, Inputs f0); `pig.kpl.rod.*` = fe0 x mu0 x rsh0.
   - (b) growth rows `pig.trg.acc|con|rdm` = cost per km of the year / of BaseYr (FromTransportCB; rdm is 1).
   - (a) base values `pig.trb.acc|con.rod.gso|die` = a|k(BaseYr) x kpl; `pig.trb.rdm.rod.die` = r x kpl x (1 - w).
   - (c) `pig.tr` = sum of base value x growth. The quick check's lvc rule holds (precedents of `ccp` reach no row of
     section 5 on). Every scenario group has the same formula (copy-paste).
2. **Module tabs (point 2).** Sheet Inputs_cob is retired. New stand-alone tabs `FromAirPollution` and
   `FromTransportCB` (after Inputs in the INPUTS group; not merged; `TAB_ORDER`, the order list, `TAB_INFO`), keyed by
   country, Egypt only, bright yellow, note at the top. FromAirPollution: value of averted PM2.5 (T3, `ApKey/ApVal/
   ApYear`), concentration coefficients (T2, `ApKapKey/ApKap`), the coefficients per t of the pollutants of the
   emission factors derived from T2 (`ApEfKey/ApEf`: other PM2.5 = PM2.5 - BC - PomPerOC x OC, columns as the Inputs EF
   columns ap0_/ap1_), memo: legacy average unit costs T1 (not read). FromTransportCB: per-km costs T4
   (`TcbKey/TcbVal/TcbYear`). The Mitigation lookups give 0 for a country without rows (`air.con.pm2` reads the
   country's first and last pollutant rows in E:F, 0 if none).
3. **Marginal air-pollution damages (point 3, legacy bug, was issue I104).** New section-1 rows `airpol.mc.<sub>.<fuel>`
   (97 rows: the subsectors of the 12 unit-cost lines, power by plant type): `pig.vpm x (D x (1 - pig.efw) + E x
   pig.efw) x Billion / PJperKtoe / Million`, D|E = sum_p kappa'[m(s), p] x EF[f, s, p] with the base-year|EFEndYear
   factors (Inputs or Inputs_power), `pig.efw` = the section-15 EF path weight, `pig.vpm` = v_PM of the year (2022
   takes 2023, see deviations). Lines: `pig.ap` (section 1) = average weighted by base-year fuel use (F) x GJ per price
   unit (residential coal x [base-year coal > ApCoalResMin x base-year buildings use]); `airpol.cost` (17b) = average
   weighted by the scenario's own subsector use (new 17b rows `fus.<sub>.<fuel>`, ktoe) x GJ per price unit. Section 18
   (social costs, FFS, subsidies, efficient prices) reads 17b as before. `wel.air` unchanged.
4. Collateral: `pav.leg` (coal, gas) sums its three consecutive quantity rows with SUM (the section-1 rows pushed it
   past 100 characters). Variables: new codes `airpol.mc`, `fus`, `pig.efw`, `pig.vpm`, `pig.trk`, `pig.fe0`,
   `pig.wsh`, `pig.mu0`, `pig.rsh0`, `pig.kpl`, `pig.trg.*`, `pig.trb.*`; `pig.trs` gone; texts of `pig.ap`, `pig.tr`,
   `airpol.cost`, `air.vpm`, `tran.*.km`, `air.con.pm2` updated. No new constant, no new MTInputs input (MT_LAST
   unchanged). check_full.py: no change needed (it covers `wel.usd` only, from sheet rows; the 17b/18 and Pigouvian
   rows are not recomputed there, as before).

## Register

- **New issue I151** (replicated proxy; Major): "The Pigouvian road-transport component is a proxy of legacy's
  scenario-1 values (Transport I322-I344 `mf.1`): base-year value x growth of the per-km costs. It holds fuel economy,
  passenger/freight shares, driving share and road share at the base year (from Transport1 data and base-year fuel use)
  where legacy's `mf.1` follows scenario 1's engineer road model; the passenger/freight split comes from the Transport1
  fuel shares, not from the engineer model's bottom-up class use (diesel passenger weight 0.589 against 0.414), and the
  road share counts subsector use only (no power use)." Egypt, against legacy 465 cached `mf.1` (Mitigation rows
  128-133 = Transport 322-344):

  | USD/l | 2022 proxy | 2022 legacy | 2030 proxy | 2030 legacy | diff | 2040 proxy | 2040 legacy | diff |
  |---|---|---|---|---|---|---|---|---|
  | gasoline acc + con (`pig.tr.all.gso`) | 0.07620 | 0.07834 | 0.09305 | 0.09790 | -5.0% | 0.15649 | 0.17225 | -9.2% |
  | of which accidents | 0.04123 | 0.04239 | 0.03849 | 0.04050 | -5.0% | 0.04988 | 0.05490 | -9.2% |
  | of which congestion | 0.03497 | 0.03595 | 0.05456 | 0.05741 | -5.0% | 0.10661 | 0.11735 | -9.2% |
  | diesel acc + con + rdm (`pig.tr.all.die`) | 0.16786 | 0.17282 | 0.17497 | 0.16403 | +6.7% | 0.20175 | 0.19426 | +3.9% |
  | of which accidents | 0.01740 | 0.01317 | 0.01625 | 0.01106 | +47% | 0.02105 | 0.01510 | +39% |
  | of which congestion | 0.01476 | 0.01117 | 0.02303 | 0.01567 | +47% | 0.04500 | 0.03228 | +39% |
  | of which road damage | 0.13570 | 0.14847 | 0.13570 | 0.13730 | -1.2% | 0.13570 | 0.14687 | -7.6% |

  Against the prototype's own scenario-1 17b values (the stored rows of the full build before this change): gasoline
  2030 0.0931 vs 0.0988 (-5.9%), 2040 0.1565 vs 0.1735 (-9.8%); diesel 2030 0.1750 vs 0.1656 (+5.7%), 2040 0.2017 vs
  0.1974 (+2.2%). Gasoline: fuel economy 13.03 km/l held (legacy 13.39 in 2022, rising to 14.4 in 2040). Diesel: fuel
  economy 8.36 km/l with the data shares (engineer model 6.42) offsets the freight share 0.411 (0.586) in road damage.
- **Bug (was issue I104; the integrator registers it)**: legacy uses the air-pollution unit costs per fuel (AP 3731-4378:
  attributed deaths per ktoe x VSL, average damages; residential LPG and kerosene include household air pollution) where
  marginal damages are meant (Pigouvian taxes rows 113-123, efficient prices 17964-18102, implicit subsidies and FFS
  17738-17951); legacy's own welfare uses the concentration model (5.7x lower in 2030). Fix: unit cost by fuel and
  subsector = v_PM(t) x sum_p kappa[m(s), p] x EF[f, s, p](t) x 1e9 / 41,868 GJ per ktoe (x GJ per litre for gasoline,
  diesel, LPG, kerosene), m(s) the module sector of section 15 (rod; res, srv, cst -> gro; foo; others oth; power
  cpp, gpp, opp), kappa per t of the EF pollutants (other PM2.5 = PM2.5 - BC - 1.3 OC); lines = fuel-use-weighted
  averages (scenario's own use in 17b; base-year use in the Pigouvian tax). I104 closes as a fixed bug; the legacy
  values stay as a memo on FromAirPollution. Egypt, scenario 1 (USD/GJ; gasoline, diesel, LPG, kerosene USD/l):

  | Line | 2022 legacy avg | 2022 marginal | 2030 legacy avg | 2030 marginal | ratio 2030 |
  |---|---|---|---|---|---|
  | coal industry | 2.376 | 1.647 | 2.337 | 1.596 | 0.68 |
  | coal residential (switch: 0 in Egypt) | 45.75 | 31.71 | 46.82 | 31.97 | 0.68 |
  | coal power | 0.748 | 0.519 | 0.745 | 0.509 | 0.68 |
  | gas industry | 0.2940 | 0.2020 | 0.3008 | 0.2037 | 0.68 |
  | gas residential | 0.0371 | 0.0254 | 0.0380 | 0.0256 | 0.67 |
  | gas power | 0.5599 | 0.3842 | 0.5635 | 0.3809 | 0.68 |
  | gasoline | 0.0608 | 0.0422 | 0.0571 | 0.0390 | 0.68 |
  | diesel | 0.2177 | 0.1639 | 0.2223 | 0.1677 | 0.75 |
  | LPG | 0.6750 | 0.0026 | 0.6887 | 0.0028 | 0.004 |
  | kerosene | 0.9370 | 0.0659 | 0.9360 | 0.0631 | 0.07 |
  | other oil, power | 5.856 | 4.059 | 5.690 | 3.886 | 0.68 |
  | other oil, industry | 23.43 | 16.24 | 22.89 | 15.62 | 0.68 |

  Effects, Egypt scenario 1 (2022 / 2030): Pigouvian tax before the switch `pigx` (2022 is 0: phase-in from CPIntro):
  gasoline 0.187 -> 0.247 $/l in 2030 (phase-in 0.8 x (transport now in: +0.093; air pollution -0.018)), diesel 0.339 -> 0.433, LPG
  0.657 -> 0.108, kerosene 0.903 -> 0.206, other oil 54.8 -> 46.0 $/bbl, coal industry 7.64 -> 7.05, coal power 6.37
  -> 6.18, gas power 3.80 -> 3.65, gas industry 3.59 -> 3.51 $/GJ (no tax change in the default scenarios:
  AddEfficientTaxes is off, so `ntxb`, `ntx`, `ccp` and every quantity are unchanged). Efficient prices `eff.price`:
  gasoline 1.403 -> 1.382 / 1.081 -> 1.060 $/l, diesel 1.841 -> 1.780 / 1.386 -> 1.324, LPG 1.645 -> 0.878 / 1.446 ->
  0.664, kerosene 2.122 -> 1.129 / 1.926 -> 0.931, coal industry 18.77 -> 18.04 / 16.72 -> 15.98, coal power 19.32 ->
  19.09 / 13.32 -> 13.08, gas power 15.11 -> 14.93 / 13.45 -> 13.27 $/GJ, electricity residential 0.0802 -> 0.0763 /
  0.1295 -> 0.1249 $/kWh. Implicit subsidies `impsub.con.tot`: 35.67 -> 25.67 / 60.27 -> 44.36 bn (6.5% -> 4.7% /
  7.8% -> 5.7% of GDP), mostly LPG 8.51 -> 1.81 / 13.89 -> 3.01, kerosene 0.86 -> 0.19 / 1.31 -> 0.32, diesel 9.32 ->
  8.39 / 14.75 -> 13.39, other oil 5.21 -> 4.01 / 9.82 -> 7.81. Explicit subsidies unchanged. Live scenario (group 2):
  FFS welfare `wel.ffs` 2030 13.44 -> 10.63 bn; `wel.usd`, `wel.air` unchanged.
- Issues to update: I106 (typed module values now on FromAirPollution / FromTransportCB, other countries 0), I105
  unchanged, I118 (transport Pigouvian part: now the I151 proxy), I111 (scenario-1 weights: no longer used by the
  Pigouvian tax).

## Deviations and caveats

- v_PM(2022) is 0 on FromAirPollution (legacy: no change in PM2.5 in 2022, so no value); the marginal costs take the
  2023 value in 2022 (`pig.vpm`). wel.air is unaffected (its change in PM2.5 in 2022 is 0).
- The opm term is linear per fuel (marginal of the aggregate MAX(0, PM2.5 - BC - POM) where it is positive).
- Base-year road share counts subsector use only (power use of gasoline or diesel left out; exact for Egypt).
- The proxy takes Transport1 at BaseYr (no data year -> 0, so the transport part is 0 for that country).

## LegacyDiff (integrator)

- LegacyDiff row "Welfare: co-benefits" (v9.0 R1-R3, rows 81-85): "typed Egypt inputs on Inputs_cob" -> "on the module
  tabs FromAirPollution and FromTransportCB".
- New row "Air-pollution unit costs": legacy average damages (deaths per ktoe x VSL) / this model marginal damages
  (value per ug/m3 x concentration coefficients x emission factors), lines weighted by fuel use / reason: bug (was
  I104) / effect: Egypt Pigouvian, efficient prices, implicit subsidies (implicit subsidies 2030 60.3 -> 44.4 bn) /
  Bug fix.
- LegacyDiff for the Pigouvian transport component (existing R3 row): "scenario 1 stored on BaselineCO2" -> "base-year
  value x growth of the per-km costs (I151)".

## Version log sentence

v9.0 (PIGAP): Pigouvian tax components live and acyclic (road transport: base-year value from base-year data x growth
of the per-km costs, issue I151; no stored scenario-1 rows on BaselineCO2); air-pollution unit costs as marginal
damages (value of averted PM2.5 x concentration coefficients x emission factors; legacy average damages, was I104);
module tabs FromAirPollution and FromTransportCB (Inputs_cob retired).

## Caveats (for CAVEATS.md)

The marginal costs of residential LPG and kerosene are about 1% and 7% of legacy's (legacy's average damages include
household air pollution, which the concentration model does not have); food & forestry fuels carry the large `foo`
coefficients. Quick check only (no full build, as instructed): the full build's BaselineCO2 no longer has the three R3
rows (rows after the CH4 store rows end earlier).
