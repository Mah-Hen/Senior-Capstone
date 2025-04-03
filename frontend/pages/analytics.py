from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash
import pandas as pd
import plotly.express as px
import sys, os
import plotly.graph_objects as go

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from data_processing import FlightDataProcessor


"""
This page will display like general overview of domestic flight data departing from BWI.
In terms of visuals, I'll need to do some research.
"""

# Read the data
processor = FlightDataProcessor()
main_data = processor.get_processed_main_data()
all_options = {
    "Histogram": [
        {
            "label": "Layover Label",
            "value": "Layover_Label",
            "search": "Layovers",
        },
        {
            "label": "Arrival Region",
            "value": "Arrival_Region",
            "search": "Arrival Region",
        },
        {
            "label": "Arrival Time Label",
            "value": "Arrival_Time_Label",
            "search": "Arrival Time",
        },
        {
            "label": "Departure Time Label",
            "value": "Departure_Time_Label",
            "search": "Departure Time",
        },
        {
            "label": "Arrival Season",
            "value": "Arrival_Season",
            "search": "Arrival Season",
        },
        {
            "label": "Departure Season",
            "value": "Departure_Season",
            "search": "Departure Season",
        },
        {
            "label": "Duration Label",
            "value": "Duration_Label",
            "search": "Duration",
        },
        {
            "label": "Seating Class",
            "value": "seating_class",
            "search": "Seating Class",
        },
        {
            "label": "Airline Name",
            "value": "airline_name",
            "search": "Airlines",
        },
    ],
    "Waterfall": [
        {"label": "Airline", "value": "airline_name"},
        {"label": "Seating Class", "value": "seating_class"},
        {"label": "Departure Season", "value": "Departure_Season"},
        {"label": "Arrival Season", "value": "Arrival_Season"},
    ],  # Days Between
    "Area": [
        {"label": "Airline", "value": "airline_name"},
        {"label": "Seating Class", "value": "seating_class"},
        {"label": "Number of Stops", "value": "num_stops"},
        {"label": "Departure Hour", "value": "Departure_Hour"},
    ],
    "Scatter Plot": [{"label": "Airline", "value": "airline_name"}],
    "Line": [{"label": "Airline", "value": "airline_name"}],
}

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
            list(all_options.keys()),
            value="Histogram",
            id="controls-and-dropdown-item-1",
            persistence=True,
            persistence_type="local",
            style={
                "width": "50%",
                "margin": "auto",
                "color": colors["secondary_text"],
            },
        ),
        dcc.Dropdown(
            id="controls-and-dropdown-item-2",
            persistence=True,
            persistence_type="local",
            style={
                "width": "50%",
                "margin": "auto",
                "color": colors["secondary_text"],
            },
        ),
        dcc.Graph(figure={}, id="controls-and-graph"),
    ],
)

# Register page AFTER layout is defined
dash.register_page(__name__, path="/analytics")


@callback(
    Output(component_id="controls-and-dropdown-item-2", component_property="options"),
    Input(component_id="controls-and-dropdown-item-1", component_property="value"),
)
def set_dropdown_values(selected_feature):
    return all_options[selected_feature]  # Return the OG list of option dictionaries


@callback(
    Output(component_id="controls-and-dropdown-item-2", component_property="value"),
    Input(component_id="controls-and-dropdown-item-2", component_property="options"),
)
def set_dropdown_options(available_options):
    if available_options and len(available_options) > 0:
        return available_options[0]["value"]
    return None


# Add controls to build the interaction
@callback(
    Output(component_id="controls-and-graph", component_property="figure"),
    Input(component_id="controls-and-dropdown-item-1", component_property="value"),
    Input(component_id="controls-and-dropdown-item-2", component_property="value"),
)
def update_graph(graph_type, feature_chosen):
    if not feature_chosen:
        return go.Figure()

    if graph_type == "Histogram":
        fig = px.histogram(
            main_data,
            x=feature_chosen,
            y="flight_price",
            color=feature_chosen,
            histfunc="avg",
            title=f"Average Flight Price by {feature_chosen.replace('_', ' ')}",
        )

    elif graph_type == "Waterfall":
        fig = go.Figure(
            go.Waterfall(
                x=main_data[feature_chosen].unique(),
                y=main_data.groupby(feature_chosen)["flight_price"].mean(),
                textposition="outside",
            )
        )

    elif graph_type == "Scatter Plot":
        fig = px.scatter(
            main_data,
            x="Departure_Month",
            y="flight_price",
            color=feature_chosen,
            symbol=feature_chosen,
        )

    elif graph_type == "Line":
        fig = px.line(main_data, x="date", y="GOOG")

    else:
        fig = px.area(
            main_data,
            x="Departure_Season",
            y="flight_price",
            color=feature_chosen,
            line_group=feature_chosen,
        )

        fig.update_layout(
            title=f"Price Distribution by {feature_chosen.replace('_', ' ')}"
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
