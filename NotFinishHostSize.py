import os

path = "D:\HostData\WebSite\LinkDB"

def readDownloadedLinkPathConfigCM(path):
    fp = open(path + "\config.CM", "r")
    data = fp.readline()
    fp.close()
    
    if (len(data) >= 2):
        data = data.split()[0]
    else:
        data = 0

    dirName = os.listdir(path)

    maxName = -100
    for file in dirName:
        name = file.split(".")[0]
        if (name == "config"):
            continue
        if (int(name) > maxName):
            maxName = int(name)
    if (maxName > int(data)):
        data = maxName
    return data

def readTotalDocSizeAndDocNumber(file):
    
    list = None
    list = []
    
    fp = open(file + ".linkPath", "r")
    list = fp.readlines()
    fp.close()
    
    size = long(0)
    for line in list:
        tokens = line.split()
        if (len(tokens) == 7):
            size += (long(tokens[6]) - long(tokens[3]) + 1)
        else:
            print "ERROR: in " + line
    if (len(list) >= 2):
        return len(list)-2, size
    else:
        return 0, 0
    
def sizeOutput(sz):
    gb, mb, kb, b = 1024**3, 1024**2, 1024**1, 1024**0

    GB = sz/gb
    sz %= gb
    MB = sz/mb
    sz %= mb
    KB = sz/kb
    sz %= kb
    B = sz/b
    
    ret = ""

    if (GB > 0):
        ret += str(GB) + " GB "
    if (MB > 0):
        ret += str(MB) + " MB "
    if (KB > 0):
        ret += str(KB) + " KB "
    if (B > 0 or len(ret) == 0):
        ret += str(B) + " Byte "
    return ret

def process():

    log = open("NotFinishHost.log", "w");    
    fp = open("hostName.txt", "r")

    hostList = fp.readlines()

    totalDocCounter = long(0)
    totalDocSize = long(0)

    for host in hostList:

        if (host.startswith("http://")):
            host = host[7:len(host)]
        elif(host.startswith("https://")):
            host = host[8:len(host)]

        if (host.endswith("\n")):
            host = host[0:len(host)-1]
        if (host.endswith("/")):
            host = host[0:len(host)-1]
            
        counter = long(0)
        size = long(0)
        hostSize = long(0)
        hostDocCounter = long(0)
        
        if (os.path.exists(path + "\\" + host)):
            if (len(os.listdir(path + "\\" + host)) == 7):
                if (os.path.exists(path + "\\" + host + "\DownloadedLinkPath")):
                    tmpPath = path + "\\" + host + "\DownloadedLinkPath"
                    totalDownloadedLinkPath = readDownloadedLinkPathConfigCM(tmpPath)
                    totalDownloadedLinkPath = int(totalDownloadedLinkPath)
                    for i in range(0, totalDownloadedLinkPath-1):          
                        counter, size = readTotalDocSizeAndDocNumber(tmpPath +"\\" + str(i + 1))
                        hostSize += size
                        hostDocCounter += counter
                        
                    totalDocCounter += hostDocCounter
                    totalDocSize += hostSize
                    
                    print "http://" + host + "/" + "\n[HOST_INFO:] SIZE=" + str(sizeOutput(hostSize)) + " NUMBER_OF_DOCUMENT=" + str(hostDocCounter)
                    print "[INFO:] TOTAL_SIZE=" + str(sizeOutput(totalDocSize)) + " TOTAL_DOCUMENT_NUMBER=" + str(totalDocCounter) + "\n"

                    log.write("http://" + host + "/" + "\n[HOST_INFO:] SIZE=" + str(sizeOutput(hostSize)) + " NUMBER_OF_DOCUMENT=" + str(hostDocCounter) + "\n")
                    log.write("TOTAL_SIZE=" + str(sizeOutput(totalDocSize)) + " TOTAL_DOCUMENT_NUMBER=" + str(totalDocCounter) + "\n\n")
                    log.flush()
            else:
                print "[ERROR:] Inconsistent host"
                log.write("[ERROR:] Inconsistent host\n")
    log.close()
    fp.close()
        
process()