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
from utils.dash_utils import get_std_badges, get_numeric_badges, get_graph_height


class CreateDynamicCardDwnld(html.Div):
    # A set of functions that create pattern-matching callbacks of the sub-components
    class ids:
        parentCardDwnld = lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'parentCardDwnld', 'aio_id': aio_id}
        parentCardCollapseDwnld = lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'parentCardCollapseDwnld', 'aio_id': aio_id}
        scrollTopDwnld = lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'scrollTopDwnld', 'aio_id': aio_id}
        closeBtnDwnld = lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'closeBtnDwnld', 'aio_id': aio_id}
        dynBarChartDwnld = lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'dynBarChartDwnld', 'aio_id': aio_id}
        dynPieChartDwnld = lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'dynPieChartDwnld', 'aio_id': aio_id}
        dynDataTableDwnld = lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'dynDataTableDwnld', 'aio_id': aio_id}
        dataTablePhDwnld =  lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'dataTablePhDwnld', 'aio_id': aio_id}
        dynStoreDwnld = lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'dynStoreDwnld', 'aio_id': aio_id}
        downloadDataButtonDwnld = lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'downloadDataButtonDwnld', 'aio_id': aio_id}
        downloadDataUtilDwnld =  lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'downloadDataUtilDwnld', 'aio_id': aio_id}
        downloadBarButtonDwnld =  lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'downloadBarButtonDwnld', 'aio_id': aio_id}
        downloadBarUtilDwnld =  lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'downloadBarUtilDwnld', 'aio_id': aio_id}
        downloadPieButtonDwnld = lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'downloadPieButtonDwnld', 'aio_id': aio_id}
        downloadPieUtilDwnld = lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'downloadPieUtilDwnld', 'aio_id': aio_id}
        collapseBtnDwnld =  lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'collapseBtnDwnld', 'aio_id': aio_id}
        collapseUtilDwnld = lambda aio_id: {'component': 'CreateDynamicCardDwnld', 'subcomponent': 'collapseUtilDwnld', 'aio_id': aio_id}
        showSummaryTileDwnld =  lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'collapseBtnDwnld', 'aio_id': aio_id}
        summaryTileCollapseDwnld = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'collapseUtilDwnld', 'aio_id': aio_id}


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
                "value": "Click to select values"
            },
            hover_name='value_complete',
            hover_data=['percentage']
            # hovertemplate="%{value_complete}"
        )
        fig.update_layout(
            autosize=True,
            height=get_graph_height(col_data_store),
            # title_font_color='secondary',
            legend_title=f"Click to select '{column_name.upper()}'",
            legend=dict(
                orientation="h",
            ),
            xaxis_title="Percentage Of Records",
            yaxis_title="Categories Values",
            yaxis_automargin=True,
            yaxis_autorange=True,
        )
        #############################
        # Creating the summary tile
        #############################

        col_summary_stat = [x for x in summary_stats_store if x["column_name"] == column_name][0]

        std_badges = get_std_badges(col_summary_stat)
        numeric_badges = get_numeric_badges(col_summary_stat)


        # Define the component's layout
        super().__init__([
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        html.H4(f"    '{column_name.upper()}'", className="text-primary float-left"),
                    ]
                    ),
                    dbc.Col([
                        dbc.Button(
                            id=self.ids.closeBtnDwnld(aio_id), children="X", n_clicks=0,
                            className="m-0 border border-dark btn-close btn btn-danger float-right btn-sm"),
                        dbc.Button(
                            id=self.ids.scrollTopDwnld(aio_id), children="^", n_clicks=0,
                            className="m-0 border border-dark btn-close btn btn-success float-right btn-sm"),
                        dbc.Button(
                            "View/Hide Summary",
                            id=self.ids.showSummaryTileDwnld(aio_id),
                            className="m-0 border border-dark btn-close btn btn-info float-right btn-sm", n_clicks=0),
                    ], width={"order": 2}
                    ),
                ],
                    # justify="end"
                ),
                dbc.Collapse([
                    dbc.Row([
                        dbc.Col(std_badges, width={"order": 1, "offset": 1}),
                    ]),
                    dbc.Row([
                        dbc.Col(numeric_badges, width={"order": 2, "offset":1}),
                    ])
                    ],
                    id=self.ids.summaryTileCollapseDwnld(aio_id),
                    is_open=True
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
                                                        id=self.ids.downloadBarButtonDwnld(aio_id),
                                                        n_clicks=0
                                                        , className="btn btn-info float-right btn-sm"),
                                                    de.Download(id=self.ids.downloadBarUtilDwnld(aio_id)),
                                                    html.Br(),
                                                ],
                                                ),
                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.Graph(id=self.ids.dynBarChartDwnld(aio_id),
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
                                                        id=self.ids.downloadPieButtonDwnld(aio_id),
                                                        n_clicks=0
                                                        , className="btn btn-info float-right btn-sm"),
                                                    de.Download(id=self.ids.downloadPieUtilDwnld(aio_id)),
                                                    html.Br(),
                                                ],
                                                ),
                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.Graph(id=self.ids.dynPieChartDwnld(aio_id),
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
                                                        id=self.ids.downloadDataButtonDwnld(aio_id),
                                                        n_clicks=0
                                                        , className="btn btn-info float-right btn-sm"),
                                                    de.Download(id=self.ids.downloadDataUtilDwnld(aio_id)),
                                                    html.Br(),
                                                ],
                                                ),
                                            ]),
                                            dbc.Row([
                                                dbc.Col([html.Div(id=self.ids.dataTablePhDwnld(aio_id), children=[])
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
                        dcc.Store(id=self.ids.dynStoreDwnld(aio_id), data=col_data_store),
                    ]
                )],
                # style={"width": "2"},
                # className="border border-3 border-primary"
            ),
            ])

    # Define CallBacks
    @callback(
        [
            Output(ids.dynPieChartDwnld(MATCH), 'figure'),
            Output(ids.dataTablePhDwnld(MATCH), 'children'),
            ],
        Input(ids.dynStoreDwnld(MATCH), 'data'),
        State(ids.dynStoreDwnld(MATCH), 'id')
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
            legend_title=f"Click to select '{column_name.upper()}'",
            legend=dict(
                orientation="h",
            ),
            autosize=True,
            height=get_graph_height(col_data_store),
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
            filter_action="native",
            sort_action="native",
            style_cell={'minWidth': 50, 'width': 95, 'maxWidth': 95},
            style_table={'height': 300,},  # default is 500
            style_header={
                'backgroundColor': '#7f7f7f',
                'color': 'white',
                'fontWeight': 'bold',
            },
        )
        return fig_pie, dyn_data_table

    @callback(
        Output(ids.summaryTileCollapseDwnld(MATCH), "is_open"),
        Input(ids.showSummaryTileDwnld(MATCH), "n_clicks"),
        State(ids.summaryTileCollapseDwnld(MATCH), "is_open"),
        prevent_initial_call=True
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open


    @callback(
        Output(ids.downloadDataUtilDwnld(MATCH), "data"),
        inputs=dict(
            n_clicks=Input(ids.downloadDataButtonDwnld(MATCH), "n_clicks"),
            id=State(ids.downloadDataButtonDwnld(MATCH), "id"),
            column_data=State(ids.dynStoreDwnld(MATCH), 'data'),
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
        Output(ids.downloadBarUtilDwnld(MATCH), "data"),
        Input(ids.downloadBarButtonDwnld(MATCH), "n_clicks"),
        State(ids.downloadBarUtilDwnld(MATCH), "id"),
        State(ids.dynBarChartDwnld(MATCH), 'figure'),
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
        Output(ids.downloadPieUtilDwnld(MATCH), "data"),
        Input(ids.downloadPieButtonDwnld(MATCH), "n_clicks"),
        State(ids.downloadPieButtonDwnld(MATCH), "id"),
        State(ids.dynPieChartDwnld(MATCH), 'figure'),
        prevent_initial_call=True
    )
    def download_bar_png(n_nlicks, id, fig):
        f=go.Figure(fig)
        column_name = id['aio_id']
        return send_bytes(f.write_image, f"{column_name}.png")




