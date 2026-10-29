"""Transport co-benefits module: placeholder with its interface (D10; spec section 4.5).

Reads from mitigation: section 5b road model (fuel use by class, fuel economy, vehicle-km, road share).
Returns: `tran.acc.km`, `tran.con.km`, `tran.rdm.km` (accident, congestion and road-damage cost per vehicle-km).
`prepare` gives Excel-AI's typed values (tab FromTransportCB); `step` computes nothing until the module is built
(later linked to the road engineer model).
"""
READS = ['trfc', 'trafg', 'trkm']
RETURNS = ['tran.acc.km', 'tran.con.km', 'tran.rdm.km']


def prepare(state, db, inputs, settings, baseline):
    """Excel-AI's typed values: tran.acc.km, tran.con.km, tran.rdm.km by year."""
    from cpat_model.core.module_values import as_year, keyed_array
    for code, arr in keyed_array(db, 'transport_cost_per_km', settings.countries, 'year').items():
        state[code] = as_year(arr)


def step(state, db, inputs, settings, baseline, t):
    """The live module (later). Nothing yet."""
