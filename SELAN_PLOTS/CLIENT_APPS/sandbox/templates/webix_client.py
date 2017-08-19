# Dummy Imports here to prevent flagging of errors when wirting code.
if GLOBAL_FLAG_IN_BROWSER == False:
    from browser import html, ajax, window, document
    from SELAN_PLOTS.brython_components import basic_container_block, jq_hash
    from SELAN_PLOTS.brython_components.brython_imports import jq
    import json
    import Plotly

    moment = window.moment

# ADD SOME SHIT SOME DUMMY
print("HELLO BRYTHON WORKING")

def max_moment_date(date_list):
    if len(date_list) <= 1: return None
    var_max_date = date_list[0]
    for date_item in date_list:
        var_max_date = moment.max(var_max_date, date_item)
    return var_max_date

def min_moment_date(date_list):
    if len(date_list) <= 1: return None
    var_min_date = date_list[0]
    for date_item in date_list:
        var_min_date = moment.min(var_min_date, date_item)
    return var_min_date


class bootstrap_combo_list():
    def __init__(self, id, list, *args, **kwargs):

        try:
            self.select_box = html.SELECT(id=id, data_size="20", Class="selectpicker")
            for item in list:
                self.select_box <= html.OPTION(item)
        except Exception as e:
            print(e)
    def selected_item(self):
        for item in self.select_box:
            if item.selected:
                return item.value

    def get_html(self):
        return self.select_box

class swab_plot_panel(basic_container_block):
    def __init__(self, *args, **kwargs):
        # Initialize this first
        super().__init__(*args, **kwargs)

        # CREATE ROOT PANEL AND ADD TO DOC
        self.well_selector = bootstrap_combo_list('well_selector',
                                                  ['BK_1', 'BK_29', 'IND_15', 'IND_14'])

        self.plot_selector = bootstrap_combo_list('plot_selector',
                                                  ['SWABBING', 'PRODUCTION'])

        self.get_root_div() <= self.well_selector.get_html() + self.plot_selector.get_html()

        self.get_root_div() <= html.BUTTON('BUTTON', id='update_plot', Class='btn btn-primary btn-sm')

        # Graphics division
        self.my_new_slider = well_prop_slider(self.get_root_div(), 'NEW_SLIDER', 'BK_1', 'TIME')
        self.graph_div = html.DIV(id='graph_div')
        self.get_root_div() <= self.graph_div

        # Create Bindings
        jq(jq(jq_hash(self.my_new_slider.get_id()))).on('valuesChanged', self.update_plot)
        jq('#update_plot').on('click', self.update_plot)
        self.well_selector.select_box.bind('change', self.load_slider)

    def load_slider(self, ev):
        self.my_new_slider.populate_slider(self.well_selector.selected_item(), 'TIME')

    def update_plot(self, ev, data=None):
        try:
            req = ajax.ajax()
            req.open('POST', '/_get_filtered_plot', True)

            req.bind('complete', self.plot_filtered_ajax)
            req.set_header('content-type', 'application/x-www-form-urlencoded')
            slider_range = jq(jq_hash(self.my_new_slider.get_id())).dateRangeSlider('values')
            print("I AM GETTING A DIV FROM INSIDE THE CLASS")

            req.send(dict(well_name=self.well_selector.selected_item(),
                          plot_name=self.plot_selector.selected_item(),
                          prop_name=self.my_new_slider.prop_name,
                          min=moment(slider_range.min).format('YYYY-MM-DD hh:mm:ss'),
                          max=moment(slider_range.max).format('YYYY-MM-DD hh:mm:ss'),
                          dtype=jq.type(slider_range.max)))

        except Exception as e:
            print("ERROR UPDATE SLIDER", e)

    def plot_filtered_ajax(self, request):
        try:
            if request.status == 200:
                ajax_plot_data = json.loads(request.responseText)
                if ajax_plot_data is not None:
                    self.graph_div.innerHTML = ''
                    Plotly.newPlot(self.graph_div, ajax_plot_data['data'], ajax_plot_data['layout'])
                else:
                    print('no data')
                    self.graph_div.innerHTML = 'NO FILTERED DATA'
            else:
                print('no data')
                self.graph_div.innerHTML = 'NO FILTERED DATA'

        except Exception as e:
            print("ERROR THIS IN PLOT FILTERED DATA. PROBABLY NO DATA RECEIVED", e)


class well_prop_slider():
    def __init__(self, html_parent_element, slider_name, well_name=None, prop_name=None):

        try:
            self.slider = html.DIV(id=slider_name)
            self.prop_name = prop_name
            self.well_name = well_name
            html_parent_element <= self.slider

            print("CREATING NEW SLIDER", slider_name)

            jq(jq_hash(slider_name)).dateRangeSlider(dict(
                bounds=dict(min=moment('2017-07-07'), max=moment('2017-07-10')),
                defaultValues=dict(min=moment('2017-07-08'), max=moment('2017-07-10')),
                formatter=self.date_slider_format,
                arrows=True,
                step=dict(hours=6)
            ))
            self.populate_slider(self.well_name, self.prop_name)

        except Exception as e:
            print("ERROR ", e)

    def populate_slider(self, well_name, prop_name):

        try:
            if well_name == None or prop_name == None: return
            req = ajax.ajax()
            # req.open('POST', '/_get_well_data', True)
            req.open('POST', '/_get_min_max_range', True)

            req.bind('complete', self.ajax_fill_slider)
            req.set_header('content-type', 'application/x-www-form-urlencoded')
            print("SLIDER REQUEST BEING SENT well name prop name", well_name, prop_name)

            # req.send(dict(well_name=well_name, prop_name=prop_name, data_filter=None))
            req.send(dict(well_name=well_name, prop_name=prop_name))

            print("SLIDER REQUEST SENT")

        except Exception as e:
            print("ERROR ", e)

    def date_slider_format(self, val):
        return moment(val).format('DD-MMM-YY hh:mm')

    def get_id(self):
        return self.slider.id

    def ajax_fill_slider(self, request):
        try:
            print("SLIDER REQUEST RECEIVED  ", request.responseText)
            min_date = moment.utc(json.loads(request.responseText)['min'])
            max_date = moment.utc(json.loads(request.responseText)['max'])

            print("FILLING SLIDERS  HERE   ", min_date.toDate(), max_date.toDate())

            jq(jq_hash(self.slider.id)).dateRangeSlider("bounds", min_date.toDate(), max_date.toDate())
            jq(jq_hash(self.slider.id)).dateRangeSlider("values", min_date.toDate(), max_date.toDate())

        except Exception as e:
            print("LOAD SLIDER AJAX ERROR ", e)


main_panel = swab_plot_panel('MAIN', parent_div=document)
