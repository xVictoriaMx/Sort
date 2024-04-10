import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import time
import random
import dash_bootstrap_components as dbc
import copy

cards = dbc.Row([
    dbc.Col(
        dbc.Card([
            html.H4("Guess the Sorting Algorithm"),
        ],
        body=True,
        style={'textAlign':'center', 'color':'white'},
        color='lightblue')),
    dbc.Col(
        dbc.Card([
            html.H4("Compare Algorithms"),
        ],
        body=True,
        style={'textAlign':'center', 'color':'white'},
        color='blue')),
    dbc.Col(
        dbc.Card([
            html.H4("Reset"),
        ],
        body=True,
        style={'textAlign':'center', 'color':'white'},
        color='darkblue')
    ),
])

navbar=dbc.NavbarSimple(
    brand='Sorting Algorithm Visualization',
    color='primary',
    fluid=True
)

app = dash.Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    navbar,
    html.Br(),
    #cards,
    html.Div(children=[
        dcc.Link(page['name'], href=page["relative_path"], className="btn btn-dark m-2 fs-5")\
            for page in dash.page_registry.values()
    ]),
    dash.page_container,
])

if __name__ == '__main__':
    app.run_server(debug=True)
