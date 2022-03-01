import dash, dash_core_components as dcc, dash_html_components as html
import plotly.express as px
import dash_bootstrap_components as dbc
from utils.params import HOST

# from databricks import koalas as ks
import pandas as pd

# df = px.data.iris()
# print(df.dtypes)


df = pd.read_csv("/home/basal/excelanalysis/local_test/crime_data.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

print(df.dtypes)

# print(type(df['lon'].sum().astype(int)))



# fig = px.scatter_mapbox(
#     df,
#     lat="Latitude",
#     lon="Longitude",
#     # hover_name="Crime_id",
#     hover_data=["Crime_type", "Month"],
#     color_discrete_sequence=["fuchsia"], zoom=15, height=300
# )
#
# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r":0,"t":1,"l":0,"b":0})

# app.layout = dbc.Container([
#     html.Br(),
#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
#     ])


if __name__ == '__main__':
    app.run_server(debug=True, port=8002, host=HOST)

# fig.show()