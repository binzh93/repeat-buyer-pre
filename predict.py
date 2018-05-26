# -*- coding: UTF-8 -*-
# 无法显示中文可用如下2行代码
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

import numpy as np
import scipy as sp
import xgboost as xgb
from sklearn import metrics
import matplotlib.pyplot as plt
import time
import math 

def sigmoid(x):
    return 1.0/(1.0+math.exp(-x))


print "---------------------------------------------"
print "--------------- Python Begin-----------------"
print "---------------------------------------------"
print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

param = {}
param['objective'] = 'binary:logitraw'
param['eta'] = 0.03       #default=0.3，
param['max_depth'] = 6
param['eval_metric'] = 'auc'
param['silent'] = 1
param['min_child_weight'] = 600   #这个原来是100，太高了导致全为0，降下了可以
param['subsample'] = 0.7
param['colsample_bytree'] = 0.7
param['scale_pos_weight'] = 2
param['nthread'] = 4




train_file = 'F:/wuyong/train_feature.csv'
test_file = 'F:/wuyong/test_feature.csv'

train_data_all = sp.genfromtxt(train_file,delimiter=',',skip_header=1)
test_data_all = sp.genfromtxt(test_file,delimiter=',',skip_header=1)

#de = [0,1,60,62,63,94,95,96]   #96是label  7, 11, 15, 19      7,11,15,19,
#de = [0, 1, 3, 7,11,17, 22, 25,29,  42 ,46, 50,92]
de = [0, 1, 3, 7,11,17, 22, 25,29,  42 ,46, 50,92]

#rows = tain_data_all.shape[0]
cols = train_data_all.shape[1]
#print cols

col_list = [i for i in xrange(cols)]
for i in xrange(len(de)):
    col_list.remove(de[i])
             
train_data = train_data_all[:,col_list]
train_label = train_data_all[:,-1]
train_label = np.mat(np.mat(train_label).T)
test_data = test_data_all[:,col_list]
um_a = test_data_all[:,[0,1]]         #存放(user,merchant)

dtrain = xgb.DMatrix(train_data, label = train_label)
dtest = xgb.DMatrix(test_data)

bst = xgb.train(param, dtrain, 1000 )
test_val = bst.predict(dtest)

n = len(test_val)
um = dict()
test_pro = []
for i in xrange(n):
    test_pro.append(sigmoid(test_val[i]))
    um[(int(um_a[i][0]),int(um_a[i][1]))] = test_pro[i]

#print um[(163968,4605)]




f1 = open('E:/tianOnly/data_format1/test_format1.csv', 'r')
f2 = open('F:/my_pro.csv', 'w')
f2.write(f1.readline())

for line in f1:
    x = line.strip('\r\n').split(',')
    #f2.write(str(x[0])+','+str(x[1])+','+str(um[(int(x[0]),int(x[1]))])+'\n')
    f2.write(str(x[0])+','+str(x[1])+','+str(um[(int(x[0]),int(x[1]))])+'\n')








print "---------------------------------------------"
print "--------------- Python END-----------------"
print "---------------------------------------------"
print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))







