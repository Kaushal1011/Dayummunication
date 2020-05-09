#!/usr/bin/env python3


import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output, State

import QPSK

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


def dashboard() -> dash.Dash:
    """Loading the model and application"""

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    # msg = np.array(
    #     [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0]
    # )  # 8PSK demo signal
    # msg = np.array([0, 1, 0, 0, 1, 1, 0, 1, 1, 0])  # QPSK demo signal
    # msg = np.random.randint(low=0, high=2, size=int(1e3))
    # M = 8
    # k = int(np.log2(M))
    t_csd = np.linspace(0.0, 2.0 * np.math.pi, 100)
    f_c = 100.0
    t_c = 1.0 / f_c

    # Sampling rate
    f_s = 10000.0
    t_s = 1.0 / f_s

    # MPSK Parameters
    Tb = 0.01
    Eb = 0.001

    app.layout = html.Div(
        children=[
            # html.H1(children="Title", style={"textAlign": "center", "margin": 20}),
            dcc.Graph(id="signal"),
            dcc.Graph(id="modulated-signal"),
            dcc.Graph(id="noisy-mod-signal"),
            html.Div(
                id="input",
                children=[
                    html.H2(
                        children="Input",
                        style={"marginBottom": 0, "textAlign": "left"},
                    ),
                    dcc.Input(id="input-str", value="0", type="text"),
                    html.Button(
                        id="submit-button-state", n_clicks=0, children="Submit"
                    ),
                ],
            ),
        ]
    )

    @app.callback(
        [
            Output("signal", "figure"),
            Output("modulated-signal", "figure"),
            Output("noisy-mod-signal", "figure"),
        ],
        [Input("submit-button-state", "n_clicks")],
        [State("input-str", "value")],
    )
    def conv(n_clicks: int, input_str: str) -> None:
        if n_clicks >= 0:
            chars = []
            for i in input_str:
                b = bin(ord(i))[2:]
                b = "0" + b if len(b) == 7 else "00" + b
                chars.append(b)

            chars = [int(i) for i in list("".join(chars))]

            mod = QPSK.modulate(chars)
            symbols = np.array([chars[0::2], chars[1::2]])
            print(symbols)

            t_sym = np.linspace(
                0,
                np.size(symbols, axis=1) * Tb,
                int(np.size(symbols, axis=1) * Tb * f_s),
            )
            t_sym = np.arange(0.0, np.size(symbols, axis=1) * 2.0 * t_c, t_s)
            print(input_str, chars)
            return (
                {
                    "data": [dict(x=list(range(len(chars))), y=chars)],
                    "layout": {
                        "display": "block",
                        "margin-left": "auto",
                        "margin-right": "auto",
                    },
                },
                {
                    "data": [dict(x=t_sym, y=mod[2])],
                    "layout": {
                        "display": "block",
                        "margin-left": "auto",
                        "margin-right": "auto",
                    },
                },
                {
                    "data": [dict(x=t_sym, y=mod[3])],
                    "layout": {
                        "display": "block",
                        "margin-left": "auto",
                        "margin-right": "auto",
                    },
                },
            )

    return app


if __name__ == "__main__":
    dashboard().run_server(debug=True)
