import base64
import datetime
import io
import uuid
from dash.long_callback import DiskcacheLongCallbackManager

import dash
from dash import dcc, html, Input, Output, State, dash_table
from pyspark.sql import functions as f

from utils.spark_utils import get_local_spark_session, with_std_column_names
from utils.deutils import run_profile
from utils.dash_utils import read_upload_into_pdf, read_upload_into_kdf

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
    dcc.Store(id='idStore', data=[]),
    html.Div(id='contentAsState', children=[]),
])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              prevent_initial_call=True
              )
def display_sample_datatable(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        try:
            pdf = read_upload_into_pdf(list_of_contents, list_of_names)
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
            data=pdf.head(100).to_dict('records'),
            columns=[{'name': i, 'id': i} for i in pdf.columns]
            ),
        html.Br(),
        html.Button("Start Analysis", id="startAnalysis", n_clicks=0),
        html.H2(f"uid for this dataset is {uuid.uuid4().hex}"),
        ])

#
# @app.callback(Output('contentAsState', 'children'),
#               Input('startAnalysis', 'n_clicks'),
#               State('upload-data', 'contents'),
#               State('upload-data', 'filename'),
#               )
# def using_content_as_state(n_clicks, list_of_contents, list_of_names):
#     if n_clicks>=1:
#         if list_of_contents is not None:
#             try:
#                 kdf = read_upload_into_kdf(list_of_contents, list_of_names)
#             except Exception as e:
#                 print(e)
#                 return html.Div([
#                     'There was an error processing this file.'
#                 ])
#
#         if list_of_contents is None:
#             return html.Div([])
#
#         # kdf = ks.from_pandas(kdf)
#         sdf_raw = kdf.to_spark()
#         sdf = sdf_raw.transform(with_std_column_names())
#         profiled_df = run_profile(spark, sdf)
#
#         histogram_sdf = profiled_df.\
#             select(
#             "column_name",
#             f.explode("histogram").alias("histogram")
#         ).selectExpr(
#             "column_name",
#             "histogram.value as value",
#             "histogram.num_occurrences as numOcc",
#             "histogram.ratio as ratio")
#
#         histogram_kdf = histogram_sdf.to_koalas()
#
#         summary_stats_sdf = profiled_df.drop("histogram")
#         summary_stats_kdf = summary_stats_sdf.to_koalas()
#
#         return html.Div([
#             html.H2("Displaying summaryStats"),
#             html.Br(),
#             dash_table.DataTable(
#                 data=summary_stats_kdf.to_dict('records'),
#                 columns=[{'name': i, 'id': i} for i in summary_stats_kdf.columns]
#             ),
#             html.H2("Displaying histogram data"),
#             html.Br(),
#             dash_table.DataTable(
#                 data=histogram_kdf.to_dict('records'),
#                 columns=[{'name': i, 'id': i} for i in histogram_kdf.columns]
#             ),
#         ])


if __name__ == '__main__':
    app.run_server(debug=True, port=8001, host="172.29.131.64")