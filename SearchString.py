import os
import sys

def search(fileLoc, searchStr):

    print "\nNow Searching ... @: ", fileLoc
    inFile = open(fileLoc, "r")

    for line in inFile.readlines():
        if line.find(searchStr) != -1:
            print "\nFound @: ", fileLoc
            print "@ Line: ", line

    inFile.close()


def searchFolder(searchStr, fileExt = "", folderLoc=os.getcwd()):

    for fileName in os.listdir(folderLoc):
        
        if fileExt == "":
            search(os.path.join(folderLoc, fileName), searchStr)
        elif fileName.endswith(fileExt):
            search(os.path.join(folderLoc, fileName), searchStr)

    print "Folder Searched"

if __name__ == "__main__":

    folderName = "E:\\LinkDB\\www.ads.co.za\\www.ads.co.za\\NewLargestData\\HostData\\WebSite\LinkDB\\www.ads.co.za\\LinkExtractionBlock\\"
    searchStr = "18 2316299414 2316299413 2316299414 2316299413 1"
    searchFolder(searchStr, ".INDEX")
    
