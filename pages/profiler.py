import dash
dash.register_page(__name__,
                   path='/'
                   )

from dash import Dash, dcc, html, Input, Output, State, MATCH, dash_table, ALL, ALLSMALLER, callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash_labs as dl
import timeit
import numpy as np
import ast

from utils.dash_utils import read_upload_into_pdf, row_col, get_summary_stats_datatable
from utils.spark_utils import spark, SPARK_NUM_PARTITIONS, get_summary_and_histogram_dfs
from utils.aio_components import CreateDynamicCard
from utils.params import HOST
import visdcc
import dash_extensions as de
import time

# app = dash.Dash(
#     __name__,
#     title = "Excel-Analysis",
#     plugins=[dl.plugins.pages],
#     external_stylesheets=[dbc.themes.BOOTSTRAP],
#     suppress_callback_exceptions=True,
#     update_title='Job Running...',
#     meta_tags=[
#         {"name": "viewport", "content": "width=device-width, initial-scale=0.7"}
#     ],
#     # requests_pathname_prefix="/profile/",
# )

# profiler_page = [page for page in dash.page_registry.values() if page["module"]=='pages.profiler'][0]

# random_lottie = int(time.time())%15
# url = app.get_asset_url(path=f"{random_lottie}_lottie.json")
# options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))


layout = dbc.Container([
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
        , width={'size':12}, md={'size': 8, "offset": 2}
        ),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(''' *Please note the __max__ file size is* **10MB** '''),
        ], className="text-center"),
    ]),
    ],
        # no_gutters=True
    ),
    html.Br(),
    # html.Div(id="lottie_div_parent",
    #     children =[ html.Div(
    #             id='lottie_div', children=[
    #                 de.Lottie(id="lottie", title="loading dataset", options=options, width="30%", height="30%", url=url,
    #                           speed=1)],
    #             style={'display': 'none'},
    #         ),]
    #          , style={'display': 'block'}),
    html.Br(),
    # dcc.Store(id='profileResultStore', data=[]),
    # dcc.Store(id='profileSummaryResultStore', data=[]),
    dcc.Loading(
        id="loadingId",
        children=[html.Div(id='dummyDivForLoadingState', children=[])],
    ),
    html.Div(id='lottie_div_parent', children=[]),
    dbc.Container(
        id='displayProfileAnalysisActions',
        # children=[],
        # fluid=True
    ),
    # html.Div(id='dummyDivPreDef', children=[]),
    dbc.Row([
        dbc.Col(html.Br())
    ]),

],
)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Run Profiling
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


@callback([Output('displayProfileAnalysisActions', 'children'),
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

    summary_stats_pdf, histogram_pdf, ds_size, num_cat_cols = get_summary_and_histogram_dfs(pdf,spark)
    num_cols = summary_stats_pdf.shape[0]
    num_cont_cols = num_cols - num_cat_cols

    # Capturing end time
    stop = timeit.default_timer()
    analysis_execution_time = stop - start
    ext_link = 'https://pandas.pydata.org/pandas-docs/stable/user_guide/categorical.html'

    profile_analysis_container = [
        dcc.Store(id='profileResultStore', data=histogram_pdf.to_dict('records')),
        dcc.Store(id='profileSummaryResultStore', data=summary_stats_pdf.to_dict('records')),
        dcc.Store(id='colsPrevSelectedStore', data=[]),
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H4(f"Analysis completed in {analysis_execution_time} seconds; \
                Number of spark partitions is {SPARK_NUM_PARTITIONS}",
                        className="text-info"),
                ],
            ),
            ]),
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H4(children=[
                    # html.A("Link to external site", href='https://plot.ly', target="_blank")
                    dcc.Markdown(
                        f''' '{upload_file_name}' contains 
                        ***```{ds_size}```*** records and 
                        ***```{num_cols}```*** columns(
                        .''',
                                 className="text-info"),

                ]),
                ]),
            ]),
        dbc.Row([
            dbc.Col([
                dcc.Markdown(f''' `{num_cat_cols}` '''),
                html.A('Categorical', href='{ext_link}', target="_blank")
                ], width={'order': '1'}
            ),
            dbc.Col(
                # dcc.Markdown(f''' `{num_cat_cols}` '''), width={'order': '1'}
            )
        ]),
        dbc.Row([
            dbc.Col([
                html.H3(f"Below is the summary stats for the dataframe",
                        className="text-info"),
                get_summary_stats_datatable(summary_stats_pdf),
                html.Br(),
            ])
        ]),
        row_col([html.Br()]),
        dbc.Row([
            dbc.Col([
                html.H3(f"Select a column from the drop down to see the value distribution", className="text-primary"),
                ],
            )
            ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='columnsDropdown', options=[
                    {'value': x, 'label': x} for x in set(histogram_pdf['column_name'])
                    ],
                    multi=True, value=[], disabled=False, placeholder="Select a column to see the distribution",
                    className="border border-3 border-primary"),
                html.Br(),
                ],
            ),
            ],
            # no_gutters=True
        ),
        dbc.Row([
            dbc.Col([
                html.Div(id="myGraphCollections", children=[]),
                ],
            )
            ],
            # no_gutters=True
        )
        ]
    return profile_analysis_container, [], {'display': 'none'}

#
# @callback(Output('lottie_div', 'style'),
#               inputs = dict(
#                 upload_content = Input('uploadData', 'filename'),
#               ),
#               prevent_initial_call=True
#               )
# def run_lottie_animation(upload_content):
#     return {'display': 'block'}


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Create callbacks for the profiling
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


@callback(Output('myGraphCollections', 'children'),
              Output('colsPrevSelectedStore', 'data'),
              inputs=dict(
                  profile_result_store = Input('profileResultStore', 'data'),
                  col_selected = Input('columnsDropdown', 'value'),
                  cols_prev_selected = State('colsPrevSelectedStore', 'data'),
                  graphs_prev_displayed = State('myGraphCollections', 'children'),
                  profile_summary_result_store = State('profileSummaryResultStore', 'data'),
              ),
              prevent_initial_call=True
              )
def on_profile_result_set_graph(
        profile_result_store,
        col_selected,
        cols_prev_selected,
        graphs_prev_displayed,
        profile_summary_result_store
):
    new_col = np.setdiff1d(col_selected, cols_prev_selected)

    if new_col.size > 0:
        new_graph=CreateDynamicCard(profile_result_store, profile_summary_result_store, new_col.tolist()[0], aio_id=new_col.tolist()[0])
        graphs_prev_displayed.insert(0, new_graph)
        return graphs_prev_displayed, col_selected
    else:
        col_selected.reverse()
        graphs = [CreateDynamicCard(profile_result_store, profile_summary_result_store, col, aio_id=col) for col in col_selected]
        return graphs, col_selected


@callback(
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
@callback(
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


# if __name__ == '__main__':
#     app.run_server(debug=True, port=8003, host=HOST)