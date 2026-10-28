# Air Pollution Module Equations (Working Specification)

Status: equation inventory transcribed and normalized from the CPAT user documentation. It is not yet the final implementation specification: each applicable equation must be reconciled with CPAT 1.0pre_459 and the coded module before workbook formulas are locked. Keep the legacy source read-only. No source-document ambiguity is resolved silently here.

Source: [`06_Air_pollution.html`](../../coded/cpat_documentation/user/06_Air_pollution.html), sections 6.4-6.7 and 6.10. The numbered equation references below refer to that document.

## 1. Boundary and indices

Indices: country `c`, year `t`, scenario `q` (baseline or policy), AP sector `s`, emissions pollutant/precursor `p`, concentration component `j`, disease `d`, sex `x`, and age group `a`.

The standalone workbook receives Mitigation's scenario emissions through the `aps.<pollutant>.<sector>` code block. It does not recalculate fuel use or emission factors. The upstream relationship is documented as:

$$E_{p,s,t,q} = FuelConsumption_{s,f,t,q} \times EF_{p,s,f,t} \tag{6.1, upstream}$$

The v7.0 Mitigation method note specifies the handoff in kt. In the 1.0pre_459 workbook, the Air Pollution inputs are coded `country.mit.em.<pollutant>.<sector>.<scenario>` and labeled tonnes/year; scenario suffix `.1` is baseline and `.2` is policy. Convert current `aps` kt to legacy tonnes/year explicitly at the module boundary, after verifying the exact annual-rate convention. Preserve both codes, source unit, converted unit, country, and source version in the input section. `E` below denotes emissions after that checked boundary conversion.

All calculations that vary by scenario are performed for both baseline and policy. Policy effects are reported as policy minus baseline or as averted burden (baseline minus policy), matching the output's meaning and the legacy implementation.

## 2. Emissions to ambient concentration

### 2.1 TM5-FASST

Source-receptor coefficients and the linearized concentration response are:

$$A_{i,j}[x,y] = \frac{\Delta C_j(y)}{\Delta E_i(x)}, \qquad \Delta E_i(x)=0.2E_{i,base}(x) \tag{6.2}$$

$$C_j(y) = C_{j,base}(y) + \sum_{x}\sum_i A_{i,j}[x,y]\,[E_i(x)-E_{i,base}(x)]\,UrbanIncFactor \tag{6.3}$$

Country downscaling, where used, is:

$$A_{i,j,country}=A_{i,j,region}\frac{Population_{region}}{Population_{country}} \tag{6.4}$$

The modeled contribution by CPAT sector is:

$$Modeled_{j,t,s}=\sum_i\sum_s A_{i,j}E_{i,s,t} \tag{6.5}$$

For PM2.5, the documented precursors are BC, POM, SO2, NOx, and other PM2.5 (OPM). NH3 is held constant and excluded from the emission perturbation. For O3, the precursors are NOx, NMVOC/VOC, SO2, and CH4. The source applies the urban increment to BC/POM and aggregates precursor contributions as follows:

$$d_{BC}=\Delta_{BC}\,UrbanIncFactor, \quad d_{POM}=\Delta_{POM}\,UrbanIncFactor \tag{6.6-6.7}$$

$$d_{SO4}=\Delta_{SO2\to SO4}+\Delta_{NOx\to SO4}+\Delta_{NH3\to SO4} \tag{6.8}$$

$$d_{NO3}=\Delta_{SO2\to NO3}+\Delta_{NOx\to NO3}+\Delta_{NH3\to NO3} \tag{6.9}$$

$$d_{NH4}=\Delta_{SO2\to NH4}+\Delta_{NOx\to NH4}+\Delta_{NH3\to NH4} \tag{6.10}$$

$$d_{OPM}=\Delta_{OPM\to OPM} \tag{6.11}, \qquad TOTdPM2.5=d_{BC}+d_{POM}+d_{SO4}+d_{NO3}+d_{NH4}+d_{OPM} \tag{6.12}$$

The scenario change is the difference between each scenario's change from FASST baseline. The workbook must use the precise transformation/aggregation in the 459 sheet; the published equations contain inconsistent indices and a POM subscript typo.

### 2.2 Source apportionment with FASST

For each AP sector, adjust its FASST contribution to the external source share:

$$AF_s=\frac{ShareFASST_{s,t_0}}{ShareExternal_s} \tag{6.13}$$

