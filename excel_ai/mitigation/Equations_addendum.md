# Equations addendum: remaining functionality R1-R13 and the reverts to legacy (v9.0)

Addendum to [`Equations.md`](Equations.md) (same notation, section 0). It defines, before the build, every new
variable of the remaining functionality agreed on 2026-10-29 (plan:
[`../plans/Remaining_functionality.md`](../plans/Remaining_functionality.md) sections 7-8, machine-readable
[`../plans/remaining_functionality.json`](../plans/remaining_functionality.json)). The Excel prototype (`build.py`)
and the Python port (`coded/`) both implement from it; `Equations.md` and the Methods volume take it in at the next
release.

The rule (NORMS 0): never replicate a legacy bug, always replicate a legacy issue. Each entry says where it follows
legacy 465 and which legacy bugs it fixes (L) or issues it replicates (I). Legacy rows are those of legacy 465
(`CPAT 1.0pre_465_NoPropData.xlsb`), sheet Mitigation unless stated. Columns K..AE are the years 2022..2041.

Not here, by decision: the elasticity-based power model; the outputs (MTOutputs).

Contents:

- A. Reverts to legacy: LD1, LD10 (bug L171), I47, and R13 (LD16 with bug L172, LD41, LD58)
- B. R1 Inputs from air pollution and transport co-benefits; R2 social costs and benefits, full welfare
- C. R3 Pigouvian taxes; R4 CBAM process emissions
- D. R5 green public investment; R11 current account; R12 GVA and emissions intensity
- E. R6-R10: residential initially-exempt split, producer-subsidy price effect, Manual inputs, the electricity
  consumer-subsidy option and power memo tables, road biofuels, aviation and navigation renewables, range anxiety
- F. Output blocks to the modules (no copies)


## A. Reverts to legacy and R13

Notation as `Equations.md`. Legacy = CPAT 1.0pre_465 (Mitigation sheet unless stated; policy block = baseline row + 6316).
Bugs proposed here: L171, L172 (numbers set by the user), L173 to L175; one unregistered prototype departure (LD80, production-cost weight); cell plans in `Equations_addendum_notes.md` section A.

### LD1. Food & forestry: industry elasticities, industry prices, industrial additional efficiency

**Legacy**: rows 5596-5618 (food & forestry block; policy 11912-11934). Prices 5598-5606: coal and gas read the
industry price rows (2513/2514 `pbc/nce.ind.coa`, 2582/2583 `pbc/nce.ind.nga`) x coverage `tcf.foo` (row 2276); fuel
use 5609-5617 reads `_el_inc_*_ind`, `_el_dem_*_ind`, `_el_eff_*_ind`, `_eff_imp_*_ind` and `$M2201` (industrial
additional efficiency, MTInputs 245). Services (5623-5642) use `_srv` elasticities: only food is "industry".
**Inputs**: Elasticities table (sector `ind`), MTInputs `AdditionalEfficiencyIndustrial` (already read, group 3).
Prototype codes: `enel`, `ener`, `aef`, Inputs columns `esec`, `eY`, `eU`, `eF`, `a`, `aeg`, `psec`.

```
LD1.1  ε^Y[f,foo], ε^U[f,foo], ε^F[f,foo], α[f,foo] = ε^Y[f,ind], ε^U[f,ind], ε^F[f,ind], α[f,ind]      (as legacy)
LD1.2  P[f,foo](t) = P^pbc_c(f,ind)(t) + nce_c(f,ind)(t) · tcf_foo(t)    for f ∈ {coal, gas};  all-sector c otherwise   (as legacy; unchanged)
LD1.3  α⁺_G(foo) = α⁺_ind  (AdditionalEfficiencyIndustrial, legacy $M2201)                              (as legacy; unchanged)
LD1.4  Q[f,foo](t): equation E-fuel-use (CPAT 3.3.3) with LD1.1-LD1.3                                    (as legacy)
```

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| `ener.foo.*` (changed, not new) | food & forestry fuel use with industry elasticities | ktoe | LD1.4 | 5609-5618 (11925-11934) |

Prototype change: `SUBSECTORS` row `foo`, elasticity sector `'srv'` -> `'ind'` (build.py line 174). Price sector (`ind`)
and additional-efficiency group (`AEG` default 3) already match legacy; nothing else changes.

### LD10. Fuel price reform after the target year (ExtendCarbonPriceBeyondOutro); feebates held

**Legacy**: rows 163-180 (shared by both blocks): E163/E164 start/target year (MTInputs 140/141), G start price
(MTInputs 142-155), H target price (156-169), J linear slope, K percentage rate, L:AE path. Feebates rows 2000-2004
(I1977/J1977 start/target year MTInputs 53/54; I, J start/target rate MTInputs 56-64). Option list of
`ExtendCarbonPriceBeyondOutro` (MTInputs F265, Dashboard L20 data validation, Mitigation C67): **No, Linear\*, Percentage**.
**Inputs**: ScenarioDefinition `fpr.yr0`, `fpr.yr1` (MTInputs 140/141), `fpr.s`, `fpr.f` (142-169),
`ExtendCarbonPriceBeyondOutro` (265; already in `CP_PARAMS`), `fb.yr0`, `fb.yr1`, `fb.s`, `fb.t`.

```
LD10.1 slope:          j_c = (F1_c − F0_c)/(T1^F − T0^F)  if T1^F > T0^F,  else 0                         (as legacy J)
LD10.2 growth rate:    k_c = (F1_c/F0_c)^(1/(T1^F−T0^F)) − 1                      if T1^F > T0^F, max(F0,F1) > 0, F0_c > 0
                           = (F1_c/(F0_c + j_c))^(1/(T1^F−T0^F)) − 1              if T1^F > T0^F, max(F0,F1) > 0, F0_c ≤ 0
                           = 0                                                     otherwise                (as legacy K)
LD10.3 path:           F_c(t) = 0                                       if t < T0^F
                              = F0_c + j_c (t − T0^F)                   if t < T1^F or ext = "Linear*"
                              = (1 + k_c) F_c(t−1)                      if ext = "Percentage"      (bug L173 fixed)
                              = F0_c + j_c (T1^F − T0^F)                otherwise ("No": hold)     (bug L171 fixed)
LD10.4 feebate rate:   b_G(t) = Λ̄(t; T0^b,T1^b,b0_G,b1_G)                    (held at b1_G after T1^b, as legacy; L174 fixed: max(T1−T0,1))
```

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| `fpr.j` | fuel price reform: linear increase per year | price unit/yr | LD10.1 | J167:J180 |
| `fpr.k` | fuel price reform: percentage increase per year | share | LD10.2 | K167:K180 |
| `fpr` (redefined) | fuel price reform path | price unit | LD10.3 | L167:AE180 |
| `fb` (redefined) | feebate rate path, held after the target year | $/tCO2 | LD10.4 | L2001:AE2004 |

`fpr.j`, `fpr.k` may stay inside the path formula (a LAMBDA `FPRPATH(year, y0, y1, s, f, ext, prev)`); E2 and E3 of
`Equations.md` change to LD10.3 and LD10.4. Carbon price (E1) unchanged.

### I47. Methane fee in the fiscal space on the scenario's own activity

**Legacy**: methane fee revenue rows 6143, 6146, 6149, 6152 (energy: upstream oil/gas, coal, downstream gas, biomass),
6155 (energy total), 6210 (agriculture), 6213 (waste); activity 6136 (= gas consumption row 6476) and 6137 (= biomass
use row 6482), same year column; 7893-7896 `mf.new.usd`; 8010 into 8012 `rev.new.usd`; fiscal space 8018-8025 (INDEX
on the same year column, scenario 1 vs own); GDP feedback 8761 (= previous year's effect, K14590). Policy block +6316
(14212, 14328, 14334-14341, 14590-14592, 8761).
**Inputs**: none new. Prototype codes read: `ch4.em.*`, `ch4.act.dg`, `ch4.act.bm`, `ch4.abt.*`, `mfee`, `rnet`, `rnew`, `rsr`, `rpsu`.

```
I47.1  Rmf(t) = Σ_j E_j(t) · GWP_j · 1[fee applies to j] · m(t) / 10⁶     (E_j on own activity Act_j(t): E84; = ch4.rev)   (as legacy)
I47.2  Rfis(t) = Rnet(t) + Rnew(t) + Rsr(t) + Rpsu(t) + Rmf(t)                                                 (as legacy rev.new.usd)
I47.3  fs(t) = (Rfis(t) − Rfis^(1)(t)) / Y0(t)        every reference to year t is to column t only (exact-year); the
                                                       GDP effect of year t enters GDP from t+1 (E95), so no loop
```

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| `fis.rev` (redefined) | total revenue incl. methane fee on own activity | USD m real | I47.2 | 7896, 8012 |

Removed: `ch4.emf.*`, `ch4.revf`, `ch4bs.dg`, `ch4bs.bm`, `ch4bs.chk`, sheet BaselineCO2 rows dg, bm (`CH4S_STORE`, `CH4S_SRC`).

### R13/LD16. Margins (dataset year 2024) and production cost, converted to real (L172)

**Legacy**: O747:O752 margin `mit.mar.<coal|gas>.<pow|res|ind>` read at the typed year **2024**; O755:O758 margin of
gasoline, diesel, LPG, kerosene at `FirstYearCalculations` (2022); O759, O760 (other oil, biomass) typed 0; P747:P752
share produced domestically `mit.coa.prod`/`mit.nga.prod` (clipped to [0,1]) and Q747:Q752 production cost
`mit.coa.prod.cost`/`mit.nga.prod.cost`, both at `FirstYearCalculations`; fixed portion J/K of rows 2453, 2476, 2499,
2522, 2545, 2568 (coal, gas: margin + share × cost), 2591, 2614, 2637, 2660, 2683, 2706 (others: margin); policy
copies +6316 (8769 ...). Retail prices and supply costs of the dataset are converted with the CPI index row 725
(L773 `...*L$725`); the margin and the cost are not (bug L172).
**Inputs**: Prices_dom `mit.mar.*`, `mit.coa.prod`, `mit.nga.prod`, `mit.coa.prod.cost`, `mit.nga.prod.cost`; ι(t) (row IP_CPI of Inputs_prices).

```
R13.1  margin year:        y^m_c = 2024 for c ∈ coal, gas (typed, as legacy);  t₀ otherwise
R13.2  share produced:     dsh_c = min(1, max(0, prod_f(c)(t₀)))   for c ∈ coal, gas;  0 otherwise           (as legacy P747:P752)
R13.3  fixed supply cost:  C̄_c = [ mar_c(y^m_c) · ι(y^m_c) + dsh_c · pcost_f(c)(t₀) · ι(t₀) ] / u_c       (bug L172 fixed)
```

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| `mary` (Inputs_prices column) | data year of the margin | year | R13.1 | O747:O758 |
| `dsh` (Inputs_prices column) | share of the fuel produced domestically | share | R13.2 | P747:P752 |
| `spf` / `fixsp` (redefined) | fixed part of the supply cost | $/GJ real | R13.3 | J/K 2453 ... 2706 |

Prototype today: `fixsp = (mar(t₀) + pccb · pcost) · ι(t₀) / gj` (coded CPAT `prices.py`): margin year t₀ for all,
production cost weighted by the **bucketed pass-through** instead of the share produced domestically (unregistered
departure, see notes), and one CPI factor.

### R13/LD41. Data vintage (note, no equation)

Re-extract from `CPAT 1.0pre_465_NoPropData.xlsb` what `extract_data.py`, `extract_legacy_tables.py` (and the other
`extract_*.py` that still name 456) read: international price forecasts Mitigation rows 633-695 (same rows in 465)
and US CPI/deflator rows 452/455; sheet Balances rows 13+; base-year fuel use (now Kernel v1.6 = 456 rows 583-602)
from 465 rows 583-602 or Balances with legacy's mapping; Prices_dom. Checked (Egypt): price forecasts identical
(1008 cells; only 'NA' text in 2041 for IEA/EIA), US CPI identical, Prices_dom identical except the junk `mit.spot.*`
columns (465 adds a 2025 row); **Balances differ** (161 cells; TFC 61,682 vs 67,089 ktoe, −8.1%; food diesel 875.3 vs
927.0). So prices "Same"; balances and base-year fuel use: re-extract (the data-vintage part of LD41 then closes).

### R13/LD58. GDP effects "Same" (benchmark)

No equation. Benchmark = legacy's cached Egypt policy run (scenario 2, carbon tax 0 to 5 $/t linear 2026-2040,
5.36 in 2041, row 8567): values in `Equations_addendum_notes.md` (rows 14334-14592, 8758-8762). Compare ε_GDP (`gdp.eff`) with legacy
row 14592 `gdp.cha.pct.2` and the fiscal space with 14336; not GDP growth (the prototype fixes L24 in E95).

