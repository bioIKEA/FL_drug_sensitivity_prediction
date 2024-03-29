# -*- coding: utf-8 -*-
"""NN_GDSC_gCSI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Sfm_egg2I73RNOLVW41nRjbxOfplKNHB
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


data_path= '/Users/kritibbhattarai/Downloads/trisha-kritib/data/sensitivity_data/new_aug2/'

GDSC_main=pd.read_csv(data_path+'GDSC_paired_common_with_gcsi.csv', index_col=0)
gCSI_main=pd.read_csv(data_path+'gCSI_paired_common_with_gdsc.csv', index_col=0)

GDSC_x = GDSC_main.iloc[:, 0:-1]
GDSC_y = GDSC_main.iloc[:, -1]

gCSI = gCSI_main.reset_index()
gCSI = gCSI.drop(columns='index')

gCSI_x = gCSI.iloc[:, 0:-1]
gCSI_y = gCSI.iloc[:, -1]

gCSI_x.iloc[0:2, 0:-20]

gCSI_x.iloc[:, 0:-21] = StandardScaler().fit_transform(gCSI_x.iloc[:, 0:-21])
GDSC_x.iloc[:, 0:-21] = StandardScaler().fit_transform(GDSC_x.iloc[:, 0:-21])

from sklearn.model_selection import train_test_split

gCSI_X_train, gCSI_X_test, gCSI_y_train, gCSI_y_test = train_test_split(gCSI_x, gCSI_y, test_size = 0.30, random_state = 42) 
GDSC_X_train, GDSC_X_test, GDSC_y_train, GDSC_y_test = train_test_split(GDSC_x, GDSC_y,test_size = 0.30, random_state = 42)

gCSI_train = pd.concat([gCSI_X_train, gCSI_y_train], axis = 1)

gCSI_test = pd.concat([gCSI_X_test, gCSI_y_test], axis = 1)

GDSC_test = pd.concat([GDSC_X_test, GDSC_y_test], axis = 1)

GDSC_train = pd.concat([GDSC_X_train, GDSC_y_train], axis = 1)

len(GDSC_test.columns)

"""custom dataset for dataloader"""

seed = 0
torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

class GDSC_Dataset(Dataset):
    # load the dataset
    def __init__(self, path, train_index, test_index,train_val_test = 1):
        # load the csv file as a dataframe
        df = path#read_csv(path, header=None)
        print("dataframe",df)
        print(type(df))
        # store the inputs and outputs
        self.X = df.values[:, 0:len(df.columns)-1]
        self.y = df.values[:, len(df.columns)-1]
        # ensure input data is floats
        self.X = self.X.astype('float32')
        self.X = StandardScaler().fit_transform(self.X)
        # label encode target and ensure the values are floats
        self.y = self.y.astype('float32')
        self.y = self.y.reshape((len(self.y), 1))

        x_train=self.X[train_index]
        x_test=self.X[test_index]

        y_train=self.y[train_index]
        y_test=self.y[test_index]
        # x_train, x_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=42)
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
        nn.Linear(len(GDSC_train.columns)-1, 64),
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

def load_data(path, train_index, test_index):
    # load the dataset
    train = GDSC_Dataset(path,train_index, test_index,train_val_test=1)
    test =GDSC_Dataset(path,train_index, test_index,train_val_test=3)
    batch_size =16

    # prepare data loaders
    train_dl = DataLoader(train, batch_size=batch_size, shuffle=True)
    test_dl = DataLoader(test, batch_size=batch_size, shuffle=False)
    return train_dl, test_dl


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


from sklearn.model_selection import KFold
num_folds = 10
kf = KFold(n_splits=num_folds,shuffle=True,random_state=42)

maes_our=[]
mses_our=[]
r2s_our=[]

i=0
for train_index, test_index in kf.split(GDSC_main,gCSI_main):
    m1 = Net().to(DEVICE)
    m2= Net().to(DEVICE)

    GDSC_trainloader, GDSC_testloader = load_data(GDSC_main, train_index, test_index)
    gCSI_trainloader, gCSI_testloader = load_data(gCSI_main, train_index,test_index)
    
    gCSI_X_train=gCSI_x.iloc[train_index,:]
    gCSI_X_test=gCSI_x.iloc[test_index,:]


    gCSI_y_train=gCSI_y[train_index]
    gCSI_y_test=gCSI_y[test_index]

    GDSC_X_train=GDSC_x.iloc[train_index,:]
    GDSC_X_test=GDSC_x.iloc[test_index,:]
    GDSC_y_train=GDSC_y[train_index]
    GDSC_y_test=GDSC_y[test_index]

    train_test_split(GDSC_x, GDSC_y,test_size = 0.30, random_state = 42)
    train(m1, GDSC_trainloader, epochs=100)
    train(m2, gCSI_trainloader, epochs = 100)

    #in-study test results GDSC 30%
    mse_loss_GDSC, mae_loss_GDSC, r2_GDSC = test(m1, GDSC_testloader)
    print(mse_loss_GDSC, mae_loss_GDSC, r2_GDSC)

    #in-study test results GDSC 30%
    mse_loss_gCSI, mae_loss_gCSI, r2_gCSI = test(m2, gCSI_testloader)
    print(mse_loss_gCSI, mae_loss_gCSI, r2_gCSI)

    #predict(GDSC_X_test.iloc[0,:], m1)

    #mixed study results trained on GDSC (70%)

    mixed_test = pd.concat([GDSC_test, gCSI_test], ignore_index=True)

    mixed_test = mixed_Dataset_for_test(mixed_test)

    mixed_test_dl = DataLoader(mixed_test, batch_size=16, shuffle=False)

    #test m1 on mixed test data
    mse_loss_mixed_m1, mae_loss_mixed_m1, r2_mixed_m1 = test(m1, mixed_test_dl)
    print(mse_loss_mixed_m1, mae_loss_mixed_m1, r2_mixed_m1)

    #test m2 on mixed test data
    mse_loss_mixed_m2, mae_loss_mixed_m2, r2_mixed_m2 = test(m2, mixed_test_dl)
    print(mse_loss_mixed_m2, mae_loss_mixed_m2, r2_mixed_m2)

    #m5

    mixed_train = pd.concat([GDSC_train, gCSI_train], ignore_index=True)

    mixed_train = mixed_Dataset_for_test(mixed_train)

    mixed_train_dl = DataLoader(mixed_train, batch_size=16, shuffle=True)

    m5 = Net().to(DEVICE)

    train(m5, mixed_train_dl, epochs=100)
    #train(m2, gCSI_trainloader, epochs = 100)

    #test m5 on mixed test data
    mse_loss_mixed_m5, mae_loss_mixed_m5, r2_mixed_m5 = test(m5, mixed_test_dl)
    print(mse_loss_mixed_m5, mae_loss_mixed_m5, r2_mixed_m5)

    GDSC_y_train_pred =test(m1, GDSC_trainloader)
    gCSI_y_train_pred = test(m2, gCSI_trainloader)

    GDSC_y_train_pred, GDSC_y_train_m1 = predict(m1, GDSC_trainloader)
    gCSI_y_train_pred, gCSI_y_train_m2 = predict(m2, gCSI_trainloader)

    GDSC_y_train_pred

    """WA method"""

    GDSC_y_pred, GDSC_y_test_m1 = predict(m1, GDSC_testloader)
    gCSI_y_pred, gCSI_y_test_m2 = predict(m2, gCSI_testloader)

    avg_y_pred = (GDSC_y_pred + gCSI_y_pred)/2

    avg_y_pred = pd.Series(avg_y_pred.squeeze())

    avg_y_pred_stacked = pd.concat([avg_y_pred, avg_y_pred], ignore_index=True)

    mixed_y_test1 = pd.concat([pd.Series(GDSC_y_pred.squeeze()),pd.Series(gCSI_y_pred.squeeze())], ignore_index =True)

    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test1, avg_y_pred_stacked))

    #mean absolute error
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test1, avg_y_pred_stacked))

    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test1, avg_y_pred_stacked))

    """do a linear regression on the training scores"""

    m4 = linear_model.LinearRegression()

    m4.fit(gCSI_y_train_pred, GDSC_y_train_pred)

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

    m3.fit(GDSC_y_train_pred, gCSI_y_train_pred)

    # Make predictions using the testing set
    gCSI_y_pred_m3 = m3.predict(GDSC_y_pred.reshape(-1,1))

    GDSC = (gCSI_y_pred_m3 + GDSC_y_pred.reshape(-1,1))/2
    print("Mean squared error: %.2f" % mean_squared_error(GDSC_y_test, GDSC))

    #mean absolute error
    print("Mean absolute error: %.2f" % mean_absolute_error(GDSC_y_test, GDSC))

    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(GDSC_y_test, GDSC))

    gdsc_ser = pd.Series(GDSC.squeeze())
    gcsi_ser =pd.Series(gCSI.squeeze())

    concated = pd.concat([gdsc_ser, gcsi_ser], ignore_index=True)

    #test on mixed data 


    i+=1
    print("fold..........................",i)
    mses_our.append(mean_squared_error(mixed_y_test1, concated))
    print("Mean squared error: %.2f" % mean_squared_error(mixed_y_test1, concated))

    #mean absolute error

    maes_our.append(mean_absolute_error(mixed_y_test1, concated))
    print("Mean absolute error: %.2f" % mean_absolute_error(mixed_y_test1, concated))

    # The coefficient of determination: 1 is perfect prediction

    r2s_our.append(r2_score(mixed_y_test1, concated))
    print("Coefficient of determination: %.2f" % r2_score(mixed_y_test1, concated))


with open("results/gdsc_gcsi_nn.txt", "a") as output:
    output.write("gdsc_gcsi_our_method_mae_nn="+str(maes_our)+"\n")
    output.write("gdsc_gcsi_our_method_mse_nn="+str(mses_our)+"\n")
    output.write("gdsc_gcsi_our_method_r2_nn="+str(r2s_our)+"\n")

