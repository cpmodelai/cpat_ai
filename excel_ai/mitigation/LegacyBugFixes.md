# Legacy CPAT: bug fixes needed (CPAT-AI-Mitigation-Prototype v8.3)

Rebuilding the legacy CPAT mitigation sheet found these bugs in legacy CPAT itself. The prototype fixes or documents each of them; **legacy CPAT still needs the fixes** unless column "In legacy 465" says Fixed. File: `CPAT 1.0pre_465 - No Prop Data.xlsb` (the bugs were found in 456; rows moved to 465), sheet Mitigation unless stated. Generated from the register (`issues_register.py`) by `make_legacy_fixes.py`; the full register, with the check of each fix in 465, is `CPAT-AI_BugsAndIssues_latest.docx`.

**132 bugs: 9 high, 43 medium, 80 low priority.** High = changes the results of standard runs (Egypt); medium = changes results in some runs or countries, or a reported number; low = latent (no effect in the Egypt runs) or reporting only. (L17 turned out to be a bug of the prototype, not of legacy, and is not listed.)

| ID | Priority | In legacy 465 | Bug | Where in legacy | Fix | In the prototype |
|---|---|---|---|---|---|---|
| L1 | High | Fixed | Services electricity demand grows with the industrial multiple after 2023 | Mitigation H3, row 3731 | Use the services multiple in every year, as in 2023 and as the label of row 3713 says. | Fixed |
| L3 | High | Fixed | Income factor on the GDP elasticity applied twice and anchored to 2023 | Mitigation H1, rows 3692-3710 | eps_Y x inc(t): the income factor once, in the year of the calculation. | Fixed |
| L13 | High | Open | Other oil products: hardcoded pass-through 1 and margin 0 | Mitigation price block (other oil products) | Take pass-through and margin of other oil products from the IMF price dataset, like the other oil products. | Fixed |
| L18 | High | Open | Non-energy methane never changes | Mitigation rows 6158-6213 (livestock, rice, waste) | Grow livestock, rice and waste methane with their drivers (income, population) and apply the abatement shares already computed in rows 6168, 6180, 6192. | Fixed |
| L19 | High | Open | Flaring CO2 counted as methane | Mitigation rows 6141-6142 | Report the CO2 from flaring as CO2 in energy, not divided by the CH4 GWP in the CH4 row. | Fixed |
| L20 | High | Open | Population growth path | Mitigation rows 481, 2428 (macro drivers) | Use the UN WPP population of sheet UNPop (or fix the growth path). | Fixed |
| L24 | High | Open | GDP effect added to GDP growth every year | Mitigation rows 2443-2446, 8274 | Raise the GDP level by the effect: growth = (1 + g) x (1 + e(t-1)) / (1 + e(t-2)) - 1, not g + e. | Fixed |
| L53 | High | Fixed | Actual capacity factors are never used | Mitigation rows 2999-3007 N, Q, W | Search the installed capacity by FirstYearCalculations over all year columns (Power F:AC). | Fixed |
| L87 | High | Fixed with caveats | Regulations never act: share 0 and the adjustments unused | Mitigation C2371, F86:F90 (MTInputs rows 247-251) | Set the regulation share (C2371) to the scenario's adjustment of MTInputs rows 247-250 (F86:F89) and use row 251 for feebates. | Fixed |
| L2 | Medium | Fixed | Autonomous efficiency gains use the efficiency elasticity instead of the usage elasticity | Mitigation H1, rows 3691, 3697, 3703, 3709 | Documentation equation (3.4.2.3) and the fuel equation use (1 + eps_U): 1 / (1 + alpha)^(1 + eps_U), with eps_U the usage ("Demand Elasticity") row 3676. | Fixed |
| L5 | Medium | Fixed | Investment spending uses the capital cost at time factor 1 | Mitigation L20, rows 4276-4284 | Use the capital cost of the year (table A13), as the levelised and amortised costs do. | Fixed |
| L6 | Medium | Fixed | Investment logit normalised by the cheapest type, including types that may not be built | Mitigation L1/L4, rows 4046, 4073-4081 | Normalise by the cheapest permitted type, so that a type that cannot be built does not change the shares of those that can. | Fixed |
| L14 | Medium | Open | Pass-through applied twice in the first projected year | Mitigation txo rows (cs) | Apply (1 - pass-through) once in the first projected year. | Fixed |
| L15 | Medium | Open | ETS: hardcoded relative price 1.1 | Mitigation row 1843 | Use the volatility inputs of the ETS+LTS table instead of the fixed 1.1. | Fixed |
| L16 | Medium | Fixed with caveats | ETS quick estimate linear in the semi-elasticity | Mitigation row 1868 | Use the log form: price = LN(cap / baseline) / (semi-elasticity x effectiveness). | Fixed |
| L21 | Medium | Open | Waste abated with the livestock curve | Mitigation row 6192 | Use the waste curve of CH4Inputs for waste (row 6192 now = M6168, the livestock share). | Fixed |
| L22 | Medium | Open | Navigation missing from the local pollutant totals | Mitigation local pollutant totals (sections 13-14) | Add domestic navigation to the transport and total pollutant rows. | Fixed |
| L27 | Medium | Open | Road: vehicle ownership calibration only scales up (and uses 2024) | Mitigation rows H4787:J4787, H4903:J4903 (engineer road model, survey B3) | Actual/expected in both directions at the last data year found in the data. | Fixed (engineer road model) |
| L28 | Medium | Open | Road: freight-share cap and 2-3 wheeler peak use 2024 | Mitigation rows $N2168, J2169 (engineer road model, survey B3b) | Last data year. | Fixed (engineer road model) |
| L30 | Medium | Open | Road: bus fuel scaled by the wrong rows | Mitigation rows 5310-5314, 5318 (engineer road model, survey B6) | Passenger fuel use by fuel in ktoe (5195-5198) and passenger electricity (5223), base bus energy in ktoe. | Fixed (engineer road model) |
| L31 | Medium | Open | Road: bus share grossed up as x(1+share) | Mitigation rows O5171:O5173 (engineer road model, survey B6b) | /(1-bus share). | Fixed (engineer road model) |
| L33 | Medium | Open | Road: wrong elasticities and rows in freight and 2-3 wheeler distance | Mitigation rows M5261, M5295, M5232, M4646 (engineer road model, survey B8) | As the sibling rows. | Fixed (engineer road model) |
| L34 | Medium | Open | Road: freight discounted at the power-sector WACC | Mitigation rows K4329 (engineer road model, survey B8w) | The consumer discount rate (row 4531). | Fixed (engineer road model) |
| L35 | Medium | Open | Road: negative PHEV sales share | Mitigation rows 4850 L:O (engineer road model, survey B9) | (EV - BEV passenger share) x passenger share, ICE shares scaled to the rest. | Fixed (engineer road model) |
| L37 | Medium | Open | Road: new BEV maintenance at the ICEV rate | Mitigation rows 4573 (engineer road model, survey B19) | EV maintenance (J4328). | Fixed (engineer road model) |
| L38 | Medium | Open | Road: used ICEV and BEV depreciation over different periods | Mitigation rows 4598 (engineer road model, survey B20) | Used ownership period - 1 (J4323-1) for both. | Fixed (engineer road model) |
| L42 | Medium | Fixed | Domestic aviation: GDP growth and shock swapped | Mitigation rows 5483-5492 | Use the standard form: (1 + g)^(eps_Y x income factor) x (1 + shock), the shock once, jet fuel with its own (oil) income elasticity. | Fixed |
| L43 | Medium | Open | Other energy use: no GDP growth | Mitigation rows 6063-6071 | Point the income factor to row 2433 and add the additional-efficiency term. | Fixed |
| L49 | Medium | Open | Balance of payments: oil without the share traded | Mitigation rows 18162-18166, 742 | Multiply the oil change in use by the share traded of row 742, as for gas and coal. | Fixed |
| L52 | Medium | Fixed | Renewables take the world power parameters, never the country ones | Mitigation rows 2981-2985 P:T | Swap the branches of the ISERROR test (take the country value where it exists). | Fixed |
| L54 | Medium | Fixed | Hydro investment always starts in the first year | Mitigation row 4067 H | Test the hydro generation share (row 3846), not the year header. | Fixed |
| L57 | Medium | Fixed | New ETS: the quick price estimate is linear in the semi-elasticity | Mitigation ETS block (quick estimate, override row) | Estimate the ETS price in log form, LN(cap / baseline) / (semi-elasticity x effectiveness). | Fixed |
| L58 | Medium | Open | Local pollutants: subsectors without a GAINS match get zero factors | Mitigation rows 15885-16685 (GAINS factor lookups) | Map subsectors without a GAINS match to the nearest GAINS subsector (services as residential, rail as road, industry as manufacturing). | Fixed |
| L59 | Medium | Open | Local pollutants and combustion CH4: fuels without a GAINS factor emit nothing | Mitigation rows 15885-16685 (GAINS factor lookups; sheet EF_PM) | Give a fuel without a GAINS factor the nearest GAINS match (LPG: natural gas of the same subsector; food & forestry: construction; else manufacturing). | Fixed |
| L67 | Medium | Fixed | Power: capacity bought for this year's demand, although it comes online next year | Mitigation rows 4022-4031 (K7) | Size the investment need on next year's demand (row 4027), as its label says, estimated as this year's demand x (1 + growth from last year to this year): reading next year's demand itself would make the workbook circular through the GDP feedback once a revenue reads fuel use (the methane fee). | Fixed |
| L68 | Medium | Open | GDP effects: the multiplier of lag 1 acts in the impulse year | Mitigation rows 8253-8274 (policy 14569-14590) | Apply multiplier(t - s) to the impulse of year s (lag 0 in the impulse year), as the multiplier notes define the lags. | Fixed |
| L77 | Medium | Open | Average prices: index rows point at the wrong rows, gas test on the policy total | Mitigation rows 16302, 16374-16390 | Point rows 16383-16390 to the average-price rows of each fuel; test the baseline gas total in E16302; relabel "baseline = 100". | Fixed |
| L79 | Medium | Open | ETS: industry and transport priced as a whole when one subsector is covered | Mitigation rows 2322-2325 (policy 8638-8641), 7775-7778 | Price and charge the ETS by subsector coverage, not MAX over the sector. | Fixed |
| L83 | Medium | Fixed | Electricity producer subsidy compounds the factor and lags a year | Mitigation rows 3592, 3601, 3630 | Project as base value x the factor of the year (J x O2213). | Fixed |
| L88 | Medium | Fixed | Regulations never reach power | Mitigation rows 3398 ff. | Add the regulation shadow price to the power shadow price (rows 3398 ff.). | Fixed |
| L98 | Medium | Fixed | Feebate inclusion of industry reads the ETS industry flag | Manual inputs P54:X54 (name FeebateInclusion -> MTInputs E66:E82) | Use =AND(Dashboard!$K$44,P53) in P54:X54. | Fixed |
| L99 | Medium | Fixed | ETS inclusion of machinery and other manufacturing uses the buildings flag | Manual inputs S11, U11 (name ETSInclusion) | Read Dashboard R30 in S11 and U11. | Fixed |
| L105 | Medium | Fixed | Dashboard industry feebate rates are lost | MTInputs E56:E64 (Dashboard H46:K47) | Transpose H46:K46 and H47:K47. | Fixed |
| L108 | Medium | Fixed | Cost of renewable subsidies counts the base subsidy twice, ignores the hydro switch and omits biomass | Mitigation rows 7883-7889 (policy +6316) | Rows 7883-7887 = the subsidy by type (rows 3148-3152) x generation. | Fixed |
| L112 | Medium | Fixed | Policy copies of the shadow-price rows read the baseline carbon price in the regulation term | Mitigation rows 8693-8704 (policy copies of 2377-2388) | In rows 8693-8704 refer to the policy block ($D$8685, L$8691) instead of $D$2369 and L$2375. | Fixed |
| L115 | Medium | Fixed with caveats | Residential gas: current ETS price reads the LPG transport row | Mitigation row 2555 (policy 8871) | Point row 2555 (and policy 8871) at the residential gas ETS row 1715. | Fixed |
| L118 | Medium | Fixed | Manual power investment: the need net of manual investment is never used | Mitigation row 4108 | Size the logit investment on row 4108 (need after manual investment), not row 4028. | Fixed |
| L119 | Medium | Open | NDC year adjustment applied twice for BAU targets and never for Fixed or Historical | Mitigation rows 18399, 18407-18412, 18426-18428, 18443-18445 | Drop the adjustment, or apply it once and to all types (compare in the target year). | Fixed |
| L122 | Medium | Open | Intensity NDC incl. LULUCF adds a blank cell instead of LULUCF emissions | Mitigation rows 18461-18462 | Add I18450 (LULUCF) instead of J18450 (non-CO2). | Fixed |
| L123 | Medium | Open | Intensity NDC: reference-year GDP read from a fixed cell | Mitigation row 18451 | None: not reproduced in the .xlsb (G470 already reads the reference year). | Fixed |
| L126 | Medium | Fixed | Power: fuel price for power averages later years | Mitigation rows 3155-3163 (A18) | Average the fuel prices over t-4 .. t (rows 3155-3163): L3155 =IF(...,L3072,AVERAGE($L3072:L3072)) for L:O, P3155 =IF(...,P3072,AVERAGE(L3072:P3072)) for P:AE. | Fixed |
| L129 | Medium | Open | Baseline renewable subsidy counted twice | Mitigation rows 2785-2788, 2947-2951, 7883-7886 (against 2743, 2745) | In rows 2785-2788, 2947-2951 and 7883-7886 drop the + L2743 term (L2745 already includes it); policy rows the same (+6,316). | Fixed |
| L4 | Low | Fixed | Long-term storage cost allocation (33%) applied twice | Mitigation J1, rows 3911 and 3912 | Apply the 33% allocation once. | Fixed |
| L7 | Low | Fixed | Early coal retirement mixes nameplate and effective capacity | Mitigation K4, row 3973 | Subtract effective retirements. | Fixed |
| L8 | Low | Fixed | Effective coal retirement is not capped like the nameplate retirement | Mitigation K5/K6, rows 3994, 4009-4011 | Effective retirement = nameplate retirement x capacity factor. | Fixed |
| L9 | Low | Fixed | Feebate rebate per kWh consumed is added to the cost per kWh generated | Mitigation D6, rows 3407-3409 | Rebate per kWh generated, so the feebate is revenue-neutral at base-year shares. | Fixed |
| L10 | Low | Fixed | Capacity needed is computed from last year's plan, not from actual capacity | Mitigation K7, row 4024 | Use the actual effective capacity of the year (capacity x capacity factor). | Fixed |
| L11 | Low | Fixed | Stray reference in dispatch | Mitigation rows 3773, 3779 (I1) | Remove the $G4291 x total term (or point it to the intended cell). | Not built |
| L12 | Low | Fixed | Total nameplate investment row is zero | Mitigation row 4273 (L19) | Sum the nine generation types instead of multiplying by $X3008. | Fixed |
| L23 | Low | Open | Services and food & forestry missing from the pollutant totals | Mitigation rows 6690, 6792, ... (total emissions of each pollutant) | Add services and food & forestry to the total of each pollutant. | Fixed |
| L25 | Low | Open | Road: distance tax and 2-3 wheeler EV subsidy apply in the baseline | Mitigation rows 4451, 4720 (engineer road model, survey B1) | Scenario number > 1. | Fixed (engineer road model) |
| L26 | Low | Open | Road: freight and 2-3 wheeler income growth read coal subsidies from 2038 | Mitigation rows 4487 AB:AE (also 4501) (engineer road model, survey B2) | Lagged GDP growth (row 2446) in all years. | Fixed (engineer road model) |
| L29 | Low | Open | Road: ownership of cars and trucks cannot fall | Mitigation rows T4328, U4328 (engineer road model, survey B4) | Allow a decrease of up to own_decline_fix a year (legacy 2-3 wheeler value, 10%). | Fixed (engineer road model) |
| L32 | Low | Open | Road: industry emission factors for road diesel and LPG | Mitigation rows G4376-G4378, G4419-G4421 (engineer road model, survey B7) | Road EFs. | Fixed (engineer road model) |
| L36 | Low | Open | Road: charging-station subsidy ramp | Mitigation rows 4343 (engineer road model, survey B10) | 0 before the start year, linear to the target level, then constant. | Fixed (engineer road model) |
| L39 | Low | Open | Road: freight distance output omits LPG and LNG trucks | Mitigation rows 5267 (engineer road model, survey B21) | All fuels. | Fixed (engineer road model) |
| L40 | Low | Open | Road: wrong rows in average gas and EV fuel economy | Mitigation rows 5368, 5373 (engineer road model, survey B22) | Right rows. | Fixed (engineer road model) |
| L41 | Low | Open | Road: PHEVs carry the full BEV range anxiety | Mitigation rows 4555 (engineer road model, survey B23) | No range anxiety for PHEVs (they refuel with gasoline). | Fixed (engineer road model) |
| L44 | Low | Fixed | Residential other oil products priced at the biomass price | Mitigation row 5559 | Read the other-oil-products price (row 5548). | Fixed |
| L45 | Low | Fixed with caveats | Residential leakage to biomass inconsistent | Mitigation rows 5574-5593 | Subtract the fossil change once, use the kerosene rows for kerosene, conserve the substituted energy. | Fixed |
| L46 | Low | Fixed | Road other biofuels: wrong price and terms | Mitigation row 5406 | Use the biofuel price, the shadow price through eps_F, the efficiency term and the road efficiency row. | Not built |
| L47 | Low | Fixed | Self-generated renewables in aviation and navigation take the shock from wrong rows | Mitigation rows 5491, 5516 | Use the shock row 2439. | Not built |
| L48 | Low | Fixed | Residential initially-exempt rows: no income factor; starred "Yes*" exemption test | Mitigation rows 5546-5547, 5568-5570 | Apply the income factor, start from the exempt share, and match the starred defaults. | Not built |
| L50 | Low | Open | Balance of payments: current account #NAME?, column lag, sign | Mitigation rows 18180-18198 | Read the WEO current account (BCA), drop the one-column lag and check the sign of policy net imports. | Fixed |
| L51 | Low | Open | Energy trade balance of coal valued at the oil price | Mitigation row 743 | Value the coal trade balance at the coal price (row 732), not the oil price (row 731). | Fixed |
| L55 | Low | Fixed | China, Japan and Korea take regional power data | Mitigation rows 2977-2985 K (Power A25:A356) | Search the country block (Power rows 110-294) before the regional block. | Fixed |
| L56 | Low | Fixed with caveats | Countries without CoC risk data get Sri Lanka's WACC parameters | CoC rows 202-390 D:V | Flag countries without CoC fixed data instead of using Sri Lanka. | Fixed |
| L60 | Low | Open | VAT payment on oil products divided by the full VAT rate | Mitigation rows 2595, 2618, 2641, 2664 (VAT payment) | VAT payment = (supply cost + taxes) x VAT rate x household share. | Fixed |
| L61 | Low | Fixed | EU ETS price grows with the carbon-tax growth | Mitigation row 1695 (from the column after the last data year) | Grow the EU ETS price with ExistingETSGrowth. | Fixed |
| L62 | Low | Not fixed (marked fixed) | Existing carbon tax on transport diesel, LPG and kerosene uses the rate row as coverage | Mitigation rows 1760-1762 | Take the fuel coverage row, and the single-price flag, for transport diesel, LPG and kerosene. | Fixed |
| L63 | Low | Not fixed (marked fixed) | Existing carbon tax fuel coverage: lookup range cut short | Mitigation J1741-J1749 (ECP!E133:E403) | Look the fuel coverage up in the whole ECP block (to row 425). | Fixed |
| L64 | Low | Fixed | No existing ETS on other oil products outside power | Mitigation rows 1711-1723 | Apply the industry ETS coverage to other oil products outside power. | Fixed |
| L65 | Low | Fixed | Carbon tax complementary to an existing ETS: last year's ETS coverage | Mitigation rows 2270-2288 | Use the ETS coverage of the year for the complementary carbon tax. | Fixed |
| L66 | Low | Open | Other energy use: no additional policy efficiency gains on fossil fuels | Mitigation rows of other energy use (fossil fuels; renewables use $M2201) | Add the industrial additional efficiency to the fossil rows of other energy use. | Fixed |
| L69 | Low | Open | GDP effects: the first cohort's excise drag is lost | Mitigation row 8057 (policy 14373) | Match the first cohort's excise use on its own row (L14372, baseline L8056), not L$8113. | Fixed |
| L70 | Low | Open | Revenue: industry gas excise uses the coal rate and coal use | Mitigation row 7747 (policy 14063) | Use the gas industry excise rate (row 2581) and gas industry use in row 7747. | Fixed |
| L71 | Low | Open | Revenue: biomass taxes, subsidies and VAT divided by the unit conversion | Mitigation rows 7791, 7805, 7859 | Multiply by _conv_ktoe_to_gj in rows 7791, 7805, 7859. | Fixed |
| L72 | Low | Open | Revenue: next-year references | Mitigation rows 7657, 7742 | Read column R (the year) in rows 7657 and 7742. | Fixed |
| L73 | Low | Open | Revenue: wrong coverage shares | Mitigation rows 7677 (policy 13993), 7704 | Divide by the industry gas total (6428) in row 7677; use power x kerosene coverage (R2265 x R2270) in row 7704. | Fixed |
| L75 | Low | Open | Revenue reports: hard-coded row and mixed totals | Mitigation rows 17145-17149, 17175, 17186 | Index the excise report by the matched row instead of 759; take electricity from rev.new in the revenue by fuel report. | Fixed |
| L76 | Low | Open | Multipliers: empty CIT table, WAGE on the GNFS table, approximate country match, default to Estimated | Multipliers rows 19-22, 38-45, 1624-1822 | Point CIT to the labour-tax or an own table (or the income group), WAGE to its own table, MATCH the country exactly (0), default unknown text to the income group. | Fixed |
| L78 | Low | Fixed | ETS: auctioned share drops to 0 after the target year unless "Constant" | Mitigation row 1863 (MTInputs row 92) | Hold the target auctioned share after the target year whatever the continuation (or offer a defined alternative). | Fixed |
| L80 | Low | Fixed | ETS: the carbon-tax trajectory rescaled when the ETS is on | Mitigation rows 2191, 2251 | Leave the carbon-tax trajectory unscaled when the ETS applies (drop E2191 from row 2251). | Fixed |
| L81 | Low | Open | Consumer subsidy phase-out: the fixed subsidy takes last year's factor | Mitigation rows 2460, 2483, 2506, ... 2598, ... 2713 (fixed portion of subsidy, each price block) | Use the factor of the same column in the fixed-subsidy rows (Q2214 for Q). | Fixed |
| L82 | Low | Open | Residential gas producer subsidy reads the oil row | Mitigation row 2547 | Point row 2547 to row 826 (gas producer subsidy). | Fixed |
| L84 | Low | Fixed with caveats | Electricity consumer subsidy phased with the price-control factor; option text mismatch | Mitigation rows 3606, 3635; MTInputs row 138 | Phase the electricity consumer subsidy with the consumer factor (row 2214); one option text. | Not built |
| L85 | Low | Open | Electricity consumer subsidy info row subtracts industry | Mitigation row 7806 | Add the industry part: -(MIN(0, res) + MIN(0, ind)). | Fixed |
| L86 | Low | Fixed | No manual override for the electricity producer subsidy | Mitigation I828 | Give the electricity producer subsidy a manual-input row. | Not built |
| L89 | Low | Fixed | Coal in road, residential and services reads the residential coal shadow price | Mitigation rows 5396, 5553, 5634 | Read the shadow price of the row's own sector for coal. | Fixed |
| L90 | Low | Fixed | Residential leakage breaks the useful-energy balance | Mitigation row 5593 | Drop $C5593* in row 5593 (biomass gain = -sum of the equivalents). | Fixed |
| L91 | Low | Fixed | Exempt residential fuel still leaks to biomass | Mitigation rows 5580, 5586 (against 5546-5547) | Compute the leakage price change from the residential after-tax price (the row's own new policy). | Fixed |
| L92 | Low | Open | ExemptMostCook never reaches Mitigation | Mitigation I1784, K1795, rows 5568-5570 | I1784 = IF(LEFT(H1784,3)="Yes",1,0); start rows 5568-5570 from L(total) x K1795. | Not built |
| L93 | Low | Fixed | Fuel coverage rows test text labels and contain #REF! | Mitigation rows 2259-2268 (column E) | Use the sector rule IF(D2369=1,IF(OR(C2173=4,C2173=9),"Yes","No"),...) in rows 2259-2268. | Not built |
| L94 | Low | Open | Exemption phase-in rules differ between rows | Mitigation rows 2259-2265, 2270-2288 against 2266-2268, 5568-5570 | One rule: MAX(MIN((t+1-YearPha)/ExemptPhaseoutPeriod,1),0) x ExemptPhaseout. | Not built |
| L95 | Low | Fixed with caveats | Power demand: efficiency increment sits on the net-exports row | Mitigation row 3719 (D3719 = D3742 'Net Exports (Imports negative)', F:J net-export data egy.mit.nxp.ecy; L3719 'Additional Efficiency Improvements - Power demand', M3719 = M2198 = MTInputs F242); read as $M3719 in rows 3691, 3697, 3703, 3709 | Put the efficiency increment on its own labelled row (or read M2198 directly); leave row 3719 to net exports. | Fixed |
| L96 | Low | Open | Fuel-use block: mislabelled parameter and fuel rows | Mitigation C2199:C2201 ('Tax in nominal or real terms?', 'Exponential option or linear' twice) beside K2199:M2201 (road, residential, industrial additional efficiency, MTInputs F243-F245); E2385 (LPG 'Road'), E2386 (kerosene 'Industry') on all-sector rows (codes shp.lpg.all, shp.ker.all); D5615, D5711, D6058, D6069 'Other oil pinducts' | Give the additional-efficiency increments their own labelled rows; label the LPG and kerosene shadow-price rows 'All'; correct the typo. | Fixed |
| L97 | Low | Open | Iron & steel memo rows unused; one reads next year's growth | Mitigation rows 5667-5676, 5703, 5727-5728 (iron & steel block; M5667 = N2446) | Delete the memo rows (or move them to a diagnostics area with the year's own growth M2446). | Not built |
| L100 | Low | Fixed | Manual domestic prices: the electricity rows are never read | Manual inputs G59:N146 (names _manual_prices, _manual_codes) | Extend both names to row 146. | Fixed |
| L101 | Low | Open | Manual services income elasticities read the industries column | Elasticities F51:F58 (Manual inputs rows 279-286) | Read N279:N286 in F51:F58. | Fixed |
| L102 | Low | Fixed | Manual non-energy elasticities can never take effect | Manual inputs K326:K327; Mitigation K366:M367 | Type the inputs and read them directly. | Fixed |
| L103 | Low | Open | Manual SCC reads a path typed on Mitigation, not the Manual inputs block | Manual inputs rows 234-240; Mitigation row 17668 | Mitigation row 17668 = 'Manual inputs'!J237 (NSCC) / J240 (GSCC). | Fixed |
| L104 | Low | Open | Name CH4Feebate points to an empty cell | Manual inputs J217 (name CH4Feebate) | Delete the name or point it at the methane fee input. | Fixed |
| L106 | Low | Fixed | Manual inputs memo swaps the renewables and electricity price elasticities | Manual inputs K315:N316 | Use rows 297 and 298 respectively. | Fixed |
| L107 | Low | Fixed | Renewable subsidy: start year of the additional subsidy reuses the consumer-subsidy phase-out year | Mitigation E2736 (policy E9052) = row 270 = MTInputs F132 (YearConsSubPha) | Add an MTInputs row (and Dashboard cell) for the start year of the additional RE subsidy and point E2736 at it. | Fixed |
| L109 | Low | Fixed with caveats | Capex decline options Low and Vhigh have no wind and solar series | Mitigation rows 3038-3046; Power rows 303-330 | Add the Low and Vhigh series to the Power tab, or map the options to the old series. | Fixed |
| L110 | Low | Fixed | Power revenue rebate counts VAT that was never collected | Mitigation rows 3615, 3644, 3663, 7874, 7735 (policy +6316 / +6316) | Use the carbon cost before VAT in the rebate, or count the VAT on the policy term in the VAT revenue. | Fixed |
| L111 | Low | Fixed | Manual electricity excise revenue counts the whole excise, also where the price does not include it | Mitigation rows 3602, 3631, 3660, 7871, 7748 | Compute row 3660 from the excise in the price. | Fixed |
| L113 | Low | Fixed | Power switches tested for the exact "Yes" (was issue I58) | Mitigation G261 (PowerRebates), row 3150 (RenewableSubsidyHydro), F201 (AdditionalExcise) | Test LEFT(switch,3)="Yes" in G261, row 3150 and F201, so Yes and Yes* both count as Yes. | Fixed |
| L114 | Low | Open | Renewable subsidies: nominal inputs used as real (was issue I55) | Mitigation rows 2734-2735, 2743, 2745 (MTInputs 352-353) | Deflate the nominal inputs (rows 2734-2735) by the CPI index before they enter row 2743, or relabel MTInputs 352-353 as real. | Fixed |
| L116 | Low | Open | Services gasoline and diesel income elasticities: step-change column reads the wrong rows | Elasticities H53, H54 | Point H53 and H54 at rows 169 and 170. | Not built |
| L117 | Low | Open | Transfers multiplier (TRNS): estimated lag-0 table read two rows off | Multipliers D44 | Read D$1220:D$1418 in D44, as E44:O44. | Fixed |
| L120 | Low | Open | NDC index rows: unconditional and conditional ratios inverted against the average | Mitigation rows 18482-18484 | Use target / start-year emissions in rows 18482-18483, as 18484. | Fixed |
| L121 | Low | Open | Historical NDC: the target "level" is the emissions cut | Mitigation rows 18443-18445 | Return F18437 - F18440 x adj (the level), as the Fixed block. | Fixed |
| L124 | Low | Fixed | Producer subsidy: the residential gas block reads the oil subsidy | Mitigation row 2547 (N2547) | Read N$826 (gas) in row 2547, as the other gas blocks (same cells as the L82 plan). | Fixed |
| L125 | Low | Fixed | Producer subsidy: other oil products add a per-liter value to a per-barrel price | Mitigation row 2685 (N2685) | Multiply by liters per barrel in row 2685. | Fixed |
| L127 | Low | Open | Power: levelised variable cost reads the variable cost to 2041 | Mitigation rows 3439-3447 (D9) | Keep the levelised variable cost (rows 3439-3447) on input-driven costs only; if an ETS price becomes endogenous, levelise the announced price path instead of the solved one. | Fixed |
| L128 | Low | Fixed | Net revenue report rows read the next year | Mitigation rows 6238, 6243 (policy 12554, 12559) | K6238 =K8024 and K6243 =K8029, filled K:AD; policy rows 12554, 12559 the same (+6,316). | Fixed |
| L130 | Low | Open | Intensity NDC: conditional and unconditional rows use different base years | Mitigation rows 18455-18456 | F18456: apply the cut to the reference-year intensity F18453, as F18455 does. | Fixed |
| L131 | Low | Open | Codes: one output code on rows with different contents | Mitigation rows 466, 2442, 16170 (gdp.pre.lvl); 7722, 7742, 7985 (sub.new.usd); 7638-13962 (rev.ctr.coa) | Give each row its own code (e.g. gdp.pre.ln, gdp.pre.mn; sub.new.usd only on its own subtotal). | Fixed |
| L132 | Low | Open | Codes: capitals and empty tokens | Mitigation rows 7606, 13922 (oc.tot.); em.pm2.All.<sector> rows | Write the codes in lower case and with a scenario number: em.pm2.all.<sector>, nox.tot.<n>. | Fixed |
| L133 | Low | Open | Codes: nox.tot holds N2O, oc.tot. holds NOx | Mitigation rows 7606, 13922 and the GHG total rows (nox.tot) | Rename the N2O total n2o.tot and the NOx forcing row nox.tot. | Fixed |
| L134 | Low | Open | Price-increase units: other oil products "$/bbn", default "$/liter" for other oil products and biomass | MTInputs rows 182-183 (columns E and G); Mitigation I177, I180 | Label the price-increase units USD/bbl (other oil products) and USD/GJ (biomass) in columns E and G of MTInputs rows 182-183. | Fixed |

