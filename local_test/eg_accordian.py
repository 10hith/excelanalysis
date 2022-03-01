import dash_bootstrap_components as dbc
from dash import html, dcc
import dash
from utils.params import HOST


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                """
                INSERT, UPDATE, DELETE, MERGE, and SELECT statements can be created.\n
CREATE TABLE, DROP TABLE, CREATE VIEW, DROP VIEW are optional.\n
The key used in UPDATE, DELETE, and MERGE is specified by setting the key column.\n
New Now it is easy to merge csv into a database table by using the new Generate MERGE feature.
A field value may be trimmed, made uppercase, or lowercase. You can add custom text around the field value by using the template feature. For example, if you are using Oracle and want to convert a field in YYYYMMDD format to DATE, use TO_DATE({f},'YYYYMMDD'). Likewise for Sql Server, use CAST({f} AS DATETIME). The field value will be substituted for {f}.
Current version supports some database specific output and support ORACLE, MYSQL, SQL SERVER, PostreSQL and ANSI SQL databases. There are slight variations in the way different databases handle NULLs, empty strings, DATES, etc. .
                """, title="What can this tool do ?"
            ),
            dbc.AccordionItem(
                [
                    dcc.Markdown("""
                    * You can specify which fields to include and specify the name of the field.
                    * You can choose to quote your column names as appropriate for your database engine.
                    * You can sort the output by column name.
                    * You can use NULL for empty fields.""", className="text-primary"
                    ),
                    dcc.Markdown('''
                    
                    Inline code snippet: `my_bool = True`
                    
                    Block code snippet:
                    ```python
                    
                    def sum(a, b):
                        return a+b
                    
                    sum(2,2)
                    
                    ```''')
                ],
                title="What are my options ?"
            ),
            dbc.AccordionItem([
                dcc.Markdown('''
                #### Dash and Markdown
                
                Dash supports [Markdown](http://commonmark.org/help).
                
                Markdown is a simple way to write and format text.
                It includes a syntax for things like **bold text** and *italics*,
                [links](http://commonmark.org/help), inline `code` snippets, lists,
                quotes, and more.
                ''')
            ],
            title="Item 3"
            ),
        ],
        start_collapsed=True,
        className="text-secondary"
    ),
)

app.layout = dbc.Container([
    dbc.Row(dbc.Col(accordion)),
    dbc.Row([
        dbc.Col(
            dbc.Button(children="X", n_clicks=0, className="d-sm-table btn float-right")
            , width={"offset": 11, "order": 5, "size": 1}
        ),
        # dbc.Col([
        #                 dbc.Button(
        #                     id=self.ids.closeBtnDwnld(aio_id), children="X", n_clicks=0,
        #                     className="m-0 border border-dark btn-close btn btn-danger float-right btn-sm"),
        #                 dbc.Button(
        #                     id=self.ids.scrollTopDwnld(aio_id), children="^", n_clicks=0,
        #                     className="m-0 border border-dark btn-close btn btn-success float-right btn-sm"),
        #                 dbc.Button(
        #                     "View/Hide Summary",
        #                     id=self.ids.showSummaryTileDwnld(aio_id),
        #                     className="m-0 border border-dark btn-close btn btn-info float-right btn-sm", n_clicks=0),
        #             ], width={"order": 2})
        # ])
    ])
    ])



if __name__ == '__main__':
    app.run_server(debug=True, port=8002, host=HOST)
