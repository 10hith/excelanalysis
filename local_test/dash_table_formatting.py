import time
import re
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import dash_table, html
from utils.params import HOST

df = px.data.iris()

dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
)

app = dash.Dash(
    __name__,
    title = "Excel-Analysis",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    # requests_pathname_prefix="/upload/"
)

completeness_formatting={
    'if': {
        'filter_query': '{completeness} > .98',
        'column_id': 'completeness'
    },
    'color': 'green',
    'fontWeight': 'bold'
 }, {
    'if': {
        'filter_query': '{column_type} = {non_numeric}',
    },
    'color': 'green',
    'fontWeight': 'bold'
 }


mark_red ={
    'if': {
        'filter_query': '{completeness} > .98',
        'column_id': 'completeness'
    },
    'color': 'tomato',
    'fontWeight': 'bold'
}

mark_green ={
    'if': {
        'filter_query': '{sepal_length} < 5',
    },
    'backgroundColor': '#FF4136',
    # 'color': 'green',
    'fontWeight': 'bold'
}

#
# overriding single column width
style_cell_conditional = [
                             {
                                 'if': {'column_id': 'Region'},
                                 'width': '250px'
                             },
                         ],

# list_of_dicts = ','.join([ f"'{x}': '{x}'" for x in df.columns ])
# tooltip_header = f"{{ {list_of_dicts} }}"

app.layout = html.Div([
    dbc.Card([
        html.H4(f"Distribution for Column - ", className="card-title"),
        html.H6(f"Viz generated @ ", className="card-subtitle"),
        dbc.Row([
            dbc.Col([
                dbc.Button("Scroll to top", className="btn btn-success"),
                dbc.Button("X", className="btn-close btn btn-danger"),
                ],
                width={"size": 1, "order": "last", "offset": 11},
                align="end"
            ),
        ], className="mb-2"),
    dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        tooltip_header=[dict((f'{x}', x) for x in df.columns)][0],
        virtualization=True,
        fixed_rows={'headers': True},
        style_cell={
            'textAlign': 'left',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0
        },
        style_data_conditional=[
            {
                'if': {'column_id': 'sepal_length'},
                'textAlign': 'left'
            },
            mark_red,
            mark_green,
        ],
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('records')
        ],
        tooltip_duration=None
    ),
    ])
    ])

if __name__ == '__main__':
    app.run_server(debug=True, port=8001, host=HOST)