# Dummy Imports here to prevent flagging of errors when wirting code.
if GLOBAL_FLAG_IN_BROWSER == False:
    from browser import html, ajax
    import json
    from SELAN_PLOTS.brython_components.brython_imports import jq

def jq_hash(name):
    return ''.join(['#', name])

def jq_find(element_type, key, value):
    query = ''.join([element_type, '[', key, '$=', '\'', value, '\']'])
    print(query)
    return query

class basic_container_block():
    def __init__(self, div_name, parent_div=None):
        # Initialize panel max for Unique ID
        self.unique_panel_counter = 0
        self.root_div = html.DIV(id=div_name, Class='container')

        # Check andd add to parent
        if parent_div != None:
            parent_div <= self.root_div

    def get_root_div(self):
        return self.root_div

    def genID(self, name):
        return ''.join([self.root_div.id, '_', name])

    def getElementById(self, id):
        return self.root_div.get(selector=''.join(['#', self.genID(id)]))

    def get_new_panel_unique_id(self):
        return str(self.unique_panel_counter + 1)

    def increment_unique_counter(self):
        self.unique_panel_counter = self.unique_panel_counter + 1

class my_edit_label():

    def __init__(self, label_id, default_text="DEFAULT"):
        self.label = html.SPAN(default_text, id=''.join([label_id, '_label']), Class="label small",
                               style={'color': 'black', 'height': 30})
        self.input = html.INPUT(id=''.join([label_id, '_input']), type="text", hidden="true")

        self.root_div = html.DIV(''.join([label_id, 'root']))

        # Properties storage
        self.label_default_color = self.label.style.backgroundColor
        self.label_hover_color = "lightgreen"

        self.root_div = self.label + self.input

        self.create_bindings()

    def end_edit(self, ev):
        self.input.style.display = 'none'
        self.label.innerHTML = self.input.value
        self.label.style.display = 'block'
        self.label.trigger('custom_change')

    def start_edit(self, ev):
        self.input.style.display = 'block'
        self.label.style.display = 'none'
        self.input.focus()
        print("cllll", ev.target)

    def check_return_key(self, ev):
        if ev.which == 13:
            self.end_edit(ev)

    def stop_hover_label(self, ev):
        self.label.style.backgroundColor = self.label_default_color

    def hover_label(self, ev):
        self.label.style.backgroundColor = self.label_hover_color

    def create_bindings(self):
        self.label.bind('click', self.start_edit)
        self.input.bind('focusout', self.end_edit)

        # Hover
        self.label.bind('mouseover', self.hover_label)
        self.label.bind('mouseout', self.stop_hover_label)
        self.input.bind('keyup', self.check_return_key)

    def get_html(self):
        print("returning root html from edit label")
        return self.root_div

    def get_value(self):
        return self.label.innerHTML

def get_item_by_id(my_list, my_unique_id):
    print("I am being called")
    print(len(my_list), my_unique_id)
    for item in my_list:
        if item['id'] == my_unique_id:
            my_item = item
            break
    else:
        my_item = None

    return my_item

class panel(basic_container_block):
    def __init__(self, *args, **kwargs):

        # Initialize this first
        super().__init__(*args, **kwargs)

        ###############################################
        # COMPONENTS BUILDING
        # CREATE TOP FORM
        self.form = html.FORM()

        # Buttons
        self.myButt = html.BUTTON("UPDATE PLOT", id=self.genID('myButt'), Class="btn btn-primary btn-sm",
                                  type="button")

        # Div to receive dat
        self.small_div = html.DIV(id=self.genID('small_div'))
        self.small_div <= " THIS IS A SMALL SUB PANEL TO TAKE IN STUFF"

        # Create a form
        self.form <= self.myButt

        # PUT ALL IN MAIN DIV
        self.get_root_div() <= self.form + self.small_div
        self.createBindings()

    def set_panel_style(self, **kwargs):
        if kwargs is not None:
            for key, value in kwargs.items():
                self.panel_style[key] = value

    # BINDINGS
    def createBindings(self):
        self.myButt.bind('click', self.show)

    # EVENT HANDLERS
    def add_numbers_ajax(self, request):

        if request.status == 200 or request.status == 0:
            print("I AM HERE ON DIV PLOT", self.get_root_div().id)
            plotly_return = json.loads(request.responseText)
            jq_div_name = ''.join(['#', self.small_div.id])

            parent_div = self.small_div.parent
            print(parent_div.id)
            # Append Plotly Plot to the panel
            jq(jq_div_name).append(plotly_return['result'])

    def show(self, ev):
        self.small_div <= 'HELLO I CLICKED HERE'
        self.small_div.style.backgroundColor = 'lightgreen'
        print(locals())

        # Ajax Code
        req = ajax.ajax()
        req.open('POST', '/_add_numbers', True)
        req.bind('complete', self.add_numbers_ajax)
        self.small_div.text = "waiting..."
        print("I AM GETTING A DIV")
        req.send()

