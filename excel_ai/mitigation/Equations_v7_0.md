# Model equations of CPAT-AI-Mitigation-MVP v6.4

CPAT-AI-Mitigation-MVP is a carbon-pricing mitigation model for one country at a time, built on the method of legacy CPAT. The country is a setting; every country-specific number comes from the reference tables (data sheets), looked up by the country code. It projects energy prices, fuel use by subsector and fuel, the power sector, government revenue, CO2 and other greenhouse gases, local air pollutants and the GDP effect of the revenue. The model runs year by year from the base year t₀ (a setting) to 2041. Each scenario is a group of year columns with the same equations and its own policy inputs: scenario 1 is the baseline, scenario 2 the live policy scenario. This note gives the equations in mathematical form, for the projection years. `Formulas_v7_0.md` is the implementation reference: every workbook formula, its rows and lookups.

## 0. Notation

Index sets:

| Index | Set |
|---|---|
| t | years t₀ (base year) to 2041 |
| f | fuels: coal, natural gas, gasoline, diesel, LPG, kerosene, other oil products, biomass (8) |
| s | subsectors (16): road, rail, domestic aviation, domestic navigation; residential, food & forestry, services; mining & chemicals, iron & steel, other metals, machinery, cement, other manufacturing, construction, fuel transformation; other energy use |
| S | sectors: transport, buildings, industry, other energy use (groups of s); power is separate |
| e | ETS and coverage sectors: power and the 16 subsectors (17) |
| G(e) | sector group of feebates and ETS benchmarks: power, transport, residential (buildings), industry |
| c | price fuels (12): coal and gas for power, residential, industry; gasoline, diesel, LPG, kerosene, other oil products, biomass; c(f,s) is the price fuel of fuel f in subsector s |
| k | generation types (9): coal, gas, oil, nuclear, wind, solar, hydro, other renewables, biomass; CG = {coal, gas} |
| u | electricity user groups: residential, industry |
| d | electricity demand groups: transport, residential, industry, services; d(s) is the group of subsector s |

Conventions:

- Every money value is in real US dollars of the results year R (scenario input). L is the last historical price year (setting). Y is the last GHG inventory year of the country (setting).
- X^(1)(t) is the value of X in scenario 1 in the same year. ΔX = X − X^(1).
- 1[·] is 1 if the condition holds, else 0. "Yes/No" inputs are switches of the scenario.
- θ = PJ per ktoe. Fuel use is in ktoe, so fuel use × θ × ($/GJ) is USD million. Other unit constants: H = hours per year, θ_e = GJ per kWh, M = million kWh per MW-year (H × 10⁻³), θ_g = GWh per ktoe; 1000 converts t to kt and kt to Mt.
- Numbers in parentheses in the symbol tables are the default assumptions of sheet Constants or Settings, not country data.
- Linear policy path from x0 in year T0 to x1 in year T1, continued linearly (Λ) or held flat (Λ̄) after T1:

```
Λ(t; T0,T1,x0,x1) = 0                                        if t < T0
                  = x0 + (x1 − x0) · (t − T0) / max(T1 − T0, 1)  otherwise
Λ̄(t; T0,T1,x0,x1) = Λ(min(t,T1); T0,T1,x0,x1)
```

Each section lists its parameters and data. The computed variables, with units and workbook codes, are in the closing table.

## 1. Policies

| Symbol | Meaning (source) |
|---|---|
| ι(t), δ(t) | US CPI and US GDP deflator indices, = 1 in R (IMF WEO): ι(t) = CPI(R)/CPI(t), δ(t) = Defl(R)/Defl(t) |
| T0, T1, x0, x1 | start and target year, start and target level of each policy (scenario inputs) |
| cov_e, cov_f | carbon tax coverage of sector e and of fuel f (switches; biomass covered, EF 0) |
| covE_e, fbcov_e | new ETS and feebate coverage of sector e (switches) |
| B0_G, B1_G | ETS benchmark (share of emission intensity allocated free) at start and target year (assumptions, sheet Constants) |
| σ_e | ETS semi-elasticity of emissions to the price (by country and sector group: power, transport, residential, industry; legacy ETS+LTS table) |
| ϑ | effectiveness of output-based allocation (setting) |
| vol, imp, risk | ETS price volatility, abatement-cost impact of volatility, carbon tax policy risk (scenario labels, Settings table) |
| CO2base_e | baseline CO2 by ETS sector: scenario-1 CO2 of section 6, held as data |
| a_ssc | share of the feebate shadow price on the efficiency margin (sheet Constants) |
| XT[j,f](t), XE[j,f](t) | existing carbon tax and ETS of ECP sector j and fuel f in data year t, real $/tCO2 (sheet Inputs_ecp from the World Bank Carbon Pricing Dashboard and ICAP data of sheet ECP; v4.12, as legacy rows 1711-1764): XT = rate_f · scov_j · fcov_f, XE = p^nat · ncov_j · nfcov_f + p^EU · rcov_j · rfcov_f; Tx = last data year |
| γ^ct, γ^ets | assumed real growth of the existing carbon tax and ETS price after Tx |
| xcov_e | national existing ETS coverage of sector e in the year (data year min(t, Tx)) |
| ex | residential LPG and kerosene always exempted (switch AlwaysExemptResLPGKer, by scenario; legacy rows 5546-5547) |

