import uuid

import dash
from dash import dcc, html, Input, Output, State, MATCH, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly_express as px
import databricks.koalas as ks

from pyspark.sql import functions as f
import numpy as np

from utils.spark_utils import get_local_spark_session, with_std_column_names
from utils.deutils import run_profile
from utils.dash_utils import read_upload_into_pdf, read_upload_into_kdf, create_dynamic_card

spark = get_local_spark_session(app_name="Upload Application")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    requests_pathname_prefix="/upload/"
)

app.layout = dbc.Container([
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
    dbc.Container(id='displayAnalysis',children=[]),
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
            columns=[{'name': i, 'id': i} for i in pdf.columns],
            virtualization=True,
            fixed_rows={'headers': True},
            style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
            style_table={'height': 300}  # default is 500
            ),
        html.Br(),
        html.Button("Start Analysis", id="startAnalysis", n_clicks=0),
        html.H2(f"uid for this dataset is {uuid.uuid4().hex}"),
        ])


@app.callback(Output('displayAnalysis', 'children'),
              Input('startAnalysis', 'n_clicks'),
              State('upload-data', 'contents'),
              State('upload-data', 'filename'),
              )
def using_content_as_state(n_clicks, list_of_contents, list_of_names):
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
        profiled_df = run_profile(spark, sdf)

        histogram_sdf = profiled_df.\
            select(
            "column_name",
            f.explode("histogram").alias("histogram")
        ).selectExpr(
            "column_name",
            "histogram.value as value",
            "histogram.num_occurrences as num_occurrences",
            "histogram.ratio as ratio")

        histogram_kdf = histogram_sdf.to_koalas()
        histogram_pdf=histogram_kdf.to_pandas()

        summary_stats_sdf = profiled_df.drop("histogram")
        summary_stats_kdf = summary_stats_sdf.to_koalas()

        after_analysis_container = [
            dcc.Store(id='resultStore', data=histogram_pdf.to_dict('records')),
            html.Br(),
            dcc.Dropdown(id='columnsDropdown', options=[
                {'value': x, 'label': x} for x in set(histogram_pdf['column_name'])
            ], multi=True, value=[], disabled=False),
            dcc.Store(id='colsPrevSelected', data=[]),
            html.Br(),
            html.Div(id="myGraphCollections", children=[]),
        ]
        return after_analysis_container

'''
Create callbacks for the analysis bit
'''


@app.callback([Output('myGraphCollections', 'children'),
              Output('colsPrevSelected', 'data')],
              [Input('resultStore', 'data'),
              Input('columnsDropdown', 'value')],
              [State('colsPrevSelected', 'data'),
              State('myGraphCollections', 'children')],
              prevent_initial_call=True
              )
def on_data_set_graph(data_store, col_selected, cols_prev_selected, graphs_prev_displayed):
    if col_selected is None:
        raise PreventUpdate
    new_col = np.setdiff1d(col_selected, cols_prev_selected)

    if new_col.size > 0:
        new_graph=create_dynamic_card(data_store, new_col.tolist()[0])
        graphs_prev_displayed.insert(0, new_graph)
        return graphs_prev_displayed, col_selected
    else:
        col_selected.reverse()
        graphs = [create_dynamic_card(data_store, col) for col in col_selected]
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
        hole=0.7,
    )
    columns = [{"name": i, "id": i} for i in col_data_store[0].keys()]
    data = col_data_store
    # Conditional styling for the data table
    style_data_conditional=[
        {
            'if': {
                'column_id': 'column_name',
            },
            'hidden': 'True',
            'color': 'white'
        }
    ]
    return fig_pie, columns, data, style_data_conditional


if __name__ == '__main__':
    app.run_server(debug=True, port=8001, host="172.29.131.64")