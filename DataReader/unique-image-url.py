import os
from time import gmtime, strftime

PATH = "H:/image_url_nelly"
file_pointer_writer = open(os.path.join(PATH, "out.txt"), "w")

print str(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
with open(os.path.join(PATH, "image_url_list.txt"), "r") as file_pointer:
	lines = file_pointer.readlines()

print "Loading ... " + str(len(lines)) + " lines .... ... ..   [Done]"
print str(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))

url_set =  set(["abc"])

for line in lines:
	try:
		image_url = line.split("[IMAGE_URL:]")[1].split("[IMAGE_ID:]")[0]
		if (image_url in url_set):
			pass
		else:
			url_set.add(image_url)
			file_pointer_writer.write(line)
	except:
		pass

file_pointer_writer.close()
print str(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))