```
E1   carbon price:          τ(t) = Λ(t; T0,T1,x0,x1) · ν(t)    (Λ̄ unless the path continues "Linear")
                            ν(t) = ι(t) if the inputs are nominal, else 1
E2   fuel price reform:     F_c(t) = Λ(t; T0^F,T1^F,F0_c,F1_c)                       (price units of c)
E3   feebate rate:          b_G(t) = Λ(t; T0^b,T1^b,b0_G,b1_G)                        ($/tCO2)
E4   ETS on:                on(t) = 1[new ETS = Yes and t ≥ T0^E]
E5   effective coverage:    κ_e(t) = on(t) · covE_e
E6   benchmark, OBR share:  B_G(t) = Λ̄(t; T0^E,T1^E,B0_G,B1_G),   ω_e(t) = min(1, max(0, B_G(e)(t)))
E7   baseline covered CO2:  bce(t) = Σ_e CO2base_e(t) · κ_e(t)
E8   cap:                   chg(t) = Λ̄(t; T0^E,T1^E,chg0,chg1)                       (t ≥ T0^E)
                            cap(t) = on(t) · cap(t−1)                    if t > T1^E and the cap is held "Constant"
                                   = on(t) · bce(t) · (1 + chg(t))        otherwise
E9   volatility adjustment: V = (1 + risk · imp) / (1 + vol · imp)
E10  semi-elasticity:       σ̄(t) = Σ_e CO2base_e κ_e σ_e (1 − (1 − ϑ) ω_e) / bce(t)
E11  fast price estimate:   p̂(t) = ln(cap/bce) / (σ̄ · V)     if on = 1, 0 < cap < bce, σ̄ < 0;  else 0
E12  permit price:          p_E(t) = on(t) · { override(t) (blank: τ(t))  if the price is overridden;  p̂(t) otherwise }
E13  tax-equivalent price:  p̃_E(t) = p_E(t) · V,      revenue factor ρ = 1/V
E14  carbon tax by sector:  T_e(t) = τ(t) · c_e · (1 − κ_e(t))
                            c_e = 1 − xcov_e if the new tax is complementary to an existing ETS, else cov_e
E15  ETS cost by sector:    A_e(t) = p̃_E(t) · κ_e(t) · (1 − ω_e(t))                  (auctioned part, in the price)
E16  shadow price:          Σ_e(t) = (b_G(e)(t) + reg_G(e)) · a_ssc · 1[fbcov_e] + p̃_E(t) · κ_e(t) · ω_e(t)
                            reg = 0 (regulations: placeholder)
E17  existing carbon tax:   φ^ct(t) = 1[apply] · (1 + γ^ct)^max(0, t − Tx)        (factor on the data)
     existing ETS:          φ^ets(t) the same with γ^ets
E18  methane fee:           m(t) = Λ(t; T0^m,T1^m,m0,m1) · 1[scenario > 1] + 1[carbon tax applies to methane] · τ(t)   ($/tCO2e)
E18a exemption factor:      x[f,s] = 0  if f ∈ {LPG, kerosene}, s = residential and ex starts with "Yes";   1 otherwise
```

- E11 is the log form of the legacy quick estimate, and V replaces its hardcoded 1.1 (fixes legacy bugs L15, L16).
- The fast estimate meets the cap only approximately. Section 6 gives the next-iteration price that a goal seek uses to close the gap; the solved prices enter E12 as the override.

## 2. Retail prices before and after policies

