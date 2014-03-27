import sys
import os
import time
from IndexSpliter import IndexSpliter

####### Global Constants #######
DIR_PATH            = "\\\\192.168.1.68\\NewLargestData\\HostData\\WebSite\\Content"  # DIR_PATH is the path of the content file & index file
RECOVERY_PATH       = "D:\\OfficeWork\\Development\\WebCrawler\\BusinessSearch\\Experiments\\PythonScripts\\IndexScripts\\IndexRecoveryTool\\IndexRecoveryOptimized_v1.2\\TestRecovery"

BUFFER_SIZE         = 3*1024*1024

TOTAL_INDEX_FILES   = 1
TOTAL_CONTENT_FILES = 1

HTTP                = "http://"
HTTPS               = "https://"

IGNORE_END_TAGS     = ["</script>", "</style>", "-->", "</iframe>"]
IGNORE_END_TAGS_PREFIX_TABLE = [[-1,0,0,0,0,0,0,0,0,0],[-1,0,0,0,0,0,0,0,0],[-1,0,1,0],[-1,0,0,0,0,0,0,0,0,0]]

IMPORTANT_PATTERNS          = ["scr", "sty", "!--", "ifr", "/ht"] # script, style, comment, iframe, </html
IMPORTANT_PATTERNS_HASH     = []

####### Global Variables #######
_entryFileDict      = dict()

_buffer             = ""
_bufferIndex        = 0

_fromByte           = long(0)
_toByte             = long(0)

_pairList           = []
_contentFileList    = []
_contentFileSize    = []

_logFileModCount    = 0
_logFile            = open("recoveryLog.txt","w")

_currentTime        = long(0)
_totalHtmlRecovered = long(0)

_totalBytesRecovered        = long(0)
_totalIncompleteHtmlFound   = long(0)

_invalidFileNameCharacters  = ['\\','/',':','*','?','"','<','>','|']

_errorLogger                = open("ERROR_REPORTS.log","w")
_indexSplitter              = None
_initTimeSnapShot           = None
_allContentTotalBytes       = long(0)

tempTotalMissingBytes       = long(0)

####### Statistics Variables #######
_printStatFlag                          = False
statStartByte                           = 0
statEndByte                             = 0
statTimeSnapShot                        = 0.0
statTotalHtmlInTheLastBlock             = 0
statTotalIncompleteHtmlInTheLastBlock   = 0
statTotalBytesProcessed                 = long(0)
statTotalHtmlProcessed                  = 0
statTotalIncompleteHtmlProcessed        = 0
statSingleBlockTimeSnapShot             = 0.0

tempByteReadCount                       = long(0)

########### Methods #############
def preProcess():
    global _pairList
    global _contentFileList
    global _contentFileSize
    global DIR_PATH
    global IMPORTANT_PATTERNS_HASH
    global _allContentTotalBytes
    global _indexSplitter
    
    #DIR_PATH = "../../WebSite\\Content"
    
    # calc hash value of importants patterns
    for i in range(len(IMPORTANT_PATTERNS)):
        h = 0
        for ch in IMPORTANT_PATTERNS[i]:
            h = (h<<8)|ord(ch)
        IMPORTANT_PATTERNS_HASH.append(h)
    
    _indexSplitter = IndexSpliter("\\\\192.168.1.68\\NewLargestData\\HostData")
    
    print("Splitting index...\n")
    currentTime = time.clock()
    _indexSplitter.split()
    print("Time taken to split index               : %8ld seconds\n\n"%(time.clock()-currentTime))
    
    # open all the contentFiles
    # precalc their size
    for i in range(TOTAL_CONTENT_FILES):
        path = DIR_PATH+"\\"+"%d.CONTENT"%(i+1)
        _contentFileList.append(open(path,"rb"))
        _contentFileSize.append(os.path.getsize(path))
        _allContentTotalBytes += _contentFileSize[i]
        
    """
    # preProcess index file
    for i in range(TOTAL_INDEX_FILES):
        indexFile = open(DIR_PATH+"\\"+"%d.INDEX"%(i+1),"r") 
        
        while True:
            line = indexFile.readline().strip()
            if(line == ""):
                break
            if(line[0] != '<'):
                tokens = line.split(' ')
                _pairList[int(tokens[0])-1].append((long(tokens[1]),long(tokens[4])))

        indexFile.close()
    """

