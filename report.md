# CS 5010 Semester Project: Mental Health

Kelly Farell - knf7vg@virginia.edu
Samy Kebaish - sak3qf@virginia.edu  
Gretchen Larrick - jem37b@virginia.edu

## Introduction
Mental health impacts everyone on an individual level, but it can be hard to visualize what the distribution of mental illness and treatment are across the United States. Using descriptive statistics, exploratory analyses, and an interactive website complete with visualizations was created to help patients, treatment providers, and the general public engage with diagnostic and healthcare information regarding mental illness and care. Additionally, trend analyses and traditional and machine-learning (ML) modeling methods were used to observe shifts over time and predict level of care and mental health diagnoses.

## Datasets
Our primary datasets include Adult and Child Health Care Quality Measures for fiscal year 2018. Each year, the Centers for Medicare and Medicaid Services (CMS) collects benchmark data from a variety of treatment providers, with the goal of summarizing the quality of care received by adult Medicaid recipients and CHIP beneficieries.  We also used the Mental Health Client-Level Data (MH-CLD) from SAHMSA (Substance Abuse and Mental Health Services Administration, a part of the US Department of Health and Human Services). We primarily focused on the year 2018, but trend analyses included data from 2013-2018. For some supplemental information regarding poverty by state, we utilized the Kaiser Family Foundation's State Facts database summarizing poverty rate by race and ethnicity, and geoJson files containing location coordinates for US state boundaries (Story and Fernandez, 2016), and state abbreviation/FIPS (World Population Review (n.d.)) to generate choropleths and merge datasets which utilized different encoding methods for state.

![Dimensions](assets/markdown-img-paste-20210508195455393.png)
Table 1: Dimensions of the primary datasets used in analysis and modeling mental health and treatment in the United States.

### Adult and Child Health Care Quality Measures
The Social Security Act enacted by the federal government requires that an annual report of predefined core measures of healthcare quality for adult Medicaid enrollees. Based on data from electronic health records and reports from treatment centers which accept Medicaid and CHIP, this dataset contains state-level performance rates for many aspects of health, including behavioral healthcare, prenatal and pregnancy-related healthcare, and early childhood care. Reporting rates vary considerably across measures--newly defined or updated measures often have lower participation rates due to the required changes that must be made to a state's health department infrastructure necessary to support the changes to research methodology.

### MH-CLD
The Mental Health Client-Level Data contain demographic, diagnoses, and treatment setting and outcome for individuals receiving services through their state mental health agency. The analyses and modeling relied on variables such as education, race, ethnicity, age, gender, primary, secondary, and tertiary mental health diagnoses, and indicators of diagnosis in a variety of illness categories (such as depressive disorders or personality disorders).

These data are somewhat limited--although the year was reported, months and days were excluded. These details would provide supplemental benefit due to the seasonality of depression. For example, in a study by Ayers et al. in 2013, Google mental health queries monitored from 2006 to 2010 revealed seasonal patterns for all mental health queries, with winter peaks and summer troughs (14% difference in the United States; 11% difference for Australia).

### KFF Datasets
Based on US Census surveys, the Kaiser Family Foundation estimated the rate of people living at or under the federal poverty line for the year 2018 and grouped that data by state, race, and ethnicity.

### Geographic Data

## Tech Stack
Code was written in Jupyter Notebook (Kluyver et al., 2016) for reproducibility and easy annotation.

Much of the exploratory data analysis was conducted with functions imported from NumPy (Harris et al., 2020) and Pandas (McKinney et al., 2010).

Visualizations for the exploratory data analysis were produced using Matplotlib (Hunter et al., 2007) and seaborn (Waskom et al., 2017). Plotly (Plotly Technologies Inc, 2015) was used to create further exploratory visualizations, as well as interactive graphics such as choropleths for the website.

Plots related to the logistic regression and advanced ML modeling were created using Plotly (2015) and bokeh (Bokeh Development Team, 2021).

Code for modeling was primarily written using Scikit (Pedregosa et al., 2011), Keras (Chollet et al., 2015), and _Flask (Grinberg, 2018). The website was hosted by AWS.

## Preprocessing
The datasets were carefully cleaned by the governmental and nongovernmental research agencies prior to publishing, so little preprocessing was required. However, null/missing values needed to be accounted for and the datasets needed to be merged together for some of the analyses.

