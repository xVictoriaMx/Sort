import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
from math import log
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/guess', name="Guess the Algorithms", external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = html.Div([
    html.H1("Sorting Algorithm Big O Graphs", className="text-center"),
    dcc.Graph(
        id='big-o-graph',
        figure={
            'data': [],
            'layout': {}
        }
    ),
    html.Label('Select the Sorting Algorithm:'),
    dcc.Dropdown(
        id='algorithm-dropdown',
        options=[
            {'label': 'Bubble Sort', 'value': 'bubble'},
            {'label': 'Selection Sort', 'value': 'selection'},
            {'label': 'Insertion Sort', 'value': 'insertion'},
            {'label': 'Merge Sort', 'value': 'merge'},
            {'label': 'Quick Sort', 'value': 'quick'}
        ],
        value=None
    ),
    html.Div(id='output')
])

@callback(
    Output('big-o-graph', 'figure'),
    [Input('algorithm-dropdown', 'value')]
)
def update_big_o_graph(selected_algorithm):
    if selected_algorithm is None:
        return {
            'data': [],
            'layout': {}
        }

    if selected_algorithm == 'bubble':
        x = [n for n in range(1, 101)]
        y = [n**2 for n in range(1, 101)]  
    elif selected_algorithm == 'selection':
        x = [n for n in range(1, 101)]
        y = [n**2 for n in range(1, 101)]  
    elif selected_algorithm == 'insertion':
        x = [n for n in range(1, 101)]
        y = [n**2 for n in range(1, 101)]  
    elif selected_algorithm == 'merge':
        x = [n for n in range(1, 101)]
        y = [n * log(n) for n in range(1, 101)]  
    elif selected_algorithm == 'quick':
        x = [n for n in range(1, 101)]
        y = [n * log(n) for n in range(1, 101)]  

    graph_data = go.Scatter(x=x, y=y, mode='lines', name=f'O({selected_algorithm})')
    layout = go.Layout(title=f'Big O Graph for {selected_algorithm} Sort', xaxis=dict(title='Input Size (n)'),
                       yaxis=dict(title='Time Complexity'))
    return {'data': [graph_data], 'layout': layout}