## B. R1 inputs from air pollution and transport co-benefits; R2 social costs and benefits, full welfare

Rows are those of `l465.xlsb` (legacy 465), labelled by each sheet's year row: **Mitigation rows 112-206 and F10
(17377-18159): K = 2021, L = 2022 … AE = 2041** (year rows 112, 17380, 17713; K16081 = 2021); Transport I..AB =
2022..2041 (row 321); Air pollution (AP) K..AC = 2022..2040 (row 973). The plans (`Air_pollution.md`,
`Transport_cobenefits.md`) and the build.py comments cite F10 rows from about 17600 on **15 rows lower in the sheet
than l465** (plan 17732 `wel.air` = l465 17717; plan 17753 = l465 17738; plan 17788 = l465 17773). Their cached
values are also from another run (a $50 tax; the l465 cache is a smaller tax from 2027).

Extra notation (on top of Equations.md section 0):

| Symbol | Meaning (source) |
|---|---|
| s, ^(1) | scenario group; scenario-1 value of the same year (`.ref`) |
| gj_c | GJ per price unit of price fuel c (Inputs column `gj`; $/l and $/bbl → $/GJ) |
| EF_c | CO2 factor of price fuel c, tCO2/GJ (Inputs `ef`; legacy rows 961-967) |
| SCCn, SCCg | selected national and global SCC (`scc.nat`, `scc.glo`, existing) |
| v̄ | general VAT rate of the year (VAT_WEO; legacy L726) |
| h_c | household share of oil product c (Inputs_prices `osh`, OilProductShares; legacy rows 801-816) |
| Q[f,S] | fuel use of sector group S ∈ {tra, bld, ind, oen} = Σ_{s∈S} Q[f,s] (ktoe, section 11); FU_k power fuel use |
| VKT, VKTf | road vehicle-km, total and freight, engineer model 5b (`trkmt`, `trkmf`), bn km — **every TrModel (I100)** |
| FE_f | 5b average fuel economy of the stock (`trafg` gso; `trafo` die, lpg, nga; `trafe` ecy), km/l or km/kWh |
| Qe[f,c] | 5b fuel use by class c ∈ {pas, fre, cyc} (`trfcp`, `trfcf`, `trfcc`, `trfce*`), bn l or bn kWh |
| εU_f, εF_f | road usage and efficiency elasticities (`_el_dem_*_rod`, `_el_eff_*_rod`; existing section 4 parameters) |
| AP[p,m] | section 15 emissions of pollutant p by air-pollution module sector m (`aps.<p>.<m>`), kt |

### R1. Inputs from air pollution and transport co-benefits (typed Egypt values)

**Legacy**: Mitigation rows 112-133 (`Advanced options`: copies of F10 rows 17738-17761), F10 rows 17717-17761;
AP rows 442-522, 974-981, 1814, 3217, 3731-3733, 3886-3887, 3924, 3961, 3998, 4313-4314, 4351, 4378; Transport rows
148-157, 162-237, 321-364; Mitigation block E rows 15710-15808.
**Inputs**: typed tables T1-T4 (values in `Equations_addendum_notes.md` section B; Egypt, cached legacy run); 5b `trkmt`, `trkmf`, `trafg`,
`trafo`, `trafe`, `trfcp`, `trfcf`, `trfcc`, `trfcep/f/c`; `ener` (road and total use by fuel); electricity road use
and total demand; section 15 `aps.<p>.<m>`; Inputs `gj`; elasticities `eldg`, `eldd`, `elfg`, `elfd` (trp.ela).
New section "17b. Inputs from air pollution and transport co-benefits" just before section 18 (typed rows are
scenario-invariant; computed rows are per group). Sections 15 and 5b are the output blocks to the modules (headings
renamed, no copies).

**Decision (what is typed).** Air pollution: legacy's per-fuel unit costs cannot reproduce legacy `wel.air`: with
legacy quantities Σ cost × Δfuel use = 0.322 bn in 2030 against `wel.air` 0.0569 (5.7×; they are average, not
marginal, damages: issue I104). So two sets are typed: (a) the unit costs `airpol.cost` (as legacy, for social
costs, subsidies, FFS and efficient prices), (b) for the welfare, the effective PM2.5 source-receptor coefficients κ
(µg/m3 per t, constant) and the value of averted modelled ambient PM2.5 v_PM(t) = legacy `wel.air` / legacy ΔPM2.5,
so that `wel.air` follows the prototype's own emissions (section 15) and equals legacy given legacy emissions.
Transport: the per-km costs a(t), k(t), r are typed (they do not depend on VKT or the scenario); the $/l values are
computed per scenario from 5b as legacy (Transport rows 186-237), so `mf.1` = scenario 1 and `mf.2` = scenario 2.

```
R1.1  typed (T1):       ĉ[f,S](t)   air-pollution cost, coa|nga × ind|res|pow, oop × pow|ind ($/GJ); gso, die, lpg, ker ($/l)
                        2022-2040 from the AP sheet, 2041 = 2040 (bugs L189, L190, L191 fixed; issue I112)
R1.2  unit costs:       apc[f,S] = ĉ[f,S] / gj_c(f)  for gso, die, lpg, ker (all sectors);  apc[f,S] = ĉ[f,S] otherwise   ($/GJ)
R1.3  res. coal switch: apc[coa,res] = ĉ[coa,res] · 1[Q[coa,bld] / Σ_f Q[f,bld] > 0.001]                 (bug L192 fixed)
R1.4  typed (T2, T3):   κ[m,p] (µg/m3 per t), m ∈ {cpp,gpp,opp,rod,gro,oth,foo}, p ∈ {so2,nox,pm2,bc,pom,opm,voc}
                        v_PM(t) (USD bn per µg/m3) = AP3217 / (AP981 − AP1814);  v_PM(2022) = 0;  2041 = 2040
R1.5  modelled PM2.5:   C_PM = Σ_m Σ_p κ[m,p] · AP[p,m] · 1000                                     (µg/m3; as AP 974-981)
R1.6  typed (T4):       a(t) accident cost per vehicle-km (Transport 185), k(t) congestion cost per vehicle-km
                        (Transport 220), r = 0.12 road damage per freight vehicle-km (Transport 232, F46)   (USD/km)
R1.7  class weights:    w_f = Qe^(1)[f,pas] / (Qe^(1)[f,pas] + Qe^(1)[f,fre])  (f = die, lpg, nga);
                        w_ecy = (Qe^(1)[ecy,pas] + Qe^(1)[ecy,cyc]) / Σ_c Qe^(1)[ecy,c];   w_gso = 1      (scenario 1, I111)
R1.8  driving share:    μ_f = εU_f / (εU_f + εF_f),  εU_f = w_f εU_gso + (1 − w_f) εU_die,  εF_f likewise;
                        μ_f = 0 when the class use is 0                                           (bug L193 fixed)
R1.9  road share:       ρ_f = Q[f,road] / Q[f] (switched model, scenario's own; ecy: road electricity / total demand)
      freight share:    φ_f = Qe[f,fre] / (Qe[f,pas] + Qe[f,fre])        (5b, scenario's own; ecy: fre / Σ_c)
R1.10 $/l by fuel:      acc_f = a · FE_f · μ_f · ρ_f;   con_f = k · FE_f · μ_f · ρ_f          (f = gso, die, lpg, nga, ecy)
                        rdm_f = r · FE_f · μ_f · φ_f · ρ_f   (f = die, lpg, nga, ecy; gso: 0)    ($/l of all use; ecy $/kWh)
                        (as legacy, average FE of passenger and freight: Transport_cobenefits.md B-d, kept as legacy until the user decides)
R1.11 per GJ:           tacc_f = acc_f / gj_f,  tcon_f = con_f / gj_f,  trdm_f = rdm_f / gj_f      ($/GJ; ecy stays $/kWh)
```

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| `airpol.cost.<f>.<S>` (typed ĉ) | Air-pollution cost per unit, 12 series: coa.ind, coa.res, coa.pow, nga.ind, nga.res, nga.pow, gso, die, lpg, ker, oop.pow, oop.ind | $/GJ, $/l | R1.1 (T1) | 17738-17749 ← AP 3924, 4351, 3731, 3998, 4378 (fixed), 3732, 3886, 3887, 4314, 4313, 3733, 3961 |
| `airpol.cost.gj.<f>.<S>` | Same per GJ (coal res with the switch) | $/GJ | R1.2-R1.3 | 17738-17749, 113-123 |
| `air.conc.coef.<m>.<p>` (κ) | Effective PM2.5 concentration coefficient | µg/m3 per t | R1.4 (T2) | AP F442:F522 × I974:I980 |
| `air.vpm` (v_PM) | Value of averted modelled ambient PM2.5 | USD bn per µg/m3 | R1.4 (T3) | AP 3217, 981, 1814 |
| `air.con.pm2.mod` | Modelled ambient PM2.5 (prototype emissions) | µg/m3 | R1.5 | AP 981 / 1814 (`air.con.pm2.all`) |
| `tran.acc.km`, `tran.con.km`, `tran.rdm.km` | Accident, congestion, road-damage cost per vehicle-km (typed) | USD/km | R1.6 (T4) | Transport 185, 220, 232 |
| `tran.wcl.<f>` | Passenger weight of the margins (scenario 1) | share | R1.7 | 15723-15730 (weights) |
| `tran.mrg.<f>` | Driving share of the response μ_f | share | R1.8 | 15721-15730; Transport 148-157 |
| `tran.rsh.<f>`, `tran.fsh.<f>` | Road share of fuel use; freight share of road use | share | R1.9 | 15768-15786; Transport 120-128, 138-146 |
| `tran.acc.cost.<f>` | Accident cost per unit of fuel (mf.s) | $/l, $/kWh | R1.10 | Transport 186-190, 322-331; Mit 17756-17757, 128-129 |
| `tran.con.cost.<f>` | Congestion cost per unit of fuel | $/l, $/kWh | R1.10 | Transport 221-225, 333-342; Mit 17758-17759, 130-131 |
| `tran.rdm.cost.<f>` | Road-damage cost per unit of fuel | $/l, $/kWh | R1.10 | Transport 234-237, 344-351; Mit 17761, 133 |
| `tran.acc.gj.<f>`, `tran.con.gj.<f>`, `tran.rdm.gj.<f>` | Same per GJ | $/GJ | R1.11 | new |

