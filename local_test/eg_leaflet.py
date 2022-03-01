import pandas as pd
from utils.params import HOST
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function
import dash_bootstrap_components as dbc

from dash import Dash, html, Input, Output, dash_table, dcc
from utils.spark_utils import spark, get_crime, PROJECT_ROOT
from utils.dash_utils import get_crime_summary_graph

from dash_extensions.javascript import Namespace
ns = Namespace("myNamespace", "mySubNamespace")
# The external stylesheet holds the location button icon.
# external_stylesheets=['https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'],

# app = JupyterDash(__name__)

app = Dash(
    external_stylesheets=[dbc.themes.ZEPHYR],
    prevent_initial_callbacks=True,
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)

cache_df = spark\
    .read\
    .load(f"{PROJECT_ROOT}/resources/data/AllCrimeParquet_bucketed_2021_4FILES")\
    .filter("mnth = '2021-01'")

cache_df.cache()
cache_df.take(1)
cache_df.createOrReplaceTempView("crime")
cache_df.printSchema()


app.layout = dbc.Container([
    dbc.Row(
        dbc.Col([
            html.Br(),
            html.Br(),
            crimeSummaryText := html.H3(children=[], className="text-info"),
        ])
    ),
    dbc.Row(
        dbc.Col([
            myMap := dl.Map([
                    dl.TileLayer(),
                    dl.LayerGroup(id="layer"),
                    dl.LayerGroup(id="layer2"),
                    # dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}),
                ], id="map",
                center=(51.354221748320946, 0.09599384789215022),
                zoom=15,
                style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
        ])
    ),
    dbc.Row([
        dbc.Col([
            crimeSummaryGraphDiv := html.Div(children=[])
        ],
        ),
    ]),
    dbc.Row(dbc.Col(
        html.Div(id="dTableDiv", children=[])
    )),
], fluid=True)


@app.callback(
    [
        Output("layer", "children"),
        Output("layer2", "children"),
        Output(myMap, "center"),
        Output("dTableDiv", "children"),
        Output(crimeSummaryText, "children"),
        Output(crimeSummaryGraphDiv, "children")
    ],
    [Input("map", "click_lat_lng")],
    prevent_initial_call=True
)
def map_click(click_lat_lng):
    print(click_lat_lng)

    '''Processing Crime data'''
    crime_sdf = get_crime(click_lat_lng[0], click_lat_lng[1], spark)
    crime_pdf = crime_sdf.toPandas()
    crime_points = crime_pdf.to_dict('records')
    crime_layer = dl.GeoJSON(
        id="crimeLayer",
        data=dlx.dicts_to_geojson(
            crime_points,
        ),
        hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),
        cluster=True,
        options=dict({"color": "red"})
    ),

    point_layer = [
        dl.CircleMarker(
            center=click_lat_lng,
            children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)),

        )
    ]

    crime_dtable = dash_table.DataTable(
        columns=[{'name': i, 'id': i} for i in crime_pdf.columns],
        data=crime_points
    )

    summary_text = f"""There were a total of {len(crime_points)} crime incidents
                   reported in the latest month"""

    summary_graph = dcc.Graph(figure=get_crime_summary_graph(crime_pdf), config={"displaylogo": False})

    return crime_layer,\
           point_layer,\
           (click_lat_lng[0], click_lat_lng[1]),\
           [crime_dtable], \
           summary_text, \
           [summary_graph]


if __name__ == '__main__':
    app.run_server(debug=True, port=8002, host=HOST)



# val =[dict(lat=-37.8, lon=175.6)]*100
# print(val)
# # fig.show()