## Details

**L1 (High; in legacy 465: fixed). Services electricity demand grows with the industrial multiple after 2023.** Mitigation H3, row 3731.

- Legacy: The 2023 formula multiplies services demand by the services multiple (row 3713); from 2024 the copied formula points six rows up, to the industrial multiple (row 3707). Services have a higher GDP elasticity (1.1 against 0.8) and a different price elasticity.
- Fix: Use the services multiple in every year, as in 2023 and as the label of row 3713 says.
- Effect: Services are about a quarter of Egypt's electricity demand, so this is the largest single effect.

**L3 (High; in legacy 465: fixed). Income factor on the GDP elasticity applied twice and anchored to 2023.** Mitigation H1, rows 3692-3710.

- Legacy: GDP term = (1 + g)^((eps_Y / $M3686) x M3686 x M2433). Row 3686 already holds the average elasticity x the income factor (row 2433), and $M fixes the denominator to 2023, so the effective elasticity is eps_Y x inc(t)^2 / inc(2023).
- Fix: eps_Y x inc(t): the income factor once, in the year of the calculation.
- Effect: The income factor falls from 1.03 to 0.95 by 2040, so the error grows over time.

**L13 (High; in legacy 465: open). Other oil products: hardcoded pass-through 1 and margin 0.** Mitigation price block (other oil products).

