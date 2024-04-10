import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import random
import time
import dash_bootstrap_components as dbc

def bubble_sort(arr):
    n = len(arr)
    states = [arr.copy()]
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                states.append(arr.copy())
    return states

def selection_sort(arr):
    n = len(arr)
    states = [arr.copy()]
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        states.append(arr.copy())
    return states

def insertion_sort(arr):
    states = [arr.copy()]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        states.append(arr.copy())
    return states

def merge_sort(arr):
    states = [arr.copy()]
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
            states.append(arr.copy())

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            states.append(arr.copy())

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            states.append(arr.copy())
    return states

def quick_sort(arr):
    states = [arr.copy()]
    if len(arr) <= 1:
        return states
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

sorting_algorithms = {
    'Bubble Sort': bubble_sort,
    'Selection Sort': selection_sort,
    'Insertion Sort': insertion_sort,
    'Merge Sort': merge_sort,
    'Quick Sort': quick_sort
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1("Sorting Algorithm Speed Comparison", className="text-center"),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='algorithm-dropdown1',
                options=[{'label': algo, 'value': algo} for algo in sorting_algorithms.keys()],
                value='Bubble Sort'
            ),
            dcc.Graph(id='comparison-graph1')
        ]),
        dbc.Col([
            dcc.Dropdown(
                id='algorithm-dropdown2',
                options=[{'label': algo, 'value': algo} for algo in sorting_algorithms.keys()],
                value='Selection Sort'
            ),
            dcc.Graph(id='comparison-graph2')
        ])
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(id='stopwatch', className="text-center")
        )
    ]),
    dcc.Interval(
        id='interval-component',
        interval=1000,  
        n_intervals=0
    )
], className="mt-5")

@app.callback(
    Output('comparison-graph1', 'figure'),
    [Input('algorithm-dropdown1', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_comparison_graph1(algo1, n_intervals):
    if algo1 is None:
        return go.Figure()

    data = random.sample(range(1, 1001), 50)
    sorted_data = sorting_algorithms[algo1](data.copy())
    frame_idx = min(n_intervals, len(sorted_data) - 1)
    n = len(sorted_data[frame_idx])
    fig = go.Figure(go.Bar(x=list(range(1, n + 1)), y=sorted_data[frame_idx], marker_color='blue'))
    fig.update_layout(title=f'Sorting Algorithm ({algo1})', xaxis=dict(title='Index'), yaxis=dict(title='Value'))

    return fig

@app.callback(
    Output('comparison-graph2', 'figure'),
    [Input('algorithm-dropdown2', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_comparison_graph2(algo2, n_intervals):
    if algo2 is None:
        return go.Figure()

    data = random.sample(range(1, 1001), 50)
    sorted_data = sorting_algorithms[algo2](data.copy())
    frame_idx = min(n_intervals, len(sorted_data) - 1)
    n = len(sorted_data[frame_idx])
    fig = go.Figure(go.Bar(x=list(range(1, n + 1)), y=sorted_data[frame_idx], marker_color='blue'))
    fig.update_layout(title=f'Sorting Algorithm ({algo2})', xaxis=dict(title='Index'), yaxis=dict(title='Value'))

    return fig

@app.callback(
    Output('stopwatch', 'children'),
    [Input('algorithm-dropdown1', 'value'),
     Input('algorithm-dropdown2', 'value')]
)
def update_stopwatch(algo1, algo2):
    if algo1 is None or algo2 is None:
        return html.Div()

    data = random.sample(range(1, 1001), 50)
    start_time = time.time()
    sorting_algorithms[algo1](data.copy())
    end_time_algo1 = time.time()
    sorting_algorithms[algo2](data.copy())
    end_time_algo2 = time.time()
    
    return html.Div(f'{algo1} execution time: {end_time_algo1 - start_time:.2f} seconds, {algo2} execution time: {end_time_algo2 - start_time:.2f} seconds', className="mt-3")

if __name__ == '__main__':
    app.run_server(debug=True)