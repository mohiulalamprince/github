#   Mohiul Alam Prince
#   Principal Software Engineer
#
#   Crawler resume script
#   or linkdb-recover script
#   or crawler configuration recover script
#   or host wise crawler configuration recover script
#
#   March 10, 2014
#
#   How to Run: Change the two path value(CRAWLER_LINKDB_PATH, CRAWLER_CONTENT_DATA_PATH) before you run the script
#   You have to explicitly tell the script the location of cralwer content folder and LinkDB folder
#   The default crawler content location is : HostData\WebSite\Content
#   The default crawler linkdb  location is : HostData\WebSite\LinkDB
#
#   Python version: 2.7

import os
import sys
import glob
import traceback

UPDATE = True
DEBUG = True

LINKDB_PATH = "LinkDB"
WEBSITE_PATH = "WebSite"
CONF_PATH = "Conf"
CONTENT_SEEN_PATH = "ContentSeen"
CONTENT_UNSEEN_PATH = "ContentUnseen"
DIFFERENT_HOST_PATH = "DifferentHost"
DOWNLOAD_LINK_PATH = "DownloadedLinkPath"
LINK_EXTRACTION_BLOCK_PATH = "LinkExtractionBlock"
URL_SEEN_BLOCK_PATH = "UrlSeenBlock"
CONTENT_PATH = "Content"
RECENT_HOST_LIST_FILE="RecentHostList.txt"

CRAWLER_HOST_CONF_PATH = r"H:\nelly\HostData\HostConf"
CRAWLER_LINKDB_PATH = r"H:\nelly\HostData\WebSite\LinkDB\www.nelly.com\www.nelly.com\nelly\HostData" + "\\" + WEBSITE_PATH + "\\" + LINKDB_PATH
CRAWLER_CONTENT_DATA_PATH = r"H:\nelly\HostData" + "\\" + WEBSITE_PATH + "\\" + CONTENT_PATH
                       

class URLInfo():
    def __init__(self):
        self.url_start_byte = None
        self.url_end_byte = None
        self.content_statt_byte = None
        self.content_end_byte = None

class ContentByteInfo(URLInfo):
    def __init__(self):
        self.content_id = None

class ConfigUtil():
    def __init__(self):
        self.last_downloaded_url_byte_info = ContentByteInfo()
    
    def last_downloaded_url_byte_info_generate(self, download_linkpath_filelist):
        last_line = None
        max_document_no = -1
        for download_linkpath_file in download_linkpath_filelist:
                with open(download_linkpath_file, 'r') as download_linkpath_file_fp:
                    for line in download_linkpath_file_fp:
                        try:
                            document_no = int(line.split(".html")[0].split(' ')[1])
                            if (document_no >= max_document_no):
                                max_document_no = document_no
                                last_line = line
                        except: 
                            if (DEBUG == True):
                                print str(traceback.print_exc(file=sys.stdout))
        content_byte_info = last_line.split(".html")[1].split(' ')

        if (len(content_byte_info) >= 6):
            self.last_downloaded_url_byte_info.content_id = content_byte_info[1]
            self.last_downloaded_url_byte_info.url_start_byte = content_byte_info[2]
            self.last_downloaded_url_byte_info.url_end_byte = content_byte_info[3]
            self.last_downloaded_url_byte_info.content_start_byte = content_byte_info[4]
            self.last_downloaded_url_byte_info.content_end_byte = content_byte_info[5]

        return self.last_downloaded_url_byte_info , last_line, max_document_no               
        