def sizeOutput(sz):
    gb, mb = 1024**3, 1024**2

    GB = sz/gb
    sz %= gb
    MB = sz/mb
    
    return (GB,MB)

def printStatistics(contentFileIndex): # generate statistics for last "BUFFER_SIZE" bytes
    global statTotalBytesProcessed
    global _indexSplitter
    
    statTotalElapsedTime        = (time.clock()-_initTimeSnapShot)
    statTotalRemainingByte      = _allContentTotalBytes - _indexSplitter.totalIndexedByte - statTotalBytesProcessed
    statEstimatedRemainingTime  = (statTotalElapsedTime/statTotalBytesProcessed)*statTotalRemainingByte
    
    (statTotalBytesProcessedGB,statTotalBytesProcessedMB) = sizeOutput(statTotalBytesProcessed)
    (statTotalRemainingByteGB,statTotalRemainingByteMB) = sizeOutput(statTotalRemainingByte)
    
    print("\n\n")
    print("Current Content File                    : %15s"%("%ld"%(contentFileIndex+1))+" CONTENT")
    print("Missing block, Start Byte               : %15s"%("%ld"%statStartByte)+" BYTE")
    print("Missing block, End Byte                 : %15s"%("%ld"%statEndByte)+" BYTE")
    print("Total Bytes Processed                   : %15s"%("%ld"%statTotalBytesProcessedGB+" GB "+"%ld"%statTotalBytesProcessedMB)+" MB")
    print("Total htmls Processed                   : %15s"%("%ld"%statTotalHtmlProcessed)+" HTMLS")
    print("Total incomplete html found             : %15s"%("%ld"%statTotalIncompleteHtmlProcessed)+" HTMLS")
    print("Total htmls in the last block           : %15s"%("%ld"%statTotalHtmlInTheLastBlock)+" HTMLS")
    print("Total incomplete html in the last block : %15s"%("%ld"%statTotalIncompleteHtmlInTheLastBlock)+" HTMLS")
    print("Total time elapsed                      : %15s"%("%.2lf"%(statTotalElapsedTime/60.0))+" MINUTES")
    print("Total time for last block               : %15s"%("%.3lf"%((time.clock()-statSingleBlockTimeSnapShot)))+" SECONDS")
    print("Total remaining bytes                   : %15s"%("%ld"%statTotalRemainingByteGB+" GB "+"%ld"%statTotalRemainingByteMB)+" MB")
    print("Estimated remaining time                : %15s"%("%.2lf"%(statEstimatedRemainingTime/60.0/60.0))+" HOURS")

def reloadBufferIfNeeded(contentFileIndex):
    global _fromByte
    global _toByte
    global _bufferIndex
    global _buffer

    global _printStatFlag
    global statStartByte
    global statEndByte
    global statTimeSnapShot
    global statTotalHtmlInTheLastBlock
    global statTotalIncompleteHtmlInTheLastBlock
    global statSingleBlockTimeSnapShot
    global statTotalBytesProcessed

    if(_bufferIndex >= len(_buffer)):
        _buffer = _contentFileList[contentFileIndex].read(min(BUFFER_SIZE,_toByte-_fromByte+1))
        _bufferIndex = 0
        
        if(_printStatFlag == True):
            printStatistics(contentFileIndex)
            
        statStartByte = _fromByte
        statEndByte = _fromByte + min(BUFFER_SIZE,_toByte-_fromByte+1) - 1
        statTotalBytesProcessed += statEndByte-statStartByte+1
        statTotalHtmlInTheLastBlock = 0
        statTotalIncompleteHtmlInTheLastBlock = 0
        statSingleBlockTimeSnapShot = time.clock()
        
        _printStatFlag = True

