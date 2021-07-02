import pandas as pd
import dash
import dash_labs as dl
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate


import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc


import time

app = dash.Dash(__name__,
                plugins=[dl.plugins.FlexibleCallbacks()],
                title="My Sidebar",
                external_stylesheets=[dbc.themes.CYBORG] ## This get overridden by template
                )
tpl = dl.templates.DbcRow(app, title="Manual Update", theme=dbc.themes.BOOTSTRAP)

hist = pd.read_csv("histogram.csv").fillna("unknown")



"""
A few things happening here - 
1) I was able to get create a call back for a component in template
2) if specifying output=tpl.graph_output(), then just return fig; Else return fig within a Graph object
3) 
"""



@app.callback(Output('dccStore', 'data'),
              Input('dropdownInput', 'value'),
              suppress_callback_exceptions=True
              )
def filter_countries(column_selected):
    if not column_selected:
        # Return all the rows on initial load/no country selected.
        return hist.to_dict('records')
    filtered_hist = hist.query(f"column_name == '{column_selected}' ")

    return filtered_hist.to_dict('records')


## Call back without the use of dcc.store
@app.callback(
    output=dict(data=Output('histogram', 'figure')),
    args=dict(
        column_selected =Input('dropdownInput', 'value'),
        dccStore=Input('dccStore', 'data')),
    suppress_callback_exceptions=True
)
def display_histogram_from_ddcStore(column_selected, dccStore):
    df = pd.DataFrame(dccStore, columns=['column_name', 'cat_value', 'counts', 'ratio'])
    filtered_df = df.query(f"column_name == '{column_selected}' ")
    fig = px.histogram(filtered_df, x="cat_value", y="ratio", color="cat_value")
    # return fig
    return dcc.Graph(figure=fig)


@app.callback(
    output = dict(data=Output('dataTable', 'data')),
    args = dict(dccStore = Input('dccStore', 'data'))
)
def on_data_set_table(dccStore):
    if dccStore is None:
        raise PreventUpdate
    return dict(data=dccStore)


app.layout = html.Div([
    dcc.Store(id='dccStore'),
    dcc.Graph(id='histogram', figure={}),
    dcc.Dropdown(
        id='dropdownInput',
        options=hist['column_name'].unique().tolist(),
    ),
    dash_table.DataTable(
        id='dataTable',
        columns=[{'name': i, 'id': i} for i in hist.columns]
    ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8000)