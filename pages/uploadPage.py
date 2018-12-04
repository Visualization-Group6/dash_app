import dash_html_components as html
import dash_core_components as dcc
from pages.menu_items import dropdownMenu
from scripts import preProcessing
import os


def serve_layout():
    cwd = preProcessing.get_working_dir()
    options = os.listdir(cwd)
    return(
        html.Div(className=None,
                 style={"border-style": 'none none solid none', 'border-color':'#0FA0CE'},
                 children=[
                     html.Iframe(src='http://127.0.0.1:8051/upload', className='upload-window', width='25%'),
                     html.H6("View uploaded dataset:"),
                     dropdownMenu.draw('datasets-dropdown', options, class_name=None, width='25%'),
                     html.A(children="Refresh datasets", className="button button-primary", href="/",
                            style={'width': "25%"}),
                 ])
    )
