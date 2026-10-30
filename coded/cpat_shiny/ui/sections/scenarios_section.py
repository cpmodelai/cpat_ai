from shiny import ui

from cpat_shiny.ui.labels import SCENARIOS

scenarios_section = ui.div(
    ui.layout_columns(
        ui.input_file(
            id="load_scenarios",
            label=SCENARIOS["load"],
            accept=[".csv"],
            multiple=False,
            width='100%'
        ),
        ui.div(
            ui.download_button("download_scenarios", SCENARIOS["download"], width='100%'),
            {"style": "margin-top: 32px;"},
        ),
        ui.input_action_button("delete_all_scenarios", SCENARIOS["delete"]),
        ui.input_action_button("run_scenarios_btn", SCENARIOS["run"]),
        col_widths=(6, 6, 6, 6),
        fill=False
    ),
    ui.output_ui("run_scenarios_progress"),
    ui.output_ui("scenarios_cards"),
    # ui.output_text_verbatim("df_scenarios_out"), # uncomment for dev
)