def readProtocol(contentFileIndex):
# on success it returns the size of the "protocol" string
# else, it returns 0
    global _hostUrl
    global _fullUrl
    global _fromByte
    global _toByte
    global _bufferIndex
    global tempByteReadCount

    httpSeeker = 0
    httpsSeeker = 0
    _hostUrl = ""
    _fullUrl = ""
    
    ret = 0
    
    while _fromByte <= _toByte:
        reloadBufferIfNeeded(contentFileIndex)
        ch = _buffer[_bufferIndex].lower()
        tempByteReadCount += 1
        if(ch == HTTP[httpSeeker]):
            httpSeeker += 1
        else:
            httpSeeker = 0
            
        if(ch == HTTPS[httpsSeeker]):
            httpsSeeker += 1
        else:
            httpsSeeker = 0
        
        _bufferIndex += 1
        _fromByte += 1
        
        if(httpSeeker == len(HTTP)):
            ret = len(HTTP)
            _hostUrl = "http://"
            _fullUrl = "http://"
            break
            
        if(httpsSeeker == len(HTTPS)):
            ret = len(HTTPS)
            _hostUrl = "https://"
            _fullUrl = "https://"
            break
    
    slashCount = 2

    while _fromByte <= _toByte:
        reloadBufferIfNeeded(contentFileIndex)    
        ch = _buffer[_bufferIndex].lower()
        tempByteReadCount += 1
        _bufferIndex += 1
        _fromByte += 1
        
        if(ch == '/'):
            slashCount += 1
        
        if(ch == '>'):
            _hostUrl = ""
            _fullUrl = ""
            ret = 0
            break
        
        if(ch == '<'):
            _fromByte -= 1
            _bufferIndex -= 1
            break

        if(ch == '?'):
            _fromByte -= 1
            _bufferIndex -= 1
            break
        
        if(slashCount == 2):
            _hostUrl += ch
        
        _fullUrl += ch
    
    return ret

def checkTheTag(contentFileIndex): #check the next 3 bytes for an IMPORTANT_PATTERN
    global _fromByte
    global _toByte
    global _bufferIndex
    
    h = 0
    
    if(_fromByte+2 > _toByte):
        return -2 # incomplete html found
    
    for i in range(3):
        reloadBufferIfNeeded(contentFileIndex)
        h = (h<<8)|ord(_buffer[_bufferIndex].lower())
        _fromByte += 1
        _bufferIndex += 1
        
    for i in range(len(IMPORTANT_PATTERNS)):
        if(IMPORTANT_PATTERNS_HASH[i] == h):
            return i
    
    return -1 # not matched

def skipIgnoreBlock(contentFileIndex, ignoreBlockIndex):
    global _fromByte
    global _toByte
    global _bufferIndex
    global tempByteReadCount
    seeker = -1
    
    while(_fromByte <= _toByte):
        reloadBufferIfNeeded(contentFileIndex)
        ch = _buffer[_bufferIndex]
        tempByteReadCount += 1
        _bufferIndex += 1
        _fromByte += 1
        
        if(seeker >= 0 and ch.lower() != IGNORE_END_TAGS[ignoreBlockIndex][seeker]):
            seeker = IGNORE_END_TAGS_PREFIX_TABLE[ignoreBlockIndex][seeker]
        
        seeker += 1    
        
        if(seeker == len(IGNORE_END_TAGS[ignoreBlockIndex])):
            return True
    
    return False

