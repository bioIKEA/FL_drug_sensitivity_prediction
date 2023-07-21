# -*- coding: utf-8 -*-
"""Ablation_linearGDSC_gCSI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/190uVUKf_APm6YxsxmK1BceVuKzTj0MhJ
"""

from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np


data_path= '/Users/kritibbhattarai/Downloads/trisha-kritib/data/sensitivity_data/new_aug2/'

GDSC=pd.read_csv(data_path+'GDSC_paired_common_with_gcsi.csv', index_col=0)
gCSI=pd.read_csv(data_path+'gCSI_paired_common_with_gdsc.csv', index_col=0)

GDSC_x = GDSC.iloc[:, 0:-1]
GDSC_y = GDSC.iloc[:, -1]

GDSC_x.head()

gCSI = gCSI.reset_index()
gCSI = gCSI.drop(columns='index')

gCSI_x = gCSI.iloc[:, 0:-1]
gCSI_y = gCSI.iloc[:, -1]

gCSI_x.head()

gCSI_x.iloc[0:2, 0:-20]

GDSC_x = GDSC_x.iloc[:, 0:-21]
gCSI_x = gCSI_x.iloc[:, 0:-21]

gCSI_x.iloc[:, :] = StandardScaler().fit_transform(gCSI_x.iloc[:, :])
GDSC_x.iloc[:, :] = StandardScaler().fit_transform(GDSC_x.iloc[:, :])

from sklearn.model_selection import train_test_split

gCSI_X_train, gCSI_X_test, gCSI_y_train, gCSI_y_test = train_test_split(gCSI_x, gCSI_y, test_size = 0.30, random_state = 42) 
GDSC_X_train, GDSC_X_test, GDSC_y_train, GDSC_y_test = train_test_split(GDSC_x, GDSC_y,test_size = 0.30, random_state = 42)

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor

from sklearn.model_selection import KFold


maes_our=[]
mses_our=[]
r2s_our=[]
kf = KFold(n_splits=10, shuffle = True, random_state= 1)


