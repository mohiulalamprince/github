import os

#command  = "tasklist /v /fi \"IMAGENAME eq " + processName + "\"";
command  = "tasklist /v /fi \"IMAGENAME eq vlc.exe \"";
f = os.popen(command)
print len(f.readlines())
