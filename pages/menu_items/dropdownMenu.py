import dash_core_components as dcc
import dash_html_components as html


def draw(element_id, elements: list, class_name='dropdown-menu', width='75%', default=None, disabled=False):
    return(
        html.Div(
            className=class_name,
            style={'width': width},
            children=dcc.Dropdown(
                id=element_id,
                options=[{'label': i, 'value': i} for i in elements],
                value=default,
                disabled=disabled
            )
        )
    )