| Symbol | Meaning (source) |
|---|---|
| gpn_m(t) | international price of commodity m (oil, coal, gas of the country's market, flat 1 for biomass), nominal, by chosen source (IMF, WB, IEA, EIA or averages) |
| h_m(t) | High/Low adjustment of m after L (1 otherwise) |
| C_c, X_c (t ≤ L) | historical supply cost and excise and other taxes (IMF price dataset, nominal × ι, per GJ) |
| C̄_c | fixed part of the supply cost (margin; coal and gas also production cost), base-year value × ι(t₀) |
| π_c, v_c, u_c | pass-through of supply-cost changes, VAT rate (gasoline, diesel, LPG, kerosene: × household share, sheet OilProductShares, as legacy), GJ per price unit |
| EF[f,s] | calibrated CO2 emission factor (tCO2/GJ), section 6 |
| j(f,s), XCP0[f,s] | ECP sector of the price fuel (coal, gas: their price sector; oil products, biomass, jet fuel: transport; other oil products: industry), existing carbon pricing embedded in the price data (XT + XE in L, $/tCO2) |

Before new policies, by price fuel c (projection t > L; data up to L):

```
E19  international price:   gp_m(t) = gpn_m(t) · δ(t) · h_m(t);   Π_c = gp of the commodity of c
E20  supply cost:           C_c(t) = C̄_c + (C_c(t−1) − C̄_c) · Π_c(t)/Π_c(t−1)
E21  floating taxes:        X̃_c(t) = X̃_c(t−1) − (C_c(t) − C_c(t−1)) · (1 − π_c);   X̃_c(t ≤ L) = X_c
E22  excise and other:      X_c(t) = max(X_c(L), X̃_c(t))  if X_c(L) ≥ 0;   X̃_c(t) otherwise
E23  split by sign:         X⁺_c = max(X_c, 0)  (taxes),   X⁻_c = min(X_c, 0)  (subsidies, negative)
E24  VAT payment:           VAT_c = (C_c + X_c) · v_c
E25  retail price:          R_c = (C_c + X_c) · (1 + v_c)
```

- Other oil products take pass-through and margin from the dataset (fixes legacy bug L13).
- E21: the floating part applies (1 − π) once, so X̃_c(t) = X_c(L) + (C_c(L) − C_c(t)) · (1 − π_c) (v4.10, legacy bug L14 fixed: legacy applies (1 − π) twice in the first projected year when the pass-through is 0.5 or 0.8; no effect for Egypt, pass-through 0 or 1).

New policies and the after-tax price, by fuel f and subsector s (e = s):

```
E26  new carbon tax:        N^ct[f,s] = T_s · EF[f,s] · cov_f · x[f,s]
E27  new ETS cost:          N^ets[f,s] = A_s · EF[f,s] · x[f,s]
E28  new excise (reform):   N^x[f,s] = F_c(f,s) / u_c(f,s) · x[f,s]
E29  total new policy:      N[f,s] = N^ct + N^ets + N^x
E30  existing carbon price: XCP[f,s]  = EF · (XT[j,f](t*) · φ^ct + XE[j,f](t*) · φ^ets),  t* = min(t, Tx)   (level)
                            ΔXCP[f,s] = XCP[f,s] − EF · XCP0[f,s]                          (change vs price data)
E31  after-tax price:       P[f,s] = max(R_c(f,s) + (N[f,s] + ΔXCP[f,s]) · (1 + v_c(f,s)), 0.01)
E32  shadow price:          Sh[f,s] = Σ_s · EF[f,s]
```

The IMF retail prices already contain any existing carbon pricing, so only its change (ΔXCP) enters the price.

An exempt fuel (E18a) carries none of the new carbon tax, ETS cost and new excise, so neither their VAT nor their revenue (E73). Existing taxes, the change in existing carbon pricing, the subsidy phase-outs and the shadow price stay, as legacy. ETS-covered emissions (E7, section 6) still count the exempt fuel where its sector is in an ETS.

## 3. Power

| Symbol | Meaning (source) |
|---|---|
| cax0_k, tcf_k(t) | capital cost at time factor 1 ($/kW) and capex time factor path of the scenario's decline option (legacy power data) |
| N_k, w_k, cf_k, ν_k | lifetime, WACC, capacity factor, thermal efficiency of the scenario (E32a) |
| dtc_k, tcx_k, opf_k, vop_k, rns_k | decommissioning and transmission capex ($/kW), fixed O&M, variable O&M (incl. nuclear fuel), renewable subsidy ($/kWh) |
| dlf_k | discounted lifetime (1 − (1+w)^−N)/(1 − (1+w)^−1) |
| e_k | tCO2 per kWh = EF_k · θ_e/ν_k (calibrated EF, section 6) |
| XCP0_k | existing carbon pricing of power and the type's fuel embedded in the price data ($/tCO2) |
| ℓ_k | VRE flag: 1 for wind, solar, other renewables |
| cbat, cint, obat, cel | battery capex ($/kWh), interface capex ($/kW), battery opex, long-term storage cost per unit (paths) |
| a_st, a_lt, x_lt, h_st, r_st, dlf_ren | storage allocations, long-term start share x_lt, short-term marginal hours h_st, kWh storage per kW, renewables' discounted lifetime |
| tmc_u, π_u, v_u | T&D add-on, pass-through, VAT rate of user group u |
| εY_d, εU_d, εF_d, α_d, α⁺, inc(t), shock(t) | electricity elasticities, autonomous and additional efficiency gain, income factor path, legacy 2023-2024 demand shock (switch Settings C19, on as legacy) |
| ρ_req, χ_k, ρ_gc | MWy required per ktoe of demand (incl. net exports, losses, own use); ktoe of fuel per MWy; generation per unit consumed |
| μ_coal, μ_gas, K_d, K_i, c_min | maximum capacity factors of coal and gas; dispatch and investment logit constants; minimum cost |
| p(t), Rs(t), rb, x_e(t), x_m,u(t) | PPA share of coal and gas generation; renewable subsidy per kWh; rebate switch (1/0); electricity excise; manual electricity excise |
| r_k, q_k, permit_k(t), tb_k | retirement rate (1/lifetime), scale-up rate, investment permitted (Yes and from year), tie breaker |
| e_max, e_f | maximum early coal retirement (share of effective coal capacity) and factor on the cost-based early retirement (legacy power data) |

Every input is read in the scenario's own MTInputs column; the data of the scenario (A0):

```
E32a capacity factor:       cf_k = cfa_k if lo_k < cfa_k < hi else cfs_k;     ν_k = νa_k if νa_k ≥ ν_min else νs_k
                            w_k = Country*: w_c + adj_coal | Tech: w_c + adj_k | else max(w_user | w_income | ws_k, w_min)
                            K_k(t₀) = G_k(t₀) / cf_k;   permit_k from NewInv_k (If Present*: K_k(t₀)/ΣK(t₀) > 0.001), from year Y_k
E32b PPA share:             p(t) = PPA · (max(0, 1 − max(0, t − T_p)/n_p) if the scenario's switch is Yes, else 1)
E32c renewable subsidy:     Rs(t) = −(Rs_base + 1[scenario > 1, t ≥ T_s] · Rs_add · max(0, 1 − (t − T_s)/n_s));
                            rns_k = Rs · 1[wind, solar, other renewables, biomass; hydro if switched on]
```

Costs per kWh ($/kWh):

```
E33  capital cost:          cax_k(t) = cax0_k · tcf_k(t)
E34  vintage averages:      cāx_k(t) = cāx_k(t−1)(1 − φ_k(t−1)) + cax_k(t−1) φ_k(t−1);     cāx_k(t₀) = cax_k(t₀)
                            sto_k(t) = sto_k(t−1)(1 − φ_k(t−1)) + ℓ_k msc(t) φ_k(t−1);     sto_k(t₀) = ℓ_k msc(t₀)
E35  amortised fixed:       fix_k = (cāx_k (1/N_k + w_k/2) + dtc_k/N_k) / (cf_k · H) + opf_k + sto_k
E36  levelised fixed:       lfx_k = (cax_k + dtc_k + tcx_k) / (cf_k · H · dlf_k) + opf_k + rns_k + ℓ_k msc
E37  fuel price:            fp_k(t) = mean of R_c(k)(τ) over τ ∈ [t−4, t] ∩ [t₀, t]   (spot option: R_c(k)(t); v6.2, legacy bug L126: legacy [t−2, t+2])
E38  existing carbon:       xc_k = e_k (XT[pow,f(k)](t*) φ^ct + XE[pow,f(k)](t*) φ^ets − XCP0_k)
E39  variable cost:         vc_k = vop_k + fp_k · θ_e/ν_k + xc_k
E40  new policy cost:       pc_k = e_k (T_pow · cov_f(k) + A_pow) + F_c(k) · θ_e/(ν_k u_c(k))
E41  shadow price, rebate:  sh_k = Σ_pow · e_k;    reb(t) = −Σ_k sh_k(t) · s_k(t₀)  (0 in t₀)
E42  total variable cost:   tvc_k = vc_k + pc_k + sh_k + reb
E43  levelised variable:    lvc_k(t) = Σ_{τ=t..2041} β_k(τ) tvc_k(τ) / Σ_{τ=t..2041} β_k(τ),   β_k(τ) = (1 + w_k)^(t₀−τ)
E44  investment cost:       tic_k = max(lfx_k + lvc_k, c_min)
E45  generation cost:       gc_k = fix_k + vc_k;     gc̄ = Σ_k s_k gc_k;     pc̄ = ρ_gc Σ_k s_k pc_k
E46  VRE share:             vre = s_wind + s_solar + s_other renewables
E47  storage cost:          cph = (cbat + cint/r_st)/(dlf_ren · H) + obat/H
                            msc = a_st · h_st · vre · cph + 2 max(0, vre − x_lt)/(1 − x_lt)² · cel · a_lt · u_lt
```

- E41: the rebate is per kWh generated, with fixed base-year shares (fixes legacy bug L9). E47 applies the long-term allocation once (fixes legacy bug L4); u_lt = LongTermStorageFor100pcVRE (legacy row 3909).

Electricity prices and demand:

```
E48  supply cost:           sc_u(t) = gc̄(t−1) + tmc_u                     (t₀: gc̄(t₀) + tmc_u)
E49  price before policies: pp_u(t) = pp_u(t−1) + π_u (sc_u(t) − sc_u(t−1)) (1 + v_u)    (data up to L)
E50  end-user price:        p_u = pp_u + (pc̄ · π_u (1 − rb) + x_u)(1 + v_u),   x_u(t) = x_e(t) + 1[t > L] π_u (x_m,u(t) − x_m,u(L))
E51  subsidy gap:           gap_u = pp_u/(1 + v_u) − sc_u                 (negative = subsidy)
E52  demand price:          pd_d(t) = w_d p_res(t−1) + (1 − w_d) p_ind(t−1)   (t₀: data of the year before); w_d = price weight of demand group d (Inputs_power)
E53  demand multiple:       M_d(t) = (1/(1 + α_d + α⁺))^(1+εU_d) · (1 + g(t))^(εY_d · inc(t))
                                     · (pd_d(t)/pd_d(t−1))^(εU_d + εF_d + εU_d εF_d) · (1 + shock(t) · switch)
E54  demand:                D_s(t) = D_s(t−1) · M_d(s)(t)  (t₀: data);   D = Σ_s D_s;   cons_res = D_res · θ_g,  cons_ind = (D − D_res) · θ_g  (GWh)
E55  required generation:   Req(t) = ρ_req · D(t)                         (t₀: actual generation)
```

- E53 fixes legacy bugs L1 (services use the services multiple), L2 (autonomous efficiency with the usage elasticity) and L3 (income factor once, not anchored to 2023). g(t) is GDP growth after the feedback (section 9).

Dispatch, capacity, retirement and investment (MW, MWy):

```
E56  capacity:              K_k(t) = K_k(t−1) − Ret_k(t−1) + I_k(t−1)  (t₀: E32a);    Ke_k = cf_k K_k;    Gmax_k = μ_k K_k
E57  coal and gas need:     Rcg = max(Req − Σ_{k∉CG} Ke_k, 0)
E58  minimum run:           Gmin_k = min(max(Rcg − Σ_{j∈CG, j≠k} Gmax_j, 0), Gmax_k),    k ∈ CG
E59  remainder, logit:      rem = max(Rcg − Σ_CG Gmin_k, 0);    λ_k = exp(−K_d max(tvc_k, c_min) / max(min_CG tvc, c_min))
E60  generation:            Gl_k = min(Gmax_k, Gmin_k + rem · λ_k / Σ_CG λ_j);   G_k = Gl_k + p (Ke_k · Rcg/Σ_CG Ke_j − Gl_k)   for k ∈ CG;   G_k = Ke_k otherwise
                            s_k = G_k / Σ_j G_j;    FU_k = χ_k G_k  (fuel use, ktoe);    G_k(t₀) = data
E61  retirement:            Ret_k = min(base_k + 1[coal] · Early, K_k);   Rete_k = cf_k Ret_k
                            base_k = planned retirement (data) if switched on for k, else r_k K_k
E62  early coal retirement: room(t) = max(0, Max_wind + Max_solar − ΔG(t−1) − Σ_{k≠coal} Rete_k(t−1)),  ΔG = max(0, G(t) − G(t−1)); t₀: Max_wind + Max_solar
                            ec = 1 / (1 + exp(−K_i (tic_wind − tvc_coal)/c̲) + exp(−K_i (tic_solar − tvc_coal)/c̲)),  c̲ = min(tvc_coal, tic_wind, tic_solar)
                            Early = max(0, min(e_max · Ke_coal, room) · (1 − ec)) / cf_coal · e_f · (1 − p),   e_f = 0 in scenario 1 unless switched on
E63  need:                  need(t) = max(Req(t) × Req(t)/Req(t−1) − (Σ_k Ke_k − Σ_k Rete_k), 0)     (v6.2: next year's requirement estimated with this year's growth, so no later year is read; legacy bug L67: legacy uses Req(t))
E64  scale-up limit:        Max_k = q_k · Σ_j Ke_j · permit_k
E65  first round (logit):   λi_k = permit_k exp(−K_i tic_k / cmin),  cmin = max(min_{permit} tic, c_min);   I1_k = min(Max_k, need · λi_k/Σ_j λi_j)
E66  second round:          I2_k = permit_k · max(0, min(Max_k − I1_k, deficit − Σ_{j: tic_j+tb_j < tic_k+tb_k} (Max_j − I1_j) permit_j)),
                            deficit = max(need − Σ_j I1_j, 0);   gas: + (deficit − Σ_j I2_j) if PwDeficitGas = Yes
E67  nameplate investment:  I_k = (I1_k + I2_k) / cf_k;    Inv$_k = I_k · cax_k(t) / 1000  (USD m);   φ_k = I_k / (K_k + I_k − Ret_k)
E68  power CO2:             CO2_k = FU_k · EF_k   (EF_k in MtCO2/ktoe)
```

- E60 has no stray reference (fixes legacy bug L11); total nameplate investment is the sum over types (fixes legacy bug L12). The PPA share runs at its capacity factor scaled to the need (legacy rows 3794-3805).
- E61 caps effective retirement like nameplate retirement (fixes legacy bug L8); E62 keeps nameplate and effective capacity apart (fixes legacy bug L7).
- E63 uses actual capacity (fixes legacy bug L10); E65 normalises by the cheapest permitted type (fixes legacy bug L6); E67 values investment at the capital cost of the year (fixes legacy bug L5).

## 4. Fuel use by subsector

| Symbol | Meaning (source) |
|---|---|
| Q[f,s](t₀) | base-year fuel use (energy balance data, ktoe) |
| εY, εU, εF | income, usage and efficiency elasticities of fuel f in subsector s (legacy CPAT elasticities) |
| α | autonomous energy efficiency improvement |

```
E69  Qᵉ[f,s](t) = Qᵉ[f,s](t−1) · (1/(1+α+α⁺_G(s)))^(1+εU) · (1 + g(t))^(εY · inc(t)) · (P(t)/P(t−1))^εU
                  · ((P(t) + Sh(t)) / (P(t−1) + Sh(t−1)))^(εF (1+εU)) · (1 + shock(t) · switch),   Qᵉ(t₀) = Q(t₀)
     Q[f,s](t)  = Qᵉ[f,s](t) + Lk[f,s](t)        (Lk: residential leakage to biomass, section 4a; 0 elsewhere)
E70  Q[S] = Σ_{s∈S} Σ_f Q[f,s];     Q[f] = Σ_s Q[f,s] + Σ_{k: fuel f} FU_k;     Q = Σ_f Q[f]
```

- P is the after-tax price (E31), Sh the shadow price (E32), g GDP growth (E95), inc(t) the income factor (legacy row 2433, as power demand E53; v4.12; in the workbook: section 0 row 14 = (1 + g)^inc − 1). α⁺_G(s) is the additional policy-induced efficiency gain of the subsector's legacy group (MTInputs 243-245 by scenario: road vehicles = road, rail, aviation, navigation; residential; industrial = the other subsectors, other energy use included: legacy bug L66), v4.13. Residential biomass has εY = 0 unless MTInputs `BiomassNormal` = Yes (legacy row 5567; v4.13). This is CPAT equation 3.3.3. shock(t) is legacy's exogenous shock on energy consumption (row 2439: −20.8% in 2023, +9.2% in 2024, 0 after), switch Settings C19, on as legacy; the same factor multiplies power demand (section 3). The shadow price of feebates and of the output-based part of the ETS acts on the efficiency margin only.
- Electricity demand D_s is shown in the sector blocks as a memo. It is not part of the fuel totals; generation fuel use FU_k is.
- Qᵉ is the elasticity model (`enel`), Q the fuel use used everywhere else (`ener`): road fuels from the engineer model where TrModel = Engineer (section 4b), the residential fuels plus their leakage (section 4a).

## 4a. Residential leakage to biomass (switch BiomassLeakage; default off)

| Symbol | Meaning (source) |
|---|---|
| lk | leakage on: MTInputs `BiomassLeakage` (scenario 1) starts with "Yes" (setting) |
| m* | most-used cooking fuel of the country, overall sample (WHOCooking); only m* ∈ M = {natural gas, LPG, kerosene} leaks |
| e_m, e_b | cookstove efficiency of fuel m and of biomass (MTInputs NatGasEff, LPGEff, KerEff, BioEff, scenario 1) |
| σ | cross-price elasticity of biomass with respect to LPG (Elasticities C131, legacy row 360; 0.25) |
| ℓ | substitution lag (1 year, sheet Constants) |

For m ∈ M in the residential subsector (s = res), t > t₀ (all flows 0 in t₀):

```
E69a new policy in the price:  W_m(t) = N[m,res](t) · (1 + v_c(m,res))
E69b leaked share:             p_m(t) = 1[lk and m = m*] · min( (1 + (W_m(t) − W_m(t−1)) / P[m,res](t−1))^(σ e_b / e_m / ℓ) − 1, 1 )
E69c fossil change:            d_m(t) = − Q[m,res](t−1) · e_m · p_m(t)
E69d biomass replacing it:     b_m(t) = − d_m(t) · e_m / e_b                       (same useful energy)
E69e cumulative changes:       Lk[m,res](t) = Lk[m,res](t−1) + d_m(t),     Lk[bio,res](t) = Lk[bio,res](t−1) + Σ_m b_m(t)
```

- A rise in the new policy relative to last year's after-tax price moves a share of the most-used cooking fuel to biomass; a fall moves it back (p < 0). The share is capped at 1. With a flat policy after its start the share is 0, so the shift happens in the years the policy rises and then stays as a level shift (Lk is not grown with GDP).
- The fossil change is weighted by the fuel's cookstove efficiency (p is read as a share of useful energy), and biomass gains the same useful energy: e_m d_m + e_b Σ b = 0 each year.
- W_m is the new policy of the row itself (E26-E29), so an exempt fuel (E18a) does not leak.
- The change is computed on last year's actual use Q(t−1), which already includes earlier leakage; Qᵉ stays the elasticity model. Every product of the fuel follows Q: CO2, CH4, local pollutants, revenues, the price-block weights and the distribution module.
 Road transport, engineer model (switch TrModel; default off)

Classes c ∈ {passenger new, passenger used, freight, 2-3 wheeler}; powertrains i ∈ ICE fuels (gasoline, diesel, LPG, CNG/LNG), PHEV (passenger), BEV. Years up to the last data year Tᴰ take the data (Transport1); the equations below are for later years. Bugs fixed against legacy: `Transport_vs_Legacy_v7_0.md`.

| Symbol | Meaning (source) |
|---|---|
| N(t), y(t) | population; GDP per capita (section 9) |
| Sat_c, γ, λ, gmax, dmax | ownership saturation (data); Gompertz constants a_G, b_G; partial adjustment; maximum annual growth and decline of ownership (parameters) |
| L_c, own_c | vehicle lifetime; ownership period of the buyer (parameters) |
| s_used | used share of passenger purchases (data) |
| P_c,i | purchase price (Transport2) |
| τ_cu, τ_av, v | customs (× import share), ad-valorem tax, VAT on vehicles (data, policy rows) |
| fb, piv | feebate rate ($/t CO2) and pivot (g CO2/km); sub: EV subsidy ($/vehicle) |
| δ1, ins, m_c,i | first-year depreciation, insurance share, maintenance $/km (parameters) |
| r(y) | consumer discount rate, linear in GDP per capita between two income levels (parameters) |
| p_i, p_e | fuel price incl. new policies ($/liter; section 2); EV electricity price = power price of t−1 + mark-up |
| dt | distance tax ($/km, policy ramp) |
| RA_c | range anxiety ($/vehicle; Transport3, then falling with charging stations) |
| k_c | logit constant; η_own, η_cross: own and cross TCO elasticities of the ICE fuel split |
| ε_D, ε_E, ε_Y, α | driving, fuel-economy and distance-income elasticities; autonomous efficiency improvement |
| FE | fuel economy (km per liter; BEV km per kWh) |

```
T1  ownership target:  O*_c(t) = Sat_c · exp(a_G · exp(b_G · y(t))) · J_c,   J_c = O_c(Tᴰ) / O*_c,raw(Tᴰ)  (two-sided)
T2  ownership demand:  O_c(t) = λ O*_c(t) + (1 − λ) O_c(t−1),   bounded to [(1 − dmax) O_c(t−1), (1 + gmax) O_c(t−1)]
                       freight: O*_fre = O*_pass · share_fre(y);   2-3 wheelers: hump in y
T3  retirement:        Ret_c(t) = min(mean of the opening stock over min(L_c, t − t₀) years / L_c, opening)
T4  purchases:         S_c(t) = O_c(t) N(t) − (opening − Ret);   passenger new / used: (1 − s_used), s_used
T5  discounted km:     K_c = Σ_{τ=1..own_c} VKT_c / (1 + r)^τ
T6  price after taxes: Pt_c,i = P_c,i (1 + τ_cu)(1 + τ_av)(1 + v) + FB_c,i − sub_c·1[BEV]
                       FB_c,i = fb · (int_c,i − piv) · K_c / 10⁶      (int: g CO2/km; BEV 0)
T7  TCO per km:        TCO_c,i = [Pt (δ1 + annuity of (1 − δ1) over L_c − 1 years) − salvage
                                  + ins · Pt · annuity + m_c,i K_c + (p_i/FE_c,i + dt) K_c + RA_c·1[BEV]] / K_c
T8  EV choice:         sh_EV,c = e^(−k_c TCO_EV/T̄) / (e^(−k_c TCO_EV/T̄) + e^(−k_c TCO_ICE/T̄)),   T̄ = TCO weighted by last year's ICE share
T9  ICE fuel split:    sh_i(t) = sh_i(t−1) · (TCO_i(t)/TCO_i(t−1))^η_own · (TCŌ_−i(t)/TCŌ_−i(t−1))^η_cross,  rescaled to 1 − sh_EV
T10 new fuel economy:  FEⁿ_i(t) = FEⁿ_i(t−1) · ((p_i + fbl_i)(t)/(p_i + fbl_i)(t−1))^|ε_E| · (1 + α)     (fbl: feebate per liter)
T11 stock fuel economy: FEˢ(t) = FEⁿ(t) · φ + FEˢ(t−1) · (1 − φ),   φ = share of new vehicles in the stock
T12 distance:          VKT_c(t) = VKT_c(t−1) · (cost per km ratio)^ε_D · (y(t)/y(t−1))^ε_Y
T13 fuel use:          F_i = Σ_c Veh_c,i · VKT_c · f1_c / FEˢ_c,i           (bln liters or kWh)
T14 calibration:       f1_c = distance factor from Σ_i (energy balance_i / bottom-up_i)(t₀) weighted by fuel use;
                       Q_i(t) = F_i(t) / lpk_i · f2_i,   f2_i = Q_i(t₀) / (F_i(t₀)/lpk_i)     (lpk: liters per ktoe)
T15 buses:             bus fuel_i(t) = bus fuel_i(t₀) · Q_pass,i(t)/Q_pass,i(t₀);   electricity likewise
T16 switch:            Q[f,rod] = Q_f(engineer) if TrModel = Engineer, else E69 (f ∈ gasoline, diesel, LPG, gas, biofuels);
                       road electricity → power demand D_rod
T17 biofuels:          Q_bio = (Q_bgs + Q_obf)(t₀) · Q_gso/Q_gso(t₀) + Q_bdi(t₀) · Q_die/Q_die(t₀)   (legacy rows 5436-5438)
T18 feebate EF:        e_gso = EF_gso · Q_gso/(Q_gso + Q_bgs)(t₀),  e_die = EF_die · Q_die/(Q_die + Q_bdi)(t₀)   (E2146:E2147; I40)
```

- T1 calibrates both ways at the last data year (legacy only scaled up, at 2024: bug L27).
- T7: used vehicles are priced at the resale value of a new vehicle and the fuel economy of their production year; both used ICEVs and used BEVs depreciate over the same period (L38); PHEVs carry no range anxiety (L41).
- No circular reference: the EV electricity price is last year's power price, and GDP is that of section 9, which uses last year's GDP effect.

## 5. Revenues (USD million)

```
E71  existing taxes:        Rtx[f,s]  = θ Q[f,s] (X⁺_c + VAT_c + ΔXCP[f,s](1 + v_c)),   c = c(f,s)
E72  existing subsidies:    Rsub[f,s] = θ Q[f,s] X⁻_c                                    (negative)
E73  new policies:          Rnew[f,s] = θ Q[f,s] (N^ct + N^x + ρ N^ets + v_c N)
E74  existing carbon (memo):Rxcp[f,s] = θ Q[f,s] XCP[f,s]
E75  power:                 Rtx_pow  = Σ_k θ FU_k (X⁺ + VAT)_c(k) + Σ_k M G_k xc_k + Σ_u pp_u v_u/(1+v_u) cons_u
                            Rsub_pow = Σ_k θ FU_k X⁻_c(k) + Σ_u gap_u cons_u + Σ_k M G_k rns_k
                            Rnew_pow = Σ_k (M G_k pc_k − CO2_k A_pow (1 − ρ)) + Σ_u ((pc̄ π_u (1 − rb) + x_u) v_u − rb pc̄ π_u + x_u) cons_u
E76  totals:                Rnet = Rtx + Rsub;   Rmf = methane fee revenue (E84);   Rtot = Rnet + Rnew + Rmf;   ΔRtot vs scenario 1
```

Totals sum the subsectors, fuels and power. The ETS raises revenue at the permit price on the auctioned part only (ρ N^ets). Feebates are revenue-neutral.

## 6. CO2 emissions and the calibration factor

| Symbol | Meaning (source) |
|---|---|
| EF⁰[f,s], EF⁰_k | CO2 emission factors before calibration (IIASA) |
| CO2inv(Y) | energy CO2 of the GHG inventory in year Y |
| β_ets | convergence exponent of the ETS price proposal (0.5) |

```
E77  calibration factor:    φ_CO2 = CO2inv(Y) / CO2^(1)_uncal(Y)   if the calibration switch is on (default off), else 1
                            EF = φ_CO2 · EF⁰ for every subsector, fuel and generation type
E78  CO2:                   CO2[f,s] = θ Q[f,s] EF[f,s];   CO2_k (E68);   CO2 = Σ_{f,s} CO2[f,s] + Σ_k CO2_k
E79  ETS check:             CO2_e by ETS sector;   cov(t) = Σ_e CO2_e κ_e;   gap = cov/cap − 1
                            lr = ln(cap/bce) / ln(cov/bce)       (0 if cap ≤ 0, cap ≥ bce or cov ≥ bce)
                            p_next = p_E · lr^β_ets               (p̂ if p_E ≤ 0 or lr = 0)
```

- CO2^(1)_uncal(Y) is scenario-1 energy CO2 with uncalibrated factors. Scenario-1 fuel use does not depend on the factors, so the calibrated baseline equals the inventory in Y. The baseline CO2 of the ETS (CO2base_e) is scenario-1 CO2_e.

## 7. Non-CO2 GHGs and methane (Mt CO2e unless stated)

| Symbol | Meaning (source) |
|---|---|
| pop(t) | population (UN WPP) |
| inv_{cat,gas}(t) | GHG inventory by category and gas, while it has the year |
| e0, e1 | combustion CH4 factors, base year and final year EFEnd (GAINS, t/ktoe) |
| GWP_F, GWP_NF | GWP100 of fossil and non-fossil methane (IPCC AR6) |
| a_j, b_j, sh_j, φ_fl | methane abatement curve and input share by source j, flared share (CH4Inputs data) |
| ηY_cat, ηN_cat | elasticities of a non-energy category to GDP per capita and population |
| d_lu | LULUCF annual decline (share of the last inventory value) |

Methane sources j: oil and gas, downstream gas, coal mining, biomass (fossil, energy); livestock, rice (agriculture); waste.

```
E80  drivers:               pop.g = pop(t)/pop(t−1) − 1;   gpc = (1 + g)/(1 + pop.g) − 1
                            ψ(t) = CO2(t)/CO2^(1)(t) if non-energy mitigation = Yes, else 1
                            dr_cat(t) = (1 + gpc)^ηY_cat (1 + pop.g)^ηN_cat · ψ(t)/ψ(t−1)    (t₀: 1)
E81  combustion CH4 (kt):   CH4[f,s] = Q[f,s] (e0 + (e1 − e0) min(1, (t − t₀)/(EFEnd − t₀))) / 1000;   power: FU_k
E82  source activity:       Act_og = gas + oil production;  Act_cm = coal production  (base-year balance, held)
                            Act_dg = Q[gas];  Act_bm = Q[biomass]
                            Act_j(t) = Act_j(t−1)(1 + gpc)^ηY (1 + pop.g)^ηN   for livestock, rice, waste (t₀: 1)
E83  source shares:         fossil j: w_j = min(10 · Act_j(Y)/Σ_fossil Act(Y), sh_j),  share_j = w_j/Σ_fossil w
                            livestock, rice: share_j = sh_j;  waste: 1
E84  abatement, emissions:  abt_j = min(1, max(0, a_j (m · GWP_j)^b_j))
                            E_j = inv_cat(j),CH4(Y) · share_j · 1000/GWP_j        (kt CH4 of source j in Y)
                            CH4_j(t) = E_j · Act_j(t)/Act_j(Y) · (1 − abt_j)      (kt)
                            Rmf = m · (GWP_F Σ_fossil CH4_j + GWP_NF Σ_non-fossil CH4_j) / 1000   (USD m)
E85  energy GHGs:           CO2_enr = CO2 + r_fl · φ_fl · E_og · Act_og(t)/Act_og(Y) · abt_og / 1000   (flaring)
                            CH4_enr = k_CH4 · (Σ_{f,s,k} CH4 + Σ_fossil CH4_j) · GWP_F/1000
                            k_CH4 = inv_enr,CH4(Y) / [(Σ CH4 + Σ_fossil CH4_j) · GWP_F/1000]^(1)(Y)
E86  other categories:      inventory value while it exists, else (prev = last year's value):
                            energy N2O:            prev · CO2(t)/CO2(t−1);   energy F-gases, LULUCF non-CO2: prev
                            industrial processes:  prev · (1 + 1[scale with industry] · max(0, growth of industrial CO2))
                            agriculture, waste CH4: (Σ_{j∈cat} CH4_j) GWP_NF/1000
                            other gases of agriculture, waste, other: prev · dr_cat
                            LULUCF CO2:            prev if prev < 0, else prev · ψ(t)/ψ(t−1) − d_lu · |inv_LULUCF,CO2(Y)|
                            GHG = Σ over categories and gases excluding LULUCF;  GHG incl. LULUCF = GHG + LULUCF
```

- The flaring term burns the flared share of the abated oil and gas methane (r_fl = 44/16 t CO2 per t CH4).
- Shares, Act_j(Y) and k_CH4 come from scenario 1: the calibration is to the observed inventory.
- Fixes: non-energy methane grows and is abated (L18); flaring is CO2, not methane (L19); population from UN WPP (L20); each source uses its own curve (L21).

## 8. Local air pollutants (kt)

| Symbol | Meaning (source) |
|---|---|
| ap0, ap1 | emission factors of pollutant p (PM2.5, NOx, SO2, VOC, BC, OC, CO), base year and EFEnd (GAINS, t/ktoe) |
| GWP_p | GWP100 of pollutant p for the country's GAINS region |
| r_POM | primary organic matter per tonne of organic carbon (legacy constant) |

```
E87  weight:                w(t) = min(1, (t − t₀)/(EFEnd − t₀))
E88  emissions:             AP[p,s] = Σ_f Q[f,s] ((1 − w) ap0[f,s,p] + w ap1[f,s,p]) / 1000;   power: Σ over FU_k
E89  totals, forcing:       AP[p] = Σ_s AP[p,s] + AP[p,pow];   F_p = AP[p] GWP_p / 1000 (Mt CO2e, memo)
E90  module sectors:        coal and gas plants, other plants, road, ground level other, other, food & forestry (sum to AP[p])
                            POM = r_POM · OC;   other PM2.5 = max(0, PM2.5 − BC − POM)
```

Totals include navigation (fixes legacy bug L22) and services and food & forestry (fixes legacy bug L23).

## 9. GDP effects and feedback

| Symbol | Meaning (source) |
|---|---|
| g0(t), Y0(t) | baseline real GDP growth and real GDP (IMF WEO) |
| sh_i | revenue-use shares: labour tax cuts, corporate tax cuts, public investment, current spending, transfers (%) |
| m_i(k) | fiscal multiplier of instrument i at lag k = 0..19 (legacy MFMod medians; global or income group; base, low, high) |

```
E91  fiscal space:          fs(t) = (Rnew(t) − Rnew^(1)(t)) / Y0(t)            (share of GDP; both in USD m)
E92  impulse:               imp(t) = fs(t) − fs(t−1)                            (t₀: fs(t₀))
E93  effect of a use:       eff_i(t) = sh_i/100 · Σ_{k=0..19} imp(t−k) m_i(k);   the revenue itself: share −1, excise multipliers
E94  GDP effect:            ε_GDP(t) = Σ_i eff_i(t) · 1[endogenous GDP = Yes]
E95  feedback:              lvl(t) = 1 + ε_GDP(t−1)  (t₀: 1);   g(t) = (1 + g0(t)) · lvl(t)/lvl(t−1) − 1;   Y(t) = Y0(t) lvl(t)
```

- E95 raises the GDP level by the effect, one year later, instead of adding it to growth every year (fixes legacy bug L24). Scenario 1 has no fiscal space, so its g = g0.

Other deliberate differences from legacy CPAT are listed on the workbook sheet LegacyDiff and in `Formulas_v7_0.md` section B.

## Symbols → workbook variable codes

| Symbol | Meaning | Unit | Code |
|---|---|---|---|
| ι, δ | CPI and deflator indices | index | `infl`, `defl` |
| τ | carbon price | $/tCO2 | `cptraj` |
| F_c | fuel price reform | price unit | `fpr` |
| b_G | feebate rate | $/tCO2 | `fb` |
| on, κ_e | ETS on, effective ETS coverage | 0/1 | `ets.on`, `etsc` |
| B_G, ω_e | ETS benchmark, OBR share | share | `etsb`, `obr` |
| bce, chg, cap | baseline covered CO2, cap change, cap | MtCO2, share | `ets.bce`, `ets.chg`, `ets.cap` |
| V, σ̄ | volatility adjustment, semi-elasticity | factor | `ets.vadj`, `ets.se` |
| p̂, p_E, p̃_E, ρ | fast estimate, permit price, tax-equivalent price, revenue factor | $/tCO2 | `ets.est`, `ets.p`, `ets.pe`, `ets.rf` |
| T_e, A_e, Σ_e | carbon tax, ETS cost, shadow price by sector | $/tCO2 | `ctr`, `etr`, `shpx` |
| φ^ct, φ^ets, t* | existing carbon tax and ETS factors, data column of the year | factor | `xct.p`, `xets.p`, `xct.c` |
| m | methane fee | $/tCO2e | `mfee` |
| gp, Π_c | international price, reference price of c | source unit | `gp`, `gpi` |
| C_c, C̄_c | supply cost, fixed part | $/GJ | `sp`, `spf` |
| X̃_c, X_c, X⁺_c, X⁻_c | floating taxes, excise and other taxes, positive and negative parts | $/GJ | `txf`, `txo`, `etx`, `esub` |
| VAT_c, R_c | VAT payment, retail price before new policies | $/GJ | `vat`, `rpb` |
| N^ct, N^ets, N^x, N | new carbon tax, ETS cost, excise, total | $/GJ | `ctxnew`, `ets`, `ntx`, `nce` |
| XCP, ΔXCP | existing carbon pricing, change vs price data | $/GJ | `xcp`, `xcpd` |
| P, Sh | after-tax price, shadow price | $/GJ | `atp`, `shp` |
| cax, cāx, sto | capital cost, vintage averages | $/kW, $/kWh | `cax`, `caxav`, `stoav` |
| fix, lfx | amortised and levelised fixed cost | $/kWh | `fix`, `lfx` |
| fp, xc, vc, pc | fuel price, existing carbon, variable cost, new policy cost | $/GJ, $/kWh | `fpp`, `xck`, `vbc`, `ccp` |
| sh, reb, tvc, lvc, tic | shadow price, rebate, total and levelised variable cost, investment cost | $/kWh | `shk`, `reb`, `tvc`, `lvc`, `tic` |
| gc, gc̄, pc̄ | generation cost, average, average policy cost | $/kWh | `gnc`, `gncav`, `ccpav` |
| vre, cph, msc | VRE share, storage cost per hour, marginal storage cost | share, $/kWh | `vre`, `cph`, `msc` |
| sc_u, pp_u, p_u, gap_u | supply cost, price before policies, end-user price, subsidy gap | $/kWh | `sc`, `rppre`, `rp`, `sgap` |
| pd_d, M_d, D_s, D, cons_u | demand price, demand multiple, demand, total, consumption | $/kWh, ktoe, GWh | `pdem`, `mult`, `dem`, `demtot`, `cons` |
| Req, Rcg, Gmin, rem, λ | required generation, coal-gas need, minimum, remainder, logit weight | MWy | `req`, `reqcg`, `gmin`, `rem`, `lgd` |
| G_k, s_k, FU_k | generation, share, fuel use | MWy, share, ktoe | `gen`, `shr`, `pe` |
| K_k, Ke_k, Ret_k, Rete_k | capacity, effective capacity, retirement | MW | `cap`, `effcap`, `ret`, `reteff` |
| room, ec, Early | early coal retirement | MW, share | `egrow`, `ecshr`, `early` |
| need, Max_k, λi_k, I1_k, I2_k | investment need, scale-up limit, logit weight, rounds | MW | `need`, `maxinv`, `lgi`, `first`, `second` |
| I_k, Inv$_k, φ_k | nameplate investment, spending, share in stock | MW, USD m, share | `nim`, `usd`, `phi` |
| Qᵉ, Q | fuel use: elasticity model, used | ktoe | `enel`, `ener` |
| x | exemption factor (switch `AlwaysExemptResLPGKer`) | factor | `exf` |
| W, p, d, b | leakage: new policy in the price, leaked share, fossil change, biomass | $/GJ, share, ktoe | `lkt`, `lkp`, `lkd`, `lkb` |
| Lk | cumulative leakage added to fuel use (fossil, biomass; none) | ktoe | `lkc`, `lkcb`, `lkz`; net change `lks` |
| Rtx, Rsub, Rnew, Rxcp | revenue: existing taxes, subsidies, new policies, existing carbon | USD m | `rtx`, `rsub`, `rnew`, `rxcp` |
| power revenue terms | by type and user group | USD m | `prtx`, `prsub`, `prxc`, `prnew`, `prrns`, `rvat`, `rgap`, `rnvat`, `rreb`, `rpex` (`rexs`, `rexm`) |
| cf, ν, w, dlf, K(t₀) of the scenario | data of the scenario (A0) | share, years, MW | `cfu`, `nuu`, `wac`, `dlf`, `cap0`; `perm`, `start`, `rate`, `rr`, `erf` |
| p, Rs, rns, rb, x_e, x_m, x | PPA share, renewable subsidy, rebate switch, excises | share, $/kWh | `ppa`, `rnsp`, `rns`, `rbs`, `exs`, `entx`, `pex` |
| Gl, Gmax | dispatch before PPAs, maximum generation | MWy | `glg`, `gmx` |
| Rnet, Rmf, Rtot | net existing, methane fee, total revenue | USD m | `rnet`, `rmf`, `rtot` |
| CO2 | CO2 from fuel combustion | MtCO2 | `co2`, `co2.sec`, `co2.ets` |
| gap, lr, p_next | ETS cap check, next price | %, $/tCO2 | `co2.gap`, `ets.lr`, `ets.next` |
| pop, pop.g, gpc | population, growth, GDP per capita growth | thousand, % | `pop`, `pop.g`, `gdppc.g` |
| ψ, dr | non-energy effort, category growth factor | factor | `ghg.m`, `ghg.dr` |
| CH4[f,s], Act_j, abt_j, CH4_j | combustion CH4, source activity, abatement, emissions | kt CH4 | `ch4`, `ch4.act`, `ch4.abt`, `ch4.em` |
| k_CH4, GHG | energy CH4 calibration, GHG emissions | factor, Mt CO2e | `ghg.k`, `ghg`, `ghg.flr`, `ghg.inc` |
| w, AP, F_p | factor weight, pollutant emissions, forcing | kt, Mt CO2e | `ap.w`, `ap`, `aps`, `apf` |
| fs, imp, eff_i, ε_GDP | fiscal space, impulse, GDP effects | share of GDP | `fis.sp`, `fis.imp`, `fis.eff`, `gdp.eff` |
| lvl, g, Y | GDP level factor, growth, GDP after feedback | factor, %, USD bn | `gdp.lvl`, `gdp.pos.pct`, `gdp.pos.usd` |


## Initially exempt residential demand (v5.6, LegacyDiff 67)

With ExemptMostCook = Yes, the share s of the most-used cooking fuel spent by the bottom ExemptCookDeciles deciles (Settings C83: HHSurvey budget share x consumption per capita x weight) is initially exempt: its fuel use F_x(t) = F_x(t-1) x [enel(t)/enel(t-1)] x [p(t)/p(t-1)]^(e_U x (phase - 1)), phase = MIN(MAX((t + 1 - YearPha)/ExemptPhaseoutPeriod, 0), 1) if ExemptPhaseout (legacy rows 5568-5570, rule of 2259-2265, L94; income factor as the row, L48). Fuel use adds F_x - s x enel through section 6b (rows lkx, lkxa, lkc).
