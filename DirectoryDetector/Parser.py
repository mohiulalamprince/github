import os
import sys
import time
from Hash2D import Hash2D

class Parser:
    
    def __init__(self):
    
        self.speicalStartChar = ('-', ':', '+', '(', '.', '[')
        self.keywordsForPhone = ("telephone", "tel", "mobile phone", "mobile number", "phone number", "phone", "mobile", "cell", "p:", "t:", "contact number")
        self.keywordsForHTMLTags = ("tel", "phone", "mobile")
        self.htmlTags = ("img", "span", "div")
        self.isPrintLog = True
        self.isKeywordInTag = False
        self.isKeywordInText = False
        self.preKeyword = ""
        self.tagKey = ""
        self.keywordFrePhone = Hash2D()
        self.keywordFreTag = Hash2D()
        self.clear()
        self.phnList = []
        self.lastDataFoundKeyword = ""
        self.lastDataFoundIdx = 0
        self.countDataLine = 0
        
    def clear(self):
        
        self.isPrintLog = False
        self.isKeywordInTag = False
        self.isKeywordInText = False
        self.preKeyword = ""
        self.tagKey = ""
        self.keywordFrePhone.clear()
        self.keywordFreTag.clear()
        self.lastDataFoundKeyword = ""
        self.lastDataFoundIdx = 0
        self.countDataLine = 0
        
    def printLog(self, logMsg):
        
        if self.isPrintLog:
            print logMsg            
    
    def getFileName(self, thisData):
        
        wTokens = thisData.split("/")
        
        if len(wTokens) > 0:
            return wTokens[-1]
        
        return ""       
        
    def getSrcValue(self, thisData):
        
        lbIDX = 0
        ubIDX = 0
        
        lbIDX = thisData.find("src")
        
        if lbIDX != -1:
            
            lbIDX = thisData.find("\"", lbIDX + 3)
            
            if lbIDX == -1:
                return ""
            
            ubIDX = thisData.find("\"", lbIDX + 1)
            
            if ubIDX == -1:
                return ""
            
            return self.getFileName(thisData[lbIDX:ubIDX])
         
        return ""

    def getImageSrcValue(self, thisData, srcTag):
        
        lbIDX = 0
        ubIDX = 0
        
        lbIDX = thisData.find(srcTag)
        
        if lbIDX != -1:
            
            lbIDX = thisData.find("\"", lbIDX + len(srcTag))
            
            if lbIDX == -1:
                return ""
            
            ubIDX = thisData.find("\"", lbIDX + 1)
            
            if ubIDX == -1:
                return ""
            
            return thisData[lbIDX:ubIDX]
         
        return ""
            
    def getKeywordFromTagData(self, thisData):
        
        #return ""
        tagIndex = -1
        tagKey = ""
        
        for i in range(len(self.htmlTags)):            
            if thisData.startswith("<" + self.htmlTags[i]):
                tagIndex = i
                break
        
        if tagIndex == -1:
            return ""
            
        #srcValue = self.getSrcValue(thisData)
        #print "SRC_VALUE: ", srcValue

        srcValue = self.getSrcValue(thisData)

        if len(srcValue) == 0:
            srcValue = self.getImageSrcValue(thisData, "class")

        #print "Data: ", thisData
        #print "SRC_VALUE: ", srcValue
        
        for key in self.keywordsForHTMLTags:
            if srcValue.find(key) != -1:
                tagKey = self.htmlTags[tagIndex] + "_" + key
                break
            
        return tagKey
    
    def isNumber(self, thisData):
        
        thisData = thisData.strip()
        
        if len(thisData) <= 0:
            return False
        
        if thisData[0] not in self.speicalStartChar and not thisData[0].isdigit():
            return False
        
        totalDigit = 0
            
        for ch in thisData:
            if ch.isdigit():
                totalDigit += 1
            
        if totalDigit >= 6:
            return True
        else:
            return False
    
    def processData(self, thisData):
        
        self.isKeywordInText = False
        
        #print "Prekey: ", self.preKeyword
        #print "TagKey: ", self.tagKey
        
        #print "\nLastDataFoundKeyword: ", self.lastDataFoundKeyword
        #print "LastDataFoundIDX: ", self.lastDataFoundIdx
        #print "DataLineCount: ", self.countDataLine
        
        keyPhoneLen = len(self.keywordsForPhone)
        
        for i in range(keyPhoneLen):
            
            keyword = self.keywordsForPhone[i]
            
            if thisData.startswith(keyword):
                
                self.isKeywordInText = True
                self.preKeyword = keyword
                #print "Keyword Found: ", self.preKeyword
                strValue = thisData[len(keyword):]
                
                idx = strValue.find(":")
                
                if idx != -1:
                    strValue = strValue[idx+1:]                   
                
                if self.isNumber(strValue):
                    #print "KeyWord Data"
                    
                    if self.lastDataFoundKeyword != self.preKeyword or (self.countDataLine - self.lastDataFoundIdx) > 2:
                        
                        self.keywordFrePhone.insert(self.preKeyword, strValue.strip())                   
                        self.lastDataFoundKeyword = self.preKeyword
                        self.lastDataFoundIdx = self.countDataLine
                    
                    #self.countDataLine += 1
                        
                    self.phnList.append(strValue.strip())  #just for test
                    #self.preKeyword = ""
                    #self.tagKey = ""
                break
            
        if not self.isKeywordInText:
            
            if self.isNumber(thisData):
                #print "Non Keyword Data"
                if len(self.preKeyword) > 0:
                    
                    if self.lastDataFoundKeyword != self.preKeyword or (self.countDataLine - self.lastDataFoundIdx) > 2:
                        self.keywordFrePhone.insert(self.preKeyword, thisData)
                        
                        self.lastDataFoundKeyword = self.preKeyword
                        self.lastDataFoundIdx = self.countDataLine
                    
                    #self.countDataLine += 1
                        
                    self.phnList.append(thisData)              #just for test     
                    
                elif len(self.tagKey) > 0:
                    
                    if self.lastDataFoundKeyword != self.preKeyword or (self.countDataLine - self.lastDataFoundIdx) > 2:
                    
                        self.keywordFreTag.insert(self.tagKey, thisData)
                    
                        self.lastDataFoundKeyword = self.preKeyword
                        self.lastDataFoundIdx = self.countDataLine
                    
                    #self.countDataLine += 1
            
            self.preKeyword = ""
            self.tagKey = ""
                
    def parseData(self, htmlData, htmlLength):
        
        startTime = time.clock()
        
        lbIDX = 0
        ubIDX = 0
        lastUBIDX = 0
        strData = ""
        tagKey = ""
        keywordData = ""
        totalTagTimeSearch = 0
        totalTimeScript = 0
        totalProcessTextTime = 0
        totalSignSearchTime = 0
        self.countDataLine = 0
                
        while True:
            
            if ubIDX < 0:
                break
            
            lastUBIDX = ubIDX
            
            #stSign = time.clock()            
            lbIDX = htmlData.find(">", ubIDX + 1)            
            #totalSignSearchTime += time.clock() - stSign
            
            if lbIDX < 0:
                break
            
            self.isKeywordInTag = False
                        
            if lastUBIDX < lbIDX:
                #print "TAG_DATA: ", htmlData[lastUBIDX:lbIDX]
                tempTag = ""
                #stTagSearchTime = time.clock()
                tempTag= self.getKeywordFromTagData(htmlData[lastUBIDX:lbIDX].strip().lower())
                #print "Time to Tag Data Search: ", (time.clock()-stTagSearchTime)
                #totalTagTimeSearch += (time.clock()-stTagSearchTime)
                
                if len(tempTag) > 0:
                    self.tagKey = tempTag
                    
                #print "TAG_KEYWORD: ", tempTag              
                    
            #stSign = time.clock()
            ubIDX = htmlData.find("<", lbIDX + 1)
            #totalSignSearchTime += time.clock() - stSign
            
            if ubIDX < 0:
                break
            
            lastUBIDX = ubIDX
            
            #stScript = time.clock()
            
            if htmlLength > ubIDX + 7 and htmlData[ubIDX+1:ubIDX+7].lower() == "script":
                
                ubIDX = htmlData.find("</script>", ubIDX + 7)               
                
                if ubIDX == -1:
                    ubIDX = lastUBIDX
                    
                continue;            
            
            if htmlLength > ubIDX + 6 and htmlData[ubIDX+1:ubIDX+6].lower() == "style":
                
                ubIDX = htmlData.find("</style>", ubIDX + 6)               
                
                if ubIDX == -1:
                    ubIDX = lastUBIDX
                    
                continue;
                
            #totalTimeScript += time.clock() - stScript
            
            lastUBIDX = ubIDX
            
            #stProcessText = time.clock()
            
            if ubIDX - lbIDX +1 > 50:
                continue
            
            strData = htmlData[lbIDX+1:ubIDX].lower()
            strData = strData.replace("&nbsp;", "").strip()
            
            if len(strData) > 1:                
                #print "TEXT_DATA: ", strData
                self.countDataLine += 1
                self.processData(strData)
                
                
            #totalProcessTextTime += time.clock() - stProcessText
        
        #print "Time to Search < >: ", totalSignSearchTime 
        #print "Time to Process Text: ", totalProcessTextTime
        #print "Time to Script Search: ", totalTimeScript 
        #print "Time to Tag Data Search: ", totalTagTimeSearch                
        self.printLog("Time For Parsing: " + "%lf"%(time.clock()-startTime) + " Sec(s)")       

if __name__ == "__main__":
    
    fileName = r"E:/DirectoryDetectorBugList/11.htm"
    inFile = open(fileName, "r")
    parser = Parser()
    data = inFile.read()
    parser.parseData(data, len(data))
    inFile.close()
    parser.keywordFrePhone.printHash()
    parser.keywordFreTag.printHash()
    
    print parser.keywordFrePhone.size()
    print parser.keywordFreTag.size()
    print parser.phnList
    print len(parser.phnList)
            
            
                
            
                
            
            
            
            
            
            
            
            
            
            
            
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
        
        
