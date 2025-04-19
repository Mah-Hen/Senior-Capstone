from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.graph_objects as go
import dash
import time
import dash_bootstrap_components as dbc
from datetime import date, datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from data_processing import FlightDataProcessor
from flight_predictor import FlightPredictionModel
from scraper import userControl

# Get current and future dates
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
months_30 = ["April", "June", "September", "November"]
months_31 = ["January", "March", "May", "July", "August", "October", "December"]


current_time = time.localtime()
max_day = 0
year, month, min_day = current_time.tm_year, current_time.tm_mon, current_time.tm_mday
max_day = min_day
new_month = month + 6
new_year = year if new_month <= 12 else year + 1
new_month = new_month if new_month <= 12 else new_month - 12
if months[new_month - 1] in months_30:
    if max_day == 31:
        max_day = 30
elif months[new_month - 1] == "February":
    if max_day > 28:
        max_day = 28

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
    "H1_text": "#F2F3F4",
}

# Seating class options
SEATING_CLASSES = ["Economy", "Prem Econ", "Business", "First Class"]

# Do a row col here with the user entry widgets to make it look nice.


layout = (
    html.Div(
        children=[
            html.H1(
                "Flight Search Page",
                id="fsp-header",
                style={"fontSize": "2rem"},
            ),
            html.Div(
                "Search for a flight below.",
                id="sfb-div",
                style={"fontSize": "1rem"},
            ),
        ],
        style={"padding": "15px", "textAlign": "center"},
    ),
    dbc.Row(
        dbc.Card(
            children=[
                dcc.Input(
                    id="input_departure",
                    type="text",
                    placeholder="Departure City",
                    style={
                        "margin": "10px",
                        "color": colors["secondary_text"],
                        "border": f"1px solid {colors['borders']}",
                        "borderRadius": "5px",
                    },
                ),
                dcc.Input(
                    id="input_arrival",
                    type="text",
                    placeholder="Arrival City",
                    style={
                        "margin": "10px",
                        "color": colors["secondary_text"],
                        "border": f"1px solid {colors['borders']}",
                        "borderRadius": "5px",
                    },
                ),
                html.Div(
                    dbc.Row(
                        [
                            # Dropdown for Seating Class
                            dbc.Col(
                                dcc.Dropdown(
                                    id="class-dropdown",
                                    options=[
                                        {"label": cls, "value": cls}
                                        for cls in SEATING_CLASSES
                                    ],
                                    placeholder="Select Seating Class",
                                    searchable=False,
                                    clearable=False,
                                    style={
                                        "width": "100%",  # Ensure it takes full width of the column
                                        "color": colors["secondary_text"],
                                        "border": f"0.5px solid {colors['borders']}",
                                        "borderRadius": "5px",
                                    },
                                ),
                                width=3,  # Adjust the width of the column (out of 12)
                            ),
                            # Date Picker
                            dbc.Col(
                                dcc.DatePickerSingle(
                                    id="depart-date-picker",
                                    clearable=True,
                                    min_date_allowed=date(year, month, min_day),
                                    max_date_allowed=date(new_year, new_month, max_day),
                                    month_format="MMMM Y",
                                    placeholder="Depart Date",
                                    style={
                                        "fontSize": "18px",
                                        "width": "100%",  # Ensure it takes full width of the column
                                        "borderColor": colors["borders"],
                                    },
                                ),
                                width=6,  # Adjust the width of the column (out of 12)
                            ),
                        ],
                        justify="center",  # Center the row horizontally
                        align="center",  # Align items vertically in the center
                        style={"marginTop": "10px"},  # Add spacing above the row
                    ),
                    style={"width": "100%"},  # Ensure the container takes full width
                ),
                # Search button and loading display
                html.Div(
                    children=[
                        # Search button
                        html.Button(
                            "Search Flights",
                            id="submit-button",
                            n_clicks=0,
                            style={"marginTop": "20px"},
                            className="btn-outline-light",
                        ),
                        # Loading button
                        dcc.Loading(
                            # Output display
                            [
                                html.Div(
                                    id="output-display",
                                    style={
                                        "marginTop": "20px",
                                        "width": "100%",  # Ensures the table takes full width
                                        "overflowX": "auto",  # Adjusts height automatically
                                    },
                                )
                            ],
                            overlay_style={
                                "visibility": "hidden",
                                "filter": "blur(5px)",
                            },
                            type="circle",
                        ),
                    ]
                ),
            ],
            # width=6,
            style={
                "backgroundColor": "#F5F5F5",  # Cool gray background
                "borderRadius": "10px",
                "padding": "1.5rem",
                "boxShadow": "0 4px 6px rgba(0,0,0,0.1)",
            },
        ),
        style={"fontFamily": "Arial, sans-serif", "padding": "20px"},
    ),
)


# Callback to update output based on user selection
@callback(
    Output("output-display", "children"),
    Input("submit-button", "n_clicks"),
    State("input_departure", "value"),
    State("input_arrival", "value"),
    State("depart-date-picker", "date"),
    State("class-dropdown", "value"),
    prevent_initial_call=True,  # Enures nothing is ran until clicked button
)
def handle_submission(n_clicks, departure, arrival, depart_date, seat_class):
    if not departure or not arrival or not depart_date or not seat_class:
        return "⚠️ Please fill in all required fields."

    # Package and preprocess data in-memory
    user_input = {
        "departure": departure,
        "arrival": arrival,
        "depart_date": depart_date,
        # "return_date": return_date,
        "seat_class": seat_class,
        "search_date": datetime.now().date(),
        "roundtrip": False,
    }
    Processor = FlightDataProcessor()
    user_data = userControl(user_input)
    query_results = Processor.get_processed_user_data(user_input, user_data)
    if query_results.empty:
        return html.Div(
            "⚠️ No results found. Please try different search criteria.",
            style={"color": colors["error_color"]},
        )

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[
                        "Ranking",
                        "Price",
                        "Airline",
                        "Departure Date",
                        "Arrival Date",
                        "# Stops",
                    ],
                    fill_color="#3F51B5",
                    align="left",
                    font=dict(color=colors["main_text"]),
                ),
                cells=dict(
                    values=[
                        query_results["Rank"],
                        query_results["Price"],
                        query_results["Airline"],
                        query_results["Formatted Departure Date"],
                        query_results["Arrival Date"],
                        query_results["Number of Stops"],
                    ],
                    fill_color="#F5F5F5",
                    align="left",
                    font=dict(color="#ECEFF1"),
                ),
            )
        ]
    )

    # Now we're at the point of predicting the user_input.
    # Call the prediction_model class and pre_process the user data
    # From there we'll start to connect the
    return dcc.Graph(
        figure=fig
    )  # f"Searching flights from {departure} to {arrival} on {depart_date}. Seating Class: {seat_class}."


# Page-specific theme callback
@callback(
    Output("fsp-header", "style"),
    Input("theme_id-store", "data"),
    # prevent_initial_call=True,
    # suppress_callback_exceptions=True,
)
def update_header_title(theme):
    if theme != "dark":
        return {
            "textAlign": "center",
            "color": "#0A0A0A",  # colors["primary_accent"],
            "fontSize": "2rem",
            "marginBottom": "1rem",
        }
    return {
        "textAlign": "center",
        "color": colors["H1_text"],
        "fontSize": "2rem",
        "marginBottom": "1rem",
    }


@callback(
    Output("sfb-div", "style"),
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


dash.register_page(__name__)
