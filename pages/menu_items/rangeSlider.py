import dash_core_components as dcc
import dash_html_components as html


def draw(element_id, start, stop, step, visible=True):
    return (
        html.Div(
            style={'width': '90%', 'height':40} if visible else {'width': '90%', 'height':40, 'visibility': 'hidden'},
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
