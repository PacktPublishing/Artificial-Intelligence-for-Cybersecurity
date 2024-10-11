# Chapter 8: User and Entity Behavior Analysis
# Code originally created using Google Collab

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

df_ueba = pd.read_csv('ueba.csv')

import ipaddress

df_ueba.describe(include='all')

import ipaddress
def iptointeger(ip):
  return int(ipaddress.ip_address(ip))

ueba_features = pd.DataFrame()

ueba_features['HostIP'] = df_ueba['HostIP'].apply(iptointeger)

ueba_features['RemoteIP'] = df_ueba['RemoteIP'].apply(iptointeger)

df_ueba["RemotePort"].value_counts().sort_index()

from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(sparse_output=False).set_output(transform="pandas")

remoteport_encoded = encoder.fit_transform(df_ueba[['RemotePort', 'HostLocation', 'RemoteIPLocation', 'ProcessImage']])

ueba_features[remoteport_encoded.columns] = remoteport_encoded

min_max_scaler = MinMaxScaler()

ueba_features_scaled = min_max_scaler.fit_transform(ueba_features)

from sklearn.ensemble import IsolationForest

isolationforest = IsolationForest(n_estimators=100, contamination=0.05)

anomaly_labels = isolationforest.fit_predict(ueba_features_scaled)

anomaly_scores = isolationforest.decision_function(ueba_features_scaled)

ueba_features['anomaly_labels'] = anomaly_labels

ueba_features['anomaly_scores'] = anomaly_scores

print(ueba_features[ueba_features['anomaly_labels']==-1])

ueba_features[ueba_features['anomaly_labels']==-1][['HostLocation_USA', 'RemoteIPLocation_China', 'RemoteIPLocation_France', 'RemoteIPLocation_Portugal', 'RemoteIPLocation_UK', 'RemoteIPLocation_USA', 'anomaly_labels', 'anomaly_scores']]

ueba_features['anomaly_scores'].plot(kind='bar')

print(ueba_features[ueba_features['anomaly_labels']==-1])