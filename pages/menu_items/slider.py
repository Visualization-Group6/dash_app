import dash_core_components as dcc
import dash_html_components as html


def draw(element_id, start, stop, step):
    return (
        html.Div(
            style={'width': 150},
            className='slider',
            children=dcc.RangeSlider(
                id=element_id,
                marks={i: str(i) for i in range(start, stop+1, step)},
                min=start,
                max=stop,
                value=[start, stop]
            )
        )
    )
