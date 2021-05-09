from app import app
from flask import render_template, send_file, make_response , Flask, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import base64
from analysis import heatmap
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
import pandas as pd
# from flask.ext.wtf import Form
# from wtforms import IntegerField, StringField, SubmitField, SelectField, DecimalField
# from wtforms.validators import Required
# import pickle
# from sklearn import datasets
df_2018= pd.read_csv("https://csprojectdatavisualizationsample50k.s3.us-east-2.amazonaws.com/sample_df.csv")
df_2017 = pd.read_csv("https://csprojectdatavisualizationsample50k.s3.us-east-2.amazonaws.com/sample_df.csv")
# from analysis import do_plot
palette = ['#ba32a0', '#f85479', '#f8c260', '#00c2ba']
df_2017 = df_2017.sample(10000)
data_frames = [df_2017, df_2018]

chart_font = 'Helvetica'
chart_title_font_size = '16pt'
chart_title_alignment = 'center'
axis_label_size = '14pt'
axis_ticks_size = '12pt'
default_padding = 30
chart_inner_left_padding = 0.015
chart_font_style_title = 'bold italic'

def mh_bar_chart(dataset, title, cpalette=palette[1:3]):
    mh_data = df_2018
    # mh_possibilities = mh_data['MH1'].value_counts().keys().tolist()
    # mh_values = mh_data['MH1'].value_counts().values
    # mh_possibilities_text = ['Trauma- and stressor-related disorders', 'Anxiety disorders', 'Attention deficit/hyperactivity disorder (ADD/ADHD)'
    # 'Conduct disorders', 'Delirium, dementia', 'Bipolar disorders', 'Depressive disorders', 'Oppositional defiant disorders', 'Pervasive developmental disorders', 'Personality disorders'
    # 'Schizophrenia or other psychotic disorders', 'Alcohol or substance use disorders', 'Other disorders/conditions', 'Missing/unknown/not collected/invalid/no or deferred diagnosis ', 'x', 'y']
     
    mh_possibilities = ['A', 'B', 'C', 'D']
    mh_values = [1,2,3,4]
    mh_possibilities_text = ['A', 'B', 'C', 'D']
    source = ColumnDataSource(data={
        'mh_values': mh_values,
        'mh_possibilities_text': mh_possibilities_text,
        'mh_values': mh_values
    })

    hover_tool = HoverTool(
        tooltips=[('Diagnoses', '@mh_possibilities_txt'), ('Count', '@mh_values')]
    )

    p = figure(tools=[hover_tool], plot_height=400, title='MH1 Disease Distribution')
    p.vbar(x='mh_possibilities_text', top='mh_values', source=source, width=0.9,
           fill_color=factor_cmap('mh_possibilities_text', palette=palette_generator(len(source.data['mh_possibilities_text']), cpalette), factors=source.data['mh_possibilities_text']))
    
    plot_styler(p)
    p.xaxis.ticker = source.data['mh_values']
    p.xaxis.major_label_overrides = { 0: 'Did not Survive', 1: 'Survived' }
    p.sizing_mode = 'scale_width'
    
    return p


def palette_generator(length, palette):
    int_div = length // len(palette)
    remainder = length % len(palette)
    return (palette * int_div) + palette[:remainder]


def plot_styler(p):
    p.title.text_font_size = chart_title_font_size
    p.title.text_font  = chart_font
    p.title.align = chart_title_alignment
    p.title.text_font_style = chart_font_style_title
    p.y_range.start = 0
    p.x_range.range_padding = chart_inner_left_padding
    p.xaxis.axis_label_text_font = chart_font
    p.xaxis.major_label_text_font = chart_font
    p.xaxis.axis_label_standoff = default_padding
    p.xaxis.axis_label_text_font_size = axis_label_size
    p.xaxis.major_label_text_font_size = axis_ticks_size
    p.yaxis.axis_label_text_font = chart_font
    p.yaxis.major_label_text_font = chart_font
    p.yaxis.axis_label_text_font_size = axis_label_size
    p.yaxis.major_label_text_font_size = axis_ticks_size
    p.yaxis.axis_label_standoff = default_padding
    p.toolbar.logo = None
    p.toolbar_location = None


def redraw(selected_class):
    # mh_bar_chart = mh_bar_chart(df, selected_class)
    mh_years = ['2013', '2014', '2015', '2016', '2017', '2018']
    mh_year = mh_years[0] 
    mh_chart = mh_bar_chart(df_2018, mh_year)



    return (
        mh_chart,
    )



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

@app.route('/chart', methods=['GET', 'POST'])
def chart():
    selected_mh_class = request.form.get('dropdown-select')

    # if selected_mh_class == 0 or selected_mh_class == None:
    #     mh_bar_chart = redraw(0)
    # else:
    #     mh_bar_chart = redraw(selected_mh_class)

    mh_bar_chart = redraw(selected_mh_class)
    script_mh_bar_chart, div_mh_bar_chart= components(mh_bar_chart)


    return render_template(
        'bokeh.html',
        div_mh_bar_chart=div_mh_bar_chart,
        script_mh_bar_chart= script_mh_bar_chart
    )



# def class_titles_bar_chart(dataset, pass_class, cpalette=palette):
#     ttl_data = dataset[dataset['Pclass'] == int(pass_class)]
#     title_possibilities = list(ttl_data['Title'].value_counts().index)
#     title_values = list(ttl_data['Title'].value_counts().values)
#     int_possibilities = np.arange(len(title_possibilities))
    
#     source = ColumnDataSource(data={
#         'titles': title_possibilities,
#         'titles_int': int_possibilities,
#         'values': title_values
#     })

#     hover_tool = HoverTool(
#         tooltips=[('Title', '@titles'), ('Count', '@values')]
#     )
    
#     chart_labels = {}
#     for val1, val2 in zip(source.data['titles_int'], source.data['titles']):
#         chart_labels.update({ int(val1): str(val2) })
        
#     p = figure(tools=[hover_tool], plot_height=300, title='Titles for Current Class')
#     p.vbar(x='titles_int', top='values', source=source, width=0.9,
#            fill_color=factor_cmap('titles', palette=palette_generator(len(source.data['titles']), cpalette), factors=source.data['titles']))
    
#     plot_styler(p)
#     p.xaxis.ticker = source.data['titles_int']
#     p.xaxis.major_label_overrides = chart_labels
#     p.xaxis.major_label_orientation = math.pi / 4
#     p.sizing_mode = 'scale_width'
    
#     return p


# def age_hist(dataset, pass_class, color=palette[1]):
#     hist, edges = np.histogram(dataset[dataset['Pclass'] == int(pass_class)]['Age'].fillna(df['Age'].mean()), bins=25)
    
#     source = ColumnDataSource({
#         'hist': hist,
#         'edges_left': edges[:-1],
#         'edges_right': edges[1:]
#     })

#     hover_tool = HoverTool(
#         tooltips=[('From', '@edges_left'), ('Thru', '@edges_right'), ('Count', '@hist')], 
#         mode='vline'
#     )
    
#     p = figure(plot_height=400, title='Age Histogram', tools=[hover_tool])
#     p.quad(top='hist', bottom=0, left='edges_left', right='edges_right', source=source,
#             fill_color=color, line_color='black')

#     plot_styler(p)
#     p.sizing_mode = 'scale_width'

#     return p





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