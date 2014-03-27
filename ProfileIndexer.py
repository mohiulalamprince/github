
class ProfileIndexer():

    def __init__(self, inputFile, outputDir, baseStTag, baseEnTag):

        self.inputFile = inputFile
        self.outputDir = outputDir
        self.baseStartTag = baseStTag
        self.baseEndTag = baseEnTag

    def getTagContent(self, content, stTag, enTag):

        tagContent = ""
        lb = 0
        lb = content.find(stTag)

        if lb==-1:
            return ""

        ub = content.find(enTag)
        return content[lb+len(stTag):ub].strip(' ')

    def saveInfo(self, strContent):

        lb = os.path.getsize(self.contentFileLocation.name) + 1
        self.contentFileLocation.write(strContent+"\n")
        self.contentFileLocation.flush()
        ub = os.path.getsize(self.profileUnq.name)
        self.indexFileLocation.write(+str(lb) +" "+ str(ub) +"\n")
        self.indexFileLocation.flush()     

    def runProfileIndexer(self):

        if not os.path.exists(self.inputFile):
            print "Input File Not Found: ", self.inputFile
            return

        if not os.path.exists(self.outputDir):
            print "Output Directory Not Found: ", self.outputDir
            return

                
        