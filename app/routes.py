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
from analysis import choromap
# from flask.ext.wtf import Form
# from wtforms import IntegerField, StringField, SubmitField, SelectField, DecimalField
# from wtforms.validators import Required
# import pickle
# from sklearn import datasets
df = pd.read_csv('https://csprojectdatavisualizationsample50k.s3.us-east-2.amazonaws.com/sample_df.csv')
print(df.head())
df = df.loc[df['MH1']> 0]
# df['Title'] = df['Name'].apply(lambda x: x.split(',')[1].strip().split(' ')[0])

########################################################################################################################
#                               > CONSTANT VALUES

mh1_2013 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2013_MH1_codes_and_frequencies.csv')
mh2_2013 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2013_MH2_codes_and_frequencies.csv')
mh3_2013 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2013_MH3_codes_and_frequencies.csv')

mh1_2014 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2014_MH1_codes_and_frequencies.csv')
mh2_2014 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2014_MH2_codes_and_frequencies.csv')
mh3_2014 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2014_MH3_codes_and_frequencies.csv')

mh1_2015 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2015_MH1_codes_and_frequencies.csv')
mh2_2015 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2015_MH2_codes_and_frequencies.csv')
mh3_2015 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2015_MH3_codes_and_frequencies.csv')

mh1_2016 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2016_MH1_codes_and_frequencies.csv')
mh2_2016 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2016_MH2_codes_and_frequencies.csv')
mh3_2016 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2016_MH3_codes_and_frequencies.csv')

mh1_2017 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2017_MH1_codes_and_frequencies.csv')
mh2_2017 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2017_MH2_codes_and_frequencies.csv')
mh3_2017 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2017_MH3_codes_and_frequencies.csv')

mh1_2018 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2018_MH1_codes_and_frequencies.csv')
mh2_2018 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2018_MH2_codes_and_frequencies.csv')
mh3_2018 = pd.read_csv('https://mentalhealth-csvs.s3.us-east-2.amazonaws.com/df_2018_MH3_codes_and_frequencies.csv')

mh1_data = [mh1_2013, mh1_2014, mh1_2015, mh1_2016, mh1_2017, mh1_2018]   
mh2_data = [mh2_2013, mh2_2014, mh2_2015, mh2_2016, mh2_2017, mh2_2018]  
mh3_data = [mh3_2013, mh3_2014, mh3_2015, mh3_2016, mh3_2017, mh3_2018]  

palette = ['#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef', '#deebf7', '#f7fbff']

chart_font = 'Helvetica'
chart_title_font_size = '16pt'
chart_title_alignment = 'center'
axis_label_size = '14pt'
axis_ticks_size = '12pt'
default_padding = 30
chart_inner_left_padding = 0.015
chart_font_style_title = 'bold italic'

########################################################################################################################
#                             > HELPER FUNCTIONS

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
    p.yaxis.formatter.use_scientific = False
    p.toolbar.logo = None
    p.toolbar_location = None


def redraw(selected_class):
    print("Roar", selected_class)

    selected_class = int(selected_class)
    if selected_class == 0: # all classes
        dataset = mh1_data[5]
        dataset_2 = mh2_data[5]
        dataset_3 = mh3_data[5]
    elif selected_class >= 2013:
        selected_class = (int(selected_class) - 2013)
    else: # single class
        dataset = mh1_data[selected_class]
        dataset_2 = mh2_data[selected_class]
        dataset_3 = mh3_data[selected_class]

    class_texts = ["2013", "2014", "2015", "2016", "2017", "2018"]
    class_text = class_texts[selected_class]
    survived_chart = survived_bar_chart(dataset, "USA MH1 Incidence for " + class_text)
    survived_chart_2 = survived_bar_chart_2(dataset_2, "USA MH2 Incidence for " + class_text)
    survived_chart_3 = survived_bar_chart_3(dataset_3, "USA MH3 Incidence for " + class_text)

    return (
        survived_chart, survived_chart_2, survived_chart_3
    )


def survived_bar_chart(dataset, title, cpalette=None):

    if cpalette is None:
        cpalette = palette[1:8]

    surv_data = dataset
    surv_data = surv_data.sort_values('MH1 Code', ascending=True)
    surv_possibilities = list(surv_data['MH1 Code'].values)
    surv_values = list(surv_data['MH1 Count'].values)
    print(surv_possibilities, surv_values)
    surv_possibilities_text = ['None', 'PTSD', 'Anxiety', ' (ADD/ADHD)', 'Malconduct', 'Delirium',
    'Bipolar', 'MDD', 'ODD', 'PDD', 'Personality', 'Schizophrenia', 'Substance Abuse', 'Other']
        
        
    source = ColumnDataSource(data={
        'possibilities': surv_possibilities,
        'possibilities_txt': surv_possibilities_text,
        'values': surv_values
    })

    hover_tool = HoverTool(
        tooltips=[('Diagnosis', '@possibilities_txt'),
                  ('Count', '@values')]
    )
    
    p = figure(tools=[hover_tool], plot_height=400, title=title)
    p.vbar(x='possibilities', top='values', source=source, width=0.9,
           fill_color=factor_cmap('possibilities_txt',
                                  palette=palette_generator(len(source.data['possibilities_txt']), cpalette),
                                  factors=source.data['possibilities_txt']))
    
    plot_styler(p)
    p.xaxis.ticker = source.data['possibilities']
    # p.xaxis.major_label_overrides = { 0: 'Did not Survive', 1: 'Survived' }
    p.sizing_mode = 'scale_width'
    
    return p

