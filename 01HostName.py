f = open("//192.168.1.68\\HostDataLargest\\HostData\\HostConf\\finishHostList.txt", "r")
out = open("01HostName.txt", "w")

for line in f:
    tmpLine = line
    tokens = tmpLine.split()
    if ((tokens) >= 3):
        if (int(tokens[3]) >= 15 and int(tokens[3]) <= 20):
            out.write(tokens[1] + "\n")
            print tokens[1]

f.close()
out.close()