- Legacy: With the hardcodes the retail price of other oil products falls with the oil price to the 0.01 floor and their fuel use rises tenfold by 2030 (Egypt).
- Fix: Take pass-through and margin of other oil products from the IMF price dataset, like the other oil products.
- Effect: Retail price falls to the 0.01 floor with the oil price; fuel use rises tenfold by 2030 (Egypt). prototype: Changed in the prototype (v0.10, user decision): pass-through and margin from the IMF dataset like the other oil products (LegacyDiff).

**L18 (High; in legacy 465: open). Non-energy methane never changes.** Mitigation rows 6158-6213 (livestock, rice, waste).

- Legacy: Livestock, rice and waste CH4 are the inventory values divided by the GWP, constant over time; the abatement shares of the methane fee are computed (rows 6168, 6180, 6192) but not applied, so a methane fee on agriculture and waste has no effect.
- Fix: Grow livestock, rice and waste methane with their drivers (income, population) and apply the abatement shares already computed in rows 6168, 6180, 6192.
- Effect: Non-energy methane is flat and a methane fee on agriculture and waste has no effect. prototype: Fixed in v2.8: the sources grow with income and population and the fee abates them along their curves (Methods, chapter Emissions).

**L19 (High; in legacy 465: open). Flaring CO2 counted as methane.** Mitigation rows 6141-6142.

- Legacy: The CO2 from flaring the abated oil and gas methane is divided by the CH4 GWP and added to the CH4 row.
- Fix: Report the CO2 from flaring as CO2 in energy, not divided by the CH4 GWP in the CH4 row.
- Effect: Methane overstated and CO2 understated when the fee abates oil and gas methane. prototype: Fixed in v2.8: reported as CO2 in energy (row ghg.flr).

**L20 (High; in legacy 465: open). Population growth path.** Mitigation rows 481, 2428 (macro drivers).

- Legacy: Population growth is 2% a year from 2027 and 3-4% from 2031, so Egypt reaches 185 million in 2041 against 147 million in the legacy sheet UNPop; it drives the agriculture, waste and other GHGs.
- Fix: Use the UN WPP population of sheet UNPop (or fix the growth path).
- Effect: Egypt reaches 185 million in 2041 instead of 147 million; agriculture, waste and other GHGs too high after 2030. prototype: Fixed in v2.8: population from UNPop (UN WPP).

**L24 (High; in legacy 465: open). GDP effect added to GDP growth every year.** Mitigation rows 2443-2446, 8274.

- Legacy: The fiscal multipliers give the change of the GDP level; legacy adds that change to the growth rate every year, so a steady effect of 0.5% raises growth by 0.5 points a year and compounds (about +10% of GDP after 20 years instead of +0.5%). No effect on the NoPropData values (the GDP effect rows are stripped to 0).
- Fix: Raise the GDP level by the effect: growth = (1 + g) x (1 + e(t-1)) / (1 + e(t-2)) - 1, not g + e.
- Effect: A steady effect of 0.5% compounds to about +10% of GDP after 20 years, in every run with endogenous GDP effects (the NoPropData file strips these rows). prototype: Fixed in v3.1: the GDP level is raised by the effect (growth from the ratio of level factors).

**L53 (High; in legacy 465: fixed). Actual capacity factors are never used.** Mitigation rows 2999-3007 N, Q, W.

- Legacy: The installed-capacity lookup searches the years 2000-2019 (Power F:Y) for 2022 (column AB), so it is #N/A, the actual capacity factor is 0 and the studies value is always used; the CFOverride bounds never act.
- Fix: Search the installed capacity by FirstYearCalculations over all year columns (Power F:AC).
- Effect: Power: actual capacity factors where data exist (Egypt: all types with capacity), base capacities change. prototype: Fixed in v4.10: installed capacity of the base year from Power rows 358-1635 (all year columns); the actual capacity factor (output / capacity) is used inside the CFOverride bounds, else the studies value (Egypt: gas 0.385, wind 0.436, solar 0.347, hydro 0.592; base-year gas capacity 52 GW instead of 35).

**L87 (High; in legacy 465: fixed with caveats). Regulations never act: share 0 and the adjustments unused.** Mitigation C2371, F86:F90 (MTInputs rows 247-251).

- Legacy: The share of the regulation shadow price on the efficiency margin, C2371 = IFNA(INDEX($F$86:$F$90, MATCH(C2370,$C$86:$C$90,0)),0), is 0: C86:C90 hold " - " plus the scenario name, so the MATCH never hits (v5.5: text read from the .xlsb; the LibreOffice conversion had shown IFNA(0)). The efficiency adjustments of MTInputs rows 247-251 are read into F86:F90 but referenced nowhere: the regulation scenarios (energy efficiency, vehicle fuel economy, residential, industrial) change no fuel use or vehicle choice.
- Fix: Set the regulation share (C2371) to the scenario's adjustment of MTInputs rows 247-250 (F86:F89) and use row 251 for feebates.
- Effect: Regulation scenarios have no effect at all. prototype: Fixed (v4.16): regulation shadow price = shadow carbon price x the scenario's adjustment x sector coverage.

**L2 (Medium; in legacy 465: fixed). Autonomous efficiency gains use the efficiency elasticity instead of the usage elasticity.** Mitigation H1, rows 3691, 3697, 3703, 3709.

- Legacy: Efficiency multiple = 1 / (1 + alpha)^(1 + eps_F), with eps_F the "Price Elasticity" row 3677.
- Fix: Documentation equation (3.4.2.3) and the fuel equation use (1 + eps_U): 1 / (1 + alpha)^(1 + eps_U), with eps_U the usage ("Demand Elasticity") row 3676.
- Effect: Efficiency gains reduce demand slightly too much every year.

**L5 (Medium; in legacy 465: fixed). Investment spending uses the capital cost at time factor 1.** Mitigation L20, rows 4276-4284.

- Legacy: New investment (USD m) = nameplate MW x the capital cost column O of table A2, which is the cost before the capital-cost time factor.
- Fix: Use the capital cost of the year (table A13), as the levelised and amortised costs do.
- Effect: Investment spending on solar is overstated by up to 80% (2040, time factor 0.55), wind by up to 9%; it is reporting only (the investment decision uses the right cost).

**L6 (Medium; in legacy 465: fixed). Investment logit normalised by the cheapest type, including types that may not be built.** Mitigation L1/L4, rows 4046, 4073-4081.

- Legacy: The logit weight is EXP(-K x cost / cheapest cost), and the cheapest cost is taken over all nine types, including types whose new investment is not permitted (coal, nuclear, other renewables, biomass for Egypt).
- Fix: Normalise by the cheapest permitted type, so that a type that cannot be built does not change the shares of those that can.
- Effect: No effect in the Egypt baseline; in the carbon-tax run nuclear (not permitted) is the cheapest type from 2024, which makes the investment logit steeper.

**L14 (Medium; in legacy 465: open). Pass-through applied twice in the first projected year.** Mitigation txo rows (cs).

- Legacy: With pass-through 0.5 or 0.8 the floating tax multiplies its last value by (1 - pass-through) a second time, so taxes jump in the first projected year.
- Fix: Apply (1 - pass-through) once in the first projected year.
- Effect: Taxes jump in the first projected year when pass-through is between 0 and 1 (none for Egypt: 0 or 1). prototype: Fixed in v4.10 (user rule: bugs are never replicated): the floating part is (1 - pass-through) x (last tax + fall in supply cost), applied once (txf; Methods, chapter Prices A10); no effect for Egypt (pass-through 0 or 1).

**L15 (Medium; in legacy 465: open). ETS: hardcoded relative price 1.1.** Mitigation row 1843.

- Legacy: The ETS price effectiveness uses a fixed 1.1 instead of the volatility inputs of the ETS+LTS table.
- Fix: Use the volatility inputs of the ETS+LTS table instead of the fixed 1.1.
- Effect: The ETS price effectiveness ignores the volatility inputs. prototype: Replaced in the prototype by the volatility adjustment (v1.02); suggested to the legacy team (TODO).

**L16 (Medium; in legacy 465: fixed with caveats). ETS quick estimate linear in the semi-elasticity.** Mitigation row 1868.

- Legacy: The fast estimate divides the reduction by the semi-elasticity (linear); the legacy note says "arguably exp/ln".
- Fix: Use the log form: price = LN(cap / baseline) / (semi-elasticity x effectiveness).
- Effect: The fast ETS price estimate is off for large cuts, so the goal seek starts far from the answer. prototype: prototype uses the log form LN(cap / baseline) / (semi-elasticity x effectiveness x volatility adjustment) (v1.02).

