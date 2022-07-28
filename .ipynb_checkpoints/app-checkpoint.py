import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table
import datetime
def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None,
                     plot_bgcolor="rgba(12,25,34, 0)",
                     paper_bgcolor="rgba(12,25,34, 0)",)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)

    return fig

config = {'displaylogo': False,
         'modeBarButtonsToAdd':['drawline',
                                'drawopenpath',
                                'drawclosedpath',
                                'drawcircle',
                                'drawrect',
                                'eraseshape'
                               ]}


df=pd.read_csv('crypto.csv')

app = dash.Dash(__name__)
server = app.server
app.title = 'Cryptocurrency Dashboard'
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.P('Cryptocurrency Dashboard',
                       id='title')
            ], className='title-div'),
            html.Div([
                html.P('Select date range between: {} and {}.'.format(datetime.datetime.strptime(df['date'].min(), "%Y-%m-%d").strftime("%d/%m/%Y"), datetime.datetime.strptime(df['date'].max(), "%Y-%m-%d").strftime("%d/%m/%Y")), id='datetext'),
                dcc.DatePickerRange(
                    id='datepicker',
                    min_date_allowed=df['date'].min(),
                    max_date_allowed=df['date'].max(),
                    initial_visible_month=datetime.date(2016, 11, 8),
                    end_date=df['date'].max(),
                    start_date=df['date'].min(),
                    display_format='DD/MM/YYYY',
                    className='datepickercontainer'
                ),
            ], className='date-picker'),
        ],className='top-row'),
        html.Div([
            html.Div([
                html.Div([

                ], className='text_area', id='title-1'),
                html.Div([
                    dcc.Graph(id='main-fig',figure=blank_fig(), config=config)
                ], className='chart_area'),
                html.Div([

                ])
            ],className='main-chart'),
            html.Div([
                html.Div([
                    html.P('Cryptocurrencies in the S&P 500', id='tabletitle')
                ], className='text_area'),
                html.Div([
                    dash_table.DataTable(
                        id='datatable',
                        columns=[{"name": 'Rank', "id": 'rank'},
                                 {"name": 'Symbol', "id": 'symbol'},
                                 {"name": 'Name', "id": 'name'},
                                 {"name": 'Market Cap', "id": 'market cap'},],
                        style_as_list_view=True,
                        style_table={'overflow_y':'auto'},
                        style_cell={
                            'minWidth': 75, 'maxWidth': 75, 'width': 75,
                            'backgroundColor': 'rgba(12,25,34, 0)',
                            'color': 'rgba(0,166,153,1)',
                            'font-weight': 'bold',
                            'textAlign': 'left',
                        },

                        style_header={'backgroundColor': 'rgba(12,25,34, 0)'},

                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto'
                        },
                        style_data_conditional=[
                                        {
                                            'if': {
                                                'filter_query': '{{name}} = {}'.format('Cryptocurrencies'),
                                            },
                                            'backgroundColor': 'rgba(225, 225, 225, 0.11)',
                                        },
                                    ]
                    ),
                ], className='chart_area'),
            ],className='table-box'),
            html.Div([
                html.Div([

                ], className='text_area', id='title-2'),
                html.Div([
                    dcc.Graph( id='btc-fig',figure=blank_fig(), config=config)
                ], className='chart_area'),
            ],className='side1'),
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown1',
                            value='alt cap',
                            options=[{'value': 'alt cap', 'label': 'Altcoin'},
                                     {'value': 'eth cap', 'label': 'ETH'}],
                            clearable= False,
                            searchable= False,
                        ),
                    ],className='dropdown-container'),
                    html.Div([

                    ], className='text_area2', id='title-3'),
                ], className='text_area'),
                html.Div([
                    dcc.Graph(id='cap-fig',figure=blank_fig(), config=config)
                ], className='chart_area'),
            ],className='side2'),
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown2',
                            value='alt share',
                            options=[{'value': 'alt share', 'label': 'Altcoin'},
                                     {'value': 'eth share', 'label': 'ETH'},
                                     {'value': 'btc share', 'label': 'Bitcoin'}],
                            clearable= False,
                            searchable= False,
                        ),
                    ],className='dropdown-container'),
                    html.Div([

                    ], className='text_area2', id='title-4'),
                ], className='text_area'),
                html.Div([
                    dcc.Graph(id='share-fig',figure=blank_fig(), config=config)
                ], className='chart_area'),
            ],className='side3'),
        ], className='content')
    ], className='main'),

])