class ConfRecover(ConfigUtil):
    def __init__(self, conf):
        
        self.id_generator_file = "idGenerator.txt"
        self.http_request_file = "httpRequest.CM"
        self.error_in_download_file = "ErrorInDownload.txt"
        self.total_download_file = "totalDownload.CM"
        self.total_url_file = "totalUrl.US"

        self.conf = conf
        self.last_downloaded_url_byte_info = ContentByteInfo()

    def recover_id_generator(self, host_name):

        sys.stdout.write("Recovering Conf => IdGenerator ...  ...  ")        
        download_linkpath_filelist = []
        DOWNLOAD_LINKPATH_DIRECTORY = "".join( CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + DOWNLOAD_LINK_PATH)
        download_linkpath_filelist = glob.glob(DOWNLOAD_LINKPATH_DIRECTORY + "\\" + "*.linkPath")

        try:
            last_line = None        
            max_document_no = -1
            last_download_url_byte_info, last_line, max_document_no = self.last_downloaded_url_byte_info_generate(download_linkpath_filelist)
                
            self.conf.id_generator = max_document_no + 1
            print "[Passed]" 
        except:
            print "[Failed]"
            if (DEBUG == True):
                print str(traceback.print_exc(file=sys.stdout))
            
        return max_document_no + 1
    
    def recover_http_request(self, host_name):
        url_seen_filelist = []
        URL_SEEN_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + URL_SEEN_BLOCK_PATH)
        url_seen_filelist = glob.glob(URL_SEEN_DIRECTORY + "\\" + "*.urlBlock")

        if (self.last_downloaded_url_byte_info.content_id == None):
            self.recover_id_generator(host_name)
            if (self.last_downloaded_url_byte_info.content_id == None):
                print "Recover Conf => HttpRequest ... [Failed]"
                return
            
        sys.stdout.write("Recovering Conf => HttpRequest ...  ...  ")

        counter = 0
        try:
            last_downloaded_content_location = "".join(CRAWLER_CONTENT_DATA_PATH
                                                   + "\\" + str(self.last_downloaded_url_byte_info.content_id)
                                                   + ".CONTENT")       
            last_downloaded_url =  None
            with open(last_downloaded_content_location, 'r') as last_downloaded_content_fp:
                last_downloaded_content_fp.seek(int(self.last_downloaded_url_byte_info.url_start_byte)-1)
                last_downloaded_url = last_downloaded_content_fp.read(int(self.last_downloaded_url_byte_info.url_end_byte)
                                                                      - int(self.last_downloaded_url_byte_info.url_start_byte) + 1)                
            recover = False
            for url_seen_file in url_seen_filelist:
                with open(url_seen_file, 'r') as url_seen_file_fp:
                    for line in url_seen_file_fp:
                        counter += 1
                        try:
                            if (line.split("|||")[0] == last_downloaded_url):
                                recover = True
                        except:
                            if (DEBUG == True):
                                print str(traceback.print_exc(file=sys.stdout))
            self.conf.http_request = counter
            
            if (recover == True):
                print "[Passed]"
            else:
                print "[Failed]"
        except:
            print "[Failed]"
            if (DEBUG == True):
                print str(traceback.print_exc(file=sys.stdout))
            
        return counter

    def recover_error_in_download(self, host_name):
        sys.stdout.write("Recovering Conf => ErrorInDownload ...  ...  ")
        if (self.conf.http_request == None):
            print "[Failed]"
            return
        else:
            print "[Passed]"
            self.conf.error_in_download = self.conf.http_request - self.conf.total_download
        return self.conf.http_request - self.conf.total_download

    def recover_total_download(self, host_name):
        sys.stdout.write("Recovering Conf => TotalDownload ...  ...  ")
        if (self.conf.id_generator == None):
            print "[Failed]"
            return
        else:
            print "[Passed]"
            self.conf.total_download = self.conf.id_generator - 1
            
        return self.conf.id_generator - 1

    def recover_total_url(self, host_name):
        counter = 0
        try:
            url_seen_filelist = []
            URL_SEEN_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                                   + "\\" + host_name
                                                   + "\\" + URL_SEEN_BLOCK_PATH)
            url_seen_filelist = glob.glob(URL_SEEN_DIRECTORY + "\\" + "*.urlBlock")

            sys.stdout.write("Recovering Conf => TotalUrl ...  ...  ")
            for url_seen_file in url_seen_filelist:
                with open(url_seen_file, 'r') as url_seen_file_fp:
                    for line in url_seen_file_fp:
                        counter += 1

            print "[Passed]"
            self.conf.total_url = counter   
        except:
            print "[Failed]"
            if (DEBUG == True):
                print str(traceback.print_exc(file=sys.stdout))
                 
        return counter

    def recover(self, host_name):
        print "Recovering http://" + host_name + "  ... ...   [Started]"
        print "Step: => 1"
        print "Recovering Conf"
        
        self.recover_id_generator(host_name)
        self.recover_total_url(host_name)
        self.recover_total_download(host_name)
        self.recover_http_request(host_name)
        self.recover_error_in_download(host_name)

        if (self.conf.id_generator == None or
            self.conf.total_download == None or
            self.conf.http_request == None or
            self.conf.error_in_download == None or
            self.conf.total_url == None):
            return False
        return True
    
    def update(self, host_name):
        self.update_id_generator(host_name)
        self.update_total_url(host_name)
        self.update_total_download(host_name)
        self.update_http_request(host_name)
        self.update_error_in_download(host_name)

        return True

    def update_id_generator(self, host_name):
        CONF_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + CONF_PATH)
        with open(CONF_DIRECTORY + "\\" + self.id_generator_file, 'w') as file_pointer:
            file_pointer.write(str(self.conf.id_generator))

    def update_total_url(self, host_name):
        CONF_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + CONF_PATH)
        with open(CONF_DIRECTORY + "\\" + self.total_url_file, 'w') as file_pointer:
            file_pointer.write(str(self.conf.total_url))            

    def update_http_request(self, host_name):
        CONF_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + CONF_PATH)
        with open(CONF_DIRECTORY + "\\" + self.http_request_file, 'w') as file_pointer:
            file_pointer.write(str(self.conf.http_request))

    def update_total_download(self, host_name):
        CONF_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + CONF_PATH)
        with open(CONF_DIRECTORY + "\\" + self.total_download_file, 'w') as file_pointer:
            file_pointer.write(str(self.conf.total_download))

    def update_error_in_download(self, host_name):
        CONF_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + CONF_PATH)
        with open(CONF_DIRECTORY + "\\" + self.error_in_download_file, 'w') as file_pointer:
            file_pointer.write(str(self.conf.error_in_download))                  
