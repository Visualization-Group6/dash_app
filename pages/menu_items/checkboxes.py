import dash_core_components as dcc
import dash_html_components as html


def draw(element_id, elements: list):
    return(
        html.Div(
            className='checkbox',
            children=dcc.RadioItems(
                id=element_id,
                options=[{'label': i, 'value': i} for i in elements],
                value=elements[0]
            )
        )
    )
