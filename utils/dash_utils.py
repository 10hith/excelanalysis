import base64
import io
import pandas as pd
from typing import List, Dict
import databricks.koalas as ks
from dash import dash_table
import dash_bootstrap_components as dbc
import plotly_express as px

from utils.spark_utils import cleanup_col_name


def row_col(list_of_components: List) -> dbc.Row:
    return dbc.Row([
        dbc.Col(
            list_of_components
        )
    ])


def get_graph_height(col_data_store: List[Dict]) -> int:
    calc_height = len(col_data_store) * 50
    if calc_height < 500:
        return 500
    elif calc_height > 2000:
        return 2000
    return calc_height


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
            'backgroundColor': '#7f7f7f',
            'color': 'white',
            'fontWeight': 'bold',
        },
        style_cell_conditional=[
         {
             'if': {'column_id': 'column_name'},
             'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
             'textAlign': 'left', 'fontWeight': 'bold'
         },
         {
            'if': {'column_id': 'num_distinct_values'},
            'minWidth': '90px', 'width': '90px', 'maxWidth': '90px',
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
                 'filter_query': '{completeness} < .10',
                 'column_id': 'completeness'
             },
             'color': 'red',
         }, {
             'if': {
                 'filter_query': '{column_type} = non_numeric',
             },
             'color': 'green',
         }
        ],
        style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
        style_table={'height': '300px', 'overflowY': 'auto'},  # default is 500,
        )
    return stats_data_table


def get_numeric_badges(col_summary_stat: Dict) -> List[dbc.Button]:
    standard_badge_styling = "ml-1 text-light"
    if col_summary_stat['column_type'] == 'numeric':
        return [
            dbc.Button(
                ["Max ",
                 dbc.Badge(f"{col_summary_stat['maximum']:.2f}", color="danger", className=standard_badge_styling)],
                color="light",
                className="m-1"
            ),
            dbc.Button(
                ["Min ",
                 dbc.Badge(f"{col_summary_stat['minimum']:.2f}", color="danger", className=standard_badge_styling)],
                color="light",
                className="m-1"
            ),
            dbc.Button(
                ["Mean ",
                 dbc.Badge(f"{col_summary_stat['mean']:.2f}", color="danger", className=standard_badge_styling)],
                color="light",
                className="m-1"
            ),
            dbc.Button(
                ["stdDev ",
                 dbc.Badge(f"{col_summary_stat['standard_deviation']:.2f}", color="danger", className=standard_badge_styling)],
                color="light",
                className="m-1"
            ),
        ]
    else:
        return []


def get_std_badges(col_summary_stat: Dict) -> List[dbc.Button]:
    num_nulls = (100 - col_summary_stat['completeness']*100)
    if num_nulls==int(num_nulls):
        print_num_nulls = f"{int(num_nulls)}"
    else:
        print_num_nulls = f"{num_nulls:.2f}"

    std_tiles = [dbc.Button(
        ["Unique value count ",
         dbc.Badge(f"{col_summary_stat['num_distinct_values']}", color="danger", className="ml-1 text-light")],
        color="light",
        className="m-1"
    ), dbc.Button(
        ["Nulls or blanks ",
         dbc.Badge(f"{print_num_nulls}%", color="danger",
                   )],
        color="light",
        className="m-1"
    )]
    return std_tiles


def get_crime_summary_graph(pdf):
    fig = px.histogram(
    pdf,
    x='crime_type',
    color="crime_type",
    text_auto='1s'
    )
    fig.update_layout(xaxis={'categoryorder':'total descending'}, uniformtext_minsize=8)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    return fig