class Conf():
    def __init__(self):
        self.id_generator = None
        self.total_url = None
        self.total_download = None
        self.http_request = None
        self.error_in_download = None        

        self.conf_recover = ConfRecover(self)
        
    def recover(self, host_name):
        if (self.conf_recover.recover(host_name) == True):
            return True
        else:
            return False
        
    def update(self, host_name):
        self.conf_recover.update(host_name)
        
class DownloadLinkPathRecover():
    def __init__(self):
        pass        

class URLSeenBlockRecover():
    def __init__(self, url_seen):
        self.config_us_file = "config.US"
        self.config_cm_file = "config.CM"
        self.url_seen = url_seen

    def recover(self, host_name):
        print "Step: => 2"
        print "Recovering URLSeenBlock"
        self.recover_config_us(host_name)
        self.recover_config_cm(host_name)

        if (self.url_seen.config_cm.block_id == None or
            self.url_seen.config_cm.block_id_byte_position == None or
            self.url_seen.config_us == None):
            print "ERROR: " + str(self.url_seen.config_cm.block_id) + str(self.url_seen.config_cm.block_id_byte_position) + str(self.url_seen.config_us)
            return False
        return True
        
    def update(self, host_name):
        self.update_config_us(host_name)
        self.update_config_cm(host_name)

    def recover_config_us(self, host_name):
        sys.stdout.write("Recovering URLSeen => Config.US ...  ...  ")
        url_seen_filelist = []
        URL_SEEN_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + URL_SEEN_BLOCK_PATH)
        url_seen_filelist = glob.glob(URL_SEEN_DIRECTORY + "\\" + "*.urlBlock")
        self.url_seen.config_us = len(url_seen_filelist)

        print "[Passed]"        
        return len(url_seen_filelist)

    def recover_config_cm(self, host_name):
        sys.stdout.write("Recovering URLSeen => Config.CM ...  ...  ")
        download_linkpath_filelist = []
        DOWNLOAD_LINKPATH_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + DOWNLOAD_LINK_PATH)
        download_linkpath_filelist = glob.glob(DOWNLOAD_LINKPATH_DIRECTORY + "\\" + "*.linkPath")
        
        config_util = ConfigUtil()
        last_downloaded_url_byte_info, last_line, max_document_no = config_util.last_downloaded_url_byte_info_generate(download_linkpath_filelist)
 
        last_downloaded_content_location = "".join(CRAWLER_CONTENT_DATA_PATH
                                                   + "\\" + str(last_downloaded_url_byte_info.content_id)
                                                   + ".CONTENT")
        last_downloaded_url =  None
        with open(last_downloaded_content_location, 'r') as last_downloaded_content_fp:
            last_downloaded_content_fp.seek(int(last_downloaded_url_byte_info.url_start_byte)-1)
            last_downloaded_url = last_downloaded_content_fp.read(int(last_downloaded_url_byte_info.url_end_byte)
                                                                  - int(last_downloaded_url_byte_info.url_start_byte) + 1)
        
        url_seen_filelist = []
        URL_SEEN_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + URL_SEEN_BLOCK_PATH)
        url_seen_filelist = glob.glob(URL_SEEN_DIRECTORY + "\\" + "*.urlBlock")

        byte_info = 0
        max_block_id = block_id = 0
        max_byte_info = 0
        recover = False
        
        for url_seen_file in url_seen_filelist:
            with open(url_seen_file, 'r') as url_seen_file_fp:
                byte_info = 0
                for line in url_seen_file_fp:
                    try:
                        byte_info += len(line)
                        byte_info += 1
                        if (line.split("|||")[0] == last_downloaded_url):
                            max_block_id = str((url_seen_file).split(".urlBlock")[0].split("\\")[-1])
                            max_byte_info = byte_info
                            recover = True
                            break
                    except:
                        if (DEBUG == True):
                            print str(traceback.print_exc(file=sys.stdout))
                    
        if (recover == True):
            print "[Passed]"
            self.url_seen.config_cm.block_id = str(int(max_block_id) - 1)
            self.url_seen.config_cm.block_id_byte_position = max_byte_info
        else:
            print "[Failed]"

        return int(max_block_id) - 1, max_byte_info            
    
    def update_config_us(self, host_name):
        URL_SEEN_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + URL_SEEN_BLOCK_PATH)
        with open(URL_SEEN_DIRECTORY + "\\" + self.config_us_file, 'w') as file_pointer:
            file_pointer.write(str(self.url_seen.config_us))  

    def update_config_cm(self, host_name):
        URL_SEEN_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + URL_SEEN_BLOCK_PATH)
        with open(URL_SEEN_DIRECTORY + "\\" + self.config_cm_file, 'w') as file_pointer:
            file_pointer.write(str(self.url_seen.config_cm.block_id) + " " + str(self.url_seen.config_cm.block_id_byte_position))
        
