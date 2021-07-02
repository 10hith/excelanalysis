import dash
import dash_labs as dl
import dash_html_components as html

import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc


import time

app = dash.Dash(__name__, plugins=[dl.plugins.FlexibleCallbacks()], title="My Sidebar")


tpl_button = dl.templates.DbcCard(app, title="My Buttons")
tpl_other_graph = dl.templates.DbcSidebar(app, title="the other graph")

div = html.Div()
click_button = html.Button(children="Click Me")
myButton = html.Button(children="Click Me too")

#
# tpl_button.add_component(click_button, label="Button to click", role="input")
# tpl_button.add_component(myButton, role="input")
# tpl_button.add_component(div, role="output")


# @app.callback(dl.Output(div, "children"), dl.Input(click_button, "n_clicks"))
# def callback(n_clicks):
#     return "Clicked {} times".format(n_clicks)


@app.callback(
    dl.Input(html.Button(children="Click Me"), "n_clicks", label="Button to click"),
    template=tpl_button,
)
def callback1(n_clicks):
    return "Clicked {} times".format(n_clicks)

@app.callback(
    args=dict(
        fun=tpl_other_graph.dropdown_input(["sin", "cos", "exp"], label="Function"),
        figure_title=tpl_other_graph.textbox_input("Initial Title", label="Figure Title"),
        phase=tpl_other_graph.slider_input(1, 10, label="Phase"),
        amplitude=tpl_other_graph.slider_input(1, 10, value=3, label="Amplitude"),
    ),
    output=tpl_other_graph.graph_output(),
    template=tpl_other_graph,
)
def callback(fun, figure_title, phase, amplitude):
    xs = np.linspace(-10, 10, 100)
    np_fn = getattr(np, fun)

    # Let parameterize infer output component
    x = xs
    y = np_fn(xs + phase) * amplitude
    return px.line(x=x, y=y).update_layout(title_text=figure_title)

lohith="true"

if (lohith == 'true'):
    app.layout = dbc.Container(id="container", fluid=True, children=tpl_button.children)
else:
    app.layout = dbc.Container(id="container", fluid=True, children=tpl_other_graph.children)


app.layout = html.Div(children=[
    dbc.Container(fluid=True, children=tpl_button.children),
    dbc.Container(fluid=True, children=tpl_other_graph.children)
])


app.layout = html.Div(children=[
    tpl_button.children,
    tpl_other_graph.children
])



if __name__ == "__main__":
    app.run_server(debug=True)