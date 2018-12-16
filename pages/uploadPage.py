import dash_html_components as html
import dash_core_components as dcc
from pages.menu_items import dropdownMenu
from scripts import preProcessing
import os
from app import app
from dash.dependencies import Input, Output, State


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
                     html.Div(id='infocontainer')
                 ])
    )


@app.callback(
    Output('infocontainer', 'children'),
    [Input('datasets-dropdown', 'value')])
def show_dataset_info(dataset):
    print(dataset)
    if dataset:
        directory = preProcessing.get_working_dir()+dataset
        with open(directory, "r") as f:
            encoded_data = f.read()
            data = [i.strip().split(" ") for i in encoded_data.split('\n') if i != ""]
            time_max = max([int(i[0]) for i in data[1:] if len(i) == 4])
            time_min = min([int(i[0]) for i in data[1:] if len(i) == 4])
        return [html.Section(" ".join(['Time running from', str(time_min), 'to', str(time_max), '.'])),
                html.H6("Data summary:"), html.Div(children=[html.Section(str(i)) for i in data[0:10]])]
    return None