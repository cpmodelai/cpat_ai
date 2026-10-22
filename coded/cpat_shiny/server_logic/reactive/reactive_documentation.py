from shiny import reactive

from cpat_shiny.mapping import ALL_DOCUMENTATION

documentation_selection = reactive.value(
    next(iter(ALL_DOCUMENTATION))
)

def create_update_documentation_selection(inputs):
    @reactive.effect
    @reactive.event(inputs.documentation_selection)
    def _():
        documentation_selection.set(inputs.documentation_selection())
