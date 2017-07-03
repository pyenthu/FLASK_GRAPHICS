import plotly.graph_objs as go
import pandas as pd
from flask import json
from plotly.offline import iplot, plot
import plotly

class curve_group(list):
    def __init__(self, group_name='default', curves=[]):
        self.curves_groups = group_name

    def add_curve(self, curve):
        self.append(curve)

class log_heatmap(object):

    def __init__(self, curve_name, x, y, z,
                 range=[0, 100], showticklabels=True,
                 xaxis_title=''
                 ):
        self.curve_name = curve_name
        self.showticklabels = showticklabels
        self.xaxis_title = xaxis_title

        # Build xaxis names. reference is for curves to refer. xaxis_name is passed  to layout to build axis
        self.trace = go.Heatmap(
            x=x, y=y, z=z
        )
        return


class log_curve(object):

    def __init__(self, curve_name, x, y,
                 range=[0, 100], showticklabels=True,
                 xaxis_title='', color='auto',
                 mode='line'):
        self.curve_name = curve_name
        self.range = range
        self.showticklabels = showticklabels
        self.xaxis_title = xaxis_title

        # Build xaxis names. reference is for curves to refer. xaxis_name is passed  to layout to build axis
        self.trace = go.Scatter(
            x=x, y=y,
            name=curve_name,
            mode=mode
        )
        if (color != 'auto'):
            self.trace[mode] = dict(color=color)

        return

class log_plot(object):

    # The first curve is the primary curve
    def __init__(self, curves=[], height=2000, width=1000, curve_groups=None, log_panes=None):
        self.layout = go.Layout()
        self.figure_size = dict(height=height, width=width)
        self.annotation = dict(tick_height=10, label_height=5)
        self.panes = []

    def _calculate_annotations(self):

        # We will need to adjust the height
        label_space = 0

        # Loop for label
        for item in self.curves:
            if (item.showticklabels == True):
                label_space = label_space + self.annotation['tick_height']
            if (item.xaxis_title != ''):
                label_space = label_space + self.annotation['label_height']

        return label_space

    def add_pane(self, pane):
        self.panes.append(pane)

    def assign_curve_group(self, curve_group, pane_number):
        self.panes[pane_number]['curve_group']= curve_group

    def build_traces(self):

        # SEND THE TRACES FOR PLOTTING
        data = []
        for pane in self.panes:
            if 'curve_group' in pane:
                for item in pane['curve_group']:
                    data.append(item.trace)
        return data

    def create_sub_plots(self, curve_groups=None, log_panes=2):

        layout = go.Layout(width=self.figure_size['width'], height=self.figure_size['height'],
                           yaxis=dict(domain=[0, 0.95]))

        for counter, pane in enumerate(self.panes):

            xaxis_name = ''.join(['xaxis', str(counter + 1)])
            layout[xaxis_name]['domain']=pane['domain']

            for_pane = counter + 1
            base_xaxis = dict(name=''.join(['xaxis', str(for_pane)]), curve_ref=''.join(['x', str(for_pane)]))

            if 'curve_group' in pane:
                for counter, element in enumerate(pane['curve_group']):
                    element.xaxis_name = ''.join([base_xaxis['name'], str(counter + 1)])
                    curve_reference = ''.join([base_xaxis['curve_ref'], str(counter + 1)])
                    if counter != 0:
                        layout[element.xaxis_name] = dict(title=element.xaxis_title,
                                                          side='top',
                                                          anchor='free',
                                                          showticklabels=element.showticklabels,
                                                          position=1,
                                                          overlaying=base_xaxis['curve_ref']
                                                          )
                        element.trace['xaxis'] = curve_reference
                        if hasattr(element, 'range'):
                            layout[element.xaxis_name]['range']=element.range
                    else:
                        layout[base_xaxis['name']] = dict(title=element.xaxis_title,
                                                          side='top',
                                                          anchor='free',
                                                          showticklabels=element.showticklabels,
                                                          position=1
                                                          )
                        layout[base_xaxis['name']]['domain']=self.panes[for_pane-1]['domain']
                        element.trace['xaxis'] = base_xaxis['curve_ref']
                        if hasattr(element, 'range'):
                            layout[base_xaxis['name']]['range'] = element.range

        data = self.build_traces()
        self.figure = go.Figure(data=data, layout=layout)

        return self.figure

    def display(self, inline=True, sub_plot=False, file_name='temp_pyplot.html'):

        self.create_sub_plots()

        if (inline == False):
            plot(self.figure, filename=file_name)
        else:
            iplot(self.figure)


    def get_div(self, sub_plot=False):

        self.create_sub_plots()
        div = plot(self.figure, show_link=False, output_type="div", include_plotlyjs=False)
        return div

    def get_json(self, sub_plot=False):

        self.create_sub_plots()
        return json.dumps(self.figure, cls=plotly.utils.PlotlyJSONEncoder)