$$ModeledPM2.5_t=\sum_p\sum_s AF_s\,FASST_{p,s}\,E_{p,s,t} \tag{6.14}$$

The source shares can be country-specific, manual, or regional fallback values. The sector map and zero-share handling must match the legacy workbook.

### 2.3 Elastic Net and OLS (PM2.5)

The monthly Elastic Net prediction (6.15) combines an intercept, sector-pollutant emissions, weather covariates, sector and pollutant emission indices, pollutant interactions, sector-weather interactions, month effects, and residual error:

$$PM2.5_m=\alpha+\sum_{s,p}\beta_{s,p}E_{s,p,m}+\sum_{k=1}^{6}\gamma_k X_{k,m}+\sum_s\delta_sT_{s,m}+\sum_p\lambda_pT_{p,m}+\mu T_{NOx,m}T_{NH3,m}+\nu T_{SO2,m}T_{NH3,m}+\xi T_{SO2,m}T_{NOx,m}+\sum_s\theta_sT_{s,m}WS_mWD_m+\phi_m+\epsilon_m \tag{6.15}$$

Annual PM2.5 is the day-weighted monthly average (6.16-6.17), with day weights `varphi_m`; constant weather contribution is:

$$PM2.5=\sum_m varphi_m PM2.5_m \tag{6.16}, \qquad Weather=\sum_{k=1}^{6}\gamma_k\overline{X_k} \tag{6.18}$$

The annual model transformations (6.19-6.26) define adjusted coefficients:

$$\delta'_s=\delta_s\sum_m varphi_mw_{s,m},\quad \lambda'_p=\lambda_p\sum_mvarphi_mw_{p,m}$$

$$\mu'=\mu\sum_mvarphi_mw_{NOx,m}w_{NH3,m},\quad \nu'=\nu\sum_mvarphi_mw_{SO2,m}w_{NH3,m},\quad \xi'=\xi\sum_mvarphi_mw_{SO2,m}w_{NOx,m}$$

$$\theta'_s=\theta_s\sum_mvarphi_mw_{s,m}WS_mWD_m,\quad \beta'_{s,p}=\beta_{s,p}/12,\quad \beta''_{s,p}=\beta'_{s,p}+\lambda'_p \tag{6.19-6.26}$$

The annual total and sector contributions are given by (6.27-6.31):

$$PM2.5=\alpha+Weather+\bar\phi+\sum_{s,p}\beta_{s,p}\bar E_{s,p}+\sum_s\delta'_sT_s+\sum_p\lambda'_pT_p+\mu'T_{NOx}T_{NH3}+\nu'T_{SO2}T_{NH3}+\xi'T_{SO2}T_{NOx}+\sum_s\theta'_sT_s+\epsilon_m \tag{6.27}$$

$$PM2.5_s=\sum_p\beta''_{s,p}T_{p,s}+\delta''_sT_s+\mu'T_{NOx,s}T_{NH3,s}+\nu'T_{SO2,s}T_{NH3,s}+\xi'T_{SO2,s}T_{NOx,s},\quad \delta''_s=\delta'_s+\theta'_s \tag{6.28-6.30}$$

Equation 6.31 allocates the cross-sector pollutant-interaction remainder outside the sector contributions. The companion OLS model (6.32-6.34) distributes modeled PM2.5 across sectors:

$$PM2.5_m=\alpha+\sum_s\delta_s\widehat T_{s,m}+\sum_{k=1}^{6}\gamma_kX_{k,m}+\epsilon_m,\quad \widehat E_{s,p,m}=\frac{E_{s,p,m}-Min_{s,p}}{Max_{s,p}-Min_{s,p}},\quad \widehat T_{s,m}=\sum_p\widehat E_{s,p,m} \tag{6.32-6.34}$$

This option requires the published fitted coefficients, emission indices, and feature definitions; these are data/model parameters, not values to refit in the workbook.

### 2.4 Intake fractions

The intake fraction and corresponding population-weighted concentration change are:

$$iF=\frac{\sum_iP_i\Delta C_iBR}{Q} \tag{6.35}, \qquad \sum_iP_i\Delta C_i=\frac{iF\,Q}{BR} \tag{6.36}$$

Scale secondary-pollutant intake fractions from the documented primary-PM ratios, and scale high-/low-stack sources against ground-level values:

