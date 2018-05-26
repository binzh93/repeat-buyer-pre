# -*- coding: UTF-8 -*-
# 无法显示中文可用如下2行代码
from pylab import mpl

from datetime import *
import time

def timepro_date(time):
    x = time.split('-')
    return date(int(x[0]), int(x[1]), int(x[2]))

def readfile(fname):
	ui_d = dict()
	f = open(fname, 'r')
	head = f.readline().strip('\r\n').split(',')
	head_len = len(head)
	for i in f.readlines():
		i = i.strip('\r\n').split(',')
		for j in xrange(head_len):
			ui_d[head[j]] = i[j]
		yield ui_d

def dataAnalysis(fname1):
	ui_set_before = set()
	ui_set_day = set()
	for e in readfile(fname1):
		action_date = timepro_date(e['time'].split(' ')[0])
		if action_date < date(2014, 12, 18):
			user = e['user_id']
			item = e['item_id']
			ui = (user, item)
			ui_set_before.add(ui)
		elif action_date == date(2014, 12, 18):
			user = e['user_id']
			item = e['item_id']
			behavior = int(e['behavior_type'])
			if behavior == 4:
				ui = (user, item)
				ui_set_day.add(ui)
				
			
			

	count = 0
	for i in ui_set_before:
		if i in ui_set_day:
			count += 1

	print '~17,all num:', len(ui_set_before)
	print 'isin:', count
	print '18 dangtian:', len(ui_set_day)
	print 'proportion:', count * 1.0/ len(ui_set_day)

def dataAnalysis2(fname1, fname2):
	ui_set_before = set()
	ui_set_day = set()
	ui_jiao_set = set()
	item_set = set()
	ui_jiao_before = set()
	for e in readfile(fname2):
		item = e['item_id']
		item_set.add(item)
	for e in readfile(fname1):
		action_date = timepro_date(e['time'].split(' ')[0])
		if action_date < date(2014, 12, 17):
			user = e['user_id']
			item = e['item_id']
			ui = (user, item)
			ui_set_before.add(ui)
		elif action_date == date(2014, 12, 17):
			user = e['user_id']
			item = e['item_id']
			behavior = int(e['behavior_type'])
			if behavior == 4:
				ui = (user, item)
				ui_set_day.add(ui)

	for ui in ui_set_day:
		if ui[1] in item_set:
			ui_jiao_set.add(ui)


	count = 0
	for i in ui_set_day:
		if i in ui_set_before:
			count += 1

	for ui in ui_set_before:
		if ui[1] in item_set:
			ui_jiao_before.add(ui)

	count2 = 0
	for ui in ui_set_day:
		if ui in ui_jiao_before:
			count2 += 1



	print '1', len(ui_set_day)
	print ' ', len(ui_jiao_set)
	print ' ', len(ui_jiao_set)*1.0/len(ui_set_day)
	print ' ', count
	print ' ', count*1.0/len(ui_set_day)
	print ' ', count2
	print ' ', count2*1.0/len(ui_set_day)


'''
	print '17号当天购买的总数：', len(ui_set_day)
	print '17号当天交集中购买的总数：', len(ui_jiao_set)
	print '17号当天交集中购买的总数占总的比例：', len(ui_jiao_set)*1.0/len(ui_set_day)
	print '17号之前的ui对在17号当天购买的总数：', count
	print '17号之前的ui对在17号当天购买的总数占总的比例：', count*1.0/len(ui_set_day)
	print '17号之前的ui对与item交集在17号当天购买的总数：', count2
	print '17号之前的ui对与item交集在17号当天购买的总数占总的比例：', count2*1.0/len(ui_set_day)
'''
def dataclean(fname1):
	user_dict =dict()
	user_set = set()
	for e in readfile(fname1):
		user = e['user_id']
		item = e['item_id']
		behavior = int(e['behavior_type']) - 1
		action_date = timepro_date(e['time'].split(' ')[0])
		day_num = (action_date - date(2014, 11, 18)).days
		#if day_num == 30:
			#if behavior == 0:
				#print '3030300330'
			

		user_set.add(user)
		if user not in user_dict:
			user_dict[user] = [0 for i in xrange(31)]
		if behavior == 0:
			user_dict[user][day_num] += 1


	f = open('F:/tttttttt.csv', 'w')
	f.write('user_id,')
	for i in xrange(30):
		f.write('day' + str(i) + ',')
	f.write('day30\n')


	for user in user_set:
		f.write(str(user) + ',')
		for i in xrange(31):
			if i == 30:
				f.write(str(user_dict[user][i]) + '\n')
			else:
				f.write(str(user_dict[user][i]) + ',')
			









if __name__ == '__main__':

  print '----------------------------------'
  print '--------------begin---------------'
  print '----------------------------------'
  print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

  #dataAnalysis2('E:/fresh_comp_offline/tianchi_fresh_comp_train_user.csv', 'E:/fresh_comp_offline/tianchi_fresh_comp_train_item.csv')

  dataclean('E:/fresh_comp_offline/tianchi_fresh_comp_train_user.csv')

  print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
  print '----------------------------------'
  print '--------------end-----------------'
  print '----------------------------------'






		
       
