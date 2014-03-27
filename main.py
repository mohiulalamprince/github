import TCPClient
import time
import os

if __name__=='__main__':
    query = None
    counter = None

    t1 = time.clock()
    listOfDirectory = os.listdir("e:\\LinkDB\\")
   
    for directory in listOfDirectory:
        listOfFiles = os.listdir('E:\\LinkDB\\' + directory + "\\LinkExtractionBlock")
        for file in listOfFiles:
            basename = file.split(".")[0]
            if (basename == "config"):
                continue
            query = '<URLSeen><HostName>' + directory + "</HostName><InputLocation>e:\\LinkDB\\" + directory + "\\LinkExtractionBlock</InputLocation><OutputLocation>e:\\LinkDB\\" + directory + "\\URLSeenBlock</OutputLocation><BlockId>" + basename + '</BlockId></URLSeen>#'
            TCPClient.clientTest(query)
        
    print time.clock() - t1, "seconds process time for 1 million data"
    