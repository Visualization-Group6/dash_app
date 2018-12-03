import dash_core_components as dcc
import dash_html_components as html


def draw(element_id, elements: list):
    return(
        html.Div(
            className='dropdown-menu',
            style={'width': '75%'},
            children=dcc.Dropdown(
                id=element_id,
                options=[{'label': i, 'value': i} for i in elements],
                value=None
            )
        )
    )
