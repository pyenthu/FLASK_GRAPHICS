# Dummy Imports here to prevent flagging of errors when wirting code.
if GLOBAL_FLAG_IN_BROWSER == False:
    from SELAN_PLOTS.brython_components import bootstrap_tab
    from browser import document, html, alert, ajax
    from SELAN_PLOTS.brython_components import my_edit_label, basic_container_block, jq_hash
    import json
    from SELAN_PLOTS.brython_components.brython_imports import jq


class divergent_tabs(bootstrap_tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.well_name = 'BK_1'
        self.add_tab({'menu': 'SWABBING', 'content': ''})
        self.add_tab({'menu': 'PRODUCTION', 'content': ''})

    def add_tab(self, tab_spec={'menu': 'menu', 'content': 'content in div'}):

        # NOTE ALL TAB NAMES ARE UNIQUE ID'S ASSUMED

        try:

            new_tab = {}
            new_tab['id'] = self.genID(tab_spec['menu'])
            print(new_tab['id'])
            dom_name_ref = new_tab['id']
            jq_name_ref = jq_hash(dom_name_ref)

            # Check if this is the first tab
            if self.unique_panel_counter == 0:
                tab_class = 'tab-pane active'
            else:
                tab_class = 'tab-pane'

            # Create each line and division for the tab
            new_tab['tab_a'] = html.A(data_toggle='tab', href=jq_name_ref)
            new_tab['tab_label'] = my_edit_label(''.join(['label', dom_name_ref]), tab_spec['menu'])
            new_tab['tab_a'] <= new_tab['tab_label'].get_html()
            new_tab['tab_line'] = html.LI(new_tab['tab_a'])

            new_tab['tab_div'] = html.DIV(id=dom_name_ref, Class=tab_class, align_items='stretch')
            new_tab['tab_div'] <= tab_spec['content']

            self.div_main_content <= new_tab['tab_div']
            self.div_main_ul_div <= new_tab['tab_line']

            jq(new_tab['tab_a']).tab('show')

            # Set counter up
            self.increment_unique_counter()
            self.tabs.append(new_tab)
            return new_tab

        except Exception as e:
            alert(e)
            print(e)

    def update_plots(self, ev):

        send_request = []

        for tab_item in self.tabs:
            send_request.append(dict(well_name=self.well_name, plot_name=tab_item['tab_label'].get_value(),
                                     tab_id=tab_item['id']))
        # Ajax Code
        req = ajax.ajax()
        req.open('POST', '/_get_well_plots', True)
        req.bind('complete', self.make_ajax_plots)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        '''tab_id: No other way otherwise in async call. This will come back from server !!!'''
        req.send({'send_request': send_request})

    def make_ajax_plots(self, request):

        if request.status == 200:
            print('I am back')
            ajax_plot_data = json.loads(request.responseText)
            for plot_item in ajax_plot_data:
                print(plot_item['plot_name'], plot_item['tab_id'])
                jq_div_var = jq(jq_hash(plot_item['tab_id']))
                jq_div_var.empty()
                jq_div_var.append(plot_item['tab_content'])

class divergent_wall(basic_container_block):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Add class Components
        self.tab_panel = divergent_tabs(self.genID('tab_block'))

        # Build Components
        self.add_button = html.BUTTON('Add Panel', Class='btn btn-primary btn-sm', id=self.genID('add_div'),
                                      type="button")
        self.update_button = html.BUTTON('Update Button', Class='btn btn-primary btn-sm', id=self.genID('update_well'),
                                         type="button")

        self.well_name_edit = my_edit_label(self.genID('well_name'), 'WELL NAME')

        self.message_box = html.DIV(id=self.genID('message_box'))

        # Build Assembly
        self.root_div <= self.well_name_edit.get_html() + self.add_button + self.update_button + self.message_box + self.tab_panel.get_root_div()

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
        self.update_button.bind('click', self.tab_panel.update_plots)


# ADD SOME SHIT SOME DUMMY
print("HELLO BRYTHON WORKING")
# CREATE ROOT PANEL AND ADD TO DOC
root_panel = divergent_wall('WALL', parent_div=document)
