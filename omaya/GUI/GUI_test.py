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

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='OMAYA'),
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
    html.Br(),
    html.Label('V min'),
        dcc.Input(id='Vmin',value=-2,type='number'),

    html.Br(),
    html.Label('V max'),
        dcc.Input(id='Vmax',value=16,type='number'),

    html.Br(),
    html.Label('step'),
        dcc.Input(id='step',value=0.1,type='number'),

    html.Br(),
    html.Label('Vs Gain'),
        dcc.Input(id='Vs_gain',value=2,type='number'),

    html.Br(),
    html.Label('Vs Gain'),
        dcc.Input(id='Is_gain',value=2,type='number'),

    html.Div([
        dcc.RadioItems(id='plot',
                        options=[{'label':'On','value':'True'},
                                {label':'Off','value':'False'}],
                        value='True')
    ]),


@app.callback(
    Output('IV_plot','plot'),
    [Input('channel','value'),
    Input('device','value'),
    Input('Vmin','value'),
    Input('Vmax','value'),
    Input('step','value'),
    Input('Vs_gain','value'),
    Input('Is_gain','value'),
    Input('plot','value')
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
