from SELAN_PLOTS.templates.base_yattag_builder import base_template_builder

class webix_builder(base_template_builder):
    def __init__(self):
        # Specify imports
        scripts = [
            {'tag': 'script', 'type': 'text/javascript', 'src': '/static/brython_lib/brython.js'},
            {'tag': 'script', 'type': 'text/javascript', 'src': '/static/brython_lib/brython_stdlib.js'},

            {'tag': 'script', 'type': 'text/javascript', 'src': '/static/plotly.min.js'},

            {'tag': 'script', 'type': 'text/javascript',
             'src': 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js'},

            {'tag': 'script', 'type': 'text/javascript',
             'src': "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"},

            {'tag': 'link', 'rel': 'stylesheet',
             'href': "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"},

            {'tag': 'script', 'type': 'text/javascript', 'src': '/static/jq_ui_bs/js/jquery-1.8.3.min.js'},

            {'tag': 'script', 'type': 'text/javascript', 'src': '/static/moment.js'},

            {'tag': 'script', 'type': 'text/javascript', 'src': '/static/jq_ui_bs/js/jquery-ui-1.9.2.custom.min.js'},

            {'tag': 'link', 'rel': 'stylesheet',
             'href': "/static/jq_ui_bs/css/custom-theme/jquery-ui-1.9.2.custom.css"},

            {'tag': 'script', 'type': 'text/javascript', 'src': '/static/jq_range_slider/JQDateRangeSlider-min.js'},

            {'tag': 'link', 'rel': 'stylesheet','href': "/static/jq_range_slider/css/iThing-min.css"},

        ]

        '''Brython files must be declared in the order of usage. Classes must be defined before using'''
        ''' Cannot share variables in different scripts'''

        brython_files = ['brython_components/brython_imports.py',
                         'brython_components/basic_components.py',
                         'brython_components/bootstrap_tab.py',
                         'CLIENT_APPS/sandbox/templates/webix_client.py'
                         ]

        super().__init__(scripts, brython_files)

    def basic_builder(self):
        self.doc.asis('<!DOCTYPE html>')
        with self.tag('html', lang='en'):
            with self.tag('head'):
                with self.tag('meta', charset="utf-8"): pass
                with self.tag('meta', name='viewport', content='width=device-width, initial-scale=1'): pass
