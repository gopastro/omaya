#general
import numpy as np
import pandas as pd
import matplotlib as pl

#dash
import dash
import dash_core_components as dcc
# from dash import dcc
import dash_html_components as html
# from dash import html
from dash.dependencies import Input, Output,State
import plotly.express as px
import plotly.graph_objects as go
import base64
import io


app = dash.Dash(__name__)

#df = pd.DataFrame({'upload file':[]})
d_dict = dict({'Unnamed: 0': 'None',
               'Vs':'Sensed Voltage [mV]',
                'Vsis':'Set Voltage [mV]',
                'Is': 'Sensed Current [µA]',
                'T1': 'Temperature 1 [K]',
                'T2': 'Temperature 2 [K]',
                'T3': 'Temperature 3 [K]',
                'T5': 'Temperature 5 [K]',
                'T6': 'Temperature 6 [K]',
                'T7': 'Temperature 7 [K]',
                'Frequency': 'IF Frequency [GHz]',
               'IFPower': 'IF Power [mW]',
                'Power_0': 'Power 0 [mW]',
                'Power_1': 'Power 1 [mW]',
              'upload file': 'upload file'})

app.layout = html.Div([
                    html.Div([
                        dcc.Upload(html.Button('Upload File'),
                                   id='file'),
                        dcc.RadioItems(id='plot-type',
                                       options=[{'label': 'IV curve','value':0},
                                                {'label':'Hot/Cold','value':1}],
                                       value= 0),
                        dcc.Store(id='dataset'),
                        html.Hr(),
                        ]),

                    html.Div([
                        dcc.Dropdown(id='xaxis-column',placeholder="x-axis"),
                        dcc.RadioItems(id='xaxis-type',
                                       options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                       value='Linear',
                                       labelStyle={'display': 'inline-block'}
                        )],
                        style={'width': '48%', 'display': 'inline-block'}),


                    dcc.Graph(id='indicator-graphic'),
                    html.Div([
                        dcc.Dropdown(id='yaxis-column',placeholder="y-axis"),
                        dcc.RadioItems(id='yaxis-type',
                                       options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                       value='Linear',
                                       labelStyle={'display': 'inline-block'})],
                        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
                        ),

                    ])

@app.callback(Output('dataset','data'),
              [Input('file','contents')],
              [State('file','filename'),
               State('file','last_modified'),
               State('plot-type','value')])
def parse_uploads(contents, names, date,plot_type):
    def parse(contents, filename):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        n = skip_rows(plot_type)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')),skiprows=n)
        return df

    def skip_rows(type):
        if plot_type==0:
            n=0
        if plot_type==1:
            n=1
        return n
    # print(contents)
    n = skip_rows(plot_type)
    df = parse(contents, names)
    # return [{'label': i, 'value': i } for i in df.columns]
# def upload_df(file_cont,file_name,plot_type):
    # if plot_type==0:
        # sis,date,year,freq,power,IF,load = file_name.split('_')
        # legend_name = '{:s} {:s}'.format(sis,load)
        # plot_title = '{:s} {:s} {:s} {:s}'.format(date,year,freq,power,IF)
        # df = pd.read_csv(file_name)

    #if plot_type==1:
        # n=1
            # sis,date,year,freq,power,IF,load = file_name.split('_')
            # legend_name = '{:s} {:s} {:s}'.format(sis,IF,load)
            # plot_title = '{:s} {:s} {:s} {:s}'.format(date,year,freq,power)
            # df = pd.read_csv(file_name, skiprows=1)

    # else:
    #         print('Error')
    return df.to_json(date_format='iso',orient='split')


@app.callback(Output('xaxis-column','options'),
             [Input('dataset','data')])
def update_dropdown_x(jsonified_data):
    df = pd.read_json(jsonified_data,orient='split')
    dropdown_list=[{'label': d_dict[key], 'value': key} for key in df.columns]
    return dropdown_list


@app.callback(Output('yaxis-column','options'),
             [Input('dataset','data')])
def update_dropdown_y(jsonified_data):
    df = pd.read_json(jsonified_data,orient='split')
    dropdown_list=[{'label': d_dict[key], 'value': key} for key in df.columns]
    return dropdown_list


@app.callback(Output('xaxis-column','value'),
             [Input('xaxis-column','options')])
def set_xaxis_value(xaxis_options):
    return xaxis_options[0]['value']


@app.callback(Output('yaxis-column','value'),
             [Input('yaxis-column','options')])
def set_yaxis_value(yaxis_options):
    return yaxis_options[0]['value']


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('dataset','data'),
     Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value')])

def update_graph(jsonified_data,xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type):
    df = pd.read_json(jsonified_data,orient='split')

    fig = px.line(x=df[xaxis_column_name], y=df[yaxis_column_name],
                 #title=plot_title,
                  markers=True)
        #fig = go.Figure(data=go.Scatter(x=df[xaxis_column_name],
                                        #y=df[yaxis_column_name]))

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                         type='linear' if yaxis_type == 'Linear' else 'log')
    fig.update_traces(marker=dict(size=8),mode='lines+markers')
    # name=legend_name)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
