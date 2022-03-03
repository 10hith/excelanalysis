import random
import dash
import dash_html_components as html
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import Namespace, assign, arrow_function

app = dash.Dash()

# Create some markers.
points = [dict(lat=55.5 + random.random(), lon=9.5 + random.random(), value=random.random()) for i in range(100)]
data = dlx.dicts_to_geojson(points)
# Create geojson.


'''Option 1 with assign function'''
draw_flag = assign("""function(feature, latlng){
const flag = L.icon({iconUrl: `https://raw.githubusercontent.com/10hith/excelanalysis/release/aio/app/dash_apps/assets/favicon.ico`, 
iconSize: [20, 30]});
return L.marker(latlng, {icon: flag});
}""")


countries = [dict(name="Denmark", iso2="dk", lat=56.26392, lon=9.501785),
             dict(name="Sweden", iso2="se", lat=59.334591, lon=18.063240),
             dict(name="Norway", iso2="no", lat=59.911491, lon=9.501785)]



geojsonData = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in countries])

'''Option 2: using JS script'''
ns = Namespace("myNamespace", "mySubNamespace")
geojson = dl.GeoJSON(data=data, options=dict(pointToLayer=ns("pointToLayer")))

# Create the app.
app.layout = html.Div([
    dl.Map([
        dl.TileLayer(),
        geojson,
        # dl.GeoJSON(
        #     data=geojsonData,
        #     options=dict(pointToLayer=draw_flag),
        #     zoomToBounds=True)
        ], center=(56, 10), zoom=8, style={'height': '50vh'}),
])

if __name__ == '__main__':
    app.run_server(dev_tools_hot_reload=True, port=5001)