from dash import Dash, Output, Input, State, html, dcc, callback, MATCH
import uuid
import dash_bootstrap_components as dbc
from dash import dcc, dash_table
from typing import List, Dict
import plotly_express as px
from utils.dash_utils import get_std_badges, get_numeric_badges, get_graph_height


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
            # labels={
            #     "value": "Click to select values"
            # },
            hover_name='value_complete',
            hover_data=['percentage']
        )
        fig.update_layout(
            autosize=True,
            height=get_graph_height(col_data_store),
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
                    dbc.Col(
                        dbc.ButtonGroup([
                            dbc.Button(
                                "View/Hide Summary",
                                id=self.ids.showSummaryTile(aio_id),
                                className="m-0 btn-info btn-sm", n_clicks=0),
                            dbc.Button(
                                id=self.ids.scrollTop(aio_id), children="^", n_clicks=0,
                                className="m-0 bg-success btn-sm"),
                            dbc.Button(
                                id=self.ids.closeBtn(aio_id), children="X", n_clicks=0,
                                className="m-0 bg-danger text-light btn-sm"),
                        ], className="float-end")
                        , width={"order": 5}
                    )
                ],
                ),
                dbc.Collapse([
                    dbc.Row([
                        dbc.Col(std_badges, width={"order": 1, "offset": 1}),
                    ]),
                    dbc.Row([
                        dbc.Col(numeric_badges, width={"order": 2, "offset":1}),
                    ])
                    ],
                    id=self.ids.summaryTileCollapse(aio_id),
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
                                                html.Br(),
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
                                                html.Br(),
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
                                                html.Br(),
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
            className="shadow p-3 mb-3 bg-white rounded"),
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
        Output(ids.summaryTileCollapse(MATCH), "is_open"),
        Input(ids.showSummaryTile(MATCH), "n_clicks"),
        State(ids.summaryTileCollapse(MATCH), "is_open"),
        prevent_initial_call=True
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open



