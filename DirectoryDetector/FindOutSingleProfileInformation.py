#!/usr/bin/env python

#mainPath = "D:\OfficeWork\Development\WebCrawler\Data\Output\DirectoryDetection\NewLargestHostData"
#endHostNumber = 100

def findOutTheNumberOfSingleProfile(mainPath, endHostNumber):

    path = mainPath + "\DirectoryListSortedByPHONE.xml"
    indexPath = mainPath + "\DataFoundURL.xml"

    directoryTypePath = mainPath + "\HostWiseSingleProfileInformation.txt"

    multipleWebsitePath = mainPath + "\MutlitpleWebsites.txt"
    singleWebsitePath = mainPath + "\SingleWebsites.txt"
    hostName = mainPath + "\HostName.txt"

    line = []

    fp = open(path, "r")
    lines = fp.readlines()

    indexFp = open(indexPath, "r")
    directoryTypeFp = open(directoryTypePath, "w")

    multipleWebsiteFp = open(multipleWebsitePath, "w")
    singleWebsiteFp = open(singleWebsitePath, "w")
    hostNameFp = open(hostName, "w")

    processingFlag = False

    hostCounter = 0
    totalNumberOfPages = 0
    totalNumberOfPhones = 0

    for line in lines:
        
        in1 = line.find("<URL>")
        in2 = line.find("</URL>")
        if (in1 != -1 and in2 != -1):
            hostName = line[in1 + 5:in2]
            hostNameFp.write(hostName + "\n");
            
        if (line.startswith("<PROFILE>")):
            processingFlag = False
            startByte = endByte = 0
            continue
        
        if (line.startswith("</PROFILE>")):
            processingFlag = True
        
        in1 = line.find("<START_BYTE>")
        in2 = line.find("</START_BYTE>")
        if (in1 != -1 and in2 != -1):
            startByte = int(line[in1 + 12:in2])

        in1 = line.find("<END_BYTE>")
        in2 = line.find("</END_BYTE>")
        if (in1 != -1 and in2 != -1):
            endByte = int(line[in1 + 10:in2])

        if (processingFlag):
            hostCounter += 1        
            multipleCounter = 0
            multipleAmount = 0
            singleCounter = 0
            singleAmount = 0
            frequencyArray = []
            
            indexFp.seek(startByte)
            data = indexFp.read(endByte - startByte + 1)
            
            index1 = index2 = 0
            dataLength = len(data)
            
            while (True):
                index1 = data.find("<PHONE>", index1)
                if (index1 != -1):
                    index2 = index1
                index2 = data.find("</PHONE>", index2)
                
                if (index1 != -1 and index2 != -1):
                    frequency = int(data[index1 + 7:index2])
                    frequencyArray.append(frequency)
                else:
                    break
                index1 = index2
                index2 = index2 + 1
            frequencyArray.sort()
            length = len(frequencyArray)
            if (length > -1):
                for i in range(0, length-1):
                    if (frequencyArray[i] > 2):
                        multipleCounter += 1
                        multipleAmount += frequencyArray[i]
                    if (frequencyArray[i] == 1):# or frequencyArray[i] == 2):
                        singleCounter += 1
                        singleAmount += frequencyArray[i]
                        totalNumberOfPages += 1
                        totalNumberOfPhones += frequencyArray[i]
                                        
                print "%-50s"%("http://" + hostName) + " NumberOfPages : " + str("%10s"%singleCounter) +"         NumberOfPhones : "+str("%10s"%singleAmount)
                directoryTypeFp.write("%-50s"%("http://" + hostName) + " NumberOfPages : " + str("%10s"%singleCounter) +"         NumberOfPhones : "+str("%10s"%singleAmount) + "\n")

        if (int(hostCounter) > int(endHostNumber)):
            break
        
    print "========================================================================================================================"
    print "                                               TotalNumberOfPages: " + str("%10s"%totalNumberOfPages) + "    TotalNumberOfPhones : " + str("%10s"%totalNumberOfPhones)

    directoryTypeFp.write("========================================================================================================================\n")
    directoryTypeFp.write("                                               TotalNumberOfPages: " + str("%10s"%totalNumberOfPages) + "    TotalNumberOfPhones : " + str("%10s"%totalNumberOfPhones))

    directoryTypeFp.close()



