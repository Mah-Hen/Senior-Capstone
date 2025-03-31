from dash import Dash, html, dcc, callback, Output, Input, State
import dash
import time
from datetime import date
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from data_processing import FlightDataProcessor
from flight_predictor import FlightPredictionModel

# Get current and future dates
current_time = time.localtime()
year, month, day = current_time.tm_year, current_time.tm_mon, current_time.tm_mday
new_month = month + 6
new_year = year if new_month <= 12 else year + 1
new_month = new_month if new_month <= 12 else new_month - 12

# Color scheme
colors = {
    "background": "#0A0A0A",
    "main_text": "#F0F0F0",
    "secondary_text": "#888888",
    "primary_accent": "#00FFE0",
}

# Seating class options
SEATING_CLASSES = ["Economy", "Premium Economy", "Business", "First Class"]

layout = html.Div(
    children=[
        html.H1("Flight Search Page", style={"color": colors["main_text"]}),
        html.Div(
            "Search for a flight below.", style={"color": colors["secondary_text"]}
        ),
        dcc.Input(
            id="input_departure",
            type="text",
            placeholder="Departure Airport",
            style={"margin": "10px", "color": colors["secondary_text"]},
        ),
        dcc.Input(
            id="input_arrival",
            type="text",
            placeholder="Arrival Airport",
            style={"margin": "10px", "color": colors["secondary_text"]},
        ),
        # Date Pickers
        dcc.DatePickerSingle(
            id="depart-date-picker",
            clearable=True,
            min_date_allowed=date(year, month, day),
            max_date_allowed=date(new_year, new_month, day),
            month_format="MMMM Y",
            placeholder="Depart Date",
            style={"fontSize": "18px", "width": "280px"},
        ),
        dcc.DatePickerSingle(
            id="return-date-picker",
            clearable=True,
            min_date_allowed=date(year, month, day),
            max_date_allowed=date(new_year, new_month, day),
            month_format="MMMM Y",
            placeholder="Return Date",
            style={"fontSize": "18px", "width": "280px"},
        ),
        html.Div(
            html.Div(
                # Dropdown for Seating Class
                dcc.Dropdown(
                    id="class-dropdown",
                    options=[{"label": cls, "value": cls} for cls in SEATING_CLASSES],
                    placeholder="Select Seating Class",
                    searchable=False,
                    clearable=False,
                    style={
                        "width": "300px",
                        "marginTop": "10px",
                        "color": colors["secondary_text"],
                        "margin": "20px",
                    },
                ),
                style={
                    "display": "flex",
                    "justifyContent": "center",  # Centers horizontally
                    "alignItems": "center",  # Aligns items properly
                    "marginTop": "10px",
                },
            ),
        ),
        html.Button(
            "Search Flights",
            id="submit-button",
            n_clicks=0,
            style={"marginTop": "20px"},
        ),
        # Output display
        html.Div(
            id="output-display",
            style={"color": colors["primary_accent"], "marginTop": "20px"},
        ),
    ],
    style={"fontFamily": "Arial, sans-serif", "padding": "20px"},
)


# Callback to update output based on user selection
@callback(
    Output("output-display", "children"),
    Input("submit-button", "n_clicks"),
    State("input_departure", "value"),
    State("input_arrival", "value"),
    State("depart-date-picker", "date"),
    State("return-date-picker", "date"),
    State("class-dropdown", "value"),
    prevent_initial_call=True,  # Enures nothing is ran until clicked button
)
def handle_submission(
    n_clicks, departure, arrival, depart_date, return_date, seat_class
):
    if not departure or not arrival or not depart_date or not seat_class:
        return "Please fill in all required fields."

    # Package and preprocess data in-memory
    user_input = {
        "departure": departure,
        "arrival": arrival,
        "depart_date": depart_date,
        "return_date": return_date,
        "seat_class": seat_class,
    }
    processed_data = FlightDataProcessor()
    processed_data = processed_data.process_user_data(user_input)
    return f"Searching flights from {departure} to {arrival} on {depart_date}. Seating Class: {seat_class}."


dash.register_page(__name__)
