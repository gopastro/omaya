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
#import sistest.gui_dummy_funcs as sisdummy

def dc_iv_sweep(channel=0, device='3',
                vmin=-2, vmax=16, step=0.1,
                gain_Vs=80, gain_Is=200,
                timeout=0.010, off=None,
                makeplot=True, save=True):
        """
        Function to get the IV sweep with no LO.
        """
        directory = 'dummy_tests'
        if not os.path.exists(directory):
            print("making directory %s" % directory)
            os.makedirs(directory)

        vlist = numpy.arange(vmin, vmax+step, step)
        lisdic = []
        for Vsis in vlist:
            dic = {}
            dic['Vsis'] = Vsis
            Vs = Vsis*1.6 + numpy.random.normal(loc=0, scale=0.05)
            Is = Vs*3e2/45 + numpy.random.normal(loc=0, scale=0.5)
            dic['Vs'] = Vs
            dic['Is'] = Is
            lisdic.append(dic)
        df = pd.DataFrame(lisdic)
        if makeplot:
            figIV, axIV = plt.subplots(1, 1, figsize=(8, 6))
            axIV.plot(df.Vs, df.Is, 'o-', label='SIS%s cold' % device)
            axIV.legend(loc='best')
            axIV.set_xlim(0, 25)
            axIV.set_ylim(-10, 200)
            axIV.grid()
        if save:
            fname = os.path.join(directory, 'sis%s_cold.csv' % device)
            df.to_csv(fname)
            print('Saving DC IV sweep to %s' % fname)
        return df

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
            {'label':'Off','value':'False'}],
            value='True')
    ]),

html.Div([
    dcc.RadioItems(id='save',
    options=[{'label':'On','value':'True'},
            {'label':'Off','value':'False'}],
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
State('plot','value'),
State('save','value')
])

data = dc_iv_sweep(channel, device,
                vmin, vmax, step,
                gain_Vs, gain_Is,
                timeout=0.010, off=None,
                makeplot, save)



if __name__ == '__main__':
    app.run_server(debug=True)
