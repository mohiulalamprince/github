import os
import sys
import shutil

linkDBLocation = r"C:\LinkDB"

for fileName in os.listdir(linkDBLocation):
    if os.path.isdir(os.path.join(linkDBLocation, fileName)):
        lnkExtDir = os.path.join(linkDBLocation, fileName, "LinkExtractionBlock")

        if os.path.exists(lnkExtDir):
            print 'now removing : ', lnkExtDir
            shutil.rmtree(lnkExtDir)
        else:
            print "Folder Not Found: ", lnkExtDir
