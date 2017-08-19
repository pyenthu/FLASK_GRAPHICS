from SELAN_PLOTS.templates.base_yattag_builder import base_template_builder

class multi_well_swabbing_html(base_template_builder):
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

            {'tag': 'link', 'rel': 'stylesheet',
             'href': "https://cdnjs.cloudflare.com/ajax/libs/x-editable/1.5.0/bootstrap3-editable/css/bootstrap-editable.css"},

            {'tag': 'script', 'type': 'text/javascript',
             'src': "https://cdnjs.cloudflare.com/ajax/libs/x-editable/1.5.0/bootstrap3-editable/js/bootstrap-editable.min.js"}
        ]

        '''Brython files must be declared in the order of usage. Classes must be defined before using'''
        ''' Cannot share variables in different scripts'''

        brython_files = ['/brython_components/brython_imports.py',
                         '/brython_components/basic_components.py',
                         '/brython_components/bootstrap_tab.py',
                         '/CLIENT_APPS/multi_well_swabbing/client_brython_multi_well_swabbing.py'
                         ]

        super().__init__(scripts, brython_files)

    def basic_builder(self):
        self.doc.asis('<!DOCTYPE html>')
        with self.tag('html', lang='en'):
            with self.tag('head'):
                with self.tag('meta', charset="utf-8"): pass
                with self.tag('meta', name='viewport', content='width=device-width, initial-scale=1'): pass
