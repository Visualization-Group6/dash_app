import dash_html_components as html


def serve_menu():
    return(
        html.Div(className='window', children=[
            html.A(children="Upload page", className="button button-primary", href="/"),
            html.A(children="Interactive Dashboard", className="button button-primary", href="/UI")
            ]))
