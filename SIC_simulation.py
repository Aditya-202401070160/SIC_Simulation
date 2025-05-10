import dash
from dash import dcc, html
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from scipy.stats import binom

# Load trading CSV data
df = pd.read_csv("trading_data.csv")
df.columns = df.columns.str.strip()  # Clean column names

# Check if 'Success_Rate' column exists
if "Success_Rate" not in df.columns:
    raise KeyError("Error: 'Success_Rate' column not found in CSV.")

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Trading Success Simulation", style={'textAlign': 'center'}),

    html.Label("Number of Trades (n):"),
    dcc.Slider(id='num_trades', min=5, max=50, step=1, value=10,
               marks={i: str(i) for i in range(5, 51, 5)}),
    
    html.Label("Average Probability of Success (p):"),
    dcc.Slider(id='success_prob', min=0.1, max=1.0, step=0.05, value=df["Success_Rate"].mean(),
               marks={round(i, 2): str(round(i, 2)) for i in np.arange(0.1, 1.05, 0.1)}),
    
    dcc.Graph(id='binomial_graph')
])

# Callback function to update graph dynamically
@app.callback(
    Output('binomial_graph', 'figure'),
    [Input('num_trades', 'value'),
     Input('success_prob', 'value')]
)
def update_graph(n, p):
    trials = 10000  # Number of simulations
    simulated_results = np.random.binomial(n, p, trials)

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=simulated_results,
        nbinsx=n+1,
        histnorm='probability',
        marker=dict(color='blue', line=dict(color='black', width=1))
    ))

    fig.update_layout(
        title="Binomial Trading Success Simulation",
        xaxis_title="Number of Successful Trades",
        yaxis_title="Probability",
        bargap=0.1
    )

    return fig

# Run Dash app
if __name__ == '__main__':
    app.run(debug=True)

