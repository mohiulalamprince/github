data1 = []
data2 = []

f1 = open("hostList.txt", "r")
data1 = f1.readlines()

f2 = open("b.txt", "r")
data2 = f2.readlines()

map = {}
mapList = {}
for line in data1:
    data = line.strip("\n")
    #data = data.split(' ')[1]
    map[data] = 1

cnt = 0
list = []
for line in data2:
    data = line.strip("\n")
    if (map.get(data) == 1):
        print data
        cnt += 1
        if (mapList.get(data) != 1):
            mapList[data] = 1
            list.append(data)

print "TOTAL Host : " + str(cnt)

for line in list:
    print line

print len(list)    