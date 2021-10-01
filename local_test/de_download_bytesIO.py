import io

import dash
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Output, Input
from dash_extensions import Download
from dash_extensions.snippets import send_bytes
from utils.params import HOST
import pyarrow as pa
import pyarrow.parquet as pq

# Example data.
data = np.column_stack((np.arange(10), np.arange(10) * 2))
df = pd.DataFrame(columns=["a column", "another column"], data=data)
# Create example app.
app = dash.Dash(prevent_initial_callbacks=True)
app.layout = html.Div(
    [
        html.Button("Download xlsx", id="btn"),
        html.Button("Download parquet", id="downloadParquetBtn"),
        Download(id="download"),
        Download(id="downloadParquet")
    ]
)


@app.callback(Output("download", "data"), [Input("btn", "n_clicks")])
def generate_xlsx(n_nlicks):

    def to_xlsx(bytes_io):
        xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")
        df.to_excel(xslx_writer, index=False, sheet_name="sheet1")
        xslx_writer.save()

    return send_bytes(to_xlsx, "some_name.xlsx")


@app.callback(Output("download", "data"), [Input("btn", "n_clicks")])
def generate_xlsx(n_nlicks):

    def to_xlsx(bytes_io):
        xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")
        df.to_excel(xslx_writer, index=False, sheet_name="sheet1")
        xslx_writer.save()

    return send_bytes(to_xlsx, "some_name.xlsx")


# @app.callback(Output("downloadParquet", "data"), [Input("downloadParquetBtn", "n_clicks")])
# def generate_xlsx(n_nlicks):
#
#     def to_parquet(bytes_io):
#         table = pa.Table.from_pandas(df)
#         p_writer = pq.ParquetWriter('example2.parquet', table.schema)
#         buf = pa.BufferOutputStream()
#         pq.write_table(table, buf)
#         buf.download
#         # buf.download()
#         return buf.download
#
#     return send_bytes(to_parquet, "10hith.parquet")


@app.callback(Output("downloadParquet", "data"), [Input("downloadParquetBtn", "n_clicks")])
def generate_xlsx(n_nlicks):
    return send_bytes(df.to_parquet, "10hith.parquet")


if __name__ == '__main__':
    app.run_server(debug=True, port=8002, host=HOST)