from dash import Dash, Output, Input, State, html, dcc, callback, MATCH
import uuid
from datetime import datetime
import dash_bootstrap_components as dbc
from dash import dcc, dash_table
from typing import List, Dict
import plotly_express as px


class CreateDynamicCard(html.Div):
    # A set of functions that create pattern-matching callbacks of the sub-components
    class ids:
        scrollTop = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'scrollTop', 'aio_id': aio_id}
        closeBtn = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'closeBtn', 'aio_id': aio_id}
        dynBarChart = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'dynBarChart', 'aio_id': aio_id}
        dynPieChart = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'dynPieChart', 'aio_id': aio_id}
        dynDataTable = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'dynDataTable', 'aio_id': aio_id}
        dynStore = lambda aio_id: {'component': 'CreateDynamicCard', 'subcomponent': 'dynStore', 'aio_id': aio_id}
    # Make the ids class a public class
    ids = ids

    # Define the arguments of the All-in-One component
    def __init__(
        self,
        data_store: List[Dict],
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
            x="ratio",
            orientation='h',
            color="value",
            text='num_occurrences'
        )

        # Define the component's layout
        super().__init__([  # Equivalent to `html.Div([...])`
            dbc.Card([
                html.H4(f"Distribution for Column - '{column_name}' ", className="card-title"),
                html.H6(f"Viz generated @ {datetime.now()}", className="card-subtitle"),
                dbc.Row([
                    dbc.Col([
                        dbc.Button(
                            id=self.ids.scrollTop(aio_id), children="Scroll to top", n_clicks=0, className="btn-close btn btn-success"
                        ),
                        dbc.Button(
                            id=self.ids.closeBtn(aio_id), children="X", n_clicks=0, className="btn-close btn btn-danger"),
                    ],
                        width={"size": 3, "order": "last"}, md={"size": 3, "order": "last"},
                        align="end"
                    ),
                ], justify="end"),
                dbc.Row([
                    dbc.Col([
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
                                            dcc.Graph(id=self.ids.dynBarChart(aio_id),
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
                                            dcc.Graph(id=self.ids.dynPieChart(aio_id)),
                                        ],

                                    ),
                                    dbc.Tab(
                                        label="View Data",
                                        tab_id="tabData",
                                        children=[
                                            html.Br(),
                                            html.Br(),
                                            dash_table.DataTable(
                                                id=self.ids.dynDataTable(aio_id),
                                            )
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
                        dcc.Store(id=self.ids.dynStore(aio_id),data=col_data_store),
                    ]
                )],
            style={"width": "2"},
            )
            ])

    # Define CallBacks
    @callback(
        [
            Output(ids.dynPieChart(MATCH), 'figure'),
            Output(ids.dynDataTable(MATCH), 'columns'),
            Output(ids.dynDataTable(MATCH), 'data'),
            Output(ids.dynDataTable(MATCH), 'style_data_conditional'),
            ],
        Input(ids.dynStore(MATCH), 'data')
    )
    def on_data_set_dyn_graph(col_data_store):
        fig_pie = px.pie(
            col_data_store,
            names="value",
            values="ratio",
            color="value",
            hole=0.6,
        )
        columns = [{"name": i, "id": i} for i in col_data_store[0].keys()]
        data = col_data_store
        # Conditional styling for the data table
        style_data_conditional = [
            {
                'if': {
                    'column_id': 'column_name',
                },
                'hidden': 'False',
                'color': 'red'
            }
        ]
        return fig_pie, columns, data, style_data_conditional