class Config_CM():
    def __init__(self):
        self.block_id = None
        self.block_id_byte_position = None
            
class URLSeen():
    def __init__(self):
        self.config_us = None
        self.config_cm = Config_CM()
        self.url_seen_recover = URLSeenBlockRecover(self)

    def recover(self, host_name):
        if (self.url_seen_recover.recover(host_name) == True):
            return True
        else:
            return False

    def update(self, host_name):
        self.url_seen_recover.update(host_name)

class LinkExtractionBlockRecover():
    def __init__(self, link_extraction):
        self.config_txt_file = "config.txt"
        self.link_extraction = link_extraction

    def recover(self, host_name):
        print "Step: => 3"
        sys.stdout.write("Recovering LinkExtraction\n")
        self.recover_config_txt(host_name)

        if (self.link_extraction.config.last_before_block_id == None or
            self.link_extraction.config.last_block_id == None or
            self.link_extraction.config.number_of_url_in_last_block == None):
            return False
        else:
            return True

    def update(self, host_name):
        self.update_config_txt(host_name)
        
    def recover_config_txt(self, host_name):
        sys.stdout.write("Recovering LinkExtraction => Config.txt ...  ...  ")
        link_extraction_block_filelist = []
        LINK_EXTRACTION_BLOCK_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + LINK_EXTRACTION_BLOCK_PATH)
        link_extraction_block_filelist = glob.glob(LINK_EXTRACTION_BLOCK_DIRECTORY + "\\" + "*.urlBlock")

        self.link_extraction.config.last_block_id = len(link_extraction_block_filelist)
        self.link_extraction.config.last_before_block_id = len(link_extraction_block_filelist)-1

        try:
            self.link_extraction.config.number_of_url_in_last_block = 0
            with open(LINK_EXTRACTION_BLOCK_DIRECTORY + "\\" + str(len(link_extraction_block_filelist)) + ".urlBlock") as file_pointer:
                for line in file_pointer:
                    self.link_extraction.config.number_of_url_in_last_block += 1
            print "[Passed]"
        except:
            print "[Failed]"
            if (DEBUG == True):
                print str(traceback.print_exc(file=sys.stdout))
            
        return self.link_extraction.config.last_block_id, self.link_extraction.config.last_before_block_id, self.link_extraction.config.number_of_url_in_last_block        
        
    def update_config_txt(self, host_name):
        LINK_EXTRACTION_BLOCK_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + LINK_EXTRACTION_BLOCK_PATH)
        with open(LINK_EXTRACTION_BLOCK_DIRECTORY + "\\" + self.config_txt_file, 'w') as file_pointer:
            file_pointer.write(str(self.link_extraction.config.last_block_id) + " " + str(self.link_extraction.config.number_of_url_in_last_block) + " " + str(self.link_extraction.config.last_before_block_id))

