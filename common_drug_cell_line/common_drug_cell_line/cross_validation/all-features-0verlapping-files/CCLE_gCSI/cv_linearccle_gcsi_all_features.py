# -*- coding: utf-8 -*-
"""CV_linearCCLE_gCSI_all_features.ipynb

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

CCLE=pd.read_csv(data_path+'CCLE_gCSI_C.csv')
gCSI=pd.read_csv(data_path+'CCLE_gCSI_C_prime.csv')

CCLE.shape, gCSI.shape

CCLE = CCLE.set_index(['cell line', 'compound' ])
gCSI = gCSI.set_index(['cell line', 'compound' ])

ccle_x = CCLE.iloc[:, 0:-1]
ccle_y = CCLE.iloc[:, -1]

gcsi_x = gCSI.iloc[:, 0:-1]
gcsi_y = gCSI.iloc[:, -1]

#last 21 columns are tissue types. one-hot encoding
gcsi_x.iloc[0:2, 0:-21]

gcsi_x.iloc[:, 0:-21] = StandardScaler().fit_transform(gcsi_x.iloc[:, 0:-21])
ccle_x.iloc[:, 0:-21] = StandardScaler().fit_transform(ccle_x.iloc[:, 0:-21])

from sklearn.model_selection import train_test_split

gcsi_X_train, gcsi_X_test, gcsi_y_train, gcsi_y_test = train_test_split(gcsi_x, gcsi_y, test_size = 0.30, random_state = 42) 
ccle_X_train, ccle_X_test, ccle_y_train, ccle_y_test = train_test_split(ccle_x, ccle_y,test_size = 0.30, random_state = 42)

"""Our method cv"""

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


maes_our=[]
mses_our=[]
r2s_our=[]
kf = KFold(n_splits=10, shuffle = True, random_state= 1)


i = 1            
for train_index, test_index in kf.split(ccle_x,ccle_y):
    #model = MLP()

    #fit ccle data to m1
    ccle_x_train= ccle_x.iloc[train_index, :]
    ccle_x_test= ccle_x.iloc[test_index, :]


    ccle_Y_train = ccle_y[train_index]
    ccle_Y_test = ccle_y[test_index]

    m1 = linear_model.Ridge()
    m1.fit(ccle_x_train, ccle_Y_train)

    # Make predictions using the testing set
    ccle_y_pred = m1.predict(ccle_x_test)

    #fit gcsi data to m2
    gcsi_x_train= gcsi_x.iloc[train_index, :]
    gcsi_x_test= gcsi_x.iloc[test_index, :]


    gcsi_Y_train = gcsi_y[train_index]
    gcsi_Y_test = gcsi_y[test_index]

    m2=  linear_model.Ridge()
    m2.fit(gcsi_x_train, gcsi_Y_train)

    # Make predictions using the testing set
    gcsi_y_pred = m2.predict(gcsi_x_test)


    #need this for evaluation
    mixed_x_test = pd.concat([ccle_x_test, gcsi_x_test], ignore_index=True)
    mixed_y_test = pd.concat([ccle_Y_test, gcsi_Y_test], ignore_index=True)

    #predictions on training sets. m1 to predict CCLE and m2 to predict gCSI
    ccle_y_train_pred = m1.predict(ccle_x_train)
    gcsi_y_train_pred = m2.predict(gcsi_x_train)

    m4 = linear_model.LinearRegression()
    #for m4, gcsi is the x and ccle is the y, reverse for m3
    m4.fit(gcsi_y_train_pred.reshape(-1, 1), ccle_y_train_pred.reshape(-1,1))

    # Make predictions using the testing set
    ccle_y_pred_m4 = m4.predict(gcsi_y_pred.reshape(-1,1))

    #avg ccle values predicted by m4 + gcsi input y values  to m4 
    gcsi = (ccle_y_pred_m4 + gcsi_y_pred.reshape(-1,1))/2


    m3 =linear_model.LinearRegression()
    #for m3, gcsi is the y and ccle is the x, reverse for m4
    m3.fit(ccle_y_train_pred.reshape(-1, 1), gcsi_y_train_pred.reshape(-1,1))

    # Make predictions using the testing set
    gcsi_y_pred_m3 = m3.predict(ccle_y_pred.reshape(-1,1))

    ccle = (gcsi_y_pred_m3 + ccle_y_pred.reshape(-1,1))/2


    #use squeeze to make it one dimensional
    ccle = pd.Series(ccle.squeeze())
    gcsi =pd.Series(gcsi.squeeze())

    #concat for comparing with mixed_y_test
    concated = pd.concat([ccle, gcsi], ignore_index=True)

    #test on mixed data 
    print("Results for Fold: ", i)
    print("-----------------------------------------------------------------------")
    i=i+1

    #mean squared loss
    mses_our.append(mean_squared_error(mixed_y_test, concated))
    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test, concated))
    
    #mean absolute error
    maes_our.append(mean_absolute_error(mixed_y_test, concated))
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test, concated))

    # The coefficient of determination: 1 is perfect prediction
    r2s_our.append(r2_score(mixed_y_test, concated))
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test, concated))

    print("-----------------------------------------------------------------------")

"""Our method NN"""

'''from sklearn.neural_network import MLPRegressor
maes_our_nn=[]
mses_our_nn=[]
r2s_our_nn=[]
kf = KFold(n_splits=10, shuffle = True, random_state= 1)


i = 1            
for train_index, test_index in kf.split(ccle_x,ccle_y):
    #model = MLP()

    #fit ccle data to m1
    ccle_x_train= ccle_x.iloc[train_index, :]
    ccle_x_test= ccle_x.iloc[test_index, :]

    ccle_Y_train = ccle_y[train_index]
    ccle_Y_test = ccle_y[test_index]

    m1 = linear_model.Ridge()
    m1.fit(ccle_x_train, ccle_Y_train)

    # Make predictions using the testing set
    ccle_y_pred = m1.predict(ccle_x_test)

    #fit gcsi data to m2
    gcsi_x_train= gcsi_x.iloc[train_index, :]
    gcsi_x_test= gcsi_x.iloc[test_index, :]

    gcsi_Y_train = gcsi_y[train_index]
    gcsi_Y_test = gcsi_y[test_index]

    m2=  linear_model.Ridge()
    m2.fit(gcsi_x_train, gcsi_Y_train)

    # Make predictions using the testing set
    gcsi_y_pred = m2.predict(gcsi_x_test)


    #need this for evaluation
    mixed_x_test = pd.concat([ccle_x_test, gcsi_x_test], ignore_index=True)
    mixed_y_test = pd.concat([ccle_Y_test, gcsi_Y_test], ignore_index=True)

    #predictions on training sets. m1 to predict CCLE and m2 to predict gCSI
    ccle_y_train_pred = m1.predict(ccle_x_train)
    gcsi_y_train_pred = m2.predict(gcsi_x_train)


    m4 = MLPRegressor(random_state=1, max_iter=200)
    #for m4, gcsi is the x and ccle is the y, reverse for m3
    m4.fit(gcsi_y_train_pred.reshape(-1, 1), ccle_y_train_pred)

    # Make predictions using the testing set
    ccle_y_pred_m4 = m4.predict(gcsi_y_pred.reshape(-1,1))

    #avg ccle values predicted by m4 + gcsi input y values  to m4 
    gcsi = (ccle_y_pred_m4 + gcsi_y_pred)/2

    #print(ccle_y_train_pred.reshape(-1, 1))
    #print(ccle_y_train_pred)

    m3 =MLPRegressor(random_state=1, max_iter=200)
    #for m3, gcsi is the y and ccle is the x, reverse for m4
    m3.fit(ccle_y_train_pred.reshape(-1, 1), gcsi_y_train_pred)

    # Make predictions using the testing set
    gcsi_y_pred_m3 = m3.predict(ccle_y_pred.reshape(-1,1))

    ccle = (gcsi_y_pred_m3 + ccle_y_pred)/2

    #print(ccle)
    #use squeeze to make it one dimensional
    ccle = pd.Series(ccle.squeeze())
    gcsi =pd.Series(gcsi.squeeze())

    #concat for comparing with mixed_y_test
    concated = pd.concat([ccle, gcsi], ignore_index=True)

    #test on mixed data 
    print("Results for Fold: ", i)
    print("-----------------------------------------------------------------------")
    i=i+1

    #mean squared loss
    mses_our_nn.append(mean_squared_error(mixed_y_test, concated))
    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test, concated))
    
    #mean absolute error
    maes_our_nn.append(mean_absolute_error(mixed_y_test, concated))
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test, concated))

    # The coefficient of determination: 1 is perfect prediction
    r2s_our_nn.append(r2_score(mixed_y_test, concated))
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test, concated))

    print("-----------------------------------------------------------------------")'''

"""Combined dataset CV"""

maes_cd=[]
mses_cd=[]
r2s_cd=[]
kf = KFold(n_splits=10, shuffle = True, random_state= 1)


i = 1            
for train_index, test_index in kf.split(ccle_x,ccle_y):
    #model = MLP()

    #fit ccle data to m1
    ccle_x_train= ccle_x.iloc[train_index, :]
    ccle_x_test= ccle_x.iloc[test_index, :]


    ccle_Y_train = ccle_y[train_index]
    ccle_Y_test = ccle_y[test_index]




    #fit gcsi data to m2
    gcsi_x_train= gcsi_x.iloc[train_index, :]
    gcsi_x_test= gcsi_x.iloc[test_index, :]


    gcsi_Y_train = gcsi_y[train_index]
    gcsi_Y_test = gcsi_y[test_index]



    m5=  linear_model.Ridge()

    #need this for evaluation
    mixed_x_test = pd.concat([ccle_x_test, gcsi_x_test], ignore_index=True)
    mixed_y_test = pd.concat([ccle_Y_test, gcsi_Y_test], ignore_index=True)

    mixed_x_train = pd.concat([ccle_x_train, gcsi_x_train], ignore_index=True)
    mixed_y_train = pd.concat([ccle_Y_train, gcsi_Y_train], ignore_index=True)

    m5.fit(mixed_x_train, mixed_y_train)

    #make predictions on the combined test data

    mixed_y_pred_m5 = m5.predict(mixed_x_test)

    #test on mixed data 
    print("Results for Fold: ", i)
    print("-----------------------------------------------------------------------")
    i=i+1

    #mean squared loss
    mses_cd.append(mean_squared_error(mixed_y_test,  mixed_y_pred_m5))
    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test, mixed_y_pred_m5))
    
    #mean absolute error
    maes_cd.append(mean_absolute_error(mixed_y_test,  mixed_y_pred_m5))
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test,  mixed_y_pred_m5))

    # The coefficient of determination: 1 is perfect prediction
    r2s_cd.append(r2_score(mixed_y_test, mixed_y_pred_m5))
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test,  mixed_y_pred_m5))

    print("-----------------------------------------------------------------------")

"""Selected Best"""

maes_sb_ccle=[]
mses_sb_ccle=[]
r2s_sb_ccle=[]
kf = KFold(n_splits=10, shuffle = True, random_state= 1)


i = 1            
for train_index, test_index in kf.split(ccle_x,ccle_y):
    #model = MLP()

    #fit ccle data to m1
    ccle_x_train= ccle_x.iloc[train_index, :]
    ccle_x_test= ccle_x.iloc[test_index, :]


    ccle_Y_train = ccle_y[train_index]
    ccle_Y_test = ccle_y[test_index]

    m1 = linear_model.Ridge()
    m1.fit(ccle_x_train, ccle_Y_train)


    #fit gcsi data to m2
    gcsi_x_train= gcsi_x.iloc[train_index, :]
    gcsi_x_test= gcsi_x.iloc[test_index, :]


    gcsi_Y_train = gcsi_y[train_index]
    gcsi_Y_test = gcsi_y[test_index]



    #need this for evaluation
    mixed_x_test = pd.concat([ccle_x_test, gcsi_x_test], ignore_index=True)
    mixed_y_test = pd.concat([ccle_Y_test, gcsi_Y_test], ignore_index=True)

    

    # Make predictions using the testing set
    mixed_y_pred = m1.predict(mixed_x_test)


    #test on mixed data 
    print("Results for Fold: ", i)
    print("-----------------------------------------------------------------------")
    i=i+1

    #mean squared loss
    mses_sb_ccle.append(mean_squared_error(mixed_y_test, mixed_y_pred))
    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test, mixed_y_pred))
    
    #mean absolute error
    maes_sb_ccle.append(mean_absolute_error(mixed_y_test, mixed_y_pred))
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test, mixed_y_pred))

    # The coefficient of determination: 1 is perfect prediction
    r2s_sb_ccle.append(r2_score(mixed_y_test, mixed_y_pred))
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test, mixed_y_pred))

    print("-----------------------------------------------------------------------")
#0.02, 0.10, 0.18

maes_sb_gcsi=[]
mses_sb_gcsi=[]
r2s_sb_gcsi=[]
kf = KFold(n_splits=10, shuffle = True, random_state= 1)


i = 1            
for train_index, test_index in kf.split(ccle_x,ccle_y):
    #model = MLP()

    #fit ccle data to m1
    ccle_x_train= ccle_x.iloc[train_index, :]
    ccle_x_test= ccle_x.iloc[test_index, :]


    ccle_Y_train = ccle_y[train_index]
    ccle_Y_test = ccle_y[test_index]



    #fit gcsi data to m2
    gcsi_x_train= gcsi_x.iloc[train_index, :]
    gcsi_x_test= gcsi_x.iloc[test_index, :]


    gcsi_Y_train = gcsi_y[train_index]
    gcsi_Y_test = gcsi_y[test_index]


    m2 = linear_model.Ridge()
    m2.fit(gcsi_x_train, gcsi_Y_train)

    #need this for evaluation
    mixed_x_test = pd.concat([ccle_x_test, gcsi_x_test], ignore_index=True)
    mixed_y_test = pd.concat([ccle_Y_test, gcsi_Y_test], ignore_index=True)

    

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

"""Weighted average"""

maes_wa=[]
mses_wa=[]
r2s_wa=[]
kf = KFold(n_splits=10, shuffle = True, random_state= 1)


i = 1            
for train_index, test_index in kf.split(ccle_x,ccle_y):
    #model = MLP()

    #fit ccle data to m1
    ccle_x_train= ccle_x.iloc[train_index, :]
    ccle_x_test= ccle_x.iloc[test_index, :]


    ccle_Y_train = ccle_y[train_index]
    ccle_Y_test = ccle_y[test_index]

    m1 = linear_model.Ridge()
    m1.fit(ccle_x_train, ccle_Y_train)

    # Make predictions using the testing set
    ccle_y_pred = m1.predict(ccle_x_test)

    #fit gcsi data to m2
    gcsi_x_train= gcsi_x.iloc[train_index, :]
    gcsi_x_test= gcsi_x.iloc[test_index, :]


    gcsi_Y_train = gcsi_y[train_index]
    gcsi_Y_test = gcsi_y[test_index]

    m2=  linear_model.Ridge()
    m2.fit(gcsi_x_train, gcsi_Y_train)

    # Make predictions using the testing set
    gcsi_y_pred = m2.predict(gcsi_x_test)


    #need this for evaluation
    mixed_x_test = pd.concat([ccle_x_test, gcsi_x_test], ignore_index=True)
    mixed_y_test = pd.concat([ccle_Y_test, gcsi_Y_test], ignore_index=True)

    avg_y_pred = (ccle_y_pred + gcsi_y_pred)/2
    avg_y_pred = pd.Series(avg_y_pred)
    #stack the avg_y_pred twice for CCLE and gCSI. first half of mixed_y_test comes from CCLE and the second half comes from gCSI
    avg_y_pred_stacked = pd.concat([avg_y_pred, avg_y_pred], ignore_index=True)

    #test on mixed data 
    print("Results for Fold: ", i)
    print("-----------------------------------------------------------------------")
    i=i+1

    #mean squared loss
    mses_wa.append(mean_squared_error(mixed_y_test, avg_y_pred_stacked))
    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test, avg_y_pred_stacked))
    
    #mean absolute error
    maes_wa.append(mean_absolute_error(mixed_y_test, avg_y_pred_stacked))
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test, avg_y_pred_stacked))

    # The coefficient of determination: 1 is perfect prediction
    r2s_wa.append(r2_score(mixed_y_test, avg_y_pred_stacked))
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test, avg_y_pred_stacked))

    print("-----------------------------------------------------------------------")

"""Model Averaging"""

maes_ma=[]
mses_ma=[]
r2s_ma=[]
kf = KFold(n_splits=10, shuffle = True, random_state= 1)


i = 1            
for train_index, test_index in kf.split(ccle_x,ccle_y):
    #model = MLP()

    #fit ccle data to m1
    ccle_x_train= ccle_x.iloc[train_index, :]
    ccle_x_test= ccle_x.iloc[test_index, :]


    ccle_Y_train = ccle_y[train_index]
    ccle_Y_test = ccle_y[test_index]

    m1 = linear_model.Ridge()
    m1.fit(ccle_x_train, ccle_Y_train)

    # Make predictions using the testing set
    #ccle_y_pred = m1.predict(ccle_x_test)

    #fit gcsi data to m2
    gcsi_x_train= gcsi_x.iloc[train_index, :]
    gcsi_x_test= gcsi_x.iloc[test_index, :]


    gcsi_Y_train = gcsi_y[train_index]
    gcsi_Y_test = gcsi_y[test_index]

    m2=  linear_model.Ridge()
    m2.fit(gcsi_x_train, gcsi_Y_train)

    # Make predictions using the testing set
    #gcsi_y_pred = m2.predict(gcsi_x_test)


    #need this for evaluation
    mixed_x_test = pd.concat([ccle_x_test, gcsi_x_test], ignore_index=True)
    mixed_y_test = pd.concat([ccle_Y_test, gcsi_Y_test], ignore_index=True)

    m_coef = (m1.coef_ + m2.coef_)/2

    m_intercept = (m1.intercept_ + m2.intercept_)/2
    #print(m_coef, m1.coef_, m2.coef_)

    mixed_y_test_pred=[]
    for i in range(len(mixed_x_test)):
      mixed_y_test_pred.append((mixed_x_test.iloc[i, :] @ m_coef) + m_intercept)

    #test on mixed data 
    print("Results for Fold: ", i)
    print("-----------------------------------------------------------------------")
    i=i+1

    #mean squared loss
    mses_ma.append(mean_squared_error(mixed_y_test, mixed_y_test_pred))
    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test, mixed_y_test_pred))
    
    #mean absolute error
    maes_ma.append(mean_absolute_error(mixed_y_test, mixed_y_test_pred))
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test, mixed_y_test_pred))

    # The coefficient of determination: 1 is perfect prediction
    r2s_ma.append(r2_score(mixed_y_test, mixed_y_test_pred))
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test, mixed_y_test_pred))

    print("-----------------------------------------------------------------------")

"""Plots"""

plt.boxplot([maes_our, maes_cd, maes_sb_ccle, maes_wa, maes_ma])
plt.title("Mean Absolute Error")
plt.xticks([1, 2, 3, 4, 5], ['Our method', 'Combining datasets', 'Selecting best', 'Result averaging', 'Model averaging'])
plt.xticks(rotation = 90)
plt.savefig(out_path+'mean_absolute_error_boxplots_cv_all_features_gCSI_gCSI.png', dpi=300, bbox_inches= 'tight')
plt.show()

plt.boxplot([mses_our, mses_cd, mses_sb_ccle,  mses_wa, mses_ma])
plt.title("Mean Squared Error")
plt.xticks([1, 2, 3, 4, 5], ['Our method', 'Combining datasets', 'Selecting best', 'Result averaging', 'Model averaging'])
plt.xticks(rotation = 90)
plt.savefig(out_path+'mean_squared_error_boxplots_cv_all_features_gCSI_gCSI.png', dpi=300, bbox_inches= 'tight')
plt.show()

plt.boxplot([r2s_our, r2s_cd,  r2s_sb_ccle, r2s_wa, r2s_ma])
plt.title("Coefficient of determination")
plt.xticks([1, 2, 3, 4, 5], ['Our method', 'Combining datasets', 'Selecting best', 'Result averaging', 'Model averaging'])
plt.xticks(rotation = 90)
plt.savefig(out_path+'r2_boxplots_cv_all_features_gCSI_gCSI.png', dpi=300, bbox_inches= 'tight')
plt.show()

"""For SB, gcsi better than gcsi
For SB, gcsi better than ccle
"""
