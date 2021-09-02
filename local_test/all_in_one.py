from aio_components import MarkdownWithColorAIO
from dash import Dash, html
from utils.params import HOST

app = Dash(__name__)



app.layout = MarkdownWithColorAIO(
    'Custom colors',
    colors=['cornflowerblue', 'darkolivegreen', 'darkslateblue', 'lohith'],
    dropdown_props={
        'persistence': True
    }
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8001, host=HOST)