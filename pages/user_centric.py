from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash
import pandas as pd
import plotly.express as px



layout = html.Div([
    html.H1('This is our User page'),
    html.Div('This is our User-centric content.'),
])

dash.register_page(__name__)
