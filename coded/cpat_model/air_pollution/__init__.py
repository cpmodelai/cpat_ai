"""Air-pollution module: placeholder with its interface (D10; spec section 4.5).

Reads from mitigation: section 15 emissions by pollutant and module sector (`aps`), energy use of power and
residential, CO2, GDP, population. Returns: `air.vpm` (value of averted PM2.5) and the concentration coefficients.
`prepare` gives Excel-AI's typed values (tab FromAirPollution: Egypt from the legacy 465 run, 0 elsewhere), which
feed the Pigouvian taxes before the year loop; `step` runs in the year loop and computes nothing until the module is
built.
"""
READS = ['aps', 'ener', 'co2', 'gdp.usd', 'pop']
RETURNS = ['air.vpm', 'air.kappa']


def prepare(state, db, inputs, settings, baseline):
    """Excel-AI's typed values: air.vpm by year; air.kappa by pollutant and module sector."""
    from cpat_model.core.rows import cached
    state.update(cached(state, 'air_pollution', lambda: _typed(db, settings)))


def _typed(db, settings):
    from cpat_model.core.module_values import as_year, keyed_array
    import xarray as xr
    vpm = keyed_array(db, 'air_vpm', settings.countries, 'year')
    kappa = keyed_array(db, 'air_kappa', settings.countries, 'module_sector')
    return {'air.vpm': as_year(vpm['air.vpm']),
            'air.kappa': xr.concat(list(kappa.values()), dim='pollutant').assign_coords(pollutant=list(kappa))}


def step(state, db, inputs, settings, baseline, t):
    """The live module (later). Nothing yet."""