### R2. Monetized social costs and benefits (F10) and the full welfare

**Legacy**: F10 rows 17666-17727 (SCC, climate costs by fuel, welfare), 17736-17764 (social cost by externality),
17766-17784 (FFS environmental benefits), 17786-17951 (explicit and implicit subsidies), 18090 (air-pollution cost
of electricity, read by R3); Transport 354-364.
**Already in the prototype (section 18)**: `scc.*` (options, `scc.nat`, `scc.glo`), `dmg.nat/glo`, `wcli.nat/glo`
(= legacy 17714-17716), `wdg.*`, `eff.*` (17621-17633 energy), `mfp.*`, `mfc.*` (17613-17619, 17630-17632),
`wel.cli`, `wel.eff`, `wel.pct`, `wel.usd`. Efficient prices and Pigouvian taxes (17955-18123) are R3: R3 reads
`cc.nat.*`, `apc.*`, `tran.*.gj.*`, `apc.ecy` from here.
**Inputs**: `scc.nat`, `scc.glo`, Inputs `ef`, `gj`, `osh`, VAT_WEO; supply cost C_c (`sp`), after-tax price P_c
(`atp`), electricity `sc`, `rp`, `cons`, `dem`; `ener`, `pe` (FU_k), `gen` (G_k); `gdp.usd`; R1 rows.

```
R2.1  climate cost per unit:  ccn_c = SCCn · EF_c,   ccg_c = SCCg · EF_c        ($/GJ; c = coa, nga, oop, gso, die, lpg, ker;
                              lk = (ccn_lpg + ccn_ker)/2 memo)   (per GJ: bug L-R2-1 fixed for oop, which legacy adds per bbl)
R2.2  AP cost of electricity: apc_ecy = Σ_{k∈{coal,gas,oil}} apc[f(k),pow] · θ FU_k / Σ_k M G_k   ($/kWh; bug L-R2-2 fixed)
R2.3  AP cost, other uses:    apc[coa,oth] = Σ_{S∈ind,bld,pow} apc[coa,S] Q[coa,S] / Σ_S Q[coa,S]   (AVERAGE if Σ = 0; L-R2-3 fixed)
                              apc[nga,oth] likewise;
                              apc[odo,oth] = (apc[die]·Q[die,tra] + apc[oop,pow]·FU_oop + apc[oop,ind]·Q[oop,ind]) / (Σ of the 3 uses)
                              apc[oop,avg] = (apc[oop,pow]·FU_oop + apc[oop,ind]·Q[oop,ind]) / (FU_oop + Q[oop,ind])
                              (weights: the scenario's own fuel use)
R2.4  road externalities:     ext_gso = apc_gso + tacc_gso + tcon_gso;  ext_die = apc_die + tacc_die + tcon_die + trdm_die   ($/GJ; no climate)
R2.5  air-pollution welfare:  wel.air = v_PM · (C_PM^(1) − C_PM)                                       (USD bn)
R2.6  transport welfare:      wrod.aci = a · (VKT^(1) − VKT);   wrod.con = k · (VKT^(1) − VKT);   wrod.dmg = r · (VKTf^(1) − VKTf)
R2.7  shares of GDP:          wel.air.pct = wel.air / gdp.usd;   wel.rod.pct = (wrod.aci + wrod.con + wrod.dmg) / gdp.usd
R2.8  national welfare:       wel.usd = wcli.nat + wel.air + wrod.aci + wrod.con + wrod.dmg − eff.all − mfc.all     (redefined)
                              wel.pct = wel.usd / gdp.usd  (existing row, new content)
R2.9  FFS environmental:      ffs_j = −u_j · ΔQ_j · θ / 1000      (USD bn; ΔQ = Q − Q^(1), ktoe), lines j:
        coa.ind: u = ccg_coa + apc[coa,ind], ΔQ[coa,ind]     coa.res: ccg_coa + apc[coa,res], ΔQ[coa,bld]     coa.pow: ccg_coa + apc[coa,pow], ΔFU_coa
        nga.ind, nga.res (bld), nga.pow likewise with ccg_nga                                   (L-R2-4 fixed: legacy crosses rows)
        gso.rd: ccg_gso + ext_gso, ΔQ[gso,tra]               die.rd: ccg_die + ext_die, ΔQ[die,tra]  (L-R2-5 fixed: conversion, road damage)
        lpg: ccg_lpg + apc_lpg, ΔQ[lpg]                     ker: ccg_ker + apc_ker, ΔQ[ker]
        oop.pow: ccg_oop + apc[oop,pow], Δ(FU_oop + FU_die)  oop.ind: ccg_oop + apc[oop,ind], Δ(Q[oop,ind] + Q[die,ind])
        coa.oth: ccg_coa + apc[coa,oth], Δ(Q[coa,tra] + Q[coa,oen])     nga.oth likewise
        gso.oth: ccg_gso + apc_gso, Δ(Q[gso] − Q[gso,tra])
        die.oth: ccg_oop + apc[odo,oth], Δ(Q[die,bld] + Q[die,oen] + Q[oop,tra] + Q[oop,bld] + Q[oop,oen])   (as legacy, I-R2-3)
R2.10 FFS totals:             ffs.all = Σ_j ffs_j;   wel.ffs = ffs.all − eff.all − mfc.all
R2.11 subsidy lines j (scenario's own prices and use; legacy computes scenario 1 only):
        sc_j = C_c (`sp`, $/GJ; ecy: sc_u $/kWh);   rp_j = P_c (`atp`; ecy: p_u)                    (L-R2-6, L-R2-7 fixed)
        ext_j: gso, die: ccg + ext (R2.4);  lpg, ker: ccg_c + apc_c;  oop: ccg_oop + apc[oop,avg];
               nga|coa × ind|res|pow: ccg_c + apc[c,S]  (nga.pow with ccg: L-R2-8 fixed);  ecy: 0 (as legacy, I-R2-4)
        vat_j = (sc_j + ext_j) · v̄ · h_j   for gso, die, lpg, ker (h_lpg: L-R2-9 fixed); oop: h = 0 (L-R2-10);
                (sc_j + ext_j) · v̄ for nga.res, coa.res, ecy.res;  0 for ind and pow lines          (I-R2-5)
        effp_j = sc_j + ext_j + vat_j
        con_j = θ Q_j (PJ; ecy: GWh): gso, die, lpg, ker, oop: Q[f]; c.ind: Q[c,ind]; c.res: Q[c,bld]; c.pow: FU_c;
                c.oth: Q[c,tra] + Q[c,oen];  ecy.ind: dem ind;  ecy.res: dem bld;  ecy.oth: dem tra + oen   (L-R2-11 fixed)
        oth lines (nga, coa: ind, res, pow; ecy: ind, res): sc, ext, vat, rp = con-weighted averages      (L-R2-12 fixed)
        exp_j = max(0, sc_j − rp_j) · con_j / 1000;   imp_j = 1[rp_j ≤ effp_j] · (effp_j − max(rp_j, sc_j)) · con_j / 1000  (USD bn)
R2.12 totals:                 exp.all = Σ_j exp_j;  imp.all = Σ_j imp_j;  exp.pct = exp.all / gdp.usd;  imp.pct = imp.all / gdp.usd  (L-R2-13 fixed)
```

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| `cc.nat.<c>` | Climate cost per unit, national SCC | $/GJ | R2.1 | 17678-17685 (136-142) |
| `cc.code.<c>` | Climate cost per unit, global SCC | $/GJ | R2.1 | 17702-17709 |
| `airpol.cost.ecy` | Air-pollution cost of electricity | $/kWh | R2.2 | 18090, 18102 (124-125) |
| `airpol.cost.<f>.other`, `airpol.cost.oop.avg` | Air-pollution cost, other uses; oil average | $/GJ | R2.3 | 17750-17753 |
| `tot.ext.<f>` (gso, die) | Total externalities of road fuels excl. climate | $/GJ | R2.4 | 17763-17764 |
| `wel.air.usd` | Averted air-pollution mortality and morbidity | USD bn | R2.5 | 17717 ← AP 3217 |
| `wel.rod.aci.usd`, `wel.rod.con.usd`, `wel.rod.dmg.usd` | Averted accidents, reduced congestion, reduced road damage | USD bn | R2.6 | 17718-17720 ← Transport 356, 360, 364 |
| `wel.air.pct`, `wel.rod.pct` | Shares of baseline GDP | share | R2.7 | 17724, 17725 |
| `wel.usd` (alias `wel.tot.tot`) | Total national welfare benefits | USD bn | R2.8 | 17722, 17727 |
| `env.ffs.cost.<f>.<S>` (16 lines) | FFS environmental benefits (Harberger) | USD bn | R2.9 | 17767-17782 |
| `env.ffs.cost.all.all`, `wel.ffs.all.all` | Sum; total national welfare (FFS) | USD bn | R2.10 | 17783, 17784 |
| `supcost.<f>.<S>`, `extcost.<f>.<S>`, `vatext.<f>.<S>`, `effprice.<f>.<S>`, `con.<f>.<S>` | Subsidy-block supply cost, externalities, VAT, efficient price, consumption (16 lines) | $/GJ ($/kWh), PJ (GWh) | R2.11 | 17792-17944 |
| `expsub.con.<f>.<S>`, `impsub.con.<f>.<S>` | Explicit and implicit consumer subsidy by line | USD bn | R2.11 | 17798-17946 |
| `expsub.con.all.all`, `impsub.con.all.all`, `expsubgdp.con.all.all`, `impsubgdp.con.all.all` | Totals; % of GDP | USD bn, share | R2.12 | 17948-17951 |

