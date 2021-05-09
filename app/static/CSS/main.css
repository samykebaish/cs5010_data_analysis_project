from app import app
from flask import render_template, send_file, make_response 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import base64
from analysis import heatmap
# from flask.ext.wtf import Form
# from wtforms import IntegerField, StringField, SubmitField, SelectField, DecimalField
# from wtforms.validators import Required
# import pickle
# from sklearn import datasets


# from analysis import do_plot

data = []

@app.route('/')

@app.route('/index')
def index():

    data = {'Data': 'Dataset'}
    # bytes_obj = do_plot()
        # Generate plot
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("title")
    axis.set_xlabel("x-axis")
    axis.set_ylabel("y-axis")
    axis.grid()
    axis.plot(range(5), range(5), "ro-")
    
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    #FigureCanvas(heatmap).print_png(pngImage2)
    
    # Encode PNG image to base64 string
    #pngImageB64String = "data:image/png;base64,"
    #pngImageB64String += base64.b64encode(pngImage2.getvalue()).decode('utf8')

#     byte_str = heatmap.read()

# # Convert to a "unicode" object
#     text_obj = byte_str.decode('UTF-8')  # Or use the encoding you expect

# Use text_obj how you see fit!
# io.StringIO(text_obj) will get you to a StringIO object if that's what you need
    

    # return render_template('index.html', title='Home', data=data, bytes_obj=bytes_obj, image=pngImageB64String)
    return render_template('index.html', title='Home', data=data)

@app.route('/plots/breast_cancer_data/correlation_matrix', methods=['GET'])
def correlation_matrix():
    bytes_obj = heatmap
    
    return send_file(bytes_obj,
                     attachment_filename='plot.png',
                     mimetype='image/png')

@app.route('/data_dictionary')
def data_dictionary():
    return render_template('data_dictionary.html', title='Data Dictionary', data=data)

@app.route('/data_analysis')
def data_analysis():
    return render_template('data_analysis.html', title='Data Analysis', data=data)


# @app.route('/data_analysis')
# def data_analysis():
#     return render_template('data_analysis.html', title='Data Analysis', data=data)


# class theForm(Form):
#     param1 = DecimalField(label='Sepal Length (cm):', places=2, validators=[Required()])
#     param2 = DecimalField(label='Sepal Width (cm):', places=2, validators=[Required()])
#     param3 = DecimalField(label='Petal Length (cm):', places=2, validators=[Required()])
#     param4 = DecimalField(label='Petal Width (cm):', places=2, validators=[Required()])
#     submit = SubmitField('Submit')


# @app.route('/', methods=['GET', 'POST'])
# def home():
#     print(session)
#     form = theForm(csrf_enabled=False)
#     if form.validate_on_submit():  # activates this if when i hit submit!
#         # Retrieve values from form
#         session['sepal_length'] = form.param1.data
#         session['sepal_width'] = form.param2.data
#         session['petal_length'] = form.param3.data
#         session['petal_width'] = form.param4.data
#         # Create array from values
#         flower_instance = [(session['sepal_length']), (session['sepal_width']), (session['petal_length']),
#                            (session['petal_width'])]

#         # Return only the Predicted iris species
#         flowers = ['setosa', 'versicolor', 'virginica']
#         session['prediction'] = flowers[machine_learning_model.predict(flower_instance)[0]]

#         # Implement Post/Redirect/Get Pattern
#         return redirect(url_for('home'))

#     return render_template('home.html', form=form, **session)


# @app.route('/data_analysis')
# def data_dictionary():
#     return render_template('data_analysis.html', title='data_analysis', data=data)