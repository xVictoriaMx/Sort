import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import random
import time
import dash_bootstrap_components as dbc


# Sorting algorithms
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
    states = []
    
    def merge_sort_helper(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort_helper(arr[:mid])
        right = merge_sort_helper(arr[mid:])
        
        return merge(left, right)
    
    def merge(left, right):
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        states.append(merged.copy())  
        return merged
    
    merge_sort_helper(arr)
    return states

def quick_sort(arr):
    states = []
    
    def quick_sort_helper(arr, start, end):
        if start < end:
            pivot_index = partition(arr, start, end)
            quick_sort_helper(arr, start, pivot_index - 1)
            quick_sort_helper(arr, pivot_index + 1, end)
    
    def partition(arr, start, end):
        pivot = arr[end]
        i = start - 1
        for j in range(start, end):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[end] = arr[end], arr[i + 1]
        states.append(arr.copy())  
        return i + 1
    
    quick_sort_helper(arr, 0, len(arr) - 1)
    return states

sorting_algorithms = {
    'Bubble Sort': bubble_sort,
    'Selection Sort': selection_sort,
    'Insertion Sort': insertion_sort,
    'Merge Sort': merge_sort,
    'Quick Sort': quick_sort
}

dash.register_page(__name__, path='/compare', name="Compare Algorithms", external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = dbc.Container([
    html.H1("Sorting Algorithm Speed Comparison", className="text-center"),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='algorithm-dropdown1',
                options=[{'label': algo, 'value': algo} for algo in sorting_algorithms.keys()],
                value='Bubble Sort'
            ),
            dcc.Graph(id='comparison-graph1')
        ]),
        html.Br(),
        dbc.Col([
            dcc.Dropdown(
                id='algorithm-dropdown2',
                options=[{'label': algo, 'value': algo} for algo in sorting_algorithms.keys()],
                value='Selection Sort'
            ),
            dcc.Graph(id='comparison-graph2')
        ])
    ]),
    html.Br(),
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

@callback(
    Output('comparison-graph1', 'figure'),
    [Input('algorithm-dropdown1', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_comparison_graph1(algo1, n_intervals):
    if algo1 is None:
        return go.Figure()

    data = random.sample(range(1, 1001), 50)
    states = sorting_algorithms[algo1](data.copy())
    frame_idx = min(n_intervals, len(states) - 1)
    n = len(states[frame_idx])
    fig = go.Figure(go.Bar(x=list(range(1, n + 1)), y=states[frame_idx], marker_color='blue'))
    fig.update_layout(title=f'{algo1}', xaxis=dict(title='Index'), yaxis=dict(title='Value'))

    return fig

@callback(
    Output('comparison-graph2', 'figure'),
    [Input('algorithm-dropdown2', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_comparison_graph2(algo2, n_intervals):
    if algo2 is None:
        return go.Figure()

    data = random.sample(range(1, 1001), 50)
    states = sorting_algorithms[algo2](data.copy())
    frame_idx = min(n_intervals, len(states) - 1)
    n = len(states[frame_idx])
    fig = go.Figure(go.Bar(x=list(range(1, n + 1)), y=states[frame_idx], marker_color='blue'))
    fig.update_layout(title=f'{algo2}', xaxis=dict(title='Index'), yaxis=dict(title='Value'))

    return fig

@callback(
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
