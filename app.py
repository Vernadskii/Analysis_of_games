# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output



game_info = pd.read_csv('games.csv')


game_info.dropna(inplace=True)      # Deleted rows which consists at least one null
game_info = game_info.loc[game_info['Year_of_Release'] >= 2000]     # Deleted rows which Year is less than 2000


fig = px.scatter(game_info, x="User_Score", y="Critic_Score", color="Genre", hover_name="Name",
                 log_x=True)

YEARS = pd.unique(game_info['Year_of_Release']).tolist()    # Количество разных лет


def prepare_to_Stacked_area_plot(value):
    """Функция построения Stacked area plot, показывающего выпуск игр по годам и платформам"""
    PLATFORMS = pd.unique(game_info['Platform']).tolist()   # Количество разных платформ
    Stacked_area_plot = go.Figure()
    for platform in PLATFORMS:
        res_years=[]
        amount_games = []
        for year in YEARS:
            if value[0]<=year<=value[1]:
                res_years.append(year)
                amount_games.append(game_info[(game_info.Platform == platform) &
                                          (game_info.Year_of_Release == year)].index.shape[0]) # Количество игр для данной платформы в этом году
        Stacked_area_plot.add_trace(go.Scatter(name=platform,
            x=res_years,
            y=amount_games,
            stackgroup='one'))
    return Stacked_area_plot

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Table(style = {"width":"100%"}, className="responsive-table", children=[
    html.Tr(children=[
        html.H3(
            children='Наименование дашборда', style={'align' : "center"}
        )
    ]),
    html.Tr(children=[
        html.H4(
            children='Описание дашборда (назначение, краткая инструкция по использованию)'
        )
    ]),
    html.Tr(children=[
        html.Th(children=[
            html.Label('Фильтр1: Фильтр жанров (множественный выбор)'),
            dcc.Dropdown(id='filtr1', clearable=True, options=[
                {'label': 'Sports', 'value': 'NYC'},
                {'label': 'Racing', 'value': 'MTL'},
                {'label': 'Platform', 'value': 'SF'},
                {'label': 'Misc', 'value': 'SF'},
                {'label': 'Action', 'value': 'SF'},
                {'label': 'Puzzle', 'value': 'SF'},
                {'label': 'Shooter', 'value': 'SF'},
                {'label': 'Fightling', 'value': 'SF'},
                {'label': 'Simulation', 'value': 'SF'},
                {'label': 'Role-Playing', 'value': 'SF'},
                {'label': 'Adventure', 'value': 'SF'}],
        value=['MTL'],
        multi=True)]),
        html.Th(
            children='Фильтр2: Фильтр рейтингов (множественный выбор)'
        )
    ]),
    html.Tr(children=[
        html.Th(
            children='Интерактивный текст 1: Количество выбранных игр (результат фильтрации)'
        ),
        html.Th()
    ]),
    html.Tr(children=[
        html.Th(dcc.Graph(id='graph0', figure=prepare_to_Stacked_area_plot([2002, 2007]), style = {'display': 'inline-block', 'width': '90vh', 'height':'80vh',
                                                            'align' : "center"})),
        html.Th(dcc.Graph(id='graph1', figure=fig, style = {'width': '90vh', 'height':'80vh',
                                                            'align': 'center'}))
    ]),
    html.Tr(children=[
        html.Th(children=[
            html.Label('Фильтр 3: Интервал годов выпуска'),
            dcc.RangeSlider(
                id='filter3',
                marks={i: '{}'.format(i) for i in range(int(min(YEARS)), int(max(YEARS)+1))},
                min = int(min(YEARS)),
                max = int(max(YEARS)),
                value=[int(min(YEARS))+2, int(min(YEARS))+7]
            )]),
        html.Th(id='output-container-range-slider')
    ])
])

@app.callback(Output('graph0', 'figure'),
              Input('filter3', 'value'))
def update_output(value):
    return prepare_to_Stacked_area_plot(value)



if __name__ == '__main__':
    app.run_server(debug=True)