def survived_bar_chart_2(dataset_2, title, cpalette=None):

    if cpalette is None:
        cpalette = palette[1:8]

    surv_data = dataset_2
    surv_data = surv_data.sort_values('MH2 Code', ascending=True)
    surv_possibilities = list(surv_data['MH2 Code'].values)
    surv_values = list(surv_data['MH2 Count'].values)
    print(surv_possibilities, surv_values)
    surv_possibilities_text = ['None', 'PTSD', 'Anxiety', ' (ADD/ADHD)', 'Malconduct', 'Delirium',
    'Bipolar', 'MDD', 'ODD', 'PDD', 'Personality', 'Schizophrenia', 'Substance Abuse', 'Other']
        
        
    source = ColumnDataSource(data={
        'possibilities': surv_possibilities,
        'possibilities_txt': surv_possibilities_text,
        'values': surv_values
    })

    hover_tool = HoverTool(
        tooltips=[('Diagnosis', '@possibilities_txt'),
                  ('Count', '@values')]
    )
    
    p = figure(tools=[hover_tool], plot_height=400, title=title)
    p.vbar(x='possibilities', top='values', source=source, width=0.9,
           fill_color=factor_cmap('possibilities_txt',
                                  palette=palette_generator(len(source.data['possibilities_txt']), cpalette),
                                  factors=source.data['possibilities_txt']))
    
    plot_styler(p)
    p.xaxis.ticker = source.data['possibilities']
    # p.xaxis.major_label_overrides = { 0: 'Did not Survive', 1: 'Survived' }
    p.sizing_mode = 'scale_width'

    return p

def survived_bar_chart_3(dataset_3, title, cpalette=None):

    if cpalette is None:
        cpalette = palette[1:8]

    surv_data = dataset_3
    surv_data = surv_data.sort_values('MH3 Code', ascending=True)
    surv_possibilities = list(surv_data['MH3 Code'].values)
    surv_values = list(surv_data['MH3 Count'].values)
    print(surv_possibilities, surv_values)
    surv_possibilities_text = ['None', 'PTSD', 'Anxiety', ' (ADD/ADHD)', 'Malconduct', 'Delirium',
    'Bipolar', 'MDD', 'ODD', 'PDD', 'Personality', 'Schizophrenia', 'Substance Abuse', 'Other']
        
    source = ColumnDataSource(data={
        'possibilities': surv_possibilities,
        'possibilities_txt': surv_possibilities_text,
        'values': surv_values
    })

    hover_tool = HoverTool(
        tooltips=[('Diagnosis', '@possibilities_txt'),
                  ('Count', '@values')]
    )
    
    p = figure(tools=[hover_tool], plot_height=400, title=title)
    p.vbar(x='possibilities', top='values', source=source, width=0.9,
           fill_color=factor_cmap('possibilities_txt',
                                  palette=palette_generator(len(source.data['possibilities_txt']), cpalette),
                                  factors=source.data['possibilities_txt']))
    
    plot_styler(p)
    p.xaxis.ticker = source.data['possibilities']
    # p.xaxis.major_label_overrides = { 0: 'Did not Survive', 1: 'Survived' }
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

    return render_template('index.html', graphJSON=choromap, title='Home', data=data)

@app.route('/plots/breast_cancer_data/correlation_matrix', methods=['GET'])
def correlation_matrix():
    bytes_obj = heatmap
    
    return send_file(bytes_obj,
                     attachment_filename='plot.png',
                     mimetype='image/png')

@app.route('/plots/choromap_plot', methods=['GET'])
def choromap_plot():
    bytes_obj_2 = choromap
    
    return send_file(bytes_obj_2,
                     attachment_filename='plot2.png',
                     mimetype='image2/png')

@app.route('/data_dictionary')
def data_dictionary():
    return render_template('data_dictionary.html', title='Data Dictionary', data=data)

@app.route('/data_analysis')
def data_analysis():
    return render_template('data_analysis.html', title='Data Analysis', data=data)

@app.route('/chart', methods=['GET', 'POST'])
def chart():
    selected_class = request.form.get('dropdown-select')
    print("Here, the selected class is : ", selected_class)


    if selected_class is None:
        selected_class = 5
    else:
        selected_class = int(request.form.get('dropdown-select')) 
    
    survived_chart = redraw(selected_class)
    survived_chart_2 = redraw(selected_class)
    survived_chart_3 = redraw(selected_class)

    script_survived_chart, div_survived_chart = components(survived_chart)
    script_survived_chart_2, div_survived_chart_2 = components(survived_chart_2)
    script_survived_chart_3, div_survived_chart_3 = components(survived_chart_3)


    return render_template(
        'bokeh.html',
        div_survived_chart=div_survived_chart,
        script_survived_chart=script_survived_chart,
        div_survived_chart_2=div_survived_chart_2,
        script_survived_chart_2=script_survived_chart_2,
        div_survived_chart_3=div_survived_chart_3,
        script_survived_chart_3=script_survived_chart_3,
    )


# class theForm(Form):
#     param1 = DecimalField(label='Age :', places=2, validators=[Required()])
#     param2 = DecimalField(label='Ethnicity:', places=2, validators=[Required()])
#     param3 = DecimalField(label='Petal Length (cm):', places=2, validators=[Required()])
#     param4 = DecimalField(label='Petal Width (cm):', places=2, validators=[Required()])
#     submit = SubmitField('Submit')

# @app.route('/ML', methods=['GET', 'POST'])
# def ML():
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
#         return redirect(url_for('ML'))

#     return render_template('ml.html', form=form, **session)

