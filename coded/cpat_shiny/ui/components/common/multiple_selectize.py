from shiny import ui

def multiple_selectize(props):
    return (
        ui.div(
            ui.input_selectize(
                **props,
                multiple=True,
                options={"plugins": ["clear_button"]},
                width='100%',
            ),
        ),
    )
# TODO add props verification
# props = {
#     'id': '',
#     'label': '',
#     'choices': {}
# }
