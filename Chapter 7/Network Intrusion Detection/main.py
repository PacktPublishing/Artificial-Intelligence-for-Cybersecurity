import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report 
import pickle

columns = (['duration','protocol_type','service','flag','src_bytes','dst_bytes','land','wrong_fragment','urgent'
            ,'hot','num_failed_logins','logged_in','num_compromised','root_shell','su_attempted','num_root'
            ,'num_file_creations','num_shells','num_access_files','num_outbound_cmds','is_host_login'
            ,'is_guest_login','count','srv_count','serror_rate','srv_serror_rate','rerror_rate','srv_rerror_rate'
            ,'same_srv_rate','diff_srv_rate','srv_diff_host_rate','dst_host_count','dst_host_srv_count'
            ,'dst_host_same_srv_rate','dst_host_diff_srv_rate','dst_host_same_src_port_rate'
            ,'dst_host_srv_diff_host_rate','dst_host_serror_rate','dst_host_srv_serror_rate','dst_host_rerror_rate'
            ,'dst_host_srv_rerror_rate','label','difficulty_level'])

train_data = pd.read_csv('dataset/KDDTrain+.txt', header=None, names=columns)

train_data.drop(['difficulty_level','num_outbound_cmds'], axis=1, inplace=True)

le = LabelEncoder()
train_data['protocol_type'] = le.fit_transform(train_data['protocol_type'])
train_data['service'] = le.fit_transform(train_data['service'])
train_data['flag'] = le.fit_transform(train_data['flag']) 

train_data['label'] = train_data['label'].apply(lambda x: 'normal' if x == 'normal' else 'abnormal')
#print(train_data['label'].value_counts())
train_data['label'] = train_data['label'].apply(lambda x: 0 if x == 'normal' else 1)

X = train_data.drop(['label'], axis=1)
y = train_data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

svm_model = SVC(kernel='rbf')
svm_model.fit(X_train, y_train)

y_pred = svm_model.predict(X_test)

print('Training accuracy: ', svm_model.score(X_train, y_train))
print('Testing accuracy: ', svm_model.score(X_test, y_test))
print('SVM Model accuracy: ', np.round(accuracy_score(y_test,y_pred),6))
print('Classification Report:\n', classification_report(y_test,y_pred,target_names=['Normal','Abnormal']))

pkl_filename = "SVM_model.pkl" 
with open(pkl_filename, 'wb') as file:
    pickle.dump(svm_model, file)

"""
print('Starting Testing Process using the Test Dataset....')

test_data = pd.read_csv('dataset/KDDTest+.txt', header=None, names=columns)
test_data.drop(['difficulty_level', 'num_outbound_cmds'], axis=1, inplace=True)

le = LabelEncoder()
test_data['protocol_type'] = le.fit_transform(test_data['protocol_type'])
test_data['service'] = le.fit_transform(test_data['service'])
test_data['flag'] = le.fit_transform(test_data['flag'])
test_data['label'] = test_data['label'].apply(lambda x: 0 if x == 'normal' else 1)

X_test = test_data.drop(['label'], axis=1)
y_test = test_data['label']
X_test = scaler.transform(X_test)

y_pred = svm_model.predict(X_test)

print('Testing Phase accuracy: ', accuracy_score(y_test, y_pred))
print('SVM Model accuracy: ', accuracy_score(y_test, y_pred))
print('Classification Report:\n', classification_report(y_test, y_pred, target_names=["Normal", "Abnormal"]))
"""
