from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash
import pandas as pd
import plotly.express as px
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from data_processing import FlightDataProcessor


"""
This page will display like general overview of domestic flight data departing from BWI.
In terms of visuals, I'll need to do some research.
"""

# Read the data
processor = FlightDataProcessor()
main_data = processor.get_processed_main_data()

# Color scheme
colors = {
    "background": "#0A0A0A",
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
}

# Define layout FIRST
layout = html.Div(
    id="analytics-main-div",
    style={"backgroundColor": colors["background"]},
    children=[
        html.H1(
            "Flight Analytics Dashboard",
            style={"textAlign": "center", "color": colors["main_text"]},
        ),
        html.Div(
            children="A dashboard designed to help you plan your next flight.",
            style={"textAlign": "center", "color": colors["secondary_text"]},
        ),
        html.Hr(),
        dcc.Dropdown(
            options=[
                "Layover_Label",
                "Arrival_Region",
                "Departure_Region",
                "Arrival_Time_Label",
                "Departure_Time_Label",
                "Arrival_Season",
                "Departure_Season",
                "Duration_Label",
                "Seating_Class",
                "Airline_Name",
            ],
            value="Arrival_Region",
            id="controls-and-dropdown-item",
            style={
                "width": "50%",
                "margin": "auto",
                "color": colors["secondary_text"],
                # "backgroundColor": colors["white"],
            },
        ),
        dcc.Graph(figure={}, id="controls-and-graph"),
    ],
)

# Register page AFTER layout is defined
dash.register_page(__name__, path="/analytics")


# Add controls to build the interaction
@callback(
    Output(component_id="controls-and-graph", component_property="figure"),
    Input(component_id="controls-and-dropdown-item", component_property="value"),
)
def update_graph(column_chosen):
    fig = px.histogram(
        main_data,
        x=column_chosen,
        y="flight_price",
        color=column_chosen,
        histfunc="avg",
        title=f"Average Flight Price by {column_chosen.replace('_', ' ')}",
    )

    fig.update_layout(
        plot_bgcolor=colors["surface"],
        paper_bgcolor=colors["background"],
        font_color=colors["main_text"],
        margin=dict(t=40, b=40),
        xaxis=dict(gridcolor="#2D2D2D", linecolor="#2D2D2D", title_font=dict(size=14)),
        yaxis=dict(gridcolor="#2D2D2D", linecolor="#2D2D2D", title_font=dict(size=14)),
    )
    return fig
