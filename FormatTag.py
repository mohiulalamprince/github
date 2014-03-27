
inFile = open("")
outFile = open("")

line = ""
count = 0

while True:
    line = inFile.readline()
    if line == None:
        break
    if line == "<PROFILE>":
        count += 1

    if count == 2:
        count = 0
        line = "</PROFILE>"

    outFile.write(line)
    outFile.flush()

outFile.close()
inFile.close()

