# -*- coding: utf-8 -*-
"""CV_linearCCLE_GDSC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17G5ZhI6J2GmB1HF94VyTaU7T4hU3l_aR
"""

from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import jaccard_score
import random

data_path= '/Users/kritibbhattarai/Downloads/trisha-kritib/data/expression_data/'



CCLE = pd.read_csv(data_path+'CCLE_exp_L1000.csv', index_col=0)
gCSI = pd.read_csv(data_path+'gCSI_exp_L1000.csv', index_col = 0)
# print(CCLE.head())

CCLE_cols=CCLE.columns.values
gCSI_cols=gCSI.columns.values
print(len(CCLE_cols), len(gCSI_cols))

#padding gcsi list 
n = ["hi" for i in range(422)] 
# print(n)
gCSI_cols_1=np.append(gCSI_cols,n)
jc_ind=jaccard_score(list(CCLE_cols), list(gCSI_cols_1),average='macro')
print(jc_ind)
