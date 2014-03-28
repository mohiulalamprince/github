import os
import glob

file_list = os.listdir("O:/business-directory/HostData/WebSite/LinkDB")

for file in file_list:
   if (file.endswith(".tar")):
      pass
   else:
      print file


