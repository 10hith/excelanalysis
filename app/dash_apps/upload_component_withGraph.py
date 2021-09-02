import uuid

import dash
from dash import dcc, html, Input, Output, State, MATCH, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly_express as px
import databricks.koalas as ks
import timeit

from pyspark.sql import functions as f
import numpy as np

from utils.spark_utils import get_local_spark_session, with_std_column_names
from utils.deutils import run_profile
from utils.dash_utils import read_upload_into_pdf, read_upload_into_kdf, create_dynamic_card, row_col
from utils.spark_utils import SPARK as spark, SPARK_NUM_PARTITIONS
from utils.params import HOST

app = dash.Dash(
    __name__,
    title = "Excel-Analysis",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    requests_pathname_prefix="/upload/"
)

app.layout = dbc.Container([
    dbc.Row([
        html.Br()
    ]),
    dbc.Row([
        dbc.Col([
                dcc.Upload(
                id='uploadData',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                    ], className="display-4 mb-2 ")
                    )
        ], className='mh-100 border border-primary text-center mb-2 text-primary')
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='uploadSampleDisplay'),
        ])
    ]),
    dcc.Store(id='uploadSampleStore', data=[]),
    dcc.Store(id='profileResultStore', data=[]),
    dcc.Store(id='profileSummaryResultStore', data=[]),
    dbc.Container(id='displayProfileAnalysisActions',children=[]),
])


@app.callback(Output('uploadSampleStore', 'data'),
              inputs = dict(
                  upload_content = Input('uploadData', 'contents'),
                  upload_file_name = State('uploadData', 'filename'),
                  upload_modified_date = State('uploadData', 'last_modified')
              ),
                  prevent_initial_call=True
              )
def on_upload_store_sample(upload_content, upload_file_name, upload_modified_date):
    if upload_content is not None:
        try:
            pdf = read_upload_into_pdf(upload_content, upload_file_name)
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

    if upload_content is None:
        return []

    return pdf.head(100).to_dict('records')


@app.callback(Output('uploadSampleDisplay', 'children'),
              inputs = dict(upload_sample_store = Input('uploadSampleStore', 'data')),
              prevent_initial_call=True
              )
def on_data_display_sample(upload_sample_store):
    display_sample_div = html.Div([
        html.H2("Displaying first 100 records", className="text-primary text-center"),
        html.Br(),
        dash_table.DataTable(
            data=upload_sample_store,
            columns=[ {'name': i, 'id': i} for i in list(upload_sample_store[0].keys()) ],
            virtualization=True,
            fixed_rows={'headers': True},
            style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
            style_table={'height': 300},  # default is 500
            style_header={'color': 'text-primary'}
            ),
        html.Br(),
        html.Button("Start Analysis", id="startAnalysis", n_clicks=0, className="btn-primary"),
        html.H2(f"uid for this dataset is {uuid.uuid4().hex}"),
        ])
    return display_sample_div


@app.callback(Output('displayProfileAnalysisActions', 'children'),
              Input('startAnalysis', 'n_clicks'),
              State('uploadData', 'contents'),
              State('uploadData', 'filename'),
              )
