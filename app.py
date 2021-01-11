# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.express as px

game_info = pd.read_csv('games.csv')

game_info.dropna(inplace=True)      # Deleted rows which consists at least one null
game_info = game_info.loc[game_info['Year_of_Release'] >= 2000]     # Deleted rows which Year is less than 2000
fig = px.scatter(game_info, x="User_Score", y="Critic_Score", color="Genre", hover_name="Name",
                 log_x=True, size_max=40)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Table(className="responsive-table", children=[
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
        html.Th(
            children='Фильтр1: Фильтр жанров (множественный выбор)'
        ),
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
        html.Th(dcc.Graph(id='graph0', figure=fig, style = {'display': 'inline-block', 'width': '90vh', 'height':'80vh',
                                                            'align' : "center"})),
        html.Th(dcc.Graph(id='graph1', figure=fig, style = {'width': '90vh', 'height':'80vh',
                                                            'align': 'center'}))
    ]),
    html.Tr(children=[
        html.Th(children='Фильтр 3: Интервал годов выпуска'),
        html.Th()
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)