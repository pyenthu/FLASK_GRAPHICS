import os
from yattag import Doc, indent












class base_template_builder():
    def __init__(self, scripts, brython_files):
        self.doc, self.tag, self.text, self.line = Doc().ttl()
        self.basic_builder()
        self.import_scripts(scripts)
        self.import_brython_files(brython_files)

    def basic_builder(self):
        pass

    def get_html(self):
        my_html = indent(self.doc.getvalue())
        return my_html

    def import_scripts(self, scripts):

        if scripts == None:
            return

        with self.doc.tag('head'):

            for script in scripts:
                if script['tag'] == 'script':
                    if 'charset' in script.keys():
                        with self.doc.tag('script', type=script['type'], src=script['src'],
                                          charset=script['charset']):
                            pass
                    else:
                        with self.doc.tag('script', type=script['type'], src=script['src']):
                            pass


                if script['tag'] == 'link':
                    with self.doc.tag('link', rel=script['rel'], href=script['href']): pass

    def import_brython_files(self, brython_files):
        if brython_files == None:
            return
        with self.doc.tag('body', onload='brython()'):
            with self.doc.tag('script', type='text/python3'):
                for py_file in brython_files:
                    module = open(os.path.join(os.getcwd(), py_file)).read()
                    self.doc.asis(module)