def start_profile(n_clicks, list_of_contents, list_of_names):
    # Capturing the start time
    start = timeit.default_timer()
    if n_clicks>=1:
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

        # kdf = ks.from_pandas(kdf)
        kdf=ks.from_pandas(pdf)
        sdf_raw = kdf.to_spark()
        sdf = sdf_raw.transform(with_std_column_names())
        profiled_sdf = run_profile(spark, sdf)

        histogram_sdf = profiled_sdf.\
            select(
            "column_name",
            f.explode("histogram").alias("histogram")
        ).selectExpr(
            "column_name",
            "histogram.value as value",
            "histogram.num_occurrences as num_occurrences",
            "histogram.ratio as ratio")

        histogram_kdf = histogram_sdf.to_koalas()
        histogram_pdf = histogram_kdf.to_pandas()

        summary_stats_sdf = profiled_sdf.drop("histogram")
        summary_stats_kdf = summary_stats_sdf.to_koalas()
        summary_stats_pdf = summary_stats_kdf.to_pandas()

        # Capturing end time
        stop = timeit.default_timer()
        analysis_execution_time = stop - start

        profile_analysis_container = [
            dcc.Store(id='profileResultStore', data=histogram_pdf.to_dict('records')),
            dcc.Store(id='profileSummaryResultStore', data=summary_stats_pdf.to_dict('records')),
            dcc.Store(id='colsPrevSelected', data=[]),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.H3(f"Analysis completed in {analysis_execution_time} seconds; \
                    Number of spark partitions is {SPARK_NUM_PARTITIONS}"),
                    ]),
                ]),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.H3(f"Below is the summary stats for the dataframe"),
                    html.Br(),
                    dash_table.DataTable(
                        data=summary_stats_pdf.to_dict("records"),
                        columns=[{'name': i, 'id': i} for i in summary_stats_pdf.columns],
                        virtualization=True,
                        fixed_rows={'headers': True},
                        style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
                        style_table={'height': 300},  # default is 500
                        style_header={'color': 'text-primary'}
                    ),
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    html.H3(f"Select a column from the drop down to see the value distribution"),
                    ])
                ]),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id='columnsDropdown', options=[
                        {'value': x, 'label': x} for x in set(histogram_pdf['column_name'])
                    ], multi=True, value=[], disabled=False),
                    html.Br(),
                    ]),
                ]),
            dbc.Row([
                dbc.Col([
                    html.Div(id="myGraphCollections", children=[]),
                    ])
                ])
            ]
        return profile_analysis_container

'''
Create callbacks for the profiling
'''


@app.callback([Output('myGraphCollections', 'children'),
              Output('colsPrevSelected', 'data')],
              inputs=dict(
                  profile_result_store = Input('profileResultStore', 'data'),
                  col_selected = Input('columnsDropdown', 'value'),
                  cols_prev_selected = State('colsPrevSelected', 'data'),
                  graphs_prev_displayed = State('myGraphCollections', 'children')
              ),
              prevent_initial_call=True
              )
def on_profile_result_set_graph(profile_result_store, col_selected, cols_prev_selected, graphs_prev_displayed):
    if col_selected is None:
        raise PreventUpdate
    new_col = np.setdiff1d(col_selected, cols_prev_selected)

    if new_col.size > 0:
        new_graph=create_dynamic_card(profile_result_store, new_col.tolist()[0])
        graphs_prev_displayed.insert(0, new_graph)
        return graphs_prev_displayed, col_selected
    else:
        col_selected.reverse()
        graphs = [create_dynamic_card(profile_result_store, col) for col in col_selected]
        return graphs, col_selected


'''
Creating Dynamic components based on the column selection. This call back will occur
'''
@app.callback(
    [
        Output(component_id={'type': 'dynPieChart', 'index': MATCH}, component_property='figure'),
        Output(component_id={'type': 'dynDataTable', 'index': MATCH}, component_property='columns'),
        Output(component_id={'type': 'dynDataTable', 'index': MATCH}, component_property='data'),
        Output(component_id={'type': 'dynDataTable', 'index': MATCH}, component_property='style_data_conditional'),
        ],
    Input(component_id={'type': 'dynStore', 'index': MATCH}, component_property='data'),
)
def on_data_set_dyn_graph(col_data_store):
    fig_pie = px.pie(
        col_data_store,
        names="value",
        values="ratio",
        color="value",
        hole=0.6,
    )
    columns = [{"name": i, "id": i} for i in col_data_store[0].keys()]
    data = col_data_store
    # Conditional styling for the data table
    style_data_conditional=[
        {
            'if': {
                'column_id': 'column_name',
            },
            'hidden': 'False',
            'color': 'red'
        }
    ]
    return fig_pie, columns, data, style_data_conditional


if __name__ == '__main__':
    app.run_server(debug=True, port=8001, host=HOST)