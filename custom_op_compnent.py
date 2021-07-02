import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
import dash_html_components as html

app = dash.Dash(__name__, plugins=[dl.plugins.FlexibleCallbacks()])
tpl = dl.templates.DbcSidebar(app, "App Title", sidebar_columns=6)

# @app.callback(
#     output=tpl.markdown_output(),
#     inputs=tpl.textarea_input(
#         "## Heading\n", opts=dict(style={"width": "100%", "height": 400})
#     ),
#     template=tpl,
# )
# def markdown_preview_old(input_text):
#     return input_text


@app.callback(
    output=tpl.div_output(),
    inputs=[tpl.textarea_input(id="text_input"
        "## Heading\n", opts=dict(style={"width": "100%", "height": 400})
    ),
    tpl.textarea_input(
        "## Heading\n", opts=dict(style={"width": "100%", "height": 400})
    )],
    template=tpl,
)
def markdown_preview(input_text1, input_text2):
    return input_text2.upper()


div = html.Div()
button = html.Button(children="Click Me")
@app.callback(dl.Output(div, "children"), dl.Input(button, "n_clicks"))
def callback(n_clicks):
    return "Clicked {} times".format(n_clicks)

app.layout = html.Div(
    [
        dbc.Container(fluid=True, children=tpl.children),
        div,
        button
     ]
)



if __name__ == "__main__":
    app.run_server(debug=True)