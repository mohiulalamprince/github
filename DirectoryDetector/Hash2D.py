
import os
import sys

class Hash2D:

    def __init__(self):
        self.hash = {}

    def clear(self):
        self.hash = {}

    def insert(self, key, value):       
        
        if self.hash.has_key(key):
            if not self.hash[key].has_key(value):
                self.hash[key][value] = True
                return True
            else:
                return False
        else:
            self.hash[key] = {value:True}
            return True
            
    
    def merge(self, otherHash2D):
        
        totalNewValue = 0
        
        otherHash = otherHash2D.hash

        for key in otherHash.keys():
            
            tempHash = otherHash[key]
            
            for value in tempHash.keys():                
                if self.insert(key, value):
                    totalNewValue += 1
            
        return totalNewValue
    
    def get(self):
        
        strKeys = ""
        strKeyFre = ""
        
        keys = self.hash.keys()
        
        for i in range(len(keys)):
            
            strKeys += keys[i]
            strKeyFre += str(len(self.hash[keys[i]]))
            
            if i != len(keys) - 1:
                strKeyFre += "#"
                strKeys += "#"       
    
        return strKeys, strKeyFre
        
    def size(self):
        
        count = 0
        
        keys = self.hash.keys()
        
        for i in range(len(keys)):
            count += len(self.hash[keys[i]])
            
        return count        
        
    def printHash(self):

        for key in self.hash.keys():
            print "KEY: ", key, " VALUES: ", str(self.hash[key].keys())
        
if __name__ == "__main__":
    
    hash2D = Hash2D()
    
    hash2D.insert("phone", "125")
    hash2D.insert("fax", "125")
    hash2D.insert("tel", "125")
    hash2D.insert("phone", "125")
    hash2D.insert("fax", "1125")
    hash2D.insert("phone", "1285")
    hash2D.insert("phone", "1525")
        
    print hash2D.get()
    hash2D.printHash()   
       
    hash2D_ = Hash2D()
    
    hash2D_.insert("phone", "125")
    hash2D_.insert("fax", "125")
    hash2D_.insert("tel", "1205")
    hash2D_.insert("phone", "125")
    hash2D_.insert("fax", "1125")
    hash2D_.insert("mobile", "1285")
    hash2D_.insert("email", "1525")
        
    print hash2D_.get()
    hash2D_.printHash()
    
    hash2D.merge(hash2D_)
    print hash2D.get()
    hash2D.printHash()   
       
    
        
        
        
        
        
        
        