### Irrelevant Data
Rows from the Adult and Child Health Care Quality Measures dataset which involved measures from treatment domains other than "Behavioral Health" were removed in order to focus on measures related to mental health. The rows were identified by filtering out rows from the column "Domain" which were not equal to "Behavioral Health" and excluding them from the dataset.

### Null Data
Null data in the MH-CLD and Adult and Child Health Care Quality Measures datasets were encoded using "#NR" or -9. These cells were removed prior to analysis and modeling. Since in nearly all cases, the data was categorical, some outlier handling techniques such as imputation with median values or upper quartile values was not possible.

### Joining Datasets
The Health Care Quality Measures dataset was merged with the folio state abbreviation list from World Population Review (n.d.) using state code/abbreviation as the shared identifier. The MH-CLD dataset was joined with the same state abbreviation list using the USPS state name as the shared identifier.

Finally, the merged Health Care Quality Measures data and merged MH-CLD data were then joined using the state code/abbreviation as the shared identifier.

## Exploratory Data Analysis
With the data cleaned, relevant descriptive statistics and other trends could be identified in order to inform the visualizations and prediction models.
### MH-CLD
#### Single Variable Analysis

The MH-CLD data set consists of a large number of categorical variables corresponding to a specific state.  To understand the data, the first object was the look at the total number of entries per state, Figure X.  

![Figure X](totalstates.png)

The next part of the exploratory analysis was to sort through the guidebook provided by  SAMHA detailing the breakdown of the variables in the dataset. Age and mental health diagnosis have a high number of populated categories so these were the main areas of focus. 

The first to explore is age. The variable is not an integer age, but a range of ages. The first goal is to get a visualization of each age group‘s total count, figure y. This shows that the 0-11 age group has a significant number of higher cases than the other age groups. 

![Figure y](agetotals.png)

With the dataset broken down into states, the data is then group into age groups by state, figure y. Again, the 0-11 age range has the highest number of cases in a majority of the states.

![Figure z](agebystate.png)

The same analysis was completed on the mental health diagnosis variable. The totals for each mental health diagnosis are shown in figure a. Depression has the highest number of cases in this dataset. 

![Figure a](mh1total.png)

The variable is then broken down by state, figure z, and the conclusion of which mental health diagnosis is the highest isn’t as clear as with the age analysis. The breakdown of the state mental health diagnosis is much more varied. 

![Figure b](mh1state.png)

#### Multivariable Analysis

After looking at age and mental health diagnosis separately, how do these two variables relate to each other? In figure c, age ranges are grouped by their mental health diagnosis. From this, it is seen that the depressive mental health diagnosis is prominent in most of the age groups, with a higher instance after an individual is over the age of 15. 

![Figure b](agemh1multi.png)

There is a difference in diagnoses for individuals who are over 18 in relation to individuals under the age of 18. Individuals under the age of 18 have a much higher number of cases in the ADD/ADHD, Trauma/Stressors, and Oppositional Defiant Disorders categories. After the age of 18, there is an increase in depression, but it varies in the over 18 age groups, but each group remains higher individually than the under 18 age groups. 

### Adult and Child Health Care Quality Measures
Overall, the measures using the adult population had a higher percentage of nonmissing data than the child population. On the documentation for the original dataset, SAHMSA indicates that comparison of the child dataset with past years may not be fasible because some measures were only created or standardized in recent years. As a result of the changes, many states do not have sufficient data to be included in the analyses.

![image replacement text.png](assets/markdown-img-paste-20210508154159182.png)
Figure 1: National Average Performance on Health Care Quality Measure (child population - right, adult population - left)

![choropleth2](assets/markdown-img-paste-20210508162358255.png)
Choroleth 1: The percentage of adults who received a follow-up visit with an outpatient treatment provider after discharge from hospitalization for mental illness, by US state

![choropleth1](assets/markdown-img-paste-20210508162327861.png)
Choropleth 2: The percentage of adults who received a follow-up visit with an outpatient treatment provider after an emergency room visit for mental illness, by US state

## General Linearized Model

### Principal Component Analysis
A Principal Component Analysis was used to evaluate all variables in the combined CLD-Health Care Quality Measures dataset.
![fig5.png](assets/markdown-img-paste-20210508161115359.png)

![fig2.png](assets/markdown-img-paste-20210508160144910.png)
### Logistic Regression
![fig3.png](assets/markdown-img-paste-20210508160836455.png)
![fig4.png](assets/markdown-img-paste-20210508160938792.png)
## Trend Analysis

