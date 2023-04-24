""" Module with main logic and frontend """
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import plotly.express as px

import pandas as pd
from pandas import DataFrame

from auxiliary.config import LOG_LEVEL
from auxiliary.stacked_area_plot import fill_stacked_area_plot
from auxiliary.custom_logger import get_app_logger

logger = get_app_logger(level=LOG_LEVEL)

GAME_INFO = pd.read_csv('games.csv')
# Delete rows which consist of at least one null
GAME_INFO.dropna(inplace=True)
# Delete rows which Year is less than 2000
GAME_INFO = GAME_INFO[GAME_INFO['Year_of_Release'] >= 2000]
YEARS = pd.unique(GAME_INFO['Year_of_Release']).tolist()  # list with unique years

result_data: DataFrame = GAME_INFO

app = dash.Dash(__name__, title='Game Industry Analytics',
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = \
    html.Div(children=[

        html.H3(
            children='The state of the gaming industry',
            style={'width': '100%', 'display': 'flex', 'alignItems': 'center',
                   'justifyContent': 'center'}
        ),
        html.H4(
            children='The dashboard is designed to get acquainted with the trends in the gaming'
                     ' IT industry. Two graphs are presented. The first describes the dynamics '
                     'of game releases well. The second is the quality of these products.',
            style={'width': '100%', 'display': 'flex', 'alignItems': 'center',
                   'justifyContent': 'center'}
        ),

        html.Table(style={"width": "100%"}, className="responsive-table", children=[

            html.Tr(
                children=[

                    html.Th(
                        children=[
                            html.Label('Filter1: Genre filter (multiple choice)'),
                            dcc.Dropdown(id='filter1genre', clearable=False,
                                         options=[
                                             {'label': val, 'value': val}
                                             for val in pd.unique(GAME_INFO['Genre']).tolist()
                                         ],
                                         value=['Sports', 'Shooter'],
                                         multi=True)
                        ]
                    ),

                    html.Th(children=[
                        html.Label('Filter2: Rating filter'),
                        dcc.Dropdown(id='filter2rating', clearable=False,
                                     options=[{'label': val, 'value': val}
                                              for val in pd.unique(GAME_INFO['Rating']).tolist()],
                                     value=['E', 'M', 'T'],
                                     multi=True)]
                    )

                ]
            ),

            html.Tr(children=[
                html.Td(dcc.Markdown(
                    id='quantity',
                    style={'width': '100%', 'display': 'flex', 'alignItems': 'center',
                           'justifyContent': 'center'}
                ),
                    colSpan='2'),
            ]),
            html.Tr(children=[
                html.Td(dcc.Graph(id='stacked_area_plot',
                                  # style={'height':'auto', 'width': '100px'}
                                  style={
                                      'height': '50vh',
                                      # 'width': '100%'
                                  }
                                  )
                        ),
                html.Td(dcc.Graph(id='scatter_plot',
                                  style={
                                      # 'width': '100%',
                                      'height': '50vh',
                                      'align': 'center'}
                                  )
                        )
            ])
        ]),
        html.Div(children=[
            html.Label('Filter3: Interval of release years'),
            dcc.RangeSlider(
                id='filter3years',
                marks={i: f'{i}' for i in
                       range(int(min(YEARS)), int(max(YEARS) + 1))},
                min=int(min(YEARS)),
                max=int(max(YEARS)),
                step=1,
                value=[int(min(YEARS)) + 2, int(min(YEARS)) + 7]
            ),
        ])
    ])


@app.callback(Output('stacked_area_plot', 'figure'),
              Output('scatter_plot', 'figure'),
              Output('quantity', 'children'),
              Input('filter1genre', 'value'),
              Input('filter2rating', 'value'),
              Input('filter3years', 'value'))
def update_output(filter1genre: list, filter2rating: list, filter3years: list):
    """ Callback for dash. It tracks 3 input filters """
    logger.info(f"Genres are %s, ratings are %s, years are %s",
                filter1genre, filter2rating, filter3years)

    # Working with year filter
    years_interval = list(range(filter3years[0], filter3years[1] + 1))
    result = GAME_INFO[GAME_INFO['Year_of_Release'].isin(years_interval)]

    # Working with rating filter
    result = result[result['Rating'].isin(filter2rating)]

    # Working with genre filter
    result = result[result['Genre'].isin(filter1genre)]

    return fill_stacked_area_plot(result), \
           px.scatter(result, x="User_Score", y="Critic_Score", color="Genre",
                      hover_name="Name", log_x=True, title='Scatter plot by genre'), \
           ("Number of games: " + str(result.shape[0]))


if __name__ == '__main__':
    app.run_server(debug=True)
