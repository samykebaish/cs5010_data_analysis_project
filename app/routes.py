from app import app
from flask import render_template

data = []

@app.route('/')
@app.route('/index')
def index():
    data = {'Data': 'Dataset'}
    return render_template('index.html', title='Home', data=data)


@app.route('/data_dictionary')
def data_dictionary():
    return render_template('data_dictionary.html', title='Data Dictionary', data=data)

@app.route('/data_analysis')
def data_analysis():
    return render_template('data_analysis.html', title='Data Analysis', data=data)


# @app.route('/data_analysis')
# def data_dictionary():
#     return render_template('data_analysis.html', title='data_analysis', data=data)