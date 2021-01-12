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

rate_res=0
genre_res=0


def fig():
    return px.scatter(game_info, x="User_Score", y="Critic_Score", color="Genre", hover_name="Name",
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
            dcc.Dropdown(id='filter1genre', clearable=False, options=[
                {'label': 'Спортивные', 'value': 'Sports'},
                {'label': 'Гонки', 'value': 'Racing'},
                {'label': 'Platform', 'value': 'Platform'},
                {'label': 'Misc', 'value': 'Misc'},
                {'label': 'Action', 'value': 'Action'},
                {'label': 'Puzzle', 'value': 'Puzzle'},
                {'label': 'Shooter', 'value': 'Shooter'},
                {'label': 'Fightling', 'value': 'Fightling'},
                {'label': 'Simulation', 'value': 'Simulation'},
                {'label': 'Role-Playing', 'value': 'Role-Playing'},
                {'label': 'Adventure', 'value': 'Adventure'}],
                value=['Sports'],
                multi=True)]
                ),
        html.Th(children=[
            html.Label('Фильтр2: Фильтр рейтингов (множественный выбор)'),
            dcc.Dropdown(id='filter2rating', clearable=False, options=[
                {'label': 'E', 'value': 'E'},
                {'label': 'M', 'value': 'M'},
                {'label': 'T', 'value': 'T'},
                {'label': 'E10+', 'value': 'E10+'},
                {'label': 'AO', 'value': 'AO'},
                {'label': 'RP', 'value': 'RP'}],
                value=['E', 'M', 'T'],
                multi=True)]
        )]
    ),
    html.Tr(children=[
        html.Th(
            children='Интерактивный текст 1: Количество выбранных игр (результат фильтрации)'
        ),
        html.Th()
    ]),
    html.Tr(children=[
        html.Th(dcc.Graph(id='graph0', style = {'display': 'inline-block', 'width': '90vh', 'height':'80vh',
                                                            'align' : "center"})),
        html.Th(dcc.Graph(id='graph1', style = {'width': '90vh', 'height':'80vh',
                                                            'align': 'center'}))
    ]),
    html.Tr(children=[
        html.Th(children=[
            html.Label('Фильтр 3: Интервал годов выпуска'),
            dcc.RangeSlider(
                id='filter3years',
                marks={i: '{}'.format(i) for i in range(int(min(YEARS)), int(max(YEARS)+1))},
                min = int(min(YEARS)),
                max = int(max(YEARS)),
                value=[int(min(YEARS))+2, int(min(YEARS))+7]
            )]),
        html.Th(id='output-container-range-slider')
    ])
])

'''Обработчик фильтров'''
@app.callback(Output('graph0', 'figure'),
              Output('graph1', 'figure'),
              Input('filter1genre', 'value'),
              Input('filter2rating', 'value'),
              Input('filter3years', 'value'))
def update_output(filter1genre, filter2rating, filter3years):
    print(filter1genre, filter2rating, filter3years)

    # Работаем с годовым фильтром
    x = filter3years[0]
    res1 = game_info[game_info.Year_of_Release == x]
    x += 1
    while x <= filter3years[1]:
        res1 = pd.concat([game_info[game_info.Year_of_Release == x], res1])
        x += 1

    # Работаем с фильтром рейтингов
    if filter2rating:
        res2 = res1[res1.Rating == filter2rating[0]]
        for i in range(1, len(filter2rating)):
            res2 = pd.concat([res1[res1.Rating == filter2rating[i]], res2])
    else:
        res2 = res1

    # Работаем с фильтром жанров
    if filter1genre:
        res3 = res2[res2.Genre == filter1genre[0]]
        for i in range(1, len(filter1genre)):
            res3 = pd.concat([res2[res2.Genre == filter1genre[i]], res3])
    else:
        res3 = res2

    """Функция построения Stacked area plot, показывающего выпуск игр по годам и платформам"""
    PLATFORMS = pd.unique(res3['Platform']).tolist()  # Количество разных платформ
    Stacked_area_plot = go.Figure(layout=go.Layout(
        title=go.layout.Title(text="Stacked area plot, показывающий выпуск игр по годам и платформам")))
    for platform in PLATFORMS:
        res_years = []
        amount_games = []
        for year in YEARS:
            if filter3years[0] <= year <= filter3years[1]:
                res_years.append(year)
                amount_games.append(game_info[(game_info.Platform == platform) &
                                              (game_info.Year_of_Release == year) &
                                              (game_info.Genre.isin(filter1genre)) &
                                    (game_info.Rating.isin(filter2rating))].index.shape[0])  # Количество игр для данной платформы в этом году
        Stacked_area_plot.add_trace(go.Scatter(name=platform,
                                               x=res_years,
                                               y=amount_games,
                                               stackgroup='one'))

    return Stacked_area_plot, px.scatter(res3, x="User_Score", y="Critic_Score",color="Genre", hover_name="Name",
                                         log_x=True)






if __name__ == '__main__':
    app.run_server(debug=True)