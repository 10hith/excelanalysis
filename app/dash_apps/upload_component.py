import dash
from dash import dcc, html, Input, Output, State, MATCH, dash_table, ALL, ALLSMALLER
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly_express as px
import timeit
from databricks import koalas as ks
from pyspark.sql import functions as f
import numpy as np
import ast

from utils.deutils import run_profile
from utils.dash_utils import read_upload_into_pdf, create_dynamic_card, row_col
from utils.spark_utils import SPARK_NUM_PARTITIONS, spark
from utils.params import HOST
import visdcc
from utils.aio_components import CreateDynamicCard

app = dash.Dash(
    __name__,
    title = "Excel-Analysis",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    # meta_tags=[
    #     {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    # ],
    requests_pathname_prefix="/upload/"
)

app.layout = dbc.Container([
    dbc.Row([
        html.Br()
    ]),
    visdcc.Run_js(id = 'jsScrollDDSelect'),
    dbc.Row([
        dbc.Col([
                dcc.Upload(
                id='uploadData',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                    ], className="display-4 mb-2 "),
                max_size=15000000,
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
    dcc.Loading(html.Div(id='dummyDivForLoadingState', children=[])),
    dbc.Container(id='displayProfileAnalysisActions', children=[]),
    html.Div(id='dummyDivPreDef', children=[]),
    dbc.Row([
        dbc.Col(html.Br())
    ]),
    dbc.Row([
        dbc.Col(html.Br())
    ]),
    dbc.Row([
        dbc.Col(html.Br())
    ]),
    dbc.Row([
        dbc.Col(html.Br())
    ]),
])

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Uploading the sample
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


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
            pdf = read_upload_into_pdf(upload_content, upload_file_name, 100)
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

    if upload_content is None:
        return []

    return pdf.head(100).to_dict('records')


@app.callback(Output('uploadSampleDisplay', 'children'),
              inputs = dict(
                  upload_sample_store = Input('uploadSampleStore', 'data'),
                  upload_file_name = State('uploadData', 'filename')
              ),
              prevent_initial_call=True
              )
def on_data_display_sample(upload_sample_store, upload_file_name):
    display_sample_div = dbc.Container([
        html.Br(),
        row_col([html.H2(f"Displaying first 100 records of file '{upload_file_name}' ")]),
        html.Br(),
        row_col([dash_table.DataTable(
            data=upload_sample_store,
            columns=[ {'name': i, 'id': i} for i in list(upload_sample_store[0].keys()) ],
            tooltip_header = [dict((f'{x}', x) for x in list(upload_sample_store[0].keys()))][0],
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in upload_sample_store
            ],
            virtualization=True,
            fixed_rows={'headers': True},
            style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
            style_table={'height': 300},  # default is 500
            style_header={'color': 'text-primary'}
            )]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Button("Start Data Profile", id="startAnalysis", n_clicks=0, className="btn-primary"),
                ]),
            ]),
        html.Br()
        ])
    return display_sample_div


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Run Profiling
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


@app.callback(Output('startAnalysis', 'disabled'),
              Output('startAnalysis', 'style'),
              Input('startAnalysis', 'n_clicks'),
              prevent_initial_call=True
              )
def disable_start_button(n_clicks):
    if n_clicks>=1:
        return True, dict(display='none')
    return False, dict()


@app.callback([Output('displayProfileAnalysisActions', 'children'),
               Output('dummyDivForLoadingState', 'children')],
              [Input('startAnalysis', 'n_clicks'),
               State('uploadData', 'contents'),
               State('uploadData', 'filename'),
               ],
              prevent_initial_call=True
              )
def start_profile(n_clicks, upload_content, upload_filename):
    # Capturing the start time
    start = timeit.default_timer()
    if n_clicks>=1:
        if upload_content is not None:
            try:
                pdf = read_upload_into_pdf(upload_content, upload_filename)
            except Exception as e:
                print(e)
                return html.Div([
                    'There was an error processing this file.'
                ]), []

        if upload_content is None:
            return html.Div([]), []

        kdf = ks.from_pandas(pdf)
        sdf = kdf.to_spark()

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

        summary_stats_sdf = profiled_sdf.drop("histogram")

        summary_stats_pdf = summary_stats_sdf.toPandas()
        histogram_pdf = histogram_sdf.toPandas()

        # Capturing end time
        stop = timeit.default_timer()
        analysis_execution_time = stop - start

        profile_analysis_container = [
            dcc.Store(id='profileResultStore', data=histogram_pdf.to_dict('records')),
            dcc.Store(id='profileSummaryResultStore', data=summary_stats_pdf.to_dict('records')),
            dcc.Store(id='colsPrevSelectedStore', data=[]),
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
                    dash_table.DataTable(id="profileSummary",
                        data=summary_stats_pdf.to_dict("records"),
                        columns=[{'name': i, 'id': i} for i in summary_stats_pdf.columns],
                        virtualization=True,
                        fixed_rows={'headers': True},
                        style_data_conditional=[
                            {
                                'if': {
                                    'filter_query': '{completeness} > .98',
                                    'column_id': 'completeness'
                                },
                                'color': 'green',
                                'fontWeight': 'bold'
                            }, {
                                'if': {
                                    'filter_query': '{column_type} = non_numeric',
                                },
                                'color': 'green',
                                'fontWeight': 'bold'
                            }
                        ],
                        style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
                        style_table={'height': 300},  # default is 500
                        style_header={'color': 'text-primary'}
                    ),
                ]),
            ]),
            row_col([html.Br()]),
            row_col([html.Br()]),
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
        return profile_analysis_container, []
    raise PreventUpdate


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Create callbacks for the profiling
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


