import base64
from datetime import datetime
import io
import pandas as pd
from typing import List, Dict
import databricks.koalas as ks
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly_express as px
import plotly.graph_objs as gobjs

from utils.spark_utils import cleanup_col_name


def row_col(list_of_components: List) -> dbc.Row:
    return dbc.Row([
        dbc.Col(
            list_of_components
        )
    ])


def read_upload_into_pdf(list_of_contents, list_of_names, num_sample_records=None) -> pd.DataFrame:
    """
    Parsing the file
    :param list_of_contents:
    :param list_of_names:
    :param num_sample_records:
    :return: Returns a html div
    """
    content_type, content_string = list_of_contents.split(',')

    decoded = base64.b64decode(content_string)
    if 'csv' in list_of_names:
        # Assume that the user uploaded a CSV file
        df: pd.DataFrame = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')), nrows=num_sample_records)
    elif 'xls' in list_of_names:
        # Assume that the user uploaded an excel file
        df: pd.DataFrame = pd.read_excel(io.BytesIO(decoded), nrows=num_sample_records)

    # Cleanup column names
    cols = df.columns
    col_rename_list = [cleanup_col_name(col) for col in cols]
    df.rename(columns=dict(col_rename_list), inplace=True)
    return df


def read_upload_into_kdf(list_of_contents, list_of_names) -> pd.DataFrame:
    """
    Parsing the file
    :param list_of_contents:
    :param list_of_names:
    :param date:
    :return: Returns a html div
    """
    content_type, content_string = list_of_contents.split(',')

    decoded = base64.b64decode(content_string)
    if 'csv' in list_of_names:
        # Assume that the user uploaded a CSV file
        df: ks.DataFrame = ks.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in list_of_names:
        # Assume that the user uploaded an excel file
        df: ks.DataFrame = ks.read_excel(io.BytesIO(decoded))

    return df


def get_summary_stats_datatable(summary_stats_pdf: pd.DataFrame) -> dash_table.DataTable:
    stats_data_table = dash_table.DataTable(
        id="profileSummary",
        data=summary_stats_pdf.to_dict("records"),
        columns=[{'name': i, 'id': i} for i in summary_stats_pdf.columns],
        tooltip_header=
        [dict((f'{x}', x) for x in list(summary_stats_pdf.to_dict("records")[0].keys()))][0],
        tooltip_data=[
         {
             column: {'value': str(value), 'type': 'markdown'}
             for column, value in row.items()
         } for row in summary_stats_pdf.to_dict("records")
        ],
        virtualization=True,
        fixed_rows={'headers': True},
        filter_action="native",
        sort_action="native",
        style_header={
         'color': 'blue',
         'fontWeight': 'bold',
        },
        style_cell_conditional=[
         {
             'if': {'column_id': 'column_name'},
             'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
             'textAlign': 'left', 'fontWeight': 'bold'
         },
        ],
        style_data_conditional=[
         {
             'if': {
                 'filter_query': '{completeness} > .98',
                 'column_id': 'completeness'
             },
             'color': 'green',
         }, {
             'if': {
                 'filter_query': '{column_type} = non_numeric',
             },
             'color': 'green',
         }
        ],
        style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
        style_table={'height': 500},  # default is 500
        )
    return stats_data_table




