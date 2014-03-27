import os
import sys

class TypeDetector:

    def __init__(self,  inputDirectory, outputDirectory):
        
        self.inputDirectory = inputDirectory
        self.outputDirectory = outputDirectory
        self.currentHostName = ""
        self.otherTypes = ("agent", "agents")
        self.productKeywords = ("price", "currency")
        self.propertyKeywords = ("property", "properties", "agent", "agents", "price", "currency")
        self.keywordsForPhone = ("telephone", "tel", "mobile phone", "mobile number", "phone number", "phone", "mobile", "cell", "p:", "t:", "contact number")
        self.phonesMap = {}
        self.keywordsForHTMLTags = ("tel", "phone", "mobile", "skype_pnh_print_container")
        self.keyForOtherType = {}
        self.keyForProperty = {}
        self.keyForProduct = {}
        self.singleKeyForOtherType = {}
        self.singleKeyForProduct = {}
        self.singleKeyForProperty = {}
        self.singlePageWiseMaxCount = 0
        self.singlePageWiseMaxCountProduct = 0
        self.singlePageWiseMaxCountProperty = 0
        self.singlePageWiseMaxCountOtherType = 0
        self.fileDirectroyType = open(os.path.join(outputDirectory, "DirectoryType.xml"), 'w')
        self.fileDirectoryTypeSinglePage = open(os.path.join(outputDirectory, "DirectoryTypeSinglePage.xml"), 'w')
        self.fileFilteredBusinessDirectory = open(os.path.join(outputDirectory, "DirectoryType.txt"), 'w')
        self.assignKeywords()
        
    def clear(self):
        
        self.singlePageWiseMaxCount = 0
        self.singlePageWiseMaxCountProduct = 0
        self.singlePageWiseMaxCountProperty = 0
        self.singlePageWiseMaxCountOtherType = 0      
        
        for key in self.keyForProduct.keys():
            self.keyForProduct[key] = 0
            
        for key in self.keyForProperty.keys():
            self.keyForProperty[key] = 0
            
        for key in self.keyForOtherType.keys():
            self.keyForOtherType[key] = 0
            
        self.phonesMap = {}
            
    def assignKeywords(self):
        
        for key in self.productKeywords:
            self.singleKeyForProduct[key] = 0
            self.keyForProduct[key] = 0
            
        for key in self.propertyKeywords:
            self.singleKeyForProperty[key] = 0
            self.keyForProperty[key] = 0
            
        for key in self.otherTypes:
            self.singleKeyForOtherType[key] = 0
            self.keyForOtherType[key] = 0

    def clearSingle(self):
        
        for key in self.singleKeyForProduct.keys():
            self.singleKeyForProduct[key] = 0
            
        for key in self.singleKeyForProperty.keys():
            self.singleKeyForProperty[key] = 0
            
        for key in self.singleKeyForOtherType.keys():
            self.singleKeyForOtherType[key] = 0
        
    def getTagData(self, thisContent, stTag, endTag):
        
        lb = 0
        ub = 0
        
        lb = thisContent.find(stTag)
        
        if lb == -1:
            return ""
        
        ub = thisContent.find(endTag, lb + len(stTag))
        
        if ub == -1:
            return ""
        
        return thisContent[lb + len(stTag):ub].strip()
        
    def getData(self, thisLocation, stByte, enByte):
        
        inFile = open(thisLocation, 'rb')        
        inFile.seek(stByte-1)
        data = inFile.read(enByte-stByte+1)
        inFile.close()
        
        return data
    
    def processContent(self, htmlData):
        
        #print htmlData
        
        lbIDX = 0
        ubIDX = 0
        lastUBIDX = 0
        strData = ""
        self.clearSingle()
        htmlLength = len(htmlData)
              
        while True:
            
            if ubIDX < 0:
                break
            
            lastUBIDX = ubIDX
         
            lbIDX = htmlData.find(">", ubIDX + 1)            
            
            if lbIDX < 0:
                break

            ubIDX = htmlData.find("<", lbIDX + 1)
            
            if ubIDX < 0:
                break
            
            lastUBIDX = ubIDX
            
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
            
            lastUBIDX = ubIDX
            
            strData = htmlData[lbIDX+1:ubIDX].lower()
            strData = strData.replace("&nbsp;", "").strip()
            
            if len(strData) > 1:
                
                if strData.startswith("price"):
                    
                    wTokens = strData.split(" ")
                    
                    if len(wTokens) >= 2:
                        
                        if self.isCurrency(wTokens[1]):
                            #print strData
                            
                            token = "price"
                            
                            if self.singleKeyForProperty.has_key(token):
                                self.singleKeyForProperty[token] += 1
                            
                            if self.singleKeyForProduct.has_key(token):
                                self.singleKeyForProduct[token] += 1
                                
                            if self.keyForProperty.has_key(token):
                                self.keyForProperty[token] += 1
                            
                            if self.keyForProduct.has_key(token):
                                self.keyForProduct[token] += 1
                            
                    continue                   
                
                dataTokens = strData.split(" ")
                                                
                for token in dataTokens:
                    
                    token = token.strip()
                    
                    if len(token) > 1:
                        
                        if self.isCurrency(token):
                            #print token
                            token = "currency"   
                                                
                        if token == "price":
                            continue
                        
                        #print token
                        
                        if self.singleKeyForProperty.has_key(token):
                            self.singleKeyForProperty[token] += 1
                            
                        if self.singleKeyForProduct.has_key(token):
                            self.singleKeyForProduct[token] += 1
                            
                        if self.singleKeyForOtherType.has_key(token):
                            self.singleKeyForOtherType[token] += 1
                        
                        if self.keyForProperty.has_key(token):
                            self.keyForProperty[token] += 1
                            
                        if self.keyForProduct.has_key(token):
                            self.keyForProduct[token] += 1
                            
                        if self.keyForOtherType.has_key(token):
                            self.keyForOtherType[token] += 1
                            
                            
    def isCurrency(self, thisStr):
        
        if thisStr.startswith(",") or thisStr.endswith(","):
            return False
        
        if thisStr.startswith(".") or thisStr.endswith("."):
            return False
        
        if thisStr.find(",") == -1:
            if thisStr.find(".") == -1:
                return False              
        
        for ch in thisStr:
            if ch == "," or ch == "." or ch.isdigit():
                continue
            else:
                return False
            
        return True

    def saveURLInfo(self, strURL, singlePageMaxFre, singlePagePhoneKeywordInfo):
        
        strData = "\n\t<URL_INFO>"
        strData += "\n\t\t<URL>" + strURL.strip() + "</URL>"
        strData += "\n\t\t<PHONE_KEYWORD_INFO>\n\t\t\t" + singlePagePhoneKeywordInfo + "\n\t\t</PHONE_KEYWORD_INFO>";
                
        strKeys = ""
        strFre = ""
        maxProductFre = 0
        maxPropertyFre = 0
        maxOtherType = 0
        maxofAll = singlePageMaxFre
        
        allKeys = self.singleKeyForProperty.keys()
        
        for i in range(len(allKeys)):
            
            if self.singleKeyForProperty[allKeys[i]] == 0:
                continue
            
            if i != 0:
                strFre += "#"
                strKeys += "#"
                
            strKeys += allKeys[i]
            strFre += str(self.singleKeyForProperty[allKeys[i]])
            
            if maxPropertyFre < self.singleKeyForProperty[allKeys[i]]:
                maxPropertyFre = self.singleKeyForProperty[allKeys[i]]
        
        if maxofAll < maxPropertyFre:
            maxofAll = maxPropertyFre
        
        strData += "\n\t\t<PROPERTY_KEYWORDS>"
        strData += "\n\t\t\t<KEYWORDS>" + strKeys + "</KEYWORDS>"
        strData += "\n\t\t\t<FREQUENCIES>" + strFre + "</FREQUENCIES>"
        strData += "\n\t\t</PROPERTY_KEYWORDS>"
        
        strKeys = ""
        strFre = ""
        allKeys = self.singleKeyForProduct.keys()
        
        for i in range(len(allKeys)):
            
            if self.singleKeyForProduct[allKeys[i]] == 0:
                continue
            
            if i != 0:
                strFre += "#"
                strKeys += "#"
                
            strKeys += allKeys[i]
            strFre += str(self.singleKeyForProduct[allKeys[i]])
            
            if maxProductFre < self.singleKeyForProduct[allKeys[i]]:
                maxProductFre = self.singleKeyForProduct[allKeys[i]]
                    
        if maxofAll < maxProductFre:
            maxofAll = maxProductFre
                
        strData += "\n\t\t<PRODUCT_KEYWORDS>"
        strData += "\n\t\t\t<KEYWORDS>" + strKeys + "</KEYWORDS>"
        strData += "\n\t\t\t<FREQUENCIES>" + strFre + "</FREQUENCIES>"
        strData += "\n\t\t</PRODUCT_KEYWORDS>"
        
        strKeys = ""
        strFre = ""
        allKeys = self.singleKeyForOtherType.keys()
        
        for i in range(len(allKeys)):
            
            if self.singleKeyForOtherType[allKeys[i]] == 0:
                continue
            
            if i != 0:
                strFre += "#"
                strKeys += "#"
                
            strKeys += allKeys[i]
            strFre += str(self.singleKeyForOtherType[allKeys[i]])
                    
        if maxOtherType < self.singleKeyForOtherType[allKeys[i]]:
            maxOtherType = self.singleKeyForOtherType[allKeys[i]]
            
        if maxofAll < maxOtherType:
            maxofAll = maxOtherType
                   
        if singlePageMaxFre >= maxofAll:
            self.singlePageWiseMaxCount += 1
        elif maxPropertyFre >= maxofAll:
            self.singlePageWiseMaxCountProperty += 1
        elif maxProductFre >= maxofAll:
            self.singlePageWiseMaxCountProduct += 1
        elif maxOtherType >= maxofAll:
            self.singlePageWiseMaxCountOtherType += 1
                                    
        strData += "\n\t\t<OTHER_TYPE_KEYWORDS>"
        strData += "\n\t\t\t<KEYWORDS>" + strKeys + "</KEYWORDS>"
        strData += "\n\t\t\t<FREQUENCIES>" + strFre + "</FREQUENCIES>"
        strData += "\n\t\t</OTHER_TYPE_KEYWORDS>"
        
        strData += "\n\t</URL_INFO>\n"
                
        self.fileDirectoryTypeSinglePage.write(strData)
        self.fileDirectoryTypeSinglePage.flush()
        
    def getMaxPhoneFreFromURLInfo(self, thisData):
        
        wTokens = thisData.split("#")
        maxPhoneFre = 0
        tempFre = 0
        
        if len(wTokens) > 0:
            
            for token in wTokens:
                
                tempFre = 0
                
                try:
                    tempFre = int(token)
                except:
                    tempFre = 0
                
                if tempFre > maxPhoneFre:
                    maxPhoneFre = tempFre
                    
        return maxPhoneFre
        
                            
    def processURL(self, thisURLInfo):
        
        singlePageMaxPhoneFre = self.getMaxPhoneFreFromURLInfo(self.getTagData(thisURLInfo, "<FREQUENCIES>", "</FREQUENCIES>"))
        singlePagePhoneKeywordInfo = self.getTagData(thisURLInfo, "<KEYWORD_INFO>", "</KEYWORD_INFO>")
        strByteInfo = self.getTagData(thisURLInfo, "<BYTE_INFO>", "</BYTE_INFO>")
        self.parsePhoneFre(thisURLInfo)
        wTokens = strByteInfo.split(" ")
        contentFileLoc = os.path.join(self.inputDirectory, "WebSite/Content/" + wTokens[0] + ".CONTENT")
        strURL = self.getData(contentFileLoc, long(wTokens[1]), long(wTokens[2])).strip()
        strContent = self.getData(contentFileLoc, long(wTokens[3]), long(wTokens[4]))
        
        self.processContent(strContent)
        self.saveURLInfo(strURL, singlePageMaxPhoneFre, singlePagePhoneKeywordInfo)

        
    def processDataFoundURL(self, stByte, enByte, pageLimit):
        
        self.fileDirectoryTypeSinglePage.write("\n<PROFILE>")
        self.fileDirectoryTypeSinglePage.write("\n\t<HOST>"+self.currentHostName+"</HOST>")
        self.fileDirectoryTypeSinglePage.flush()
        
        dataFoundURL = os.path.join(self.outputDirectory, "DataFoundURL.xml")
        
        fileDataFoundURL = open(dataFoundURL, 'rb')
        
        fileDataFoundURL.seek(stByte)
        
        line = ""
        pageCount = 0
        strURLInfo = ""
        
        while True:
            
            line = fileDataFoundURL.readline().strip()
            
            if len(line) == 0 and fileDataFoundURL.tell() == os.path.getsize(dataFoundURL):
                break
            
            if line.find("</PROFILE>") != -1:                
                break
            
            strURLInfo += line
            
            if line.startswith("</URL_INFO>"):
                
                self.processURL(strURLInfo)
                strURLInfo = ""
                
                pageCount += 1
                
                if pageCount >= pageLimit:
                    break
               
        self.fileDirectoryTypeSinglePage.write("</PROFILE>\n")
        fileDataFoundURL.close()
        
    def saveProfileInfo(self, maxFrePhones, thisProfile):
        
        strData = "<PROFILE>"
        strData += "\n\t<HOST_NAME>" + self.currentHostName + "<HOST_NAME>"
        strData += "\n\t<INPUT_DIRECTORY>" + self.getTagData(thisProfile, "<INPUT_DIRECTORY>", "</INPUT_DIRECTORY>") + "</INPUT_DIRECTORY>"
        strData += "\n\t<OUTPUT_DIRECTORY>" + self.getTagData(thisProfile, "<OUTPUT_DIRECTORY>", "</OUTPUT_DIRECTORY>") + "</OUTPUT_DIRECTORY>"
        strData += "\n\t<TOTAL_PAGES>" + self.getTagData(thisProfile, "<TOTAL_PAGES>", "</TOTAL_PAGES>") + "</TOTAL_PAGES>"
        strData += "\n\t<TOTAL_PAGES_DATA_FOUND>" + self.getTagData(thisProfile, "<TOTAL_PAGES_DATA_FOUND>", "</TOTAL_PAGES_DATA_FOUND>") + "</TOTAL_PAGES_DATA_FOUND>"
        strData += "\n\t<START_BYTE>" + self.getTagData(thisProfile, "<START_BYTE>", "</START_BYTE>") + "</START_BYTE>"
        strData += "\n\t<END_BYTE>" + self.getTagData(thisProfile, "<END_BYTE>", "</END_BYTE>") + "</END_BYTE>"
                
        strKeys = ""
        strFre = ""
        maxFreProduct = 0
        maxFreProperty = 0
        maxFreOther = 0
        
        allKeys = self.keyForProperty.keys()
        
        for i in range(len(allKeys)):
            
            if self.keyForProperty[allKeys[i]] == 0:
                continue
            
            if i != 0:
                strFre += "#"
                strKeys += "#"
                
            strKeys += allKeys[i]
            strFre += str(self.keyForProperty[allKeys[i]])
            
            if self.keyForProperty[allKeys[i]] > maxFreProperty:
                maxFreProperty = self.keyForProperty[allKeys[i]]
                
        
        strData += "\n\t<PROPERTY_KEYWORDS>"
        strData += "\n\t\t<KEYWORDS>" + strKeys + "</KEYWORDS>"
        strData += "\n\t\t<FREQUENCIES>" + strFre + "</FREQUENCIES>"
        strData += "\n\t</PROPERTY_KEYWORDS>"
        
        strKeys = ""
        strFre = ""
        allKeys = self.keyForProduct.keys()
        
        for i in range(len(allKeys)):
            
            if self.keyForProduct[allKeys[i]] == 0:
                continue
            
            if i != 0:
                strFre += "#"
                strKeys += "#"
                
            strKeys += allKeys[i]
            strFre += str(self.keyForProduct[allKeys[i]])
            
            if self.keyForProduct[allKeys[i]] > maxFreProduct:
                maxFreProduct = self.keyForProduct[allKeys[i]]               

        strData += "\n\t<PRODUCT_KEYWORDS>"
        strData += "\n\t\t<KEYWORDS>" + strKeys + "</KEYWORDS>"
        strData += "\n\t\t<FREQUENCIES>" + strFre + "</FREQUENCIES>"
        strData += "\n\t</PRODUCT_KEYWORDS>"
        
        strKeys = ""
        strFre = ""
        allKeys = self.keyForOtherType.keys()
        
        for i in range(len(allKeys)):
            
            if self.keyForOtherType[allKeys[i]] == 0:
                continue
            
            if i != 0:
                strFre += "#"
                strKeys += "#"
                
            strKeys += allKeys[i]
            strFre += str(self.keyForOtherType[allKeys[i]])
            
            if self.keyForOtherType[allKeys[i]] > maxFreOther:
                maxFreOther = self.keyForOtherType[allKeys[i]]                
        
        strData += "\n\t<OTHER_KEYWORDS>"
        strData += "\n\t\t<KEYWORDS>" + strKeys + "</KEYWORDS>"
        strData += "\n\t\t<FREQUENCIES>" + strFre + "</FREQUENCIES>"
        strData += "\n\t</OTHER_KEYWORDS>"
    
        strKeys = ""
        strFre = ""
        allKeys = self.phonesMap.keys()
        
        for i in range(len(allKeys)):
            
            if self.phonesMap[allKeys[i]] == 0:
                continue
            
            if i != 0:
                strFre += "#"
                strKeys += "#"
                
            strKeys += allKeys[i]
            strFre += str(self.phonesMap[allKeys[i]])           

        strData += "\n\t<PHONE_KEYWORDS>"
        strData += "\n\t\t<KEYWORDS>" + strKeys + "</KEYWORDS>"
        strData += "\n\t\t<FREQUENCIES>" + strFre + "</FREQUENCIES>"
        strData += "\n\t</PHONE_KEYWORDS>"    
            
        dirType = ""
        
        maxFreProduct = self.keyForProduct['price']
        
        if maxFreProduct < self.keyForProduct['currency']:
            maxFreProduct = self.keyForProduct['currency']
            
        maxFreProperty = self.keyForProperty['price']
        
        if maxFreProperty < self.keyForProperty['currency']:
            maxFreProperty = self.keyForProperty['currency']
        
        print "maxFreProduct: ", maxFreProduct
        print "maxFreProperty: ", maxFreProperty
        print "maxFrePhones: ", maxFrePhones
        
        if maxFreProduct > maxFrePhones:
            dirType = "PRODUCT"
        elif maxFreProperty > maxFrePhones:
            dirType = "PRODUCT"
        elif maxFreOther > maxFrePhones:
            dirType = "OTHER"
        else:
            dirType = "Business Directory"
            #self.fileFilteredBusinessDirectory.write(self.currentHostName+"\n")
            #self.fileFilteredBusinessDirectory.flush()
        
        strData += "\n\t<TYPE>" + dirType + "</TYPE>"
        
        #self.singlePageWiseMaxCount = 0
        #self.singlePageWiseMaxCountProduct = 0
        #self.singlePageWiseMaxCountProperty = 0
        #self.singlePageWiseMaxCountOtherType = 0
        
        maxOfAllFinal = self.singlePageWiseMaxCount
        
        if maxOfAllFinal < self.singlePageWiseMaxCountProduct:
            maxOfAllFinal = self.singlePageWiseMaxCountProduct
            
        if maxOfAllFinal < self.singlePageWiseMaxCountProperty:
            maxOfAllFinal = self.singlePageWiseMaxCountProperty
            
        if maxOfAllFinal < self.singlePageWiseMaxCountOtherType:
            maxOfAllFinal = self.singlePageWiseMaxCountOtherType
        
        dirType = ""
        
        if self.singlePageWiseMaxCount >= maxOfAllFinal:
            dirType = "Business Directory"
        elif self.singlePageWiseMaxCountProperty >= maxOfAllFinal:
            dirType = "Property"
        elif self.singlePageWiseMaxCountProduct >= maxOfAllFinal:
            dirType = "Product"
        elif self.singlePageWiseMaxCountOtherType >= maxOfAllFinal:
            dirType = "Other"

        strData += "\n\t<SINGLE_PAGE_ANALYSIS_TYPE>" + dirType + "</SINGLE_PAGE_ANALYSIS_TYPE>"
        
        strData += "\n</PROFILE>\n"
                
        self.fileFilteredBusinessDirectory.write(self.currentHostName +"##"+ dirType +"\n")
        self.fileFilteredBusinessDirectory.flush()
        self.fileDirectroyType.write(strData)
        self.fileDirectroyType.flush()
        
    def parsePhoneFre(self, thisURLInfo):
        
        strKeywordsContent = self.getTagData(thisURLInfo, "<KEYWORD_INFO>", "</KEYWORD_INFO>")
        strFre = self.getTagData(strKeywordsContent, "<FREQUENCIES>", "</FREQUENCIES>")
        strKeys = self.getTagData(strKeywordsContent, "<KEYWORDS>", "</KEYWORDS>")
        
        if len(strFre.strip()) != 0:
 
            wFre = strFre.split("#")
            wKeys = strKeys.split("#")
            
            for i in range(len(wFre)):
                
                iFre = int(wFre[i])
                
                if self.phonesMap.has_key(wKeys[i]):
                    self.phonesMap[wKeys[i]] += iFre
                else:
                    self.phonesMap[wKeys[i]] = 0      
            
        strKeywordsContent = self.getTagData(thisURLInfo, "<KEYWORD_IN_TAG>", "</KEYWORD_IN_TAG>")
        strFre = self.getTagData(strKeywordsContent, "<FREQUENCIES>", "</FREQUENCIES>")
        strKeys = self.getTagData(strKeywordsContent, "<KEYWORDS>", "</KEYWORDS>")

        if len(strFre.strip()) != 0:
 
            wFre = strFre.split("#")
            wKeys = strKeys.split("#")
            
            for i in range(len(wFre)):
                
                iFre = int(wFre[i])
                
                if self.phonesMap.has_key(wKeys[i]):
                    self.phonesMap[wKeys[i]] += iFre
                else:
                    self.phonesMap[wKeys[i]] = 0

    def getMaxPhone(self):
        
        maxPhone = 0
        
        for key in self.phonesMap.keys():
            
            if self.phonesMap[key] > maxPhone:
                maxPhone = self.phonesMap[key]
                
        return maxPhone            
        
    def processProfile(self, thisProfile):
                
        stByte = long(self.getTagData(thisProfile, "<START_BYTE>", "</START_BYTE>"))
        enByte = long(self.getTagData(thisProfile, "<END_BYTE>", "</END_BYTE>"))
        self.currentHostName = self.getTagData(thisProfile, "<URL>", "</URL>")
        self.clear()
        
        print "Now Processing Host: ", self.currentHostName
        
        self.processDataFoundURL(stByte, enByte, 1000)
        maxPhone = self.getMaxPhone()
        self.saveProfileInfo(maxPhone, thisProfile)
        
        print "Processed Host: ", self.currentHostName
        
    def detect(self):

        sortedDirList = os.path.join(self.outputDirectory, "DirectoryListSortedByPHONE.xml")
        
        fileSortedDirList = open(sortedDirList, 'r')
        
        line = ""
        strProfile = ""
        
        while True:
            
            line = fileSortedDirList.readline()
            
            if len(line.strip()) == 0:
                break
            
            strProfile += line
            
            if line.startswith("</PROFILE>"):
                
                totalPhones = int(self.getTagData(strProfile, "<PHONE>", "</PHONE>"))
        
                if totalPhones < 100:
                    break
                       
                self.processProfile(strProfile)
                strProfile = ""
                
        fileSortedDirList.close()
        
if __name__ == "__main__":
    
    #inFile = open(r"F:\OfficeWork\Development\BusinessSearch\Working\Python Scripts\FetchedData.html", "r")
    typeDetector = TypeDetector(r"\\192.168.1.68\SATopBusinessDirectory\HostData", r"C:\SATopBusinessDirectory\BusinessSearch\Data\DirectoryDetectorData")
    typeDetector.detect()
    #typeDetector.processContent(inFile.read())   
        
        
        
        
        
        
