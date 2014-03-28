import os
import sys

class RemoveHostWithQmark:

    def __init__(self, fileExt = ""):
        self.fileExt = fileExt

    def remove(self, thisFolder = os.getcwd()):
        
        for fileName in os.listdir(thisFolder):
            
            if fileName.endswith(self.fileExt):
            
                fileName = os.path.join(thisFolder, fileName)
                
                print "Now Processing: ", fileName
                
                cFileBackupName = fileName + ".backup"
                
                os.rename(fileName, cFileBackupName)
                
                cFileBackup = open(cFileBackupName, "r")
                cFile = open(fileName, "w")            
                
                for hostName in cFileBackup.readlines():                
                    if hostName.find("?") == -1:
                        cFile.write(hostName)
                
                cFile.close()
                cFileBackup.close()
                os.remove(cFileBackupName)
                
                print "File Processed: ", fileName
            

if __name__ == "__main__":
    
    removeHostWithQmark = RemoveHostWithQmark("HostSeen")
    removeHostWithQmark.remove()
