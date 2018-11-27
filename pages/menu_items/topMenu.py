import dash_html_components as html


def serve_menu():
    return(
        html.Div([
            html.A(children="Home page", className="button button-primary", href="/"),
            html.A(children="Data-sets page", className="button button-primary", href="/pages/showDatasetsPage")
            ]))
