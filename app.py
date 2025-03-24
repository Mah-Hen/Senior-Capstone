from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from data_processing import FlightDataProcessor

# from folder.file import class

# Read the data
processor = FlightDataProcessor()
main_data = processor.get_processed_main_data()


# Intialize the app
app = Dash(__name__)



# App layout
colors = {
    'background': '#0A0A0A',
    'surface': '#1A1A1A',
    'main_text': '#F0F0F0',
    'secondary_text':'#888888', 
    'primary accent': '00FFE0',
    'secondary accent':'FF00FF',
    'tertiary accent': '#CCFF00',
    'borders': '#4A4A4A',
    'plot_bgcolor': '#121212',
    'paper_bgcolor': '#121212',
    'error_color': '#FF3860',
    'success_color': '#00FF88',
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children = 'MaxyMal: Flight Data Analysis', style={
        "textAlign": "center", 
        "color": colors['main_text']}),
    html.Div(children='A dashboard design to help you plan your next flight.', style={
        "textAlign": "center", 
        "color":colors['secondary_text']}),
    html.Hr(),
    dcc.Dropdown(options=['Layover_Label', 'Arrival_Region', 'Departure_Region', 'Arrival_Time_Label', 'Departure_Time_Label', 'Arrival_Season', 'Departure_Season', 'Duration_Label', 'Seating_Class', 'Airline_Name'], value='Arrival_Region', id='controls-and-dropdown-item', 
                 style={
                     'width': '50%',
                     'margin': 'auto',
                     'color': colors['primary accent'],
                     'backgroundColor': colors['secondary accent']
                 }), 
    #dash_table.DataTable(data=main_data.to_dict('records'),page_size = 5),
    #dcc.Graph(figure=px.histogram(main_data, x='Arrival_Region', y='flight_price', color='Arrival_Region', histfunc='avg')),
    dcc.Graph(figure={}, id='controls-and-graph')
])


# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-dropdown-item', component_property='value')
)
def update_graph(column_chosen):
    fig = px.histogram(main_data, x=column_chosen, y='flight_price', color=column_chosen, histfunc='avg', title=f"Average Flight Price by {column_chosen}".replace('_', ' '), hover_data='flight_price')  
    fig.update_layout(
        plot_bgcolor=colors['surface'],
        paper_bgcolor=colors['background'],
        font_color=colors['main_text'], 
        margin = dict(t=40, b=40),
        xaxis=dict(
            gridcolor='#2D2D2D',
            linecolor='#2D2D2D',
            title_font=dict(size=14)
        ),
        yaxis=dict(
            gridcolor='#2D2D2D',    
            linecolor='#2D2D2D',
            title_font=dict(size=14)
        )
    )
    return fig



# Run the app
if __name__ == "__main__":
    app.run(debug=True)