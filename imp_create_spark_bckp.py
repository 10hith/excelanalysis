import time

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_labs as dl
from dash.dependencies import Input, Output, State
import uuid
import requests
session = requests.Session()
session.trust_env = False

# Defining the Session Id
session_id = str(uuid.uuid4())

app = dash.Dash(
    __name__,
    plugins=[dl.plugins.FlexibleCallbacks()],
    external_stylesheets=[dbc.themes.CYBORG],
    title="DeDash",
    requests_pathname_prefix='/login/'
)

tpl = dl.templates.DbcCard(app, title="Welcome to DeDash")


@app.callback(
    inputs=dict(
    racf_input=tpl.textbox_input(id="racfInput", label="Please provide your RACF", kind=dl.State),
    app_name=tpl.textbox_input(label="Please provide an App name", kind=dl.State),
    button_input=tpl.button_input(id="buttonCreateSpark", children="Create Spark Session", label=""),
    ),
    outputs= dict(op=tpl.div_output()),
    template=tpl,
    prevent_initial_call=True
)
def template_callback(racf_input: str, app_name: str, button_input: int):
    # return html.Div(["this is *divOuput*", dbc.Spinner(color="primary")])
    return ""


# Use of callback context !! this is amazing
@app.callback(
    output=dict(
        op=Output("buttonCreateSpark", "children"),
        op_disable=Output("buttonCreateSpark", "disabled"),
    ),
    inputs=dict(
        nclicks=Input("buttonCreateSpark", "n_clicks"),
        racf=Input("racfInput", "value"),
    ),
    prevent_initial_call=True
)
def start_spinner(nclicks, racf: str):
    ctx = dash.callback_context
    print(ctx.triggered)
    print(ctx.triggered[0])
    print(ctx.triggered[0]['value'])

    if nclicks is not None and nclicks>=2:
        return dict(op="Issue creating a spark session, Refresh the page and try again")

    if nclicks is not None and nclicks==1:
        return dict(op=dbc.Spinner(size="sm"), op_disable="True")


# dcc.Loading(id="loading-1", children=[html.Div(id="loading-output-1")], type="default")

app.layout = html.Div([
    dbc.Row(
        dbc.Col(
            dbc.Container(fluid=True, children=tpl.children),
            width={'size':3, 'offset':4, 'order':1},
        ),
        align="center", no_gutters=True, justify='start',
    ),
    dbc.Row(
        dbc.Col(
            [
                # perform a get request so the cookie is set
                dcc.Link('Navigate to "/"', href='http://11.15.93.81:8000/set-cookie-get/ravina', refresh=True),
                html.Button(id='clientSideCb', children="Request"),
                html.Div(id="hiddenDiv", children=[""])
                ]
        )
    ),
    ])


''' Example of requests from within dash
'''
# @app.callback(
#     Output("hiddenDiv", "children"),
#     Input("clientSideCb", "n_clicks")
# )
# def send_cookie_request(nclicks: int):
#     session.get("http://11.15.93.81:8000/set-cookie-get/within_dash")
#     print("request sent from Dash")
#     return [""]

if __name__ == "__main__":
    app.run_server(debug=True)