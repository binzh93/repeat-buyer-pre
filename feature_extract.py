# -*- coding: utf-8 -*-
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
import numpy as np
from datetime import *
import time
def timepro_date(time):
  x = time.split('-')
  return date(int(x[0]),int(x[1]),int(x[2]))

def readfile(fname):
  f = open(fname, 'r')
  head = f.readline().strip('\n').split(',')
  len_h = len(head)
  res = dict()

  for i in f:
    lines = i.strip('\r\n').split(',')
    for j in xrange(len_h):
      res[head[j]] = lines[j]
    yield res
	

def data_analysis(fname1, fname2):
  #tmp = np.ones((100, 6))  #
  #x = tmp.astype(np.str)    #转换成字符类型

  day_item = [set() for i in xrange(31)]
  day_item_buy = [dict() for i in xrange(31)]
  day_item_notbuy = [dict() for i in xrange(31)]
  count_buy_all = [0 for i in xrange(31)]
  count_buy_exist = [0 for i in xrange(31)]
  count_por = [0 for i in xrange(31)]
  for e in readfile(fname1):
    item = e['item_id']
    time = e['time']
    behavior = int(e['behavior_type'])
    action_date = timepro_date(e['time'].split(' ')[0])
    day_num = (action_date -date(2014,11,18)).days   #将11.18 - 12.18转换成0-29

    if behavior == 4:
      count_buy_all[day_num] += 1
      if item in day_item_buy[day_num]:
        day_item_buy[day_num][item] += 1
      else:
        day_item_buy[day_num][item] = 1
    '''
    else:
      if item in day_item_notbuy[day_num]:
        day_item_notbuy[day_num] += 1
      else:
        day_item_notbuy[day_num] = 1
    '''
    day_item[day_num].add(item)
  for i in xrange(30):
    day_item[i+1] = day_item[i+1] | day_item[i]    #已经add到最后了，最后一个是全集
    #day_item[i+1].add(day_item[i])   
  #每天买的东西有访问记录没   第一天没法记录
  for i in xrange(30):
    for j in day_item_buy[i+1]:
      if j in day_item[i]:
        count_buy_exist[i+1] += day_item_buy[i+1][j]
  print count_buy_all
  print count_buy_exist
  for i in xrange(30):
    count_por[i+1] = count_buy_exist[i+1]*1.0/count_buy_all[i+1]
  print count_por


