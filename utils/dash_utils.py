import base64
from datetime import datetime
import io
import pandas as pd
from typing import List, Dict
import databricks.koalas as ks
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly_express as px


def read_upload_into_pdf(list_of_contents, list_of_names) -> pd.DataFrame:
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
        df: pd.DataFrame = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in list_of_names:
        # Assume that the user uploaded an excel file
        df: pd.DataFrame = pd.read_excel(io.BytesIO(decoded))

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


def create_dynamic_card(data_store: List[Dict], column_name: str) -> dbc.Card:
    """
    Creates a card block with tabs for bar chart, pie chart and a data table
    :param data_store: Data store containing the value distribution
    :param column_name: Column for which the card block will be created
    :return: A card block
    """
    col_data_store = [x for x in data_store if x["column_name"] == column_name]
    fig = px.bar(
        col_data_store,
        y="value",
        x="ratio",
        orientation='h',
        color="value",
        text='num_occurrences'
    )

    card = dbc.Card([
        html.H4(f"Distribution for Column - '{column_name}' ", className="card-title"),
        html.H6(f"Viz generated @ {datetime.now()}", className="card-subtitle"),
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(
                        label="View Bar Chart",
                        tab_id="tabBarChart",
                        children=[
                            html.Br(),
                            html.H6(f"Viz generated @ {datetime.now()}", className="card-subtitle"),
                            html.Br(),
                            dcc.Graph(
                            id={
                                'type': 'dynBarChart',
                                'index': column_name
                            },
                            figure=fig
                            )
                        ],
                    ),
                    dbc.Tab(
                        label="View Pie Chart",
                        tab_id="tabPieChart",
                        children=[
                            html.Br(),
                            html.Br(),
                            dcc.Graph(
                                id={
                                    'type': 'dynPieChart',
                                    'index': column_name
                                },
                            )
                        ],

                    ),
                    dbc.Tab(
                        label="View Data",
                        tab_id="tabData",
                        children=[
                            html.Br(),
                            html.Br(),
                            dash_table.DataTable(
                                id={
                                    'type': 'dynDataTable',
                                    'index': column_name
                                },
                                # columns=[{"name": i, "id": i} for i in col_data_store[0].keys()],
                                # data=col_data_store,
                            )
                        ],

                    ),
                ],
                active_tab="tabBarChart",
            )
        ),
        dbc.CardBody(
            id={
                'type': 'dynCardBody',
                'index': column_name
            },
        children=[
            dcc.Store(
                id={
                    'type': 'dynStore',
                    'index': column_name
                },
                data=col_data_store
            ),
        ]
    )],
    style={"width": "3"},
    )
    return card
