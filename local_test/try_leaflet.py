import dash
import dash_leaflet as dl
from utils.params import HOST

app = dash.Dash()
app.layout = dl.Map(dl.TileLayer(), style={'width': '1000px', 'height': '500px'})

if __name__ == '__main__':
    app.run_server(debug=True, port=8001, host=HOST)
