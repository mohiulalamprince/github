import os
import shutil
import tarfile
import sys
from Robustness import Robustness

###
# It works for writing a host information as an XML format.
###

def compare(xFileInfo, yFileInfo):    
    return xFileInfo.fileID - yFileInfo.fileID

class FileInfo:
    
    def __init__(self):
	
	self.fileID = 0
	self.fileExt = ""
	
    def getName(self):
	return str(self.fileID) + "." + self.fileExt

class LinkDb:
    
    indexFileNO=0
    indexNumber=0
    index=0
    containerNO=0
    where=0
    startByte=0
    endByte=0
    flag = False
    
    #fileName = ("Conf","ContentSeen","ContentUnseen","DifferentHost","UrlSeenBlock","DownloadedLinkPath","LinkExtractionBlock")
    fileName = ("Conf","UrlSeenBlock","DownloadedLinkPath")
    
    
	#summary of method : It wroks for padding of FinishedHostListLinkDBInfo file writing.
	#@param self
	#@param data : Some data to print.
	#@param maxValue : Number of space;
	#@return : Returns the string of spaces for padding.	
    def printWithPadding(self, data, maxValue):
        length = len(data)
        maxValue -= length
        
        x = ""
        for i in range(0, maxValue):
            x += ' '
        data = data + x
        
        return data
    
	#summary of method : It is the heart of this class. It writes the whole thing as an xml tree.
	#@param self
	#@param cFile : It is the current file or folder path.
	#@param tab : This is the tab/tabs added as string as the current contant depth.
	#@return : No return type.
    def getTree(self, cFile, tab):

        cFile = cFile.strip()
        
        data = os.listdir(cFile)     ##Containing all the file or foder list.
        
	
	# Sorting Files
	
        #array = []
        #textArray = []
        #text = ""
        #
        #for file in data:
        #    if (len(file) > 0 and file[0] >= '0' and file[0] <= '9'):
        #        number = int(file.split('.')[0])
        #        text = file.split('.')[1]
        #        array.append(number)
        #    else:
        #        textArray.append(file)
        #        
        #array.sort()
        #
        #data = []
        #for line in array:
        #    data.append(str(line)+ "." + text)
        #
        #for line in textArray:
        #    data.append(line)
	
	numberedFile = []
	textedFile = []
	
	for currentFile in data:	    
	    if len(currentFile) > 0 and currentFile[0] >= '0' and currentFile[0] <= '9':
		wTokens = currentFile.split('.')
		tempFileInfo = FileInfo()
		tempFileInfo.fileID = int(wTokens[0])
		tempFileInfo.fileExt = wTokens[1]
		numberedFile.append(tempFileInfo)
	    else:
		textedFile.append(currentFile)
		
	numberedFile.sort(cmp=compare)
	data = []
	
	for fileInfo in numberedFile:
	    data.append(fileInfo.getName())
	    
	for fileName in textedFile:
	    data.append(fileName)
	    
	#print "Total Files: ", len(data)
	
        for directory in data:
	    
	    #print "FileName: ", directory

            st=os.path.join(cFile,directory)
            
            # if it's not a folder.
            if not(os.path.isdir(st)):
                fopen = open(st,'r')
                self.fWrite.write(tab+'<'+directory.upper()+'>\n')
            
                for line in fopen.readlines():
                    line=line.strip()
                    self.fWrite.write(tab+"\t"+line+"\n")
                    
                fopen.close()
                
                self.fWrite.write(tab+'</'+directory.upper()+'>\n\n')
            else:                                                               #if it's a folder.
                flag=False
                for file in self.fileName:
                   if(cmp(file,directory)==0):
                    self.hostInfo=file
                    self.hostInfoStartbyte= self.getFileSize()
                    flag=True
                    self.nFWrite.write("\t<"+self.hostInfo.upper()+">\n")
                    self.nFWrite.write("\t\t<START_BYTE>"+ str(self.hostInfoStartbyte+1) +"</START_BYTE>\n")
                    
                self.fWrite.write(tab+'<'+directory.upper()+'>\n')
                ntab=tab+"\t"
                self.getTree(st,ntab)
                self.fWrite.write(tab+'</'+directory.upper()+'>\n\n')
                
                if(flag):
                    self.hostInfoEndbyte= self.getFileSize()
                    self.nFWrite.write("\t\t<END_BYTE>"+ str(self.hostInfoEndbyte) +"</END_BYTE>\n")
                    self.nFWrite.write("\t</"+self.hostInfo.upper()+">\n")
                    flag = False

	
	#summary of method : It reads the configuration files.
	#@param self
	#@param filePath : It is the path location of the conguration files.
	#@return : No return type.
    def readConfig(self, filePath):
        st=os.path.join(filePath,"ContainerConfig.txt")
        self.robustness = Robustness(st)
        fileData = self.robustness.read()
        self.where = int(self.robustness.getNthValue(fileData, 1))
        print "self.where: ", self.where
                
        st=os.path.join(filePath,"IndexConfig.txt")
        self.robustness.setPath(st)
        rtnValue=self.robustness.read()
        self.index=int(self.robustness.getNthValue(rtnValue, 1))
        self.indexFileNO=int(self.robustness.getNthValue(rtnValue, 2))
        print "self.indexFileNO : ", self.indexFileNO
        
	#summary of method : It opens a new container file.
	#@param self
	#@param fileName : Name of the current container.
	#@return : No return type.
    def openAnewFile(self, fileName):
        global fWrite
        self.fWrite = open(fileName,'a')
	
	#summary of method : It takes the current container name.
	#@param self
	#@return : It returns the current container name.
    def getFileName(self):
        return self.fWrite.name
	
	#summary of method : It closes the container file.
	#@param self
	#@return : No return type.
    def fileClose(self):
        self.fWrite.close()

	#summary of method : It takes the current file size of the container.
	#@param self
	#@return : It returns the current size of the container.
    def getFileSize(self):
        self.fWrite.flush()
        return os.path.getsize(self.fWrite.name)
		
	#summary of method : It cleans up the extract folder.
	#@param self
	#@param path : Location of the extract folder.
	#@return : No return type.
    def emptyExtract(self,path):
	
	try:
	    data = os.listdir(path)
	    for folder in data:
		folder=folder.strip()
		dirt=os.path.join(path,folder)
		shutil.rmtree(dirt)
	except:
	    print "Exception on epmtyExtract(): ", path
	    print "Exception: ", str(sys.exc_info())
	
	#summary of method : It extracts the tar file to the output location in extract folder.
	#@param self
	#@param hostPath : This is the path of hosts.
	#@param outputLocation : This is the output location.
	#@return : No return type.
    def extraction(self, hostName, outputLocation):
        
        if hostName.endswith(".tar"):
            tar = tarfile.open(hostName)
            st=os.path.join(outputLocation,"extract")                           # making extraction directory
            if not (os.path.exists(st)):
                os.mkdir(st)
                ##print "Yes directory has made."

            tar.extractall(st)                                                  # extracting
            tar.close()
            return st
        else:
            return hostName
    
	#summary of method : It writes the index file.
	#@param self
	#@param hostPath : This is the path of hosts.
	#@param hostName : This is the name of the hosts.
	#@return : No return type.
    def indexFileWrite(self,hostPath,hostName,outputLocation):
        
        ## writing the FinishedHostListLinkDBInfo.txt file.
        st=os.path.join(outputLocation,"INDEX"+str(self.indexFileNO)+".TXT")
        size=os.path.getsize(st)
        if(size==0):size =-1
        
        ##Truncation the .TAR extention from hostname
        if hostName.endswith(".tar"):
            hostName=hostName[0:len(hostName)-4]
        
        openFile=open(outputLocation+"\FinishedHostListLinkDBInfo.txt",'a')
        openFile.write("HOST:= " + self.printWithPadding(hostName, 35)+" " + "INDEX_NO:= " + self.printWithPadding(str(self.indexFileNO), 15) + " "+ "INDEX_START_BYTE:= " + self.printWithPadding(str(size+1), 15)+" ")
                
        self.nFWrite.write("<INDEX NO="+ str(self.indexNumber) +">\n")
        self.nFWrite.write("\t<HOST_NAME>"+hostName+"</HOST_NAME>\n")
        
        self.fWrite.write("<"+hostName+">\n\n")                                             ##writing Host name on container.
        self.getTree(hostPath,"\t")                                               #calling the getTree() function
        
	if (os.path.exists(outputLocation + "\\" + "extract")):
            self.emptyExtract(outputLocation + "\\" + "extract")
        
        self.startByte=self.endByte+1
        self.fWrite.write("</"+hostName+">\n\n")                                             ##writing Host name on container.
        self.endByte=self.getFileSize()
                
        self.nFWrite.write("\t<START_BYTE>"+ str(self.startByte) +"</START_BYTE>\n")
        self.nFWrite.write("\t<END_BYTE>"+ str(self.endByte) +"</END_BYTE>\n")
        ##self.nFWrite.write("\t<FILE_NAME>"+ self.getFileName() +"</FILE_NAME>\n")
        self.nFWrite.write("\t<FILE_NAME>"+"CONTAINER"+str(self.containerNO)+".TXT"+"</FILE_NAME>\n")
        self.nFWrite.write("</INDEX>\n")
        self.nFWrite.flush()
        
        ## writing and closing the FinishedHostListLinkDBInfo.txt file.
        size=os.path.getsize(st)
        openFile.write( "INDEX_END_BYTE:= " + self.printWithPadding(str(size), 15) +"\n")
        openFile.flush()
        openFile.close()
        
        ## index filesize chacking.
        if(os.path.getsize(st)>1024 * 1024 * 100):
            self.indexFileNO += 1
            st=os.path.join(outputLocation,"INDEX"+str(self.indexFileNO)+".TXT")
            self.nFWrite=open(st,'w')
            
        if(self.getFileSize()>1024 * 1024 * 1024 * 10):
            #  * close
            self.fileClose()
            if(hostName != None ):                                              # whether to creat a new container or not.
                ##print   self.indexNumber , len(hostName)

                self.containerNO = self.containerNO + 1
                st="CONTAINER"+ str(self.containerNO) +".TXT"
                st=os.path.join(outputLocation,st)
                self.openAnewFile(st)                                           #creating  Main containers  #  ** open  
                
            self.startByte = 0
            self.endByte = - 1                                                  # end for()loop
            
    #summary of method : It writes the new configuration file.
	#@param self
	#@param outputLocation : It is the location where the config files are kept.
	#@return : No retur type.
    def writeNewConfiguration(self,outputLocation):
        ## creating indexConfig file
        st=os.path.join(outputLocation,"IndexConfig.txt")
        fileOpen=open(st,'w')
        fileOpen.write((str(1)+" "+str(1)+"\n"))
        fileOpen.close()
        
        ## creating containerConfig file
        st=os.path.join(outputLocation,"ContainerConfig.txt")
        fileOpen=open(st,'w')
        fileOpen.write((str(1)+"\n"))
        fileOpen.close()
    
	#summary of method : It checks wheather the configuration files are there or not .
	#@param self
	#@param outputLocaton : It is the location where the config files are kept.
	#@return : No retur type.
    def checkConfiguration(self,outputLocation):
        st=os.path.join(outputLocation,"ContainerConfig.txt")
        if not(os.path.exists(st)):
            self.writeNewConfiguration(outputLocation)
            print "ContainerConfig.txt is not found.\n"
        st=os.path.join(outputLocation,"IndexConfig.txt")
        if not(os.path.exists(st)):
            print "IndexConfig.txt is not found.\n"
    

	#summary of method : It is the main method of this class 
	#@param self : 
	#@param hostListFileLocation  : 
	#@param maxValue
	#@return 
    def doCrawl(self, hostListFileLocation, inputLocation, outputLocation, step):
        
        print "LinkDB Crawling For Host: ", hostListFileLocation
        
        if (step == "restart" or step == "RESTART"):
            self.checkConfiguration(outputLocation)
        elif(step == "fresh_start" or step == "FRESH_START"):
            self.writeNewConfiguration(outputLocation)
        else:
            print "Check your spelling\n"
            return
               
        
        ## if the path exist or not
        st=os.path.join(inputLocation,hostListFileLocation)
        if not (os.path.exists(st)):
            print "The HostName does not exist\n"
            return
        
        self.readConfig( outputLocation)
        st=os.path.join(outputLocation,"INDEX"+str(self.indexFileNO)+".TXT")
        self.nFWrite=open(st,'a')                                               #creating  index file  ** open a file
        
        self.indexNumber=self.index
        self.containerNO=self.where
        
        st=os.path.join(outputLocation,"CONTAINER"+str(self.containerNO)+".TXT")
        
        self.openAnewFile(st)
        
        self.startByte = 0
        self.endByte=self.getFileSize()
        if(self.endByte==0):
            self.endByte=-1
        
        ## if it is a file
        if(hostListFileLocation.endswith(".txt")):
            
            fRead = open(hostListFileLocation,'r') #  ** open
            
            for hostName in fRead.readlines():                                  # start for()loop
                hostName=hostName.strip()
                print "http://" + hostName + "/"
                st=os.path.join(inputLocation,hostName)
                hostPath=self.extraction(st,outputLocation)                      # doing extraction if needed .
                print hostPath, " ", hostName, " ", outputLocation
                self.indexFileWrite(hostPath,hostName,outputLocation)
                self.indexNumber += 1
                # end for()loop
            fRead.close()   #  * close
        ## or it is a tar file or a normal folder
        else:
            hostName=hostListFileLocation
            st=os.path.join(inputLocation,hostName)
            hostPath=self.extraction(st,outputLocation)
            
            self.indexFileWrite(hostPath,hostName,outputLocation)
            self.indexNumber += 1
        print "I am here ...."
        
        ##writing ContainerConfig
        self.robustness.setPath(os.path.join(outputLocation, "ContainerConfig.txt"))
        self.robustness.write(str(self.containerNO)+"\n")
        
        ##writing indexFileConfig
        self.robustness.setPath(os.path.join(outputLocation, "IndexConfig.txt"))
        self.robustness.write(str(self.indexNumber)+" "+str(self.indexFileNO)+"\n")
        
        self.nFWrite.flush()
        self.nFWrite.close()#  * close
        self.fileClose() #  * main container close
        
class Test:
    def __int__(self):
        print 'h'
        
if __name__ == "__main__":

    linkDb = LinkDb()
    linkDb.doCrawl("www.hotelstuff.co.za.tar", r"E:\ReCrawlHostDataLargest\HostData\WebSite\LinkDB", r"E:\Output", "FRESH_START")
    ##for file
    ##linkDb.doCrawl("F:\crawler\HostList.txt","//192.168.1.68/NewLargestData/HostData/WebSite/LinkDB/","F:\crawler", "RESTART")
    ##for directory
    #linkDb.doCrawl("www.2ko.co.za","F:\crawler","F:\crawler","FRESH_START")
    ##for tar file
    ##linkDb.doCrawl("F:\crawler\HostList.txt","F:\crawler","F:\crawler","RESTART")








