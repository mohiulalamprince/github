import os

total_download = 0
total_url = 0
total_http_request = 0
total_error = 0

FINISH_HOST_LIST = "O:/2013SA/HostConf/HostConf/finishHostList.txt"

with open(FINISH_HOST_LIST, "r") as file_pointer:
	for line in file_pointer:
		try:
			information = line.strip().split( )
			total_download += int(information[3].strip())
			total_url += int(information[5].strip())
			total_http_request += int(information[7].strip())
			total_error += int(information[9].strip())
		except:
			print "ERROR"

print str(total_download), str(total_url), str(total_http_request), str(total_error), str(total_error + total_download)