i=1
for train_index, test_index in kf.split(GDSC_x,GDSC_y):

    # Create linear regression object
    # change to RandomForestRegressor() while needed 
    m1 = linear_model.Ridge()# RandomForestRegressor(max_depth = 4)#linear_model.Ridge()
    m2=  linear_model.Ridge() #RandomForestRegressor(max_depth = 4)#linear_model.Ridge()

    GDSC_X_train=GDSC_x.iloc[train_index,:]
    GDSC_X_test=GDSC_x.iloc[test_index,:]


    GDSC_y_train=GDSC_y[train_index]
    GDSC_y_test=GDSC_y[test_index]


    gCSI_X_train=gCSI_x.iloc[train_index,:]
    gCSI_X_test=gCSI_x.iloc[test_index,:]


    gCSI_y_train=gCSI_y[train_index]
    gCSI_y_test=gCSI_y[test_index]

    # in-study results: GDSC
    m1.fit(GDSC_X_train, GDSC_y_train)

    # Make predictions using the testing set
    GDSC_y_pred = m1.predict(GDSC_X_test)


    # The mean squared error
    print("Mean squared error: %.2f" % mean_squared_error(GDSC_y_test, GDSC_y_pred))

    #mean absolute error
    print("Mean absolute error: %.2f" % mean_absolute_error(GDSC_y_test, GDSC_y_pred))

    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(GDSC_y_test, GDSC_y_pred))

    #mixed study results trained on GDSC (70%)

    mixed_x_test = pd.concat([GDSC_X_test, gCSI_X_test], ignore_index=True)
    mixed_y_test = pd.concat([GDSC_y_test, gCSI_y_test], ignore_index=True)

    mixed_y_pred_m1 = m1.predict(mixed_x_test)

    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test, mixed_y_pred_m1))

    #mean absolute error
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test, mixed_y_pred_m1))

    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test, mixed_y_pred_m1))

    #trained on gCSI 70% data , tested on 30% gCSI

    m2.fit(gCSI_X_train, gCSI_y_train)

    # Make predictions using the testing set
    gCSI_y_pred = m2.predict(gCSI_X_test)

    # The coefficients
    #print("Coefficients: \n", regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f" % mean_squared_error(gCSI_y_test, gCSI_y_pred))

    #mean absolute error
    print("Mean absolute error: %.2f" % mean_absolute_error(gCSI_y_test, gCSI_y_pred))

    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(gCSI_y_test, gCSI_y_pred))

    #mixed study results trained on gCSI (70%)

    mixed_y_pred_m2 = m2.predict(mixed_x_test)

    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test, mixed_y_pred_m2))

    #mean absolute error
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test, mixed_y_pred_m2))

    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test, mixed_y_pred_m2))

    #mixed model m5
    #train on mixed dataset and test on mixed dataset

    m5=  linear_model.Ridge()

    mixed_x_train = pd.concat([GDSC_X_train, gCSI_X_train], ignore_index=True)
    mixed_y_train = pd.concat([GDSC_y_train, gCSI_y_train], ignore_index=True)

    m5.fit(mixed_x_train, mixed_y_train)

    #make predictions on the combined test data

    mixed_y_pred_m5 = m5.predict(mixed_x_test)   

    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test, mixed_y_pred_m5))

    #mean absolute error
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test, mixed_y_pred_m5))

    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test, mixed_y_pred_m5))

    GDSC_y_train_pred = m1.predict(GDSC_X_train)
    gCSI_y_train_pred = m2.predict(gCSI_X_train)

    """best that can be done on training sets"""

    print("Mean squared error: %.2f" % mean_squared_error(gCSI_y_train, gCSI_y_train_pred))

    #mean absolute error
    print("Mean absolute error: %.2f" % mean_absolute_error(gCSI_y_train, gCSI_y_train_pred))

    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(gCSI_y_train, gCSI_y_train_pred))

    print("Mean squared error: %.2f" % mean_squared_error(GDSC_y_train, GDSC_y_train_pred))

    #mean absolute error
    print("Mean absolute error: %.2f" % mean_absolute_error(GDSC_y_train, GDSC_y_train_pred))

    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(GDSC_y_train, GDSC_y_train_pred))

    """WA method"""

    avg_y_pred = (GDSC_y_pred + gCSI_y_pred)/2

    avg_y_pred = pd.Series(avg_y_pred)

    avg_y_pred_stacked = pd.concat([avg_y_pred, avg_y_pred], ignore_index=True)

    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test, avg_y_pred_stacked))

    #mean absolute error
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test, avg_y_pred_stacked))

    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test, avg_y_pred_stacked))

    """do a linear regression on the training scores"""

    m4 = linear_model.LinearRegression()

    m4.fit(gCSI_y_train_pred.reshape(-1, 1), GDSC_y_train_pred.reshape(-1,1))

    # Make predictions using the testing set
    GDSC_y_pred_m4 = m4.predict(gCSI_y_pred.reshape(-1,1))

    #avg GDSC values predicted by m4 + gCSI input y values  to m4 
    gCSI = (GDSC_y_pred_m4 + gCSI_y_pred.reshape(-1,1))/2

    #print(gCSI)
    print("Mean squared error: %.2f" % mean_squared_error(gCSI_y_test, gCSI))

    #mean absolute error
    print("Mean absolute error: %.2f" % mean_absolute_error(gCSI_y_test, gCSI))

    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(gCSI_y_test, gCSI))

    m3 =linear_model.LinearRegression()

    m3.fit(GDSC_y_train_pred.reshape(-1, 1), gCSI_y_train_pred.reshape(-1,1))

    # Make predictions using the testing set
    gCSI_y_pred_m3 = m3.predict(GDSC_y_pred.reshape(-1,1))

    GDSC = (gCSI_y_pred_m3 + GDSC_y_pred.reshape(-1,1))/2
    print("Mean squared error: %.2f" % mean_squared_error(GDSC_y_test, GDSC))

    #mean absolute error
    print("Mean absolute error: %.2f" % mean_absolute_error(GDSC_y_test, GDSC))

    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(GDSC_y_test, GDSC))

    GDSC = pd.Series(GDSC.squeeze())
    gCSI =pd.Series(gCSI.squeeze())

    #proposed model's results are stored in concated
    concated = pd.concat([GDSC, gCSI], ignore_index=True)

    #test on mixed data 

    mses_our.append(mean_squared_error(mixed_y_test, concated))
    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test, concated))
    
    #mean absolute error
    maes_our.append(mean_absolute_error(mixed_y_test, concated))
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test, concated))

    # The coefficient of determination: 1 is perfect prediction
    r2s_our.append(r2_score(mixed_y_test, concated))
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test, concated))

    print("-----------------------------------------------------------------------")



with open("results/gdsc_gcsi_ridge.txt", "a") as output:
    output.write("gdsc_gcsi_our_method_mae_ridge="+str(maes_our)+"\n")
    output.write("gdsc_gcsi_our_method_mse_ridge="+str(mses_our)+"\n")
    output.write("gdsc_gcsi_our_method_r2_ridge="+str(r2s_our)+"\n")
