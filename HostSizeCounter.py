
hostCounter = None
totalDocumentFound = 0
hostCounter = 1

totalIndexFiles = 1
contentDirPath = "\\\\192.168.1.68\\NewLargestData\\HostData\\WebSite\\Content\\"
statFileNamePrefix = "stat_hostLargestData"

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

def process(input,output):
    global hostCounter
    global totalDocumentFound
    
    singleHostByteCount, allHostByteCount, htmlCount = 0, 0, 0

    while True:
        line = input.readline().strip()
        if (line == ""):
            break

        if (line[0] == '<'):
            if (len(line) > 1 and line[1] == '/'):
                output.write("<HOST_INFORMATION NO=" +str(hostCounter)+ ">\n")
                hostCounter = hostCounter + 1
                length = len(line)
                output.write("\t<HOST_NAME> "+line[2:length-1]+" </HOST_NAME>\n")
                output.write("\t<DATA_SIZE> "+sizeOutput(singleHostByteCount)+"</DATA_SIZE>\n")
                output.write("\t<DOWNLOADED_HTML> "+str(htmlCount)+" </DOWNLOADED_HTML>\n")
                output.write("</HOST_INFORMATION>\n\n")

                totalDocumentFound += htmlCount                
                allHostByteCount += singleHostByteCount
                singleHostByteCount, htmlCount = 0, 0
                #print "http://" + line[2:length-2]
        else:
            tokens = line.split(' ')
            if (len(tokens) == 6):
                singleHostByteCount += long(tokens[4])-long(tokens[1])+1
                htmlCount += 1
            else:
                print "[ERROR] index file format error "
                for value in tokens:
                    print value
    
    output.write("<TOTAL_SIZE> " + sizeOutput(allHostByteCount) + " </TOTAL_SIZE>\n")
    output.write("<TOTAL_DOCUMENT_FOUND> " + str(totalDocumentFound) + " </TOTAL_DOCUMENT_FOUND>")
    output.close()
    input.close()

for i in range(totalIndexFiles):
    input = open(contentDirPath+str(i+1)+".INDEX","r")
    output = open(statFileNamePrefix+"("+str(i+1)+".INDEX).txt","w")
    process(input,output)
