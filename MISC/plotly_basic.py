from pprint import pprint

import numpy as np
import pandas as pd
import plotly
from flask import json


def modify_basic_plot():

    try:

        rng = pd.date_range('1/1/2011', periods=30, freq='H')
        ts = pd.Series(np.random.randn(len(rng)), index=rng)

        graphs = [
            dict(
                data=[
                    dict(
                        x=[1, 2, 3, 5],
                        y=[50, 40, 100, 2],
                        type='scatter'
                    ),
                ],
                layout=dict(
                    title='first graph',
                    domain = [0.0, 0.6]
                )
            ),

            dict(
                data=[
                    dict(
                        x=[1, 3, 5],
                        y=[10, 50, 30],
                        type='bar'
                    ),
                ],
                layout=dict(
                    title='second graph'
                )
            ),

            dict(
                data=[
                    dict(
                        x=ts.index,  # Can use the pandas data structures directly
                        y=ts
                    )
                ]
            )
        ]

        # Convert the figures to JSON
        # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
        # objects to their JSON equivalents
        return json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    except Exception as e:
        pprint(["PROBLEM IN PLOTLY BASIC", str(e)])
        raise

    def gowell_plot_div():
        return build_gowell_plot().get_div()

    def gowell_plot_json(start=0, end=0):
        return build_gowell_plot(start, end).get_json()


def make_basic_plot():

    try:

        rng = pd.date_range('1/1/2011', periods=30, freq='H')
        ts = pd.Series(np.random.randn(len(rng)), index=rng)

        graphs = [
            dict(
                data=[
                    dict(
                        x=[1, 2, 3, 5],
                        y=[10, 20, 30, 2],
                        type='scatter'
                    ),
                ],
                layout=dict(
                    title='first graph',
                    domain = [0.0, 0.6]
                )
            ),

            dict(
                data=[
                    dict(
                        x=[1, 3, 5],
                        y=[10, 50, 30],
                        type='bar'
                    ),
                ],
                layout=dict(
                    title='second graph'
                )
            ),

            dict(
                data=[
                    dict(
                        x=ts.index,  # Can use the pandas data structures directly
                        y=ts
                    )
                ]
            )
        ]

        # Add "ids" to each of the graphs to pass up to the client
        # for templating
        ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

        # Convert the figures to JSON
        # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
        # objects to their JSON equivalents
        #graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
        return json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    except Exception as e:
        pprint(["PROBLEM IN PLOTLY BASIC", str(e)])
        raise