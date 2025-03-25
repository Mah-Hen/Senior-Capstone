from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash
import pandas as pd
import plotly.express as px


dash.register_page(__name__, path="/")

layout = html.Div([
    html.H1('This is our Home page'),
    html.Div('This is our Home page content.'),
])