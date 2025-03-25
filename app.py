from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


# from folder.file import class
colors = {
    'background': '#0A0A0A',
    'surface': '#1A1A1A',
    'main_text': '#F0F0F0',
    'secondary_text':'#888888', 
    'primary_accent': '#00FFE0', 
    'secondary_accent': '#FF00FF',  
    'tertiary_accent': '#CCFF00',
    'borders': '#4A4A4A',
    'plot_bgcolor': '#121212',
    'paper_bgcolor': '#121212',
    'error_color': '#FF3860',
    'success_color': '#00FF88',
}


# Intialize the app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])


# Custom navigatition card
def navigation_card(page):
    return dbc.Card(
            dbc.CardBody(
                [
                    html.H4(page['name'], className="card-title text-primary"),
                    html.P(f"Explore the {page['name'].lower()} section of our flight data analysis platform.", 
                    className="card-text text-muted"),
                    dbc.Button("Go to page", href=page["relative_path"], color=colors["secondary_accent"], className="btn-outline-primary"),
                ]), 
                className="cardBody"
    )

app.layout = html.Div([
    html.Div([
        html.H1('MaxyMal: Flight Data Analysis', 
                className='primary-center-header'),
        html.P('Comprehensive Flight Insights and Analytics', 
               className='secondary-center-text'),

        dbc.Container([
            dbc.Row([
                dbc.Col(navigation_card(page), width=4) 
                for page in dash.page_registry.values()
            ], className="card-deck")
        ]),

        dash.page_container
    ], className='container')
])
    


# Run the app
if __name__ == "__main__":
    app.run(debug=True)