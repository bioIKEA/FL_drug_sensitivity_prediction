# -*- coding: utf-8 -*-
"""NN_CCLE_GDSC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1I6PSCKSZnziqO98fHjyI5TlkSMDz-UwJ
"""

from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

from multiprocessing import reduction
import warnings
from collections import OrderedDict
from torch import Tensor
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision.datasets import CIFAR10
from torchvision.transforms import Compose, Normalize, ToTensor
from tqdm import tqdm
from sklearn.metrics import r2_score
import pandas as pd
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset
from numpy import vstack
from sklearn.preprocessing import StandardScaler

from google.colab import drive
drive.mount('/content/drive', force_remount=True)

data_path= '/content/drive/My Drive/INTERN_2022/DRUG/data/sensitivity_data/new_aug2/'

CCLE=pd.read_csv(data_path+'CCLE_paired_common.csv', index_col=0)
GDSC=pd.read_csv(data_path+'GDSC_paired_common.csv', index_col=0)

ccle_x = CCLE.iloc[:, 0:-1]
ccle_y = CCLE.iloc[:, -1]

GDSC = GDSC.reset_index()
GDSC = GDSC.drop(columns='index')

gdsc_x = GDSC.iloc[:, 0:-1]
gdsc_y = GDSC.iloc[:, -1]

gdsc_x.iloc[0:2, 0:-21]

gdsc_x.iloc[:, 0:-21] = StandardScaler().fit_transform(gdsc_x.iloc[:, 0:-21])
ccle_x.iloc[:, 0:-21] = StandardScaler().fit_transform(ccle_x.iloc[:, 0:-21])

from sklearn.model_selection import train_test_split

gdsc_X_train, gdsc_X_test, gdsc_y_train, gdsc_y_test = train_test_split(gdsc_x, gdsc_y, test_size = 0.30, random_state = 42) 
ccle_X_train, ccle_X_test, ccle_y_train, ccle_y_test = train_test_split(ccle_x, ccle_y,test_size = 0.30, random_state = 42)

gdsc_train = pd.concat([gdsc_X_train, gdsc_y_train], axis = 1)

gdsc_test = pd.concat([gdsc_X_test, gdsc_y_test], axis = 1)

ccle_test = pd.concat([ccle_X_test, ccle_y_test], axis = 1)

ccle_train = pd.concat([ccle_X_train, ccle_y_train], axis = 1)

len(ccle_test.columns)

"""custom dataset for dataloader"""

seed = 0
torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

class CCLE_Dataset(Dataset):
    # load the dataset
    def __init__(self, path, train_val_test = 1):
        # load the csv file as a dataframe
        df = path#read_csv(path, header=None)
        # store the inputs and outputs
        self.X = df.values[:, 0:len(df.columns)-1]
        self.y = df.values[:, len(df.columns)-1]
        # ensure input data is floats
        self.X = self.X.astype('float32')
        self.X = StandardScaler().fit_transform(self.X)
        # label encode target and ensure the values are floats
        self.y = self.y.astype('float32')
        self.y = self.y.reshape((len(self.y), 1))
        x_train, x_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=42)
        #x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.5, train_size=0.5, random_state=0, stratify = y_test)

        self.train_val_test = train_val_test
        # two modes - train and test
        if( train_val_test ==1):
            self.x_data, self.y_data = x_train, y_train
        else:
            self.x_data, self.y_data = x_test, y_test

    # number of rows in the dataset
    def __len__(self):
        return len(self.x_data)

    # get a row at an index
    def __getitem__(self, idx):
        #print(self.x_data[idx].shape, self.y_data[idx].shape)
        return [self.x_data[idx], self.y_data[idx]]

class mixed_Dataset_for_test(Dataset):
    # load the dataset
    def __init__(self, path):
        # load the csv file as a dataframe
        df = path#read_csv(path, header=None)
        # store the inputs and outputs
        self.X = df.values[:, 0:len(df.columns)-1]
        self.y = df.values[:, len(df.columns)-1]
        # ensure input data is floats
        self.X = self.X.astype('float32')
        self.X = StandardScaler().fit_transform(self.X)
        # label encode target and ensure the values are floats
        self.y = self.y.astype('float32')
        self.y = self.y.reshape((len(self.y), 1))

    # number of rows in the dataset
    def __len__(self):
        return len(self.X)

    # get a row at an index
    def __getitem__(self, idx):
        #print(self.x_data[idx].shape, self.y_data[idx].shape)
        return [self.X[idx], self.y[idx]]

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor

