# GDP and international prices
This section outlines calculations performed to obtain GDP relative to base year monetary values and international prices of fossil fuels.

### GDP relative to base year monetary values
| Notation | Variable |
| -------- | -------- |
|\\(t\\)| Year |
|\\(t0\\)| Base year |
|\\(tm\\)| Last available year for GDP data |
|\\(Y\\)| GDP factor |
|\\(dY\\)| GDP growth |

The first step after loading and filtering the data according to the country selection is adjustment of GDP monetary values to be relative to the base year:

<div>
$$
\begin{array}{l}
Y_t =
\begin{cases}
\frac{Y_t}{Y_{t0}}, & \text{if } t \leqslant tm \\[10pt]
Y_{t-1} \cdot Y_{grow}, & \text{if } t > tm
\end{cases} \\[10pt]
\text{where:}
\\[10pt]
Y_{grow} = Y_{tm} - Y_{tm - 1}
\end{array}
$$
</div>


Temporarily scenario specific post policy GDP growth is obtained as follows:
$$
dY_t = \frac{Y_t}{Y_{t-1}}
$$

In order to receive accurate values for GDP growth, calculations of revenues and revenue recycling are required.
### International prices of fossil fuels
| Notation | Variable |
| -------- | -------- |
|\\(t\\)| Year |
|\\(t0\\)| Base year |
|\\(intp\\)| International Prices |
|\\(cf\\)| Conversion factor |
|\\(H4\\)| Helper for pass-through coefficient in consumer-side subsidy calculation |
|\\(cs\\)| Consumer-side subsidy |
|\\(pptc\\)| Coefficient detailing the degree of international price pass-through |

For the following fuels: \\(\text{oop, coa, nga}\\), international prices are adjusted by a fuel specific conversion factor:
$$
intp_{f} = \frac{intp_{f}}{cf_{f}}, \quad \text{where } f \in \text{\{oop, coa, nga\}}
$$

Helper parameter \\(H4\\), further used in consumer-side subsidy calculation, is obtained as follows:
<div>
$$
\begin{array}{l}
H4 =
\begin{cases}
0, & \text{if } cs_{t0} = 0\\[10pt]
\min \bigg(
cs_{t0} - pptc \cdot intp_{t0} - intp_{t0 -1},
0
\bigg), & \text{otherwise}
\end{cases} \\[10pt]
\end{array}
$$
</div>

