import dash_html_components as html


def serve_layout():
    return(html.Div(className="container", children=[
        html.H1("Rens heeft een pagina"),
        html.A(children="link", href="www.youtube.com", target="blank")
    ]))