# Create linear regression object
# change to RandomForestRegressor() while needed 
#m1 = RandomForestRegressor(max_depth=4)#linear_model.Ridge()
#m2=  RandomForestRegressor(max_depth=4)#linear_model.Ridge()

class Net(nn.Module):
    """Model (simple CNN adapted from 'PyTorch: A 60 Minute Blitz')"""

    def __init__(self) -> None:
        super(Net, self).__init__()
        #self.lin = nn.Linear(620,1)
        self.layers = nn.Sequential(
        nn.Linear(len(CCLE.columns)-1, 64),
        nn.ReLU(),
        nn.Linear(64, 32),
        nn.ReLU(),
        nn.Linear(32, 1)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.layers(x)
        return x

def train(net, trainloader, epochs):
    """Train the model on the training set."""
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    # enumerate epochs
    for epoch in range(epochs):
        # enumerate mini batches
        for i, (inputs, targets) in enumerate(trainloader):
            # clear the gradients
            optimizer.zero_grad()
            # compute the model output
            yhat = net(inputs)
            # calculate loss
            loss = criterion(yhat, targets)
            # credit assignment
            loss.backward()
            # update model weights
            optimizer.step()

def test(net, testloader):
    """Validate the model on the test set."""
    net.eval()
    criterion = torch.nn.MSELoss()
    correct, total, loss = 0, 0, 0.0
    predictions, actuals = list(), list()
    for i, (inputs, targets) in enumerate(testloader):
        # evaluate the model on the test set
        yhat = net(inputs)
        # retrieve numpy array

        #yhat = yhat.detach().numpy()
        #actual = targets.numpy()
        actual = targets.reshape((len(targets), 1))

        loss += criterion(yhat,actual).item()

        #print(yhat)
        predictions.append(yhat.detach().numpy())
        actuals.append(actual.detach().numpy())
    
    #print(type(predictions))
    predictions, actuals= vstack(predictions), vstack(actuals)

    
    print("Mean squared error: %.2f" % mean_squared_error(actuals,predictions))

    #mean absolute error
    print("Mean absolute error: %.2f" % mean_absolute_error(actuals, predictions))

    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(actuals, predictions))

    return mean_squared_error(actuals,predictions), mean_absolute_error(actuals, predictions), r2_score(actuals, predictions)

warnings.filterwarnings("ignore", category=UserWarning)
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def load_data(path):
    # load the dataset
    train = CCLE_Dataset(path,train_val_test=1)
    test =CCLE_Dataset(path,train_val_test=3)
    batch_size =16

    # prepare data loaders
    train_dl = DataLoader(train, batch_size=batch_size, shuffle=True)
    test_dl = DataLoader(test, batch_size=batch_size, shuffle=False)
    return train_dl, test_dl

m1 = Net().to(DEVICE)
m2= Net().to(DEVICE)

ccle_trainloader, ccle_testloader = load_data(CCLE)
gdsc_trainloader, gdsc_testloader = load_data(GDSC)

# make a class prediction for one row of data
def predict(net, testloader):
    net.eval()
    criterion = torch.nn.MSELoss()
    correct, total, loss = 0, 0, 0.0
    predictions, actuals = list(), list()
    for i, (inputs, targets) in enumerate(testloader):
        # evaluate the model on the test set
        yhat = net(inputs)
        # retrieve numpy array

        #yhat = yhat.detach().numpy()
        #actual = targets.numpy()
        actual = targets.reshape((len(targets), 1))

        loss += criterion(yhat,actual).item()

        #print(yhat)
        predictions.append(yhat.detach().numpy())
        actuals.append(actual.detach().numpy())
    
    #print(type(predictions))
    predictions, actuals= vstack(predictions), vstack(actuals)
    return predictions, actuals

train(m1, ccle_trainloader, epochs=100)
train(m2, gdsc_trainloader, epochs = 100)

#in-study test results ccle 30%
mse_loss_ccle, mae_loss_ccle, r2_ccle = test(m1, ccle_testloader)
print(mse_loss_ccle, mae_loss_ccle, r2_ccle)

#in-study test results ccle 30%
mse_loss_gdsc, mae_loss_gdsc, r2_gdsc = test(m2, gdsc_testloader)
print(mse_loss_gdsc, mae_loss_gdsc, r2_gdsc)

#predict(ccle_X_test.iloc[0,:], m1)

#mixed study results trained on CCLE (70%)

mixed_test = pd.concat([ccle_test, gdsc_test], ignore_index=True)

mixed_test = mixed_Dataset_for_test(mixed_test)

mixed_test_dl = DataLoader(mixed_test, batch_size=16, shuffle=False)

