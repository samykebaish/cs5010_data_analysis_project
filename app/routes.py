from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    data = {'Data': 'Dataset'}
    return render_template('index.html', title='Home', data=data)


@app.route('/data_dictionary')
def data_dictionary():
    return render_template('about.html', title='Data Dictionary', data=data)