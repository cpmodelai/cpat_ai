# Power engineer model: features to add (plan, 2026-10-18; decisions recorded)

**Status (v5.6, 2026-10-19): P1-P5 done** (P3 manual capacity and investment, P5 coal implicit cost and memo rows in v5.6; the optional GoalSeekCoal calibration script is not built: the stored legacy values are used). Earlier status: **(v5.4) P1, P2 and P4 done.** Item 1 in v4.14; items 3, 4 (P1), 2 (P2) and 5, 6, 7, 12 (P4) in v5.4 (Methods, chapter Power, Methods, chapter Power). Open: P3 item 8 (manual capacity and investment) and P5 (items 10, 13), planned for v5.5. Dropped: items 11 and 14.

User request (2026-10-18): plan the features of the power engineer model that the prototype does not have yet. This is a plan, not a method note; each release gets its method text in `PowerModel_Method` / `PowerPrices_Method` when it is built.

Source: survey of the legacy power block (Mitigation rows 2731-4301 baseline, +6331 for the policy run; ScenarioDefinition rows from the template; 'Manual inputs'), checked against `build.py`. Every feature below is **off or zero for Egypt**, except items 1 and 2 (which change Egypt's results) and possibly item 9 (data). So most releases leave Egypt's numbers unchanged until a user sets an input; each needs a test scenario that switches it on.

Classification follows NORMS 0: a legacy feature is replicated (bugs fixed); a legacy bug is fixed and registered; anything that extends legacy needs your decision. Under the input rule (NORMS 4) the inputs come from ScenarioDefinition; the few that legacy keeps elsewhere ('Manual inputs', typed cells) go to Settings or a data tab.

## 1. The features

| # | Feature | Legacy (rows; inputs) | What the prototype lacks | Class | Egypt | Size |
|---|---|---|---|---|---|---|
| 1 | **Capacity for next year's demand** (I8, U9) | Investment need (rows 4022-4031) uses "Next Year Demand" (row 4027), but its formula is this year's demand (M3752). Row 4031 "should be the same" compares with next year's capacity. | `need` uses this year's demand, as legacy | **Legacy bug** (label and check row show the intent): fix, keep a switch for the legacy comparison. No circularity: next year's demand depends on this year's price. | Changes results: more new capacity a year earlier, less gas dispatch | Tiny |
| 2 | **Policy power inputs per scenario** (done v5.4) | Legacy runs each ScenarioDefinition column with its own baseline and policy run, so every power input can differ by scenario. | Inputs_pset reads every power setting from scenario 1, so a scenario that changes e.g. NewInvCoal ("no new coal"), early retirement or AdditionalEfficiencyPower has no effect | Departure from legacy (not a bug): replicate for the **policy-like** inputs; keep the **technical** ones (logit constants, WACC, CF bounds, storage, cost decline) global on scenario 1 and say so | None (shipped scenarios use the defaults) | Medium (plumbing) |
| 3 | **Final deficit to gas** (done v5.4) | Typed switch E4248 = No: the deficit left after the second investment round goes to gas (row 4252) | Not built | Legacy feature (input outside ScenarioDefinition: Settings, as legacy's typed cell) | None (off) | Tiny |
| 4 | **Two ignored inputs** (done v5.4) | MaximumGasCF (ScenarioDefinition 373) caps gas (row 3784); LongTermStorageFor100pcVRE (394) scales the long-term storage term (row 3909) | Gas uses the coal cap (MaximumCoalCF); the storage factor is implicitly 1 | Departures (same values at the defaults): wire both | None at the defaults | Tiny |
| 5 | **PPAs** (coal and gas; done v5.4) | Share (ScenarioDefinition 382) x phase-out factor (383 baseline / 384 policy, start 385, years 386; row 2218): that share runs at its historical capacity factor whatever its cost (rows 3801-3805) and cannot retire early (3987, 3993) | Not built | Legacy feature. Legacy oddities: share to phase out typed as 1 (Q2193); the switch fires only on the exact text "Yes*" (treat as an issue: replicate with "Yes" or "Yes*") | None (share 0) | Small |
| 6 | **Renewable subsidies** (done v5.4) | rns = base subsidy (354) + additional subsidy (355, policy only) phasing out over 356 years; hydro if 357 = Yes; enters levelised cost and revenue (rows 3142-3152, 3303-3313, 3665-3669) | Slot exists (rns = 0) | Legacy feature. Legacy bug: the start year reuses the consumer-subsidy phase-out year (ScenarioDefinition 132). Oddity: "nominal" input used as real | None (0) | Small |
| 7 | **Power revenue rebate** (PowerRebates, 342; done v5.4) | Carbon cost removed from end-user prices (rows 3595, 3615, 3644), revenue memo 3663 | Rebate fixed at 0 in `rp` | Legacy feature | None (off) | Small |
| 8 | **Manual capacity and investment** | NewInv<type> = "Manual" (397-405) and a capacity path per scenario ('Manual inputs' 342-371): investment = path increase + retirement (rows 4097-4105); all-manual mode (4287-4296) | Not built | Legacy feature. Legacy bug: the need net of manual investment (row 4108) is never used, so logit investment comes on top (over-investment). Unclear: one-year lag in the all-manual mode | None (no Manual type), but **the only way to enter El Dabaa nuclear** (no nuclear in the base year, so NewInvNuc "If Present*" blocks it) | Medium (rows + data table) |
| 9 | **Planned retirement data** (U13) | Coal only, Global Coal Plant Tracker (Power rows 1636-1878); Egypt: no data | The mechanism exists for every type; Egypt has no data | Data task | Changes results once data are entered | Small (data) |
| 10 | **Coal implicit cost** (D3) | Short- to long-term value by 2030 (rows 3361-3371), calibrated per country (tab GoalSeekCoal, 85 countries, not Egypt); No / Manual options (369-371) | Not built | Legacy feature. Issues: it also raises generation costs and tariffs (a calibration wedge treated as a cash cost); the gas implicit cost points at an empty cell. The lookups are stripped in the NoPropData file: data needed | None (no coal) | Small-medium + data + optional calibration script |
| 11 | **Feebate on power demand** | Row 3683 should feed a carbon price into the efficiency term of demand, but points at a blank row (L$2255): always 0 | Not built | Legacy bug with no working reference: needs a design decision | None | Small |
| 12 | **Electricity excise** (done v5.4) | Policy type 11 (row 2253: grid intensity x carbon price) and the manual electricity excise ('Manual inputs' 161-162) | Not built | Legacy feature | None | Small |
| 13 | **Memo tables** | F1-F7 (system cost, fuel prices per kWh, carbon intensity, switching carbon prices gas over coal), cost breakdown (344) | Not built | Reporting only | None | Small |
| 14 | **Elasticity-based power model** (legacy section 3) | A reduced-form model (about 220 rows a run), chosen by PowModelSelected (227: Engineer / Elasticity / Average); its demand can feed the engineer model (364) | Not built (engineer only) | Legacy feature, large. Legacy oddity: in "New" cost mode thermal plants carry only fuel and carbon costs | None (Egypt runs Engineer) | Large |

## 2. Decisions (user, 2026-10-18)

| # | Question | Decision |
|---|---|---|
| 1 | Item 1, capacity sized for this year's demand | **A legacy bug**: fix it (I8 becomes a legacy bug in the register when P1 is built), with a switch that reproduces legacy |
| 2 | Which power inputs per scenario | **Every power input on ScenarioDefinition** is read per scenario (technical ones too) |
| 3 | Manual capacity and investment, El Dabaa and announced plans | **The functionality is needed; no Egypt data to add.** Capacity plans come from 'Manual inputs': time to bring in the legacy 'Manual inputs' tab, the second input source after ScenarioDefinition |
| 4 | Item 11, demand-side power feebate | **Not built**: CPAT already has the functionality through the rebating of power prices (item 7) |
| 5 | Item 14, elasticity power model | **Not built** |
| 6 | Item 10, coal implicit cost in tariffs | **A switch, default as legacy** (the implicit cost enters generation costs and tariffs) |
| 7 | P3, capacity blocks | **One capacity block per prototype scenario** (an extension of legacy's two blocks, baseline and policy; user 2026-10-18) |
| 8 | P2, scope | **As legacy**: each scenario's ScenarioDefinition column holds everything a scenario changes; technical inputs are not usually changed across scenarios (user 2026-10-18) |

Not now (user 2026-10-18): the plan is defined, nothing is built yet. Built since: P1, P2, P4 in v5.4 (2026-10-19).

## 3. Releases

| Release | Content | Changes Egypt? |
|---|---|---|
| **P1: corrections** (done: item 1 v4.14, items 3 and 4 v5.4) | Item 1 **done in v4.14** (legacy bug L67; legacy kept as a switch in the Python reference only, NORMS 0) (and the capacity check of bug L10); item 3 (final deficit to gas, switch on Settings as legacy's typed cell E4248); item 4 (MaximumGasCF, LongTermStorageFor100pcVRE wired) | Yes (item 1) |
| **P2: power inputs per scenario** (done v5.4) | Every ScenarioDefinition power input read in the scenario's own column (section 1 / section 3 rows by scenario instead of Inputs_pset and Inputs_ptech scenario 1), e.g. NewInv<type> and their years (397-415), early retirement (378-379), pass-through (343), AdditionalEfficiencyPower (242), scale-up limits (359-362), logit constants, WACC, CF bounds, storage | No (shipped scenarios use the defaults) |
| **P3: the Manual inputs tab** (done in v5.2: the whole tab placed; the manual capacity block 342-371 is read when item 8 is built) | The legacy 'Manual inputs' tab in the INPUTS group at its legacy addresses (paste-compatible, as the data tabs, NORMS 1.5), read by the model where legacy reads it; the items the prototype already takes from legacy 'Manual inputs' move onto it (methane fee switches J196-J200, now Settings rows 47-51; ETS price override O15:AB15; BEV fuel economy paths 375-377, now TransportPaths). Then item 8: manual capacity and investment (NewInv<type> = Manual; capacity paths rows 342-371; legacy bug 4108 fixed: logit investment sized on the need net of manual investment; the all-manual lag decided when built). One capacity block per scenario (decision 7; legacy has a baseline and a policy block). No Egypt data | No (no data) |
| **P4: power policies** (done v5.4) | Item 5 (PPAs, baseline / policy phase-out by scenario); item 6 (renewable subsidies, own start year: legacy bug fixed); item 7 (power revenue rebate, PowerRebates, which also covers the demand-side feebate); item 12 (electricity excise: policy type and 'Manual inputs' 161-162, after P3) | No |
| **P5: coal implicit cost and memos** | Item 10 with the switch, default as legacy (enters tariffs); GoalSeekCoal data from the full legacy file; optional calibration script. Item 13 memo tables (F1-F7, cost breakdown) | No |

Dropped: item 11 (covered by item 7), item 14 (elasticity model). Item 9 (planned retirement data): the mechanism exists for every type; no Egypt data to add.

Each release: Python reference (`power_model_ref`) first, a test scenario that switches the feature on, quick check, paste test, register and LegacyDiff rows 28 and 34.

## 4. Points to settle when building

- P2: the prototype has one baseline (scenario 1) for every scenario, while legacy runs each ScenarioDefinition column with its own baseline. A technical input changed in a policy scenario therefore changes that scenario only, and its difference to scenario 1 mixes the input change with the policy. Technical inputs are not usually changed across scenarios (decision 8); said so on Inputs_pset (v5.4).

How v5.4 settled the points of the build:
- P2: the settings are section-1 rows (ScenarioDefinition, the scenario's column; sub-heading "Power sector settings"); section 3 sub-table A0 applies them to the power data of Inputs (capacity factor, efficiency, WACC, discounted lifetime, base-year capacity, permits and start years, scale-up and retirement rates, storage, PPA, subsidy, rebate and excise switches). The power data tables on Inputs keep scenario 1's values for reference. Not read (no prototype feature): CostBreakdownYear (344, P5 memo), ElasticityModel (345, dead), PowGenCostsOldNew (349) and UseElasticityModelPowerDemandInEngineerModel (364, elasticity model dropped), SupplyCostDeltaSubsidy (353, telescoped price S4), coal implicit cost (369-371, P5).
- P4 item 6: the start year of the additional subsidy is a new ScenarioDefinition row after the template (RenSubsidyAddStartYear, row 482, default 2027; legacy bug L107). The revenue counts the base subsidy once (legacy bug L108).
- P4 item 7: the rebate removes the carbon cost passed through (and its VAT) from end-user prices in policy scenarios with PowerRebates = Yes or a feebate scenario of the legacy scenario table; the government returns the carbon cost to consumers (row rreb; legacy bug L110: legacy's memo includes VAT never counted).
- P4 item 12: the electricity excise of the scenario Electricity excise (grid CO2 intensity of the base year x carbon price, issue I56) and the manual electricity excise of Manual inputs rows 161-162 (AdditionalExcise = Yes, policy scenarios; enters the price like the supply cost, relative to the last historical year, with pass-through; revenue = the excise in the price: legacy bug L111).
- Switches that legacy tests for the exact "Yes" or "Yes*" accept both (LEFT 3): PPA phase-out (issue I54), PowerRebates, RenewableSubsidyHydro, AdditionalExcise (issue I58).
- The capex decline options Low and Vhigh have no wind and solar series in the Power tab: the older series of the same option is used (legacy bug L109).
- P3: the Manual inputs tab is the second input source (NORMS 4); policy inputs there should come from legacy, not extend it.

## 5. Uncertain (from the survey)

- The one-year lag in legacy's all-manual mode (row 4288).
- Why the GoalSeekCoal lookups are empty in the NoPropData file.

