import time
print '--------start------'
print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

print 'read file begin'

f1 = open('E:/tianOnly/data_format2/test_format2.csv','r')
head = f1.readline()

tmp = []
for line in f1:
	tes = line.strip('\r\n').split(',')
	if tes[4] == '':
		tmp.append(line)
print len(tmp)
f1.close()

print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print 'write result begin'

f2 = open('F:/testresult.csv','w')
f2.write(head)
for i in tmp:
	f2.write(i)
f2.close()

print '-------end---------'
print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))