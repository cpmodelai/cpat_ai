# Mitigation module
The following section contains equations used in scope of the CPAT Python mitigation module and describes selected parameters related to this module.

### Notation
| Notation | Variable |
| -------- | -------- |
|\\(t\\)| Year |
|\\(t0\\)| Base year |
|\\(t_{ct}\\)|CT introduction year|
|\\(t_{ets}\\)|ETS introduction year|
|\\(\hat{cp}\\)|Binary value indicating if existing CP applies|
|\\(ps\\)|Producer-side subsidy|
|\\(\phi_{PS}\\)|Phase-out factor for producer-side subsidies|
|\\(\phi_{CS}\\)|Phase-out factor for consumer-side subsidies|
|\\(\phi_{PC}\\)|Phase-out factor for price controls|
|\\(sp\\)|Supply Price|
|\\(fsc\\)|Fixed supply costs|
|\\(H4\\)|Helper for pass-through coefficient in consumer-side subsidy calculation|
|\\(pptc\\)|Coefficient detailing the degree of international price pass-through|
|\\(intp\\)|International Prices|
|\\(vat\\)|VAT payment|
|\\(\hat{txo}\\)| Binary indicator whether to apply externality VAT |
|\\(txo\\)|Excise and other taxes|
|\\(fao\\)|Fixed or Ad valorem taxes|
|\\(cs\\)|Consumer-side subsidy|
|\\(xct\\)|Existing carbon tax rate (Fuel-sector specific)|
|\\(XCT\\)|Existing carbon tax (Nation-wide value)|
|\\(\varphi_{XCT}\\)|Existing carbon tax coverage by sector and fuel|
|\\(xetsp\\)|Existing ETS rate (Fuel-sector specific)|
|\\(XETSP\\)|Existing ETS price|
|\\(\varphi_{XETS}\\)|Existing ETS coverage by sector and fuel|
|\\(nct\\)|New carbon tax rate (Fuel-sector specific)|
|\\(NCT\\)|National price per ton of CO2 under a Carbon tax|
|\\(\varphi_{NCT}\\)|Sector-fuel coverage for the new Carbon tax policy|
|\\(netsp\\)|New ETS permit rate (Fuel-sector specific)|
|\\(NETSP\\)|National price per ton of CO2 under an ETS|
|\\(\varphi_{ETS}\\)|Sector-fuel coverage for the new ETS policy|
|\\(p\\)|Retail price|
|\\(ec\\)|Energy Consumption|
|\\(em\\)|CO2 emissions|
|\\(\Psi\\)|Covid adjustment factor to energy demand|
|\\(dY\\)|GDP growth|
|\\(df\\)|Discount factor|
|\\(af\\)|Adjustment factor|
|\\(\epsilon_Y\\)|(ElasticityIncome) Forward-looking real GDP-elasticity of fuel demand|
|\\(\epsilon_F\\)|(ElasticityOwnPriceEffic) Efficiency price elasticity|
|\\(\epsilon_U\\)|(ElasticityOwnPriceUsage) Elasticity of usage of energy products and services|
|\\(\alpha\\)| Autonomous annual energy efficiency improvement|
|\\(\varphi_{sh}\\)| Shadow price coverage |
|\\(shp\\)| Shadow price rate |

### Equations
#### Producer-side subsidy
$$
ps_t = ps_{t-1} \cdot \phi _{PS t}
$$

#### Supply Price
$$
sp_t = \max \left( fsc + \left( sp_{t-1} - fsc \right) \cdot \frac{intp_t}{intp_{t-1}} + ps_t \cdot (1 - \phi_{PS_t}), \quad 0.01 \right)
$$

#### VAT payment
$$
vat_t = \left( \frac{vat_{t-1}}{sp_{t-1} + txo_{t-1} \cdot \hat{txo}} \right) \cdot \left( sp_{t} + txo_{t} \cdot \hat{txo} \right)
$$

#### Fixed or Ad valorem taxes
<div>
$$
\begin{array}{l}
fao_t =
\begin{cases}
\frac{1}{3} \sum_{i=t_0-2}^{t_0} fao_i, & \text{if taxes are fixed} \\[10pt]
\frac{fao_{t_0}}{sp_{t_0}} \cdot sp_{t-1} \cdot x_t, & \text{if taxes are ad valorem}
\end{cases} \\[10pt]
\text{where:}
\\[10pt]
x_t =
\begin{cases}
\hat{cp}, & \text{if } fao_{t_0} > 0 \land \big(t > t_{ct} \lor t > t_{ets}\big) \\[10pt]
1, & \text{otherwise}
\end{cases}
\end{array}
$$
</div>

#### Consumer-side subsidy
<div>
$$
\begin{array}{l}
cs_t = \min \Bigg( 
\max \bigg( 
H4 \cdot \phi_{CS_t} + 
(pptc - 1) \cdot ( intp_t - intp_{t-1} ) \cdot \phi_{PC_t},
\quad \frac{1}{N} \sum_{i=0}^{N-1} cs_{t-i}
\bigg),
0
\Bigg)
\\[10pt]
\text{where:}
\\[10pt]
N \text{ is the number of years considered, starting from } t_0 \text{ and going back to } t_0 - (N - 1).
\end{array}
$$
</div>


#### Existing carbon tax rate (Fuel-sector specific)
$$
xct_t = XCT_{t} \cdot ef \cdot \varphi_{XCT,t}
$$

#### Existing ETS rate (Fuel-sector specific)
$$
xetsp_t = XETSP_{t} \cdot ef \cdot \varphi_{XETS,t}
$$

#### New carbon tax rate (Fuel-sector specific)
$$
nct_t = NCT_{t} \cdot ef \cdot \varphi_{NCT,t}
$$

#### New ETS permit rate (Fuel-sector specific)
$$
netsp_t = NETSP_{t} \cdot \varphi_{ETS,t}
$$

#### Excise and other taxes
$$
txo_t = fao_{t} + cs_t + xct_t + xetsp_t + nct_t + netsp_t
$$

#### Retail price
$$
p_t = sp_{t} + txo_t + vat_t
$$

#### Energy Consumption
$$
ec_t = ec_{t-1} \cdot \left( 1 + dY_t \right) ^ {\epsilon_Y \cdot df} \cdot \left( 1 + \psi_t \right) \cdot \left( \frac{p_t}{p_{t-1}}\right)^{\epsilon_U} \cdot \left( \frac{\left( \frac{p_t}{p_{t-1}} + \varphi_{sh,t} \cdot shp_t\right) ^{\epsilon_F}}{1 + \alpha + \psi_{t-1}} \right) ^{1 + \epsilon_Y}
$$

#### CO2 emissions
$$
em_t = ec_{t} \cdot ef \cdot af
$$

### Carbon tax trajectory
In the input section user can select carbon tax trajectory applied in the algorithm. The available choices are as follows:
<ul>
<li>Target CT value - positions between starting and ending years are linearly interpolated based on starting and target carbon price values. For years following policy ending year, values equal to carbon price target value are used</li>
<li>Linear projection - positions between policy starting year and last year of simulation are linearly interpolated based on starting and target carbon price values</li>
</ul>