def readHtml(contentFileIndex):
    global _fromByte
    global _toByte
    global _htmlDepth
    global _bufferIndex
    global tempByteReadCount
        
    while(_fromByte <= _toByte):
        reloadBufferIfNeeded(contentFileIndex)        
        ch = _buffer[_bufferIndex]
        tempByteReadCount += 1
        _bufferIndex += 1
        _fromByte += 1
        
        if(ch == '<'):
            ret = checkTheTag(contentFileIndex)
            
            if(ret == -2): # incomplete html
                return False
            if(ret == 4): # end html tag found
                # we check only the 2nd,3rd & 4th char
                # read the next 3
                if(_fromByte+2 > _toByte):
                    return False

                reloadBufferIfNeeded(contentFileIndex)
                _fromByte += 3
                _bufferIndex += 3
                
                return True
            elif(ret > -1):
                if(not skipIgnoreBlock(contentFileIndex,ret)):
                    return False
        
    return False

def initializationForParsing():
    global _hostUrl
    global _fullUrl
    
    _hostUrl = ""
    _fullUrl = ""

def recover(contentFileIndex, fromByte, toByte): # recovers from 'fromByte' to 'toByte'
    global _fromByte
    global _toByte
    global _contentFileList
    global _hostUrl
    global _fullUrl
    global _totalIncompleteHtmlFound
    global _totalHtmlRecovered
    global _totalBytesRecovered
    global _logFileModCount

    global statTotalBytesProcessed
    global statTotalHtmlProcessed
    global statTotalIncompleteHtmlProcessed
    global statTotalHtmlInTheLastBlock
    global statTotalIncompleteHtmlInTheLastBlock
    
    global tempTotalMissingBytes

    _fromByte = fromByte-1
    _toByte = toByte-1

    if(_fromByte > _toByte):
        return
    
    tempTotalMissingBytes += (toByte-fromByte+1)

    _contentFileList[contentFileIndex].seek(_fromByte)
    reloadBufferIfNeeded(contentFileIndex)
    #print "FromByte: %d"%_fromByte+" ToByte: %d"%_toByte
    return
    while _fromByte <= _toByte:
        temp_fromByte = _fromByte
        initializationForParsing()
        protocolSize = readProtocol(contentFileIndex)
        
        if(protocolSize == 0):
            #statTotalBytesProcessed += (_fromByte-temp_fromByte)
            _totalIncompleteHtmlFound += 1
            statTotalHtmlProcessed += 1
            statTotalIncompleteHtmlProcessed += 1
            statTotalHtmlInTheLastBlock += 1
            statTotalIncompleteHtmlInTheLastBlock += 1
            continue
        
        urlStartsAt = _fromByte - len(_fullUrl)
        _fullUrl = _fullUrl.strip()
        urlEndsAt = urlStartsAt + len(_fullUrl) - 1
        
        htmlStartsAt = _fromByte
        
        if(readHtml(contentFileIndex) == False):
            #statTotalBytesProcessed += (_fromByte-temp_fromByte)
            _totalIncompleteHtmlFound += 1
            statTotalHtmlProcessed += 1
            statTotalIncompleteHtmlProcessed += 1
            statTotalHtmlInTheLastBlock += 1
            statTotalIncompleteHtmlInTheLastBlock += 1
            continue

        htmlEndsAt = _fromByte-1
        _hostUrl = _hostUrl.strip()
        
        entryFileNamePrefix = _hostUrl[protocolSize:len(_hostUrl)]
        
        entryFileName = entryFileNamePrefix+".ENTRY"
        entryFilePath = RECOVERY_PATH+"\\"+entryFileName

        try:
            entryFile = _entryFileDict[entryFileNamePrefix]
            entryFile.write("%d %d %d %d %d 1\n"%((contentFileIndex+1),urlStartsAt+1,urlEndsAt+1,htmlStartsAt+1,htmlEndsAt+1))
            #statTotalBytesProcessed += (htmlEndsAt-urlStartsAt+1)
            statTotalHtmlProcessed += 1
            statTotalHtmlInTheLastBlock += 1
            entryFile.flush()

            if(_logFileModCount == 0):
                _logFile.write("\tRecovered an html:: startByte %d, endByte %d\n"%(htmlStartsAt+1,htmlEndsAt+1))
                _logFile.flush()
            _logFileModCount = (_logFileModCount+1)&1023
            
            _totalHtmlRecovered += 1
            _totalBytesRecovered += long(htmlStartsAt-urlStartsAt+1)
        except KeyError:
            try:
                entryFile = open(entryFilePath,"a")
                entryFile.write("%d %d %d %d %d 1\n"%((contentFileIndex+1),urlStartsAt+1,urlEndsAt+1,htmlStartsAt+1,htmlEndsAt+1))
                #statTotalBytesProcessed += (htmlEndsAt-urlStartsAt+1)
                statTotalHtmlProcessed += 1
                statTotalHtmlInTheLastBlock += 1
                entryFile.flush()
                _entryFileDict[entryFileNamePrefix] = entryFile

                if(_logFileModCount == 0):
                    _logFile.write("\tRecovered an html:: startByte %d, endByte %d\n"%(htmlStartsAt+1,htmlEndsAt+1))
                    _logFile.flush()
                _logFileModCount = (_logFileModCount+1)&1023
            
                _totalHtmlRecovered += 1
                _totalBytesRecovered += long(htmlStartsAt-urlStartsAt+1)
            except IOError:
                _logFile.write("\tFile Opening Error: "+entryFileName+"\n")
                _logFile.flush()

