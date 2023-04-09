# Module for building stacked area chart
import pandas as pd
from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.graph_objects as go

from auxiliary.config import LOG_LEVEL
from auxiliary.custom_logger import get_app_logger

logger = get_app_logger("stacked_area_plot.py", level=LOG_LEVEL)


def __get_stacked_area_plot() -> Figure:
    return go.Figure(layout=go.Layout(
        title=go.layout.Title(text="Stacked area plot showing game releases by year and platform")))


def fill_stacked_area_plot(data: DataFrame) -> Figure:
    """ Return stacked area plot with traces"""
    stacked_area_plot = __get_stacked_area_plot()

    df_platform_games = data.groupby(
        ["Platform", "Year_of_Release"]).size()  # number of games per platform

    for platform in pd.unique(data['Platform']).tolist():
        logger.debug(str(platform) +
                     str(list(df_platform_games[platform].index)) +
                     str(list(df_platform_games[platform].values)))
        stacked_area_plot.add_trace(go.Scatter(
            name=platform, fill='tozeroy', #stackgroup='one',
            x=df_platform_games[platform].index, y=df_platform_games[platform].values)
        )

    return stacked_area_plot