**L21 (Medium; in legacy 465: open). Waste abated with the livestock curve.** Mitigation row 6192.

- Legacy: The abatement share of waste equals that of livestock (=M6168) instead of the waste curve of CH4Inputs.
- Fix: Use the waste curve of CH4Inputs for waste (row 6192 now = M6168, the livestock share).
- Effect: Waste methane is abated as if it were livestock. prototype: Fixed in v2.8: every source uses its own curve.

**L22 (Medium; in legacy 465: open). Navigation missing from the local pollutant totals.** Mitigation local pollutant totals (sections 13-14).

- Legacy: The transport and total pollutant rows sum road, rail and aviation but leave out domestic navigation.
- Fix: Add domestic navigation to the transport and total pollutant rows.
- Effect: Pollutant totals miss navigation. prototype: Fixed in v2.9: navigation included (section 15).

**L27 (Medium; in legacy 465: open). Road: vehicle ownership calibration only scales up (and uses 2024).** Mitigation rows H4787:J4787, H4903:J4903 (engineer road model, survey B3).

- Legacy: Ownership calibration MAX(1, actual/expected) at 2024 (column N).
- Fix: Actual/expected in both directions at the last data year found in the data.
- Effect: Egypt engineer baseline 2035: gasoline -33.9%, diesel -37.9%, road electricity -52.4%, passenger EV sales share -2.6 points. prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L28 (Medium; in legacy 465: open). Road: freight-share cap and 2-3 wheeler peak use 2024.** Mitigation rows $N2168, J2169 (engineer road model, survey B3b).

- Legacy: Freight-share cap and 2-3 wheeler peak read 2024 (column N).
- Fix: Last data year.
- Effect: Egypt engineer baseline 2035: gasoline +0.0%, diesel +0.0%, road electricity -0.6%, passenger EV sales share -0.1 points. prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L30 (Medium; in legacy 465: open). Road: bus fuel scaled by the wrong rows.** Mitigation rows 5310-5314, 5318 (engineer road model, survey B6).

- Legacy: Bus fuel scaled by the wrong rows (LPG, gas and PHEV distance, BEV vehicles) and bus electricity from a sum of liters and kWh.
- Fix: Passenger fuel use by fuel in ktoe (5195-5198) and passenger electricity (5223), base bus energy in ktoe.
- Effect: Egypt engineer baseline 2035: gasoline +0.0%, diesel -0.3%, road electricity -16.8%, passenger EV sales share +0.0 points. prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L31 (Medium; in legacy 465: open). Road: bus share grossed up as x(1+share).** Mitigation rows O5171:O5173 (engineer road model, survey B6b).

- Legacy: Bus share added to the bottom-up fuel use as x(1+bus share).
- Fix: /(1-bus share).
- Effect: Egypt engineer baseline 2035: gasoline -0.0%, diesel +0.0%, road electricity -0.3%, passenger EV sales share +0.0 points. prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L33 (Medium; in legacy 465: open). Road: wrong elasticities and rows in freight and 2-3 wheeler distance.** Mitigation rows M5261, M5295, M5232, M4646 (engineer road model, survey B8).

- Legacy: BEV freight distance uses the 2-3 wheeler income elasticity; BEV 2-3 wheeler distance uses the cost ratio twice and no income term; LPG freight base row; freight ICE depreciation switches to the passenger discount rate from 2023.
- Fix: As the sibling rows.
- Effect: Egypt engineer baseline 2035: gasoline -0.0%, diesel -0.2%, road electricity +4.0%, passenger EV sales share +0.0 points. prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L34 (Medium; in legacy 465: open). Road: freight discounted at the power-sector WACC.** Mitigation rows K4329 (engineer road model, survey B8w).

- Legacy: Freight discounted at the average power-sector WACC.
- Fix: The consumer discount rate (row 4531).
- Effect: Egypt engineer baseline 2035: gasoline +0.0%, diesel +0.2%, road electricity -1.0%, passenger EV sales share -0.0 points. prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L35 (Medium; in legacy 465: open). Road: negative PHEV sales share.** Mitigation rows 4850 L:O (engineer road model, survey B9).

- Legacy: PHEV sales share = passenger EV share - blended passenger/light BEV share (negative).
- Fix: (EV - BEV passenger share) x passenger share, ICE shares scaled to the rest.
- Effect: Egypt engineer baseline 2035: gasoline -0.0%, diesel +0.1%, road electricity +0.2%, passenger EV sales share +0.0 points. prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L37 (Medium; in legacy 465: open). Road: new BEV maintenance at the ICEV rate.** Mitigation rows 4573 (engineer road model, survey B19).

- Legacy: New BEV maintenance uses the ICEV maintenance cost (J4327).
- Fix: EV maintenance (J4328).
- Effect: Egypt engineer baseline 2035: gasoline -0.1%, diesel -0.0%, road electricity +1.2%, passenger EV sales share +0.5 points. prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L38 (Medium; in legacy 465: open). Road: used ICEV and BEV depreciation over different periods.** Mitigation rows 4598 (engineer road model, survey B20).

- Legacy: Used ICEV depreciation annuity over own_years-1 (6) years, used BEV over 12.
- Fix: Used ownership period - 1 (J4323-1) for both.
- Effect: Egypt engineer baseline 2035: gasoline +5.1%, diesel +3.1%, road electricity -50.7%, passenger EV sales share -10.0 points. prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L42 (Medium; in legacy 465: fixed). Domestic aviation: GDP growth and shock swapped.** Mitigation rows 5483-5492.

- Legacy: GDP growth enters with elasticity 1 while the shock carries eps_Y x income factor; coal and gas get the shock twice; jet fuel takes the diesel income elasticity.
- Fix: Use the standard form: (1 + g)^(eps_Y x income factor) x (1 + shock), the shock once, jet fuel with its own (oil) income elasticity.
- Effect: Jet fuel x0.87 (2023) to x1.07 (2040) against the standard form. prototype: Fixed in v3.11: jet fuel in the prototype with the standard form (shock once) and the transport oil income elasticity.

**L43 (Medium; in legacy 465: open). Other energy use: no GDP growth.** Mitigation rows 6063-6071.

- Legacy: The income factor points to the blank row 2440, so other energy use never grows with GDP; rows 6063-6070 have no additional-efficiency term.
- Fix: Point the income factor to row 2433 and add the additional-efficiency term.
- Effect: Other energy use flat with GDP: about -46 ktoe (2030) and -124 ktoe (2040) for Egypt. prototype: Fixed in the prototype: other energy use grows with GDP (oil, industry elasticities).

**L49 (Medium; in legacy 465: open). Balance of payments: oil without the share traded.** Mitigation rows 18162-18166, 742.

- Legacy: The value of the change in net imports of oil is the change in use x the price, while gas (and coal) apply the share traded of rows 741-743 (oil products 0.47), so the oil effect is about twice too large (Egypt 2030: 3.2 bn USD).
- Fix: Multiply the oil change in use by the share traded of row 742, as for gas and coal.
- Effect: Reported balance of payments only: the oil effect is about twice too large (Egypt 2030: 3.2 bn USD). prototype: Fixed in v3.16: every fuel group applies its share (section 16b).

**L52 (Medium; in legacy 465: fixed). Renewables take the world power parameters, never the country ones.** Mitigation rows 2981-2985 P:T.

- Legacy: The fallback IF(ISERROR(country), country, IF(ISERROR(world), ...)) is inverted, so wind, solar, hydro, other renewables and biomass always take the world efficiency, fixed and variable O&M, WACC and lifetime (Egypt: solar fixed O&M 15 instead of the country 11.831 $/kW/y).
- Fix: Swap the branches of the ISERROR test (take the country value where it exists).
- Effect: Power: solar fixed O&M of Egypt 11.831 instead of 15 $/kW/y (other renewables: no country data). prototype: Fixed in v4.10: every type takes the country value where it exists, else the world value (Egypt: solar fixed O&M 11.831 $/kW/y).

**L54 (Medium; in legacy 465: fixed). Hydro investment always starts in the first year.** Mitigation row 4067 H.

- Legacy: IF($L$3827>50%, FirstYearCalculations, NewInvHydYear) tests a year header (2022 > 0.5) instead of a share, so hydro can invest from 2022 instead of 2030.
- Fix: Test the hydro generation share (row 3846), not the year header.
- Effect: Power: hydro investment from NewInvHydYear (2030) unless hydro is above 50%. prototype: Fixed in v4.10: the base year only when the hydro generation share is above HydInvShare (50%), else NewInvHydYear (Egypt: 2030).

**L57 (Medium; in legacy 465: fixed). New ETS: the quick price estimate is linear in the semi-elasticity.** Mitigation ETS block (quick estimate, override row).

- Legacy: The cap is a relative change of covered emissions, which respond log-linearly to the price; the linear quick estimate misses the cap (legacy note: "arguably exp/ln") and leaves it to the VBA goal seek.
- Fix: Estimate the ETS price in log form, LN(cap / baseline) / (semi-elasticity x effectiveness).
- Effect: New ETS scenarios: the quick estimate meets the cap (legacy relies on the VBA goal seek). prototype: Fixed (v1.02; bug by user decision 2026-10-18, was LegacyDiff row 6): the fast estimate in log form, LN(cap / baseline) / (semi-elasticity x effectiveness x volatility adjustment); the build stores it (no goal seek).

**L58 (Medium; in legacy 465: open). Local pollutants: subsectors without a GAINS match get zero factors.** Mitigation rows 15885-16685 (GAINS factor lookups).

- Legacy: The GAINS factors are looked up by subsector; services, rail, industry and other energy use have no GAINS match and silently get 0, although they burn fuel.
- Fix: Map subsectors without a GAINS match to the nearest GAINS subsector (services as residential, rail as road, industry as manufacturing).
- Effect: Local pollutants of services, rail and industry no longer zero. prototype: Fixed (v2.9; bug by user decision 2026-10-18, was issue I27 and LegacyDiff row 49): each subsector takes the GAINS subsector of its CH4 factor (services as residential, rail as road, industry as manufacturing).

**L59 (Medium; in legacy 465: open). Local pollutants and combustion CH4: fuels without a GAINS factor emit nothing.** Mitigation rows 15885-16685 (GAINS factor lookups; sheet EF_PM).

- Legacy: A fuel that its GAINS subsector has no factor for gets 0, although it burns: Egypt 2022 residential LPG (3,182 ktoe), other mining diesel (3,819), food & forestry diesel (927), fuel transformation LPG (2,466); food & forestry shows about 1 t of NOx (legacy row 15924).
- Fix: Give a fuel without a GAINS factor the nearest GAINS match (LPG: natural gas of the same subsector; food & forestry: construction; else manufacturing).
- Effect: Egypt 2022: NOx +11%, PM2.5 +5%, combustion CH4 +20%. prototype: Fixed (v4.12; bug by user decision 2026-10-18, was issue I35): the nearest GAINS match (LPG: natural gas of the same GAINS subsector; food & forestry: construction, off-road machinery; biomass: residential; else manufacturing). A fuel the subsector has factors for keeps a missing pollutant at 0 (GAINS omits zero factors).

**L67 (Medium; in legacy 465: fixed). Power: capacity bought for this year's demand, although it comes online next year.** Mitigation rows 4022-4031 (K7).

