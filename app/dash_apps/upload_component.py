import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from utils.spark_utils import get_local_spark_session
from utils.deutils import run_profile
from pyspark.sql import functions as f
import databricks.koalas as ks
import json

# df = pd.DataFrame()

df = pd.DataFrame({'num_legs': [2, 4, 8, 0],
                   'num_wings': [2, 0, 0, 0],
                   'num_specimen_seen': [10, 2, 1, 8]},
                  index=['falcon', 'dog', 'spider', 'fish']
                  )

spark = get_local_spark_session(app_name="Upload Application")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    # requests_pathname_prefix="/upload/"
)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-data-upload'),
    html.Div(id='recordCount', children=[]),
    dcc.Store(id='resultStore', data=[]),
])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              prevent_initial_call=True
              )
def read_contents_into_pdf(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        content_type, content_string = list_of_contents.split(',')

        decoded = base64.b64decode(content_string)
        global df
        try:
            if 'csv' in list_of_names:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in list_of_names:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

    if list_of_contents is None:
        return html.Div([])

    return html.Div([
        html.H2("Displaying first 100 records"),
        html.Br(),
        dash_table.DataTable(
            data=df.head(100).to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
            ),
        html.Br(),
        html.Button("Start Analysis", id="startAnalysis", n_clicks=0)
        ])


# @app.callback(Output('recordCount', 'children'),
#               Input('startAnalysis', 'n_clicks'),
#               )
# def display_record_count(n_clicks):
#     record_count = df.count()
#     if n_clicks>=1:
#         return html.Div([
#             html.H3(f"The record count is {record_count}")
#         ])
#     else:
#         return html.Div([])


@app.callback(Output('recordCount', 'children'),
              Input('startAnalysis', 'n_clicks'),
              )
def display_record_count(n_clicks):
    if n_clicks>=1:
        kdf = ks.from_pandas(df)
        profiled_df = run_profile(spark, kdf.to_spark())
        unpacked_df = profiled_df.\
            select(
            "column_name",
            f.explode("histogram").alias("histogram")
        ).selectExpr(
            "column_name",
            "histogram.value as value",
            "histogram.num_occurrences as numOcc",
            "histogram.ratio as ratio")
        # data_table = dash_table.DataTable(
        #     data=unpacked_df.to_dict('records'),
        #     columns=[{'name': i, 'id': i} for i in df.columns]
        # )
        df_as_string = unpacked_df.collect()
        return html.Div([
            html.H6(f"The dataframe as a string is {df_as_string}")
        ])


if __name__ == '__main__':
    app.run_server(debug=True)