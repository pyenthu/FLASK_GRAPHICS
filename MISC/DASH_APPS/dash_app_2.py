# coding=utf-8
from pprint import pprint

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, State, Input, Output

app = dash.Dash()
app.config.supress_callback_exceptions = True


class custom_div:
    def __init__(self, dash_app, div_name):
        self.app = dash_app
        self.parent_name = div_name
        self.div = html.Div(id=div_name,
                            style={'background-color': 'yellow',
                                   'resize': 'both',
                                   'width': 500
                                   },
                            children=[
                                dcc.Input(id=self.gen_id('id_width'), value=200, type="text"),
                                html.Button('Set Width', id=self.gen_id('width-butt'), type='submit'),
                                html.P('mint', id=self.gen_id('mint'))
                            ])
        self.app.layout['root'].children.append(self.div)

    def gen_id(self, comp_name):
        sName = ''.join([self.parent_name, '.', comp_name])
        print(sName)
        return sName


app.layout = html.Div([
    html.Button('Add Div', id='add-div', type='submit'),
    html.Div(id='root', children=[
        dcc.Input(id='id_input', value=200, type="number")
    ]),
    html.P('INFO', id='info'),
])


@app.callback(
    Output('root', 'children'),
    events=[Event('add-div', 'click')],
)
def add_new_div():
    my_div = custom_div(app, 'new_div')
    return app.layout['root'].children


my_div = custom_div(app, 'my_div')

if __name__ == '__main__':
    app.run_server(debug=True)
