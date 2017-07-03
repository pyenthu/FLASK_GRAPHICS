# coding=utf-8
from pprint import pprint

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children=[

    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization',
                'hovermode': 'none',
                'displayModeBar': 'false'
            }
        }
    )
], style={'height': '500px', 'width':'1000px',
          'background-color': 'powderblue',
          'overflow':'scroll',
          'resize': 'both'})

app.layout.children.append(html.P('Example P', id='my-p-element'))
pprint (app.layout)

if __name__ == '__main__':
    app.run_server(debug=True)