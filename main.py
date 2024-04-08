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
        yield arr

def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
        yield arr

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
        yield arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

data = random.sample(range(1, 101), 20)
figs = [go.Figure() for _ in range(5)]
complexity_figs = [go.Figure() for _ in range(5)]

SortAlgs = [selection_sort, insertion_sort, bubble_sort, merge_sort, quick_sort]
sort_generators = [iter(sort_alg(data.copy()) )for sort_alg in SortAlgs]

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
            dcc.Graph(id=f'sorting-graph-{i+1}', figure=figs[i+1]) for i in range(0, 4, 2)
        ]),
        dbc.Col([
            dcc.Graph(id=f'complexity-graph-{i+1}', figure=complexity_figs[i+1]) for i in range(0, 4, 2)
        ])
]),
    dcc.Interval(
        id='interval-component',
        interval=1000, 
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
            # Generate the next step of sorting data for the ith sorting algorithm
            generated_data = next(sort_generators[i])
            new_data.append(generated_data)
        except StopIteration:
            # If the sorting is finished, append the last state of the data
            new_data.append(figs[i].data[0].y if figs[i].data else [])
        except Exception as e:
            print(f"Error in sorting algorithm {SortAlgs[i].__name__}: {str(e)}")
    
    updated_figs = []
    for i in range(5):
        fig = copy.deepcopy(figs[i]) 
        fig.data = [] 
        if isinstance(new_data[i], list):
            fig.add_trace(go.Bar(x=list(range(len(new_data[i]))), y=new_data[i], marker_color='blue'))
        
        updated_figs.append(fig)
    
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
