import os
import sys


class URLLister:

    def __init__(self):

        self.urls = []

    def reset(self):
        self.urls = []

    def feed(self, thisData):

        lb = 0
        ub = 0

        #print thisData        
        
        while True:

            lb = thisData.find("href=\"", ub)

            if lb == -1:
                break

            ub = thisData.find("\"", lb+6)
            #print lb, " ", ub
            print "URL: ", thisData[lb+6:ub]
            self.urls.append(thisData[lb+6:ub])
            

if __name__ == "__main__":

	import urllib
	usock = urllib.urlopen("http://smslib.org/")
	parser = URLLister()
	parser.feed(usock.read())
	usock.close()


                



