import os

physical_address = 0
PATH = "O:/AllUnion"
file_pointer_writer = open(os.path.join(PATH, "out.xml"), "w")

with open(os.path.join(PATH, "AllUnion.xml"), "r") as file_pointer:
	lines = file_pointer.readlines()

for line in lines:
	if (line.strip(" \t\n\r") == ("<PHYSICAL_ADDRESS>")):
		physical_address += 1
	if(physical_address != 2):
		file_pointer_writer.write(line)
	if (line.strip(" \t\n\r") == ("</PHYSICAL_ADDRESS>")):
		if (physical_address == 2):
			physical_address = 0
	if (line.strip(" \t\n\r") == "</BUSINESS_PROFILE>"):
		physical_address = 0
file_pointer_writer.close()