$$iF_{secondary}=\frac{iF_{PM2.5,Apte}}{iF_{PM2.5,Humbert}}iF_{secondary,Humbert} \tag{6.37}, \quad iF_{high/low}=iF_{PM2.5,Fantke}\frac{iF_{PM2.5,Humbert,high/low}}{iF_{PM2.5,Humbert,ground}} \tag{6.38}$$

For power plants, equation 6.39 estimates each plant's intake fraction from population bands and precipitation using the documented regression coefficients. Country averages are generation-weighted. The implied concentration matrix is:

$$CM=\frac{\Delta C[\mu g/m^3]}{1\ [tonne/year]}=\frac{iF\,(ppm)}{BR\,(m^3/day)\,365\,(day/year)\,Population}\,10^6 \tag{6.40}$$

### 2.5 Machine learning, method average, and total ambient concentration

The emissions perturbation is relative to the model's baseline year (2019 in the documentation):

$$P_{s,p,t}=\left(\frac{Emissions_{s,p,t}}{Emissions_{s,p,t_0}}-1\right)100 \tag{6.41}$$

The piecewise response (6.42) uses fitted intercepts `a_k` and slopes `b_k` at the breakpoints `k = -100,-80,...,80,100`:

$$C(P)=\begin{cases}
a_{-100}, & P<-100\\
a_k+b_k(P-k), & k\le P<k+20,\quad k\in\{-100,-80,-60,-40,-20,0,20,40,60,80\}\\
a_{100}+b_{100}(P-100), & P>100
\end{cases} \tag{6.42}$$

The source specifies sector-pollutant baseline contribution and scenario contribution as:

$$C_{s,p,t_0}=-C_{s,p,t}(P_{s,p,t}=-100) \tag{6.43}$$

$$C_{s,p,t}=C_{s,p,t}(P_{s,p,t})-BaselineConcentration+C_{s,p,t_0} \tag{6.44}$$

Subtract the baseline and policy contributions for the policy change. The method uses fitted interval coefficients; do not extrapolate a different response without confirmation. The documented method-average option is the arithmetic mean of intake-fraction and source-apportionment/FASST estimates; verify the exact averaging point and missing-method behavior in 459.

The documented average method is the arithmetic mean of intake fractions and source-apportionment/FASST results. For all methods, calibrate the non-modeled concentration in the base year and hold it constant:

$$C_0=ObservedC_{t_0}-ModeledC_{t_0} \tag{6.45}, \qquad AmbientC_t=ModeledC_t+C_0 \tag{6.46}$$

O3 health concentrations use the TM5-FASST diagonal coefficients or the O3 machine-learning method. O3 concentration units and annual/seasonal metric must be retained explicitly.

## 3. Exposure, health risks, and outcomes

For each risk curve, relative risk is defined in the source as `RR=y0/yc` (6.47). For PM2.5, CPAT uses its GBD 2019 IER/MR-BRT relative-risk table with TMREL 4.15 micrograms per cubic metre. For population shares `p_HAP` exposed to household pollution:

$$RR_{OAP}=MRBRT(Exp_{OAP})/MRBRT(TMREL),\quad RR_{HAP}=MRBRT(Exp_{OAP}+Exp_{HAP})/MRBRT(TMREL) \tag{6.48-6.49}$$

$$RR_{PM}=RR_{OAP}(1-p_{HAP})+RR_{HAP}p_{HAP},\quad PAF_{PM}=1-1/RR_{PM} \tag{6.50-6.51}$$

$$PAF_{OAP}=\frac{Exp_{OAP}}{Exp_{OAP}+p_{HAP}Exp_{HAP}}PAF_{PM},\quad PAF_{HAP}=\frac{p_{HAP}Exp_{HAP}}{Exp_{OAP}+p_{HAP}Exp_{HAP}}PAF_{PM} \tag{6.52-6.53}$$

For cause, sex, age, and year, outcomes are:

$$DALY_{d,x,a,t}=YLL_{d,x,a,t}+YLD_{d,x,a,t} \tag{6.54}$$

$$YLL_{d,x,a,t}=Deaths_{d,x,a,t}L_{x,a},\qquad YLD_{d,x,a,t}=Prevalence_{d,x,a,t}DW_{d,x,a} \tag{6.55-6.56}$$

For O3-related COPD, the source uses:

