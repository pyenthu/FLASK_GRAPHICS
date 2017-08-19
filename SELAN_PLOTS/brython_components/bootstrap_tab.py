if GLOBAL_FLAG_IN_BROWSER == False:
    from browser import html, alert
    from SELAN_PLOTS.brython_components import my_edit_label, basic_container_block


class bootstrap_tab(basic_container_block):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Abstraction of TAB menu/Labels/Div in a list
        self.tabs = []

        # Main Components of tab line and div
        self.div_main_ul_div = html.UL(id=self.genID('root_tab'), Class='nav nav-tabs')
        self.div_main_content = html.DIV(Class='tab-content', display='flex')

        self.root_div <= self.div_main_ul_div + self.div_main_content

    def add_tab(self, tab_spec={'menu': 'menu', 'content': 'content in div'}):

        try:

            new_tab = {}
            new_tab['id'] = self.genID(self.get_new_panel_unique_id())
            print(new_tab['id'])
            dom_name_ref = new_tab['id']
            jq_name_ref = ''.join(['#', dom_name_ref])

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

            new_tab['tab_div'] = html.DIV(id=dom_name_ref, Class=tab_class)
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

    def get_active_tab_handles(self):

        child_tabs = self.div_main_content.children
        for item in child_tabs:
            if item.Class == 'tab-pane active':
                activeTab = item
        tab_handles = get_item_by_id(self.tabs, activeTab.id)
        return tab_handles

    def del_tab(self, id):

        try:
            jq_name_ref = ''.join(['#', self.genID(id)])
            print('so far so good while tryng to delete tab', jq_name_ref)

            # Find and delete tab and line
            tab_div = jq(jq_name_ref)
            if (tab_div.length != 0):
                tab_div.remove()
                print('found again removed again')
            else:
                print('no element found')

            tab_line = jq(jq_find('a', 'href', jq_name_ref))
            if (tab_line.length != 0):
                tab_line.remove()
                print('Line found removed ')
            else:
                print('no Line found')

        except Exception as e:
            alert(''.join(['Nothing found', e]))
            print(''.join(['Nothing found', e]))

