from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import uvicorn


# Create the Dash application, make sure to adjust requests_pathname_prefx
app_dash = dash.Dash(__name__, requests_pathname_prefix='/login/')
# app_dash = dash.Dash(__name__, routes_pathname_prefix='/dash/')

app_dash.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Button('Disappear Graph', id='submitVal'),
    html.Br(),
    html.Button('Test request to fastapi', id='requestToFastApi'),
    dcc.Link('Go to fastapi', href='/fastapi'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5],
                    'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])


@app_dash.callback(
    Output(component_id='example-graph', component_property='figure'),
    [Input(component_id='submitVal', component_property='n_clicks')],
    prevent_initial_call=True,
)
def disappear_graph(click):
    return {}


# Now create your regular FASTAPI application


app = FastAPI()


@app.get("/fastapi")
def read_main():
    return {"message": "Hello World this is fun"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


appId = "something"

# Now mount you dash server into main fastapi application
# app.mount(f"/login/?racf={appId}", WSGIMiddleware(app_dash.server))
app.mount(f"/login/", WSGIMiddleware(app_dash.server))

if __name__ == "__main__":
    uvicorn.run("wDash:app", host="11.15.93.81", port=8000, reload=True)