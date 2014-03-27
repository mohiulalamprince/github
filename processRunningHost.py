import os
import time
import sys


class processRunningHost():
    def __init__(self,dir,h):
        self.defautlpath=dir
        self.host=h
        #self.currentDir="D:/OfficeWork/Development/WebCrawler/Working/testCode/processRunningHostofv0.6.0/DownloadedLinkPath"
        self.currentDir="F:/HostData/WebSite/LinkDB/www.searchengine.co.za/DownloadedLinkPath"

    def getData(self, fileLoc, stByte, enByte):
        if not os.path.exists(fileLoc):
            return None
        
        #self.lock.acquire();
        currentFile = open(fileLoc, 'r')
        if stByte > 0:
            stByte -= 1    
        currentFile.seek(stByte)
        fileData = currentFile.read(enByte-stByte)
        currentFile.close()
        #self.lock.release();
        return fileData
        
    def processHost(self):
        print "Path ",self.defautlpath
        print "Host ",self.host
        if not os.path.exists(self.defautlpath):
            return
        dirList=[]
        dirList=os.listdir(self.currentDir)
        fContent=open(self.host+".CONTENT",'w')
        fIndex=open(self.host+".INDEX",'w')
        name=self.host+".CONTENT"
        #dirList.sort()
        fIndex.write("<"+self.host+">\n")
        i=0
        ii=0
        for dir in dirList:
            if dir.endswith(".linkPath"):
                i=i+1
                tDir=self.currentDir+"/"+dir
                print "processing tDir ",tDir
                #tDir=self.currentDir+"/10.linkPath"
                f=open(tDir,'r')
                tmp=self.defautlpath+"/WebSite/Content/"
                #print fileLoc
                ii=0
                for line in f.readlines():
                    #ii=ii+1
                    #if ii>=5:
                    #    break
                    line=line.strip()
                    #print "===",line
                    w=[]
                    w=line.split(' ')
                    wLen=len(w)
                    try:
                        fileLoc=tmp+w[wLen-5]+".CONTENT"
                        #print fileLoc
                        #print w[wLen-5]," ",w[wLen-4]," ",w[wLen-3]," ",w[wLen-2]," ",w[wLen-1]
                        #print "Url: ",w[wLen-4]," ",w[wLen-3]
                        url=self.getData(fileLoc,int(w[wLen-4]),int(w[wLen-3]))
                        #print "URL: ",url
                        #print "Content: ",w[wLen-2]," ",w[wLen-1]
                        page=self.getData(fileLoc,int(w[wLen-2]),int(w[wLen-1]))
                        #print len(page)
                        #print page
                        ust=os.path.getsize(name)+1
                        fContent.write(str(url))
                        fContent.flush()
                        ued=os.path.getsize(str(name))
                        cst=ued+1
                        fContent.write(page)
                        fContent.flush()
                        ced=os.path.getsize(name)
                        s=" "+str(ust)+" "+str(ued)+" "+str(cst)+" "+str(ced)+"\n"
                        fIndex.write(s)
                        fIndex.flush()
                    except:
                        pass
                f.close()
                #if i>=2:
                #    break
        fIndex.write("<"+self.host+"/>\n")
        fContent.close()
        fIndex.close()
                    
        


if __name__=='__main__':
    o=processRunningHost("F:/HostData","www.searchengine.co.za")
    o.processHost()
    print "Ok"
