import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

from pages import indexPage, showDatasetsPage, examplePage, rensPage


def serve_menu():
    return(
        html.Div([
            html.A(children="Home page", className="button button-primary", href="/"),
            html.A(children="Data-sets page", className="button button-primary", href="/pages/showDatasetsPage")
            ]))

app.layout = html.Div([
    serve_menu(),
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # This function called when ever a user navigates to a page:
    if pathname == '/pages/showDatasetsPage':
        return showDatasetsPage.serve_layout()
    if pathname == '/':  # The homepage.
        return indexPage.serve_layout()
    if pathname == '/pages/examplePage':
        return examplePage.serve_layout()
    if pathname == '/wemakenhetlink':
        return rensPage.serve_layout()
    else:  # When a user navigates to a page that does not exist.
        return 404


if __name__ == '__main__':
    app.run_server(debug=True)