#test m1 on mixed test data
mse_loss_mixed_m1, mae_loss_mixed_m1, r2_mixed_m1 = test(m1, mixed_test_dl)
print(mse_loss_mixed_m1, mae_loss_mixed_m1, r2_mixed_m1)

#test m2 on mixed test data
mse_loss_mixed_m2, mae_loss_mixed_m2, r2_mixed_m2 = test(m2, mixed_test_dl)
print(mse_loss_mixed_m2, mae_loss_mixed_m2, r2_mixed_m2)

#m5

mixed_train = pd.concat([ccle_train, gdsc_train], ignore_index=True)

mixed_train = mixed_Dataset_for_test(mixed_train)

mixed_train_dl = DataLoader(mixed_train, batch_size=16, shuffle=True)

m5 = Net().to(DEVICE)

train(m5, mixed_train_dl, epochs=100)
#train(m2, gdsc_trainloader, epochs = 100)

#test m5 on mixed test data
mse_loss_mixed_m5, mae_loss_mixed_m5, r2_mixed_m5 = test(m5, mixed_test_dl)
print(mse_loss_mixed_m5, mae_loss_mixed_m5, r2_mixed_m5)

ccle_y_train_pred =test(m1, ccle_trainloader)
gdsc_y_train_pred = test(m2, gdsc_trainloader)

ccle_y_train_pred, ccle_y_train_m1 = predict(m1, ccle_trainloader)
gdsc_y_train_pred, gdsc_y_train_m2 = predict(m2, gdsc_trainloader)

ccle_y_train_pred

"""WA method"""

ccle_y_pred, ccle_y_test_m1 = predict(m1, ccle_testloader)
gdsc_y_pred, gdsc_y_test_m2 = predict(m2, gdsc_testloader)

avg_y_pred = (ccle_y_pred + gdsc_y_pred)/2

avg_y_pred = pd.Series(avg_y_pred.squeeze())

avg_y_pred_stacked = pd.concat([avg_y_pred, avg_y_pred], ignore_index=True)

mixed_y_test1 = pd.concat([pd.Series(ccle_y_pred.squeeze()),pd.Series(gdsc_y_pred.squeeze())], ignore_index =True)

print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test1, avg_y_pred_stacked))

#mean absolute error
print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test1, avg_y_pred_stacked))

# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(mixed_y_test1, avg_y_pred_stacked))

"""do a linear regression on the training scores"""

m4 = linear_model.LinearRegression()

m4.fit(gdsc_y_train_pred, ccle_y_train_pred)

# Make predictions using the testing set
ccle_y_pred_m4 = m4.predict(gdsc_y_pred.reshape(-1,1))

#avg ccle values predicted by m4 + gdsc input y values  to m4 
gdsc = (ccle_y_pred_m4 + gdsc_y_pred.reshape(-1,1))/2

#print(gdsc)
print("Mean squared error: %.2f" % mean_squared_error(gdsc_y_test, gdsc))

#mean absolute error
print("Mean absolute error: %.2f" % mean_absolute_error(gdsc_y_test, gdsc))

# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(gdsc_y_test, gdsc))

m3 =linear_model.LinearRegression()

m3.fit(ccle_y_train_pred, gdsc_y_train_pred)

# Make predictions using the testing set
gdsc_y_pred_m3 = m3.predict(ccle_y_pred.reshape(-1,1))

ccle = (gdsc_y_pred_m3 + ccle_y_pred.reshape(-1,1))/2
print("Mean squared error: %.2f" % mean_squared_error(ccle_y_test, ccle))

#mean absolute error
print("Mean absolute error: %.2f" % mean_absolute_error(ccle_y_test, ccle))

# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(ccle_y_test, ccle))

ccle = pd.Series(ccle.squeeze())
gdsc =pd.Series(gdsc.squeeze())

concated = pd.concat([ccle, gdsc], ignore_index=True)

#test on mixed data 

print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test1, concated))

#mean absolute error
print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test1, concated))

# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(mixed_y_test1, concated))

"""FL"""

params1 = []
for param in m1.parameters():
  params1.append(param.data)

params2 = []
for param in m2.parameters():
  params2.append(param.data)

m6 = Net().to(DEVICE)
params3 = iter(params1 + params2)
for param in m6.parameters():
  param.data = next(params3)

#test m6 on mixed test data
mse_loss_mixed_m6, mae_loss_mixed_m6, r2_mixed_m6 = test(m6, mixed_test_dl)
print(mse_loss_mixed_m6, mae_loss_mixed_m6, r2_mixed_m6)