@app.callback(Output('myGraphCollections', 'children'),
              Output('colsPrevSelectedStore', 'data'),
              inputs=dict(
                  profile_result_store = Input('profileResultStore', 'data'),
                  col_selected = Input('columnsDropdown', 'value'),
                  cols_prev_selected = State('colsPrevSelectedStore', 'data'),
                  graphs_prev_displayed = State('myGraphCollections', 'children')
              ),
              prevent_initial_call=True
              )
def on_profile_result_set_graph(
        profile_result_store,
        col_selected,
        cols_prev_selected,
        graphs_prev_displayed
):
    # if col_selected is None:
    #     raise PreventUpdate

    new_col = np.setdiff1d(col_selected, cols_prev_selected)

    if new_col.size > 0:
        # new_graph=create_dynamic_card(profile_result_store, new_col.tolist()[0])
        new_graph=CreateDynamicCard(profile_result_store, new_col.tolist()[0], aio_id=new_col.tolist()[0])
        graphs_prev_displayed.insert(0, new_graph)
        return graphs_prev_displayed, col_selected
    else:
        col_selected.reverse()
        # graphs = [create_dynamic_card(profile_result_store, col) for col in col_selected]
        graphs = [CreateDynamicCard(profile_result_store, col, aio_id=col) for col in col_selected]
        return graphs, col_selected


'''
Creating Dynamic components based on the column selection. This call back will occur
'''
# @app.callback(
#     [
#         Output(component_id={'type': 'dynPieChart', 'index': MATCH}, component_property='figure'),
#         Output(component_id={'type': 'dynDataTable', 'index': MATCH}, component_property='columns'),
#         Output(component_id={'type': 'dynDataTable', 'index': MATCH}, component_property='data'),
#         Output(component_id={'type': 'dynDataTable', 'index': MATCH}, component_property='style_data_conditional'),
#         ],
#     Input(component_id={'type': 'dynStore', 'index': MATCH}, component_property='data'),
# )
# def on_data_set_dyn_graph(col_data_store):
#     fig_pie = px.pie(
#         col_data_store,
#         names="value",
#         values="ratio",
#         color="value",
#         hole=0.6,
#     )
#     columns = [{"name": i, "id": i} for i in col_data_store[0].keys()]
#     data = col_data_store
#     # Conditional styling for the data table
#     style_data_conditional=[
#         {
#             'if': {
#                 'column_id': 'column_name',
#             },
#             'hidden': 'False',
#             'color': 'red'
#         }
#     ]
#     return fig_pie, columns, data, style_data_conditional


@app.callback(
    Output('jsScrollDDSelect', 'run'),
    inputs = dict(
        scroll_btn_click=Input(
            component_id={'component': 'CreateDynamicCard', 'subcomponent': 'scrollTop', 'aio_id': ALL},
            component_property='n_clicks')
    ),
         prevent_initial_call = True
)
def scroll_to_top(scroll_btn_click):
    ctx = dash.callback_context

    if ctx.triggered[0]['value'] is None:
        raise PreventUpdate

    if ctx.triggered[0]['value'] >= 1:
        return "window.scrollTo(0,0)"
    return ""

# '''
# Close button using click context
# '''
@app.callback(
    Output('columnsDropdown', 'value'),
    inputs = dict(
        # close_btn = Input(component_id={'type': 'closeBtn', 'index': ALL}, component_property='n_clicks'),
        close_btn_click = Input(
            component_id={'component': 'CreateDynamicCard', 'subcomponent': 'closeBtn','aio_id': ALL},
            component_property='n_clicks'),
        dropdown_values = State('columnsDropdown', 'value'),
    ),
    prevent_initial_call=True
)
def update_dropdown(close_btn_click, dropdown_values):
    # Capture the callback context state
    ctx = dash.callback_context

    if ctx.triggered[0]['value'] is None:
        raise PreventUpdate

    if ctx.triggered[0]['value']>=1:
        ctx = dash.callback_context
        component = ctx.triggered[0]['prop_id']
        component_key_dict = ast.literal_eval(component.split('.')[0])
        column_removed = component_key_dict['aio_id']
        return [x for x in dropdown_values if column_removed not in x]

    return dropdown_values


if __name__ == '__main__':
    app.run_server(debug=True, port=8002, host=HOST)