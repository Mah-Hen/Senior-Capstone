from dash import Dash, html, dcc, callback, Output, Input, State
import dash
import time
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
    "main_text": "#F0F0F0",
    "secondary_text": "#888888",
    "primary_accent": "#00FFE0",
}

# Seating class options
SEATING_CLASSES = ["Economy", "Prem Econ", "Business", "First Class"]

layout = html.Div(
    children=[
        html.H1("Flight Search Page", style={"color": colors["main_text"]}),
        html.Div(
            "Search for a flight below.", style={"color": colors["secondary_text"]}
        ),
        dcc.Input(
            id="input_departure",
            type="text",
            placeholder="Departure City",
            style={"margin": "10px", "color": colors["secondary_text"]},
        ),
        dcc.Input(
            id="input_arrival",
            type="text",
            placeholder="Arrival City",
            style={"margin": "10px", "color": colors["secondary_text"]},
        ),
        # Date Pickers
        dcc.DatePickerSingle(
            id="depart-date-picker",
            clearable=True,
            min_date_allowed=date(year, month, min_day),
            max_date_allowed=date(new_year, new_month, max_day),
            month_format="MMMM Y",
            placeholder="Depart Date",
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
                        "margin": "5px",
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
            className="btn-outline-light",
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
    State("class-dropdown", "value"),
    prevent_initial_call=True,  # Enures nothing is ran until clicked button
)
def handle_submission(n_clicks, departure, arrival, depart_date, seat_class):
    if not departure or not arrival or not depart_date or not seat_class:
        return "Please fill in all required fields."

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
    user_data = Processor.get_processed_user_data(user_data)

    # Now we're at the point of predicting the user_input.
    # Call the prediction_model class and pre_process the user data
    # From there we'll start to connect the
    return f"Searching flights from {departure} to {arrival} on {depart_date}. Seating Class: {seat_class}."


dash.register_page(__name__)