$$RR_{O3}=e^{\beta\Delta C_{O3}},\qquad PAF_{O3}=1-e^{-\beta\Delta C_{O3}} \tag{6.57-6.58}$$

For multiple risks, combine PAFs multiplicatively. The COPD correction is:

$$PAF_{1..n}=1-\prod_{i=1}^{n}(1-PAF_i) \tag{6.59}$$

$$PAF_{PM2.5,O3,COPD}=1-(1-PAF_{PM2.5})(1-PAF_{O3}) \tag{6.60}$$

$$CorrFactor=\frac{PAF_{PM2.5,O3,COPD}}{PAF_{PM2.5}+PAF_{O3}} \tag{6.61}$$

The source applies this correction when adding PM2.5 and O3 deaths for VSL valuation.

The documented solid-fuel leakage relationships are:

$$ProportionHH_{policy}=ProportionHH_{baseline}(1+Leakage\,F_{prop,HH}) \tag{6.62}$$

$$F_{prop,HH,adjusted}=\left(\frac{MaxPropHH}{ProportionHH_{baseline}}-1\right)\frac{1}{Leakage} \tag{6.63}$$

$$F_{prop,HH}=\begin{cases}F_{prop,HH,adjusted},&ProportionHH_{policy}>MaxPropHH\\ProportionHH_{policy},&otherwise\end{cases} \tag{6.64}$$

The last branch returns the policy proportion where the first returns a leakage factor; reconcile this dimensional inconsistency with the legacy sheet. Post-neonatal mortality uses:

$$Deaths=\left[1-\frac{1}{(1-Incidence)e^{\beta\Delta Q}+Incidence}\right]Incidence\,Population \tag{6.65}$$

For depression, the published PM2.5 relationship is:

$$RR\approx OR_{10}\frac{PM2.5_{current}-PM2.5_{counterfactual}}{10} \tag{6.66}$$

with counterfactual PM2.5 of 25 micrograms per cubic metre. The prior legacy extraction describes a different log-linear implementation; reconcile before coding.

The implementation strategy in appendix 6.10.3 derives a pollution-free incidence rate from baseline mortality and baseline exposure, then calculates scenario mortality change:

$$\lambda_{TMREL}=\frac{M_0}{Population}\frac{1}{p_HRR^0_{HAP}+(1-p_H)RR^0_{OAP}} \tag{6.97-6.101}$$

$$\Delta M=M_0\left[1-\frac{p_H^1RR^1_{HAP}+(1-p_H^1)RR^1_{OAP}}{p_H^0RR^0_{HAP}+(1-p_H^0)RR^0_{OAP}}\right] \tag{6.102}$$

Apply the legacy country, disease, sex, age, urban/rural, and exposed/unexposed incidence conventions after reconciling them with the 459 workbook and coded version. The workbook reports mortality, YLL, YLD, and DALYs separately and in their documented totals.

## 4. Economic effects and unit damages

Working-day losses and fallback wage (6.67-6.69):

$$PAF_{WDL}=1-e^{-\beta\Delta C},\quad WDL=Population_{15-64}\,WDL_{baseline/person}(1-e^{-\beta C_{baseline}}) \tag{6.67-6.68}$$

$$DailyWage=\frac{GDP\,\alpha}{PersonsEmployed}\frac{1}{DaysPerYear} \tag{6.69}$$

Productivity and mortality output loss (6.70-6.77):

$$W_{ij}=\left(\frac{L_{ij}}{N_{ij}}\right)\left(\frac{\alpha Y_i}{L_i}\right),\qquad W_p=\left(\frac{L_p}{N_p}\right)\left(\frac{\alpha Y_p}{L_p}\right)=\frac{\alpha Y_p}{N_p} \tag{6.70-6.71}$$

$$W'_{ij,2017}=\left[\frac{L_{ij}}{N_{ij}}+hp\left(1-\frac{L_{ij}}{N_{ij}}\right)\right]\frac{\alpha Y_i}{L_i} \tag{6.72}$$

$$PV_{ij}=\sum_{a=j}^{84}\pi_{ij,t}\left[\frac{L_{it}}{N_{it}}+hp\left(1-\frac{L_{it}}{N_{it}}\right)\right]\frac{\alpha Y_i}{L_i}\left(\frac{1+g}{1+r}\right)^{t-j} \tag{6.73}$$

Under the CPAT simplifications `hp=0`, constant output per worker, and deaths through age 64 only:

