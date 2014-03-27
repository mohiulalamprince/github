cmpString = "|||CRAWLER_DEPTH="
searchUrlData = []
urlData = "http://www.gooogle.com|||CRAWER_DEPTH="
j = None
i = 0

while (True):
    if (urlData[i] == None):
        break;
    if (urlData[i] == '|'):
        j = i;
        while (True):
            if (urlData[j] == None):
                break;
            if (cmpString[j-i] != urlData[j]):
                break;
            if (j - i == 17 and urlData[j] == '='):
                j = -100;
                break;
            j = j + 1
    else:
        searchUrlData.append(urlData[i]);
    if (j == -100) :
        break;
    i = i + 1

print searchUrlData;