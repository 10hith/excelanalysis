from utils.params import HOST
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function
import dash_bootstrap_components as dbc
import dash
from dash import Dash, html, Input, Output, dash_table, dcc, callback, get_asset_url
from utils.spark_utils import get_crime, PROJECT_ROOT, spark
from utils.dash_utils import get_crime_summary_graph
from dash_extensions.javascript import assign


# The external stylesheet holds the location button icon.
# external_stylesheets=['https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'],

dash.register_page(__name__,
                   path='/interactive_crime_map'
                   )

cache_df = spark\
    .read\
    .load(f"{PROJECT_ROOT}/resources/data/AllCrimeParquet_bucketed_2021_4FILES")\
    .filter("mnth in ('2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06')")

cache_df.cache()
cache_df.take(1)
cache_df.createOrReplaceTempView("crime")
# cache_df.printSchema()

'''This works too'''
# url = get_asset_url(path=f"favicon.ico")

geojson_points_w_icon = assign("""function(feature, latlng){
const flag = L.icon({iconUrl: 'https://flagcdn.com/64x48/dk.png', iconSize: [24, 48]});
return L.marker(latlng, {icon: flag});
}""")


icons ={
    "iconUrl": 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-yellow.png',
    "shadowUrl": 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    "iconSize": [25, 41],
    "iconAnchor": [12, 41],
    "popupAnchor": [1, -34],
    "shadowSize": [41, 41]
    }

layout = dbc.Container([
    dbc.Row(
        dbc.Col([
            html.Br(),
            html.Br(),
            html.H3(id="crimeSummary", children=[], className="text-info"),
        ])
    ),
    dbc.Row(
        dbc.Col([
            dl.Map([
                    # dl.TileLayer(),
                    dl.TileLayer(
                        url="http://www.google.co.uk/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}"
                        #url="https://www.ign.es/wmts/mapa-raster?request=getTile&layer=MTN&TileMatrixSet=GoogleMapsCompatible&TileMatrix={z}&TileCol={x}&TileRow={y}&format=image/jpeg",
                    ),
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
            html.Div(id="crimeSummaryGraphDiv", children=[])
        ],
        ),
    ]),
    dbc.Row(dbc.Col(
        html.Div(id="dTableDiv", children=[])
    )),
])

#            15,\

@callback(
    [
        Output("layer", "children"),
        Output("layer2", "children"),
        Output("map", "center"),
        Output("map", "zoom"),
        Output("dTableDiv", "children"),
        Output("crimeSummary", "children"),
        Output("crimeSummaryGraphDiv", "children")
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
        zoomToBounds=True,
        # zoomToBoundsOnClick=True,
        # options=dict(pointToLayer=geojson_points_w_icon),
        cluster=True
    ),

    point_layer = [
        dl.CircleMarker(
            center=click_lat_lng,
            children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)),
        )
    ]

    point_layer1 = [
        dl.Marker(
        position=[click_lat_lng[0], click_lat_lng[1]], children=dl.Tooltip(f"{click_lat_lng}"), icon=icons
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
           point_layer1,\
           (click_lat_lng[0], click_lat_lng[1]),\
           "15",\
           [crime_dtable], \
           summary_text, \
           [summary_graph]