## Above and Beyond: Advanced ML Methods and Interactive Website

### Naive Bayes

### k-Nearest Neighbors

### Multilabel Classification Optimization

### Interactive Website
A website complete with user-interactive visualizations was created to encourage engagement with the datasets and analyses. The choropleths show the raw percentages for the Health Care Quality measure performance of a given state when the user hovers their mouse over it. Additionally ....

## Unit Testing
Testing was performed to  ...
## Conclusions

## Future Research Opportunities
Will trends change over the next few years due to covid-19?
Minority oversampling and future linear analyses
Other variables that could contribute

## Works Cited
Ayers, J. W., Althouse, B. M., Allem, J. P., Rosenquist, J. N., & Ford, D. E. (2013). Seasonality in seeking mental health information on Google. _American journal of preventive medicine_, 44(5), 520-525. https://www.sciencedirect.com/science/article/abs/pii/S0749379713000809

Bedre, R. (2021). "Performing and visualizing the Principal component analysis (PCA) from PCA function and scratch in Python". _Renesh Bedre Data Science Blog_. https://www.reneshbedre.com/blog/principal-component-analysis.html

Bokeh Development Team (2021). Bokeh: Python library for interactive visualization. https://bokeh.org

Chollet, F., & others. (2015). Keras. GitHub. Retrieved from https://github.com/fchollet/keras

Grinberg, M. (2018). _Flask web development: developing web applications with python_. " O&#x27;Reilly Media, Inc."

Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., … Oliphant, T. E. (2020). Array programming with NumPy. _Nature_, 585, 357–362. https://doi.org/10.1038/s41586-020-2649-2

Hunter, J. D., "Matplotlib: A 2D Graphics Environment," in _Computing in Science & Engineering_, vol. 9, no. 3, pp. 90-95, May-June 2007, doi: 10.1109/MCSE.2007.55.

The Kaiser Family Foundation State Health Facts, Poverty Rate by Race/Ethnicity. Data Source: KFF estimates based on the 2008-2019 American Community Survey (United States Census Bureau), 1-Year Estimates.https://www.kff.org/2d5cbf8/

Kluyver, T., Ragan-Kelley, B., Fernando P&#x27;erez, Granger, B., Bussonnier, M., Frederic, J., … Willing, C. (2016). Jupyter Notebooks – a publishing format for reproducible computational workflows. In F. Loizides & B. Schmidt (Eds.), _Positioning and Power in Academic Publishing: Players, Agents and Agendas_ (pp. 87–90).

McKinney, W., & others. (2010). Data structures for statistical computing in python. In _Proceedings of the 9th Python in Science Conference_ (Vol. 445, pp. 51–56).

Pedregosa, F., Varoquaux, Ga"el, Gramfort, A., Michel, V., Thirion, B., Grisel, O., … others. (2011). Scikit-learn: Machine learning in Python. _Journal of Machine Learning Research_, 12(Oct), 2825–2830.

Plotly Technologies Inc (2015). Collaborative data science. Montreal, QC: Plotly Technologies Inc. Retrieved from https://plot.ly

Stojiljković, M. “Logistic Regression in Python.” _Real Python_, Real Python, 24 Nov. 2020, realpython.com/logistic-regression-python/#logistic-regression-in-python-with-scikit-learn-example-1.

Story, R., Fernandez, F. us-states.json. folium, 2016. https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json

Substance Abuse and Mental Health Services Administration, Center for Behavioral Health Statistics and Quality. _Mental Health Client-Level Data 2018_. Rockville, MD: Substance Abuse and Mental Health Services Administration, 2020. https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/MH-CLD-2018/MH-CLD-2018-datasets/MH-CLD-2018-DS0001/MH-CLD-2018-DS0001-info/MH-CLD-2018-DS0001-info-codebook.pdf

Waskom, M., Botvinnik, O., O&#x27;Kane, D., Hobson, P., Lukauskas, S., Gemperline, D. C., … Qalieh, A. (2017). _mwaskom/seaborn: v0.8.1 (September 2017)_. Zenodo. https://doi.org/10.5281/zenodo.883859

World Population Review. (n.d.). List of STATE ABBREVIATIONS (DOWNLOAD CSV, JSON). https://worldpopulationreview.com/states/state-abbreviations.
