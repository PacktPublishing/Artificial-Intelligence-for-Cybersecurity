# https://github.com/ibrahimyilmaz04/Anomaly-Detection-inIndustrial-Control-Systems/blob/master/Machine%20Learning%20Models/KNN.py
# use the knn as our classification algorithm

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.nn.init as init
import torch.utils.data

import sklearn

df = pd.read_csv("scada.csv")
data = df.drop(['Address','CommandResponse','ControlMode','ControlScheme','InvalidDataLength','InvalidFunctionCode','deltaPIDCycleTime','deltaPIDDeadband','deltaPIDGain','deltaPIDRate','deltaPIDReset','deltaSetPoint','PIDCycleTime','PIDDeadband','PIDGain','PIDRate','PIDReset','SetPoint'], axis=1)
label_encoder = LabelEncoder()
data['FunctionCode'] = label_encoder.fit_transform(data['FunctionCode'])
data = data[data.PumpState != 'X']
data = data[data.SolenoidState != 'X']
data = data.replace({'Label' : { 'Good' : 1, 'Burst' : 0, 'Fast' : 0, 'Negative' : 0, 'Setpoint' : 0,'Single' : 0, 'Slow' : 0, 'Wave' : 0}})
y = data.Label
x= data.drop(['Label'], axis=1)
x['PumpState'] = label_encoder.fit_transform(x['PumpState'])
x['SolenoidState'] = label_encoder.fit_transform(x['SolenoidState'])

XData = np.array(x)
YData = np.array

scaling = MinMaxScaler(feature_range=(-1,1)).fit(XData)
XData = scaling.transform(XData)

scaler = sklearn.preprocessing.StandardScaler().fit(XData)
XData = scaler.transform(XData)


X_train, X_test, y_train, y_test = train_test_split(XData, YData, test_size=0.2, shuffle=True, random_state=1)
knn = KNeighborsClassifier(n_neighbors=2)
knn.fit(X_train,y_train)
knn.score(X_test,y_test)