@app.callback(
    Output('main-fig','figure'),
    [Input('datepicker','start_date'),
     Input('datepicker','end_date'),]
)

def update_graph(start_date, end_date):
    dff=df
    dff['date'] = pd.to_datetime(dff['date'])
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    dff=dff.loc[mask]
    fig=px.area(dff, x='date', y='market cap', log_y=True, hover_data={'date': False}, color_discrete_sequence=['rgba(0,166,153,1)'])
    fig.update_layout(template = 'plotly_dark',
                     plot_bgcolor="rgba(12,25,34, 0)",
                     paper_bgcolor="rgba(12,25,34, 0)",
                     margin=dict(l=0, t=10, r=0, b=0),
                     hovermode='x unified',
                     hoverlabel=dict(bgcolor='rgba(20, 20, 20, 0.7)',
                                     font=dict(color=' #E6E9EE'),
                                     bordercolor='#686868',
                                     namelength=1),
                     yaxis=dict(tickmode = 'linear'))

    fig.update_xaxes(title_text="Date",
                     showspikes=True,
                     spikecolor='black',
                     spikethickness=1,
                     spikemode= 'across',
                     spikedash= 'solid',
                     spikesnap= 'cursor',
                     showgrid=False,)

    fig.update_yaxes(title_text='Market Cap',
                     showspikes=True,
                     spikecolor= 'black',
                     spikethickness=1,
                     spikemode= 'across',
                     spikedash='solid',
                     zeroline=True)
    return fig



@app.callback(
    Output('title-1','children'),
    [Input('datepicker','end_date')]
)

def update_title(end_date):
    cap=round(int(list(df['market cap'][df['date'] == end_date])[0]), 0)
    return html.P('Total Market Cap: ${:,}'.format(cap), id='main-maintext')


@app.callback(
    Output('btc-fig','figure'),
    [Input('datepicker','start_date'),
     Input('datepicker','end_date'),]
)

def update_graph(start_date, end_date):
    dff=df
    dff['date'] = pd.to_datetime(dff['date'])
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    dff=dff.loc[mask]
    fig=px.area(dff, x='date', y='btc cap', log_y=True, hover_data={'date': False}, color_discrete_sequence=['rgba(0,166,153,1)'])
    fig.update_layout(template = 'plotly_dark',
                     plot_bgcolor="rgba(12,25,34, 0)",
                     paper_bgcolor="rgba(12,25,34, 0)",
                     margin=dict(l=0, t=10, r=0, b=0),
                     hovermode='x unified',
                     hoverlabel=dict(bgcolor='rgba(20, 20, 20, 0.7)',
                                     font=dict(color=' #E6E9EE'),
                                     bordercolor='#686868',
                                     namelength=1),
                     yaxis=dict(tickmode = 'linear'))

    fig.update_xaxes(title_text="Date",
                     showspikes=True,
                     spikecolor='black',
                     spikethickness=1,
                     spikemode= 'across',
                     spikedash= 'solid',
                     spikesnap= 'cursor',
                     showgrid=False,)

    fig.update_yaxes(title_text='BTC Market Cap',
                     showspikes=True,
                     spikecolor= 'black',
                     spikethickness=1,
                     spikemode= 'across',
                     spikedash='solid',
                     zeroline=True)
    return fig

@app.callback(
    Output('title-2','children'),
    [Input('datepicker','end_date')]
)

def update_title(end_date):
    cap=round(int(list(df['btc cap'][df['date'] == end_date])[0]), -6)/1000000
    return html.P('Bitcoin Market Cap: ${:,}M'.format(round(cap)), id='text1-text')


@app.callback(
    Output('cap-fig','figure'),
    [Input('datepicker','start_date'),
     Input('datepicker','end_date'),
     Input('dropdown1','value'),]
)

