from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash
import pandas as pd
import plotly.express as px

"""
I do not know what to put on this page yet.
I will leave it blank for now.
"""

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

dash.register_page(__name__, path="/")

layout = html.Div(
    children=[
        html.H1(
            "This is our Home page",
            id="header-H1",
            style={
                "fontSize": "2rem",
                "marginBottom": "1rem",
            },
        ),
        html.Div(
            "This is our Home page content.",
            id="header-div",
            style={"fontSize": "1rem"},
        ),
    ]
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
