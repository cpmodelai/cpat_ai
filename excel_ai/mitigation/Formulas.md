# Workbook formulas of CPAT-AI-Mitigation-Prototype v1.0.4 (implementation reference)

Generated from the workbook by `make_equations.py` (do not edit by hand): every formula of the Mitigation sheet, scenario 1, with cell references replaced by variable codes, the changes against legacy CPAT (section B) and the LAMBDA library (section C). For the model itself read the equations in mathematical form, `Equations.md`; this file is for checking and editing the workbook.

**Notation.** `code[f,s](t)`: variable `code` for fuel f and sector s in year t, where f, s and t are those of the row being defined (other fuels or sectors are named, e.g. `ener[gso,rod](t-1)`); `code[n rows](t)`: the block of n rows of that variable (a lookup or sum over it); `(t-2..t+2)`: a span of years; `<label>`: a parameter of the row (columns D:G, defined under *Parameters*); `data`: a number from the data step or an input; `year`: the year of the column; named constants (e.g. `MWyMkWh`) and defined names of data tables are as on sheet `Constants` and in the name manager. 2041 is the LAMBDA year: its cells call the named LAMBDAs of section C with the same arguments as the plain formulas of the other years. `(B)` after a block: the fuel column of those rows. `SecVar`, `SecSub`, `SecFuel`: the variable, sector and fuel columns of the sector blocks (sections 5-8), so `SUMIFS(block{...}(t),SecVar,"co2",SecFuel,f)` is the sum of `co2` over every subsector for fuel f. `X[<price position>](t)`: variable X of the price block of the row's price fuel and sector (section 2).

## A. Equations in model order

### 0

**E1. `infl`: Inflation index: US CPI, ResultsYear = 1 (nominal -> real for domestic prices and nominal policy inputs)** (index)

- Description: WEO USA|pcpi: CPI(ResultsYear) / CPI(year)
- Legacy: legacy Mitigation rows 456 / 725 (inflation index, 2026 = 100)
  - 2022-2041: `infl(t) = CPIRes/INDEX(WEOVal,MATCH("USA|pcpi",WEOKey,0),MATCH(year,WEOYear,0))`

**E2. `defl`: Deflator index: US GDP deflator, ResultsYear = 1 (nominal -> real for international prices)** (index)

- Description: WEO USA|ngdp_d: deflator(ResultsYear) / deflator(year)
- Legacy: legacy Mitigation row 467 (row 630 = 1 / it)
  - 2022-2041: `defl(t) = DeflRes/INDEX(WEOVal,MATCH("USA|ngdp_d",WEOKey,0),MATCH(year,WEOYear,0))`

**E3. `gdp.usd`: Real GDP, baseline** (USD bn)

- Description: Sheet WEO (EGY|gdp_usd); v0.3.13: header row
- Legacy: legacy Mitigation row 465
- Rows: all,all
  - 2022-2041: `gdp.usd(t) = INDEX(WEOVal,MATCH(CtryCode&"|gdp_usd",WEOKey,0),MATCH(year,WEOYear,0))`

**E4. `gdp.lcu`: Real GDP, baseline, local currency** (LCU bn)

- Description: Sheet WEO (EGY|gdp_lcu); header row (v0.3.13)
- Legacy: legacy Mitigation row 464
- Rows: all,all
  - 2022-2041: `gdp.lcu(t) = INDEX(WEOVal,MATCH(CtryCode&"|gdp_lcu",WEOKey,0),MATCH(year,WEOYear,0))`
- Rows: all,all
  - 2022-2041: `gdp.lcu(t) = gdp.lcu[f,s](t)`

**E5. `xr`: Exchange rate implied by real GDP (local currency per USD; constant in real terms)** (LCU/USD)

- Description: gdp.lcu / gdp.usd (header row, v0.3.13)
- Legacy: legacy Mitigation rows 464-465
- Rows: all,all
  - 2022-2041: `xr(t) = gdp.lcu[f,s](t)/gdp.usd[f,s](t)`
- Rows: all,all
  - 2022-2041: `xr(t) = xr[f,s](t)`

**E6. `gdp.pos.pct`: Real GDP growth (after the GDP feedback of section 16)** (%)

- Description: (1 + gdp.base) x gdp.lvl / gdp.lvl(t-1) - 1
- Legacy: legacy Mitigation row 2446 (fixed: L24)
- Changes against legacy: LD54, L24 (section B)
  - 2022: `gdp.pos.pct(t) = gdp.base[all,all](t)`
  - 2023-2041: `gdp.pos.pct(t) = (1+gdp.base[all,all](t))*gdp.lvl[all,all](t)/gdp.lvl[all,all](t-1)-1`

### 1

**E7. `CPIntro`: Carbon pricing start year** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 18
  - 2022-2041: `CPIntro(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E8. `CPLevelStart`: Starting carbon price** (nom. USD/tCO2)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 19
  - 2022-2041: `CPLevelStart(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E9. `CPLevelTarget`: Target level of carbon price** (nom. USD/tCO2)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 20
  - 2022-2041: `CPLevelTarget(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E10. `CPOutro`: Year to reach target level** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 21
  - 2022-2041: `CPOutro(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E11. `ExtendCarbonPriceBeyondOutro`: Price pathway continues to rise after target year?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 265
  - 2022-2041: `ExtendCarbonPriceBeyondOutro(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E12. `NomorReal`: Tax pathway is in nominal or real terms?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 266
  - 2022-2041: `NomorReal(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E13. `cp.t`: Carbon price path: years since the start year (held at the target year unless the path continues linearly)** (years)

- Description: IF(Extend = Linear*, year, MIN(year, CPOutro)) - CPIntro
- Legacy: legacy row 2248
  - 2022-2041: `cp.t(t) = IF(ExtendCarbonPriceBeyondOutro(t)="Linear*",year,MIN(year,CPOutro(t)))-CPIntro(t)`

**E14. `cp.nom`: Carbon price inputs: nominal-to-real factor** (factor)

- Description: CPI index if NomorReal = Nominal, else 1
- Legacy: legacy row 2249
  - 2022-2041: `cp.nom(t) = IF(LEFT(NomorReal(t),7)="Nominal",infl(t),1)`

**E15. `ExemptPhaseout`: Apply exemption phaseout?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 49
  - 2022-2041: `ExemptPhaseout(t) = INDEX(ScenarioDefinition!J1:AZ511,<p1>,MATCH(scenario(t),ScenarioDefinition!J5:AZ5,0))`
  - Parameters: `<p1>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E16. `YearPha`: Year to start exemption phaseout (if applicable)** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 50
  - 2022-2041: `YearPha(t) = INDEX(ScenarioDefinition!J1:AZ511,<p1>,MATCH(scenario(t),ScenarioDefinition!J5:AZ5,0))`
  - Parameters: `<p1>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E17. `ExemptPhaseoutPeriod`: Period to reach full exemption phaseout (if applicable)** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 51
  - 2022-2041: `ExemptPhaseoutPeriod(t) = INDEX(ScenarioDefinition!J1:AZ511,<p1>,MATCH(scenario(t),ScenarioDefinition!J5:AZ5,0))`
  - Parameters: `<p1>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E18. `exph`: Exemption phase-out: share of an uncovered fuel or sector taxed** (share)

- Description: policy scenarios with ExemptPhaseout = TRUE, from CPIntro: MAX(MIN((year + 1 - YearPha) / ExemptPhaseoutPeriod, 1), 0) (v0.5.6)
- Legacy: legacy rows 2259-2265 (rule chosen for every row, L94)
  - 2022-2041: `exph(t) = IF(AND(scenario(t)>1,ExemptPhaseout(t)=TRUE,year>=CPIntro(t)),MAX(MIN((year+1-YearPha(t))/ExemptPhaseoutPeriod(t),1),0),0)`

**E19. `ctcov`: Carbon tax coverage (Apply tax?)** (switch)

- Description: MTInputs (scenario column); v0.5.6: if not covered, exph
- Legacy: MTInputs MCov* rows 23-47; biomass has no switch (EF 0)
- Changes against legacy: LD13 (section B)
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all, all,pow, all,rod, all,ral, ... (26 rows)
  - 2022-2041: `ctcov(t) = IF(MTInputs[code](scenario),1,exph(t))`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E20. `fpr.yr0`: Fuel price reform: starting year** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 140
  - 2022-2041: `fpr.yr0(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E21. `fpr.yr1`: Fuel price reform: target year** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 141
  - 2022-2041: `fpr.yr1(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E22. `fpr.s`: Fuel price reform: starting price increase** (price unit)

- Description: MTInputs (scenario column)
- Legacy: MTInputs rows 142-155
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, ecy,res, ecy,ind, gso,all, die,all, lpg,all, ker,all, ... (14 rows)
  - 2022-2041: `fpr.s(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E23. `fpr.f`: Fuel price reform: final price increase** (price unit)

- Description: MTInputs (scenario column)
- Legacy: MTInputs rows 156-169
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, ecy,res, ecy,ind, gso,all, die,all, lpg,all, ker,all, ... (14 rows)
  - 2022-2041: `fpr.f(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E24. `fprj`: Fuel price reform: linear increase per year** (price unit)

- Description: FPRSLOPE
- Legacy: legacy rows 167-180 J
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, ecy,res, ecy,ind, gso,all, die,all, lpg,all, ker,all, ... (14 rows)
  - 2022-2041: `fprj(t) = IF(fpr.yr1(t)>fpr.yr0(t),(fpr.f[f,s](t)-fpr.s[f,s](t))/(fpr.yr1(t)-fpr.yr0(t)),0)`

**E25. `fprk`: Fuel price reform: annual rate of increase (Percentage continuation)** (share)

- Description: FPRRATE
- Legacy: legacy rows 167-180 K
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, ecy,res, ecy,ind, gso,all, die,all, lpg,all, ker,all, ... (14 rows)
  - 2022-2041: `fprk(t) = IF(AND(fpr.yr1(t)>fpr.yr0(t),MAX(fpr.s[f,s](t),fpr.f[f,s](t))>0),(fpr.f[f,s](t)/IF(fpr.s[f,s](t)>0,fpr.s[f,s](t),fpr.s[f,s](t)+fprj[f,s](t)))^(1/(fpr.yr1(t)-fpr.yr0(t)))-1,0)`

**E26. `fprp`: Fuel price reform: value of the year before the target year** (price unit)

- Description: FPRBASE
- Legacy: legacy rows 167-180 (column before the target year)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, ecy,res, ecy,ind, gso,all, die,all, lpg,all, ker,all, ... (14 rows)
  - 2022-2041: `fprp(t) = fpr.s[f,s](t)+fprj[f,s](t)*MAX(fpr.yr1(t)-fpr.yr0(t)-1,0)`

**E27. `fpra`: Fuel price reform: value after the target year (Percentage: rate; No: held)** (price unit)

- Description: FPRAFTER
- Legacy: legacy rows 167-180 (L171, L173 fixed)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, ecy,res, ecy,ind, gso,all, die,all, lpg,all, ker,all, ... (14 rows)
  - 2022-2041: `fpra(t) = IF(ExtendCarbonPriceBeyondOutro(t)="Percentage",fprp[f,s](t)*(1+fprk[f,s](t))^(year-fpr.yr1(t)+1),IF(fpr.yr1(t)>fpr.yr0(t),fpr.f[f,s](t),fpr.s[f,s](t)))`

**E28. `fpr`: Fuel price reform: price increase path** (price unit)

- Description: Linear to the target; after it linear (Linear*), annual rate (Percentage) or held (No); FPRPATH
- Legacy: legacy rows 167-180 (v0.9.0; L171, L173 fixed)
- Changes against legacy: LD10, LD18 (section B)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, ecy,res, ecy,ind, gso,all, die,all, lpg,all, ker,all, ... (14 rows)
  - 2022-2041: `fpr(t) = IF(year<fpr.yr0(t),0,IF(OR(year<fpr.yr1(t),ExtendCarbonPriceBeyondOutro(t)="Linear*"),fpr.s[f,s](t)+fprj[f,s](t)*(year-fpr.yr0(t)),fpra[f,s](t)))`

**E29. `scc`: Social cost of carbon: target-consistent, Ricke national and global, manual, US EPA; selected national and global** (USD/tCO2 real)

- Description: Target: SCCTgt x (1 + SCCGr) ^ (year - SCCTgtYr); Ricke (sheet SCC) and EPA: base-year value x (1 + SCCGr) ^ (year - base year); manual: data; selected: CHOOSE by NSCCSrc / GSCCSrc
- Legacy: legacy rows 17671-17713, sheet SCC; v0.3.17
- Rows: tgt,all
  - 2022-2041: `scc(t) = SCCTgt*(1+SCCGr)^(year-SCCTgtYr)`
- Rows: rkn,all
  - 2022-2041: `scc(t) = INDEX(SCCVal,MATCH(RickeN,SCCKey,0))*(1+SCCGr)^(year-BaseYr)`
- Rows: rkg,all
  - 2022-2041: `scc(t) = INDEX(SCCVal,MATCH(RickeG,SCCKey,0))*(1+SCCGr)^(year-BaseYr)`
- Rows: man,all
  - 2022-2041: `scc(t) = INDEX(SCCManVal,MATCH(year,SCCManYear,0))`
- Rows: epa,all
  - 2022-2041: `scc(t) = SCCEpa*(1+SCCGr)^(year-BaseYr)`
- Rows: nat,all
  - 2022-2041: `scc(t) = CHOOSE(MATCH(LEFT(NSCCSrc,1),{"T","R","M","U","E"},0),scc[tgt,s](t),scc[rkn,s](t),scc[man,s](t),scc[epa,s](t),scc[epa,s](t))`
- ... and 1 further row patterns (see the workbook)

**E30. `AddEfficientTaxes`: Add Pigouvian tax on top?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 217
  - 2022-2041: `AddEfficientTaxes(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E31. `ClimateEffTax`: Include climate externality in Pigouvian tax?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 216
  - 2022-2041: `ClimateEffTax(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E32. `AddEfficientTaxesPhaseInYears`: Years to phase in Pigouvian tax?** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 212
  - 2022-2041: `AddEfficientTaxesPhaseInYears(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E33. `ExternalityAddVAT`: Externalities are part of VAT base for optimal taxes?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 218
  - 2022-2041: `ExternalityAddVAT(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E34. `pig.phi`: Pigouvian tax: phase-in share** (share)

- Description: MIN(MAX(year - CPIntro + 1, 0) / MAX(AddEfficientTaxesPhaseInYears, 1), 1) (R3.1)
- Legacy: legacy row 146 (L195, L196 fixed)
  - 2022-2041: `pig.phi(t) = MIN(MAX(year-CPIntro(t)+1,0)/MAX(AddEfficientTaxesPhaseInYears(t),1),1)`

**E35. `pig.efw`: Emission-factor path weight (EFEndYear factors), as section 15 ap.w** (share)

- Description: EFFinShare x (year - BaseYr) / (EFEndYear - BaseYr) (v0.9.0 PIGAP)
- Legacy: legacy rows 1052-1663 (EF path)
  - 2022-2041: `pig.efw(t) = EFFinShare*(year-BaseYr)/(EFEndYear-BaseYr)`

**E36. `pig.vpm`: Value of averted modelled ambient PM2.5 for the marginal damages** (USD bn per ug/m3)

- Description: FromAirPollution air.vpm of the year; 2022: 2023 (legacy has no change in PM2.5 in 2022, so no value) (v0.9.0 PIGAP)
- Legacy: legacy AP rows 3217, 981, 1814
  - 2022-2041: `pig.vpm(t) = IFERROR(INDEX(ApVal,MATCH(CtryCode&"|air.vpm",ApKey,0),MATCH(MAX(year,BaseYr+1),ApYear,0)),0)`

**E37. `airpol.mc`: Marginal air-pollution damage per GJ of the fuel in the subsector (power: by plant type)** (USD/GJ)

- Description: pig.vpm x (D x (1 - pig.efw) + E x pig.efw) x Billion / PJperKtoe / Million: value of averted PM2.5 x sum over pollutants of coefficient of the module sector x emission factor (v0.9.0 PIGAP; legacy average damages, I104 fixed)
- Legacy: legacy AP rows 442-522, 974-981, 3217 (module); Mitigation rows 1052-1663 (EF)
- Rows: coa,mch, coa,irn, coa,nfm, coa,mac, coa,cem, coa,omn, coa,cst, coa,ftr, coa,res, coa,foo, coa,srv, coa,pow, ... (97 rows)
  - 2022-2041: `airpol.mc(t) = pig.vpm(t)*(<ug/m3 per ktoe, base-year EF>*(1-pig.efw(t))+<ug/m3 per ktoe, EFEndYear EF>*pig.efw(t))*Billion/PJperKtoe/Million`
  - Parameters: `<ug/m3 per ktoe, base-year EF>` = `IFERROR(SUMPRODUCT(INDEX(ApEf,MATCH(CtryCode&"|oth|0",ApEfKey,0),0),Inputs!AG68:AT68),0)`; `<ug/m3 per ktoe, EFEndYear EF>` = `IFERROR(SUMPRODUCT(INDEX(ApEf,MATCH(CtryCode&"|oth|1",ApEfKey,0),0),Inputs!AG68:AT68),0)`; `<base-year fuel use (ktoe; weight)>` = `Inputs!X68`

**E38. `pig.trk`: Transport1 row of the country's base year** (row)

- Description: MATCH(country|BaseYr, Transport1 key) (v0.9.0 PIGAP)
- Legacy: legacy rows 2017-2121 (data year)
  - 2022-2041: `pig.trk(t) = <row>`
  - Parameters: `<row>` = `IFERROR(MATCH(CtryCode&"|"&BaseYr,TrKey,0),0)`

**E39. `pig.fe0`: Base-year fuel economy of the road fuel (pas: passenger and light by ownership; all: with 2-3 wheelers or freight by fuel share)** (km/l)

- Description: pas: (FE pas x own pas + FE light x own light) / (own pas + own light) (legacy trfem); all: w x FE pas + (1 - w) x D, w = pig.wsh (legacy AVGFE with data shares) (v0.9.0 PIGAP)
- Legacy: legacy rows 2034-2121, 5356, 5360
- Rows: gso,pas, die,pas
  - 2022-2041: `pig.fe0(t) = IF(<Transport1 value 3>+<Transport1 value 4>=0,<Transport1 value 1>,(<Transport1 value 1>*<Transport1 value 3>+<Transport1 value 2>*<Transport1 value 4>)/(<Transport1 value 3>+<Transport1 value 4>))`
  - Parameters: `<Transport1 value 1>` = `IF(<row of pig.trk>=0,0,INDEX(TrVal,<row of pig.trk>,MATCH("fuel economy gasoline passenger",TrVar,0))+0)`; `<Transport1 value 2>` = `IF(<row of pig.trk>=0,0,INDEX(TrVal,<row of pig.trk>,MATCH("fuel economy light",TrVar,0))+0)`; `<Transport1 value 3>` = `IF(<row of pig.trk>=0,0,INDEX(TrVal,<row of pig.trk>,MATCH("ownership passenger",TrVar,0))+0)`; `<Transport1 value 4>` = `IF(<row of pig.trk>=0,0,INDEX(TrVal,<row of pig.trk>,MATCH("ownership light",TrVar,0))+0)`
- Rows: gso,all, die,all
  - 2022-2041: `pig.fe0(t) = pig.wsh[f,rod](t)*pig.fe0[f,pas](t)+(1-pig.wsh[f,rod](t))*<Transport1 value 1>`
  - Parameters: `<Transport1 value 1>` = `IF(<row of pig.trk>=0,0,INDEX(TrVal,<row of pig.trk>,MATCH("fuel economy gasoline cycle",TrVar,0))+0)`

**E40. `pig.wsh`: Base-year passenger and light share of the road use of the fuel (Transport1 fuel shares; diesel without buses)** (share)

- Description: gasoline: 1 - cycle share; diesel: 1 - freight / (1 - bus) (v0.9.0 PIGAP)
- Legacy: legacy rows 2017-2031; 15723-15730 (weights)
- Rows: gso,rod
  - 2022-2041: `pig.wsh(t) = 1-<Transport1 share 1>`
  - Parameters: `<Transport1 share 1>` = `IF(<row of pig.trk>=0,0,INDEX(TrVal,<row of pig.trk>,MATCH("share of gasoline for cycle",TrVar,0))+0)`
- Rows: die,rod
  - 2022-2041: `pig.wsh(t) = IF(<Transport1 share 1>>=1,0,1-<Transport1 share 2>/(1-<Transport1 share 1>))`
  - Parameters: `<Transport1 share 1>` = `IF(<row of pig.trk>=0,0,INDEX(TrVal,<row of pig.trk>,MATCH("share of diesel for bus",TrVar,0))+0)`; `<Transport1 share 2>` = `IF(<row of pig.trk>=0,0,INDEX(TrVal,<row of pig.trk>,MATCH("share of diesel for freight",TrVar,0))+0)`

**E41. `pig.mu0`: Base-year driving share of the response of the fuel** (share)

- Description: (D + w x E) / (F + w x G), w = pig.wsh (gasoline: eps_U / (eps_U + eps_F)) (v0.9.0 PIGAP, R1.8)
- Legacy: legacy rows 15721-15730
- Rows: gso,rod
  - 2022-2041: `pig.mu0(t) = IF(<eps_U diesel (gasoline: eps_U)>+<eps_U gasoline - diesel (gasoline: eps_F)>=0,0,<eps_U diesel (gasoline: eps_U)>/(<eps_U diesel (gasoline: eps_U)>+<eps_U gasoline - diesel (gasoline: eps_F)>))`
  - Parameters: `<eps_U diesel (gasoline: eps_U)>` = `Inputs!P7`; `<eps_U gasoline - diesel (gasoline: eps_F)>` = `Inputs!Q7`
- Rows: die,rod
  - 2022-2041: `pig.mu0(t) = IFERROR((<eps_U diesel (gasoline: eps_U)>+pig.wsh[f,s](t)*<eps_U gasoline - diesel (gasoline: eps_F)>)/(<eps_U + eps_F diesel>+pig.wsh[f,s](t)*<eps_U + eps_F gasoline - diesel>),0)`
  - Parameters: `<eps_U diesel (gasoline: eps_U)>` = `Inputs!P8`; `<eps_U gasoline - diesel (gasoline: eps_F)>` = `Inputs!P7-Inputs!P8`; `<eps_U + eps_F diesel>` = `Inputs!P8+Inputs!Q8`; `<eps_U + eps_F gasoline - diesel>` = `Inputs!P7+Inputs!Q7-Inputs!P8-Inputs!Q8`

**E42. `pig.rsh0`: Base-year road share of the fuel (subsector use)** (share)

- Description: base-year road use / base-year use of all subsectors (Inputs; power use not counted) (v0.9.0 PIGAP)
- Legacy: legacy rows 15768-15786
- Rows: gso,rod, die,rod
  - 2022-2041: `pig.rsh0(t) = IF(<use of all subsectors (ktoe)>=0,0,<road use (ktoe)>/<use of all subsectors (ktoe)>)`
  - Parameters: `<road use (ktoe)>` = `Inputs!X7`; `<use of all subsectors (ktoe)>` = `SUMIF(Inputs!B5:B148,"gso",Inputs!X5:X148)`

**E43. `pig.kpl`: Base-year driving-weighted km per litre of all use** (km/l)

- Description: pig.fe0 x pig.mu0 x pig.rsh0 (v0.9.0 PIGAP)
- Legacy: legacy Transport rows 186-237 (factors)
- Rows: gso,rod, die,rod
  - 2022-2041: `pig.kpl(t) = pig.fe0[f,all](t)*pig.mu0[f,s](t)*pig.rsh0[f,s](t)`

**E44. `pig.trg.acc`: Growth of the accident cost per vehicle-km relative to the base year** (ratio)

- Description: a(year) / a(BaseYr) (FromTransportCB) (v0.9.0 PIGAP)
- Legacy: legacy Transport row 185
  - 2022-2041: `pig.trg.acc(t) = IF(<base-year value (USD/km)>=0,0,INDEX(TcbVal,<row>,MATCH(year,TcbYear,0))/<base-year value (USD/km)>)`
  - Parameters: `<data key>` = `data`; `<row>` = `IFERROR(MATCH(CtryCode&<data key>,TcbKey,0),0)`; `<base-year value (USD/km)>` = `IF(<row>=0,0,INDEX(TcbVal,<row>,MATCH(BaseYr,TcbYear,0)))`

**E45. `pig.trg.con`: Growth of the congestion cost per vehicle-km relative to the base year** (ratio)

- Description: k(year) / k(BaseYr) (FromTransportCB) (v0.9.0 PIGAP)
- Legacy: legacy Transport row 220
  - 2022-2041: `pig.trg.con(t) = IF(<base-year value (USD/km)>=0,0,INDEX(TcbVal,<row>,MATCH(year,TcbYear,0))/<base-year value (USD/km)>)`
  - Parameters: `<data key>` = `data`; `<row>` = `IFERROR(MATCH(CtryCode&<data key>,TcbKey,0),0)`; `<base-year value (USD/km)>` = `IF(<row>=0,0,INDEX(TcbVal,<row>,MATCH(BaseYr,TcbYear,0)))`

**E46. `pig.trg.rdm`: Growth of the road damage cost per freight vehicle-km relative to the base year (constant)** (ratio)

- Description: r(year) / r(BaseYr) (FromTransportCB) (v0.9.0 PIGAP)
- Legacy: legacy Transport row 232
  - 2022-2041: `pig.trg.rdm(t) = IF(<base-year value (USD/km)>=0,0,INDEX(TcbVal,<row>,MATCH(year,TcbYear,0))/<base-year value (USD/km)>)`
  - Parameters: `<data key>` = `data`; `<row>` = `IFERROR(MATCH(CtryCode&<data key>,TcbKey,0),0)`; `<base-year value (USD/km)>` = `IF(<row>=0,0,INDEX(TcbVal,<row>,MATCH(BaseYr,TcbYear,0)))`

**E47. `pig.trb.acc`: Base-year accident cost per litre** (USD/l)

- Description: a(BaseYr) x pig.kpl (v0.9.0 PIGAP)
- Legacy: legacy Transport rows 322, 324 (base year)
- Rows: gso,rod, die,rod
  - 2022-2041: `pig.trb.acc(t) = <base-year value (USD/km) of pig.trg.acc>*pig.kpl[f,s](t)`

**E48. `pig.trb.con`: Base-year congestion cost per litre** (USD/l)

- Description: k(BaseYr) x pig.kpl (v0.9.0 PIGAP)
- Legacy: legacy Transport rows 333, 335 (base year)
- Rows: gso,rod, die,rod
  - 2022-2041: `pig.trb.con(t) = <base-year value (USD/km) of pig.trg.con>*pig.kpl[f,s](t)`

**E49. `pig.trb.rdm`: Base-year road damage cost per litre** (USD/l)

- Description: r(BaseYr) x pig.kpl x (1 - pig.wsh) (v0.9.0 PIGAP)
- Legacy: legacy Transport row 344 (base year)
- Rows: die,rod
  - 2022-2041: `pig.trb.rdm(t) = <base-year value (USD/km) of pig.trg.rdm>*pig.kpl[f,s](t)*(1-pig.wsh[f,s](t))`

**E50. `pig.ap`: Pigouvian tax component: air-pollution cost per price unit (marginal damages)** (USD per price unit)

- Description: airpol.mc of the subsectors of the fuel and sector group weighted by base-year fuel use x GJ per price unit (other oil products: power cost x GJ per barrel, L194 fixed); residential coal x [base-year coal > ApCoalResMin x buildings use]; electricity, biomass 0 (R3.4, issue I119; v0.9.0 PIGAP: marginal, I104 fixed)
- Legacy: legacy rows 113-123
- Rows: coa,pow, nga,pow
  - 2022-2041: `pig.ap(t) = airpol.mc[f,s](t)*<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `data`
- Rows: coa,res
  - 2022-2041: `pig.ap(t) = IFERROR(SUMPRODUCT(airpol.mc[3 rows](t),airpol.mc[3 rows](F))/SUM(airpol.mc[3 rows](F)),AVERAGE(airpol.mc[3 rows](t)))*<GJ per price unit>*<residential coal switch (base year)>`
  - Parameters: `<GJ per price unit>` = `data`; `<residential coal switch (base year)>` = `--(SUM(airpol.mc[3 rows](F))>ApCoalResMin*SUM(Inputs!X41:X67))`
- Rows: coa,ind, nga,ind
  - 2022-2041: `pig.ap(t) = IFERROR(SUMPRODUCT(airpol.mc[8 rows](t),airpol.mc[8 rows](F))/SUM(airpol.mc[8 rows](F)),AVERAGE(airpol.mc[8 rows](t)))*<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `data`
- Rows: nga,res
  - 2022-2041: `pig.ap(t) = IFERROR(SUMPRODUCT(airpol.mc[3 rows](t),airpol.mc[3 rows](F))/SUM(airpol.mc[3 rows](F)),AVERAGE(airpol.mc[3 rows](t)))*<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `data`
- Rows: ecy,res, ecy,ind, bio,all
  - 2022-2041: `pig.ap(t) = 0`
- Rows: gso,all, die,all, lpg,all, ker,all
  - 2022-2041: `pig.ap(t) = IFERROR(SUMPRODUCT(airpol.mc[16 rows](t),airpol.mc[16 rows](F))/SUM(airpol.mc[16 rows](F)),AVERAGE(airpol.mc[16 rows](t)))*<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `<GJ per price unit of pset[f,s]>`
- ... and 1 further row patterns (see the workbook)

**E51. `cc.code`: Pigouvian tax component: climate damage per price unit (national SCC x generic EF)** (USD per price unit)

- Description: scc.nat x generic EF (tCO2/GJ, Inputs_ef, not calibrated) x GJ per price unit (R3.2-R3.3, issue I116)
- Legacy: legacy rows 136-142, 17678-17684
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, ecy,res, ecy,ind
  - 2022-2041: `cc.code(t) = scc[nat,all](t)*<generic EF (tCO2/GJ)>*<GJ per price unit>`
  - Parameters: `<generic EF (tCO2/GJ)>` = `IFERROR(INDEX(EFGen,MATCH(f,EFGenKey,0)),0)`; `<GJ per price unit>` = `<GJ per price unit of pset[f,s]>`
- Rows: gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `cc.code(t) = scc[nat,s](t)*<generic EF (tCO2/GJ)>*<GJ per price unit>`
  - Parameters: `<generic EF (tCO2/GJ)>` = `IFERROR(INDEX(EFGen,MATCH(f,EFGenKey,0)),0)`; `<GJ per price unit>` = `<GJ per price unit of pset[f,s]>`

**E52. `pig.tr`: Pigouvian tax component: road transport externalities per litre (base-year value x growth)** (USD per price unit)

- Description: pig.trb.acc x pig.trg.acc + pig.trb.con x pig.trg.con (+ pig.trb.rdm x pig.trg.rdm for diesel); 0 for other fuels (R3.5, issue I118; v0.9.0 PIGAP: proxy of scenario 1, issue I151)
- Legacy: legacy rows 128-133 (Transport I322-I344)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, ecy,res, ecy,ind, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `pig.tr(t) = 0`
- Rows: gso,all
  - 2022-2041: `pig.tr(t) = pig.trb.acc[f,rod](t)*pig.trg.acc(t)+pig.trb.con[f,rod](t)*pig.trg.con(t)`
- Rows: die,all
  - 2022-2041: `pig.tr(t) = pig.trb.acc[f,rod](t)*pig.trg.acc(t)+pig.trb.con[f,rod](t)*pig.trg.con(t)+pig.trb.rdm[f,rod](t)*pig.trg.rdm(t)`

**E53. `pigx`: Pigouvian tax per price unit (before the AddEfficientTaxes switch)** (USD per price unit)

- Description: pig.phi x (pig.ap + cc.code x [ClimateEffTax = Yes] + pig.tr) (R3.6)
- Legacy: legacy rows 148-160
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, ecy,res, ecy,ind, gso,all, die,all, lpg,all, ker,all, ... (14 rows)
  - 2022-2041: `pigx(t) = pig.phi(t)*(pig.ap[f,s](t)+cc.code[f,s](t)*(LEFT(ClimateEffTax(t),3)="Yes")+pig.tr[f,s](t))`

**E54. `ntxg`: Gross new excise: fuel price reform + Pigouvian tax if AddEfficientTaxes** (USD per price unit)

- Description: fpr + pigx x [AddEfficientTaxes = Yes] (R3.7; the manual fossil excise is not built)
- Legacy: legacy rows 205-215
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, ecy,res, ecy,ind, gso,all, die,all, lpg,all, ker,all, ... (14 rows)
  - 2022-2041: `ntxg(t) = fpr[f,s](t)+pigx[f,s](t)*(LEFT(AddEfficientTaxes(t),3)="Yes")`

**E55. `xcpb`: Change in existing carbon pricing of the price block** (USD/GJ)

- Description: generic EF x (carbon tax x factor + ETS x factor - embedded level) of the block's ECP sector | fuel (R3.8)
- Legacy: legacy rows 8824-8825 of each block
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `xcpb(t) = <generic EF (tCO2/GJ)>*(INDEX(XCTVal,<ECP table row (sector | fuel)>,xct.c(t))*xct.p(t)+INDEX(XETSVal,<ECP table row (sector | fuel)>,xct.c(t))*xets.p(t)-<embedded existing pricing ($/tCO2)>)`
  - Parameters: `<generic EF (tCO2/GJ)>` = `IFERROR(INDEX(EFGen,MATCH(f,EFGenKey,0)),0)`; `<ECP table row (sector | fuel)>` = `IFERROR(MATCH("pow|coa",XKey,0),1)`; `<embedded existing pricing ($/tCO2)>` = `INDEX(XCTVal,<ECP table row (sector | fuel)>,ECPEmb)+INDEX(XETSVal,<ECP table row (sector | fuel)>,ECPEmb)`
- Rows: ecy,res, ecy,ind
  - 2022-2041: `xcpb(t) = 0`

**E56. `xpre`: Existing taxes before new policy of the price block** (USD/GJ)

- Description: txo + pcsw + ppcw (section 2 block) + xcpb (R3.8)
- Legacy: legacy rows 8821-8825 of each block
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `xpre(t) = txo[f,s](t)+pcsw[f,s](t)+ppcw[f,s](t)+xcpb[f,s](t)`
- Rows: ecy,res, ecy,ind
  - 2022-2041: `xpre(t) = 0`

**E57. `ntxb`: New excise of the price block (read by ntx and the power cost ccp)** (USD per price unit)

- Description: [scenario > 1] x (ntxg, or MIN(ntxg, MAX(0, ntxg - xpre x GJ per unit)) if AddEfficientTaxes) (R3.9, issue I113)
- Legacy: legacy rows 8782, 8805, ... 9012
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, ecy,res, ecy,ind, gso,all, die,all, lpg,all, ker,all, ... (14 rows)
  - 2022-2041: `ntxb(t) = (scenario(t)>1)*IF(LEFT(AddEfficientTaxes(t),3)="Yes",MIN(ntxg[f,s](t),MAX(0,ntxg[f,s](t)-xpre[f,s](t)*<GJ per price unit>)),ntxg[f,s](t))`
  - Parameters: `<GJ per price unit>` = `<GJ per price unit of pset[f,s]>`

**E58. `NewETS`: Apply new ETS?** (No)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 84
  - 2022-2041: `NewETS(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E59. `ETSChangeRelStart`: Change Relative to Baseline in Start Year** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 85
  - 2022-2041: `ETSChangeRelStart(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E60. `ETSChangeRelTarget`: Change Relative to Baseline in Target Year** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 86
  - 2022-2041: `ETSChangeRelTarget(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E61. `ETSCapCont`: Cap continuation after target year?** (Constant)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 87
  - 2022-2041: `ETSCapCont(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E62. `ETSIntro`: ETS Start Year** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 88
  - 2022-2041: `ETSIntro(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E63. `ETSOutro`: ETS Target Year** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 89
  - 2022-2041: `ETSOutro(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E64. `ETSAuctStart`: Proportion Auctioned in Starting Year** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 90
  - 2022-2041: `ETSAuctStart(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E65. `ETSAuctTarget`: Proportion Auctioned in Target Year** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 91
  - 2022-2041: `ETSAuctTarget(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E66. `ETSPriceOverride`: Override ETS price** (No)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 93
  - 2022-2041: `ETSPriceOverride(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E67. `ETSVolatility`: ETS Volatility** (Medium*)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 95
  - 2022-2041: `ETSVolatility(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E68. `ETSVolImpact`: Impact of Volatility on Abatement Costs** (Medium*)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 96
  - 2022-2041: `ETSVolImpact(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E69. `ETSCTRisk`: Carbon Tax Policy Risk** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 97
  - 2022-2041: `ETSCTRisk(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E70. `ets.on`: New ETS applied and started (1/0)** (0/1)

- Description: NewETS = Yes and year >= ETSIntro
- Legacy: new
  - 2022-2041: `ets.on(t) = IF(AND(LEFT(NewETS(t),3)="Yes",year>=ETSIntro(t)),1,0)`

**E71. `etscov`: ETS sector coverage (Apply?)** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs rows 99-115
- Rows: all,pow, all,rod, all,ral, all,avi, all,nav, all,res, all,foo, all,srv, all,mch, all,irn, all,nfm, all,mac, ... (17 rows)
  - 2022-2041: `etscov(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E72. `etsc`: Effective ETS coverage (new ETS applied, started, sector covered)** (0/1)

- Description: Calculation
- Legacy: new
- Rows: all,pow, all,rod, all,ral, all,avi, all,nav, all,res, all,foo, all,srv, all,mch, all,irn, all,nfm, all,mac, ... (17 rows)
  - 2022-2041: `etsc(t) = IF(ets.on(t)=1,IF(etscov[f,s](t),1,0),0)`

**E73. `etsb.s`: ETS benchmark at the start year (share of emission intensity allocated free)** (share)

- Description: 1 - ETSAuctStart (FREESHARE)
- Legacy: legacy rows 1806, 1863-1864 (MTInputs row 90; v0.4.15)
- Rows: all,pow, all,tra, all,res, all,ind
  - 2022-2041: `etsb.s(t) = 1-ETSAuctStart(t)`

**E74. `etsb.t`: ETS benchmark at the target year (share of emission intensity allocated free)** (share)

- Description: 1 - ETSAuctTarget (FREESHARE)
- Legacy: legacy rows 1807, 1863-1864 (MTInputs row 91; v0.4.15)
- Rows: all,pow, all,tra, all,res, all,ind
  - 2022-2041: `etsb.t(t) = 1-ETSAuctTarget(t)`

**E75. `etsb`: ETS benchmark path** (share)

- Description: Linear from ETSIntro to ETSOutro, flat after
- Legacy: new
- Changes against legacy: LD7 (section B)
- Rows: all,pow, all,tra, all,res, all,ind
  - 2022-2041: `etsb(t) = IF(year<ETSIntro(t),0,etsb.s[f,s](t)+(etsb.t[f,s](t)-etsb.s[f,s](t))/MAX(ETSOutro(t)-ETSIntro(t),1)*(MIN(year,ETSOutro(t))-ETSIntro(t)))`

**E76. `obr`: ETS output-based (OBR) share = benchmark (auctioned share = 1 - OBR)** (share)

- Description: MIN(1, MAX(0, benchmark of the sector group))
- Legacy: legacy rows 1863-1864 (one auctioned proportion)
- Changes against legacy: LD7 (section B)
- Rows: all,pow, all,rod, all,ral, all,avi, all,nav, all,res, all,foo, all,srv, all,mch, all,irn, all,nfm, all,mac, ... (17 rows)
  - 2022-2041: `obr(t) = MIN(1,MAX(0,INDEX(etsb[4 rows](t),<ETS group (Constants)>)))`
  - Parameters: `<ETS group (Constants)>` = `INDEX(CovEtsPos,MATCH(s,CovKey,0))`; `<semi-elasticity (Constants)>` = `INDEX(ETSSemiVal,MATCH(CtryCode,ETSSemiKey,0),INDEX(CovSemiPos,MATCH(s,CovKey,0)))`

**E77. `bco2`: Baseline CO2 by ETS sector (data from scenario 1)** (MtCO2)

- Description: Values of scenario 1 co2.sec
- Legacy: legacy rows 1888-1919 (baseline emissions)
- Rows: all,pow, all,rod, all,ral, all,avi, all,nav, all,res, all,foo, all,srv, all,mch, all,irn, all,nfm, all,mac, ... (17 rows)
  - 2022-2041: `bco2(t) = INDEX(BaseCO2Val,MATCH(CtryCode&"|"&s,BaseCO2Key,0),MATCH(year,BaseCO2Year,0))`

**E78. `ch4bs`: Methane activity of scenario 1 (downstream gas, biomass use; data)** (ktoe)

- Description: Values of scenario 1 ch4.act (sheet BaselineCO2)
- Legacy: new (v0.6.2, I47)
- Rows: all,dg, all,bm
  - 2022-2041: `ch4bs(t) = INDEX(BaseCO2Val,MATCH(CtryCode&"|"&s,BaseCO2Key,0),MATCH(year,BaseCO2Year,0))`

**E79. `ets.vol`: ETS: assumed annual price volatility (Settings table, label ETSVolatility)** (share)

- Description: Settings row 17
- Legacy: legacy ETS+LTS rows 5-8
- Changes against legacy: LD8 (section B)
  - 2022-2041: `ets.vol(t) = INDEX(Settings[Assumed annual price volatility of the ETS]:F17,MATCH(SUBSTITUTE(ETSVolatility(t),"*",""),Settings[ETS volatility table]:F16,0))`

**E80. `ets.imp`: ETS: abatement cost increase per unit of volatility (Settings table, label ETSVolImpact)** (factor)

- Description: Settings row 18
- Legacy: legacy ETS+LTS rows 5-8
  - 2022-2041: `ets.imp(t) = INDEX(Settings[Abatement cost increase per unit of volatility]:F18,MATCH(SUBSTITUTE(ETSVolImpact(t),"*",""),Settings[ETS volatility table]:F16,0))`

**E81. `ets.vadj`: ETS volatility adjustment (tax-equivalent price per $ of permit price)** (factor)

- Description: (1 + carbon tax policy risk x impact) / (1 + ETS volatility x impact)
- Legacy: legacy row 2191 (1/1.1); ETS+LTS rows 5-9
- Changes against legacy: LD8 (section B)
  - 2022-2041: `ets.vadj(t) = (1+ETSCTRisk(t)*ets.imp(t))/(1+ets.vol(t)*ets.imp(t))`

**E82. `ets.bce`: Baseline covered emissions** (MtCO2)

- Description: SUMPRODUCT(bco2, etsc)
- Legacy: legacy row 1956
  - 2022-2041: `ets.bce(t) = SUMPRODUCT(bco2[17 rows](t),etsc[17 rows](t))`

**E83. `ets.chg`: ETS cap: change relative to baseline covered emissions** (share)

- Description: Linear from ETSChangeRelStart (start year) to ETSChangeRelTarget (target year), flat after
- Legacy: legacy rows 1958-1960
  - 2022-2041: `ets.chg(t) = ETSChangeRelStart(t)+(ETSChangeRelTarget(t)-ETSChangeRelStart(t))/MAX(ETSOutro(t)-ETSIntro(t),1)*(MIN(year,ETSOutro(t))-ETSIntro(t))`

**E84. `ets.cap`: ETS cap** (MtCO2)

- Description: Baseline covered emissions x (1 + change path); constant after the target year if ETSCapCont = Constant
- Legacy: legacy rows 1958-1960
  - 2022-2041: `ets.cap(t) = IF(ets.on(t)=1,IF(AND(year>ETSOutro(t),LEFT(ETSCapCont(t),8)="Constant"),ets.cap(t-1),ets.bce(t)*(1+ets.chg(t))),0)`

**E85. `ets.se`: Effective covered semi-elasticity (allocation effectiveness: auctioned 1, OBR 0.5)** (per USD/tCO2)

- Description: Baseline-weighted semi-elasticities x (1 - 0.5 OBR)
- Legacy: legacy rows 1845, 1866-1867
  - 2022-2041: `ets.se(t) = IF(ets.bce(t)>0,SUMPRODUCT(bco2[17 rows](t),etsc[17 rows](t),SemiEl,1-(1-OBREff)*obr[17 rows](t))/ets.bce(t),0)`

**E86. `ets.est`: ETS price, fast estimate** (USD/tCO2 real)

- Description: LN(cap / baseline) / (semi-elasticity x volatility adjustment)
- Legacy: legacy row 1868 (QuickEstimateOfETSPrices; linear there)
- Changes against legacy: LD6, L15, L16 (section B)
  - 2022-2041: `ets.est(t) = IF(AND(ets.on(t)=1,ets.cap(t)>0,ets.cap(t)<ets.bce(t),ets.se(t)<0,ets.vadj(t)>0),LN(ets.cap(t)/ets.bce(t))/(ets.se(t)*ets.vadj(t)),0)`

**E87. `ets.ovr`: ETS price override (pasted values, e.g. from ets_goalseek.py)** (USD/tCO2 real)

- Description: Typed / pasted values
- Legacy: legacy Manual inputs O15:AB15 (OverrideOfETSPrices)
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)

**E88. `ets.p`: ETS permit price used** (USD/tCO2 real)

- Description: Override row if ETSPriceOverride = Yes (blank: carbon price path), else the fast estimate
- Legacy: legacy row 1873
- Changes against legacy: LD6 (section B)
  - 2022-2041: `ets.p(t) = IF(ets.on(t)=1,IF(LEFT(ETSPriceOverride(t),3)="Yes",IF(ets.ovr(t)="",cptraj(t),ets.ovr(t)),ets.est(t)),0)`

**E89. `ets.pe`: ETS tax-equivalent price (permit price x volatility adjustment)** (USD/tCO2 real)

- Description: ets.p x ets.vadj
- Legacy: legacy row 2191 applied to the ETS price
  - 2022-2041: `ets.pe(t) = ets.p(t)*ets.vadj(t)`

**E90. `ets.rf`: ETS revenue factor (permit price per $ of tax-equivalent price)** (factor)

- Description: 1 / ets.vadj
- Legacy: new
  - 2022-2041: `ets.rf(t) = IF(ets.vadj(t)>0,1/ets.vadj(t),0)`

**E91. `fb.yr0`: Feebates: start date** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 53
  - 2022-2041: `fb.yr0(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E92. `fb.yr1`: Feebates: target date** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 54
  - 2022-2041: `fb.yr1(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E93. `fb.s`: Feebates: starting rate** (USD/tCO2)

- Description: MTInputs (scenario column)
- Legacy: MTInputs rows 56-59
- Rows: all,pow, all,tra, all,res, all,ind
  - 2022-2041: `fb.s(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E94. `fb.t`: Feebates: target rate** (USD/tCO2)

- Description: MTInputs (scenario column)
- Legacy: MTInputs rows 61-64
- Rows: all,pow, all,tra, all,res, all,ind
  - 2022-2041: `fb.t(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E95. `fb`: Feebates: rate path** (USD/tCO2)

- Description: Linear to the target year, flat after (v0.9.0, as legacy)
- Legacy: legacy rows 2000-2004 (L174 fixed)
- Changes against legacy: LD10, LD12 (section B)
- Rows: all,pow, all,tra, all,res, all,ind
  - 2022-2041: `fb(t) = IF(year<fb.yr0(t),0,fb.s[f,s](t)+(fb.t[f,s](t)-fb.s[f,s](t))/MAX(fb.yr1(t)-fb.yr0(t),1)*(MIN(year,fb.yr1(t))-fb.yr0(t)))`

**E96. `fbcov`: Feebates sector coverage (Apply?)** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs rows 66-82
- Rows: all,pow, all,rod, all,ral, all,avi, all,nav, all,res, all,foo, all,srv, all,mch, all,irn, all,nfm, all,mac, ... (17 rows)
  - 2022-2041: `fbcov(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E97. `ScenarioSelected`: Chosen policy** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 13
  - 2022-2041: `ScenarioSelected(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E98. `SPPEffAdjEnergyEfficiencyRegulations`: Energy efficiency regulations** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 247
  - 2022-2041: `SPPEffAdjEnergyEfficiencyRegulations(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E99. `SPPEffAdjVehicleFuelEconomy`: Vehicle fuel economy** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 248
  - 2022-2041: `SPPEffAdjVehicleFuelEconomy(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E100. `SPPEffAdjRes`: Residential efficiency regulations** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 249
  - 2022-2041: `SPPEffAdjRes(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E101. `SPPEffAdjInd`: Industrial efficiency regulations** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 250
  - 2022-2041: `SPPEffAdjInd(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E102. `SPPEffAdjFeebates`: Feebates** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 251
  - 2022-2041: `SPPEffAdjFeebates(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E103. `scn`: Row of the main scenario in the legacy scenario table (Mapping; 0 = not found: explicit pricing)** (row)

- Description: SCNROW(ScenarioSelected)
- Legacy: legacy Mitigation rows 222-262 (v0.4.16, LD9)
  - 2022-2041: `scn(t) = IFERROR(MATCH(ScenarioSelected(t),ScnName,0),0)`

**E104. `cp.exp`: Explicit carbon pricing of the main scenario (1) or shadow pricing (0)** (0/1)

- Description: EXPLICIT(scn)
- Legacy: legacy row 259 "Explicit pricing variant?" (v0.4.16)
  - 2022-2041: `cp.exp(t) = IF(scn(t)=0,1,--(INDEX(ScnExpl,scn(t))="Yes"))`

**E105. `cpx`: Explicit carbon price (the carbon tax rates ctr)** (USD/tCO2 real)

- Description: cptraj x cp.exp
- Legacy: legacy row 2306 (v0.4.16)
  - 2022-2041: `cpx(t) = cptraj(t)*cp.exp(t)`

**E106. `cp.shd`: Shadow carbon price (regulations, feebate scenarios)** (USD/tCO2 real)

- Description: cptraj - cpx
- Legacy: legacy row 2375 "General carbon price" (v0.4.16)
  - 2022-2041: `cp.shd(t) = cptraj(t)-cpx(t)`

**E107. `regadj`: Efficiency adjustment of the scenario's regulation (MTInputs rows 247-251)** (share)

- Description: REGADJ(scn, rows 247-251)
- Legacy: legacy Mitigation F86:F90 (read, never used in legacy: bug L87; v0.4.16)
  - 2022-2041: `regadj(t) = IF(scn(t)=0,0,IF(INDEX(ScnAdj,scn(t))=0,0,INDEX(block@SPPEffAdjEnergyEfficiencyRegulations{SPPEffAdjEnergyEfficiencyRegulations, SPPEffAdjVehicleFuelEconomy, SPPEffAdjRes, SPPEffAdjInd, ... 5 variables}(t),INDEX(ScnAdj,scn(t)))))`

**E108. `regc`: Sector covered by the scenario's regulation** (0/1)

- Description: REGCOVER(scn, sector)
- Legacy: legacy rows 240-257 of the scenario table (v0.4.16)
- Rows: all,pow, all,rod, all,ral, all,avi, all,nav, all,res, all,foo, all,srv, all,mch, all,irn, all,nfm, all,mac, ... (17 rows)
  - 2022-2041: `regc(t) = IF(scn(t)=0,0,--(INDEX(ScnCov,scn(t),<column of the sector in the scenario table>)="Yes"))`
  - Parameters: `<column of the sector in the scenario table>` = `MATCH(s,CovKey,0)`

**E109. `reg`: Regulation shadow price on the efficiency margin** (USD/tCO2)

- Description: cp.shd x regadj x regc
- Legacy: legacy rows 2369-2388 (shp by fuel = shadow carbon price x EF), share C2371 = 0 in legacy (bug L87; v0.4.16)
- Changes against legacy: LD9 (section B)
- Rows: all,pow, all,rod, all,ral, all,avi, all,nav, all,res, all,foo, all,srv, all,mch, all,irn, all,nfm, all,mac, ... (17 rows)
  - 2022-2041: `reg(t) = cp.shd(t)*regadj(t)*regc[f,s](t)`

**E110. `ssc`: Share of the feebate shadow price impacting efficiency** (share)

- Description: Feebate coverage x SPPEffAdjFeebates (MTInputs row 251; v0.4.16, was the constant 1.0)
- Legacy: legacy Mitigation rows 2403-2419: egy.mit.ssc.rod.1
- Rows: all,pow, all,rod, all,ral, all,avi, all,nav, all,res, all,foo, all,srv, all,mch, all,irn, all,nfm, all,mac, ... (17 rows)
  - 2022-2041: `ssc(t) = IF(fbcov[f,s](t),1,0)*SPPEffAdjFeebates(t)`

**E111. `ctr`: New carbon tax rate by sector (not where the new ETS covers the sector)** (USD/tCO2)

- Description: carbon price x sector coverage x (1 - ETS coverage); complementary to an existing ETS: sector coverage = 1 - national ETS sector coverage of the year (v0.4.12)
- Legacy: legacy Mitigation row 2510 (before EF and fuel coverage); rows 2270-2288
- Rows: all,pow, all,rod, all,ral, all,avi, all,nav, all,res, all,foo, all,srv, all,mch, all,irn, all,nfm, all,mac, ... (17 rows)
  - 2022-2041: `ctr(t) = cpx(t)*IF(LEFT(CTaxComplimentaryToETS(t),3)="Yes",1-INDEX(ECPVal,<existing ETS coverage (ECP)>,xct.c(t)),ctcov[f,s](t))*(1-etsc[f,s](t))`
  - Parameters: `<existing ETS coverage (ECP)>` = `MATCH("ees.pow",ECPKey,0)`

**E112. `etr`: New ETS cost in the fuel price by sector (tax-equivalent price, auctioned part)** (USD/tCO2)

- Description: ETS tax-equivalent price x ETS coverage x (1 - OBR share)
- Legacy: legacy ets inside txo (before the EF)
- Rows: all,pow, all,rod, all,ral, all,avi, all,nav, all,res, all,foo, all,srv, all,mch, all,irn, all,nfm, all,mac, ... (17 rows)
  - 2022-2041: `etr(t) = ets.pe(t)*etsc[f,s](t)*(1-obr[f,s](t))`

**E113. `shpx`: Shadow price on the efficiency margin by sector (feebates and regulations x share impacting efficiency + ETS tax-equivalent price x ETS coverage x OBR share)** (USD/tCO2)

- Description: Calculation
- Legacy: legacy rows 2377 (per tCO2 before the EF)
- Rows: all,pow, all,rod, all,ral, all,avi, all,nav, all,res, all,foo, all,srv, all,mch, all,irn, all,nfm, all,mac, ... (17 rows)
  - 2022-2041: `shpx(t) = INDEX(fb[4 rows](t),<feebate sector (Constants)>)*ssc[f,s](t)+reg[f,s](t)+ets.pe(t)*etsc[f,s](t)*obr[f,s](t)`
  - Parameters: `<feebate sector (Constants)>` = `INDEX(CovFbPos,MATCH(s,CovKey,0))`

**E114. `ExistingCTApply`: Apply existing carbon tax (if exists)?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 213
  - 2022-2041: `ExistingCTApply(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E115. `ExistingCTGrowth`: Assumed existing carbon tax growth per annum (real terms)** (%, real)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 214
  - 2022-2041: `ExistingCTGrowth(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E116. `ExistingETSApply`: Apply existing ETS (if exists)?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 208
  - 2022-2041: `ExistingETSApply(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E117. `ExistingETSGrowth`: Existing ETS permit price growth per annum (real terms)** (%, real)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 209
  - 2022-2041: `ExistingETSGrowth(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E118. `CTaxComplimentaryToETS`: New carbon tax complementary to existing ETS coverage** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 210
  - 2022-2041: `CTaxComplimentaryToETS(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E119. `xct.c`: Existing carbon pricing: data column of the year in the Inputs_ecp tables (last data year after)** (index)

- Description: MATCH(MIN(year, last data year), ECP years)
- Legacy: legacy row 1677 (ECP year columns)
  - 2022-2041: `xct.c(t) = MATCH(MIN(year,ECPLast),ECPYear,0)`

**E120. `xct.p`: Existing carbon tax: factor on the data rates** (factor)

- Description: ExistingCTApply x (1 + ExistingCTGrowth)^(years after the last data year); v0.4.12: rates by fuel and coverage by year in Inputs_ecp
- Legacy: legacy rows 1727-1736 (growth after the data), MTInputs 213-214
  - 2022-2041: `xct.p(t) = IF(LEFT(ExistingCTApply(t),3)="Yes",(1+ExistingCTGrowth(t))^MAX(0,year-ECPLast),0)`

**E121. `xets.p`: Existing ETS: factor on the data prices (national and EU ETS)** (factor)

- Description: ExistingETSApply x (1 + ExistingETSGrowth)^(years after the last data year); v0.4.12: national and EU ETS in Inputs_ecp
- Legacy: legacy rows 1680, 1695 (legacy grows the EU ETS with ExistingCTGrowth: bug L61), MTInputs 208-209
  - 2022-2041: `xets.p(t) = IF(LEFT(ExistingETSApply(t),3)="Yes",(1+ExistingETSGrowth(t))^MAX(0,year-ECPLast),0)`

**E122. `ProdSubPh`: Apply producer subsidies phaseout in the policy scenario?** (TRUE/FALSE)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 123
  - 2022-2041: `ProdSubPh(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E123. `YearProdSubPha`: Year to start producer subsidies phaseout (if applicable)** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 124
  - 2022-2041: `YearProdSubPha(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E124. `FFSProdPhaseoutPeriod`: Period to reach full producer subsidies phaseout (if applicable)** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 125
  - 2022-2041: `FFSProdPhaseoutPeriod(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E125. `ShareofProdSubPha`: Share of producer subsidies to phase-out** (%)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 126
  - 2022-2041: `ShareofProdSubPha(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E126. `ProdSubPhaBaseline`: Apply producer subsidies phaseout in the baseline?** (Yes/No)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 127
  - 2022-2041: `ProdSubPhaBaseline(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E127. `FFSProdPhaseoutPeriodBA`: Period to reach full producer subsidies phaseout (baseline)** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 128
  - 2022-2041: `FFSProdPhaseoutPeriodBA(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E128. `ShareOfProdSubPhaBA`: Share of producer subsidies to phase-out in the baseline** (%)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 129
  - 2022-2041: `ShareOfProdSubPhaBA(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E129. `ConsSubPha`: Apply consumer subsidies phaseout?** (TRUE/FALSE)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 131
  - 2022-2041: `ConsSubPha(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E130. `YearConsSubPha`: Year to start consumer subsidies phaseout (if applicable)** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 132
  - 2022-2041: `YearConsSubPha(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E131. `FFPhaseOut`: Period to reach full consumer subsidies phaseout (if applicable)** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 133
  - 2022-2041: `FFPhaseOut(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E132. `ShareOfConsSubPha`: Share of consumer subsidies to phase-out** (%)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 134
  - 2022-2041: `ShareOfConsSubPha(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E133. `ConsSubPhaBaseline`: Apply consumer subsidies phaseout in the baseline?** (Yes/No)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 135
  - 2022-2041: `ConsSubPhaBaseline(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E134. `FFSConsPhaseoutPeriodBA`: Period to reach full consumer subsidies phaseout (baseline)** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 136
  - 2022-2041: `FFSConsPhaseoutPeriodBA(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E135. `ShareofConsSubPhaBA`: Share of consumer subsidies to phase-out in the baseline** (%)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 137
  - 2022-2041: `ShareofConsSubPhaBA(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E136. `PrcContPha`: Apply price controls phaseout?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 191
  - 2022-2041: `PrcContPha(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E137. `YearPrcContPha`: Year to start price controls phaseout (if applicable)** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 192
  - 2022-2041: `YearPrcContPha(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E138. `PrcControlPhaseout`: Period to reach full price controls phaseout (if applicable)** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 193
  - 2022-2041: `PrcControlPhaseout(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E139. `PrcContPhaBaseline`: Apply price controls phaseout in the baseline scenario?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 195
  - 2022-2041: `PrcContPhaBaseline(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E140. `po.on`: Phase-out applies (scenario 1: the baseline switch; others: the policy switch)** (0/1)

- Description: PHASEON / PCON
- Legacy: legacy rows 264-274, I2188-I2201 (v0.4.16, LD18, LD19)
- Rows: all,ps
  - 2022-2041: `po.on(t) = IF(scenario(t)=1,OR(ProdSubPhaBaseline(t)=TRUE,LEFT(ProdSubPhaBaseline(t),3)="Yes"),OR(ProdSubPh(t)=TRUE,LEFT(ProdSubPh(t),3)="Yes"))*1`
- Rows: all,cs
  - 2022-2041: `po.on(t) = IF(scenario(t)=1,OR(ConsSubPhaBaseline(t)=TRUE,LEFT(ConsSubPhaBaseline(t),3)="Yes"),OR(ConsSubPha(t)=TRUE,LEFT(ConsSubPha(t),3)="Yes"))*1`
- Rows: all,pc
  - 2022-2041: `po.on(t) = AND(OR(PrcContPha(t)=TRUE,LEFT(PrcContPha(t),3)="Yes"),OR(scenario(t)>1,OR(PrcContPhaBaseline(t)=TRUE,LEFT(PrcContPhaBaseline(t),3)="Yes")))*1`

**E141. `po.n`: Phase-out period of the scenario** (years)

- Description: PICKSCEN(baseline, policy period)
- Legacy: legacy rows 265, 269, 273
- Rows: all,ps
  - 2022-2041: `po.n(t) = IF(scenario(t)=1,FFSProdPhaseoutPeriodBA(t),FFSProdPhaseoutPeriod(t))`
- Rows: all,cs
  - 2022-2041: `po.n(t) = IF(scenario(t)=1,FFSConsPhaseoutPeriodBA(t),FFPhaseOut(t))`
- Rows: all,pc
  - 2022-2041: `po.n(t) = IF(scenario(t)=1,PrcControlPhaseout(t),PrcControlPhaseout(t))`

**E142. `po.sh`: Share to phase out (price controls: the consumer share, as legacy, issue I48)** (share)

- Description: PHASESHARE: scenario 1 the baseline share, others MAX(baseline, policy)
- Legacy: legacy rows 267, 271
- Rows: all,ps
  - 2022-2041: `po.sh(t) = IF(scenario(t)=1,ShareOfProdSubPhaBA(t),MAX(ShareOfProdSubPhaBA(t),ShareofProdSubPha(t)))`
- Rows: all,cs, all,pc
  - 2022-2041: `po.sh(t) = IF(scenario(t)=1,ShareofConsSubPhaBA(t),MAX(ShareofConsSubPhaBA(t),ShareOfConsSubPha(t)))`

**E143. `pof`: Phase-out factor: share of the original subsidy (or floating tax) kept** (share)

- Description: PHASEOUT: MAX(1 - share, 1 - share x (year - start) / period after the start year)
- Legacy: legacy rows 2213-2216 (same year: legacy lags the fixed subsidy a year, bug L81, fixed)
- Rows: all,ps
  - 2022-2041: `pof(t) = MAX(1-po.sh[f,s](t),IF(po.on[f,s](t)*(year>YearProdSubPha(t)),1-po.sh[f,s](t)*(year-YearProdSubPha(t))/MAX(po.n[f,s](t),1),1))`
- Rows: all,cs
  - 2022-2041: `pof(t) = MAX(1-po.sh[f,s](t),IF(po.on[f,s](t)*(year>YearConsSubPha(t)),1-po.sh[f,s](t)*(year-YearConsSubPha(t))/MAX(po.n[f,s](t),1),1))`
- Rows: all,pc
  - 2022-2041: `pof(t) = MAX(1-po.sh[f,s](t),IF(po.on[f,s](t)*(year>YearPrcContPha(t)),1-po.sh[f,s](t)*(year-YearPrcContPha(t))/MAX(po.n[f,s](t),1),1))`

**E144. `csi`: Consumer subsidy phase-out applies to the price block (MTInputs ConsSubPhaseScope_*, per scenario; v0.5.6)** (switch)

- Description: Constant (prototype: by price fuel | sector)
- Legacy: new (v0.4.16)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `csi(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E145. `csf`: Consumer subsidy factor of the price block** (share)

- Description: INCLFACTOR(csi, pof.cs)
- Legacy: legacy row 2214 (v0.4.16)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `csf(t) = 1-csi[f,s](t)*(1-pof[all,cs](t))`

**E146. `pci`: Price-control phase-out applies to the price block (MTInputs PriceCtrlPhaseScope_*, per scenario; v0.5.6)** (switch)

- Description: Constant (prototype: by price fuel | sector)
- Legacy: new (v0.4.16)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `pci(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E147. `pcf`: Price-control factor of the price block** (share)

- Description: INCLFACTOR(pci, pof.pc)
- Legacy: legacy rows 2216-2217 (v0.4.16)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `pcf(t) = 1-pci[f,s](t)*(1-pof[all,pc](t))`

**E148. `psi`: Producer subsidy phase-out applies to the fuel (MTInputs ProdSubPhaseScope_*, per scenario; v0.5.6)** (switch)

- Description: Constant
- Legacy: new (v0.4.16)
- Rows: coa,all, nga,all, oil,all, bio,all, ecy,all
  - 2022-2041: `psi(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E149. `psf`: Producer subsidy factor of the fuel** (share)

- Description: INCLFACTOR(psi, pof.ps)
- Legacy: legacy row 2213 (v0.4.16)
- Rows: coa,all, nga,all, oil,all, bio,all, ecy,all
  - 2022-2041: `psf(t) = 1-psi[f,s](t)*(1-pof[all,ps](t))`

**E150. `pros`: Producer subsidy of the fuel before the phase-out** (USD m real)

- Description: PRODSUB: Prices_dom mit.pros (USD bn nominal) x CPI factor up to the last price year, then held
- Legacy: legacy rows 825-829 (v0.4.16)
- Rows: coa,all, nga,all, oil,all, bio,all, ecy,all
  - 2022-2041: `pros(t) = IF(year<=LastHist,IFERROR(INDEX(MPU,MATCH(year,MPUYr,0),<Prices_dom column>)+0,0)*infl(t)*MperBn,pros[f,s](t-1))`
  - Parameters: `<Prices_dom column>` = `MATCH("mit.pros."&f&".all",MPUHdr,0)`

**E151. `psd`: Demand spreading the producer subsidy (oil: liters; coal, gas, biomass: GJ)** (liters | GJ)

- Description: oil: world demand x liters per ktoe; coal, gas: average of world demand and domestic consumption x GJ per ktoe; biomass: domestic consumption x GJ per ktoe
- Legacy: legacy rows 717-719, 584-597, 825-829 (v0.6.1, I49)
- Rows: oil,all
  - 2022-2041: `psd(t) = ch4.wd[f,s](t)*Thousand*LitersPerKtoeOil`
- Rows: coa,all
  - 2022-2041: `psd(t) = AVERAGE(ch4.wd[f,s](t)*Thousand,ConsCoa)*MethGJperKtoe`
- Rows: nga,all
  - 2022-2041: `psd(t) = AVERAGE(ch4.wd[f,s](t)*Thousand,ConsGas)*MethGJperKtoe`
- Rows: bio,all
  - 2022-2041: `psd(t) = ConsBio*MethGJperKtoe`

**E152. `psu`: Producer subsidy per unit of the fuel after the phase-out (negative; $/liter oil, $/GJ coal, gas, biomass)** (per unit real)

- Description: PRODSUBUNIT: -pros / demand (oil: world; coal, gas: half world, half domestic; biomass: domestic) up to the last price year, then the last value x psf (v0.9.0, R7.1: the phase-out in the supply cost, as legacy)
- Legacy: legacy rows 825-829, 2213 (v0.6.1, I49)
- Rows: oil,all, coa,all, nga,all, bio,all
  - 2022-2041: `psu(t) = IF(year<=LastHist,IFERROR(-pros[f,s](t)*USDperM/psd[f,s](t),0),INDEX(psu[f,s](..t-1),lastHistCol(t))*psf[f,s](t))`

**E153. `AdditionalEfficiencyRoadVehicle`: Road vehicles** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 243
  - 2022-2041: `AdditionalEfficiencyRoadVehicle(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E154. `AdditionalEfficiencyResidential`: Residential** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 244
  - 2022-2041: `AdditionalEfficiencyResidential(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E155. `AdditionalEfficiencyIndustrial`: Industrial** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 245
  - 2022-2041: `AdditionalEfficiencyIndustrial(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E156. `AlwaysExemptResLPGKer`: Residential LPG/kerosene always exempted** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 268
  - 2022-2041: `AlwaysExemptResLPGKer(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E157. `exf`: Exemption factor of the new policies (1 = taxed, 0 = exempt; v0.5.1)** (factor)

- Description: exf.all: 1 (sheet Constants); exf.res: 0 if AlwaysExemptResLPGKer = Yes (EXEMPTFACTOR; LEFT(switch, 3), so a starred Yes* counts)
- Legacy: legacy rows 5546-5547: IF(AlwaysExemptResLPGKer="Yes",0,new policy x coverage)
- Rows: all,all
  - 2022-2041: `exf(t) = INDEX(ConstVal,MATCH(code&"|"&f&"|"&s,ConstKey,0))`
- Rows: all,res
  - 2022-2041: `exf(t) = IF(LEFT(AlwaysExemptResLPGKer(t),3)="Yes",0,1)`

**E158. `CTforMethane`: Apply carbon tax to methane** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 185
  - 2022-2041: `CTforMethane(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E159. `MPIntro`: Year of methane fee introduction** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 186
  - 2022-2041: `MPIntro(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E160. `MPLevelStart`: Starting methane fee (real USD per ton CO2eq)** (USD per ton of CO2 eq)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 187
  - 2022-2041: `MPLevelStart(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E161. `MPLevelTarget`: Target level of methane fee** (USD per ton of CO2 eq)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 188
  - 2022-2041: `MPLevelTarget(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E162. `MPOutro`: Year to reach target methane fee level** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 189
  - 2022-2041: `MPOutro(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E163. `mfee.p`: Methane fee path** (USD/tCO2e real)

- Description: PATH(MPIntro, MPOutro, MPLevelStart, MPLevelTarget), linear after the target year as legacy
- Legacy: legacy Mitigation rows 2236-2238
  - 2022-2041: `mfee.p(t) = IF(year<MPIntro(t),0,MPLevelStart(t)+(MPLevelTarget(t)-MPLevelStart(t))/MAX(MPOutro(t)-MPIntro(t),1)*(year-MPIntro(t)))`

**E164. `mfee`: Methane fee used** (USD/tCO2e real)

- Description: mfee.p in policy scenarios (scenario number > 1; v0.4.12) + carbon price if CTforMethane = Yes
- Legacy: legacy Mitigation rows 2238-2240
- Changes against legacy: LD46 (section B)
  - 2022-2041: `mfee(t) = mfee.p(t)*(scenario(t)>1)+IF(LEFT(CTforMethane(t),3)="Yes",cptraj(t),0)`

**E165. `AdditionMitigationPoliciesNonEnergy`: Additional mitigation policies in non-energy sectors?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 207
  - 2022-2041: `AdditionMitigationPoliciesNonEnergy(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E166. `IndustrialProcessEmissionsScaleEner`: Industrial process emissions scale with industrial CO2 energy emissions?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 239
  - 2022-2041: `IndustrialProcessEmissionsScaleEner(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E167. `LULUCFAnnualEmissionsDecline`: LULUCF emissions decline at % pa (in absolute value of start year)?** (%)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 240
  - 2022-2041: `LULUCFAnnualEmissionsDecline(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E168. `PowerSubsidyExemptInclude`: Include power subsidies in any phase out?** (Exempt/Include*)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 138
  - 2022-2041: `PowerSubsidyExemptInclude(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E169. `SupplyCostDeltaSubsidy`: Treat over/underestimate of supply costs as subsidy/tax** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 351
  - 2022-2041: `SupplyCostDeltaSubsidy(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E170. `AdditionalEfficiencyPower`: Power** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 242
  - 2022-2041: `AdditionalEfficiencyPower(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E171. `IncElAdj`: Adjust income elasticities for GDP levels?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 262
  - 2022-2041: `IncElAdj(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E172. `EngineerModelProportionOfCovidFactor`: Proportion of GHG adjustment passed on to engineer model power demand** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 372
  - 2022-2041: `EngineerModelProportionOfCovidFactor(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E173. `PowerRebates`: Power Rebate** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 340
  - 2022-2041: `PowerRebates(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E174. `PowerSectorPriceChangePassOn`: Power price: portion of cost change passed-on:** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 341
  - 2022-2041: `PowerSectorPriceChangePassOn(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E175. `AdditionalExcise`: Add additional excise tax (see 'Manual inputs' tab)?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 215
  - 2022-2041: `AdditionalExcise(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E176. `kDispatch`: k Parameter dispatch** (coefficient)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 344
  - 2022-2041: `kDispatch(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E177. `kInvestment`: k Parameter investment** (coefficient)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 345
  - 2022-2041: `kInvestment(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E178. `MinPostSubsidyPowerPrice`: Minimum (post subsidy) generation cost $/kwh real** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 349
  - 2022-2041: `MinPostSubsidyPowerPrice(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E179. `MaximumCoalCF`: Maximum Coal Capacity Factor** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 370
  - 2022-2041: `MaximumCoalCF(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E180. `MaximumGasCF`: Maximum Gas Capacity Factor** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 371
  - 2022-2041: `MaximumGasCF(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E181. `UseSpotFuelPricesInEngineerModel`: Use Spot Fuel Prices in Engineer Power Model** (No*)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 366
  - 2022-2041: `UseSpotFuelPricesInEngineerModel(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E182. `MinimumThermalEfficiency`: Minimum Thermal Efficiency** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 378
  - 2022-2041: `MinimumThermalEfficiency(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E183. `CFOverrideIfBelowWndSol`: Override Capacity Factor if below (Wind and Solar)** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 373
  - 2022-2041: `CFOverrideIfBelowWndSol(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E184. `CFOverrideIfBelowFosOth`: Override Capacity Factor if below (Others)** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 374
  - 2022-2041: `CFOverrideIfBelowFosOth(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E185. `CFOverrideIfAbove`: Override Capacity Factor if below (All)** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 375
  - 2022-2041: `CFOverrideIfAbove(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E186. `WACCSource`: Cost of capital: User-defined, Inc-dep,  or Tech-dep?** (Tech)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 363
  - 2022-2041: `WACCSource(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E187. `WACCUserGlobal`: If Global, what Value?** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 364
  - 2022-2041: `WACCUserGlobal(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E188. `MinimumWACC`: Minimum WACC** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 346
  - 2022-2041: `MinimumWACC(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E189. `RenewableCostDeclineRate`: Renewable Cost Declines** (Medium*)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 365
  - 2022-2041: `RenewableCostDeclineRate(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E190. `HydroDoesntRetire`: Hydro retirement rate set to zero** (Yes)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 348
  - 2022-2041: `HydroDoesntRetire(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E191. `MaxCostBasedEarlyRetirement`: Proportion of coal capacity that can be retired** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 376
  - 2022-2041: `MaxCostBasedEarlyRetirement(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E192. `EarlyRetirementInBaseline`: Allow cost-based coal phaseout in baseline?** (Yes)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 377
  - 2022-2041: `EarlyRetirementInBaseline(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E193. `MaxNonVREAsPCOfTotalGen`: Max new investment in coal/gas/hyd as a percentage of total generation** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 357
  - 2022-2041: `MaxNonVREAsPCOfTotalGen(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E194. `MaxNonNucOreBioAsPCOfTotalGen`: Max new investment oil/nucl/ore/bio as a percentage of total generation** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 358
  - 2022-2041: `MaxNonNucOreBioAsPCOfTotalGen(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E195. `MaxWindSolarScaleup`: User-Defined Setting for VRE Max-Scale up (if used)** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 359
  - 2022-2041: `MaxWindSolarScaleup(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E196. `MaxScaleUpRateCategory`: Max renewable scaleup rate setting** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 360
  - 2022-2041: `MaxScaleUpRateCategory(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E197. `AllocateSTStorageToVRE`: Percent allocation of ST storage costs to VRE** (%)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 386
  - 2022-2041: `AllocateSTStorageToVRE(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E198. `TotalHoursStorageFor100pcVRE`: Total hours short term strorage for 100% VRE** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 387
  - 2022-2041: `TotalHoursStorageFor100pcVRE(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E199. `StorageToInterfaceRatioSTStorage`: kwh storage to kw interface ratio (hours)** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 388
  - 2022-2041: `StorageToInterfaceRatioSTStorage(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E200. `AllocateLTStorageToVRE`: Percent allocation of LT storage costs to VRE** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 390
  - 2022-2041: `AllocateLTStorageToVRE(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E201. `StartingPointWhenLTStorageIsNeeded`: Starting point of long term storage requirement (%VRE)** (%)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 391
  - 2022-2041: `StartingPointWhenLTStorageIsNeeded(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E202. `LongTermStorageFor100pcVRE`: GW electrolyzer per Gwy/y for 100% VRE (%)** (%)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 392
  - 2022-2041: `LongTermStorageFor100pcVRE(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E203. `StorageHoursForLTStorage`: Storage hours for LT storage** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 393
  - 2022-2041: `StorageHoursForLTStorage(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E204. `PPAProportionCoalGas`: Proportion of PPAs in Coal and Gas Generation** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 380
  - 2022-2041: `PPAProportionCoalGas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E205. `PhaseOutCoalAndGasPPAsBaseline`: Phase out any coal and gas PPAs? (Baseline)** (Yes*)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 381
  - 2022-2041: `PhaseOutCoalAndGasPPAsBaseline(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E206. `PhaseOutCoalAndGasPPAsPolicy`: Phase out any coal and gas PPAs? (Policy)** (Yes*)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 382
  - 2022-2041: `PhaseOutCoalAndGasPPAsPolicy(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E207. `YearPPACoalGas`: Phase begins when?** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 383
  - 2022-2041: `YearPPACoalGas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E208. `YearsToPhaseOutPPAs`: Phase out coal and gas PPAs over n years?** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 384
  - 2022-2041: `YearsToPhaseOutPPAs(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E209. `RenewableSubsidyBL`: Baseline renewable energy subsidy, $/kwh nom** ($/kwh nom)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 352
  - 2022-2041: `RenewableSubsidyBL(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E210. `RenSubsidyAddUSDkwh`: New renewable energy subsidy, $/kwh nom** ($/kwh nom)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 353
  - 2022-2041: `RenSubsidyAddUSDkwh(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E211. `RenSubsidyAddPhaseoutYrs`: New renewable energy subsidy, phaseout** (years)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 354
  - 2022-2041: `RenSubsidyAddPhaseoutYrs(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E212. `RenSubsidyAddStartYear`: =MT** (=MT)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 480
  - 2022-2041: `RenSubsidyAddStartYear(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E213. `RenewableSubsidyHydro`: Apply additional RE subsidy to hydroelectric power?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 355
  - 2022-2041: `RenewableSubsidyHydro(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E214. `AdditionalCoalIntangibleCost`: Use Additional Coal Intangible Cost** (Yes*)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 367
  - 2022-2041: `AdditionalCoalIntangibleCost(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E215. `ManualCoalIntangibleCostST`: Manual Coal Intangible Cost (short term)** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 368
  - 2022-2041: `ManualCoalIntangibleCostST(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E216. `ManualCoalIntangibleCostLT`: Manual Coal Intangible Cost (long term)** (-)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 369
  - 2022-2041: `ManualCoalIntangibleCostLT(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E217. `NewInvCoa`: Coal - New Investment Override** (Switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 395
  - 2022-2041: `NewInvCoa(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E218. `NewInvNga`: Natural gas - New Investment Override** (Switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 396
  - 2022-2041: `NewInvNga(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E219. `NewInvOil`: Oil - New Investment Override** (Switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 397
  - 2022-2041: `NewInvOil(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E220. `NewInvNuc`: Nuclear - New Investment Override** (Switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 398
  - 2022-2041: `NewInvNuc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E221. `NewInvWnd`: Wind - New Investment Override** (Switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 399
  - 2022-2041: `NewInvWnd(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E222. `NewInvSol`: Solar - New Investment Override** (Switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 400
  - 2022-2041: `NewInvSol(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E223. `NewInvHyd`: Hydro - New Investment Override** (Switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 401
  - 2022-2041: `NewInvHyd(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E224. `NewInvOre`: Other renewables - New Investment Override** (Switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 402
  - 2022-2041: `NewInvOre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E225. `NewInvBio`: Biomass - New Investment Override** (Switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 403
  - 2022-2041: `NewInvBio(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E226. `NewInvCoaYear`: Coal** (Year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 405
  - 2022-2041: `NewInvCoaYear(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E227. `NewInvNgaYear`: Natural gas** (Year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 406
  - 2022-2041: `NewInvNgaYear(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E228. `NewInvOilYear`: Oil** (Year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 407
  - 2022-2041: `NewInvOilYear(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E229. `NewInvNucYear`: Nuclear** (Year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 408
  - 2022-2041: `NewInvNucYear(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E230. `NewInvWndYear`: Wind** (Year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 409
  - 2022-2041: `NewInvWndYear(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E231. `NewInvSolYear`: Solar** (Year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 410
  - 2022-2041: `NewInvSolYear(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E232. `NewInvHydYear`: Hydro** (Year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 411
  - 2022-2041: `NewInvHydYear(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E233. `NewInvOreYear`: Other renewables** (Year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 412
  - 2022-2041: `NewInvOreYear(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E234. `NewInvBioYear`: Biomass** (Year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 413
  - 2022-2041: `NewInvBioYear(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E235. `cptraj`: Carbon price trajectory used** (USD/tCO2 real)

- Description: Calculation (legacy rows 2248, 2251); x infl if NomorReal = Nominal
- Legacy: legacy Mitigation row 2251: egy.mit.cptraj.1
- Changes against legacy: LD10 (section B)
  - 2022-2041: `cptraj(t) = IF(year<CPIntro(t),0,CPLevelStart(t)+(CPLevelTarget(t)-CPLevelStart(t))/MAX(CPOutro(t)-CPIntro(t),1)*cp.t(t))*cp.nom(t)`

### 2

**E236. `IntEnerPricForeSource`: International energy price forecasts** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 220
  - 2022-2041: `IntEnerPricForeSource(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E237. `IntEnerPricForecastAdjustment`: International energy prices adjustment** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 258
  - 2022-2041: `IntEnerPricForecastAdjustment(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E238. `gp.src`: International prices: source key (MTInputs selector without the *)** (key)

- Description: SUBSTITUTE(IntEnerPricForeSource, "*", "")
- Legacy: MTInputs row 220
  - 2022-2041: `gp.src(t) = SUBSTITUTE(IntEnerPricForeSource(t),"*","")`

**E239. `gp.adj`: International prices: adjustment after the last historical year (1 none, 2 High, 3 Low)** (choice)

- Description: From IntEnerPricForecastAdjustment
- Legacy: MTInputs row 258
  - 2022-2041: `gp.adj(t) = IF(LEFT(IntEnerPricForecastAdjustment(t),4)="High",2,IF(LEFT(IntEnerPricForecastAdjustment(t),3)="Low",3,1))`

**E240. `gpn`: International energy price, nominal, of the chosen source** (source unit)

- Description: Prices_int (1 without commodity key)
- Legacy: legacy Mitigation rows 633-695 (sources by year)
- Rows: oil,int, coa,int, nga,int, one,int
  - 2022-2041: `gpn(t) = IF(<commodity key>="",1,INDEX(PIntVal,MATCH(gp.src(t)&"|"&<commodity key>,PIntKey,0),MATCH(year,PIntYear,0)))`
  - Parameters: `<commodity key>` = `data`

**E241. `gp`: International energy price (real; source and adjustment from MTInputs)** (source unit)

- Description: gpn x defl x High/Low factor after the last historical year
- Legacy: legacy Mitigation rows 633-695 (sources by year)
- Rows: oil,int, coa,int, nga,int, one,int
  - 2022-2041: `gp(t) = IF(<commodity key>="",1,gpn[f,s](t)*defl(t)*IF(year>Settings[Last historical price year],CHOOSE(gp.adj(t),1,<High factor (Constants)>,<Low factor (Constants)>),1))`
  - Parameters: `<commodity key>` = `data`; `<High factor (Constants)>` = `INDEX(ConstVal,MATCH("gp.hi|"&f,ConstKey,0))`; `<Low factor (Constants)>` = `INDEX(ConstVal,MATCH("gp.lo|"&f,ConstKey,0))`

**E242. `pset`: Price parameters of the fuel | sector (D pass-through, E VAT rate, F GJ per price unit, G international price position)** (-)

- Description: Inputs_prices
- Legacy: legacy price coefficients
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<pass-through>` = `INDEX(Inputs!K158:K169,MATCH(f&"."&s,Inputs!A158:A169,0))`; `<VAT rate>` = `INDEX(Inputs!V158:V169,MATCH(f&"."&s,Inputs!A158:A169,0))`; `<GJ per price unit>` = `INDEX(Inputs!G158:G169,MATCH(f&"."&s,Inputs!A158:A169,0))`; `<international price position (gp row)>` = `INDEX(Inputs!F158:F169,MATCH(f&"."&s,Inputs!A158:A169,0))`

**E243. `gpi`: International reference price of the fuel (its commodity, real; ratios drive the supply cost)** (source unit)

- Description: gp row of the international price position (G of the parameter row)
- Legacy: legacy gp of the fuel
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `gpi(t) = INDEX(gp[4 rows](t),<international price position (gp row) of pset[f,s]>)`

**E244. `spf`: Supply cost: fixed part (margins; coal and gas also production cost)** (USD/GJ real)

- Description: Inputs_prices fixsp in the base year, then constant
- Legacy: legacy fixsp; coded prices.py
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022: `spf(t) = INDEX(Inputs!R158:R169,MATCH(f&"."&s,Inputs!A158:A169,0))`
  - 2023-2041: `spf(t) = spf[f,s](t-1)`

**E245. `esubpu`: Existing consumer subsidy per price unit (negative; input for a later per-fuel policy)** (price unit real)

- Description: esub x GJ per price unit
- Legacy: new (units as MTInputs rows 142-169)
- Changes against legacy: LD14 (section B)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `esubpu(t) = esub[f,s](t)*<GJ per price unit of pset[f,s]>`

**E246. `ps`: Producer subsidy of the block after the phase-out (negative; in the supply cost, before taxes)** (USD/GJ real)

- Description: psu of the fuel (G position) x liters per barrel for other oil products / GJ per price unit (v0.9.0, R7.1: psu carries the phase-out factor psf, as legacy O2455 = $J2456 x O2213)
- Legacy: legacy rows 2455-2708 "in which: producer-side subsidies" (v0.6.1, I49; L124, L125 fixed)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `ps(t) = INDEX(psu[4 rows](t),<international price position (gp row) of pset[f,s]>)*IF(f="oop",LitersPerBbl,1)/<GJ per price unit of pset[f,s]>`

**E247. `sp`: Supply cost (pre-tax price)** (USD/GJ real)

- Description: Historical: Inputs_prices; then fixed part spf + floating part x gp(t) / gp(t-1)
- Legacy: legacy Mitigation row 2498: egy.mit.sp.ind.coa.a.1; coded prices.py
- Changes against legacy: LD2, LD4, LD16, L13 (section B)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2024: `sp(t) = INDEX(IPsp,MATCH(f&"."&s,IPKey,0),MATCH(year,IPspY,0))`
  - 2025-2041: `sp(t) = spf[f,s](t)+(sp[f,s](t-1)-spf[f,s](t)-ps[f,s](t-1))*gpi[f,s](t)/gpi[f,s](t-1)+ps[f,s](t)`

**E248. `txf`: Excise and other taxes before the floor (pass-through rule)** (USD/GJ real)

- Description: txo_L + (sp_L - sp) x (1 - pcc) (v0.4.10: L14 fixed); year by year: last year - change in sp x (1 - pcc)
- Legacy: legacy fadtx + cs; coded prices.py
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2024: `txf(t) = txo[f,s](t)`
  - 2025-2041: `txf(t) = txf[f,s](t-1)-(sp[f,s](t)-sp[f,s](t-1))*(1-<pass-through of pset[f,s]>)`

**E249. `txo`: Excise and other taxes (before new policies)** (USD/GJ real)

- Description: Historical: Inputs_prices; then txf, not below the last historical value txo_L if txo_L >= 0 (legacy rule)
- Legacy: legacy txo = fadtx + fixs + cs (+ nce); coded prices.py
- Changes against legacy: LD2, LD4, LD20, L13, L14 (section B)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2024: `txo(t) = INDEX(IPtxo,MATCH(f&"."&s,IPKey,0),MATCH(year,IPtxoY,0))`
  - 2025-2041: `txo(t) = IF(INDEX(txo[f,s](..t-1),lastHistCol(t))>=0,MAX(INDEX(txo[f,s](..t-1),lastHistCol(t)),txf[f,s](t)),txf[f,s](t))`

**E250. `fadtx`: Fixed part of the existing taxes / subsidy (txo): pass-through x txo of the last historical year** (USD/GJ real)

- Description: history: pcc x txo; projection: pcc x txo of the last historical year
- Legacy: legacy rows 2597-2598 of each block (v0.4.16)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2024: `fadtx(t) = <pass-through of pset[f,s]>*txo[f,s](t)`
  - 2025-2041: `fadtx(t) = <pass-through of pset[f,s]>*INDEX(txo[f,s](..t-1),lastHistCol(t))`

**E251. `cs`: Floating part of txo (moves with the supply cost; price controls)** (USD/GJ real)

- Description: txo - txfx
- Legacy: legacy row 2599 of each block (v0.4.16)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `cs(t) = txo[f,s](t)-fadtx[f,s](t)`

**E252. `etx`: Existing excise and other taxes (positive part of txo)** (USD/GJ real)

- Description: max(txo, 0)
- Legacy: legacy fadtx + positive cs (split here by sign)
- Changes against legacy: LD17 (section B)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `etx(t) = MAX(txo[f,s](t),0)`

**E253. `esub`: Existing consumer subsidy (negative part of txo; negative = subsidy)** (USD/GJ real)

- Description: min(txo, 0)
- Legacy: legacy fixs + negative cs (split here by sign)
- Changes against legacy: LD14, LD17 (section B)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `esub(t) = MIN(txo[f,s](t),0)`

**E254. `vat`: VAT payment before new policies** (USD/GJ real)

- Description: (sp + txo) x VAT rate
- Legacy: legacy vat; coded prices.py
- Changes against legacy: LD3, LD5 (section B)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `vat(t) = (sp[f,s](t)+txo[f,s](t))*<VAT rate of pset[f,s]>`

**E255. `pbc`: Retail price before new taxes and subsidies** (USD/GJ real)

- Description: (sp + txo) x (1 + VAT rate)
- Legacy: legacy retail price rp without nce; coded prices.py
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `pbc(t) = (sp[f,s](t)+txo[f,s](t))*(1+<VAT rate of pset[f,s]>)`

**E256. `pnq`: Fuel use of the subsectors priced by the block (weights of the new-policy rows)** (ktoe)

- Description: SUMIFS of the ener rows aligned with the atp rows whose D = block position
- Legacy: new (v0.4.1)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `pnq(t) = SUMIFS(block@ener{ener, co2, ch4, rtx, ... 600 variables}(t),PVar,"atp",PPar,<price position>)`
  - Parameters: `<price position>` = `INDEX(Inputs!E158:E169,MATCH(f&"."&s,Inputs!A158:A169,0))`

**E257. `pctx`: New carbon tax, weighted by subsector fuel use** (USD/GJ real)

- Description: SUMPRODUCT(ctxnew, ener) / pnq
- Legacy: new (v0.4.1)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `pctx(t) = IF(pnq[f,s](t)=0,0,SUMPRODUCT(--(PVar&PPar="atp"&<price position of pnq[f,s]>),block@ctxnew{ctxnew, ets, ntx, nce, ... 600 variables}(t),block@ener{ener, co2, ch4, rtx, ... 600 variables}(t))/pnq[f,s](t))`

**E258. `etsnew`: New ETS cost in the price, weighted by subsector fuel use** (USD/GJ real)

- Description: SUMPRODUCT(ets, ener) / pnq
- Legacy: new (v0.4.1)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `etsnew(t) = IF(pnq[f,s](t)=0,0,SUMPRODUCT(--(PVar&PPar="atp"&<price position of pnq[f,s]>),block@ets{ets, ntx, nce, xcp, ... 600 variables}(t),block@ener{ener, co2, ch4, rtx, ... 600 variables}(t))/pnq[f,s](t))`

**E259. `pntx`: New excise tax (fuel price reform), weighted by subsector fuel use** (USD/GJ real)

- Description: SUMPRODUCT(ntx, ener) / pnq
- Legacy: new (v0.4.1)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `pntx(t) = IF(pnq[f,s](t)=0,0,SUMPRODUCT(--(PVar&PPar="atp"&<price position of pnq[f,s]>),block@ntx{ntx, nce, xcp, xcpd, ... 600 variables}(t),block@ener{ener, co2, ch4, rtx, ... 600 variables}(t))/pnq[f,s](t))`

**E260. `pxcd`: Change in existing carbon pricing, weighted by subsector fuel use** (USD/GJ real)

- Description: SUMPRODUCT(xcpd, ener) / pnq
- Legacy: new (v0.4.1)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `pxcd(t) = IF(pnq[f,s](t)=0,0,SUMPRODUCT(--(PVar&PPar="atp"&<price position of pnq[f,s]>),block@xcpd{xcpd, csw, pcw, atp, ... 600 variables}(t),block@ener{ener, co2, ch4, rtx, ... 600 variables}(t))/pnq[f,s](t))`

**E261. `pcsw`: Consumer subsidy reform wedge of the block (before VAT)** (USD/GJ real)

- Description: SUBREFORM: -(1 - csf) x MIN(txfx, 0)
- Legacy: legacy row 2598 (fixed subsidy x factor; v0.4.16, LD18)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `pcsw(t) = -(1-INDEX(csf[12 rows](t),MATCH(f&"."&s,IPKey,0)))*MIN(fadtx[f,s](t),0)`

**E262. `ppcw`: Price-control phase-out wedge of the block (before VAT)** (USD/GJ real)

- Description: PCREFORM: -(1 - pcf) x txfl
- Legacy: legacy row 2599 (floating part x factor; v0.4.16, LD18)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `ppcw(t) = -(1-INDEX(pcf[12 rows](t),MATCH(f&"."&s,IPKey,0)))*cs[f,s](t)`

**E263. `pvatn`: VAT on the new taxes and subsidies (and the price floor)** (USD/GJ real)

- Description: pnce - (pctx + pets + pntx + pxcd)
- Legacy: new (v0.4.1)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `pvatn(t) = pnce[f,s](t)-SUM(block@pctx{pctx, etsnew, pntx, pxcd, ... 6 variables}(t))`

**E264. `pnce`: Total new policy: new taxes and subsidies incl. VAT, weighted by subsector fuel use** (USD/GJ real)

- Description: rpn - rpb
- Legacy: new (v0.4.1)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `pnce(t) = rpn[f,s](t)-pbc[f,s](t)`

**E265. `rpn`: Retail price incl. new taxes and subsidies (fuel-use weighted average of the after-tax prices atp of the subsectors priced by the block; rpb where they use none)** (USD/GJ real)

- Description: SUMPRODUCT(atp, ener) / pnq over the atp rows with D = block position
- Legacy: new (v0.4.1; legacy F5b by price block)
- Rows: coa,pow, coa,res, coa,ind, nga,pow, nga,res, nga,ind, gso,all, die,all, lpg,all, ker,all, oop,all, bio,all
  - 2022-2041: `rpn(t) = IF(pnq[f,s](t)=0,pbc[f,s](t),SUMPRODUCT(--(PVar&PPar="atp"&<price position of pnq[f,s]>),block@atp{atp, shp, aef, enel, ... 600 variables}(t),block@ener{ener, co2, ch4, rtx, ... 600 variables}(t))/pnq[f,s](t))`
- Rows: coa,ind, nga,ind, oop,all, gso,all, die,all, lpg,all, ker,all
  - 2022-2041: `rpn(t) = rpn[f,s](t)`

**E266. `pav.sp`: Spending on the fuel at after-tax prices (sum over subsectors of atp x fuel use; electricity: rp x consumption, USD m; all energy: USD m)** (USD/GJ x ktoe)

- Description: SUMPRODUCT of the atp and ener rows of sections 5-8
- Legacy: legacy F5b (16293-16352)
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all
  - 2022-2041: `pav.sp(t) = SUMPRODUCT(--(SecVar="atp"),--(SecFuel=f),block{ener, eldem, ctxnew, ets, ... 600 variables}(t),block@nce{nce, xcp, xcpd, csw, ... 603 variables}(t))`
- Rows: ecy,all
  - 2022-2041: `pav.sp(t) = SUMPRODUCT(rp[2 rows](t),cons[2 rows](t))`
- Rows: all,all
  - 2022-2041: `pav.sp(t) = SUMIFS(block{pav.sp, pav.q, pav.uv, pav.spr, ... 11 variables}(t),block{pav.sp, pav.q, pav.uv, pav.spr, ... 11 variables}(A),code,block{pav.sp, pav.q, pav.uv, pav.spr, ... 11 variables}(B),"<>ecy")*Settings[PJ per ktoe]+pav.sp[ecy,s](t)`
- Rows: coa,all, nga,all, oop,all, gso,all, die,all, lpg,all, ker,all, ecy,all
  - 2022-2041: `pav.sp(t) = pav.sp[f,s](t)`

**E267. `pav.q`: Fuel use (sum over subsectors; electricity: consumption, GWh; all energy: ktoe incl. electricity)** (ktoe)

- Description: SUMIFS of the ener rows
- Legacy: legacy F5b
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all
  - 2022-2041: `pav.q(t) = SUMIFS(block{ener, eldem, ctxnew, ets, ... 600 variables}(t),SecVar,"ener",SecFuel,f)`
- Rows: ecy,all
  - 2022-2041: `pav.q(t) = SUM(cons[2 rows](t))`
- Rows: all,all
  - 2022-2041: `pav.q(t) = SUMIFS(block{pav.sp, pav.q, pav.uv, pav.spr, ... 11 variables}(t),block{pav.sp, pav.q, pav.uv, pav.spr, ... 11 variables}(A),code,block{pav.sp, pav.q, pav.uv, pav.spr, ... 11 variables}(B),"<>ecy")+pav.q[ecy,s](t)*GJperkWh/PJperKtoe`

**E268. `pav.uv`: Average price (unit value: spending / fuel use, own quantities of each scenario)** (USD/GJ real)

- Description: pav.sp / pav.q
- Legacy: legacy F5b (consumption-weighted average price)
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all, ecy,all, all,all
  - 2022-2041: `pav.uv(t) = IF(pav.q[f,s](t)=0,0,pav.sp[f,s](t)/pav.q[f,s](t))`

**E269. `pav.spr`: Spending at scenario 1 quantities of the same year** (USD/GJ x ktoe)

- Description: SUMPRODUCT of atp and scenario-1 ener (header row 10)
- Legacy: new (v0.3.10)
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all
  - 2022-2041: `pav.spr(t) = SUMPRODUCT(--(SecVar="atp"),--(SecFuel=f),block{ener, eldem, ctxnew, ets, ... 600 variables}(t),INDEX(block@nce{nce, xcp, xcpd, csw, ... 603 variables}(..t),0,row10(t)))`
- Rows: ecy,all
  - 2022-2041: `pav.spr(t) = SUMPRODUCT(rp[2 rows](t),INDEX(cons[2 rows](..t),0,row10(t)))`
- Rows: all,all
  - 2022-2041: `pav.spr(t) = SUMIFS(block{pav.sp, pav.q, pav.uv, pav.spr, ... 11 variables}(t),block{pav.sp, pav.q, pav.uv, pav.spr, ... 11 variables}(A),code,block{pav.sp, pav.q, pav.uv, pav.spr, ... 11 variables}(B),"<>ecy")*Settings[PJ per ktoe]+pav.spr[ecy,s](t)`

**E270. `pav.las`: Price index against scenario 1 (Laspeyres: scenario 1 quantities; scenario 1 = 1)** (index)

- Description: pav.spr / pav.sp of scenario 1
- Legacy: new (v0.3.10; I31)
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all, ecy,all, all,all
  - 2022-2041: `pav.las(t) = IF(INDEX(pav.sp[f,s](..t),row10(t))=0,0,pav.spr[f,s](t)/INDEX(pav.sp[f,s](..t),row10(t)))`

**E271. `pav.sp0`: Spending at the base-year quantities** (USD/GJ x ktoe)

- Description: SUMPRODUCT of atp and base-year ener
- Legacy: new (v0.3.10)
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all
  - 2022-2041: `pav.sp0(t) = SUMPRODUCT(--(SecVar="atp"),--(SecFuel=f),block{ener, eldem, ctxnew, ets, ... 600 variables}(t),block@nce{nce, xcp, xcpd, csw, ... 603 variables}(2022))`
- Rows: ecy,all
  - 2022-2041: `pav.sp0(t) = SUMPRODUCT(rp[2 rows](t),cons[2 rows](2022))`
- Rows: all,all
  - 2022-2041: `pav.sp0(t) = SUMIFS(block{pav.sp, pav.q, pav.uv, pav.spr, ... 11 variables}(t),block{pav.sp, pav.q, pav.uv, pav.spr, ... 11 variables}(A),code,block{pav.sp, pav.q, pav.uv, pav.spr, ... 11 variables}(B),"<>ecy")*Settings[PJ per ktoe]+pav.sp0[ecy,s](t)`

**E272. `pav.time`: Price index over time (base-year quantities; base year = 1)** (index)

- Description: pav.sp0 / pav.sp of the base year
- Legacy: new (v0.3.10; I31)
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all, ecy,all, all,all
  - 2022-2041: `pav.time(t) = IF(pav.sp[f,s](2022)=0,0,pav.sp0[f,s](t)/pav.sp[f,s](2022))`

**E273. `pav.mix`: Mix effect: unit-value ratio against scenario 1 / price index (1 = no composition change)** (index)

- Description: (pav.uv / pav.uv of scenario 1) / pav.las
- Legacy: new (v0.3.10; I31: legacy F5c mixes both)
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all, ecy,all, all,all
  - 2022-2041: `pav.mix(t) = IF(INDEX(pav.uv[f,s](..t),row10(t))*pav.las[f,s](t)=0,0,pav.uv[f,s](t)/INDEX(pav.uv[f,s](..t),row10(t))/pav.las[f,s](t))`

**E274. `pav.leg`: Average price as legacy F5b (coal, gas: power, residential, industry prices at scenario-1 quantities; electricity: own quantities; oil products: the price of the .all block; others: the unit value)** (USD/GJ real)

- Description: LEGAVG / TOTAL / SHAREOF
- Legacy: legacy rows 16320-16352 (v0.4.15, I31)
- Rows: coa,all, nga,all
  - 2022-2041: `pav.leg(t) = IF(SUM(block@pavl.qr{pavl.qr, pavl.qi, pavl.qp}(t))=0,pav.uv[f,s](t),(rpn[f,res](t)*pavl.qr[f,s](t)+rpn[f,ind](t)*pavl.qi[f,s](t)+pavl.pp[f,s](t)*pavl.qp[f,s](t))/SUM(block@pavl.qr{pavl.qr, pavl.qi, pavl.qp}(t)))`
- Rows: gso,all, die,all, lpg,all, ker,all, oop,all
  - 2022-2041: `pav.leg(t) = rpn[f,s](t)`
- Rows: jfu,all, bio,all, ecy,all, all,all
  - 2022-2041: `pav.leg(t) = IF(pav.q[f,s](t)=0,0,pav.sp[f,s](t)/pav.q[f,s](t))`

**E275. `pav.lidx`: Legacy average price against scenario 1 (scenario 1 = 1; fuels without a legacy average: pav.las)** (index)

- Description: pav.leg / pav.leg of scenario 1
- Legacy: legacy rows 16379-16396 (100 x index; v0.4.15)
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, oop,all, ecy,all
  - 2022-2041: `pav.lidx(t) = IF(INDEX(pav.leg[f,s](..t),row10(t))=0,0,pav.leg[f,s](t)/INDEX(pav.leg[f,s](..t),row10(t)))`
- Rows: jfu,all, bio,all, all,all
  - 2022-2041: `pav.lidx(t) = pav.las[f,s](t)`

**E276. `pav.idx`: Price index reported (Settings C54: Legacy* = pav.lidx, Laspeyres = pav.las)** (index)

- Description: PICKINDEX
- Legacy: new (v0.4.15, I31)
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all, ecy,all, all,all
  - 2022-2041: `pav.idx(t) = IF(LEFT(PavMethod,3)="Leg",pav.lidx[f,s](t),pav.las[f,s](t))`

**E277. `pavl.qr`: Legacy average weights: residential fuel use of scenario 1 (same year)** (ktoe)

- Description: SUBQTY
- Legacy: legacy rows 16296-16309 (v0.4.15)
- Rows: coa,all, nga,all
  - 2022-2041: `pavl.qr(t) = SUMIFS(INDEX(block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(..t),0,row10(t)),block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(A),"ener",block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(B),f)`

**E278. `pavl.qi`: Legacy average weights: fuel use of the 8 industry subsectors, scenario 1 (same year)** (ktoe)

- Description: SUBQTY
- Legacy: legacy rows 16296-16309 (v0.4.15)
- Rows: coa,all, nga,all
  - 2022-2041: `pavl.qi(t) = SUMIFS(INDEX(block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(..t),0,row10(t)),block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(A),"ener",block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(B),f)`

**E279. `pavl.qp`: Legacy average weights: power generation fuel use of scenario 1 (same year)** (ktoe)

- Description: SUMOF
- Legacy: legacy rows 16296-16309 (v0.4.15)
- Rows: coa,all, nga,all
  - 2022-2041: `pavl.qp(t) = SUMIFS(INDEX(pe[9 rows](..t),0,row10(t)),pe[9 rows](B),f)`

**E280. `pavl.pp`: Power fuel price incl. new policies (pre-policy price + policy cost per GJ of the type)** (USD/GJ real)

- Description: PWFUELPRICE
- Legacy: legacy rows 16285-16286 (v0.4.15)
- Rows: coa,all, nga,all
  - 2022-2041: `pavl.pp(t) = pbc[f,pow](t)+IF(pe[f,pow](t)=0,0,gen_mwy[f,pow](t)*MWyMkWh*xac[f,pow](t)/(pe[f,pow](t)*Settings[PJ per ktoe]))`

**E281. `rpe`: Average retail energy price, all energy incl. new taxes and subsidies (summary row of section 2)** (USD/GJ real)

- Description: pav.uv of all energy (price memo)
- Legacy: new (v0.4.1)
- Rows: all,all
  - 2022-2041: `rpe(t) = pav.uv[f,s](t)`

### 3

**E282. `cfu`: Capacity factor used (actual within the CFOverride bounds of the scenario, else the studies value)** (share)

- Description: CFUSED(actual, studies, lower bound (wind and solar or others), upper bound)
- Legacy: legacy A4 W (rows 2999-3007; L53 fixed)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `cfu(t) = IF(AND(<actual capacity factor>>IF(<wind or solar (1/0)>=1,CFOverrideIfBelowWndSol(t),CFOverrideIfBelowFosOth(t)),<actual capacity factor><CFOverrideIfAbove(t)),<actual capacity factor>,<studies capacity factor>)`
  - Parameters: `<actual capacity factor>` = `INDEX(Inputs!AX207:AX215,MATCH(f,Inputs!A207:A215,0))`; `<studies capacity factor>` = `INDEX(Inputs!AY207:AY215,MATCH(f,Inputs!A207:A215,0))`; `<wind or solar (1/0)>` = `INDEX(Inputs!AZ207:AZ215,MATCH(f,Inputs!A207:A215,0))`

**E283. `nuu`: Efficiency used (actual unless below MinimumThermalEfficiency, else the studies value)** (share)

- Description: EFFUSED(actual, studies, minimum)
- Legacy: legacy A4 V (rows 2999-3007)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `nuu(t) = IF(<actual efficiency (-1 without input)><MinimumThermalEfficiency(t),<studies efficiency>,<actual efficiency (-1 without input)>)`
  - Parameters: `<actual efficiency (-1 without input)>` = `INDEX(Inputs!BA207:BA215,MATCH(f,Inputs!A207:A215,0))`; `<studies efficiency>` = `INDEX(Inputs!BB207:BB215,MATCH(f,Inputs!A207:A215,0))`

**E284. `wsel`: WACC option of the scenario (C Country*, T Tech, blank: User, Income* or studies)** (code)

- Description: WACCCODE(WACCSource)
- Legacy: legacy X2988 (D_WACCSource)
  - 2022-2041: `wsel(t) = IF(LEFT(WACCSource(t),7)="Country","C",IF(WACCSource(t)="Tech","T",""))`

**E285. `wfx`: WACC of the options User and Income* (blank otherwise)** (share)

- Description: WACCFIXED(WACCSource, WACCUserGlobal)
- Legacy: legacy R2988:R2996
  - 2022-2041: `wfx(t) = IF(WACCSource(t)="User",WACCUserGlobal(t),IF(LEFT(WACCSource(t),6)="Income",PsIncWacc,""))`

**E286. `wac`: WACC used** (share)

- Description: WACCUSED(option, Country*, Tech, studies, fixed, MinimumWACC)
- Legacy: legacy rows 2988-2996 X (Final WACC)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `wac(t) = IF(wsel(t)="C",<WACC Country*>,IF(wsel(t)="T",<WACC Tech>,MAX(IF(wfx(t)="",<WACC of the studies>,wfx(t)),MinimumWACC(t))))`
  - Parameters: `<WACC Country*>` = `INDEX(Inputs!BC207:BC215,MATCH(f,Inputs!A207:A215,0))`; `<WACC Tech>` = `INDEX(Inputs!BD207:BD215,MATCH(f,Inputs!A207:A215,0))`; `<WACC of the studies>` = `INDEX(Inputs!BE207:BE215,MATCH(f,Inputs!A207:A215,0))`

**E287. `dlf`: Discounted lifetime (annuity factor) at the WACC used** (years)

- Description: (1 - (1 + wacc)^-N) / (1 - (1 + wacc)^-1)
- Legacy: legacy rows 3026-3034 (A6 G)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `dlf(t) = (1-(1+wac[f,s](t))^-<lifetime N>)/(1-(1+wac[f,s](t))^-1)`
  - Parameters: `<lifetime N>` = `INDEX(Inputs!D207:D215,MATCH(f,Inputs!A207:A215,0))`

**E288. `dlfr`: Discounted lifetime of renewables (average of wind and solar)** (years)

- Description: AVERAGE(dlf wind, dlf solar)
- Legacy: legacy row 3883
  - 2022-2041: `dlfr(t) = AVERAGE(dlf[wnd,pow](t),dlf[sol,pow](t))`

**E289. `kwh`: Fuel per kWh generated** (GJ/kWh)

- Description: price-fuel flag x 0.0036 / efficiency used
- Legacy: legacy rows 3385-3393 (D5 factor)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `kwh(t) = <has a price fuel (1/0)>*GJperkWh/nuu[f,s](t)`
  - Parameters: `<has a price fuel (1/0)>` = `INDEX(Inputs!BJ207:BJ215,MATCH(f,Inputs!A207:A215,0))`

**E290. `cap0`: Base-year nameplate capacity (base-year generation / capacity factor used)** (MW)

- Description: gen0 / cfu
- Legacy: legacy A4 Y (rows 2999-3007)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `cap0(t) = IF(cfu[f,s](t)=0,0,<base-year generation>/cfu[f,s](t))`
  - Parameters: `<base-year generation>` = `INDEX(Inputs!AF207:AF215,MATCH(f,Inputs!A207:A215,0))`

**E291. `invs`: New investment setting of the type (MTInputs rows 395-403 of the scenario)** (option)

- Description: INDEX(NewInv rows of section 1, type position)
- Legacy: legacy rows 4061-4069 (L3)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `invs(t) = NewInvCoa[<type position>](t)`
  - Parameters: `<type position>` = `INDEX(Inputs!BN207:BN215,MATCH(f,Inputs!A207:A215,0))`

**E292. `perm`: New investment permitted (Yes / No; If Present*: more than InvPresentShare of base-year capacity)** (Yes/No)

- Description: INVPRESENT(setting, cap0, SUM(cap0))
- Legacy: legacy rows 4061-4069 (L3)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `perm(t) = IF(invs[f,s](t)="If Present*",IF(cap0[f,s](t)/SUM(cap0[9 rows](t))>InvPresentShare,"Yes","No"),invs[f,s](t))`

**E293. `start`: Start year of new investment (MTInputs rows 405-413 of the scenario; hydro rule L54)** (year)

- Description: INVSTART(hydro, base-year generation share, MTInputs year)
- Legacy: legacy rows 4061-4069 (L3; L54 fixed)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `start(t) = IF(AND(<hydro (1/0)>=1,<base-year generation share>>HydInvShare),BaseYr,NewInvCoaYear[<type position>](t))`
  - Parameters: `<type position>` = `INDEX(Inputs!BN207:BN215,MATCH(f,Inputs!A207:A215,0))`; `<hydro (1/0)>` = `INDEX(Inputs!BL207:BL215,MATCH(f,Inputs!A207:A215,0))`; `<base-year generation share>` = `INDEX(Inputs!AQ207:AQ215,MATCH(f,Inputs!A207:A215,0))`

**E294. `scat`: Scale-up rate of the MaxScaleUpRateCategory of the scenario (Power I20:J23)** (share)

- Description: SCALECAT(category)
- Legacy: legacy S85:S91
  - 2022-2041: `scat(t) = IFERROR(INDEX(PowScRate,MATCH(MaxScaleUpRateCategory(t),PowScCat,0)),0)`

**E295. `scv`: Scale-up rate of wind and solar (country default, user defined or the category)** (share)

- Description: SCALEVRE(category, user rate, category rate)
- Legacy: legacy S85:S91
  - 2022-2041: `scv(t) = IF(LEFT(MaxScaleUpRateCategory(t),4)="Ctry",PsScCtry,IF(MaxScaleUpRateCategory(t)="UserDefined",MaxWindSolarScaleup(t),scat(t)))`

**E296. `rate`: Scale-up rate by type (coal, gas, hydro; wind, solar; others)** (share)

- Description: SCALETYPE(flags, MaxNonVRE, wind and solar, MaxNonNucOreBio)
- Legacy: legacy rows 4130-4138 (L8)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `rate(t) = IF(<coal, gas, hydro (1/0)>=1,MaxNonVREAsPCOfTotalGen(t),IF(<wind or solar (1/0)>=1,scv(t),MaxNonNucOreBioAsPCOfTotalGen(t)))`
  - Parameters: `<coal, gas, hydro (1/0)>` = `INDEX(Inputs!BO207:BO215,MATCH(f,Inputs!A207:A215,0))`; `<wind or solar (1/0)>` = `INDEX(Inputs!AZ207:AZ215,MATCH(f,Inputs!A207:A215,0))`

**E297. `rr`: Retirement rate (1 / lifetime; hydro 0 if HydroDoesntRetire = Yes)** (share)

- Description: RETIRERATE(1/N, hydro, HydroDoesntRetire)
- Legacy: legacy rows 4009-4017 (J)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `rr(t) = IF(AND(<hydro (1/0)>=1,HydroDoesntRetire(t)="Yes"),0,<1 / lifetime>)`
  - Parameters: `<1 / lifetime>` = `INDEX(Inputs!BF207:BF215,MATCH(f,Inputs!A207:A215,0))`; `<hydro (1/0)>` = `INDEX(Inputs!BL207:BL215,MATCH(f,Inputs!A207:A215,0))`

**E298. `erf`: Factor on cost-based early coal retirement (scenario 1: 0 unless EarlyRetirementInBaseline = Yes)** (factor)

- Description: EARLYFACTOR(scenario, switch, MaxCostBasedEarlyRetirement)
- Legacy: legacy F3993
  - 2022-2041: `erf(t) = IF(AND(scenario(t)=1,EarlyRetirementInBaseline(t)<>"Yes"),0,MaxCostBasedEarlyRetirement(t))`

**E299. `spot`: Spot fuel prices for power (1 / 0): Settings SpotPow or UseSpotFuelPricesInEngineerModel** (0/1)

- Description: SPOTSWITCH(MTInputs switch)
- Legacy: legacy row 3155 (MTInputs 366)
  - 2022-2041: `spot(t) = --OR(SpotPow="Yes",LEFT(UseSpotFuelPricesInEngineerModel(t),3)="Yes")`

**E300. `ctf`: Capex time-factor scenario of the renewables (low, med, hgh, vhg)** (code)

- Description: DECLINECODE(RenewableCostDeclineRate)
- Legacy: legacy rows 3038-3046
  - 2022-2041: `ctf(t) = IF(RenewableCostDeclineRate(t)="High","hgh",IF(LEFT(RenewableCostDeclineRate(t),1)="V","vhg",LOWER(LEFT(RenewableCostDeclineRate(t),3))))`

**E301. `stm`: Short-term storage: marginal hours allocated to VRE** (hours)

- Description: AllocateSTStorageToVRE x 2 x TotalHoursStorageFor100pcVRE
- Legacy: legacy rows 3871-3873
  - 2022-2041: `stm(t) = AllocateSTStorageToVRE(t)*(StMargFactor*TotalHoursStorageFor100pcVRE(t))`

**E302. `ltu`: Long-term storage: units for 100% VRE allocated to VRE** (factor)

- Description: AllocateLTStorageToVRE x LongTermStorageFor100pcVRE
- Legacy: legacy rows 3876, 3878 (v0.5.4: wired, row 3909)
  - 2022-2041: `ltu(t) = AllocateLTStorageToVRE(t)*LongTermStorageFor100pcVRE(t)`

**E303. `ppa`: PPA share of coal and gas generation (runs at its capacity factor whatever its cost)** (share)

- Description: PPAProportionCoalGas x phase-out factor (Yes or Yes*; baseline switch in scenario 1, policy elsewhere)
- Legacy: legacy rows 2188-2193, 2218, 3801 (issue I54: switch only on "Yes*" and share to phase out typed 1)
  - 2022-2041: `ppa(t) = PPAProportionCoalGas(t)*IF(LEFT(IF(scenario(t)=1,PhaseOutCoalAndGasPPAsBaseline(t),PhaseOutCoalAndGasPPAsPolicy(t)),3)="Yes",MAX(0,1-MAX(0,year-YearPPACoalGas(t))/YearsToPhaseOutPPAs(t)),1)`

**E304. `rnsp`: Renewable subsidy per kWh (negative = subsidy)** (USD/kWh)

- Description: -(base + additional x phase-out factor from its own start year, policy scenarios)
- Legacy: legacy rows 2733-2745 (L107 fixed: own start year; issue I55: nominal inputs used as real)
  - 2022-2041: `rnsp(t) = -(RenewableSubsidyBL(t)+IF(AND(scenario(t)>1,year>=RenSubsidyAddStartYear(t)),RenSubsidyAddUSDkwh(t)*MAX(0,1-(year-RenSubsidyAddStartYear(t))/RenSubsidyAddPhaseoutYrs(t)),0))*infl(t)`

**E305. `rns`: Renewable subsidy by type (negative = subsidy)** (USD/kWh)

- Description: rnsp x (wind, solar, other renewables, biomass; hydro if RenewableSubsidyHydro = Yes)
- Legacy: legacy rows 3143-3152 (A17)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `rns(t) = rnsp(t)*IF(<renewable (1/0)>=1,1,<hydro (1/0)>*(LEFT(RenewableSubsidyHydro(t),3)="Yes"))`
  - Parameters: `<renewable (1/0)>` = `INDEX(Inputs!BP207:BP215,MATCH(f,Inputs!A207:A215,0))`; `<hydro (1/0)>` = `INDEX(Inputs!BL207:BL215,MATCH(f,Inputs!A207:A215,0))`

**E306. `rbs`: Power revenues rebated to electricity users (1 / 0)** (0/1)

- Description: policy scenarios: PowerRebates = Yes or a feebate scenario (scenario table)
- Legacy: legacy rows 261, 2188, J3595
  - 2022-2041: `rbs(t) = --AND(scenario(t)>1,OR(LEFT(PowerRebates(t),3)="Yes",IF(scn(t)=0,FALSE,INDEX(ScnReb,scn(t))="Yes")))`

**E307. `exs`: Electricity excise (scenario Electricity excise)** (USD/kWh)

- Description: grid CO2 intensity (PwGInt) x carbon price
- Legacy: legacy rows 2190, 2253
  - 2022-2041: `exs(t) = IF(OR(scenario(t)=1,scn(t)=0),0,--(INDEX(ScnElx,scn(t))="Yes"))*PwGInt*cptraj(t)`

**E308. `tcf`: Capex time factor (capital cost relative to its level at factor 1)** (factor)

- Description: PowerPaths, decline scenario of the scenario (ctf)
- Legacy: legacy Mitigation rows 3038-3046 (A7)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `tcf(t) = INDEX(PPathVal,MATCH(CtryCode&"|"&<data key>&"|"&ctf(t),PPathKey,0),MATCH(year,PPathYear,0))`
  - Parameters: `<data key>` = `code&"|"&f`

**E309. `cbat`: Battery storage capital cost** (USD/kWh storage)

- Description: PowerPaths
- Legacy: legacy row 3887 (J2)
  - 2022-2041: `cbat(t) = INDEX(PPathVal,MATCH(CtryCode&"|"&<data key>,PPathKey,0),MATCH(year,PPathYear,0))`
  - Parameters: `<data key>` = `code`

**E310. `cint`: Battery interface capital cost** (USD/kW)

- Description: PowerPaths
- Legacy: legacy row 3888 (J2)
  - 2022-2041: `cint(t) = INDEX(PPathVal,MATCH(CtryCode&"|"&<data key>,PPathKey,0),MATCH(year,PPathYear,0))`
  - Parameters: `<data key>` = `code`

**E311. `obat`: Battery storage operating cost** (USD/kWh storage/yr)

- Description: PowerPaths
- Legacy: legacy row 3891 (J2)
  - 2022-2041: `obat(t) = INDEX(PPathVal,MATCH(CtryCode&"|"&<data key>,PPathKey,0),MATCH(year,PPathYear,0))`
  - Parameters: `<data key>` = `code`

**E312. `elcx`: Electrolyser capital cost** (USD/kW)

- Description: PowerPaths
- Legacy: legacy row 3893 (J2)
  - 2022-2041: `elcx(t) = INDEX(PPathVal,MATCH(CtryCode&"|"&<data key>,PPathKey,0),MATCH(year,PPathYear,0))`
  - Parameters: `<data key>` = `code`

**E313. `eltk`: Long-term storage (tank) capital cost per kWh** (USD/kWh)

- Description: PowerPaths
- Legacy: legacy row 3895 (J2)
  - 2022-2041: `eltk(t) = INDEX(PPathVal,MATCH(CtryCode&"|"&<data key>,PPathKey,0),MATCH(year,PPathYear,0))`
  - Parameters: `<data key>` = `code`

**E314. `elof`: Electrolyser fixed opex** (USD/kW/yr)

- Description: PowerPaths
- Legacy: legacy row 3898 (J2)
  - 2022-2041: `elof(t) = INDEX(PPathVal,MATCH(CtryCode&"|"&<data key>,PPathKey,0),MATCH(year,PPathYear,0))`
  - Parameters: `<data key>` = `code`

**E315. `elov`: Electrolyser variable opex** (USD/kWh)

- Description: PowerPaths
- Legacy: legacy row 3899 (J2)
  - 2022-2041: `elov(t) = INDEX(PPathVal,MATCH(CtryCode&"|"&<data key>,PPathKey,0),MATCH(year,PPathYear,0))`
  - Parameters: `<data key>` = `code`

**E316. `cel`: Long-term storage cost per marginal unit (electrolyser and storage capital, fixed and variable opex)** (USD/kWh)

- Description: (elcx + eltk x StorageHoursForLTStorage) / (dlfr x 8,760) + elof / 8,760 + elov (v0.5.4: hours and WACC of the scenario)
- Legacy: legacy rows 3893-3906 (J2)
  - 2022-2041: `cel(t) = (elcx(t)+eltk(t)*StorageHoursForLTStorage(t))/(dlfr(t)*HoursYr)+elof(t)/HoursYr+elov(t)`

**E317. `incp`: Income factor on the GDP elasticities before the switch IncElAdj** (factor)

- Description: PowerPaths
- Legacy: legacy row 2432 (macro block)
  - 2022-2041: `incp(t) = INDEX(PPathVal,MATCH(CtryCode&"|"&<data key>,PPathKey,0),MATCH(year,PPathYear,0))`
  - Parameters: `<data key>` = `code`

**E318. `inc.ela.adj`: Income-dependent factor on the GDP elasticities (power demand and fuel use)** (factor)

- Description: incp if IncElAdj of the scenario starts with Yes, else 1
- Legacy: legacy row 2433 (macro block)
  - 2022-2041: `inc.ela.adj(t) = IF(LEFT(IncElAdj(t),3)="Yes",incp(t),1)`

**E319. `shock`: Exogenous shock on energy demand (legacy calibration 2023-2024; used if Settings C19 = 1)** (share)

- Description: PowerPaths
- Legacy: legacy row 2439
- Changes against legacy: LD24 (section B)
  - 2022-2041: `shock(t) = INDEX(PPathVal,MATCH(CtryCode&"|"&<data key>,PPathKey,0),MATCH(year,PPathYear,0))`
  - Parameters: `<data key>` = `code`

**E320. `cax`: Capital cost of new plants** (USD/kW real)

- Description: cax0 x capex time factor
- Legacy: legacy rows 3099-3107 (A13)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `cax(t) = <cax0 (factor 1)>*tcf[f,s](t)`
  - Parameters: `<cax0 (factor 1)>` = `INDEX(Inputs!C207:C215,MATCH(f,Inputs!A207:A215,0))`

**E321. `caxav`: Weighted average capital cost of the stock (vintages)** (USD/kW real)

- Description: Base year cax; then caxav(t-1) x (1 - phi(t-1)) + cax(t-1) x phi(t-1)
- Legacy: legacy rows 3181-3189 (B2)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022: `caxav(t) = cax[f,s](t)`
  - 2023-2041: `caxav(t) = caxav[f,s](t-1)*(1-phi[f,s](t-1))+cax[f,s](t-1)*phi[f,s](t-1)`

**E322. `stoav`: Weighted average storage cost of the stock (vintages)** (USD/kWh)

- Description: Base year msc x VRE flag; then stoav(t-1) x (1 - phi(t-1)) + msc(t) x VRE flag x phi(t-1)
- Legacy: legacy rows 3225-3233 (B6)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022: `stoav(t) = <VRE flag>*msc(t)`
  - 2023-2041: `stoav(t) = stoav[f,s](t-1)*(1-phi[f,s](t-1))+<VRE flag>*msc(t)*phi[f,s](t-1)`
  - Parameters: `<VRE flag>` = `INDEX(Inputs!O207:O215,MATCH(f,Inputs!A207:A215,0))`

**E323. `fix`: Amortised fixed cost of the existing stock (capital, interest, decommissioning, storage, fixed O&M)** (USD/kWh)

- Description: (caxav x (1/N + wacc/2) + decommissioning/N + fixed opex)/(cf x 8,760) + stoav (WACC, cf of the scenario)
- Legacy: legacy rows 3247-3255 (B8 = B3 + B4 + B5 + B6 + B7)
- Changes against legacy: LD30 (section B)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `fix(t) = (caxav[f,s](t)*(<1 / lifetime>+wac[f,s](t)*CapAvgShr)+<decommissioning / N + fixed opex ($/kW/y)>)/(cfu[f,s](t)*HoursYr)+stoav[f,s](t)`
  - Parameters: `<1 / lifetime>` = `INDEX(Inputs!BF207:BF215,MATCH(f,Inputs!A207:A215,0))`; `<decommissioning / N + fixed opex ($/kW/y)>` = `INDEX(Inputs!BG207:BG215,MATCH(f,Inputs!A207:A215,0))`

**E324. `lfx`: Levelised fixed cost of new plants** (USD/kWh)

- Description: (cax + decommissioning + transmission capex)/(cf x 8,760 x dlf) + fixed opex/(cf x 8,760) + rns + msc x VRE flag (of the scenario)
- Legacy: legacy rows 3326-3334 (C7 = C1 + ... + C6)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `lfx(t) = (cax[f,s](t)+<decommissioning + transmission capex>)/(cfu[f,s](t)*HoursYr*dlf[f,s](t))+<fixed opex ($/kW/y)>/(cfu[f,s](t)*HoursYr)+rns[f,s](t)+<VRE flag>*msc(t)`
  - Parameters: `<decommissioning + transmission capex>` = `INDEX(Inputs!BH207:BH215,MATCH(f,Inputs!A207:A215,0))`; `<fixed opex ($/kW/y)>` = `INDEX(Inputs!BI207:BI215,MATCH(f,Inputs!A207:A215,0))`; `<VRE flag>` = `INDEX(Inputs!O207:O215,MATCH(f,Inputs!A207:A215,0))`

**E325. `cics`: Coal implicit cost chosen, short term (first year of calculations)** (USD/kWh)

- Description: No = 0; Manual = ManualCoalIntangibleCostST; else GoalSeekCoal B by country (name CoalICSTc) (v0.5.6)
- Legacy: legacy J89:J90
  - 2022-2041: `cics(t) = IF(LEFT(AdditionalCoalIntangibleCost(t),1)="N",0,IF(AdditionalCoalIntangibleCost(t)="Manual",ManualCoalIntangibleCostST(t),CoalICSTc))`

**E326. `cicl`: Coal implicit cost chosen, long term (2030)** (USD/kWh)

- Description: No = 0; Manual = ManualCoalIntangibleCostLT; else GoalSeekCoal C by country (CoalICLTc) (v0.5.6)
- Legacy: legacy K89:K90
  - 2022-2041: `cicl(t) = IF(LEFT(AdditionalCoalIntangibleCost(t),1)="N",0,IF(AdditionalCoalIntangibleCost(t)="Manual",ManualCoalIntangibleCostLT(t),CoalICLTc))`

**E327. `cic`: Coal implicit cost (short to long term by 2030)** (USD/kWh)

- Description: AdditionalCoalIntangibleCost: No = 0; Manual = MTInputs ST/LT; else GoalSeekCoal (B, C) by country; weight MIN(1, (t - base year)/(2030 - base year)). Added to the coal variable cost (dispatch, investment); in generation cost and tariffs if PwCoalICTariff = Yes (v0.5.6, P5)
- Legacy: legacy rows 3360-3363 (D3), J89:K90
  - 2022-2041: `cic(t) = cics(t)+(cicl(t)-cics(t))*MIN(1,(year-BaseYr)/(CoalICYr-BaseYr))`

**E328. `fpn`: Fuel price for power before new policies, this year (rpb of the price fuel)** (USD/GJ real)

- Description: BLOCKPRICE: rpb of the price block at the price position
- Legacy: legacy rows 3155-3163 (A18; v0.6.2: own row, so the average below reads one row, not the price-block area)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `fpn(t) = pbc[<price position (section 2)>](t)`
  - Parameters: `<price position (section 2)>` = `INDEX(Inputs!X207:X215,MATCH(f,Inputs!A207:A215,0))`

**E329. `fpp`: Fuel price for power before new policies (trailing 5-year moving average, or spot)** (USD/GJ real)

- Description: spot = 1 (Settings SpotPow or the scenario switch): fpn; else the average of fpn over t-4 .. t within 2022-2041 (v0.6.2, L126) (errors skipped)
- Legacy: legacy rows 3155-3163 (A18; legacy 465: AVERAGE over t-4 .. t from 2022, L126 fixed)
- Changes against legacy: LD31 (section B)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `fpp(t) = IF(spot(t)=1,fpn[f,s](t),AVERAGE(INDEX(fpn[f,s](..t),COLUMN()-MIN(year-BaseYr,PwAvgLag)):fpn[f,s](t)))`

**E330. `xck`: Change in existing carbon pricing against the price data, per kWh generated** (USD/kWh)

- Description: tCO2/kWh x (carbon tax x factor + ETS x factor - embedded; Inputs_ecp tables, row pow | fuel; v0.4.12)
- Legacy: new (legacy: existing pricing is part of txo of power fuels)
- Changes against legacy: LD38 (section B)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `xck(t) = <EF (tCO2/GJ; x kwh)>*kwh[f,s](t)*(INDEX(XCTVal,<ECP table row>,xct.c(t))*xct.p(t)+INDEX(XETSVal,<ECP table row>,xct.c(t))*xets.p(t)-<embedded ($/tCO2)>)`
  - Parameters: `<EF (tCO2/GJ; x kwh)>` = `INDEX(Inputs!Y207:Y215,MATCH(f,Inputs!A207:A215,0))`; `<ECP table row>` = `INDEX(Inputs!AU207:AU215,MATCH(f,Inputs!A207:A215,0))`; `<embedded ($/tCO2)>` = `INDEX(Inputs!AV207:AV215,MATCH(f,Inputs!A207:A215,0))`

**E331. `vbc`: Variable cost before new policies (fuel and variable O&M)** (USD/kWh)

- Description: Variable O&M + fixed fuel cost + fpp (fuel price for power, $/GJ) x kwh + xck
- Legacy: legacy rows 3374-3382 (D4; moving-average fuel prices as legacy A18)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `vbc(t) = <var. O&M + fixed fuel>+fpp[f,s](t)*kwh[f,s](t)+xck[f,s](t)+(f="coa")*cic(t)`
  - Parameters: `<var. O&M + fixed fuel>` = `INDEX(Inputs!V207:V215,MATCH(f,Inputs!A207:A215,0))`; `<price position>` = `INDEX(Inputs!X207:X215,MATCH(f,Inputs!A207:A215,0))`

**E332. `xac`: New policy cost per kWh generated (carbon tax, ETS, fuel price reform)** (USD/kWh)

- Description: tCO2/kWh x (carbon tax rate of power x fuel coverage + ETS cost rate of power; section 1 ctr, etr) + fuel price reform x 0.0036/efficiency/GJ per unit
- Legacy: legacy rows 3385-3393 (D5)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `xac(t) = <EF (tCO2/GJ; x kwh)>*kwh[f,s](t)*(ctr[all,s](t)*INDEX(ctcov[9 rows](t),<fuel position>)+etr[all,s](t))+INDEX(ntxb[14 rows](t),<price-fuel position>)*kwh[f,s](t)/<GJ per price unit>`
  - Parameters: `<EF (tCO2/GJ; x kwh)>` = `INDEX(Inputs!Y207:Y215,MATCH(f,Inputs!A207:A215,0))`; `<fuel position>` = `INDEX(Inputs!AA207:AA215,MATCH(f,Inputs!A207:A215,0))`; `<price-fuel position>` = `INDEX(Inputs!AB207:AB215,MATCH(f,Inputs!A207:A215,0))`; `<GJ per price unit>` = `INDEX(Inputs!AC207:AC215,MATCH(f,Inputs!A207:A215,0))`

**E333. `shk`: Shadow price per kWh generated (power feebates, ETS output-based part)** (USD/kWh)

- Description: shadow price of power (shpx, section 1: feebate rate x share impacting efficiency + ETS tax-equivalent price x ETS coverage x OBR share) x tCO2/kWh
- Legacy: legacy rows 3398-3406 (D6)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `shk(t) = shpx[all,s](t)*<EF (tCO2/GJ; x kwh)>*kwh[f,s](t)`
  - Parameters: `<EF (tCO2/GJ; x kwh)>` = `INDEX(Inputs!Y207:Y215,MATCH(f,Inputs!A207:A215,0))`; `<base-year generation share (rebate)>` = `INDEX(Inputs!AQ207:AQ215,MATCH(f,Inputs!A207:A215,0))`

**E334. `reb`: Feebate rebate per kWh generated (fixed base-year shares; from the second year)** (USD/kWh)

- Description: -SUMPRODUCT(shk, base-year generation shares)
- Legacy: legacy rows 3407-3409 (fixed: per kWh generated, legacy per kWh consumed)
- Changes against legacy: LD23, L9 (section B)
  - 2022: `reb(t) = 0`
  - 2023-2041: `reb(t) = -SUMPRODUCT(shk[9 rows](t),shk[9 rows](E))`

**E335. `tvc`: Total variable cost (dispatch; levelised for investment)** (USD/kWh)

- Description: vbc + ccp + shk + reb
- Legacy: legacy rows 3423-3431 (D7)
- Changes against legacy: L9 (section B)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `tvc(t) = vbc[f,s](t)+xac[f,s](t)+shk[f,s](t)+reb(t)`

**E336. `tvcx`: Total variable cost used in the levelised window (tvc; last year's where the host cannot evaluate the LAMBDA year 2041)** (USD/kWh)

- Description: IFERROR(tvc, tvc(t-1))
- Legacy: new (no-LAMBDA fallback)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `tvcx(t) = IFERROR(tvc[f,s](t),tvc[f,s](t-1))`

**E337. `dsum`: Sum of discount factors from the year to the end of the horizon** (years)

- Description: (1 + wac)^(base year - year) + next year (blank after the last year)
- Legacy: legacy A5 discount factors (row 3012)
- Changes against legacy: LD29 (section B)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `dsum(t) = (1+wac[f,s](t))^(Settings[Base year]-year)+dsum[f,s](t+1)`

**E338. `lvc`: Levelised variable cost: discounted average of tvc from the year to the end of the horizon** (USD/kWh)

- Description: (df x tvc + (dsum - df) x lvc of next year) / dsum (df at the WACC used, wac)
- Legacy: legacy rows 3439-3447 (D9; capacity factors constant)
- Changes against legacy: LD29 (section B)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `lvc(t) = ((1+wac[f,s](t))^(Settings[Base year]-year)*tvcx[f,s](t)+(dsum[f,s](t)-(1+wac[f,s](t))^(Settings[Base year]-year))*lvc[f,s](t+1))/dsum[f,s](t)`

**E339. `gnc`: Generation cost before new policies (cost recovery)** (USD/kWh)

- Description: fix + vbc
- Legacy: legacy rows 3486-3494 (E3)
- Changes against legacy: LD30 (section B)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `gnc(t) = fix[f,s](t)+vbc[f,s](t)-IF(PwCoalICTariff="No",(f="coa")*cic(t),0)`

**E340. `gncav`: Average generation cost (weighted by generation shares)** (USD/kWh)

- Description: SUMPRODUCT(shr, gnc)
- Legacy: legacy row 3495 (E3 weighted average)
  - 2022-2041: `gncav(t) = SUMPRODUCT(shr[9 rows](t),gnc[9 rows](t))*<factor (Constants)>`
  - Parameters: `<factor (Constants)>` = `INDEX(ConstVal,MATCH("pw.c|"&code,ConstKey,0))`

**E341. `ccpav`: Average new policy cost per kWh consumed** (USD/kWh)

- Description: SUMPRODUCT(shr, ccp) x generation / consumption
- Legacy: legacy row 3395 (D5 per kWh consumed)
  - 2022-2041: `ccpav(t) = SUMPRODUCT(shr[9 rows](t),xac[9 rows](t))*<generation / consumption>`
  - Parameters: `<generation / consumption>` = `INDEX(PParVal,MATCH(CtryCode&"|gen_per_cons",PParKey,0))`

**E342. `tic`: Levelised investment cost (levelised fixed + levelised variable)** (USD/kWh)

- Description: MAX(lfx + lvc, MinPostSubsidyPowerPrice)
- Legacy: legacy rows 3463-3471 (E1) = L1
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `tic(t) = MAX(lfx[f,s](t)+lvc[f,s](t),MinPostSubsidyPowerPrice(t))`

**E343. `fce`: Memo: post-tax fuel cost per kWh generated** (USD/kWh)

- Description: fpp x kwh (v0.5.6)
- Legacy: legacy F2-F3 rows 3532-3552
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `fce(t) = fpp[f,s](t)*kwh[f,s](t)`

**E344. `cik`: Memo: carbon intensity of generation** (tCO2/kWh)

- Description: EF x GJ per kWh (v0.5.6)
- Legacy: legacy F4 rows 3554-3557
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `cik(t) = <EF (tCO2/GJ; x kwh) of xac[f,s]>*kwh[f,s](t)`

**E345. `swi`: Memo: switching carbon price, gas over coal, new investment** (USD/tCO2)

- Description: (tic gas - tic coal) / (cik coal - cik gas) (v0.5.6)
- Legacy: legacy F7 row 3571 (F5 = tic)
  - 2022-2041: `swi(t) = IFERROR((tic[nga,pow](t)-tic[coa,pow](t))/(cik[coa,pow](t)-cik[nga,pow](t)),0)`

**E346. `swd`: Memo: switching carbon price, gas over coal, dispatch** (USD/tCO2)

- Description: (tvc gas - tvc coal) / (cik coal - cik gas) (v0.5.6)
- Legacy: legacy F7 row 3572 (F6 = tvc)
  - 2022-2041: `swd(t) = IFERROR((tvc[nga,pow](t)-tvc[coa,pow](t))/(cik[coa,pow](t)-cik[nga,pow](t)),0)`

**E347. `cur`: Memo: current total cost by type** (USD/kWh)

- Description: INVCOST: MAX(lfx + tvc, MinPostSubsidyPowerPrice)
- Legacy: legacy E4 rows 3498-3506
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `cur(t) = MAX(lfx[f,s](t)+tvc[f,s](t),MinPostSubsidyPowerPrice(t))`

**E348. `sys`: Memo: system cost by type (decommissioning, transmission share, storage, coal implicit cost)** (USD/kWh)

- Description: SYSCOST: (dtc + TrCostShare x tcx) / (cfu x 8,760 x dlf) + VRE x msc + coal x cic
- Legacy: legacy F1 rows 3522-3530
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `sys(t) = <decommissioning + transmission share ($/kW)>/(cfu[f,s](t)*HoursYr*dlf[f,s](t))+<VRE flag>*msc(t)+((f="coa")*cic(t))`
  - Parameters: `<decommissioning + transmission share ($/kW)>` = `INDEX(Inputs!BH207:BH215,MATCH(f,Inputs!A207:A215,0))`; `<VRE flag>` = `INDEX(Inputs!O207:O215,MATCH(f,Inputs!A207:A215,0))`

**E349. `pcbcap`: Memo: cost breakdown, capital** (USD/kWh)

- Description: LEVCAPEX: cax / (cfu x 8,760 x dlf)
- Legacy: legacy E5 rows 3509-3517 L (C1)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `pcbcap(t) = cax[f,s](t)/(cfu[f,s](t)*HoursYr*dlf[f,s](t))`

**E350. `pcbom`: Memo: cost breakdown, O&M** (USD/kWh)

- Description: OMCOST: fixed O&M / (cfu x 8,760) + variable O&M
- Legacy: legacy E5 rows 3509-3517 M (A16 + D1)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `pcbom(t) = <fixed O&M ($/kW per year)>/(cfu[f,s](t)*HoursYr)+<variable O&M ($/kWh)>`
  - Parameters: `<fixed O&M ($/kW per year)>` = `INDEX(Inputs!BI207:BI215,MATCH(f,Inputs!A207:A215,0))`; `<variable O&M ($/kWh)>` = `INDEX(Inputs!K207:K215,MATCH(f,Inputs!A207:A215,0))`

**E351. `pcbfu`: Memo: cost breakdown, fuel (incl. the change in existing carbon pricing)** (USD/kWh)

- Description: VARCOST: fixed fuel cost + fpp x kwh + xck
- Legacy: legacy E5 rows 3509-3517 N (D2)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `pcbfu(t) = <fixed fuel cost ($/kWh)>+fpp[f,s](t)*kwh[f,s](t)+xck[f,s](t)`
  - Parameters: `<fixed fuel cost ($/kWh)>` = `INDEX(Inputs!L207:L215,MATCH(f,Inputs!A207:A215,0))`

**E352. `pcbcp`: Memo: cost breakdown, new carbon price** (USD/kWh)

- Description: ccp
- Legacy: legacy E5 rows 3509-3517 P (D5)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `pcbcp(t) = xac[f,s](t)`

**E353. `pcbrns`: Memo: cost breakdown, renewable subsidy** (USD/kWh)

- Description: rns
- Legacy: legacy E5 rows 3509-3517 Q (A17)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `pcbrns(t) = rns[f,s](t)`

**E354. `pcbchk`: Memo: cost breakdown check, parts - current total cost (shadow price, rebate and price floor not a column, I142)** (USD/kWh)

- Description: pcbcap + pcbom + pcbfu + sys + pcbcp + pcbrns - cur
- Legacy: legacy E5 rows 3509-3517 S
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `pcbchk(t) = (pcbcap[f,s](t)+pcbom[f,s](t)+pcbfu[f,s](t)+sys[f,s](t)+pcbcp[f,s](t)+pcbrns[f,s](t))-cur[f,s](t)`

**E355. `pcbct`: Memo: carbon tax of the scenario (0 in scenario 1)** (USD/tCO2 real)

- Description: cptraj x (scenario > 1)
- Legacy: legacy E5 T3509, T9825 (L222 fixed: the block's own scenario)
  - 2022-2041: `pcbct(t) = cptraj(t)*((scenario(t)>1)*1)`

**E356. `cons`: Electricity consumption by price group** (GWh)

- Description: residential: residential demand; industry: total minus residential; x GWh per ktoe
- Legacy: legacy rows 3621, 3650 (G1, G2)
- Rows: ecy,res
  - 2022-2041: `cons(t) = (<weight on total>*demtot(t)+<weight on residential>*dem[f,s](t))*<GWh per ktoe>`
  - Parameters: `<weight on total>` = `INDEX(Inputs!D221:D222,MATCH(s,Inputs!A221:A222,0))`; `<weight on residential>` = `INDEX(Inputs!E221:E222,MATCH(s,Inputs!A221:A222,0))`; `<GWh per ktoe>` = `INDEX(PParVal,MATCH(CtryCode&"|ktoe_gwh",PParKey,0))`
- Rows: ecy,ind
  - 2022-2041: `cons(t) = (<weight on total>*demtot(t)+<weight on residential>*dem[f,res](t))*<GWh per ktoe>`
  - Parameters: `<weight on total>` = `INDEX(Inputs!D221:D222,MATCH(s,Inputs!A221:A222,0))`; `<weight on residential>` = `INDEX(Inputs!E221:E222,MATCH(s,Inputs!A221:A222,0))`; `<GWh per ktoe>` = `INDEX(PParVal,MATCH(CtryCode&"|ktoe_gwh",PParKey,0))`

**E357. `sc`: Supply cost of electricity (average generation cost of the previous year + transmission and distribution)** (USD/kWh)

- Description: gncav(t-1) + T&D add-on; base year gncav(t) + T&D
- Legacy: legacy rows 3600, 3629
- Changes against legacy: LD32 (section B)
- Rows: ecy,res, ecy,ind
  - 2022: `sc(t) = gncav(t)+<T&D add-on>`
  - 2023-2041: `sc(t) = gncav(t-1)+<T&D add-on>`
  - Parameters: `<T&D add-on>` = `INDEX(Inputs!F221:F222,MATCH(s,Inputs!A221:A222,0))`

**E358. `rppre`: Electricity price before new policies (incl. VAT)** (USD/kWh real)

- Description: Data up to the last historical year (x CPI index), then rppre(t-1) + pass-through x (change in sc + pseu + csd + ores) x (1 + VAT) (v0.9.0, R7.9, R9.3)
- Legacy: legacy rows 3613, 3642 (telescoped: held components cancel; pass-through of the scenario)
- Changes against legacy: LD32, LD33 (section B)
- Rows: ecy,res, ecy,ind
  - 2022-2024: `rppre(t) = INDEX(Inputs!J221:M222,<user-group position>,MATCH(year,Inputs!J220:M220,0))`
  - 2025-2041: `rppre(t) = rppre[f,s](t-1)+PowerSectorPriceChangePassOn(t)*(sc[f,s](t)+pseu[f,s](t)+csd[f,s](t)+ores[f,s](t)-(sc[f,s](t-1)+pseu[f,s](t-1)+csd[f,s](t-1)+ores[f,s](t-1)))*(1+<VAT rate>)`
  - Parameters: `<user-group position>` = `INDEX(Inputs!C221:C222,MATCH(s,Inputs!A221:A222,0))`; `<VAT rate>` = `INDEX(Inputs!H221:H222,MATCH(s,Inputs!A221:A222,0))`

**E359. `entxd`: New electricity excise typed on 'Manual inputs' (rows 161-162)** (USD/kWh)

- Description: Manual inputs J:AF of the year (blank = 0)
- Legacy: legacy rows 195-196
- Rows: ecy,res, ecy,ind
  - 2022-2041: `entxd(t) = IFERROR(INDEX(ManExcVal,MATCH(<Manual inputs code>,ManExcKey,0),MATCH(year,ManExcYr,0))+0,0)`
  - Parameters: `<Manual inputs code>` = `"mit.ntx.ecy."&s`

**E360. `entx`: Manual electricity excise of policy scenarios with AdditionalExcise = Yes, plus the electricity fuel price reform (v0.5.6, I59)** (USD/kWh real)

- Description: entxd x (1, or the deflator index if NomorReal is not Real)
- Legacy: legacy rows 199-217, 3602, 3631
- Rows: ecy,res, ecy,ind
  - 2022-2041: `entx(t) = IF(scenario(t)>1,IF(LEFT(AdditionalExcise(t),3)="Yes",entxd[f,s](t)*IF(LEFT(NomorReal(t),4)="Real",1,defl(t)),0)+fpr[f,s](t),0)`

**E361. `pex`: Excise in the electricity price before VAT** (USD/kWh real)

- Description: exs + after the last historical year: pass-through x (entx - entx of the last historical year)
- Legacy: legacy rows 3602-3616, 3631-3645 (the manual excise enters the price before policy, passed through like the supply cost)
- Rows: ecy,res, ecy,ind
  - 2022: `pex(t) = exs(t)`
  - 2023-2041: `pex(t) = exs(t)+IF(year>LastHist,PowerSectorPriceChangePassOn(t)*(entx[f,s](t)-INDEX(entx[f,s](..t-1),lastHistCol(t))),0)`

**E362. `rp`: End-user electricity price** (USD/kWh real)

- Description: MAX(rppre + (ccpav x pass-through x (1 - rbs) + pex) x (1 + VAT), MinPostSubsidyPowerPrice) (v0.5.6: floor, I60)
- Legacy: legacy rows 3614-3617, 3643-3646 (v0.5.4: rebate and excise)
- Changes against legacy: LD32 (section B)
- Rows: ecy,res, ecy,ind
  - 2022-2041: `rp(t) = MAX(rppre[f,s](t)+(ccpav(t)*PowerSectorPriceChangePassOn(t)*(1-rbs(t))+pex[f,s](t))*(1+<VAT rate>),MinPostSubsidyPowerPrice(t))`
  - Parameters: `<VAT rate>` = `INDEX(Inputs!H221:H222,MATCH(s,Inputs!A221:A222,0))`
- Rows: ecy,res, ecy,ind
  - 2022-2041: `rp(t) = rp[f,s](t)`

**E363. `sgap`: Subsidy gap: price before VAT minus supply cost (negative = price below cost, a subsidy)** (USD/kWh)

- Description: rppre / (1 + VAT rate) - sc
- Legacy: new (legacy producer-subsidy and over/under-estimate rows)
- Rows: ecy,res, ecy,ind
  - 2022-2041: `sgap(t) = rppre[f,s](t)/(1+<VAT rate>)-sc[f,s](t)`
  - Parameters: `<VAT rate>` = `INDEX(Inputs!H221:H222,MATCH(s,Inputs!A221:A222,0))`

**E364. `rcarb`: New-policy cost per user group (carbon tax, ETS at the tax-equivalent price, fuel price reform; memo, revenue: prnew in M)** (USD m real)

- Description: ccpav x consumption
- Legacy: legacy power carbon revenue
- Rows: ecy,res, ecy,ind
  - 2022-2041: `rcarb(t) = ccpav(t)*<factor (Constants)>*cons[f,s](t)`
  - Parameters: `<factor (Constants)>` = `INDEX(ConstVal,MATCH("pw.c|"&code,ConstKey,0))`

**E365. `rexs`: Electricity excise revenue, of which the excise of the scenario Electricity excise (carbon-based)** (USD m real)

- Description: exs x total consumption
- Legacy: legacy rows 3664, 7889
  - 2022-2041: `rexs(t) = exs(t)*SUM(cons[2 rows](t))`

**E366. `rexm`: Electricity excise revenue, of which the manual excise (AdditionalExcise)** (USD m real)

- Description: SUM(rpex) - rexs
- Legacy: legacy rows 3660, 7762 (additional excise)
  - 2022-2041: `rexm(t) = SUM(rpex[2 rows](t))-rexs(t)`

**E367. `rvat`: VAT revenue from electricity** (USD m real)

- Description: rppre x VAT/(1 + VAT) x consumption
- Legacy: new
- Rows: ecy,res, ecy,ind
  - 2022-2041: `rvat(t) = rppre[f,s](t)*<VAT share of price>*cons[f,s](t)`
  - Parameters: `<VAT share of price>` = `INDEX(Inputs!I221:I222,MATCH(s,Inputs!A221:A222,0))`

**E368. `rnvat`: VAT on the new-policy cost passed through to electricity users** (USD m real)

- Description: (ccpav x pass-through x (1 - rbs) + pex) x VAT rate x consumption
- Legacy: new
- Changes against legacy: M2 (section B)
- Rows: ecy,res, ecy,ind
  - 2022-2041: `rnvat(t) = (ccpav(t)*PowerSectorPriceChangePassOn(t)*(1-rbs(t))+pex[f,s](t))*<VAT rate>*cons[f,s](t)`
  - Parameters: `<VAT rate>` = `INDEX(Inputs!H221:H222,MATCH(s,Inputs!A221:A222,0))`

**E369. `rreb`: Rebate of the carbon cost to electricity users (negative)** (USD m real)

- Description: -rbs x ccpav x pass-through x consumption
- Legacy: legacy row 3663 (with VAT: rnvat falls by the VAT part)
- Rows: ecy,res, ecy,ind
  - 2022-2041: `rreb(t) = (-rbs(t)*ccpav(t))*PowerSectorPriceChangePassOn(t)*cons[f,s](t)`

**E370. `rpex`: Electricity excise revenue** (USD m real)

- Description: pex x consumption
- Legacy: legacy rows 3660, 3664
- Rows: ecy,res, ecy,ind
  - 2022-2041: `rpex(t) = pex[f,s](t)*cons[f,s](t)`

**E371. `rgap`: Electricity subsidy gap (negative = fiscal cost)** (USD m real)

- Description: sgap x consumption
- Legacy: new
- Rows: ecy,res, ecy,ind
  - 2022-2041: `rgap(t) = sgap[f,s](t)*<factor (Constants)>*cons[f,s](t)`
  - Parameters: `<factor (Constants)>` = `INDEX(ConstVal,MATCH("pw.c|"&code,ConstKey,0))`

**E372. `rpnv`: Electricity price before VAT of the dataset (last price year held)** (USD/kWh real)

- Description: HISTHOLD: retail price (Inputs_power) / (1 + VAT rate)
- Legacy: legacy rows 3575, 3581
- Rows: ecy,res, ecy,ind
  - 2022-2041: `rpnv(t) = IF(year<=LastHist,INDEX(PwRp,<user-group position>,MATCH(year,PwRpYr,0))/(1+<VAT rate>),rpnv[f,s](t-1))`
  - Parameters: `<user-group position>` = `INDEX(Inputs!C221:C222,MATCH(s,Inputs!A221:A222,0))`; `<VAT rate>` = `INDEX(Inputs!H221:H222,MATCH(s,Inputs!A221:A222,0))`

**E373. `txg`: Electricity price gap before VAT: price - supply cost - manual excise** (USD/kWh real)

- Description: PRICEGAP: rpnv - sc - entx
- Legacy: legacy N3605, N3607 terms
- Rows: ecy,res, ecy,ind
  - 2022-2041: `txg(t) = rpnv[f,s](t)-sc[f,s](t)-entx[f,s](t)`

**E374. `txe`: Electricity consumer tax / subsidy (dataset, last price year held)** (USD/kWh real)

- Description: ELTAXBASE: Prices_dom mit.txo.ecy x CPI index; no data: txg if SupplyCostDeltaSubsidy = Yes, else 0
- Legacy: legacy rows 3577, 3583, 3604-3606
- Rows: ecy,res, ecy,ind
  - 2022-2041: `txe(t) = IF(year<=LastHist,IFERROR(INDEX(PwTx,<user-group position>,MATCH(year,PwTxYr,0))+0,txg[f,s](t)*(SupplyCostDeltaSubsidy(t)="Yes")),txe[f,s](t-1))`
  - Parameters: `<user-group position>` = `INDEX(Inputs!C221:C222,MATCH(s,Inputs!A221:A222,0))`

**E375. `scl`: Supply cost of electricity, after the last price year capped at its value then** (USD/kWh real)

- Description: CAPLAST: sc; after the last price year MIN(sc, sc of the last price year)
- Legacy: legacy O3607 (MIN(0, O3600 - $J3600))
- Rows: ecy,res, ecy,ind
  - 2022-2041: `scl(t) = IF(year<=LastHist,sc[f,s](t),MIN(sc[f,s](t),INDEX(scl[f,s](..t-1),lastHistCol(t))))`

**E376. `psegap`: Pre-tax gap of electricity x consumption (allocation of the producer subsidy)** (USD m real)

- Description: PREGAP: MAX(0, sc - (rpnv - txe)) x cons
- Legacy: legacy row 3588 (terms)
- Rows: ecy,res, ecy,ind
  - 2022-2041: `psegap(t) = MAX(0,sc[f,s](t)-(rpnv[f,s](t)-txe[f,s](t)))*cons[f,s](t)`

**E377. `psegs`: Pre-tax gap x consumption, both user groups** (USD m real)

- Description: SUM(psegap)
- Legacy: legacy row 3588 (sum)
  - 2022-2041: `psegs(t) = SUM(psegap[2 rows](t))`

**E378. `psesh`: Share of the electricity producer subsidy to the user group** (share)

- Description: PSALLOC: psegap / psegs, else cons / total, else 1 (residential); held after the last price year
- Legacy: legacy rows 3588-3589
- Rows: ecy,res, ecy,ind
  - 2022-2041: `psesh(t) = IF(year<=LastHist,IFERROR(psegap[f,s](t)/psegs(t),IFERROR(cons[f,s](t)/SUM(cons[2 rows](t)),1-<weight on total demand (fallback: 1 - weight)>)),psesh[f,s](t-1))`
  - Parameters: `<weight on total demand (fallback: 1 - weight)>` = `INDEX(Inputs!D221:D222,MATCH(s,Inputs!A221:A222,0))`

**E379. `pseu`: Electricity producer subsidy per kWh after the phase-out (floored at PsElFloor)** (USD/kWh real)

- Description: PSELEC: MAX(PsElFloor, -pros.ecy x psesh / cons); then the last value x psf.ecy
- Legacy: legacy rows 3590-3591, 3601, 3630 (I146)
- Rows: ecy,res, ecy,ind
  - 2022-2041: `pseu(t) = IF(year<=LastHist,IFERROR(MAX(PsElFloor,-pros[f,all](t)*psesh[f,s](t)/cons[f,s](t)),0),INDEX(pseu[f,s](..t-1),lastHistCol(t))*psf[f,all](t))`

**E380. `pser`: Electricity producer subsidy above the floor (memo, outside prices)** (USD m real)

- Description: PSERESID: -pros.ecy - SUM(cons x pseu); then the last value x psf.ecy
- Legacy: legacy row 3592
  - 2022-2041: `pser(t) = IF(year<=LastHist,-pros[ecy,all](t)-(cons[ecy,res](t)*pseu[ecy,res](t)+cons[ecy,ind](t)*pseu[ecy,ind](t)),INDEX(pser(..t-1),lastHistCol(t))*psf[ecy,all](t))`

**E381. `csd`: Consumer subsidy phase-out: change in the electricity price before VAT** (USD/kWh real)

- Description: CSELEC: txe x (pof.cs - 1) if txe < 0 and PowerSubsidyExemptInclude = Include
- Legacy: legacy O3606, O3635
- Rows: ecy,res, ecy,ind
  - 2022-2041: `csd(t) = IF(AND(year>LastHist,txe[f,s](t)<0,PowerSubsidyExemptInclude(t)="Include"),txe[f,s](t)*(pof[all,cs](t)-1),0)`

**E382. `ores`: Electricity price-chain residual (over / under-estimate of the price)** (USD/kWh real)

- Description: ORESID: txg - txe - pseu up to the last price year; then held, a negative one x scl / scl(t-1)
- Legacy: legacy rows 3607, 3636
- Rows: ecy,res, ecy,ind
  - 2022-2041: `ores(t) = IF(year<=LastHist,txg[f,s](t)-txe[f,s](t)-pseu[f,s](t),IF(ores[f,s](t-1)<0,ores[f,s](t-1)*scl[f,s](t)/scl[f,s](t-1),ores[f,s](t-1)))`

**E383. `spe`: Electricity supply cost of the subsidy lines (removing the over / under-estimate)** (USD/kWh real)

- Description: ELSUPPLY: sc + ores + ccpav x pass-through x (1 - rbs) + pex
- Legacy: legacy rows 3620, 3649 (code sp.res/ind.ecy)
- Rows: ecy,res, ecy,ind
  - 2022-2041: `spe(t) = sc[f,s](t)+ores[f,s](t)+ccpav(t)*PowerSectorPriceChangePassOn(t)*(1-rbs(t))+pex[f,s](t)`

**E384. `pdem`: Electricity price of the previous year used by demand (by demand group)** (USD/kWh real)

- Description: weight x residential price(t-1) + (1 - weight) x industrial price(t-1); base year: 2021 prices
- Legacy: legacy rows 3687-3689 (deliberately lagged)
- Rows: ecy,tra, ecy,srv
  - 2022: `pdem(t) = <2021 price>`
  - 2023-2041: `pdem(t) = <weight on the residential price>*rp[f,res](t-1)+(1-<weight on the residential price>)*rp[f,ind](t-1)`
  - Parameters: `<weight on the residential price>` = `INDEX(Inputs!D231:D234,MATCH(s,Inputs!A231:A234,0))`; `<2021 price>` = `INDEX(Inputs!K231:K234,MATCH(s,Inputs!A231:A234,0))`
- Rows: ecy,res
  - 2022: `pdem(t) = <2021 price>`
  - 2023-2041: `pdem(t) = <weight on the residential price>*rp[f,s](t-1)+(1-<weight on the residential price>)*rp[f,ind](t-1)`
  - Parameters: `<weight on the residential price>` = `INDEX(Inputs!D231:D234,MATCH(s,Inputs!A231:A234,0))`; `<2021 price>` = `INDEX(Inputs!K231:K234,MATCH(s,Inputs!A231:A234,0))`
- Rows: ecy,ind
  - 2022: `pdem(t) = <2021 price>`
  - 2023-2041: `pdem(t) = <weight on the residential price>*rp[f,res](t-1)+(1-<weight on the residential price>)*rp[f,s](t-1)`
  - Parameters: `<weight on the residential price>` = `INDEX(Inputs!D231:D234,MATCH(s,Inputs!A231:A234,0))`; `<2021 price>` = `INDEX(Inputs!K231:K234,MATCH(s,Inputs!A231:A234,0))`

**E385. `aeef`: Efficiency multiple of electricity demand (autonomous and additional efficiency of the scenario)** (factor)

- Description: (1 / (1 + alpha + AdditionalEfficiencyPower))^(1 + eps_U)
- Legacy: legacy rows 3691, 3697, 3703, 3709 (fixed: exponent eps_U)
- Rows: ecy,tra, ecy,res, ecy,ind, ecy,srv
  - 2022-2041: `aeef(t) = (1/(1+<alpha>+AdditionalEfficiencyPower(t)))^(1+<eps_U>)`
  - Parameters: `<alpha>` = `INDEX(Inputs!H231:H234,MATCH(s,Inputs!A231:A234,0))`; `<eps_U>` = `INDEX(Inputs!F231:F234,MATCH(s,Inputs!A231:A234,0))`

**E386. `mult`: Growth multiple of electricity demand (efficiency, GDP, price; demand shock if switched on)** (factor)

- Description: efficiency multiple x (1 + GDP growth)^(eps_Y x income factor) x (p/p(t-1))^(total price elasticity) x (1 + shock x switch x EngineerModelProportionOfCovidFactor)
- Legacy: legacy rows 3685, 3691-3713 (fixed: efficiency exponent, income factor)
- Changes against legacy: LD23, L1, L2, L3 (section B)
- Rows: ecy,tra, ecy,res, ecy,ind, ecy,srv
  - 2022: `mult(t) = 1`
  - 2023-2041: `mult(t) = aeef[f,s](t)*(1+gdp.pos.pct(t))^(<eps_Y>*inc.ela.adj(t))*(pdem[f,s](t)/pdem[f,s](t-1))^<total price elasticity>*(1+shock(t)*Settings[Fuel use and power demand: apply the legacy 2023-2]*EngineerModelProportionOfCovidFactor(t))`
  - Parameters: `<eps_Y>` = `INDEX(Inputs!E231:E234,MATCH(s,Inputs!A231:A234,0))`; `<total price elasticity>` = `INDEX(Inputs!J231:J234,MATCH(s,Inputs!A231:A234,0))`

**E387. `dem`: Electricity demand** (ktoe)

- Description: demand(t-1) x multiple of the demand group (v0.3.5: road from section 5b where TrModel = Engineer)
- Legacy: legacy rows 3725-3739 (H3; fixed: services keep the services multiple)
- Changes against legacy: LD23, LD24, LD25, LD27 (section B)
- Rows: ecy,rod
  - 2022: `dem(t) = <base-year demand>`
  - 2023-2041: `dem(t) = IF(<road engineer flag (1 = road)>*tr.sw[all,all](t)>0,trkte[f,s](t),dem[f,s](t-1)*INDEX(mult[4 rows](t),<demand-group position>))`
  - Parameters: `<demand-group position>` = `INDEX(Inputs!D238:D252,MATCH(s,Inputs!A238:A252,0))`; `<base-year demand>` = `INDEX(Inputs!E238:E252,MATCH(s,Inputs!A238:A252,0))`; `<road engineer flag (1 = road)>` = `INDEX(Inputs!I238:I252,MATCH(s,Inputs!A238:A252,0))`
- Rows: ecy,ral, ecy,avi, ecy,nav, ecy,res, ecy,foo, ecy,srv, ecy,mch, ecy,irn, ecy,nfm, ecy,mac, ecy,cem, ecy,omn, ... (14 rows)
  - 2022: `dem(t) = <base-year demand>`
  - 2023-2041: `dem(t) = IF(<road engineer flag (1 = road)>*tr.sw[all,all](t)>0,trkte[f,rod](t),dem[f,s](t-1)*INDEX(mult[4 rows](t),<demand-group position>))`
  - Parameters: `<demand-group position>` = `INDEX(Inputs!D238:D252,MATCH(s,Inputs!A238:A252,0))`; `<base-year demand>` = `INDEX(Inputs!E238:E252,MATCH(s,Inputs!A238:A252,0))`; `<road engineer flag (1 = road)>` = `INDEX(Inputs!I238:I252,MATCH(s,Inputs!A238:A252,0))`

**E388. `demg`: Electricity demand by demand group (memo)** (ktoe)

- Description: Sum over the subsectors of the group
- Legacy: legacy H3 (groups of H1)
- Rows: ecy,tra, ecy,res, ecy,ind, ecy,srv
  - 2022-2041: `demg(t) = SUMIF(dem[15 rows](D),<demand-group position>,dem[15 rows](t))`
  - Parameters: `<demand-group position>` = `INDEX(Inputs!C231:C234,MATCH(s,Inputs!A231:A234,0))`

**E389. `demtot`: Electricity demand, total** (ktoe)

- Description: Sum over subsectors
- Legacy: legacy row 3741
  - 2022-2041: `demtot(t) = SUM(dem[15 rows](t))`

**E390. `req`: Required generation (incl. net exports, transmission and statistical differences, own use)** (MWy)

- Description: Base year: actual generation; then total demand x required-generation factor
- Legacy: legacy rows 3746-3752
  - 2022: `req(t) = SUM(gen_mwy[9 rows](t))`
  - 2023-2041: `req(t) = demtot(t)*<MWy per ktoe of demand>`
  - Parameters: `<MWy per ktoe of demand>` = `Inputs!B261`

**E391. `reqcg`: Generation required from coal and gas** (MWy)

- Description: MAX(required generation - fixed-output generation, 0)
- Legacy: legacy row 3779
  - 2022-2041: `reqcg(t) = MAX(req(t)-SUMPRODUCT(effcap[9 rows](t),1-PwCG),0)`

**E392. `vcmin`: Lowest variable cost of coal and gas** (USD/kWh)

- Description: MAX(MIN over coal and gas of tvc, MinPostSubsidyPowerPrice)
- Legacy: legacy rows 3790-3793
  - 2022-2041: `vcmin(t) = MAX(MINIFS(tvc[9 rows](t),PwCG,1),MinPostSubsidyPowerPrice(t))`

**E393. `rem`: Coal and gas generation left after the minima** (MWy)

- Description: MAX(reqcg - sum of minima, 0)
- Legacy: legacy row 3789
  - 2022-2041: `rem(t) = MAX(reqcg(t)-SUM(gmin[9 rows](t)),0)`

**E394. `gmx`: Maximum generation of coal and gas** (MWy)

- Description: cap x (coal x MaximumCoalCF + gas x MaximumGasCF)
- Legacy: legacy rows 3783-3786 (v0.5.4: gas with its own maximum)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `gmx(t) = cap[f,s](t)*(<coal (1/0)>*MaximumCoalCF(t)+<gas (1/0)>*MaximumGasCF(t))`
  - Parameters: `<coal (1/0)>` = `INDEX(Inputs!AO207:AO215,MATCH(f,Inputs!A207:A215,0))`; `<gas (1/0)>` = `INDEX(Inputs!BM207:BM215,MATCH(f,Inputs!A207:A215,0))`

**E395. `gmin`: Minimum generation (coal if gas runs at its maximum, and vice versa)** (MWy)

- Description: coal/gas flag x MIN(MAX(reqcg - maximum of the other, 0), own maximum)
- Legacy: legacy rows 3787-3788
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `gmin(t) = <coal/gas flag>*MIN(MAX(reqcg(t)-(SUM(gmx[9 rows](t))-gmx[f,s](t)),0),gmx[f,s](t))`
  - Parameters: `<coal/gas flag>` = `INDEX(Inputs!AN207:AN215,MATCH(f,Inputs!A207:A215,0))`

**E396. `lgd`: Dispatch logit weight (coal and gas)** (weight)

- Description: flag x EXP(-kDispatch x MAX(tvc, minimum) / lowest)
- Legacy: legacy rows 3795-3796
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `lgd(t) = <coal/gas flag>*EXP(-kDispatch(t)*MAX(tvc[f,s](t),MinPostSubsidyPowerPrice(t))/vcmin(t))`
  - Parameters: `<coal/gas flag>` = `INDEX(Inputs!AN207:AN215,MATCH(f,Inputs!A207:A215,0))`

**E397. `glg`: Generation before PPAs (logit dispatch)** (MWy)

- Description: coal and gas: MIN(maximum, minimum + rem x logit share); others: effective capacity
- Legacy: legacy rows 3799-3800
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `glg(t) = IF(<coal/gas flag>=1,MIN(gmx[f,s](t),gmin[f,s](t)+rem(t)*lgd[f,s](t)/SUM(lgd[9 rows](t))),effcap[f,s](t))`
  - Parameters: `<coal/gas flag>` = `INDEX(Inputs!AN207:AN215,MATCH(f,Inputs!A207:A215,0))`

**E398. `ppr`: Coal and gas need / their effective capacity (PPA scaling)** (ratio)

- Description: IF(effective capacity = 0, 1, reqcg / effective capacity of coal and gas)
- Legacy: legacy row 3794
  - 2022-2041: `ppr(t) = IF(SUMPRODUCT(effcap[9 rows](t),PwCG)=0,1,reqcg(t)/SUMPRODUCT(effcap[9 rows](t),PwCG))`

**E399. `gen_mwy`: Generation** (MWy)

- Description: Base year: data; coal and gas: glg + ppa x (effcap x ppr - glg); others: effective capacity
- Legacy: legacy rows 3804-3812 (I3; v0.5.4: PPAs; scale-down not used)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022: `gen_mwy(t) = <base-year generation>`
  - 2023-2041: `gen_mwy(t) = glg[f,s](t)+<coal/gas flag>*ppa(t)*(effcap[f,s](t)*ppr(t)-glg[f,s](t))`
  - Parameters: `<coal/gas flag>` = `INDEX(Inputs!AN207:AN215,MATCH(f,Inputs!A207:A215,0))`; `<base-year generation>` = `INDEX(Inputs!AF207:AF215,MATCH(f,Inputs!A207:A215,0))`

**E400. `gtot`: Generation, total** (MWy)

- Description: Sum over types
- Legacy: legacy row 3813
  - 2022-2041: `gtot(t) = SUM(gen_mwy[9 rows](t))`

**E401. `dgen`: Increase in total generation (0 in the base year)** (MWy)

- Description: MAX(0, gtot - gtot(t-1))
- Legacy: legacy row 3972 (used lagged)
  - 2022: `dgen(t) = 0`
  - 2023-2041: `dgen(t) = MAX(0,gtot(t)-gtot(t-1))`

**E402. `shr`: Generation share** (share)

- Description: gen / gtot
- Legacy: legacy rows 3840-3848 (I6) = E0
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `shr(t) = IF(gtot(t)=0,0,gen_mwy[f,s](t)/gtot(t))`
  - Parameters: `<counts in VRE share>` = `INDEX(Inputs!P207:P215,MATCH(f,Inputs!A207:A215,0))`

**E403. `pe`: Fuel use (primary energy) of power generation** (ktoe)

- Description: gen x 8.76 / GWh per ktoe / efficiency used (nuu)
- Legacy: legacy rows 3855-3863 (I7)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `pe(t) = IF(nuu[f,s](t)=0,0,(gen_mwy[f,s](t)*<ktoe per MWy x efficiency>)/nuu[f,s](t))`
  - Parameters: `<ktoe per MWy x efficiency>` = `INDEX(Inputs!BK207:BK215,MATCH(f,Inputs!A207:A215,0))`; `<fuel flag>` = `INDEX(Inputs!AW207:AW215,MATCH(f,Inputs!A207:A215,0))`

**E404. `co2`: CO2 emissions from fuel combustion** (MtCO2)

- Description: Fuel use x PJ/ktoe x EF (power generation, section 3: generation fuel use (ktoe) x MtCO2 per ktoe)
- Legacy: legacy CO2 emissions by sector and fuel (inventory-adjusted EFs)
- Changes against legacy: LD36, LD39, LD57 (section B)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `co2(t) = pe[f,s](t)*<EF (power: MtCO2 per ktoe)>`
  - Parameters: `<EF (power: MtCO2 per ktoe)>` = `INDEX(Inputs!AS207:AS215,MATCH(f,Inputs!A207:A215,0))`
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `co2(t) = ener[f,s](t)*Settings[PJ per ktoe]*<EF (power: MtCO2 per ktoe)>`
  - Parameters: `<EF (power: MtCO2 per ktoe)>` = `INDEX(Inputs!W5:W148,MATCH(f&"|"&s,Inputs!A5:A148,0))`
- Rows: all,tra, all,bld, all,ind, all,oen
  - 2022-2041: `co2(t) = SUMIF(block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(A),"co2",block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(t))`
- Rows: all,pow
  - 2022-2041: `co2(t) = SUM(co2[9 rows](t))`
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all
  - 2022-2041: `co2(t) = SUMIFS(block{ener, eldem, ctxnew, ets, ... 600 variables}(t),SecVar,"co2",SecFuel,f)+SUMIF(co2[9 rows](B),f,co2[9 rows](t))`
- Rows: all,all
  - 2022-2041: `co2(t) = SUMIF(SecVar,"co2",block{ener, eldem, ctxnew, ets, ... 600 variables}(t))+co2[f,pow](t)`

**E405. `vre`: Variable renewable share of generation (wind, solar, other renewables)** (share)

- Description: SUMPRODUCT(shr, VRE-share flag)
- Legacy: legacy rows 3851, 3907
- Changes against legacy: M4 (section B)
  - 2022-2041: `vre(t) = SUMPRODUCT(shr[9 rows](t),shr[9 rows](D))*<factor (Constants)>`
  - Parameters: `<factor (Constants)>` = `INDEX(ConstVal,MATCH("pw.c|"&code,ConstKey,0))`

**E406. `cph`: Short-term storage cost per marginal hour of storage** (USD/kWh)

- Description: (battery capex + interface capex / kWh per kW)/(dlf of renewables x 8,760) + battery opex / 8,760
- Legacy: legacy row 3905 (J2; ratio of the scenario, dlfr)
- Changes against legacy: L4 (section B)
  - 2022-2041: `cph(t) = (cbat(t)+cint(t)/StorageToInterfaceRatioSTStorage(t))/(dlfr(t)*HoursYr)+obat(t)/HoursYr`

**E407. `msc`: Marginal storage cost of variable renewables (wind, solar, other renewables)** (USD/kWh)

- Description: alloc x 2 x hours x vre x cph + 2 x MAX(0, vre - start)/(1 - start)^2 x cel x LT allocation x LT units for 100% VRE (settings of the scenario)
- Legacy: legacy rows 3908-3912 (J1; fixed: LT allocation once; v0.5.4: LongTermStorageFor100pcVRE, row 3909)
- Changes against legacy: LD23, L4, M3 (section B)
  - 2022-2041: `msc(t) = stm(t)*vre(t)*cph(t)+2*MAX(0,vre(t)-StartingPointWhenLTStorageIsNeeded(t))/(1-StartingPointWhenLTStorageIsNeeded(t))^2*cel(t)*ltu(t)`

**E408. `cap`: Nameplate capacity** (MW)

- Description: Base year: data; then cap(t-1) - retirement(t-1) + new nameplate investment(t-1)
- Legacy: legacy rows 3932-3940 (K1) = L21 of the previous year; base year cap0
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022: `cap(t) = cap0[f,s](t)`
  - 2023-2041: `cap(t) = cap[f,s](t-1)-ret[f,s](t-1)+nim[f,s](t-1)`

**E409. `captot`: Nameplate capacity, total** (MW)

- Description: Sum over types
- Legacy: legacy row 3941
  - 2022-2041: `captot(t) = SUM(cap[9 rows](t))`

**E410. `effcap`: Effective capacity (expected generation)** (MW)

- Description: cap x capacity factor used (cfu)
- Legacy: legacy rows 3956-3964 (K3)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `effcap(t) = cap[f,s](t)*cfu[f,s](t)`

**E411. `pret`: Planned retirement (data; used where the type's switch is Yes)** (MW)

- Description: PowerPaths pret|<type> (Egypt: no data, 0)
- Legacy: legacy row 3992 (K5, coal only; data from sheet Power)
- Changes against legacy: LD26 (section B)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `pret(t) = INDEX(PPathVal,MATCH(CtryCode&"|"&<data key>,PPathKey,0),MATCH(year,PPathYear,0))`
  - Parameters: `<data key>` = `code&"|"&f`

**E412. `ret`: Retirement of nameplate capacity** (MW)

- Description: MIN(planned retirement if switched on, else cap x retirement rate; + early coal retirement; cap)
- Legacy: legacy rows 3992-4002 (K5; planned retirement for every type, legacy coal only; rate rr of the scenario)
- Changes against legacy: LD26 (section B)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `ret(t) = MIN(IF(<planned retirement used (1/0)>=1,pret[f,s](t),cap[f,s](t)*rr[f,s](t))+<early-retirement flag>*early(t),cap[f,s](t))`
  - Parameters: `<early-retirement flag>` = `INDEX(Inputs!AO207:AO215,MATCH(f,Inputs!A207:A215,0))`; `<planned retirement used (1/0)>` = `INDEX(Inputs!AM207:AM215,MATCH(f,Inputs!A207:A215,0))`

**E413. `rec`: Retirement of effective capacity** (MW)

- Description: ret x capacity factor used (cfu)
- Legacy: legacy rows 4009-4019 (K6; fixed: coal as nameplate)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `rec(t) = ret[f,s](t)*cfu[f,s](t)`

**E414. `egrow`: Room for early coal retirement: maximum wind and solar additions less last year's demand increase and non-coal retirements** (MW)

- Description: MAX(0, ...)
- Legacy: legacy rows 3970-3974 (fixed: effective retirements)
  - 2022: `egrow(t) = MAX(0,maxinv[wnd,pow](t)+maxinv[sol,pow](t))`
  - 2023-2041: `egrow(t) = MAX(0,maxinv[wnd,pow](t)+maxinv[sol,pow](t)-dgen(t-1)-(SUM(rec[9 rows](t-1))-rec[coa,pow](t-1)))`

**E415. `ecmin`: Early coal retirement: lowest of coal variable cost and wind and solar investment cost** (USD/kWh)

- Description: MIN(tvc coal, tic wind, tic solar)
- Legacy: legacy row 3982
  - 2022-2041: `ecmin(t) = MIN(tvc[coa,pow](t),tic[wnd,pow](t),tic[sol,pow](t))`

**E416. `ecshr`: Early coal retirement: coal share of the logit (coal variable cost vs wind and solar investment cost)** (share)

- Description: 1 / (1 + EXP(-K (tic wind - tvc coal) / lowest) + EXP(-K (tic solar - tvc coal) / lowest)); K = kInvestment of the scenario
- Legacy: legacy row 3983
  - 2022-2041: `ecshr(t) = 1/(1+EXP(-kInvestment(t)*(tic[wnd,pow](t)-tvc[coa,pow](t))/ecmin(t))+EXP(-kInvestment(t)*(tic[sol,pow](t)-tvc[coa,pow](t))/ecmin(t)))`

**E417. `early`: Cost-based early coal retirement (nameplate)** (MW)

- Description: MAX(0, MIN(coal effective capacity x 0.8, room) x (1 - coal share of the logit)) / cf x erf x (1 - ppa)
- Legacy: legacy rows 3975-3993 (K4; v0.5.4: not the PPA share, rows 3987, 3993)
- Changes against legacy: LD23, L7 (section B)
  - 2022-2041: `early(t) = MAX(0,MIN(effcap[coa,pow](t)*<maximum share>,egrow(t))*(1-ecshr(t)))/cfu[coa,pow](t)*erf(t)*(1-ppa(t))`
  - Parameters: `<maximum share>` = `INDEX(PParVal,MATCH(CtryCode&"|early_max",PParKey,0))`

**E418. `kafter`: Effective capacity after this year's retirements** (MW)

- Description: SUM(effcap) - SUM(reteff)
- Legacy: legacy row 4026 (fixed: actual capacity, legacy last year's plan)
  - 2022-2041: `kafter(t) = SUM(effcap[9 rows](t))-SUM(rec[9 rows](t))`

**E419. `need`: Effective capacity investment needed** (MW)

- Description: MAX(next year's required generation (v0.4.14; 2041: this year's) - kafter, 0)
- Legacy: legacy rows 4027-4028 (legacy: this year's demand under the label "Next Year Demand": bug L67)
- Changes against legacy: LD23, L10 (section B)
  - 2022-2041: `need(t) = MAX(req(t)*IFERROR(req(t)/req(t-1),1)-kafter(t),0)`

**E420. `mancap`: Manual capacity path (Manual inputs rows 349-357 scenario 1, 363-371 other scenarios)** (MW)

- Description: INDEX(Manual inputs capacity block of the scenario group, type, year); blank = 0 (v0.5.6, P3)
- Legacy: legacy rows 3944-3952 (from Manual inputs 342-371)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `mancap(t) = IFERROR(INDEX(ManCapVal,<type position>+IF(scenario(t)=1,0,ManCapOff),MATCH(year,ManCapYr,0))+0,0)`
  - Parameters: `<type position>` = `INDEX(Inputs!BN207:BN215,MATCH(f,Inputs!A207:A215,0))`

**E421. `mani`: Manual new effective investment (NewInv<type> = Manual)** (MW)

- Description: IF(setting = Manual, MAX(0, next year's path - this year's path + retirement) x cfu, 0); 2041: 0 (v0.5.6, P3)
- Legacy: legacy rows 4097-4105, 4110-4118
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `mani(t) = IF(AND(invs[f,s](t)="Manual",ISNUMBER(mancap[f,s](t+1))),MAX(0,mancap[f,s](t+1)-mancap[f,s](t)+ret[f,s](t))*cfu[f,s](t),0)`

**E422. `needm`: Effective investment needed after manual investment** (MW)

- Description: MAX(need - SUM(mani), 0) (v0.5.6, P3)
- Legacy: legacy row 4108 (never used in legacy: logit investment came on top of the manual one, bug L118)
  - 2022-2041: `needm(t) = MAX(need(t)-SUM(mani[9 rows](t)),0)`

**E423. `cmin`: Lowest levelised investment cost of the permitted types** (USD/kWh)

- Description: MAX(MIN over permitted, MinPostSubsidyPowerPrice)
- Legacy: legacy row 4046 (fixed: permitted types only)
- Changes against legacy: LD23 (section B)
  - 2022-2041: `cmin(t) = MAX(MINIFS(tic[9 rows](t),permit[9 rows](t),1),MinPostSubsidyPowerPrice(t))`

**E424. `deficit`: Investment left for the second round** (MW)

- Description: MAX(needm - SUM(first round), 0)
- Legacy: legacy row 4153
  - 2022-2041: `deficit(t) = MAX(needm(t)-SUM(first[9 rows](t)),0)`

**E425. `permit`: New investment permitted (0/1)** (0/1)

- Description: perm = Yes from the start year (A0)
- Legacy: legacy rows 4061-4069 (L3)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `permit(t) = IF(AND(perm[f,s](t)="Yes",year>=start[f,s](t)),1,0)`

**E426. `maxinv`: Maximum effective investment (scale-up limit)** (MW)

- Description: rate x total effective capacity x permit
- Legacy: legacy rows 4130-4138 (L8)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `maxinv(t) = rate[f,s](t)*SUM(effcap[9 rows](t))*permit[f,s](t)`

**E427. `lgi`: Investment logit weight** (weight)

- Description: permit x EXP(-kInvestment x tic / cmin)
- Legacy: legacy rows 4073-4081 (L4)
- Changes against legacy: LD23, L6 (section B)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `lgi(t) = permit[f,s](t)*EXP(-kInvestment(t)*tic[f,s](t)/cmin(t))`

**E428. `pni`: Share of new investment (logit)** (share)

- Description: lgi / SUM(lgi)
- Legacy: legacy rows 4085-4093 (L5)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `pni(t) = IF(SUM(lgi[9 rows](t))=0,0,lgi[f,s](t)/SUM(lgi[9 rows](t)))`

**E429. `first`: New effective investment, first round (logit within scale-up limits)** (MW)

- Description: MIN(maxinv, needm x pni)
- Legacy: legacy rows 4143-4151 (L9)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `first(t) = MIN(maxinv[f,s](t),needm(t)*pni[f,s](t))`

**E430. `space`: Remaining space under the scale-up limit** (MW)

- Description: (maxinv - first) x permit
- Legacy: legacy rows 4158-4166 (L10)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `space(t) = (maxinv[f,s](t)-first[f,s](t))*permit[f,s](t)`

**E431. `second`: New effective investment, second round (cheapest remaining space first)** (MW)

- Description: permit x MAX(0, MIN(space, deficit - space of cheaper types))
- Legacy: legacy rows 4169-4246 (L11-L17 in one row)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `second(t) = permit[f,s](t)*MAX(0,MIN(space[f,s](t),deficit(t)-SUMPRODUCT((tic[9 rows](t)+PwTie<tic[f,s](t)+<tie breaker>)*space[9 rows](t))))`
  - Parameters: `<tie breaker>` = `INDEX(Inputs!AT207:AT215,MATCH(f,Inputs!A207:A215,0))`

**E432. `dgas`: Investment deficit left after the second round, to gas (Settings PwDeficitGas = Yes)** (MW)

- Description: IF(switch = Yes, deficit - SUM(second), 0)
- Legacy: legacy rows 4247-4248, 4252 (typed switch E4248, No)
  - 2022-2041: `dgas(t) = IF(PwDeficitGas="Yes",deficit(t)-SUM(second[9 rows](t)),0)`

**E433. `nei`: New effective investment** (MW)

- Description: first + second (+ dgas for gas) + mani (v0.5.6)
- Legacy: legacy rows 4251-4259 (L18)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `nei(t) = first[f,s](t)+(second[f,s](t)+<gas (1/0)>*dgas(t)+mani[f,s](t))`
  - Parameters: `<gas (1/0)>` = `INDEX(Inputs!BM207:BM215,MATCH(f,Inputs!A207:A215,0))`

**E434. `nim`: New nameplate investment** (MW)

- Description: nei / capacity factor used (cfu)
- Legacy: legacy rows 4264-4272 (L19)
- Changes against legacy: LD23 (section B)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `nim(t) = IF(cfu[f,s](t)=0,0,nei[f,s](t)/cfu[f,s](t))`

**E435. `nimtot`: New nameplate investment, total** (MW)

- Description: Sum over types
- Legacy: legacy row 4273
- Changes against legacy: L12 (section B)
  - 2022-2041: `nimtot(t) = SUM(nim[9 rows](t))`

**E436. `nid`: New investment** (USD m real)

- Description: nim x cax / 1000
- Legacy: legacy rows 4276-4284 (L20; fixed: capital cost of the year)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `nid(t) = nim[f,s](t)*cax[f,s](t)*kWperMW/USDperM`

**E437. `usdtot`: New investment, total** (USD m real)

- Description: Sum over types
- Legacy: legacy row 4285
  - 2022-2041: `usdtot(t) = SUM(nid[9 rows](t))`

**E438. `phi`: New investment as a share of the stock after retirements** (share)

- Description: nim / (cap + nim - ret)
- Legacy: legacy rows 3169-3177 (B1)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `phi(t) = IF(cap[f,s](t)+nim[f,s](t)-ret[f,s](t)=0,0,nim[f,s](t)/(cap[f,s](t)+nim[f,s](t)-ret[f,s](t)))`

**E439. `prtx`: Existing taxes on generation fuels (excise and other taxes + VAT of the price fuel)** (USD m real)

- Description: fuel flag x fuel use (ktoe) x PJ/ktoe x (etx + vat)
- Legacy: new
- Changes against legacy: LD39 (section B)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `prtx(t) = <fuel flag>*pe[f,s](t)*Settings[PJ per ktoe]*(etx[<price position>](t)+vat[<price position>](t))`
  - Parameters: `<price position>` = `INDEX(Inputs!X207:X215,MATCH(f,Inputs!A207:A215,0))`; `<fuel flag>` = `INDEX(Inputs!AW207:AW215,MATCH(f,Inputs!A207:A215,0))`

**E440. `prsub`: Existing subsidies on generation fuels (negative = fiscal cost)** (USD m real)

- Description: fuel flag x fuel use x PJ/ktoe x esub
- Legacy: new
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `prsub(t) = <fuel flag>*pe[f,s](t)*Settings[PJ per ktoe]*(esub[<price position>](t))`
  - Parameters: `<price position>` = `INDEX(Inputs!X207:X215,MATCH(f,Inputs!A207:A215,0))`; `<fuel flag>` = `INDEX(Inputs!AW207:AW215,MATCH(f,Inputs!A207:A215,0))`

**E441. `prxc`: Change in existing carbon pricing revenue against the price data** (USD m real)

- Description: xck x generation (MWy x 8.76 = GWh)
- Legacy: new
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `prxc(t) = xck[f,s](t)*MWyMkWh*gen_mwy[f,s](t)`

**E442. `prnew`: New-policy revenue (carbon tax, ETS at the permit price, fuel price reform)** (USD m real)

- Description: ccp x GWh - CO2 x ETS cost rate of power x (1 - revenue factor)
- Legacy: legacy power carbon revenue (fixed: ETS at the permit price)
- Changes against legacy: LD35, M6 (section B)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `prnew(t) = gen_mwy[f,s](t)*MWyMkWh*xac[f,s](t)-co2[f,s](t)*etr[all,s](t)*(1-ets.rf(t))`

**E443. `prxl`: Existing carbon pricing revenue (memo: level)** (USD m real)

- Description: CO2 x (carbon tax x factor + ETS x factor; Inputs_ecp tables, v0.4.12)
- Legacy: legacy ECP revenue
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `prxl(t) = co2[f,s](t)*(INDEX(XCTVal,<ECP table row>,xct.c(t))*xct.p(t)+INDEX(XETSVal,<ECP table row>,xct.c(t))*xets.p(t))`
  - Parameters: `<ECP table row>` = `INDEX(Inputs!AU207:AU215,MATCH(f,Inputs!A207:A215,0))`

**E444. `prrns`: Renewable subsidy revenue by type (negative = fiscal cost)** (USD m real)

- Description: rns x generation (MWy x 8.76 = GWh)
- Legacy: legacy rows 3665-3669, 7897-7903 (L108 fixed: the base subsidy once)
- Rows: coa,pow, nga,pow, oop,pow, nuc,pow, wnd,pow, sol,pow, hyd,pow, ore,pow, bio,pow
  - 2022-2041: `prrns(t) = rns[f,s](t)*MWyMkWh*gen_mwy[f,s](t)`

**E445. `pet`: Fuel use of power generation (coal, gas, oil, biomass)** (ktoe)

- Description: SUMPRODUCT(pe, fuel flag)
- Legacy: new (summary line of section 3)
- Rows: all,pow
  - 2022-2041: `pet(t) = SUMPRODUCT(pe[9 rows](t),pe[9 rows](E))`

### 5

**E446. `ener`: Fuel use** (ktoe)

- Description: enel; road gasoline, diesel, LPG, gas and biofuels from section 5b where TrModel = Engineer (v0.3.5); + the cumulative residential leakage to biomass of section 6b (v0.5.1)
- Legacy: legacy Mitigation rows 5430-5440 (road: engineer or elasticity model), 5554-5560 (residential: + leakage)
- Changes against legacy: LD1, LD21, LD39 (section B)
- Rows: all,rod, all,ral, all,res, all,foo, all,srv, all,mch, all,irn, all,nfm, all,mac, all,cem, all,omn, all,cst, ... (14 rows)
  - 2022-2041: `ener(t) = SUM(ener[9 rows](t))`
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, coa,ral, nga,ral, gso,ral, die,ral, ... (143 rows)
  - 2022-2041: `ener(t) = IF(<engineer road row (position in section 5b; 0 = elasticity model)>*tr.sw[all,all](t)>0,trkt[<engineer road row (position in section 5b; 0 = elasticity model)>](t),enel[f,s](t))+lkz[<leakage row (position in section 6b; 1 = none)>](t)`
  - Parameters: `<engineer road row (position in section 5b; 0 = elasticity model)>` = `INDEX(Inputs!AF5:AF148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<leakage row (position in section 6b; 1 = none)>` = `INDEX(Inputs!BF5:BF148,MATCH(f&"|"&s,Inputs!A5:A148,0))`
- Rows: bio,rod
  - 2022-2041: `ener(t) = IF(<engineer road row (position in section 5b; 0 = elasticity model)>*tr.sw[all,all](t)>0,trkt[<engineer road row (position in section 5b; 0 = elasticity model)>](t),trbe[f,s](t))+lkz[<leakage row (position in section 6b; 1 = none)>](t)`
  - Parameters: `<engineer road row (position in section 5b; 0 = elasticity model)>` = `INDEX(Inputs!AF5:AF148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<leakage row (position in section 6b; 1 = none)>` = `INDEX(Inputs!BF5:BF148,MATCH(f&"|"&s,Inputs!A5:A148,0))`
- Rows: all,avi, all,nav
  - 2022-2041: `ener(t) = SUM(ener[9 rows](t))+ener[ren,s](t)`
- Rows: all,tra
  - 2022-2041: `ener(t) = SUMIFS(block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(t),block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(A),"ener",block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(B),"<>all")+ener[ren,avi](t)+ener[ren,nav](t)`
- Rows: ren,avi
  - 2022: `ener(t) = <aviation of trp.rn0[all,all]>`
  - 2023-2041: `ener(t) = ener[f,s](t-1)*trrena[f,tra](t)*(1+row14(t))^<income elasticity of trp.rne[all,all]>*(trpren[f,tra](t)/trpren[f,tra](t-1))^<usage elasticity of trp.rne[all,all]>*((trpren[f,tra](t)+0)/(trpren[f,tra](t-1)+0))^<efficiency exponent eps_F x (1 + eps_U) of trp.rne[all,all]>*row6(t)`
- ... and 6 further row patterns (see the workbook)

**E447. `eldem`: Electricity demand (memo: power model H; not in the fuel totals; sector policies do not act on it)** (ktoe)

- Description: Section 3 H, demand by subsector
- Legacy: legacy H3 (rows 3725-3739)
- Rows: ecy,rod, ecy,ral, ecy,avi, ecy,nav, ecy,res, ecy,foo, ecy,srv, ecy,mch, ecy,irn, ecy,nfm, ecy,mac, ecy,cem, ... (16 rows)
  - 2022-2041: `eldem(t) = SUMIF(dem[15 rows](C),s,dem[15 rows](t))`
- Rows: ecy,all
  - 2022-2041: `eldem(t) = SUM(eldem[4 rows](t))`
- Rows: ecy,tra, ecy,bld, ecy,ind, ecy,oen
  - 2022-2041: `eldem(t) = SUMIF(block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(A),"eldem",block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(t))`

**E448. `ctxnew`: New carbon tax** (USD/GJ)

- Description: Carbon tax rate of the sector (ctr, section 1) x EF x fuel coverage x exemption factor (exf, v0.5.1)
- Legacy: legacy Mitigation row 2510: egy.mit.ctxnew.ind.coa.a.1
- Changes against legacy: LD57 (section B)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `ctxnew(t) = INDEX(ctr[17 rows](t),<sector position>)*<EF>*INDEX(ctcov[9 rows](t),<fuel position>)*INDEX(exf[2 rows](t),<exemption group>)`
  - Parameters: `<EF>` = `INDEX(Inputs!W5:W148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<fuel position>` = `INDEX(Inputs!L5:L148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<sector position>` = `INDEX(Inputs!M5:M148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<exemption group>` = `INDEX(Inputs!BE5:BE148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E449. `ets`: New ETS cost in the fuel price (tax-equivalent, auctioned part)** (USD/GJ)

- Description: ETS cost rate of the sector (etr, section 1) x EF x exemption factor (exf, v0.5.1)
- Legacy: legacy ets inside txo; coded prices/ets.py
- Changes against legacy: LD57 (section B)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `ets(t) = INDEX(etr[17 rows](t),<sector position>)*<EF>*INDEX(exf[2 rows](t),<exemption group>)`
  - Parameters: `<EF>` = `INDEX(Inputs!W5:W148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<sector position>` = `INDEX(Inputs!M5:M148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<exemption group>` = `INDEX(Inputs!BE5:BE148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E450. `ntx`: New excise tax (fuel price reform)** (USD/GJ)

- Description: Fuel price reform path / GJ per unit x exemption factor (exf, v0.5.1)
- Legacy: legacy Mitigation row 2512: egy.mit.ntx.ind.coa.a.1
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `ntx(t) = INDEX(ntxb[14 rows](t),<price-fuel position>)/<GJ per unit>*INDEX(exf[2 rows](t),<exemption group>)`
  - Parameters: `<price-fuel position>` = `INDEX(Inputs!N5:N148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<GJ per unit>` = `INDEX(Inputs!K5:K148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<exemption group>` = `INDEX(Inputs!BE5:BE148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E451. `nce`: Total new policy** (USD/GJ)

- Description: New carbon tax + new excise tax
- Legacy: legacy Mitigation row 2514: egy.mit.nce.ind.coa.a.1
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `nce(t) = ctxnew[f,s](t)+ets[f,s](t)+ntx[f,s](t)`

**E452. `xcp`: Existing carbon pricing (carbon tax + ETS) per GJ** (USD/GJ)

- Description: EF x (carbon tax x factor + ETS x factor) of the ECP sector | fuel (Inputs_ecp tables: rate x sector x fuel coverage of the data year; national and EU ETS; v0.4.12)
- Legacy: legacy rows 1711-1723 (ets), 1752-1764 (ctx)
- Changes against legacy: LD38 (section B)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `xcp(t) = <EF>*(INDEX(XCTVal,<ECP table row>,xct.c(t))*xct.p(t)+INDEX(XETSVal,<ECP table row>,xct.c(t))*xets.p(t))`
  - Parameters: `<EF>` = `INDEX(Inputs!W5:W148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<ECP table row>` = `INDEX(Inputs!Z5:Z148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E453. `xcpd`: Change in existing carbon pricing against the price data (enters the after-tax price)** (USD/GJ)

- Description: EF x (carbon tax x factor + ETS x factor - the level embedded in the price data)
- Legacy: new (legacy: ctx and ets are parts of txo)
- Changes against legacy: LD38 (section B)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `xcpd(t) = <EF>*(INDEX(XCTVal,<ECP table row>,xct.c(t))*xct.p(t)+INDEX(XETSVal,<ECP table row>,xct.c(t))*xets.p(t)-<embedded ($/tCO2)>)`
  - Parameters: `<EF>` = `INDEX(Inputs!W5:W148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<ECP table row>` = `INDEX(Inputs!Z5:Z148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<embedded ($/tCO2)>` = `INDEX(Inputs!AA5:AA148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E454. `csw`: Consumer subsidy reform wedge of the subsector (the block's pcsw)** (USD/GJ real)

- Description: BLOCKWEDGE
- Legacy: v0.4.16 (LD18)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `csw(t) = pcsw[<price position>](t)`
  - Parameters: `<price position>` = `INDEX(Inputs!U5:U148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E455. `pcw`: Price-control phase-out wedge of the subsector (the block's ppcw)** (USD/GJ real)

- Description: BLOCKWEDGE
- Legacy: v0.4.16 (LD18)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `pcw(t) = ppcw[<price position>](t)`
  - Parameters: `<price position>` = `INDEX(Inputs!U5:U148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E456. `atp`: After-tax price** (USD/GJ real)

- Description: max(rpb of the price fuel + nce x (1 + VAT rate), 0.01)
- Legacy: legacy Mitigation row 5416: egy.mit.atp.rod.gso.e.1 (legacy unit $/liter for liquids)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `atp(t) = MAX(pbc[<price position>](t)+(nce[f,s](t)+xcpd[f,s](t)+csw[f,s](t)+pcw[f,s](t))*(1+<VAT rate>),PriceFloor)`
  - Parameters: `<price position>` = `INDEX(Inputs!U5:U148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<VAT rate>` = `INDEX(Inputs!V5:V148,MATCH(f&"|"&s,Inputs!A5:A148,0))`
- Rows: coa,res, nga,res, oop,res, gso,res, die,res, ker,res, lpg,res
  - 2022-2041: `atp(t) = atp[f,s](t)`

**E457. `shp`: Shadow price on the efficiency margin** (USD/GJ)

- Description: Shadow price of the sector (shpx, section 1) x EF
- Legacy: legacy Mitigation row 2377: egy.mit.shp.coa.pow.1
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `shp(t) = INDEX(shpx[17 rows](t),<sector position>)*<EF>`
  - Parameters: `<EF>` = `INDEX(Inputs!W5:W148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<sector position>` = `INDEX(Inputs!M5:M148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E458. `aef`: Efficiency factor of fuel use: autonomous plus additional policy-induced efficiency gains** (factor)

- Description: (1 / (1 + alpha + additional efficiency of the group))^(1 + eps_U); additional efficiency: MTInputs 243-245 (road vehicles, residential, industrial; section 1), v0.4.13
- Legacy: legacy fuel rows: /(1 + _eff_imp + $M2199:$M2201)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `aef(t) = (1/(1+<alpha (AEEI)>+AdditionalEfficiencyRoadVehicle[<additional efficiency group>](t)))^(1+<eps_U>)`
  - Parameters: `<alpha (AEEI)>` = `INDEX(Inputs!R5:R148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<additional efficiency group>` = `INDEX(Inputs!S5:S148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<eps_U>` = `INDEX(Inputs!P5:P148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E459. `enel`: Fuel use, elasticity model** (ktoe)

- Description: Inputs (base year), CPAT eq. 3.3.3
- Legacy: legacy Mitigation row 5430: egy.mit.ener.rod.gso.e.1 (v0.3.5: the elasticity part of ener)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022: `enel(t) = INDEX(Inputs!X5:X148,MATCH(f&"|"&s,Inputs!A5:A148,0))`
  - 2023-2041: `enel(t) = enel[f,s](t-1)*aef[f,s](t)*(1+row14(t))^<eps_Y>*(atp[f,s](t)/atp[f,s](t-1))^<eps_U>*((atp[f,s](t)+shp[f,s](t))/(atp[f,s](t-1)+shp[f,s](t-1)))^<efficiency exponent eps_F x (1 + eps_U)>*row6(t)`
  - Parameters: `<eps_Y>` = `INDEX(Inputs!O5:O148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<eps_U>` = `INDEX(Inputs!P5:P148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<efficiency exponent eps_F x (1 + eps_U)>` = `INDEX(Inputs!T5:T148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E460. `ch4`: CH4 emissions from fuel combustion** (kt CH4)

- Description: Fuel use (ktoe) x CH4 EF (t/ktoe; GAINS, sheet EF_PM by legacy EF code, country else region else world, Inputs_ef; linear from the base year to the EFSel final factor in EFEndYear, continued after) / tPerKt; power: section 14
- Legacy: legacy Mitigation rows 1514-1586 (factors), 7203-7307 (ch4 block of section 13; legacy 465 factors blank: I34)
- Changes against legacy: LD47 (section B)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `ch4(t) = ener[f,s](t)*(<CH4 EF, base year (t/ktoe)>+(<CH4 EF, EFEndYear (t/ktoe)>-<CH4 EF, base year (t/ktoe)>)*EFFinShare*(year-BaseYr)/(EFEndYear-BaseYr))/tPerKt`
  - Parameters: `<CH4 EF, base year (t/ktoe)>` = `INDEX(Inputs!AD5:AD148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<CH4 EF, EFEndYear (t/ktoe)>` = `INDEX(Inputs!AE5:AE148,MATCH(f&"|"&s,Inputs!A5:A148,0))`
- Rows: coa,pow, nga,pow, oop,pow, bio,pow
  - 2022-2041: `ch4(t) = pe[f,s](t)*(<CH4 EF, base year (t/ktoe)>+(<CH4 EF, EFEndYear (t/ktoe)>-<CH4 EF, base year (t/ktoe)>)*EFFinShare*(year-BaseYr)/(EFEndYear-BaseYr))/tPerKt`
  - Parameters: `<CH4 EF, base year (t/ktoe)>` = `IFERROR(INDEX(NCEfIn,MATCH("pow.coa.ch4",NCEfKey,0)),0)`; `<CH4 EF, EFEndYear (t/ktoe)>` = `IFERROR(INDEX(NCEfFin,MATCH("pow.coa.ch4",NCEfKey,0)),0)`

**E461. `rtx`: Revenue from existing taxes (excise and other taxes + VAT; incl. the change in existing carbon pricing)** (USD m real)

- Description: Fuel use x PJ/ktoe x (etx + vat + xcpd x (1 + VAT rate)); power: fuel taxes, change in existing carbon pricing, electricity VAT
- Legacy: legacy revenue block (existing taxes)
- Changes against legacy: LD37 (section B)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `rtx(t) = ener[f,s](t)*Settings[PJ per ktoe]*(etx[<price position>](t)+vat[<price position>](t)+xcpd[f,s](t)*(1+<VAT rate>))`
  - Parameters: `<price position>` = `INDEX(Inputs!U5:U148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<VAT rate>` = `INDEX(Inputs!V5:V148,MATCH(f&"|"&s,Inputs!A5:A148,0))`
- Rows: all,all
  - 2022-2041: `rtx(t) = SUMIFS(block{ener, eldem, ctxnew, ets, ... 600 variables}(t),SecVar,"rtx")+rtx[f,pow](t)`
- Rows: all,tra, all,bld, all,ind, all,oen
  - 2022-2041: `rtx(t) = SUMIFS(block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(t),block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(A),"rtx")`
- Rows: all,pow
  - 2022-2041: `rtx(t) = SUM(prtx[9 rows](t))+SUM(prxc[9 rows](t))+SUM(rvat[2 rows](t))`

**E462. `rsub`: Existing consumer subsidies (negative = fiscal cost)** (USD m real)

- Description: Fuel use x PJ/ktoe x esub
- Legacy: legacy subsidy cost
- Changes against legacy: LD14, LD37 (section B)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `rsub(t) = ener[f,s](t)*Settings[PJ per ktoe]*(esub[<price position>](t))`
  - Parameters: `<price position>` = `INDEX(Inputs!U5:U148,MATCH(f&"|"&s,Inputs!A5:A148,0))`
- Rows: all,all
  - 2022-2041: `rsub(t) = SUMIFS(block{ener, eldem, ctxnew, ets, ... 600 variables}(t),SecVar,"rsub")+rsub[f,pow](t)`
- Rows: all,tra, all,bld, all,ind, all,oen
  - 2022-2041: `rsub(t) = SUMIFS(block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(t),block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(A),"rsub")`
- Rows: all,pow
  - 2022-2041: `rsub(t) = SUM(prsub[9 rows](t))+SUM(rgap[2 rows](t))+SUM(prrns[9 rows](t))`

**E463. `rnew`: Revenue from new policies (carbon tax, excise, auctioned ETS, VAT on them)** (USD m real)

- Description: Fuel use x PJ/ktoe x (ctxnew + ntx + ets x revenue factor + nce x VAT rate)
- Legacy: legacy new revenue
- Changes against legacy: LD37 (section B)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `rnew(t) = ener[f,s](t)*Settings[PJ per ktoe]*(ctxnew[f,s](t)+ntx[f,s](t)+ets[f,s](t)*ets.rf(t)+nce[f,s](t)*<VAT rate>)`
  - Parameters: `<VAT rate>` = `INDEX(Inputs!V5:V148,MATCH(f&"|"&s,Inputs!A5:A148,0))`
- Rows: all,all
  - 2022-2041: `rnew(t) = SUMIFS(block{ener, eldem, ctxnew, ets, ... 600 variables}(t),SecVar,"rnew")+rnew[f,pow](t)`
- Rows: all,tra, all,bld, all,ind, all,oen
  - 2022-2041: `rnew(t) = SUMIFS(block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(t),block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(A),"rnew")`
- Rows: all,pow
  - 2022-2041: `rnew(t) = SUM(prnew[9 rows](t))+SUM(rnvat[2 rows](t))+SUM(rreb[2 rows](t))+SUM(rpex[2 rows](t))`
- Rows: all,all
  - 2022-2041: `rnew(t) = rnew[f,s](t)`

**E464. `rxcp`: Revenue from existing carbon pricing (memo: level; the part embedded in the price data is in rtx)** (USD m real)

- Description: Fuel use x PJ/ktoe x xcp (power: CO2 x coverage x price)
- Legacy: legacy ECP revenue (crv, erv; not used)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `rxcp(t) = ener[f,s](t)*Settings[PJ per ktoe]*(xcp[f,s](t))`
- Rows: all,all
  - 2022-2041: `rxcp(t) = SUMIFS(block{ener, eldem, ctxnew, ets, ... 600 variables}(t),SecVar,"rxcp")+rxcp[f,pow](t)`
- Rows: all,tra, all,bld, all,ind, all,oen
  - 2022-2041: `rxcp(t) = SUMIFS(block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(t),block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(A),"rxcp")`
- Rows: all,pow
  - 2022-2041: `rxcp(t) = SUM(prxl[9 rows](t))`

**E465. `rex`: Revenue from the new excise (fuel price reform; part of rnew)** (USD m real)

- Description: Fuel use x PJ/ktoe x ntx
- Legacy: legacy rows 7753-7771 (additional excise), v0.4.15
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `rex(t) = ener[f,s](t)*Settings[PJ per ktoe]*(ntx[f,s](t))`

**E466. `rvt`: VAT revenue (on the price with existing taxes, and on the changes from existing and new pricing)** (USD m real)

- Description: Fuel use x PJ/ktoe x (vat + (xcpd + nce) x VAT rate)
- Legacy: legacy rows 7864-7876 (VAT), v0.4.15
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `rvt(t) = ener[f,s](t)*Settings[PJ per ktoe]*(vat[<price position>](t)+(xcpd[f,s](t)+nce[f,s](t)+csw[f,s](t)+pcw[f,s](t))*<VAT rate>)`
  - Parameters: `<price position>` = `INDEX(Inputs!U5:U148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<VAT rate>` = `INDEX(Inputs!V5:V148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E467. `rsr`: Subsidy reform revenue (consumer subsidy and price-control phase-outs incl. VAT)** (USD m real)

- Description: Fuel use x PJ/ktoe x (csw + pcw) x (1 + VAT rate) (v0.9.0, R7.3: the producer subsidy phase-out is in the supply cost, its VAT in rvt through vat)
- Legacy: legacy rows 7798-7807 (part of existing revenue; v0.4.16)
- Rows: coa,rod, nga,rod, gso,rod, die,rod, lpg,rod, ker,rod, jfu,rod, oop,rod, bio,rod, coa,ral, nga,ral, gso,ral, ... (144 rows)
  - 2022-2041: `rsr(t) = ener[f,s](t)*Settings[PJ per ktoe]*((csw[f,s](t)+pcw[f,s](t))*(1+<VAT rate>))`
  - Parameters: `<VAT rate>` = `INDEX(Inputs!V5:V148,MATCH(f&"|"&s,Inputs!A5:A148,0))`
- Rows: all,all
  - 2022-2041: `rsr(t) = SUMIFS(block{ener, eldem, ctxnew, ets, ... 600 variables}(t),SecVar,"rsr")+rsr[f,pow](t)`
- Rows: all,tra, all,bld, all,ind, all,oen
  - 2022-2041: `rsr(t) = SUMIFS(block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(t),block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(A),"rsr")`
- Rows: all,pow
  - 2022-2041: `rsr(t) = 0`

### 5b; 6

**E468. `TrModel`: Engineering or elasticity model** (option)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 338 (TrModel; legacy Dashboard G61)
- Rows: all,all
  - 2022-2041: `TrModel(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E469. `tr.sw`: Engineer road model switched on (1 = TrModel Engineer: road gasoline, diesel, LPG, gas and biofuels of section 5 and road electricity of section 3 H come from section 5b)** (0/1)

- Description: Calculation
- Legacy: legacy MTInputs F340 TrModel; Mitigation rows 5428-5440 (switch)
- Rows: all,all
  - 2022-2041: `tr.sw(t) = IF(LEFT(TrModel[f,s](t),8)="Engineer",1,0)`

**E470. `tr.dk`: Data year of the transport data (Transport1 has the year)** (0/1)

- Description: Calculation
- Legacy: legacy columns L-O (2022-2025)
- Rows: all,all
  - 2022-2041: `tr.dk(t) = IF(ISNUMBER(MATCH(year,TrYr,0)),1,0)`

**E471. `tr.col`: Years from the base year, counting the base year as 1** (years)

- Description: Calculation
- Legacy: legacy rows 4739, 4875, 4955
- Rows: all,all
  - 2022-2041: `tr.col(t) = year-BaseYr+1`

**E472. `tr.pol`: Policy scenario (scenario number above 1)** (0/1)

- Description: Calculation
- Legacy: legacy ($C2173>1) (B1 fixed)
- Rows: all,all
  - 2022-2041: `tr.pol(t) = IF(scenario(t)>1,1,0)`

**E473. `TrFbYearPas`: Vehicle feebate: year of introduction, passenger** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 416 (v0.3.5; legacy Dashboard G63)
- Rows: all,all
  - 2022-2041: `TrFbYearPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E474. `TrFbYearFre`: Vehicle feebate: year of introduction, freight** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 417 (v0.3.5; legacy Dashboard L63)
- Rows: all,all
  - 2022-2041: `TrFbYearFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E475. `TrFbYearCyc`: Vehicle feebate: year of introduction, 2-3 wheeler** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 418 (v0.3.5; legacy Dashboard Q63)
- Rows: all,all
  - 2022-2041: `TrFbYearCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E476. `TrFbRatePas`: Vehicle feebate: rate, passenger** (USD/tCO2)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 419 (v0.3.5; legacy Dashboard G64)
- Rows: all,all
  - 2022-2041: `TrFbRatePas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E477. `TrFbRateFre`: Vehicle feebate: rate, freight** (USD/tCO2)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 420 (v0.3.5; legacy Dashboard L64)
- Rows: all,all
  - 2022-2041: `TrFbRateFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E478. `TrFbRateCyc`: Vehicle feebate: rate, 2-3 wheeler** (USD/tCO2)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 421 (v0.3.5; legacy Dashboard Q64)
- Rows: all,all
  - 2022-2041: `TrFbRateCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E479. `TrFbPivotTypePas`: Vehicle feebate: pivot type (Average / Manual), passenger** (option)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 422 (v0.3.5; legacy Dashboard G65)
- Rows: all,all
  - 2022-2041: `TrFbPivotTypePas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E480. `TrFbPivotTypeFre`: Vehicle feebate: pivot type (Average / Manual), freight** (option)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 423 (v0.3.5; legacy Dashboard L65)
- Rows: all,all
  - 2022-2041: `TrFbPivotTypeFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E481. `TrFbPivotTypeCyc`: Vehicle feebate: pivot type (Average / Manual), 2-3 wheeler** (option)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 424 (v0.3.5; legacy Dashboard Q65)
- Rows: all,all
  - 2022-2041: `TrFbPivotTypeCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E482. `TrFbPivotPas`: Vehicle feebate: manual pivot point, passenger** (gCO2/km)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 425 (v0.3.5; legacy Dashboard G66)
- Rows: all,all
  - 2022-2041: `TrFbPivotPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E483. `TrFbPivotFre`: Vehicle feebate: manual pivot point, freight** (gCO2/km)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 426 (v0.3.5; legacy Dashboard L66)
- Rows: all,all
  - 2022-2041: `TrFbPivotFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E484. `TrFbPivotCyc`: Vehicle feebate: manual pivot point, 2-3 wheeler** (gCO2/km)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 427 (v0.3.5; legacy Dashboard Q66)
- Rows: all,all
  - 2022-2041: `TrFbPivotCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E485. `TrFbPivotChgPas`: Vehicle feebate: annual decline of the manual pivot, passenger** (gCO2/km)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 428 (v0.3.5; legacy Dashboard G67)
- Rows: all,all
  - 2022-2041: `TrFbPivotChgPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E486. `TrFbPivotChgFre`: Vehicle feebate: annual decline of the manual pivot, freight** (gCO2/km)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 429 (v0.3.5; legacy Dashboard L67)
- Rows: all,all
  - 2022-2041: `TrFbPivotChgFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E487. `TrFbPivotChgCyc`: Vehicle feebate: annual decline of the manual pivot, 2-3 wheeler** (gCO2/km)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 430 (v0.3.5; legacy Dashboard Q67)
- Rows: all,all
  - 2022-2041: `TrFbPivotChgCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E488. `TrDtYearPas`: Distance tax: year of introduction, passenger** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 431 (v0.3.5; legacy Dashboard G73)
- Rows: all,all
  - 2022-2041: `TrDtYearPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E489. `TrDtYearFre`: Distance tax: year of introduction, freight** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 432 (v0.3.5; legacy Dashboard L73)
- Rows: all,all
  - 2022-2041: `TrDtYearFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E490. `TrDtYearCyc`: Distance tax: year of introduction, 2-3 wheeler** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 433 (v0.3.5; legacy Dashboard Q73)
- Rows: all,all
  - 2022-2041: `TrDtYearCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E491. `TrDtStartPas`: Distance tax: amount in the first year, passenger** (USD/km)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 434 (v0.3.5; legacy Dashboard G74)
- Rows: all,all
  - 2022-2041: `TrDtStartPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E492. `TrDtStartFre`: Distance tax: amount in the first year, freight** (USD/km)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 435 (v0.3.5; legacy Dashboard L74)
- Rows: all,all
  - 2022-2041: `TrDtStartFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E493. `TrDtStartCyc`: Distance tax: amount in the first year, 2-3 wheeler** (USD/km)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 436 (v0.3.5; legacy Dashboard Q74)
- Rows: all,all
  - 2022-2041: `TrDtStartCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E494. `TrDtTargetYearPas`: Distance tax: target year, passenger** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 437 (v0.3.5; legacy Dashboard G75)
- Rows: all,all
  - 2022-2041: `TrDtTargetYearPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E495. `TrDtTargetYearFre`: Distance tax: target year, freight** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 438 (v0.3.5; legacy Dashboard L75)
- Rows: all,all
  - 2022-2041: `TrDtTargetYearFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E496. `TrDtTargetYearCyc`: Distance tax: target year, 2-3 wheeler** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 439 (v0.3.5; legacy Dashboard Q75)
- Rows: all,all
  - 2022-2041: `TrDtTargetYearCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E497. `TrDtTargetPas`: Distance tax: amount in the target year, passenger** (USD/km)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 440 (v0.3.5; legacy Dashboard G76)
- Rows: all,all
  - 2022-2041: `TrDtTargetPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E498. `TrDtTargetFre`: Distance tax: amount in the target year, freight** (USD/km)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 441 (v0.3.5; legacy Dashboard L76)
- Rows: all,all
  - 2022-2041: `TrDtTargetFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E499. `TrDtTargetCyc`: Distance tax: amount in the target year, 2-3 wheeler** (USD/km)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 442 (v0.3.5; legacy Dashboard Q76)
- Rows: all,all
  - 2022-2041: `TrDtTargetCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E500. `TrSubYearPas`: EV purchase subsidy: year of introduction, passenger** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 443 (v0.3.5; legacy Dashboard G69)
- Rows: all,all
  - 2022-2041: `TrSubYearPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E501. `TrSubYearFre`: EV purchase subsidy: year of introduction, freight** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 444 (v0.3.5; legacy Dashboard L69)
- Rows: all,all
  - 2022-2041: `TrSubYearFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E502. `TrSubYearCyc`: EV purchase subsidy: year of introduction, 2-3 wheeler** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 445 (v0.3.5; legacy Dashboard Q69)
- Rows: all,all
  - 2022-2041: `TrSubYearCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E503. `TrSubAmountPas`: EV purchase subsidy: amount, passenger** (USD/vehicle)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 446 (v0.3.5; legacy Dashboard G70)
- Rows: all,all
  - 2022-2041: `TrSubAmountPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E504. `TrSubAmountFre`: EV purchase subsidy: amount, freight** (USD/vehicle)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 447 (v0.3.5; legacy Dashboard L70)
- Rows: all,all
  - 2022-2041: `TrSubAmountFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E505. `TrSubAmountCyc`: EV purchase subsidy: amount, 2-3 wheeler** (USD/vehicle)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 448 (v0.3.5; legacy Dashboard Q70)
- Rows: all,all
  - 2022-2041: `TrSubAmountCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E506. `TrSubChgPas`: EV purchase subsidy: annual change, passenger** (USD/vehicle)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 449 (v0.3.5; legacy Dashboard G71)
- Rows: all,all
  - 2022-2041: `TrSubChgPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E507. `TrSubChgFre`: EV purchase subsidy: annual change, freight** (USD/vehicle)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 450 (v0.3.5; legacy Dashboard L71)
- Rows: all,all
  - 2022-2041: `TrSubChgFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E508. `TrSubChgCyc`: EV purchase subsidy: annual change, 2-3 wheeler** (USD/vehicle)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 451 (v0.3.5; legacy Dashboard Q71)
- Rows: all,all
  - 2022-2041: `TrSubChgCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E509. `TrAdvIceBasePas`: Ad-valorem purchase tax on ICEVs, baseline, passenger** (share)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 452 (v0.3.5; legacy Dashboard G89)
- Rows: all,all
  - 2022-2041: `TrAdvIceBasePas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E510. `TrAdvIceBaseFre`: Ad-valorem purchase tax on ICEVs, baseline, freight** (share)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 453 (v0.3.5; legacy Dashboard L89)
- Rows: all,all
  - 2022-2041: `TrAdvIceBaseFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E511. `TrAdvIceBaseCyc`: Ad-valorem purchase tax on ICEVs, baseline, 2-3 wheeler** (share)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 454 (v0.3.5; legacy Dashboard Q89)
- Rows: all,all
  - 2022-2041: `TrAdvIceBaseCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E512. `TrAdvBevBasePas`: Ad-valorem purchase tax on BEVs, baseline, passenger** (share)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 455 (v0.3.5; legacy Dashboard G90)
- Rows: all,all
  - 2022-2041: `TrAdvBevBasePas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E513. `TrAdvBevBaseFre`: Ad-valorem purchase tax on BEVs, baseline, freight** (share)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 456 (v0.3.5; legacy Dashboard L90)
- Rows: all,all
  - 2022-2041: `TrAdvBevBaseFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E514. `TrAdvBevBaseCyc`: Ad-valorem purchase tax on BEVs, baseline, 2-3 wheeler** (share)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 457 (v0.3.5; legacy Dashboard Q90)
- Rows: all,all
  - 2022-2041: `TrAdvBevBaseCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E515. `TrAdvIcePolPas`: Ad-valorem purchase tax on ICEVs, policy, passenger** (share)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 458 (v0.3.5; legacy Dashboard G91)
- Rows: all,all
  - 2022-2041: `TrAdvIcePolPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E516. `TrAdvIcePolFre`: Ad-valorem purchase tax on ICEVs, policy, freight** (share)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 459 (v0.3.5; legacy Dashboard L91)
- Rows: all,all
  - 2022-2041: `TrAdvIcePolFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E517. `TrAdvIcePolCyc`: Ad-valorem purchase tax on ICEVs, policy, 2-3 wheeler** (share)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 460 (v0.3.5; legacy Dashboard Q91)
- Rows: all,all
  - 2022-2041: `TrAdvIcePolCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E518. `TrAdvBevPolPas`: Ad-valorem purchase tax on BEVs, policy, passenger** (share)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 461 (v0.3.5; legacy Dashboard G92)
- Rows: all,all
  - 2022-2041: `TrAdvBevPolPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E519. `TrAdvBevPolFre`: Ad-valorem purchase tax on BEVs, policy, freight** (share)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 462 (v0.3.5; legacy Dashboard L92)
- Rows: all,all
  - 2022-2041: `TrAdvBevPolFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E520. `TrAdvBevPolCyc`: Ad-valorem purchase tax on BEVs, policy, 2-3 wheeler** (share)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 463 (v0.3.5; legacy Dashboard Q92)
- Rows: all,all
  - 2022-2041: `TrAdvBevPolCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E521. `TrAdvYearPas`: Ad-valorem purchase tax: year of the policy rate, passenger** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 464 (v0.3.5; legacy Dashboard G93)
- Rows: all,all
  - 2022-2041: `TrAdvYearPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E522. `TrAdvYearFre`: Ad-valorem purchase tax: year of the policy rate, freight** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 465 (v0.3.5; legacy Dashboard L93)
- Rows: all,all
  - 2022-2041: `TrAdvYearFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E523. `TrAdvYearCyc`: Ad-valorem purchase tax: year of the policy rate, 2-3 wheeler** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 466 (v0.3.5; legacy Dashboard Q93)
- Rows: all,all
  - 2022-2041: `TrAdvYearCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E524. `TrCustYearPas`: Customs duty on BEVs: year of the policy rate, passenger** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 467 (v0.3.5; legacy Dashboard G86)
- Rows: all,all
  - 2022-2041: `TrCustYearPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E525. `TrCustYearFre`: Customs duty on BEVs: year of the policy rate, freight** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 468 (v0.3.5; legacy Dashboard L86)
- Rows: all,all
  - 2022-2041: `TrCustYearFre(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E526. `TrCustYearCyc`: Customs duty on BEVs: year of the policy rate, 2-3 wheeler** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 469 (v0.3.5; legacy Dashboard Q86)
- Rows: all,all
  - 2022-2041: `TrCustYearCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E527. `TrVatYearPas`: VAT on BEVs: year of the policy rate, passenger** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 470 (v0.3.5; legacy Dashboard G81)
- Rows: all,all
  - 2022-2041: `TrVatYearPas(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E528. `TrVatYearCyc`: VAT on BEVs: year of the policy rate, 2-3 wheeler** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 471 (v0.3.5; legacy Dashboard Q81)
- Rows: all,all
  - 2022-2041: `TrVatYearCyc(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E529. `TrVatPolFactor`: VAT on BEVs, policy: factor on the baseline VAT rate** (factor)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 472 (v0.3.5; legacy formula literal *1)
- Rows: all,all
  - 2022-2041: `TrVatPolFactor(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E530. `TrCustPolFactor`: Customs duty on BEVs, policy: factor on the baseline duty** (factor)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 473 (v0.3.5; legacy formula literal *1)
- Rows: all,all
  - 2022-2041: `TrCustPolFactor(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E531. `TrCsStartYear`: Charging-station subsidy: start year** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 474 (v0.3.5; legacy Dashboard G97, labelled "target year")
- Rows: all,all
  - 2022-2041: `TrCsStartYear(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E532. `TrCsStartLevel`: Charging-station subsidy: share of the cost in the start year** (share)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 475 (v0.3.5; legacy Dashboard G95, labelled "start year")
- Rows: all,all
  - 2022-2041: `TrCsStartLevel(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E533. `TrCsTargetYear`: Charging-station subsidy: target year** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 476 (v0.3.5; legacy Dashboard G98, labelled "target level")
- Rows: all,all
  - 2022-2041: `TrCsTargetYear(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E534. `TrCsTargetLevel`: Charging-station subsidy: share of the cost in the target year** (share)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 477 (v0.3.5; legacy Dashboard G96, labelled "start level")
- Rows: all,all
  - 2022-2041: `TrCsTargetLevel(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E535. `trp.life`: Vehicle lifetimes** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy J4322, J4324-L4324
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<ownership years, new passenger>` = `INDEX(TrParVal,MATCH("own_years|pass",TrParKey,0))`; `<useful life, passenger>` = `INDEX(TrParVal,MATCH("life|pass",TrParKey,0))`; `<useful life, freight>` = `INDEX(TrParVal,MATCH("life|fre",TrParKey,0))`; `<useful life, 2-3 wheeler>` = `INDEX(TrParVal,MATCH("life|cyc",TrParKey,0))`

**E536. `trp.dep`: First-year depreciation and the insurance factor** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy J4325-L4325; 0.5 in rows 4541 ff.
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<first-year depreciation, passenger>` = `INDEX(TrParVal,MATCH("dep1|pass",TrParKey,0))`; `<first-year depreciation, freight>` = `INDEX(TrParVal,MATCH("dep1|fre",TrParKey,0))`; `<first-year depreciation, 2-3 wheeler>` = `INDEX(TrParVal,MATCH("dep1|cyc",TrParKey,0))`; `<factor on the insurance annuity>` = `INDEX(TrParVal,MATCH("ins_factor",TrParKey,0))`

**E537. `trp.ins`: Insurance (share of the vehicle value a year)** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy J4326-L4326
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<insurance, passenger>` = `INDEX(TrParVal,MATCH("ins|pass",TrParKey,0))`; `<insurance, freight>` = `INDEX(TrParVal,MATCH("ins|fre",TrParKey,0))`; `<insurance, 2-3 wheeler>` = `INDEX(TrParVal,MATCH("ins|cyc",TrParKey,0))`

**E538. `trp.mic`: Maintenance cost of ICEVs** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy J4327-L4327
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<USD/km, passenger>` = `INDEX(TrParVal,MATCH("maint_ice|pass",TrParKey,0))`; `<USD/km, freight>` = `INDEX(TrParVal,MATCH("maint_ice|fre",TrParKey,0))`; `<USD/km, 2-3 wheeler>` = `INDEX(TrParVal,MATCH("maint_ice|cyc",TrParKey,0))`

**E539. `trp.mev`: Maintenance cost of EVs** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy J4328-L4328
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<USD/km, passenger>` = `INDEX(TrParVal,MATCH("maint_ev|pass",TrParKey,0))`; `<USD/km, freight>` = `INDEX(TrParVal,MATCH("maint_ev|fre",TrParKey,0))`; `<USD/km, 2-3 wheeler>` = `INDEX(TrParVal,MATCH("maint_ev|cyc",TrParKey,0))`

**E540. `trp.inc`: Income elasticity of distance driven** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy J4330-L4330
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<passenger>` = `INDEX(TrParVal,MATCH("inc_el_vkt|pass",TrParKey,0))`; `<freight>` = `INDEX(TrParVal,MATCH("inc_el_vkt|fre",TrParKey,0))`; `<2-3 wheeler>` = `INDEX(TrParVal,MATCH("inc_el_vkt|cyc",TrParKey,0))`

**E541. `trp.gap`: Fuel economy of new vehicles above the stock average (data years)** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy J4331-L4331
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<passenger>` = `INDEX(TrParVal,MATCH("fe_gap|pass",TrParKey,0))`; `<freight>` = `INDEX(TrParVal,MATCH("fe_gap|fre",TrParKey,0))`; `<2-3 wheeler>` = `INDEX(TrParVal,MATCH("fe_gap|cyc",TrParKey,0))`

**E542. `trp.k`: Logit k-parameter of the EV choice** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy J4332-L4332
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<passenger>` = `INDEX(TrParVal,MATCH("k|pass",TrParKey,0))`; `<freight>` = `INDEX(TrParVal,MATCH("k|fre",TrParKey,0))`; `<2-3 wheeler>` = `INDEX(TrParVal,MATCH("k|cyc",TrParKey,0))`

**E543. `trp.own`: Vehicle ownership: adjustment speed and Gompertz income coefficient** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy T4322:U4323
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<adjustment speed, passenger>` = `INDEX(TrParVal,MATCH("own_adj|pass",TrParKey,0))`; `<adjustment speed, freight>` = `INDEX(TrParVal,MATCH("own_adj|fre",TrParKey,0))`; `<Gompertz income coefficient, passenger>` = `INDEX(TrParVal,MATCH("own_gomp_b|pass",TrParKey,0))`; `<Gompertz income coefficient, freight>` = `INDEX(TrParVal,MATCH("own_gomp_b|fre",TrParKey,0))`

**E544. `trp.ogr`: Vehicle ownership: maximum annual growth; Gompertz constant** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy T4327:V4327; -5.897 in rows 4786, 4902
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<maximum growth, passenger>` = `INDEX(TrParVal,MATCH("own_max_growth|pass",TrParKey,0))`; `<maximum growth, freight>` = `INDEX(TrParVal,MATCH("own_max_growth|fre",TrParKey,0))`; `<maximum growth, 2-3 wheeler>` = `INDEX(TrParVal,MATCH("own_max_growth|cyc",TrParKey,0))`; `<Gompertz constant>` = `INDEX(TrParVal,MATCH("gomp_a",TrParKey,0))`

**E545. `trp.odc`: Vehicle ownership: maximum annual decrease (passenger and freight TrOwnDecline, fix B4)** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy T4328:V4328 (0 for passenger and freight: B4)
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<passenger (TrOwnDecline)>` = `TrOwnDecline`; `<freight (TrOwnDecline)>` = `TrOwnDecline`; `<2-3 wheeler>` = `INDEX(TrParVal,MATCH("own_max_decline|cyc",TrParKey,0))`

**E546. `trp.vkt`: Distance for the purchase decision: freight limits and price response** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy U4325:U4326; Dashboard Q551
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<minimum freight km>` = `INDEX(TrParVal,MATCH("fre_vkt_min",TrParKey,0))`; `<maximum freight km>` = `INDEX(TrParVal,MATCH("fre_vkt_max",TrParKey,0))`; `<responds to prices (Yes / No)>` = `INDEX(TrParVal,MATCH("vkt_new_price",TrParKey,0))`; `<prices act (1 = yes)>` = `IF(<responds to prices (Yes / No)>="No",0,1)`

**E547. `trp.cap`: Cap on the BEV / ICEV distance ratio (data years)** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy H2056, H2114, H2136
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<passenger>` = `INDEX(TrParVal,MATCH("bev_vkt_cap|pass",TrParKey,0))`; `<freight>` = `INDEX(TrParVal,MATCH("bev_vkt_cap|fre",TrParKey,0))`; `<2-3 wheeler>` = `INDEX(TrParVal,MATCH("bev_vkt_cap|cyc",TrParKey,0))`

**E548. `trp.chs`: Charging stations and range anxiety: elasticities** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy P4322, P4327, P4328
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<stations to the BEV stock>` = `INDEX(TrParVal,MATCH("ch_el_stock",TrParKey,0))`; `<stations to their cost>` = `INDEX(TrParVal,MATCH("ch_el_cost",TrParKey,0))`; `<range anxiety to stations>` = `INDEX(TrParVal,MATCH("ra_el_stations",TrParKey,0))`

**E549. `trp.mku`: Charging mark-up on the electricity price** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy P4323:P4326
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<minimum USD/kWh>` = `INDEX(TrParVal,MATCH("ch_cost_min",TrParKey,0))`; `<maximum USD/kWh>` = `INDEX(TrParVal,MATCH("ch_cost_max",TrParKey,0))`; `<EV share of the minimum>` = `INDEX(TrParVal,MATCH("ch_sat",TrParKey,0))`; `<share of public charging>` = `INDEX(TrParVal,MATCH("ch_public",TrParKey,0))`

**E550. `trp.dsc`: Consumer discount rate by income** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy Z4322:Z4325
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<rate at low income>` = `INDEX(TrParVal,MATCH("disc_max",TrParKey,0))`; `<rate at high income>` = `INDEX(TrParVal,MATCH("disc_min",TrParKey,0))`; `<low income (USD)>` = `INDEX(TrParVal,MATCH("disc_inc_low",TrParKey,0))`; `<high income (USD)>` = `INDEX(TrParVal,MATCH("disc_inc_high",TrParKey,0))`

**E551. `trp.ice`: ICE fuel split elasticities; gas and PHEV unit factors** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy T4329:T4330; /26 and x9 in rows 4370, 4371
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<own-TCO elasticity>` = `INDEX(TrParVal,MATCH("own_price_el",TrParKey,0))`; `<cross-TCO elasticity>` = `INDEX(TrParVal,MATCH("cross_price_el",TrParKey,0))`; `<gas liters per GJ>` = `INDEX(TrParVal,MATCH("gas_l_per_gj",TrParKey,0))`; `<PHEV kWh per liter>` = `INDEX(TrParVal,MATCH("phev_l_per_kwh",TrParKey,0))`

**E552. `trp.frs`: Freight share of ownership and the 2-3 wheeler hump** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy H2168:I2169
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<freight: income at the target>` = `INDEX(TrParVal,MATCH("fre_inc_target",TrParKey,0))`; `<freight: target share>` = `INDEX(TrParVal,MATCH("fre_share_target",TrParKey,0))`; `<2-3 wheeler: peak income>` = `INDEX(TrParVal,MATCH("cyc_peak_inc",TrParKey,0))`; `<2-3 wheeler: scale>` = `INDEX(TrParVal,MATCH("cyc_scale",TrParKey,0))`

**E553. `trp.yrs`: Data years of customs, import shares and bus electricity; electricity reconciliation** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy Dashboard G83:Q87, N2064, Q556
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<customs year>` = `INDEX(TrParVal,MATCH("customs_year",TrParKey,0))`; `<import-share year>` = `INDEX(TrParVal,MATCH("import_year",TrParKey,0))`; `<bus electricity year>` = `INDEX(TrParVal,MATCH("bus_ele_year",TrParKey,0))`; `<reconcile electricity>` = `INDEX(TrParVal,MATCH("recon_ele",TrParKey,0))`

**E554. `trp.ela`: Road elasticities (Inputs, road): usage (distance) and efficiency (new fuel economy)** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy _el_dem_gso_rod, _el_dem_die_rod, _el_eff_gso_rod, _el_eff_die_rod
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<usage, gasoline>` = `INDEX(Inputs!P5:P148,MATCH("gso|rod",Inputs!A5:A148,0))`; `<usage, diesel>` = `INDEX(Inputs!P5:P148,MATCH("die|rod",Inputs!A5:A148,0))`; `<efficiency, gasoline>` = `INDEX(Inputs!Q5:Q148,MATCH("gso|rod",Inputs!A5:A148,0))`; `<efficiency, diesel>` = `INDEX(Inputs!Q5:Q148,MATCH("die|rod",Inputs!A5:A148,0))`

**E555. `trp.mod`: Autonomous efficiency gain (road oil), GWh per ktoe, VAT on vehicles** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy _eff_imp_oil_rod; GWh per ktoe; Mitigation N726
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<autonomous efficiency gain>` = `INDEX(Inputs!R5:R148,MATCH("gso|rod",Inputs!A5:A148,0))`; `<GWh per ktoe>` = `Inputs!B260`; `<VAT rate on vehicles (customs year)>` = `INDEX(PDomVal,MATCH(CtryCode&<customs year of trp.yrs[f,s]>,PDomKey,0),MATCH("VAT_WEO",PDomHdr,0))+0`

**E556. `trp.gj`: GJ per liter** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy conversion factors
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<Gasoline>` = `INDEX(Inputs!K5:K148,MATCH("gso|rod",Inputs!A5:A148,0))`; `<Diesel>` = `INDEX(Inputs!K5:K148,MATCH("die|rod",Inputs!A5:A148,0))`; `<LPG>` = `INDEX(Inputs!K5:K148,MATCH("lpg|rod",Inputs!A5:A148,0))`

**E557. `trp.lpk`: Liters per ktoe (gas: liters of gasoline equivalent, as legacy)** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy _conv_ktoe_liter_* (gas uses the gasoline factor)
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<Gasoline>` = `Settings[PJ per ktoe]*Million/<Gasoline of trp.gj[f,s]>`; `<Diesel>` = `Settings[PJ per ktoe]*Million/<Diesel of trp.gj[f,s]>`; `<LPG>` = `Settings[PJ per ktoe]*Million/<LPG of trp.gj[f,s]>`; `<natural gas>` = `<Gasoline>`

**E558. `trp.ef`: Emission factors (tCO2 per liter; gas per GJ / gas liters per GJ)** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy G4375:G4378 (road EFs: fix B7)
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<Gasoline>` = `INDEX(Inputs!W5:W148,MATCH("gso|rod",Inputs!A5:A148,0))*<Gasoline of trp.gj[f,s]>`; `<Diesel>` = `INDEX(Inputs!W5:W148,MATCH("die|rod",Inputs!A5:A148,0))*<Diesel of trp.gj[f,s]>`; `<LPG>` = `INDEX(Inputs!W5:W148,MATCH("lpg|rod",Inputs!A5:A148,0))*<LPG of trp.gj[f,s]>`; `<natural gas>` = `INDEX(Inputs!W5:W148,MATCH("nga|rod",Inputs!A5:A148,0))/<gas liters per GJ of trp.ice[f,s]>`

**E559. `trp.eb`: Road fuel use in the base year (ktoe; energy balance, Inputs)** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy _EnergyConsumptionBaseYear (rows 583-602)
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<Gasoline>` = `INDEX(Inputs!X5:X148,MATCH("gso|rod",Inputs!A5:A148,0))`; `<Diesel>` = `INDEX(Inputs!X5:X148,MATCH("die|rod",Inputs!A5:A148,0))`; `<LPG>` = `INDEX(Inputs!X5:X148,MATCH("lpg|rod",Inputs!A5:A148,0))`; `<Natural gas>` = `INDEX(Inputs!X5:X148,MATCH("nga|rod",Inputs!A5:A148,0))`

**E560. `trp.ebb`: Road biofuels in the base year, Balances (ktoe)** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy rows 535-552 (column E)
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<bioethanol>` = `IFERROR(INDEX(BalVal,MATCH(CtryCode&"|road",BalKey,0),MATCH("bgs",BalFuel,0)),0)`; `<biodiesel>` = `IFERROR(INDEX(BalVal,MATCH(CtryCode&"|road",BalKey,0),MATCH("bdi",BalFuel,0)),0)`; `<other biofuels>` = `IFERROR(INDEX(BalVal,MATCH(CtryCode&"|road",BalKey,0),MATCH("obf",BalFuel,0)),0)`

**E561. `trp.ebc`: Road biofuels in the base year, EnergyCons (ktoe)** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy rows 598-600 (column G)
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<bioethanol>` = `IFERROR(INDEX(ConsVal,MATCH(CodePrefix&"enc.bgs",ConsKey,0),MATCH("rod",ConsSub,0)),0)`; `<biodiesel>` = `IFERROR(INDEX(ConsVal,MATCH(CodePrefix&"enc.bdi",ConsKey,0),MATCH("rod",ConsSub,0)),0)`; `<other biofuels>` = `IFERROR(INDEX(ConsVal,MATCH(CodePrefix&"enc.obf",ConsKey,0),MATCH("rod",ConsSub,0)),0)`

**E562. `trp.eb2`: Road electricity and biofuels in the base year (ktoe; biofuels: Balances or EnergyCons, MTInputs BalancesOrConsumption)** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy rows 3725, 598-600
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<electricity (PowerDemand)>` = `INDEX(Inputs!E238:E252,MATCH("rod",Inputs!A238:A252,0))`; `<bioethanol>` = `IF(LEFT(BalOpt,3)="Bal",<bioethanol of trp.ebb[f,s]>,<bioethanol of trp.ebc[f,s]>)`; `<biodiesel>` = `IF(LEFT(BalOpt,3)="Bal",<biodiesel of trp.ebb[f,s]>,<biodiesel of trp.ebc[f,s]>)`; `<other biofuels>` = `IF(LEFT(BalOpt,3)="Bal",<other biofuels of trp.ebb[f,s]>,<other biofuels of trp.ebc[f,s]>)`

**E563. `trp.efa`: Fossil share of road gasoline and diesel (base year): scales the CO2 per liter of the vehicle feebate, as legacy** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy E2146:E2147
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<gasoline>` = `IFERROR(<Gasoline of trp.eb[f,s]>/(<Gasoline of trp.eb[f,s]>+<bioethanol of trp.eb2[f,s]>),1)`; `<diesel>` = `IFERROR(<Diesel of trp.eb[f,s]>/(<Diesel of trp.eb[f,s]>+<biodiesel of trp.eb2[f,s]>),1)`

**E564. `trshf`: Share of road fuel use by vehicle type (Transport1)** (share)

- Description: Sheet Transport1 (country, data years; blank = 0)
- Legacy: legacy rows 2017-2031 (L)
- Rows: gso,pas, gso,cyc, die,pas, die,bus, die,fre, lpg,pas, lpg,bus, lpg,fre, nga,pas, nga,bus, nga,fre
  - 2022-2041: `trshf(t) = IFERROR(INDEX(TrVal,MATCH(CtryCode&"|"&year,TrKey,0),MATCH(<Transport1 variable>,TrVar,0))+0,"")`
  - Parameters: `<Transport1 variable>` = `data`

**E565. `trfe`: Fuel economy of the stock (Transport1)** (km/l (BEV km/kWh))

- Description: Sheet Transport1 (country, data years; blank = 0)
- Legacy: legacy rows 2034-2050, 2092-2094, 2121
- Rows: ice,lgt, gso,pas, die,pas, lpg,pas, nga,pas, phv,pas, bev,pas, die,fre, lpg,fre, nga,fre, gso,cyc
  - 2022-2041: `trfe(t) = IFERROR(INDEX(TrVal,MATCH(CtryCode&"|"&year,TrKey,0),MATCH(<Transport1 variable>,TrVar,0))+0,"")`
  - Parameters: `<Transport1 variable>` = `data`

**E566. `trown`: Vehicle ownership (Transport1)** (per 1,000 people)

- Description: Sheet Transport1 (country, data years; blank = 0)
- Legacy: legacy rows 2036, 2037, 2108, 2129
- Rows: all,pas, all,lgt, all,fre, all,cyc
  - 2022-2041: `trown(t) = IFERROR(INDEX(TrVal,MATCH(CtryCode&"|"&year,TrKey,0),MATCH(<Transport1 variable>,TrVar,0))+0,"")`
  - Parameters: `<Transport1 variable>` = `data`

**E567. `trvkd`: Average distance driven (Transport1)** (km per vehicle)

- Description: Sheet Transport1 (country, data years; blank = 0)
- Legacy: legacy rows 2058, 2059, 2115, 2133
- Rows: all,pas, all,lgt, all,fre, all,cyc
  - 2022-2041: `trvkd(t) = IFERROR(INDEX(TrVal,MATCH(CtryCode&"|"&year,TrKey,0),MATCH(<Transport1 variable>,TrVar,0))+0,"")`
  - Parameters: `<Transport1 variable>` = `data`

**E568. `trevp`: EV share of purchases (Transport1)** (share)

- Description: Sheet Transport1 (country, data years; blank = 0)
- Legacy: legacy rows 2063, 2065, 2067, 2101, 2126
- Rows: ev,pas, bev,pas, bev,lgt, bev,fre, bev,cyc
  - 2022-2041: `trevp(t) = IFERROR(INDEX(TrVal,MATCH(CtryCode&"|"&year,TrKey,0),MATCH(<Transport1 variable>,TrVar,0))+0,"")`
  - Parameters: `<Transport1 variable>` = `data`

**E569. `trevo`: EV share of the stock (Transport1)** (share)

- Description: Sheet Transport1 (country, data years; blank = 0)
- Legacy: legacy rows 2064, 2066, 2068, 2102, 2127
- Rows: ev,pas, bev,pas, bev,lgt, bev,fre, bev,cyc
  - 2022-2041: `trevo(t) = IFERROR(INDEX(TrVal,MATCH(CtryCode&"|"&year,TrKey,0),MATCH(<Transport1 variable>,TrVar,0))+0,"")`
  - Parameters: `<Transport1 variable>` = `data`

**E570. `trdut`: Import duty (Transport1)** (share)

- Description: Sheet Transport1 (country, data years; blank = 0)
- Legacy: legacy rows 2157-2162
- Rows: bev,cyc, bev,fre, bev,pas, ice,cyc, ice,fre, ice,pas
  - 2022-2041: `trdut(t) = IFERROR(INDEX(TrVal,MATCH(CtryCode&"|"&year,TrKey,0),MATCH(<Transport1 variable>,TrVar,0))+0,"")`
  - Parameters: `<Transport1 variable>` = `data`

**E571. `trimp`: Share of imported vehicles (Transport1)** (share)

- Description: Sheet Transport1 (country, data years; blank = 0)
- Legacy: legacy rows 2163, 2164
- Rows: all,pas, all,fre
  - 2022-2041: `trimp(t) = IFERROR(INDEX(TrVal,MATCH(CtryCode&"|"&year,TrKey,0),MATCH(<Transport1 variable>,TrVar,0))+0,"")`
  - Parameters: `<Transport1 variable>` = `data`

**E572. `trusd`: Share of used vehicles in passenger purchases (Transport1)** (share)

- Description: Sheet Transport1 (country, data years; blank = 0)
- Legacy: legacy row 2150
- Rows: all,pas
  - 2022-2041: `trusd(t) = IFERROR(INDEX(TrVal,MATCH(CtryCode&"|"&year,TrKey,0),MATCH(<Transport1 variable>,TrVar,0))+0,"")`
  - Parameters: `<Transport1 variable>` = `data`

**E573. `trchs`: EV charging stations (Transport1)** (stations)

- Description: Sheet Transport1 (country, data years; blank = 0)
- Legacy: legacy row 2165
- Rows: all,all
  - 2022-2041: `trchs(t) = IFERROR(INDEX(TrVal,MATCH(CtryCode&"|"&year,TrKey,0),MATCH(<Transport1 variable>,TrVar,0))+0,"")`
  - Parameters: `<Transport1 variable>` = `data`

**E574. `trsat`: Ownership saturation point (Transport1)** (per 1,000 people)

- Description: Sheet Transport1 (country, data years; blank = 0)
- Legacy: legacy row 2166
- Rows: all,all
  - 2022-2041: `trsat(t) = IFERROR(INDEX(TrVal,MATCH(CtryCode&"|"&year,TrKey,0),MATCH(<Transport1 variable>,TrVar,0))+0,"")`
  - Parameters: `<Transport1 variable>` = `data`

**E575. `trfeb`: BEV fuel economy of the stock, light, freight, 2-3 wheeler (path)** (km/kWh)

- Description: Sheet TransportPaths (global paths)
- Legacy: legacy rows 2051, 2095, 2122 (hardcoded)
- Rows: bev,lgt, bev,fre, bev,cyc
  - 2022-2041: `trfeb(t) = INDEX(TrPathVal,MATCH(<TransportPaths key>,TrPathKey,0),MATCH(year,TrPathYr,0))`
  - Parameters: `<TransportPaths key>` = `data`

**E576. `trcpp`: Charging-station cost per port (path)** (USD/port)

- Description: Sheet TransportPaths (global paths)
- Legacy: legacy row 2170 (hardcoded)
- Rows: all,all
  - 2022-2041: `trcpp(t) = INDEX(TrPathVal,MATCH(<TransportPaths key>,TrPathKey,0),MATCH(year,TrPathYr,0))`
  - Parameters: `<TransportPaths key>` = `data`

**E577. `trfen`: BEV fuel economy of new vehicles (path)** (km/kWh)

- Description: Sheet Manual inputs J375:AC377 (legacy addresses; v0.5.2)
- Legacy: legacy Manual inputs rows 375-377 (Mitigation rows 4399, 4433, 4446)
- Rows: bev,pas, bev,fre, bev,cyc
  - 2022-2041: `trfen(t) = INDEX(BEVFEVal,MATCH(<Label of the row in Manual inputs D375:D377 (legacy label)>,BEVFELab,0),MATCH(year,BEVFEYr,0))`
  - Parameters: `<Label of the row in Manual inputs D375:D377 (legacy label)>` = `data`

**E578. `trvp`: Vehicle purchase price (Transport2; last price carried forward)** (USD/vehicle)

- Description: Sheet Transport2 (country, 2022-2040)
- Legacy: legacy rows 2151-2156
- Rows: ice,pas, bev,pas, ice,fre, bev,fre, ice,cyc, bev,cyc
  - 2022-2041: `trvp(t) = IFERROR(INDEX(VPVal,MATCH(CtryCode&"|"&year,VPKey,0),MATCH(<Transport2 variable>,VPVar,0)),N(trvp[f,s](t-1)))`
  - Parameters: `<Transport2 variable>` = `data`

**E579. `trp.bsh`: Base-year road fuel use by vehicle type: share, ktoe, bln liters (light = rest)** (-)

- Description: Transport1 shares x energy balance
- Legacy: legacy rows 2017-2031 (L share, M ktoe, N bln liters)
- Rows: gso,pas, gso,cyc, gso,lgt, die,pas, die,bus, die,fre, die,lgt, lpg,pas, lpg,bus, lpg,fre, lpg,lgt, nga,pas, ... (15 rows)
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<share>` = `trshf[f,s](2022)`; `<ktoe>` = `<share>*<Gasoline of trp.eb[all,all]>`; `<bln liters>` = `<ktoe>*<Gasoline of trp.lpk[all,all]>/Billion`

**E580. `trp.tax`: Purchase taxes: VAT (no VAT on freight vehicles, as legacy), import duty on ICEVs and BEVs (customs year), share of imports (import-share year; 2-3 wheelers: passenger)** (-)

- Description: Transport1, Prices_dom VAT_WEO
- Legacy: legacy side table V4304:X4312
- Rows: all,pas, all,fre, all,cyc
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<VAT rate>` = `<VAT rate on vehicles (customs year) of trp.mod[f,all]>`; `<duty, ICEV>` = `INDEX(trdut[ice,s](2022..2041),<customs year of trp.yrs[f,all]>-BaseYr+1)`; `<duty, BEV>` = `INDEX(trdut[bev,s](2022..2041),<customs year of trp.yrs[f,all]>-BaseYr+1)`; `<share of imports>` = `INDEX(trimp[f,s](2022..2041),<import-share year of trp.yrs[f,all]>-BaseYr+1)`

**E581. `trp.bus`: Buses: road fuel use of the base year (ktoe; electricity = EV stock share x bus fuel)** (ktoe)

- Description: Transport1, energy balance
- Legacy: legacy rows 2140-2143
- Rows: all,bus
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<diesel>` = `<ktoe of trp.bsh[die,s]>`; `<LPG>` = `<ktoe of trp.bsh[lpg,s]>`; `<natural gas>` = `<ktoe of trp.bsh[nga,s]>`; `<electricity>` = `INDEX(trevo[ev,pas](2022..2041),<bus electricity year of trp.yrs[f,all]>-BaseYr+1)*SUM(trp.bus[f,s][D:F])`

**E582. `trprl`: Road fuel price incl. new policies (after-tax price x GJ per liter)** (USD/liter)

- Description: Section 5 road atp
- Legacy: legacy rows 2589, 2612, 2635 (L4367-L4369)
- Rows: gso,rod, die,rod, lpg,rod
  - 2022-2041: `trprl(t) = atp[f,s](t)*<GJ per liter (Inputs)>`
  - Parameters: `<GJ per liter (Inputs)>` = `INDEX(Inputs!K5:K148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E583. `trprg`: Road natural gas price incl. new policies per liter equivalent (residential gas, / gas liters per GJ)** (USD/liter eq.)

- Description: Calculation
- Legacy: legacy L4370 = L2543/26
- Rows: nga,rod
  - 2022-2041: `trprg(t) = atp[f,s](t)/<gas liters per GJ of trp.ice[all,all]>`

**E584. `trpphv`: PHEV fuel price: gasoline share x gasoline price + rest x EV electricity price x kWh per liter** (USD/liter eq.)

- Description: Calculation
- Legacy: legacy row 4371
- Rows: phv,pas
  - 2022-2041: `trpphv(t) = trphg[f,s](t)*trprl[gso,rod](t)+(1-trphg[f,s](t))*(trpev[ecy,res](t)*<PHEV kWh per liter of trp.ice[all,all]>)`

**E585. `trpri`: Industrial natural gas price incl. the road new policies (freight LNG)** (USD/GJ)

- Description: Section 2 rpb + section 5 road nce, xcpd
- Legacy: legacy L2566
- Rows: nga,ind
  - 2022-2041: `trpri(t) = MAX(pbc[<price position (nga.ind)>](t)+(nce[f,rod](t)+xcpd[f,rod](t))*(1+<VAT rate (nga.ind)>),PriceFloor)`
  - Parameters: `<price position (nga.ind)>` = `INDEX(Inputs!E158:E169,MATCH("nga.ind",Inputs!A158:A169,0))`; `<VAT rate (nga.ind)>` = `INDEX(Inputs!V158:V169,MATCH("nga.ind",Inputs!A158:A169,0))`

**E586. `trprn`: Freight fuel price net of VAT** (USD/liter)

- Description: Calculation
- Legacy: legacy L2612-L2618, L2635-L2641
- Rows: die,rod, lpg,rod
  - 2022-2041: `trprn(t) = trprl[f,s](t)/(1+<VAT rate (Inputs)>)`
  - Parameters: `<VAT rate (Inputs)>` = `INDEX(Inputs!V5:V148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E587. `trprm`: Freight LNG price net of VAT per liter equivalent** (USD/liter eq.)

- Description: Calculation
- Legacy: legacy L4412 = (L2566-L2572)/26
- Rows: nga,fre
  - 2022-2041: `trprm(t) = trpri[f,ind](t)/((1+<VAT rate (nga.ind) of trpri[f,ind]>)*<gas liters per GJ of trp.ice[all,all]>)`

**E588. `trpop`: Population (section 14, in millions)** (million)

- Description: Calculation
- Legacy: legacy row 428
- Rows: all,all
  - 2022-2041: `trpop(t) = pop[f,s](t)/Thousand`

**E589. `trgpc`: GDP per capita (section 16 real GDP after the feedback / population)** (USD)

- Description: Calculation
- Legacy: legacy row 444 (2167)
- Rows: all,all
  - 2022-2041: `trgpc(t) = (gdp.pos.usd[f,s](t)*Million)/pop[f,s](t)`

**E590. `trgdl`: GDP growth of the previous year (row 7; base year: WEO)** (%)

- Description: Calculation
- Legacy: legacy rows 4463, 4487, 4501 (lagged row 2446; B2 fixed)
- Rows: all,all
  - 2022: `trgdl(t) = N(INDEX(WEOVal,MATCH(CtryCode&"|gdp_growth",WEOKey,0),MATCH(year-1,WEOYear,0)))`
  - 2023-2041: `trgdl(t) = gdp.pos.pct(t-1)`

**E591. `trdisc`: Consumer discount rate (linear in GDP per capita between the two income levels)** (share)

- Description: Calculation
- Legacy: legacy row 4531 (freight: fix B8w)
- Rows: all,all
  - 2022-2041: `trdisc(t) = MIN(<rate at low income of trp.dsc[f,s]>,MAX(<rate at high income of trp.dsc[f,s]>,<rate at low income of trp.dsc[f,s]>-(trgpc[f,s](t)-<low income (USD) of trp.dsc[f,s]>)/(<high income (USD) of trp.dsc[f,s]>-<low income (USD) of trp.dsc[f,s]>)*(<rate at low income of trp.dsc[f,s]>-<rate at high income of trp.dsc[f,s]>)))`

**E592. `trsps`: Passenger share of passenger and light ownership** (share)

- Description: Calculation
- Legacy: legacy row 2038
- Rows: all,pas
  - 2022-2041: `trsps(t) = IF(tr.dk[f,all](t)=1,trown[f,s](t)/(trown[f,s](t)+trown[f,lgt](t)),"")`

**E593. `trfem`: Fuel economy, passenger and light blended** (km/l)

- Description: Calculation
- Legacy: legacy rows 2041, 2043
- Rows: gso,pas, die,pas
  - 2022-2041: `trfem(t) = IF(tr.dk[all,all](t)=1,trfe[f,s](t)*trsps[all,s](t)+trfe[ice,lgt](t)*(1-trsps[all,s](t)),"")`

**E594. `trfem2`: Fuel economy, passenger and light blended (light scaled by the fuel / gasoline ratio)** (km/l)

- Description: Calculation
- Legacy: legacy rows 2045, 2047
- Rows: lpg,pas, nga,pas
  - 2022-2041: `trfem2(t) = IF(tr.dk[all,all](t)=1,trfe[f,s](t)*trsps[all,s](t)+(trfe[ice,lgt](t)*trfe[f,s](t)/trfe[gso,s](t))*(1-trsps[all,s](t)),"")`

**E595. `trphs`: PHEV: gasoline share of distance (fuel economy gasoline / PHEV)** (share)

- Description: Calculation
- Legacy: legacy row 2049
- Rows: phv,pas
  - 2022-2041: `trphs(t) = IF(tr.dk[all,all](t)=1,trfe[gso,s](t)/trfe[f,s](t),"")`

**E596. `trfebm`: BEV fuel economy, passenger and light blended** (km/kWh)

- Description: Calculation
- Legacy: legacy row 2052
- Rows: bev,pas
  - 2022-2041: `trfebm(t) = IF(tr.dk[all,all](t)=1,trfe[f,s](t)*trsps[all,s](t)+trfeb[f,lgt](t)*(1-trsps[all,s](t)),"")`

**E597. `trpkg`: Gasoline cost per km before new policies (data years)** (USD/km)

- Description: Calculation
- Legacy: legacy row 2054
- Rows: gso,pas
  - 2022-2041: `trpkg(t) = IF(tr.dk[all,all](t)=1,pbc[<price position (gso.all)>](t)*<GJ per liter>/trfem[f,s](t),"")`
  - Parameters: `<price position (gso.all)>` = `INDEX(Inputs!E158:E169,MATCH("gso.all",Inputs!A158:A169,0))`; `<GJ per liter>` = `<Gasoline of trp.gj[all,all]>`

**E598. `trpke`: Electricity cost per km of BEVs, previous year's residential price before new policies (data years)** (USD/km)

- Description: Calculation
- Legacy: legacy row 2055
- Rows: bev,pas
  - 2022: `trpke(t) = IF(tr.dk[all,all](t)=1,<residential price 2021 (real $/kWh)>/trfebm[f,s](t),"")`
  - 2023-2041: `trpke(t) = IF(tr.dk[all,all](t)=1,rppre[ecy,res](t-1)/trfebm[f,s](t),"")`
  - Parameters: `<residential price 2021 (real $/kWh)>` = `Inputs!J221`

**E599. `trbvu`: BEV distance relative to ICEV (cost per km ratio ^ usage elasticity, capped; data years)** (factor)

- Description: Calculation
- Legacy: legacy rows 2056, 2114, 2136
- Rows: bev,pas
  - 2022-2041: `trbvu(t) = IF(tr.dk[all,all](t)=1,IF(trpke[f,s](t)=0,1,MIN(<passenger of trp.cap[all,all]>,(trpke[f,s](t)/trpkg[gso,s](t))^<usage, gasoline of trp.ela[all,all]>)),"")`
- Rows: bev,fre
  - 2022-2041: `trbvu(t) = IF(tr.dk[all,all](t)=1,IF(trpkef[f,s](t)=0,1,MIN(<freight of trp.cap[all,all]>,(trpkef[f,s](t)/trpkd[die,s](t))^<usage, diesel of trp.ela[all,all]>)),"")`
- Rows: bev,cyc
  - 2022-2041: `trbvu(t) = IF(tr.dk[all,all](t)=1,IF(trpkec[f,s](t)=0,1,MIN(<2-3 wheeler of trp.cap[all,all]>,(trpkec[f,s](t)/trpkc[gso,s](t))^<usage, gasoline of trp.ela[all,all]>)),"")`

**E600. `trvkm`: Distance per vehicle, passenger and light blended (data years)** (km)

- Description: Calculation
- Legacy: legacy row 2060
- Rows: all,pas
  - 2022-2041: `trvkm(t) = IF(tr.dk[f,all](t)=1,trvkd[f,s](t)*trsps[f,s](t)+trvkd[f,lgt](t)*(1-trsps[f,s](t)),"")`

**E601. `trvkb`: Distance per BEV (data years)** (km)

- Description: Calculation
- Legacy: legacy row 2061
- Rows: bev,pas
  - 2022-2041: `trvkb(t) = IF(tr.dk[all,all](t)=1,trvkm[all,s](t)*trbvu[f,s](t),"")`

**E602. `trevom`: EV share of the stock, passenger and light blended** (share)

- Description: Calculation
- Legacy: legacy row 2069
- Rows: ev,pas
  - 2022-2041: `trevom(t) = IF(tr.dk[all,all](t)=1,trevo[f,s](t)*trsps[all,s](t)+trevo[bev,lgt](t)*(1-trsps[all,s](t)),"")`

**E603. `trphv`: PHEV share of distance (EV less BEV stock share x gasoline share)** (share)

- Description: Calculation
- Legacy: legacy row 2070
- Rows: phv,pas
  - 2022-2041: `trphv(t) = IF(tr.dk[all,all](t)=1,(trevo[ev,s](t)-trevo[bev,s](t))*trphs[f,s](t)*trsps[all,s](t),"")`

**E604. `trvkg`: Distance of gasoline vehicles, passenger and light (fuel economy x fuel, data years)** (bln km)

- Description: Calculation
- Legacy: legacy row 2072
- Rows: gso,pas
  - 2022-2041: `trvkg(t) = IF(tr.dk[all,all](t)=1,trfem[f,s](t)*<bln liters, passenger and light>*(1-trphv[phv,s](t)),"")`
  - Parameters: `<bln liters, passenger and light>` = `<bln liters of trp.bsh[f,s]>+<bln liters of trp.bsh[f,lgt]>`

**E605. `trvkf`: Distance by fuel, passenger and light (fuel economy x fuel, data years)** (bln km)

- Description: Calculation
- Legacy: legacy rows 2073-2075
- Rows: die,pas
  - 2022-2041: `trvkf(t) = IF(tr.dk[all,all](t)=1,trfem[f,s](t)*<bln liters, passenger and light>,"")`
  - Parameters: `<bln liters, passenger and light>` = `<bln liters of trp.bsh[f,s]>+<bln liters of trp.bsh[f,lgt]>`
- Rows: lpg,pas, nga,pas
  - 2022-2041: `trvkf(t) = IF(tr.dk[all,all](t)=1,trfem2[f,s](t)*<bln liters, passenger and light>,"")`
  - Parameters: `<bln liters, passenger and light>` = `<bln liters of trp.bsh[f,s]>+<bln liters of trp.bsh[f,lgt]>`

**E606. `trvkp`: Distance of PHEVs (data years)** (bln km)

- Description: Calculation
- Legacy: legacy row 2076
- Rows: phv,pas
  - 2022-2041: `trvkp(t) = IF(tr.dk[all,all](t)=1,trfe[f,s](t)*<bln liters, passenger and light>*trphv[f,s](t),"")`
  - Parameters: `<bln liters, passenger and light>` = `<bln liters of trp.bsh[gso,s]>+<bln liters of trp.bsh[gso,lgt]>`

**E607. `trvk0`: Distance by fuel in the base year (held)** (bln km)

- Description: Calculation
- Legacy: legacy $L2072:$L2075
- Rows: gso,pas
  - 2022: `trvk0(t) = trvkg[f,s](t)`
  - 2023-2041: `trvk0(t) = trvk0[f,s](t-1)`
- Rows: die,pas, lpg,pas, nga,pas
  - 2022: `trvk0(t) = trvkf[f,s](t)`
  - 2023-2041: `trvk0(t) = trvk0[f,s](t-1)`

**E608. `trvsh`: Vehicle share by fuel, passenger and light (base-year distance split, data years)** (share)

- Description: Calculation
- Legacy: legacy rows 2078-2081
- Rows: gso,pas, die,pas, lpg,pas, nga,pas
  - 2022-2041: `trvsh(t) = IF(tr.dk[all,all](t)=1,trvk0[f,s](t)/SUM(trvk0[4 rows](t))*(1-trevom[ev,s](t)),"")`

**E609. `trphvs`: PHEV share of the stock (EV less BEV, data years)** (share)

- Description: Calculation
- Legacy: legacy row 2082
- Rows: phv,pas
  - 2022-2041: `trphvs(t) = IF(tr.dk[all,all](t)=1,trevom[ev,s](t)-trevbm[bev,s](t),"")`

**E610. `trevbm`: BEV share of the stock, passenger and light blended** (share)

- Description: Calculation
- Legacy: legacy row 2083
- Rows: bev,pas
  - 2022-2041: `trevbm(t) = IF(tr.dk[all,all](t)=1,trevo[f,s](t)*trsps[all,s](t)+trevo[f,lgt](t)*(1-trsps[all,s](t)),"")`

**E611. `trownb`: Ownership of ICEVs, passenger and light (data years)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 2086
- Rows: ice,pas
  - 2022-2041: `trownb(t) = IF(tr.dk[all,all](t)=1,(trown[all,s](t)+trown[all,lgt](t))*(1-trevbm[bev,s](t)),"")`

**E612. `trowne`: Ownership of BEVs, passenger and light (data years)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 2087
- Rows: bev,pas
  - 2022-2041: `trowne(t) = IF(tr.dk[all,all](t)=1,trown[all,s](t)+trown[all,lgt](t)-trownb[ice,s](t),"")`

**E613. `trevpm`: BEV share of purchases, passenger and light blended** (share)

- Description: Calculation
- Legacy: legacy row 2088
- Rows: bev,pas
  - 2022-2041: `trevpm(t) = IF(tr.dk[all,all](t)=1,trevp[f,s](t)*trsps[all,s](t)+trevp[f,lgt](t)*(1-trsps[all,s](t)),"")`

**E614. `trvkfr`: Distance by fuel, freight (fuel economy x fuel, data years)** (bln km)

- Description: Calculation
- Legacy: legacy rows 2097-2099
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trvkfr(t) = IF(tr.dk[all,all](t)=1,trfe[f,s](t)*<bln liters, freight>,"")`
  - Parameters: `<bln liters, freight>` = `<bln liters of trp.bsh[f,s]>`

**E615. `trvkr0`: Freight distance by fuel in the base year (held)** (bln km)

- Description: Calculation
- Legacy: legacy $L2097:$L2099
- Rows: die,fre, lpg,fre, nga,fre
  - 2022: `trvkr0(t) = trvkfr[f,s](t)`
  - 2023-2041: `trvkr0(t) = trvkr0[f,s](t-1)`

**E616. `trvsf1`: Vehicle share, freight diesel (base-year distance split; 1 without freight fuel, data years)** (share)

- Description: Calculation
- Legacy: legacy row 2104
- Rows: die,fre
  - 2022-2041: `trvsf1(t) = IF(tr.dk[all,all](t)=1,IF(SUM(trvkr0[3 rows](t))=0,1,trvkr0[f,s](t)/SUM(trvkr0[3 rows](t))*(1-trevo[bev,s](t))),"")`

**E617. `trvsf`: Vehicle share, freight LPG and LNG (base-year distance split; data years)** (share)

- Description: Calculation
- Legacy: legacy rows 2105-2106
- Rows: lpg,fre, nga,fre
  - 2022-2041: `trvsf(t) = IF(tr.dk[all,all](t)=1,IF(SUM(trvkr0[3 rows](t))=0,0,trvkr0[f,s](t)/SUM(trvkr0[3 rows](t))*(1-trevo[bev,s](t))),"")`

**E618. `trownf`: Ownership of ICE freight vehicles (data years)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 2109
- Rows: ice,fre
  - 2022-2041: `trownf(t) = IF(tr.dk[all,all](t)=1,trown[all,s](t)*(1-trevo[bev,s](t)),"")`

**E619. `trownfe`: Ownership of BEV freight vehicles (data years)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 2110
- Rows: bev,fre
  - 2022-2041: `trownfe(t) = IF(tr.dk[all,all](t)=1,trown[all,s](t)-trownf[ice,s](t),"")`

**E620. `trpkd`: Diesel cost per km of freight before new policies, net of VAT (data years)** (USD/km)

- Description: Calculation
- Legacy: legacy row 2112
- Rows: die,fre
  - 2022-2041: `trpkd(t) = IF(tr.dk[all,all](t)=1,pbc[<price position (die.all)>](t)*<GJ per liter>/(1+<VAT rate (die.all)>)/trfe[f,s](t),"")`
  - Parameters: `<price position (die.all)>` = `INDEX(Inputs!E158:E169,MATCH("die.all",Inputs!A158:A169,0))`; `<GJ per liter>` = `<Diesel of trp.gj[all,all]>`; `<VAT rate (die.all)>` = `INDEX(Inputs!V158:V169,MATCH("die.all",Inputs!A158:A169,0))`

**E621. `trpkef`: Electricity cost per km of BEV freight, industrial price before new policies (data years)** (USD/km)

- Description: Calculation
- Legacy: legacy row 2113
- Rows: bev,fre
  - 2022-2041: `trpkef(t) = IF(tr.dk[all,all](t)=1,rppre[ecy,ind](t)/trfeb[f,s](t),"")`

**E622. `trvkbf`: Distance per BEV freight vehicle for the purchase decision (data years)** (km)

- Description: Calculation
- Legacy: legacy row 2116
- Rows: bev,fre
  - 2022-2041: `trvkbf(t) = IF(tr.dk[all,all](t)=1,trbvu[f,s](t)*trvkd[all,s](t),"")`

**E623. `trvkfd`: Distance per freight vehicle from the fuel shares (base year; then x passenger distance ratio, data years)** (km)

- Description: Calculation
- Legacy: legacy row 2117 (survey B14: kept as legacy)
- Rows: all,fre
  - 2022: `trvkfd(t) = IF(trvsf1[die,s](t)=0,trvkd[f,s](t),trvkfr[die,s](t)/(trvsf1[die,s](t)*trown[f,s](t)*trpop[f,all](t))*Million)`
  - 2023-2041: `trvkfd(t) = IF(tr.dk[f,all](t)=1,trvkfd[f,s](t-1)*trvkm[f,pas](t)/trvkm[f,pas](t-1),"")`

**E624. `trvkfb`: Distance per BEV freight vehicle (data years)** (km)

- Description: Calculation
- Legacy: legacy row 2118
- Rows: bev,fre
  - 2022: `trvkfb(t) = trbvu[f,s](t)*trvkfd[all,s](t)`
  - 2023-2041: `trvkfb(t) = IF(tr.dk[all,all](t)=1,trvkfb[f,s](t-1)*trvkb[f,pas](t)/trvkb[f,pas](t-1),"")`

**E625. `trownc`: Ownership of ICE 2-3 wheelers (data years)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 2130
- Rows: ice,cyc
  - 2022-2041: `trownc(t) = IF(tr.dk[all,all](t)=1,trown[all,s](t)*(1-trevo[bev,s](t)),"")`

**E626. `trownce`: Ownership of BEV 2-3 wheelers (data years)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 2131
- Rows: bev,cyc
  - 2022-2041: `trownce(t) = IF(tr.dk[all,all](t)=1,trown[all,s](t)-trownc[ice,s](t),"")`

**E627. `trpkc`: Gasoline cost per km of 2-3 wheelers before new policies (data years)** (USD/km)

- Description: Calculation
- Legacy: legacy row 2134
- Rows: gso,cyc
  - 2022-2041: `trpkc(t) = IF(tr.dk[all,all](t)=1,pbc[<price position (gso.all)>](t)*<GJ per liter>/trfe[f,s](t),"")`
  - Parameters: `<price position (gso.all)>` = `INDEX(Inputs!E158:E169,MATCH("gso.all",Inputs!A158:A169,0))`; `<GJ per liter>` = `<Gasoline of trp.gj[all,all]>`

**E628. `trpkec`: Electricity cost per km of BEV 2-3 wheelers, industrial price before new policies (data years)** (USD/km)

- Description: Calculation
- Legacy: legacy row 2135
- Rows: bev,cyc
  - 2022-2041: `trpkec(t) = IF(tr.dk[all,all](t)=1,rppre[ecy,ind](t)/trfeb[f,s](t),"")`

**E629. `trvkbc`: Distance per BEV 2-3 wheeler (data years)** (km)

- Description: Calculation
- Legacy: legacy row 2137
- Rows: bev,cyc
  - 2022-2041: `trvkbc(t) = IF(tr.dk[all,all](t)=1,trvkd[all,s](t)*trbvu[f,s](t),"")`

**E630. `trnc`: Freight share of ownership in the last data year (held)** (share)

- Description: Calculation
- Legacy: legacy $N2168 (B3b fixed: last data year)
- Rows: all,fre
  - 2022-2041: `trnc(t) = IF(tr.dk[f,all](t)=1,trown[f,s](t)/(trown[f,pas](t)+trown[f,lgt](t)),trnc[f,s](t-1))`

**E631. `trfsh`: Freight share of ownership (data years; then falling with income to the target, capped at the last data year)** (share)

- Description: Calculation
- Legacy: legacy row 2168
- Rows: all,fre
  - 2022-2041: `trfsh(t) = IF(tr.dk[f,all](t)=1,trown[f,s](t)/(trown[f,pas](t)+trown[f,lgt](t)),MIN(trnc[f,s](t-1),MAX(<freight: target share of trp.frs[f,all]>,trnc[f,s](t-1)-(trnc[f,s](t-1)-<freight: target share of trp.frs[f,all]>)*trgpc[f,all](t)/<freight: income at the target of trp.frs[f,all]>)))`

**E632. `trjc`: 2-3 wheeler ownership hump: peak level from the last data year (held)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy J2169 (B3b fixed)
- Rows: all,cyc
  - 2022-2041: `trjc(t) = IF(tr.dk[f,all](t)=1,(1+(1-trgpc[f,all](t)/<2-3 wheeler: peak income of trp.frs[f,all]>)*<2-3 wheeler: scale of trp.frs[f,all]>)*trown[f,s](t),trjc[f,s](t-1))`

**E633. `trcyh`: 2-3 wheeler ownership demand (data; then the income hump)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 2169
- Rows: all,cyc
  - 2022-2041: `trcyh(t) = IF(tr.dk[f,all](t)=1,trown[f,s](t),(trjc[f,s](t-1)+trjc[f,s](t-1))/(trgpc[f,all](t)/<2-3 wheeler: peak income of trp.frs[f,all]>+<2-3 wheeler: peak income of trp.frs[f,all]>/trgpc[f,all](t)))`

**E634. `trush`: Share of used vehicles in passenger purchases (data; held after)** (share)

- Description: Calculation
- Legacy: legacy rows 4740, 4406
- Rows: all,pas
  - 2022-2041: `trush(t) = IF(tr.dk[f,all](t)=1,trusd[f,s](t),trush[f,s](t-1))`

**E635. `trowny`: Ownership years, passenger and light (weighted new and used)** (years)

- Description: Calculation
- Legacy: legacy row 4741
- Rows: all,pas
  - 2022-2041: `trowny(t) = trush[f,s](t)*<useful life, passenger of trp.life[f,all]>+(1-trush[f,s](t))*<ownership years, new passenger of trp.life[f,all]>`

**E636. `trstd`: Vehicle stock, data years (passenger)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4742, 4761
- Rows: ice,pas
  - 2022-2041: `trstd(t) = IF(tr.dk[all,all](t)=1,trownb[f,s](t),"")`
- Rows: bev,pas
  - 2022-2041: `trstd(t) = IF(tr.dk[all,all](t)=1,trowne[f,s](t),"")`

**E637. `trstdf`: Vehicle stock, data years (freight)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4876, 4886
- Rows: ice,fre
  - 2022-2041: `trstdf(t) = IF(tr.dk[all,all](t)=1,trownf[f,s](t),"")`
- Rows: bev,fre
  - 2022-2041: `trstdf(t) = IF(tr.dk[all,all](t)=1,trownfe[f,s](t),"")`

**E638. `trstdc`: Vehicle stock, data years (2-3 wheeler)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4956, 4966
- Rows: ice,cyc
  - 2022-2041: `trstdc(t) = IF(tr.dk[all,all](t)=1,trownc[f,s](t),"")`
- Rows: bev,cyc
  - 2022-2041: `trstdc(t) = IF(tr.dk[all,all](t)=1,trownce[f,s](t),"")`

**E639. `tropn`: Opening stock, passenger and light bought new** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4744, 4763
- Rows: ice,pas, bev,pas
  - 2022-2041: `tropn(t) = IF(N(trstd[f,s](t))>0,N(trstd[f,s](t))*(1-trush[all,s](t)),N(trclon[f,s](t-1)))`

**E640. `tropu`: Opening stock, passenger and light bought used** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4752, 4771
- Rows: ice,pau, bev,pau
  - 2022-2041: `tropu(t) = IF(N(trstd[f,pas](t))>0,N(trstd[f,pas](t))*trush[all,pas](t),N(trclou[f,s](t-1)))`

**E641. `tropf`: Opening stock, freight** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4878, 4888
- Rows: ice,fre, bev,fre
  - 2022-2041: `tropf(t) = IF(N(trstdf[f,s](t))>0,N(trstdf[f,s](t))*1,N(trclof[f,s](t-1)))`

**E642. `tropc`: Opening stock, 2-3 wheelers** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4958, 4968
- Rows: ice,cyc, bev,cyc
  - 2022-2041: `tropc(t) = IF(N(trstdc[f,s](t))>0,N(trstdc[f,s](t))*1,N(trcloc[f,s](t-1)))`

**E643. `travn`: Trailing-average stock (last min(life, years) years), passenger and light bought new** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4745, 4764
- Rows: ice,pas, bev,pas
  - 2022-2041: `travn(t) = AVERAGE(INDEX(tropn[f,s](..t),1,COLUMNS(tropn[f,s](..t))+1-MIN(<ownership years, new passenger of trp.life[all,all]>,tr.col[all,all](t))):tropn[f,s](t))`

**E644. `travu`: Trailing-average stock (last min(life, years) years), passenger and light bought used** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4753, 4772
- Rows: ice,pau, bev,pau
  - 2022-2041: `travu(t) = AVERAGE(INDEX(tropu[f,s](..t),1,COLUMNS(tropu[f,s](..t))+1-MIN(<useful life, passenger of trp.life[all,all]>-<ownership years, new passenger of trp.life[all,all]>,tr.col[all,all](t))):tropu[f,s](t))`

**E645. `travf`: Trailing-average stock (last min(life, years) years), freight** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4879, 4889
- Rows: ice,fre, bev,fre
  - 2022-2041: `travf(t) = AVERAGE(INDEX(tropf[f,s](..t),1,COLUMNS(tropf[f,s](..t))+1-MIN(<useful life, freight of trp.life[all,all]>,tr.col[all,all](t))):tropf[f,s](t))`

**E646. `travc`: Trailing-average stock (last min(life, years) years), 2-3 wheelers** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4959, 4969
- Rows: ice,cyc, bev,cyc
  - 2022-2041: `travc(t) = AVERAGE(INDEX(tropc[f,s](..t),1,COLUMNS(tropc[f,s](..t))+1-MIN(<useful life, 2-3 wheeler of trp.life[all,all]>,tr.col[all,all](t))):tropc[f,s](t))`

**E647. `trretn`: Retirement, passenger and light bought new** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4746, 4765
- Rows: ice,pas, bev,pas
  - 2022-2041: `trretn(t) = MIN(travn[f,s](t)/<ownership years, new passenger of trp.life[all,all]>,tropn[f,s](t))`

**E648. `trretu`: Retirement, passenger and light bought used** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4754, 4773
- Rows: ice,pau, bev,pau
  - 2022-2041: `trretu(t) = MIN(travu[f,s](t)/(<useful life, passenger of trp.life[all,all]>-<ownership years, new passenger of trp.life[all,all]>),tropu[f,s](t))`

**E649. `trretf`: Retirement, freight** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4880, 4890
- Rows: ice,fre, bev,fre
  - 2022-2041: `trretf(t) = MIN(travf[f,s](t)/<useful life, freight of trp.life[all,all]>,tropf[f,s](t))`

**E650. `trretc`: Retirement, 2-3 wheelers** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4960, 4970
- Rows: ice,cyc, bev,cyc
  - 2022-2041: `trretc(t) = MIN(travc[f,s](t)/<useful life, 2-3 wheeler of trp.life[all,all]>,tropc[f,s](t))`

**E651. `traftn`: Stock after retirement, passenger and light bought new** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4747, 4766
- Rows: ice,pas, bev,pas
  - 2022-2041: `traftn(t) = tropn[f,s](t)-trretn[f,s](t)`

**E652. `traftu`: Stock after retirement, passenger and light bought used** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4755, 4774
- Rows: ice,pau, bev,pau
  - 2022-2041: `traftu(t) = tropu[f,s](t)-trretu[f,s](t)`

**E653. `traftf`: Stock after retirement, freight** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4881, 4891
- Rows: ice,fre, bev,fre
  - 2022-2041: `traftf(t) = tropf[f,s](t)-trretf[f,s](t)`

**E654. `traftc`: Stock after retirement, 2-3 wheelers** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4961, 4971
- Rows: ice,cyc, bev,cyc
  - 2022-2041: `traftc(t) = tropc[f,s](t)-trretc[f,s](t)`

**E655. `trbuyn`: Purchases, passenger and light bought new** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4823, 4824
- Rows: ice,pas
  - 2022-2041: `trbuyn(t) = trshn[f,s](t)*trbytn[all,s](t)`
- Rows: bev,pas
  - 2022-2041: `trbuyn(t) = trshnb[f,s](t)*trbytn[all,s](t)`

**E656. `trbuyu`: Purchases, passenger and light bought used** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4825, 4826
- Rows: ice,pau
  - 2022-2041: `trbuyu(t) = trshu[f,s](t)*trbytu[all,s](t)`
- Rows: bev,pau
  - 2022-2041: `trbuyu(t) = trshub[f,s](t)*trbytu[all,s](t)`

**E657. `trbuyf`: Purchases, freight** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4921, 4922
- Rows: ice,fre
  - 2022-2041: `trbuyf(t) = trshfi[f,s](t)*trbytf[all,s](t)`
- Rows: bev,fre
  - 2022-2041: `trbuyf(t) = trshfb[f,s](t)*trbytf[all,s](t)`

**E658. `trbuyc`: Purchases, 2-3 wheelers** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4997, 4998
- Rows: ice,cyc
  - 2022-2041: `trbuyc(t) = trshc[f,s](t)*trbytc[all,s](t)`
- Rows: bev,cyc
  - 2022-2041: `trbuyc(t) = trshcb[f,s](t)*trbytc[all,s](t)`

**E659. `trplgn`: Data-year adjustment, passenger and light bought new** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4749, 4768
- Rows: ice,pas, bev,pas
  - 2022-2041: `trplgn(t) = IF(N(trstd[f,s](t))>0,N(trstd[f,s](t))*(1-trush[all,s](t))-traftn[f,s](t)-trbuyn[f,s](t),0)`

**E660. `trplgu`: Data-year adjustment, passenger and light bought used** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4757, 4776
- Rows: ice,pau, bev,pau
  - 2022-2041: `trplgu(t) = IF(N(trstd[f,pas](t))>0,N(trstd[f,pas](t))*trush[all,pas](t)-traftu[f,s](t)-trbuyu[f,s](t),0)`

**E661. `trplgf`: Data-year adjustment, freight** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4883, 4893
- Rows: ice,fre, bev,fre
  - 2022-2041: `trplgf(t) = IF(N(trstdf[f,s](t))>0,N(trstdf[f,s](t))*1-traftf[f,s](t)-trbuyf[f,s](t),0)`

**E662. `trplgc`: Data-year adjustment, 2-3 wheelers** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4963, 4973
- Rows: ice,cyc, bev,cyc
  - 2022-2041: `trplgc(t) = IF(N(trstdc[f,s](t))>0,N(trstdc[f,s](t))*1-traftc[f,s](t)-trbuyc[f,s](t),0)`

**E663. `trclon`: Closing stock, passenger and light bought new** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4750, 4769
- Rows: ice,pas, bev,pas
  - 2022-2041: `trclon(t) = traftn[f,s](t)+trbuyn[f,s](t)+trplgn[f,s](t)`

**E664. `trclou`: Closing stock, passenger and light bought used** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4758, 4777
- Rows: ice,pau, bev,pau
  - 2022-2041: `trclou(t) = traftu[f,s](t)+trbuyu[f,s](t)+trplgu[f,s](t)`

**E665. `trclof`: Closing stock, freight** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4884, 4894
- Rows: ice,fre, bev,fre
  - 2022-2041: `trclof(t) = traftf[f,s](t)+trbuyf[f,s](t)+trplgf[f,s](t)`

**E666. `trcloc`: Closing stock, 2-3 wheelers** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4964, 4974
- Rows: ice,cyc, bev,cyc
  - 2022-2041: `trcloc(t) = traftc[f,s](t)+trbuyc[f,s](t)+trplgc[f,s](t)`

**E667. `trstt`: Stock of passenger and light vehicles (opening, all types)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4779
- Rows: all,pas
  - 2022-2041: `trstt(t) = SUM(block@tropn{tropn, tropu}(t))`

**E668. `trevst`: EV share of the passenger and light stock (opening)** (share)

- Description: Calculation
- Legacy: legacy row 4778
- Rows: ev,pas
  - 2022-2041: `trevst(t) = IF(trstt[all,s](t)=0,0,(tropn[bev,s](t)+tropu[bev,pau](t))/trstt[all,s](t))`

**E669. `trevsf`: BEV share of the freight stock (opening)** (share)

- Description: Calculation
- Legacy: legacy row 4895
- Rows: bev,fre
  - 2022-2041: `trevsf(t) = IF((tropf[f,s](t)+tropf[ice,s](t))=0,0,tropf[f,s](t)/(tropf[f,s](t)+tropf[ice,s](t)))`

**E670. `trevsc`: BEV share of the 2-3 wheeler stock (opening)** (share)

- Description: Calculation
- Legacy: legacy row 4975
- Rows: bev,cyc
  - 2022-2041: `trevsc(t) = IF((tropc[f,s](t)+tropc[ice,s](t))=0,0,tropc[f,s](t)/(tropc[f,s](t)+tropc[ice,s](t)))`

**E671. `trafts`: Stock after retirement, passenger and light** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4788
- Rows: all,pas
  - 2022-2041: `trafts(t) = SUM(block@traftn{traftn, traftu}(t))`

**E672. `traftsf`: Stock after retirement, freight** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4904
- Rows: all,fre
  - 2022-2041: `traftsf(t) = SUM(traftf[2 rows](t))`

**E673. `traftsc`: Stock after retirement, 2-3 wheelers** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4980
- Rows: all,cyc
  - 2022-2041: `traftsc(t) = SUM(traftc[2 rows](t))`

**E674. `trbevm`: BEV stock (passenger, light, freight, 2-3 wheelers)** (million)

- Description: Calculation
- Legacy: legacy row 4340
- Rows: bev,all
  - 2022-2041: `trbevm(t) = (tropn[f,pas](t)+tropu[f,pau](t)+tropf[f,fre](t)+tropc[f,cyc](t))*trpop[all,s](t)/Thousand`

**E675. `trcss`: Charging-station subsidy (share of the cost; policy scenarios; fix B10)** (share)

- Description: Calculation
- Legacy: legacy row 4343
- Rows: all,all
  - 2022-2041: `trcss(t) = IF(year<TrCsStartYear[f,s](t),0,TrCsStartLevel[f,s](t)+(TrCsTargetLevel[f,s](t)-TrCsStartLevel[f,s](t))*MIN(1,(year-TrCsStartYear[f,s](t))/MAX(1,TrCsTargetYear[f,s](t)-TrCsStartYear[f,s](t))))*tr.pol[f,s](t)`

**E676. `trcsc`: Charging-station cost after the subsidy** (USD/port)

- Description: Calculation
- Legacy: legacy row 4344
- Rows: all,all
  - 2022-2041: `trcsc(t) = trcpp[f,s](t)*(1-trcss[f,s](t))`

**E677. `trsta`: Charging stations (data; then with the BEV stock and the cost per port)** (stations)

- Description: Calculation
- Legacy: legacy row 4347
- Rows: all,all
  - 2022-2041: `trsta(t) = IF(tr.dk[f,s](t)=1,trchs[f,s](t),trsta[f,s](t-1)*(trbevm[bev,s](t)/trbevm[bev,s](t-1))^<stations to the BEV stock of trp.chs[f,s]>*(trcsc[f,s](t)/trcsc[f,s](t-1))^<stations to their cost of trp.chs[f,s]>)`

**E678. `trmku`: Charging mark-up on the electricity price** (USD/kWh)

- Description: Calculation
- Legacy: legacy row 4350
- Rows: all,all
  - 2022-2041: `trmku(t) = MAX(<minimum USD/kWh of trp.mku[f,s]>,<maximum USD/kWh of trp.mku[f,s]>*(<EV share of the minimum of trp.mku[f,s]>-trevst[ev,pas](t))/(1-<EV share of the minimum of trp.mku[f,s]>))*<share of public charging of trp.mku[f,s]>`

**E679. `trpev`: EV electricity price: end-user price of the previous year (section 3) + charging mark-up** (USD/kWh)

- Description: Calculation
- Legacy: legacy rows 4351, 4352
- Rows: ecy,res, ecy,ind
  - 2022: `trpev(t) = rp[f,s](t)+trmku[all,all](t)`
  - 2023-2041: `trpev(t) = rp[f,s](t-1)+trmku[all,all](t)`

**E680. `trra`: Range anxiety (Transport3 value of the country, then falling with charging stations)** (USD/vehicle)

- Description: Calculation
- Legacy: legacy rows 4354-4356 (Transport3 H, N, T)
- Rows: bev,pas, bev,fre, bev,cyc
  - 2022-2041: `trra(t) = IF(tr.col[all,all](t)<=TrRALag,<Transport3 value (average if none)>,IF(trra[f,s](t-1)<0,trra[f,s](t-1),MAX(trra[f,s](t-1)*(1-<annual decline>)*(trsta[all,all](t)/trsta[all,all](t-1))^<range anxiety to stations of trp.chs[all,all]>,0)))`
  - Parameters: `<Transport3 value (average if none)>` = `IFERROR(INDEX(RAPas,MATCH(CtryName,RAKey,0)),AVERAGE(RAPas))`; `<annual decline>` = `INDEX(TrParVal,MATCH("ra_decline|pass",TrParKey,0))`; `<Transport3 actual EV sales share (fit year)>` = `IFERROR(INDEX(RAPasA,MATCH(CtryName,RAKey,0)),"")`; `<Transport3 calculated EV sales share (fit year)>` = `IFERROR(INDEX(RAPasC,MATCH(CtryName,RAKey,0)),"")`

**E681. `trfew`: Fuel mix of passenger and light ICEVs (data; then last year's ownership shares)** (share)

- Description: Calculation
- Legacy: legacy rows 4360-4364
- Rows: gso,pas, die,pas, lpg,pas, nga,pas
  - 2022-2041: `trfew(t) = IF(tr.dk[all,all](t)=1,trvsh[f,s](t),tricw[f,s](t-1))`
- Rows: phv,pas
  - 2022-2041: `trfew(t) = IF(tr.dk[all,all](t)=1,trphvs[f,s](t),tricw[f,s](t-1))`

**E682. `trphg`: PHEV gasoline share of distance (data; held after)** (share)

- Description: Calculation
- Legacy: legacy rows 4366, 5221
- Rows: phv,pas
  - 2022-2041: `trphg(t) = IF(tr.dk[all,all](t)=1,trphs[f,s](t),trphg[f,s](t-1))`

**E683. `trpav`: Average fuel price of passenger and light ICEVs** (USD/liter)

- Description: Calculation
- Legacy: legacy row 4372
- Rows: all,pas
  - 2022-2041: `trpav(t) = SUMPRODUCT(block@trprl{trprl, trprg, trpphv}(t),trfew[5 rows](t))/SUM(trfew[5 rows](t))`

**E684. `trfbtp`: Vehicle feebate rate incl. the road regulation shadow price, pas** (USD/tCO2)

- Description: Calculation
- Legacy: legacy row 4374
- Rows: all,pas
  - 2022-2041: `trfbtp(t) = (IF(year>=TrFbYearPas[f,all](t),TrFbRatePas[f,all](t),0)+reg[f,rod](t)*1)*tr.pol[f,all](t)`

**E685. `trfbtf`: Vehicle feebate rate incl. the road regulation shadow price, fre** (USD/tCO2)

- Description: Calculation
- Legacy: legacy row 4418
- Rows: all,fre
  - 2022-2041: `trfbtf(t) = (IF(year>=TrFbYearFre[f,all](t),TrFbRateFre[f,all](t),0)+reg[f,rod](t)*1)*tr.pol[f,all](t)`

**E686. `trfbtc`: Vehicle feebate rate incl. the road regulation shadow price, cyc** (USD/tCO2)

- Description: Calculation
- Legacy: legacy row 4440
- Rows: all,cyc
  - 2022-2041: `trfbtc(t) = (IF(year>=TrFbYearCyc[f,all](t),TrFbRateCyc[f,all](t),0)+reg[f,rod](t)*1)*tr.pol[f,all](t)`

**E687. `trfbl`: Vehicle feebate per liter (rate x EF)** (USD/liter)

- Description: Calculation
- Legacy: legacy rows 4375-4379
- Rows: gso,pas, die,pas, lpg,pas, nga,pas, phv,pas
  - 2022-2041: `trfbl(t) = trfbtp[all,s](t)*<EF (tCO2 per liter)>`
  - Parameters: `<EF (tCO2 per liter)>` = `<Gasoline of trp.ef[all,all]>*<gasoline of trp.efa[all,all]>`

**E688. `trfbr`: Change in fuel price incl. feebate (ratio to last year)** (ratio)

- Description: Calculation
- Legacy: legacy rows 4380-4383
- Rows: gso,pas, die,pas, lpg,pas
  - 2022: `trfbr(t) = ""`
  - 2023-2041: `trfbr(t) = (trprl[f,rod](t)+trfbl[f,s](t))/(trprl[f,rod](t-1)+trfbl[f,s](t-1))`
- Rows: nga,pas
  - 2022: `trfbr(t) = ""`
  - 2023-2041: `trfbr(t) = (trprg[f,rod](t)+trfbl[f,s](t))/(trprg[f,rod](t-1)+trfbl[f,s](t-1))`

**E689. `trfbr5`: Change in the average fuel price incl. the gasoline feebate (PHEV fuel economy)** (ratio)

- Description: Calculation
- Legacy: legacy row 4384
- Rows: phv,pas
  - 2022: `trfbr5(t) = ""`
  - 2023-2041: `trfbr5(t) = (trpav[all,s](t)+trfbl[f,s](t))/(trpav[all,s](t-1)+trfbl[f,s](t-1))`

**E690. `trfn`: Fuel economy of new vehicles (data x (1 + gap); then price response and autonomous gain)** (km/l)

- Description: Calculation
- Legacy: legacy rows 4386-4389
- Rows: gso,pas, die,pas
  - 2022-2041: `trfn(t) = IF(tr.dk[all,all](t)=1,trfem[f,s](t)*(1+<passenger of trp.gap[all,all]>),trfn[f,s](t-1)*trfbr[f,s](t)^ABS(<efficiency, gasoline of trp.ela[all,all]>)*(1+<autonomous efficiency gain of trp.mod[all,all]>))`
- Rows: lpg,pas, nga,pas
  - 2022-2041: `trfn(t) = IF(tr.dk[all,all](t)=1,trfem2[f,s](t)*(1+<passenger of trp.gap[all,all]>),trfn[f,s](t-1)*trfbr[f,s](t)^ABS(<efficiency, gasoline of trp.ela[all,all]>)*(1+<autonomous efficiency gain of trp.mod[all,all]>))`

**E691. `trfnp`: Fuel economy of new PHEVs** (km/l)

- Description: Calculation
- Legacy: legacy row 4390
- Rows: phv,pas
  - 2022-2041: `trfnp(t) = IF(tr.dk[all,all](t)=1,trfe[f,s](t)*(1+<passenger of trp.gap[all,all]>),trfnp[f,s](t-1)*trfbr5[f,s](t)^ABS(<efficiency, gasoline of trp.ela[all,all]>)*(1+<autonomous efficiency gain of trp.mod[all,all]>))`

**E692. `trfna`: Average fuel economy of new ICEVs, passenger and light** (km/l)

- Description: Calculation
- Legacy: legacy row 4391
- Rows: all,pas
  - 2022-2041: `trfna(t) = SUMPRODUCT(block@trfn{trfn, trfnp}(t),trfew[5 rows](t))/SUM(trfew[5 rows](t))`

**E693. `trint`: CO2 intensity of new vehicles** (gCO2/km)

- Description: Calculation
- Legacy: legacy rows 4392-4396
- Rows: gso,pas, die,pas, lpg,pas, nga,pas
  - 2022-2041: `trint(t) = (<EF (tCO2 per liter)>*Million)/trfn[f,s](t)`
  - Parameters: `<EF (tCO2 per liter)>` = `<Gasoline of trp.ef[all,all]>`
- Rows: phv,pas
  - 2022-2041: `trint(t) = (<EF (tCO2 per liter)>*Million)/trfnp[f,s](t)`
  - Parameters: `<EF (tCO2 per liter)>` = `<Gasoline of trp.ef[all,all]>`

**E694. `trinta`: Average CO2 intensity of new ICEVs, passenger and light** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4397
- Rows: all,pas
  - 2022-2041: `trinta(t) = SUMPRODUCT(trfew[5 rows](t),trint[5 rows](D))/SUM(trfew[5 rows](t))/trfna[f,s](t)*Million`

**E695. `trfeu`: Fuel economy of used ICEVs (average of new over the last ownership years)** (km/l)

- Description: Calculation
- Legacy: legacy row 4401
- Rows: all,pau
  - 2022-2041: `trfeu(t) = AVERAGE(INDEX(trfna[f,pas](..t),1,COLUMNS(trfna[f,pas](..t))+1-MIN(tr.col[f,all](t),<ownership years, new passenger of trp.life[f,all]>)):trfna[f,pas](t))`

**E696. `trintu`: CO2 intensity of used ICEVs (new vehicles the ownership years earlier)** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4402
- Rows: all,pau
  - 2022-2041: `trintu(t) = INDEX(trinta[f,pas](..t),1,COLUMNS(trinta[f,pas](..t))+1-MIN(tr.col[f,all](t),<ownership years, new passenger of trp.life[f,all]>))`

**E697. `trfeub`: Fuel economy of used BEVs (new BEVs the ownership years earlier)** (km/kWh)

- Description: Calculation
- Legacy: legacy row 4403
- Rows: bev,pau
  - 2022-2041: `trfeub(t) = INDEX(trfen[f,pas](..t),1,COLUMNS(trfen[f,pas](..t))+1-MIN(tr.col[all,all](t),<ownership years, new passenger of trp.life[all,all]>))`

**E698. `tricl`: ICE share of new passenger purchases, last year (base year: data)** (share)

- Description: Calculation
- Legacy: legacy rows 4808, 4404
- Rows: ice,pas
  - 2022: `tricl(t) = 1-trevpm[bev,s](t)`
  - 2023-2041: `tricl(t) = trshn[f,s](t-1)`

**E699. `triclu`: ICE share of used passenger purchases, last year (base year: this year)** (share)

- Description: Calculation
- Legacy: legacy rows 4821, 4405
- Rows: ice,pau
  - 2022: `triclu(t) = trshu[f,s](t)`
  - 2023-2041: `triclu(t) = trshu[f,s](t-1)`

**E700. `trints`: CO2 intensity of last year's passenger sales (new and used)** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4407
- Rows: all,pas
  - 2022: `trints(t) = ""`
  - 2023-2041: `trints(t) = trush[f,s](t)*(trintu[f,pau](t-1)*triclu[ice,pau](t))+(1-trush[f,s](t))*(trinta[f,s](t-1)*tricl[ice,s](t))`

**E701. `trfewf`: Fuel mix of ICE freight vehicles (data; then last year's ownership shares)** (share)

- Description: Calculation
- Legacy: legacy rows 4413-4415
- Rows: die,fre
  - 2022-2041: `trfewf(t) = IF(tr.dk[all,all](t)=1,trvsf1[f,s](t),tricwf[f,s](t-1))`
- Rows: lpg,fre, nga,fre
  - 2022-2041: `trfewf(t) = IF(tr.dk[all,all](t)=1,trvsf[f,s](t),tricwf[f,s](t-1))`

**E702. `trpavf`: Average fuel price of ICE freight vehicles (net of VAT)** (USD/liter)

- Description: Calculation
- Legacy: legacy row 4416
- Rows: all,fre
  - 2022-2041: `trpavf(t) = SUMPRODUCT(block@trprn{trprn, trprm}(t),trfewf[3 rows](t))/SUM(trfewf[3 rows](t))`

**E703. `trfblf`: Vehicle feebate per liter, freight** (USD/liter)

- Description: Calculation
- Legacy: legacy rows 4419-4421
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trfblf(t) = trfbtf[all,s](t)*<EF (tCO2 per liter)>`
  - Parameters: `<EF (tCO2 per liter)>` = `<Diesel of trp.ef[all,all]>*<diesel of trp.efa[all,all]>`

**E704. `trfbrf`: Change in freight fuel price incl. feebate (ratio to last year)** (ratio)

- Description: Calculation
- Legacy: legacy rows 4422-4424
- Rows: die,fre, lpg,fre
  - 2022: `trfbrf(t) = ""`
  - 2023-2041: `trfbrf(t) = (trprn[f,rod](t)+trfblf[f,s](t))/(trprn[f,rod](t-1)+trfblf[f,s](t-1))`
- Rows: nga,fre
  - 2022: `trfbrf(t) = ""`
  - 2023-2041: `trfbrf(t) = (trprm[f,s](t)+trfblf[f,s](t))/(trprm[f,s](t-1)+trfblf[f,s](t-1))`

**E705. `trfnf`: Fuel economy of new freight vehicles** (km/l)

- Description: Calculation
- Legacy: legacy rows 4425-4427
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trfnf(t) = IF(tr.dk[all,all](t)=1,trfe[f,s](t)*(1+<freight of trp.gap[all,all]>),trfnf[f,s](t-1)*trfbrf[f,s](t)^ABS(<efficiency, diesel of trp.ela[all,all]>)*(1+<autonomous efficiency gain of trp.mod[all,all]>))`

**E706. `trfnaf`: Average fuel economy of new ICE freight vehicles** (km/l)

- Description: Calculation
- Legacy: legacy row 4428
- Rows: all,fre
  - 2022-2041: `trfnaf(t) = SUMPRODUCT(trfnf[3 rows](t),trfewf[3 rows](t))/SUM(trfewf[3 rows](t))`

**E707. `trintf`: CO2 intensity of new freight vehicles** (gCO2/km)

- Description: Calculation
- Legacy: legacy rows 4429-4431
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trintf(t) = (<EF (tCO2 per liter)>*Million)/trfnf[f,s](t)`
  - Parameters: `<EF (tCO2 per liter)>` = `<Diesel of trp.ef[all,all]>`

**E708. `trintaf`: Average CO2 intensity of new ICE freight vehicles** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4432
- Rows: all,fre
  - 2022-2041: `trintaf(t) = SUMPRODUCT(trfewf[3 rows](t),trintf[3 rows](D))/SUM(trfewf[3 rows](t))/trfnaf[f,s](t)*Million`

**E709. `triclf`: ICE share of freight purchases, last year (base year: data)** (share)

- Description: Calculation
- Legacy: legacy rows 4919, 4907, 4434
- Rows: ice,fre
  - 2022: `triclf(t) = 1-N(trevp[bev,s](t))`
  - 2023-2041: `triclf(t) = trshfi[f,s](t-1)`

**E710. `trintsf`: CO2 intensity of last year's freight sales** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4435
- Rows: all,fre
  - 2022: `trintsf(t) = ""`
  - 2023-2041: `trintsf(t) = triclf[ice,s](t)*trintaf[f,s](t-1)`

**E711. `trfblc`: Vehicle feebate per liter, 2-3 wheelers** (USD/liter)

- Description: Calculation
- Legacy: legacy row 4441
- Rows: gso,cyc
  - 2022-2041: `trfblc(t) = trfbtc[all,s](t)*<EF (tCO2 per liter)>`
  - Parameters: `<EF (tCO2 per liter)>` = `<Gasoline of trp.ef[all,all]>*<gasoline of trp.efa[all,all]>`

**E712. `trfbrc`: Change in 2-3 wheeler fuel price incl. feebate (ratio to last year)** (ratio)

- Description: Calculation
- Legacy: legacy row 4442
- Rows: gso,cyc
  - 2022: `trfbrc(t) = ""`
  - 2023-2041: `trfbrc(t) = (trprl[f,rod](t)+trfblc[f,s](t))/(trprl[f,rod](t-1)+trfblc[f,s](t-1))`

**E713. `trfnc`: Fuel economy of new 2-3 wheelers** (km/l)

- Description: Calculation
- Legacy: legacy row 4444
- Rows: gso,cyc
  - 2022-2041: `trfnc(t) = IF(tr.dk[all,all](t)=1,trfe[f,s](t)*(1+<2-3 wheeler of trp.gap[all,all]>),trfnc[f,s](t-1)*trfbrc[f,s](t)^ABS(<efficiency, gasoline of trp.ela[all,all]>)*(1+<autonomous efficiency gain of trp.mod[all,all]>))`

**E714. `trintc`: CO2 intensity of new 2-3 wheelers** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4445
- Rows: gso,cyc
  - 2022-2041: `trintc(t) = (<EF (tCO2 per liter)>*Million)/trfnc[f,s](t)`
  - Parameters: `<EF (tCO2 per liter)>` = `<Gasoline of trp.ef[all,all]>`

**E715. `triclc`: ICE share of 2-3 wheeler purchases, last year (base year: data)** (share)

- Description: Calculation
- Legacy: legacy rows 4995, 4447
- Rows: ice,cyc
  - 2022: `triclc(t) = 1-N(trevp[bev,s](t))`
  - 2023-2041: `triclc(t) = trshc[f,s](t-1)`

**E716. `trintsc`: CO2 intensity of last year's 2-3 wheeler sales** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4448
- Rows: gso,cyc
  - 2022: `trintsc(t) = ""`
  - 2023-2041: `trintsc(t) = triclc[ice,s](t)*trintc[f,s](t-1)`

**E717. `trdtxp`: Distance tax (pas; policy scenarios, fix B1)** (USD/km)

- Description: Calculation
- Legacy: legacy row 4451
- Rows: all,pas
  - 2022-2041: `trdtxp(t) = IF(year=TrDtYearPas[f,all](t),TrDtStartPas[f,all](t),MIN(TrDtTargetPas[f,all](t),N(trdtxp[f,s](t-1))+(TrDtTargetPas[f,all](t)-TrDtStartPas[f,all](t))/(TrDtTargetYearPas[f,all](t)-TrDtYearPas[f,all](t))))*(year>=TrDtYearPas[f,all](t))*tr.pol[f,all](t)`

**E718. `trdtxf`: Distance tax (fre; policy scenarios, fix B1)** (USD/km)

- Description: Calculation
- Legacy: legacy row 4479
- Rows: all,fre
  - 2022-2041: `trdtxf(t) = IF(year=TrDtYearFre[f,all](t),TrDtStartFre[f,all](t),MIN(TrDtTargetFre[f,all](t),N(trdtxf[f,s](t-1))+(TrDtTargetFre[f,all](t)-TrDtStartFre[f,all](t))/(TrDtTargetYearFre[f,all](t)-TrDtYearFre[f,all](t))))*(year>=TrDtYearFre[f,all](t))*tr.pol[f,all](t)`

**E719. `trdtxc`: Distance tax (cyc; policy scenarios, fix B1)** (USD/km)

- Description: Calculation
- Legacy: legacy row 4497
- Rows: all,cyc
  - 2022-2041: `trdtxc(t) = IF(year=TrDtYearCyc[f,all](t),TrDtStartCyc[f,all](t),MIN(TrDtTargetCyc[f,all](t),N(trdtxc[f,s](t-1))+(TrDtTargetCyc[f,all](t)-TrDtStartCyc[f,all](t))/(TrDtTargetYearCyc[f,all](t)-TrDtYearCyc[f,all](t))))*(year>=TrDtYearCyc[f,all](t))*tr.pol[f,all](t)`

**E720. `trckm`: Cost per km of new ICEVs (fuel price / new fuel economy + distance tax)** (USD/km)

- Description: Calculation
- Legacy: legacy rows 4452-4456
- Rows: gso,pas, die,pas, lpg,pas
  - 2022-2041: `trckm(t) = trprl[f,rod](t)/trfn[f,s](t)+trdtxp[all,s](t)`
- Rows: nga,pas
  - 2022-2041: `trckm(t) = trprg[f,rod](t)/trfn[f,s](t)+trdtxp[all,s](t)`
- Rows: phv,pas
  - 2022-2041: `trckm(t) = trpphv[f,s](t)/trfnp[f,s](t)+trdtxp[all,s](t)`

**E721. `trckr`: Change in cost per km (ratio to last year)** (ratio)

- Description: Calculation
- Legacy: legacy rows 4457-4461
- Rows: gso,pas, die,pas, lpg,pas, nga,pas, phv,pas
  - 2022: `trckr(t) = ""`
  - 2023-2041: `trckr(t) = trckm[f,s](t)/trckm[f,s](t-1)`

**E722. `trvkn`: Distance per new ICEV for the purchase decision** (km)

- Description: Calculation
- Legacy: legacy rows 4465-4469
- Rows: gso,pas, die,pas, lpg,pas, nga,pas, phv,pas
  - 2022-2041: `trvkn(t) = IF(tr.dk[all,all](t)=1,trvkm[all,s](t),trvkn[f,s](t-1)*IF(<prices act (1 = yes) of trp.vkt[all,all]>,trckr[f,s](t),1)^<usage, gasoline of trp.ela[all,all]>*(1+trgdl[all,all](t))^<passenger of trp.inc[all,all]>)`

**E723. `trvkna`: Average distance per new ICEV, passenger and light** (km)

- Description: Calculation
- Legacy: legacy row 4470
- Rows: all,pas
  - 2022-2041: `trvkna(t) = SUMPRODUCT(trvkn[5 rows](t),trfew[5 rows](t))/SUM(trfew[5 rows](t))`

**E724. `trckbp`: Cost per km of new BEVs, pas (EV electricity price / fuel economy + distance tax)** (USD/km)

- Description: Calculation
- Legacy: legacy row 4472
- Rows: bev,pas
  - 2022-2041: `trckbp(t) = trpev[ecy,res](t)/trfen[f,s](t)+trdtxp[all,s](t)`

**E725. `trckbr`: Change in BEV cost per km (ratio to last year)** (ratio)

- Description: Calculation
- Legacy: legacy rows 4473, 4493, 4504
- Rows: bev,pas
  - 2022: `trckbr(t) = ""`
  - 2023-2041: `trckbr(t) = trckbp[f,s](t)/trckbp[f,s](t-1)`
- Rows: bev,fre
  - 2022: `trckbr(t) = ""`
  - 2023-2041: `trckbr(t) = trckbf[f,s](t)/trckbf[f,s](t-1)`
- Rows: bev,cyc
  - 2022: `trckbr(t) = ""`
  - 2023-2041: `trckbr(t) = trckbc[f,s](t)/trckbc[f,s](t-1)`

**E726. `trckbf`: Cost per km of new BEVs, fre (EV electricity price / fuel economy + distance tax)** (USD/km)

- Description: Calculation
- Legacy: legacy row 4492
- Rows: bev,fre
  - 2022-2041: `trckbf(t) = trpev[ecy,ind](t)/trfen[f,s](t)+trdtxf[all,s](t)`

**E727. `trckbc`: Cost per km of new BEVs, cyc (EV electricity price / fuel economy + distance tax)** (USD/km)

- Description: Calculation
- Legacy: legacy row 4503
- Rows: bev,cyc
  - 2022-2041: `trckbc(t) = trpev[ecy,res](t)/trfen[f,s](t)+trdtxc[all,s](t)`

**E728. `trvknb`: Distance per new BEV for the purchase decision, passenger** (km)

- Description: Calculation
- Legacy: legacy row 4474
- Rows: bev,pas
  - 2022-2041: `trvknb(t) = IF(tr.dk[all,all](t)=1,trvkb[f,s](t),trvknb[f,s](t-1)*IF(<prices act (1 = yes) of trp.vkt[all,all]>,trckbr[f,s](t),1)^<usage, gasoline of trp.ela[all,all]>*(1+trgdl[all,all](t))^<passenger of trp.inc[all,all]>)`

**E729. `trvku`: Distance per used ICEV (x fuel economy ratio new / used ^ usage elasticity)** (km)

- Description: Calculation
- Legacy: legacy row 4475
- Rows: all,pau
  - 2022-2041: `trvku(t) = trvkna[f,pas](t)*(trfna[f,pas](t)/trfeu[f,s](t))^<usage, gasoline of trp.ela[f,all]>`

**E730. `trvkub`: Distance per used BEV** (km)

- Description: Calculation
- Legacy: legacy row 4476
- Rows: bev,pau
  - 2022-2041: `trvkub(t) = trvknb[f,pas](t)*(trfen[f,pas](t)/trfeub[f,s](t))^<usage, gasoline of trp.ela[all,all]>`

**E731. `trckf`: Cost per km of new ICE freight vehicles (net of VAT)** (USD/km)

- Description: Calculation
- Legacy: legacy rows 4480-4482
- Rows: die,fre, lpg,fre
  - 2022-2041: `trckf(t) = trprn[f,rod](t)/trfnf[f,s](t)+trdtxf[all,s](t)`
- Rows: nga,fre
  - 2022-2041: `trckf(t) = trprm[f,s](t)/trfnf[f,s](t)+trdtxf[all,s](t)`

**E732. `trckfr`: Change in freight cost per km (ratio to last year)** (ratio)

- Description: Calculation
- Legacy: legacy rows 4483-4485
- Rows: die,fre, lpg,fre, nga,fre
  - 2022: `trckfr(t) = ""`
  - 2023-2041: `trckfr(t) = trckf[f,s](t)/trckf[f,s](t-1)`

**E733. `trvknf`: Distance per new ICE freight vehicle (between the minimum and maximum)** (km)

- Description: Calculation
- Legacy: legacy rows 4488-4490
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trvknf(t) = IF(tr.dk[all,all](t)=1,trvkd[all,s](t),MAX(<minimum freight km of trp.vkt[all,all]>,MIN(<maximum freight km of trp.vkt[all,all]>,trvknf[f,s](t-1)*IF(<prices act (1 = yes) of trp.vkt[all,all]>,trckfr[f,s](t),1)^<usage, diesel of trp.ela[all,all]>*(1+trgdl[all,all](t))^<freight of trp.inc[all,all]>)))`

**E734. `trvknaf`: Average distance per new ICE freight vehicle** (km)

- Description: Calculation
- Legacy: legacy row 4491
- Rows: all,fre
  - 2022-2041: `trvknaf(t) = SUMPRODUCT(trvknf[3 rows](t),trfewf[3 rows](t))/SUM(trfewf[3 rows](t))`

**E735. `trvknbf`: Distance per new BEV freight vehicle (between the minimum and maximum)** (km)

- Description: Calculation
- Legacy: legacy row 4494
- Rows: bev,fre
  - 2022-2041: `trvknbf(t) = IF(tr.dk[all,all](t)=1,trvkbf[f,s](t),MAX(<minimum freight km of trp.vkt[all,all]>,MIN(<maximum freight km of trp.vkt[all,all]>,trvknbf[f,s](t-1)*IF(<prices act (1 = yes) of trp.vkt[all,all]>,trckbr[f,s](t),1)^<usage, diesel of trp.ela[all,all]>*(1+trgdl[all,all](t))^<freight of trp.inc[all,all]>)))`

**E736. `trckc`: Cost per km of new ICE 2-3 wheelers** (USD/km)

- Description: Calculation
- Legacy: legacy row 4498
- Rows: gso,cyc
  - 2022-2041: `trckc(t) = trprl[f,rod](t)/trfnc[f,s](t)+trdtxc[all,s](t)`

**E737. `trckcr`: Change in 2-3 wheeler cost per km (ratio to last year)** (ratio)

- Description: Calculation
- Legacy: legacy row 4499
- Rows: gso,cyc
  - 2022: `trckcr(t) = ""`
  - 2023-2041: `trckcr(t) = trckc[f,s](t)/trckc[f,s](t-1)`

**E738. `trvkncg`: Distance per new 2-3 wheeler (gso)** (km)

- Description: Calculation
- Legacy: legacy row 4502
- Rows: gso,cyc
  - 2022-2041: `trvkncg(t) = IF(tr.dk[all,all](t)=1,trvkd[all,s](t),trvkncg[f,s](t-1)*IF(<prices act (1 = yes) of trp.vkt[all,all]>,trckcr[f,s](t),1)^<usage, gasoline of trp.ela[all,all]>*(1+trgdl[all,all](t))^<2-3 wheeler of trp.inc[all,all]>)`

**E739. `trvkncb`: Distance per new 2-3 wheeler (bev)** (km)

- Description: Calculation
- Legacy: legacy row 4505
- Rows: bev,cyc
  - 2022-2041: `trvkncb(t) = IF(tr.dk[all,all](t)=1,trvkbc[f,s](t),trvkncb[f,s](t-1)*IF(<prices act (1 = yes) of trp.vkt[all,all]>,trckbr[f,s](t),1)^<usage, gasoline of trp.ela[all,all]>*(1+trgdl[all,all](t))^<2-3 wheeler of trp.inc[all,all]>)`

**E740. `trdkmpasi`: Discounted km over the ownership period (pas, ice)** (km)

- Description: Calculation
- Legacy: legacy row 4509
- Rows: ice,pas
  - 2022-2041: `trdkmpasi(t) = -PV(trdisc[all,all](t),<ownership years, new passenger of trp.life[all,all]>,trvkna[all,s](t))`

**E741. `trdkmpasb`: Discounted km over the ownership period (pas, bev)** (km)

- Description: Calculation
- Legacy: legacy row 4513
- Rows: bev,pas
  - 2022-2041: `trdkmpasb(t) = -PV(trdisc[all,all](t),<ownership years, new passenger of trp.life[all,all]>,trvknb[f,s](t))`

**E742. `trdkmpaui`: Discounted km over the ownership period (pau, ice)** (km)

- Description: Calculation
- Legacy: legacy row 4586
- Rows: ice,pau
  - 2022-2041: `trdkmpaui(t) = -PV(trdisc[all,all](t),<useful life, passenger of trp.life[all,all]>-<ownership years, new passenger of trp.life[all,all]>,trvku[all,s](t))`

**E743. `trdkmpaub`: Discounted km over the ownership period (pau, bev)** (km)

- Description: Calculation
- Legacy: legacy row 4588
- Rows: bev,pau
  - 2022-2041: `trdkmpaub(t) = -PV(trdisc[all,all](t),<useful life, passenger of trp.life[all,all]>-<ownership years, new passenger of trp.life[all,all]>,trvkub[f,s](t))`

**E744. `trdkmfrei`: Discounted km over the ownership period (fre, ice)** (km)

- Description: Calculation
- Legacy: legacy row 4628
- Rows: ice,fre
  - 2022-2041: `trdkmfrei(t) = -PV(trdisc[all,all](t),<useful life, freight of trp.life[all,all]>,trvknaf[all,s](t))`

**E745. `trdkmfreb`: Discounted km over the ownership period (fre, bev)** (km)

- Description: Calculation
- Legacy: legacy row 4630
- Rows: bev,fre
  - 2022-2041: `trdkmfreb(t) = -PV(trdisc[all,all](t),<useful life, freight of trp.life[all,all]>,trvknbf[f,s](t))`

**E746. `trdkmcyci`: Discounted km over the ownership period (cyc, ice)** (km)

- Description: Calculation
- Legacy: legacy row 4685
- Rows: ice,cyc
  - 2022-2041: `trdkmcyci(t) = -PV(trdisc[all,all](t),<useful life, 2-3 wheeler of trp.life[all,all]>,trvkncg[gso,s](t))`

**E747. `trdkmcycb`: Discounted km over the ownership period (cyc, bev)** (km)

- Description: Calculation
- Legacy: legacy row 4687
- Rows: bev,cyc
  - 2022-2041: `trdkmcycb(t) = -PV(trdisc[all,all](t),<useful life, 2-3 wheeler of trp.life[all,all]>,trvkncb[f,s](t))`

**E748. `trpvap`: Feebate pivot, average type (pas)** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4517 (Average)
- Rows: all,pas
  - 2022-2041: `trpvap(t) = IF(tr.col[f,all](t)<=TrPivotLag,"",N(trints[f,s](t))*N(trints[f,s](t))/N(trints[f,s](t-1)))`

**E749. `trpvmp`: Feebate pivot, manual type (pas; declining after the start year)** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4517 (Manual)
- Rows: all,pas
  - 2022-2041: `trpvmp(t) = IF(tr.col[f,all](t)<=TrPivotLag,"",IF(year=TrFbYearPas[f,all](t),TrFbPivotPas[f,all](t),IF(year>TrFbYearPas[f,all](t),MAX(0,N(trpvmp[f,s](t-1))-TrFbPivotChgPas[f,all](t)),0)))`

**E750. `trpvp`: Feebate pivot used (pas)** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4517
- Rows: all,pas
  - 2022-2041: `trpvp(t) = IF(LEFT(TrFbPivotTypePas[f,all](t),3)="Ave",trpvap[f,s](t),trpvmp[f,s](t))`

**E751. `trfbvpi`: Vehicle feebate (pas, ice; BEV intensity 0)** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4520
- Rows: ice,pas
  - 2022: `trfbvpi(t) = ""`
  - 2023-2041: `trfbvpi(t) = (trinta[all,s](t)-N(trpvp[all,s](t)))*trfbtp[all,s](t)/Million*trdkmpasi[f,s](t)`

**E752. `trfbvpb`: Vehicle feebate (pas, bev; BEV intensity 0)** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4521
- Rows: bev,pas
  - 2022: `trfbvpb(t) = ""`
  - 2023-2041: `trfbvpb(t) = (0-N(trpvp[all,s](t)))*trfbtp[all,s](t)/Million*trdkmpasb[f,s](t)`

**E753. `tradvpi`: Ad-valorem purchase tax rate used (pas, ice)** (share)

- Description: Calculation
- Legacy: legacy row 4525
- Rows: ice,pas
  - 2022-2041: `tradvpi(t) = IF(OR(tr.pol[all,all](t)=0,year<TrAdvYearPas[all,all](t)),TrAdvIceBasePas[all,all](t),TrAdvIcePolPas[all,all](t))`

**E754. `tradvpb`: Ad-valorem purchase tax rate used (pas, bev)** (share)

- Description: Calculation
- Legacy: legacy row 4559
- Rows: bev,pas
  - 2022-2041: `tradvpb(t) = IF(OR(tr.pol[all,all](t)=0,year<TrAdvYearPas[all,all](t)),TrAdvBevBasePas[all,all](t),TrAdvBevPolPas[all,all](t))`

**E755. `tradvfi`: Ad-valorem purchase tax rate used (fre, ice)** (share)

- Description: Calculation
- Legacy: legacy row 4641
- Rows: ice,fre
  - 2022-2041: `tradvfi(t) = IF(OR(tr.pol[all,all](t)=0,year<TrAdvYearFre[all,all](t)),TrAdvIceBaseFre[all,all](t),TrAdvIcePolFre[all,all](t))`

**E756. `tradvfb`: Ad-valorem purchase tax rate used (fre, bev)** (share)

- Description: Calculation
- Legacy: legacy row 4664
- Rows: bev,fre
  - 2022-2041: `tradvfb(t) = IF(OR(tr.pol[all,all](t)=0,year<TrAdvYearFre[all,all](t)),TrAdvBevBaseFre[all,all](t),TrAdvBevPolFre[all,all](t))`

**E757. `tradvci`: Ad-valorem purchase tax rate used (cyc, ice)** (share)

- Description: Calculation
- Legacy: legacy row 4698
- Rows: ice,cyc
  - 2022-2041: `tradvci(t) = IF(OR(tr.pol[all,all](t)=0,year<TrAdvYearCyc[all,all](t)),TrAdvIceBaseCyc[all,all](t),TrAdvIcePolCyc[all,all](t))`

**E758. `tradvcb`: Ad-valorem purchase tax rate used (cyc, bev)** (share)

- Description: Calculation
- Legacy: legacy row 4718
- Rows: bev,cyc
  - 2022-2041: `tradvcb(t) = IF(OR(tr.pol[all,all](t)=0,year<TrAdvYearCyc[all,all](t)),TrAdvBevBaseCyc[all,all](t),TrAdvBevPolCyc[all,all](t))`

**E759. `trcuep`: Import duty x import share on BEVs (pas; policy rate from its year)** (share)

- Description: Calculation
- Legacy: legacy row 4558
- Rows: bev,pas
  - 2022-2041: `trcuep(t) = IF(OR(tr.pol[all,all](t)=0,year<TrCustYearPas[all,all](t)),<duty, BEV of trp.tax[all,s]>*<share of imports of trp.tax[all,s]>,<duty, BEV of trp.tax[all,s]>*TrCustPolFactor[all,all](t)*<share of imports of trp.tax[all,s]>)`

**E760. `trcuef`: Import duty x import share on BEVs (fre; policy rate from its year)** (share)

- Description: Calculation
- Legacy: legacy row 4663
- Rows: bev,fre
  - 2022-2041: `trcuef(t) = IF(OR(tr.pol[all,all](t)=0,year<TrCustYearFre[all,all](t)),<duty, BEV of trp.tax[all,s]>*<share of imports of trp.tax[all,s]>,<duty, BEV of trp.tax[all,s]>*TrCustPolFactor[all,all](t)*<share of imports of trp.tax[all,s]>)`

**E761. `trcuec`: Import duty x import share on BEVs (cyc; policy rate from its year)** (share)

- Description: Calculation
- Legacy: legacy row 4717
- Rows: bev,cyc
  - 2022-2041: `trcuec(t) = IF(OR(tr.pol[all,all](t)=0,year<TrCustYearCyc[all,all](t)),<duty, BEV of trp.tax[all,s]>*<share of imports of trp.tax[all,s]>,<duty, BEV of trp.tax[all,s]>*TrCustPolFactor[all,all](t)*<share of imports of trp.tax[all,s]>)`

**E762. `trvatbp`: VAT rate on BEVs (pas; policy rate from its year)** (share)

- Description: Calculation
- Legacy: legacy row 4560
- Rows: bev,pas
  - 2022-2041: `trvatbp(t) = IF(OR(tr.pol[all,all](t)=0,year<TrVatYearPas[all,all](t)),<VAT rate of trp.tax[all,s]>,<VAT rate of trp.tax[all,s]>*TrVatPolFactor[all,all](t))`

**E763. `trvatbc`: VAT rate on BEVs (cyc; policy rate from its year)** (share)

- Description: Calculation
- Legacy: legacy row 4719
- Rows: bev,cyc
  - 2022-2041: `trvatbc(t) = IF(OR(tr.pol[all,all](t)=0,year<TrVatYearCyc[all,all](t)),<VAT rate of trp.tax[all,s]>,<VAT rate of trp.tax[all,s]>*TrVatPolFactor[all,all](t))`

**E764. `trsubp`: EV purchase subsidy (pas; negative; policy scenarios, fix B1)** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4561
- Rows: bev,pas
  - 2022-2041: `trsubp(t) = IF(year=TrSubYearPas[all,all](t),-TrSubAmountPas[all,all](t),IF(year>TrSubYearPas[all,all](t),MIN(0,N(trsubp[f,s](t-1))-TrSubChgPas[all,all](t)),0))*tr.pol[all,all](t)`

**E765. `trsubf`: EV purchase subsidy (fre; negative; policy scenarios, fix B1)** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4665
- Rows: bev,fre
  - 2022-2041: `trsubf(t) = IF(year=TrSubYearFre[all,all](t),-TrSubAmountFre[all,all](t),IF(year>TrSubYearFre[all,all](t),MIN(0,N(trsubf[f,s](t-1))-TrSubChgFre[all,all](t)),0))*tr.pol[all,all](t)`

**E766. `trsubc`: EV purchase subsidy (cyc; negative; policy scenarios, fix B1)** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4720
- Rows: bev,cyc
  - 2022-2041: `trsubc(t) = IF(year=TrSubYearCyc[all,all](t),-TrSubAmountCyc[all,all](t),IF(year>TrSubYearCyc[all,all](t),MIN(0,N(trsubc[f,s](t-1))-TrSubChgCyc[all,all](t)),0))*tr.pol[all,all](t)`

**E767. `trppip`: Purchase price after taxes and feebate, new ICEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4527
- Rows: ice,pas
  - 2022-2041: `trppip(t) = trvp[f,s](t)*(1+(<duty, ICEV of trp.tax[all,s]>*<share of imports of trp.tax[all,s]>))*(1+tradvpi[f,s](t))*(1+<VAT rate of trp.tax[all,s]>)+N(trfbvpi[f,s](t))`

**E768. `trdppin`: First-year depreciation, new ICEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4533
- Rows: ice,pas
  - 2022-2041: `trdppin(t) = trppip[f,s](t)*<first-year depreciation, passenger of trp.dep[all,all]>`

**E769. `tranpin`: Depreciation annuity after the first year, new ICEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4534
- Rows: ice,pas
  - 2022-2041: `tranpin(t) = (trppip[f,s](t)-trdppin[f,s](t))/(<useful life, passenger of trp.life[all,all]>-1)/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<useful life, passenger of trp.life[all,all]>-1))`

**E770. `trsvpin`: Salvage value (negative), new ICEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4535
- Rows: ice,pas
  - 2022-2041: `trsvpin(t) = MIN(0,-trppip[f,s](t)*((<useful life, passenger of trp.life[all,all]>-<ownership years, new passenger of trp.life[all,all]>)/<useful life, passenger of trp.life[all,all]>*(1-<first-year depreciation, passenger of trp.dep[all,all]>))/(1+trdisc[all,all](t))^<ownership years, new passenger of trp.life[all,all]>)`

**E771. `trimpin`: Insurance and maintenance, new ICEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4541
- Rows: ice,pas
  - 2022-2041: `trimpin(t) = trppip[f,s](t)*<insurance, passenger of trp.ins[all,all]>/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<ownership years, new passenger of trp.life[all,all]>+1))*<factor on the insurance annuity of trp.dep[all,all]>+<USD/km, passenger of trp.mic[all,all]>*trdkmpasi[f,s](t)`

**E772. `trfupin`: Fuel and distance tax, new ICEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4546
- Rows: ice,pas
  - 2022-2041: `trfupin(t) = (trpav[all,s](t)/trfna[all,s](t)+trdtxp[all,s](t))*trdkmpasi[f,s](t)`

**E773. `trtopin`: TCO, new ICEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4548
- Rows: ice,pas
  - 2022-2041: `trtopin(t) = SUM(block@trdppin{trdppin, tranpin, trsvpin, trimpin, ... 5 variables}(t))`

**E774. `trpkpin`: TCO per km, new ICEV passenger** (USD/km)

- Description: Calculation
- Legacy: legacy row 4549
- Rows: ice,pas
  - 2022-2041: `trpkpin(t) = trtopin[f,s](t)/trdkmpasi[f,s](t)`

**E775. `trresp`: Resale price of a 7-year-old ICEV before taxes (price used vehicle)** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4537
- Rows: ice,pas
  - 2022-2041: `trresp(t) = trvp[f,s](t)*(1-(<first-year depreciation, passenger of trp.dep[all,all]>+(<ownership years, new passenger of trp.life[all,all]>-1)/(<useful life, passenger of trp.life[all,all]>-1)*(1-<first-year depreciation, passenger of trp.dep[all,all]>)))`

**E776. `trresgp`: Price of a used ICEV after taxes** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4538
- Rows: ice,pas
  - 2022-2041: `trresgp(t) = trresp[f,s](t)*(1+(<duty, ICEV of trp.tax[all,s]>*<share of imports of trp.tax[all,s]>))*(1+tradvpi[f,s](t))*(1+<VAT rate of trp.tax[all,s]>)+0`

**E777. `trtcf`: TCO by ICE fuel, new passenger (cost per km by fuel; feebate by fuel intensity)** (USD/vehicle)

- Description: Calculation
- Legacy: legacy rows 4551-4554
- Rows: gso,pas, die,pas, lpg,pas, nga,pas
  - 2022-2041: `trtcf(t) = trdkmpasi[ice,s](t)*trckm[f,s](t)+(SUM(block@trdppin{trdppin, tranpin, trsvpin}(t))+trimpin[ice,s](t))+N(trfbvpi[ice,s](t))*(trint[f,s](t)/trinta[all,s](t))`

**E778. `trppbp`: Purchase price after taxes, feebate and subsidy, new BEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4562
- Rows: bev,pas
  - 2022-2041: `trppbp(t) = trvp[f,s](t)*(1+trcuep[f,s](t))*(1+trvatbp[f,s](t))*(1+tradvpb[f,s](t))+(trsubp[f,s](t)+N(trfbvpb[f,s](t)))`

**E779. `trdppbn`: First-year depreciation, new BEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4565
- Rows: bev,pas
  - 2022-2041: `trdppbn(t) = trppbp[f,s](t)*<first-year depreciation, passenger of trp.dep[all,all]>`

**E780. `tranpbn`: Depreciation annuity after the first year, new BEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4566
- Rows: bev,pas
  - 2022-2041: `tranpbn(t) = (trppbp[f,s](t)-trdppbn[f,s](t))/(<useful life, passenger of trp.life[all,all]>-1)/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<useful life, passenger of trp.life[all,all]>-1))`

**E781. `trsvpbn`: Salvage value (negative), new BEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4567
- Rows: bev,pas
  - 2022-2041: `trsvpbn(t) = MIN(0,-trppbp[f,s](t)*((<useful life, passenger of trp.life[all,all]>-<ownership years, new passenger of trp.life[all,all]>)/<useful life, passenger of trp.life[all,all]>*(1-<first-year depreciation, passenger of trp.dep[all,all]>))/(1+trdisc[all,all](t))^<ownership years, new passenger of trp.life[all,all]>)`

**E782. `trimpbn`: Insurance and maintenance, new BEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4573
- Rows: bev,pas
  - 2022-2041: `trimpbn(t) = trppbp[f,s](t)*<insurance, passenger of trp.ins[all,all]>/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<ownership years, new passenger of trp.life[all,all]>+1))*<factor on the insurance annuity of trp.dep[all,all]>+<USD/km, passenger of trp.mev[all,all]>*trdkmpasb[f,s](t)`

**E783. `trfupbn`: Fuel and distance tax, new BEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4577
- Rows: bev,pas
  - 2022-2041: `trfupbn(t) = (trpev[ecy,res](t)/trfen[f,s](t)+trdtxp[all,s](t))*trdkmpasb[f,s](t)`

**E784. `trtopbn`: TCO, new BEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4581
- Rows: bev,pas
  - 2022-2041: `trtopbn(t) = SUM(block@trdppbn{trdppbn, tranpbn, trsvpbn, trimpbn, ... 5 variables}(t))+trra[f,s](t)`

**E785. `trpkpbn`: TCO per km, new BEV passenger** (USD/km)

- Description: Calculation
- Legacy: legacy row 4582
- Rows: bev,pas
  - 2022-2041: `trpkpbn(t) = trtopbn[f,s](t)/trdkmpasb[f,s](t)`

**E786. `trimphv`: Insurance and maintenance, new PHEV (insurance on the BEV price, ICEV maintenance per km and distance; bug M17 fixed)** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4555 (legacy used row 4541, the ICEV's)
- Rows: phv,pas
  - 2022-2041: `trimphv(t) = trppbp[bev,s](t)*<insurance, passenger of trp.ins[all,all]>/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<ownership years, new passenger of trp.life[all,all]>+1))*<factor on the insurance annuity of trp.dep[all,all]>+<USD/km, passenger of trp.mic[all,all]>*trdkmpasi[ice,s](t)`

**E787. `trtcfp`: TCO of a new PHEV (BEV depreciation, insurance on the BEV price, no range anxiety: fixes B23, M17)** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4555
- Rows: phv,pas
  - 2022-2041: `trtcfp(t) = trdkmpasi[ice,s](t)*trckm[f,s](t)+(SUM(block@trdppbn{trdppbn, tranpbn, trsvpbn}(t))+trimphv[f,s](t))+N(trfbvpi[ice,s](t))*(trint[f,s](t)/trinta[all,s](t))`

**E788. `trresb`: Resale price of a 7-year-old BEV before taxes** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4569
- Rows: bev,pas
  - 2022-2041: `trresb(t) = trvp[f,s](t)*(1-(<first-year depreciation, passenger of trp.dep[all,all]>+(<ownership years, new passenger of trp.life[all,all]>-1)/(<useful life, passenger of trp.life[all,all]>-1)*(1-<first-year depreciation, passenger of trp.dep[all,all]>)))`

**E789. `trresgb`: Price of a used BEV after taxes** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4570
- Rows: bev,pas
  - 2022-2041: `trresgb(t) = trresb[f,s](t)*(1+trcuep[f,s](t))*(1+tradvpb[f,s](t))*(1+trvatbp[f,s](t))+0`

**E790. `trfbvui`: Vehicle feebate, used passenger ice** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4593
- Rows: ice,pau
  - 2022: `trfbvui(t) = ""`
  - 2023-2041: `trfbvui(t) = (trintu[all,s](t)-N(trpvp[all,pas](t)))*trfbtp[all,pas](t)/Million*trdkmpaui[f,s](t)`

**E791. `trfbvub`: Vehicle feebate, used passenger bev** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4594
- Rows: bev,pau
  - 2022: `trfbvub(t) = ""`
  - 2023-2041: `trfbvub(t) = (0-N(trpvp[all,pas](t)))*trfbtp[all,pas](t)/Million*trdkmpaub[f,s](t)`

**E792. `trppui`: Price of a used ICEV incl. feebate** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4597
- Rows: ice,pau
  - 2022-2041: `trppui(t) = trresgp[f,pas](t)+N(trfbvui[f,s](t))`

**E793. `tranpiu`: Depreciation annuity over the used ownership period, used ICEV passenger (fix B20)** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4598
- Rows: ice,pau
  - 2022-2041: `tranpiu(t) = trppui[f,s](t)/(<useful life, passenger of trp.life[all,all]>-<ownership years, new passenger of trp.life[all,all]>-1)/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<useful life, passenger of trp.life[all,all]>-<ownership years, new passenger of trp.life[all,all]>-1))`

**E794. `trimpiu`: Insurance and maintenance, used ICEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4600
- Rows: ice,pau
  - 2022-2041: `trimpiu(t) = trppui[f,s](t)*<insurance, passenger of trp.ins[all,all]>/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^((<useful life, passenger of trp.life[all,all]>-<ownership years, new passenger of trp.life[all,all]>)+1))*<factor on the insurance annuity of trp.dep[all,all]>+<USD/km, passenger of trp.mic[all,all]>*trdkmpaui[f,s](t)`

**E795. `trfupiu`: Fuel and distance tax, used ICEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4605
- Rows: ice,pau
  - 2022-2041: `trfupiu(t) = (trpav[all,pas](t)/trfeu[all,s](t)+trdtxp[all,pas](t))*trdkmpaui[f,s](t)`

**E796. `trtopiu`: TCO, used ICEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4607
- Rows: ice,pau
  - 2022-2041: `trtopiu(t) = SUM(block@tranpiu{tranpiu, trimpiu, trfupiu}(t))`

**E797. `trpkpiu`: TCO per km, used ICEV passenger** (USD/km)

- Description: Calculation
- Legacy: legacy row 4608
- Rows: ice,pau
  - 2022-2041: `trpkpiu(t) = trtopiu[f,s](t)/trdkmpaui[f,s](t)`

**E798. `trppub`: Price of a used BEV incl. feebate and subsidy** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4612
- Rows: bev,pau
  - 2022-2041: `trppub(t) = trresgb[f,pas](t)+N(trfbvub[f,s](t))+trsubp[f,pas](t)`

**E799. `trrau`: Range anxiety of a used BEV (scaled by the used / new price)** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4621
- Rows: bev,pau
  - 2022-2041: `trrau(t) = (trra[f,pas](t)*trppub[f,s](t))/trppbp[f,pas](t)`

**E800. `tranpbu`: Depreciation annuity over the used ownership period, used BEV passenger (fix B20)** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4613
- Rows: bev,pau
  - 2022-2041: `tranpbu(t) = trppub[f,s](t)/(<useful life, passenger of trp.life[all,all]>-<ownership years, new passenger of trp.life[all,all]>-1)/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<useful life, passenger of trp.life[all,all]>-<ownership years, new passenger of trp.life[all,all]>-1))`

**E801. `trimpbu`: Insurance and maintenance, used BEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4615
- Rows: bev,pau
  - 2022-2041: `trimpbu(t) = trppub[f,s](t)*<insurance, passenger of trp.ins[all,all]>/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^((<useful life, passenger of trp.life[all,all]>-<ownership years, new passenger of trp.life[all,all]>)+1))*<factor on the insurance annuity of trp.dep[all,all]>+<USD/km, passenger of trp.mev[all,all]>*trdkmpaub[f,s](t)`

**E802. `trfupbu`: Fuel and distance tax, used BEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4619
- Rows: bev,pau
  - 2022-2041: `trfupbu(t) = (trpev[ecy,res](t)/trfeub[f,s](t)+trdtxp[all,pas](t))*trdkmpaub[f,s](t)`

**E803. `trtopbu`: TCO, used BEV passenger** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4623
- Rows: bev,pau
  - 2022-2041: `trtopbu(t) = SUM(block@tranpbu{tranpbu, trimpbu, trfupbu}(t))+trrau[f,s](t)`

**E804. `trpkpbu`: TCO per km, used BEV passenger** (USD/km)

- Description: Calculation
- Legacy: legacy row 4624
- Rows: bev,pau
  - 2022-2041: `trpkpbu(t) = trtopbu[f,s](t)/trdkmpaub[f,s](t)`

**E805. `trpvaf`: Feebate pivot, average type (fre)** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4633 (Average)
- Rows: all,fre
  - 2022-2041: `trpvaf(t) = IF(tr.col[f,all](t)<=TrPivotLag,"",N(trintsf[f,s](t))*N(trintsf[f,s](t))/N(trintsf[f,s](t-1)))`

**E806. `trpvmf`: Feebate pivot, manual type (fre; declining after the start year)** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4633 (Manual)
- Rows: all,fre
  - 2022-2041: `trpvmf(t) = IF(tr.col[f,all](t)<=TrPivotLag,"",IF(year=TrFbYearFre[f,all](t),TrFbPivotFre[f,all](t),IF(year>TrFbYearFre[f,all](t),MAX(0,N(trpvmf[f,s](t-1))-TrFbPivotChgFre[f,all](t)),0)))`

**E807. `trpvf`: Feebate pivot used (fre)** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4633
- Rows: all,fre
  - 2022-2041: `trpvf(t) = IF(LEFT(TrFbPivotTypeFre[f,all](t),3)="Ave",trpvaf[f,s](t),trpvmf[f,s](t))`

**E808. `trfbvfi`: Vehicle feebate, freight ice** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4636
- Rows: ice,fre
  - 2022: `trfbvfi(t) = ""`
  - 2023-2041: `trfbvfi(t) = (trintaf[all,s](t)-N(trpvf[all,s](t)))*trfbtf[all,s](t)/Million*trdkmfrei[f,s](t)`

**E809. `trfbvfb`: Vehicle feebate, freight bev** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4637
- Rows: bev,fre
  - 2022: `trfbvfb(t) = ""`
  - 2023-2041: `trfbvfb(t) = (0-N(trpvf[all,s](t)))*trfbtf[all,s](t)/Million*trdkmfreb[f,s](t)`

**E810. `trppfi`: Purchase price after taxes and feebate, new ICE freight vehicle (no VAT, as legacy)** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4642
- Rows: ice,fre
  - 2022-2041: `trppfi(t) = trvp[f,s](t)*(1+(<duty, ICEV of trp.tax[all,s]>*<share of imports of trp.tax[all,s]>))*(1+tradvfi[f,s](t))*(1+0)+N(trfbvfi[f,s](t))`

**E811. `trdpfin`: First-year depreciation, new ICE freight** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4645
- Rows: ice,fre
  - 2022-2041: `trdpfin(t) = trppfi[f,s](t)*<first-year depreciation, freight of trp.dep[all,all]>`

**E812. `tranfin`: Depreciation annuity after the first year, new ICE freight** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4646
- Rows: ice,fre
  - 2022-2041: `tranfin(t) = (trppfi[f,s](t)-trdpfin[f,s](t))/(<useful life, freight of trp.life[all,all]>-1)/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<useful life, freight of trp.life[all,all]>-1))`

**E813. `trimfin`: Insurance and maintenance, new ICE freight** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4648
- Rows: ice,fre
  - 2022-2041: `trimfin(t) = trppfi[f,s](t)*<insurance, freight of trp.ins[all,all]>/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<useful life, freight of trp.life[all,all]>+1))*<factor on the insurance annuity of trp.dep[all,all]>+<USD/km, freight of trp.mic[all,all]>*trdkmfrei[f,s](t)`

**E814. `trfufin`: Fuel and distance tax, new ICE freight** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4653
- Rows: ice,fre
  - 2022-2041: `trfufin(t) = (trpavf[all,s](t)/trfnaf[all,s](t)+trdtxf[all,s](t))*trdkmfrei[f,s](t)`

**E815. `trtofin`: TCO, new ICE freight** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4655
- Rows: ice,fre
  - 2022-2041: `trtofin(t) = SUM(block@trdpfin{trdpfin, tranfin, trimfin, trfufin}(t))`

**E816. `trpkfin`: TCO per km, new ICE freight** (USD/km)

- Description: Calculation
- Legacy: legacy row 4656
- Rows: ice,fre
  - 2022-2041: `trpkfin(t) = trtofin[f,s](t)/trdkmfrei[f,s](t)`

**E817. `trtcff`: TCO by ICE fuel, new freight vehicle** (USD/vehicle)

- Description: Calculation
- Legacy: legacy rows 4658-4660
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trtcff(t) = trdkmfrei[ice,s](t)*trckf[f,s](t)+SUM(block@trdpfin{trdpfin, tranfin, trimfin}(t))+N(trfbvfi[ice,s](t))*(trintf[f,s](t)/trintaf[all,s](t))`

**E818. `trppfb`: Purchase price after taxes, feebate and subsidy, new BEV freight vehicle** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4666
- Rows: bev,fre
  - 2022-2041: `trppfb(t) = trvp[f,s](t)*(1+trcuef[f,s](t))*(1+tradvfb[f,s](t))*(1+0)+(N(trfbvfb[f,s](t))+trsubf[f,s](t))`

**E819. `trdpfbn`: First-year depreciation, new BEV freight** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4669
- Rows: bev,fre
  - 2022-2041: `trdpfbn(t) = trppfb[f,s](t)*<first-year depreciation, freight of trp.dep[all,all]>`

**E820. `tranfbn`: Depreciation annuity after the first year, new BEV freight** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4670
- Rows: bev,fre
  - 2022-2041: `tranfbn(t) = (trppfb[f,s](t)-trdpfbn[f,s](t))/(<useful life, freight of trp.life[all,all]>-1)/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<useful life, freight of trp.life[all,all]>-1))`

**E821. `trimfbn`: Insurance and maintenance, new BEV freight** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4672
- Rows: bev,fre
  - 2022-2041: `trimfbn(t) = trppfb[f,s](t)*<insurance, freight of trp.ins[all,all]>/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<useful life, freight of trp.life[all,all]>+1))*<factor on the insurance annuity of trp.dep[all,all]>+<USD/km, freight of trp.mev[all,all]>*trdkmfreb[f,s](t)`

**E822. `trfufbn`: Fuel and distance tax, new BEV freight** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4676
- Rows: bev,fre
  - 2022-2041: `trfufbn(t) = (trpev[ecy,ind](t)/trfen[f,s](t)+trdtxf[all,s](t))*trdkmfreb[f,s](t)`

**E823. `trtofbn`: TCO, new BEV freight** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4680
- Rows: bev,fre
  - 2022-2041: `trtofbn(t) = SUM(block@trdpfbn{trdpfbn, tranfbn, trimfbn, trfufbn}(t))+trra[f,s](t)`

**E824. `trpkfbn`: TCO per km, new BEV freight** (USD/km)

- Description: Calculation
- Legacy: legacy row 4681
- Rows: bev,fre
  - 2022-2041: `trpkfbn(t) = trtofbn[f,s](t)/trdkmfreb[f,s](t)`

**E825. `trpvac`: Feebate pivot, average type (cyc)** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4690 (Average)
- Rows: all,cyc
  - 2022-2041: `trpvac(t) = IF(tr.col[f,all](t)<=TrPivotLag,"",N(trintsc[gso,s](t))*N(trintsc[gso,s](t))/N(trintsc[gso,s](t-1)))`

**E826. `trpvmc`: Feebate pivot, manual type (cyc; declining after the start year)** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4690 (Manual)
- Rows: all,cyc
  - 2022-2041: `trpvmc(t) = IF(tr.col[f,all](t)<=TrPivotLag,"",IF(year=TrFbYearCyc[f,all](t),TrFbPivotCyc[f,all](t),IF(year>TrFbYearCyc[f,all](t),MAX(0,N(trpvmc[f,s](t-1))-TrFbPivotChgCyc[f,all](t)),0)))`

**E827. `trpvc`: Feebate pivot used (cyc)** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 4690
- Rows: all,cyc
  - 2022-2041: `trpvc(t) = IF(LEFT(TrFbPivotTypeCyc[f,all](t),3)="Ave",trpvac[f,s](t),trpvmc[f,s](t))`

**E828. `trfbvci`: Vehicle feebate, 2-3 wheeler ice** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4693
- Rows: ice,cyc
  - 2022: `trfbvci(t) = ""`
  - 2023-2041: `trfbvci(t) = (trintc[gso,s](t)-N(trpvc[all,s](t)))*trfbtc[all,s](t)/Million*trdkmcyci[f,s](t)`

**E829. `trfbvcb`: Vehicle feebate, 2-3 wheeler bev** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4694
- Rows: bev,cyc
  - 2022: `trfbvcb(t) = ""`
  - 2023-2041: `trfbvcb(t) = (0-N(trpvc[all,s](t)))*trfbtc[all,s](t)/Million*trdkmcycb[f,s](t)`

**E830. `trppci`: Purchase price after taxes and feebate, new ICE 2-3 wheeler** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4700
- Rows: ice,cyc
  - 2022-2041: `trppci(t) = trvp[f,s](t)*(1+(<duty, ICEV of trp.tax[all,s]>*<share of imports of trp.tax[all,s]>))*(1+<VAT rate of trp.tax[all,s]>)*(1+tradvci[f,s](t))+N(trfbvci[f,s](t))`

**E831. `trdpcin`: First-year depreciation, new ICE 2-3 wheeler** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4703
- Rows: ice,cyc
  - 2022-2041: `trdpcin(t) = trppci[f,s](t)*<first-year depreciation, 2-3 wheeler of trp.dep[all,all]>`

**E832. `trancin`: Depreciation annuity after the first year, new ICE 2-3 wheeler** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4704
- Rows: ice,cyc
  - 2022-2041: `trancin(t) = (trppci[f,s](t)-trdpcin[f,s](t))/(<useful life, 2-3 wheeler of trp.life[all,all]>-1)/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<useful life, 2-3 wheeler of trp.life[all,all]>-1))`

**E833. `trimcin`: Insurance and maintenance, new ICE 2-3 wheeler** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4706
- Rows: ice,cyc
  - 2022-2041: `trimcin(t) = trppci[f,s](t)*<insurance, 2-3 wheeler of trp.ins[all,all]>/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<useful life, 2-3 wheeler of trp.life[all,all]>+1))*<factor on the insurance annuity of trp.dep[all,all]>+<USD/km, 2-3 wheeler of trp.mic[all,all]>*trdkmcyci[f,s](t)`

**E834. `trfucin`: Fuel and distance tax, new ICE 2-3 wheeler** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4711
- Rows: ice,cyc
  - 2022-2041: `trfucin(t) = (trprl[gso,rod](t)/trfnc[gso,s](t)+trdtxc[all,s](t))*trdkmcyci[f,s](t)`

**E835. `trtocin`: TCO, new ICE 2-3 wheeler** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4713
- Rows: ice,cyc
  - 2022-2041: `trtocin(t) = SUM(block@trdpcin{trdpcin, trancin, trimcin, trfucin}(t))`

**E836. `trpkcin`: TCO per km, new ICE 2-3 wheeler** (USD/km)

- Description: Calculation
- Legacy: legacy row 4714
- Rows: ice,cyc
  - 2022-2041: `trpkcin(t) = trtocin[f,s](t)/trdkmcyci[f,s](t)`

**E837. `trppcb`: Purchase price after taxes, feebate and subsidy, new BEV 2-3 wheeler** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4721
- Rows: bev,cyc
  - 2022-2041: `trppcb(t) = trvp[f,s](t)*(1+trcuec[f,s](t))*(1+trvatbc[f,s](t))*(1+tradvcb[f,s](t))+(N(trfbvcb[f,s](t))+trsubc[f,s](t))`

**E838. `trdpcbn`: First-year depreciation, new BEV 2-3 wheeler** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4724
- Rows: bev,cyc
  - 2022-2041: `trdpcbn(t) = trppcb[f,s](t)*<first-year depreciation, 2-3 wheeler of trp.dep[all,all]>`

**E839. `trancbn`: Depreciation annuity after the first year, new BEV 2-3 wheeler** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4725
- Rows: bev,cyc
  - 2022-2041: `trancbn(t) = (trppcb[f,s](t)-trdpcbn[f,s](t))/(<useful life, 2-3 wheeler of trp.life[all,all]>-1)/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<useful life, 2-3 wheeler of trp.life[all,all]>-1))`

**E840. `trimcbn`: Insurance and maintenance, new BEV 2-3 wheeler** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4727
- Rows: bev,cyc
  - 2022-2041: `trimcbn(t) = trppcb[f,s](t)*<insurance, 2-3 wheeler of trp.ins[all,all]>/trdisc[all,all](t)*(1-1/(1+trdisc[all,all](t))^(<useful life, 2-3 wheeler of trp.life[all,all]>+1))*<factor on the insurance annuity of trp.dep[all,all]>+<USD/km, 2-3 wheeler of trp.mev[all,all]>*trdkmcycb[f,s](t)`

**E841. `trfucbn`: Fuel and distance tax, new BEV 2-3 wheeler** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4731
- Rows: bev,cyc
  - 2022-2041: `trfucbn(t) = (trpev[ecy,res](t)/trfen[f,s](t)+trdtxc[all,s](t))*trdkmcycb[f,s](t)`

**E842. `trtocbn`: TCO, new BEV 2-3 wheeler** (USD/vehicle)

- Description: Calculation
- Legacy: legacy row 4735
- Rows: bev,cyc
  - 2022-2041: `trtocbn(t) = SUM(block@trdpcbn{trdpcbn, trancbn, trimcbn, trfucbn}(t))+trra[f,s](t)`

**E843. `trpkcbn`: TCO per km, new BEV 2-3 wheeler** (USD/km)

- Description: Calculation
- Legacy: legacy row 4736
- Rows: bev,cyc
  - 2022-2041: `trpkcbn(t) = trtocbn[f,s](t)/trdkmcycb[f,s](t)`

**E844. `trjhp`: Ownership expected from the Gompertz curve in the last data year, passenger and light (held)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy H4787 / H4903 (B3: last data year)
- Rows: all,pas
  - 2022-2041: `trjhp(t) = IF(tr.dk[f,all](t)=1,(trsat[f,all](t)*(1-trfsh[f,fre](t)))*EXP(<Gompertz constant of trp.ogr[f,all]>*EXP(trgpc[f,all](t)*<Gompertz income coefficient, passenger of trp.own[f,all]>/Thousand)),trjhp[f,s](t-1))`

**E845. `trjip`: Actual ownership in the last data year, passenger and light (held)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy I4787 / I4903 (B3)
- Rows: all,pas
  - 2022-2041: `trjip(t) = IF(tr.dk[f,all](t)=1,trowne[bev,s](t)+trownb[ice,s](t),trjip[f,s](t-1))`

**E846. `trjjp`: Ownership calibration factor actual / expected, passenger and light (held; fix B3: both ways)** (factor)

- Description: Calculation
- Legacy: legacy J4787 / J4903 (B3)
- Rows: all,pas
  - 2022-2041: `trjjp(t) = IF(tr.dk[f,all](t)=1,trjip[f,s](t)/trjhp[f,s](t),trjjp[f,s](t-1))`

**E847. `trjhf`: Ownership expected from the Gompertz curve in the last data year, freight (held)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy H4787 / H4903 (B3: last data year)
- Rows: all,fre
  - 2022-2041: `trjhf(t) = IF(tr.dk[f,all](t)=1,(trsat[f,all](t)*trfsh[f,s](t))*EXP(<Gompertz constant of trp.ogr[f,all]>*EXP(trgpc[f,all](t)*<Gompertz income coefficient, freight of trp.own[f,all]>/Thousand)),trjhf[f,s](t-1))`

**E848. `trjif`: Actual ownership in the last data year, freight (held)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy I4787 / I4903 (B3)
- Rows: all,fre
  - 2022-2041: `trjif(t) = IF(tr.dk[f,all](t)=1,trownfe[bev,s](t)+trownf[ice,s](t),trjif[f,s](t-1))`

**E849. `trjjf`: Ownership calibration factor actual / expected, freight (held; fix B3: both ways)** (factor)

- Description: Calculation
- Legacy: legacy J4787 / J4903 (B3)
- Rows: all,fre
  - 2022-2041: `trjjf(t) = IF(tr.dk[f,all](t)=1,trjif[f,s](t)/trjhf[f,s](t),trjjf[f,s](t-1))`

**E850. `trsatp`: Ownership saturation point (data; held after)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4781, 4897
- Rows: all,pas
  - 2022-2041: `trsatp(t) = IF(tr.dk[f,all](t)=1,trsat[f,all](t),trsatp[f,s](t-1))`

**E851. `trsatq`: Saturation point, passenger and light (x (1 - freight share))** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4783
- Rows: all,pas
  - 2022-2041: `trsatq(t) = trsatp[f,s](t)*(1-trfsh[f,fre](t))`

**E852. `trgtp`: Gompertz ownership target x calibration, passenger and light** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4786 (Gompertz term)
- Rows: all,pas
  - 2022-2041: `trgtp(t) = trsatq[f,s](t)*EXP(<Gompertz constant of trp.ogr[f,all]>*EXP(trgpc[f,all](t)*<Gompertz income coefficient, passenger of trp.own[f,all]>/Thousand))*N(trjjp[f,s](t-1))`

**E853. `trdemp`: Ownership demand with partial adjustment, passenger and light** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4786
- Rows: all,pas
  - 2022-2041: `trdemp(t) = IF(N(trstd[ice,s](t))>0,N(trstd[ice,s](t))+N(trstd[bev,s](t)),<adjustment speed, passenger of trp.own[f,all]>*trgtp[f,s](t)+(1-<adjustment speed, passenger of trp.own[f,all]>)*N(trdmcp[f,s](t-1)))`

**E854. `trdmcp`: Ownership, passenger and light (growth and decline limits; fix B4)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4787
- Rows: all,pas
  - 2022-2041: `trdmcp(t) = IF(N(trstd[ice,s](t))>0,N(trstd[ice,s](t))+N(trstd[bev,s](t)),MAX(N(trdmcp[f,s](t-1))*(1-<passenger (TrOwnDecline) of trp.odc[f,all]>),MIN(N(trdmcp[f,s](t-1))*(1+<maximum growth, passenger of trp.ogr[f,all]>),trdemp[f,s](t))))`

**E855. `trbyt`: Purchases, passenger and light (ownership - stock after retirement)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4789
- Rows: all,pas
  - 2022-2041: `trbyt(t) = trdmcp[f,s](t)-trafts[f,s](t)`

**E856. `trbytn`: Purchases of new passenger vehicles** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4790
- Rows: all,pas
  - 2022-2041: `trbytn(t) = trbyt[f,s](t)*(1-trush[f,s](t))`

**E857. `trbytu`: Purchases of used passenger vehicles** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4791
- Rows: all,pau
  - 2022-2041: `trbytu(t) = trbyt[f,pas](t)-trbytn[f,pas](t)`

**E858. `trtcav`: Average TCO per km, new passenger (weighted by last year's ICE share)** (USD/km)

- Description: Calculation
- Legacy: legacy row 4799
- Rows: all,pas
  - 2022-2041: `trtcav(t) = tricl[ice,s](t)*trpkpin[ice,s](t)+(1-tricl[ice,s](t))*trpkpbn[bev,s](t)`

**E859. `trlgn`: ICE share of new passenger purchases, calculated (logit)** (share)

- Description: Calculation
- Legacy: legacy row 4802
- Rows: ice,pas
  - 2022-2041: `trlgn(t) = 1/(1+EXP(-<passenger of trp.k[all,all]>*(trpkpbn[bev,s](t)-trpkpin[f,s](t))/trtcav[all,s](t)))`

**E860. `trlgnb`: EV share of new passenger purchases, calculated** (share)

- Description: Calculation
- Legacy: legacy row 4803
- Rows: bev,pas
  - 2022-2041: `trlgnb(t) = 1-trlgn[ice,s](t)`

**E861. `trevac`: BEV share of passenger purchases, actual (data years)** (share)

- Description: Calculation
- Legacy: legacy row 4805
- Rows: bev,pas
  - 2022-2041: `trevac(t) = IF(tr.dk[all,all](t)=1,trevpm[f,s](t),"")`

**E862. `trshn`: ICE share of new passenger purchases (actual in data years)** (share)

- Description: Calculation
- Legacy: legacy row 4806
- Rows: ice,pas
  - 2022-2041: `trshn(t) = IF(ISNUMBER(trevac[bev,s](t)),1-trevac[bev,s](t),trlgn[f,s](t))`

**E863. `trshnb`: BEV share of new passenger purchases** (share)

- Description: Calculation
- Legacy: legacy row 4807
- Rows: bev,pas
  - 2022-2041: `trshnb(t) = 1-trshn[ice,s](t)`

**E864. `trtcau`: Average TCO per km, used passenger (weighted by last year's ICE share)** (USD/km)

- Description: Calculation
- Legacy: legacy row 4813
- Rows: all,pau
  - 2022: `trtcau(t) = tricl[ice,pas](t)*trpkpiu[ice,s](t)+(1-tricl[ice,pas](t))*trpkpbu[bev,s](t)`
  - 2023-2041: `trtcau(t) = triclu[ice,s](t)*trpkpiu[ice,s](t)+(1-triclu[ice,s](t))*trpkpbu[bev,s](t)`

**E865. `trlgu`: ICE share of used passenger purchases, calculated (logit)** (share)

- Description: Calculation
- Legacy: legacy row 4816
- Rows: ice,pau
  - 2022-2041: `trlgu(t) = 1/(1+EXP(-<passenger of trp.k[all,all]>*(trpkpbu[bev,s](t)-trpkpiu[f,s](t))/trtcau[all,s](t)))`

**E866. `trlgub`: EV share of used passenger purchases, calculated** (share)

- Description: Calculation
- Legacy: legacy row 4817
- Rows: bev,pau
  - 2022-2041: `trlgub(t) = 1-trlgu[ice,s](t)`

**E867. `trshu`: ICE share of used passenger purchases (actual in data years)** (share)

- Description: Calculation
- Legacy: legacy row 4819
- Rows: ice,pau
  - 2022-2041: `trshu(t) = IF(ISNUMBER(trevac[bev,pas](t)),1-trevac[bev,pas](t),trlgu[f,s](t))`

**E868. `trshub`: BEV share of used passenger purchases** (share)

- Description: Calculation
- Legacy: legacy row 4820
- Rows: bev,pau
  - 2022-2041: `trshub(t) = 1-trshu[ice,s](t)`

**E869. `trevcc`: EV share of passenger purchases, calculated (new and used)** (share)

- Description: Calculation
- Legacy: legacy row 4827
- Rows: ev,pas
  - 2022-2041: `trevcc(t) = trush[all,s](t)*trlgub[bev,pau](t)+(1-trush[all,s](t))*trlgnb[bev,s](t)`

**E870. `trevsh`: EV share of passenger purchases (actual where data, else calculated)** (share)

- Description: Calculation
- Legacy: legacy row 4828
- Rows: ev,pas
  - 2022-2041: `trevsh(t) = IF(N(trevac[bev,s](t))>0,trevac[bev,s](t),trevcc[f,s](t))`

**E871. `trtrn`: Share of the stock bought new each year, passenger (1 / weighted life)** (share)

- Description: Calculation
- Legacy: legacy row 4831
- Rows: all,pas
  - 2022-2041: `trtrn(t) = 1/(trush[f,s](t)*<ownership years, new passenger of trp.life[f,all]>+<useful life, passenger of trp.life[f,all]>*(1-trush[f,s](t)))`

**E872. `trnwbn`: Share of this year's BEV purchases in the closing BEV stock (pas)** (share)

- Description: Calculation
- Legacy: legacy row 4832
- Rows: bev,pas
  - 2022-2041: `trnwbn(t) = IF((trclon[f,s](t)+trclou[f,pau](t))=0,0,(trclon[f,s](t)-traftn[f,s](t))/(trclon[f,s](t)+trclou[f,pau](t)))`

**E873. `trnwbu`: Share of this year's BEV purchases in the closing BEV stock (pau)** (share)

- Description: Calculation
- Legacy: legacy row 4833
- Rows: bev,pau
  - 2022-2041: `trnwbu(t) = IF((trclon[f,pas](t)+trclou[f,s](t))=0,0,(trclou[f,s](t)-traftu[f,s](t))/(trclon[f,pas](t)+trclou[f,s](t)))`

**E874. `trics`: ICE fuel shares of passenger purchases, data years** (share)

- Description: Calculation
- Legacy: legacy rows 4835-4839
- Rows: gso,pas, die,pas, lpg,pas, nga,pas
  - 2022-2041: `trics(t) = IF(tr.dk[all,all](t)=1,trvsh[f,s](t),"")`
- Rows: phv,pas
  - 2022-2041: `trics(t) = IF(tr.dk[all,all](t)=1,trphvs[f,s](t),"")`

**E875. `trtcr`: Change in TCO by ICE fuel (ratio to last year)** (ratio)

- Description: Calculation
- Legacy: legacy rows 4840-4844
- Rows: gso,pas, die,pas, lpg,pas, nga,pas
  - 2022: `trtcr(t) = ""`
  - 2023-2041: `trtcr(t) = trtcf[f,s](t)/trtcf[f,s](t-1)`
- Rows: phv,pas
  - 2022: `trtcr(t) = ""`
  - 2023-2041: `trtcr(t) = trtcfp[f,s](t)/trtcfp[f,s](t-1)`

**E876. `tricd`: ICE fuel shares of passenger purchases in the data years (scaled to the ICE total; fix B9)** (share)

- Description: Calculation
- Legacy: legacy rows 4846-4849 (data years)
- Rows: gso,pas, die,pas, lpg,pas, nga,pas
  - 2022-2041: `tricd(t) = IF(tr.dk[all,all](t)=1,trics[f,s](t)/SUM(trics[4 rows](t))*(1-trevac[bev,s](t)-tricdp[phv,s](t)),"")`

**E877. `tricdp`: PHEV share of passenger purchases in the data years ((EV - BEV share) x passenger share; fix B9)** (share)

- Description: Calculation
- Legacy: legacy row 4850 (data years)
- Rows: phv,pas
  - 2022-2041: `tricdp(t) = IF(tr.dk[all,all](t)=1,MAX(0,trevp[ev,s](t)-trevp[bev,s](t))*trsps[all,s](t),"")`

**E878. `trcrs`: Weighted change in the TCO of the other ICE fuels (cross term)** (ratio)

- Description: Calculation
- Legacy: legacy rows 4846-4850
- Rows: gso,pas, die,pas, lpg,pas, nga,pas, phv,pas
  - 2022: `trcrs(t) = ""`
  - 2023-2041: `trcrs(t) = IFERROR((SUMPRODUCT(tricp[5 rows](t-1),trtcr[5 rows](t))-tricp[f,s](t-1)*trtcr[f,s](t))/(SUM(tricp[5 rows](t-1))-tricp[f,s](t-1)),"")`

**E879. `tricp`: ICE fuel shares of passenger purchases before scaling (own and cross TCO elasticities)** (share)

- Description: Calculation
- Legacy: legacy rows 4846-4850
- Rows: gso,pas, die,pas, lpg,pas, nga,pas
  - 2022-2041: `tricp(t) = IF(ISNUMBER(tricd[f,s](t)),tricd[f,s](t),IF(ISNUMBER(trcrs[f,s](t)),N(tricp[f,s](t-1))*trtcr[f,s](t)^<own-TCO elasticity of trp.ice[all,all]>*trcrs[f,s](t)^<cross-TCO elasticity of trp.ice[all,all]>,N(tricp[f,s](t-1))))`
- Rows: phv,pas
  - 2022-2041: `tricp(t) = IF(ISNUMBER(tricdp[f,s](t)),tricdp[f,s](t),IF(ISNUMBER(trcrs[f,s](t)),N(tricp[f,s](t-1))*trtcr[f,s](t)^<own-TCO elasticity of trp.ice[all,all]>*trcrs[f,s](t)^<cross-TCO elasticity of trp.ice[all,all]>,N(tricp[f,s](t-1))))`

**E880. `tricn`: ICE fuel shares of passenger purchases (scaled to 1 - EV share)** (share)

- Description: Calculation
- Legacy: legacy rows 4851-4855
- Rows: gso,pas, die,pas, lpg,pas, nga,pas, phv,pas
  - 2022-2041: `tricn(t) = IF(ISNUMBER(trics[f,s](t)),tricp[f,s](t),tricp[f,s](t)/SUM(tricp[5 rows](t))*(1-trevsh[ev,s](t)))`

**E881. `trico`: ICE fuel shares of the passenger stock (moving average over the ownership years)** (share)

- Description: Calculation
- Legacy: legacy rows 4856-4860
- Rows: gso,pas, die,pas, lpg,pas, nga,pas, phv,pas
  - 2022-2041: `trico(t) = IF(ISNUMBER(trics[f,s](t)),trics[f,s](t),N(trico[f,s](t-1))*(trowny[all,s](t)-1)/trowny[all,s](t)+tricn[f,s](t)/trowny[all,s](t))`

**E882. `tricw`: ICE fuel shares of the passenger stock incl. EVs** (share)

- Description: Calculation
- Legacy: legacy rows 4861-4865
- Rows: gso,pas, die,pas, lpg,pas, nga,pas, phv,pas
  - 2022-2041: `tricw(t) = trico[f,s](t)/(SUM(trico[5 rows](t))+trevst[ev,s](t))`

**E883. `trveh`: Passenger and light ICEVs by fuel** (million)

- Description: Calculation
- Legacy: legacy rows 4867-4871
- Rows: gso,pas, die,pas, lpg,pas, nga,pas, phv,pas
  - 2022-2041: `trveh(t) = (trstt[all,s](t)*tricw[f,s](t))*trpop[all,all](t)/Thousand`

**E884. `trvehb`: Passenger and light BEVs** (million)

- Description: Calculation
- Legacy: legacy row 4872
- Rows: bev,pas
  - 2022-2041: `trvehb(t) = (trclon[f,s](t)+trclou[f,pau](t))*trpop[all,all](t)/Thousand`

**E885. `trsatf`: Ownership saturation point (data; held after), freight** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4897
- Rows: all,fre
  - 2022-2041: `trsatf(t) = IF(tr.dk[f,all](t)=1,trsat[f,all](t),trsatf[f,s](t-1))`

**E886. `trsatg`: Saturation point, freight (x freight share)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4899
- Rows: all,fre
  - 2022-2041: `trsatg(t) = trsatf[f,s](t)*trfsh[f,s](t)`

**E887. `trgtf`: Gompertz ownership target x calibration, freight** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4902 (Gompertz term)
- Rows: all,fre
  - 2022-2041: `trgtf(t) = trsatg[f,s](t)*EXP(<Gompertz constant of trp.ogr[f,all]>*EXP(trgpc[f,all](t)*<Gompertz income coefficient, freight of trp.own[f,all]>/Thousand))*N(trjjf[f,s](t-1))`

**E888. `trdemf`: Ownership demand with partial adjustment, freight** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4902
- Rows: all,fre
  - 2022-2041: `trdemf(t) = IF(N(trstdf[ice,s](t))>0,N(trstdf[ice,s](t))+N(trstdf[bev,s](t)),<adjustment speed, freight of trp.own[f,all]>*trgtf[f,s](t)+(1-<adjustment speed, freight of trp.own[f,all]>)*N(trdmcf[f,s](t-1)))`

**E889. `trdmcf`: Ownership, freight (growth and decline limits; fix B4)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4903
- Rows: all,fre
  - 2022-2041: `trdmcf(t) = IF(N(trstdf[ice,s](t))>0,N(trstdf[ice,s](t))+N(trstdf[bev,s](t)),MAX(N(trdmcf[f,s](t-1))*(1-<freight (TrOwnDecline) of trp.odc[f,all]>),MIN(N(trdmcf[f,s](t-1))*(1+<maximum growth, freight of trp.ogr[f,all]>),trdemf[f,s](t))))`

**E890. `trbytf`: Purchases, freight** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4905
- Rows: all,fre
  - 2022-2041: `trbytf(t) = trdmcf[f,s](t)-traftsf[f,s](t)`

**E891. `trtcaf`: Average TCO per km, freight (weighted by last year's ICE share)** (USD/km)

- Description: Calculation
- Legacy: legacy row 4910
- Rows: all,fre
  - 2022-2041: `trtcaf(t) = triclf[ice,s](t)*trpkfin[ice,s](t)+(1-triclf[ice,s](t))*trpkfbn[bev,s](t)`

**E892. `trlgf`: ICE share of freight purchases, calculated (logit)** (share)

- Description: Calculation
- Legacy: legacy row 4913
- Rows: ice,fre
  - 2022-2041: `trlgf(t) = 1/(1+EXP(-<freight of trp.k[all,all]>*(trpkfbn[bev,s](t)-trpkfin[f,s](t))/trtcaf[all,s](t)))`

**E893. `trlgfb`: BEV share of freight purchases, calculated** (share)

- Description: Calculation
- Legacy: legacy row 4914
- Rows: bev,fre
  - 2022-2041: `trlgfb(t) = 1-trlgf[ice,s](t)`

**E894. `trevaf`: BEV share of freight purchases, actual (data years)** (share)

- Description: Calculation
- Legacy: legacy row 4916
- Rows: bev,fre
  - 2022-2041: `trevaf(t) = IF(tr.dk[all,all](t)=1,trevp[f,s](t),"")`

**E895. `trshfi`: ICE share of freight purchases (actual in data years)** (share)

- Description: Calculation
- Legacy: legacy row 4917
- Rows: ice,fre
  - 2022-2041: `trshfi(t) = IF(ISNUMBER(trevaf[bev,s](t)),1-trevaf[bev,s](t),trlgf[f,s](t))`

**E896. `trshfb`: BEV share of freight purchases** (share)

- Description: Calculation
- Legacy: legacy row 4918
- Rows: bev,fre
  - 2022-2041: `trshfb(t) = 1-trshfi[ice,s](t)`

**E897. `trnwf`: Share of this year's purchases in the closing BEV freight stock** (share)

- Description: Calculation
- Legacy: legacy row 4927
- Rows: bev,fre
  - 2022-2041: `trnwf(t) = IF(trclof[f,s](t)=0,0,(trclof[f,s](t)-traftf[f,s](t))/trclof[f,s](t))`

**E898. `tricsf`: ICE fuel shares of freight purchases, data years** (share)

- Description: Calculation
- Legacy: legacy rows 4929-4931
- Rows: die,fre
  - 2022-2041: `tricsf(t) = IF(tr.dk[all,all](t)=1,trvsf1[f,s](t),"")`
- Rows: lpg,fre, nga,fre
  - 2022-2041: `tricsf(t) = IF(tr.dk[all,all](t)=1,trvsf[f,s](t),"")`

**E899. `trtcrf`: Change in freight TCO by ICE fuel (ratio to last year)** (ratio)

- Description: Calculation
- Legacy: legacy rows 4932-4934
- Rows: die,fre, lpg,fre, nga,fre
  - 2022: `trtcrf(t) = ""`
  - 2023-2041: `trtcrf(t) = trtcff[f,s](t)/trtcff[f,s](t-1)`

**E900. `trcrsf`: Weighted change in the TCO of the other freight fuels (cross term; blank if they have no share)** (ratio)

- Description: Calculation
- Legacy: legacy rows 4936-4938
- Rows: die,fre, lpg,fre, nga,fre
  - 2022: `trcrsf(t) = ""`
  - 2023-2041: `trcrsf(t) = IFERROR((SUMPRODUCT(tricpf[3 rows](t-1),trtcrf[3 rows](t))-tricpf[f,s](t-1)*trtcrf[f,s](t))/(SUM(tricpf[3 rows](t-1))-tricpf[f,s](t-1)),"")`

**E901. `tricpf`: ICE fuel shares of freight purchases before scaling** (share)

- Description: Calculation
- Legacy: legacy rows 4936-4938
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `tricpf(t) = IF(ISNUMBER(tricsf[f,s](t)),tricsf[f,s](t),IF(ISNUMBER(trcrsf[f,s](t)),N(tricpf[f,s](t-1))*trtcrf[f,s](t)^<own-TCO elasticity of trp.ice[all,all]>*trcrsf[f,s](t)^<cross-TCO elasticity of trp.ice[all,all]>,N(tricpf[f,s](t-1))))`

**E902. `tricnf`: ICE fuel shares of freight purchases (scaled to 1 - EV share)** (share)

- Description: Calculation
- Legacy: legacy rows 4939-4941
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `tricnf(t) = IF(ISNUMBER(tricsf[f,s](t)),tricpf[f,s](t),tricpf[f,s](t)/SUM(tricpf[3 rows](t))*(1-trshfb[bev,s](t)))`

**E903. `tricof`: ICE fuel shares of the freight stock (moving average over the life)** (share)

- Description: Calculation
- Legacy: legacy rows 4942-4944
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `tricof(t) = IF(ISNUMBER(tricsf[f,s](t)),tricsf[f,s](t),N(tricof[f,s](t-1))*(<useful life, freight of trp.life[all,all]>-1)/<useful life, freight of trp.life[all,all]>+tricnf[f,s](t)/<useful life, freight of trp.life[all,all]>)`

**E904. `tricwf`: ICE fuel shares of the freight stock incl. BEVs** (share)

- Description: Calculation
- Legacy: legacy rows 4945-4947
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `tricwf(t) = tricof[f,s](t)/(SUM(tricof[3 rows](t))+trevsf[bev,s](t))`

**E905. `trvehf`: ICE freight vehicles by fuel** (million)

- Description: Calculation
- Legacy: legacy rows 4949-4951
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trvehf(t) = ((trclof[ice,s](t)+trclof[bev,s](t))*tricwf[f,s](t))*trpop[all,all](t)/Thousand`

**E906. `trvehfb`: BEV freight vehicles** (million)

- Description: Calculation
- Legacy: legacy row 4952
- Rows: bev,fre
  - 2022-2041: `trvehfb(t) = trclof[f,s](t)*trpop[all,all](t)/Thousand`

**E907. `trdmcc`: Ownership, 2-3 wheelers (data; then the income hump within the growth and decline limits)** (per 1,000 people)

- Description: Calculation
- Legacy: legacy rows 4978, 4979
- Rows: all,cyc
  - 2022-2041: `trdmcc(t) = IF(N(trstdc[ice,s](t))>0,N(trstdc[ice,s](t))+N(trstdc[bev,s](t)),MAX(N(trdmcc[f,s](t-1))*(1-<2-3 wheeler of trp.odc[f,all]>),MIN(N(trdmcc[f,s](t-1))*(1+<maximum growth, 2-3 wheeler of trp.ogr[f,all]>),trcyh[f,s](t))))`

**E908. `trbytc`: Purchases, 2-3 wheelers** (per 1,000 people)

- Description: Calculation
- Legacy: legacy row 4981
- Rows: all,cyc
  - 2022-2041: `trbytc(t) = trdmcc[f,s](t)-traftsc[f,s](t)`

**E909. `trtcac`: Average TCO per km, 2-3 wheelers (weighted by last year's ICE share)** (USD/km)

- Description: Calculation
- Legacy: legacy row 4986
- Rows: all,cyc
  - 2022-2041: `trtcac(t) = triclc[ice,s](t)*trpkcin[ice,s](t)+(1-triclc[ice,s](t))*trpkcbn[bev,s](t)`

**E910. `trlgc`: ICE share of 2-3 wheeler purchases, calculated (logit)** (share)

- Description: Calculation
- Legacy: legacy row 4989
- Rows: ice,cyc
  - 2022-2041: `trlgc(t) = 1/(1+EXP(-<2-3 wheeler of trp.k[all,all]>*(trpkcbn[bev,s](t)-trpkcin[f,s](t))/trtcac[all,s](t)))`

**E911. `trlgcb`: BEV share of 2-3 wheeler purchases, calculated** (share)

- Description: Calculation
- Legacy: legacy row 4990
- Rows: bev,cyc
  - 2022-2041: `trlgcb(t) = 1-trlgc[ice,s](t)`

**E912. `trevacc`: BEV share of 2-3 wheeler purchases, actual (data years)** (share)

- Description: Calculation
- Legacy: legacy row 4992
- Rows: bev,cyc
  - 2022-2041: `trevacc(t) = IF(tr.dk[all,all](t)=1,trevp[f,s](t),"")`

**E913. `trshc`: ICE share of 2-3 wheeler purchases (actual in data years)** (share)

- Description: Calculation
- Legacy: legacy row 4993
- Rows: ice,cyc
  - 2022-2041: `trshc(t) = IF(ISNUMBER(trevacc[bev,s](t)),1-trevacc[bev,s](t),trlgc[f,s](t))`

**E914. `trshcb`: BEV share of 2-3 wheeler purchases** (share)

- Description: Calculation
- Legacy: legacy row 4994
- Rows: bev,cyc
  - 2022-2041: `trshcb(t) = 1-trshc[ice,s](t)`

**E915. `trnwc`: Share of this year's purchases in the closing BEV 2-3 wheeler stock** (share)

- Description: Calculation
- Legacy: legacy row 5003
- Rows: bev,cyc
  - 2022-2041: `trnwc(t) = IF(trcloc[f,s](t)=0,0,(trcloc[f,s](t)-traftc[f,s](t))/trcloc[f,s](t))`

**E916. `trvehc`: 2-3 wheelers (ICE, BEV)** (million)

- Description: Calculation
- Legacy: legacy rows 5006, 5007
- Rows: ice,cyc, bev,cyc
  - 2022-2041: `trvehc(t) = trcloc[f,s](t)*trpop[all,all](t)/Thousand`

**E917. `trfso`: Fuel economy of the passenger stock, opening (data years: data)** (km/l)

- Description: Calculation
- Legacy: legacy rows 5017-5029
- Rows: gso,pas, die,pas
  - 2022-2041: `trfso(t) = IF(ISNUMBER(trfem[f,s](t)),trfem[f,s](t),N(trfsc[f,s](t-1)))`
- Rows: lpg,pas, nga,pas
  - 2022-2041: `trfso(t) = IF(ISNUMBER(trfem2[f,s](t)),trfem2[f,s](t),N(trfsc[f,s](t-1)))`

**E918. `trfsop`: Fuel economy of the PHEV stock, opening** (km/l)

- Description: Calculation
- Legacy: legacy row 5033
- Rows: phv,pas
  - 2022-2041: `trfsop(t) = IF(ISNUMBER(trfe[f,s](t)),trfe[f,s](t),N(trfscp[f,s](t-1)))`

**E919. `trfsc`: Fuel economy of the passenger stock, closing** (km/l)

- Description: Calculation
- Legacy: legacy rows 5019-5031
- Rows: gso,pas, die,pas
  - 2022-2041: `trfsc(t) = IF(ISNUMBER(trfem[f,s](t)),trfem[f,s](t),trfn[f,s](t)*trtrn[all,s](t)+trfso[f,s](t)*(1-trtrn[all,s](t)))`
- Rows: lpg,pas, nga,pas
  - 2022-2041: `trfsc(t) = IF(ISNUMBER(trfem2[f,s](t)),trfem2[f,s](t),trfn[f,s](t)*trtrn[all,s](t)+trfso[f,s](t)*(1-trtrn[all,s](t)))`

**E920. `trfscp`: Fuel economy of the PHEV stock, closing** (km/l)

- Description: Calculation
- Legacy: legacy row 5035
- Rows: phv,pas
  - 2022-2041: `trfscp(t) = IF(ISNUMBER(trfe[f,s](t)),trfe[f,s](t),trfnp[f,s](t)*trtrn[all,s](t)+trfsop[f,s](t)*(1-trtrn[all,s](t)))`

**E921. `trcks`: Cost per km of the passenger stock by fuel** (USD/km)

- Description: Calculation
- Legacy: legacy rows 5040-5060
- Rows: gso,pas, die,pas, lpg,pas
  - 2022-2041: `trcks(t) = trprl[f,rod](t)/trfso[f,s](t)+trdtxp[all,s](t)`
- Rows: nga,pas
  - 2022-2041: `trcks(t) = trprg[f,rod](t)/trfso[f,s](t)+trdtxp[all,s](t)`
- Rows: phv,pas
  - 2022-2041: `trcks(t) = trpphv[f,s](t)/trfsop[f,s](t)+trdtxp[all,s](t)`

**E922. `trcksr`: Change in the cost per km of the passenger stock (ratio to last year)** (ratio)

- Description: Calculation
- Legacy: legacy rows 5041-5061
- Rows: gso,pas, die,pas, lpg,pas, nga,pas, phv,pas
  - 2022: `trcksr(t) = ""`
  - 2023-2041: `trcksr(t) = trcks[f,s](t)/trcks[f,s](t-1)`

**E923. `trgpcr`: Change in GDP per capita (ratio to last year)** (ratio)

- Description: Calculation
- Legacy: legacy rows 5064, 5125, 5158
- Rows: all,all
  - 2022: `trgpcr(t) = ""`
  - 2023-2041: `trgpcr(t) = trgpc[f,s](t)/trgpc[f,s](t-1)`

**E924. `trvku0`: Distance per passenger vehicle by fuel, uncalibrated (data; then cost per km and income)** (km)

- Description: Calculation
- Legacy: legacy rows 5067-5071
- Rows: gso,pas, die,pas, lpg,pas, nga,pas, phv,pas
  - 2022-2041: `trvku0(t) = IF(ISNUMBER(trvkm[all,s](t)),trvkm[all,s](t)*1,N(trvku0[f,s](t-1))*trcksr[f,s](t)^<usage, gasoline of trp.ela[all,all]>*trgpcr[all,all](t)^<passenger of trp.inc[all,all]>)`

**E925. `trbkm0`: Distance driven by fuel, passenger, uncalibrated** (bln km)

- Description: Calculation
- Legacy: legacy rows 5079-5083
- Rows: gso,pas, die,pas, lpg,pas, nga,pas, phv,pas
  - 2022-2041: `trbkm0(t) = trveh[f,s](t)*trvku0[f,s](t)/Thousand`

**E926. `trfu0g`: Gasoline use, passenger incl. PHEVs, uncalibrated** (bln liters)

- Description: Calculation
- Legacy: legacy row 5085
- Rows: gso,pas
  - 2022-2041: `trfu0g(t) = trbkm0[f,s](t)/trfsc[f,s](t)+trbkm0[phv,s](t)/trfscp[phv,s](t)`

**E927. `trfu0`: Fuel use, passenger, uncalibrated** (bln liters)

- Description: Calculation
- Legacy: legacy rows 5086-5088
- Rows: die,pas, lpg,pas, nga,pas
  - 2022-2041: `trfu0(t) = trbkm0[f,s](t)/trfsc[f,s](t)`

**E928. `trfsof`: Fuel economy of the freight stock, opening** (km/l)

- Description: Calculation
- Legacy: legacy rows 5096, 5100, 5104
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trfsof(t) = IF(ISNUMBER(trfe[f,s](t)),trfe[f,s](t),N(trfscf[f,s](t-1)))`

**E929. `trfscf`: Fuel economy of the freight stock, closing (1/life bought new)** (km/l)

- Description: Calculation
- Legacy: legacy rows 5098, 5102, 5106
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trfscf(t) = IF(ISNUMBER(trfe[f,s](t)),trfe[f,s](t),trfnf[f,s](t)*(1/<useful life, freight of trp.life[all,all]>)+trfsof[f,s](t)*(1-(1/<useful life, freight of trp.life[all,all]>)))`

**E930. `trcksf`: Cost per km of the freight stock by fuel** (USD/km)

- Description: Calculation
- Legacy: legacy rows 5111, 5116, 5121
- Rows: die,fre, lpg,fre
  - 2022-2041: `trcksf(t) = trprn[f,rod](t)/trfsof[f,s](t)+trdtxf[all,s](t)`
- Rows: nga,fre
  - 2022-2041: `trcksf(t) = trprm[f,s](t)/trfsof[f,s](t)+trdtxf[all,s](t)`

**E931. `trcksfr`: Change in the cost per km of the freight stock (ratio to last year)** (ratio)

- Description: Calculation
- Legacy: legacy rows 5112, 5117, 5122
- Rows: die,fre, lpg,fre, nga,fre
  - 2022: `trcksfr(t) = ""`
  - 2023-2041: `trcksfr(t) = trcksf[f,s](t)/trcksf[f,s](t-1)`

**E932. `trvku0f`: Distance per freight vehicle by fuel, uncalibrated** (km)

- Description: Calculation
- Legacy: legacy rows 5127-5129
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trvku0f(t) = IF(ISNUMBER(trvkfd[all,s](t)),trvkfd[all,s](t)*1,N(trvku0f[f,s](t-1))*trcksfr[f,s](t)^<usage, diesel of trp.ela[all,all]>*trgpcr[all,all](t)^<freight of trp.inc[all,all]>)`

**E933. `trbkm0f`: Distance driven by fuel, freight, uncalibrated** (bln km)

- Description: Calculation
- Legacy: legacy rows 5135-5137
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trbkm0f(t) = trvehf[f,s](t)*trvku0f[f,s](t)/Thousand`

**E934. `trfsoc`: Fuel economy of the 2-3 wheeler stock, opening** (km/l)

- Description: Calculation
- Legacy: legacy row 5147
- Rows: gso,cyc
  - 2022-2041: `trfsoc(t) = IF(ISNUMBER(trfe[f,s](t)),trfe[f,s](t),N(trfscc[f,s](t-1)))`

**E935. `trfscc`: Fuel economy of the 2-3 wheeler stock, closing** (km/l)

- Description: Calculation
- Legacy: legacy row 5149
- Rows: gso,cyc
  - 2022-2041: `trfscc(t) = IF(ISNUMBER(trfe[f,s](t)),trfe[f,s](t),trfnc[f,s](t)*(1/<useful life, 2-3 wheeler of trp.life[all,all]>)+trfsoc[f,s](t)*(1-(1/<useful life, 2-3 wheeler of trp.life[all,all]>)))`

**E936. `trcksc`: Cost per km of the 2-3 wheeler stock** (USD/km)

- Description: Calculation
- Legacy: legacy row 5154
- Rows: gso,cyc
  - 2022-2041: `trcksc(t) = trprl[f,rod](t)/trfsoc[f,s](t)+trdtxc[all,s](t)`

**E937. `trckscr`: Change in the cost per km of the 2-3 wheeler stock** (ratio)

- Description: Calculation
- Legacy: legacy row 5155
- Rows: gso,cyc
  - 2022: `trckscr(t) = ""`
  - 2023-2041: `trckscr(t) = trcksc[f,s](t)/trcksc[f,s](t-1)`

**E938. `trvku0c`: Distance per 2-3 wheeler, uncalibrated** (km)

- Description: Calculation
- Legacy: legacy row 5161
- Rows: gso,cyc
  - 2022-2041: `trvku0c(t) = IF(ISNUMBER(trvkd[all,s](t)),trvkd[all,s](t)*1,N(trvku0c[f,s](t-1))*trckscr[f,s](t)^<usage, gasoline of trp.ela[all,all]>*trgpcr[all,all](t)^<2-3 wheeler of trp.inc[all,all]>)`

**E939. `trbkm0c`: Distance driven, 2-3 wheelers, uncalibrated** (bln km)

- Description: Calculation
- Legacy: legacy row 5165
- Rows: gso,cyc
  - 2022-2041: `trbkm0c(t) = trvehc[ice,s](t)*trvku0c[f,s](t)/Thousand`

**E940. `trfu0c`: Gasoline use, 2-3 wheelers, uncalibrated** (bln liters)

- Description: Calculation
- Legacy: legacy row 5167
- Rows: gso,cyc
  - 2022-2041: `trfu0c(t) = trbkm0c[f,s](t)/trfscc[f,s](t)`

**E941. `trfu0f`: Fuel use, freight, uncalibrated** (bln liters)

- Description: Calculation
- Legacy: legacy rows 5139-5141
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trfu0f(t) = trbkm0f[f,s](t)/trfscf[f,s](t)`

**E942. `trbu`: Bottom-up road fuel use of the base year incl. buses (held)** (ktoe)

- Description: Calculation (base year)
- Legacy: legacy O5170:O5173
- Rows: gso,rod
  - 2022: `trbu(t) = (trfu0g[f,pas](t)+trfu0c[f,cyc](t))/<liters per ktoe>*Billion/(1-<bus share>)`
  - 2023-2041: `trbu(t) = trbu[f,s](t-1)`
  - Parameters: `<liters per ktoe>` = `<Gasoline of trp.lpk[all,all]>`
- Rows: die,rod, lpg,rod, nga,rod
  - 2022: `trbu(t) = (trfu0[f,pas](t)+trfu0f[f,fre](t))/<liters per ktoe>*Billion/(1-<bus share>)`
  - 2023-2041: `trbu(t) = trbu[f,s](t-1)`
  - Parameters: `<liters per ktoe>` = `<Diesel of trp.lpk[all,all]>`; `<bus share>` = `<share of trp.bsh[f,bus]>`

**E943. `trcq`: Calibration factor step 1 by fuel: energy balance / bottom-up (1 without either; held)** (factor)

- Description: Calculation (base year)
- Legacy: legacy Q5170:Q5173
- Rows: gso,rod, die,rod, lpg,rod, nga,rod
  - 2022: `trcq(t) = IF(OR(trbu[f,s](t)=0,<energy balance (ktoe)>=0),1,<energy balance (ktoe)>/trbu[f,s](t))`
  - 2023-2041: `trcq(t) = trcq[f,s](t-1)`
  - Parameters: `<energy balance (ktoe)>` = `<Gasoline of trp.eb[all,all]>`

**E944. `trdfp`: Distance factor, passenger and light (fuel-use weighted step-1 factors; held)** (factor)

- Description: Calculation (base year)
- Legacy: legacy U5170 = G5177
- Rows: all,pas
  - 2022: `trdfp(t) = SUMPRODUCT(block@trfu0g{trfu0g, trfu0}(t),trcq[4 rows](t))/SUM(block@trfu0g{trfu0g, trfu0}(t))`
  - 2023-2041: `trdfp(t) = trdfp[f,s](t-1)`

**E945. `trdff`: Distance factor, freight (fuel-use weighted step-1 factors; held)** (factor)

- Description: Calculation (base year)
- Legacy: legacy V5170 = G5231
- Rows: all,fre
  - 2022: `trdff(t) = SUMPRODUCT(trfu0f[3 rows](t),trcq[3 rows](t))/SUM(trfu0f[3 rows](t))`
  - 2023-2041: `trdff(t) = trdff[f,s](t-1)`

**E946. `trdfc`: Distance factor, 2-3 wheelers (gasoline step-1 factor; held)** (factor)

- Description: Calculation (base year)
- Legacy: legacy W5170 = G5273
- Rows: all,cyc
  - 2022: `trdfc(t) = trcq[gso,rod](t)`
  - 2023-2041: `trdfc(t) = trdfc[f,s](t-1)`

**E947. `trvkc`: Distance per passenger vehicle by fuel, calibrated** (km)

- Description: Calculation
- Legacy: legacy rows 5177-5181
- Rows: gso,pas, die,pas, lpg,pas, nga,pas, phv,pas
  - 2022-2041: `trvkc(t) = IF(ISNUMBER(trvkm[all,s](t)),trvkm[all,s](t)*trdfp[all,s](t),N(trvkc[f,s](t-1))*trcksr[f,s](t)^<usage, gasoline of trp.ela[all,all]>*trgpcr[all,all](t)^<passenger of trp.inc[all,all]>)`

**E948. `trbkm`: Distance driven by fuel, passenger** (bln km)

- Description: Calculation
- Legacy: legacy rows 5189-5193
- Rows: gso,pas, die,pas, lpg,pas, nga,pas, phv,pas
  - 2022-2041: `trbkm(t) = trveh[f,s](t)*trvkc[f,s](t)/Thousand`

**E949. `trfup`: Fuel use, passenger (gasoline incl. PHEVs)** (bln liters)

- Description: Calculation
- Legacy: legacy rows 5195-5198
- Rows: gso,pas
  - 2022-2041: `trfup(t) = trbkm[f,s](t)/trfsc[f,s](t)+trbkm[phv,s](t)/trfscp[phv,s](t)`
  - Parameters: `<EF (tCO2 per liter)>` = `<Gasoline of trp.ef[all,all]>`
- Rows: die,pas, lpg,pas, nga,pas
  - 2022-2041: `trfup(t) = trbkm[f,s](t)/trfsc[f,s](t)`
  - Parameters: `<EF (tCO2 per liter)>` = `<Diesel of trp.ef[all,all]>`

**E950. `trco2p`: CO2 from passenger and light vehicles** (ktCO2)

- Description: Calculation
- Legacy: legacy row 5199
- Rows: all,pas
  - 2022-2041: `trco2p(t) = SUMPRODUCT(trfup[4 rows](t),trfup[4 rows](D))*Thousand`

**E951. `trfebn`: Fuel economy of BEVs bought this year (new and used, by their stock shares)** (km/kWh)

- Description: Calculation
- Legacy: legacy row 5205
- Rows: bev,pas
  - 2022-2041: `trfebn(t) = IF(trnwbn[f,s](t)+trnwbu[f,pau](t)=0,AVERAGE(trfen[f,s](t),trfeub[f,pau](t)),(trfen[f,s](t)*trnwbn[f,s](t)+trfeub[f,pau](t)*trnwbu[f,pau](t))/(trnwbn[f,s](t)+trnwbu[f,pau](t)))`

**E952. `trfebo`: Fuel economy of the BEV stock, opening, passenger** (km/kWh)

- Description: Calculation
- Legacy: legacy row 5207
- Rows: bev,pas
  - 2022-2041: `trfebo(t) = IF(N(trfebs[f,s](t-1))>0,trfebs[f,s](t-1),trfebn[f,s](t))`

**E953. `trfebs`: Fuel economy of the BEV stock, closing, passenger** (km/kWh)

- Description: Calculation
- Legacy: legacy row 5209
- Rows: bev,pas
  - 2022-2041: `trfebs(t) = (trnwbn[f,s](t)+trnwbu[f,pau](t))*trfebn[f,s](t)+(1-(trnwbn[f,s](t)+trnwbu[f,pau](t)))*trfebo[f,s](t)`

**E954. `trckb2`: Cost per km of the BEV stock, passenger** (USD/km)

- Description: Calculation
- Legacy: legacy row 5213
- Rows: bev,pas
  - 2022-2041: `trckb2(t) = trpev[ecy,res](t)/trfebo[f,s](t)+trdtxp[all,s](t)`

**E955. `trckb2r`: Change in the cost per km of the BEV stock, passenger** (ratio)

- Description: Calculation
- Legacy: legacy row 5214
- Rows: bev,pas
  - 2022: `trckb2r(t) = ""`
  - 2023-2041: `trckb2r(t) = trckb2[f,s](t)/trckb2[f,s](t-1)`

**E956. `trvkcb`: Distance per BEV, passenger, calibrated** (km)

- Description: Calculation
- Legacy: legacy row 5217
- Rows: bev,pas
  - 2022-2041: `trvkcb(t) = IF(ISNUMBER(trvkb[f,s](t)),trvkb[f,s](t)*trdfp[all,s](t),N(trvkcb[f,s](t-1))*trckb2r[f,s](t)^<usage, gasoline of trp.ela[all,all]>*trgpcr[all,all](t)^<passenger of trp.inc[all,all]>)`

**E957. `trbkmb`: Distance driven by BEVs, passenger** (bln km)

- Description: Calculation
- Legacy: legacy row 5220
- Rows: bev,pas
  - 2022-2041: `trbkmb(t) = trvkcb[f,s](t)*trvehb[f,s](t)/Thousand`

**E958. `trelph`: Electricity use of PHEVs** (bln kWh)

- Description: Calculation
- Legacy: legacy row 5222
- Rows: phv,pas
  - 2022-2041: `trelph(t) = trbkm[f,s](t)/trfebs[bev,s](t)*(1-trphg[f,s](t))`

**E959. `trelp`: Electricity use, passenger (BEVs and PHEVs)** (bln kWh)

- Description: Calculation
- Legacy: legacy row 5223
- Rows: ecy,pas
  - 2022-2041: `trelp(t) = (trbkmb[bev,s](t)/trfebs[bev,s](t))+trelph[phv,s](t)`

**E960. `trbkmt`: Distance driven, passenger and light (all types)** (bln km)

- Description: Calculation
- Legacy: legacy row 5225
- Rows: all,pas
  - 2022-2041: `trbkmt(t) = SUM(trbkm[5 rows](t))+trbkmb[bev,s](t)`

**E961. `trintp`: CO2 intensity of passenger and light vehicles** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 5226
- Rows: all,pas
  - 2022-2041: `trintp(t) = trco2p[f,s](t)/trbkmt[f,s](t)*Thousand`

**E962. `trvkcf`: Distance per freight vehicle by fuel, calibrated (fix B8: diesel base row)** (km)

- Description: Calculation
- Legacy: legacy rows 5231-5233
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trvkcf(t) = IF(ISNUMBER(trvkfd[all,s](t)),trvkfd[all,s](t)*trdff[all,s](t),N(trvkcf[f,s](t-1))*trcksfr[f,s](t)^<usage, diesel of trp.ela[all,all]>*trgpcr[all,all](t)^<freight of trp.inc[all,all]>)`

**E963. `trbkmf`: Distance driven by fuel, freight** (bln km)

- Description: Calculation
- Legacy: legacy rows 5239-5241
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trbkmf(t) = trvehf[f,s](t)*trvkcf[f,s](t)/Thousand`

**E964. `trfuf`: Fuel use, freight** (bln liters)

- Description: Calculation
- Legacy: legacy rows 5243-5245
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trfuf(t) = trbkmf[f,s](t)/trfscf[f,s](t)`
  - Parameters: `<EF (tCO2 per liter)>` = `<Diesel of trp.ef[all,all]>`

**E965. `trco2f`: CO2 from freight vehicles** (ktCO2)

- Description: Calculation
- Legacy: legacy row 5246
- Rows: all,fre
  - 2022-2041: `trco2f(t) = SUMPRODUCT(trfuf[3 rows](t),trfuf[3 rows](D))*Thousand`

**E966. `trfebof`: Fuel economy of the BEV stock, opening, freight** (km/kWh)

- Description: Calculation
- Legacy: legacy row 5251
- Rows: bev,fre
  - 2022-2041: `trfebof(t) = IF(N(trfebsf[f,s](t-1))>0,trfebsf[f,s](t-1),trfen[f,s](t))`

**E967. `trfebsf`: Fuel economy of the BEV stock, closing, freight** (km/kWh)

- Description: Calculation
- Legacy: legacy row 5253
- Rows: bev,fre
  - 2022-2041: `trfebsf(t) = trnwf[f,s](t)*trfen[f,s](t)+(1-trnwf[f,s](t))*trfebof[f,s](t)`

**E968. `trckbf2`: Cost per km of the BEV stock, freight** (USD/km)

- Description: Calculation
- Legacy: legacy row 5257
- Rows: bev,fre
  - 2022-2041: `trckbf2(t) = trpev[ecy,ind](t)/trfebof[f,s](t)+trdtxf[all,s](t)`

**E969. `trckbf2r`: Change in the cost per km of the BEV stock, freight** (ratio)

- Description: Calculation
- Legacy: legacy row 5258
- Rows: bev,fre
  - 2022: `trckbf2r(t) = ""`
  - 2023-2041: `trckbf2r(t) = trckbf2[f,s](t)/trckbf2[f,s](t-1)`

**E970. `trvkcbf`: Distance per BEV, freight, calibrated (fix B8: freight income elasticity)** (km)

- Description: Calculation
- Legacy: legacy row 5261
- Rows: bev,fre
  - 2022-2041: `trvkcbf(t) = IF(ISNUMBER(trvkfb[f,s](t)),trvkfb[f,s](t)*trdff[all,s](t),N(trvkcbf[f,s](t-1))*trckbf2r[f,s](t)^<usage, diesel of trp.ela[all,all]>*trgpcr[all,all](t)^<freight of trp.inc[all,all]>)`

**E971. `trbkmbf`: Distance driven by BEVs, freight** (bln km)

- Description: Calculation
- Legacy: legacy row 5264
- Rows: bev,fre
  - 2022-2041: `trbkmbf(t) = trvkcbf[f,s](t)*trvehfb[f,s](t)/Thousand`

**E972. `trelf`: Electricity use, freight** (bln kWh)

- Description: Calculation
- Legacy: legacy row 5265
- Rows: ecy,fre
  - 2022-2041: `trelf(t) = trbkmbf[bev,s](t)/trfebsf[bev,s](t)`

**E973. `trbkmtf`: Distance driven, freight (all types; fix B21)** (bln km)

- Description: Calculation
- Legacy: legacy row 5267
- Rows: all,fre
  - 2022-2041: `trbkmtf(t) = SUM(trbkmf[3 rows](t))+trbkmbf[bev,s](t)`

**E974. `trintf2`: CO2 intensity of freight vehicles** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 5268
- Rows: all,fre
  - 2022-2041: `trintf2(t) = IF(trbkmtf[f,s](t)=0,<Diesel of trp.ef[f,all]>/trfsof[die,s](t)*Million,trco2f[f,s](t)/trbkmtf[f,s](t)*Thousand)`

**E975. `trvkcc`: Distance per 2-3 wheeler, calibrated** (km)

- Description: Calculation
- Legacy: legacy row 5273
- Rows: gso,cyc
  - 2022-2041: `trvkcc(t) = IF(ISNUMBER(trvkd[all,s](t)),trvkd[all,s](t)*trdfc[all,s](t),N(trvkcc[f,s](t-1))*trckscr[f,s](t)^<usage, gasoline of trp.ela[all,all]>*trgpcr[all,all](t)^<2-3 wheeler of trp.inc[all,all]>)`

**E976. `trbkmc`: Distance driven by ICE 2-3 wheelers** (bln km)

- Description: Calculation
- Legacy: legacy row 5277
- Rows: gso,cyc
  - 2022-2041: `trbkmc(t) = trvehc[ice,s](t)*trvkcc[f,s](t)/Thousand`

**E977. `trfuc`: Gasoline use, 2-3 wheelers** (bln liters)

- Description: Calculation
- Legacy: legacy row 5279
- Rows: gso,cyc
  - 2022-2041: `trfuc(t) = trbkmc[f,s](t)/trfscc[f,s](t)`

**E978. `trco2c`: CO2 from 2-3 wheelers** (ktCO2)

- Description: Calculation
- Legacy: legacy row 5280
- Rows: all,cyc
  - 2022-2041: `trco2c(t) = trfuc[gso,s](t)*(<Gasoline of trp.ef[f,all]>*Thousand)`

**E979. `trfeboc`: Fuel economy of the BEV stock, opening, 2-3 wheelers** (km/kWh)

- Description: Calculation
- Legacy: legacy row 5285
- Rows: bev,cyc
  - 2022-2041: `trfeboc(t) = IF(N(trfebsc[f,s](t-1))>0,trfebsc[f,s](t-1),trfen[f,s](t))`

**E980. `trfebsc`: Fuel economy of the BEV stock, closing, 2-3 wheelers** (km/kWh)

- Description: Calculation
- Legacy: legacy row 5287
- Rows: bev,cyc
  - 2022-2041: `trfebsc(t) = trnwc[f,s](t)*trfen[f,s](t)+(1-trnwc[f,s](t))*trfeboc[f,s](t)`

**E981. `trckbc2`: Cost per km of the BEV stock, 2-3 wheelers** (USD/km)

- Description: Calculation
- Legacy: legacy row 5291
- Rows: bev,cyc
  - 2022-2041: `trckbc2(t) = trpev[ecy,res](t)/trfeboc[f,s](t)+trdtxc[all,s](t)`

**E982. `trckbc2r`: Change in the cost per km of the BEV stock, 2-3 wheelers** (ratio)

- Description: Calculation
- Legacy: legacy row 5292
- Rows: bev,cyc
  - 2022: `trckbc2r(t) = ""`
  - 2023-2041: `trckbc2r(t) = trckbc2[f,s](t)/trckbc2[f,s](t-1)`

**E983. `trvkcbc`: Distance per BEV 2-3 wheeler, calibrated (fix B8)** (km)

- Description: Calculation
- Legacy: legacy row 5295
- Rows: bev,cyc
  - 2022-2041: `trvkcbc(t) = IF(ISNUMBER(trvkbc[f,s](t)),trvkbc[f,s](t)*trdfc[all,s](t),N(trvkcbc[f,s](t-1))*trckbc2r[f,s](t)^<usage, gasoline of trp.ela[all,all]>*trgpcr[all,all](t)^<2-3 wheeler of trp.inc[all,all]>)`

**E984. `trbkmbc`: Distance driven by BEV 2-3 wheelers** (bln km)

- Description: Calculation
- Legacy: legacy row 5298
- Rows: bev,cyc
  - 2022-2041: `trbkmbc(t) = trvkcbc[f,s](t)*trvehc[f,s](t)/Thousand`

**E985. `trelc`: Electricity use, 2-3 wheelers** (bln kWh)

- Description: Calculation
- Legacy: legacy row 5299
- Rows: ecy,cyc
  - 2022-2041: `trelc(t) = trbkmbc[bev,s](t)/trfebsc[bev,s](t)`

**E986. `trbkmtc`: Distance driven, 2-3 wheelers** (bln km)

- Description: Calculation
- Legacy: legacy row 5301
- Rows: all,cyc
  - 2022-2041: `trbkmtc(t) = trbkmc[gso,s](t)+trbkmbc[bev,s](t)`

**E987. `trintc2`: CO2 intensity of 2-3 wheelers** (gCO2/km)

- Description: Calculation
- Legacy: legacy row 5302
- Rows: all,cyc
  - 2022-2041: `trintc2(t) = trco2c[f,s](t)/trbkmtc[f,s](t)*Thousand`

**E988. `trbusp`: Passenger fuel use (ktoe)** (ktoe)

- Description: Calculation
- Legacy: legacy rows 5310-5313 (fix B6)
- Rows: gso,pas, die,pas, lpg,pas, nga,pas
  - 2022-2041: `trbusp(t) = trfup[f,s](t)/<liters per ktoe>*Billion*1`
  - Parameters: `<liters per ktoe>` = `<Gasoline of trp.lpk[all,all]>`

**E989. `trbuse`: Passenger electricity use (ktoe)** (ktoe)

- Description: Calculation
- Legacy: legacy row 5314 (fix B6)
- Rows: ecy,pas
  - 2022-2041: `trbuse(t) = trelp[f,s](t)*Thousand/<GWh per ktoe of trp.mod[all,all]>*1`

**E990. `trbus0`: Passenger fuel and electricity use in the base year (ktoe; held)** (ktoe)

- Description: Calculation
- Legacy: legacy row 5310:5314 base year
- Rows: all,pas
  - 2022: `trbus0(t) = SUM(block@trbusp{trbusp, trbuse}(t))`
  - 2023-2041: `trbus0(t) = trbus0[f,s](t-1)`

**E991. `trbusf`: Bus fuel use (base-year bus fuel x passenger fuel use / base year)** (bln liters)

- Description: Calculation
- Legacy: legacy rows 5315-5317
- Rows: die,bus, lpg,bus, nga,bus
  - 2022-2041: `trbusf(t) = <bus fuel of the base year (ktoe)>*<liters per ktoe>/Billion*SUM(trbusp[4 rows](t))/trbus0[all,pas](t)`
  - Parameters: `<bus fuel of the base year (ktoe)>` = `<diesel of trp.bus[all,s]>`; `<liters per ktoe>` = `<Diesel of trp.lpk[all,all]>`

**E992. `trbusel`: Bus electricity use (base-year bus energy x EV stock share, x passenger electricity / base year)** (bln kWh)

- Description: Calculation
- Legacy: legacy row 5318 (fix B6)
- Rows: ecy,bus
  - 2022-2041: `trbusel(t) = <bus energy of the base year incl. electricity (ktoe)>*<GWh per ktoe of trp.mod[all,all]>/Thousand*trbuse[f,pas](t)/trbus0[all,pas](t)`
  - Parameters: `<bus energy of the base year incl. electricity (ktoe)>` = `<diesel of trp.bus[all,s]>+<LPG of trp.bus[all,s]>+<natural gas of trp.bus[all,s]>+<electricity of trp.bus[all,s]>`

**E993. `trfua`: Gasoline use, road (passenger and 2-3 wheelers)** (bln liters)

- Description: Calculation
- Legacy: legacy row 5321
- Rows: gso,all
  - 2022-2041: `trfua(t) = trfup[f,pas](t)+trfuc[f,cyc](t)`

**E994. `trfub`: Fuel use, road (passenger, freight, buses)** (bln liters)

- Description: Calculation
- Legacy: legacy rows 5322-5324
- Rows: die,all, lpg,all, nga,all
  - 2022-2041: `trfub(t) = trfup[f,pas](t)+trfuf[f,fre](t)+trbusf[f,bus](t)`

**E995. `trelt`: Electricity use, road (buses, 2-3 wheelers, freight, passenger)** (bln kWh)

- Description: Calculation
- Legacy: legacy row 5330
- Rows: ecy,all
  - 2022-2041: `trelt(t) = (trbusel[f,bus](t)+trelc[f,cyc](t))+trelf[f,fre](t)+trelp[f,pas](t)`

**E996. `trcf2`: Calibration factor step 2 by fuel: energy balance / calculated in the base year (held)** (factor)

- Description: Calculation (base year)
- Legacy: legacy E5325:E5328
- Rows: gso,all
  - 2022: `trcf2(t) = IF(OR(trfua[f,s](t)=0,<energy balance (ktoe)>=0),1,<energy balance (ktoe)>/(trfua[f,s](t)/<liters per ktoe>*Billion))`
  - 2023-2041: `trcf2(t) = trcf2[f,s](t-1)`
  - Parameters: `<energy balance (ktoe)>` = `<Gasoline of trp.eb[all,s]>`; `<liters per ktoe>` = `<Gasoline of trp.lpk[all,s]>`
- Rows: die,all, lpg,all, nga,all
  - 2022: `trcf2(t) = IF(OR(trfub[f,s](t)=0,<energy balance (ktoe)>=0),1,<energy balance (ktoe)>/(trfub[f,s](t)/<liters per ktoe>*Billion))`
  - 2023-2041: `trcf2(t) = trcf2[f,s](t-1)`
  - Parameters: `<energy balance (ktoe)>` = `<Diesel of trp.eb[all,s]>`; `<liters per ktoe>` = `<Diesel of trp.lpk[all,s]>`

**E997. `trcf2e`: Calibration factor step 2, electricity (1 unless reconciled; held)** (factor)

- Description: Calculation (base year)
- Legacy: legacy E5331
- Rows: ecy,all
  - 2022: `trcf2e(t) = IF(OR(trelt[f,s](t)=0,<energy balance (ktoe)>=0,LEFT(<reconcile (Yes / No)>,2)="No"),1,<energy balance (ktoe)>/(trelt[f,s](t)/<GWh per ktoe of trp.mod[all,s]>*Thousand))`
  - 2023-2041: `trcf2e(t) = trcf2e[f,s](t-1)`
  - Parameters: `<energy balance (ktoe)>` = `<electricity (PowerDemand) of trp.eb2[all,s]>`; `<reconcile (Yes / No)>` = `<reconcile electricity of trp.yrs[all,s]>`

**E998. `trkt`: Road fuel use from the engineer model (calibrated)** (ktoe)

- Description: Calculation
- Legacy: legacy rows 5325-5328
- Rows: gso,rod
  - 2022-2041: `trkt(t) = trfua[f,all](t)/<liters per ktoe>*Billion*trcf2[f,all](t)`
  - Parameters: `<liters per ktoe>` = `<Gasoline of trp.lpk[all,all]>`
- Rows: die,rod, lpg,rod, nga,rod
  - 2022-2041: `trkt(t) = trfub[f,all](t)/<liters per ktoe>*Billion*trcf2[f,all](t)`
  - Parameters: `<liters per ktoe>` = `<Diesel of trp.lpk[all,all]>`

**E999. `trbio`: Road biofuels with the engineer model: bioethanol and other biofuels follow gasoline, biodiesel follows diesel (base year x use / base-year use)** (ktoe)

- Description: Calculation
- Legacy: legacy rows 5435-5438
- Rows: bio,rod
  - 2022-2041: `trbio(t) = IF(<gasoline, base year (ktoe)>=0,<bioethanol and other biofuels, base year (ktoe)>,<bioethanol and other biofuels, base year (ktoe)>*trkt[gso,s](t)/<gasoline, base year (ktoe)>)+IF(<diesel, base year (ktoe)>=0,<biodiesel, base year (ktoe)>,<biodiesel, base year (ktoe)>*trkt[die,s](t)/<diesel, base year (ktoe)>)`
  - Parameters: `<bioethanol and other biofuels, base year (ktoe)>` = `<bioethanol of trp.eb2[all,all]>+<other biofuels of trp.eb2[all,all]>`; `<biodiesel, base year (ktoe)>` = `<biodiesel of trp.eb2[all,all]>`; `<gasoline, base year (ktoe)>` = `<Gasoline of trp.eb[all,all]>`; `<diesel, base year (ktoe)>` = `<Diesel of trp.eb[all,all]>`

**E1000. `trkte`: Road electricity use from the engineer model (to power demand when switched on)** (ktoe)

- Description: Calculation
- Legacy: legacy row 5331 (to row 3725)
- Rows: ecy,rod
  - 2022-2041: `trkte(t) = trelt[f,all](t)*Thousand/<GWh per ktoe of trp.mod[all,all]>*trcf2e[f,all](t)`

**E1001. `trkmp`: Distance driven, pas (calibrated)** (bln km)

- Description: Calculation
- Legacy: legacy row 5333
- Rows: all,pas
  - 2022-2041: `trkmp(t) = trbkmt[f,s](t)*trcf2[gso,all](t)`

**E1002. `trkmf`: Distance driven, fre (calibrated)** (bln km)

- Description: Calculation
- Legacy: legacy row 5334
- Rows: all,fre
  - 2022-2041: `trkmf(t) = trbkmtf[f,s](t)*trcf2[die,all](t)`

**E1003. `trkmc`: Distance driven, cyc (calibrated)** (bln km)

- Description: Calculation
- Legacy: legacy row 5335
- Rows: all,cyc
  - 2022-2041: `trkmc(t) = trbkmtc[f,s](t)*trcf2[gso,all](t)`

**E1004. `trkmt`: Distance driven, road** (bln km)

- Description: Calculation
- Legacy: legacy row 5336
- Rows: all,all
  - 2022-2041: `trkmt(t) = trkmp[f,pas](t)+trkmf[f,fre](t)+trkmc[f,cyc](t)`

**E1005. `trfcp`: Fuel use, passenger and light (calibrated)** (bln liters)

- Description: Calculation
- Legacy: legacy rows 5339-5342
- Rows: gso,pas, die,pas, lpg,pas, nga,pas
  - 2022-2041: `trfcp(t) = trfup[f,s](t)*trcf2[f,all](t)`

**E1006. `trfcep`: Electricity use, pas (calibrated if reconciled)** (bln kWh)

- Description: Calculation
- Legacy: legacy row 5343
- Rows: ecy,pas
  - 2022-2041: `trfcep(t) = trelp[f,s](t)*trcf2e[f,all](t)`

**E1007. `trfcef`: Electricity use, fre (calibrated if reconciled)** (bln kWh)

- Description: Calculation
- Legacy: legacy row 5348
- Rows: ecy,fre
  - 2022-2041: `trfcef(t) = trelf[f,s](t)*trcf2e[f,all](t)`

**E1008. `trfcec`: Electricity use, cyc (calibrated if reconciled)** (bln kWh)

- Description: Calculation
- Legacy: legacy row 5351
- Rows: ecy,cyc
  - 2022-2041: `trfcec(t) = trelc[f,s](t)*trcf2e[f,all](t)`

**E1009. `trfcf`: Fuel use, freight (calibrated)** (bln liters)

- Description: Calculation
- Legacy: legacy rows 5345-5347
- Rows: die,fre, lpg,fre, nga,fre
  - 2022-2041: `trfcf(t) = trfuf[f,s](t)*trcf2[f,all](t)`

**E1010. `trfcc`: Gasoline use, 2-3 wheelers (calibrated)** (bln liters)

- Description: Calculation
- Legacy: legacy row 5350
- Rows: gso,cyc
  - 2022-2041: `trfcc(t) = trfuc[f,s](t)*trcf2[f,all](t)`

**E1011. `trafg`: Average fuel economy, gasoline (passenger and 2-3 wheelers by fuel use)** (km/l)

- Description: Calculation
- Legacy: legacy row 5356
- Rows: gso,all
  - 2022-2041: `trafg(t) = IF(trfua[f,s](t)=0,trfso[f,pas](t)*TrFEWGso+trfsoc[f,cyc](t)*(1-TrFEWGso),(trfso[f,pas](t)*trfup[f,pas](t)+trfsoc[f,cyc](t)*trfuc[f,cyc](t))/(trfup[f,pas](t)+trfuc[f,cyc](t)))`

**E1012. `trafo`: Average fuel economy, diesel, LPG, gas (passenger and freight by fuel use)** (km/l)

- Description: Calculation
- Legacy: legacy rows 5360, 5364, 5368 (fix B22)
- Rows: die,all, lpg,all, nga,all
  - 2022-2041: `trafo(t) = IF(trfub[f,s](t)=0,trfso[f,pas](t)*TrFEWHalf+trfsof[f,fre](t)*(1-TrFEWHalf),(trfso[f,pas](t)*trfup[f,pas](t)+trfsof[f,fre](t)*trfuf[f,fre](t))/(trfup[f,pas](t)+trfuf[f,fre](t)))`

**E1013. `trafen`: EV fuel economy x electricity use (passenger, freight, 2-3 wheelers)** (km)

- Description: Calculation
- Legacy: legacy row 5373 (numerator)
- Rows: ecy,all
  - 2022-2041: `trafen(t) = trfebo[bev,pas](t)*trelp[f,pas](t)+trfebof[bev,fre](t)*trelf[f,fre](t)+trfeboc[bev,cyc](t)*trelc[f,cyc](t)`

**E1014. `trafe`: Average fuel economy of EVs (by electricity use; fix B22)** (km/kWh)

- Description: Calculation
- Legacy: legacy row 5373
- Rows: ecy,all
  - 2022-2041: `trafe(t) = IF(trelt[f,s](t)=0,trfebo[bev,pas](t)*TrFEWEvP+(trfebof[bev,fre](t)+trfeboc[bev,cyc](t))*TrFEWEvO,trafen[f,s](t)/(trelp[f,pas](t)+trelf[f,fre](t)+trelc[f,cyc](t)))`

**E1015. `trvht`: Vehicles, passenger and light (all types)** (million)

- Description: Calculation
- Legacy: legacy row 5375
- Rows: all,pas
  - 2022-2041: `trvht(t) = SUM(trveh[5 rows](t))+trvehb[bev,s](t)`

**E1016. `trvhtf`: Vehicles, freight** (million)

- Description: Calculation
- Legacy: legacy row 5376
- Rows: all,fre
  - 2022-2041: `trvhtf(t) = SUM(trvehf[3 rows](t))+trvehfb[bev,s](t)`

**E1017. `trvhtc`: Vehicles, 2-3 wheelers** (million)

- Description: Calculation
- Legacy: legacy row 5377
- Rows: all,cyc
  - 2022-2041: `trvhtc(t) = trvehc[ice,s](t)+trvehc[bev,s](t)`

**E1018. `trvhta`: Vehicles, road** (million)

- Description: Calculation
- Legacy: legacy row 5378
- Rows: all,all
  - 2022-2041: `trvhta(t) = trvht[f,pas](t)+trvhtf[f,fre](t)+trvhtc[f,cyc](t)`

**E1019. `trrafp`: EV sales share, calculated less actual (pas; data years)** (share)

- Description: Calculation
- Legacy: legacy rows 18981-18987 (Transport3 row 4)
- Rows: ev,pas
  - 2022-2041: `trrafp(t) = IF(tr.dk[all,all](t)=1,trevcc[f,s](t)-trevac[bev,s](t),"")`

**E1020. `trraff`: EV sales share, calculated less actual (fre; data years)** (share)

- Description: Calculation
- Legacy: legacy rows 18981-18987 (Transport3 row 4)
- Rows: ev,fre
  - 2022-2041: `trraff(t) = IF(tr.dk[all,all](t)=1,trlgfb[bev,s](t)-trevaf[bev,s](t),"")`

**E1021. `trrafc`: EV sales share, calculated less actual (cyc; data years)** (share)

- Description: Calculation
- Legacy: legacy rows 18981-18987 (Transport3 row 4)
- Rows: ev,cyc
  - 2022-2041: `trrafc(t) = IF(tr.dk[all,all](t)=1,trlgcb[bev,s](t)-trevacc[bev,s](t),"")`

**E1022. `trq`: Fuel use of the switched model read by the transport co-benefits module: road and total (electricity: demand)** (ktoe)

- Description: Calculation
- Legacy: legacy E2 rows 15744-15787
- Rows: gso,rod, die,rod, lpg,rod, nga,rod, gso,all, die,all, lpg,all, nga,all
  - 2022-2041: `trq(t) = ener[f,s](t)`
- Rows: ecy,rod, ecy,all
  - 2022-2041: `trq(t) = eldem[f,s](t)`

**E1023. `tran.rsh`: Road share of the fuel: road use / total use (switched model; electricity: road demand / total demand)** (share)

- Description: Calculation
- Legacy: legacy E2 rows 15768-15786; Transport rows 120-128 (R1.9)
- Rows: gso,rod, die,rod, lpg,rod, nga,rod, ecy,rod
  - 2022-2041: `tran.rsh(t) = IF(trq[f,all](t)=0,0,trq[f,s](t)/trq[f,all](t))`

**E1024. `trp.bfe`: Elasticities and autonomous efficiency gain, other road biofuels: oil | transport (legacy rows 5392, 5406; I143)** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy Elasticities (Inputs_ela)
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<income elasticity>` = `INDEX(ElaSel,MATCH("inc|oil|tra",ElaSelKey,0))`; `<usage elasticity>` = `INDEX(ElaSel,MATCH("usg|oil|tra",ElaSelKey,0))`; `<efficiency exponent eps_F x (1 + eps_U)>` = `INDEX(ElaSel,MATCH("eff|oil|tra",ElaSelKey,0))*(1+<usage elasticity>)`; `<autonomous efficiency gain>` = `INDEX(ElaSel,MATCH("aei|oil|tra",ElaSelKey,0))`

**E1025. `trp.rne`: Elasticities and autonomous efficiency gain, self-generated renewables: renewables | transport (legacy 5491, 5516; I144)** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy Elasticities (Inputs_ela)
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<income elasticity>` = `INDEX(ElaSel,MATCH("inc|ren|tra",ElaSelKey,0))`; `<usage elasticity>` = `INDEX(ElaSel,MATCH("usg|ren|tra",ElaSelKey,0))`; `<efficiency exponent eps_F x (1 + eps_U)>` = `INDEX(ElaSel,MATCH("eff|ren|tra",ElaSelKey,0))*(1+<usage elasticity>)`; `<autonomous efficiency gain>` = `INDEX(ElaSel,MATCH("aei|ren|tra",ElaSelKey,0))`

**E1026. `trp.rn0`: Self-generated renewables in the base year (ktoe; EnergyCons)** (-)

- Description: Parameters (sheets TransportParams, Transport1-3, Inputs)
- Legacy: legacy rows 5491, 5516 (base year)
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<aviation>` = `IFERROR(INDEX(ConsVal,MATCH(CodePrefix&"enc.ren",ConsKey,0),MATCH("avi",ConsSub,0)),0)`; `<navigation>` = `IFERROR(INDEX(ConsVal,MATCH(CodePrefix&"enc.ren",ConsKey,0),MATCH("nav",ConsSub,0)),0)`

**E1027. `trbe`: Road biofuels, elasticity road model (bioethanol, biodiesel, other biofuels; total = road biomass where TrModel is not Engineer)** (ktoe)

- Description: Calculation
- Legacy: legacy rows 5403-5406, 5435-5438
- Rows: bgs,rod
  - 2022: `trbe(t) = <bioethanol of trp.eb2[all,all]>`
  - 2023-2041: `trbe(t) = IF(enel[gso,s](t-1)=0,trbe[f,s](t-1),trbe[f,s](t-1)*enel[gso,s](t)/enel[gso,s](t-1))`
- Rows: bdi,rod
  - 2022: `trbe(t) = <biodiesel of trp.eb2[all,all]>`
  - 2023-2041: `trbe(t) = IF(enel[die,s](t-1)=0,trbe[f,s](t-1),trbe[f,s](t-1)*enel[die,s](t)/enel[die,s](t-1))`
- Rows: obf,rod
  - 2022: `trbe(t) = <other biofuels of trp.eb2[all,all]>`
  - 2023-2041: `trbe(t) = trbe[f,s](t-1)*trbea[f,s](t)*(1+row14(t))^<income elasticity of trp.bfe[all,all]>*(atp[bio,s](t)/atp[bio,s](t-1))^<usage elasticity of trp.bfe[all,all]>*((atp[bio,s](t)+shp[bio,s](t))/(atp[bio,s](t-1)+shp[bio,s](t-1)))^<efficiency exponent eps_F x (1 + eps_U) of trp.bfe[all,all]>*row6(t)`
- Rows: bio,rod
  - 2022-2041: `trbe(t) = trbe[bgs,s](t)+trbe[bdi,s](t)+trbe[obf,s](t)`

**E1028. `trbea`: Efficiency factor of other road biofuels (oil AEEI and the road group additional efficiency)** (factor)

- Description: Calculation
- Legacy: legacy row 5406 (AEEI term)
- Rows: obf,rod
  - 2022-2041: `trbea(t) = (1/(1+<autonomous efficiency gain of trp.bfe[all,all]>+AdditionalEfficiencyRoadVehicle(t)))^(1+<usage elasticity of trp.bfe[all,all]>)`

**E1029. `trpren`: Price of self-generated renewables: levelised investment cost of solar (section 3 E)** (USD/kWh)

- Description: Calculation
- Legacy: legacy rows 2805-2806 (= row 3468), 5480, 5505
- Rows: ren,tra
  - 2022-2041: `trpren(t) = tic[sol,pow](t)`

**E1030. `trrena`: Efficiency factor of self-generated renewables (renewables AEEI and the road group additional efficiency)** (factor)

- Description: Calculation
- Legacy: legacy rows 5491, 5516 (AEEI term)
- Rows: ren,tra
  - 2022-2041: `trrena(t) = (1/(1+<autonomous efficiency gain of trp.rne[all,all]>+AdditionalEfficiencyRoadVehicle(t)))^(1+<usage elasticity of trp.rne[all,all]>)`

**E1031. `trsum`: Road fuel and electricity use from the engineer model (used where TrModel = Engineer)** (ktoe)

- Description: Sum of the section 5b result rows (fuels, biofuels, electricity)
- Legacy: legacy rows 5325-5331
- Rows: all,rod
  - 2022-2041: `trsum(t) = SUM(block@trkt{trkt, trbio}(t))+trkte[ecy,s](t)`

### 6b; 7; 8

**E1032. `lkt`: Leakage: new policy in the residential price of the fuel (new carbon tax, ETS and excise, incl. VAT)** (USD/GJ)

- Description: nce of the residential row of the fuel x (1 + VAT rate) (LEAKTAX)
- Legacy: legacy rows 5574, 5580, 5586 (new policy x residential coverage; L91 fixed: an exempt fuel has none)
- Rows: nga,res, lpg,res, ker,res
  - 2022-2041: `lkt(t) = INDEX(nce[9 rows](t),<fuel position (residential block)>)*(1+<VAT rate>)`
  - Parameters: `<VAT rate>` = `INDEX(Inputs!V5:V148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<fuel position (residential block)>` = `INDEX(Inputs!L5:L148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E1033. `lkp`: Leakage: share of the fuel moving to biomass in the year (negative: back to the fuel)** (share)

- Description: on x MIN((1 + (lkt - lkt last year) / atp last year)^coef - 1, 1); base year 0 (LEAKSHARE)
- Legacy: legacy rows 5575-5576, 5581-5582, 5587-5589 (L45 fixed: kerosene with its own price and share)
- Rows: nga,res, lpg,res, ker,res
  - 2022: `lkp(t) = 0`
  - 2023-2041: `lkp(t) = <on (BioLeak Yes and the most-used cooking fuel CookFuel)>*MIN((1+(lkt[f,s](t)-lkt[f,s](t-1))/INDEX(atp[9 rows](t-1),<fuel position (residential block)>))^<coefficient sigma x e_bio / e_fuel / lag>-1,1)`
  - Parameters: `<on (BioLeak Yes and the most-used cooking fuel CookFuel)>` = `IF(AND(LEFT(BioLeak,3)="Yes",CookFuel=f),1,0)`; `<coefficient sigma x e_bio / e_fuel / lag>` = `ResBioSubst*CookEffBio/INDEX(CookEffVal,MATCH(f,CookEffKey,0))/ResSubstLag`; `<fuel position (residential block)>` = `INDEX(Inputs!L5:L148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E1034. `lkd`: Leakage: change in residential fossil fuel use in the year** (ktoe)

- Description: - (fuel use last year - initially exempt use lkx last year) x cookstove efficiency of the fuel x lkp; base year 0 (LEAKCHANGE; v0.9.0, R6.7: exempt use does not leak, I138)
- Legacy: legacy rows 5577, 5583, 5588 (L45 fixed: on actual use; as legacy on the not-exempt rows 5564-5566)
- Rows: nga,res, lpg,res, ker,res
  - 2022: `lkd(t) = 0`
  - 2023-2041: `lkd(t) = -(INDEX(ener[9 rows](t-1),<fuel position (residential block)>)-lkx[f,s](t-1))*<cookstove efficiency of the fuel>*lkp[f,s](t)`
  - Parameters: `<cookstove efficiency of the fuel>` = `INDEX(CookEffVal,MATCH(f,CookEffKey,0))`; `<fuel position (residential block)>` = `INDEX(Inputs!L5:L148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E1035. `lkb`: Leakage: biomass replacing the fuel in the year (same useful energy)** (ktoe)

- Description: - lkd x efficiency of the fuel / efficiency of biomass (LEAKBIOMASS)
- Legacy: legacy rows 5578, 5584, 5591, 5593 (L90 fixed: legacy multiplies by the biomass efficiency again)
- Rows: nga,res, lpg,res, ker,res
  - 2022-2041: `lkb(t) = -lkd[f,s](t)*<cookstove efficiency of the fuel>/<cookstove efficiency of biomass>`
  - Parameters: `<cookstove efficiency of the fuel>` = `INDEX(CookEffVal,MATCH(f,CookEffKey,0))`; `<cookstove efficiency of biomass>` = `CookEffBio`

**E1036. `lkxp`: Initially exempt demand: phase-in of the usage elasticity** (share)

- Description: PHASEIN (ExemptPhaseout, YearPha, ExemptPhaseoutPeriod; v0.5.6)
- Legacy: legacy rows 5568-5570 (rule of 2259-2265, L94)
- Rows: none,res
  - 2022-2041: `lkxp(t) = IF(ExemptPhaseout(t)=TRUE,MAX(MIN((year+1-YearPha(t))/ExemptPhaseoutPeriod(t),1),0),0)`

**E1037. `lkxe`: Initially exempt demand: growth of the fuel use of the row (enel)** (ratio)

- Description: XRATIO (v0.5.6)
- Legacy: new
- Rows: nga,res, lpg,res, ker,res
  - 2022: `lkxe(t) = 1`
  - 2023-2041: `lkxe(t) = IF(INDEX(enel[9 rows](t-1),<fuel position (Inputs)>)=0,1,INDEX(enel[9 rows](t),<fuel position (Inputs)>)/INDEX(enel[9 rows](t-1),<fuel position (Inputs)>))`
  - Parameters: `<fuel position (Inputs)>` = `INDEX(Inputs!L5:L148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E1038. `lkxr`: Initially exempt demand: ratio of the after-tax price** (ratio)

- Description: XRATIO (v0.5.6)
- Legacy: new
- Rows: nga,res, lpg,res, ker,res
  - 2022: `lkxr(t) = 1`
  - 2023-2041: `lkxr(t) = IF(INDEX(atp[9 rows](t-1),<fuel position (Inputs)>)=0,1,INDEX(atp[9 rows](t),<fuel position (Inputs)>)/INDEX(atp[9 rows](t-1),<fuel position (Inputs)>))`
  - Parameters: `<fuel position (Inputs)>` = `INDEX(Inputs!L5:L148,MATCH(f&"|"&s,Inputs!A5:A148,0))`

**E1039. `lkx`: Initially exempt fuel use of the most-used cooking fuel** (ktoe)

- Description: base: ExemptCookShare x fuel use; then XPATH: the usage elasticity phased in (v0.5.6; income factor as the row, L48 fixed)
- Legacy: legacy rows 5568-5570
- Rows: nga,res, lpg,res, ker,res
  - 2022: `lkx(t) = <initially exempt share>*INDEX(enel[9 rows](t),<fuel position (Inputs)>)`
  - 2023-2041: `lkx(t) = lkx[f,s](t-1)*lkxe[f,s](t)*lkxr[f,s](t)^(<usage elasticity (residential block)>*(lkxp[none,s](t)-1))`
  - Parameters: `<fuel position (Inputs)>` = `INDEX(Inputs!L5:L148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<usage elasticity (residential block)>` = `INDEX(enel[9 rows](E),<fuel position (Inputs)>)`; `<initially exempt share>` = `IF(CookFuel=f,ExemptCookShare,0)`

**E1040. `lkxa`: Initially exempt demand: adjustment added to fuel use (through lkc)** (ktoe)

- Description: lkx - share x enel (v0.5.6)
- Legacy: legacy totals 5554, 5557, 5558 (not-exempt + initially exempt)
- Rows: nga,res, lpg,res, ker,res
  - 2022: `lkxa(t) = 0`
  - 2023-2041: `lkxa(t) = lkx[f,s](t)-<initially exempt share>*INDEX(enel[9 rows](t),<fuel position (Inputs)>)`
  - Parameters: `<fuel position (Inputs)>` = `INDEX(Inputs!L5:L148,MATCH(f&"|"&s,Inputs!A5:A148,0))`; `<initially exempt share>` = `IF(CookFuel=f,ExemptCookShare,0)`

**E1041. `lkz`: Leakage: none (position 1 of the rows added to fuel use)** (ktoe)

- Description: 0
- Legacy: new (v0.5.1)
- Rows: none,res
  - 2022-2041: `lkz(t) = 0`

**E1042. `lkc`: Leakage: cumulative change in residential fossil fuel use (added to fuel use)** (ktoe)

- Description: lkc last year + lkd; base year 0 (LEAKCUM)
- Legacy: legacy totals 5554, 5557, 5558 (SUM of the changes; L45 fixed)
- Rows: nga,res, lpg,res, ker,res
  - 2022: `lkc(t) = 0`
  - 2023-2041: `lkc(t) = lkc[f,s](t-1)+(lkd[f,s](t)+lkxa[f,s](t)-lkxa[f,s](t-1))`

**E1043. `lkcb`: Leakage: cumulative change in residential biomass use (added to fuel use)** (ktoe)

- Description: lkcb last year + the sum of lkb; base year 0 (LEAKCUM)
- Legacy: legacy total 5560 (SUM of the changes)
- Rows: bio,res
  - 2022: `lkcb(t) = 0`
  - 2023-2041: `lkcb(t) = lkcb[f,s](t-1)+SUM(lkb[3 rows](t))`

**E1044. `lks`: Residential leakage to biomass: net change in residential fuel use (summary row of section 6b)** (ktoe)

- Description: Sum of lkc and lkcb
- Legacy: new (v0.5.1)
- Rows: all,res
  - 2022-2041: `lks(t) = SUM(block@lkc{lkc, lkcb}(t))`

### 11

**E1045. `ener.chk`: Check: totals by subsector (and power) and by fuel minus total fuel use (should be 0)** (ktoe)

- Description: Check
- Legacy: new
  - 2022-2041: `ener.chk(t) = ABS(SUM(ener[17 rows](t))-ener[all,all](t))+ABS(SUM(ener[9 rows](t))+ener[ren,avi](t)+ener[ren,nav](t)-ener[all,all](t))`

**E1046. `ener.ref`: Fuel use, scenario 1 (same year)** (ktoe)

- Description: Lookup
- Legacy: new
- Rows: all,all
  - 2022-2041: `ener.ref(t) = INDEX(ener[f,s](..t),MATCH(year,year(..t),0))`

**E1047. `ener.pct`: Change in fuel use vs scenario 1** (%)

- Description: Calculation
- Legacy: new
- Rows: all,all
  - 2022-2041: `ener.pct(t) = ener[f,s](t)/ener.ref[f,s](t)-1`

**E1048. `echg`: Energy consumption: change against scenario 1 (same year)** (ktoe)

- Description: Row of section 11 (fuel incl. power generation; sector total; power fuels) - scenario 1
- Legacy: legacy F7, v0.3.14
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all, all,tra, all,bld, all,ind, ... (15 rows)
  - 2022-2041: `echg(t) = ener[f,s](t)-INDEX(ener[f,s](..t),row10(t))`

**E1049. `epct`: Energy consumption: % change against scenario 1** (%)

- Description: echg / (level - echg); 0 when 0
- Legacy: legacy F7, v0.3.14
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all, all,tra, all,bld, all,ind, ... (14 rows)
  - 2022-2041: `epct(t) = IF(ener[f,s](t)-echg[f,s](t)=0,0,echg[f,s](t)/(ener[f,s](t)-echg[f,s](t)))`

### 12

**E1050. `rmf`: Revenue from the methane fee** (USD m real)

- Description: ch4.rev (section 14)
- Legacy: legacy Mitigation row 6169
- Rows: all,all
  - 2022-2041: `rmf(t) = ch4.rev[f,s](t)`

**E1051. `rpsu`: Producer subsidies after the phase-out (negative = fiscal cost)** (USD m real)

- Description: -SUMPRODUCT(pros, psf)
- Legacy: legacy rows 7824-7862 (v0.4.16, LD19)
- Rows: all,all
  - 2022-2041: `rpsu(t) = -SUMPRODUCT(pros[5 rows](t),psf[5 rows](t))`

**E1052. `rnet`: Net revenue from existing taxes and subsidies** (USD m real)

- Description: rtx + rsub (rsub negative)
- Legacy: new
- Rows: all,all
  - 2022-2041: `rnet(t) = rtx[f,s](t)+rsub[f,s](t)`

**E1053. `rtot.ref`: Total revenue, scenario 1 (same year)** (USD m real)

- Description: Lookup
- Legacy: new
- Rows: all,all
  - 2022-2041: `rtot.ref(t) = INDEX(rtot[f,s](..t),MATCH(year,year(..t),0))`

**E1054. `rev.chk`: Check: revenue totals minus their sector and power rows (rtx, rsub, rnew; should be 0)** (USD m real)

- Description: Check
- Legacy: new
- Rows: all,all
  - 2022-2041: `rev.chk(t) = ABS(rtx[f,s](t)-SUM(rtx[5 rows](t)))+ABS(rsub[f,s](t)-SUM(rsub[5 rows](t)))+ABS(rnew[f,s](t)-SUM(rnew[5 rows](t)))`

**E1055. `rfu`: Revenue by fuel net of subsidies: final use (fuels), electricity (VAT, subsidy gap, VAT on new policies)** (USD m real)

- Description: Fuels: rtx + rsub + rnew of the fuel over all subsectors; electricity: rvat + rgap + rnvat (section 3 G)
- Legacy: legacy section 16 info rows (F9), v0.3.13
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all
  - 2022-2041: `rfu(t) = SUMPRODUCT(SUMIFS(block{ener, eldem, ctxnew, ets, ... 600 variables}(t),SecVar,{"rtx","rsub","rnew","rsr"},SecFuel,f))`
- Rows: ecy,pow
  - 2022-2041: `rfu(t) = SUM(block@rvat{rvat, rnvat, rreb, rpex, ... 5 variables}(t))+SUM(prrns[9 rows](t))`

**E1056. `rfg`: Revenue from fuels burnt in power generation, net of subsidies** (USD m real)

- Description: prtx + prxc + prsub + prnew of the generation type (section 3 M)
- Legacy: legacy section 16 info rows (F9), v0.3.13
- Rows: coa,pow, nga,pow, oop,pow, bio,pow
  - 2022-2041: `rfg(t) = prtx[f,s](t)+prxc[f,s](t)+prsub[f,s](t)+prnew[f,s](t)`

**E1057. `rfu.chk`: Check: revenue by fuel minus (rnet + rnew), all sectors (0 = consistent)** (USD m real)

- Description: ABS(sum of rfu and rfg - rnet.all - rnew.all)
- Legacy: new (v0.3.13)
- Rows: all,all
  - 2022-2041: `rfu.chk(t) = ABS(SUM(block@rfu{rfu, rfg}(t))-rnet[f,s](t)-rnew[f,s](t)-rsr[f,s](t))`

**E1058. `rbe`: Base erosion: change in existing taxes net of subsidies against scenario 1** (USD m real)

- Description: rnet - rnet of scenario 1 (same year)
- Legacy: legacy section 16 info rows (base erosion), v0.3.13
- Rows: all,all
  - 2022-2041: `rbe(t) = rnet[f,s](t)-INDEX(rnet[f,s](..t),row10(t))`

**E1059. `rpct`: Revenue as a share of baseline real GDP** (% of GDP)

- Description: USD m / (gdp.usd x MperBn); GDPSHARE
- Legacy: legacy section 16 info rows (% of GDP), v0.3.13
- Rows: tot,all
  - 2022-2041: `rpct(t) = rtot[all,s](t)/(gdp.usd[all,s](t)*MperBn)`
- Rows: net,all
  - 2022-2041: `rpct(t) = rnet[all,s](t)/(gdp.usd[all,s](t)*MperBn)`
- Rows: sub,all
  - 2022-2041: `rpct(t) = rsub[all,s](t)/(gdp.usd[all,s](t)*MperBn)`
- Rows: new,all
  - 2022-2041: `rpct(t) = rnew[all,s](t)/(gdp.usd[all,s](t)*MperBn)`
- Rows: chg,all
  - 2022-2041: `rpct(t) = rtot.chg[all,s](t)/(gdp.usd[all,s](t)*MperBn)`
- Rows: be,all
  - 2022-2041: `rpct(t) = rbe[all,s](t)/(gdp.usd[all,s](t)*MperBn)`

**E1060. `gdpn`: Nominal GDP (local currency, USD)** (bn nominal (LCU or USD, by row))

- Description: WEO NGDP (LCU) and NGDPD (USD), extended with nominal growth past the last data year (Inputs_macro; v0.5.6)
- Legacy: legacy rows 424 (NGDP); NGDPD new
- Rows: lcu,all
  - 2022-2041: `gdpn(t) = INDEX(WEOVal,MATCH(CtryCode&"|ngdp",WEOKey,0),MATCH(year,WEOYear,0))`
- Rows: usd,all
  - 2022-2041: `gdpn(t) = INDEX(WEOVal,MATCH(CtryCode&"|ngdpd",WEOKey,0),MATCH(year,WEOYear,0))`

**E1061. `rpol`: Total revenue by policy (12e, legacy rows 8016-8027): ct new carbon tax, exc new excise, exi existing taxes and subsidies, vat VAT, ets auctioned ETS, psu producer subsidies (electricity subsidy gap), ren renewable subsidies, mf methane fee, trs transport; ctp, etp: of which power** (USD m real)

- Description: ct = SUMPRODUCT(covct, ctr); ets = SUMPRODUCT(co2.sec, etr) x revenue factor; exc = rex + power prnew - ctp - etp; vat = rvt + electricity VAT; psu = rgap; exi = rnet + rnew - the others; ren, trs 0 (not modelled)
- Legacy: legacy rows 8016-8027 (v0.4.15, LD37)
- Rows: ct,all
  - 2022-2041: `rpol(t) = SUMPRODUCT(covct[17 rows](t),ctr[17 rows](t))+SUM(rreb[2 rows](t))+rexs(t)`
- Rows: exc,all
  - 2022-2041: `rpol(t) = SUMIFS(block{ener, eldem, ctxnew, ets, ... 600 variables}(t),SecVar,"rex")+SUM(prnew[9 rows](t))-rpol[ctp,s](t)-rpol[etp,s](t)+rexm(t)`
- Rows: exi,all
  - 2022-2041: `rpol(t) = rtot[all,s](t)-rmf[all,s](t)-rpol[ct,s](t)-rpol[exc,s](t)-rpol[vat,s](t)-rpol[ets,s](t)-rpol[psu,s](t)-rpol[ren,s](t)`
- Rows: vat,all
  - 2022-2041: `rpol(t) = SUMIFS(block{ener, eldem, ctxnew, ets, ... 600 variables}(t),SecVar,"rvt")+SUM(rvat[2 rows](t))+SUM(rnvat[2 rows](t))`
- Rows: ets,all
  - 2022-2041: `rpol(t) = SUMPRODUCT(co2.sec[17 rows](t),etr[17 rows](t))*ets.rf(t)`
- Rows: psu,all
  - 2022-2041: `rpol(t) = SUM(rgap[2 rows](t))+rpsu[all,s](t)`
- ... and 6 further row patterns (see the workbook)

**E1062. `rpol.chk`: Check: total by policy minus total revenue (should be 0)** (USD m real)

- Description: ABS(rpol.tot - rtot)
- Legacy: legacy row 8016 (by fuel = by policy)
- Rows: all,all
  - 2022-2041: `rpol.chk(t) = ABS(rpol[tot,s](t)-rtot[f,s](t))`

**E1063. `rtot`: Total revenue (net existing + new policies + methane fee)** (USD m real)

- Description: rnet + rnew + rmf
- Legacy: new
- Rows: all,all
  - 2022-2041: `rtot(t) = rnet[f,s](t)+rnew[f,s](t)+rsr[f,s](t)+rpsu[f,s](t)+rmf[f,s](t)`

**E1064. `rtot.chg`: Change in total revenue vs scenario 1 (fiscal effect)** (USD m real)

- Description: rtot - rtot.ref
- Legacy: new
- Rows: all,all
  - 2022-2041: `rtot.chg(t) = rtot[f,s](t)-rtot.ref[f,s](t)`

### 13

**E1065. `co2.ref`: CO2 emissions, scenario 1 (same year)** (MtCO2)

- Description: Lookup
- Legacy: new
- Rows: all,all
  - 2022-2041: `co2.ref(t) = INDEX(co2[f,s](..t),MATCH(year,year(..t),0))`

**E1066. `co2.pct`: Change in CO2 emissions vs scenario 1** (%)

- Description: co2 / co2.ref - 1
- Legacy: new
- Rows: all,all
  - 2022-2041: `co2.pct(t) = co2[f,s](t)/co2.ref[f,s](t)-1`

**E1067. `co2.sec`: CO2 emissions by ETS sector** (MtCO2)

- Description: Sum over fuels (power: section 3, v0.1.06)
- Legacy: new
- Rows: all,pow, all,rod, all,ral, all,avi, all,nav, all,res, all,foo, all,srv, all,mch, all,irn, all,nfm, all,mac, ... (17 rows)
  - 2022-2041: `co2.sec(t) = SUMIFS(block{ener, eldem, ctxnew, ets, ... 600 variables}(t),SecVar,"co2",SecSub,s)+SUMIF(co2[9 rows](C),s,co2[9 rows](t))`

**E1068. `co2.ets`: CO2 emissions covered by the new ETS** (MtCO2)

- Description: SUMPRODUCT(co2.sec, etsc)
- Legacy: legacy row 1959
- Rows: all,all
  - 2022-2041: `co2.ets(t) = SUMPRODUCT(co2.sec[17 rows](t),etsc[17 rows](t))`

**E1069. `co2.cap`: ETS cap** (MtCO2)

- Description: ets.cap (section 1)
- Legacy: legacy row 1960
- Rows: all,all
  - 2022-2041: `co2.cap(t) = ets.cap(t)`

**E1070. `co2.gap`: Covered emissions vs cap (0 = cap met)** (%)

- Description: co2.ets / co2.cap - 1
- Legacy: legacy rows 1961-1963
- Rows: all,all
  - 2022-2041: `co2.gap(t) = IF(co2.cap[f,s](t)>0,co2.ets[f,s](t)/co2.cap[f,s](t)-1,0)`

**E1071. `ets.lr`: ETS: log ratio LN(cap / baseline) / LN(covered / baseline) (0 if the cap does not bind)** (ratio)

- Description: Calculation
- Legacy: legacy PricesAdjustedByErrorFactor (row 1966)
- Rows: all,all
  - 2022-2041: `ets.lr(t) = IF(OR(ets.cap(t)<=0,ets.cap(t)>=ets.bce(t),co2.ets[f,s](t)>=ets.bce(t)),0,LN(ets.cap(t)/ets.bce(t))/LN(co2.ets[f,s](t)/ets.bce(t)))`

**E1072. `ets.next`: ETS price proposal for the next iteration** (USD/tCO2 real)

- Description: p x log ratio ^ convergence exponent (Settings); fast estimate if no price or no log ratio
- Legacy: legacy PricesAdjustedByErrorFactor (row 1966)
- Rows: all,all
  - 2022-2041: `ets.next(t) = IF(OR(ets.p(t)<=0,ets.lr[f,s](t)=0),ets.est(t),ets.p(t)*ets.lr[f,s](t)^Settings[ETS: convergence exponent of the next-price propos])`

**E1073. `bco2.chk`: Check: baseline CO2 data minus scenario 1 CO2 (0 = data up to date)** (MtCO2)

- Description: SUM(bco2) - co2.ref
- Legacy: new
- Rows: all,all
  - 2022-2041: `bco2.chk(t) = SUM(bco2[17 rows](t))-co2.ref[f,s](t)`

**E1074. `co2.chk`: Check: CO2 total minus sectors and power, and minus the fuels (should be 0)** (MtCO2)

- Description: Check
- Legacy: new
- Rows: all,all
  - 2022-2041: `co2.chk(t) = ABS(co2[f,s](t)-SUM(co2[5 rows](t)))+ABS(co2[f,s](t)-SUM(co2[9 rows](t)))`

**E1075. `cchg`: CO2 from fuel combustion: change against scenario 1** (MtCO2)

- Description: Row of section 13 - scenario 1
- Legacy: legacy F13, v0.3.14
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all, all,tra, all,bld, all,ind, ... (14 rows)
  - 2022-2041: `cchg(t) = co2[f,s](t)-INDEX(co2[f,s](..t),row10(t))`

**E1076. `co2.grid`: Grid emission intensity** (tCO2 per MWh)

- Description: co2.pow x Million / (gtot x HoursYr); SAFEDIV
- Legacy: legacy Mitigation row 6582, v0.3.14
- Rows: all,pow
  - 2022-2041: `co2.grid(t) = IF(gtot(t)*HoursYr=0,0,co2[f,s](t)*Million/(gtot(t)*HoursYr))`

**E1077. `kaya`: Kaya identity: population (mn), GDP per capita (thousand USD), total primary energy supply (ktoe), energy intensity (ktoe per USD bn), carbon intensity (ktCO2 per ktoe)** (mixed)

- Description: Baseline real GDP (header), total primary energy supply = fuel use incl. power generation (section 11) + primary electricity (pe of nuclear and renewables, section 3; v0.3.18), total CO2 incl. processes (ghg.g.co2); SAFEDIV
- Legacy: legacy rows 18877-18885 (F14), v0.3.14
- Rows: pop,all
  - 2022-2041: `kaya(t) = IF(Thousand=0,0,pop[all,s](t)/Thousand)`
- Rows: gpc,all
  - 2022-2041: `kaya(t) = IF(kaya[pop,s](t)=0,0,gdp.usd[all,s](t)/kaya[pop,s](t))`
- Rows: tpes,all
  - 2022-2041: `kaya(t) = ener[all,s](t)+SUM(pe[5 rows](t))`
- Rows: ei,all
  - 2022-2041: `kaya(t) = IF(gdp.usd[all,s](t)=0,0,kaya[tpes,s](t)/gdp.usd[all,s](t))`
- Rows: ci,all
  - 2022-2041: `kaya(t) = IF(kaya[tpes,s](t)=0,0,ghg[co2,s](t)*Thousand/kaya[tpes,s](t))`

**E1078. `kidx`: Kaya identity against the base year (base year = 1); chk = product of the four factors = CO2 index** (index)

- Description: Level / level of the base year (scenario 1)
- Legacy: legacy rows 18887-18893 (F14), v0.3.14
- Rows: pop,all, gpc,all, ei,all, ci,all
  - 2022-2041: `kidx(t) = IF(kaya[f,s](2022)=0,0,kaya[f,s](t)/kaya[f,s](2022))`
- Rows: gdp,all
  - 2022-2041: `kidx(t) = IF(gdp.usd[all,s](2022)=0,0,gdp.usd[all,s](t)/gdp.usd[all,s](2022))`
- Rows: co2,all
  - 2022-2041: `kidx(t) = IF(ghg[f,s](2022)=0,0,ghg[f,s](t)/ghg[f,s](2022))`
- Rows: chk,all
  - 2022-2041: `kidx(t) = kidx[pop,s](t)*kidx[gpc,s](t)*kidx[ei,s](t)*kidx[ci,s](t)`

**E1079. `co2.chg`: Change in CO2 emissions vs scenario 1** (MtCO2)

- Description: co2 - co2.ref
- Legacy: new
- Rows: all,all
  - 2022-2041: `co2.chg(t) = co2[f,s](t)-co2.ref[f,s](t)`

### 14

**E1080. `pop`: Population** (thousand)

- Description: UN World Population Prospects (sheet UNPop)
- Legacy: legacy Mitigation row 2428 (legacy growth path differs: see LegacyDiff)
- Changes against legacy: LD45, L20 (section B)
- Rows: all,all
  - 2022-2041: `pop(t) = INDEX(PopVal,MATCH(CtryCode,PopKey,0),MATCH(year,PopYear,0))`
- Rows: all,all
  - 2022-2041: `pop(t) = pop[f,s](t)`

**E1081. `pop.g`: Population growth** (%)

- Description: pop / pop(t-1) - 1
- Legacy: legacy Mitigation rows 481, 7557
- Changes against legacy: LD45 (section B)
- Rows: all,all
  - 2022: `pop.g(t) = pop[f,s](t)/INDEX(PopVal,MATCH(CtryCode,PopKey,0),MATCH(year-1,PopYear,0))-1`
  - 2023-2041: `pop.g(t) = pop[f,s](t)/pop[f,s](t-1)-1`

**E1082. `gdppc.g`: GDP per capita growth** (%)

- Description: (1 + real GDP growth) / (1 + population growth) - 1
- Legacy: legacy Mitigation rows 2430, 7556
- Rows: all,all
  - 2022-2041: `gdppc.g(t) = (1+gdp.pos.pct(t))/(1+pop.g[f,s](t))-1`

**E1083. `ghg.h`: Row of the year on sheet GHGs (0 = no inventory value)** (row)

- Description: MATCH(country|year)
- Legacy: new
- Rows: all,all
  - 2022-2041: `ghg.h(t) = IFERROR(MATCH(CtryCode&"|"&year,GHGKey,0),0)`

**E1084. `ghg.m`: Mitigation effort in non-energy sectors (multiplier)** (factor)

- Description: Energy CO2 of the scenario / scenario 1 if AdditionMitigationPoliciesNonEnergy = Yes, else 1
- Legacy: legacy Mitigation rows 7542-7549
- Rows: all,all
  - 2022-2041: `ghg.m(t) = IF(AND(LEFT(AdditionMitigationPoliciesNonEnergy(t),3)="Yes",co2.ref[f,s](t)>0),co2[f,s](t)/co2.ref[f,s](t),1)`

**E1085. `ghg.gi`: Growth of industrial energy CO2** (%)

- Description: co2 industry / co2 industry (t-1) - 1
- Legacy: legacy Mitigation row 7553
- Rows: all,ind
  - 2022: `ghg.gi(t) = 0`
  - 2023-2041: `ghg.gi(t) = IF(co2[f,s](t-1)=0,0,co2[f,s](t)/co2[f,s](t-1)-1)`

**E1086. `ghg.dr`: Growth factor of a non-energy category** (factor)

- Description: (1 + gdppc.g)^el x (1 + pop.g)^el x ghg.m / ghg.m(t-1)
- Legacy: legacy Mitigation rows 7571-7588
- Rows: all,agr, all,wst, all,oth
  - 2022: `ghg.dr(t) = 1`
  - 2023-2041: `ghg.dr(t) = (1+gdppc.g[f,all](t))^<elasticity to GDP per capita (Manual inputs row 327)>*(1+pop.g[f,all](t))^<elasticity to population (Manual inputs row 326)>*ghg.m[f,all](t)/ghg.m[f,all](t-1)`
  - Parameters: `<elasticity to GDP per capita (Manual inputs row 327)>` = `N(INDEX(GhgElInc,MATCH("Agriculture",GhgElCat,0)))`; `<elasticity to population (Manual inputs row 326)>` = `N(INDEX(GhgElPop,MATCH("Agriculture",GhgElCat,0)))`

**E1087. `ghg.invb`: Inventory values in the last inventory year (D energy CH4, E agriculture CH4, F waste CH4, G LULUCF CO2)** (Mt CO2e)

- Description: Sheet GHGs, year GHGYear
- Legacy: legacy Mitigation rows 839-881
- Rows: all,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<energy CH4 (Mt CO2e)>` = `INDEX(GHGVal,MATCH(CtryCode&"|"&GHGYear,GHGKey,0),MATCH("enr.ch4",GHGCol,0))`; `<agriculture CH4 (Mt CO2e)>` = `INDEX(GHGVal,MATCH(CtryCode&"|"&GHGYear,GHGKey,0),MATCH("agr.ch4",GHGCol,0))`; `<waste CH4 (Mt CO2e)>` = `INDEX(GHGVal,MATCH(CtryCode&"|"&GHGYear,GHGKey,0),MATCH("wst.ch4",GHGCol,0))`; `<LULUCF CO2 (Mt CO2e)>` = `INDEX(GHGVal,MATCH(CtryCode&"|"&GHGYear,GHGKey,0),MATCH("lucf.co2",GHGCol,0))`

**E1088. `ch4.src`: Methane source: share of its inventory category (D input share, E activity in GHGYear, F weight, G share)** (share)

- Description: Fossil: weight = MIN(MethShareCap x activity share, input share), normalised; livestock, rice: input share; waste: 1
- Legacy: legacy Mitigation rows 893-908
- Rows: og,all, dg,all, cm,all, bm,all, liv,all, ric,all, wst,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<input share (CH4Inputs)>` = `IFERROR(INDEX(MethVal,MATCH(CtryCode&"|oil",MethKey,0),MATCH("per_upstream_og",MethCol,0)),0)`; `<activity in the base year (data)>` = `<base production (Balances, ktoe) of ch4.prd[oil,s]>+<base production (Balances, ktoe) of ch4.prd[nga,s]>`; `<weight>` = `MIN(MethShareCap*<activity in the base year (data)>/SUM(ch4.src[4 rows](E)),<input share (CH4Inputs)>)`; `<share of the inventory>` = `IF(SUM(ch4.src[4 rows](F))=0,0,<weight>/SUM(ch4.src[4 rows](F)))`

**E1089. `ch4.wd`: World demand of the fuel (global demand scenario, MTOE)** (MTOE)

- Description: Prices_int rows 323-333 (GlobalEnergyDemand of scenario 1; legacy CHOOSE: the 3rd and 4th options both read the Net Zero row) (v0.5.6)
- Legacy: legacy rows 717-719
- Rows: oil,all, coa,all, nga,all
  - 2022-2041: `ch4.wd(t) = INDEX(WDData,<position of the fuel (Prices_int)>+WDIdx-1,MATCH(year,WDYear,0))`
  - Parameters: `<position of the fuel (Prices_int)>` = `MATCH("Oil",Prices_int!F323:F333,0)`

**E1090. `ch4.fk`: Methane fee per ktoe produced (after abatement)** (USD/ktoe)

- Description: fee per t CH4 x t CH4 per ktoe after abatement (v0.5.6)
- Legacy: legacy rows 6112, 6129
- Rows: og,all, cm,all
  - 2022: `ch4.fk(t) = 0`
  - 2023-2041: `ch4.fk(t) = IF(<base production (ktoe)>=0,0,mfee(t)*<GWP of ch4.abt[f,s]>*<fee applies (1 = yes; Settings, legacy Manual inputs J196-J200) of ch4.abt[f,s]>*tPerKt*<emissions in GHGYear (kt CH4) of ch4.em[f,s]>/<base production (ktoe)>*(1-ch4.abt[f,s](t)))`
  - Parameters: `<base production (ktoe)>` = `<base production (Balances, ktoe) of ch4.prd[oil,s]>+<base production (Balances, ktoe) of ch4.prd[nga,s]>`

**E1091. `ch4.pi`: Producer price index from the methane fee** (index)

- Description: 1 + change of the fee per unit / international price x pass-through (Manual inputs J194) (v0.5.6)
- Legacy: legacy rows 6137-6144
- Rows: oil,all, nga,all
  - 2022: `ch4.pi(t) = 1`
  - 2023-2041: `ch4.pi(t) = 1+(ch4.fk[og,s](t)-ch4.fk[og,s](t-1))/(gp[f,int](t)*<price units per ktoe>)*<pass-through (Manual inputs J194)>`
  - Parameters: `<price units per ktoe>` = `MethGJperKtoe/MethGJperBbl`; `<pass-through (Manual inputs J194)>` = `'Manual inputs'!J194`
- Rows: coa,all
  - 2022: `ch4.pi(t) = 1`
  - 2023-2041: `ch4.pi(t) = 1+(ch4.fk[cm,s](t)-ch4.fk[cm,s](t-1))/(gp[f,int](t)*<price units per ktoe>)*<pass-through (Manual inputs J194)>`
  - Parameters: `<price units per ktoe>` = `MethGJperKtoe/MethGJperT`; `<pass-through (Manual inputs J194)>` = `'Manual inputs'!J194`

**E1092. `ch4.prd`: Fuel production** (ktoe)

- Description: Balances production in the base year and the next; then previous x price index ^ elasticity (Manual inputs J190:J192) x world demand growth of the year before (v0.5.6, I66)
- Legacy: legacy rows 6146-6149
- Rows: oil,all, coa,all, nga,all
  - 2022-2041: `ch4.prd(t) = IF(year<=BaseYr+1,<base production (Balances, ktoe)>,ch4.prd[f,s](t-1)*ch4.pi[f,s](t)^<price elasticity of production>*ch4.wd[f,s](t-1)/ch4.wd[f,s](t-2))`
  - Parameters: `<base production (Balances, ktoe)>` = `INDEX(BalVal,MATCH(CtryCode&"|production",BalKey,0),MATCH("oop",BalFuel,0))`; `<price elasticity of production>` = `'Manual inputs'!J190`

**E1093. `ch4.act`: Methane source: activity** (ktoe or index)

- Description: Oil and gas, coal: production (sheet Balances); downstream gas, biomass: fuel use (section 11); livestock, rice, waste: index with income and population
- Legacy: legacy Mitigation rows 6146-6151, 6212-6214
- Changes against legacy: LD43, L18 (section B)
- Rows: og,all
  - 2022-2041: `ch4.act(t) = ch4.prd[oil,s](t)+ch4.prd[nga,s](t)`
  - Parameters: `<gas production / income elasticity (Manual inputs row 327)>` = `INDEX(BalVal,MATCH(CtryCode&"|production",BalKey,0),MATCH("nga",BalFuel,0))`; `<oil production / population elasticity (Manual inputs row 326)>` = `INDEX(BalVal,MATCH(CtryCode&"|production",BalKey,0),MATCH("oop",BalFuel,0))`
- Rows: dg,all
  - 2022-2041: `ch4.act(t) = ener[nga,s](t)`
- Rows: cm,all
  - 2022-2041: `ch4.act(t) = ch4.prd[coa,s](t)`
  - Parameters: `<gas production / income elasticity (Manual inputs row 327)>` = `INDEX(BalVal,MATCH(CtryCode&"|production",BalKey,0),MATCH("coa",BalFuel,0))`
- Rows: bm,all
  - 2022-2041: `ch4.act(t) = ener[bio,s](t)`
- Rows: liv,all, ric,all, wst,all
  - 2022: `ch4.act(t) = 1`
  - 2023-2041: `ch4.act(t) = ch4.act[f,s](t-1)*(1+gdppc.g[all,s](t))^<gas production / income elasticity (Manual inputs row 327)>*(1+pop.g[all,s](t))^<oil production / population elasticity (Manual inputs row 326)>`
  - Parameters: `<gas production / income elasticity (Manual inputs row 327)>` = `N(INDEX(GhgElInc,MATCH("Agriculture",GhgElCat,0)))`; `<oil production / population elasticity (Manual inputs row 326)>` = `N(INDEX(GhgElPop,MATCH("Agriculture",GhgElCat,0)))`

**E1094. `ch4.abc`: Methane source: abatement-curve coefficients, country and average (CH4Inputs)** (coefficient)

- Description: CH4Inputs avg_pow_a, avg_pow_b of ISO|tier and of AVG|tier (I152, v1.0.2)
- Legacy: legacy Mitigation L6084:M6084 and the rows of the other sources (country, else Average)
- Rows: og,all, dg,all, cm,all, bm,all, liv,all, ric,all, wst,all
  - No values in the year columns: an input row left blank (or a row of parameters only, columns D:G)
  - Parameters: `<curve a, country>` = `IFERROR(INDEX(MethVal,MATCH(CtryCode&"|oil",MethKey,0),MATCH("avg_pow_a",MethCol,0)),0)`; `<curve b, country>` = `IFERROR(INDEX(MethVal,MATCH(CtryCode&"|oil",MethKey,0),MATCH("avg_pow_b",MethCol,0)),0)`; `<curve a, average (AVG)>` = `IFERROR(INDEX(MethVal,MATCH("AVG|oil",MethKey,0),MATCH("avg_pow_a",MethCol,0)),0)`; `<curve b, average (AVG)>` = `IFERROR(INDEX(MethVal,MATCH("AVG|oil",MethKey,0),MATCH("avg_pow_b",MethCol,0)),0)`

**E1095. `ch4.abt`: Methane source: abatement share from the methane fee** (share)

- Description: MIN(1, MAX(0, a x (fee x GWP)^b)), curves of sheet CH4Inputs
- Legacy: legacy Mitigation rows 6104-6106, 6126, 6182-6206
- Changes against legacy: LD43, LD46, L21 (section B)
- Rows: og,all, dg,all, cm,all, bm,all, liv,all, ric,all, wst,all
  - 2022-2041: `ch4.abt(t) = MIN(1,MAX(0,<curve a (country, else average)>*(mfee(t)*<GWP>*<fee applies (1 = yes; Settings, legacy Manual inputs J196-J200)>)^<curve b (country, else average)>))`
  - Parameters: `<curve a (country, else average)>` = `IF(<curve a, country of ch4.abc[f,s]>=0,<curve a, average (AVG) of ch4.abc[f,s]>,<curve a, country of ch4.abc[f,s]>)`; `<curve b (country, else average)>` = `IF(<curve b, country of ch4.abc[f,s]>=0,<curve b, average (AVG) of ch4.abc[f,s]>,<curve b, country of ch4.abc[f,s]>)`; `<GWP>` = `GWPCH4F`; `<fee applies (1 = yes; Settings, legacy Manual inputs J196-J200)>` = `IF(LEFT(MFeeFF,3)="Yes",1,0)`

**E1096. `ch4.int`: Methane source: intensity index (autonomous technological improvement)** (index)

- Description: INTDECLINE: (1 - rate)^MAX(0, year - GHGYear); rate: Manual inputs J185 oil and gas (also downstream gas and biomass, I141), J186 coal, J187 agriculture, J188 waste (v0.9.0, R8.6)
- Legacy: legacy Mitigation rows 6077-6079, 6103, 6159, 6171, 6183 (Manual inputs J185:J188)
- Rows: og,all, dg,all, cm,all, bm,all, liv,all, ric,all, wst,all
  - 2022-2041: `ch4.int(t) = (1-<rate of decline (% per year; Manual inputs J185:J188)>)^MAX(0,year-GHGYear)`
  - Parameters: `<rate of decline (% per year; Manual inputs J185:J188)>` = `'Manual inputs'!J185`

**E1097. `ch4.em`: Methane source: emissions** (kt CH4)

- Description: base-year emissions x activity / activity in GHGYear x intensity index x (1 - abatement) (v0.9.0, R8.7; L135 fixed: livestock, rice and waste also decline)
- Legacy: legacy Mitigation rows 6154-6165, 6203, 6206, 6212, 6217-6226
- Changes against legacy: LD43, L18 (section B)
- Rows: og,all, dg,all, cm,all, bm,all, liv,all, ric,all, wst,all
  - 2022-2041: `ch4.em(t) = IF(<activity in the base year (data) of ch4.src[f,s]>=0,0,<emissions in GHGYear (kt CH4)>*ch4.act[f,s](t)/<activity in the base year (data) of ch4.src[f,s]>*ch4.int[f,s](t)*(1-ch4.abt[f,s](t)))`
  - Parameters: `<emissions in GHGYear (kt CH4)>` = `<energy CH4 (Mt CO2e) of ghg.invb[all,s]>*<share of the inventory of ch4.src[f,s]>*ktPerMt/GWPCH4F`

**E1098. `ch4.c`: CH4 from fuel combustion by sector** (kt CH4)

- Description: Sum of the ch4 rows (sectors 5-8; power: section 14)
- Legacy: legacy Mitigation rows 7295-7307
- Rows: all,tra, all,bld, all,ind, all,oen
  - 2022-2041: `ch4.c(t) = SUMIF(block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(A),"ch4",block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(t))`
- Rows: all,pow
  - 2022-2041: `ch4.c(t) = SUM(ch4[4 rows](t))`
- Rows: all,all
  - 2022-2041: `ch4.c(t) = SUM(ch4.c[5 rows](t))`

**E1099. `ch4.sup`: CH4 from fossil fuel supply (oil and gas, downstream gas, coal mining, biomass)** (kt CH4)

- Description: Sum of the fossil methane sources
- Legacy: legacy Mitigation row 6168
- Rows: all,all
  - 2022-2041: `ch4.sup(t) = SUM(ch4.em[4 rows](t))`

**E1100. `ghg.k`: Calibration of energy CH4 to the inventory** (factor)

- Description: Inventory energy CH4 / modelled (combustion + supply) in GHGYear
- Legacy: legacy Mitigation row 7562 (B)
- Rows: ch4,enr
  - 2022-2041: `ghg.k(t) = IF((<combustion CH4 in GHGYear (kt; scenario 1, stored)>+<supply CH4 in GHGYear (kt; scenario 1, stored)>)*GWPCH4F/ktPerMt=0,0,<inventory energy CH4 (Mt CO2e)>/((<combustion CH4 in GHGYear (kt; scenario 1, stored)>+<supply CH4 in GHGYear (kt; scenario 1, stored)>)*GWPCH4F/ktPerMt))`
  - Parameters: `<inventory energy CH4 (Mt CO2e)>` = `<energy CH4 (Mt CO2e) of ghg.invb[all,all]>`; `<combustion CH4 in GHGYear (kt; scenario 1, stored)>` = `INDEX(BaseCO2Val,MATCH(CtryCode&"|ch4c",BaseCO2Key,0),MATCH(GHGYear,BaseCO2Year,0))`; `<supply CH4 in GHGYear (kt; scenario 1, stored)>` = `INDEX(BaseCO2Val,MATCH(CtryCode&"|ch4sup",BaseCO2Key,0),MATCH(GHGYear,BaseCO2Year,0))`

**E1101. `ghg.flr`: CO2 from flaring abated oil and gas methane** (Mt CO2)

- Description: FlareCO2perCH4 x flared share x abated oil and gas CH4
- Legacy: legacy Mitigation row 6155 (counted as CH4 there)
- Changes against legacy: LD44, L19 (section B)
- Rows: co2,enr
  - 2022-2041: `ghg.flr(t) = IF(<activity in the base year (data) of ch4.src[og,all]>=0,0,FlareCO2perscenarioName(scenario 4)*<flared share (CH4Inputs)>*<emissions in GHGYear (kt CH4) of ch4.em[og,all]>*ch4.act[og,all](t)/<activity in the base year (data) of ch4.src[og,all]>*ch4.abt[og,all](t)/ktPerMt)`
  - Parameters: `<flared share (CH4Inputs)>` = `IFERROR(INDEX(MethVal,MATCH(CtryCode&"|oil",MethKey,0),MATCH("per_flare",MethCol,0)),0)`

**E1102. `ghg`: GHG emissions** (Mt CO2e)

- Description: Inventory while it has the year, then projected (section 14 note)
- Legacy: legacy Mitigation rows 7561-7640
- Changes against legacy: LD36 (section B)
- Rows: co2,enr
  - 2022-2041: `ghg(t) = co2[all,all](t)+ghg.flr[f,s](t)`
  - Parameters: `<inventory column (sheet GHGs)>` = `MATCH("enr.co2",GHGCol,0)`
- Rows: ch4,enr
  - 2022-2041: `ghg(t) = ghg.k[f,s](t)*(ch4.c[all,all](t)+ch4.sup[all,all](t))*GWPCH4F/ktPerMt`
  - Parameters: `<inventory column (sheet GHGs)>` = `MATCH("enr.ch4",GHGCol,0)`
- Rows: n2o,enr
  - 2022: `ghg(t) = IF(ghg.h[all,all](t)>0,INDEX(GHGVal,ghg.h[all,all](t),<inventory column (sheet GHGs)>),0)`
  - 2023-2041: `ghg(t) = IF(ghg.h[all,all](t)>0,INDEX(GHGVal,ghg.h[all,all](t),<inventory column (sheet GHGs)>),ghg[f,s](t-1)*IF(co2[all,all](t-1)=0,1,co2[all,all](t)/co2[all,all](t-1)))`
  - Parameters: `<inventory column (sheet GHGs)>` = `MATCH("enr.n2o",GHGCol,0)`
- Rows: fga,enr, ch4,lucf, n2o,lucf, fga,lucf
  - 2022: `ghg(t) = IF(ghg.h[all,all](t)>0,INDEX(GHGVal,ghg.h[all,all](t),<inventory column (sheet GHGs)>),0)`
  - 2023-2041: `ghg(t) = IF(ghg.h[all,all](t)>0,INDEX(GHGVal,ghg.h[all,all](t),<inventory column (sheet GHGs)>),ghg[f,s](t-1))`
  - Parameters: `<inventory column (sheet GHGs)>` = `MATCH("enr.fga",GHGCol,0)`
- Rows: co2,ipr, ch4,ipr, n2o,ipr, fga,ipr
  - 2022: `ghg(t) = IF(ghg.h[all,all](t)>0,INDEX(GHGVal,ghg.h[all,all](t),<inventory column (sheet GHGs)>),0)`
  - 2023-2041: `ghg(t) = IF(ghg.h[all,all](t)>0,INDEX(GHGVal,ghg.h[all,all](t),<inventory column (sheet GHGs)>),ghg[f,s](t-1)*(1+IF(LEFT(IndustrialProcessEmissionsScaleEner(t),3)="Yes",ghg.gi[all,ind](t),0)))`
  - Parameters: `<inventory column (sheet GHGs)>` = `MATCH("ipr.co2",GHGCol,0)`
- Rows: co2,agr, n2o,agr, fga,agr, co2,wst, n2o,wst, fga,wst, co2,oth, ch4,oth, n2o,oth, fga,oth
  - 2022: `ghg(t) = IF(ghg.h[all,all](t)>0,INDEX(GHGVal,ghg.h[all,all](t),<inventory column (sheet GHGs)>),0)`
  - 2023-2041: `ghg(t) = IF(ghg.h[all,all](t)>0,INDEX(GHGVal,ghg.h[all,all](t),<inventory column (sheet GHGs)>),ghg[f,s](t-1)*ghg.dr[all,s](t))`
  - Parameters: `<inventory column (sheet GHGs)>` = `MATCH("agr.co2",GHGCol,0)`
- ... and 14 further row patterns (see the workbook)

**E1103. `ghg.inc`: GHG emissions including LULUCF** (Mt CO2e)

- Description: ghg + LULUCF
- Legacy: legacy Mitigation row 7595
- Rows: all,all
  - 2022-2041: `ghg.inc(t) = ghg[f,s](t)+ghg[f,lucf](t)`

**E1104. `ghg.ref`: GHG emissions, scenario 1 (same year)** (Mt CO2e)

- Description: Lookup
- Legacy: new
- Rows: all,all
  - 2022-2041: `ghg.ref(t) = INDEX(ghg[f,s](..t),MATCH(year,year(..t),0))`

**E1105. `ghg.pct`: Change in GHG emissions vs scenario 1** (%)

- Description: ghg / ghg.ref - 1
- Legacy: new
- Rows: all,all
  - 2022-2041: `ghg.pct(t) = IF(ghg.ref[f,s](t)=0,0,ghg[f,s](t)/ghg.ref[f,s](t)-1)`

**E1106. `ch4.rev`: Revenue from the methane fee** (USD m real)

- Description: CH4 (kt) x GWP x fee x tPerKt / USDperM
- Legacy: legacy Mitigation rows 6157-6169
- Rows: all,all
  - 2022-2041: `ch4.rev(t) = SUMPRODUCT(ch4.em[7 rows](t),ch4.abt[7 rows](F),ch4.abt[7 rows](G))*mfee(t)*tPerKt/USDperM`

**E1107. `ch4.emf`: Methane of a source for the fiscal space (kt): as ch4.em, with the scenario-1 activity for downstream gas and biomass use** (kt CH4)

- Description: METHSOURCE(base kt, ch4bs, base activity, abatement); other sources = ch4.em
- Legacy: new (v0.6.2, I47)
- Rows: og,all, cm,all, liv,all, ric,all, wst,all
  - 2022-2041: `ch4.emf(t) = ch4.em[f,s](t)`
- Rows: dg,all
  - 2022-2041: `ch4.emf(t) = IF(<activity in the base year (data) of ch4.src[f,s]>=0,0,<emissions in GHGYear (kt CH4) of ch4.em[f,s]>*ch4bs[all,dg](t)/<activity in the base year (data) of ch4.src[f,s]>*ch4.int[f,s](t)*(1-ch4.abt[f,s](t)))`
- Rows: bm,all
  - 2022-2041: `ch4.emf(t) = IF(<activity in the base year (data) of ch4.src[f,s]>=0,0,<emissions in GHGYear (kt CH4) of ch4.em[f,s]>*ch4bs[all,bm](t)/<activity in the base year (data) of ch4.src[f,s]>*ch4.int[f,s](t)*(1-ch4.abt[f,s](t)))`

**E1108. `ch4.revf`: Memo: methane fee revenue on the stored scenario-1 activity (v0.6.2-v0.8.5 fiscal space; not used since v0.9.0, I47)** (USD m real)

- Description: FEEREV over ch4.emf
- Legacy: new (v0.6.2, I47)
- Rows: all,all
  - 2022-2041: `ch4.revf(t) = SUMPRODUCT(ch4.emf[7 rows](t),ch4.abt[7 rows](F),ch4.abt[7 rows](G))*mfee(t)*tPerKt/USDperM`

**E1109. `ch4bs.chk`: Check: stored scenario-1 methane activity minus own activity in scenario 1 (0 = data up to date)** (ktoe)

- Description: ABS(ch4bs - ch4.act), scenario 1 only
- Legacy: new (v0.6.2, I47)
- Rows: all,all
  - 2022-2041: `ch4bs.chk(t) = IF(scenario(t)=1,ABS(ch4bs[f,dg](t)-ch4.act[dg,s](t))+ABS(ch4bs[f,bm](t)-ch4.act[bm,s](t)),0)`

**E1110. `gchg`: GHG emissions: change against scenario 1 by inventory category and gas** (Mt CO2e)

- Description: Row of section 14 - scenario 1
- Legacy: legacy F12 rows 18229-18264, v0.3.14
- Rows: all,enr, all,ipr, all,agr, all,lucf, all,wst, all,oth, co2,all, ch4,all, n2o,all, fga,all
  - 2022-2041: `gchg(t) = ghg[f,s](t)-INDEX(ghg[f,s](..t),row10(t))`

**E1111. `ghg.enrp`: Energy-related GHGs including the forcing of the local pollutants** (Mt CO2e)

- Description: ghg.c.enr + apf.all
- Legacy: legacy rows 18310, 18321 (F12), v0.3.14
- Rows: all,enr
  - 2022-2041: `ghg.enrp(t) = ghg[f,s](t)+apf[f,all](t)`

**E1112. `ndc.key`: NDC: country|submission key (MTInputs NDCs: First round, Second round, else Latest*)** (text)

- Description: CtryCode & | & round
- Legacy: legacy NDCs F5, rows 28-35
- Rows: all,all
  - 2022-2041: `ndc.key(t) = CtryCode&"|"&IF(OR(NDCSub="First round",NDCSub="Second round"),NDCSub,"Latest*")`

**E1113. `ndc.typ`: NDC: type (BAU, Fixed, Historical, Intensity, Unquantifiable)** (text)

- Description: sheet NDCs (Unquantifiable if not found)
- Legacy: legacy NDCs E7
- Rows: all,all
  - 2022-2041: `ndc.typ(t) = IFERROR(INDEX(NDCTab,MATCH(ndc.key[f,s](t),NDCKey,0),MATCH("type",NDCHdr,0)),"Unquantifiable")`

**E1114. `ndc.k`: NDC: type number (position in NDCTypes)** (number)

- Description: MATCH(type, NDCTypes); not found: Unquantifiable
- Legacy: legacy row 18489 G
- Rows: all,all
  - 2022-2041: `ndc.k(t) = IFERROR(MATCH(ndc.typ[f,s](t),NDCTypes,0),COUNTA(NDCTypes))`

**E1115. `ndc.ty`: NDC: target year (ty1, ty2 as given; all: the one used, at most NDCYrCap)** (year)

- Description: ty2 if NDCTargetYear is not Main* and ty2 is given, else ty1
- Legacy: legacy NDCs E11, row 18405
- Rows: ty1,all
  - 2022-2041: `ndc.ty(t) = IFERROR(INDEX(NDCTab,MATCH(ndc.key[all,s](t),NDCKey,0),MATCH("ty1",NDCHdr,0)),"")`
- Rows: ty2,all
  - 2022-2041: `ndc.ty(t) = IFERROR(INDEX(NDCTab,MATCH(ndc.key[all,s](t),NDCKey,0),MATCH("ty2",NDCHdr,0)),"")`
- Rows: all,all
  - 2022-2041: `ndc.ty(t) = IFERROR(MIN(NDCYrCap,IF(ndc.alt[f,s](t),ndc.ty[ty2,s](t),ndc.ty[ty1,s](t))),NDCYrCap)`

**E1116. `ndc.alt`: NDC: second target year used** (TRUE/FALSE)

- Description: NDCTargetYear <> Main* and ty2 > 0
- Legacy: legacy NDCs F6
- Rows: all,all
  - 2022-2041: `ndc.alt(t) = AND(NDCTyr<>"Main*",N(ndc.ty[ty2,s](t))>0)`

**E1117. `ndc.ref`: NDC: reference year (Historical, Intensity)** (year)

- Description: sheet NDCs
- Legacy: legacy NDCs E8, row 18404
- Rows: all,all
  - 2022-2041: `ndc.ref(t) = IFERROR(INDEX(NDCTab,MATCH(ndc.key[f,s](t),NDCKey,0),MATCH("ref",NDCHdr,0)),"")`

**E1118. `ndc.x`: NDC: target value as given (u unconditional, c conditional; reduction negative, Fixed in Mt CO2e)** (text)

- Description: sheet NDCs columns u1/c1 or u2/c2; blank if none
- Legacy: legacy NDCs E13-E14, rows 18406-18407
- Rows: u,all
  - 2022-2041: `ndc.x(t) = IFERROR(INDEX(NDCTab,MATCH(ndc.key[all,s](t),NDCKey,0),MATCH(IF(ndc.alt[all,s](t),"u2","u1"),NDCHdr,0)),"")&""`
- Rows: c,all
  - 2022-2041: `ndc.x(t) = IFERROR(INDEX(NDCTab,MATCH(ndc.key[all,s](t),NDCKey,0),MATCH(IF(ndc.alt[all,s](t),"c2","c1"),NDCHdr,0)),"")&""`

**E1119. `ndc.lu`: NDC: LULUCF included or excluded** (text)

- Description: sheet NDCs
- Legacy: legacy row 18408
- Rows: all,all
  - 2022-2041: `ndc.lu(t) = IFERROR(INDEX(NDCTab,MATCH(ndc.key[f,s](t),NDCKey,0),MATCH("lulucf",NDCHdr,0)),"")`

**E1120. `ndc.gas`: NDC: gases (CO2 or GHGs)** (text)

- Description: CO2 if the gases are CO2 only
- Legacy: legacy row 18409
- Rows: all,all
  - 2022-2041: `ndc.gas(t) = IF(IFERROR(INDEX(NDCTab,MATCH(ndc.key[f,s](t),NDCKey,0),MATCH("gases",NDCHdr,0)),"")="CO2","CO2","GHGs")`

**E1121. `ndc.co2`: CO2 on the NDC LULUCF basis** (Mt CO2)

- Description: ghg.g.co2 + LULUCF CO2 if included
- Legacy: legacy rows 18547, 18566
- Rows: all,all
  - 2022-2041: `ndc.co2(t) = ghg[co2,s](t)+IF(ndc.lu[f,s](t)="Includes",ghg[co2,lucf](t),0)`

**E1122. `ndc.bs`: Emissions on the NDC basis (gases, LULUCF)** (Mt CO2e)

- Description: CO2: ndc.co2; GHGs: ghg.inc or ghg.all
- Legacy: legacy rows 18234-18235
- Rows: all,all
  - 2022-2041: `ndc.bs(t) = IF(ndc.gas[f,s](t)="CO2",ndc.co2[f,s](t),IF(ndc.lu[f,s](t)="Includes",ghg.inc[f,s](t),ghg[f,s](t)))`

**E1123. `ndc.bty`: Modelled BAU (scenario 1) on the NDC basis in the target year** (Mt CO2e)

- Description: scenario-1 ndc.bs in ndc.ty
- Legacy: legacy row 18421
- Rows: all,all
  - 2022-2041: `ndc.bty(t) = IFERROR(INDEX(ndc.bs[f,s](2022..2041),MATCH(ndc.ty[f,s](t),year(2022..2041),0)),"N/A")`

**E1124. `ndc.bi`: Modelled BAU (scenario 1) GHGs incl. LULUCF in the target year** (Mt CO2e)

- Description: scenario-1 ghg.inc in ndc.ty
- Legacy: legacy row 18421 G
- Rows: all,all
  - 2022-2041: `ndc.bi(t) = IFERROR(INDEX(ghg.inc[f,s](2022..2041),MATCH(ndc.ty[f,s](t),year(2022..2041),0)),"N/A")`

**E1125. `ndc.hk`: Historical emissions key (group|reference year, sheet GHGHist)** (text)

- Description: exc, inc or co2 & | & ndc.ref
- Legacy: legacy rows 884-889
- Rows: all,all
  - 2022-2041: `ndc.hk(t) = IF(ndc.gas[f,s](t)="CO2","co2|",IF(ndc.lu[f,s](t)="Includes","inc|","exc|"))&ndc.ref[f,s](t)`

**E1126. `ndc.hh`: Historical emissions on the NDC basis in the reference year** (Mt CO2e)

- Description: sheet GHGHist
- Legacy: legacy rows 885-889
- Rows: all,all
  - 2022-2041: `ndc.hh(t) = IFERROR(INDEX(GHHTab,MATCH(CtryCode,GHHIso,0),MATCH(ndc.hk[f,s](t),GHHHdr,0)),"N/A")`

**E1127. `ndc.hc`: GHGs inventory column of the NDC basis (v0.6.1, I95)** (text)

- Description: texc or tinc & .tot or .co2
- Legacy: new (v0.6.1, I95)
- Rows: all,all
  - 2022-2041: `ndc.hc(t) = IF(ndc.lu[f,s](t)="Includes","tinc","texc")&IF(ndc.gas[f,s](t)="CO2",".co2",".tot")`

**E1128. `ndc.hv`: Inventory emissions on the NDC basis in the reference year (sheet GHGs, 2021-2024; v0.6.1, I95)** (Mt CO2e)

- Description: sheet GHGs
- Legacy: new (v0.6.1, I95)
- Rows: all,all
  - 2022-2041: `ndc.hv(t) = IFERROR(INDEX(GHGVal,MATCH(CtryCode&"|"&ndc.ref[f,s](t),GHGKey,0),MATCH(ndc.hc[f,s](t),GHGCol,0)),"N/A")`

**E1129. `ndc.h`: Emissions on the NDC basis in the reference year** (Mt CO2e)

- Description: scenario 1 if the year is modelled, else the GHGs inventory (ndc.hv), else GHGHist (ndc.hh)
- Legacy: legacy rows 18446-18447, 18464 (v0.6.1: + inventory, I95)
- Rows: all,all
  - 2022-2041: `ndc.h(t) = IFERROR(INDEX(ndc.bs[f,s](2022..2041),MATCH(ndc.ref[f,s](t),year(2022..2041),0)),IF(ISNUMBER(ndc.hv[f,s](t)),ndc.hv[f,s](t),ndc.hh[f,s](t)))`

**E1130. `ndc.gdp`: Real GDP in the reference (ref) or target (ty) year** (USD bn)

- Description: WEO gdp_usd
- Legacy: legacy rows 18466-18467 (fixed: L123)
- Rows: ref,all
  - 2022-2041: `ndc.gdp(t) = IFERROR(INDEX(WEOData,MATCH(CtryCode&".NGDP_R.A",WEOCode,0),MATCH(ndc.ref[all,s](t),WEOYr,0)),"N/A")`
- Rows: ty,all
  - 2022-2041: `ndc.gdp(t) = IFERROR(INDEX(WEOData,MATCH(CtryCode&".NGDP_R.A",WEOCode,0),MATCH(ndc.ty[all,s](t),WEOYr,0)),"N/A")`

**E1131. `ndc.hi`: Intensity NDC: reference-year emissions x target-year GDP / reference-year GDP** (Mt CO2e)

- Description: ndc.h / ndc.gdp.ref x ndc.gdp.ty
- Legacy: legacy rows 18468-18473
- Rows: all,all
  - 2022-2041: `ndc.hi(t) = IFERROR(ndc.h[f,s](t)/ndc.gdp[ref,s](t)*ndc.gdp[ty,s](t),"N/A")`

**E1132. `ndc.f`: NDC: 1 + target value (N/A if none)** (factor)

- Description: 1 + ndc.x
- Legacy: legacy rows 18406-18407
- Rows: u,all, c,all
  - 2022-2041: `ndc.f(t) = IFERROR(1+VALUE(ndc.x[f,s](t)),"N/A")`

**E1133. `ndc.lv`: NDC target level on its basis in the target year** (Mt CO2e)

- Description: CHOOSE(type: BAU bty x f; Fixed x; Historical h x f; Intensity hi x f; Unquantifiable bty)
- Legacy: legacy rows 18425, 18435, 18452, 18473 (fixed: L119-L122)
- Rows: u,all, c,all
  - 2022-2041: `ndc.lv(t) = IFERROR(CHOOSE(ndc.k[all,s](t),ndc.bty[all,s](t)*ndc.f[f,s](t),ndc.f[f,s](t)-1,ndc.h[all,s](t)*ndc.f[f,s](t),ndc.hi[all,s](t)*ndc.f[f,s](t),ndc.bty[all,s](t)),"N/A")`

**E1134. `ndc.r`: NDC: reduction against the modelled BAU (u, c, a average, sel chosen by Conditionality)** (share)

- Description: 1 - ndc.lv / ndc.bty; a: AVERAGE (0 if none); sel: MTInputs Conditionality, else a
- Legacy: legacy rows 18490-18492
- Rows: u,all, c,all
  - 2022-2041: `ndc.r(t) = IFERROR(1-ndc.lv[f,s](t)/ndc.bty[all,s](t),"N/A")`
- Rows: a,all
  - 2022-2041: `ndc.r(t) = IFERROR(AVERAGE(ndc.r[u,s](t),ndc.r[c,s](t)),0)`
- Rows: sel,all
  - 2022-2041: `ndc.r(t) = IFERROR(1*CHOOSE(MATCH(NDCCond,{"Unconditional","Conditional"},0),ndc.r[u,s](t),ndc.r[c,s](t)),ndc.r[a,s](t))`

**E1135. `ndc.lvl`: NDC target, GHGs incl. LULUCF** (Mt CO2e)

- Description: MIN(ndc.bi, ndc.bi x (1 - ndc.r))
- Legacy: legacy rows 18494-18496, 18511-18512
- Rows: u,all, c,all, sel,all
  - 2022-2041: `ndc.lvl(t) = IFERROR(MIN(ndc.bi[all,s](t),ndc.bi[all,s](t)*(1-ndc.r[f,s](t))),"N/A")`

**E1136. `ndc.idx`: NDC target against GHGs incl. LULUCF of the base year (scenario 1)** (ratio)

- Description: ndc.lvl / base-year ghg.inc
- Legacy: legacy rows 18497-18499, 18509-18510 (fixed: L120)
- Rows: u,all, c,all
  - 2022-2041: `ndc.idx(t) = IFERROR(ndc.lvl[f,s](t)/ghg.inc[all,s](2022),"N/A")`

**E1137. `ndc.bau`: GHGs incl. LULUCF, scenario 1 (same year)** (Mt CO2e)

- Description: Lookup
- Legacy: legacy row 18226
- Rows: all,all
  - 2022-2041: `ndc.bau(t) = INDEX(ghg.inc[f,s](..t),MATCH(year,year(..t),0))`

**E1138. `ndc.red`: Reduction of GHGs incl. LULUCF against scenario 1** (share)

- Description: 1 - ghg.inc / ndc.bau
- Legacy: legacy row 18516
- Rows: all,all
  - 2022-2041: `ndc.red(t) = IF(ndc.bau[f,s](t)=0,0,1-ghg.inc[f,s](t)/ndc.bau[f,s](t))`

**E1139. `ndc.gap`: Share of the NDC reduction achieved** (share)

- Description: ndc.red / ndc.r.sel (1 if no reduction is required)
- Legacy: legacy rows 18517-18518
- Rows: all,all
  - 2022-2041: `ndc.gap(t) = IF(ndc.r[sel,s](t)>0,ndc.red[f,s](t)/ndc.r[sel,s](t),1)`

**E1140. `ndc.over`: GHGs incl. LULUCF above the chosen NDC target** (Mt CO2e)

- Description: ghg.inc - ndc.lvl.sel
- Legacy: legacy G18501
- Rows: all,all
  - 2022-2041: `ndc.over(t) = IFERROR(ghg.inc[f,s](t)-ndc.lvl[sel,s](t),0)`

**E1141. `ghg.chg`: Change in GHG emissions vs scenario 1** (Mt CO2e)

- Description: ghg - ghg.ref
- Legacy: new
- Rows: all,all
  - 2022-2041: `ghg.chg(t) = ghg[f,s](t)-ghg.ref[f,s](t)`

### 16

**E1142. `EXPLabortax`: Labor tax reductions** (% of revenues)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 197
- Rows: all,all
  - 2022-2041: `EXPLabortax(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E1143. `EXPCIT`: Corporate taxes** (% of revenues)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 198
- Rows: all,all
  - 2022-2041: `EXPCIT(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E1144. `EXPCapex`: Public investment** (% of revenues)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 199
- Rows: all,all
  - 2022-2041: `EXPCapex(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E1145. `EXPGoodsandserv`: Current spending** (% of revenues)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 200
- Rows: all,all
  - 2022-2041: `EXPGoodsandserv(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E1146. `EXPTransfers`: Targeted transfers** (% of revenues)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 201
- Rows: all,all
  - 2022-2041: `EXPTransfers(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E1147. `MultipliersSource`: Fiscal multipliers** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 226
- Rows: all,all
  - 2022-2041: `MultipliersSource(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E1148. `GDPStartYear`: Start year for GDP calculations** (year)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 236
- Rows: all,all
  - 2022-2041: `GDPStartYear(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E1149. `FmAdj`: Fiscal multipliers adjustment** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 263
- Rows: all,all
  - 2022-2041: `FmAdj(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E1150. `GDPEndogenous`: Include endogenous GDP effects?** (switch)

- Description: MTInputs (scenario column)
- Legacy: MTInputs row 267
- Rows: all,all
  - 2022-2041: `GDPEndogenous(t) = MTInputs[code](scenario)`
  - Parameters: `<MTInputs row (Mapping)>` = `INDEX(MTRowNum,MATCH(code&"|"&f&"|"&s,MTRowKey,0))`

**E1151. `gdp.base`: Real GDP growth, baseline (before the GDP feedback)** (%)

- Description: WEO (lookup by country)
- Legacy: legacy Mitigation row 2444
- Rows: all,all
  - 2022-2041: `gdp.base(t) = INDEX(WEOVal,MATCH(CtryCode&"|gdp_growth",WEOKey,0),MATCH(year,WEOYear,0))`

**E1152. `fis.rev`: Total revenue (existing taxes net of subsidies + new policies + methane fee)** (USD m real)

- Description: rnet + rnew + rsr + rpsu + ch4.rev (methane fee on the scenario's own activity, as legacy; v0.9.0, I47)
- Legacy: legacy Mitigation row 8024
- Changes against legacy: LD55 (section B)
- Rows: all,all
  - 2022-2041: `fis.rev(t) = rnet[f,s](t)+rnew[f,s](t)+rsr[f,s](t)+rpsu[f,s](t)+ch4.rev[f,s](t)`

**E1153. `fis.ref`: Total revenue, scenario 1 (same year)** (USD m real)

- Description: Lookup (scenario 1, up to this column)
- Legacy: legacy Mitigation row 8036
- Rows: all,all
  - 2022-2041: `fis.ref(t) = INDEX(fis.rev[f,s](..t),MATCH(year,year(..t),0))`

**E1154. `fis.sp`: Fiscal space: total revenue above scenario 1** (share of GDP)

- Description: (fis.rev - fis.ref) / (gdp.usd x MperBn)
- Legacy: legacy Mitigation rows 8034, 8038, 14355
- Changes against legacy: LD55 (section B)
- Rows: all,all
  - 2022-2041: `fis.sp(t) = (fis.rev[f,s](t)-fis.ref[f,s](t))/(gdp.usd[f,s](t)*MperBn)`

**E1155. `fis.imp`: Fiscal impulse of the year (change in revenue above scenario 1 / this year's GDP)** (share of GDP)

- Description: 0 before GDPStartYear; fis.sp - fis.sp(t-1) x gdp.usd(t-1) / gdp.usd
- Legacy: legacy Mitigation row 14356 (v0.4.15)
- Rows: all,all
  - 2022: `fis.imp(t) = IF(year<GDPStartYear[f,s](t),0,fis.sp[f,s](t))`
  - 2023-2041: `fis.imp(t) = IF(year<GDPStartYear[f,s](t),0,fis.sp[f,s](t)-fis.sp[f,s](t-1)*gdp.usd[f,s](t-1)/gdp.usd[f,s](t))`

**E1156. `fis.lag`: Fiscal impulse k years back** (share of GDP)

- Description: Previous column of the row above
- Legacy: legacy Mitigation rows 8068-8244 (one block per year of the reform)
- Rows: l1,all
  - 2022: `fis.lag(t) = 0`
  - 2023-2041: `fis.lag(t) = fis.imp[all,s](t-1)`
- Rows: l2,all
  - 2022: `fis.lag(t) = 0`
  - 2023-2041: `fis.lag(t) = fis.lag[l1,s](t-1)`
- Rows: l3,all
  - 2022: `fis.lag(t) = 0`
  - 2023-2041: `fis.lag(t) = fis.lag[l2,s](t-1)`
- Rows: l4,all
  - 2022: `fis.lag(t) = 0`
  - 2023-2041: `fis.lag(t) = fis.lag[l3,s](t-1)`
- Rows: l5,all
  - 2022: `fis.lag(t) = 0`
  - 2023-2041: `fis.lag(t) = fis.lag[l4,s](t-1)`
- Rows: l6,all
  - 2022: `fis.lag(t) = 0`
  - 2023-2041: `fis.lag(t) = fis.lag[l5,s](t-1)`
- ... and 13 further row patterns (see the workbook)

**E1157. `fis.impp`: Fiscal impulse used by the revenue uses (0 before CPIntro)** (share of GDP)

- Description: IF(year < CPIntro, 0, fis.imp)
- Legacy: legacy Mitigation rows 96-100 (v0.5.7, I43)
- Rows: all,all
  - 2022-2041: `fis.impp(t) = IF(year<CPIntro(t),0,fis.imp[f,s](t))`

**E1158. `fis.lagp`: Fiscal impulse used by the revenue uses, k years back** (share of GDP)

- Description: Previous column of the row above
- Legacy: legacy Mitigation rows 8068-8244 (v0.5.7, I43)
- Rows: l1,all
  - 2022: `fis.lagp(t) = 0`
  - 2023-2041: `fis.lagp(t) = fis.impp[all,s](t-1)`
- Rows: l2,all
  - 2022: `fis.lagp(t) = 0`
  - 2023-2041: `fis.lagp(t) = fis.lagp[l1,s](t-1)`
- Rows: l3,all
  - 2022: `fis.lagp(t) = 0`
  - 2023-2041: `fis.lagp(t) = fis.lagp[l2,s](t-1)`
- Rows: l4,all
  - 2022: `fis.lagp(t) = 0`
  - 2023-2041: `fis.lagp(t) = fis.lagp[l3,s](t-1)`
- Rows: l5,all
  - 2022: `fis.lagp(t) = 0`
  - 2023-2041: `fis.lagp(t) = fis.lagp[l4,s](t-1)`
- Rows: l6,all
  - 2022: `fis.lagp(t) = 0`
  - 2023-2041: `fis.lagp(t) = fis.lagp[l5,s](t-1)`
- ... and 13 further row patterns (see the workbook)

**E1159. `fis.grp`: Multiplier group** (text)

- Description: global, est (Estimated), man (Manual), else the income group
- Legacy: legacy sheet Multipliers rows 19-21 (v0.4.15: est, man)
- Rows: all,all
  - 2022-2041: `fis.grp(t) = IFERROR(INDEX(MultSrcVal,MATCH(LEFT(MultipliersSource[f,s](t),3),MultSrcKey,0)),LOWER(IncomeGrp))`

**E1160. `fis.key`: Multiplier key prefix (group|range|)** (text)

- Description: fis.grp & range (Base, Low, High from FmAdj)
- Legacy: legacy sheet Multipliers rows 22, 36-57
- Changes against legacy: LD56 (section B)
- Rows: all,all
  - 2022-2041: `fis.key(t) = fis.grp[f,s](t)&"|"&LOWER(SUBSTITUTE(FmAdj[f,s](t),"*",""))&"|"`

**E1161. `fis.eff`: GDP effect of a revenue use** (share of GDP)

- Description: share x SUMPRODUCT(impulses of the year and the 19 years before, multipliers at those lags); revenue (exc) share -1
- Legacy: legacy Mitigation rows 8267-8274
- Changes against legacy: LD56 (section B)
- Rows: exc,all
  - 2022-2041: `fis.eff(t) = -1*SUMPRODUCT(block@fis.imp{fis.imp, fis.lag}(t),INDEX(MultVal,0,MATCH(fis.key[all,s](t)&<Instrument (key on sheet Multipliers)>,MultKey,0)))`
  - Parameters: `<Instrument (key on sheet Multipliers)>` = `data`
- Rows: pit,all
  - 2022-2041: `fis.eff(t) = EXPLabortax[all,s](t)/PctPerUnit*SUMPRODUCT(block@fis.impp{fis.impp, fis.lagp}(t),INDEX(MultVal,0,MATCH(fis.key[all,s](t)&<Instrument (key on sheet Multipliers)>,MultKey,0)))`
  - Parameters: `<Instrument (key on sheet Multipliers)>` = `data`
- Rows: cit,all
  - 2022-2041: `fis.eff(t) = EXPCIT[all,s](t)/PctPerUnit*SUMPRODUCT(block@fis.impp{fis.impp, fis.lagp}(t),INDEX(MultVal,0,MATCH(fis.key[all,s](t)&<Instrument (key on sheet Multipliers)>,MultKey,0)))`
  - Parameters: `<Instrument (key on sheet Multipliers)>` = `data`
- Rows: capt,all
  - 2022-2041: `fis.eff(t) = EXPCapex[all,s](t)/PctPerUnit*SUMPRODUCT(block@fis.impp{fis.impp, fis.lagp}(t),INDEX(MultVal,0,MATCH(fis.key[all,s](t)&<Instrument (key on sheet Multipliers)>,MultKey,0)))`
  - Parameters: `<Instrument (key on sheet Multipliers)>` = `data`
- Rows: gnfs,all
  - 2022-2041: `fis.eff(t) = EXPGoodsandserv[all,s](t)/PctPerUnit*SUMPRODUCT(block@fis.impp{fis.impp, fis.lagp}(t),INDEX(MultVal,0,MATCH(fis.key[all,s](t)&<Instrument (key on sheet Multipliers)>,MultKey,0)))`
  - Parameters: `<Instrument (key on sheet Multipliers)>` = `data`
- Rows: trns,all
  - 2022-2041: `fis.eff(t) = EXPTransfers[all,s](t)/PctPerUnit*SUMPRODUCT(block@fis.impp{fis.impp, fis.lagp}(t),INDEX(MultVal,0,MATCH(fis.key[all,s](t)&<Instrument (key on sheet Multipliers)>,MultKey,0)))`
  - Parameters: `<Instrument (key on sheet Multipliers)>` = `data`

**E1162. `gdp.lvl`: GDP level factor used this year (1 + last year's GDP effect)** (factor)

- Description: 1 + gdp.eff(t-1)
- Legacy: new (legacy adds the effect to growth: L24)
- Changes against legacy: LD54, L24 (section B)
- Rows: all,all
  - 2022: `gdp.lvl(t) = 1`
  - 2023-2041: `gdp.lvl(t) = 1+gdp.eff[f,s](t-1)`

**E1163. `gdp.pos.usd`: Real GDP after the feedback** (USD bn)

- Description: gdp.usd x gdp.lvl
- Legacy: legacy Mitigation row 2443
- Rows: all,all
  - 2022-2041: `gdp.pos.usd(t) = gdp.usd[f,s](t)*gdp.lvl[f,s](t)`

**E1164. `gdpg`: Real GDP growth effect of a revenue use (memo)** (share)

- Description: (1 + gdp.base) x (fis.eff(t-1) - fis.eff(t-2)) / gdp.lvl(t-1) if GDPEndogenous = Yes; all: from gdp.eff (sums to gdp.pos.pct - gdp.base)
- Legacy: legacy Mitigation rows 16166-16175 (v0.5.7)
- Rows: exc,all, pit,all, cit,all, capt,all, gnfs,all, trns,all
  - 2022: `gdpg(t) = 0`
  - 2023: `gdpg(t) = (1+gdp.base[all,s](t))*(fis.eff[f,s](t-1)-0)/gdp.lvl[all,s](t-1)*(LEFT(GDPEndogenous[all,s](t),3)="Yes")`
  - 2024-2041: `gdpg(t) = (1+gdp.base[all,s](t))*(fis.eff[f,s](t-1)-fis.eff[f,s](t-2))/gdp.lvl[all,s](t-1)*(LEFT(GDPEndogenous[all,s](t),3)="Yes")`
- Rows: all,all
  - 2022: `gdpg(t) = 0`
  - 2023: `gdpg(t) = (1+gdp.base[f,s](t))*(gdp.eff[f,s](t-1)-0)/gdp.lvl[f,s](t-1)`
  - 2024-2041: `gdpg(t) = (1+gdp.base[f,s](t))*(gdp.eff[f,s](t-1)-gdp.eff[f,s](t-2))/gdp.lvl[f,s](t-1)`

**E1165. `gdpy`: Year of the reform (memo; the growth effect of year N = gdpg.all where gdpy = N)** (year number)

- Description: year - GDPStartYear + 1
- Legacy: legacy Mitigation rows 16183-16194 (v0.6.0: a number row, not a shifted row)
- Rows: all,all
  - 2022-2041: `gdpy(t) = year-GDPStartYear[f,s](t)+1`

**E1166. `gdp.chg.usd`: Change in real GDP level against the baseline (memo)** (USD bn)

- Description: gdp.pos.usd - gdp.usd
- Legacy: legacy Mitigation row 16201 (v0.5.7)
- Rows: all,all
  - 2022-2041: `gdp.chg.usd(t) = gdp.pos.usd[f,s](t)-gdp.usd[f,s](t)`

**E1167. `xnim`: Change in net energy imports against scenario 1 (positive = more imports)** (USD bn real)

- Description: Fuels: echg x PJ per ktoe x supply price sp ($/GJ) x import share (D) / MperBn (REVENUE); groups: sums
- Legacy: legacy rows 18181, 18187, 18193 (F11), v0.3.16; share also on oil (legacy bug L49)
- Rows: coa,all, nga,all
  - 2022-2041: `xnim(t) = echg[f,s](t)*Settings[PJ per ktoe]*sp[f,ind](t)*<share traded (sheet WEO)>/MperBn`
  - Parameters: `<share traded (sheet WEO)>` = `INDEX(WEOVal,MATCH(CtryCode&"|ts_coa",WEOKey,0),1)`
- Rows: gso,all, die,all, lpg,all, ker,all, oop,all
  - 2022-2041: `xnim(t) = echg[f,s](t)*Settings[PJ per ktoe]*sp[f,s](t)*<share traded (sheet WEO)>/MperBn`
  - Parameters: `<share traded (sheet WEO)>` = `INDEX(WEOVal,MATCH(CtryCode&"|ts_oil",WEOKey,0),1)`
- Rows: jfu,all
  - 2022-2041: `xnim(t) = echg[f,s](t)*Settings[PJ per ktoe]*sp[ker,s](t)*<share traded (sheet WEO)>/MperBn`
  - Parameters: `<share traded (sheet WEO)>` = `INDEX(WEOVal,MATCH(CtryCode&"|ts_oil",WEOKey,0),1)`
- Rows: oil,grp
  - 2022-2041: `xnim(t) = SUM(xnim[6 rows](t))`
- Rows: nga,grp, coa,grp
  - 2022-2041: `xnim(t) = xnim[f,all](t)`
- Rows: all,all
  - 2022-2041: `xnim(t) = SUM(xnim[3 rows](t))`

**E1168. `xtb`: Energy trade balance, baseline (exports - imports) by fuel group** (USD bn real)

- Description: Sheet WEO (EGY|tb_oil, tb_nga, tb_coa)
- Legacy: legacy Mitigation rows 741-743
- Rows: oil,all
  - 2022-2041: `xtb(t) = INDEX(WEOVal,MATCH(CtryCode&"|tb_oil",WEOKey,0),MATCH(year,WEOYear,0))`
- Rows: nga,all
  - 2022-2041: `xtb(t) = INDEX(WEOVal,MATCH(CtryCode&"|tb_nga",WEOKey,0),MATCH(year,WEOYear,0))`
- Rows: coa,all
  - 2022-2041: `xtb(t) = INDEX(WEOVal,MATCH(CtryCode&"|tb_coa",WEOKey,0),MATCH(year,WEOYear,0))`
- Rows: all,all
  - 2022-2041: `xtb(t) = SUM(xtb[3 rows](t))`

**E1169. `xtbp`: Energy trade balance of the scenario: baseline - change in net imports** (USD bn real)

- Description: xtb.all - xnim.all
- Legacy: legacy rows 18215, 18218 (F11), v0.3.16
- Rows: all,all
  - 2022-2041: `xtbp(t) = xtb[f,s](t)-xnim[f,s](t)`

**E1170. `xtb.pct`: Energy trade balance of the scenario, % of baseline real GDP** (%)

- Description: xtbp / gdp.usd (SAFEDIV)
- Legacy: legacy rows 18217, 18219, v0.3.16
- Rows: all,all
  - 2022-2041: `xtb.pct(t) = IF(gdp.usd[f,s](t)=0,0,(xtbp[f,s](t))/gdp.usd[f,s](t))`

**E1171. `xnim.pct`: Change in net energy imports, % of baseline real GDP** (%)

- Description: xnim.all / gdp.usd (SAFEDIV)
- Legacy: legacy rows 18207-18210, v0.3.16
- Rows: all,all
  - 2022-2041: `xnim.pct(t) = IF(gdp.usd[f,s](t)=0,0,(xnim[f,s](t))/gdp.usd[f,s](t))`

**E1172. `bca`: Current account balance, pre-policy (typed WEO EGY.BCA.A, held at 2031)** (USD bn nominal)

- Description: Inputs EGY|bca (typed; other countries 0)
- Legacy: legacy row 18182 (bug L50 fixed: stale WEO codes)
- Rows: all,all
  - 2022-2041: `bca(t) = IFERROR(INDEX(WEOVal,MATCH(CtryCode&"|bca",WEOKey,0),MATCH(year,WEOYear,0)),0)`

**E1173. `bca.gdp`: Current account balance, pre-policy, % of GDP (typed WEO EGY.BCA_NGDPD.A, held at 2031)** (% of GDP (percent units))

- Description: Inputs EGY|bca_gdp (typed; other countries 0)
- Legacy: legacy row 18191 (bug L50 fixed)
- Rows: all,all
  - 2022-2041: `bca.gdp(t) = IFERROR(INDEX(WEOVal,MATCH(CtryCode&"|bca_gdp",WEOKey,0),MATCH(year,WEOYear,0)),0)`

**E1174. `bca.r`: Current account balance, pre-policy, real** (USD bn real)

- Description: bca x US CPI index (infl)
- Legacy: legacy row 18184 (18183 = row 456)
- Rows: all,all
  - 2022-2041: `bca.r(t) = bca[f,s](t)*infl(t)`

**E1175. `bca.d`: Change in the current account by fuel group (positive = fewer net imports)** (USD bn real)

- Description: - xnim of the fuel group (section 16b: supply price, share traded also on oil)
- Legacy: legacy rows 18185-18187 (L49 fixed; gas unit bug L215 not replicated: xnim prices in USD/GJ)
- Rows: oil,all, nga,all, coa,all
  - 2022-2041: `bca.d(t) = -xnim[f,grp](t)`

**E1176. `bca.p`: Current account balance after the policy** (USD bn real)

- Description: bca.r + bca.d of oil, gas and coal
- Legacy: legacy row 18188
- Rows: all,all
  - 2022-2041: `bca.p(t) = bca.r[f,s](t)+bca.d[oil,s](t)+bca.d[nga,s](t)+bca.d[coa,s](t)`

**E1177. `bca.y`: Implied GDP / 100 (helper): real current account over its share of GDP** (USD bn real)

- Description: ABS(bca.r / bca.gdp); 0 if bca.gdp = 0
- Legacy: legacy rows 18192-18194 (as legacy, issue I129)
- Rows: all,all
  - 2022-2041: `bca.y(t) = IF(bca.gdp[f,s](t)=0,0,ABS(bca.r[f,s](t)/bca.gdp[f,s](t)))`

**E1178. `bca.dp`: Change in the current account by fuel group, % of GDP** (% of GDP (percent units))

- Description: bca.d / bca.y (SAFEDIV)
- Legacy: legacy rows 18192-18194
- Rows: oil,all, nga,all, coa,all
  - 2022-2041: `bca.dp(t) = IF(bca.y[all,s](t)=0,0,(bca.d[f,s](t))/bca.y[all,s](t))`

**E1179. `bca.pp`: Current account balance after the policy, % of GDP** (% of GDP (percent units))

- Description: bca.gdp + bca.dp of oil, gas and coal
- Legacy: legacy row 18195 (bug L214 fixed: coal included)
- Rows: all,all
  - 2022-2041: `bca.pp(t) = bca.gdp[f,s](t)+bca.dp[oil,s](t)+bca.dp[nga,s](t)+bca.dp[coa,s](t)`

**E1180. `bca.n`: Current account balance, current prices (memo, typed)** (USD bn nominal)

- Description: Inputs EGY|bca_n (typed; 0 after 2031 as legacy, issue I130)
- Legacy: legacy row 18198
- Rows: all,all
  - 2022-2041: `bca.n(t) = IFERROR(INDEX(WEOVal,MATCH(CtryCode&"|bca_n",WEOKey,0),MATCH(year,WEOYear,0)),0)`

**E1181. `gdp.eff`: GDP effect of the revenue use (level, vs baseline)** (share of GDP)

- Description: SUM(fis.eff) if GDPEndogenous = Yes
- Legacy: legacy Mitigation rows 8288, 8290
- Rows: all,all
  - 2022-2041: `gdp.eff(t) = SUM(fis.eff[6 rows](t))*(LEFT(GDPEndogenous[f,s](t),3)="Yes")`

### 17

**E1182. `tcp`: Implicit carbon price by fuel: existing taxes, subsidies and new policies per tonne of CO2** (USD/tCO2)

- Description: Fuels: (rfu + rfg of the fuel) / co2.f; all: fossil fuels / co2 (SAFEDIV); biomass left out
- Legacy: legacy F5d (total carbon price by fuel), v0.3.15
- Rows: coa,all, nga,all, oop,all
  - 2022-2041: `tcp(t) = IF(co2[f,s](t)=0,0,(rfu[f,s](t)+rfg[f,pow](t))/co2[f,s](t))`
- Rows: gso,all, die,all, lpg,all, ker,all, jfu,all
  - 2022-2041: `tcp(t) = IF(co2[f,s](t)=0,0,(rfu[f,s](t))/co2[f,s](t))`
- Rows: all,all
  - 2022-2041: `tcp(t) = IF(co2[f,s](t)=0,0,(SUM(rfu[8 rows](t))+rfg[coa,pow](t)+rfg[nga,pow](t)+rfg[oop,pow](t))/co2[f,s](t))`

**E1183. `cpeff`: Effective carbon tax: carbon price x share of energy CO2 covered by it** (USD/tCO2)

- Description: cptraj x cov.ct.all (SCALEBY)
- Legacy: legacy row 16137, v0.3.15
- Rows: all,all
  - 2022-2041: `cpeff(t) = cptraj(t)*cov.ct[f,s](t)`

**E1184. `covct`: CO2 covered by the new carbon tax, by coverage sector** (MtCO2)

- Description: SUMPRODUCT(co2 of the fuels x fuel switch fc) x (carbon tax rate ctr of the sector > 0)
- Legacy: new (v0.3.15)
- Rows: all,pow
  - 2022-2041: `covct(t) = (co2[coa,s](t)*ctcov[coa,all](t)+co2[nga,s](t)*ctcov[nga,all](t)+co2[oop,s](t)*ctcov[oop,all](t))*(ctr[f,s](t)>0)`
- Rows: all,rod, all,ral, all,avi, all,nav, all,res, all,foo, all,srv, all,mch, all,irn, all,nfm, all,mac, all,cem, ... (16 rows)
  - 2022-2041: `covct(t) = SUMPRODUCT(co2[9 rows](t)*ctcov[9 rows](t))*(ctr[f,s](t)>0)`

**E1185. `cov.ct`: Share of energy CO2 covered by the new carbon tax** (%)

- Description: covct of the sectors / co2 (SAFEDIV)
- Legacy: legacy rows 16152-16157, v0.3.15
- Rows: all,tra
  - 2022-2041: `cov.ct(t) = IF(co2[f,all](t)=0,0,(SUM(covct[4 rows](t)))/co2[f,all](t))`
- Rows: all,bld
  - 2022-2041: `cov.ct(t) = IF(co2[f,all](t)=0,0,(SUM(covct[3 rows](t)))/co2[f,all](t))`
- Rows: all,ind
  - 2022-2041: `cov.ct(t) = IF(co2[f,all](t)=0,0,(SUM(covct[8 rows](t)))/co2[f,all](t))`
- Rows: all,oen, all,pow
  - 2022-2041: `cov.ct(t) = IF(co2[f,all](t)=0,0,(covct[f,s](t))/co2[f,all](t))`
- Rows: all,all
  - 2022-2041: `cov.ct(t) = IF(co2[f,s](t)=0,0,(SUM(covct[17 rows](t)))/co2[f,s](t))`

**E1186. `cov.ets`: Share of energy CO2 covered by the new ETS** (%)

- Description: co2.ets / co2 (SAFEDIV)
- Legacy: new (v0.3.15)
- Rows: all,all
  - 2022-2041: `cov.ets(t) = IF(co2[f,s](t)=0,0,(co2.ets[f,s](t))/co2[f,s](t))`

**E1187. `cov.all`: Share of energy CO2 covered by the carbon tax or the ETS** (%)

- Description: cov.ct.all + cov.ets
- Legacy: legacy row 16152, v0.3.15
- Rows: all,all
  - 2022-2041: `cov.all(t) = cov.ct[f,s](t)+cov.ets[f,s](t)`

**E1188. `ecr`: Effective carbon rate, economy-wide: revenue net of subsidies (incl. electricity VAT and subsidy gap) per tonne of energy CO2** (USD/tCO2)

- Description: (rnet + rnew) / co2 (SAFEDIV)
- Legacy: legacy row 16662 (F5e), v0.3.15
- Rows: all,all
  - 2022-2041: `ecr(t) = IF(co2[f,s](t)=0,0,(rnet[f,s](t)+rnew[f,s](t)+rsr[f,s](t))/co2[f,s](t))`

### 17b

**E1189. `airpol.cost`: Air-pollution cost per unit of fuel, marginal damages (coal, gas, other oil products USD/GJ; gasoline, diesel, LPG, kerosene USD/l)** (USD per unit)

- Description: airpol.mc of the subsectors of the line weighted by the scenario's own fuel use (fus) x GJ per price unit (R1.1; v0.9.0 PIGAP: legacy average damages, I104 fixed; the legacy values are a memo on FromAirPollution)
- Legacy: legacy rows 17738-17749
- Rows: coa,ind, nga,ind, oop,ind
  - 2022-2041: `airpol.cost(t) = IFERROR(SUMPRODUCT(airpol.mc[8 rows](t),fus[8 rows](t))/SUM(fus[8 rows](t)),AVERAGE(airpol.mc[8 rows](t)))*<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `data`
- Rows: coa,res, nga,res
  - 2022-2041: `airpol.cost(t) = IFERROR(SUMPRODUCT(airpol.mc[3 rows](t),fus[3 rows](t))/SUM(fus[3 rows](t)),AVERAGE(airpol.mc[3 rows](t)))*<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `data`
- Rows: coa,pow, nga,pow, oop,pow
  - 2022-2041: `airpol.cost(t) = airpol.mc[f,s](t)*<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `data`
- Rows: gso,all, die,all, lpg,all, ker,all
  - 2022-2041: `airpol.cost(t) = IFERROR(SUMPRODUCT(airpol.mc[16 rows](t),fus[16 rows](t))/SUM(fus[16 rows](t)),AVERAGE(airpol.mc[16 rows](t)))*<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `<GJ per price unit of pset[f,s]>`

**E1190. `fus`: Fuel use of the subsector (weights of the air-pollution cost lines)** (ktoe)

- Description: ener of the subsector and fuel (sections 5-8), scenario's own (v0.9.0 PIGAP)
- Legacy: legacy rows 16849-16930
- Rows: coa,mch, coa,irn, coa,nfm, coa,mac, coa,cem, coa,omn, coa,cst, coa,ftr, coa,res, coa,foo, coa,srv, nga,mch, ... (94 rows)
  - 2022-2041: `fus(t) = ener[f,s](t)`

**E1191. `airpol.cost.gj`: Air-pollution cost per GJ (17b: by fuel and sector; 18: other uses, oil average)** (USD/GJ)

- Description: 17b: typed / GJ per litre (oil products); residential coal x [coal > ApCoalResMin x buildings fuel use] (L192 fixed); 18: use-weighted averages (L178 fixed) (R1.2-R1.3, R2.3)
- Legacy: legacy rows 17738-17753, 113-123
- Rows: coa,ind, coa,pow, nga,ind, nga,res, nga,pow, gso,all, die,all, lpg,all, ker,all, oop,pow, oop,ind
  - 2022-2041: `airpol.cost.gj(t) = airpol.cost[f,s](t)/<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `data`
- Rows: coa,res
  - 2022-2041: `airpol.cost.gj(t) = airpol.cost[f,s](t)*(fuq[f,bld](t)>ApCoalResMin*ener[all,bld](t))`
  - Parameters: `<GJ per price unit>` = `data`
- Rows: coa,oth, nga,oth
  - 2022-2041: `airpol.cost.gj(t) = IFERROR(SUMPRODUCT(airpol.cost.gj[3 rows](t),apq[3 rows](t))/SUM(apq[3 rows](t)),AVERAGE(airpol.cost.gj[3 rows](t)))`
- Rows: odo,oth
  - 2022-2041: `airpol.cost.gj(t) = IFERROR((airpol.cost.gj[die,all](t)*apq[die,tra](t)+SUMPRODUCT(airpol.cost.gj[2 rows](t),apq[2 rows](t)))/SUM(apq[3 rows](t)),0)`
- Rows: oop,avg
  - 2022-2041: `airpol.cost.gj(t) = IF(SUM(apq[2 rows](t))=0,0,SUMPRODUCT(airpol.cost.gj[2 rows](t),apq[2 rows](t))/SUM(apq[2 rows](t)))`

**E1192. `fuq`: Fuel use by sector group (weights of the costs per unit)** (ktoe)

- Description: SUMIFS of the subsector rows ener of the group
- Legacy: legacy rows 16849-16930
- Rows: coa,tra, nga,tra, gso,tra, die,tra, lpg,tra, ker,tra, oop,tra, coa,bld, nga,bld, gso,bld, die,bld, lpg,bld, ... (28 rows)
  - 2022-2041: `fuq(t) = SUMIFS(block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(t),block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(A),"ener",block@ener{ener, eldem, ctxnew, ets, ... 23 variables}(B),f)`

**E1193. `air.con.pm2`: Modelled ambient PM2.5 by air-pollution module sector (total: the summary row)** (ug/m3)

- Description: SUMPRODUCT(emissions of the sector (section 15), coefficients of the sector (FromAirPollution)) x tPerKt (R1.5)
- Legacy: legacy AP rows 974-981, 1814
- Rows: cpp, gpp, opp, rod, gro, oth, foo
  - 2022-2041: `air.con.pm2(t) = IF(<first pollutant row>,SUMPRODUCT(aps[10 rows](t),INDEX(ApKap,<first pollutant row>,<sector position (FromAirPollution column)>):INDEX(ApKap,<last pollutant row>,<sector position (FromAirPollution column)>))*tPerKt,0)`
  - Parameters: `<sector position (FromAirPollution column)>` = `MATCH("cpp",ApKapHdr,0)`; `<first pollutant row>` = `IFERROR(MATCH(CtryCode&"|nox",ApKapKey,0),0)`; `<last pollutant row>` = `IFERROR(MATCH(CtryCode&"|oc",ApKapKey,0),0)`
- Rows: mod
  - 2022-2041: `air.con.pm2(t) = SUM(air.con.pm2[7 rows](t))`

**E1194. `air.vpm`: Value of averted modelled ambient PM2.5, typed** (USD bn per ug/m3)

- Description: Tab FromAirPollution: legacy wel.air / change in modelled PM2.5 of the legacy run (R1.4; issue I105)
- Legacy: legacy AP rows 3217, 981, 1814
  - 2022-2041: `air.vpm(t) = IFERROR(INDEX(ApVal,MATCH(CtryCode&<data key (FromAirPollution)>,ApKey,0),MATCH(year,ApYear,0)),0)`
  - Parameters: `<data key (FromAirPollution)>` = `data`

**E1195. `tran.acc.km`: Accident cost per vehicle-km, typed** (USD/km)

- Description: Tab FromTransportCB (R1.6)
- Legacy: legacy Transport row 185
  - 2022-2041: `tran.acc.km(t) = IFERROR(INDEX(TcbVal,MATCH(CtryCode&<data key (FromTransportCB)>,TcbKey,0),MATCH(year,TcbYear,0)),0)`
  - Parameters: `<data key (FromTransportCB)>` = `data`

**E1196. `tran.con.km`: Congestion cost per vehicle-km, typed** (USD/km)

- Description: Tab FromTransportCB (R1.6)
- Legacy: legacy Transport row 220
  - 2022-2041: `tran.con.km(t) = IFERROR(INDEX(TcbVal,MATCH(CtryCode&<data key (FromTransportCB)>,TcbKey,0),MATCH(year,TcbYear,0)),0)`
  - Parameters: `<data key (FromTransportCB)>` = `data`

**E1197. `tran.rdm.km`: Road damage cost per freight vehicle-km, typed** (USD/km)

- Description: Tab FromTransportCB (R1.6; not deflated, issue I111)
- Legacy: legacy Transport row 232
  - 2022-2041: `tran.rdm.km(t) = IFERROR(INDEX(TcbVal,MATCH(CtryCode&<data key (FromTransportCB)>,TcbKey,0),MATCH(year,TcbYear,0)),0)`
  - Parameters: `<data key (FromTransportCB)>` = `data`

**E1198. `tran.cls`: Road fuel use by the vehicle classes of the fuel (passenger and freight; gasoline: passenger and 2-3 wheelers; electricity: all three)** (bln liters or kWh)

- Description: Section 5b class rows (engineer model, issue I100)
- Legacy: legacy rows 15710-15721
- Rows: gso,rod
  - 2022-2041: `tran.cls(t) = trfcp[f,pas](t)+trfcc[f,cyc](t)`
- Rows: die,rod, lpg,rod, nga,rod
  - 2022-2041: `tran.cls(t) = trfcp[f,pas](t)+trfcf[f,fre](t)`
- Rows: ecy,rod
  - 2022-2041: `tran.cls(t) = trfcep[f,pas](t)+trfcef[f,fre](t)+trfcec[f,cyc](t)`

**E1199. `tran.wcl`: Passenger weight of the fuel, scenario 1** (share)

- Description: 1 - freight use / class use of scenario 1; gasoline 1 (R1.7, issue I111)
- Legacy: legacy rows 15723-15730
- Rows: gso,rod
  - 2022-2041: `tran.wcl(t) = 1`
- Rows: die,rod, lpg,rod, nga,rod
  - 2022-2041: `tran.wcl(t) = IFERROR(1-INDEX(trfcf[f,fre](..t),row10(t))/INDEX(tran.cls[f,s](..t),row10(t)),0)`
- Rows: ecy,rod
  - 2022-2041: `tran.wcl(t) = IFERROR(1-INDEX(trfcef[f,fre](..t),row10(t))/INDEX(tran.cls[f,s](..t),row10(t)),0)`

**E1200. `tran.mrg`: Driving share of the response of the fuel (usage / (usage + efficiency elasticity))** (share)

- Description: (D + w x E) / (F + w x G), w = tran.wcl; 0 without class use (R1.8, bug L193 fixed)
- Legacy: legacy rows 15721-15730; Transport rows 148-157
- Rows: gso,rod, die,rod, lpg,rod, nga,rod, ecy,rod
  - 2022-2041: `tran.mrg(t) = IF(INDEX(tran.cls[f,s](..t),row10(t))=0,0,(<eps_U diesel>+tran.wcl[f,s](t)*<eps_U gasoline - diesel>)/(<eps_U + eps_F diesel>+tran.wcl[f,s](t)*<eps_U + eps_F gasoline - diesel>))`
  - Parameters: `<eps_U diesel>` = `<usage, diesel of trp.ela[all,all]>`; `<eps_U gasoline - diesel>` = `<usage, gasoline of trp.ela[all,all]>-<usage, diesel of trp.ela[all,all]>`; `<eps_U + eps_F diesel>` = `<usage, diesel of trp.ela[all,all]>+<efficiency, diesel of trp.ela[all,all]>`; `<eps_U + eps_F gasoline - diesel>` = `<usage, gasoline of trp.ela[all,all]>+<efficiency, gasoline of trp.ela[all,all]>-<usage, diesel of trp.ela[all,all]>-<efficiency, diesel of trp.ela[all,all]>`

**E1201. `tran.fsh`: Freight share of the class use of the fuel, own scenario** (share)

- Description: freight / class use (R1.9)
- Legacy: legacy rows 15768-15786; Transport rows 138-146
- Rows: die,rod, lpg,rod, nga,rod
  - 2022-2041: `tran.fsh(t) = IF(tran.cls[f,s](t)=0,0,trfcf[f,fre](t)/tran.cls[f,s](t))`
- Rows: ecy,rod
  - 2022-2041: `tran.fsh(t) = IF(tran.cls[f,s](t)=0,0,trfcef[f,fre](t)/tran.cls[f,s](t))`

**E1202. `tran.acc.cost`: Accident cost per unit of the fuel (all use)** (USD per liter or kWh)

- Description: tran.acc.km x fuel economy (5b) x tran.mrg x tran.rsh (R1.10; average fuel economy as legacy)
- Legacy: legacy Transport rows 186-190, 322-331
- Rows: gso,all
  - 2022-2041: `tran.acc.cost(t) = tran.acc.km(t)*trafg[f,s](t)*tran.mrg[f,rod](t)*tran.rsh[f,rod](t)`
- Rows: die,all, lpg,all, nga,all
  - 2022-2041: `tran.acc.cost(t) = tran.acc.km(t)*trafo[f,s](t)*tran.mrg[f,rod](t)*tran.rsh[f,rod](t)`
- Rows: ecy,all
  - 2022-2041: `tran.acc.cost(t) = tran.acc.km(t)*trafe[f,s](t)*tran.mrg[f,rod](t)*tran.rsh[f,rod](t)`

**E1203. `tran.con.cost`: Congestion cost per unit of the fuel (all use)** (USD per liter or kWh)

- Description: tran.con.km x fuel economy x tran.mrg x tran.rsh (R1.10)
- Legacy: legacy Transport rows 221-225, 333-342
- Rows: gso,all
  - 2022-2041: `tran.con.cost(t) = tran.con.km(t)*trafg[f,s](t)*tran.mrg[f,rod](t)*tran.rsh[f,rod](t)`
- Rows: die,all, lpg,all, nga,all
  - 2022-2041: `tran.con.cost(t) = tran.con.km(t)*trafo[f,s](t)*tran.mrg[f,rod](t)*tran.rsh[f,rod](t)`
- Rows: ecy,all
  - 2022-2041: `tran.con.cost(t) = tran.con.km(t)*trafe[f,s](t)*tran.mrg[f,rod](t)*tran.rsh[f,rod](t)`

**E1204. `tran.rdm.cost`: Road damage cost per unit of the fuel (all use)** (USD per liter or kWh)

- Description: tran.rdm.km x fuel economy x tran.mrg x tran.fsh x tran.rsh (R1.10)
- Legacy: legacy Transport rows 234-237, 344-351
- Rows: die,all, lpg,all, nga,all
  - 2022-2041: `tran.rdm.cost(t) = tran.rdm.km(t)*trafo[f,s](t)*tran.mrg[f,rod](t)*tran.fsh[f,rod](t)*tran.rsh[f,rod](t)`
- Rows: ecy,all
  - 2022-2041: `tran.rdm.cost(t) = tran.rdm.km(t)*trafe[f,s](t)*tran.mrg[f,rod](t)*tran.fsh[f,rod](t)*tran.rsh[f,rod](t)`

**E1205. `tran.acc.gj`: Accident cost per GJ** (USD/GJ)

- Description: tran.acc.cost / GJ per liter (R1.11)
- Legacy: new
- Rows: gso,all, die,all, lpg,all
  - 2022-2041: `tran.acc.gj(t) = tran.acc.cost[f,s](t)/<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `<GJ per price unit of pset[f,s]>`

**E1206. `tran.con.gj`: Congestion cost per GJ** (USD/GJ)

- Description: tran.con.cost / GJ per liter (R1.11)
- Legacy: new
- Rows: gso,all, die,all, lpg,all
  - 2022-2041: `tran.con.gj(t) = tran.con.cost[f,s](t)/<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `<GJ per price unit of pset[f,s]>`

**E1207. `tran.rdm.gj`: Road damage cost per GJ** (USD/GJ)

- Description: tran.rdm.cost / GJ per liter (R1.11)
- Legacy: new
- Rows: die,all, lpg,all
  - 2022-2041: `tran.rdm.gj(t) = tran.rdm.cost[f,s](t)/<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `<GJ per price unit of pset[f,s]>`

### 18

**E1208. `dmg`: Climate damages of GHG emissions excl. LULUCF (national SCC, global SCC)** (USD bn real)

- Description: scc x ghg / MperBn (SCALEBY)
- Legacy: legacy rows 17688-17689, 17704-17705; v0.3.17
- Rows: nat,all, glo,all
  - 2022-2041: `dmg(t) = scc[f,s](t)*ghg[all,s](t)/MperBn`

**E1209. `wcli`: Climate damages avoided against scenario 1 (national, global)** (USD bn real)

- Description: dmg of scenario 1 - dmg
- Legacy: legacy rows 17690, 17729-17731; v0.3.17
- Rows: nat,all, glo,all
  - 2022-2041: `wcli(t) = INDEX(dmg[f,s](..t),row10(t))-dmg[f,s](t)`

**E1210. `wdg`: Tax wedge: revenue net of subsidies per unit of use (fuels incl. power generation; electricity demand)** (USD m/ktoe)

- Description: (rfu + rfg) / fuel use (section 11); electricity: rfu.ecy / eldem (SAFEDIV)
- Legacy: new (v0.3.17)
- Rows: coa,all, nga,all, oop,all, bio,all
  - 2022-2041: `wdg(t) = IF(ener[f,s](t)=0,0,(rfu[f,s](t)+rfg[f,pow](t))/ener[f,s](t))`
- Rows: gso,all, die,all, lpg,all, ker,all, jfu,all
  - 2022-2041: `wdg(t) = IF(ener[f,s](t)=0,0,(rfu[f,s](t))/ener[f,s](t))`
- Rows: ecy,all
  - 2022-2041: `wdg(t) = IF(eldem[f,s](t)=0,0,(rfu[f,pow](t))/eldem[f,s](t))`

**E1211. `eff`: Efficiency (deadweight) cost of energy use (positive = cost; negative = gain from lower subsidised use)** (USD bn real)

- Description: -(wedge + wedge of scenario 1) / 2 x change in use / MperBn (TRAPEZOID)
- Legacy: legacy rows 17636-17648 (trapezoid); v0.3.17, the LPG, conversion and row-offset bugs not replicated
- Rows: coa,all, nga,all, gso,all, die,all, lpg,all, ker,all, jfu,all, oop,all, bio,all
  - 2022-2041: `eff(t) = -AVERAGE(wdg[f,s](t),INDEX(wdg[f,s](..t),row10(t)))*echg[f,s](t)/MperBn`
- Rows: ecy,all
  - 2022-2041: `eff(t) = -AVERAGE(wdg[f,s](t),INDEX(wdg[f,s](..t),row10(t)))*(eldem[f,s](t)-INDEX(eldem[f,s](..t),row10(t)))/MperBn`
- Rows: all,all
  - 2022-2041: `eff(t) = SUM(eff[10 rows](t))`

**E1212. `mfp`: Methane fee per t CH4 used on the abatement curve** (USD/tCH4)

- Description: MIN(fee x GWP, fee where a x fee ^ b = 1) (MFEEPRICE)
- Legacy: new (v0.3.17)
- Rows: og,all, dg,all, cm,all, bm,all, liv,all, ric,all, wst,all
  - 2022-2041: `mfp(t) = IF(<curve a (country, else average) of ch4.abt[f,s]>=0,0,MIN(mfee(t)*<GWP of ch4.abt[f,s]>*<fee applies (1 = yes; Settings, legacy Manual inputs J196-J200) of ch4.abt[f,s]>,IFERROR(<curve a (country, else average) of ch4.abt[f,s]>^(-1/<curve b (country, else average) of ch4.abt[f,s]>),mfee(t)*<GWP of ch4.abt[f,s]>*<fee applies (1 = yes; Settings, legacy Manual inputs J196-J200) of ch4.abt[f,s]>)))`

**E1213. `mfc`: Efficiency cost of the methane fee: area under the abatement curve** (USD bn real)

- Description: unabated emissions (kt CH4) x abatement share x price x b / (1 + b) / Million (MFEECOST)
- Legacy: legacy rows 17628-17634 (integral); v0.3.17
- Rows: og,all, dg,all, cm,all, bm,all, liv,all, ric,all, wst,all
  - 2022-2041: `mfc(t) = IF(<activity in the base year (data) of ch4.src[f,s]>=0,0,<emissions in GHGYear (kt CH4) of ch4.em[f,s]>*ch4.act[f,s](t)/<activity in the base year (data) of ch4.src[f,s]>)*ch4.abt[f,s](t)*mfp[f,s](t)*<curve b (country, else average) of ch4.abt[f,s]>/(1+<curve b (country, else average) of ch4.abt[f,s]>)/Million`
- Rows: all,all
  - 2022-2041: `mfc(t) = SUM(mfc[7 rows](t))`

**E1214. `cc.nat`: Climate cost per GJ of fuel, national SCC** (USD/GJ)

- Description: scc.nat x generic EF (R2.1; L176 fixed)
- Legacy: legacy rows 17678-17685
- Rows: coa,all, nga,all, oop,all, gso,all, die,all, lpg,all, ker,all
  - 2022-2041: `cc.nat(t) = scc[nat,s](t)*<generic EF (tCO2/GJ)>`
  - Parameters: `<generic EF (tCO2/GJ)>` = `IFERROR(INDEX(EFGen,MATCH(f,EFGenKey,0)),0)`

**E1215. `cc.glo`: Climate cost per GJ of fuel, global SCC** (USD/GJ)

- Description: scc.glo x generic EF (R2.1)
- Legacy: legacy rows 17702-17709
- Rows: coa,all, nga,all, oop,all, gso,all, die,all, lpg,all, ker,all
  - 2022-2041: `cc.glo(t) = scc[glo,s](t)*<generic EF (tCO2/GJ)>`
  - Parameters: `<generic EF (tCO2/GJ)>` = `IFERROR(INDEX(EFGen,MATCH(f,EFGenKey,0)),0)`

**E1216. `airpol.ecy`: Air-pollution cost of electricity (memo)** (USD/kWh)

- Description: sum of power cost x fuel use x PJ per ktoe / (generation x MWyMkWh) (R2.2; L177 fixed)
- Legacy: legacy row 18090
  - 2022-2041: `airpol.ecy(t) = (airpol.cost.gj[coa,pow](t)*pe[coa,pow](t)+airpol.cost.gj[nga,pow](t)*pe[nga,pow](t)+airpol.cost.gj[oop,pow](t)*pe[oop,pow](t))*PJperKtoe/(gtot(t)*MWyMkWh)`

**E1217. `apq`: Fuel use weights of the other-use air-pollution costs** (ktoe)

- Description: fuq or power fuel use pe
- Legacy: legacy rows 16911-16920
- Rows: coa,ind, coa,bld, nga,ind, nga,bld, die,tra, oop,ind
  - 2022-2041: `apq(t) = fuq[f,s](t)`
- Rows: coa,pow, nga,pow, oop,pow
  - 2022-2041: `apq(t) = pe[f,s](t)`

**E1218. `tot.ext`: Total externalities of road fuels excl. climate** (USD/GJ)

- Description: air pollution + accidents + congestion (+ road damage, diesel) per GJ (R2.4)
- Legacy: legacy rows 17763-17764
- Rows: gso,all
  - 2022-2041: `tot.ext(t) = airpol.cost.gj[f,s](t)+tran.acc.gj[f,s](t)+tran.con.gj[f,s](t)`
- Rows: die,all
  - 2022-2041: `tot.ext(t) = airpol.cost.gj[f,s](t)+tran.acc.gj[f,s](t)+tran.con.gj[f,s](t)+tran.rdm.gj[f,s](t)`

**E1219. `wel`: Welfare, national: avoided damages and co-benefits - efficiency costs (USD bn real; % of baseline real GDP)** (mixed)

- Description: usd = wcli.nat + wel.air.usd + wel.rod - eff.all - mfc.all (v0.9.0, R2.8); air.usd = air.vpm x (modelled PM2.5 of scenario 1 - own) (R2.5); pct, cli, eff, air.pct, rod.pct = shares of gdp.usd
- Legacy: legacy rows 17716-17727; v0.3.17
- Rows: usd,air
  - 2022-2041: `wel(t) = air.vpm(t)*(INDEX(air.con.pm2[mod](..t),row10(t))-air.con.pm2[mod](t))`
- Rows: pct,all
  - 2022-2041: `wel(t) = IF(gdp.usd[all,s](t)=0,0,(wel[usd,s](t))/gdp.usd[all,s](t))`
- Rows: cli,all
  - 2022-2041: `wel(t) = IF(gdp.usd[all,s](t)=0,0,(wcli[nat,s](t))/gdp.usd[all,s](t))`
- Rows: pct,air
  - 2022-2041: `wel(t) = wel[usd,s](t)/gdp.usd[all,all](t)`
- Rows: pct,rod
  - 2022-2041: `wel(t) = SUM(wel.rod[3 rows](t))/gdp.usd[all,all](t)`
- Rows: eff,all
  - 2022-2041: `wel(t) = IF(gdp.usd[all,s](t)=0,0,(eff[all,s](t)+mfc[all,s](t))/gdp.usd[all,s](t))`
- ... and 1 further row patterns (see the workbook)

**E1220. `wel.rod`: Road transport co-benefits: averted accidents, reduced congestion, reduced road damage** (USD bn real)

- Description: cost per vehicle-km x (vehicle-km of scenario 1 - vehicle-km; road damage: freight) (R2.6, issue I111)
- Legacy: legacy rows 17718-17720 (Transport 356, 360, 364)
- Rows: usd,aci
  - 2022-2041: `wel.rod(t) = tran.acc.km(t)*(INDEX(trkmt[all,all](..t),row10(t))-trkmt[all,all](t))`
- Rows: usd,con
  - 2022-2041: `wel.rod(t) = tran.con.km(t)*(INDEX(trkmt[all,all](..t),row10(t))-trkmt[all,all](t))`
- Rows: usd,dmg
  - 2022-2041: `wel.rod(t) = tran.rdm.km(t)*(INDEX(trkmf[all,fre](..t),row10(t))-trkmf[all,fre](t))`

**E1221. `ffs.q`: Fossil fuel subsidy reform: quantity of the line** (ktoe)

- Description: fuel use of the line (R2.9)
- Legacy: legacy rows 17767-17782
- Rows: coa,ind, nga,ind
  - 2022-2041: `ffs.q(t) = fuq[f,s](t)`
- Rows: coa,res, nga,res
  - 2022-2041: `ffs.q(t) = fuq[f,bld](t)`
- Rows: coa,pow, nga,pow, oop,pow
  - 2022-2041: `ffs.q(t) = pe[f,s](t)`
- Rows: gso,rd, die,rd
  - 2022-2041: `ffs.q(t) = fuq[f,tra](t)`
- Rows: lpg,all
  - 2022-2041: `ffs.q(t) = ener[f,s](t)`
- Rows: ker,all
  - 2022-2041: `ffs.q(t) = (ener[f,s](t)+ener[jfu,s](t))`
- ... and 4 further row patterns (see the workbook)

**E1222. `env.ffs.cost`: Fossil fuel subsidy reform: environmental benefits (Harberger)** (USD bn real)

- Description: -(global climate cost + local costs) x change in use x PJ per ktoe / MperBn (R2.9-R2.10; issue I107)
- Legacy: legacy rows 17767-17783 (L179, L180 fixed)
- Rows: coa,ind, coa,res, coa,pow, nga,ind, nga,res, nga,pow, oop,pow, oop,ind, coa,oth, nga,oth
  - 2022-2041: `env.ffs.cost(t) = -(cc.glo[f,all](t)+airpol.cost.gj[f,s](t))*(ffs.q[f,s](t)-INDEX(ffs.q[f,s](..t),row10(t)))*PJperKtoe/MperBn`
- Rows: gso,rd, die,rd
  - 2022-2041: `env.ffs.cost(t) = -(cc.glo[f,all](t)+tot.ext[f,all](t))*(ffs.q[f,s](t)-INDEX(ffs.q[f,s](..t),row10(t)))*PJperKtoe/MperBn`
- Rows: lpg,all, ker,all
  - 2022-2041: `env.ffs.cost(t) = -(cc.glo[f,s](t)+airpol.cost.gj[f,s](t))*(ffs.q[f,s](t)-INDEX(ffs.q[f,s](..t),row10(t)))*PJperKtoe/MperBn`
- Rows: gso,oth
  - 2022-2041: `env.ffs.cost(t) = -(cc.glo[f,all](t)+airpol.cost.gj[f,all](t))*(ffs.q[f,s](t)-INDEX(ffs.q[f,s](..t),row10(t)))*PJperKtoe/MperBn`
- Rows: die,oth
  - 2022-2041: `env.ffs.cost(t) = -(cc.glo[oop,all](t)+airpol.cost.gj[odo,s](t))*(ffs.q[f,s](t)-INDEX(ffs.q[f,s](..t),row10(t)))*PJperKtoe/MperBn`
- Rows: tot
  - 2022-2041: `env.ffs.cost(t) = SUM(env.ffs.cost[16 rows](t))`

**E1223. `wel.ffs`: Total national welfare benefits (FFS)** (USD bn real)

- Description: env.ffs.cost total - eff.all - mfc.all (R2.10)
- Legacy: legacy row 17784
  - 2022-2041: `wel.ffs(t) = env.ffs.cost[tot](t)-eff[all,all](t)-mfc[all,all](t)`

**E1224. `vatgen`: General VAT rate of the year** (share)

- Description: VAT_WEO of the year up to LastHistPriceYear, then the last historical year's rate (bug M15 fixed, v0.9.2)
- Legacy: legacy: one fixed cell
  - 2022-2041: `vatgen(t) = INDEX(VatWeo,MATCH(MIN(year,Settings[Last historical price year]),VatWeoYr,0))`

**E1225. `supcost`: Energy subsidies: supply cost** (USD/GJ, USD/kWh)

- Description: sp of section 2 (electricity: spe of 3 G2, v0.9.0); other lines: use-weighted (R2.11, L187 fixed)
- Legacy: legacy rows 17792-17944
- Rows: gso,all, die,all, lpg,all, ker,all, oop,all, nga,ind, nga,res, nga,pow, coa,ind, coa,res, coa,pow
  - 2022-2041: `supcost(t) = sp[f,s](t)`
- Rows: nga,oth, coa,oth
  - 2022-2041: `supcost(t) = IFERROR(SUMPRODUCT(supcost[3 rows](t),con[3 rows](t))/SUM(con[3 rows](t)),AVERAGE(supcost[3 rows](t)))`
- Rows: ecy,ind, ecy,res
  - 2022-2041: `supcost(t) = spe[f,s](t)`
- Rows: ecy,oth
  - 2022-2041: `supcost(t) = IFERROR(SUMPRODUCT(supcost[2 rows](t),con[2 rows](t))/SUM(con[2 rows](t)),AVERAGE(supcost[2 rows](t)))`

**E1226. `extcost`: Energy subsidies: externalities incl. climate (global SCC)** (USD/GJ, USD/kWh)

- Description: cc.glo + local costs; electricity 0 (R2.11, issue I108; L183 fixed)
- Legacy: legacy rows 17794-17941
- Rows: gso,all, die,all
  - 2022-2041: `extcost(t) = cc.glo[f,s](t)+tot.ext[f,s](t)`
- Rows: lpg,all, ker,all
  - 2022-2041: `extcost(t) = cc.glo[f,s](t)+airpol.cost.gj[f,s](t)`
- Rows: oop,all
  - 2022-2041: `extcost(t) = cc.glo[f,s](t)+airpol.cost.gj[f,avg](t)`
- Rows: nga,ind, nga,res, nga,pow, coa,ind, coa,res, coa,pow
  - 2022-2041: `extcost(t) = cc.glo[f,all](t)+airpol.cost.gj[f,s](t)`
- Rows: nga,oth, coa,oth
  - 2022-2041: `extcost(t) = IFERROR(SUMPRODUCT(extcost[3 rows](t),con[3 rows](t))/SUM(con[3 rows](t)),AVERAGE(extcost[3 rows](t)))`
- Rows: ecy,ind, ecy,res
  - 2022-2041: `extcost(t) = 0`
- ... and 1 further row patterns (see the workbook)

**E1227. `vatext`: Energy subsidies: VAT on supply cost and externalities** (USD/GJ, USD/kWh)

- Description: (supcost + extcost) x D x vatgen (D: household share for oil products; residential lines 1; others 0) (R2.11, issue I109; L184, L185, M15 fixed)
- Legacy: legacy rows 17796-17943
- Rows: gso,all, die,all, lpg,all, ker,all, oop,all, nga,ind, nga,res, nga,pow, coa,ind, coa,res, coa,pow, ecy,ind, ... (13 rows)
  - 2022-2041: `vatext(t) = (supcost[f,s](t)+extcost[f,s](t))*<consumer flag x household share>*vatgen(t)`
  - Parameters: `<consumer flag x household share>` = `Inputs!U164`
- Rows: nga,oth, coa,oth
  - 2022-2041: `vatext(t) = IFERROR(SUMPRODUCT(vatext[3 rows](t),con[3 rows](t))/SUM(con[3 rows](t)),AVERAGE(vatext[3 rows](t)))`
- Rows: ecy,oth
  - 2022-2041: `vatext(t) = IFERROR(SUMPRODUCT(vatext[2 rows](t),con[2 rows](t))/SUM(con[2 rows](t)),AVERAGE(vatext[2 rows](t)))`

**E1228. `effprice`: Energy subsidies: efficient price** (USD/GJ, USD/kWh)

- Description: supcost + extcost + vatext (R2.11)
- Legacy: legacy rows 17795-17942
- Rows: gso,all, die,all, lpg,all, ker,all, oop,all, nga,ind, nga,res, nga,pow, nga,oth, coa,ind, coa,res, coa,pow, ... (16 rows)
  - 2022-2041: `effprice(t) = supcost[f,s](t)+extcost[f,s](t)+vatext[f,s](t)`

**E1229. `rpsub`: Energy subsidies: retail price of the scenario** (USD/GJ, USD/kWh)

- Description: rpn of section 2 (electricity: rp of 3 G) (R2.11; L181, L182 fixed)
- Legacy: legacy rows 17797-17943
- Rows: gso,all, die,all, lpg,all, ker,all, oop,all, nga,ind, nga,res, nga,pow, coa,ind, coa,res, coa,pow
  - 2022-2041: `rpsub(t) = rpn[f,s](t)`
- Rows: nga,oth, coa,oth
  - 2022-2041: `rpsub(t) = IFERROR(SUMPRODUCT(rpsub[3 rows](t),con[3 rows](t))/SUM(con[3 rows](t)),AVERAGE(rpsub[3 rows](t)))`
- Rows: ecy,ind, ecy,res
  - 2022-2041: `rpsub(t) = rp[f,s](t)`
- Rows: ecy,oth
  - 2022-2041: `rpsub(t) = IFERROR(SUMPRODUCT(rpsub[2 rows](t),con[2 rows](t))/SUM(con[2 rows](t)),AVERAGE(rpsub[2 rows](t)))`

**E1230. `con`: Energy subsidies: consumption of the line** (PJ, GWh)

- Description: fuel use x PJ per ktoe (electricity: demand x KtoeGWh) (R2.11, L186 fixed)
- Legacy: legacy rows 17793-17940
- Rows: gso,all, die,all, lpg,all, oop,all
  - 2022-2041: `con(t) = ener[f,s](t)*PJperKtoe`
- Rows: ker,all
  - 2022-2041: `con(t) = (ener[f,s](t)+ener[jfu,s](t))*PJperKtoe`
- Rows: nga,ind, coa,ind
  - 2022-2041: `con(t) = fuq[f,s](t)*PJperKtoe`
- Rows: nga,res, coa,res
  - 2022-2041: `con(t) = fuq[f,bld](t)*PJperKtoe`
- Rows: nga,pow, coa,pow
  - 2022-2041: `con(t) = pe[f,s](t)*PJperKtoe`
- Rows: nga,oth, coa,oth
  - 2022-2041: `con(t) = (fuq[f,tra](t)+fuq[f,oen](t))*PJperKtoe`
- ... and 3 further row patterns (see the workbook)

**E1231. `expsub.con`: Explicit consumer subsidy** (USD bn real)

- Description: MAX(0, supcost - rpsub) x con / MperBn (R2.11-R2.12)
- Legacy: legacy rows 17798-17948
- Rows: gso,all, die,all, lpg,all, ker,all, oop,all, nga,ind, nga,res, nga,pow, nga,oth, coa,ind, coa,res, coa,pow, ... (16 rows)
  - 2022-2041: `expsub.con(t) = MAX(0,supcost[f,s](t)-rpsub[f,s](t))*con[f,s](t)/MperBn`
- Rows: tot
  - 2022-2041: `expsub.con(t) = SUM(expsub.con[16 rows](t))`

**E1232. `impsub.con`: Implicit consumer subsidy** (USD bn real)

- Description: [rpsub <= effprice] x (effprice - MAX(rpsub, supcost)) x con / MperBn (R2.11-R2.12)
- Legacy: legacy rows 17799-17949
- Rows: gso,all, die,all, lpg,all, ker,all, oop,all, nga,ind, nga,res, nga,pow, nga,oth, coa,ind, coa,res, coa,pow, ... (16 rows)
  - 2022-2041: `impsub.con(t) = (rpsub[f,s](t)<=effprice[f,s](t))*(effprice[f,s](t)-MAX(rpsub[f,s](t),supcost[f,s](t)))*con[f,s](t)/MperBn`
- Rows: tot
  - 2022-2041: `impsub.con(t) = SUM(impsub.con[16 rows](t))`

**E1233. `expsubgdp.con`: Explicit consumer subsidy, share of baseline GDP** (share)

- Description: total / gdp.usd of the year (R2.12, L188 fixed)
- Legacy: legacy row 17950
- Rows: tot
  - 2022-2041: `expsubgdp.con(t) = expsub.con[s](t)/gdp.usd[all,all](t)`

**E1234. `impsubgdp.con`: Implicit consumer subsidy, share of baseline GDP** (share)

- Description: total / gdp.usd (R2.12)
- Legacy: legacy row 17951
- Rows: tot
  - 2022-2041: `impsubgdp.con(t) = impsub.con[s](t)/gdp.usd[all,all](t)`

**E1235. `airpol.ecy.g`: Air-pollution cost of electricity for the efficient price (own scenario; read for scenario 1)** (USD/kWh)

- Description: sum of power cost x generation / total generation x KtoeGWh / Thousand (R3.15, issue I121)
- Legacy: legacy row 18090
  - 2022-2041: `airpol.ecy.g(t) = (airpol.cost.gj[coa,pow](t)*gen_mwy[coa,pow](t)+airpol.cost.gj[nga,pow](t)*gen_mwy[nga,pow](t)+airpol.cost.gj[oop,pow](t)*gen_mwy[oop,pow](t))/gtot(t)*KtoeGWh/Thousand`

**E1236. `acc.cost`: Efficient price: accident cost per litre (scenario)** (USD/l)

- Description: tran.acc.cost (R3.14)
- Legacy: legacy rows 17965, 17980
- Rows: gso,all, die,all
  - 2022-2041: `acc.cost(t) = tran.acc.cost[f,s](t)`

**E1237. `con.cost`: Efficient price: congestion cost per litre (scenario)** (USD/l)

- Description: tran.con.cost (R3.14)
- Legacy: legacy rows 17966, 17981
- Rows: gso,all, die,all
  - 2022-2041: `con.cost(t) = tran.con.cost[f,s](t)`

**E1238. `rdm.cost`: Efficient price: road damage cost per litre of diesel (scenario)** (USD/l)

- Description: tran.rdm.cost (R3.14, issue I118)
- Legacy: legacy row 17982
- Rows: die,all
  - 2022-2041: `rdm.cost(t) = tran.rdm.cost[f,s](t)`

**E1239. `sup.cost`: Efficient price: supply cost of scenario 1** (USD per price unit)

- Description: sp of scenario 1 x GJ per price unit (electricity: spe, v0.9.0) (R3.13)
- Legacy: legacy rows 17963-18101 (16194-16206)
- Rows: gso,all, die,all, lpg,all, ker,all, coa,ind, coa,res, coa,pow, nga,ind, nga,res, nga,pow
  - 2022-2041: `sup.cost(t) = INDEX(sp[f,s](..t),row10(t))*<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `<GJ per price unit of pset[f,s]>`
- Rows: ecy,ind, ecy,res
  - 2022-2041: `sup.cost(t) = INDEX(spe[f,s](..t),row10(t))*<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `data`

**E1240. `airpol.cost.s`: Efficient price: air-pollution cost** (USD per price unit)

- Description: airpol.cost (oil products), airpol.cost.gj (coal, gas), airpol.ecy.g of scenario 1 (electricity) (R3.14-R3.15)
- Legacy: legacy rows 17964-18102
- Rows: gso,all, die,all, lpg,all, ker,all
  - 2022-2041: `airpol.cost.s(t) = airpol.cost[f,s](t)`
- Rows: coa,ind, coa,res, coa,pow, nga,ind, nga,res, nga,pow
  - 2022-2041: `airpol.cost.s(t) = airpol.cost.gj[f,s](t)`
- Rows: ecy,ind, ecy,res
  - 2022-2041: `airpol.cost.s(t) = INDEX(airpol.ecy.g(..t),row10(t))`

**E1241. `scc.cost`: Efficient price: climate damage (national SCC)** (USD per price unit)

- Description: cc.code of section 1 (R3.14)
- Legacy: legacy rows 17968-18079
- Rows: gso,all, die,all, lpg,all, ker,all, coa,ind, coa,res, coa,pow, nga,ind, nga,res, nga,pow
  - 2022-2041: `scc.cost(t) = cc.code[f,s](t)`
- Rows: ecy,ind, ecy,res
  - 2022-2041: `scc.cost(t) = 0`

**E1242. `pig`: Pigouvian tax: all externalities (reference)** (USD per price unit)

- Description: air pollution + climate + accidents + congestion + road damage (R3.20)
- Legacy: legacy rows 17974-18109
- Rows: gso,all
  - 2022-2041: `pig(t) = airpol.cost.s[f,s](t)+scc.cost[f,s](t)+acc.cost[f,s](t)+con.cost[f,s](t)`
- Rows: die,all
  - 2022-2041: `pig(t) = airpol.cost.s[f,s](t)+scc.cost[f,s](t)+acc.cost[f,s](t)+con.cost[f,s](t)+rdm.cost[f,s](t)`
- Rows: lpg,all, ker,all, coa,ind, coa,res, coa,pow, nga,ind, nga,res, nga,pow, ecy,ind, ecy,res
  - 2022-2041: `pig(t) = airpol.cost.s[f,s](t)+scc.cost[f,s](t)`

**E1243. `vat.cost`: Efficient price: potential VAT** (USD per price unit)

- Description: (sup.cost + pig x [ExternalityAddVAT = Yes]) x D x vatgen (D: 1 for consumer fuels, else 0) (R3.16, issue I120; M15 fixed)
- Legacy: legacy rows 17969-18104
- Rows: gso,all, die,all, lpg,all, ker,all, coa,ind, coa,res, coa,pow, nga,ind, nga,res, nga,pow, ecy,ind, ecy,res
  - 2022-2041: `vat.cost(t) = (sup.cost[f,s](t)+pig[f,s](t)*(LEFT(ExternalityAddVAT(t),3)="Yes"))*<consumer flag>*vatgen(t)`
  - Parameters: `<consumer flag>` = `data`

**E1244. `eff.price`: Efficient price** (USD per price unit)

- Description: sup.cost + pig + vat.cost (R3.17)
- Legacy: legacy rows 17962-18100
- Rows: gso,all, die,all, lpg,all, ker,all, coa,ind, coa,res, coa,pow, nga,ind, nga,res, nga,pow, ecy,ind, ecy,res
  - 2022-2041: `eff.price(t) = sup.cost[f,s](t)+pig[f,s](t)+vat.cost[f,s](t)`

**E1245. `rp.eff`: Efficient price block: retail price of the scenario** (USD per price unit)

- Description: rpn x GJ per price unit (electricity: rp) (R3.18)
- Legacy: legacy rows 17970-18105
- Rows: gso,all, die,all, lpg,all, ker,all, coa,ind, coa,res, coa,pow, nga,ind, nga,res, nga,pow
  - 2022-2041: `rp.eff(t) = rpn[f,s](t)*<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `<GJ per price unit of pset[f,s]>`
- Rows: ecy,ind, ecy,res
  - 2022-2041: `rp.eff(t) = rp[f,s](t)*<GJ per price unit>`
  - Parameters: `<GJ per price unit>` = `data`

**E1246. `tgap`: Tax gap: retail price - efficient price** (USD per price unit)

- Description: rp.eff - eff.price (R3.19)
- Legacy: legacy rows 17971-18106
- Rows: gso,all, die,all, lpg,all, ker,all, coa,ind, coa,res, coa,pow, nga,ind, nga,res, nga,pow, ecy,ind, ecy,res
  - 2022-2041: `tgap(t) = rp.eff[f,s](t)-eff.price[f,s](t)`

**E1247. `pig.co2e`: Pigouvian tax per tonne of CO2 (fuel lines; avg: weighted by the fuel use of the scenario)** (USD/tCO2)

- Description: pig x scc.glo / scc.cost (0 without climate cost); avg: SUMPRODUCT with effp.q (R3.21-R3.22)
- Legacy: legacy rows 17975-18111, 18117-18118
- Rows: gso,all, die,all, lpg,all, ker,all
  - 2022-2041: `pig.co2e(t) = IFERROR(pig[f,s](t)*scc[glo,s](t)/scc.cost[f,s](t),0)`
- Rows: coa,ind, coa,res, coa,pow, nga,ind, nga,res, nga,pow, ecy,ind, ecy,res
  - 2022-2041: `pig.co2e(t) = IFERROR(pig[f,s](t)*scc[glo,all](t)/scc.cost[f,s](t),0)`
- Rows: avg
  - 2022-2041: `pig.co2e(t) = IF(SUM(effp.q[10 rows](t))=0,0,SUMPRODUCT(pig.co2e[10 rows](t),effp.q[10 rows](t))/SUM(effp.q[10 rows](t)))`

**E1248. `app`: Air-pollution part of the Pigouvian tax per tonne of CO2** (USD/tCO2)

- Description: pig.co2e x airpol.cost.s / pig; avg: weighted (R3.21-R3.22)
- Legacy: legacy rows 17976-18111, 18122-18123
- Rows: gso,all, die,all, lpg,all, ker,all, coa,ind, coa,res, coa,pow, nga,ind, nga,res, nga,pow, ecy,ind, ecy,res
  - 2022-2041: `app(t) = IFERROR(pig.co2e[f,s](t)*airpol.cost.s[f,s](t)/pig[f,s](t),0)`
- Rows: avg
  - 2022-2041: `app(t) = IF(SUM(effp.q[10 rows](t))=0,0,SUMPRODUCT(app[10 rows](t),effp.q[10 rows](t))/SUM(effp.q[10 rows](t)))`

**E1249. `txo.co2e`: Excise and other taxes of scenario 1 per tonne of CO2** (USD/tCO2)

- Description: txo of scenario 1 x GJ per price unit x scc.glo / scc.cost (0 without climate cost, L203) (R3.21)
- Legacy: legacy rows 17972-18108
- Rows: gso,all, die,all, lpg,all, ker,all
  - 2022-2041: `txo.co2e(t) = IFERROR(INDEX(txo[f,s](..t),row10(t))*<GJ per price unit>*scc[glo,s](t)/scc.cost[f,s](t),0)`
  - Parameters: `<GJ per price unit>` = `<GJ per price unit of pset[f,s]>`
- Rows: coa,ind, coa,res, coa,pow, nga,ind, nga,res, nga,pow
  - 2022-2041: `txo.co2e(t) = IFERROR(INDEX(txo[f,s](..t),row10(t))*<GJ per price unit>*scc[glo,all](t)/scc.cost[f,s](t),0)`
  - Parameters: `<GJ per price unit>` = `<GJ per price unit of pset[f,s]>`
- Rows: ecy,ind, ecy,res
  - 2022-2041: `txo.co2e(t) = 0`
  - Parameters: `<GJ per price unit>` = `data`

**E1250. `effp.q`: Efficient prices: fuel use weights of the averages** (ktoe)

- Description: total use (oil products), sector use (coal, gas: industry, buildings, power) (R3.22)
- Legacy: legacy rows 18113-18116
- Rows: gso,all, die,all, lpg,all
  - 2022-2041: `effp.q(t) = ener[f,s](t)`
- Rows: ker,all
  - 2022-2041: `effp.q(t) = (ener[f,s](t)+ener[jfu,s](t))`
- Rows: coa,ind, nga,ind
  - 2022-2041: `effp.q(t) = fuq[f,s](t)`
- Rows: coa,res, nga,res
  - 2022-2041: `effp.q(t) = fuq[f,bld](t)`
- Rows: coa,pow, nga,pow
  - 2022-2041: `effp.q(t) = pe[f,s](t)`

### 15; 19

**E1251. `ap.w`: Weight of the final emission factor (local air pollutants)** (share)

- Description: EFFinShare x (year - base year) / (EFEndYear - base year)
- Legacy: legacy Mitigation rows 1052-1663 (linear factor path)
- Rows: all,all
  - 2022-2041: `ap.w(t) = EFFinShare*(year-BaseYr)/(EFEndYear-BaseYr)`

**E1252. `apfd`: Food fuel use within food & forestry** (ktoe)

- Description: Food & forestry fuel use x food share of the fuel (Balances info_food / info_agrc + info_fish + info_food + info_wood; v0.4.11, LD53)
- Legacy: legacy Mitigation rows 501-504, 1666-1673
- Rows: coa,foo
  - 2022-2041: `apfd(t) = ener[f,s](t)*Inputs!BD50`
- Rows: nga,foo
  - 2022-2041: `apfd(t) = ener[f,s](t)*Inputs!BD51`
- Rows: gso,foo
  - 2022-2041: `apfd(t) = ener[f,s](t)*Inputs!BD52`
- Rows: die,foo
  - 2022-2041: `apfd(t) = ener[f,s](t)*Inputs!BD53`
- Rows: lpg,foo
  - 2022-2041: `apfd(t) = ener[f,s](t)*Inputs!BD54`
- Rows: ker,foo
  - 2022-2041: `apfd(t) = ener[f,s](t)*Inputs!BD55`
- ... and 3 further row patterns (see the workbook)

**E1253. `ap`: Local air pollutant emissions** (kt)

- Description: Fuel use x emission factor (GAINS, sheet EF_PM by legacy EF code: country, else region, else world; other energy the maximum of the other subsectors; Inputs_ef; base-year and final factor weighted by ap.w), summed over the fuels; power: generation fuel use by type
- Legacy: legacy Mitigation rows 1052-1663 (factors), 6591-7409 (section 13)
- Changes against legacy: LD49, LD50, L22, LD52, L23 (section B)
- Rows: pm2,rod
  - 2022-2041: `ap(t) = SUMPRODUCT(ener[9 rows](t),Inputs!AG5:AG13*(1-ap.w[all,all](t))+ap.w[all,all](t)*Inputs!AH5:AH13)/tPerKt`
- Rows: pm2,ral
  - 2022-2041: `ap(t) = SUMPRODUCT(ener[9 rows](t),Inputs!AG14:AG22*(1-ap.w[all,all](t))+ap.w[all,all](t)*Inputs!AH14:AH22)/tPerKt`
- Rows: pm2,avi
  - 2022-2041: `ap(t) = SUMPRODUCT(ener[9 rows](t),Inputs!AG23:AG31*(1-ap.w[all,all](t))+ap.w[all,all](t)*Inputs!AH23:AH31)/tPerKt`
- Rows: pm2,nav
  - 2022-2041: `ap(t) = SUMPRODUCT(ener[9 rows](t),Inputs!AG32:AG40*(1-ap.w[all,all](t))+ap.w[all,all](t)*Inputs!AH32:AH40)/tPerKt`
- Rows: pm2,res
  - 2022-2041: `ap(t) = SUMPRODUCT(ener[9 rows](t),Inputs!AG41:AG49*(1-ap.w[all,all](t))+ap.w[all,all](t)*Inputs!AH41:AH49)/tPerKt`
- Rows: pm2,foo
  - 2022-2041: `ap(t) = SUMPRODUCT(ener[9 rows](t),Inputs!AG50:AG58*(1-ap.w[all,all](t))+ap.w[all,all](t)*Inputs!AH50:AH58)/tPerKt`
- ... and 125 further row patterns (see the workbook)

**E1254. `apf`: Forcing of local air pollutants (memo, not in the GHG totals)** (Mt CO2e)

- Description: Emissions (kt) x GWP100 of the GAINS region / ktPerMt
- Legacy: legacy Mitigation rows 7459-7530
- Rows: bc,all, oc,all, nox,all, so2,all, voc,all, co,all
  - 2022-2041: `apf(t) = ap[f,s](t)*<GWP100 (sheet EF_GHG, gwp100 rows)>/ktPerMt`
  - Parameters: `<GWP100 (sheet EF_GHG, gwp100 rows)>` = `INDEX(EFVal,MATCH(INDEX(RegVal,MATCH(CtryCode,RegKey,0))&".mit.gwp100.bc",EFKey,0))`
- Rows: all,all
  - 2022-2041: `apf(t) = SUM(apf[6 rows](t))`

**E1255. `aps`: Local air pollutant emissions by air-pollution module sector** (kt)

- Description: Coal and gas power plants: fuel use of the type x emission factor; other sectors: sums of the subsector rows; POM = PomPerOC x OC; other PM2.5 = MAX(0, PM2.5 - BC - POM); CH4 (v0.3.12, as legacy): combustion CH4 of the sector, plus fossil fuel supply methane in other and agriculture and waste methane in food & forestry; all = sum of the seven sectors
- Legacy: legacy Mitigation rows 6693-6704 (each pollutant), 7310-7321, 7425-7446; input table 15859-15961
- Changes against legacy: LD51, LD52 (section B)
- Rows: nox,cpp
  - 2022-2041: `aps(t) = SUMPRODUCT(pe[coa,pow](t),Inputs!BU207*(1-ap.w[all,all](t))+ap.w[all,all](t)*Inputs!BV207)/tPerKt`
- Rows: so2,cpp
  - 2022-2041: `aps(t) = SUMPRODUCT(pe[coa,pow](t),Inputs!BW207*(1-ap.w[all,all](t))+ap.w[all,all](t)*Inputs!BX207)/tPerKt`
- Rows: bc,cpp
  - 2022-2041: `aps(t) = SUMPRODUCT(pe[coa,pow](t),Inputs!CA207*(1-ap.w[all,all](t))+ap.w[all,all](t)*Inputs!CB207)/tPerKt`
- Rows: pom,cpp, pom,gpp, pom,opp, pom,rod, pom,gro, pom,oth, pom,foo
  - 2022-2041: `aps(t) = aps[oc,s](t)*PomPerOC`
- Rows: opm,cpp, opm,gpp, opm,opp, opm,rod, opm,gro, opm,oth, opm,foo
  - 2022-2041: `aps(t) = MAX(0,aps[pm2,s](t)-aps[bc,s](t)-aps[pom,s](t))`
- Rows: voc,cpp
  - 2022-2041: `aps(t) = SUMPRODUCT(pe[coa,pow](t),Inputs!BY207*(1-ap.w[all,all](t))+ap.w[all,all](t)*Inputs!BZ207)/tPerKt`
- ... and 22 further row patterns (see the workbook)

**E1256. `apen`: Energy use read by the air-pollution module: power generation and residential by fuel** (ktoe)

- Description: pe of section 3 I; residential ener (electricity: demand) of section 6
- Legacy: legacy E3 rows 15814-15840
- Rows: coa,pow, nga,pow, oop,pow, bio,pow
  - 2022-2041: `apen(t) = pe[f,s](t)`
- Rows: coa,res, nga,res, gso,res, die,res, lpg,res, ker,res, jfu,res, oop,res, bio,res
  - 2022-2041: `apen(t) = ener[f,s](t)`
- Rows: ecy,res
  - 2022-2041: `apen(t) = eldem[f,s](t)`

**E1257. `apco2`: CO2 from energy read by the air-pollution module** (MtCO2)

- Description: co2.all of section 13
- Legacy: legacy E3 row 16054
  - 2022-2041: `apco2(t) = co2[all,all](t)`

## B. Changes against legacy CPAT

Each change is described in the workbook sheet `LegacyDiff` (LD) or in the register of bugs, issues and upgrades (`Legacy_CPAT_Bugs_v<version>.docx` and the tracker: L legacy bug fixed, M bug of an earlier prototype version). Equations: the numbers of section A it touches.

| ID | Area | Type | Equations |
|---|---|---|---|
| LD1 | Elasticities: food & forestry: The same (v0.9.0; v0.0.11-v0.8.5: services elasticities) | Same | E446 |
| LD2 | Other oil products: pass-through and margin: From the IMF dataset like the other oil products (Egypt 0 and 7.95 $/bbl) | Decision | E247, E249 |
| LD3 | VAT rate where the dataset is blank: General VAT rate VAT_WEO for residential coal and gas and all-sector oil products; 0 for power, industry, biomass. Only for blank cells (v0.0.14) | Bug fix | E254 |
| LD4 | Egypt price data: The same (checked cell by cell 2026-10-29: equal but the spot coal and gas cells, which 465 fills with a year and 0, issue I150); cells changed from the original module data still bright yellow in Prices_dom | Same | E247, E249 |
| LD5 | Oil-product share in the VAT of transport fuels: VAT rate x household share of the oil product (sheet OilProductShares, as legacy rows 801-816; v0.4.12); VAT payment = (supply cost + taxes) x rate x share | Bug fix | E254 |
| LD6 | New ETS price: Same cap; fast estimate in log form LN(cap/baseline)/(semi x effectiveness x volatility adjustment); override row pasted from ets_goalseek.py (Python, same damped log-space step, no VBA); baseline covered emissions are data from scenario 1 (bco2) | Bug fix | E86, E88 |
| LD7 | ETS allocation: As legacy (v0.4.15, user 2026-10-18; issue I21): one auctioned share of the scenario (MTInputs rows 90-91) for every sector; benchmark = 1 - auctioned share (sector groups pow, tra, res, ind kept for benchmarks by sector later), linear from the start to the target year, held after it; OBR share = benchmark | Same | E76, E75 |
| LD8 | ETS volatility: Volatility adjustment (1 + policy risk x impact)/(1 + volatility x impact) from MTInputs 95-97 (1/1.1 at Medium) on the tax-equivalent price and in the fast estimate | Bug fix | E81, E79 |
| LD9 | Sectoral shadow prices: As legacy, bugs fixed (v0.4.16, LD9): feebates x MTInputs row 251 + regulation shadow price + OBR part of the ETS; the main scenario (MTInputs row 13, ScenarioSelected; legacy scenario table on Mapping) sets explicit or shadow pricing, the efficiency adjustment (rows 247-251) and the sectors covered; under shadow pricing the carbon price path is a shadow price (reg = shadow carbon price x adjustment x coverage) and there is no explicit carbon tax; power included | Same | E109 |
| LD10 | Policy paths after the target year: The same (v0.9.0; v0.0.8-v0.8.5: linear for the reform and feebates); legacy bugs L171 (hold the target under No) and L173 (1 + rate) fixed; ETS benchmarks constant; ETS cap per MTInputs switch | Bug fix | E235, E28, E95 |
| LD11 | Scenario batch runs: Same idea: RunAllScenarios copies each definition (MTInputs L onwards, Run? = Yes) into the live column K, runs the ETS goal seek when needed, stores MTOutputs values in StoredResults; ScenarioCompare compares one year | Same | - |
| LD12 | Feebate grouping: Same: food & forestry and services take the residential rate; other energy use the industry rate | Same | E95 |
| LD13 | Biomass carbon-tax coverage: TRUE (EF 0) | Decision | E19 |
| LD14 | Sign of subsidies: Subsidies negative: esub, esubpu, rsub, prsub, sgap, rgap; net existing revenue rnet = rtx + rsub | Decision | E462, E253, E245 |
| LD15 | Constants and row pointers: Looked up: named constants and policy assumptions on sheet Constants, MTInputs rows on Mapping (by NameOfParameter or label), baseline CO2 on sheet BaselineCO2 | Decision | - |
| LD16 | Margins and production costs: The same years and weight (v0.9.0), converted to real with the CPI index of the year read | Bug fix | E247 |
| LD17 | Existing taxes and subsidies: Split by the sign of txo: etx = max(txo, 0), esub = min(txo, 0) (subsidies negative) | Same | E252, E253 |
| LD18 | Subsidy and price-control phase-outs: As legacy (v0.4.16, LD18): separate policy lines, not in the pre-policy build-up (user 2026-10-18): phase-out factors (MTInputs 123-137, 191-195; baseline / policy as legacy rows 264-274), lines by price fuel | sector (inclusion switches on Constants, default every block), txo split into a fixed and a floating part, wedges pcsw (consumer subsidy reform: the fixed subsidy) and ppcw (price-control phase-out: the floating part) by price block, csw and pcw in every subsector block (after-tax price), revenue rsr | Same | E28 |
| LD19 | Producer subsidies: In the supply cost as legacy (v0.9.0, R7): per-unit subsidy psu (Prices_dom mit.pros, or Manual inputs) up to the last price year, then x the phase-out factor psf; block row psp in the supply cost, so the floating taxes and price controls absorb (1 - pass-through) of the phase-out; fiscal line rpsu by fuel. Electricity: allocation by the pre-tax gap (psesh), per kWh floored at -0.3 $/kWh (pseu), residual memo (pser), passed through in the price before policies (rppre). v0.4.16-v0.8.5: fiscal line only; v0.6.2-v0.8.5: a separate wedge (psw, ppsw, psr; removed) | Same | - |
| LD20 | Ad-valorem baseline taxes; Europe LNG shift: v0.5.6: as legacy (Inputs_pint series nga.eus, row 3 share path; Settings C12 = eus for Europe markets); fixed taxes as legacy | Same | E249 |
| LD21 | Fuel-use equation: CPAT eq. 3.3.3 x the shock factor (v0.3.11, header row 6, switch Settings C19 on, as legacy; issue I92); v0.4.12: GDP growth with the income factor (row 14; was issue I23); v0.4.13: additional policy efficiency gains as legacy (MTInputs 243-245 by scenario: road vehicles = road, rail, aviation, navigation; residential; industrial = the other subsectors; row aef of each subsector); v0.5.4: power demand takes MTInputs 242 of its own scenario, like every power input (section-1 row AdditionalEfficiencyPower, section 3 row aeef) | Same | E446 |
| LD22 | Power engineer model (v0.1.06): Same method, year by year (method test: 208 legacy rows of the baseline and the carbon-tax run reproduced to 1e-13 with the bugs switched on) | Same | - |
| LD23 | Power: bug fixes (v0.1.06): Fixed | Bug fix | E386, E387, E427, E434, E334, E423, E417, E419, E407 |
| LD24 | Power demand: 2023-2024 demand shock: Same: switch Settings C19, on by default since v0.3.11 (fuels and power, as legacy; issue I92) | Same | E319, E387 |
| LD25 | Power demand and sector policies: Same; electricity demand shown as memo lines in the sector blocks and section 11 (not in the fuel totals) | Same | E387 |
| LD26 | Power: planned retirement: Every type: switch planned_retirement (PowerTech) and data rows pret|<type> (PowerPaths); retirement = MIN(planned or rate-based + early coal, capacity) | Same | E411, E412 |
| LD27 | Power demand: road electricity: v0.3.5: from section 5b (engineer road model) where TrModel = Engineer; else grows with the transport multiple (legacy fallback) | Same | E387 |
| LD28 | Power: features not built: Dropped (user decisions 4 and 5 of the power plan; the rebate covers the demand-side feebate). Built: v0.5.4 PPAs, deficit to gas, renewable subsidies, rebate, electricity excise, every power input by scenario; v0.5.6 manual capacity and investment (P3: rows mancap, mani, needm; Manual inputs 349-357 scenario 1, 363-371 other scenarios; legacy bug L118 fixed: logit investment sized on the need net of manual investment) | Simplification | - |
| LD29 | Power: levelised variable cost window: To the last model year 2041 (v0.2.3); without LAMBDA support the 2041 cost is last year's (tvcx) | Same | E338, E337 |
| LD30 | Power: generation costs (v0.1.05): One row per type for amortised and for levelised fixed cost; discounted lifetime in closed form; constants derived in Inputs_power | Same | E323, E339 |
| LD31 | Power: fuel prices: Trailing average of the price before new policies over t-4 .. t from 2022 (row fpp; L126 fixed, as legacy 465 rows 3155-3157); Settings C21 SpotPow = Yes for spot prices | Same | E329 |
| LD32 | Power: end-user prices: Telescoped (S4) with every legacy component: price(t) = price(t-1) + pass-through x change in (supply cost + producer subsidy pseu + consumer subsidy phase-out csd + price-chain residual ores) x (1 + VAT) after the last historical year (v0.9.0, R7.9, R9.3; ores as legacy 465 rows 3607, 3636: held, a negative one scaled by MIN(sc, sc of the last price year)); row spe = the supply cost removing the estimation (legacy 3620, 3649), read by the subsidy and efficient-price lines of section 18 | Same | E357, E358, E362 |
| LD33 | Power: historical electricity prices and VAT: The same | Same | E358 |
| LD34 | Power: coal implicit cost: Built v0.5.6 (P5): row cic from GoalSeekCoal (legacy table, 85 countries, not Egypt) or the Manual inputs of MTInputs 368-369, in the coal variable cost; in generation cost and tariffs unless Settings PwCoalICTariff = No (default Yes, as legacy); memo rows fce, cik, swi, swd (legacy F2-F4, F7; F1, F5, F6 = rows lfx/tic, tvc). The calibration script (goal seek) is not built: the stored legacy values are used | Same | - |
| LD35 | Power: new-policy revenue: v0.1.09: by generation type (prnew): policy cost x generation, the ETS part at the permit price (as the subsectors); rcarb (ccpav x consumption) kept as a memo | Same | E442 |
| LD36 | Emissions: As legacy: CO2 from fuel combustion (IIASA EFs adjusted to the inventory as legacy since v0.4.11, issue I32 replicated; power from v0.1.06); v0.2.8: CH4 from combustion and fuel supply, the inventory categories (process, agriculture, LULUCF, waste, other) and N2O in section 14; v0.2.9: local pollutants in section 15 | Same | E404, E1102 |
| LD37 | Revenue structure: As legacy (v0.4.15, user 2026-10-18: replicate legacy, note issues): the three calculations per subsector and fuel (existing taxes incl. VAT, consumer subsidies, new policies) and power as before, plus block 12e, total revenue by policy as legacy rows 8016-8027: new carbon tax, new excise, existing taxes and subsidies, VAT, auctioned ETS, producer subsidies (electricity subsidy gap), renewable subsidies, methane fee, transport, total (= rtot, check row); per pair rex (excise) and rvt (VAT) | Same | E461, E462, E463 |
| LD38 | Existing carbon pricing: As legacy (v0.4.12): carbon tax with the single rate or fuel rates (single price? flag), national ETS and the EU ETS (EU ETS? = Yes or Both) added up, coverage of each data year (blank = 0), the last data year after; each scheme read from its own block of sheet ECP; the sector of the price fuel (oil products: transport; other oil products: industry); only the change against the level in the price data enters prices and revenue (legacy: ctx and ets inside txo, same numbers); existing ETS revenue at full price and free-allocation and revenue data unused, as legacy | Bug fix | E452, E453, E330 |
| LD39 | Power in the totals: v0.1.09: generation fuel use (coal, gas, oil, biomass) in the fuel totals of section 11; power revenues in section 12; electricity final demand a memo | Same | E446, E404, E439 |
| LD40 | Horizon and indices: To 2041 (v0.2.3; the last year is the LAMBDA year); same indices; values after 2030 not a legacy target | Decision | - |
| LD41 | Data vintage: The same: every extract re-read from legacy 465 (v0.9.0; was 456): balances, base-year fuel use (465 rows 583-601), power plant data, GTAP, non-CO2 EFs changed; prices, CO2 EFs, elasticities identical; HHSurvey and HH_Elast still from 456 (465 holds only headers) | Same | - |
| LD42 | Formula structure: One plain formula per variable block for 2022-2040 (at most 100 characters, no LAMBDA needed); the last year 2041 calls the named LAMBDA of each calculated row (v0.2.3); sheet Lambdas lists them | Same | - |
| LD43 | GHGs: non-energy methane (v0.2.8): Grow with income and population (legacy elasticities); the methane fee abates each source along its own CH4Inputs curve | Bug fix | E1093, E1095, E1097 |
| LD44 | GHGs: flaring (v0.2.8): Reported as CO2 in energy (ghg.flr) | Bug fix | E1101 |
| LD45 | GHGs: population (v0.2.8): UN WPP (sheet UNPop) | Bug fix | E1080, E1081 |
| LD46 | GHGs: methane fee scope (v0.2.8): As legacy (v0.4.12): a switch per source on sheet Manual inputs J196:J200 (v0.5.2: the legacy addresses; shown on Settings rows 47-51; biomass No; downstream gas, fossil fuel production, agriculture, waste Yes), in abatement and revenue; the fee only in policy scenarios (scenario number > 1, legacy row 2238) | Same | E164, E1095 |
| LD47 | GHGs: combustion emission factors (v0.2.8): The same (v0.8.4, issue I98; was a departure: final factor FE fin, flat after) | Same | E460 |
| LD48 | GHGs: local pollutants (v0.2.9): Built in v0.2.9: section 15, by subsector and power (fuel use x GAINS factor), totals by pollutant, forcing memo | Same | - |
| LD49 | Local pollutants: factor mapping (v0.2.9): The same (v0.9.0; table Inputs_nc; v0.2.9-v0.8.5: own subsector mapping and nearest-match fallback) | Same | E1253 |
| LD50 | Local pollutants: navigation (v0.2.9): Navigation included in the transport and total rows | Bug fix | E1253 |
| LD51 | Local pollutants: air-pollution sectors (v0.3.0): Built in v0.3.0 (same sectors, POM = 1.3 x OC, other PM2.5 = MAX(0, PM2.5 - BC - POM)); the hand-off itself to an air-pollution module is not built | Same | E1255 |
| LD52 | Local pollutants: total (v0.3.0): Total = all subsectors + power = sum of the seven air-pollution sectors | Bug fix | E1253, E1255 |
| LD53 | Local pollutants: food split (v0.3.0): Split as legacy (v0.4.11): the food share of each fuel = info_food / the four info_ flows of the processed Balances (legacy rows 501-504, 1666-1673); memo rows ap.<pollutant>.fod / .fag | Same | - |
| LD54 | GDP effects: feedback (v0.3.1): GDP level raised by the effect: growth = (1 + baseline growth) x (1 + effect(t-1)) / (1 + effect(t-2)) - 1 | Bug fix | E1162, E6 |
| LD55 | GDP effects: revenue (v0.3.1): As legacy (v0.4.15): total revenue rnet + rnew (existing taxes net of subsidies and new policies, incl. power) above scenario 1; impulse = change in USD over this year's GDP, 0 before GDPStartYear; lag 0 in the impulse year | Same | E1152, E1154 |
| LD56 | GDP effects: multipliers (v0.3.1): As legacy (v0.4.15): Global, income group, Estimated (the country table of the legacy Multipliers tab, exact match, income group as fallback) or Manual (sheet Manual inputs J261:U268, legacy addresses); base, low, high with the income group's standard deviation | Same | E1161, E1160 |
| LD57 | Energy CO2: calibration to the inventory (v0.3.2): v0.4.11 as legacy: every CO2 EF x EFCalib = inventory energy CO2 of the year before the base year / scenario-1 energy CO2 of the base year with uncalibrated EFs (Egypt: 2021 inventory against 2022, 0.930); switch Settings C27, default Yes (legacy Yes* for Annex I and non-Annex I) | Same | E404, E448, E449 |
| LD58 | GDP effects: legacy values (v0.3.1): Computed, the same equations (v0.9.0: classified Same) | Same | - |
| LD59 | Road transport: engineer model (v0.3.5): Section 5b of every scenario group, every row live (Methods, chapter Transport); TrModel default Elasticity, Engineer by switch; the 17 legacy bugs of Methods, chapter Transport section 3 fixed (B1-B23) | Decision | - |
| LD60 | Road transport: policy inputs (v0.3.5): Policies: MTInputs rows 416-477 after the template (scenario-specific, legacy Dashboard defaults, all off); parameters and hardcoded literals (Gompertz constant, gas liters per GJ, PHEV kWh per liter, insurance factor, BEV distance caps, price elasticities): sheets TransportParams, TransportPaths and named constants | Decision | - |
| LD61 | Road transport: inputs from the rest of the model (v0.3.5): Section 5 road after-tax prices x GJ per liter (gas $/GJ / gas liters per GJ); industrial gas: section 2 price + road new policies; power prices of section 3 G (last year); GDP growth of row 7 (last year); population and real GDP after the feedback; carbon price x road feebate coverage; 2-3 wheelers: the gasoline price incl. new policies (legacy row 4438: before new policies); VAT on vehicles: VAT_WEO of the customs year (Egypt 0.14; legacy 0.1531) | Assumption | - |
| LD62 | Road transport: biofuels (v0.3.5): Engineer road model as legacy (v0.4.12): bioethanol and other biofuels follow road gasoline, biodiesel follows diesel (base year x use / base-year use; Balances or EnergyCons); the feebate CO2 per liter of gasoline and diesel x their fossil share (E2146:E2147). Elasticity road model (the default): as legacy (v0.9.0, R10, rows 5403-5406, 5435): bioethanol and biodiesel follow the elasticity-model gasoline and diesel (trbe.bgs, trbe.bdi), other biofuels the fuel-use equation with oil elasticities and the biomass price (trbe.obf; issue I143; L46 not reproduced in 465) | Same | - |
| LD63 | Road transport: range anxiety (v0.3.5): Goal seek on the prototype's model (v0.9.0, R10.8-R10.9: ra_goalseek.py, scenario 1, 2025, stored in data_old/range_anxiety_fit, written over the country's Transport3 cells, bright yellow); fit reported in rows trraf | Same | - |
| LD64 | Road transport: kept as legacy (v0.3.5): Kept (freight distance, data years: parameters) or not built (externalities) | To check (bucket 5) | - |
| LD65 | Residential leakage to biomass (v0.5.1): Section 6b (rows lkt, lkp, lkd, lkb, lkc, lkcb): the legacy design replicated (most-used fuel only, coefficient, cap at 1, reversible, permanent level shift, fossil change dF = -F x e_fuel x share: issue I51); fuel use = the elasticity model + the cumulative change on last year's actual use, one row set per fuel, biomass with the same useful energy dB = -dF x e_fuel / e_bio, the new policy of the row itself (an exempt fuel does not leak); the switch on Settings C59 (BioLeak, MTInputs scenario 1) as BiomassNormal | Same | - |
| LD66 | Residential LPG and kerosene always exempted (v0.5.1): Section 1 rows AlwaysExemptResLPGKer (per scenario) and exf (exf.all 1, exf.res 0 if the switch starts with Yes); Inputs column exg = 2 for residential LPG and kerosene: the new carbon tax, ETS cost and new excise of those rows are 0, so their new-policy VAT and revenue (rnew, rex, rvt) are 0 too; existing taxes, existing carbon pricing, subsidy phase-outs and the shadow price stay, as legacy; ETS-covered emissions still count the exempt fuels where the residential sector is in an ETS | Same | - |
| LD67 | Exemption phase-out of uncovered fuels and sectors: v0.5.6: built. The phase-out of uncovered fuels and sectors (rows fc, sc: 1 if covered, else exph) and the initially exempt residential demand of the most-used cooking fuel (section 6b rows lkxp, lkxe, lkxr, lkx, lkxa through lkc; share ExemptCookShare on Settings C83 from HHSurvey; usage elasticity phased in; income factor as the row, L48 fixed). v0.9.0 (R6): share over the economy-wide basket spend (I136), lpg if the WHOCooking code is missing (I137), leakage on the not-exempt use (I138) | Same | - |
| LD68 | Manual inputs tab (v0.5.2): The whole tab at the legacy addresses (paste the legacy tab from row 3; legacy values typed, formulas of other tabs replaced by the prototype equivalent or their default). Read where the prototype has the feature: ETS goal-seek settings, price controls, methane fee scope, manual international prices, fiscal multipliers, non-energy GHG elasticities, fuel economy of new BEVs; v0.9.0 (R8): manual domestic prices (G59:N146; I139), manual elasticities (K279:N307, L319; L101, L220 fixed), methane intensity decline (J185:J188; L135 fixed, I141); the other blocks are placed and not read (features not built; the note on each block's title row says which) | Same | - |
| LD69 | ETS goal-seek settings (v0.5.2): The same cells and names, read by the macro SolveETS and ets_goalseek.py (before v0.5.2: constants in the code); values 20, Continue, 0.005, the prototype error being the worst yearly |covered / cap - 1|; StartFresh starts from the fast estimate ets.est, Continue from the override row if it holds prices | Decision | - |
| LD70 | Price controls when GovPriceControls = Manual (v0.5.2): The same cells, by code (column G), in Inputs_prices column pcm (blank = 1); before v0.5.2 one constant PassManual = 0.8 for every block. Electricity rows not read (electricity prices from the power section) | Same | - |
| LD71 | Manual international prices (v0.5.2): Inputs_pint rows Manual: IMF to 2025, from 2026 Manual inputs D221:AF225 by label and year (before v0.5.2 typed copies of the same values) | Same | - |
| LD72 | Non-energy GHG elasticities (v0.5.2): Read from Manual inputs K326:M327 (legacy default values typed; text "na" = 0) by the rows ghg.dr and ch4.act of section 14; before v0.5.2 sheet Constants (ghg.el) | Bug fix | - |
| LD73 | Fuel economy of new BEVs (v0.5.2): The same cells by year (row 374) in section 5b rows trfen; before v0.5.2 sheet TransportPaths (bev_fe_new) | Same | - |
| LD74 | Power: inputs by scenario (v0.5.4, P2): Every MTInputs power input (rows 242, 262, 340-413, 482) read in the scenario's own column (section-1 rows; section 3 sub-table A0 applies them to the power data); scenario 1 is the baseline of every scenario, so a technical input changed in a policy scenario changes that scenario only | Decision | - |
| LD75 | Power: PPAs (v0.5.4): Same (rows ppa, ppr, glg, gen, early); the switch accepts Yes or Yes* (issue I54) | Same | - |
| LD76 | Power: renewable subsidies (v0.5.4): Rows rnsp, rns, lfx, prrns: own start year RenSubsidyAddStartYear (MTInputs row 482, default 2027 = the default of row 132); revenue = subsidy x generation by type, in the power subsidies and 12e row ren; nominal inputs used as real, as legacy | Bug fix | - |
| LD77 | Power: revenue rebate and electricity excise (v0.5.4): Rows rbs, exs, entxd, entx, pex, rp, rnvat, rreb, rpex, rexs, rexm: rebate = carbon cost x pass-through (its VAT falls out of rnvat); excise revenue = the excise in the price x consumption; switches accept Yes or Yes* (issue I58) | Bug fix | - |
| LD78 | Power: final deficit to gas, maximum gas capacity factor, long-term storage factor (v0.5.4, P1): Same: Settings C45 (PwDeficitGas, default No; global as legacy, issue I57), row dgas; row gmx; row ltu. Before v0.5.4 gas used MaximumCoalCF and the storage factor was 1 | Same | - |
| LD79 | Power: capex decline options Low and Vhigh (v0.5.4): The missing series falls back to the older series of the same option (wind, solar) or Medium (Inputs_ppath rows tcf|<type>|<option>) | Bug fix | - |
| LD80 | Fixed supply cost of coal and gas: domestic production: The same (v0.9.0; v0.3.4-v0.8.5 and coded CPAT: x bucketed pass-through, Egypt gas 0) | Same | - |
| LD81 | Welfare: co-benefits: wel.usd = climate + air pollution (value per ug/m3 x change in the modelled PM2.5 of the prototype's emissions, section 17b) + road co-benefits (accidents, congestion, road damage per litre) - efficiency costs (v0.9.0, R1-R2); typed Egypt inputs on the module tabs FromAirPollution and FromTransportCB (other countries 0) | Bug fix | - |
| LD82 | Social costs, FFS and subsidies: Section 18 (v0.9.0, R2): climate costs per GJ, own-sector quantities, consumption-weighted other lines, GDP of the year; explicit and implicit subsidies (16 lines x 8 variables) in every scenario group (I110) | Bug fix | - |
| LD83 | Pigouvian taxes: Section 1 rows pig.*, cc.code, xcpb, ntxb (v0.9.0, R3): the same option and netting; the transport and residential coal parts: base-year value x growth of the per-km costs, live in every group (I151); marginal air-pollution costs (L224); electricity Pigouvian 0 (I119) | Same | - |
| LD84 | Efficient prices: Section 18 (v0.9.0, R3.13-R3.22): by price fuel in every scenario group; the year table at YearFuelPrices (R3.23) not built (it belongs to the output sheets) | Same | - |
| LD85 | Electricity subsidies and efficient prices: Row spe (ELSUPPLY: sc + ores + carbon cost passed through + excise) read by the subsidy lines and the efficient prices (v0.9.0, R1R2 hand-off; was the power-model supply cost sc) | Same | - |
| LD86 | Methane intensity decline: Section 14 rows ch4.int.<source> = (1 - rate)^MAX(0, year - GHGYear) for every source (v0.9.0, R8.6-R8.7) | Same | - |
| LD87 | Power cost memos E4, E5, F1: Section 3 sub-table E2 (v0.9.0, R9.4-R9.13): yearly rows cur, sys, pcbcap, pcbom, pcbfu, pcbcp, pcbrns, pcbchk, pcbct; the CostBreakdownYear value is that year's column | Same | - |
| LD88 | Self-generated renewables in aviation and navigation: Section 5b rows trp.ren, trp.renaef, ener.avi.ren, ener.nav.ren (v0.9.0, R10.5-R10.7), in the totals | Same | - |
| LD89 | External balance (current account): Section 16b rows bca.* (v0.9.0, R11): typed WEO values for Egypt (held at 2031), change = - xnim by fuel group, % of GDP over the implied GDP, coal included; other countries 0 (I148) | Bug fix | - |
| LD90 | CBAM process emissions, green public investment, emissions intensity of industrial output: Not built (R4, R5, R12 deferred by the user 2026-10-29; designs on branch wip-r4-r5-r12) | Not yet | - |
| LD91 | Air-pollution unit costs: Marginal damages (v0.9.0): value of averted PM2.5 x concentration coefficients x emission factors, lines weighted by fuel use; legacy values kept as a memo on FromAirPollution | Bug fix | - |
| L1 | Services electricity demand grows with the industrial multiple after 2023 | Legacy bug (fixed) | E386 |
| L2 | Autonomous efficiency gains use the efficiency elasticity instead of the usage elasticity | Legacy bug (fixed) | E386 |
| L3 | Income factor on the GDP elasticity applied twice and anchored to 2023 | Legacy bug (fixed) | E386 |
| L4 | Long-term storage cost allocation (33%) applied twice | Legacy bug (fixed) | E407, E406 |
| L5 | Investment spending uses the capital cost at time factor 1 | Legacy bug (fixed) | - |
| L6 | Investment logit normalised by the cheapest type, including types that may not be built | Legacy bug (fixed) | E427 |
| L7 | Early coal retirement mixes nameplate and effective capacity | Legacy bug (fixed) | E417 |
| L8 | Effective coal retirement is not capped like the nameplate retirement | Legacy bug (fixed) | - |
| L9 | Feebate rebate per kWh consumed is added to the cost per kWh generated | Legacy bug (fixed) | E334, E335 |
| L10 | Capacity needed is computed from last year's plan, not from actual capacity | Legacy bug (fixed) | E419 |
| L11 | Stray reference in dispatch | Legacy bug | - |
| L12 | Total nameplate investment row is zero | Legacy bug | E435 |
| L13 | Other oil products: hardcoded pass-through 1 and margin 0 | Legacy bug | E247, E249 |
| L14 | Pass-through applied twice in the first projected year | Legacy bug | E249 |
| L15 | ETS: hardcoded relative price 1.1 | Legacy bug | E86 |
| L16 | ETS quick estimate linear in the semi-elasticity | Legacy bug | E86 |
| L18 | Non-energy methane never changes | Legacy bug | E1093, E1097 |
| L19 | Flaring CO2 counted as methane | Legacy bug | E1101 |
| L20 | Population growth path | Legacy bug | E1080 |
| L21 | Waste abated with the livestock curve | Legacy bug | E1095 |
| L22 | Navigation missing from the local pollutant totals | Legacy bug | E1253 |
| L23 | Services and food & forestry missing from the pollutant totals | Legacy bug | E1253 |
| L24 | GDP effect added to GDP growth every year | Legacy bug | E1162, E6 |
| L25 | Road: distance tax and 2-3 wheeler EV subsidy apply in the baseline | Legacy bug | - |
| L26 | Road: freight and 2-3 wheeler income growth read coal subsidies from 2038 | Legacy bug | - |
| L27 | Road: vehicle ownership calibration only scales up (and uses 2024) | Legacy bug | - |
| L28 | Road: freight-share cap and 2-3 wheeler peak use 2024 | Legacy bug | - |
| L29 | Road: ownership of cars and trucks cannot fall | Legacy bug | - |
| L30 | Road: bus fuel scaled by the wrong rows | Legacy bug | - |
| L31 | Road: bus share grossed up as x(1+share) | Legacy bug | - |
| L32 | Road: industry emission factors for road diesel and LPG | Legacy bug | - |
| L33 | Road: wrong elasticities and rows in freight and 2-3 wheeler distance | Legacy bug | - |
| L34 | Road: freight discounted at the power-sector WACC | Legacy bug | - |
| L35 | Road: negative PHEV sales share | Legacy bug | - |
| L36 | Road: charging-station subsidy ramp | Legacy bug | - |
| L37 | Road: new BEV maintenance at the ICEV rate | Legacy bug | - |
| L38 | Road: used ICEV and BEV depreciation over different periods | Legacy bug | - |
| L39 | Road: freight distance output omits LPG and LNG trucks | Legacy bug | - |
| L40 | Road: wrong rows in average gas and EV fuel economy | Legacy bug | - |
| L41 | Road: PHEVs carry the full BEV range anxiety | Legacy bug | - |
| L42 | Domestic aviation: GDP growth and shock swapped | Legacy bug | - |
| L43 | Other energy use: no GDP growth | Legacy bug | - |
| L44 | Residential other oil products priced at the biomass price | Legacy bug | - |
| L45 | Residential leakage to biomass inconsistent | Legacy bug | - |
| L46 | Road other biofuels: wrong price and terms | Legacy bug | - |
| L47 | Self-generated renewables in aviation and navigation take the shock from wrong rows | Legacy bug | - |
| L48 | Residential initially-exempt rows: no income factor; starred "Yes*" exemption test | Legacy bug | - |
| L49 | Balance of payments: oil without the share traded | Legacy bug | - |
| L50 | Balance of payments: current account #NAME?, column lag, sign | Legacy bug | - |
| L51 | Energy trade balance of coal valued at the oil price | Legacy bug | - |
| L52 | Renewables take the world power parameters, never the country ones | Legacy bug | - |
| L53 | Actual capacity factors are never used | Legacy bug | - |
| L54 | Hydro investment always starts in the first year | Legacy bug | - |
| L55 | China, Japan and Korea take regional power data | Legacy bug | - |
| L56 | Countries without CoC risk data get Sri Lanka's WACC parameters | Legacy bug | - |
| L57 | New ETS: the quick price estimate is linear in the semi-elasticity | Legacy bug | - |
| L58 | Local pollutants: subsectors without a GAINS match get zero factors | Legacy bug | - |
| L59 | Local pollutants and combustion CH4: fuels without a GAINS factor emit nothing | Legacy bug | - |
| L60 | VAT payment on oil products divided by the full VAT rate | Legacy bug | - |
| L61 | EU ETS price grows with the carbon-tax growth | Legacy bug | - |
| L62 | Existing carbon tax on transport diesel, LPG and kerosene uses the rate row as coverage | Legacy bug | - |
| L63 | Existing carbon tax fuel coverage: lookup range cut short | Legacy bug | - |
| L64 | No existing ETS on other oil products outside power | Legacy bug | - |
| L65 | Carbon tax complementary to an existing ETS: last year's ETS coverage | Legacy bug | - |
| L66 | Other energy use: no additional policy efficiency gains on fossil fuels | Legacy bug | - |
| L67 | Power: capacity bought for this year's demand, although it comes online next year | Legacy bug | - |
| L68 | GDP effects: the multiplier of lag 1 acts in the impulse year | Legacy bug | - |
| L69 | GDP effects: the first cohort's excise drag is lost | Legacy bug | - |
| L70 | Revenue: industry gas excise uses the coal rate and coal use | Legacy bug | - |
| L71 | Revenue: biomass taxes, subsidies and VAT divided by the unit conversion | Legacy bug | - |
| L72 | Revenue: next-year references | Legacy bug | - |
| L73 | Revenue: wrong coverage shares | Legacy bug | - |
| L75 | Revenue reports: hard-coded row and mixed totals | Legacy bug | - |
| L76 | Multipliers: empty CIT table, WAGE on the GNFS table, approximate country match, default to Estimated | Legacy bug | - |
| L77 | Average prices: index rows point at the wrong rows, gas test on the policy total | Legacy bug | - |
| L78 | ETS: auctioned share drops to 0 after the target year unless "Constant" | Legacy bug | - |
| L79 | ETS: industry and transport priced as a whole when one subsector is covered | Legacy bug | - |
| L80 | ETS: the carbon-tax trajectory rescaled when the ETS is on | Legacy bug | - |
| L81 | Consumer subsidy phase-out: the fixed subsidy takes last year's factor | Legacy bug | - |
| L82 | Residential gas producer subsidy reads the oil row | Legacy bug | - |
| L83 | Electricity producer subsidy compounds the factor and lags a year | Legacy bug | - |
| L84 | Electricity consumer subsidy phased with the price-control factor; option text mismatch | Legacy bug | - |
| L85 | Electricity consumer subsidy info row subtracts industry | Legacy bug | - |
| L86 | No manual override for the electricity producer subsidy | Legacy bug | - |
| L87 | Regulations never act: share 0 and the adjustments unused | Legacy bug | - |
| L88 | Regulations never reach power | Legacy bug | - |
| L89 | Coal in road, residential and services reads the residential coal shadow price | Legacy bug | - |
| L90 | Residential leakage breaks the useful-energy balance | Legacy bug | - |
| L91 | Exempt residential fuel still leaks to biomass | Legacy bug | - |
| L92 | ExemptMostCook never reaches Mitigation | Legacy bug | - |
| L93 | Fuel coverage rows test text labels and contain #REF! | Legacy bug | - |
| L94 | Exemption phase-in rules differ between rows | Legacy bug | - |
| L95 | Power demand: efficiency increment sits on the net-exports row | Legacy bug | - |
| L96 | Fuel-use block: mislabelled parameter and fuel rows | Legacy bug | - |
| L97 | Iron & steel memo rows unused; one reads next year's growth | Legacy bug | - |
| L98 | Feebate inclusion of industry reads the ETS industry flag | Legacy bug | - |
| L99 | ETS inclusion of machinery and other manufacturing uses the buildings flag | Legacy bug | - |
| L100 | Manual domestic prices: the electricity rows are never read | Legacy bug | - |
| L101 | Manual services income elasticities read the industries column | Legacy bug | - |
| L102 | Manual non-energy elasticities can never take effect | Legacy bug | - |
| L103 | Manual SCC reads a path typed on Mitigation, not the Manual inputs block | Legacy bug | - |
| L104 | Name CH4Feebate points to an empty cell | Legacy bug | - |
| L105 | Dashboard industry feebate rates are lost | Legacy bug | - |
| L106 | Manual inputs memo swaps the renewables and electricity price elasticities | Legacy bug | - |
| L107 | Renewable subsidy: start year of the additional subsidy reuses the consumer-subsidy phase-out year | Legacy bug | - |
| L108 | Cost of renewable subsidies counts the base subsidy twice, ignores the hydro switch and omits biomass | Legacy bug | - |
| L109 | Capex decline options Low and Vhigh have no wind and solar series | Legacy bug | - |
| L110 | Power revenue rebate counts VAT that was never collected | Legacy bug | - |
| L111 | Manual electricity excise revenue counts the whole excise, also where the price does not include it | Legacy bug | - |
| L112 | Policy copies of the shadow-price rows read the baseline carbon price in the regulation term | Legacy bug | - |
| L113 | Power switches tested for the exact "Yes" (was issue I58) | Legacy bug | - |
| L114 | Renewable subsidies: nominal inputs used as real (was issue I55) | Legacy bug | - |
| L115 | Residential gas: current ETS price reads the LPG transport row | Legacy bug | - |
| L116 | Services gasoline and diesel income elasticities: step-change column reads the wrong rows | Legacy bug | - |
| L117 | Transfers multiplier (TRNS): estimated lag-0 table read two rows off | Legacy bug | - |
| L118 | Manual power investment: the need net of manual investment is never used | Legacy bug | - |
| L119 | NDC year adjustment applied twice for BAU targets and never for Fixed or Historical | Legacy bug | - |
| L120 | NDC index rows: unconditional and conditional ratios inverted against the average | Legacy bug | - |
| L121 | Historical NDC: the target "level" is the emissions cut | Legacy bug | - |
| L122 | Intensity NDC incl. LULUCF adds a blank cell instead of LULUCF emissions | Legacy bug | - |
| L123 | Intensity NDC: reference-year GDP read from a fixed cell | Legacy bug | - |
| L124 | Producer subsidy: the residential gas block reads the oil subsidy | Legacy bug | - |
| L125 | Producer subsidy: other oil products add a per-liter value to a per-barrel price | Legacy bug | - |
| L126 | Power: fuel price for power averages later years | Legacy bug | - |
| L127 | Power: levelised variable cost reads the variable cost to 2041 | Legacy bug | - |
| L128 | Net revenue report rows read the next year | Legacy bug | - |
| L129 | Baseline renewable subsidy counted twice | Legacy bug | - |
| L130 | Intensity NDC: conditional and unconditional rows use different base years | Legacy bug | - |
| L131 | Codes: one output code on rows with different contents | Legacy bug | - |
| L132 | Codes: capitals and empty tokens | Legacy bug | - |
| L133 | Codes: nox.tot holds N2O, oc.tot. holds NOx | Legacy bug | - |
| L134 | Price-increase units: other oil products "$/bbn", default "$/liter" for other oil products and biomass | Legacy bug | - |
| M1 | Version-log rows rewritten with the current version | prototype bug (fixed) | - |
| M2 | Power: VAT left out on the policy term | prototype bug (fixed) | E368 |
| M3 | Power: long-term storage allocation left out | prototype bug (fixed) | E407 |
| M4 | Power: VRE share without other renewables | prototype bug (fixed) | E405 |
| M5 | Defined name clashed with a LAMBDA name | prototype bug (fixed) | - |
| M6 | Power ETS revenue valued at the tax-equivalent price | prototype bug (fixed) | E442 |
| M7 | Stale texts in the workbook and notes | prototype bug (fixed) | - |
| M8 | LegacyDiff rows out of date | prototype bug (fixed) | - |
| M9 | Legacy comparison note from v0.1.01 | prototype bug (fixed) | - |
| M10 | Total rows labelled "All subsectors" | prototype bug (fixed) | - |
| M11 | Macros read 19 year columns | prototype bug (fixed) | - |
| M12 | Sheet Lambdas: formula texts named merged sheets | prototype bug (fixed) | - |
| M13 | Road vehicle feebate counted the carbon price twice | prototype bug (fixed) | - |
| M14 | LAMBDA library texts named a merged-away sheet | prototype bug (fixed) | - |
| M15 | Section 18: VAT on efficient prices at the 2022 general rate in every year | prototype bug (fixed) | - |
| M16 | Road: freight BEV feebate valued at the ICEV truck's distance | prototype bug (fixed) | - |
| M17 | Road: plug-in hybrid cost mixed BEV capital cost with ICEV insurance and maintenance | prototype bug (fixed) | - |
| M19 | Nominal GDP divided by a billion although WEO is in billions | prototype bug (fixed) | - |
| M20 | International prices: World Bank and IEA LNG and Europe gas series swapped | prototype bug (fixed) | - |
| M21 | Methane fee: marginal abatement price #DIV/0 where the curve exponent is 0 | prototype bug (fixed) | - |
| M22 | Distribution: percentile recycling rows added a % row to amounts in local currency | prototype bug (fixed) | - |

## C. LAMBDA library (the 2041 cells)

Each 2041 cell calls one of these named LAMBDAs (sheet `Lambdas`, name manager).

| LAMBDA | Parameters | Body | Note |
|---|---|---|---|
| `PATH` | year, start_yr, target_yr, start, target, cont | `IF(year<start_yr,0,start+(target-start)/MAX(target_yr-start_yr,1)*IF(OR(year<=target_yr,cont),year-start_yr,target_yr-start_yr))` | Policy path: 0 before start_yr, linear from start (start_yr) to target (target_yr); after target_yr linear if cont, else flat |
| `PATHYEARS` | year, start_yr, target_yr, cont | `IF(cont,year,MIN(year,target_yr))-start_yr` | Years along a policy path: year - start_yr, held at target_yr - start_yr after the target year unless cont |
| `FPRSLOPE` | start_yr, target_yr, start, target | `IF(target_yr>start_yr,(target-start)/(target_yr-start_yr),0)` | Fuel price reform: linear increase per year (legacy column J; 0 unless the target year is later) |
| `FPRRATE` | start_yr, target_yr, start, target, incr | `IF(AND(target_yr>start_yr,MAX(start,target)>0),(target/IF(start>0,start,start+incr))^(1/(target_yr-start_yr))-1,0)` | Fuel price reform: annual rate (target/start)^(1/n) - 1, start 0: target/(start + increase) (legacy column K) |
| `FPRBASE` | start_yr, target_yr, start, incr | `start+incr*MAX(target_yr-start_yr-1,0)` | Fuel price reform: value of the year before the target year (base of the Percentage continuation) |
| `FPRAFTER` | year, start_yr, target_yr, ext, start, target, pbase, rate | `IF(ext="Percentage",pbase*(1+rate)^(year-target_yr+1),IF(target_yr>start_yr,target,start))` | Fuel price reform after the target year: Percentage: base x (1 + rate)^years (L173 fixed: legacy rate x last year); otherwise held at the target (L171 fixed: legacy 0) |
| `FPRPATH` | year, start_yr, target_yr, ext, start, incr, after | `IF(year<start_yr,0,IF(OR(year<target_yr,ext="Linear*"),start+incr*(year-start_yr),after))` | Fuel price reform path (v0.9.0, as legacy rows 167-180): 0 before the start year, linear to the target year and after it with Linear*, else the value after the target (FPRAFTER) |
| `NOMFACTOR` | basis, cpi_index | `IF(LEFT(basis,7)="Nominal",cpi_index,1)` | Nominal-to-real factor of the carbon price inputs: the CPI index if they are nominal, else 1 |
| `ETSON` | apply, year, start_year | `IF(AND(LEFT(apply,3)="Yes",year>=start_year),1,0)` | 1 if the new ETS applies (Yes) and has started, else 0 |
| `ETSPRICE` | ets_on, override, override_price, estimate, carbon_price | `IF(ets_on=1,IF(LEFT(override,3)="Yes",IF(override_price="",carbon_price,override_price),estimate),0)` | ETS permit price ($/tCO2) once a new ETS applies: override row if the override switch is Yes (blank cell: carbon price path), else the fast estimate |
| `OBRSHARE` | benchmark | `MIN(1,MAX(0,benchmark))` | Output-based (OBR) share of an ETS sector: its benchmark, between 0 and 1 |
| `VOLPICK` | label, values | `INDEX(values,MATCH(SUBSTITUTE(label,"*",""),Settings!$C$16:$F$16,0))` | Value of the Settings volatility table (legacy ETS+LTS) for an MTInputs label (Medium, High, Low, Zero; a trailing * ignored) |
| `VOLADJ` | volatility, impact, ct_risk | `(1+ct_risk*impact)/(1+volatility*impact)` | ETS volatility adjustment: (1 + carbon tax policy risk x impact) / (1 + ETS volatility x impact) |
| `COVERED` | emissions, coverage | `SUMPRODUCT(emissions,coverage)` | Covered emissions: SUMPRODUCT(emissions by ETS sector, effective coverage) |
| `CAPCHANGE` | year, start_yr, target_yr, change_start, change_target | `change_start+(change_target-change_start)/MAX(target_yr-start_yr,1)*(MIN(year,target_yr)-start_yr)` | Relative change of the ETS cap: linear from the start to the target year, flat after |
| `ETSCAP` | ets_on, year, target_yr, cont, base, change, cap_prev | `IF(ets_on=1,IF(AND(year>target_yr,LEFT(cont,8)="Constant"),cap_prev,base*(1+change)),0)` | ETS cap: baseline covered emissions x (1 + relative change); after the target year constant if the continuation is Constant, else the relative change is kept |
| `ETSSEMI` | emissions, coverage, semi, obr, obr_eff, base | `IF(base>0,SUMPRODUCT(emissions,coverage,semi,1-(1-obr_eff)*obr)/base,0)` | Effective covered semi-elasticity: baseline-weighted sector semi-elasticities x allocation effectiveness (auctioned 1, OBR obr_eff) |
| `ETSESTIMATE` | ets_on, cap, base, semi, vadj | `IF(AND(ets_on=1,cap>0,cap<base,semi<0,vadj>0),LN(cap/base)/(semi*vadj),0)` | Fast ETS price estimate: LN(cap / baseline covered emissions) / (semi-elasticity x volatility adjustment), 0 if the cap does not bind |
| `TAXEQUIV` | price, vadj | `price*vadj` | ETS tax-equivalent price: permit price x volatility adjustment |
| `REVFACTOR` | vadj | `IF(vadj>0,1/vadj,0)` | ETS revenue factor: permit price per $ of tax-equivalent price (1 / volatility adjustment) |
| `FREESHARE` | auctioned | `1-auctioned` | ETS benchmark (share allocated free) = 1 - auctioned share (v0.4.15, I21: MTInputs rows 90-91) |
| `ETSCOVER` | ets_on, covered | `IF(ets_on=1,IF(covered,1,0),0)` | Effective ETS coverage of a sector: 1 if the new ETS applies, has started and covers it |
| `SHADOWSHARE` | coverage, adjustment | `IF(coverage,1,0)*adjustment` | Share of the shadow price impacting efficiency: coverage x efficiency-margin adjustment |
| `SUPPLYCOST` | year, key, fix_sp, sp_prev, gp_now, gp_prev, ps_now, ps_prev | `IF(year<=LastHist,IFERROR(INDEX(IPsp,MATCH(key,IPKey,0),MATCH(year,IPspY,0)),0),fix_sp+(sp_prev-fix_sp-ps_prev)*gp_now/gp_prev+ps_now)` | Supply cost: data up to the last historical year (Inputs_prices, price code key), then fixed part + floating part x gp(t)/gp(t-1) + producer subsidy per price unit (v0.6.1, I49: floating part = sp - fixed - producer subsidy) |
| `PRODSUBUNIT` | yr, subsidy, demand, last_unit, kept | `IF(yr<=LastHist,IFERROR(-subsidy*USDperM/demand,0),last_unit*kept)` | Producer subsidy per unit (v0.6.1, I49): -subsidy / demand up to the last price year, then the last value x the phase-out factor psf (v0.9.0, R7.1; legacy rows 825-829, 2213) |
| `PSDEMAND` | world, domestic, unit | `AVERAGE(world,domestic)*unit` | Demand spreading the producer subsidy (v0.6.2, I49): average of world and domestic demand x units per ktoe (oil: world only, biomass: domestic only) |
| `PSPRICEUNIT` | per_unit, per_barrel, gj | `per_unit*IF(per_barrel,LitersPerBbl,1)/gj` | Existing producer subsidy of a block ($/GJ): per unit x liters per barrel for a barrel-priced block (L125) / GJ per price unit (v0.6.1, I49; v0.6.2: $/GJ) |
| `OTHERTAX` | year, key, txo_last, before_floor | `IF(year<=LastHist,IFERROR(INDEX(IPtxo,MATCH(key,IPKey,0),MATCH(year,IPtxoY,0)),0),IF(txo_last>=0,MAX(txo_last,before_floor),before_floor))` | Excise and other taxes: data up to the last historical year, then the value before the floor, not below its last historical value if that is >= 0 (legacy rule) |
| `RETAILPRICE` | sp, txo, vat_rate | `(sp+txo)*(1+vat_rate)` | Retail price before new policies: (supply cost + excise and other taxes) x (1 + VAT rate) |
| `VATPAY` | sp, txo, vat_rate | `(sp+txo)*vat_rate` | VAT payment before new policies: (supply cost + excise and other taxes) x VAT rate |
| `TAXPART` | txo | `MAX(txo,0)` | Existing tax: positive part of excise and other taxes |
| `SUBSIDYPART` | txo | `MIN(txo,0)` | Existing consumer subsidy: negative part of excise and other taxes (subsidies are negative) |
| `PERUNIT` | value_gj, gj_per_unit | `value_gj*gj_per_unit` | Value per GJ converted to the price unit (MTInputs units: $/liter, $/bbl, $/GJ) |
| `SECTORTAX` | price, sector_cov, ets_cov, complement, xets_cov | `price*IF(LEFT(complement,3)="Yes",1-xets_cov,sector_cov)*(1-ets_cov)` | Carbon tax rate of a sector ($/tCO2): carbon price x sector coverage (complementary to an existing ETS: 1 - its sector coverage), not where the new ETS covers |
| `ECPFACTOR` | apply, growth, year | `IF(LEFT(apply,3)="Yes",(1+growth)^MAX(0,year-ECPLast),0)` | Existing carbon pricing factor on the data (v0.4.12): (1 + growth) after the last data year if the existing scheme applies (Yes), else 0 |
| `XCARBON` | ef, ct_data, ct_factor, ets_data, ets_factor, embedded | `ef*(ct_data*ct_factor+ets_data*ets_factor-embedded)` | Existing carbon pricing per unit (v0.4.12): EF (or CO2) x (carbon tax of the ECP sector / fuel x its factor + ETS x its factor - the level embedded in the price data, for the change; 0 for the level) |
| `SECTORETS` | price, ets_cov, obr | `price*ets_cov*(1-obr)` | ETS cost rate of a sector in the fuel price ($/tCO2): tax-equivalent price x effective ETS coverage x auctioned share (1 - OBR) |
| `CARBONTAX` | rate, ef, fuel_cov, exempt_fac | `rate*ef*fuel_cov*exempt_fac` | New carbon tax ($/GJ): carbon tax rate of the sector x EF x fuel coverage x exemption factor (v0.5.1) |
| `ETSCOST` | rate, ef, exempt_fac | `rate*ef*exempt_fac` | New ETS in the fuel price ($/GJ): ETS cost rate of the sector x EF; ETS rate x effective coverage and auctioned share are in the rate. Legacy: tax-equivalent price x EF x effective ETS coverage x auctioned share (1 - OBR); x exemption factor (v0.5.1) |
| `NEWEXCISE` | increase, gj_per_unit, exempt_fac | `increase/gj_per_unit*exempt_fac` | New excise (fuel price reform): increase per price unit / GJ per price unit x exemption factor (v0.5.1) |
| `EXEMPTFACTOR` | exempt_sw | `IF(LEFT(exempt_sw,3)="Yes",0,1)` | Exemption factor of the new policies: 0 if the exemption switch starts with Yes (Yes, Yes*), else 1 (v0.5.1; legacy rows 5546-5547 test the exact "Yes") |
| `LEAKTAX` | new_policy, vat_rate | `new_policy*(1+vat_rate)` | Leakage to biomass: new policy in the residential price of the fuel, new carbon tax + ETS + new excise incl. VAT (legacy rows 5574, 5580, 5586; v0.5.1) |
| `LEAKSHARE` | leak_on, tax_now, tax_prev, p_prev, coef | `leak_on*MIN((1+(tax_now-tax_prev)/p_prev)^coef-1,1)` | Leakage to biomass: share of the fuel moving to biomass, on x MIN((1 + change in the new policy / last year's after-tax price)^coef - 1, 1); negative when the policy falls (legacy rows 5576, 5582, 5589; v0.5.1) |
| `LEAKCHANGE` | f_prev, cook_eff, leak_share | `-f_prev*cook_eff*leak_share` | Leakage to biomass: change in fossil fuel use = - last year's fuel use x cookstove efficiency x share (legacy rows 5577, 5583, 5588; v0.5.1) |
| `LEAKBIOMASS` | change, cook_eff, bio_eff | `-change*cook_eff/bio_eff` | Leakage to biomass: biomass with the same useful energy, - change x efficiency of the fuel / efficiency of biomass (legacy rows 5578-5593; L90 fixed, v0.5.1) |
| `LEAKCUM` | cum_prev, flow | `cum_prev+flow` | Leakage to biomass: cumulative change = last year's + this year's flow (legacy totals 5554-5560, SUM of the flows; v0.5.1) |
| `PHASEIN` | phase_on, yr, start, period | `IF(phase_on=TRUE,MAX(MIN((yr+1-start)/period,1),0),0)` | Exemption phase-in share: (year + 1 - YearPha) / ExemptPhaseoutPeriod within 0-1 if ExemptPhaseout (legacy rows 5568-5570 with the rule of 2259-2265, L94; v0.5.6) |
| `XRATIO` | this_yr, last_yr | `IF(last_yr=0,1,this_yr/last_yr)` | Ratio of this year to last year (1 if last year is 0) (v0.5.6) |
| `XPATH` | prev, demand_ratio, price_ratio, eps_u, phase | `prev*demand_ratio*price_ratio^(eps_u*(phase-1))` | Initially exempt fuel use: last year x the growth of the fuel use of the row x the price ratio ^ (usage elasticity x (phase - 1)), so the usage elasticity is phased in (legacy rows 5568-5570; v0.5.6) |
| `XADJ` | path, share, fuel_use | `path-share*fuel_use` | Adjustment of fuel use for the initially exempt part: exempt path - exempt share x fuel use of the row (v0.5.6) |
| `NEWPOLICY` | carbon_tax, ets, excise | `carbon_tax+ets+excise` | Total new policy: new carbon tax + ETS + new excise |
| `POSTTAX` | pre_policy_p, new_policy, vat_rate | `MAX(pre_policy_p+new_policy*(1+vat_rate),PriceFloor)` | After-tax price: retail price before new policies + new policies x (1 + VAT rate), at least PriceFloor |
| `SHADOWTOTAL` | feebate, share, regulation, ets_price, ets_cov, obr | `feebate*share+regulation+ets_price*ets_cov*obr` | Shadow price on the efficiency margin of a sector ($/tCO2): sector shadow price x share impacting efficiency + regulation shadow price (v0.4.16) + ETS tax-equivalent price x ETS coverage x OBR share |
| `SCNROW` | scenario | `IFERROR(MATCH(scenario,ScnName,0),0)` | Column of the legacy scenario table (Mapping; legacy Mitigation rows 222-262) of the scenario's ScenarioSelected (MTInputs row 13); 0 if not found (v0.4.16) |
| `EXPLICIT` | scn_row | `IF(scn_row=0,1,--(INDEX(ScnExpl,scn_row)="Yes"))` | Explicit carbon pricing (1) or shadow pricing (0) of the scenario (legacy row 259; v0.4.16) |
| `REGADJ` | scn_row, adjustments | `IF(scn_row=0,0,IF(INDEX(ScnAdj,scn_row)=0,0,INDEX(adjustments,INDEX(ScnAdj,scn_row))))` | Efficiency adjustment of the scenario's regulation (MTInputs rows 247-251; legacy F86:F90, unused there: bug; v0.4.16) |
| `REGCOVER` | scn_row, sector_pos | `IF(scn_row=0,0,--(INDEX(ScnCov,scn_row,sector_pos)="Yes"))` | Sector covered by the scenario's regulation (legacy rows 240-257; v0.4.16) |
| `REGSHADOW` | shadow_price, adjustment, covered | `shadow_price*adjustment*covered` | Regulation shadow price ($/tCO2) = shadow carbon price x adjustment x covered (v0.4.16) |
| `PHASEON` | scen, baseline_sw, policy_sw | `IF(scen=1,OR(baseline_sw=TRUE,LEFT(baseline_sw,3)="Yes"),OR(policy_sw=TRUE,LEFT(policy_sw,3)="Yes"))*1` | Phase-out applies: scenario 1 the baseline switch, other scenarios the policy switch (legacy rows 264-271; v0.4.16) |
| `PCON` | scen, baseline_sw, policy_sw | `AND(OR(policy_sw=TRUE,LEFT(policy_sw,3)="Yes"),OR(scen>1,OR(baseline_sw=TRUE,LEFT(baseline_sw,3)="Yes")))*1` | Price-control phase-out applies: policy switch and (scenario > 1 or the baseline switch) (legacy I2189) |
| `PICKSCEN` | scen, baseline, policy | `IF(scen=1,baseline,policy)` | Scenario 1 takes the baseline input, the others the policy input (v0.4.16) |
| `PHASESHARE` | scen, baseline, policy | `IF(scen=1,baseline,MAX(baseline,policy))` | Share to phase out: scenario 1 the baseline share, others MAX(baseline, policy) (legacy G267, G271) |
| `PHASEOUT` | yr, on, start, period, share | `MAX(1-share,IF(on*(yr>start),1-share*(yr-start)/MAX(period,1),1))` | Phase-out factor (share of the original kept): MAX(1 - share, 1 - share x (year - start) / period after the start year) (legacy rows 2213-2216; v0.4.16) |
| `INCLFACTOR` | included, factor | `1-included*(1-factor)` | Factor of one price fuel / sector: 1 - included x (1 - phase-out factor) (v0.4.16) |
| `PRODSUB` | yr, last_yr, usd_bn, cpi, held | `IF(yr<=last_yr,usd_bn*cpi*MperBn,held)` | Producer subsidy (USD m real): data (USD bn nominal x CPI factor) up to the last price year, then held (v0.4.16) |
| `SUBREFORM` | factor, fixed_part | `-(1-factor)*MIN(fixed_part,0)` | Consumer subsidy reform wedge ($/GJ): -(1 - factor) x the fixed subsidy (fixed part of txo, <= 0) (legacy rows 2598 ff.; v0.4.16) |
| `PCREFORM` | factor, floating_part | `-(1-factor)*floating_part` | Price-control phase-out wedge ($/GJ): -(1 - factor) x the floating part of txo (legacy rows 2599 ff.) |
| `BLOCKWEDGE` | block_wedge | `block_wedge` | The wedge of the subsector's price block (lookup; v0.4.16) |
| `BLOCKPRICE` | block_price | `block_price` | The price before new policies of the fuel's price block (lookup; v0.6.2) |
| `FIXEDPART` | year, share, txo_now, txo_last | `share*IF(year<=LastHist,txo_now,txo_last)` | Fixed part of txo: share x txo up to the last historical year, then share x txo of that year (v0.4.16) |
| `SHADOWGJ` | shadow_price, ef | `shadow_price*ef` | Shadow price per unit of energy: shadow price ($/tCO2) x emission factor (tCO2 per GJ or per kWh) |
| `KWHPOLICY` | intensity, ct_rate, fuel_cov, ets_rate, reform, reform_factor | `intensity*(ct_rate*fuel_cov+ets_rate)+reform*reform_factor` | New policy cost per kWh generated: tCO2/kWh x (carbon tax x fuel coverage + ETS cost) + fuel price reform x its kWh factor |
| `FLOATTAX` | year, key, pcc, prev, sp_now, sp_prev | `IF(year<=LastHist,IFERROR(INDEX(IPtxo,MATCH(key,IPKey,0),MATCH(year,IPtxoY,0)),0),prev-(sp_now-sp_prev)*(1-pcc))` | Excise and other taxes before the floor: txo_L + (sp_L - sp) x (1 - pcc), computed year by year: history txo, then last year - change in sp x (1 - pcc) (v0.4.10: L14 fixed; legacy applied (1 - pcc) twice in the first projected year) |
| `REVENUE` | fuel_use, pj_per_ktoe, rate | `fuel_use*pj_per_ktoe*rate` | Revenue (USD million real): fuel use (ktoe) x PJ per ktoe x rate ($/GJ) |
| `EMISSIONS` | fuel_use, pj_per_ktoe, ef | `fuel_use*pj_per_ktoe*ef` | CO2 emissions (MtCO2): fuel use (ktoe) x PJ per ktoe x emission factor (tCO2/GJ) |
| `NONCO2` | fuel_use, ef_start, ef_end, year | `fuel_use*(ef_start+(ef_end-ef_start)*EFFinShare*(year-BaseYr)/(EFEndYear-BaseYr))/tPerKt` | Non-CO2 combustion emissions (kt): fuel use (ktoe) x emission factor (t/ktoe) on a linear path from the base-year factor to the final factor of EFSel in EFEndYear, continued after (as legacy) |
| `METHANEFEE` | fee_path, policy_scen, ct_switch, carbon_price | `fee_path*policy_scen+IF(LEFT(ct_switch,3)="Yes",carbon_price,0)` | Methane fee used (USD/tCO2e): the fee path in policy scenarios (scenario number > 1, legacy row 2238; v0.4.12), plus the carbon price if the carbon tax applies to methane (CTforMethane = Yes) |
| `GROWTHRATE` | cur, prev | `IF(prev=0,0,cur/prev-1)` | Growth rate: now / previous - 1 (0 if the previous value is 0) |
| `EFWEIGHT` | yr | `EFFinShare*(yr-BaseYr)/(EFEndYear-BaseYr)` | Weight of the final emission factor (FE fin): 0 in the base year, rising linearly to EFFinShare in EFEndYear (EFSel: Constant 0, Variable 1, Average 0.5), continuing after, as legacy |
| `OTHERPM` | total_pm, black_carbon, organic_matter | `MAX(0,total_pm-black_carbon-organic_matter)` | Other PM2.5: PM2.5 less black carbon and primary organic matter, at least 0 |
| `FISCALSPACE` | revenue, revenue_ref, gdp_bn | `(revenue-revenue_ref)/(gdp_bn*MperBn)` | Fiscal space (share of GDP): revenue above scenario 1 / GDP (USD bn x MperBn) |
| `GDPSHARE` | usd_m, gdp_bn | `usd_m/(gdp_bn*MperBn)` | Share of GDP: USD m / (GDP in USD bn x MperBn) (v0.3.13, 12d) |
| `SAFEDIV` | amount, activity | `IF(activity=0,0,amount/activity)` | Amount per unit of activity, 0 when the activity is 0 (v0.3.14: grid intensity, Kaya) |
| `GROWPATH` | level, growth, years | `level*(1+growth)^years` | Level x (1 + real growth) ^ years (v0.3.17: social cost of carbon paths) |
| `TRAPEZOID` | wedge, wedge_ref, change | `-AVERAGE(wedge,wedge_ref)*change/MperBn` | Efficiency cost (USD bn): -average of the wedge and the scenario-1 wedge x change in use (v0.3.17) |
| `MFEEPRICE` | coef_a, coef_b, fee | `IF(coef_a=0,0,MIN(fee,IFERROR(coef_a^(-1/coef_b),fee)))` | Methane fee per t CH4 used on the abatement curve, capped where abatement reaches 1 (v0.3.17) |
| `MFEECOST` | base_kt, abated, price, coef_b | `base_kt*abated*price*coef_b/(1+coef_b)/Million` | Area under the abatement curve a x fee ^ b: base x abated share x price x b / (1 + b) (v0.3.17) |
| `IMPULSE` | year, start, space, space_prev, gdp_prev, gdp | `IF(year<start,0,space-space_prev*gdp_prev/gdp)` | Fiscal impulse (legacy row 14356, v0.4.15): change in revenue above scenario 1 (USD) / this year's GDP, 0 before GDPStartYear |
| `MULTGROUP` | mult_source, income_group | `IFERROR(INDEX(MultSrcVal,MATCH(LEFT(mult_source,3),MultSrcKey,0)),LOWER(income_group))` | Multiplier group: global, est (country estimates), man (Manual inputs), else the income group of the country (v0.4.15, LD56) |
| `MULTPREFIX` | mult_group, mult_range | `mult_group&"/"&LOWER(SUBSTITUTE(mult_range,"*",""))&"/"` | Multiplier key prefix: group/range/ (range Base, Low or High) |
| `FISCALEFFECT` | use_share, impulses, mults | `use_share*SUMPRODUCT(impulses,mults)` | GDP effect of one revenue use: share x SUMPRODUCT(impulses by lag, multipliers by lag) |
| `GDPEFFECT` | effects, endogenous | `effects*(LEFT(endogenous,3)="Yes")` | GDP effect (share of GDP): the sum of the uses, if endogenous GDP effects are switched on |
| `LEVELFACTOR` | effect_before | `1+effect_before` | GDP level factor of the year: 1 + last year's GDP effect (one-year lag, no circularity) |
| `GDPGROWTH` | base_growth, level_now, level_before | `(1+base_growth)*level_now/level_before-1` | Real GDP growth after the feedback: (1 + baseline growth) x level factor / last year's - 1 |
| `POLLUTANT` | fuel_use, ef_start, ef_end, weight | `SUMPRODUCT(fuel_use,ef_start*(1-weight)+weight*ef_end)/tPerKt` | Emissions of a pollutant (kt): fuel use (ktoe) x emission factor (t/ktoe, between the base-year and final factor by weight), summed over the fuels, / tPerKt |
| `PERCAPITA` | growth_total, growth_pop | `(1+growth_total)/(1+growth_pop)-1` | Per-capita growth: (1 + total growth) / (1 + population growth) - 1 |
| `EFFORT` | on_flag, emis, emis_ref | `IF(AND(LEFT(on_flag,3)="Yes",emis_ref>0),emis/emis_ref,1)` | Mitigation effort in non-energy sectors: energy CO2 of the scenario / scenario 1 if switched on, else 1 |
| `DRIVER` | growth_inc, el_inc, growth_pop, el_pop, effort, effort_prev | `(1+growth_inc)^el_inc*(1+growth_pop)^el_pop*effort/effort_prev` | Growth factor of a non-energy category: income and population growth with their elasticities, times the change in the mitigation effort |
| `GROWINDEX` | prev, growth_inc, el_inc, growth_pop, el_pop | `prev*(1+growth_inc)^el_inc*(1+growth_pop)^el_pop` | Activity index of a methane source: previous x income and population growth with elasticities |
| `ABATE` | coef_a, coef_b, fee | `MIN(1,MAX(0,coef_a*fee^coef_b))` | Methane abatement share: MIN(1, MAX(0, a x fee ^ b)), fee in USD per t CH4 (curves of sheet CH4Inputs) |
| `METHSOURCE` | base_kt, activity, activity_base, intensity, abate | `IF(activity_base=0,0,base_kt*activity/activity_base*intensity*(1-abate))` | Methane of a source (kt): base-year emissions x activity / base-year activity x intensity index x (1 - abatement) (v0.9.0, R8.7: intensity decline as legacy rows 6077-6079, 6103, 6159-6183; L135 fixed) |
| `INTDECLINE` | decline, cur_year | `(1-decline)^MAX(0,cur_year-GHGYear)` | Methane intensity index (v0.9.0, R8.6): (1 - rate of decline)^MAX(0, year - GHGYear) (legacy rows 6077-6079, 6103, 6159, 6171, 6183; Manual inputs J185:J188) |
| `FLARING` | flare_share, base_kt, activity, activity_base, abate | `IF(activity_base=0,0,FlareCO2perCH4*flare_share*base_kt*activity/activity_base*abate/ktPerMt)` | CO2 from flaring the abated oil and gas methane (Mt): FlareCO2perCH4 x flared share x abated CH4 |
| `CALIBRATE` | inventory, modelled | `IF(modelled=0,0,inventory/modelled)` | Calibration factor: inventory / modelled (0 if nothing is modelled) |
| `INVORMODEL` | hist, inventory, model | `IF(hist>0,inventory,model)` | Inventory value while the inventory has the year (hist > 0), else the model |
| `IPPU` | hist, inventory, prev, on_flag, growth | `IF(hist>0,inventory,prev*(1+IF(LEFT(on_flag,3)="Yes",growth,0)))` | Industrial processes: inventory, else the previous value grown with industrial energy CO2 (increases only, legacy) if the switch is Yes |
| `LULUCF` | hist, inventory, prev, effort, effort_prev, decline | `IF(hist>0,inventory,IF(prev<0,prev,prev/effort_prev*effort-decline))` | LULUCF CO2: inventory, else (if positive) the previous value with the effort change, minus the annual decline (share of the last inventory value) |
| `FEEREV` | emissions_kt, gwp, applies, fee | `SUMPRODUCT(emissions_kt,gwp,applies)*fee*tPerKt/USDperM` | Methane fee revenue (USD million): SUMPRODUCT of CH4 by source (kt), its GWP and whether the fee applies (v0.4.12, legacy Manual inputs J196-J200) x fee (USD/tCO2e) x tPerKt / USDperM |
| `NEWREVRATE` | carbon_tax, excise, ets, rev_factor, new_policy, vat_rate | `carbon_tax+excise+ets*rev_factor+new_policy*vat_rate` | New-policy revenue rate ($/GJ): carbon tax + new excise + ETS x revenue factor + VAT on new policies (feebates are revenue-neutral) |
| `FUELUSE` | f_prev, p_now, p_prev, shp_now, shp_prev, gdp_g, eps_y, eps_u, eff_exp, aeei_factor, shock_f | `f_prev*aeei_factor*(1+gdp_g)^eps_y*(p_now/p_prev)^eps_u*((p_now+shp_now)/(p_prev+shp_prev))^eff_exp*shock_f` | Fuel use, CPAT documentation 3.3.3, shadow price on the efficiency margin, x the fuel-use shock factor (legacy row 2439); efficiency exponent = eps_F x (1+eps_U); aeei_factor = row aef; gdp_g = GDP growth with the income factor |
| `CAPEX` | capex_base, time_factor | `capex_base*time_factor` | Capital cost of new plants ($/kW): capital cost at factor 1 x capex time factor |
| `AEEIFACTOR` | alpha, extra_eff, eps_u | `(1/(1+alpha+extra_eff))^(1+eps_u)` | Efficiency factor of fuel use (v0.4.13): (1/(1 + autonomous efficiency gain + additional policy-induced gain of the group, MTInputs 243-245))^(1 + usage elasticity), legacy fuel rows |
| `VINTAGE` | avg_prev, new_value, share_prev | `avg_prev*(1-share_prev)+new_value*share_prev` | Vintage average: last year's average x (1 - last year's investment share) + new value x last year's investment share (legacy B2, B6) |
| `AMORTISED` | capex_avg, inv_life, wacc, cap_factor, other_fixed, storage_avg | `(capex_avg*(inv_life+wacc*CapAvgShr)+other_fixed)/(cap_factor*HoursYr)+storage_avg` | Amortised fixed cost ($/kWh): (average capex x (1 / lifetime + WACC x CapAvgShr) + decommissioning / lifetime + fixed opex) / (capacity factor x 8,760) + storage average (v0.5.4: WACC and capacity factor of the scenario) |
| `LEVELISED` | capex, dtc_tcx, cap_factor, dlf, opex_fix, subsidy, vre_flag, storage | `(capex+dtc_tcx)/(cap_factor*HoursYr*dlf)+opex_fix/(cap_factor*HoursYr)+subsidy+vre_flag*storage` | Levelised fixed cost of new plants ($/kWh): (capex + decommissioning + transmission capex) / (capacity factor x 8,760 x discounted lifetime) + fixed opex / (capacity factor x 8,760) + renewable subsidy + storage if VRE (v0.5.4: of the scenario) |
| `VARCOST` | fixed_part, fuel_price, gj_per_kwh, xcarbon | `fixed_part+fuel_price*gj_per_kwh+xcarbon` | Variable cost ($/kWh): variable O&M and fixed fuel + fuel price ($/GJ) x GJ per kWh + change in existing carbon pricing |
| `EXEMPTPHASE` | scen, phase_on, yr, intro, start, period | `IF(AND(scen>1,phase_on=TRUE,yr>=intro),MAX(MIN((yr+1-start)/period,1),0),0)` | Exemption phase-out: share of an uncovered fuel or sector taxed in policy scenarios (legacy rows 2259-2265; v0.5.6) |
| `COALICPICK` | setting, manual, data | `IF(LEFT(setting,1)="N",0,IF(setting="Manual",manual,data))` | Coal implicit cost chosen ($/kWh): No = 0, Manual = MTInputs, else GoalSeekCoal by country (v0.5.6, P5) |
| `COALIC` | short_term, long_term, year | `short_term+(long_term-short_term)*MIN(1,(year-BaseYr)/(CoalICYr-BaseYr))` | Coal implicit cost ($/kWh): short term to long term by CoalICYr (2030), linear (v0.5.6, P5; legacy D3) |
| `GENCOSTIC` | fixed_cost, variable_cost, coal_ic | `fixed_cost+variable_cost-IF(PwCoalICTariff="No",coal_ic,0)` | Generation cost: fixed + variable cost, less the coal implicit cost if PwCoalICTariff = No (v0.5.6, P5) |
| `POWFUELPRICE` | spot, price_now, prices | `IF(spot=1,price_now,AVERAGE(prices))` | Fuel price for power ($/GJ; v0.6.2: trailing 5-year average, legacy bug L126): spot price if the spot switch is 1 (SpotPow or the scenario's MTInputs switch), else the average of the years t-4 to t from the base year (legacy 465 A18) |
| `PNEWREV` | gen, policy_cost, emissions, ets_rate, rev_factor | `gen*MWyMkWh*policy_cost-emissions*ets_rate*(1-rev_factor)` | Power new-policy revenue (USD million): generation (MWy) x MWyMkWh x policy cost ($/kWh) - CO2 x ETS cost rate x (1 - revenue factor) |
| `GENCOST` | fixed_cost, variable_cost | `fixed_cost+variable_cost` | Generation cost before new policies ($/kWh): fixed + variable |
| `WEIGHTED` | shares, values, factor | `SUMPRODUCT(shares,values)*factor` | Generation-weighted sum: SUMPRODUCT(shares, values) x factor |
| `STORAGEHOUR` | battery, interface, opex, kwh_per_kw, dlf | `(battery+interface/kwh_per_kw)/(dlf*HoursYr)+opex/HoursYr` | Short-term storage cost per marginal hour ($/kWh): annualised battery and interface capex + opex |
| `STORAGECOST` | st_hours, vre, cph, lt_start, lt_cost, lt_units | `st_hours*vre*cph+2*MAX(0,vre-lt_start)/(1-lt_start)^2*lt_cost*lt_units` | Marginal storage cost of variable renewables ($/kWh): short-term (allocated marginal hours x VRE share x cph) + long-term (2 x MAX(0, VRE share - start)/(1 - start)^2 x cost per unit x allocated units for 100% VRE) |
| `POWERSUPPLY` | gen_cost, tmc | `gen_cost+tmc` | Supply cost of electricity: generation cost (previous year) + transmission and distribution |
| `POWERPRICE` | year, pos, price_prev, pass, sc_now, sc_prev, vat_rate | `IF(year<=Settings!$C$10,IFERROR(INDEX(PwRpHist,pos,MATCH(year,PwRpYear,0)),0),price_prev+pass*(sc_now-sc_prev)*(1+vat_rate))` | Electricity price before new policies: data up to the last historical year (Inputs_power, row pos), then the previous price + pass-through x change in supply cost x (1 + VAT) |
| `ENDUSERPOWER` | pre_policy_p, policy_cost, pass, vat_rate, rebate, excise, min_price | `MAX(pre_policy_p+(policy_cost*pass*(1-rebate)+excise)*(1+vat_rate),min_price)` | End-user electricity price: price before new policies + (average new policy cost x pass-through x (1 - rebate switch) + excise) x (1 + VAT), floored at MinPostSubsidyPowerPrice (v0.5.4: rebate and excise; v0.5.6: floor, legacy rows 3614-3617, I60) |
| `SUBSIDYGAP` | supply_cost, pre_policy_p, vat_rate | `pre_policy_p/(1+vat_rate)-supply_cost` | Subsidy gap ($/kWh): price before VAT - supply cost (negative = subsidy) |
| `POWERREV` | unit_value, factor, consumption | `unit_value*factor*consumption` | Power revenue (USD million): rate ($/kWh) x factor x consumption (GWh) |
| `REBATE` | fees, shares | `-SUMPRODUCT(fees,shares)` | Feebate rebate per kWh generated: -SUMPRODUCT(shadow price per kWh, base-year generation shares) |
| `VARTOTAL` | base_cost, policy_cost, shadow, rebate | `base_cost+policy_cost+shadow+rebate` | Total variable cost: before new policies + new policy cost + shadow price + rebate |
| `INVCOST` | levelised_fixed, levelised_var, minimum | `MAX(levelised_fixed+levelised_var,minimum)` | Levelised investment cost: MAX(levelised fixed + levelised variable cost, minimum) |
| `SYSCOST` | dtc_tcx, cap_factor, dlf, vre_flag, storage, coal_ic | `dtc_tcx/(cap_factor*HoursYr*dlf)+vre_flag*storage+coal_ic` | System cost by type ($/kWh; v0.9.0, R9.5, legacy F1): (decommissioning + transmission share) / (capacity factor x 8,760 x discounted lifetime) + storage if VRE + coal implicit cost |
| `LEVCAPEX` | capex, cap_factor, dlf | `capex/(cap_factor*HoursYr*dlf)` | Levelised capital cost by type ($/kWh; v0.9.0, R9.6, legacy E5 C1): capex / (capacity factor x 8,760 x discounted lifetime) |
| `OMCOST` | opex_fix, cap_factor, opex_var | `opex_fix/(cap_factor*HoursYr)+opex_var` | O&M cost by type ($/kWh; v0.9.0, R9.7, legacy E5 A16 + D1): fixed O&M / (capacity factor x 8,760) + variable O&M |
| `MEMOOF` | amount | `amount` | Memo copy of a value of the same column (v0.9.0, R9.10-R9.11) |
| `HISTHOLD` | cur_year, amount, held | `IF(cur_year<=LastHist,amount,held)` | Value up to the last historical price year, then held (v0.9.0, R7, R9) |
| `PRICEGAP` | net_price, supply, excise | `net_price-supply-excise` | Electricity price before VAT less the supply cost and the manual excise (v0.9.0, R9.1, legacy N3605) |
| `ELTAXBASE` | cur_year, data_val, gap, scds, held | `IF(cur_year<=LastHist,IFERROR(data_val+0,gap*(scds="Yes")),held)` | Electricity consumer tax / subsidy (v0.9.0, R9.1, legacy rows 3604-3606): the dataset value up to the last price year (blank: the price gap if SupplyCostDeltaSubsidy = Yes, else 0), then held |
| `PREGAP` | supply, net_price, tax, cons | `MAX(0,supply-(net_price-tax))*cons` | Pre-tax gap x consumption: MAX(0, supply cost - (price before VAT - tax)) x GWh (v0.9.0, R7.5, legacy 3588) |
| `PSALLOC` | cur_year, gap_u, gaps, cons_u, conss, fallback, held | `IF(cur_year<=LastHist,IFERROR(gap_u/gaps,IFERROR(cons_u/conss,fallback)),held)` | Share of the electricity producer subsidy (v0.9.0, R7.5, legacy 3588-3589): by the pre-tax gap, else by consumption, else the fallback; held after the last price year |
| `PSELEC` | cur_year, pros, alloc, cons, last_unit, kept | `IF(cur_year<=LastHist,IFERROR(MAX(PsElFloor,-pros*alloc/cons),0),last_unit*kept)` | Electricity producer subsidy per kWh (v0.9.0, R7.6, R7.8, legacy 3590-3591, 3601): -subsidy x share / consumption, at least PsElFloor (I146); after the last price year the last value x the phase-out factor |
| `PSERESID` | cur_year, pros, used, last_val, kept | `IF(cur_year<=LastHist,-pros-used,last_val*kept)` | Electricity producer subsidy above the floor (USD m; v0.9.0, R7.7, legacy 3592): -subsidy - consumption x per kWh; after the last price year x the phase-out factor |
| `CSELEC` | cur_year, tax, incl, kept | `IF(AND(cur_year>LastHist,tax<0,incl="Include"),tax*(kept-1),0)` | Electricity consumer subsidy phase-out (v0.9.0, R9.2, legacy O3606): tax of the last price year x (factor - 1) if it is a subsidy and PowerSubsidyExemptInclude = Include |
| `ELSUPPLY` | supply, resid, policy_cost, pass, rebate, excise | `supply+resid+policy_cost*pass*(1-rebate)+excise` | Electricity supply cost of the subsidy lines (v0.9.0, R9; legacy rows 3620, 3649 "supply costs (removing estimation)"): supply cost + price-chain residual + new carbon cost passed through (less the rebate) + excise |
| `CAPLAST` | cur_year, supply, supply_last | `IF(cur_year<=LastHist,supply,MIN(supply,supply_last))` | Supply cost up to the last price year, then capped at its value then (v0.9.0, R9.3, legacy O3607) |
| `ORESID` | cur_year, hist_val, prev_val, capped, capped_prev | `IF(cur_year<=LastHist,hist_val,IF(prev_val<0,prev_val*capped/capped_prev,prev_val))` | Electricity price-chain residual (v0.9.0, R9.3, legacy rows 3607, 3636): price gap - tax - producer subsidy up to the last price year; then held, a negative one x capped supply cost / last year's |
| `CONSUMPTION` | total, res, w_total, w_res, gwh_per_ktoe | `(w_total*total+w_res*res)*gwh_per_ktoe` | Electricity consumption (GWh) of a price group: (w_total x total + w_res x residential demand) x GWh per ktoe |
| `PRICEMIX` | w_res, p_res, p_ind | `w_res*p_res+(1-w_res)*p_ind` | Price used by a demand group: weighted residential and industrial price |
| `DEMANDMULT` | eff_mult, gdp_g, eps_y, income, p_now, p_prev, eps_p, shock, shock_on | `eff_mult*(1+gdp_g)^(eps_y*income)*(p_now/p_prev)^eps_p*(1+shock*shock_on)` | Growth multiple of electricity demand: efficiency multiple x GDP term x price term x (1 + shock x switch) |
| `GROW` | prev, multiple | `prev*multiple` | Previous value x multiple |
| `SCALEBY` | value, factor | `value*factor` | Value x factor |
| `SWITCHPRICE` | cost_gas, cost_coal, int_coal, int_gas | `IFERROR((cost_gas-cost_coal)/(int_coal-int_gas),0)` | Switching carbon price gas over coal ($/tCO2): cost difference / carbon intensity difference (v0.5.6, P5 memo, legacy F7) |
| `RESIDUAL` | total, part | `MAX(total-part,0)` | MAX(total - part, 0) |
| `NEEDNEXT` | req_now, req_prev, kafter | `MAX(req_now*IFERROR(req_now/req_prev,1)-kafter,0)` | Effective capacity needed (v0.4.14, legacy bug L67 fixed): next year's required generation (this year's in the last year) - capacity after retirements, not below 0; bought this year, online next year |
| `FLOORMIN` | values, flags, min_value | `MAX(_xlfn.MINIFS(values,flags,1),min_value)` | Lowest value among flagged members (flag = 1), at least the floor |
| `MINDISPATCH` | flag, required, max_all, max_own | `flag*MIN(MAX(required-(max_all-max_own),0),max_own)` | Minimum generation of coal or gas: what is still needed if the other runs at its maximum |
| `LOGITW` | flag, k, cost, lowest | `flag*EXP(-k*cost/lowest)` | Logit weight: flag x EXP(-K x cost / lowest cost) |
| `DISPATCH` | flag, fixed_output, max_gen, min_gen, remainder, weight, weight_sum | `IF(flag=1,MIN(max_gen,min_gen+remainder*weight/weight_sum),fixed_output)` | Generation: coal and gas MIN(maximum, minimum + remainder x logit share); other types their effective capacity |
| `INCREASE` | value_now, value_prev | `MAX(0,value_now-value_prev)` | MAX(0, value - previous value) |
| `SHAREOF` | part, total | `IF(total=0,0,part/total)` | Part / total (0 if the total is 0) |
| `SUBQTY` | values, vars, fuels, fuel | `SUMIFS(values,vars,"ener",fuels,fuel)` | Fuel use of a fuel in a range of subsector rows (I31 legacy weights; v0.4.15) |
| `SUMOF` | values, keys, key | `SUMIFS(values,keys,key)` | Sum of the values whose key equals the key (SUMIFS; v0.4.15) |
| `PWFUELPRICE` | rpb, gen, ccp, fuel_use, pj_per_ktoe, mwy | `rpb+IF(fuel_use=0,0,gen*mwy*ccp/(fuel_use*pj_per_ktoe))` | Power fuel price incl. new policies ($/GJ): pre-policy price + policy cost of the type / its fuel use (v0.4.15, I31) |
| `LEGAVG` | p_res, q_res, p_ind, q_ind, p_pow, q_pow, fallback | `IF(q_res+q_ind+q_pow=0,fallback,(p_res*q_res+p_ind*q_ind+p_pow*q_pow)/(q_res+q_ind+q_pow))` | Average price as legacy F5b (v0.4.15, I31): residential, industry and power prices weighted by scenario-1 quantities |
| `PICKINDEX` | method, legacy, laspeyres | `IF(LEFT(method,3)="Leg",legacy,laspeyres)` | Price index reported: the legacy average price index or the Laspeyres index (Settings C54; v0.4.15) |
| `FUELSPEND` | fuel, prices, qty | `SUMPRODUCT(--(SecVar="atp"),--(SecFuel=fuel),prices,qty)` | Spending on one fuel: sum over the sector rows of after-tax price x fuel use (v0.3.10) |
| `FUELQTY` | fuel, qty | `SUMIFS(qty,SecVar,"ener",SecFuel,fuel)` | Fuel use of one fuel: sum over the sector rows (v0.3.10) |
| `BLOCKQTY` | pos, qty | `SUMIFS(qty,PVar,"atp",PPar,pos)` | Fuel use of the subsectors priced by one section-2 price block (atp rows whose D = the block position; qty = the ener rows aligned with the atp rows) (v0.4.1) |
| `BLOCKAVG` | pos, vals, qty, total, before | `IF(total=0,before,SUMPRODUCT(--(PVar&PPar="atp"&pos),vals,qty)/total)` | Fuel-use weighted average over the subsectors priced by one section-2 price block of a subsector row (vals, aligned with the atp rows); before if the block has no fuel use (v0.4.1) |
| `SPENDSUM` | prices, qty | `SUMPRODUCT(prices,qty)` | Spending: SUMPRODUCT of prices and quantities (electricity, v0.3.10) |
| `ALLSPEND` | fuel_sum, factor, ele | `fuel_sum*factor+ele` | All energy: fuel spending x PJ per ktoe + electricity spending (USD m, v0.3.10) |
| `MIXEFFECT` | ratio_uv, ref_uv, laspeyres | `IF(ref_uv*laspeyres=0,0,ratio_uv/ref_uv/laspeyres)` | Mix effect: unit value / unit value of scenario 1 / price index (v0.3.10) |
| `CARRY` | cap_prev, ret_prev, inv_prev | `cap_prev-ret_prev+inv_prev` | Capacity: last year less last year's retirements plus last year's new investment |
| `RETIRE` | cap, ret_rate, early_flag, early, planned_on, planned | `MIN(IF(planned_on=1,planned,cap*ret_rate)+early_flag*early,cap)` | Retirement: MIN(planned retirement (data, if switched on) or capacity x rate, + early retirement (coal), capacity) |
| `EARLYROOM` | add_wind, add_solar, demand_increase, retirements | `MAX(0,add_wind+add_solar-demand_increase-(retirements))` | Room for early coal retirement: maximum wind and solar additions less demand increase and retirements |
| `LOWEST3` | x, y, z | `MIN(x,y,z)` | Lowest of three values |
| `COALSHARE` | k, c_coal, c_wind, c_solar, lowest | `1/(1+EXP(-k*(c_wind-c_coal)/lowest)+EXP(-k*(c_solar-c_coal)/lowest))` | Coal share of the early-retirement logit: EXP(-K c_coal / lowest) / (sum over coal, wind, solar), written as 1 / (1 + EXP(-K (c_wind - c_coal) / lowest) + EXP(-K (c_solar - c_coal) / lowest)) |
| `EARLYRET` | coal_eff, max_share, room, coal_share, factor, cf_coal | `MAX(0,MIN(coal_eff*max_share,room)*(1-coal_share))/cf_coal*factor` | Cost-based early coal retirement (nameplate): MIN(coal effective capacity x maximum share, room) x (1 - logit share of coal) / capacity factor x factor |
| `DIFF` | minuend, subtrahend | `minuend-subtrahend` | Difference |
| `PERMITTED` | outcome, start, year | `IF(AND(outcome="Yes",year>=start),1,0)` | 1 if new investment is permitted (Yes) and the year is at least the start year |
| `SCALEUP` | up_rate, capacity, permit | `up_rate*capacity*permit` | Maximum effective investment: scale-up rate x total effective capacity x permit |
| `FIRSTROUND` | max_inv, need, share | `MIN(max_inv,need*share)` | First-round investment: MIN(maximum, need x logit share) |
| `SPACE` | max_inv, first, permit | `(max_inv-first)*permit` | Remaining space: (maximum - first round) x permit |
| `CHEAPFILL` | permit, space, deficit, cheaper_space | `permit*MAX(0,MIN(space,deficit-cheaper_space))` | Second round, cheapest first: permit x MAX(0, MIN(space, deficit - space of cheaper types)) |
| `ADDED` | round_1, round_2 | `round_1+round_2` | First + second round |
| `INVSPEND` | nameplate, capex | `nameplate*capex*kWperMW/USDperM` | Investment (USD million): nameplate MW x capital cost ($/kW) x kWperMW / USDperM |
| `VINTSHARE` | new, cap, ret | `IF(cap+new-ret=0,0,new/(cap+new-ret))` | Share of new investment in the stock after retirements: new / (cap + new - ret) |
| `CFUSED` | actual, studies, bound_lo, bound_hi | `IF(AND(actual>bound_lo,actual<bound_hi),actual,studies)` | Capacity factor used: the actual one when strictly inside the bounds (CFOverride settings of the scenario), else the studies value (L53 fixed) |
| `EFFUSED` | actual, studies, minimum | `IF(actual<minimum,studies,actual)` | Efficiency used: the actual one unless below the minimum thermal efficiency (no input: -1), else the studies value |
| `WACCCODE` | source | `IF(LEFT(source,7)="Country","C",IF(source="Tech","T",""))` | WACC option of the scenario: C (Country*), T (Tech), "" (User, Income* or the studies) |
| `WACCFIXED` | source, user_wacc | `IF(source="User",user_wacc,IF(LEFT(source,6)="Income",PsIncWacc,""))` | WACC of the options User (WACCUserGlobal) and Income* (by income group, Power N20:N23); "" otherwise |
| `WACCUSED` | w_code, w_country, w_tech, w_studies, w_fixed, w_min | `IF(w_code="C",w_country,IF(w_code="T",w_tech,MAX(IF(w_fixed="",w_studies,w_fixed),w_min)))` | WACC used by type: Country* or Tech option, else MAX(fixed or studies WACC, minimum WACC) (legacy X of rows 2988-2996) |
| `LIFEFACTOR` | wacc, life | `(1-(1+wacc)^-life)/(1-(1+wacc)^-1)` | Discounted lifetime (annuity factor) (1 - (1 + WACC)^-life) / (1 - (1 + WACC)^-1) |
| `PAIRMEAN` | value_a, value_b | `AVERAGE(value_a,value_b)` | Average of two values |
| `FUELPERKWH` | has_fuel, efficiency | `has_fuel*GJperkWh/efficiency` | Fuel per kWh (GJ/kWh): GJperkWh / efficiency for types with a price fuel, else 0 |
| `PICKTYPE` | settings, pos | `INDEX(settings,pos)` | The setting of the type: INDEX(settings, position) |
| `MANCAP` | pos, scen, year | `IFERROR(INDEX(ManCapVal,pos+IF(scen=1,0,ManCapOff),MATCH(year,ManCapYr,0))+0,0)` | Manual capacity path of the type (MW): Manual inputs rows 349-357 (scenario 1) or 363-371 (other scenarios), by year; blank = 0 (v0.5.6, P3) |
| `MANINV` | setting, cap_next, cap_now, retired, cf | `IF(AND(setting="Manual",ISNUMBER(cap_next)),MAX(0,cap_next-cap_now+retired)*cf,0)` | Manual new effective investment (MW): if NewInv<type> = Manual, MAX(0, next year's path - this year's path + retirement) x capacity factor; 0 in the last year (v0.5.6, P3; legacy rows 4097-4118) |
| `INVPRESENT` | setting, cap_type, cap_all | `IF(setting="If Present*",IF(cap_type/SUM(cap_all)>InvPresentShare,"Yes","No"),setting)` | New investment permitted: "If Present*" = Yes if the type has more than InvPresentShare of base-year capacity, else the setting |
| `INVSTART` | hydro, gen_share, start_in | `IF(AND(hydro=1,gen_share>HydInvShare),BaseYr,start_in)` | Start year of new investment: the base year for hydro with a generation share above HydInvShare (L54), else the MTInputs year |
| `SCALECAT` | category | `IFERROR(INDEX(PowScRate,MATCH(category,PowScCat,0)),0)` | Scale-up rate of a category (Low, Medium*, High, Vhigh; Power I20:J23), 0 if not found |
| `SCALEVRE` | category, user_rate, cat_rate | `IF(LEFT(category,4)="Ctry",PsScCtry,IF(category="UserDefined",user_rate,cat_rate))` | Scale-up rate of wind and solar: country default (Ctry*), user defined or the category rate |
| `SCALETYPE` | non_vre, wind_solar, r_non_vre, r_vre, r_other | `IF(non_vre=1,r_non_vre,IF(wind_solar=1,r_vre,r_other))` | Scale-up rate by type: coal, gas, hydro; wind and solar; the others |
| `RETIRERATE` | inv_life, hydro, no_retire | `IF(AND(hydro=1,no_retire="Yes"),0,inv_life)` | Retirement rate: 1 / lifetime; hydro 0 if HydroDoesntRetire = Yes |
| `EARLYFACTOR` | scen, in_baseline, max_share | `IF(AND(scen=1,in_baseline<>"Yes"),0,max_share)` | Factor on cost-based early coal retirement: 0 in scenario 1 unless EarlyRetirementInBaseline = Yes, else MaxCostBasedEarlyRetirement (legacy F3993) |
| `SPOTSWITCH` | setting | `--OR(SpotPow="Yes",LEFT(setting,3)="Yes")` | 1 if spot fuel prices are used for power: Settings SpotPow or the scenario's MTInputs switch |
| `DECLINECODE` | decline | `IF(decline="High","hgh",IF(LEFT(decline,1)="V","vhg",LOWER(LEFT(decline,3))))` | Capex time-factor scenario code (low, med, hgh, vhg) of RenewableCostDeclineRate |
| `PPASHARE` | ppa_share, scen, phase_base, phase_pol, cur_year, start, years | `ppa_share*IF(LEFT(IF(scen=1,phase_base,phase_pol),3)="Yes",MAX(0,1-MAX(0,cur_year-start)/years),1)` | PPA share of coal and gas generation: share x phase-out factor (Yes or Yes*: linear to 0 over the years after the start year; baseline switch in scenario 1, policy switch elsewhere; legacy row 2218) |
| `RENSUBSIDY` | base_sub, add_sub, scen, cur_year, start, years, nom_to_real | `-(base_sub+IF(AND(scen>1,cur_year>=start),add_sub*MAX(0,1-(cur_year-start)/years),0))*nom_to_real` | Renewable subsidy per kWh (negative): base subsidy + additional subsidy of policy scenarios from its start year, phased out linearly (legacy rows 2743-2745) |
| `RENBYTYPE` | subsidy, renewable, hydro, hydro_on | `subsidy*IF(renewable=1,1,hydro*(LEFT(hydro_on,3)="Yes"))` | Renewable subsidy of the type: wind, solar, other renewables, biomass; hydro if switched on |
| `REBATESWITCH` | scen, setting, scn | `--AND(scen>1,OR(LEFT(setting,3)="Yes",IF(scn=0,FALSE,INDEX(ScnReb,scn)="Yes")))` | Power revenues rebated (1 / 0): policy scenarios with PowerRebates = Yes or a feebate scenario (scenario table; legacy rows 261, 2188) |
| `EXCISECARBON` | scen, scn, carbon | `IF(OR(scen=1,scn=0),0,--(INDEX(ScnElx,scn)="Yes"))*PwGInt*carbon` | Electricity excise ($/kWh): grid CO2 intensity x carbon price in the scenario Electricity excise (legacy rows 2190, 2253) |
| `LTSTORAGE` | capex, tank, hours, dlf, opex_fix, opex_var | `(capex+tank*hours)/(dlf*HoursYr)+opex_fix/HoursYr+opex_var` | Long-term storage cost per marginal unit: (electrolyser + tank x hours) / (discounted lifetime x 8,760) + fixed opex / 8,760 + variable opex |
| `INCOMESWITCH` | setting, factor | `IF(LEFT(setting,3)="Yes",factor,1)` | Income factor on the GDP elasticities: the factor if IncElAdj starts with Yes, else 1 |
| `MAXOUTPUT` | cap, coal, cf_coal, gas, cf_gas | `cap*(coal*cf_coal+gas*cf_gas)` | Maximum generation of coal (MaximumCoalCF) or gas (MaximumGasCF): capacity x maximum capacity factor |
| `PPARATIO` | required, eff_cap | `IF(eff_cap=0,1,required/eff_cap)` | Coal and gas need / their effective capacity (1 if none; legacy row 3794) |
| `PPAMIX` | logit_gen, flag, ppa, eff_cap, ratio | `logit_gen+flag*ppa*(eff_cap*ratio-logit_gen)` | Generation of coal or gas with PPAs: logit dispatch + PPA share x (effective capacity x ratio - logit dispatch) (legacy rows 3804-3805) |
| `MANEXCISE` | scen, switch_on, excise, basis, defl, reform | `IF(scen>1,IF(LEFT(switch_on,3)="Yes",excise*IF(LEFT(basis,4)="Real",1,defl),0)+reform,0)` | Manual electricity excise of policy scenarios with AdditionalExcise = Yes (Manual inputs rows 161-162), x deflator index if NomorReal is not Real, plus the electricity fuel price reform path of the scenario (legacy rows 199-217, 3602; v0.5.6, I59) |
| `EXCISEPRICE` | excise_ct, after, pass, excise, excise_last | `excise_ct+IF(after,pass*(excise-excise_last),0)` | Excise in the price before VAT: electricity excise + pass-through x (manual excise - its value in the last historical year) after that year |
| `GASDEFICIT` | switch_on, deficit, second_all | `IF(switch_on="Yes",deficit-SUM(second_all),0)` | Investment deficit left after the second round, to gas if the switch is Yes (legacy rows 4247-4252) |
| `ENGINEERON` | choice | `IF(LEFT(choice,8)="Engineer",1,0)` | 1 if the MTInputs choice TrModel starts with Engineer, else 0 |
| `TRDATA` | flag, data, model | `IF(flag=1,data,model)` | Data years (flag 1): the data expression; other years: the model expression |
| `TRBLEND` | flag, value_a, value_b, weight | `IF(flag=1,value_a*weight+value_b*(1-weight),"")` | Data years: passenger and light blended by the passenger share of ownership; else blank |
| `OPENING` | data, frac, close_prev | `IF(N(data)>0,N(data)*frac,N(close_prev))` | Opening stock: data x share (new or used) where there are data, else last year's closing stock |
| `TRAILAVG` | anchor, span, first | `AVERAGE(INDEX(first:anchor,1,COLUMNS(first:anchor)+1-span):anchor)` | Average of the row over the last span years, this year included |
| `LAGVALUE` | anchor, span, first | `INDEX(first:anchor,1,COLUMNS(first:anchor)+1-span)` | Value of the row span - 1 years earlier |
| `RETIRED` | avg_stock, life, opening | `MIN(avg_stock/life,opening)` | Retirement: trailing-average stock / life, at most the opening stock |
| `MARKUP` | floor_v, cap_v, sat, ev_share, public | `MAX(floor_v,cap_v*(sat-ev_share)/(1-sat))*public` | Charging mark-up: MAX(floor, cap x (sat - EV share) / (1 - sat)) x share of public charging |
| `STATIONS` | flag, data, prev, stock, stock_prev, el_stock, cost, cost_prev, el_cost | `IF(flag=1,data,prev*(stock/stock_prev)^el_stock*(cost/cost_prev)^el_cost)` | Charging stations: data, else last year x (stock ratio)^elasticity x (cost ratio)^elasticity |
| `RANGEANX` | colnum, lag, start_v, prev, decline, stations, stations_prev, el_st | `IF(colnum<=lag,start_v,IF(prev<0,prev,MAX(prev*(1-decline)*(stations/stations_prev)^el_st,0)))` | Range anxiety: start value for the first lag years, then x (1 - decline) x (stations ratio)^elasticity (at least 0; a negative value is held) |
| `NEWFE` | flag, data, gap, prev, ratio, el_fe, aei | `IF(flag=1,data*(1+gap),prev*ratio^ABS(el_fe)*(1+aei))` | Fuel economy of new vehicles: data x (1 + gap), else last year x price ratio^/elasticity/ x (1 + AEI) |
| `FEEBATE` | yr, fyear, fb_rate, cprice, cov, pol | `(IF(yr>=fyear,fb_rate,0)+cprice*cov)*pol` | Vehicle feebate rate: feebate from its year + carbon price x road coverage, policy scenarios only |
| `RATIO` | now_v, before_v | `now_v/before_v` | Ratio of two values |
| `WAVG` | vals, wts | `SUMPRODUCT(vals,wts)/SUM(wts)` | Weighted average: SUMPRODUCT(values, weights) / SUM(weights) |
| `MIXTWO` | weight, value_a, value_b | `weight*value_a+(1-weight)*value_b` | Weighted mix of two values: weight x a + (1 - weight) x b |
| `GROWVKT` | flag, data, prev, ratio, price_on, el_p, gdp_g, el_y | `IF(flag=1,data,prev*IF(price_on,ratio,1)^el_p*(1+gdp_g)^el_y)` | Distance for the purchase decision: data, else last year x cost ratio^elasticity (if prices act) x (1 + lagged GDP growth)^income elasticity |
| `CLAMPVKT` | flag, data, prev, ratio, price_on, el_p, gdp_g, el_y, km_min, km_max | `IF(flag=1,data,MAX(km_min,MIN(km_max,prev*IF(price_on,ratio,1)^el_p*(1+gdp_g)^el_y)))` | As GROWVKT, kept between the minimum and maximum freight distance |
| `USEDVKT` | vkt, fe_new, fe_used, el_p | `vkt*(fe_new/fe_used)^el_p` | Distance of a used vehicle: new distance x (fuel economy new / used)^usage elasticity |
| `DISCKM` | disc_rate, nyears, km | `-PV(disc_rate,nyears,km)` | Discounted km over the years: -PV(rate, years, km) |
| `COSTKM` | fuel_price, fe, dist_tax | `fuel_price/fe+dist_tax` | Cost per km: fuel price / fuel economy + distance tax |
| `DISTTAX` | yr, yr_start, start_v, yr_target, target_v, prev, flag | `IF(yr=yr_start,start_v,MIN(target_v,N(prev)+(target_v-start_v)/(yr_target-yr_start)))*(yr>=yr_start)*flag` | Distance tax: start amount in its year, then rising linearly to the target (capped), policy scenarios |
| `CSRAMP` | yr, yr_start, yr_target, start_v, target_v, pol | `IF(yr<yr_start,0,start_v+(target_v-start_v)*MIN(1,(yr-yr_start)/MAX(1,yr_target-yr_start)))*pol` | Charging-station subsidy: 0 before the start year, linear to the target level, then constant (policy scenarios) |
| `PIVOTAVG` | colnum, lag, avg_now, avg_prev | `IF(colnum<=lag,"",avg_now*avg_now/avg_prev)` | Feebate pivot, average type: last year's sales intensity squared / the year before (blank at first) |
| `PIVOTMAN` | colnum, lag, yr, fyear, pivot, prev, decline | `IF(colnum<=lag,"",IF(yr=fyear,pivot,IF(yr>fyear,MAX(0,N(prev)-decline),0)))` | Feebate pivot, manual type: the pivot in the feebate year, then falling by the decline (at least 0) |
| `PIVOTPICK` | ptype, avg_pv, man_pv | `IF(LEFT(ptype,3)="Ave",avg_pv,man_pv)` | Feebate pivot used: average or manual type |
| `FBVEH` | intensity, pivot, fb_rate, km | `(intensity-N(pivot))*fb_rate/Million*km` | Vehicle feebate: (intensity - pivot) x rate / Million x discounted km |
| `GROSSUP` | veh_price, tax_a, tax_b, tax_c, extra | `veh_price*(1+tax_a)*(1+tax_b)*(1+tax_c)+extra` | Price after taxes: price x (1 + tax a) x (1 + tax b) x (1 + tax c) + extra (feebate, subsidy) |
| `POLPICK` | pol, yr, pyear, base_v, pol_v | `IF(OR(pol=0,yr<pyear),base_v,pol_v)` | Baseline value, or the policy value from its year in policy scenarios |
| `EVSUB` | yr, syear, amount, prev, step, pol | `IF(yr=syear,-amount,IF(yr>syear,MIN(0,N(prev)-step),0))*pol` | EV purchase subsidy (negative): amount in its year, then changing by the step (at most 0); policy scenarios |
| `ANNUITY` | amount, nyears, disc_rate | `amount/nyears/disc_rate*(1-1/(1+disc_rate)^nyears)` | Depreciation annuity: amount / years / rate x (1 - (1 + rate)^-years) |
| `SALVAGE` | veh_price, life, own, first_dep, disc_rate | `MIN(0,-veh_price*((life-own)/life*(1-first_dep))/(1+disc_rate)^own)` | Salvage value (negative) at the end of ownership, discounted |
| `RESALE` | veh_price, first_dep, own, life | `veh_price*(1-(first_dep+(own-1)/(life-1)*(1-first_dep)))` | Resale price after the ownership years (first-year and straight-line depreciation) |
| `INSMAINT` | veh_price, ins, disc_rate, nyears, ins_f, maint, km | `veh_price*ins/disc_rate*(1-1/(1+disc_rate)^(nyears+1))*ins_f+maint*km` | Insurance (annuity x factor) and maintenance (USD per km x discounted km) |
| `FUELKM` | fuel_price, fe, dist_tax, km | `(fuel_price/fe+dist_tax)*km` | Fuel and distance tax over the discounted km |
| `TOTAL` | parts | `SUM(parts)` | Sum of the parts |
| `TOTALRA` | parts, extra | `SUM(parts)+extra` | Sum of the parts + range anxiety (or another extra) |
| `TCOFUEL` | km, cost_km, fix_cost, feebate, int_ratio | `km*cost_km+fix_cost+N(feebate)*int_ratio` | TCO by ICE fuel: km x cost per km + fixed costs + feebate x intensity ratio |
| `LOGITICE` | k_par, tco_ice, tco_ev, tco_avg | `1/(1+EXP(-k_par*(tco_ev-tco_ice)/tco_avg))` | ICE share of purchases: logistic in the TCO difference relative to the average TCO |
| `ACTSHARE` | actual, calc | `IF(ISNUMBER(actual),1-actual,calc)` | ICE share: 1 - actual EV share where there are data, else calculated |
| `REST` | share | `1-share` | One minus the share |
| `ACTORCALC` | actual, calc | `IF(N(actual)>0,actual,calc)` | Actual value where positive, else calculated |
| `OWNEXP` | flag, sat, inc, coef_a, coef_b, prev | `IF(flag=1,sat*EXP(coef_a*EXP(inc*coef_b/Thousand)),prev)` | Ownership expected from the Gompertz curve in the data years (held after) |
| `GOMPTGT` | sat, inc, coef_a, coef_b, calib | `sat*EXP(coef_a*EXP(inc*coef_b/Thousand))*calib` | Gompertz ownership target: saturation x EXP(a x EXP(b x income / Thousand)) x calibration |
| `OWNDEM` | test, data_v, adj, target, prev | `IF(N(test)>0,data_v,adj*target+(1-adj)*N(prev))` | Ownership demand: data where there are data, else partial adjustment to the target |
| `CLAMPOWN` | test, data_v, prev, decline, max_growth, demand | `IF(N(test)>0,data_v,MAX(N(prev)*(1-decline),MIN(N(prev)*(1+max_growth),demand)))` | Ownership: data, else the demand within the decline and growth limits |
| `PLUG` | data, frac, after, purch | `IF(N(data)>0,N(data)*frac-after-purch,0)` | Data-year adjustment of purchases so that the closing stock equals the data |
| `ADDTHREE` | part_a, part_b, part_c | `part_a+part_b+part_c` | Sum of three values |
| `TURNOVER` | used_share, own, life | `1/(used_share*own+life*(1-used_share))` | Share of the stock bought new each year: 1 / weighted life |
| `NEWINSTOCK` | closing, after, den | `IF(den=0,0,(closing-after)/den)` | Share of this year's purchases in the closing stock (0 without stock) |
| `CROSSRATIO` | prev_sh, ratios, own_prev, own_ratio | `IFERROR((SUMPRODUCT(prev_sh,ratios)-own_prev*own_ratio)/(SUM(prev_sh)-own_prev),"")` | Weighted change in the TCO of the other fuels (blank if they have no share) |
| `ICESPLIT` | data, prev, ratio, el_own, cross, el_cross | `IF(ISNUMBER(data),data,IF(ISNUMBER(cross),N(prev)*ratio^el_own*cross^el_cross,N(prev)))` | ICE fuel share: data, else last year x own ratio^own elasticity x cross ratio^cross elasticity |
| `NORMSH` | test, share, total, ev_share | `IF(ISNUMBER(test),share,share/total*(1-ev_share))` | ICE fuel share scaled to 1 - EV share (data years: data) |
| `OWNSH` | data, prev, life, sales | `IF(ISNUMBER(data),data,N(prev)*(life-1)/life+sales/life)` | Fuel share of the stock: data, else moving average with this year's purchases (1 / life) |
| `PERTH` | value_a, value_b | `value_a*value_b/Thousand` | Per-1,000 value x value / Thousand |
| `OPENFE` | data, close_prev | `IF(ISNUMBER(data),data,N(close_prev))` | Opening stock fuel economy: data, else last year's closing |
| `STOCKFE` | data, new_fe, share_new, opening | `IF(ISNUMBER(data),data,new_fe*share_new+opening*(1-share_new))` | Closing stock fuel economy: data, else new x share bought new + opening x rest |
| `VKTFUEL` | data, factor, prev, ratio, el_p, inc_ratio, el_y | `IF(ISNUMBER(data),data*factor,N(prev)*ratio^el_p*inc_ratio^el_y)` | Distance per vehicle: data x calibration factor, else last year x cost ratio^elasticity x income ratio^income elasticity |
| `TWOFUEL` | km_a, fe_a, km_b, fe_b | `km_a/fe_a+km_b/fe_b` | Fuel use of two vehicle types: km / fuel economy each |
| `BEVFENEW` | fe_a, w_a, fe_b, w_b | `IF(w_a+w_b=0,AVERAGE(fe_a,fe_b),(fe_a*w_a+fe_b*w_b)/(w_a+w_b))` | Fuel economy of BEVs bought this year (new and used by their weights) |
| `BEVFEOPEN` | prev, new_fe | `IF(N(prev)>0,prev,new_fe)` | Opening BEV stock fuel economy: last year's closing, else new |
| `PHEVELE` | vkt, fe, gso_share | `vkt/fe*(1-gso_share)` | PHEV electricity: km / fuel economy x electric share |
| `EMITFUEL` | fuel, efs | `SUMPRODUCT(fuel,efs)*Thousand` | CO2 (kt): SUMPRODUCT(fuel, EF) x Thousand |
| `INTENSITY` | emis, km | `emis/km*Thousand` | CO2 intensity (g/km): emissions / km x Thousand |
| `INTENS0` | emis, km, ef, fe | `IF(km=0,ef/fe*Million,emis/km*Thousand)` | CO2 intensity; without distance: EF / fuel economy x Million |
| `KTOE` | bln_l, lpk, factor | `bln_l/lpk*Billion*factor` | Liters to ktoe: bln liters / liters per ktoe x Billion x factor |
| `KTOEELE` | bln_kwh, gwh, factor | `bln_kwh*Thousand/gwh*factor` | Electricity to ktoe: bln kWh x Thousand / GWh per ktoe x factor |
| `BUSFUEL` | base_ktoe, lpk, pas_now, pas_base | `base_ktoe*lpk/Billion*pas_now/pas_base` | Bus fuel: base-year bus fuel (ktoe) in bln liters x passenger fuel use / base year |
| `BUSELE` | base_ktoe, gwh, ele_now, pas_base | `base_ktoe*gwh/Thousand*ele_now/pas_base` | Bus electricity: base-year bus energy (ktoe) in bln kWh x passenger electricity / base year |
| `AVGFE` | test, fe_a, use_a, fe_b, use_b, weight | `IF(test=0,fe_a*weight+fe_b*(1-weight),(fe_a*use_a+fe_b*use_b)/(use_a+use_b))` | Average fuel economy weighted by fuel use (fixed weights without fuel use) |
| `AVGFEEV` | test, fe_a, fe_b, fe_c, weighted, e_sum | `IF(test=0,fe_a*TrFEWEvP+(fe_b+fe_c)*TrFEWEvO,weighted/e_sum)` | Average EV fuel economy weighted by electricity use (fixed weights without electricity use) |
| `PROD3SUM` | value_a, w_a, value_b, w_b, value_c, w_c | `value_a*w_a+value_b*w_b+value_c*w_c` | Sum of three products: a x weight a + b x weight b + c x weight c |
| `BIOFOLLOW` | prev_val, fuel_now, fuel_prev | `IF(fuel_prev=0,prev_val,prev_val*fuel_now/fuel_prev)` | Road bioethanol / biodiesel of the elasticity road model (v0.9.0, R10.1-R10.2, legacy 5404-5405): last year x gasoline / diesel use of this year / last year (held if last year is 0) |
| `BIOSPLIT` | gso_bio, die_bio, gso_base, die_base, gso_now, die_now | `IF(gso_base=0,gso_bio,gso_bio*gso_now/gso_base)+IF(die_base=0,die_bio,die_bio*die_now/die_base)` | Road biofuels (v0.4.12, legacy rows 5436-5438): bioethanol and other biofuels x gasoline / base year, biodiesel x diesel / base year |
| `HOLD` | prev | `prev` | Value of the previous year (base year: own formula) |
| `DISCRATE` | inc, top_rate, low_rate, inc_low, inc_high | `MIN(top_rate,MAX(low_rate,top_rate-(inc-inc_low)/(inc_high-inc_low)*(top_rate-low_rate)))` | Consumer discount rate, linear in GDP per capita between the two income levels |
| `FRESHARE` | flag, own_f, own_pl, cap_v, target, inc, inc_t | `IF(flag=1,own_f/own_pl,MIN(cap_v,MAX(target,cap_v-(cap_v-target)*inc/inc_t)))` | Freight share of ownership: data, else falling with income to the target, capped |
| `CYCHUMP` | flag, own, peak_v, peak_inc, inc | `IF(flag=1,own,(peak_v+peak_v)/(inc/peak_inc+peak_inc/inc))` | 2-3 wheeler ownership: data, else the income hump 2 x peak / (inc / peak inc + peak inc / inc) |
| `BEVUPLIFT` | flag, p_ev, p_ice, cap_v, el_p | `IF(flag=1,IF(p_ev=0,1,MIN(cap_v,(p_ev/p_ice)^el_p)),"")` | BEV / ICEV distance ratio in the data years: cost-per-km ratio^usage elasticity, capped |
| `INTAVG` | wts, efs, fe | `SUMPRODUCT(wts,efs)/SUM(wts)/fe*Million` | Average CO2 intensity of new ICEVs: SUMPRODUCT(weights, EF) / SUM(weights) / fuel economy x Million |
| `ROADSWITCH` | pos, switch_on, eng_rows, elastic, leak_rows, leak_pos | `IF(pos*switch_on>0,INDEX(eng_rows,pos),elastic)+INDEX(leak_rows,leak_pos)` | Fuel use: the engineer road row (section 5b) at the position where switched on, else the elasticity model; + the cumulative residential leakage to biomass of section 6b at its position (1 = none; v0.5.1) |
| `DEMROAD` | flag, switch_on, eng, prev, multiple | `IF(flag*switch_on>0,eng,prev*multiple)` | Electricity demand: road electricity of section 5b where the engineer model is on, else last year x the growth multiple |
| `DPCHG` | p_new, p_ref | `p_new/p_ref-1` | Distribution: relative price change of the analysis year against scenario 1 (fraction) |
| `DFAC` | peds, dp, eps | `dp*IF(LEFT(peds,3)="Yes",(1+dp)^eps,1)` | Distribution: price factor dp x (1 + dp)^eps of a decile (elasticity adjustment if PEDs = Yes) |
| `DTARGET` | share, cum, pct | `MAX(0,MIN(share,pct-cum+share))` | Distribution: targeted share of a decile (population share inside the bottom pct; cum = cumulative share through the decile) |
| `DPITPICK` | method, pa, prop, te | `IF(method="Personal Allowance",pa,IF(method="Proportional Compensation",prop,te))` | Distribution: PIT reduction per capita of the chosen method (MTInputs PITReductionType) |
| `DPOST` | cons, loss_pct | `cons*(1+loss_pct/PctPerUnit)` | Distribution: consumption after the policy (effect in % of consumption) |
| `DGINI` | cons, weights | `1-SUMPRODUCT(cons,weights)/SUM(cons)` | Distribution: Gini of decile consumption from the Lorenz-fit weights (legacy C.IX, DGiniW) |

## D. Index of variables

`acc.cost` E1236 · `AddEfficientTaxes` E30 · `AddEfficientTaxesPhaseInYears` E32 · `AdditionalCoalIntangibleCost` E214 · `AdditionalEfficiencyIndustrial` E155 · `AdditionalEfficiencyPower` E170 · `AdditionalEfficiencyResidential` E154 · `AdditionalEfficiencyRoadVehicle` E153 · `AdditionalExcise` E175 · `AdditionMitigationPoliciesNonEnergy` E165 · `aeef` E385 · `aef` E458 · `air.con.pm2` E1193 · `air.vpm` E1194 · `airpol.cost` E1189 · `airpol.cost.gj` E1191 · `airpol.cost.s` E1240 · `airpol.ecy` E1216 · `airpol.ecy.g` E1235 · `airpol.mc` E37 · `AllocateLTStorageToVRE` E200 · `AllocateSTStorageToVRE` E197 · `AlwaysExemptResLPGKer` E156 · `ap` E1253 · `ap.w` E1251 · `apco2` E1257 · `apen` E1256 · `apf` E1254 · `apfd` E1252 · `app` E1248 · `apq` E1217 · `aps` E1255 · `atp` E456 · `bca` E1172 · `bca.d` E1175 · `bca.dp` E1178 · `bca.gdp` E1173 · `bca.n` E1180 · `bca.p` E1176 · `bca.pp` E1179 · `bca.r` E1174 · `bca.y` E1177 · `bco2` E77 · `bco2.chk` E1073 · `cap` E408 · `cap0` E290 · `captot` E409 · `cax` E320 · `caxav` E321 · `cbat` E309 · `cc.code` E51 · `cc.glo` E1215 · `cc.nat` E1214 · `cchg` E1075 · `ccpav` E341 · `cel` E316 · `CFOverrideIfAbove` E185 · `CFOverrideIfBelowFosOth` E184 · `CFOverrideIfBelowWndSol` E183 · `cfu` E282 · `ch4` E460 · `ch4.abc` E1094 · `ch4.abt` E1095 · `ch4.act` E1093 · `ch4.c` E1098 · `ch4.em` E1097 · `ch4.emf` E1107 · `ch4.fk` E1090 · `ch4.int` E1096 · `ch4.pi` E1091 · `ch4.prd` E1092 · `ch4.rev` E1106 · `ch4.revf` E1108 · `ch4.src` E1088 · `ch4.sup` E1099 · `ch4.wd` E1089 · `ch4bs` E78 · `ch4bs.chk` E1109 · `cic` E327 · `cicl` E326 · `cics` E325 · `cik` E344 · `cint` E310 · `ClimateEffTax` E31 · `cmin` E423 · `co2` E404 · `co2.cap` E1069 · `co2.chg` E1079 · `co2.chk` E1074 · `co2.ets` E1068 · `co2.gap` E1070 · `co2.grid` E1076 · `co2.pct` E1066 · `co2.ref` E1065 · `co2.sec` E1067 · `con` E1230 · `con.cost` E1237 · `cons` E356 · `ConsSubPha` E129 · `ConsSubPhaBaseline` E133 · `cov.all` E1187 · `cov.ct` E1185 · `cov.ets` E1186 · `covct` E1184 · `cp.exp` E104 · `cp.nom` E14 · `cp.shd` E106 · `cp.t` E13 · `cpeff` E1183 · `cph` E406 · `CPIntro` E7 · `CPLevelStart` E8 · `CPLevelTarget` E9 · `CPOutro` E10 · `cptraj` E235 · `cpx` E105 · `cs` E251 · `csd` E381 · `csf` E145 · `csi` E144 · `csw` E454 · `CTaxComplimentaryToETS` E118 · `ctcov` E19 · `ctf` E300 · `CTforMethane` E158 · `ctr` E111 · `ctxnew` E448 · `cur` E347 · `deficit` E424 · `defl` E2 · `dem` E387 · `demg` E388 · `demtot` E389 · `dgas` E432 · `dgen` E401 · `dlf` E287 · `dlfr` E288 · `dmg` E1208 · `dsum` E337 · `early` E417 · `EarlyRetirementInBaseline` E192 · `echg` E1048 · `ecmin` E415 · `ecr` E1188 · `ecshr` E416 · `eff` E1211 · `eff.price` E1244 · `effcap` E410 · `effp.q` E1250 · `effprice` E1228 · `egrow` E414 · `elcx` E312 · `eldem` E447 · `elof` E314 · `elov` E315 · `eltk` E313 · `enel` E459 · `ener` E446 · `ener.chk` E1045 · `ener.pct` E1047 · `ener.ref` E1046 · `EngineerModelProportionOfCovidFactor` E172 · `entx` E360 · `entxd` E359 · `env.ffs.cost` E1222 · `epct` E1049 · `erf` E298 · `esub` E253 · `esubpu` E245 · `etr` E112 · `ets` E449 · `ets.bce` E82 · `ets.cap` E84 · `ets.chg` E83 · `ets.est` E86 · `ets.imp` E80 · `ets.lr` E1071 · `ets.next` E1072 · `ets.on` E70 · `ets.ovr` E87 · `ets.p` E88 · `ets.pe` E89 · `ets.rf` E90 · `ets.se` E85 · `ets.vadj` E81 · `ets.vol` E79 · `ETSAuctStart` E64 · `ETSAuctTarget` E65 · `etsb` E75 · `etsb.s` E73 · `etsb.t` E74 · `etsc` E72 · `ETSCapCont` E61 · `ETSChangeRelStart` E59 · `ETSChangeRelTarget` E60 · `etscov` E71 · `ETSCTRisk` E69 · `ETSIntro` E62 · `etsnew` E258 · `ETSOutro` E63 · `ETSPriceOverride` E66 · `ETSVolatility` E67 · `ETSVolImpact` E68 · `etx` E252 · `ExemptPhaseout` E15 · `ExemptPhaseoutPeriod` E17 · `exf` E157 · `ExistingCTApply` E114 · `ExistingCTGrowth` E115 · `ExistingETSApply` E116 · `ExistingETSGrowth` E117 · `EXPCapex` E1144 · `EXPCIT` E1143 · `EXPGoodsandserv` E1145 · `exph` E18 · `EXPLabortax` E1142 · `expsub.con` E1231 · `expsubgdp.con` E1233 · `EXPTransfers` E1146 · `exs` E307 · `extcost` E1226 · `ExtendCarbonPriceBeyondOutro` E11 · `ExternalityAddVAT` E33 · `fadtx` E250 · `fb` E95 · `fb.s` E93 · `fb.t` E94 · `fb.yr0` E91 · `fb.yr1` E92 · `fbcov` E96 · `fce` E343 · `FFPhaseOut` E131 · `ffs.q` E1221 · `FFSConsPhaseoutPeriodBA` E134 · `FFSProdPhaseoutPeriod` E124 · `FFSProdPhaseoutPeriodBA` E127 · `first` E429 · `fis.eff` E1161 · `fis.grp` E1159 · `fis.imp` E1155 · `fis.impp` E1157 · `fis.key` E1160 · `fis.lag` E1156 · `fis.lagp` E1158 · `fis.ref` E1153 · `fis.rev` E1152 · `fis.sp` E1154 · `fix` E323 · `FmAdj` E1149 · `fpn` E328 · `fpp` E329 · `fpr` E28 · `fpr.f` E23 · `fpr.s` E22 · `fpr.yr0` E20 · `fpr.yr1` E21 · `fpra` E27 · `fprj` E24 · `fprk` E25 · `fprp` E26 · `fuq` E1192 · `fus` E1190 · `gchg` E1110 · `gdp.base` E1151 · `gdp.chg.usd` E1166 · `gdp.eff` E1181 · `gdp.lcu` E4 · `gdp.lvl` E1162 · `gdp.pos.pct` E6 · `gdp.pos.usd` E1163 · `gdp.usd` E3 · `GDPEndogenous` E1150 · `gdpg` E1164 · `gdpn` E1060 · `gdppc.g` E1082 · `GDPStartYear` E1148 · `gdpy` E1165 · `gen_mwy` E399 · `ghg` E1102 · `ghg.chg` E1141 · `ghg.dr` E1086 · `ghg.enrp` E1111 · `ghg.flr` E1101 · `ghg.gi` E1085 · `ghg.h` E1083 · `ghg.inc` E1103 · `ghg.invb` E1087 · `ghg.k` E1100 · `ghg.m` E1084 · `ghg.pct` E1105 · `ghg.ref` E1104 · `glg` E397 · `gmin` E395 · `gmx` E394 · `gnc` E339 · `gncav` E340 · `gp` E241 · `gp.adj` E239 · `gp.src` E238 · `gpi` E243 · `gpn` E240 · `gtot` E400 · `HydroDoesntRetire` E190 · `impsub.con` E1232 · `impsubgdp.con` E1234 · `inc.ela.adj` E318 · `IncElAdj` E171 · `incp` E317 · `IndustrialProcessEmissionsScaleEner` E166 · `infl` E1 · `IntEnerPricForecastAdjustment` E237 · `IntEnerPricForeSource` E236 · `invs` E291 · `kafter` E418 · `kaya` E1077 · `kDispatch` E176 · `kidx` E1078 · `kInvestment` E177 · `kwh` E289 · `lfx` E324 · `lgd` E396 · `lgi` E427 · `lkb` E1035 · `lkc` E1042 · `lkcb` E1043 · `lkd` E1034 · `lkp` E1033 · `lks` E1044 · `lkt` E1032 · `lkx` E1039 · `lkxa` E1040 · `lkxe` E1037 · `lkxp` E1036 · `lkxr` E1038 · `lkz` E1041 · `LongTermStorageFor100pcVRE` E202 · `ltu` E302 · `LULUCFAnnualEmissionsDecline` E167 · `lvc` E338 · `mancap` E420 · `mani` E421 · `ManualCoalIntangibleCostLT` E216 · `ManualCoalIntangibleCostST` E215 · `MaxCostBasedEarlyRetirement` E191 · `MaximumCoalCF` E179 · `MaximumGasCF` E180 · `maxinv` E426 · `MaxNonNucOreBioAsPCOfTotalGen` E194 · `MaxNonVREAsPCOfTotalGen` E193 · `MaxScaleUpRateCategory` E196 · `MaxWindSolarScaleup` E195 · `mfc` E1213 · `mfee` E164 · `mfee.p` E163 · `mfp` E1212 · `MinimumThermalEfficiency` E182 · `MinimumWACC` E188 · `MinPostSubsidyPowerPrice` E178 · `MPIntro` E159 · `MPLevelStart` E160 · `MPLevelTarget` E161 · `MPOutro` E162 · `msc` E407 · `mult` E386 · `MultipliersSource` E1147 · `nce` E451 · `ndc.alt` E1116 · `ndc.bau` E1137 · `ndc.bi` E1124 · `ndc.bs` E1122 · `ndc.bty` E1123 · `ndc.co2` E1121 · `ndc.f` E1132 · `ndc.gap` E1139 · `ndc.gas` E1120 · `ndc.gdp` E1130 · `ndc.h` E1129 · `ndc.hc` E1127 · `ndc.hh` E1126 · `ndc.hi` E1131 · `ndc.hk` E1125 · `ndc.hv` E1128 · `ndc.idx` E1136 · `ndc.k` E1114 · `ndc.key` E1112 · `ndc.lu` E1119 · `ndc.lv` E1133 · `ndc.lvl` E1135 · `ndc.over` E1140 · `ndc.r` E1134 · `ndc.red` E1138 · `ndc.ref` E1117 · `ndc.ty` E1115 · `ndc.typ` E1113 · `ndc.x` E1118 · `need` E419 · `needm` E422 · `nei` E433 · `NewETS` E58 · `NewInvBio` E225 · `NewInvBioYear` E234 · `NewInvCoa` E217 · `NewInvCoaYear` E226 · `NewInvHyd` E223 · `NewInvHydYear` E232 · `NewInvNga` E218 · `NewInvNgaYear` E227 · `NewInvNuc` E220 · `NewInvNucYear` E229 · `NewInvOil` E219 · `NewInvOilYear` E228 · `NewInvOre` E224 · `NewInvOreYear` E233 · `NewInvSol` E222 · `NewInvSolYear` E231 · `NewInvWnd` E221 · `NewInvWndYear` E230 · `nid` E436 · `nim` E434 · `nimtot` E435 · `NomorReal` E12 · `ntx` E450 · `ntxb` E57 · `ntxg` E54 · `nuu` E283 · `obat` E311 · `obr` E76 · `ores` E382 · `pav.idx` E276 · `pav.las` E270 · `pav.leg` E274 · `pav.lidx` E275 · `pav.mix` E273 · `pav.q` E267 · `pav.sp` E266 · `pav.sp0` E271 · `pav.spr` E269 · `pav.time` E272 · `pav.uv` E268 · `pavl.pp` E280 · `pavl.qi` E278 · `pavl.qp` E279 · `pavl.qr` E277 · `pbc` E255 · `pcbcap` E349 · `pcbchk` E354 · `pcbcp` E352 · `pcbct` E355 · `pcbfu` E351 · `pcbom` E350 · `pcbrns` E353 · `pcf` E147 · `pci` E146 · `pcsw` E261 · `pctx` E257 · `pcw` E455 · `pdem` E384 · `pe` E403 · `perm` E292 · `permit` E425 · `pet` E445 · `pex` E361 · `PhaseOutCoalAndGasPPAsBaseline` E205 · `PhaseOutCoalAndGasPPAsPolicy` E206 · `phi` E438 · `pig` E1242 · `pig.ap` E50 · `pig.co2e` E1247 · `pig.efw` E35 · `pig.fe0` E39 · `pig.kpl` E43 · `pig.mu0` E41 · `pig.phi` E34 · `pig.rsh0` E42 · `pig.tr` E52 · `pig.trb.acc` E47 · `pig.trb.con` E48 · `pig.trb.rdm` E49 · `pig.trg.acc` E44 · `pig.trg.con` E45 · `pig.trg.rdm` E46 · `pig.trk` E38 · `pig.vpm` E36 · `pig.wsh` E40 · `pigx` E53 · `pnce` E264 · `pni` E428 · `pnq` E256 · `pntx` E259 · `po.n` E141 · `po.on` E140 · `po.sh` E142 · `pof` E143 · `pop` E1080 · `pop.g` E1081 · `PowerRebates` E173 · `PowerSectorPriceChangePassOn` E174 · `PowerSubsidyExemptInclude` E168 · `ppa` E303 · `PPAProportionCoalGas` E204 · `ppcw` E262 · `ppr` E398 · `PrcContPha` E136 · `PrcContPhaBaseline` E139 · `PrcControlPhaseout` E138 · `pret` E411 · `prnew` E442 · `ProdSubPh` E122 · `ProdSubPhaBaseline` E126 · `pros` E150 · `prrns` E444 · `prsub` E440 · `prtx` E439 · `prxc` E441 · `prxl` E443 · `ps` E246 · `psd` E151 · `psegap` E376 · `psegs` E377 · `pser` E380 · `psesh` E378 · `pset` E242 · `pseu` E379 · `psf` E149 · `psi` E148 · `psu` E152 · `pvatn` E263 · `pxcd` E260 · `rate` E296 · `rbe` E1058 · `rbs` E306 · `rcarb` E364 · `rdm.cost` E1238 · `reb` E334 · `rec` E413 · `reg` E109 · `regadj` E107 · `regc` E108 · `rem` E393 · `RenewableCostDeclineRate` E189 · `RenewableSubsidyBL` E209 · `RenewableSubsidyHydro` E213 · `RenSubsidyAddPhaseoutYrs` E211 · `RenSubsidyAddStartYear` E212 · `RenSubsidyAddUSDkwh` E210 · `req` E390 · `reqcg` E391 · `ret` E412 · `rev.chk` E1054 · `rex` E465 · `rexm` E366 · `rexs` E365 · `rfg` E1056 · `rfu` E1055 · `rfu.chk` E1057 · `rgap` E371 · `rmf` E1050 · `rnet` E1052 · `rnew` E463 · `rns` E305 · `rnsp` E304 · `rnvat` E368 · `rp` E362 · `rp.eff` E1245 · `rpct` E1059 · `rpe` E281 · `rpex` E370 · `rpn` E265 · `rpnv` E372 · `rpol` E1061 · `rpol.chk` E1062 · `rppre` E358 · `rpsu` E1051 · `rpsub` E1229 · `rr` E297 · `rreb` E369 · `rsr` E467 · `rsub` E462 · `rtot` E1063 · `rtot.chg` E1064 · `rtot.ref` E1053 · `rtx` E461 · `rvat` E367 · `rvt` E466 · `rxcp` E464 · `sc` E357 · `scat` E294 · `scc` E29 · `scc.cost` E1241 · `ScenarioSelected` E97 · `scl` E375 · `scn` E103 · `scv` E295 · `second` E431 · `sgap` E363 · `ShareOfConsSubPha` E132 · `ShareofConsSubPhaBA` E135 · `ShareofProdSubPha` E125 · `ShareOfProdSubPhaBA` E128 · `shk` E333 · `shock` E319 · `shp` E457 · `shpx` E113 · `shr` E402 · `sp` E247 · `space` E430 · `spe` E383 · `spf` E244 · `spot` E299 · `SPPEffAdjEnergyEfficiencyRegulations` E98 · `SPPEffAdjFeebates` E102 · `SPPEffAdjInd` E101 · `SPPEffAdjRes` E100 · `SPPEffAdjVehicleFuelEconomy` E99 · `ssc` E110 · `start` E293 · `StartingPointWhenLTStorageIsNeeded` E201 · `stm` E301 · `stoav` E322 · `StorageHoursForLTStorage` E203 · `StorageToInterfaceRatioSTStorage` E199 · `sup.cost` E1239 · `supcost` E1225 · `SupplyCostDeltaSubsidy` E169 · `swd` E346 · `swi` E345 · `sys` E348 · `tcf` E308 · `tcp` E1182 · `tgap` E1246 · `tic` E342 · `tot.ext` E1218 · `TotalHoursStorageFor100pcVRE` E198 · `tr.col` E471 · `tr.dk` E470 · `tr.pol` E472 · `tr.sw` E469 · `TrAdvBevBaseCyc` E514 · `TrAdvBevBaseFre` E513 · `TrAdvBevBasePas` E512 · `TrAdvBevPolCyc` E520 · `TrAdvBevPolFre` E519 · `TrAdvBevPolPas` E518 · `tradvcb` E758 · `tradvci` E757 · `tradvfb` E756 · `tradvfi` E755 · `TrAdvIceBaseCyc` E511 · `TrAdvIceBaseFre` E510 · `TrAdvIceBasePas` E509 · `TrAdvIcePolCyc` E517 · `TrAdvIcePolFre` E516 · `TrAdvIcePolPas` E515 · `tradvpb` E754 · `tradvpi` E753 · `TrAdvYearCyc` E523 · `TrAdvYearFre` E522 · `TrAdvYearPas` E521 · `trafe` E1014 · `trafen` E1013 · `trafg` E1011 · `trafo` E1012 · `traftc` E654 · `traftf` E653 · `traftn` E651 · `trafts` E671 · `traftsc` E673 · `traftsf` E672 · `traftu` E652 · `tran.acc.cost` E1202 · `tran.acc.gj` E1205 · `tran.acc.km` E1195 · `tran.cls` E1198 · `tran.con.cost` E1203 · `tran.con.gj` E1206 · `tran.con.km` E1196 · `tran.fsh` E1201 · `tran.mrg` E1200 · `tran.rdm.cost` E1204 · `tran.rdm.gj` E1207 · `tran.rdm.km` E1197 · `tran.rsh` E1023 · `tran.wcl` E1199 · `trancbn` E839 · `trancin` E832 · `tranfbn` E820 · `tranfin` E812 · `tranpbn` E780 · `tranpbu` E800 · `tranpin` E769 · `tranpiu` E793 · `travc` E646 · `travf` E645 · `travn` E643 · `travu` E644 · `trbe` E1027 · `trbea` E1028 · `trbevm` E674 · `trbio` E999 · `trbkm` E948 · `trbkm0` E925 · `trbkm0c` E939 · `trbkm0f` E933 · `trbkmb` E957 · `trbkmbc` E984 · `trbkmbf` E971 · `trbkmc` E976 · `trbkmf` E963 · `trbkmt` E960 · `trbkmtc` E986 · `trbkmtf` E973 · `trbu` E942 · `trbus0` E990 · `trbuse` E989 · `trbusel` E992 · `trbusf` E991 · `trbusp` E988 · `trbuyc` E658 · `trbuyf` E657 · `trbuyn` E655 · `trbuyu` E656 · `trbvu` E599 · `trbyt` E855 · `trbytc` E908 · `trbytf` E890 · `trbytn` E856 · `trbytu` E857 · `trcf2` E996 · `trcf2e` E997 · `trchs` E573 · `trckb2` E954 · `trckb2r` E955 · `trckbc` E727 · `trckbc2` E981 · `trckbc2r` E982 · `trckbf` E726 · `trckbf2` E968 · `trckbf2r` E969 · `trckbp` E724 · `trckbr` E725 · `trckc` E736 · `trckcr` E737 · `trckf` E731 · `trckfr` E732 · `trckm` E720 · `trckr` E721 · `trcks` E921 · `trcksc` E936 · `trckscr` E937 · `trcksf` E930 · `trcksfr` E931 · `trcksr` E922 · `trcloc` E666 · `trclof` E665 · `trclon` E663 · `trclou` E664 · `trco2c` E978 · `trco2f` E965 · `trco2p` E950 · `trcpp` E576 · `trcq` E943 · `trcrs` E878 · `trcrsf` E900 · `trcsc` E676 · `trcss` E675 · `TrCsStartLevel` E532 · `TrCsStartYear` E531 · `TrCsTargetLevel` E534 · `TrCsTargetYear` E533 · `trcuec` E761 · `trcuef` E760 · `trcuep` E759 · `TrCustPolFactor` E530 · `TrCustYearCyc` E526 · `TrCustYearFre` E525 · `TrCustYearPas` E524 · `trcyh` E633 · `trdemf` E888 · `trdemp` E853 · `trdfc` E946 · `trdff` E945 · `trdfp` E944 · `trdisc` E591 · `trdkmcycb` E747 · `trdkmcyci` E746 · `trdkmfreb` E745 · `trdkmfrei` E744 · `trdkmpasb` E741 · `trdkmpasi` E740 · `trdkmpaub` E743 · `trdkmpaui` E742 · `trdmcc` E907 · `trdmcf` E889 · `trdmcp` E854 · `trdpcbn` E838 · `trdpcin` E831 · `trdpfbn` E819 · `trdpfin` E811 · `trdppbn` E779 · `trdppin` E768 · `TrDtStartCyc` E493 · `TrDtStartFre` E492 · `TrDtStartPas` E491 · `TrDtTargetCyc` E499 · `TrDtTargetFre` E498 · `TrDtTargetPas` E497 · `TrDtTargetYearCyc` E496 · `TrDtTargetYearFre` E495 · `TrDtTargetYearPas` E494 · `trdtxc` E719 · `trdtxf` E718 · `trdtxp` E717 · `TrDtYearCyc` E490 · `TrDtYearFre` E489 · `TrDtYearPas` E488 · `trdut` E570 · `trelc` E985 · `trelf` E972 · `trelp` E959 · `trelph` E958 · `trelt` E995 · `trevac` E861 · `trevacc` E912 · `trevaf` E894 · `trevbm` E610 · `trevcc` E869 · `trevo` E569 · `trevom` E602 · `trevp` E568 · `trevpm` E613 · `trevsc` E670 · `trevsf` E669 · `trevsh` E870 · `trevst` E668 · `trfbl` E687 · `trfblc` E711 · `trfblf` E703 · `TrFbPivotChgCyc` E487 · `TrFbPivotChgFre` E486 · `TrFbPivotChgPas` E485 · `TrFbPivotCyc` E484 · `TrFbPivotFre` E483 · `TrFbPivotPas` E482 · `TrFbPivotTypeCyc` E481 · `TrFbPivotTypeFre` E480 · `TrFbPivotTypePas` E479 · `trfbr` E688 · `trfbr5` E689 · `TrFbRateCyc` E478 · `TrFbRateFre` E477 · `TrFbRatePas` E476 · `trfbrc` E712 · `trfbrf` E704 · `trfbtc` E686 · `trfbtf` E685 · `trfbtp` E684 · `trfbvcb` E829 · `trfbvci` E828 · `trfbvfb` E809 · `trfbvfi` E808 · `trfbvpb` E752 · `trfbvpi` E751 · `trfbvub` E791 · `trfbvui` E790 · `TrFbYearCyc` E475 · `TrFbYearFre` E474 · `TrFbYearPas` E473 · `trfcc` E1010 · `trfcec` E1008 · `trfcef` E1007 · `trfcep` E1006 · `trfcf` E1009 · `trfcp` E1005 · `trfe` E565 · `trfeb` E575 · `trfebm` E596 · `trfebn` E951 · `trfebo` E952 · `trfeboc` E979 · `trfebof` E966 · `trfebs` E953 · `trfebsc` E980 · `trfebsf` E967 · `trfem` E593 · `trfem2` E594 · `trfen` E577 · `trfeu` E695 · `trfeub` E697 · `trfew` E681 · `trfewf` E701 · `trfn` E690 · `trfna` E692 · `trfnaf` E706 · `trfnc` E713 · `trfnf` E705 · `trfnp` E691 · `trfsc` E919 · `trfscc` E935 · `trfscf` E929 · `trfscp` E920 · `trfsh` E631 · `trfso` E917 · `trfsoc` E934 · `trfsof` E928 · `trfsop` E918 · `trfu0` E927 · `trfu0c` E940 · `trfu0f` E941 · `trfu0g` E926 · `trfua` E993 · `trfub` E994 · `trfuc` E977 · `trfucbn` E841 · `trfucin` E834 · `trfuf` E964 · `trfufbn` E822 · `trfufin` E814 · `trfup` E949 · `trfupbn` E783 · `trfupbu` E802 · `trfupin` E772 · `trfupiu` E795 · `trgdl` E590 · `trgpc` E589 · `trgpcr` E923 · `trgtf` E887 · `trgtp` E852 · `tricd` E876 · `tricdp` E877 · `tricl` E698 · `triclc` E715 · `triclf` E709 · `triclu` E699 · `tricn` E880 · `tricnf` E902 · `trico` E881 · `tricof` E903 · `tricp` E879 · `tricpf` E901 · `trics` E874 · `tricsf` E898 · `tricw` E882 · `tricwf` E904 · `trimcbn` E840 · `trimcin` E833 · `trimfbn` E821 · `trimfin` E813 · `trimp` E571 · `trimpbn` E782 · `trimpbu` E801 · `trimphv` E786 · `trimpin` E771 · `trimpiu` E794 · `trint` E693 · `trinta` E694 · `trintaf` E708 · `trintc` E714 · `trintc2` E987 · `trintf` E707 · `trintf2` E974 · `trintp` E961 · `trints` E700 · `trintsc` E716 · `trintsf` E710 · `trintu` E696 · `trjc` E632 · `trjhf` E847 · `trjhp` E844 · `trjif` E848 · `trjip` E845 · `trjjf` E849 · `trjjp` E846 · `trkmc` E1003 · `trkmf` E1002 · `trkmp` E1001 · `trkmt` E1004 · `trkt` E998 · `trkte` E1000 · `trlgc` E910 · `trlgcb` E911 · `trlgf` E892 · `trlgfb` E893 · `trlgn` E859 · `trlgnb` E860 · `trlgu` E865 · `trlgub` E866 · `trmku` E678 · `TrModel` E468 · `trnc` E630 · `trnwbn` E872 · `trnwbu` E873 · `trnwc` E915 · `trnwf` E897 · `tropc` E642 · `tropf` E641 · `tropn` E639 · `tropu` E640 · `trown` E566 · `trownb` E611 · `trownc` E625 · `trownce` E626 · `trowne` E612 · `trownf` E618 · `trownfe` E619 · `trowny` E635 · `trp.bfe` E1024 · `trp.bsh` E579 · `trp.bus` E581 · `trp.cap` E547 · `trp.chs` E548 · `trp.dep` E536 · `trp.dsc` E550 · `trp.eb` E559 · `trp.eb2` E562 · `trp.ebb` E560 · `trp.ebc` E561 · `trp.ef` E558 · `trp.efa` E563 · `trp.ela` E554 · `trp.frs` E552 · `trp.gap` E541 · `trp.gj` E556 · `trp.ice` E551 · `trp.inc` E540 · `trp.ins` E537 · `trp.k` E542 · `trp.life` E535 · `trp.lpk` E557 · `trp.mev` E539 · `trp.mic` E538 · `trp.mku` E549 · `trp.mod` E555 · `trp.odc` E545 · `trp.ogr` E544 · `trp.own` E543 · `trp.rn0` E1026 · `trp.rne` E1025 · `trp.tax` E580 · `trp.vkt` E546 · `trp.yrs` E553 · `trpav` E683 · `trpavf` E702 · `trpev` E679 · `trphg` E682 · `trphs` E595 · `trphv` E603 · `trphvs` E609 · `trpkc` E627 · `trpkcbn` E843 · `trpkcin` E836 · `trpkd` E620 · `trpke` E598 · `trpkec` E628 · `trpkef` E621 · `trpkfbn` E824 · `trpkfin` E816 · `trpkg` E597 · `trpkpbn` E785 · `trpkpbu` E804 · `trpkpin` E774 · `trpkpiu` E797 · `trplgc` E662 · `trplgf` E661 · `trplgn` E659 · `trplgu` E660 · `trpop` E588 · `trppbp` E778 · `trppcb` E837 · `trppci` E830 · `trppfb` E818 · `trppfi` E810 · `trpphv` E584 · `trppip` E767 · `trppub` E798 · `trppui` E792 · `trpren` E1029 · `trprg` E583 · `trpri` E585 · `trprl` E582 · `trprm` E587 · `trprn` E586 · `trpvac` E825 · `trpvaf` E805 · `trpvap` E748 · `trpvc` E827 · `trpvf` E807 · `trpvmc` E826 · `trpvmf` E806 · `trpvmp` E749 · `trpvp` E750 · `trq` E1022 · `trra` E680 · `trrafc` E1021 · `trraff` E1020 · `trrafp` E1019 · `trrau` E799 · `trrena` E1030 · `trresb` E788 · `trresgb` E789 · `trresgp` E776 · `trresp` E775 · `trretc` E650 · `trretf` E649 · `trretn` E647 · `trretu` E648 · `trsat` E574 · `trsatf` E885 · `trsatg` E886 · `trsatp` E850 · `trsatq` E851 · `trshc` E913 · `trshcb` E914 · `trshf` E564 · `trshfb` E896 · `trshfi` E895 · `trshn` E862 · `trshnb` E863 · `trshu` E867 · `trshub` E868 · `trsps` E592 · `trsta` E677 · `trstd` E636 · `trstdc` E638 · `trstdf` E637 · `trstt` E667 · `TrSubAmountCyc` E505 · `TrSubAmountFre` E504 · `TrSubAmountPas` E503 · `trsubc` E766 · `TrSubChgCyc` E508 · `TrSubChgFre` E507 · `TrSubChgPas` E506 · `trsubf` E765 · `trsubp` E764 · `TrSubYearCyc` E502 · `TrSubYearFre` E501 · `TrSubYearPas` E500 · `trsum` E1031 · `trsvpbn` E781 · `trsvpin` E770 · `trtcac` E909 · `trtcaf` E891 · `trtcau` E864 · `trtcav` E858 · `trtcf` E777 · `trtcff` E817 · `trtcfp` E787 · `trtcr` E875 · `trtcrf` E899 · `trtocbn` E842 · `trtocin` E835 · `trtofbn` E823 · `trtofin` E815 · `trtopbn` E784 · `trtopbu` E803 · `trtopin` E773 · `trtopiu` E796 · `trtrn` E871 · `trusd` E572 · `trush` E634 · `trvatbc` E763 · `trvatbp` E762 · `TrVatPolFactor` E529 · `TrVatYearCyc` E528 · `TrVatYearPas` E527 · `trveh` E883 · `trvehb` E884 · `trvehc` E916 · `trvehf` E905 · `trvehfb` E906 · `trvht` E1015 · `trvhta` E1018 · `trvhtc` E1017 · `trvhtf` E1016 · `trvk0` E607 · `trvkb` E601 · `trvkbc` E629 · `trvkbf` E622 · `trvkc` E947 · `trvkcb` E956 · `trvkcbc` E983 · `trvkcbf` E970 · `trvkcc` E975 · `trvkcf` E962 · `trvkd` E567 · `trvkf` E605 · `trvkfb` E624 · `trvkfd` E623 · `trvkfr` E614 · `trvkg` E604 · `trvkm` E600 · `trvkn` E722 · `trvkna` E723 · `trvknaf` E734 · `trvknb` E728 · `trvknbf` E735 · `trvkncb` E739 · `trvkncg` E738 · `trvknf` E733 · `trvkp` E606 · `trvkr0` E615 · `trvku` E729 · `trvku0` E924 · `trvku0c` E938 · `trvku0f` E932 · `trvkub` E730 · `trvp` E578 · `trvsf` E617 · `trvsf1` E616 · `trvsh` E608 · `tvc` E335 · `tvcx` E336 · `txe` E374 · `txf` E248 · `txg` E373 · `txo` E249 · `txo.co2e` E1249 · `usdtot` E437 · `UseSpotFuelPricesInEngineerModel` E181 · `vat` E254 · `vat.cost` E1243 · `vatext` E1227 · `vatgen` E1224 · `vbc` E331 · `vcmin` E392 · `vre` E405 · `wac` E286 · `WACCSource` E186 · `WACCUserGlobal` E187 · `wcli` E1209 · `wdg` E1210 · `wel` E1219 · `wel.ffs` E1223 · `wel.rod` E1220 · `wfx` E285 · `wsel` E284 · `xac` E332 · `xck` E330 · `xcp` E452 · `xcpb` E55 · `xcpd` E453 · `xct.c` E119 · `xct.p` E120 · `xets.p` E121 · `xnim` E1167 · `xnim.pct` E1171 · `xpre` E56 · `xr` E5 · `xtb` E1168 · `xtb.pct` E1170 · `xtbp` E1169 · `YearConsSubPha` E130 · `YearPha` E16 · `YearPPACoalGas` E207 · `YearPrcContPha` E137 · `YearProdSubPha` E123 · `YearsToPhaseOutPPAs` E208
