from dash import Dash
import dash_html_components as html
import dash_ui as dui
import dash_core_components as dcc

def serve_layout():
    return([html.Div(
        className="row",
        children=[
            html.Div(
                className="two columns",
                children=[
                    html.Div(
                        children=dcc.Graph(
                            id='left-graph-t',
                            className='window',
                            figure={
                                'data': [{
                                    'x': [1, 2, 3],
                                    'y': [3, 1, 2],
                                    'type': 'bar'
                                }],
                                'layout': {
                                    'height': 400,
                                    'margin': {
                                        'l': 0, 'b': 0, 't': 0, 'r': 0
                                    }
                                }
                            }
                        )
                    )
                ]
            ),
            html.Div(
                className="eight columns",
                children=[
                    html.Div(
                        children=dcc.Graph(
                            id='mid-graph-t',
                            className='window',
                            figure={
                                'data': [{
                                    'x': [1, 2, 3],
                                    'y': [3, 1, 2],
                                    'type': 'bar'
                                }],
                                'layout': {
                                    'height': 400,
                                    'margin': {
                                        'l': 0, 'b': 0, 't': 0, 'r': 0
                                    }
                                }
                            }
                        )
                    )
                ]
            ),
            html.Div(
                className="two columns",
                children=html.Div([
                    dcc.Graph(
                        id='right-graph-t',
                        className='window',
                        figure={
                            'data': [{
                                'x': [1, 2, 3],
                                'y': [3, 1, 2],
                                'type': 'bar'
                            }],
                            'layout': {
                                'height': 400,
                                'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                            }
                        }
                    )
                ])
            )
        ]),
          html.Div(
              className="row",
              children=[
                  html.Div(
                      className="two columns",
                      children=[
                          html.Div(
                              children=dcc.Graph(
                                  id='left-graph-b',
                                  className='window',
                                  figure={
                                      'data': [{
                                          'x': [1, 2, 3],
                                          'y': [3, 1, 2],
                                          'type': 'bar'
                                      }],
                                      'layout': {
                                          'height': 200,
                                          'margin': {
                                              'l': 0, 'b': 0, 't': 0, 'r': 0
                                          }
                                      }
                                  }
                              )
                          )
                      ]
                  ),
                  html.Div(
                      className="eight columns",
                      children=[
                          html.Div(
                              children=dcc.Graph(
                                  id='mid-graph-b',
                                  className='window',
                                  figure={
                                      'data': [{
                                          'x': [1, 2, 3],
                                          'y': [3, 1, 2],
                                          'type': 'bar'
                                      }],
                                      'layout': {
                                          'height': 200,
                                          'margin': {
                                              'l': 0, 'b': 0, 't': 0, 'r': 0
                                          }
                                      }
                                  }
                              )
                          )
                      ]
                  ),
                  html.Div(
                      className="two columns",
                      children=html.Div([
                          dcc.Graph(
                              id='right-graph-b',
                              className='window',
                              figure={
                                  'data': [{
                                      'x': [1, 2, 3],
                                      'y': [3, 1, 2],
                                      'type': 'bar'
                                  }],
                                  'layout': {
                                      'height': 200,
                                      'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}
                                  }
                              }
                          )
                      ])
                  )
              ])])

