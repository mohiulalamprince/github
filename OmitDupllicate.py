import os
import time

class OmitDuplicate:

    def __init__(self):
        
        self.companiesName = []
        self.companiesAddress = []
        self.companiesType = []
        self.profileUnq = None
        self.profileUnqIndex = None
        self.profileDuplicate = None

    def isDuplicate(self, strName, strType, strAddress):

        for i in range(len(self.companiesName)):
            if self.companiesName[i] == strName:
                if self.companiesAddress[i]==strAddress:
                    if self.companiesType[i]==strType:
                        return True
        return False                        

        
    def isDuplicate1(self, strName, strType, strAddress):

        if strName in self.companiesName:
            idx = self.companiesName.index(strName)
        else:
            return False

        if len(strType)!=0 and self.companiesType[idx]!=strType:
            return False

        if len(strAddress)!=0 and self.companiesAddress[idx]!=strAddress:
            return False          

        return True

    def getTagContent(self, content, stTag, enTag):

        tagContent = ""
        lb = 0
        lb = content.find(stTag)

        if lb==-1:
            return ""

        ub = content.find(enTag)
        return content[lb+len(stTag):ub].strip(' ')

    def saveInfo(self, strContent):

        lb = os.path.getsize(self.profileUnq.name) + 1
        self.profileUnq.write(strContent+"\n")
        self.profileUnq.flush()
        ub = os.path.getsize(self.profileUnq.name)
        self.profileUnqIndex.write(str(lb) +" "+ str(ub) +"\n")
        self.profileUnqIndex.flush()      
        
    def parseContent(self, strContent):

#        print strContent

        tagName = self.getTagContent(strContent, "<COMPANY>", "</COMPANY>")
        tagType = self.getTagContent(strContent, "<TYPE>", "</TYPE>")
        tagAddress = self.getTagContent(strContent, "<ADDRESS>", "</ADDRESS>")

        if self.isDuplicate(tagName, tagType, tagAddress):
            print "DUPLICATE: ", tagName
            self.profileDuplicate.write(strContent)
            self.profileDuplicate.flush()
            print strContent
            #time.sleep(5)
            return

        self.saveInfo(strContent)
        self.companiesName.append(tagName)
        self.companiesAddress.append(tagAddress)
        self.companiesType.append(tagType)

    def omitDuplicate(self, fileNameContent, fileNameIndex):

        inContentFile = open(fileNameContent, 'r')
        inIndexFile = open(fileNameIndex, 'r')
        self.profileUnq = open("E:\SearchEngine_11-10-2010\Unique Profiles/BusinessProfileUnique.xml", 'w')
        self.profileUnqIndex = open("E:\SearchEngine_11-10-2010\Unique Profiles/BusinessProfileUnique.index", 'w')
        self.profileDuplicate = open("E:\SearchEngine_11-10-2010\Unique Profiles/BusinessProfileDuplicate.xml", 'w')

        for line in inIndexFile.readlines():

            tokens = line.split(' ')

            if len(tokens) < 2:
                continue

            inContentFile.seek(int(tokens[0])-1)
            self.parseContent(inContentFile.read(int(tokens[1])-int(tokens[0])+1))

        self.profileUnq.close()
        self.profileUnqIndex.close()


if __name__ == "__main__":

    omitDuplicate = OmitDuplicate()
    omitDuplicate.omitDuplicate("E:\SearchEngine_11-10-2010\XML Formatted Profiles\BusinessData.xml", "E:\SearchEngine_11-10-2010\XML Formatted Profiles\BusinessData.index")

        
        
        

    
        

        
