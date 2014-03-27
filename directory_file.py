import os


class FileTree:

    fWrite = open("WRITE.txt","w")
    fWrite.close()
    
    def getTree(self, cFile, tab):

        cFile = cFile.strip()
        
        data = os.listdir(cFile)
        
        for directory in data:


            if not(os.path.isdir(cFile+"/"+directory)):  #if it's a file.
                fopen = open(cFile+"/"+directory,'r')
                
                self.fWrite.write(tab+'<'+directory.upper()+'>\n')

                for line in fopen.readlines():
                    self.fWrite.write(tab+' '+line)
                    
                fopen.close()
                
                self.fWrite.write('\n'+tab+'</'+directory.upper()+'>\n')
            else:                         #if it's a folder.
                self.fWrite.write(tab+'<'+directory.upper()+'>\n')
                ntab=tab+"  "
                self.getTree(cFile+"/"+directory,ntab)
                self.fWrite.write(tab+'</'+directory.upper()+'>\n')
                
    def openAnewFile(self, fileName):
        self.fWrite = open(fileName,"w")
    def getFileName(self):
        return self.fWrite.name

    def fileClose(self):
        self.fWrite.close()

    def getFileSize(self):
        self.fWrite.flush()
        return os.path.getsize(self.fWrite.name)

    def doCrawl(self, hostListFileLocation, inputLocation, outputLocation):
        
        nFWrite=open(outputLocation+"/"+"INDEX.TXT",'w')        #creating  index file.
        i=1
        j=2
        startByte = 0
        endByte=-1
        
        self.openAnewFile(outputLocation+"/"+"CONTAINER1.TXT")  #creating  Main container.
        fRead = open(hostListFileLocation,'r')
        
        for hostName in fRead.readlines():
            hostName=hostName.strip()
            self.getTree(inputLocation+hostName,"")
            startByte=endByte+1
            endByte=self.getFileSize()
            
            nFWrite.write("<INDEX NO="+ str(i) +">\n")
            nFWrite.write("  <HOST NAME>"+hostName+"</HOST NAME>\n")
            nFWrite.write("  <START_BYTE>"+ str(startByte) +"</START_BYTE>\n")
            nFWrite.write("  <END_BYTE>"+ str(endByte) +"</END_BYTE>\n")
            nFWrite.write("  <FILE_NAME>"+ self.getFileName() +"</FILE_NAME>\n")
            nFWrite.write("</INDEX>\n")
            nFWrite.flush()
            i += 1


            #if(fileTree.getFileSize()>1.073741824e+10):
            if(self.getFileSize()>100): #1.073741824e+10
                self.fileClose()
                #if(i<=len(hostList)):       # whether to creat a new container or not.
                self.openAnewFile(outputLocation+"/"+"CONTAINER"+ str(j) +".TXT")   #creating  Main containers.
                j += 1
                startByte = 0
                endByte=-1
        fRead.close()
        nFWrite.close()
        self.fileClose()

    
        
class Test:
    def __int__(self):
        print 'h'
        
if __name__ == "__main__":

    fileTree = FileTree()
    fileTree.doCrawl("F:\\test\\Host_List.txt","F:\\test\\","F:\\test\\")
    
