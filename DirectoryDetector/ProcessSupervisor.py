import os
import threading

class ProcessSupervisor(threading.Thread):
    
    def __inti_(self):
        
        threading.Thread.__init__(self)
        self.applicationLocation = [""]
    
    def runCommand(self, thisCommand):
        
        try:
            process = os.popen(thisCommand)
            output = process.readlines()
            print output
            return len(output)
        except:
            return 0
        
    def isProcessRunning(self, thisProcess):
        
        strCommand = command  = "tasklist /v /fi \"IMAGENAME eq " + thisProcess + "\""
        
        if self.runCommand(strCommand) >= 2:
            return True
        else:
            return False
        
    def runApplication(self, thisApplication):        
        self.runCommand(thisApplication)
        
    def run(self):
                
        while True:
            pass
            
        

if __name__ == '__main__':
    
    processSupervisor = ProcessSupervisor()
    processSupervisor.start()
    
    
    
    
    
    
    
    