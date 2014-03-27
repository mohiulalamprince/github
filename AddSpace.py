
import os, sys

class AddSpace:
    
    def getTagContent(self, thisContent, startTag, endTag):
        
        lbIDX = thisContent.find(startTag)
        
        if lbIDX == -1:
            return ""
        
        ubIDX = thisContent.find(endTag, len(startTag) + lbIDX)
        
        if ubIDX == -1:
            return ""
        
        return thisContent[lbIDX+len(startTag) : ubIDX]
        
    def seperateWord(self, thisWord):
        
        resStr = ""
        tempStr = ""
        preDigit = False
        
        for ch in thisWord:
            if (not preDigit and ch.isdigit()) or ch.isupper():                
                resStr += " " + tempStr
                tempStr = ch
                preDigit = ch.isdigit()
            else:
                tempStr += ch
        
        if len(tempStr) != 0:
            resStr += " " + tempStr
                
        return resStr.strip(" ")
    
    def formatString(self, thisStr):
        
        resStr = ""
        
        tokens = thisStr.split(" ")
        
        for token in tokens:            
            resStr += " " + self.seperateWord(token)
            
        return resStr.strip(" ")      
    
    def addSpace(self, inputFilePath, outputFilePath):
        
        if not os.path.exists(inputFilePath):
            print "No Such File: ", inputFilePath
            return
        
        try:
            
            inputFile = open(inputFilePath, "r")
            outputFile = open(outputFilePath, "w")
            
            tempProfile = ""
            isAddress = False
            
            while True:
                
                line = inputFile.readline()
                
                if line == None:
                    break
            
                if isAddress:
                    isAddress = False
                    line = self.formatString(line)                                        
                
                tempProfile += line
                    
                if line.find("</BUSINESS_PROFILE>") != -1:
                
                    outputFile.write(tempProfile)
                    outputFile.flush()
                    tempProfile = ""
                
                elif line.find("<ADDRESS>") != -1:                    
                    isAddress = True
                    
        except:
            print "Exception: ", str(sys.exc_info())        
        finally:
            
            if inputFile != None:
                inputFile.close()
            
            if outputFile != None:
                outputFile.close()
        
            
            
if __name__ == "__main__":
    addSpace = AddSpace()
    print addSpace.formatString("32 Lincoln RoadIndustrial SitesBenoni South1502South Africa")