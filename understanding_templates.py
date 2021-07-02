import dash
import dash_labs as dl
import numpy as np
import dash_core_components as dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_html_components as html

app = dash.Dash(__name__, plugins=[dl.plugins.FlexibleCallbacks()])
tpl = dl.templates.DbcRow(app, title="Manual Update", theme=dbc.themes.BOOTSTRAP, input_cols=2, )

@app.callback(
    args=dict(
        fun=tpl.dropdown_input(["sin", "cos", "exp"], label="Function", kind=dl.State),
        figure_title=tpl.textbox_input(
            "Initial Title", label="Figure Title",
        ),
        phase=tpl.slider_input(1, 10, label="Phase", ),
        amplitude=tpl.slider_input(1, 10, value=3, label="Amplitude", ),
        n_clicks=tpl.button_input("Update", label=None, kind=dl.Input),
    ),
    template=tpl,
)
def greet(fun, figure_title, phase, amplitude, n_clicks):
    print(fun, figure_title, phase, amplitude)
    xs = np.linspace(-10, 10, 100)
    return [
        dcc.Graph(
        figure=px.line(
            x=xs,
            y=getattr(np, fun)(xs + phase) * amplitude,
            template="ggplot2"
        ).update_layout(
            title_text=figure_title,
            margin=dict(l=40, r=0, t=40, b=30)
        ), ),
        html.Br(),
        dcc.Graph(
            figure=px.line(x=xs, y=getattr(np, fun)(xs + phase) * amplitude).update_layout(
                title_text=figure_title
        )),
        ]

app.layout = dbc.Container(fluid=True, children=tpl.children)

if __name__ == "__main__":
    app.run_server(debug=True)