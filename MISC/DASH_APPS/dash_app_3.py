import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.config.supress_callback_exceptions = True

class dash_wrapper:
    def __init__(self, dash_app, app_name):
        self.app = app_name

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
                                dcc.Input(id=self.gen_id('id_width'), value=200, type="number"),
                                html.Button('Set Width', id=self.gen_id('width-butt'), type='submit'),
                                html.P('mint', id=self.gen_id('mint'))
                            ])
        self.app.layout['root'].children.append(self.div)

    def assign_callback(self):
        @app.callback(
            Output(self.gen_id('mint'), 'children'),
            [Input(self.gen_id('id_width'), 'value')]
        )
        def update_P(input_value):
            #print (self.gen_id('id_width'), self.gen_id('mint'), self.parent_name)
            return 'You\'ve entered "{}"'.format(input_value)

        @app.callback(
            Output(self.parent_name, 'style'),
            [Input(self.gen_id('id_width'), 'value')]
        )
        def update_width(input_value):
            self.div.style['width']=input_value
            return self.div.style

    def gen_id(self, comp_name):
        sName = ''.join([self.parent_name, '_', comp_name])
        print(sName)
        return sName

#RESET THE APP NOW
app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type="text"),
    html.Div(id='my-div'),
    html.Button('Add Div', id='add-div', type='submit'),
    html.Div(id='root', children=[]),
    html.P('DONE', id='done')
])

@app.callback(
    Output('done', 'children'),
    events=[Event('add-div', 'click')],
)
def add_new_div():
    new_div_0.assign_callback()
    return 'DONE CLICK'

@app.callback(
    Output('my-div', 'children'),
    [Input('my-id', 'value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

new_div_0 = custom_div(app, 'new_div_0')
new_div_1 = custom_div(app, 'new_div_1')
new_div_2 = custom_div(app, 'new_div_2')

new_div_1.assign_callback()
new_div_2.assign_callback()

if __name__ == '__main__':
    app.run_server()