$$PV_j=W\sum_{t=j}^{64}\pi_{j,t}\left(\frac{1+g}{1+r}\right)^{t-j},\quad \frac{PV_j}{W}=\sum_{t=j}^{64}\pi_{j,t}\left(\frac{1+g}{1+r}\right)^{t-j} \tag{6.74-6.75}$$

$$TotalOutputLost=\sum_jPV_jD_j,\qquad M_{ij}=W_{ij}YLD_{ij} \tag{6.76-6.77}$$

For a five-year mortality bucket, the source expands the bucket probability equally across ages and derives survival as:

$$d_{25,29}=d_{25}+d_{26}+d_{27}+d_{28}+d_{29},\quad d_{25}=\cdots=d_{29}=d_{25,29}/5 \tag{6.78-6.79}$$

$$\pi_{25,29}=1-d_{25,29}/5=\pi_{25}=\cdots=\pi_{29} \tag{6.80}$$

Equation 6.81 groups the present-value sum by five-year buckets using `a=(1+g)/(1+r)`. The geometric series equations are printed as:

$$\sum_{k=0}^{n}a^k=\frac{1-a^{n+1}}{1-a} \tag{6.82}$$

$$\sum_{k=m}^{n}a^k=\frac{1-a^{n+1}}{1-a}-\frac{1-a^{m+1}}{1-a} \tag{6.83, as printed}$$

Equation 6.83's second upper bound appears to require review (the standard subtraction would use the sum through `m-1`); do not silently change it.

Health spending attributed to pollution and disease is (6.84-6.85):

$$ShareBoD_{d,c,t}=DALY_{d,c,t}/TotalDALY_{c,t},\qquad HEAP_{c,t}=\sum_dShareBoD_{d,c,t}PAF_{d,t}THE_{c,t}$$

The published VSL transfer and projection equations are:

$$VSL_c=VSL_{OECD,2005}\left(\frac{Y_c}{Y_{OECD,2005}}\right)^b(1+\%\Delta P+\%\Delta Y)^b \tag{6.86}$$

$$VSL_{OECD,t,2011PPP}=VSL_{OECD,2005}\left(\frac{Y_{OECD,t}}{Y_{OECD,2005}}\right)^{0.8}(1+\%\Delta P_{2005,2011})^{0.8} \tag{6.87}$$

$$VSL_{OECD,2014}=VSL_{OECD,2014}\left(\frac{Y_{c,2014}}{Y_{OECD,2014}}\right)^b \tag{6.88, as printed}$$

$$VSL_{c,t}=VSL_{c,2014}\left(\frac{Y_{c,t}}{Y_{c,2014}}\right)^b \tag{6.89}$$

The 2011-dollar-to-results-year deflator conversion follows the prose after 6.89. Equation 6.88 is self-referential as published and must not be implemented literally; use the 459 calculation and selected VSL method.

Morbidity valuation converts YLDs to disease days and values those days at a disability-weight fraction of daily wages (6.93-6.95):

$$M=\sum_dYLD_d\frac{365}{DW_d},\qquad CostDay_d=w\frac{DW_d}{D},\qquad CostMorbidity=\sum_dCostDay_d\,M$$

Fuel externalities are report-only in this version. The documented calculation chain is: baseline ambient deaths per microgram per cubic metre; concentration impact per unit of fuel from emissions factors and the selected concentration method; deaths per ktoe; VSL plus ambient morbidity cost; then convert to dollars per GJ or litre using calorific value and density. The legacy workbook determines the exact scenario/year basis and aggregation.

Equations 6.90-6.92 describe travel time and valuation for the Transport module, not the standalone Air Pollution calculation chain; exclude them unless the 459 sheet establishes an Air Pollution output dependency.

## 5. Radiative forcing and unit conversions

The source provides regional GWP100 coefficients in Table 6.2 for CO, NH3, NOx, BC, OC, SO2, and VOC, but no complete numbered forcing equation. Verify whether the standalone workbook includes forcing and reproduce the 459 calculation and signs; do not infer them from the coefficient table alone.

The appendix conversions are reproduced below as written; each must pass dimensional checks and comparison against 459 before implementation.

$$EF\,[ton/ktoe]=EF\,[kton/PJ]\frac{1\,PJ}{10^6\,GJ}\frac{10^3\,ton}{1\,kton}\frac{41868\,GJ}{1\,ktoe} \tag{6.103}$$

