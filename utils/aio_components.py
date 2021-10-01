from dash import Dash, Output, Input, State, html, dcc, callback, MATCH
import uuid
from datetime import datetime
import dash_bootstrap_components as dbc
from dash import dcc, dash_table
from typing import List, Dict
import plotly_express as px
import dash_extensions as de
from dash_extensions.snippets import send_bytes
import pandas as pd
import plotly.graph_objects as go
from utils.dash_utils import row_col

class CreateDynamicCard(html.Div):
    # A set of functions that create pattern-matching callbacks of the sub-components
    class ids:
        showParentCard = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'parentCard', 'aio_id': aio_id}
        parentCardCollapse = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'parentCardCollapse', 'aio_id': aio_id}
        scrollTop = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'scrollTop', 'aio_id': aio_id}
        closeBtn = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'closeBtn', 'aio_id': aio_id}
        dynBarChart = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'dynBarChart', 'aio_id': aio_id}
        dynPieChart = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'dynPieChart', 'aio_id': aio_id}
        dynDataTable = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'dynDataTable', 'aio_id': aio_id}
        dataTablePh =  lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'dataTablePh', 'aio_id': aio_id}
        dynStore = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'dynStore', 'aio_id': aio_id}
        downloadDataButton = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'downloadDataButton', 'aio_id': aio_id}
        downloadDataUtil =  lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'downloadDataUtil', 'aio_id': aio_id}
        downloadBarButton =  lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'downloadBarButton', 'aio_id': aio_id}
        downloadBarUtil =  lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'downloadBarUtil', 'aio_id': aio_id}
        downloadPieButton = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'downloadPieButton', 'aio_id': aio_id}
        downloadPieUtil = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'downloadPieUtil', 'aio_id': aio_id}
        showSummaryTile =  lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'collapseBtn', 'aio_id': aio_id}
        summaryTileCollapse = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'collapseUtil', 'aio_id': aio_id}


    # Make the ids class a public class
    ids = ids

    # Define the arguments of the All-in-One component
    def __init__(
        self,
        data_store: List[Dict],
        summary_stats_store: List[Dict],
        column_name: str,
        aio_id = None
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        # Filter the datastore and create the first graph
        col_data_store = [x for x in data_store if x["column_name"] == column_name]

        fig = px.bar(
            col_data_store,
            y="value",
            x="percentage",
            orientation='h',
            color="value",
            # text='num_occurrences',
            labels={
                "value": "Categories"
            },
            hover_name='value_complete',
            hover_data=['percentage']
            # hovertemplate="%{value_complete}"
        )

        fig.update_layout(
            title={
                'text': f"Value Distribution - '{aio_id}'",
                'y': 0.95,
                'x': 0.4,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            # autosize=False,
            title_font_color='#800000',
            xaxis_title="Percentage Of Records",
            yaxis_title="Categories Values",
            legend_title="Categories",
            yaxis_automargin=True,
            yaxis_autorange=True,
            # paper_bgcolor="LightSteelBlue",
        )
        #############################
        # Creating the summary tile
        #############################

        col_summary_stat = [x for x in summary_stats_store if x["column_name"] == column_name][0]

        print(type(col_summary_stat))
        print(f"num_distinct_values is {col_summary_stat['num_distinct_values']}")
        print(f"completeness is {col_summary_stat['completeness']}")
        print(f"column_type is {col_summary_stat['column_type']}")

        tiles = [
            dbc.Button(
                ["approx unique values", dbc.Badge(f"{col_summary_stat['num_distinct_values']}", color="dark", className="ml-1")],
                color="warning",
                className="m-1 btn-sm"
            ),
            dbc.Button(
                ["Nulls",
                 dbc.Badge(f"{1 - int(col_summary_stat['completeness'])}%", color="dark", className="ml-1 text-secondary")],
                color="danger",
                className="m-1 btn-sm"
            ),
            dbc.Button(
                ["Data Type",
                 dbc.Badge(f"{col_summary_stat['column_type']}", color="danger", className="ml-1 text-dark")],
                color="light",
                className="m-1 btn-sm"
            )
            ]


        # Define the component's layout
        super().__init__([
            dbc.Card([
                html.H4(f"Distribution for Column - '{column_name}' ", className="card-title"),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Button(
                            id=self.ids.closeBtn(aio_id), children="X", n_clicks=0,
                            className="m-0 border border-dark btn-close btn btn-danger float-right btn-sm"),
                        dbc.Button(
                            id=self.ids.scrollTop(aio_id), children="^", n_clicks=0,
                            className="m-0 border border-dark btn-close btn btn-success float-right btn-sm"),
                        dbc.Button(
                            "View Summary",
                            id=self.ids.showSummaryTile(aio_id),
                            className="m-0 border border-dark btn-close btn btn-info float-right btn-sm", n_clicks=0),
                    ],
                    ),
                ],
                    justify="end"
                ),
                dbc.Collapse(
                    dbc.Row([
                        dbc.Col(tiles, width={"order": 1, "offset": 1}),
                    ]),
                    id=self.ids.summaryTileCollapse(aio_id),
                    is_open=False
                ),
                dbc.Row([
                    dbc.Col([
                        dbc.CardHeader(
                            dbc.Tabs(
                                [
                                    dbc.Tab(
                                        label="View Bar Chart",
                                        tab_id="tabBarChart",
                                        children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Button(
                                                        "Download graph as Image",
                                                        id=self.ids.downloadBarButton(aio_id),
                                                        n_clicks=0
                                                        , className="btn btn-info float-right btn-sm"),
                                                    de.Download(id=self.ids.downloadBarUtil(aio_id)),
                                                    html.Br(),
                                                ],
                                                ),
                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.Graph(id=self.ids.dynBarChart(aio_id),
                                                              figure=fig,
                                                              config={
                                                                  "displaylogo": False,
                                                                  "modeBarButtonsToRemove": ['toImage']
                                                              }
                                                              )
                                                ])
                                            ]),
                                        ],
                                    ),
                                    dbc.Tab(
                                        label="View Pie Chart",
                                        tab_id="tabPieChart",
                                        children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Button(
                                                        "Download graph as Image",
                                                        id=self.ids.downloadPieButton(aio_id),
                                                        n_clicks=0
                                                        , className="btn btn-info float-right btn-sm"),
                                                    de.Download(id=self.ids.downloadPieUtil(aio_id)),
                                                    html.Br(),
                                                ],
                                                ),
                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.Graph(id=self.ids.dynPieChart(aio_id),
                                                              config={
                                                                  "displaylogo": False,
                                                                  "modeBarButtonsToRemove": ['toImage']
                                                              }),
                                                ])
                                            ]),

                                        ],

                                    ),
                                    dbc.Tab(
                                        label="View Data",
                                        tab_id="tabData",
                                        children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Button(
                                                        f"Download data as Excel",
                                                        id=self.ids.downloadDataButton(aio_id),
                                                        n_clicks=0
                                                        , className="btn btn-info float-right btn-sm"),
                                                    de.Download(id=self.ids.downloadDataUtil(aio_id)),
                                                    html.Br(),
                                                ],
                                                ),
                                            ]),
                                            dbc.Row([
                                                dbc.Col([html.Div(id=self.ids.dataTablePh(aio_id), children=[])
                                                         ],
                                                        )
                                            ]),
                                        ],
                                    ),
                                ],
                                active_tab="tabBarChart",
                            )
                        ),
                    ], )
                ]),
                dbc.CardBody(
                    children=[
                        dcc.Store(id=self.ids.dynStore(aio_id), data=col_data_store),
                    ]
                )],
                style={"width": "2"},
            ),
            ])

    # Define CallBacks
    @callback(
        [
            Output(ids.dynPieChart(MATCH), 'figure'),
            Output(ids.dataTablePh(MATCH), 'children'),
            ],
        Input(ids.dynStore(MATCH), 'data'),
        State(ids.dynStore(MATCH), 'id')
    )
    def on_data_set_dyn_graph(col_data_store, id):
        fig_pie = px.pie(
            col_data_store,
            names="value",
            values="percentage",
            color="value",
            hole=0.6,
            hover_name='value_complete'
        )
        column_name = id['aio_id']

        fig_pie.update_layout(
            title={
                'text': f"Value Distribution - '{column_name}'",
                'y': 0.95,
                'x': 0.4,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            title_font_color='blue',
            legend_title="Categories",
        )

        col_data_store_clean = col_data_store
        [d.pop('value') for d in col_data_store_clean]

        dyn_data_table=dash_table.DataTable(
            data=col_data_store_clean,
            columns=[{'name': i, 'id': i} for i in list(col_data_store_clean[0].keys())],
            tooltip_header=[dict((f'{x}', x) for x in list(col_data_store_clean[0].keys()))][0],
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in col_data_store_clean
            ],
            fixed_rows={'headers': True},
            style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
            style_table={'height': 300},  # default is 500
            style_header={'color': 'blue'}
        )

        return fig_pie, dyn_data_table


    @callback(
        Output(ids.downloadDataUtil(MATCH), "data"),
        inputs=dict(
            n_clicks=Input(ids.downloadDataButton(MATCH), "n_clicks"),
            id=State(ids.downloadDataButton(MATCH), "id"),
            column_data=State(ids.dynStore(MATCH), 'data'),
        ),
        prevent_initial_call=True
    )
    def generate_xlsx(n_clicks, id, column_data):
        def to_xlsx(bytes_io):
            df = pd.DataFrame(column_data)
            xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")
            df.to_excel(xslx_writer, index=False, sheet_name="sheet1")
            xslx_writer.save()
        column_name = id['aio_id']
        return send_bytes(to_xlsx, f"{column_name}.xlsx")

    @callback(
        Output(ids.downloadBarUtil(MATCH), "data"),
        Input(ids.downloadBarButton(MATCH), "n_clicks"),
        State(ids.downloadBarUtil(MATCH), "id"),
        State(ids.dynBarChart(MATCH), 'figure'),
        prevent_initial_call=True
    )
    def download_bar_png(n_nlicks, id, fig):

        column_name = id['aio_id']
        f = go.Figure(fig,
                      # layout=go.Layout(title=go.layout.Title(text=f"Value ONLYGraphs Distribution - '{column_name}'"))
                      layout=dict(title=dict(text="A Figure Specified By A Graph Object"))
                      )
        return send_bytes(f.write_image, f"{column_name}.png")

    @callback(
        Output(ids.downloadPieUtil(MATCH), "data"),
        Input(ids.downloadPieButton(MATCH), "n_clicks"),
        State(ids.downloadPieButton(MATCH), "id"),
        State(ids.dynPieChart(MATCH), 'figure'),
        prevent_initial_call=True
    )
    def download_bar_png(n_nlicks, id, fig):
        f=go.Figure(fig)
        column_name = id['aio_id']
        return send_bytes(f.write_image, f"{column_name}.png")


    @callback(
        Output(ids.summaryTileCollapse(MATCH), "is_open"),
        Input(ids.showSummaryTile(MATCH), "n_clicks"),
        State(ids.summaryTileCollapse(MATCH), "is_open"),
        prevent_initial_call=True
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