# def get_bar_chart(col_data_store: List[Dict], aio_id: str):
#     fig = px.bar(
#         col_data_store,
#         y="value",
#         x="percentage",
#         orientation='h',
#         color="value",
#         # text='num_occurrences',
#         labels={
#             "value": "Categories"
#         },
#         hover_name='value_complete',
#         hover_data=['percentage']
#     )
#
#     fig.update_layout(
#         title={
#             'text': f"Value Distribution - '{aio_id}'",
#             'y': 0.95,
#             'x': 0.4,
#             'xanchor': 'center',
#             'yanchor': 'top'
#         },
#         # autosize=False,
#         title_font_color='#800000',
#         xaxis_title="Percentage Of Records",
#         yaxis_title="Categories Values",
#         legend_title="Categories",
#         yaxis_automargin=True,
#         yaxis_autorange=True,
#         # paper_bgcolor="LightSteelBlue",
#     )
#     return fig
#
#
# def get_pie_chart(col_data_store: List[Dict], column_name: str):
#     fig_pie = px.pie(
#         col_data_store,
#         names="value",
#         values="percentage",
#         color="value",
#         hole=0.6,
#         hover_name='value_complete'
#     )
#     fig_pie.update_layout(
#         title={
#             'text': f"Value Distribution - '{column_name}'",
#             'y': 0.95,
#             'x': 0.4,
#             'xanchor': 'center',
#             'yanchor': 'top'
#         },
#         title_font_color='blue',
#         legend_title="Categories",
#     )
#
#
# def create_dynamic_card(data_store: List[Dict], column_name: str) -> dbc.Card:
#     """
#     Creates a card block with tabs for bar chart, pie chart and a data table
#     :param data_store: Data store containing the value distribution
#     :param column_name: Column for which the card block will be created
#     :return: A card block
#     """
#     col_data_store = [x for x in data_store if x["column_name"] == column_name]
#     fig = px.bar(
#         col_data_store,
#         y="value",
#         x="ratio",
#         orientation='h',
#         color="value",
#         text='num_occurrences'
#     )
#
#     card = dbc.Card([
#         html.H4(f"Distribution for Column - '{column_name}' ", className="card-title"),
#         html.H6(f"Viz generated @ {datetime.now()}", className="card-subtitle"),
#         dbc.Row([
#             dbc.Col([
#                 html.Div(id={
#                     'type': 'dummyDiv',
#                     'index': column_name
#                 }, children=[]),
#                 dbc.Button(
#                     id={
#                         'type': 'scrollTop',
#                         'index': column_name
#                     }, children="Scroll to top", n_clicks=0, className="btn-close btn btn-success"),
#                 dbc.Button(
#                     id={
#                         'type': 'closeBtn',
#                         'index': column_name
#                     }, children="X", n_clicks=0, className="btn-close btn btn-danger"),
#             ],
#                 width={"size": 3, "order": "last"}, md={"size": 3, "order": "last"},
#                 align="end"
#             ),
#         ], justify="end"),
#         dbc.Row([
#             dbc.Col([
#                 dbc.CardHeader(
#                     dbc.Tabs(
#                         [
#                             dbc.Tab(
#                                 label="View Bar Chart",
#                                 tab_id="tabBarChart",
#                                 children=[
#                                     html.Br(),
#                                     html.H6(f"Viz generated @ {datetime.now()}", className="card-subtitle"),
#                                     html.Br(),
#                                     dcc.Graph(
#                                     id={
#                                         'type': 'dynBarChart',
#                                         'index': column_name
#                                     },
#                                     figure=fig
#                                     )
#                                 ],
#                             ),
#                             dbc.Tab(
#                                 label="View Pie Chart",
#                                 tab_id="tabPieChart",
#                                 children=[
#                                     html.Br(),
#                                     html.Br(),
#                                     dcc.Graph(
#                                         id={
#                                             'type': 'dynPieChart',
#                                             'index': column_name
#                                         },
#                                     )
#                                 ],
#
#                             ),
#                             dbc.Tab(
#                                 label="View Data",
#                                 tab_id="tabData",
#                                 children=[
#                                     html.Br(),
#                                     html.Br(),
#                                     dash_table.DataTable(
#                                         id={
#                                             'type': 'dynDataTable',
#                                             'index': column_name
#                                         },
#                                     )
#                                 ],
#
#                             ),
#                         ],
#                         active_tab="tabBarChart",
#                     )
#                 ),
#                 ], )
#         ]),
#         dbc.CardBody(
#             id={
#                 'type': 'dynCardBody',
#                 'index': column_name
#             },
#         children=[
#             dcc.Store(
#                 id={
#                     'type': 'dynStore',
#                     'index': column_name
#                 },
#                 data=col_data_store
#             ),
#         ]
#     )],
#     style={"width": "2"},
#     )
#     return card