Lines j of R2.11 (legacy rows): gso 17789-17799, die 17801-17811, lpg 17813-17822, ker 17824-17833, oop 17835-17844,
nga.ind 17846-17853, nga.res 17855-17863, nga.pow 17865-17872, nga.oth 17874-17881, coa.ind 17883-17890, coa.res
17892-17900, coa.pow 17902-17909, coa.oth 17911-17918, ecy.ind 17920-17927, ecy.res 17929-17937, ecy.oth 17939-17946.
Not built (display only): chart rows 17729-17734, "info only" triangles 17640-17654, breakdown 18125-18157.

## C. R3 Pigouvian taxes; R4 CBAM process emissions

Years by the year row (Mitigation row 1 / 204: L = 2022 ... AE = 2041; K = 2021). Price units ("pu") are legacy's:
$/GJ (coal, gas), $/l (gasoline, diesel, LPG, kerosene), $/bbl (other oil products), $/kWh (electricity);
u_c = GJ per price unit of price fuel c (prototype `gj`, legacy rows 932-938). Bug and issue numbers: `Equations_addendum_notes.md`.

### R3. Pigouvian (efficient) taxes

**Legacy**: Mitigation 81-82, 111-160 (externalities, phase-in, Pigouvian tax by price fuel), 199-218 (new excise
ntx by price fuel, `mit.ntx.<c>`), policy ntx rows 8782, 8805, 8828, 8851, 8874, 8897, 8920, 8943, 8966, 8989, 9012
(and baseline twins 2466-2696, typed 0), 3602/3631 + 9918/9947 (electricity), 2202-2203 (dead), 17670-17685 (climate
damage per unit), 17738-17750 (air pollution per unit), 17953-18157 (efficient prices, Pigouvian CO2e, year table).
**Inputs** (ScenarioDefinition, all present, none read yet): `AddEfficientTaxes` (row 217, "Yes"/"No*"),
`ClimateEffTax` (216, "Yes*"/"No"), `AddEfficientTaxesPhaseInYears` (212, 5), `ExternalityAddVAT` (218, "Yes*"/"No"),
`YearFuelPrices` (282), `CPIntro`. **From R1** (typed Egypt section): `ap.cost[f,s]` (baseline `.1`; $/GJ coal, gas,
oil-for-power; $/l gasoline, diesel, LPG, kerosene), `tran.acc.cost[f]`, `tran.con.cost[f]`, `tran.rdm.cost[die]` ($/l)
in both `mf.1` and `mf.2`. **Prototype codes read**: `scc.nat`, `scc.glo` (welfare section), `fpr.<c>`, `txo`, `pcsw`,
`ppcw`, `xct`/`xets` rates, `exf`, Inputs_ef `EFSel`, `sp`, `rpn`, `vat` (VAT_WEO), `ener`, power `gen`.