def update_graph(start_date, end_date, value):
    dff=df
    dff['date'] = pd.to_datetime(dff['date'])
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    dff=dff.loc[mask]
    if value == 'alt cap':
        name= 'Altcoin'
    else:
        name= 'ETH'
    fig=px.area(dff, x='date', y=value, log_y=True, hover_data={'date': False}, color_discrete_sequence=['rgba(0,166,153,1)'])
    fig.update_layout(template = 'plotly_dark',
                     plot_bgcolor="rgba(12,25,34, 0)",
                     paper_bgcolor="rgba(12,25,34, 0)",
                     margin=dict(l=0, t=10, r=0, b=0),
                     hovermode='x unified',
                     hoverlabel=dict(bgcolor='rgba(20, 20, 20, 0.7)',
                                     font=dict(color=' #E6E9EE'),
                                     bordercolor='#686868',
                                     namelength=1),
                     yaxis=dict(tickmode = 'linear'))

    fig.update_xaxes(title_text="Date",
                     showspikes=True,
                     spikecolor='black',
                     spikethickness=1,
                     spikemode= 'across',
                     spikedash= 'solid',
                     spikesnap= 'cursor',
                     showgrid=False,)

    fig.update_yaxes(title_text='{} Market Cap'.format(name),
                     showspikes=True,
                     spikecolor= 'black',
                     spikethickness=1,
                     spikemode= 'across',
                     spikedash='solid',
                     zeroline=True)
    return fig

@app.callback(
    Output('title-3','children'),
    [Input('datepicker','end_date'),
     Input('dropdown1','value'),]
)

def update_title(end_date, value):
    cap=round(int(list(df[value][df['date'] == end_date])[0]), -6)/1000000
    return html.P('Market Cap: ${:,}M'.format(round(cap)), id='text2-text')



@app.callback(
    Output('share-fig','figure'),
    [Input('datepicker','start_date'),
     Input('datepicker','end_date'),
     Input('dropdown2','value'),]
)

def update_graph(start_date, end_date, value):
    dff=df
    dff['date'] = pd.to_datetime(dff['date'])
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    dff=dff.loc[mask]
    if value == 'alt share':
        name= 'Altcoin'
    elif value == 'eth share':
        name= 'ETH'
    else:
        name= 'Bitcoin'
    fig=px.area(dff, x='date', y=value, log_y=False, hover_data={'date': False}, color_discrete_sequence=['rgba(0,166,153,1)'])
    fig.update_layout(template = 'plotly_dark',
                     plot_bgcolor="rgba(12,25,34, 0)",
                     paper_bgcolor="rgba(12,25,34, 0)",
                     margin=dict(l=0, t=10, r=0, b=0),
                     hovermode='x unified',
                     hoverlabel=dict(bgcolor='rgba(20, 20, 20, 0.7)',
                                     font=dict(color=' #E6E9EE'),
                                     bordercolor='#686868',
                                     namelength=1),
#                      yaxis=dict(tickmode = 'linear')
                     )

    fig.update_xaxes(title_text="Date",
                     showspikes=True,
                     spikecolor='black',
                     spikethickness=1,
                     spikemode= 'across',
                     spikedash= 'solid',
                     spikesnap= 'cursor',
                     showgrid=False,)

    fig.update_yaxes(title_text='{} Market share'.format(name),
                     showspikes=True,
                     spikecolor= 'black',
                     spikethickness=1,
                     spikemode= 'across',
                     spikedash='solid',
                     zeroline=True)
    return fig

@app.callback(
    Output('title-4','children'),
    [Input('datepicker','end_date'),
     Input('dropdown2','value'),]
)

def update_title(end_date, value):
    share=round(float(list(df[value][df['date'] == end_date])[0]), 2)
    return html.P('Market share: {}%'.format(share), id='text3-text')



@app.callback(
    Output('datatable', 'data'),
    [Input('datepicker', 'end_date')]
)
def update_rows(end_date):
    sp=pd.read_csv('sp.csv')
    sp=sp[sp['date'] == end_date]
    sp=sp[[ 'symbol', 'name', 'market cap']]
    cap=int(df['market cap'][df['date'] == end_date].iloc[0])
    df2 = pd.DataFrame([[ '___', 'Cryptocurrencies', cap]], columns=list(sp.columns), index=['x'])
    sp=sp.append(df2)
    sp=sp.sort_values(by='market cap', ascending=False)
    sp=sp.reset_index(drop=True)
    sp['rank'] = list(range(len(sp)))
    sp['rank'] = sp['rank']+1
    index=sp.index[sp['name']=='Cryptocurrencies'].tolist()[0]
    if index < 3:
        sp=sp.iloc[0:5]
    else:
        sp=sp.iloc[index-2, index+2]

    sp['market cap'] = (sp['market cap']/1000000).astype(int).map('{:,}'.format).astype(str) + 'M'

    return sp.to_dict('records')


if __name__ == "__main__":
    app.run_server(debug=False)
