import dash
import dash_labs as dl
import numpy as np
import dash_core_components as dcc
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = dash.Dash(__name__, plugins=[dl.plugins.FlexibleCallbacks()])
tpl = dl.templates.DbcRow(app, title="Manual Update", theme=dbc.themes.SOLAR)

@app.callback(
    args=dict(
        fun=tpl.dropdown_input(options = ["sin", "cos", "exp"], label="Function", id="function_type"),
        figure_title=tpl.textbox_input(
            "Initial Title", label="Figure Title"
        ),
        phase=tpl.slider_input(1, 10, label="Phase"),
        amplitude=tpl.slider_input(1, 10, value=3, label="Amplitude"),
    ),
    template=tpl,
)
def greet(fun, figure_title, phase, amplitude):
    print(fun, figure_title, phase, amplitude)
    xs = np.linspace(-10, 10, 100)
    return dcc.Graph(
        figure=px.line(x=xs, y=getattr(np, fun)(xs + phase) * amplitude).update_layout(
            title_text=figure_title
        )
    )


@app.callback(
    Output(component_id="function_type", component_property="options"),
    inputs=dict(
        n_clicks = tpl.button_input("Update Figure type", label=None),
    ),
)
def go_exponential(n_clicks):
    return ["something"]


app.layout = dbc.Container(fluid=True, children=tpl.children)

if __name__ == "__main__":
    app.run_server(debug=True)