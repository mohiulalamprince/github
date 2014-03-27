import os

# get N profiles from a file

class GetNProfiles:

    def getNProfiles(self, inputLocation, totalProfile):

        inputFile = open(inputLocation, 'r')

        if os.path.exists("BusinessProfiles.xml"):
            outputFile = open("BusinessProfiles.xml" , 'a')
        else:
            outputFile = open("BusinessProfiles.xml" , 'a')

        tempProfile = ""
        countProfile = 0

        for line in inputFile.readlines():

            tempProfile += line
            
            if line.find("</BUSINESS_PROFILE>") != -1 :
                outputFile.write(tempProfile)
                outputFile.flush()
                tempProfile = ""
                countProfile += 1

                if countProfile >= totalProfile:
                    break

        inputFile.close()
        outputFile.close()
                                
if __name__ == "__main__":
    
    ob = GetNProfiles()
    ob.getNProfiles("F:\\OfficeWork\\Development\\BusinessSearch\\Data\\Profiles\\Release 04-05-2011\\LatLngFind\\AmazonCloud700GBUnion.xml", 177206)
