import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import time
import random
import dash_bootstrap_components as dbc

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

# Sorting algorithms
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Generate random data for sorting
data = random.sample(range(1, 101), 20)

# Create figures for sorting visualizations and time complexity
figs = [go.Figure() for _ in range(5)]
complexity_figs = [go.Figure() for _ in range(5)]

# Initialize sorting generators for each figure
sort_generators = [selection_sort(data.copy()) for _ in range(5)]

# Layout of the Dash app
app.layout = html.Div([
    navbar,
    html.Br(),
    cards,
    dbc.Row([
        dbc.Col([
            dcc.Graph(id=f'sorting-graph-{i}', figure=figs[i]) for i in range(0, 5, 2)
        ]),
        dbc.Col([
            dcc.Graph(id=f'complexity-graph-{i}', figure=complexity_figs[i]) for i in range(0, 5, 2)
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id=f'sorting-graph-{i}', figure=figs[i]) for i in range(1, 5, 2)
        ]),
        dbc.Col([
            dcc.Graph(id=f'complexity-graph-{i}', figure=complexity_figs[i]) for i in range(1, 5, 2)
        ])
]),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # Update every 1 second
        n_intervals=0
    ),
])

# Update sorting graphs callback
@app.callback(
    [Output(f'sorting-graph-{i}', 'figure') for i in range(5)],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):
    new_data = []
    for i in range(5):
        try:
            new_data.append(next(sort_generators[i]))
        except StopIteration:
            new_data.append(figs[i].data[0].y)
    updated_figs = []
    for i in range(5):
        figs[i].data = []
        figs[i].add_trace(go.Bar(x=list(range(len(new_data[i]))), y=new_data[i], marker_color='blue'))
        updated_figs.append(figs[i])
    return updated_figs

# Update complexity graphs callback
@app.callback(
    [Output(f'complexity-graph-{i}', 'figure') for i in range(5)],
    [Input('interval-component', 'n_intervals')]
)
def update_complexity_graphs(n):
    sizes = list(range(1, 101))
    complexities = [size**2 for size in sizes]  # Quadratic complexity of selection sort
    updated_figs = []
    for i in range(5):
        complexity_figs[i].data = []
        complexity_figs[i].add_trace(go.Scatter(x=sizes, y=complexities, mode='lines', name='O(n^2)'))
        updated_figs.append(complexity_figs[i])
    return updated_figs

if __name__ == '__main__':
    app.run_server(debug=True)
