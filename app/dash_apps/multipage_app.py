import dash  # pip install dash
import dash_labs as dl  # pip install dash-labs
import dash_bootstrap_components as dbc # pip install dash-bootstrap-components
# Code from: https://github.com/plotly/dash-labs/tree/main/docs/demos/multi_page_example1
from utils.params import HOST
from dash import dcc, html, Input, Output, State
import visdcc
import dash_extensions as de
import time

# URL_BASE_PATHNAME= "/base/mapp/"
# URL_BASE_PATHNAME='/'

app = dash.Dash(
    __name__, plugins=[dl.plugins.pages],
    external_stylesheets=[dbc.themes.ZEPHYR],
    suppress_callback_exceptions=True,
    update_title='Job Running...',
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=0.7"}
    ],
    # requests_pathname_prefix="/mapp/",
    # routes_pathname_prefix="/mapp/",
    # url_base_pathname=URL_BASE_PATHNAME
)



random_lottie = int(time.time())%15
url = app.get_asset_url(path=f"{random_lottie}_lottie.json")
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))


# profiler_page = [page for page in dash.page_registry.values() if page["module"]=='pages.profiler'][0]

# for x in dash.page_registry.values():
#     print(x)

navbar = dbc.NavbarSimple([
    # [
        dbc.NavItem(
            dbc.NavLink(page["name"], href=page["path"])
        )
        for page in dash.page_registry.values()
        if page["module"] != "pages.not_found_404"
    # ],
    # dbc.DropdownMenu(
    #     [
    #         dbc.DropdownMenuItem(page["name"],
    #                              # href=f"{URL_BASE_PATHNAME}{page['path']}"
    #                             href=page['path']
    #                              )
    #         for page in dash.page_registry.values()
    #         if page["module"] != "pages.not_found_404"
    #     ],
    #     nav=True,
    #     label="More Pages",
    # )
    ],
    brand="Welcome to Excel-Analysis",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(
    [
        navbar,
        dl.plugins.page_container,
        # dcc.Store(id='profileResultStore', data=[]),
        # dcc.Store(id='profileSummaryResultStore', data=[]),
    ],
    # fluid=True,
)

if __name__ == '__main__':
    print(f"{type(dash.page_registry.values())}")
    [print(i) for i in dash.page_registry.values()]
    # print(f"{type(dash.page_registry['module'])}")
    app.run_server(debug=True, port=8003, host=HOST)
