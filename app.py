import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

game_info = pd.read_csv('games.csv')

# Delete rows which consist of at least one null
game_info.dropna(inplace=True)

# Delete rows which Year is less than 2000
game_info = game_info[game_info['Year_of_Release'] >= 2000]

YEARS = pd.unique(game_info['Year_of_Release']).tolist()  # list with unique years

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Table(style={"width": "100%"}, className="responsive-table", children=[

    html.Tr(
        children=[
            html.H3(
                children='The state of the gaming industry', style={'align': "center"}
            )
        ]
    ),

    html.Tr(
        children=[
            html.H4(
                children='The dashboard is designed to get acquainted with the trends in the gaming'
                         ' IT industry. Two graphs are presented. The first describes the dynamics '
                         'of game releases well. The second is the quality of these products.',
            )
        ]
    ),

    html.Tr(
        children=[
            html.Th(
                children=[
                    html.Label('Filter1: Genre filter (multiple choice)'),
                    dcc.Dropdown(id='filter1genre', clearable=False, options=[
                        {'label': 'Sports', 'value': 'Sports'},
                        {'label': 'Racing', 'value': 'Racing'},
                        {'label': 'Platform', 'value': 'Platform'},
                        {'label': 'Misc', 'value': 'Misc'},
                        {'label': 'Action', 'value': 'Action'},
                        {'label': 'Puzzle', 'value': 'Puzzle'},
                        {'label': 'Shooter', 'value': 'Shooter'},
                        {'label': 'Fightling', 'value': 'Fightling'},
                        {'label': 'Simulation', 'value': 'Simulation'},
                        {'label': 'Role-Playing', 'value': 'Role-Playing'},
                        {'label': 'Adventure', 'value': 'Adventure'}
                    ],
                                 value=['Sports', 'Shooter'],
                                 multi=True)
                ]
            ),

            html.Th(children=[
                html.Label('Filter2: Rating filter'),
                dcc.Dropdown(id='filter2rating', clearable=False, options=[
                    {'label': 'E', 'value': 'E'},
                    {'label': 'M', 'value': 'M'},
                    {'label': 'T', 'value': 'T'},
                    {'label': 'E10+', 'value': 'E10+'},
                    {'label': 'AO', 'value': 'AO'},
                    {'label': 'RP', 'value': 'RP'}
                ],
                            value=['E', 'M', 'T'],
                            multi=True)]
            )
        ]
    ),

    html.Tr(children=[
        html.Th(dcc.Markdown(id='quantity')),
        html.Th()
    ]),
    html.Tr(children=[
        html.Th(dcc.Graph(id='graph0',
                          style={'display': 'inline-block', 'width': '90vh', 'height': '80vh',
                                 'align': "center"})),
        html.Th(dcc.Graph(id='graph1', style={'width': '90vh', 'height': '80vh',
                                              'align': 'center'}))
    ]),
    html.Tr(children=[
        html.Th(children=[
            html.Label('Filter3: Interval of release years'),
            dcc.RangeSlider(
                id='filter3years',
                marks={i: '{}'.format(i) for i in range(int(min(YEARS)), int(max(YEARS) + 1))},
                min=int(min(YEARS)),
                max=int(max(YEARS)),
                value=[int(min(YEARS)) + 2, int(min(YEARS)) + 7]
            )]),
        html.Th(id='output-container-range-slider')
    ])
])


''' Filter Handler '''


@app.callback(Output('graph0', 'figure'),
              Output('graph1', 'figure'),
              Output('quantity', 'children'),
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
        filter2rating = pd.unique(game_info['Rating']).tolist()

    # Работаем с фильтром жанров
    if filter1genre:
        res3 = res2[res2.Genre == filter1genre[0]]
        for i in range(1, len(filter1genre)):
            res3 = pd.concat([res2[res2.Genre == filter1genre[i]], res3])
    else:
        res3 = res2
        filter1genre = pd.unique(game_info['Genre']).tolist()

    """The function of constructing a Stacked area plot showing the release of games
     by year and platform"""
    PLATFORMS = pd.unique(res3['Platform']).tolist()  # Number of different platforms
    Stacked_area_plot = go.Figure(layout=go.Layout(
        title=go.layout.Title(
            text="Stacked area plot showing game releases by year and platform")))
    for platform in PLATFORMS:
        res_years = []
        amount_games = []
        for year in YEARS:
            if filter3years[0] <= year <= filter3years[1]:
                res_years.append(year)
                amount_games.append(game_info[(game_info.Platform == platform) &
                                              (game_info.Year_of_Release == year) &
                                              (game_info.Genre.isin(filter1genre)) &
                                              (game_info.Rating.isin(filter2rating))].index.shape[
                                        0])  # Number of games for this platform this year
        Stacked_area_plot.add_trace(go.Scatter(name=platform,
                                               x=res_years,
                                               y=amount_games,
                                               stackgroup='one'))

    quantity_games = res3.shape[0]

    return Stacked_area_plot, px.scatter(res3, x="User_Score", y="Critic_Score", color="Genre",
                                         hover_name="Name",
                                         log_x=True, title='Scatter plot by genre'), \
        ("Number of games: " + str(quantity_games))


if __name__ == '__main__':
    app.run_server(debug=True)
