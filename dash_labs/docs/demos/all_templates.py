import dash
import dash_labs as dl
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, plugins=[dl.plugins.FlexibleCallbacks()])

# tpl = dl.templates.FlatDiv(app)
# tpl = dl.templates.HtmlCard(app, title="Dash Labs App", width="500px")
# tpl = dl.templates.DbcCard(app, title="Dash Labs App", columns=6)
# tpl = dl.templates.DbcRow(app, title="Dash Labs App")
tpl = dl.templates.DbcSidebar(app, title="Dash Labs App")
# tpl = dl.templates.DdkCard(app, title="Dash Labs App", width=50)
# tpl = dl.templates.DdkRow(app, title="Dash Labs App")
# tpl = dl.templates.DdkSidebar(app, title="Dash Labs App")
#
# tpl = dl.templates.DbcSidebar(
#     app,
#     title="Dash Labs App",
#     theme="https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/superhero/bootstrap.min.css",
#     figure_template=True
# )

# import dash_bootstrap_components as dbc
#
# tpl = dl.templates.DbcSidebar(
#     app,
#     title="Dash Labs App",
#     theme=dbc.themes.CYBORG,
# )

from my_theme import theme

# tpl = dl.templates.DdkSidebar(app, title="Dash Labs App")


@app.callback(
    args=dict(
        fun=tpl.dropdown_input(["sin", "cos", "exp"], label="Function"),
        figure_title1=tpl.textbox_input("Initial Title", label="Figure Title"),
        phase=tpl.slider_input(1, 10, label="Phase"),
        amplitude=tpl.slider_input(1, 10, value=3, label="Amplitude"),
    ),
    output=tpl.graph_output(),
    template=tpl,
)
def callback(fun, figure_title1, phase, amplitude):
    xs = np.linspace(-10, 10, 100)
    np_fn = getattr(np, fun)

    # Let parameterize infer output component
    x = xs
    y = np_fn(xs + phase) * amplitude
    return px.line(x=x, y=y).update_layout(title_text=figure_title1)


app.layout = dbc.Container(fluid=True, children=tpl.children)

# # For DBC templates
# import dash_bootstrap_components as dbc
# app.layout = dbc.Container(fluid=True, children=tpl.children)

if __name__ == "__main__":
    app.run_server(debug=True)