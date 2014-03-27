import os

list = []
dirList = os.listdir("D:\OfficeWork\Development\WebCrawler\BusinessSearch\Experiment")
for dir in dirList:
    if (os.path.isdir(dir)):
        path = "http://" + dir + "/\n"
        list.append(path)

f = open("HostName.txt", "a")
for hostName in list:
    f.write(hostName)
f.close()
