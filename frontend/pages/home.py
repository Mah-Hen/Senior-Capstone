from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from data_processing import FlightDataProcessor

"""
I do not know what to put on this page yet.
I will leave it blank for now.
"""

colors = {
    "background": "#242124",
    "surface": "#1A1A1A",
    "main_text": "#F0F0F0",
    "secondary_text": "#888888",
    "primary_accent": "#00FFE0",
    "secondary_accent": "#FF00FF",
    "tertiary_accent": "#CCFF00",
    "borders": "#4A4A4A",
    "plot_bgcolor": "#121212",
    "paper_bgcolor": "#121212",
    "error_color": "#FF3860",
    "success_color": "#00FF88",
    "white": "#F8F8FF",
    "H1_text": "#F2F3F4",
}

dash.register_page(__name__, path="/")
main_data = FlightDataProcessor()
main_data = main_data.get_processed_main_data()

layout = html.Div(
    children=[
        html.H1(
            "Welcome",
            id="header-H1",
            style={
                "fontSize": "2rem",
                "margin-top": "25px",
                "marginBottom": "1rem",
            },
        ),
        html.Div(
            children=[
                html.P(
                    "The initial notion of MaxyMal were to put the cap on my CS undergrad with a senior capstone project."
                ),
                html.P(
                    "However, it has grown into an interesting project that's consisted of data scraping, data analysis, and data visualization of trends in flight prices."
                ),
                dcc.Graph(
                    id="map-graph",
                    config={
                        "displayModeBar": True,
                        "displaylogo": False,
                        "modeBarButtonsToRemove": [
                            "toImage",
                            "sendDataToCloud",
                            "editInChartStudio",
                            "zoom2d",
                            "select2d",
                            "lasso2d",
                            "autoScale2d",
                            "resetScale2d",
                        ],
                    },
                    figure=px.choropleth(
                        main_data.groupby("Arrival_State")["flight_price"]
                        .mean()
                        .reset_index(),
                        locationmode="USA-states",
                        locations="Arrival_State",  # State abbreviations
                        color="flight_price",
                        scope="usa",
                    ),
                ),
            ],
            id="header-div",
            style={"fontSize": "1rem"},
        ),
    ],
    style={"paddingTop": "45px"},  # Add padding to push content away from the top
)


# Page-specific theme callback
@callback(
    Output("header-H1", "style"),
    Input("theme_id-store", "data"),
    # prevent_initial_call=True,
    # suppress_callback_exceptions=True,
)
def update_header_title(theme):
    if theme != "dark":
        return {
            "color": "#0A0A0A",  # colors["primary_accent"],
            "fontSize": "2rem",
            "marginBottom": "1rem",
        }
    return {
        "color": colors["H1_text"],
        "fontSize": "2rem",
        "marginBottom": "1rem",
    }


@callback(
    Output("header-div", "style"),
    Input("theme_id-store", "data"),
    # prevent_initial_call=True,
    # suppress_callback_exceptions=True,
)
def update_div_title_theme(theme):
    if theme != "dark":
        return {
            "color": "#0A0A0A",  # colors["primary_accent"],
            "fontSize": "1rem",
            "marginBottom": "1rem",
        }
    return {
        "color": colors["H1_text"],
        "fontSize": "1rem",
        "marginBottom": "1rem",
    }


@callback(
    Output("map-graph", "figure"),
    Input("theme_id-store", "data"),
)
def update_map_figure(theme):
    df = main_data.groupby("Arrival_State")["flight_price"].mean().reset_index()

    fig = px.choropleth(
        df,
        locationmode="USA-states",
        locations="Arrival_State",
        color="flight_price",
        scope="usa",
        color_continuous_scale="Blues",
    )

    # Theme-aware background settings
    if theme == "dark":
        bg_color = colors["background"]
        text_color = colors["main_text"]
    else:
        bg_color = "#F8F8FF"
        text_color = "#0A0A0A"

    fig.update_layout(
        geo=dict(bgcolor=bg_color),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(color=text_color),
        margin=dict(l=0, r=0, t=40, b=0),
        title=dict(
            text="Average Flight Price by State",
            x=0.5,
            font=dict(size=20),
        ),
        transition_duration=500,
    )

    return fig
