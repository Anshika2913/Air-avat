import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import requests

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# ---------- Layout ----------

app.layout = dbc.Container([

    html.H1("AIR-AVAT Aircraft Health Monitoring System",
            className="text-center my-4"),

    dbc.Row([

        # Input Panel
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Input Parameters", className="card-title"),

                    html.Label("Cycle"),
                    dbc.Input(id="cycle", type="number", value=50),

                    html.Br(),

                    html.Label("Sensor 7 (Vibration)"),
                    dbc.Input(id="sensor_7", type="number", value=553.90),

                    html.Br(),

                    dbc.Button("Run Prediction",
                               id="predict-btn",
                               color="primary",
                               className="w-100")
                ])
            ])
        ], width=4),

        # Output Panel
        dbc.Col([

            dbc.Row([
                dbc.Col(dcc.Graph(id="rul-gauge"), width=6),
                dbc.Col(html.Div(id="health-badge"), width=6)
            ]),

            html.Br(),

            dbc.Card([
                dbc.CardBody([
                    html.H4("Alerts"),
                    html.Div(id="alerts-output")
                ])
            ])
        ], width=8)
    ])

], fluid=True)


# ---------- Callback ----------

@app.callback(
    [Output("rul-gauge", "figure"),
     Output("health-badge", "children"),
     Output("alerts-output", "children")],
    Input("predict-btn", "n_clicks"),
    State("cycle", "value"),
    State("sensor_7", "value")
)
def predict(n_clicks, cycle, sensor_7):

    if not n_clicks:
        return go.Figure(), "", ""

    data = {
        "cycle": cycle,
        "op_setting1": 0.0,
        "op_setting2": 0.0,

        "sensor_1": 518.67,
        "sensor_2": 642.15,
        "sensor_3": 1589.70,
        "sensor_4": 1400.60,
        "sensor_5": 14.62,
        "sensor_6": 21.61,
        "sensor_7": sensor_7,
        "sensor_8": 2388.02,
        "sensor_9": 9046.19,
        "sensor_10": 1.30,
        "sensor_11": 47.47,
        "sensor_12": 521.66,
        "sensor_13": 2388.02,
        "sensor_14": 8138.62,
        "sensor_15": 8.4195,
        "sensor_16": 0.03,
        "sensor_17": 392,
        "sensor_20": 39.06,
        "sensor_21": 23.4190
    }

    response = requests.post("http://127.0.0.1:8000/predict", json=data)
    result = response.json()

    rul = result["Predicted_RUL"]
    health = result["Health_Status"]
    alerts = result["Alerts"]

    # -------- Gauge --------
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rul,
        title={"text": "Remaining Useful Life"},
        gauge={
            "axis": {"range": [0, 130]},
            "bar": {"color": "cyan"},
            "steps": [
                {"range": [0, 10], "color": "red"},
                {"range": [10, 30], "color": "orange"},
                {"range": [30, 130], "color": "green"},
            ],
        }
    ))

    # -------- Health Badge --------
    color_map = {
        "NORMAL": "success",
        "WARNING": "warning",
        "CRITICAL": "danger"
    }

    badge = dbc.Alert(
        f"Health Status: {health}",
        color=color_map.get(health, "secondary"),
        style={"fontSize": "22px", "textAlign": "center"}
    )

    # -------- Alerts --------
    alert_list = html.Ul([html.Li(a) for a in alerts])

    return gauge, badge, alert_list


if __name__ == "__main__":
    app.run(debug=True, port=8050)