import dash
from dash import html, Input, Output
import dash_extensions as de
from dash_extensions import Ticker, Download

# Setup options.
url = "https://assets9.lottiefiles.com/packages/lf20_YXD37q.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))
# Create example app.
app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([de.Lottie(title="loading dataset",options=options, width="25%", height="25%", url=url, speed=1)],
    style={'display': 'true'},
             ),
    html.Div(Ticker([html.Div("Some text")], direction="toRight")),
    html.Button("Download", id="btn"), Download(id="download")
    ]
)


@app.callback(Output("download", "data"), [Input("btn", "n_clicks")],
              prevent_initial_call=True)
def func(n_clicks):
    return dict(content="Hello world!", filename="hello.txt")


if __name__ == '__main__':
    app.run_server(debug=True, port=8002, host="172.24.33.121")

