import sys
import os
from Tkinter import *
from tkFileDialog import askopenfilename
from tkMessageBox import showinfo
from tkCommonDialog import Dialog
from DirectoryDetector import DirectoryDetector
from ProcessSupervisor import ProcessSupervisor
import shutil

class RunDirectoryDetector(Frame):

    def __init__(self):
        
        Frame.__init__(self)
        self.master.title("Business Search")
        self.grid(sticky=W+E+N+S)

        self.entryFileLoc = Entry(self, width=80)
        self.entryFileLoc.grid(row=0, column=0, rowspan=1, columnspan=5, padx=5, pady=5, sticky=W+E+N+S)   

        self.btnBrowse = Button(self, text="Browse", command=self.actionForBtnBrowse, width=10)
        self.btnBrowse.grid(row=0, column=6, rowspan=1, columnspan=2, padx=5, pady=5, sticky=W+E+N+S)
        
        self.varChkBox = BooleanVar()
        self.chkBoxRegExp = Checkbutton(self, text="Clean Previous Data", variable=self.varChkBox)
        self.chkBoxRegExp.grid(row=2, column=1, rowspan=1, columnspan=1, padx=5, pady=5, sticky=W+E+N+S)   

        self.btnGetData = Button(self, text="Start", command=self.actionForBtnGetData, width=5)
        self.btnGetData.grid(row=2, column=2, rowspan=1, columnspan=1, padx=5, pady=5, sticky=W+E+N+S)        

                
    def actionForBtnGetData(self):

        inputFile = self.entryFileLoc.get()

        if len(inputFile) == 0:
             showinfo("Error", "Please Select a Folder.")
             return

        self.start(inputFile)
        
        #showinfo("Info", "Data Fetched.")

    def askForDirectory(self, **options):
        return apply(FileChooser, (), options).show()
        
    def actionForBtnBrowse(self):
        
        strFolderLocation = self.askForDirectory().strip()

        if strFolderLocation == None or len(strFolderLocation) == 0:
            return

        if not strFolderLocation.endswith("HostData"):

            strFolderLocation = os.path.join(strFolderLocation, "HostData")

            if not os.path.exists(strFolderLocation):            
                showinfo("Error", "Please Select a HostData Folder.")
                return

        if strFolderLocation != None and len(strFolderLocation) != 0:            
            self.entryFileLoc.delete(0, END)
            self.entryFileLoc.insert(0, strFolderLocation)
            
            
    def isProcessFinished(self, fileLocation):
        
        if not os.path.exists(fileLocation):
            return False
        
        inFile = open(fileLocation, 'r')
        
        statusMsg = inFile.read().strip()
        
        inFile.close()
        
        if statusMsg.lower().startswith("finished"):
            return True
        
        return False       
        
    def start(self, inputFolder):
        
        self.master.withdraw()       
        workingDir = "../../"
        processSupervisor = ProcessSupervisor()
        
        if self.varChkBox.get():
            print "Now Deleteing Previous Data."
            os.system("call " + os.path.join(workingDir, "Reset.bat"))
        
        print "Now Writing Crawled Data Location."
        confFile = open(os.path.join(workingDir, "Conf/Config.xml"), 'w')
        confFile.write("<BUSINESS_SEARCH>\n\t<CRAWLED_DATA_LOCATION>\n\t\t" + str(inputFolder) + "\n\t</CRAWLED_DATA_LOCATION>\n</BUSINESS_SEARCH>\n" )
        confFile.close()        
                
        print "Directory Detector Starting ..."
        directoryDetector = DirectoryDetector(inputFolder, os.path.join(workingDir, "Data"))
        directoryDetector.detect()

        """
        print "AnchorText Indentifier Starting ..."
        
        os.system("call RunAnchorTextIdentifier.bat")
        
        if not self.isProcessFinished(os.path.join(workingDir, "Source/AnchorTextIdentifier/STATUS.txt")):
            showinfo("Error", "Anchor Text Identifier Not Successfully Finished.\nYou Have to Complete This Process Manually.")
            sys.exit(1)
            return
        
        print "AnchorText Indentifier Finished."

    
        
        print "SingleProfileParser Starting ..."
        
        os.system("call RunSingleProfileParser.bat")
        
        if not self.isProcessFinished(os.path.join(workingDir, "Source/ProfileParser/SingleProfileParser/STATUS.txt")):
            showinfo("Error", "Single Profile Parser Not Successfully Finished.\nYou Have to Complete This Process Manually.")
            sys.exit(2)
            return
        
        print "Single Profile Parser Finished."
                
        print "Multiple Profile Parser Starting ..."
        
        os.system("call RunMultipleProfileParser.bat")
        
        if not self.isProcessFinished(os.path.join(workingDir, "Source/ProfileParser/MultipleProfileParser/STATUS.txt")):
            showinfo("Error", "Multiple Profile Parser Not Successfully Finished.\nYou Have to Complete This Process Manually.")
            sys.exit(3)
            return
        
        print "Multiple Profile Parsing Finished."

        """

        print "Profile Parser Starting ..."
        
        #os.system("call RunProfileParser.bat")
        
        #if not self.isProcessFinished(os.path.join(workingDir, "Source/ProfileParser/ProfileParser/STATUS.txt")):
        #    showinfo("Error", "Profile Parser Not Successfully Finished.\nYou Have to Complete This Process Manually.")
        #    sys.exit(1)
        #    return
        
        #print "Profile Parsing Finished."
        
        showinfo("Info", "Directory Detector Successfully Finished.")
        sys.exit(0)                
              
class FileChooser(Dialog):

    command = "tk_chooseDirectory"

    def _fixresult(self, widget, result):
        if result:
            self.options["initialdir"] = result
        self.directory = result
        return result

if __name__ == "__main__":
    
    getDataGUI = RunDirectoryDetector()
    getDataGUI.mainloop()

            
