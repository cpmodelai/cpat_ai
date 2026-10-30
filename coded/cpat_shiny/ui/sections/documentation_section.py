from shiny import ui
from htmltools import Tag

import markdown

from cpat_shiny.ui.labels import DOCUMENTATION
from cpat_shiny.mapping import ALL_DOCUMENTATION

def html_content(md_file: str):
    with open(f"cpat_documentation/user/{md_file}.md", "r", encoding="utf-8") as file:
        md_content = file.read()
    return markdown.markdown(md_content, extensions=['tables'])

def documentation_section(
        documentation_selection: str
        ) -> Tag:
    return ui.div(
        ui.tags.script(
            src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js"
        ),
        ui.tags.style("""
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        """),
        ui.input_selectize(
            id="documentation_selection",
            label=DOCUMENTATION['documentationSelection'],
            choices=ALL_DOCUMENTATION,
            selected=documentation_selection,
            width='50%'
        ),
        ui.output_ui("render_documentation_section"),
    )