Which externality vintage legacy uses: the **Pigouvian tax** (rows 128-133) reads Transport I322/I324/I333/I335/I344 =
`tran.*.cost.<f>.mf.1` (baseline); the **efficient prices** (17965-17982) read Transport I323/I325/I334/I336/I345 =
`mf.2` (scenario). Air pollution has one vintage (`airpol.cost.*.1`, the Air pollution sheet's baseline blocks) used by
both. Climate uses the national SCC (`scc.nat`, row 17670); the CO2-equivalent rows use the global SCC (17959).

```
R3.1  phase-in:              φ(t) = Λ̄(t; T0^ct − 1, T0^ct − 1 + n_φ, 0, 1)           T0^ct = CPIntro, n_φ = AddEfficientTaxesPhaseInYears
                                   = min(max(t − T0^ct + 1, 0)/max(n_φ,1), 1)           (bugs L195, -3 fixed)
R3.2  generic CO2 factor:    ē_c = u_c · mean_{k∈K(c)} EFSel[f(c)|k]                   (tCO2/pu; base-year selection, not calibrated; as legacy 961-967)
                             K: coa,nga {pow,res,ind}; gso,die {rod,res}; lpg {res,res,ind}; ker {res,ind};
                             oop: IEA 20 tC/TJ·44/12/1000 · GJ/l(oop) · l/bbl
R3.3  climate damage/unit:   cd_c(t) = scc.nat(t) · ē_c                                ($/pu; legacy 136-142 = 17678-17684)
R3.4  air pollution/unit:    ap_c(t) = ap.cost[f(c),s(c)](t)  for coa,nga × pow,res,ind; gso,die,lpg,ker (all)
                             ap_oop(t) = ap.cost[oop,pow](t) · u_oop                    (bug L194 fixed: $/GJ → $/bbl)
                             ap_ecy = 0, ap_bio n.a.                                     (as legacy, issue I119)
R3.5  transport/unit:        tr_gso = acc[gso]^mf1 + con[gso]^mf1;  tr_die = acc[die]^mf1 + con[die]^mf1 + rdm[die]^mf1;  else 0
R3.6  Pigouvian tax:         Pig_c(t) = φ(t) · (ap_c + 1[ClimateEffTax="Yes…"]·cd_c + tr_c)   ($/pu; legacy 148-160, computed in every scenario)
R3.7  gross new excise:      R_c(t) = F_c(t) + 1[AddEfficientTaxes="Yes…"] · Pig_c(t)  ($/pu; legacy 205-215 less the
                                                                                            fossil manual excise, not built)
R3.8  existing taxes before
      new policy (block):    X^pre_c(t) = txo_c + pcsw_c + ppcw_c + ΔXCP_c              ($/GJ; legacy 8821-8825 of the block;
                                                                                            ΔXCP_c with the block's EF and ECP sector, not pxcd)
R3.9  new excise (block):    N^x_c(t) = 1[scen>1] · R_c/u_c                                        if AddEfficientTaxes off
                                      = 1[scen>1] · min(R_c/u_c, max(0, R_c/u_c − X^pre_c))        if on      (as legacy, issue I113)
R3.10 new excise [f,s]:      N^x[f,s] = N^x_c(f,s) · x[f,s]                              (replaces E28; enters N, P, Rnew, rex as E29-E31, E73)
R3.11 power fuels:           ccp uses u_c·N^x_c (c = coa.pow, nga.pow, oop.all) in place of fpr_c
R3.12 electricity:           entx unchanged (Pigouvian term = 0, as legacy row 216 × L159 = 0)
```

Efficient (reference) prices, by price fuel c ∈ {gso, die, lpg, ker; coa.ind, coa.res, coa.pow; nga.ind, nga.res,
nga.pow; ecy.ind, ecy.res} (no oop, bio), per scenario s (legacy: the live scenario only), in $/pu:

```
R3.13 supply cost:           sc_c = sp_c^(1) · u_c                                       (scenario 1; legacy 16194-16206)
R3.14 components:            ap_c (R3.4; ecy: R3.15), acc_c = acc[f]^mf2, con_c = con[f]^mf2 (gso, die), rdm_die = rdm[die]^mf2,
                             cd_c (R3.3; ecy 0)
R3.15 electricity AP:        ap_ecy = Σ_{k∈coa,nga,oop} ap.cost[k,pow] · G_k^(1)/G^(1) · θ_g/1000   (ind = res; as legacy 18090, issue I121)
R3.16 potential VAT:         pv_c = (sc_c + χ·Σ ext_c) · v̄   for c ∈ {gso,die,lpg,ker,coa.res,nga.res,ecy.res};  0 otherwise
                             χ = 0 if ExternalityAddVAT = "No" else 1;  v̄ = VAT_WEO(t₀)   (as legacy, issue I120)
R3.17 efficient price:       EP_c = sc_c + Σ ext_c + pv_c,   Σ ext_c = ap_c + acc_c + con_c + rdm_c + cd_c
R3.18 retail price:          RP_c = rpn_c^(s) · u_c
R3.19 tax gap:               tg_c = RP_c − EP_c
R3.20 Pigouvian (reference): pig_c = Σ ext_c
R3.21 CO2 equivalents:       pig.co2e_c = IFERROR(pig_c · scc.glo / cd_c, 0);   app_c = pig.co2e_c · ap_c / pig_c
                             txo.co2e_c = txo_c^(1) · u_c · scc.glo / cd_c          (n.a. where cd_c = 0; L203)
R3.22 averages:              pig.co2e.all^(s) = Σ_c pig.co2e_c Q_c^(s) / Σ_c Q_c^(s),   app.all^(s) likewise
                             c over 10 fossil: gso,die,lpg,ker (total use); coa,nga × ind, bld, pow (sector use)
R3.23 year table:            X_c(Y), Y = YearFuelPrices, for sc, ap, cd, pv, EP (coal, gas, electricity, ind and res)
```

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| `pig.phi` | Phase-in share of the Pigouvian tax | share | R3.1 | 146 |
| `cc.code.<f>` | Climate damage per unit (national SCC × generic EF) | $/pu | R3.2-R3.3 | 136-142, 17678-17684, 17702-17708 |
| `pig.ap.<c>` | Air pollution cost per unit (from R1) | $/pu | R3.4 | 113-123, 17738-17748 |
| `pig.tr.<f>` | Transport externality per litre, baseline | $/l | R3.5 | 128-133 |
| `pigx.<c>` | Pigouvian tax per unit (before the AddEfficientTaxes switch) | $/pu | R3.6 | 148-160 |
| `ntxg.<c>` | Gross new excise: reform + Pigouvian | $/pu | R3.7 | 205-215 |
| `xpre.<c>` | Existing taxes before new policy, block | $/GJ | R3.8 | 8821-8825 (each block) |
| `ntxb.<c>` | New excise of the block after netting | $/GJ | R3.9 | 8782 ... 9012 |
| `ntx` (existing) | New excise [f,s] | $/GJ | R3.10 | 2512 etc. |
| `sup.cost.<c>` | Supply cost, efficient-price block | $/pu | R3.13 | 17963, 17978, 17993, 18005, 18017, 18029, 18041, 18053, 18065, 18077, 18089, 18101 |
| `airpol.cost.<c>.s` | Air pollution cost in the efficient price | $/pu | R3.14-15 | 17964, 17979, 17994, 18006, 18018, 18030, 18042, 18054, 18066, 18078, 18090, 18102 |
| `acc.cost.<c>` / `con.cost.<c>` / `rdm.cost.<c>` | Accident, congestion, road damage (mf.2) | $/l | R3.14 | 17965-17967, 17980-17982 |
| `scc.cost.<c>` | Climate damage in the efficient price | $/pu | R3.14 | 17968, 17983, 17995, 18007, 18019, 18031, 18043, 18055, 18067, 18079 |
| `vat.cost.<c>` | Potential VAT | $/pu | R3.16 | 17969, 17984, 17996, 18008, 18020 ... 18104 |
| `eff.price.<c>` | Efficient price | $/pu | R3.17 | 17962, 17977, 17992, 18004, 18016, 18028, 18040, 18052, 18064, 18076, 18088, 18100 |
| `rp.<c>` | Retail price, scenario | $/pu | R3.18 | 17970, 17985, ... 18105 (= 16316-16328) |
| `tgap.<c>` | Tax gap | $/pu | R3.19 | 17971, 17986, ... 18106 |
| `pig.<c>` | Pigouvian tax (reference, all externalities) | $/pu | R3.20 | 17974, 17989, 18001, 18013, 18025, 18037, 18049, 18061, 18073, 18085, 18097, 18109 |
| `pig.co2e.<c>` / `app.<c>` | Pigouvian / air-pollution part in $/tCO2 | $/tCO2 | R3.21 | 17975-17976 ... 18110-18111 |
| `txo.co2e.<c>` | Baseline excise in $/tCO2 | $/tCO2 | R3.21 | 17972-17973 ... 18107-18108 |
| `pig.co2e.all.all` / `app.all.all` | Weighted averages, baseline and scenario | $/tCO2 | R3.22 | 18117-18118, 18122-18123 |
| `effp.yr.*` | Breakdown at YearFuelPrices | $/pu | R3.23 | 18127-18157 |

### R4. CBAM process emissions in the carbon tax and ETS

**Legacy**: Mitigation 1832-1836 (CBAMProcess rows of the ETS sector table: switch E, emissions F = O1905:O1909,
semi-elasticity G = 'ETS+LTS' column CBAMProcess = -0.001, proportion J typed 0), 1905-1909 and 1939-1943 (emission
lookups, empty), 1918 (display sum), 2206-2210 (switch copy per block; policy 8522-8526), 5867-6022 (block "CBAM Goods
(WIP, Egypt Only at present)"; policy copy +6,316). Sheet CBAM: a scratch model, not read. **Inputs**: `CBAMProcMch`,
`CBAMProcIrn`, `CBAMProcNfm`, `CBAMProcMac`, `CBAMProcCem` (ScenarioDefinition 117-121; legacy default False; legacy
E = Manual inputs H22:L22 = AND(Dashboard G20 master switch, row 21)); Manual inputs 30-37 (Scope-1 EFs by product:
fc, fp, np, no), 40-47 (semi-elasticity σ_p); typed in Mitigation: production 2024 and growth F5898:G5905 (Egypt only,
`IF(country="EGY", F, 0)`), product prices G5910:G5917. **Prototype**: nothing built (Manual inputs block 18-47 placed,
not read; CBAMProc* rows present, not read; industrial process CO2 of the inventory (I25) is separate and untaxed).

How legacy 465 prices process emissions: **nowhere**. The carbon prices of the block (5869-5871) are typed 0 with the
intended links left as text ('=L2727', '=L2322', '=L2346'), the ETS-table lookup L1905 is text, J1832:J1836 are 0, and
no row of the block (`cpe.*`, `emis.cbam.tot`, `emr.cbam.tot`, `rev.cbam.tot`) is read by revenue, GHG totals, the
ETS cap or MTOutputs. All results are 0 for every switch setting, except the pre-policy product emissions. The
equations below are the block as intended, with bugs L197 to -9 fixed; its link to totals is decision D-R4.

Products p ∈ {DRI-EAF, Scrap-EAF, BF-BOF steel → irn; clinker → cem; ammonia, urea, AN → mch; primary Al → nfm};
s(p) its sector; machinery has no product.

```
R4.1  production:            Pr_p(t) = Pr_p(2024) · (1 + g_p)^(t − 2024)                 (kt; Egypt only, typed)
R4.2  emission factors:      e^f_p = fc_p + fp_p,   e^n_p = max(np_p + no_p, 0)          (tCO2e/t)
R4.3  pre-policy emissions:  E^f_p = Pr_p e^f_p / 1000,   E^n_p = Pr_p e^n_p / 1000      (Mt; legacy label "tCO2e")
R4.4  coverage:              c^ct_s = cov_s (carbon tax coverage of s; legacy E2278 ≠ "No"),  c^ets_s = κ_s (E5),
                             cb_s = 1[CBAMProc<s>]  (live switch, both blocks)
R4.5  prices:                τ(t) carbon tax rate (E1), p^A(t) = p̃_E(t)(1 − ω_s) auctioned ETS price (E15 per tCO2)   (bug -6 fixed)
R4.6  price on fuel CO2:     π^f_p = c^ct_s τ + c^ets_s p^A                              ($/tCO2)
R4.7  price on process:      π^n_p = cb_s · π^f_p
R4.8  product price change:  Δpr_p = (π^f_p e^f_p + π^n_p e^n_p) / P_p                   (share of product price; memo)
R4.9  fuel abatement (memo): ΔE^f_p = E^f_p (exp(−σ_p π^f_p) − 1)                       (bug -7 fixed; not added to totals)
R4.10 process abatement:     ΔE^n_p = E^n_p (exp(−σ_p π^n_p) − 1)
R4.11 post-policy process:   PE_s = Σ_{p∈s} (E^n_p + ΔE^n_p);  PE = Σ_s PE_s            (legacy 6007-6012)
R4.12 revenue:               Rcb = Σ_p (E^n_p + ΔE^n_p) · π^n_p                          (USD m; bug -8 fixed)
R4.13 ETS table:             F_s (row 1832+) = PE_s at the ETS reference year; J_s = 0 (as legacy: no weight in σ̄)
D-R4  (decision, legacy has none): add Rcb to Rnew; add ΣΔE^n_p to the GHG change (not E^n_p: the inventory process
      CO2, I25, already holds the level); add cb_s c^ets_s PE_s to ETS-covered emissions and the cap base.
```

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| `cbam.prod.<p>` | Production of CBAM good p | kt | R4.1 | 5898-5905 |
| `cbam.eff.<p>` / `cbam.efn.<p>` | Fuel and non-fuel EFs | tCO2e/t | R4.2 | 5886-5893, 5952-5959 F:G |
| `cbam.emf.<p>` / `cbam.emn.<p>` | Pre-policy fuel / process emissions | Mt | R4.3 | 5952-5960 / 5963-5971 |
| `cbam.cov.<s>` | Ctax, ETS, process inclusion | 0/1 | R4.4 | 5875-5879 E:I, 2206-2210, 1832-1836 |
| `cbam.pf.<p>` / `cbam.pn.<p>` | Carbon price on fuel / process emissions | $/tCO2 | R4.5-R4.7 | 5869-5871, 5921-5928, 5932-5939 |
| `cbam.dpr.<p>` | Product price increase | share | R4.8 | 5942-5949 |
| `cbam.erf.<p>` | Fuel-emission reduction (memo) | Mt | R4.9 | 5974-5982 |
| `emr.cbam.tot` | Process-emission reduction | Mt | R4.10 | 5985-5993 |
| `cpe.ind.<s>` / `emis.cbam.tot` | Post-policy process emissions | Mt | R4.11 | 6007-6012 |
| `rev.cbam.tot` | Revenue on process emissions | USD m | R4.12 | 6014-6022 |

## D. R5 green public investment; R11 current account; R12 GVA and emissions intensity

### R5. Green public investment

**Legacy**: Mitigation section 10 "Green Public Investment", rows 6215-6267 (scenario 1) and 12531-12583 (scenario 2,
offset +6316); columns K:AD (2021-2040; no 2041 column). Report only: no cell outside the block (Mitigation, MTOutputs,
Dashboard or any other sheet) reads it, so it feeds neither GDP nor emissions.
**Inputs**: MTInputs `EXPCapex` (legacy row 98 -> 2181, 0 before `CPIntro`); data ETS+LTS rows 261-302 (World Bank
CCDR mitigation investment need, column H = D/G, already in the prototype tab ETS+LTS at legacy addresses); constants
typed in Mitigation D6219-D6224 (not MTInputs): T_g = 2026 (green investment start), g = 0.5 (green proportion),
T_nz0 = 2026, T_nz1 = 2060 (net zero start and end years), p = 0.5 (public part). Prototype codes read: `fis.rev`,
`fis.ref`, `fis.sp`, `ghg.ref`.

```
R5.1   need ratio (data):       m = H[c] of ETS+LTS rows 261-302 = Mitigation_c / GDPcum_c        (as legacy; #N/A if c absent)
R5.2   net revenue:             ΔR(t) = (fis.rev(t) − fis.ref(t)) / 1000                             (USD bn; as legacy row 8024)
R5.3   public share:            a(t) = 1[t ≥ CPIntro] · EXPCapex / 100                             (legacy rows 98, 2181)
R5.4   net public investment:   PI(t) = ΔR(t) · a(t)                                               (bug L204 fixed, col K)
R5.5   green share:             GI(t) = g · PI(t)                                                  (as legacy)
R5.6   net revenue, % GDP:      ΔR%(t) = fs(t) = fis.sp(t)                                         (bug L205 fixed)
R5.7   net public inv., % GDP:  PI%(t) = fs(t) · a(t)                                              (bug L206 fixed)
R5.8   green share, % GDP:      GI%(t) = g · PI%(t)                                                (bug L207 fixed)
R5.9   public inv. need, %GDP:  N(t) = 1[t ≥ T_g] · m                                              (bug L208 fixed)
R5.10  cumulative need:         Ncum = m · (2060 − 2025)                                           (as legacy, I124)
R5.11  net zero phase-out:      φ(t) = 1 if t < T_nz0;  φ(t−1) − 1/(T_nz1 − T_nz0) otherwise        (bug L209 fixed)
R5.12  requirement to date:     Req(t) = Ncum · (1 − φ(t))                         (t ≥ T_g)       (bug L210 fixed)
R5.13  public requirement:      PReq(t) = p · Req(t)                               (t ≥ T_g)       (bug L211 fixed)
R5.14  BAU emissions:           E_B(t) = GHG^(1)(t) = ghg.ref(t)                                    (bug L212 fixed)
R5.15  net zero path:           E_NZ(t) = E_B(t) · φ(t)
R5.16  reduction to net zero:   ER(t) = E_NZ(t) − E_B(t)                                           (≤ 0, as legacy)
R5.17  public part:             ERp(t) = p · ER(t)                                                 (bug L211 fixed)
R5.18  cumulative green inv.:   CGI(t) = Σ_{τ ≤ t} GI%(τ)                                         (bug L213 fixed, scen. 2)
R5.19  share of requirement:    π(t) = min(CGI(t) / PReq(t), 1)                    (t ≥ T_g)
R5.20  abatement:               ERg(t) = π(t) · ERp(t)                             (t ≥ T_g)       (Mt CO2e, ≤ 0)
```
Years: rows R5.12, R5.13, R5.19, R5.20 are blank before T_g (legacy columns L:O empty); every row stops at 2040 (I125).

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| gpi.m | Mitigation investment need, share of cumulative GDP (CCDR) | share of GDP | R5.1 | 6218, 6227 H |
| gpi.rev | Net revenue against scenario 1 | USD bn real | R5.2 | 6238 |
| gpi.a | Share of revenue to public capital investment | share | R5.3 | 6232 (2181, 98) |
| gpi.pi | Net public investment | USD bn real | R5.4 | 6239 |
| gpi.gi | Green public investment | USD bn real | R5.5 | 6240 |
| gpi.revp | Net revenue | share of GDP | R5.6 | 6243 |
| gpi.pip | Net public investment | share of GDP | R5.7 | 6244 |
| gpi.gip | Green public investment | share of GDP | R5.8 | 6245 |
| gpi.need | Public investment need (from T_g) | share of GDP | R5.9 | 6249 |
| gpi.ncum | Cumulative investment requirement for net zero (scalar) | share of GDP | R5.10 | 6250 H |
| gpi.phi | Net zero phase-out factor | factor | R5.11 | 6256 |
| gpi.req | Cumulative requirement to date | share of GDP | R5.12 | 6250 P:AD |
| gpi.preq | Cumulative requirement attributable to public investment | share of GDP | R5.13 | 6251 P:AD |
| gpi.ebau | GHG emissions, scenario 1 (BAU) | Mt CO2e | R5.14 | 6255 |
| gpi.enz | GHG emissions on the net zero 2060 path | Mt CO2e | R5.15 | 6257 |
| gpi.er | Emissions reduction to net zero | Mt CO2e | R5.16 | 6260 |
| gpi.erp | Emissions reduction attributable to public investment | Mt CO2e | R5.17 | 6261 |
| gpi.cgi | Cumulative green investment | share of GDP | R5.18 | 6264 |
| gpi.prop | Proportion of the public net zero requirement met | share | R5.19 | 6265 |
| gpi.erg | Emissions reduction from green public investment | Mt CO2e | R5.20 | 6266 |

### R11. Balance of payments: current account

**Legacy**: Mitigation section 11 "Balance of payments", rows 18160-18204 (block F11; legacy bug L50): fuel blocks
18162-18178, current account USD 18180-18188, % of GDP 18190-18195, current prices 18197-18198, energy trade balance
18200-18204 (already built as 16b `xtb`, `xtbp`).
**Inputs**: typed Egypt values (decision R11): WEO `EGY.BCA.A` (current account, USD bn nominal) and `EGY.BCA_NGDPD.A`
(% of GDP), the series legacy reads once bug L50 (stale codes) is fixed; held at the last non-zero data year (2031) by
legacy's own rule. Prototype codes read: `xnim.g.oil`, `xnim.g.nga`, `xnim.g.coa` (change in net imports against
scenario 1, USD bn real, positive = more imports), ι(t) (US CPI index, = 1 in R; legacy row 456).

```
R11.1  current account, typed:  CA0(t) = BCA_EGY(min(t, 2031))                     (USD bn nominal; bug L50 fixed)
R11.2  % of GDP, typed:         ca0(t) = BCA%_EGY(min(t, 2031))                    (% of GDP, percent units)
R11.3  real:                    CAr(t) = CA0(t) · ι(t)                                             (USD bn real)
R11.4  fuel effect:             ΔCA_g(t) = −xnim.g(t),  g ∈ {oil, nga, coa}                       (USD bn real; L49 fixed)
R11.5  after policy:            CA1(t) = CAr(t) + Σ_g ΔCA_g(t)
R11.6  implied GDP / 100:       Ŷ(t) = |CAr(t) / ca0(t)|                                           (as legacy, I129)
R11.7  fuel effect, % GDP:      Δca_g(t) = ΔCA_g(t) / Ŷ(t)
R11.8  after policy, % GDP:     ca1(t) = ca0(t) + Σ_g Δca_g(t)                                     (bug L214 fixed)
R11.9  current prices (memo):   CAn(t) = BCA_EGY(t) for t ≤ 2031;  0 for 2032-2041                 (as legacy, I130)
```
Legacy fuel import bill (R11.4 source; the prototype's `xnim` replaces it, v3.16): ΔNI_oil = ΔQ_oil · bbl/ktoe ·
P_crude($/bbl real)/10⁹ (no share traded: L49); ΔNI_gas = ΔQ_gas · GJ/ktoe · P_gas($/MMBtu real)/10⁹ · s_gas (bug
L215, unit); ΔNI_coal = ΔQ_coal · GJ/ktoe · P_coal($/GJ real)/10⁹ · s_coal; ΔQ = total use of the scenario
− scenario 1 (ktoe; oil = gasoline, diesel, LPG, kerosene, other oil products); ΔCA_g = −ΔNI_g.

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| bca | Current account balance, pre-policy (typed WEO EGY.BCA.A) | USD bn nominal | R11.1 | 18182 |
| bca.gdp | Current account balance, pre-policy (typed WEO EGY.BCA_NGDPD.A) | % of GDP | R11.2 | 18191 |
| bca.r | Current account, pre-policy, real | USD bn real | R11.3 | 18184 (18183 = row 456) |
| bca.d.{oil,nga,coa} | Change in the current account by fuel group | USD bn real | R11.4 | 18185-18187 |
| bca.p | Current account after the policy | USD bn real | R11.5 | 18188 |
| bca.y | Implied GDP / 100 (helper) | USD bn real | R11.6 | in 18192-18194 |
| bca.dp.{oil,nga,coa} | Change in the current account by fuel group | % of GDP | R11.7 | 18192-18194 |
| bca.pp | Current account after the policy | % of GDP | R11.8 | 18195 |
| bca.n | Current account, current prices (memo, typed) | USD bn nominal | R11.9 | 18198 |

Typed values: `Equations_addendum_notes.md` (R11). Legacy output codes: `bca_bp6`, `bca_gdp_bp6` (rows 18182, 18191, 18198).

### R12. Emissions intensity of industrial output (MTOutputs emin)

**Legacy**: Mitigation rows 18631-18666 (CO2 by subsector, power intensity), 18720-18743 (indirect and total),
18745-18758 (intensity table, base year), 18759-18772 (cumulative table); GVA from rows 15632-15705 (GTAP IO OUTPUT
column by CPAT sector, Mapping column R, x US CPI 2014 index G15631, x WEO GDP 2022 / GTAP GDP: J15705); MTOutputs rows
123-143 (codes `mit.emin.<s>`). One year only: t₀ (FirstYearCalculations, column L), scenario 2 (= scenario 1 in t₀).
**Inputs**: typed Egypt GVA by sector (decision R12; legacy K18747:K18756). Prototype codes read: `co2.sec.<s>`
(MtCO2), `dem` of subsector s (ktoe; legacy ener.<s>.ecy.t rows 10046-10071, ftr = domestic use), `co2.grid`
(tCO2/MWh = MtCO2/TWh; legacy row 18665 = co2.pow / electricity supplied, TWh), θ_g.
Sectors S10 = foo, srv, mch, irn, nfm, mac, cem, omn, cst, ftr.

```
R12.1  GVA, typed:              V_s,  s ∈ S10                                      (USD bn real R, base year t₀)
R12.2  indirect CO2:            C^i_s = dem_s(t₀) · θ_g / 1000 · co2.grid(t₀)                     (MtCO2; rows 18721-18730)
R12.3  direct CO2:              C^d_s = co2.sec.s(t₀)                                              (MtCO2; rows 18638-18663)
R12.4  direct intensity:        e^d_s = 1000 · C^d_s / V_s                                         (tCO2 per USD m)
R12.5  indirect intensity:      e^i_s = 1000 · C^i_s / V_s                                         (bug L216 fixed, ftr)
R12.6  total intensity:         e_s = e^d_s + e^i_s
R12.7  GVA share:               v_s = max(0.01, V_s / Σ_{S10} V)                                   (as legacy, I131)
R12.8  emissions share:         c_s = C^d_s / Σ_{S10} C^d                                          (bug L217 fixed)
R12.9  cumulative (MTOutputs):  cv_k = Σ_{j ≤ k} v_j,  cc_k = Σ_{j ≤ k} c_j   in the order ftr, foo, mch, omn, cem, irn,
                                cst, mac, nfm, srv                                                  (bug L218 fixed)
```

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| gva.<s> | Gross value added of sector s, base year (typed) | USD bn real | R12.1 | 18747-18756 K |
| co2.ind.<s> | Indirect CO2 of sector s (electricity use x grid intensity) | MtCO2 | R12.2 | 18721-18730 |
| emin.d.<s> | Direct CO2 intensity of output | tCO2 per USD m | R12.4 | 18747-18756 G; MTOutputs 124-132 K |
| emin.i.<s> | Indirect CO2 intensity of output | tCO2 per USD m | R12.5 | 18747-18756 H; MTOutputs L |
| emin.<s> | Total CO2 intensity of output | tCO2 per USD m | R12.6 | 18747-18756 I; MTOutputs M, 134-143 M |
| emin.v.<s> | Share of GVA (min 1%) | share | R12.7 | 18747-18756 L; MTOutputs N, 134-143 K |
| emin.c.<s> | Share of direct CO2 of S10 | share | R12.8 | 18762-18771 I; MTOutputs 134-143 L |
| emin.cv.<s>, emin.cc.<s> | Cumulative GVA and emissions shares | share | R12.9 | MTOutputs 134-143 N, O |

Typed values and the Egypt results: `Equations_addendum_notes.md` (R12).

## E. R6-R10

### R6. Residential initially-exempt demand (most-used cooking fuel), as legacy

**Legacy**: Mitigation rows 1784-1795 (share), 5554/5557/5558 (totals), 5564-5566 (not-exempt rows), 5568-5570
(initially exempt rows), 5577/5583/5588 (leakage base), 2258 (years since CPIntro); Distribution rows 1077-1079,
2246-2263, 2288-2289. Columns L = 2022 (base year) ... AE = 2041 (year row 5540).
**Inputs**: MTInputs `ExemptMostCook`, `ExemptCookDeciles` (scenario 1; prototype Settings C69:C70), `ExemptPhaseout`,
`YearPha`, `ExemptPhaseoutPeriod` (per scenario; prototype `R_POL`); HHSurvey `<fuel>_share`, `cons_pc_acrent`,
`popw` of `distn.bsh.dec.ove.mean.<d>` and of the basket `distn.bsh.bkt.ove.mean.9999`; WHOCooking `distn.pcoff.ove`.
Prototype codes read: `enel`, `ener`, `atp` (residential), `lkp`, `lkx`, `lkxp`, `CookFuel`, `ExemptCookShare`.

The prototype v5.6 split (Equations.md last section; section 6b rows `lkxp`, `lkxe`, `lkxr`, `lkx`, `lkxa`) already
matches legacy rows 5568-5570 algebraically (enel ratio × price ratio^(εU(phase−1)) = legacy income, shock, efficiency
terms with the usage term εU·phase). Three changes make it legacy-exact: R6.1 (cooking-fuel default), R6.3 (basket
denominator), R6.7 (leakage on the not-exempt part only).

```
R6.1  most-used cooking fuel:   m* = WHOCooking fuel of distn.pcoff.ove;  "lpg" if the code is missing      (as legacy L1784; I137)
R6.2  exempt-deciles spend:     S_x = Σ_{d ≤ D} b_d · y_d · w_d · 1[ExemptMostCook = Yes]                   (D = ExemptCookDeciles; L92 not reproduced)
R6.3  exempt share:             s = S_x / (b_bkt · y_bkt · w_bkt)   if m* ∈ {nga, lpg, ker}, else 0       (as legacy K1795; I136)
                                b: budget share of m* (HHSurvey <m*>_share), y: cons_pc_acrent, w: popw; bkt = basket row 9999
R6.4  phase-in:                 φx(t) = 1[ExemptPhaseout] · min(max((t + 1 − YearPha)/ExemptPhaseoutPeriod, 0), 1)   (bug L94 fixed: rule of rows 2259-2265; unchanged lkxp)
R6.5  initially exempt use:     F_x(t₀) = s · Qᵉ[m*,res](t₀)
                                F_x(t) = F_x(t−1) · Qᵉ[m*,res](t)/Qᵉ[m*,res](t−1) · (P[m*,res](t)/P[m*,res](t−1))^(εU (φx(t) − 1))
                                (= legacy M5568:M5570 with the usage term εU·φx; income factor present, L48 not reproduced; unchanged lkx)
R6.6  adjustment to fuel use:   A_x(t) = F_x(t) − s · Qᵉ[m*,res](t)              (unchanged lkxa; enters Lk through lkc as now)
R6.7  leakage change (E69c):    d_m(t) = − (Q[m,res](t−1) − F_x,m(t−1)) · e_m · p_m(t)      (as legacy 5577, 5583, 5588: exempt use does not leak; I138)
```

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| CookFuel (Settings C65) | Most-used cooking fuel, default lpg | text | R6.1 | 1784 L |
| ExemptCookShare (Settings C83) | Initially exempt share of the most-used cooking fuel, basket denominator | share | R6.2-R6.3 | 1787-1795 |
| lkd (changed) | Leakage change computed on the not-exempt use | ktoe | R6.7 | 5577, 5583, 5588 |
| lkxp, lkx, lkxa (unchanged) | Phase-in, initially exempt use, adjustment | share, ktoe | R6.4-R6.6 | 2259-2265, 5568-5570, 5554-5558 |

### R7. Producer subsidies with their price effect, as legacy

**Legacy**: per-unit subsidy rows 825-829 (spread over world / domestic demand); every price block "in which:
producer-side subsidies" (e.g. 2455 coal power, 2547 residential gas): history = row 825-829 value, projection
O = $J × row 2213 (factor of the year); supply cost = fixed + floating + producer subsidy (rows 2452, 2544); floating
taxes (2461, 2553) = (sp_L − sp(t) + cs_L)(1 − π), floored, × price-control factor 2216/2217. Electricity: rows
3587-3592 (allocation, per kWh, residual), 3601/3630 (in the price sum 3609/3638, passed through at π by 3610/3639).
**Inputs**: MTInputs producer-subsidy phase-out rows (prototype `SUB_PARAMS`, `ProdSubPhaseScope_*`); Prices_dom
`mit.pros.<f>.all` (coa, nga, oil, bio, ecy), `mit.txo.ecy.res/ind` (new read), `mit.rp.ecy.*`. Prototype codes
read: `psu`, `psd`, `psf`, `pros`, `psp`, `spf`, `gpi`, `pcc` (D), `sc`, `cons`, `rppre`, `pass`.

The fossil price effect is built (v6.1-6.2, I49): `psp` in the supply cost, reform as a separate wedge `ppsw`
(= π·Δps), equal to legacy except where the floor of E22 or the price-control phase-out acts on the floating part.
As legacy, the reform moves into the supply cost (R7.1-R7.2), so E21-E22 and the price-control wedge see it.

```
R7.1  producer subsidy in the block:  ps_c(t) = psp_c(t) · psf_f(c)(t)        (t > L; ≤ 0)              (as legacy O2455 = $J2456 × O2213)
R7.2  supply cost (E20):              C_c(t) = C̄_c + (C_c(t−1) − C̄_c − ps_c(t−1)) · Π_c(t)/Π_c(t−1) + ps_c(t)
                                      E21-E23 unchanged (they now absorb (1 − π_c) of the reform; floors as E22)
R7.3  wedge:                          ppsw = psw = 0  (or memo = Δretail of the reform);  rsr: drop the psw VAT term   (VAT is in E24)
R7.4  fiscal line:                    rpsu = −Σ_f pros_f · psf_f                                       (unchanged; L82, L83 not reproduced in 465)
Electricity (t ≤ L data years, then held; u ∈ {res, ind}):
R7.5  allocation to residential:      a_res = (max(0, sc_res − (rp_res − tx_res)) · cons_res) / Σ_u max(0, sc_u − (rp_u − tx_u)) · cons_u
                                      fallback cons_res / Σ_u cons_u if the sum is 0; 1 if both fail;  a_ind = 1 − a_res   (as legacy 3588-3589)
R7.6  per kWh:                        ps_u = max(−0.3, −pros_ecy · a_u / cons_u · 10³)   ($/kWh; pros_ecy USD bn > 0 as data)   (as legacy 3590-3591; I146)
R7.7  residual (memo):                psr_e = −pros_ecy − Σ_u cons_u ps_u / 10³                         (USD bn; as legacy 3592)
R7.8  projection (t > L):             ps_u(t) = ps_u(L) · f_ps(t);   psr_e(t) = psr_e(L) · f_ps(t)       (f_ps = pof.ps × ProdSubPhaseScope_ecy)
R7.9  price before policies (E49):    pp_u(t) = pp_u(t−1) + π_u [ (sc_u(t) − sc_u(t−1)) + (ps_u(t) − ps_u(t−1)) ] (1 + v_u)   (as legacy 3601, 3609-3610)
```
- tx_u is the dataset excise / subsidy of electricity (Prices_dom `mit.txo.ecy.u` × CPI index), rp_u, sc_u, cons_u the
  values of the year (legacy columns K..N, held from the last data year: $J). Revenue: `rpsu` keeps the fiscal line
  (pros incl. ecy × factor); the electricity price change enters `rgap` through pp_u as now.

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| psb | Producer subsidy of the block after the phase-out (in the supply cost) | $/GJ real | R7.1 | 2455, 2478, 2501, 2524, 2547, ... (block row "in which: producer-side subsidies") |
| sp (changed) | Supply cost incl. the phased producer subsidy | $/GJ real | R7.2 | 2452, 2544, ... |
| ps.ecy.sh | Share of the electricity producer subsidy to the user group | share | R7.5 | 3588-3589 |
| ps.ecy | Electricity producer subsidy per kWh by user group (floored at −0.3) | $/kWh | R7.6, R7.8 | 3590-3591, 3601, 3630 |
| ps.ecy.res | Electricity producer subsidy above the floor (memo) | USD bn | R7.7-R7.8 | 3592 |
| rppre (changed) | Electricity price before policies, incl. the producer subsidy change | $/kWh | R7.9 | 3609-3613, 3638-3642 |

### R8. Manual inputs: domestic prices, elasticities, electricity producer subsidy, methane intensity decline

**Legacy**: Mitigation rows 765-829 (domestic prices, column F flag, K..P = 2021..2026 by year row 764), Manual inputs
G59:N146 (names `_manual_codes` G59:G146, `_manual_prices` G59:N146, `_manual_years` G59:N59 = 2021..2026);
Elasticities C27:C133 (F manual, G simple, D adjustment); Manual inputs K279:N307, L319:L321; Mitigation rows
6077-6079, 6103, 6159, 6171, 6183 (intensity paths), 6203, 6206, 6212 (emissions), Manual inputs J185:J188.
**Inputs**: MTInputs `DomPrTax` (= name EnergyPricesManualSwitch), `ElIncMainSrc`, `ElPrcMainSrc` (in the
prototype ScenarioDefinition, not read; scenario 1); Manual inputs tab (prototype, legacy addresses, placed). Prototype
codes read: Inputs_prices `rpn`, `spn`, `txn`, `vrd` (by year), `pros`; Inputs_power `rp`, `vatrate` (ecy); Inputs_ela
(key type|fuel|sector); `ch4.em`, `ch4.act`, GHGYear.

```
Manual domestic prices, every price code k = mit.<var>.<fuel>.<sector> of Manual inputs G59:G146 (var ∈ sp, txo, vatrate, rp, pros):
R8.1  manual flag:            man_k = 1[DomPrTax = Yes] · 1[ISNUMBER(M_k(2021))]          (as legacy F765:F829; issue I53 replicated)
R8.2  value of year y:        V_k(y) = M_k(y) · ι(y)   if man_k = 1 and ISNUMBER(M_k(y)),  else Data_k(y) · ι(y)
                              (vatrate: no ι; pros: USD bn; y ∈ 2021..2026, later years: data)   (as legacy rows 765-829; L86, L100 not reproduced)
                              V replaces the Prices_dom value in rpn, spn, txn, vrd, pros (fuels) and rp, txo, vatrate (ecy)
Manual elasticities, key (type, fuel group f, sector group g), g ∈ {tra, res, ind, srv} = Manual inputs columns K, L, M, N:
R8.3  income:                 εY[f,g] = max(MI_inc[f,g] + adjY[f,g], 0)   if ElIncMainSrc = Manual             (rows 279-286; bug L101 fixed: srv reads N)
R8.4  usage, efficiency:      εU[f,g] = min(MI_usg[f,g] + adjP, 0),  εF[f,g] = min(MI_eff[f,g] + adjP, 0)  if ElPrcMainSrc = Manual   (rows 291-298, 300-307)
R8.5  cross-price:            σ_j = MI_cro,j   if ElPrcMainSrc = Manual   (j: biomass/LPG, biomass/kerosene, gasoline/diesel; L319:L321;
                              bug L220 fixed: default = the simple value Elasticities G131:G133, not C91:C93)
                              blank manual cell → #N/A, as legacy "no data" (I140); adj = 0 (Base; adjustments not built)
Methane intensity decline (CH4 sources j; rate δ_j: og, dg, bm = J185; cm = J186; liv, ric = J187; wst = J188):
R8.6  intensity index:        κ_j(t) = (1 − δ_j)^max(0, t − Y)        (Y = GHGYear; legacy: 1 up to 2023, declining from 2024)   (I141)
R8.7  emissions (E84):        CH4_j(t) = E_j · Act_j(t)/Act_j(Y) · κ_j(t) · (1 − abt_j)            (bug L135 fixed for liv, ric, wst; as legacy for og, dg, cm, bm)
```

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| man.flag | Manual price row in use (by code) | 0/1 | R8.1 | 765-829 F |
| rpn, spn, txn, vrd, pros, ecy rp/txo/vatrate (changed) | Domestic price data, manual where flagged | per unit real | R8.2 | 765-829 K:P |
| ela (Inputs_ela, changed) | Elasticity used: manual or country | elasticity | R8.3-R8.5 | Elasticities C27:C133 |
| ch4.int | Methane intensity index of source j | index | R8.6 | 6077-6079, 6103, 6159, 6171, 6183 |
| ch4.em (changed) | Methane emissions of source j | kt CH4 | R8.7 | 6140-6151, 6203, 6206, 6212 |

### R9. Electricity consumer subsidy option and the power cost memo tables

**Legacy**: rows 3575-3578, 3604-3607 (historical tax/subsidy), 3606/3635 (projection), 2214 (consumer factor),
MTInputs row 138; E4 rows 3497-3506 (`cur`), E5 rows 3508-3517 (`pcb`, CostBreakdownYear), F1 rows 3521-3530;
scenario 2 = +6316 (9824-9833). F2-F4, F5, F6, F7 are built (`fce`, `cik`, `tic`, `tvc`, `swi`, `swd`).
**Inputs**: MTInputs `PowerSubsidyExemptInclude` (missing in the prototype; options DoNotPhaseOut* / Include, legacy
Dashboard L54), `CostBreakdownYear` (in ScenarioDefinition, not read), `SupplyCostDeltaSubsidy` (not read); Prices_dom
`mit.txo.ecy.res/ind`. Prototype codes read: `pof.cs`, `sc`, `rppre`, `pass`, `cax`, `dlf`, `cfu`, `opf`, `vop`, `fpp`,
`xck`, `cic`, `msc`, `ccp`, `shk`, `rns`, `lfx`, `tvc`, `TrCostShare`, `cptraj`.

```
Consumer subsidy (u ∈ {res, ind}; L = last historical price year):
R9.1  base tax / subsidy:     tx_u(L) = Prices_dom txo.ecy.u(L) · ι(L)   if the dataset has it;
                              else rp_u(L) − sc_u(L) − ntx_u(L) if SupplyCostDeltaSubsidy = Yes; else 0    (as legacy 3604-3606)
R9.2  phase-out:              Δcs_u(t) = 1[tx_u(L) < 0 and PowerSubsidyExemptInclude = Include] · tx_u(L) · (pof.cs(t) − 1)   (as legacy O3606, O3635; L84 not reproduced)
R9.3  price before policies:  E49 (with R7.9) + π_u (Δcs_u(t) − Δcs_u(t−1)) (1 + v_u)      (passed through at π as legacy 3610/3639)
Cost memos by type k (year columns; $/kWh):
R9.4  current total cost:     cur_k = max(lfx_k + tvc_k, c_min)                                          (as legacy E4 3498-3506)
R9.5  system cost:            sys_k = dtc_k/(cf_k H dlf_k) + ℓ_k msc + cic_k + TrCostShare · tcx_k/(cf_k H dlf_k)   (as legacy F1 3522-3530)
Breakdown in T_b = CostBreakdownYear (columns L..T of E5):
R9.6  capital:                kc_k = cax_k(T_b)/(cf_k H dlf_k)                                         (C1)
R9.7  O&M:                    om_k = opf_k/(cf_k H) + vop_k                                           (A16 + D1)
R9.8  fuel:                   fu_k = fpp_k θ_e/ν_k + xck_k                                            (D2; existing carbon as the prototype vbc)
R9.9  system integration:     sys_k(T_b)                                                              (F1)
R9.10 carbon price:           cp_k = ccp_k(T_b)                                                       (D5)
R9.11 renewable subsidy:      rs_k = rns_k(T_b) for wind, solar, hydro, other renewables, biomass; blank otherwise   (A17)
R9.12 total, check:           cur_k(T_b);   chk_k = kc + om + fu + sys + cp + rs − cur_k        (shadow price and floor not a column: I142)
R9.13 carbon tax memo:        τ_b = cptraj(T_b) · 1[scenario > 1]                                     (bug L222 fixed)
```

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| txe | Electricity consumer tax / subsidy of the last price year (dataset) | $/kWh real | R9.1 | 3577, 3583, 3604-3606 J |
| csd | Consumer subsidy phase-out change in the electricity price | $/kWh | R9.2-R9.3 | 3606, 3635 |
| cur | Current total cost by type | $/kWh | R9.4 | 3498-3506 |
| sys | System cost (decommissioning, storage, coal implicit cost, transmission share) | $/kWh | R9.5 | 3522-3530 |
| pcb.cap, pcb.om, pcb.fuel, pcb.sys, pcb.cp, pcb.rns, pcb.tot, pcb.chk | Cost breakdown by type in CostBreakdownYear | $/kWh | R9.6-R9.12 | 3509-3517 L:S |
| pcb.ct | Carbon tax in CostBreakdownYear | $/tCO2 | R9.13 | 3509 T, 9825 T |

### R10. Road biofuels in the elasticity road model, self-generated renewables in aviation and navigation, range-anxiety fit

**Legacy**: rows 5390-5392, 5403-5406 (elasticity branch), 5435-5438 (switch), 5480/5505 (renewables price),
5491/5516 (renewables use), 2805-2806 (renewables price block = solar `tic`, row 3468), 4354-4356 (range anxiety),
18966-18972 (EV sales shares), Transport3 rows 1-226 (fit year A1 = 2025, stored solutions H, N, T).
**Inputs**: `TrModel`; base-year road bgs, bdi, obf (prototype `trp.ebb`/`trp.ebc`, `eb|bgs` ...); EnergyCons `ren` of
avi, nav (new read); Inputs_ela keys `inc|oil|tra`, `usg|oil|tra`, `eff|oil|tra`, `aei|oil|tra`, `*|ren|tra`;
`AddEffRoad` group α⁺ (AEG road group). Prototype codes read: `enel` (rod gso, die), `atp` (bio, rod), `shp.bio`,
`tic.sol`, `cov` (avi, nav), `trra`, `trraf*`, Transport3 tables RAPas/RAFre/RACyc.

```
Road biofuels, elasticity road model (TrModel ≠ Engineer; engineer branch T17 unchanged):
R10.1 bioethanol:             Q_bgs(t) = Q_bgs(t−1) · Qᵉ[gso,rod](t)/Qᵉ[gso,rod](t−1)   (hold if Qᵉ[gso,rod](t−1) = 0)   (as legacy 5404)
R10.2 biodiesel:              Q_bdi(t) = Q_bdi(t−1) · Qᵉ[die,rod](t)/Qᵉ[die,rod](t−1)                                  (as legacy 5405)
R10.3 other biofuels:         Q_obf = E69 with P = P[bio,rod], Sh = Sh[bio,rod], εY, εU, εF, α of oil|tra, α⁺ road group  (as legacy 5406; I143; L46 not reproduced)
R10.4 road biomass:           Q[bio,rod] = Q_bgs + Q_bdi + Q_obf                                      (replaces the biomass-elasticity row; as legacy 5403, 5435)
Self-generated renewables, s ∈ {avi, nav}:
R10.5 price:                  P[ren,s](t) = tic_sol(t) + 0 · cov_s                    (nce of renewables typed 0, as legacy 2805-2806, 5480, 5505)
R10.6 use:                    Q[ren,s](t) = Q[ren,s](t−1) (1/(1+α_ren+α⁺_road))^(1+εU) (1+g)^(εY inc) (1 + shock·switch)
                                            · (P/P₋₁)^εU · (P/P₋₁)^(εF (1+εU))        (elasticities ren|tra; no shadow price: I144;
                                                                                      shock row 2439 as every row, L47 not reproduced)
R10.7 totals:                 Q[ren,s] enters Q[S] and the sector totals (ktoe); no CO2, CH4 or revenue
Range anxiety fit (goal seek, scenario 1, class c ∈ {pas, fre, cyc}; T_f = 2025):
R10.8 residual:               r_c(RA0_c) = sh_EV,c^(1)(T_f; RA0_c) − act_c(T_f)                       (as Transport3 G4, M4 (× 10), S4)
R10.9 solution:               RA0_c* : r_c = 0 (root on the start value of trra; negative values allowed: I145),
                              stored by country in the RA tables (RAPas, RAFre, RACyc), read by trra as now (LD63)
```

| Code | Meaning | Unit | Equation | Legacy rows |
|---|---|---|---|---|
| ener.rod.bgs | Road bioethanol (elasticity model) | ktoe | R10.1 | 5404, 5436 |
| ener.rod.bdi | Road biodiesel (elasticity model) | ktoe | R10.2 | 5405, 5437 |
| ener.rod.obf | Road other biofuels (elasticity model) | ktoe | R10.3 | 5392, 5406, 5438 |
| ener.rod.bio (changed) | Road biomass = sum of the three biofuels | ktoe | R10.4 | 5403, 5435 |
| atp.ren | Price of self-generated renewables (solar levelised investment cost) | $/kWh | R10.5 | 2805-2806, 5480, 5505 |
| ener.avi.ren, ener.nav.ren | Self-generated renewables in aviation, navigation | ktoe | R10.6-R10.7 | 5491, 5516 |
| ra.fit | Range anxiety start value solved on the fit year (stored table) | $/vehicle | R10.8-R10.9 | Transport3 H, N, T; 4354-4356 N |

## F. Output blocks to the modules (no copies)

User decision 2026-10-29: the air pollution and transport co-benefits modules read the Mitigation sheet in place;
there are no export copies for them (section 19 keeps only 19a, Distribution). Each output block is one section
whose heading says so; every row a module reads sits in that section. The rows are model rows (computed once,
used by the sheet and read by the module), so no new variable is defined here, only placement and headings.

```
F.1  section 15 heading:  "15. Local air pollutants: outputs to the air pollution module"
F.2  section 5b heading:  "5b. Road transport: engineer model and outputs to the transport co-benefits module"
```

| Block | Rows the module reads (both scenarios: 1 and the scenario) | Legacy (465) | Prototype |
|---|---|---|---|
| 15 | Emissions by module sector (coal and gas plants, other plants, road, ground level other, other, food & forestry) and pollutant (t/year) | E3 rows 15844-16053 | `ap` by module sector (E90), in section 15 |
| 15 | Energy use of the power and residential sectors by fuel (ktoe) | E3 rows 15814-15840 | sums of `ener` (power: `pe`), new rows in section 15 |
| 15 | CO2 from energy (Mt) | E3 row 16054 | reference to `co2` total, row in section 15 |
| 5b | Road fuel use by vehicle class (passenger, 2-3 wheeler, freight) and fuel (gasoline, diesel, LPG, gas, electricity; bln liter or kWh) | E2 rows 15710-15721 | engineer 5b fuel use by class (`trfcp`, `trfcc`, `trfcf`, `trfce`) |
| 5b | Road and total consumption by fuel (ktoe), road share of each fuel | E2 rows 15744-15787 | switched model `ener` (rod, total); share = road / total; new rows in 5b |
| 5b | Fuel economy by fuel (km per liter or kWh) | E2 rows 15788-15799 | `trafg`, `trafo`, `trafe` |
| 5b | Vehicle-km: passenger, freight, 2-3 wheeler, all (bln km) | E2 rows 15800-15809 | `trkm` by class, `trkmt` |

Issue I100 (replicated): vehicle-km, fuel economy and class splits come from the engineer road model whatever
TrModel is; only the road share of each fuel follows TrModel.
