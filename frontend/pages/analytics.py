from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash
import dash_bootstrap_components as dbc
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
min_price = main_data["flight_price"].min()
q1_price = main_data["flight_price"].quantile(0.25)
q2_price = main_data["flight_price"].quantile(0.5)
q3_price = main_data["flight_price"].quantile(0.75)
max_price = main_data["flight_price"].max()

chart_options = {
    "Histogram": [
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
    "Scat Plot": [
        {"label": "Airline", "value": "airline_name"},
        {"label": "Arrival Region", "value": "Arrival_Region"},
        {"label": "Departure Time", "value": "Departure_Time_Label"},
        {"label": "Arrival Time", "value": "Arrival_Time_Label"},
        {"label": "Departure Season", "value": "Departure_Season"},
        {"label": "Arrival Season", "value": "Arrival_Season"},
        {"label": "Seating Class", "value": "seating_class"},
        {"label": "# of Stops", "value": "num_stops"},
    ],
    "Line": [
        {"label": "Duration Hour", "value": "Duration_Hour"},
        {"label": "Days Between", "value": "Days_Between"},
        {"label": "Departure Hour", "value": "Departure_Hour"},
        {"label": "Arrival Hour", "value": "Arrival_Hour"},
        {"label": "Departure Month", "value": "Departure_Month"},
        {"label": "Search Month", "value": "Search_Month"},
        {"label": "Arrival Month", "value": "Arrival_Month"},
        {"label": "# of Stops", "value": "num_stops"},
    ],
}

# Color scheme
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


def createFilterSidebar(*dropdown_components):
    return dbc.Col(
        dbc.Card(
            [
                # Header with title and divider
                html.Div(
                    [
                        html.H4(
                            "FILTERS",
                            style={
                                "color": "#2D2D2D",
                                "fontWeight": "600",
                                "marginBottom": "0.5rem",
                            },
                        ),
                        html.Hr(
                            style={
                                "borderTop": "2px solid #E1E1E1",
                                "marginTop": "0",
                                "marginBottom": "1.5rem",
                            }
                        ),
                    ]
                ),
                # Dropdown components passed to the function
                *dropdown_components,
                html.Div(style={"height": "200px"}),
            ],
            style={
                "backgroundColor": "#F5F5F5",  # Cool gray background
                "borderRadius": "10px",
                "padding": "1.5rem",
                "boxShadow": "0 4px 6px rgba(0,0,0,0.1)",
            },
        ),
        width=6,  # Adjust width as needed (1-12)
        style={"paddingRight": "0"},  # Remove right padding for tight layout
    )


# Create the dropdown components
chart_dropdown = dcc.Dropdown(
    id="controls-and-dropdown-item-1",
    options=list(chart_options.keys()),
    value="Histogram",
    multi=False,
    placeholder="Select a chart type",
    style={
        "width": "90%",  # Adjust width to fit within the card
        "margin": "10px auto",  # Add spacing between dropdowns
        "backgroundColor": colors["white"],
        "color": colors["secondary_text"],
        "border": f"1px solid {colors['borders']}",
        "borderRadius": "5px",
    },
    persistence=True,
    persistence_type="local",
)
feature_dropdown = dcc.Dropdown(
    id="controls-and-dropdown-item-2",
    persistence=True,
    persistence_type="local",
    placeholder="Select a feature type",
    style={
        "width": "90%",  # Adjust width to fit within the card
        "margin": "10px auto",  # Add spacing between dropdowns
        "color": colors["secondary_text"],
        "backgroundColor": colors["white"],
        "border": f"1px solid {colors['borders']}",
        "borderRadius": "5px",
    },
)
"""
price_dropdown = dcc.Dropdown(
    id="controls-and-dropdown-item-3",
    options=[
        [
            {
                "label": f"${min_price}-${q1_price}",
                "value": f"${min_price}-${q1_price}",
            },
            {"label": f"${q1_price}-${q2_price}", "value": f"${q1_price}-${q2_price}"},
            {"label": f"${q2_price}-${q3_price}", "value": f"${q2_price}-${q3_price}"},
            {
                "label": f"${q3_price}-${max_price}",
                "value": f"${q3_price}-${max_price}",
            },
        ],
    ],
    placeholder="Price Range",
    stlye={
        "width": "50%",
        "margin": "auto",
        "color": colors["secondary_text"],
        "backgroundColor": colors["white"],
        "border": f"1px solid {colors['borders']}",
        "borderRadius": "5px",
    },
)
"""
# Create the graph component
graph = dcc.Graph(
    id="controls-and-graph",
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
    figure={},
)

# Create the sidebar with dropdowns
sidebar = createFilterSidebar(chart_dropdown, feature_dropdown)

# Define layout FIRST
layout = html.Div(
    id="analytics-main-div",
    style={"backgroundColor": colors["white"], "padding": "20px"},
    children=[
        dbc.Row(
            dbc.Col(
                [
                    html.H1(
                        "Flight Analytics Dashboard",
                        id="fad-header",
                        style={
                            "textAlign": "center",
                            "color": colors["main_text"],
                            "marginTop": "20px",
                            "marginBottom": "10px",
                        },
                    ),
                    html.Div(
                        children="A dashboard designed to help you plan your next flight.",
                        id="div-subheader",
                        style={
                            "textAlign": "center",
                            "color": colors["secondary_text"],
                            "marginBottom": "20px",
                        },
                    ),
                ]
            )
        ),
        dbc.Row(
            [
                dbc.Col(sidebar, style={"paddingRight": "2px"}),
                dbc.Col(graph, style={"paddingLeft": "0px"}),  # Adjusted paddingLeft
            ],
            style={"marginTop": "20px"},
        ),
    ],
)

# Register page AFTER layout is defined
dash.register_page(__name__, path="/analytics")


@callback(
    Output("analytics-main-div", "style"),  # (classname, according argument)
    Input("theme_id-store", "data"),
)
def toggle_theme(theme):
    if theme == "dark":
        return {
            "background": colors["background"],  # colors["background"],
            "padding": "20px",
            "textAlign": "center",
        }
    return {
        "background": colors["white"],
        "padding": "20px",
        "textAlign": "center",
    }


# Page-specific theme callback
@callback(
    Output("fad-header", "style"),
    Input("theme_id-store", "data"),
    # prevent_initial_call=True,
    # suppress_callback_exceptions=True,
)
def update_header_title(theme):
    if theme != "dark":
        return {
            "textAlign": "center",
            "color": "#0A0A0A",
            "fontSize": "2.5rem",
            "marginTop": "20px",
            "marginBottom": "10px",
        }
    return {
        "textAlign": "center",
        "color": colors["white"],
        "fontSize": "2.5rem",
        "marginTop": "20px",
        "marginBottom": "10px",
    }


@callback(
    Output("div-subheader", "style"),
    Input("theme_id-store", "data"),
)
def update_subheader_title(theme):
    if theme != "dark":
        return {
            "textAlign": "center",
            "color": "#0A0A0A",
            "marginBottom": "20px",
        }
    return {
        "textAlign": "center",
        "color": colors["secondary_text"],
        "marginBottom": "20px",
    }


@callback(
    Output(component_id="controls-and-dropdown-item-2", component_property="options"),
    Input(component_id="controls-and-dropdown-item-1", component_property="value"),
    suppress_callback_exceptions=True,
)
def set_dropdown_values(selected_feature):
    try:
        return chart_options[
            selected_feature
        ]  # Return the OG list of option dictionaries
    except KeyError:
        return []


@callback(
    Output(component_id="controls-and-dropdown-item-2", component_property="value"),
    Input(component_id="controls-and-dropdown-item-2", component_property="options"),
    suppress_callback_exceptions=True,
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
    suppress_callback_exceptions=True,
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
            pattern_shape="Layover_Label",
        )

    elif graph_type == "Waterfall":
        fig = go.Figure(
            go.Waterfall(
                x=main_data[feature_chosen].unique(),
                y=main_data.groupby(feature_chosen)["flight_price"].mean(),
                textposition="outside",
            )
        )
        fig.update_layout(
            title=f"Average Flight Price by {feature_chosen.replace('_', ' ')}"
        )

    elif graph_type == "Scat Plot":
        df = (
            main_data.groupby(["Departure_Month", feature_chosen])["flight_price"]
            .mean()
            .reset_index()
        )
        fig = px.scatter(
            df,
            x="Departure_Month",
            y="flight_price",
            color=feature_chosen,
            # symbol=feature_chosen,
        )
        fig.update_layout(scattermode="group")

    elif graph_type == "Line":
        df = main_data.groupby(feature_chosen)["flight_price"].mean().reset_index()
        fig = px.line(df, x=feature_chosen, y="flight_price")
        fig.update_traces(mode="lines+markers")
        fig.update_layout(title=f"Average Price by {feature_chosen.replace('_', ' ')}")
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
        title_automargin=True,
        # yref="paper",
        title=dict(
            x=0.5,
            y=0.95,
            xanchor="center",
            yanchor="top",
            font=dict(
                color=colors["main_text"],
                size=20,
                family="Arial, sans-serif",
                shadow="auto",
            ),
        ),
        plot_bgcolor=colors["white"],
        paper_bgcolor=colors["plot_bgcolor"],
        font=dict(
            color=colors["main_text"],
            family="Arial, sans-serif",
            size=12,
        ),
        margin=dict(t=40, b=40),
        xaxis=dict(gridcolor="#2D2D2D", linecolor="#2D2D2D", title_font=dict(size=14)),
        yaxis=dict(gridcolor="#2D2D2D", linecolor="#2D2D2D", title_font=dict(size=14)),
        transition=dict(duration=500, easing="cubic-in-out", ordering="layout first"),
    )

    return fig