$$1\,ktoe=1\,ktoe\frac{1\,kcal}{10^{-10}\,ktoe}\frac{1}{CalVal\,[kcal/kg]}\frac{1}{Dens\,[ton/m^3]}\frac{1\,ton}{10^3\,kg} \tag{6.104}$$

$$Conv_{ktoe\to m^3}=\frac{10^7}{CalVal\,[kcal/kg]\,Dens\,[ton/m^3]} \tag{6.105, label as printed}$$

$$Conv_{ktoe\to liter}=\frac{10^{10}}{CalVal\,[kcal/kg]\,Dens\,[ton/m^3]} \tag{6.106}$$

$$\frac{1\,kton}{PJ}\frac{1000\,ton}{1\,kton}CalVal\,[PJ/ton]Dens\,[ton/m^3]\frac{1\,m^3}{1000\,L} \tag{6.107}$$

$$\frac{1\,kton}{PJ}\frac{1000\,ton}{1\,kton}CalVal\,[kcal/kg]\frac{1000\,kg}{ton}Dens\,[ton/m^3]\frac{1\,m^3}{1000\,L}\frac{1\,PJ}{2.39\times10^{11}\,kcal} \tag{6.108}$$

$$1\,ktoe\frac{1}{CalVal\,[kcal/kg]}\frac{1\,kcal}{10^{-10}\,ktoe}\frac{1}{Dens\,[ton/m^3]\,1000\,kg/ton\,1\,m^3/1000\,liter} \tag{6.109}$$

The appendix labels 6.105 as a litre conversion despite its prose saying cubic metres; 6.106 is explicitly litres. Keep these distinct until the unit tests and 459 comparison establish the intended factors.

## 6. Reconciliation issues before formulas

| Source item | Issue to resolve against 1.0pre_459 and coded module |
|---|---|
| 6.2-6.5 | Index naming, emissions units, regional/country downscaling, and placement of `UrbanIncFactor` are not fully consistent in the prose/equations. |
| 6.6-6.12 | POM index typo, precursor aggregation, and the treatment of NH3 must match the selected legacy method. |
| 6.13-6.14 | `ShareExternal` zero/missing-data behavior and sector mapping need explicit rules. |
| 6.15-6.34 | Monthly fitted model coefficients/features versus annual workbook implementation; zero ranges in OLS normalization. |
| 6.35-6.40 | Intake-fraction units, source-height classes, and power-plant weights/concentration conversion. |
| 6.41-6.46 | Machine-learning baseline year and piecewise endpoint behavior; constant non-modeled concentration calibration. |
| 6.62-6.66 | Leakage cap output and depression risk expression are ambiguous or inconsistent with the prior legacy extraction notes. |
| 6.86-6.89 | VSL transfer base year, currencies, and the self-referential printed equation 6.88. |
| 6.103-6.109 | Conversion equation labels and dimensional consistency. |
| 6.7.9 | Exact unit-damage baseline/scenario, pollutant/sector/fuel, and monetization aggregation. |
| Radiative forcing | Formula and signs are absent from the equations section; compare against 459 before adding. |

Under the repository rule, a discrepancy is not silently corrected: establish whether it is a legacy bug or issue, fix and register bugs, and reproduce/register issues unless the user approves a departure.

## 7. Implementation decisions

- **First country:** Senegal, matching the 1.0pre_459_NoPropData Dashboard selection.
- **Adult disease incidence:** use the 25+ incidence rates for adult disease populations; independently reassess whether the optional GBD adjustment factor then double-corrects the burden.
- **Household-air-pollution leakage cap:** cap the final share of households using solid fuels at the configured maximum; route residual leakage to the HAP exposure level. Compare both parts with the coded implementation and register the 459 difference.
- **Depression risk:** use the formula verified in 1.0pre_459; document the difference from published Eq. 6.66 and classify it under the repository bug/issue rule.
- **OECD VSL:** repair the legacy `Transfer from OECD` path using verified OECD reference values and explicit year/currency conversions; do not reproduce an `#N/A` result.
- **Python comparison:** use the supplied `cpat_python` module as a secondary cross-check only. Where it differs from 1.0pre_459, preserve the legacy method unless the difference is a confirmed bug or a user-approved departure.
- **Fuel externalities:** report-only; do not feed them back into Mitigation prices in this version.
