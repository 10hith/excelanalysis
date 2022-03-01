import dash, dash_core_components as dcc, dash_html_components as html
import plotly.express as px
import dash_bootstrap_components as dbc
from utils.params import HOST

# from databricks import koalas as ks
import pandas as pd
#
# df = px.data.iris()
# print(df.dtypes)

import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html

app = Dash()
app.layout = html.Div([
    dl.Map([
        dl.TileLayer(),
        # From in-memory geojson. All markers at same point forces spiderfy at any zoom level.
        dl.GeoJSON(data=dlx.dicts_to_geojson([dict(lat=-37.8, lon=175.6), dict(lat=-37.7, lon=175.7)]), cluster=True,
                    zoomToBoundsOnClick=True,
                   superClusterOptions={"radius": 100}
                   ),
        # From hosted asset (best performance).
        dl.GeoJSON(url='assets/leaflet_50k.pbf', format="geobuf", cluster=True, id="sc", zoomToBoundsOnClick=True,
                   superClusterOptions={"radius": 100}),
    ], center=(-37.75, 175.4), zoom=11, style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
])


if __name__ == '__main__':
    app.run_server(debug=True, port=8002, host=HOST)

# fig.show()