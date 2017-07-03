import random
from pandas import json
from pprint import pprint
from flask import Flask, render_template, render_template_string, make_response, jsonify
from flask_bower import Bower
from gowell_mtd_mfc import make_basic_plot, gowell_plot_div, gowell_plot_json
from MISC.plotly_basic import modify_basic_plot, make_basic_plot
from MISC.mpl_trial import create_mpl_response
from try_mpld3 import try_mpld3_html

app = Flask(__name__)
Bower(app)


@app.route('/')
def hello_world():
    return render_template('MISC/trial_xtk/trial.html')


@app.route('/2')
def try2():
    pprint("HELLO")
    # return render_template('trial_xtk/trial2.html')
    return ("HELLO WORLD")


@app.route('/3')
def three():
    return render_template('MISC/three_try.html')


@app.route('/mpl')
def render_basic():
    # return("Hello World")
    render_template('MISC/flask_jinja_pyplot/submit.html')


@app.route('/mpl/get_image')
def get_flask():
    response = make_response(create_mpl_response())
    response.content_type = 'image/svg+xml'
    return response


@app.route('/px')
def newpage():
    try:
        # generate some random integers, sorted
        exponent = .7 + random.random() * .6
        dta = []
        for i in range(5):
            rnum = int((random.random() * 10) ** exponent)
            dta.append(rnum)
            y = sorted(dta)
            x = range(len(y))
        return render_template('MISC/flask_jinja_pyplot/figures.html', y=y)

    except Exception as e:
        pprint(e)


@app.route('/ex')
def indexPage():
    try:
        return render_template('MISC/flask_jinja_pyplot/figures.html', y=y)

    except Exception as e:
        pprint(e)


@app.route('/trans')
def new_trans():
    try:
        return render_template('TRANS/trans_hello.html')

    except Exception as e:
        pprint(e)


@app.route('/jqdemo')
def jqdemo():
    try:
        return render_template('TRANS/jquery_demo.html')

    except Exception as e:
        pprint(e)


@app.route('/d3demo')
def trans_d3():
    try:
        return render_template('TRANS/d3_demo.html')

    except Exception as e:
        pprint(e)


@app.route('/mathbox')
def mathbox():
    try:
        return render_template('derived_three.html')  # 'threestrap.html')

    except Exception as e:
        pprint(e)


@app.route('/mpld_eg', methods=['GET', 'POST'])
def mpld_eg():
    try:
        # return render_template_string(try_mpld3_html())
        return try_mpld3_html()
    except Exception as e:
        pprint(e)


@app.route('/plotly', methods=['GET', 'POST'])
def plotly():
    try:
        get_plotly_plot = make_basic_plot()
        return render_template('PLOTLY/plotly_base.html')

    except Exception as e:
        pprint(e)

@app.route('/go_plotly_div', methods=['GET', 'POST'])
def go_plot_div():
    try:
        return gowell_plot_div()
    except Exception as e:
        pprint(e)

@app.route('/go_plotly_json', methods=['GET', 'POST'])
def go_plot():
    try:
        return gowell_plot_json()
    except Exception as e:
        pprint(e)

@app.route('/plotly_ajax', methods=['GET', 'POST'])
def plotly_ajax():

    try:
        return make_basic_plot()

    except Exception as e:
        pprint(e)


@app.route('/get_new_data', methods=['GET', 'POST'])
def high_update():
    try:
        return modify_basic_plot()

    except Exception as e:
        pprint(e)


if __name__ == '__main__':
    app.run(debug=True)
