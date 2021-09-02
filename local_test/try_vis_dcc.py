import dash
from dash import html, Input,Output
import dash_bootstrap_components as dbc
import visdcc
from utils.params import  HOST

app = dash.Dash(
    __name__,
    title = "Excel-Analysis",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    # requests_pathname_prefix="/new_upload/"
)

app.layout = html.Div([
    html.Button('open url', id = 'button'),
    visdcc.Run_js(id = 'javascript')
])

@app.callback(
    Output('javascript', 'run'),
    [Input('button', 'n_clicks')])
def myfun(x):
    if x:
        return "window.scrollTo(0,0)"
    return ""


if __name__ == '__main__':
    app.run_server(debug=True, port=8001, host=HOST)