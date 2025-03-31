from dash import Dash, html, dcc, callback, Output, Input, State
import dash
import dash_bootstrap_components as dbc


# from folder.file import class
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
}


# Intialize the app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])


# Custom navigatition card
def navigation_card(page):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(page["name"], className="card-title text-white"),
                html.P(
                    f"Explore the {page['name'].lower()} page",
                    className="card-text text-dark",
                    style={"color": colors["secondary_text"]},
                ),
                dbc.Button(
                    "Go to page",
                    href=page["relative_path"],
                    color="dark",
                    className="btn-outline-light",
                ),
            ]
        ),
        className="shadow-lg shadow-dark transform transition hover:scale-105",
        style={
            "box-shadow": "0 4px 6px rgba(255, 255, 255, 0.1)",
            "transition": "all 0.3s ease",
        },
        inverse=True,
    )


# Add a callback to toggle between dark mode and light mode
app.layout = html.Div(
    [
        dcc.Store(
            "theme_id-store", storage_type="local", data="dark"
        ),  # True means dark background
        html.Div(
            id="main-div",
            style={
                "background": colors["background"],
                "padding": "5rem 1rem",
                "textAlign": "center",
            },
            children=[
                html.Div(
                    style={"textAlign": "center"},
                    children=[
                        html.H1(
                            "MaxyMal: Flight Insights Pro",
                            className="primary-center-header",
                            style={
                                "color": colors[
                                    "primary_accent"
                                ],  # colors["primary_accent"],
                                "fontSize": "2.5rem",
                                "marginBottom": "1rem",
                            },
                        ),
                        html.P(
                            "Real-time aviation analytics for smarter travel decisions",
                            style={
                                "color": "#888888",  # colors["secondary_text"],
                                "fontSize": "1.5rem",
                                "maxWidth": "800px",
                                "margin": "0 auto 2rem",
                            },
                        ),
                        dbc.Button(
                            "Toggle Dark/Light Mode",
                            id="toggle-theme-btn",
                            color="primary",
                            className="ms-auto",
                            style={
                                "position": "fixed",
                                "bottom": "20px",
                                "left": "20px",
                                "zIndex": 1000,
                            },
                        ),
                        dbc.Container(
                            [
                                dbc.Row(
                                    children=[
                                        dbc.Col(navigation_card(page), width=4)
                                        for page in dash.page_registry.values()
                                    ],
                                    className="card-deck",
                                )
                            ]
                        ),
                        dash.page_container,
                    ],
                    className="container",
                )
            ],
        ),
    ]
)


# Callback to toggle between dark and light mode
@app.callback(
    Output("theme_id-store", "data"),
    Input("toggle-theme-btn", "n_clicks"),
    State("theme_id-store", "data"),
    prevent_initial_call=True,
    # suppress_callback_exceptions=True,
)
def update_theme_store(n_clicks, current_theme):
    return "light" if current_theme == "dark" else "dark"


@app.callback(
    Output("main-div", "style"),  # (classname, according argument)
    Input("theme_id-store", "data"),
)
def toggle_theme(theme):
    if theme == "dark":
        return {
            "background": colors["background"],  # colors["background"],
            "padding": "5rem 1rem",
            "textAlign": "center",
        }
    else:
        return {
            "background": "#F8F8FF",
            "padding": "5rem 1rem",
            "textAlign": "center",
        }


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