def initializeGlobalVariables():
    global _currentTime
    global _totalBytesRecovered
    global _totalHtmlRecovered
    global _totalIncompleteHtmlFound
    global _bufferIndex
    global _buffer
    global _logFileModCount
    
    _buffer = ""
    _bufferIndex = 0
    _currentTime = time.clock()
    _totalBytesRecovered = 0
    _totalHtmlRecovered = 0
    _totalIncompleteHtmlFound = 0
    _logFileModCount = 0
    
def report(contentFileIndex):
    global _logFile
    _logFile.write("Log for the recovery of %d.CONTENT\n"%(contentFileIndex+1))
    _logFile.write("\tTime Taken: %d seconds\n"%(time.clock()-_currentTime))
    _logFile.write("\n\tTotal Html Recovered: %d\n"%(_totalHtmlRecovered))
    _logFile.write("\tTotal Bytes Recovered: %d\n"%(_totalBytesRecovered))
    _logFile.write("\tTotal Incomplete Html Found: %d\n\n"%(_totalIncompleteHtmlFound))
    _logFile.flush()

def mainProcess():
    global _contentFileList
    global _pairList
    global _contentFileSize
    global _logFile
    global _entryFileDict
    global _initTimeSnapShot
    
    _initTimeSnapShot = time.clock()
    print "MainProcess"
    
    for i in range(TOTAL_CONTENT_FILES):

        contentIndexFile = open(str(i+1)+".ContentIndex","r")
        
        lineCount = 0
        prevEndByte = 0
                
        for line in contentIndexFile:
            temp = line.split()
            recover(i,prevEndByte+1,int(temp[2])-1)
            prevEndByte = int(temp[5])
        
        recover(i,prevEndByte+1,_contentFileSize[i])
    
    for (entryFile,filePtr) in _entryFileDict.iteritems():
        filePtr.close()

    _logFile.close()

#sys.stderr = _errorLogger

print "Running Index Recovery Script... (IndexRecoveryOptimized_v1.2.py)\n\n"
preProcessingTime = time.clock()
preProcess()
print "preprocessing completed in %d seconds...\n\n"%(time.clock()-preProcessingTime)
print "totalIndexedByte: "+str(_indexSplitter.totalIndexedByte)
mainProcessTime = time.clock()
mainProcess()

i = long(0)

while i < tempTotalMissingBytes:
    i += 1

print "MainProcess time: "+str(time.clock()-mainProcessTime)
print "Total Missing Byte: %d"%tempTotalMissingBytes
