import dash
from dash.dependencies import Output, Input
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from utils.params import HOST

app = dash.Dash(__name__)
app.layout = html.Div([
    html.Button("Download Excel", id="btn_xlsx"),
    dcc.Download(id="download-dataframe-xlsx"),
])


df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 1, 5, 6], "c": ["x", "x", "y", "y"]})


@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_excel, "mydf.xlsx", sheet_name="Sheet_name_1")


if __name__ == "__main__":
    app.run_server(debug=True, port=8003, host=HOST)
