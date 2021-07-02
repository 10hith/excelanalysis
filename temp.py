import time

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_labs as dl
from dash.dependencies import Input, Output, State
import uuid

# Defining the Session Id
session_id = str(uuid.uuid4())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )


app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1("Stock Market Dashboard",
                        className='text-center text-primary mb-4'),
                width=12)
    ),
    dbc.Row(
        dbc.Col(
            dcc.Text()
        )
    )

    ])


if __name__=='__main__':
    app.run_server(debug=True, port=8000)