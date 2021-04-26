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


heatmap = do_plot()


    # data = load_breast_cancer()
    # breast_cancer_df = pd.DataFrame(data['data'])
    # breast_cancer_df.columns = data['feature_names']
    # breast_cancer_df['target'] = data['target']
    # breast_cancer_df['diagnosis'] = [data['target_names'][x] for x in data['target']]
    # feature_names= data['feature_names']

    # corr = breast_cancer_df[list(feature_names)].corr(method='pearson')

    # f, ax = plt.subplots(figsize=(11, 9))
    # cmap = sns.diverging_palette(220, 10, as_cmap=True)
    # mask = np.zeros_like(corr, dtype=np.bool)
    # mask[np.triu_indices_from(mask)] = True

    # sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
    #             square=True, linewidths=.5, cbar_kws={"shrink": .5})

    # # here is the trick save your figure into a bytes object and you can afterwards expose it via flas
    # bytes_image = io.BytesIO()
    # plt.savefig(bytes_image, format='png')
    # bytes_image.seek(0)
    # return bytes_image