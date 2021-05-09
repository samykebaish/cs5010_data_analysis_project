from app import app
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
from sklearn.datasets import load_breast_cancer

def do_plot():
    mental_health_df = pd.read_csv("https://csprojectdatavisualizationsample50k.s3.us-east-2.amazonaws.com/sample_df.csv")

    corr =mental_health_df.corr(method='pearson')

    f, ax = plt.subplots(figsize=(11, 9))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})

    # here is the trick save your figure into a bytes object and you can afterwards expose it via flas
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image


################################################################################
#                            - END OF MAIN ROUTE -                             #
################################################################################


################################################################################
#                        > CHART GENERATION FUNCTIONS                          #
################################################################################

def survived_bar_chart(dataset, pass_class, cpalette=palette[1:3]):
    surv_data = dataset[dataset['Pclass'] == int(pass_class)]
    surv_possibilities = list(surv_data['Survived'].value_counts().index)
    surv_values = list(surv_data['Survived'].value_counts().values)
    surv_possibilities_text = ['Did not Survive', 'Survived']
        
    source = ColumnDataSource(data={
        'possibilities': surv_possibilities,
        'possibilities_txt': surv_possibilities_text,
        'values': surv_values
    })

    hover_tool = HoverTool(
        tooltips=[('Survived?', '@possibilities_txt'), ('Count', '@values')]
    )
    
    p = figure(tools=[hover_tool], plot_height=400, title='Did/Did not Survive for Current Class')
    p.vbar(x='possibilities', top='values', source=source, width=0.9,
           fill_color=factor_cmap('possibilities_txt', palette=palette_generator(len(source.data['possibilities_txt']), cpalette), factors=source.data['possibilities_txt']))
    
    plot_styler(p)
    p.xaxis.ticker = source.data['possibilities']
    p.xaxis.major_label_overrides = { 0: 'Did not Survive', 1: 'Survived' }
    p.sizing_mode = 'scale_width'
    
    return p


def class_titles_bar_chart(dataset, pass_class, cpalette=palette):
    ttl_data = dataset[dataset['Pclass'] == int(pass_class)]
    title_possibilities = list(ttl_data['Title'].value_counts().index)
    title_values = list(ttl_data['Title'].value_counts().values)
    int_possibilities = np.arange(len(title_possibilities))
    
    source = ColumnDataSource(data={
        'titles': title_possibilities,
        'titles_int': int_possibilities,
        'values': title_values
    })

    hover_tool = HoverTool(
        tooltips=[('Title', '@titles'), ('Count', '@values')]
    )
    
    chart_labels = {}
    for val1, val2 in zip(source.data['titles_int'], source.data['titles']):
        chart_labels.update({ int(val1): str(val2) })
        
    p = figure(tools=[hover_tool], plot_height=300, title='Titles for Current Class')
    p.vbar(x='titles_int', top='values', source=source, width=0.9,
           fill_color=factor_cmap('titles', palette=palette_generator(len(source.data['titles']), cpalette), factors=source.data['titles']))
    
    plot_styler(p)
    p.xaxis.ticker = source.data['titles_int']
    p.xaxis.major_label_overrides = chart_labels
    p.xaxis.major_label_orientation = math.pi / 4
    p.sizing_mode = 'scale_width'
    
    return p


def age_hist(dataset, pass_class, color=palette[1]):
    hist, edges = np.histogram(dataset[dataset['Pclass'] == int(pass_class)]['Age'].fillna(df['Age'].mean()), bins=25)
    
    source = ColumnDataSource({
        'hist': hist,
        'edges_left': edges[:-1],
        'edges_right': edges[1:]
    })

    hover_tool = HoverTool(
        tooltips=[('From', '@edges_left'), ('Thru', '@edges_right'), ('Count', '@hist')], 
        mode='vline'
    )
    
    p = figure(plot_height=400, title='Age Histogram', tools=[hover_tool])
    p.quad(top='hist', bottom=0, left='edges_left', right='edges_right', source=source,
            fill_color=color, line_color='black')

    plot_styler(p)
    p.sizing_mode = 'scale_width'

    return p

################################################################################
#                    - END OF CHART GENERATION FUNCTIONS -                     #
################################################################################


    # return bytes_image