import os
import sys

file_pointer = open("H:\image_name.txt", "a")

image_counter = 0
for counter in range(1, 1400000):
	try:
		statinfo = os.stat(r"H:/pic/" + str(counter))
		if (statinfo.st_size >= 81920 and statinfo.st_size <= 102400):
			print "image : " + str(counter)
			image_counter += 1
			file_pointer.write(str(counter) + "\n")
	except:
		pass
file_pointer.close()

print "IMAGE_COUNTER : " + str(image_counter)