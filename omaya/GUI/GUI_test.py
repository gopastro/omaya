#!/usr/bin/env python
# coding: utf-8



#general
import numpy as np
import pandas as pd
import matplotlib.pyplot as pl

#dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import plotly.express as px
import plotly.graph_objects as go
import sistest.gui_dummy_funcs as sisdummy

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='OMAYA')
    ]),
    html.Div([
    dcc.RadioItems(id='channel',
        options=[{'label':'Channel 0','value':0},
                {'label':'Channel 1','value':1},
                {'label':'Channel 2','value':2}],
                value='0')

        ]),
    html.Div([
        dcc.RadioItems(id='device',
            options=[{'label':'Device 1','value':1},
                    {'label':'Device 2','value':2},
                    {'label':'Device 3','value':3}],
                    value='3')

        ]),
    html.Div([
        html.Label('V min'),
        dcc.Input(id='Vmin',value=-2,type='number')
        ]),


    html.Div([
        html.Label('V max'),
        dcc.Input(id='Vmax',value=16,type='number')
        ]),

    html.Div([
        html.Label('step'),
        dcc.Input(id='step',value=0.1,type='number')
        ]),

    html.Div([
        html.Label('Vs Gain'),
        dcc.Input(id='Vs_gain',value=2,type='number')
        ]),

    html.Div([
        html.Label('Vs Gain'),
        dcc.Input(id='Is_gain',value=2,type='number')
        ]),

    html.Div([
        dcc.RadioItems(id='plot',
        options=[{'label':'On','value':'True'},
                {label':'Off','value':'False'}],
                value='True')
        ]),


@app.callback(
Output('IV_plot','plot'),
[State('channel','value'),
State('device','value'),
State('Vmin','value'),
State('Vmax','value'),
State('step','value'),
State('Vs_gain','value'),
State('Is_gain','value'),
State('plot','value')
])

if __name__ == '__main__':
app.run_server(debug=True)