class LinkExtractionConfig():
    def __init__(self):
        self.last_block_id = None
        self.last_before_block_id = None
        self.number_of_url_in_last_block = None
    
class LinkExtraction():
    def __init__(self):
        self.config = LinkExtractionConfig()
        self.link_extraction_block_recover = LinkExtractionBlockRecover(self)

    def recover(self, host_name):
        if (self.link_extraction_block_recover.recover(host_name) == True):
            return True
        else:
            return False

    def update(self, host_name):
        self.link_extraction_block_recover.update(host_name)

class DownloadLinkPathRecover():
    def __init__(self, download_link_path):
        self.config_cm_file = "config.CM"
        self.config_txt_file = "config.txt"
        self.download_link_path = download_link_path
        
    def recover(self, host_name):
        print "Step: => 4"
        sys.stdout.write("Recovering DownloadLinkPath\n")
        self.recover_config_txt(host_name)
        self.recover_config_cm(host_name)

        if (self.download_link_path.config_cm.last_block_id == None or
            self.download_link_path.config_cm.total_number_of_files_in_last_block == None):
            return False

        if (self.download_link_path.config_txt.block_no == None or
            self.download_link_path.config_txt.byte_info == None or
            self.download_link_path.config_txt.next_document_id == None or
            self.download_link_path.config_txt.previous_document_id == None):
            return False

        return True

    def update(self, host_name):
        self.update_config_txt(host_name)
        self.update_config_cm(host_name)
        
    def recover_config_txt(self, host_name):
        sys.stdout.write("Recovering DownloadLinkPath => Config.txt ...  ...  ")
        link_extraction_block_filelist = []
        LINK_EXTRACTION_BLOCK_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + LINK_EXTRACTION_BLOCK_PATH)
        link_extraction_block_filelist = glob.glob(LINK_EXTRACTION_BLOCK_DIRECTORY + "\\" + "*.urlBlock")

        last_line = None
        last_line_byte_info = None
        try:
            with open(LINK_EXTRACTION_BLOCK_DIRECTORY + "\\" + str(len(link_extraction_block_filelist)) + ".urlBlock") as file_pointer:
                for line in file_pointer:
                    if (line.find("</ANCHOR_TEXT>")):
                        last_line = line

            last_line_byte_info = last_line.split("SOURCE_URL ")[1].split(" <ANCHOR_TEXT>")[0]
        except:
            print "[Failed]"
            if (DEBUG == True):
                print str(traceback.print_exc(file=sys.stdout))
            return

        download_linkpath_filelist = []
        DOWNLOAD_LINKPATH_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + DOWNLOAD_LINK_PATH)
        download_linkpath_filelist = glob.glob(DOWNLOAD_LINKPATH_DIRECTORY + "\\" + "*.linkPath")
        
        byte_info = 0
        preserver_byte_info = 0
        block_no = 0
        document_no = None
        try:
            for download_linkpath_file in download_linkpath_filelist:    
                with open(download_linkpath_file, 'r') as download_linkpath_file_fp:
                    byte_info = 0
                    for line in download_linkpath_file_fp:
                        try:
                            byte_info += len(line)
                            byte_info += 1 #Manually added the value "ENTER" key in windows
                            if (line.split("CRAWLER_DEPTH=")[1].split(" CRAWL_TIME")[0].endswith(last_line_byte_info)):
                                document_no = int(line.split(".html")[0].split(' ')[1])
                                block_no = str((download_linkpath_file).split(".linkPath")[0].split("\\")[-1])                
                                preserver_byte_info = byte_info

                                statinfo = os.stat(download_linkpath_file)
                                if (statinfo.st_size == byte_info):
                                    (block_no) = int(block_no) + 1
                                    preserver_byte_info = 0
                                break
                        except:
                            if (DEBUG == True):
                                print str(traceback.print_exc(file=sys.stdout))
        except:
            print "[Failed]"
            if (DEBUG == True):
                print str(traceback.print_exc(file=sys.stdout))
            return

        byte_info = preserver_byte_info

        print "[Passed]"

        self.download_link_path.config_txt.block_no = block_no
        self.download_link_path.config_txt.byte_info = byte_info
        self.download_link_path.config_txt.next_document_id = document_no + 1
        self.download_link_path.config_txt.previous_document_id = document_no

        return int(block_no), int(byte_info), int(document_no) + 1, int(document_no)
    
    def recover_config_cm(self, host_name):
        sys.stdout.write("Recovering DownloadLinkPath => Config.CM ...  ...  ")
        download_link_path_filelist = []
        DOWNLOAD_LINK_PATH_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + DOWNLOAD_LINK_PATH)
        download_link_path_filelist = glob.glob(DOWNLOAD_LINK_PATH_DIRECTORY + "\\" + "*.linkPath")
        self.download_link_path.config_cm.last_block_id = len(download_link_path_filelist)
        self.download_link_path.config_cm.total_number_of_files_in_last_block = 0

        with open(DOWNLOAD_LINK_PATH_DIRECTORY + "\\" + str(len(download_link_path_filelist)) + ".linkPath") as file_pointer:
            for line in file_pointer:
                self.download_link_path.config_cm.total_number_of_files_in_last_block += 1

        print "[Passed]"        
        return len(download_link_path_filelist), self.download_link_path.config_cm.total_number_of_files_in_last_block
    
    def update_config_txt(self, host_name):
        DOWNLOAD_LINK_PATH_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + DOWNLOAD_LINK_PATH)
        with open(DOWNLOAD_LINK_PATH_DIRECTORY + "\\" + self.config_txt_file, 'w') as file_pointer:
            file_pointer.write(str(self.download_link_path.config_txt.block_no) + " " 
                + str(self.download_link_path.config_txt.byte_info) + " "
                + str(self.download_link_path.config_txt.next_document_id) + " "
                + str(self.download_link_path.config_txt.previous_document_id) + " ")

    def update_config_cm(self, host_name):
        DOWNLOAD_LINK_PATH_DIRECTORY = "".join(CRAWLER_LINKDB_PATH
                                               + "\\" + host_name
                                               + "\\" + DOWNLOAD_LINK_PATH)
        with open(DOWNLOAD_LINK_PATH_DIRECTORY + "\\" + self.config_cm_file, 'w') as file_pointer:
            file_pointer.write(str(self.download_link_path.config_cm.last_block_id) + " " 
                + str(self.download_link_path.config_cm.total_number_of_files_in_last_block))

