
inFile = open("Profiles.xml" , "r")


while True:

    line = inFile.readline()

    if line == None:
        break

    print line
    
