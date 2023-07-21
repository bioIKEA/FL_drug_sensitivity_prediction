# -*- coding: utf-8 -*-
"""CV_linearGDSC_gCSI_all_features.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S77yBqEdignu8PNBTXmHeQP3_Dd0IxcR
"""

from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data_path= '/Users/kritibbhattarai/Downloads/trisha-kritib/data/sensitivity_data/new_aug2/'

out_path = '/Users/kritibbhattarai/Downloads/trisha-kritib/code/new_pipeline/common_drug_cell_line/results_kritib/'

# C and C' 

GDSC=pd.read_csv(data_path+'GDSC_gCSI_C.csv')
gCSI=pd.read_csv(data_path+'GDSC_gCSI_C_prime.csv')

GDSC.shape, gCSI.shape

GDSC = GDSC.set_index(['cell line', 'compound' ])
gCSI = gCSI.set_index(['cell line', 'compound' ])

gdsc_x = GDSC.iloc[:, 0:-1]
gdsc_y = GDSC.iloc[:, -1]

gcsi_x = gCSI.iloc[:, 0:-1]
gcsi_y = gCSI.iloc[:, -1]

#last 21 columns are tissue types. one-hot encoding
gcsi_x.iloc[0:2, 0:-21]

gcsi_x.iloc[:, 0:-21] = StandardScaler().fit_transform(gcsi_x.iloc[:, 0:-21])
gdsc_x.iloc[:, 0:-21] = StandardScaler().fit_transform(gdsc_x.iloc[:, 0:-21])

from sklearn.model_selection import train_test_split

gcsi_X_train, gcsi_X_test, gcsi_y_train, gcsi_y_test = train_test_split(gcsi_x, gcsi_y, test_size = 0.30, random_state = 42) 
gdsc_X_train, gdsc_X_test, gdsc_y_train, gdsc_y_test = train_test_split(gdsc_x, gdsc_y,test_size = 0.30, random_state = 42)


from numpy import mean
from numpy import std
from sklearn.datasets import make_classification
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor


"""Selected Best"""

maes_sb_gdsc=[]
mses_sb_gdsc=[]
r2s_sb_gdsc=[]
kf = KFold(n_splits=10, shuffle = True, random_state= 1)


i = 1            
for train_index, test_index in kf.split(gdsc_x,gdsc_y):
    #model = MLP()

    #fit gdsc data to m1
    gdsc_x_train= gdsc_x.iloc[train_index, :]
    gdsc_x_test= gdsc_x.iloc[test_index, :]


    gdsc_Y_train = gdsc_y[train_index]
    gdsc_Y_test = gdsc_y[test_index]

    m1 = linear_model.Ridge()
    m1.fit(gdsc_x_train, gdsc_Y_train)


    #fit gcsi data to m2
    gcsi_x_train= gcsi_x.iloc[train_index, :]
    gcsi_x_test= gcsi_x.iloc[test_index, :]


    gcsi_Y_train = gcsi_y[train_index]
    gcsi_Y_test = gcsi_y[test_index]



    #need this for evaluation
    mixed_x_test = pd.concat([gdsc_x_test, gcsi_x_test], ignore_index=True)
    mixed_y_test = pd.concat([gdsc_Y_test, gcsi_Y_test], ignore_index=True)

    

    # Make predictions using the testing set
    mixed_y_pred = m1.predict(mixed_x_test)


    #test on mixed data 
    print("Results for Fold: ", i)
    print("-----------------------------------------------------------------------")
    i=i+1

    #mean squared loss
    mses_sb_gdsc.append(mean_squared_error(mixed_y_test, mixed_y_pred))
    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test, mixed_y_pred))
    
    #mean absolute error
    maes_sb_gdsc.append(mean_absolute_error(mixed_y_test, mixed_y_pred))
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test, mixed_y_pred))

    # The coefficient of determination: 1 is perfect prediction
    r2s_sb_gdsc.append(r2_score(mixed_y_test, mixed_y_pred))
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test, mixed_y_pred))

    print("-----------------------------------------------------------------------")
#0.02, 0.10, 0.18

maes_sb_gcsi=[]
mses_sb_gcsi=[]
r2s_sb_gcsi=[]
kf = KFold(n_splits=10, shuffle = True, random_state= 1)


i = 1            
for train_index, test_index in kf.split(gdsc_x,gdsc_y):
    #model = MLP()

    #fit gdsc data to m1
    gdsc_x_train= gdsc_x.iloc[train_index, :]
    gdsc_x_test= gdsc_x.iloc[test_index, :]


    gdsc_Y_train = gdsc_y[train_index]
    gdsc_Y_test = gdsc_y[test_index]



    #fit gcsi data to m2
    gcsi_x_train= gcsi_x.iloc[train_index, :]
    gcsi_x_test= gcsi_x.iloc[test_index, :]


    gcsi_Y_train = gcsi_y[train_index]
    gcsi_Y_test = gcsi_y[test_index]


    m2 = linear_model.Ridge()
    m2.fit(gcsi_x_train, gcsi_Y_train)

    #need this for evaluation
    mixed_x_test = pd.concat([gdsc_x_test, gcsi_x_test], ignore_index=True)
    mixed_y_test = pd.concat([gdsc_Y_test, gcsi_Y_test], ignore_index=True)

    

    # Make predictions using the testing set
    mixed_y_pred = m2.predict(mixed_x_test)


    #test on mixed data 
    print("Results for Fold: ", i)
    print("-----------------------------------------------------------------------")
    i=i+1

    #mean squared loss
    mses_sb_gcsi.append(mean_squared_error(mixed_y_test, mixed_y_pred))
    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test, mixed_y_pred))
    
    #mean absolute error
    maes_sb_gcsi.append(mean_absolute_error(mixed_y_test, mixed_y_pred))
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test, mixed_y_pred))

    # The coefficient of determination: 1 is perfect prediction
    r2s_sb_gcsi.append(r2_score(mixed_y_test, mixed_y_pred))
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test, mixed_y_pred))

    print("-----------------------------------------------------------------------")


with open("results/selected_best.txt", "a") as output:
    output.write("gdsc_gcsi_selected_best_mae="+str(maes_sb_gdsc)+"\n")
    output.write("gdsc_gcsi_selected_best_mse="+str(mses_sb_gdsc)+"\n")
    output.write("gdsc_gcsi_selected_best_r2="+str(r2s_sb_gdsc)+"\n")
