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
from utils.aio_components import CreateDynamicCard
from utils.params import HOST
import visdcc
import dash_extensions as de
import time


app = dash.Dash(
    __name__,
    title = "Excel-Analysis",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    update_title='Job Running...',
    # meta_tags=[
    #     {"name": "viewport", "content": "width=device-width, initial-scale=0.8"}
    # ],
    requests_pathname_prefix="/new_upload/",
)

# Lottie Setup
# url="https://assets9.lottiefiles.com/packages/75244-analyse.json"
random_lottie = int(time.time())%15
url = app.get_asset_url(f"{random_lottie}_lottie.json")
# url = "https://assets9.lottiefiles.com/packages/lf20_YXD37q.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))


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
                max_size=100000000,
            )
        ], className='mh-100 border border-primary text-center mb-2 text-primary'
        , width={'size':112}, md={'size': 8, "offset": 2}
        )
    ], no_gutters=True),
    html.Br(),
    html.Div(id="lottie_div_parent",
        children =[ html.Div(
                id='lottie_div', children=[
                    de.Lottie(id="lottie", title="loading dataset", options=options, width="30%", height="30%", url=url,
                              speed=1)],
                style={'display': 'none'},
            ),]
             , style={'display': 'block'}),
    html.Br(),
    dcc.Store(id='profileResultStore', data=[]),
    dcc.Store(id='profileSummaryResultStore', data=[]),
    dcc.Loading(
        id="loadingId",
        children=[html.Div(id='dummyDivForLoadingState', children=[])],
    ),
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
Run Profiling
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


@app.callback([Output('displayProfileAnalysisActions', 'children'),
               Output('dummyDivForLoadingState', 'children'),
               Output('lottie_div_parent', 'style')],
                inputs = dict(
                  upload_content = Input('uploadData', 'contents'),
                  upload_file_name = State('uploadData', 'filename'),
              ),
                prevent_initial_call=True
              )
def start_profile(upload_content, upload_file_name):
    # Capturing the start time
    start = timeit.default_timer()
    if upload_content is not None:
        try:
            pdf = read_upload_into_pdf(upload_content, upload_file_name)
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
                ],
                width={'size': 10}, md={'size': 8, "offset": 2}
            ),
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
            ],
            width={'size': 10}, md={'size': 8, "offset": 2}
            ),
        ]),
        row_col([html.Br()]),
        row_col([html.Br()]),
        dbc.Row([
            dbc.Col([
                html.H3(f"Select a column from the drop down to see the value distribution"),
                ],
                width={'size': 10}, md={'size': 8, "offset": 2}
            )
            ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='columnsDropdown', options=[
                    {'value': x, 'label': x} for x in set(histogram_pdf['column_name'])
                ], multi=True, value=[], disabled=False),
                html.Br(),
                ],
                width={'size': 10}, md={'size': 8, "offset": 2}
            ),
            ], no_gutters=True),
        dbc.Row([
            dbc.Col([
                html.Div(id="myGraphCollections", children=[]),
                ],
                width={'size': 10}, md={'size': 8, "offset": 2}
            )
            ], no_gutters=True)
        ]
    return profile_analysis_container, [], {'display': 'none'}


@app.callback(Output('lottie_div', 'style'),
              inputs = dict(
                upload_content = Input('uploadData', 'filename'),
              ),
              prevent_initial_call=True
              )
def run_lottie_animation(upload_content):
    return {'display': 'block'}


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