class DownloadLinkConfig_CM():
    def __init__(self):
        self.last_block_id = None
        self.total_number_of_files_in_last_block = None

class DownloadLinkConfig_txt():
    def __init__(self):
        self.block_id = None
        self.byte_position = None
        self.next_document_id = None
        self.previous_document_id = None

class DownloadLinkPath():
    def __init__(self):
        self.config_cm = DownloadLinkConfig_CM()
        self.config_txt = DownloadLinkConfig_txt()
        self.download_link_path_recover = DownloadLinkPathRecover(self)

    def recover(self, host_name):
        if (self.download_link_path_recover.recover(host_name) == True):
            return True
        else:
            return False

    def update(self, host_name):
        self.download_link_path_recover.update(host_name)
        
class ConfigurationManager():
    def __init__(self):
        self.conf = Conf()
        self.url_seen = URLSeen()
        self.link_extraction = LinkExtraction()
        self.download_link_path = DownloadLinkPath()
        
    def recover(self, host_name):
        #Crawler conf recover
        if (self.conf.recover(host_name)):
            pass
        else:
            return False

        #Crawler url seen recover
        if (self.url_seen.recover(host_name)):
            pass 
        else:
            return False

        #Crawler Link Extraction recover        
        if (self.link_extraction.recover(host_name)):
            pass
        else:
            return False

        #Crawler Download link path recover        
        if (self.download_link_path.recover(host_name)):
            pass
        else:
            return False
        
        return True        
        
    def update(self, host_name):
        sys.stdout.write("Updating Conf ... ...  ")
        self.conf.update(host_name)
        print "[Passed]"

        sys.stdout.write("Updating URLSeen ... ...  ")
        self.url_seen.update(host_name)
        print "[Passed]"

        sys.stdout.write("Updating LinkExtraction ... ...  ")
        self.link_extraction.update(host_name)
        print "[Passed]"

        sys.stdout.write("Updating DownloadLinkPath ... ...  ")
        self.download_link_path.update(host_name)
        print "[Passed]" 

        return True       
        
class Configuration():
    def __init__(self):
        self.configuration_manager = ConfigurationManager()
        
    def recover(self, host_name):
        if (self.configuration_manager.recover(host_name) == True):
            print "Recovering Host : http://" + host_name + " ...  ...  " + "[Passed]"
            if (UPDATE == True):
                print "Updated Process  ...  ...  ...  [Started]"
                if (self.update(host_name) == True):
                    self.addHostInHostConf(host_name)
                    print "Host: http://" + host_name + "  ...  ...  ...   [DONE]"
                else:
                    print "Host: http://" + host_name + "  ...  ...  ...   [Failed]"
            else:
                pass
        else:
            pass

    def update(self, host_name):
        if (self.configuration_manager.update(host_name) == True):
            return True
        else:
            return False

    def addHostInHostConf(self, host_name):
        with open(CRAWLER_HOST_CONF_PATH + "\\" + "RecentHostList.txt", 'a') as file_pointer:
            file_pointer.write("http://" + host_name + "/\\n")

configuration = Configuration()
configuration.recover("www.nelly.com")
