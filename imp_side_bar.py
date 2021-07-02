"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import uuid

# Defining the Session Id
session_id = str(uuid.uuid4())

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    # "background-color": "#f8f9fa",
    "background-color": "purple",
}

TOPBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    # "left": "16rem",
    "right":0,
    # "bottom": 0,
    # "background-color": "#f8f9fa",
    "background-color": "yellow",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

topbarNav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Active", active=True, href="#")),
        dbc.NavItem(dbc.NavLink("A link", href="#")),
        dbc.NavItem(dbc.NavLink("Another link", href="#")),
        dbc.NavItem(dbc.NavLink("Disabled", disabled=True, href="#")),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem("Item 1"), dbc.DropdownMenuItem("Item 2")],
            label="Dropdown",
            nav=True,
        ),
    ]
, style=TOPBAR_STYLE)

topbar = html.Div([topbarNav])

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact", id="page1"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        dbc.Button(id="disableMe",children="", className="ml-2"),
        html.Hr(),
        dbc.Button(children="button_to_disable", id="buttonToDisable"),
        html.Hr(),
        dbc.Button(children="TakeMe out of here", id="takeMeOutOfHere")
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, topbar, content, html.Div(id='hiddenContent')])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P(f"This is the content of the home page! And the session id is {session_id} ")
    elif pathname == "/page-1":
        return html.P(f"This is the content of page 1. Yay! And the session id is {session_id}")
        # return sidebar
    elif pathname == "/page-2":
        return html.P(f"Oh cool, this is page 2! And the session id is {session_id}")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# @app.callback(
#     Output("disableMe", "children"),
#     Input("buttonToDisable", "n_clicks"),
#     prevent_initial_call=True
# )
# def disable_button(nclicks):
#     if nclicks==0:
#         return ""
#     return "Click to view DQ results"

#
@app.callback(
    Output("page1", "disabled"),
    Input("buttonToDisable", "n_clicks"),
    prevent_initial_call=True
)
def disable_button(nclicks):
    if nclicks==0:
        return False
    return True

#
app.clientside_callback(
    """
    function(nClicks) {
        if (nClicks>0) {
            location.replace("http://11.15.93.81:8000/notes")
            }
        return [""]
    }
    """,
    Output('hiddenContent', 'children'),
    Input('takeMeOutOfHere', 'n_clicks')
)


if __name__ == "__main__":
    app.run_server(debug=True)