# Dummy Imports here to prevent flagging of errors when wirting code.
if GLOBAL_FLAG_IN_BROWSER == False:
    from SELAN_PLOTS.brython_components import bootstrap_tab
    from browser import document, html, ajax
    from SELAN_PLOTS.brython_components import basic_container_block, jq_hash
    import json
    from SELAN_PLOTS.brython_components.brython_imports import jq

class custom_tab(bootstrap_tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.well_list = []
        self.get_well_list()

    def get_well_list(self):

        req = ajax.ajax()
        req.open('POST', '/_get_well_list', True)
        req.bind('complete', self.update_well_list)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        print("I AM GETTING WELL LIST")
        req.send()

    def update_well_list(self, request):

        if request.status == 200 or request.status == 0:
            print(request.responseText)
            self.well_list = json.loads(request.responseText)
            for well_name in self.well_list['result']:
                print(well_name)
                self.add_tab({'menu': well_name, 'content': ''})

    def update_plot_on_well_change(self, ev):

        tab_handle = self.get_active_tab_handles()
        if tab_handle == None:
            print("No Tab returning")
            return

        well_name = tab_handle['tab_label'].get_value()
        tab_id = tab_handle['id']
        tab_div = tab_handle['tab_div']
        print('THIS IS THE WELL NAME', well_name)

        # Ajax Code
        req = ajax.ajax()
        req.open('POST', '/_get_well_plot', True)
        req.bind('complete', self.plot_swabbing_ajax)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        tab_div <= "waiting..."
        print("I AM GETTING A DIV")
        req.send({'well_name': well_name, 'plot_name': 'SWABBING', 'tab_id': tab_id})

    def plot_swabbing_ajax(self, request):

        if request.status == 200 or request.status == 0:
            data = json.loads(request.responseText)
            tab_id = data['tab_id']
            jq_div_name = jq_hash(tab_id)

            # Append Plotly Plot to the panel
            jq(jq_div_name).text= ''
            jq(jq_div_name).append(data['tab_content'])

    def get_swabbing_plot(self, well_name):

        print(locals())

        # Ajax Code
        req = ajax.ajax()
        req.open('POST', '/_add_numbers', True)
        req.bind('complete', self.add_numbers_ajax)
        self.small_div.text = "waiting..."
        print("I AM GETTING A DIV")
        req.send()


class wall(basic_container_block):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Add class Components
        self.tab_panel = custom_tab(self.genID('tab_block'))

        # Build Components
        self.add_button = html.BUTTON('Add Panel', Class='btn btn-primary btn-sm', id=self.genID('add_div'),
                                      type="button")
        self.update_button = html.BUTTON('Update Button', Class='btn btn-primary btn-sm', id=self.genID('update_well'),
                                         type="button")

        self.message_box = html.DIV(id=self.genID('message_box'))

        # Build Assembly
        self.root_div <= self.add_button + self.update_button + self.message_box + self.tab_panel.get_root_div()

        # Create Bindings
        self.createBindings()

    def add_panel(self, well_name='Well'):

        try:
            self.tab_panel.add_tab({'menu': 'well', 'content': ''})
            self.increment_unique_counter()

        except Exception as e:
            self.message_box <= e

    def get_root_div(self):
        return self.root_div

    ###BINDINGS
    def createBindings(self):
        self.add_button.bind('click', self.add_panel)
        self.update_button.bind('click', self.tab_panel.update_plot_on_well_change)


# ADD SOME SHIT SOME DUMMY
print("HELLO BRYTHON WORKING")
# CREATE ROOT PANEL AND ADD TO DOC
root_panel = wall('WALL', parent_div=document)