- Legacy: New capacity bought in a year produces from the next year, but the investment need is sized on this year's demand: row 4027 is labelled "Next Year Demand" and row 4031 "Actual effective generation in next year (should be the same)", yet row 4027 reads this year's demand. The system enters every year one year of demand growth short (Egypt about 4% a year), and existing plants, mostly gas, run harder to cover it.
- Fix: Size the investment need on next year's demand (row 4027), as its label says, estimated as this year's demand x (1 + growth from last year to this year): reading next year's demand itself would make the workbook circular through the GDP feedback once a revenue reads fuel use (the methane fee).
- Effect: Egypt (legacy inputs, v6.2 estimate): capacity 77.9 GW in 2030 and 109.6 GW in 2040 against legacy 75.2 and 107.3 (next year read directly: 77.3, 109.5); the need follows the 2023-2024 demand shock (4.3 GW in 2024, 0 in 2025). prototype: Fixed (v4.14; bug by user decision 2026-10-18, was issue I8). v6.2 (user 2026-10-20): next year's required generation is estimated as this year's x (1 + growth from last year to this year), so neither legacy nor the prototype reads a later year and the GDP feedback (last year's effect) cannot loop; legacy kept as a switch in power_model_ref only.

**L68 (Medium; in legacy 465: open). GDP effects: the multiplier of lag 1 acts in the impulse year.** Mitigation rows 8253-8274 (policy 14569-14590).

- Legacy: The effect in year t sums impulse(s) x multiplier(t - s + 1): an impulse already gets the lag-1 multiplier in its own year, although the multiplier notes (Manual inputs D269, Multipliers) define lag 1 as one year after implementation. The GDP effect runs one year early.
- Fix: Apply multiplier(t - s) to the impulse of year s (lag 0 in the impulse year), as the multiplier notes define the lags.
- Effect: The GDP effect of every impulse comes one year early. prototype: Fixed (v4.15): lag 0 in the impulse year (multiplier 0), lag 1 the year after.

**L77 (Medium; in legacy 465: open). Average prices: index rows point at the wrong rows, gas test on the policy total.** Mitigation rows 16302, 16374-16390.

- Legacy: The "indexed vs 2022" rows read rows 16316-16323 (electricity industry, electricity residential, coal industry, ...) under the labels electricity, coal, gas, oil, ...; E16302 tests the policy gas total instead of the baseline one; labels say 2022 = 100 where baseline = 100.
- Fix: Point rows 16383-16390 to the average-price rows of each fuel; test the baseline gas total in E16302; relabel "baseline = 100".
- Effect: The reported price indices are of the wrong fuels. prototype: Fixed (v4.15): pav.leg and pav.lidx per fuel against scenario 1.

**L79 (Medium; in legacy 465: open). ETS: industry and transport priced as a whole when one subsector is covered.** Mitigation rows 2322-2325 (policy 8638-8641), 7775-7778.

- Legacy: The auctioned price of industry and transport takes MAX over the subsector coverage flags, and the revenue is charged on the whole sector's CO2: uncovered subsectors pay, while the price estimate counts covered subsectors only.
- Fix: Price and charge the ETS by subsector coverage, not MAX over the sector.
- Effect: Uncovered industry and transport subsectors pay the permit price; revenue on the whole sector's CO2. prototype: Fixed: coverage, price and revenue by subsector (etsc, v1.07).

**L83 (Medium; in legacy 465: fixed). Electricity producer subsidy compounds the factor and lags a year.** Mitigation rows 3592, 3601, 3630.

- Legacy: The projection is the previous value x the previous factor (N3601 x N2213), so the factors multiply year on year and lag.
- Fix: Project as base value x the factor of the year (J x O2213).
- Effect: Electricity producer subsidies fall too fast (compounding) and a year late. prototype: Fixed (v4.16): base value x the factor of the year (fiscal line rpsu; the electricity price effect waits for the power features).

**L88 (Medium; in legacy 465: fixed). Regulations never reach power.** Mitigation rows 3398 ff..

- Legacy: The power shadow price reads the feebate and ETS rows (2354) only, though the energy efficiency regulation scenario covers power.
- Fix: Add the regulation shadow price to the power shadow price (rows 3398 ff.).
- Effect: Economy-wide regulations skip power. prototype: Fixed (v4.16): shpx.pow includes reg.pow.

**L98 (Medium; in legacy 465: fixed). Feebate inclusion of industry reads the ETS industry flag.** Manual inputs P54:X54 (name FeebateInclusion -> MTInputs E66:E82).

- Legacy: P54:X54 = AND(Dashboard!$R$30, P53): the ETS industry flag, not the feebate flag K44.
- Fix: Use =AND(Dashboard!$K$44,P53) in P54:X54.
- Effect: Industry feebate coverage follows the ETS switch on the Dashboard. prototype: Not applicable in the prototype (feebate coverage typed per scenario, MTInputs rows 66-82).

**L99 (Medium; in legacy 465: fixed). ETS inclusion of machinery and other manufacturing uses the buildings flag.** Manual inputs S11, U11 (name ETSInclusion).

- Legacy: S11 and U11 read Dashboard Q30 (buildings) while mch, irn, nfm, cem read R30 (industry).
- Fix: Read Dashboard R30 in S11 and U11.
- Effect: Machinery and other manufacturing join the ETS with buildings, not industry. prototype: Not applicable in the prototype (ETS coverage typed per scenario, MTInputs rows 99-115).

**L105 (Medium; in legacy 465: fixed). Dashboard industry feebate rates are lost.** MTInputs E56:E64 (Dashboard H46:K47).

- Legacy: E56:E58 and E61:E63 transpose Dashboard H46:J46 and H47:J47; E59 and E64 (industry) are empty, so the Dashboard industry feebate rates K46 / K47 never reach MTInputs.
- Fix: Transpose H46:K46 and H47:K47.
- Effect: Industry feebate rates set on the Dashboard have no effect. prototype: Not applicable in the prototype (feebate rates typed per scenario on MTInputs).

**L108 (Medium; in legacy 465: fixed). Cost of renewable subsidies counts the base subsidy twice, ignores the hydro switch and omits biomass.** Mitigation rows 7883-7889 (policy +6316).

- Legacy: Rows 7883-7886 = (row 2743 + row 2745) x generation, but row 2745 already equals row 2743 minus the additional subsidy, so the base subsidy enters twice; hydro (7885) ignores RenewableSubsidyHydro; biomass has no row; 7889 enters total revenue (row 8009).
- Fix: Rows 7883-7887 = the subsidy by type (rows 3148-3152) x generation.
- Effect: Wrong total revenue whenever a renewable subsidy is set. prototype: Fixed (v5.4): revenue = subsidy x generation by type (row prrns), hydro by its switch, biomass included; in rsub.pow and rpol.ren.

**L112 (Medium; in legacy 465: fixed). Policy copies of the shadow-price rows read the baseline carbon price in the regulation term.** Mitigation rows 8693-8704 (policy copies of 2377-2388).

- Legacy: The policy copies keep $D$2369 and L$2375 (absolute rows of the baseline block), so their regulation term reads the baseline carbon price (0) instead of the policy run's; once L87 is fixed, regulations still do nothing in the policy run. Found by the v5.5 cell plans (text read from the .xlsb); to confirm in Excel.
- Fix: In rows 8693-8704 refer to the policy block ($D$8685, L$8691) instead of $D$2369 and L$2375.
- Effect: Regulations have no effect in the policy run even after the L87 fix. prototype: Not replicated: the prototype's regulation shadow price is per scenario group (reg rows, v4.16).

**L115 (Medium; in legacy 465: fixed with caveats). Residential gas: current ETS price reads the LPG transport row.** Mitigation row 2555 (policy 8871).

- Legacy: Row 2555 (nga res, current ETS permit price) = K$1720 (LPG, transport/industry) instead of K$1715 (natural gas, residential); the other blocks read their own row. Found 2026-10-19 while planning L64/L65.
- Fix: Point row 2555 (and policy 8871) at the residential gas ETS row 1715.
- Effect: Residential gas price carries the LPG permit price wherever an existing ETS covers either fuel. prototype: Fixed by design: the prototype reads the existing ETS price by fuel and sector (section 2).

**L118 (Medium; in legacy 465: fixed). Manual power investment: the need net of manual investment is never used.** Mitigation row 4108.

- Legacy: Row 4108 (needed effective investment after manual investment) is computed but the logit investment (rows 4110-4118) reads row 4028, so logit investment comes on top of the manual one (over-investment). Found by the power plan survey (item 8).
- Fix: Size the logit investment on row 4108 (need after manual investment), not row 4028.
- Effect: Over-investment whenever a type is set to Manual: logit investment comes on top of the manual capacity path. prototype: Fixed (v5.6, P3): rows needm, first and deficit use the need net of manual investment.

**L119 (Medium; in legacy 465: open). NDC year adjustment applied twice for BAU targets and never for Fixed or Historical.** Mitigation rows 18399, 18407-18412, 18426-18428, 18443-18445.

- Legacy: F18399 = IF(target year < 2030, (2030 - base)/(target year - base), 1) is at least 1, so the "<1" branches of the Fixed and Historical blocks (rows 18426-18428, 18443-18445) never run, while the BAU block multiplies both the reduction (18407) and the level (18410: BAU x (1 - reduction x adj) x adj) by it: a 2025 BAU target is scaled up twice and the other types not at all. Found by the item 8 plan (v5.7).
- Fix: Drop the adjustment, or apply it once and to all types (compare in the target year).
- Effect: BAU targets before 2030 scaled twice; Fixed and Historical never adjusted. prototype: Fixed (v5.7, NDC comparison 14c): the prototype compares every NDC in its own target year (each year is modelled), so no adjustment is needed.

**L122 (Medium; in legacy 465: open). Intensity NDC incl. LULUCF adds a blank cell instead of LULUCF emissions.** Mitigation rows 18461-18462.

- Legacy: The excludes-LULUCF branch adds $J$18450 where the LULUCF emissions are in column I (I18450 = G - F). J18450 is not blank: it holds the non-CO2 emissions (F - H, 254.9 Mt for Egypt), so non-CO2 is counted twice and LULUCF is missed (cell plan 2026-10-20 corrected the register). Found by the item 8 plan (v5.7).
- Fix: Add I18450 (LULUCF) instead of J18450 (non-CO2).
- Effect: Intensity targets incl. LULUCF count non-CO2 twice and miss LULUCF. prototype: Fixed (v5.7, NDC comparison 14c): the reduction is computed on the NDC basis and applied to the BAU incl. LULUCF, as for the other types.

**L123 (Medium; in legacy 465: open). Intensity NDC: reference-year GDP read from a fixed cell.** Mitigation row 18451.

- Legacy: Not reproduced in the .xlsb (cell plan 2026-10-20): G469 = _NDC_Year, so G470 is the WEO real GDP of the reference year and F18466 = G470 is right; the fixed-cell reading came from the LibreOffice conversion. Only gap: reference years before 2000 find no GDP (#VALUE! or N/A; the prototype also gives N/A). Kept for the record. Found by the item 8 plan (v5.7).
- Fix: None: not reproduced in the .xlsb (G470 already reads the reference year).
- Effect: None. prototype: Fixed (v5.7, NDC comparison 14c): ndc.gdp.ref looks the reference year up (WEO real GDP; N/A when the year is not in the data).

**L126 (Medium; in legacy 465: fixed). Power: fuel price for power averages later years.** Mitigation rows 3155-3163 (A18).

- Legacy: The fuel price for power is a centred 5-year average, AVERAGE(t-2 .. t+2) of the fuel prices (rows 3072-3080), so this year's power costs read the next two years. Safe only while those prices depend on inputs alone: any quantity-dependent price (an endogenous ETS price, a supply-cost feedback) closes a circular reference through the GDP feedback. Found by the circular-reference review (v6.2, user 2026-10-20).
- Fix: Average the fuel prices over t-4 .. t (rows 3155-3163): L3155 =IF(...,L3072,AVERAGE($L3072:L3072)) for L:O, P3155 =IF(...,P3072,AVERAGE(L3072:P3072)) for P:AE.
- Effect: Power costs read the next two years' prices: a circular reference as soon as a price depends on quantities. prototype: Fixed (v6.2): trailing average t-4 .. t (fpp over the row fpn; AVERAGEIFS on the year row keeps the scenario's own years). Price changes reach power costs about two years later than in legacy.

**L129 (Medium; in legacy 465: open). Baseline renewable subsidy counted twice.** Mitigation rows 2785-2788, 2947-2951, 7883-7886 (against 2743, 2745).

- Legacy: The rows add L2743 + L2745, but L2745 already includes L2743, so the baseline renewable subsidy is counted twice. Only when MTInputs row 352 (RenewableSubsidyBL) is not zero; 0 for Egypt. Found by the cell plans (user 2026-10-20: a bug).
- Fix: In rows 2785-2788, 2947-2951 and 7883-7886 drop the + L2743 term (L2745 already includes it); policy rows the same (+6,316).
- Effect: With a baseline renewable subsidy (MTInputs 352) the subsidy cost is counted twice. prototype: Fixed (prototype: one renewable subsidy row rnsp = baseline + additional, counted once).

**L4 (Low; in legacy 465: fixed). Long-term storage cost allocation (33%) applied twice.** Mitigation J1, rows 3911 and 3912.

- Legacy: Row 3911 multiplies the long-term storage cost by the allocation share; row 3912 multiplies it again.
- Fix: Apply the 33% allocation once.
- Effect: No effect for Egypt (variable renewables stay below the 75% threshold); it matters for high-renewable scenarios.

**L7 (Low; in legacy 465: fixed). Early coal retirement mixes nameplate and effective capacity.** Mitigation K4, row 3973.

- Legacy: The room for early coal retirement subtracts last year's non-coal retirements in nameplate MW from additions and demand growth in effective MW.
- Fix: Subtract effective retirements.
- Effect: Latent for Egypt (no coal). Too little early coal retirement where solar (low capacity factor) retires.

**L8 (Low; in legacy 465: fixed). Effective coal retirement is not capped like the nameplate retirement.** Mitigation K5/K6, rows 3994, 4009-4011.

- Legacy: Nameplate coal retirement is MIN(planned + early, capacity); the effective retirement uses planned + early without the cap.
- Fix: Effective retirement = nameplate retirement x capacity factor.
- Effect: Latent for Egypt. Where early retirement is large, capacity needed is overstated.

**L9 (Low; in legacy 465: fixed). Feebate rebate per kWh consumed is added to the cost per kWh generated.** Mitigation D6, rows 3407-3409.

- Legacy: The rebate is the average feebate per kWh generated divided by consumption/generation (x 1.22), and is then added to the cost per kWh generated of every type.
- Fix: Rebate per kWh generated, so the feebate is revenue-neutral at base-year shares.
- Effect: Latent for Egypt (no power feebate in the runs). Over-rebates by 22% when a power feebate is set.

**L10 (Low; in legacy 465: fixed). Capacity needed is computed from last year's plan, not from actual capacity.** Mitigation K7, row 4024.

- Legacy: Effective capacity before retirements = last year's planned capacity (capacity after retirements + investment needed), whether or not the investment could be placed.
- Fix: Use the actual effective capacity of the year (capacity x capacity factor).
- Effect: Latent: it only matters when scale-up limits leave a deficit; then the model under-invests next year too.

**L11 (Low; in legacy 465: fixed). Stray reference in dispatch.** Mitigation rows 3773, 3779 (I1).

- Legacy: Required generation from coal and gas is MAX(required - other generation, $G4291 x total); G4291 is an unrelated, empty cell of table L21.
- Fix: Remove the $G4291 x total term (or point it to the intended cell).
- Effect: None while G4291 stays empty; wrong dispatch if anything is typed there. prototype: Harmless while the cell is empty; not built in the prototype.

**L12 (Low; in legacy 465: fixed). Total nameplate investment row is zero.** Mitigation row 4273 (L19).

- Legacy: The total multiplies by $X3008, an empty cell, instead of summing the types.
- Fix: Sum the nine generation types instead of multiplying by $X3008.
- Effect: Reported total investment is 0. prototype: Reporting only; the prototype sums.

**L23 (Low; in legacy 465: open). Services and food & forestry missing from the pollutant totals.** Mitigation rows 6690, 6792, ... (total emissions of each pollutant).

- Legacy: The total of each pollutant sums power, transport, residential, industry and other energy use but leaves out services and food & forestry, which the air-pollution sectors (ground level other, food & forestry) include. No effect on the legacy Egypt values (services and food & forestry emit zero there: legacy total = sum of its sectors), but it matters wherever they emit.
- Fix: Add services and food & forestry to the total of each pollutant.
- Effect: None for Egypt (they emit zero there); totals too low wherever they emit. prototype: Fixed in v3.0: totals = all subsectors + power.

**L25 (Low; in legacy 465: open). Road: distance tax and 2-3 wheeler EV subsidy apply in the baseline.** Mitigation rows 4451, 4720 (engineer road model, survey B1).

- Legacy: Passenger distance tax and 2-3 wheeler EV subsidy test ($C2227>1), text "res" > 1 is TRUE, so they also apply in the baseline.
- Fix: Scenario number > 1.
- Effect: None in the Egypt engineer run (the policy or fuel is zero there). prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L26 (Low; in legacy 465: open). Road: freight and 2-3 wheeler income growth read coal subsidies from 2038.** Mitigation rows 4487 AB:AE (also 4501) (engineer road model, survey B2).

- Legacy: Freight and 2-3 wheeler income growth read row 2455 (coal producer subsidies) from 2038.
- Fix: Lagged GDP growth (row 2446) in all years.
- Effect: None in the Egypt engineer run (the policy or fuel is zero there). prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L29 (Low; in legacy 465: open). Road: ownership of cars and trucks cannot fall.** Mitigation rows T4328, U4328 (engineer road model, survey B4).

- Legacy: Ownership cannot fall (max annual decrease 0 for passenger and freight).
- Fix: Allow a decrease of up to own_decline_fix a year (legacy 2-3 wheeler value, 10%).
- Effect: None in the Egypt engineer run (the policy or fuel is zero there). prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L32 (Low; in legacy 465: open). Road: industry emission factors for road diesel and LPG.** Mitigation rows G4376-G4378, G4419-G4421 (engineer road model, survey B7).

- Legacy: Stale emission-factor names: diesel and LPG use industry EFs, CNG/LNG the residential gas EF.
- Fix: Road EFs.
- Effect: None in the Egypt engineer run (the policy or fuel is zero there). prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L36 (Low; in legacy 465: open). Road: charging-station subsidy ramp.** Mitigation rows 4343 (engineer road model, survey B10).

- Legacy: Charging-station subsidy ramp accumulates before the start year and is not capped at the target year.
- Fix: 0 before the start year, linear to the target level, then constant.
- Effect: None in the Egypt engineer run (the policy or fuel is zero there). prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L39 (Low; in legacy 465: open). Road: freight distance output omits LPG and LNG trucks.** Mitigation rows 5267 (engineer road model, survey B21).

- Legacy: Freight distance output omits LPG and LNG trucks.
- Fix: All fuels.
- Effect: None in the Egypt engineer run (the policy or fuel is zero there). prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L40 (Low; in legacy 465: open). Road: wrong rows in average gas and EV fuel economy.** Mitigation rows 5368, 5373 (engineer road model, survey B22).

- Legacy: Average gas fuel economy weights freight by LPG freight fuel (5244) instead of LNG (5245); the EV fuel-economy fallback tests diesel (5326) instead of electricity.
- Fix: Right rows.
- Effect: None in the Egypt engineer run (the policy or fuel is zero there). prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L41 (Low; in legacy 465: open). Road: PHEVs carry the full BEV range anxiety.** Mitigation rows 4555 (engineer road model, survey B23).

- Legacy: PHEV TCO includes the full BEV range anxiety (about 100,000 $/vehicle), so PHEV sales vanish.
- Fix: No range anxiety for PHEVs (they refuel with gasoline).
- Effect: None in the Egypt engineer run (the policy or fuel is zero there). prototype: Fixed in the prototype engineer road model (v3.5; Methods, chapter Transport); latent in the legacy Egypt run (elasticity road model).

**L44 (Low; in legacy 465: fixed). Residential other oil products priced at the biomass price.** Mitigation row 5559.

- Legacy: The price term reads row 5549 (biomass) instead of 5548.
- Fix: Read the other-oil-products price (row 5548).
- Effect: None for Egypt today. prototype: Fixed in the prototype: own price.

**L45 (Low; in legacy 465: fixed with caveats). Residential leakage to biomass inconsistent.** Mitigation rows 5574-5593.

- Legacy: Sign and cumulation differ between rows 5564 and 5554; kerosene uses the LPG price and share rows (5587, 5588); duplicate kerosene change rows.
- Fix: Subtract the fossil change once, use the kerosene rows for kerosene, conserve the substituted energy.
- Effect: None while BiomassLeakage = No. prototype: Fixed in v5.1 (feature built, section 6b): one row set per fuel with its own price and share; fuel use = elasticity model + cumulative change computed on last year's actual use; one switch (BiomassLeakage, Settings C59).

**L46 (Low; in legacy 465: fixed). Road other biofuels: wrong price and terms.** Mitigation row 5406.

- Legacy: Uses the bioethanol price, applies the shadow price through eps_U, has an efficiency term equal to 1 and uses M2259 (coal exemption phase-out) as additional efficiency.
- Fix: Use the biofuel price, the shadow price through eps_F, the efficiency term and the road efficiency row.
- Effect: None for Egypt (no road biofuels). prototype: Not built in the prototype (road biofuels follow gasoline and diesel; none in Egypt).

**L47 (Low; in legacy 465: fixed). Self-generated renewables in aviation and navigation take the shock from wrong rows.** Mitigation rows 5491, 5516.

- Legacy: The "shock" is row 2512 (coal industry new excise) or row 2473 (blank).
- Fix: Use the shock row 2439.
- Effect: None for Egypt (no self-generated renewables). prototype: Not built in the prototype (no self-generated renewables outside power).

**L48 (Low; in legacy 465: fixed). Residential initially-exempt rows: no income factor; starred "Yes*" exemption test.** Mitigation rows 5546-5547, 5568-5570.

- Legacy: The initially-exempt rows M5568:M5570 grow without the income factor M2433; the AlwaysExemptResLPGKer test misses the starred defaults. The split itself works in the .xlsb (L5564:L5570 = IFNA(IF($L$1784=B, ... $K$1795 ...))); it is 0 in Egypt because ExemptMostCook is off (v5.5 check from the .xlsb; the LibreOffice conversion had shown IFNA(0)).
- Fix: Apply the income factor, start from the exempt share, and match the starred defaults.
- Effect: None (the initial exempt share is 0). prototype: Not built (the D8 initially-exempt split stays dead; LegacyDiff 67). The starred AlwaysExemptResLPGKer test is fixed in v5.1 (LEFT(x,3)="Yes", rows exf).

**L50 (Low; in legacy 465: open). Balance of payments: current account #NAME?, column lag, sign.** Mitigation rows 18180-18198.

- Legacy: The pre-policy current account (WEO BCA) is #NAME?, so the whole % of GDP panel errors (v5.5: the rows do look up INDEX(WEO,...); the cell plan L50 was built from texts the LibreOffice conversion truncated and is to be redone); the policy rows lag one column; the sign of policy net imports looks reversed.
- Fix: Read the WEO current account (BCA), drop the one-column lag and check the sign of policy net imports.
- Effect: Reported balance of payments only (the % of GDP panel shows errors). prototype: Not replicated (v3.16): the energy trade balance (data) and its change in the scenario year, no current-account level until WEO data are added.

**L51 (Low; in legacy 465: open). Energy trade balance of coal valued at the oil price.** Mitigation row 743.

- Legacy: The coal trade balance multiplies coal net imports by the crude oil price per GJ (row 731) instead of the coal price (row 732); Egypt 2022: -1.4 bn USD instead of about -0.5.
- Fix: Value the coal trade balance at the coal price (row 732), not the oil price (row 731).
- Effect: Reported energy trade balance only (Egypt: about 0.6 bn USD a year). prototype: Fixed in v4.6: coal at the coal price (data step Inputs_macro, from Balances and the international prices).

**L55 (Low; in legacy 465: fixed). China, Japan and Korea take regional power data.** Mitigation rows 2977-2985 K (Power A25:A356).

- Legacy: The country lookup searches the regional block (rows 42-109) first, whose codes chn.mpp.*, jpn.mpp.*, kor.mpp.* equal the country codes, so the regional rows replace the country rows.
- Fix: Search the country block (Power rows 110-294) before the regional block.
- Effect: None for Egypt. prototype: Fixed in v4.10: the country rows are looked up in the country block (Power rows 112-294) first; no effect for Egypt.

**L56 (Low; in legacy 465: fixed with caveats). Countries without CoC risk data get Sri Lanka's WACC parameters.** CoC rows 202-390 D:V.

- Legacy: The WACC calculator falls back to row 172 (Sri Lanka) for countries without fixed data, silently.
- Fix: Flag countries without CoC fixed data instead of using Sri Lanka.
- Effect: None for Egypt. prototype: Fixed in v4.10: such countries take the default WACC (as countries missing from CoC), flagged on Inputs (PsCoCData); no effect for Egypt.

**L60 (Low; in legacy 465: open). VAT payment on oil products divided by the full VAT rate.** Mitigation rows 2595, 2618, 2641, 2664 (VAT payment).

- Legacy: The retail price of gasoline, diesel, LPG and kerosene carries VAT x household share (rows 797-816), but the VAT payment is retail price / (1 + VAT rate) x VAT rate x share, so VAT is understated where the share is below 1 and the excise residual absorbs the gap.
- Fix: VAT payment = (supply cost + taxes) x VAT rate x household share.
- Effect: None for Egypt (VAT 0 on oil). prototype: Fixed (v4.12): VAT = (supply cost + taxes) x rate x share, consistent with the retail price.

**L61 (Low; in legacy 465: fixed). EU ETS price grows with the carbon-tax growth.** Mitigation row 1695 (from the column after the last data year).

- Legacy: After the last data year the EU ETS price grows with ExistingCTGrowth (MTInputs 214) instead of ExistingETSGrowth (209).
- Fix: Grow the EU ETS price with ExistingETSGrowth.
- Effect: None for Egypt. prototype: Fixed (v4.12): ETS prices grow with ExistingETSGrowth, carbon tax rates with ExistingCTGrowth.

**L62 (Low; in legacy 465: not fixed (marked fixed)). Existing carbon tax on transport diesel, LPG and kerosene uses the rate row as coverage.** Mitigation rows 1760-1762.

- Legacy: The fuel coverage is looked up with INDEX over rows 1732-1749 by fuel code, which finds the fuel rate row (1732-1734) before the coverage row (1745-1747): the tax becomes rate x rate x sector coverage; the single-price flag is ignored.
- Fix: Take the fuel coverage row, and the single-price flag, for transport diesel, LPG and kerosene.
- Effect: None for Egypt. prototype: Fixed (v4.12): every fuel takes rate x sector coverage x fuel coverage, the fuel rate only where the country has one and no single price.

**L63 (Low; in legacy 465: not fixed (marked fixed)). Existing carbon tax fuel coverage: lookup range cut short.** Mitigation J1741-J1749 (ECP!E133:E403).

- Legacy: The fuel coverage block of sheet ECP runs to row 425, the lookup stops at 403: part of Ukraine, Uruguay and the United Kingdom get no fuel coverage, so no existing carbon tax.
- Fix: Look the fuel coverage up in the whole ECP block (to row 425).
- Effect: None for Egypt. prototype: Fixed (v4.12): each scheme is looked up in its whole block (Inputs_ecp columns K:L).

**L64 (Low; in legacy 465: fixed). No existing ETS on other oil products outside power.** Mitigation rows 1711-1723.

- Legacy: The ETS block has other oil products for power only (row 1717); the all-sector price of other oil products gets no existing ETS, while the carbon tax block applies industry coverage to it (row 1758).
- Fix: Apply the industry ETS coverage to other oil products outside power.
- Effect: None for Egypt. prototype: Fixed (v4.12): other oil products take the industry coverage of both schemes.

**L65 (Low; in legacy 465: fixed). Carbon tax complementary to an existing ETS: last year's ETS coverage.** Mitigation rows 2270-2288.

- Legacy: With CTaxComplimentaryToETS = Yes the new tax covers 1 - the national ETS sector coverage of the previous year (column one to the left).
- Fix: Use the ETS coverage of the year for the complementary carbon tax.
- Effect: None for Egypt. prototype: Fixed (v4.12): the coverage of the year (the same from 2026, coverage being held after the last data year).

**L66 (Low; in legacy 465: open). Other energy use: no additional policy efficiency gains on fossil fuels.** Mitigation rows of other energy use (fossil fuels; renewables use $M2201).

- Legacy: The additional policy-induced efficiency gain of industry (MTInputs 245, row 2201) enters every industrial subsector and the renewables row of other energy use, but not its fossil rows.
- Fix: Add the industrial additional efficiency to the fossil rows of other energy use.
- Effect: None while the input is 0. prototype: Fixed (v4.13): other energy use takes the industrial gain on every fuel.

**L69 (Low; in legacy 465: open). GDP effects: the first cohort's excise drag is lost.** Mitigation row 8057 (policy 14373).

- Legacy: The excise (revenue) use of the first cohort looks up L$8113, a baseline-block cell (0), instead of the cohort's own row (L14372); the contractionary effect of the first year's revenue is dropped (Egypt about 3e-5 of GDP).
- Fix: Match the first cohort's excise use on its own row (L14372, baseline L8056), not L$8113.
- Effect: The first year's revenue has no contractionary effect (Egypt about 3e-5 of GDP). prototype: Fixed: every cohort counts its revenue use (share -1).

**L70 (Low; in legacy 465: open). Revenue: industry gas excise uses the coal rate and coal use.** Mitigation row 7747 (policy 14063).

- Legacy: The additional excise of gas in industry is the coal industry tax (R2512) x coal industry use (R6422).
- Fix: Use the gas industry excise rate (row 2581) and gas industry use in row 7747.
- Effect: Gas industry excise revenue is wrong wherever coal and gas excises differ (none for Egypt). prototype: Fixed: each subsector and fuel takes its own excise and use (rex, v4.15).

**L71 (Low; in legacy 465: open). Revenue: biomass taxes, subsidies and VAT divided by the unit conversion.** Mitigation rows 7791, 7805, 7859.

- Legacy: Biomass existing taxes, subsidies and VAT divide by _conv_ktoe_to_gj instead of multiplying, so they are about 0 (2.7e-11).
- Fix: Multiply by _conv_ktoe_to_gj in rows 7791, 7805, 7859.
- Effect: Biomass taxes, subsidies and VAT are 0. prototype: Fixed: fuel use x PJ/ktoe x rate for every fuel.

**L72 (Low; in legacy 465: open). Revenue: next-year references.** Mitigation rows 7657, 7742.

- Legacy: The LPG price-control row reads S$738 (next year) and the coal power excise S2466 (next year) instead of column R.
- Fix: Read column R (the year) in rows 7657 and 7742.
- Effect: Revenue of the year uses next year's rate. prototype: Fixed: the year's own column.

**L73 (Low; in legacy 465: open). Revenue: wrong coverage shares.** Mitigation rows 7677 (policy 13993), 7704.

- Legacy: Gas industry coverage divides by R6027 instead of the industry gas total (6428); kerosene power coverage multiplies power by domestic shipping (R2270 x R2273).
- Fix: Divide by the industry gas total (6428) in row 7677; use power x kerosene coverage (R2265 x R2270) in row 7704.
- Effect: Coverage shares of gas industry and kerosene power are wrong (info rows). prototype: Fixed: coverage by subsector and fuel (ctxnew, covct).

**L75 (Low; in legacy 465: open). Revenue reports: hard-coded row and mixed totals.** Mitigation rows 17145-17149, 17175, 17186.

- Legacy: The "additional revenues from excises" report indexes a hard-coded 759 (all zeros); "revenue by fuel source" takes electricity from the total (rev.tot) while the fuel rows are carbon tax revenue (rev.new).
- Fix: Index the excise report by the matched row instead of 759; take electricity from rev.new in the revenue by fuel report.
- Effect: The excise report is all zeros; revenue by fuel mixes totals. prototype: Fixed: 12d and 12e read the revenue rows (v3.13, v4.15).

**L76 (Low; in legacy 465: open). Multipliers: empty CIT table, WAGE on the GNFS table, approximate country match, default to Estimated.** Multipliers rows 19-22, 38-45, 1624-1822.

- Legacy: With MultipliersSource = Estimated, CIT lags 1+ read the empty rows 1624-1822 (so 0), WAGE reads the public consumption (GNFS) table, the country row is found by approximate MATCH (a code missing from the sorted list takes its neighbour), and any unknown source text means Estimated.
- Fix: Point CIT to the labour-tax or an own table (or the income group), WAGE to its own table, MATCH the country exactly (0), default unknown text to the income group.
- Effect: Estimated multipliers: CIT 0, WAGE = GNFS, a missing country takes its neighbour's. prototype: Fixed (v4.15): CIT and WAGE take the income group, exact match with the income group as fallback, unknown text the income group.

**L78 (Low; in legacy 465: fixed). ETS: auctioned share drops to 0 after the target year unless "Constant".** Mitigation row 1863 (MTInputs row 92).

- Legacy: With D_ETSAuctCont other than Constant the auctioned share becomes 0 after the target year (all permits free), whatever the target share.
- Fix: Hold the target auctioned share after the target year whatever the continuation (or offer a defined alternative).
- Effect: An auctioned share drops to 0 (all free) after the target year. prototype: Fixed (v4.15): the target share is held after the target year.

**L80 (Low; in legacy 465: fixed). ETS: the carbon-tax trajectory rescaled when the ETS is on.** Mitigation rows 2191, 2251.

- Legacy: E2191 = 1 / the volatility ratio multiplies the carbon-tax trajectory (row 2251) when the new ETS is applied.
- Fix: Leave the carbon-tax trajectory unscaled when the ETS applies (drop E2191 from row 2251).
- Effect: The carbon tax outside the ETS is cut by the volatility ratio. prototype: Fixed: the carbon tax path is the MTInputs path; the volatility adjustment acts on the ETS price only.

**L81 (Low; in legacy 465: open). Consumer subsidy phase-out: the fixed subsidy takes last year's factor.** Mitigation rows 2460, 2483, 2506, ... 2598, ... 2713 (fixed portion of subsidy, each price block).

- Legacy: The projected fixed subsidy is the base value x the consumer factor of the previous column (P2214 for Q), while the floating and producer rows use the year's own factor: the consumer phase-out lags a year.
- Fix: Use the factor of the same column in the fixed-subsidy rows (Q2214 for Q).
- Effect: A consumer subsidy phase-out starts and ends a year late. prototype: Fixed (v4.16): every wedge takes the factor of its year.

**L82 (Low; in legacy 465: open). Residential gas producer subsidy reads the oil row.** Mitigation row 2547.

- Legacy: The producer subsidy of the residential gas block reads row 827 (oil, $/liter) instead of 826 (gas, $/GJ).
- Fix: Point row 2547 to row 826 (gas producer subsidy).
- Effect: Residential gas takes the oil producer subsidy. prototype: Fixed (v4.16): producer subsidies by fuel (pros, psf); no price effect in the prototype (issue I49).

**L84 (Low; in legacy 465: fixed with caveats). Electricity consumer subsidy phased with the price-control factor; option text mismatch.** Mitigation rows 3606, 3635; MTInputs row 138.

- Legacy: The electricity consumer subsidy (PowerSubsidyExemptInclude = Include) is phased with the price-control factor (row 2216), not the consumer factor (2214); the unit says Exempt/Include* while the value is DoNotPhaseOut*.
- Fix: Phase the electricity consumer subsidy with the consumer factor (row 2214); one option text.
- Effect: An electricity subsidy reform follows the price-control timing. prototype: Not built (power parked); to fix with the power features: the consumer factor, one option text.

**L85 (Low; in legacy 465: open). Electricity consumer subsidy info row subtracts industry.** Mitigation row 7806.

- Legacy: The info row is -(MIN(0, res) - MIN(0, ind)) instead of -(MIN(0, res) + MIN(0, ind)).
- Fix: Add the industry part: -(MIN(0, res) + MIN(0, ind)).
- Effect: Reported electricity consumer subsidies wrong. prototype: Not applicable (info row; the prototype subsidy gap rgap sums both groups).

**L86 (Low; in legacy 465: fixed). No manual override for the electricity producer subsidy.** Mitigation I828.

- Legacy: The manual-input row of the electricity producer subsidy is #N/A, so a manual value is ignored.
- Fix: Give the electricity producer subsidy a manual-input row.
- Effect: Manual values ignored. prototype: Not built (Manual inputs to come).

**L89 (Low; in legacy 465: fixed). Coal in road, residential and services reads the residential coal shadow price.** Mitigation rows 5396, 5553, 5634.

- Legacy: The coal rows of road, residential and services read row 2378 (coal, residential) whatever the sector.
- Fix: Read the shadow price of the row's own sector for coal.
- Effect: Coal in road and services takes the residential shadow price (minor). prototype: Fixed: shadow prices by coverage sector x EF (shp).

**L90 (Low; in legacy 465: fixed). Residential leakage breaks the useful-energy balance.** Mitigation row 5593.

- Legacy: The biomass gain is -dF x e_m (the equivalent biomass is multiplied by BioEff again); conserving cooking energy needs -dF x e_m / e_b, so the gain is 5 times too small.
- Fix: Drop $C5593* in row 5593 (biomass gain = -sum of the equivalents).
- Effect: Biomass gain 5 times too small when leakage is on. prototype: Fixed in v5.1 (lkb = -lkd x e_m / e_b).

**L91 (Low; in legacy 465: fixed). Exempt residential fuel still leaks to biomass.** Mitigation rows 5580, 5586 (against 5546-5547).

- Legacy: The leakage price change is taken from M2652 / M2675 even when AlwaysExemptResLPGKer removes the new policy from the residential price.
- Fix: Compute the leakage price change from the residential after-tax price (the row's own new policy).
- Effect: An exempt LPG still leaks to biomass. prototype: Fixed in v5.1 (lkt reads the row's own new policy nce).

**L92 (Low; in legacy 465: open). ExemptMostCook never reaches Mitigation.** Mitigation I1784, K1795, rows 5568-5570.

- Legacy: Not reproduced in the .xlsb (v5.5 check): I1784 = IF(AND(H1784="Yes",ISNUMBER(MATCH(L1784,...))),1,0) with H1784 = MTInputs F312 (ExemptMostCook), and K1795 feeds L5564:L5570; the "typed 0" came from the LibreOffice conversion. The exempt share is 0 in Egypt because ExemptMostCook is off. Kept as an entry for traceability; no fix needed.
- Fix: I1784 = IF(LEFT(H1784,3)="Yes",1,0); start rows 5568-5570 from L(total) x K1795.
- Effect: ExemptMostCook has no effect on fuel use or revenue. prototype: Not built (D8; LegacyDiff 67).

**L93 (Low; in legacy 465: fixed). Fuel coverage rows test text labels and contain #REF!.** Mitigation rows 2259-2268 (column E).

- Legacy: The rows test D2312-D2320 / D2367 (text labels) and #REF!; the branch is never taken.
- Fix: Use the sector rule IF(D2369=1,IF(OR(C2173=4,C2173=9),"Yes","No"),...) in rows 2259-2268.
- Effect: None (dead branch). prototype: Not built (coverage by switch).

**L94 (Low; in legacy 465: open). Exemption phase-in rules differ between rows.** Mitigation rows 2259-2265, 2270-2288 against 2266-2268, 5568-5570.

- Legacy: The first group uses YearPha with the ExemptPhaseout switch; the second counts from CPIntro (row 2258) and ignores the switch.
- Fix: One rule: MAX(MIN((t+1-YearPha)/ExemptPhaseoutPeriod,1),0) x ExemptPhaseout.
- Effect: Biomass, renewables and jet fuel phase in differently from the other fuels. prototype: Not built (LegacyDiff 67).

**L95 (Low; in legacy 465: fixed with caveats). Power demand: efficiency increment sits on the net-exports row.** Mitigation row 3719 (D3719 = D3742 'Net Exports (Imports negative)', F:J net-export data egy.mit.nxp.ecy; L3719 'Additional Efficiency Improvements - Power demand', M3719 = M2198 = MTInputs F242); read as $M3719 in rows 3691, 3697, 3703, 3709.

- Legacy: One row carries two things: net-exports data (columns D-J) and the power-demand efficiency increment (L:M). The demand formulas read $M3719 as the efficiency term, so the row label misleads.
- Fix: Put the efficiency increment on its own labelled row (or read M2198 directly); leave row 3719 to net exports.
- Effect: None on values (increment 0 by default); a reader of the row label takes the efficiency term for a trade term. prototype: Fixed in the prototype (v5.1 register; the power-demand efficiency term has its own labelled row, AdditionalEfficiencyPower).

**L96 (Low; in legacy 465: open). Fuel-use block: mislabelled parameter and fuel rows.** Mitigation C2199:C2201 ('Tax in nominal or real terms?', 'Exponential option or linear' twice) beside K2199:M2201 (road, residential, industrial additional efficiency, MTInputs F243-F245); E2385 (LPG 'Road'), E2386 (kerosene 'Industry') on all-sector rows (codes shp.lpg.all, shp.ker.all); D5615, D5711, D6058, D6069 'Other oil pinducts'.

- Legacy: Column C of rows 2199-2201 labels the carbon-tax settings of column E, while every fuel row reads K:M of the same rows as the additional-efficiency term; the sector labels of the LPG and kerosene shadow prices do not match their all-sector codes; a typo in four rows.
- Fix: Give the additional-efficiency increments their own labelled rows; label the LPG and kerosene shadow-price rows 'All'; correct the typo.
- Effect: None on values; formula audits misread the additional-efficiency term as a carbon-price setting. prototype: Fixed in the prototype (v5.1 register; own labels: additional efficiency, shadow prices by coverage sector, fuel names).

**L97 (Low; in legacy 465: open). Iron & steel memo rows unused; one reads next year's growth.** Mitigation rows 5667-5676, 5703, 5727-5728 (iron & steel block; M5667 = N2446).

- Legacy: An EF-weighted average price (5703), an elasticity table (5668-5676) and 'Fuel'/'Average' demand and efficiency multiples (5727-5728) are computed but referenced nowhere; M5667 takes next year's GDP growth (N2446).
- Fix: Delete the memo rows (or move them to a diagnostics area with the year's own growth M2446).
- Effect: None (dead calculation); would be wrong if anything used it. prototype: Not built in the prototype (dead memo rows).

**L100 (Low; in legacy 465: fixed). Manual domestic prices: the electricity rows are never read.** Manual inputs G59:N146 (names _manual_prices, _manual_codes).

- Legacy: _manual_prices (G59:N133) and _manual_codes (G59:G133) stop at row 133, so the electricity prices and producer subsidy (rows 136-146) are never read (the cause of L86).
- Fix: Extend both names to row 146.
- Effect: Manual electricity prices ignored. prototype: Not applicable in the prototype (manual domestic prices not built; block placed, not read).

**L101 (Low; in legacy 465: open). Manual services income elasticities read the industries column.** Elasticities F51:F58 (Manual inputs rows 279-286).

- Legacy: F51:F58 (services) read Manual inputs column M (industries) instead of N; the price and efficiency rows are right.
- Fix: Read N279:N286 in F51:F58.
- Effect: Manual services income elasticities equal the industry ones. prototype: Not applicable in the prototype (manual elasticities not built; block placed, not read).

**L102 (Low; in legacy 465: fixed). Manual non-energy elasticities can never take effect.** Manual inputs K326:K327; Mitigation K366:M367.

- Legacy: K326:K327 are IF($E$293="Manual",#REF!,...) and Mitigation K366:M367 test E288 (MTInputs ElastIncAdjustment), which never equals "Manual".
- Fix: Type the inputs and read them directly.
- Effect: Manual non-energy elasticities ignored. prototype: Fixed in v5.2 (typed inputs on Manual inputs K325:M327, read directly; same values; LegacyDiff 72).

**L103 (Low; in legacy 465: open). Manual SCC reads a path typed on Mitigation, not the Manual inputs block.** Manual inputs rows 234-240; Mitigation row 17668.

- Legacy: The SCC block of Manual inputs is read by nothing; the Manual option of NSCCSource / GSCCSource takes the path typed on Mitigation row 17668.
- Fix: Mitigation row 17668 = 'Manual inputs'!J237 (NSCC) / J240 (GSCC).
- Effect: Manual SCC entered on Manual inputs is ignored. prototype: Fixed in v5.2 (scc.man reads Manual inputs row 237 by year; names SCCManVal, SCCManYear). No effect on the shipped scenarios (SCC source Target).

**L104 (Low; in legacy 465: open). Name CH4Feebate points to an empty cell.** Manual inputs J217 (name CH4Feebate).

- Legacy: The defined name CH4Feebate points to J217, which is empty (the methane block ends at row 200).
- Fix: Delete the name or point it at the methane fee input.
- Effect: None (unused name). prototype: Not applicable in the prototype (name not used).

**L106 (Low; in legacy 465: fixed). Manual inputs memo swaps the renewables and electricity price elasticities.** Manual inputs K315:N316.

- Legacy: The memo totals of renewables and electricity use the price elasticity rows 298 and 297 the wrong way round.
- Fix: Use rows 297 and 298 respectively.
- Effect: None (memo only). prototype: Fixed in the placed memo (display only).

**L107 (Low; in legacy 465: fixed). Renewable subsidy: start year of the additional subsidy reuses the consumer-subsidy phase-out year.** Mitigation E2736 (policy E9052) = row 270 = MTInputs F132 (YearConsSubPha).

- Legacy: The additional renewable subsidy (MTInputs 353) starts in the year the consumer fuel subsidies start to be phased out; it has no start-year input of its own.
- Fix: Add an MTInputs row (and Dashboard cell) for the start year of the additional RE subsidy and point E2736 at it.
- Effect: The two policies cannot be timed apart. prototype: Fixed (v5.4): own input RenSubsidyAddStartYear (MTInputs row 482, default 2027 = the default of row 132); rows rnsp, rns.

**L109 (Low; in legacy 465: fixed with caveats). Capex decline options Low and Vhigh have no wind and solar series.** Mitigation rows 3038-3046; Power rows 303-330.

- Legacy: RenewableCostDeclineRate Low gives codes wld.ctf.low.wnd/sol and Vhigh wld.ctf.vhg.wnd/sol/ore, which the Power tab does not hold (only oldlow, oldvhg); the MATCH fails and the INDEX errors.
- Fix: Add the Low and Vhigh series to the Power tab, or map the options to the old series.
- Effect: Low and Vhigh options give errors. prototype: Fixed (v5.4): the older series of the same option (wind, solar) or Medium (other renewables, Vhigh), Inputs_ppath tcf|<type>|<option>. User to confirm the fallback.

**L110 (Low; in legacy 465: fixed). Power revenue rebate counts VAT that was never collected.** Mitigation rows 3615, 3644, 3663, 7874, 7735 (policy +6316 / +6316).

- Legacy: The rebate includes VAT (carbon cost x pass-through x (1 + VAT)) and enters total revenue through row 7735, while the VAT on the carbon cost is never counted as revenue.
- Fix: Use the carbon cost before VAT in the rebate, or count the VAT on the policy term in the VAT revenue.
- Effect: Revenue split inconsistent (total unchanged). prototype: Fixed (v5.4): the rebate returns the carbon cost passed through (row rreb, without VAT) and the VAT on it is not collected (rnvat); the total change equals legacy's.

**L111 (Low; in legacy 465: fixed). Manual electricity excise revenue counts the whole excise, also where the price does not include it.** Mitigation rows 3602, 3631, 3660, 7871, 7748.

- Legacy: The revenue memo 3660 (and 7748) = manual excise x consumption in every year, while the price includes only the change since the last historical year x pass-through.
- Fix: Compute row 3660 from the excise in the price.
- Effect: Excise revenue overstated when AdditionalExcise is on. prototype: Fixed (v5.4): excise revenue = the excise in the price x consumption (rows pex, rpex, rexm).

**L113 (Low; in legacy 465: fixed). Power switches tested for the exact "Yes" (was issue I58).** Mitigation G261 (PowerRebates), row 3150 (RenewableSubsidyHydro), F201 (AdditionalExcise).

- Legacy: The switches test ="Yes", so the starred default "Yes*" of the MTInputs dropdowns counts as No: choosing the default option switches the feature off. Reclassified as a bug by the user (2026-10-19), as the PPA switch.
- Fix: Test LEFT(switch,3)="Yes" in G261, row 3150 and F201, so Yes and Yes* both count as Yes.
- Effect: Choosing the default option ("Yes*") of PowerRebates, RenewableSubsidyHydro or AdditionalExcise switches the feature off. prototype: Fixed (v5.4): the prototype accepts Yes or Yes* (LEFT 3).

**L114 (Low; in legacy 465: open). Renewable subsidies: nominal inputs used as real (was issue I55).** Mitigation rows 2734-2735, 2743, 2745 (MTInputs 352-353).

- Legacy: MTInputs 352-353 are labelled $/kWh nominal but enter the real cost and revenue without deflation (row 2743 = -E2734). A formula that contradicts its label: reclassified as a bug by the user (2026-10-19).
- Fix: Deflate the nominal inputs (rows 2734-2735) by the CPI index before they enter row 2743, or relabel MTInputs 352-353 as real.
- Effect: Renewable subsidies too large in real terms in later years (nominal value read as real). prototype: Fixed (v5.6): the inputs are converted to real with the CPI factor of the year (row rnsp).

**L116 (Low; in legacy 465: open). Services gasoline and diesel income elasticities: step-change column reads the wrong rows.** Elasticities H53, H54.

- Legacy: H53 = H173 (renewables, services) and H54 = H174 (electricity, services) instead of H169 and H170 (gasoline, diesel, services); every other row reads its own. No effect today (all 0.13).
- Fix: Point H53 and H54 at rows 169 and 170.
- Effect: None today (equal values); wrong step-change elasticity for services gasoline and diesel when regional values differ. prototype: Not built: the prototype reads the income elasticities by code from the data step.

**L117 (Low; in legacy 465: open). Transfers multiplier (TRNS): estimated lag-0 table read two rows off.** Multipliers D44.

- Legacy: D44 reads INDEX(D$1218:D$1418, ...) while E44:O44 read $1220:$1418 (rows 1218-1219 are titles). No effect today (lag 0 is 0 for every country).
- Fix: Read D$1220:D$1418 in D44, as E44:O44.
- Effect: None today (lag 0 is 0); the lag-0 transfers multiplier would come from the wrong country. prototype: Not replicated: the prototype reads the multiplier table by country code.

**L120 (Low; in legacy 465: open). NDC index rows: unconditional and conditional ratios inverted against the average.** Mitigation rows 18482-18484.

- Legacy: Rows 18482-18483 divide the start-year emissions by the target (G18431/F18479) while row 18484 divides the target by the start-year emissions; the chart rows 18494-18495 read 18484 for the unconditional line and 18483 (inverted) for the conditional one. Found by the item 8 plan (v5.7).
- Fix: Use target / start-year emissions in rows 18482-18483, as 18484.
- Effect: Conditional NDC line plotted as the inverse ratio. prototype: Fixed (v5.7, NDC comparison 14c): ndc.idx = target / base-year GHGs incl. LULUCF for both.

**L121 (Low; in legacy 465: open). Historical NDC: the target "level" is the emissions cut.** Mitigation rows 18443-18445.

- Legacy: Rows 18443-18445 return the cut (F18440 x adj) when adj < 1 and the level otherwise; harmless today only because adj < 1 never happens (L119). Found by the item 8 plan (v5.7).
- Fix: Return F18437 - F18440 x adj (the level), as the Fixed block.
- Effect: None today (branch never runs); a cut would be read as a level. prototype: Fixed (v5.7, NDC comparison 14c): level = reference-year emissions x (1 - reduction).

**L124 (Low; in legacy 465: fixed). Producer subsidy: the residential gas block reads the oil subsidy.** Mitigation row 2547 (N2547).

- Legacy: The "in which: producer-side subsidies" row of the gas | residential block reads N$827 (oil, $/liter) where the other gas blocks read N$826 (gas, $/GJ). Found by I49 (v6.1). The same cells as L82 (fix plan L82 covers it).
- Fix: Read N$826 (gas) in row 2547, as the other gas blocks (same cells as the L82 plan).
- Effect: A gas producer subsidy misses residential gas, which takes the oil value instead. prototype: Fixed (v6.1, I49): every block reads the per-unit subsidy of its own fuel by its international price position (psp).

**L125 (Low; in legacy 465: fixed). Producer subsidy: other oil products add a per-liter value to a per-barrel price.** Mitigation row 2685 (N2685).

- Legacy: The other-oil-products block ($/bbl) adds the oil subsidy per liter (row 827) unconverted, about 159 times too small. Found by I49 (v6.1).
- Fix: Multiply by liters per barrel in row 2685.
- Effect: The oil producer subsidy is about 159 times too small for other oil products. prototype: Fixed (v6.1, I49): x liters per barrel (LitersPerBbl) for a barrel-priced block.

**L127 (Low; in legacy 465: open). Power: levelised variable cost reads the variable cost to 2041.** Mitigation rows 3439-3447 (D9).

- Legacy: Investment choices use the variable cost levelised from the year to the end of the horizon (perfect foresight of the cost path). Safe only while that cost is built from inputs alone (prices before new policies, announced policy rates); a variable cost that reads quantities would close a circular reference. Latent today. Found by the circular-reference review (v6.2, user 2026-10-20).
- Fix: Keep the levelised variable cost (rows 3439-3447) on input-driven costs only; if an ETS price becomes endogenous, levelise the announced price path instead of the solved one.
- Effect: Latent: investment would read future quantities through the cost path. prototype: Fixed (v6.2) as a rule with a test: the levelised cost reads only input-driven costs (tvc: fuel price for power, variable O&M, policy rates, shadow price, rebate); the quick check tests that no other row reads a later year and that tvc reaches no fuel use, GDP or power quantity row.

**L128 (Low; in legacy 465: fixed). Net revenue report rows read the next year.** Mitigation rows 6238, 6243 (policy 12554, 12559).

- Legacy: The net revenue rows (USD and % of GDP) read the next column of rows 8024 and 8029 (K6238 = L8024 ... AD6238 = AE8024), so each year shows the next year's net revenue. Report only (rows 6239, 6244 read them). Found by the read-of-later-years scan of legacy (v6.2, user 2026-10-20).
- Fix: K6238 =K8024 and K6243 =K8029, filled K:AD; policy rows 12554, 12559 the same (+6,316).
- Effect: Each year reports the next year's net revenue (USD and % of GDP). prototype: Not in the prototype (its revenue rows read the same year; reporting rebuilt). Legacy fix: K6238 =K8024 and K6243 =K8029, filled K:AD.

**L130 (Low; in legacy 465: open). Intensity NDC: conditional and unconditional rows use different base years.** Mitigation rows 18455-18456.

- Legacy: F18456 (conditional) applies the cut to the target-year BAU intensity (F18454); F18455 (unconditional) applies it to the reference-year intensity (F18453). Found by the cell plans (user 2026-10-20: a bug).
- Fix: F18456: apply the cut to the reference-year intensity F18453, as F18455 does.
- Effect: Conditional and unconditional intensity targets are not comparable. prototype: Fixed (prototype 14c: ndc.hi applies the cut to the reference-year intensity x target-year GDP, for both).

**L131 (Low; in legacy 465: open). Codes: one output code on rows with different contents.** Mitigation rows 466, 2442, 16170 (gdp.pre.lvl); 7722, 7742, 7985 (sub.new.usd); 7638-13962 (rev.ctr.coa).

- Legacy: Legacy reuses a code for other quantities: gdp.pre.lvl for ln(GDP pc), GDP in $mn and in bn US$; sub.new.usd for revenue subtotals; rev.ctr.coa for the gasoline to electricity rows. A lookup by code finds the first row only. Found by the codes crosswalk (v7.1).
- Fix: Give each row its own code (e.g. gdp.pre.ln, gdp.pre.mn; sub.new.usd only on its own subtotal).
- Effect: Lookups by code (MTOutputs, the data link) return the first row of a reused code. prototype: Fixed (v7.2, codes R7): every prototype code is unique (check_codes; the 18 copy rows carry no code).

**L132 (Low; in legacy 465: open). Codes: capitals and empty tokens.** Mitigation rows 7606, 13922 (oc.tot.); em.pm2.All.<sector> rows.

- Legacy: Legacy codes mix capitals (All) into the lower-case protocol and end with an empty token (oc.tot., no scenario number), so a lookup of the protocol code fails. Found by the codes crosswalk (v7.1).
- Fix: Write the codes in lower case and with a scenario number: em.pm2.all.<sector>, nox.tot.<n>.
- Effect: Lookups of the protocol codes fail. prototype: Fixed (v7.2): prototype codes are lower case with no empty token (code formula; check_codes).

**L133 (Low; in legacy 465: open). Codes: nox.tot holds N2O, oc.tot. holds NOx.** Mitigation rows 7606, 13922 and the GHG total rows (nox.tot).

- Legacy: The N2O total in CO2e carries the code nox.tot and the NOx forcing row the code oc.tot. (labels: Nitrous oxide; Nitrogen oxides): a reader of the codes takes one gas for the other. Found by the codes crosswalk (v7.1).
- Fix: Rename the N2O total n2o.tot and the NOx forcing row nox.tot.
- Effect: A reader of the codes takes one gas for the other. prototype: Fixed (v7.2, codes R5): n2o.tot and nox.tot carry their own gas.

**L134 (Low; in legacy 465: open). Price-increase units: other oil products "$/bbn", default "$/liter" for other oil products and biomass.** MTInputs rows 182-183 (columns E and G); Mitigation I177, I180.

- Legacy: The unit labels of the price-increase inputs read "$/bbn" (for $/bbl) for other oil products, and the default column says "$/liter" for other oil products and biomass, whose prices are per barrel and per GJ. No formula reads the labels (Mitigation rows 168-180 use the amounts in G and H only), so no value changes; a user typing an increase per liter for these fuels gets a wrong price path. Found by the tracker leads (2026-10-23).
- Fix: Label the price-increase units USD/bbl (other oil products) and USD/GJ (biomass) in columns E and G of MTInputs rows 182-183.
- Effect: Labels only: no value changes; a user may type an increase in the wrong unit. prototype: Fixed (v8.3): the prototype's ScenarioDefinition rows 182-183 read $/bbl and $/GJ, defaults included.
