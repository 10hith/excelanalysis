import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
from utils.params import HOST
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                )


first_card = dbc.Card(
    dbc.CardBody(
        [
            html.P("num_distinct -> 329"),
        ]
    ), color="info", inverse=True, className="h-100"
)


second_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("100%", className="card-title"),
            dbc.Badge("Completeness1", color="primary"),
            dbc.Button(
                ["Completeness", dbc.Badge("100%", color="light", className="ml-3")],
                color="info", className="btn-sm"
            ),
        ],
    ), color="primay", inverse=False, outline=True,
)


third_card = dbc.Card(
    dbc.CardBody(
        [
            dbc.Button(
                ["approx distinct value  ", dbc.Badge(" 329", color="light", className="display-1")],
                color="primary",
            )
        ],
    ), color="primay", inverse=False, outline=True,
)

#
# non_numeric_button_group = dbc.ButtonGroup(
#     [
#         dbc.Button("approx distinct value -> 329", className="border-info text-left"),
#         dbc.Button("completeness -> 1", className="border-info text-left"),
#         dbc.Button("column type -> numeric", className="border-info text-left"),
#     ],
#     vertical=True,
#     className="bg-info text-white",
#     size="sm"
# )
#
# numeric_button_group1 = dbc.ButtonGroup(
#     [
#         dbc.Button("sum -> 16893702.26", className="border-info text-left"),
#         dbc.Button("max -> 3291", className="border-info text-left"),
#         dbc.Button("min -> -40617.5", className="border-info text-left"),
#     ],
#
#     vertical=True,
#     className="bg-info text-white",
#     size="sm"
# )
#
# numeric_button_group2 = dbc.ButtonGroup(
#     [
#         dbc.Button("mean -> 24133.860371428575", className="border-info text-left"),
#         dbc.Button("stdDev -> 254080.60355172996", className="border-info text-left"),
#     ],
#
#     vertical=True,
#     className="bg-info text-white",
#     size="sm"
# )
#
# dbc.Collapse(
#     dbc.Row([
#         dbc.Col(non_numeric_button_group, width={"order": 1, "offset": 1}),
#         dbc.Col(numeric_button_group1, width={"order": 2}),
#         dbc.Col(numeric_button_group2, width={"order": 3})
#     ]),
#     id="collapse",
#     is_open=False,
# )

app.layout=html.Div([

    first_card,
    dbc.Row([
        dbc.Col(second_card, width=3, className="mh-300")
    ]),
    third_card
    # dbc.Button(
    #     "Open collapse",
    #     id="collapse-button",
    #     className="mb-3",
    #     color="primary",
    #     n_clicks=0,
    # ),
    # dbc.Collapse(
    #     dbc.Row([
    #         dbc.Col(non_numeric_button_group, width={"order": 1, "offset": 1}),
    #         dbc.Col(numeric_button_group1, width={"order": 2}),
    #         dbc.Col(numeric_button_group2, width={"order": 3})
    #     ]),
    #     id="collapse",
    #     is_open=False,)
])

# @app.callback(
#     Output("collapse", "is_open"),
#     [Input("collapse-button", "n_clicks")],
#     [State("collapse", "is_open")],
#     prevent_initial_call=True
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open


if __name__ == '__main__':
    app.run_server(debug=True, port=8001, host=HOST)