def feature_extract(fname1, fname2, flag):
  print 'extract tain_and_test_dict'
  print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

  train_dict = dict()
  user_set = set()
  item_set = set()
  ui_set = set()

  for e in readfile(fname1):
    action_date = timepro_date(e['time'].split(' ')[0])
    if action_date == date(2014, 12, 17):          #后面要改
      user = e['user_id']
      item = e['item_id']
      behavior = int(e['behavior_type'])

      user_set.add(user)
      item_set.add(item)
      ui_set.add((user, item))

      if (user, item) in train_dict:
        if behavior == 4:
          train_dict[(user, item)] = 1
        else:
          train_dict[(user, item)] += 0
      else:
        if behavior == 4:
          train_dict[(user, item)] = 1
        else:
          train_dict[(user, item)] = 0

    '''
    elif action_date == date(2014,12, 18):
      user = e['user_id']
      item = e['item_id']
      behavior = int(e['behavior_type'])
      if (user, item) in train_dict:
        if behavior == 4:
          train_dict[(user, item)] = 1
        else:
          train_dict[(user, item)] += 0
      else:
        if behavior == 4:
          train_dict[(user, item)] = 1
        else:
          train_dict[(user, item)] = 0
    '''


  print 'extract user feature'
  print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

  user_feature = dict()
  user_count = dict()
  user_tmp_set = dict()
  user_tmp_dcit = dict()
  user_day_count = dict()
  user_cate_count = dict()

  for e in readfile(fname1):
    user = e['user_id']
    if user in user_set:
      item = e['item_id']
      date_hour = e['time']
      behavior = int(e['behavior_type']) - 1
      action_date = timepro_date(date_hour.split(' ')[0])
      action_hour = int(date_hour.split(' ')[1])
      item_cate = e['item_category']

      if action_date < date(2014, 12, 17):#后面这里要改，因为这里设置
        if user not in user_feature:
          user_feature[user] = [0 for i in xrange(33)]           
          user_count[user] = [0 for i in xrange(8)]            
          user_tmp_set[user] = [set() for i in xrange(9)]         
          user_tmp_dcit[user] = [dict() for i in xrange(5)]
          user_day_count[user] = [0 for i in xrange(29)]   #后面天数不一样需要改的地方
          user_cate_count[user] = [dict() for i in xrange(29)]   #后面天数不一样需要改的地方

        user_count[user][behavior] += 1
        user_tmp_set[user][behavior].add(item)
        user_tmp_set[user][behavior+4].add(action_date)
        user_tmp_set[user][8].add(date_hour)
      
        if action_date == date(2014, 12, 12):
          user_count[user][behavior+4] += 1

        #下面要改  这个要结合 user_day_count[user] 一起改
        day_num = (action_date - date(2014, 11, 18)).days
        if behavior == 3:
          user_day_count[user][day_num] += 1
          if item in user_tmp_dcit[user][0]:
            user_tmp_dcit[user][0][item] += 1
          else:
            user_tmp_dcit[user][0][item] = 1

          if item_cate in user_tmp_dcit[user][1]:
            user_tmp_dcit[user][1][item_cate] += 1
          else:
            user_tmp_dcit[user][1][item_cate] = 1

        if item_cate not in user_tmp_dcit[user][2]:
          user_tmp_dcit[user][2][item_cate] = 1
        else:
          user_tmp_dcit[user][2][item_cate] += 1

        if item_cate not in user_tmp_dcit[user][3]:
          user_tmp_dcit[user][3][item_cate] = [0 for i in xrange(4)]
          user_tmp_dcit[user][3][item_cate][behavior] += 1
        else:
          user_tmp_dcit[user][3][item_cate][behavior] += 1
        if action_date == date(2014, 12, 12):
          if item_cate not in user_tmp_dcit[user][4]:
            user_tmp_dcit[user][4][item_cate] = [0 for i in xrange(4)]
            user_tmp_dcit[user][4][item_cate][behavior] += 1
          else:
            user_tmp_dcit[user][4][item_cate][behavior] += 1

        if item_cate not in user_cate_count[user][day_num]:
          user_cate_count[user][day_num][item_cate] = 1
        else:
          user_cate_count[user][day_num][item_cate] = 1

  for user in user_set:
    if user in user_feature:
      for i in xrange(4):
        user_feature[user][i] = user_count[user][i]
        user_feature[user][i+4] = user_count[user][i+4]
        user_feature[user][i+8] = user_feature[user][i+4]*1.0/user_feature[user][i] if user_feature[user][i] != 0 else 0
        user_feature[user][i+12] = user_feature[user][i]*1.0/29   #后面要该天数
        #下面这个要改
        if len(user_tmp_set[user][i+4]) == 0:
          user_feature[user][i+16] = -1
        else:
          user_feature[user][i+16] = (date(2014, 12, 17) - np.sort(np.array(list(user_tmp_set[user][i+4])))[-1]).days

      for i in xrange(3):
        user_feature[user][i+20] = user_feature[user][3]*1.0/user_feature[user][i] if user_feature[user][i] != 0 else 0
        user_feature[user][i+23] = user_feature[user][7]*1.0/user_feature[user][i+4] if user_feature[user][i+4] != 0 else 0
        user_feature[user][i+26] = len(user_tmp_set[user][3])*1.0/len(user_tmp_set[user][i]) if len(user_tmp_set[user][i]) != 0 else 0

      user_feature[user][29] = len(user_tmp_set[user][8])/29   #后面要该天数

      for i in user_tmp_dcit[user][0]:
        if user_tmp_dcit[user][0][i] >= 2:
          user_feature[user][30] += 1 

      user_feature[user][31] = user_feature[user][30]*1.0/user_feature[user][3] if user_feature[user][3] != 0 else 0

      tmp = 0
      day_len = len(user_day_count[user])
      for i in xrange(day_len):
        if user_day_count[user][i] >= user_day_count[user][tmp]:
          tmp = i
      user_feature[user][32] = 29 - tmp          #后面要改

  del user_count, user_day_count
  #user_feature, user_tmp_set, user_tmp_dcit, user_cate_count 可用


  print 'extract item feature'
  print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

  item_feature = dict()
  item_count = dict()
  item_tmp_dict = dict()
  item_tmp_set = dict()
  item_cate_dict = [dict() for i in xrange(4)]
  item_day_count = dict()

  for e in readfile(fname1):
    item = e['item_id']
    user = e['user_id']
    date_hour = e['time']
    behavior = int(e['behavior_type']) - 1
    action_date = timepro_date(date_hour.split(' ')[0])
    action_hour = int(date_hour.split(' ')[1])
    item_cate = e['item_category']

    if action_date < date(2014, 12, 17):
      if item not in item_feature:
        item_feature[item] = [0 for i in xrange(27)]
        item_count[item] = [0 for i in xrange(13)]
        item_tmp_dict[item] = [dict() for i in xrange(2)]
        item_tmp_set[item] = [set() for i in xrange(4)]
        item_day_count[item] = [0 for i in xrange(29)]    #后面天数不一样需要改的地方

      item_count[item][behavior] += 1
      item_tmp_set[item][behavior].add(user)
      item_tmp_dict[item][0][item] = item_cate

      if action_date == date(2014, 12, 12):
        item_count[item][behavior+4] += 1
      #这里感觉挺乱的   for example: item_cate_dict[0]{'cate_A':{'1001':2}}
      if item_cate not in item_cate_dict[behavior]:
        item_cate_dict[behavior][item_cate] = dict()
        if item not in item_cate_dict[behavior][item_cate]:
          item_cate_dict[behavior][item_cate][item] = 1
        else:
          item_cate_dict[behavior][item_cate][item] += 1
      else:
        if item not in item_cate_dict[behavior][item_cate]:
          item_cate_dict[behavior][item_cate][item] = 1
        else:
          item_cate_dict[behavior][item_cate][item] += 1

      day_num = (action_date - date(2014, 11, 18)).days
      #统计多次购买的人
      if behavior == 3:
        item_day_count[item][day_num] += 1
        if user in item_tmp_dict[item][1]:
          item_tmp_dict[item][1][user] += 1
        else:
          item_tmp_dict[item][1][user] = 1

  for item in item_set:
    if item in item_feature:
      #统计每种类别下的操作量
      for i in xrange(4):
        if item_tmp_dict[item][0][item] in item_cate_dict[i]:
          for j in item_cate_dict[i]:
            item_count[item][i+8] += item_cate_dict[i][j]

      for i in xrange(4):
        item_feature[item][i] = item_count[item][i]
        item_feature[item][i+4] = item_count[item][i+4]
        item_feature[item][i+8] = item_feature[item][i+4]*1.0/item_feature[item][i] if item_feature[item][i] != 0 else 0
        item_feature[item][i+12] = item_count[item][i]*1.0/item_count[i+8] if item_count[i+8] != 0 else 0

      for i in xrange(3):
        item_feature[item][i+16] = item_count[item][3]*1.0/item_count[item][i] if item_count[item][i] != 0 else 0
        item_feature[item][i+19] = item_count[item][7]*1.0/item_count[item][i+4] if item_count[item][i+4] != 0 else 0
        item_feature[item][i+22] = len(item_tmp_set[item][3])*1.0/len(item_tmp_set[item][i]) if len(item_tmp_set[item][i]) != 0 else 0
    
      #计算多次购买的user数
      for i in item_tmp_dict[item][1]:
        if item_tmp_dict[item][1][i] >= 2:
          item_count[item][12] += 1

      item_feature[item][25] = item_count[item][12]*1.0/len(item_tmp_set[item][3]) if len(item_tmp_set[item][3]) != 0 else 0

      tmp = 0
      day_len = len(item_day_count[item])
      for i in xrange(day_len):
        if item_day_count[item][i] >= item_day_count[item][tmp]:
          tmp = i

      item_feature[item][26] = 29 - tmp     #后面天数不一样需要改的地方

  del item_count, item_tmp_dict, item_tmp_set, item_cate_dict, item_day_count
  #item_feature


  print 'extract ui_feature'
  print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
  ui_feature = dict()
  ui_count = dict()
  ui_tmp_dict = dict()
  ui_tmp_set = dict()
  ui_day_count = dict()
  
  for e in readfile(fname1):
    action_date = timepro_date(date_hour.split(' ')[0])
    if action_date < date(2014, 12, 17):                       #这里后面要改
      user = e['user_id']
      item = e['item_id']
      ui = (user, item)
      if ui in ui_set:
        behavior = int(e['behavior_type']) - 1
        date_hour = e['time']
        action_date = timepro_date(date_hour.split(' ')[0])
        action_hour = int(date_hour.split(' ')[1])
        item_cate = e['item_category']

        if ui not in ui_feature:
          ui_feature[ui] = [0 for i in xrange(32)]
          ui_count[ui] = [0 for i in xrange(8)]
          ui_tmp_dict[ui] = dict()
          ui_tmp_set[ui] = [set() for i in xrange(5)]
          ui_day_count[ui] = [0 for i in xrange(29)]        #这里后面要改


        ui_count[ui][behavior] += 1
        ui_tmp_set[ui][behavior].add(action_date)
        ui_tmp_set[ui][4].add(date_hour)

        if item not in ui_tmp_dict[ui]:
          ui_tmp_dict[ui][item] = item_cate

        if action_date == date(2014, 12, 12):
          ui_count[ui][behavior+4] += 1

        #统计每日的交互量
        day_num = (action_date - date(2014, 11, 18)).days
        ui_day_count[ui][day_num] += 1

  for ui in ui_set:
    if ui in ui_feature:
      for i in xrange(4):
        ui_feature[ui][i] = ui_count[ui][i]
        ui_feature[ui][i + 4] = ui_count[ui][i + 4]
        ui_feature[ui][i + 8] = ui_feature[ui][i] * 1.0 / user_feature[ui[0]][i] if user_feature[ui[0]][i] != 0 else 0
        ui_feature[ui][i + 12] = ui_feature[ui][i + 4] * 1.0 / ui_feature[ui][i] if ui_feature[ui][i] != 0 else 0
        if len(ui_tmp_set[ui][i]) == 0:
          ui_feature[ui][i + 16] = -1
        else:
          ui_feature[ui][i + 16] = (date(2014, 12, 17) - np.sort(np.array(list(ui_tmp_set[ui][i])))[-1]).days
        ui_feature[ui][i + 20] = user_tmp_dcit[ui[0]][4][ui_tmp_dict[ui][ui[1]]][i] * 1.0 / user_tmp_dcit[ui[0]][3][ui_tmp_dict[ui][ui[1]]][i]

      ui_feature[ui][24] = len(ui_tmp_set[ui][4]) * 1.0 / len(user_tmp_set[ui[0]][8]) if len(
        user_tmp_set[ui[0]][8]) != 0 else 0
      tmp = 0
      day_len = len(ui_day_count[ui])
      for i in xrange(day_len):
        if ui_day_count[ui][i] >= ui_day_count[ui][tmp]:
          tmp = i
      ui_feature[ui][25] = 29 - tmp  # 这里后面要改

      # 计算买的最多的item,该item是不是买的最多的item
      tmp_item_set = set()
      # 字典按value从大到小排序
      tmp_list = sorted(user_tmp_dcit[ui[0]][0].iteritems(), key=lambda x: x[1], reverse=True)
      tmp_max_value = tmp_list[0][1]
      for i in tmp_list:
        if i[1] == tmp_max_value:
          tmp_item_set.add(i[0])
      if ui[1] in tmp_item_set:
        ui_feature[ui][26] = 1

      # 计算买的最多的item_cate,该item对应的cate是不是买的最多的item_cate
      tmp_cate_set = set()
      tmp_list = sorted(user_tmp_dcit[ui[0]][1].iteritems(), key=lambda x: x[1], reverse=True)
      tmp_max_value = tmp_list[0][1]
      for i in tmp_list:
        if i[1] in tmp_list:
          tmp_cate_set.add(i[0])
      if ui_tmp_dict[ui][ui[1]] in tmp_cate_set:
        ui_feature[ui][27] = 1

      ui_feature[ui][28] = user_tmp_dcit[ui[0]][1][ui_tmp_dict[ui][ui[1]]]
      ui_feature[ui][29] = ui_feature[ui][24] * 1.0 / user_feature[ui[0]][3] if user_feature[ui[0]][3] != 0 else 0
      tmp_value = user_feature[ui[0]][0] + user_feature[ui[0]][1] + user_feature[ui[0]][2] + user_feature[ui[0]][3]
      ui_feature[ui][30] = user_tmp_dcit[ui[0]][2][ui_tmp_dict[ui][ui[1]]] * 1.0 / (tmp_value)

      day_len = len(user_cate_count[ui[0]])
      tmp_list = [0 for i in xrange(day_len)]
      for i in xrange(day_len):
        if ui_tmp_dict[ui][ui[1]] in user_cate_count[ui[0]][i]:
          tmp_list[i] = user_cate_count[ui[0]][i][ui_tmp_dict[ui][ui[1]]]
      tmp_max = 0
      for i in xrange(day_len):
        if tmp_list[i] >= tmp_list[tmp_max]:
          tmp_max = i

      ui_feature[ui][31] = 29 - tmp_max
  del user_tmp_set, user_tmp_dcit, user_cate_count, item_feature, ui_count, ui_tmp_dict, ui_tmp_set, ui_day_count

  print 'extract write_feature_to_file'
  print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
  fwr = open(fname2, 'w')
  fwr.write('user_id, item_id,')
  for i in xrange(32):
    fwr.write('ui' + str(i) + ',')
  for i in xrange(33):
    fwr.write('u' + str(i) + ',')
  for i in xrange(27):
    if i == 26:
      fwr.write('i' + str(i))
    else:
      fwr.write('i'+str(i)+',')
  if flag == 1:
    fwr.write(',label\n')
  else:
    fwr.write('\n')
  for ui in train_dict:
    for i in xrange(32):
      fwr.write(str(ui_feature[ui][i]) + ',')
    for i in xrange(33):
      fwr.write(str(user_feature[ui[0]][i]) + ',')
    for i in xrange(27):
      if i == 26:
        fwr.write(str(item_feature[ui[1]][i]))
      else:
        fwr.write(str(item_feature[ui[1]][i]) + ',')
    if flag == 1:
      fwr.write(',' + str(train_dict[ui]) + '\n')
    else:
      fwr.write('\n')



 


if __name__ == '__main__':
  print '----------------------------------'
  print '--------------begin---------------'
  print '----------------------------------'
  print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


  #data_analysis('E:/fresh_comp_offline/tianchi_fresh_comp_train_user.csv','da')
  feature_extract('E:/fresh_comp_offline/tianchi_fresh_comp_train_user.csv', 'E:/17_feature', 1)


  print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
  print '----------------------------------'
  print '--------------end-----------------'
  print '----------------------------------'




