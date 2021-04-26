import pandas as pd

df = pd.read_csv("https://csprojectdatavisualization.s3.us-east-2.amazonaws.com/MHCLD_PUF_2018.csv")

average_age = df["age"].mean()
print(average_age)


import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier