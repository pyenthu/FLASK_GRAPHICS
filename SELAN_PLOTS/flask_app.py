import os
from pprint import pprint
import arrow
import yaml
from flask import Flask, request, jsonify
from SELAN_PLOTS.CLIENT_APPS.multi_well_swabbing.html_build_multi_well_swabbing import multi_well_swabbing_html
from SELAN_PLOTS.CLIENT_APPS.sandbox.templates.webix_html_builder import webix_builder
from SELAN_PLOTS.CLIENT_APPS.single_well_multi_plots.html_build_single_well_multi_plots import \
    single_well_multi_plot_html













app = Flask(__name__)

from SELAN_PLOTS.make_plots import swabbing_data_plots

swabbing_data_pack = swabbing_data_plots()

@app.route('/')
def hello_world():
    return "HELLO THIS IS JUST A CHECK"

@app.route('/webix_try')
def webix_try():
    my_tag = webix_builder()
    return my_tag.get_html()

@app.route('/_get_min_max_range', methods=['POST'])
def get_min_max():
    try:
        print ('******************* REQUEST RECEIVED')
        property = request.form.get('prop_name')
        well_name = request.form.get('well_name')
        result = swabbing_data_pack.get_min_max(well_name, property)
        print (result)
        return jsonify(result)
    except Exception as e:
        print("_get_min_maxERROR", e)

@app.route('/_get_filtered_plot', methods=['POST'])
def get_filtered_plot():
    try:
        well_name = request.form.get('well_name')
        plot_name = request.form.get('plot_name')
        property = request.form.get('prop_name')
        dtype = request.form.get('dtype')
        if 'date' in dtype:
            min = arrow.get(request.form.get('min')).datetime
            max = arrow.get(request.form.get('max')).datetime
            print("ARROW ", min, max)
            print("string date", request.form.get('min'), request.form.get('max'))
        else:
            min = request.form.get('min')
            max = request.form.get('max')

        filters = []
        filters.append(dict(property=property, min=min, max=max))

        plot_data = swabbing_data_pack.make_plots(well_name, plot_name, filters, 'json')

        return plot_data
    except Exception as e:
        print("_get_filtered_plot  ERROR", e)


@app.route('/_get_well_data', methods=['POST'])
def get_well_data():
    try:
        well_name = request.form.get('well_name')
        prop_name = request.form.get('prop_name')
        print('getting data for ', well_name, prop_name)
        data_series = swabbing_data_pack.get_prop(well_name, prop_name)

        print(data_series.dtype)

        return jsonify(dict(series=data_series.tolist(), data_type=str(data_series.dtype)))

    except Exception as e:
        print("GET DATA ERROR  ", e)
        raise e


@app.route('/swabbing/<well_name>')
def swabbing_well_plot(well_name):
    print("IN FLASK APP", 'SWABBING', well_name)
    return swabbing_data_pack.make_plots(well_name, 'SWABBING', 'div')

@app.route('/production/<well_name>')
def production_well_plot(well_name):
    print("IN FLASK APP", 'PRODUCTION', well_name)
    return swabbing_data_pack.make_plots(well_name, 'PRODUCTION', 'div')

@app.route('/well_plots')
def well_plots():
    my_tag = single_well_multi_plot_html()
    return my_tag.get_html()

@app.route('/_get_well_plots', methods=['POST'])
def get_well_plots():
    meta_list = request.form.getlist('send_request')
    plot_list = []
    for item in meta_list:
        plot_list.append(yaml.load(item))
    print(plot_list[0], plot_list[1])
    return jsonify(get_plots(plot_list))


@app.route('/_get_well_plot', methods=['POST'])
def get_well_plot():
    well_name = request.form.get('well_name')
    plot_name = request.form.get('plot_name')
    tab_id = request.form.get('tab_id')

    print(well_name, plot_name, tab_id)

    return jsonify({'tab_content': make_plots(well_name, plot_name),
                    'well_name': well_name,
                    'plot_name': plot_name,
                    'tab_id': tab_id
                    })


@app.route('/multi_well_swabbing')
def multi_well_swabbing():
    my_tag = multi_well_swabbing_html()
    return my_tag.get_html()


@app.route('/_get_well_list', methods=['POST'])
def get_well_list():
    try:
        print("HELLO THIS IS A REQUEST FOR WELL LIST FROM FILE")
        well_list = get_well_list_from_file()
        return jsonify(result=well_list)

    except Exception as e:
        return (e)

if __name__ == '__main__':
    package_path = os.getcwd()
    package_MISC = os.path.join(package_path, 'MISC')
    pprint(package_path)
    app.run(debug=True)
