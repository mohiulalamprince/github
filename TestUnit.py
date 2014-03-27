#!/usr/bin/env python

import math
import unittest

class MyClass:
    
    def getSum(self, a, b):
        return a + b
    
    
    
    
class TestMyClass(unittest.TestCase):
    
    def testSum(self):
        myClass = MyClass()
        self.assertEqual(5, myClass.getSum(2, 3))
        self.assertAlmostEqual(5, myClass.getSum(2, 3))
        self.assertEqual(10, myClass.getSum(2, 3))
        self.assertEqual(5, myClass.getSum(2, 3))
        
#class TestMath(unittest.TestCase):
#    def testFloor(self):
#        self.assertEqual(1, math.floor(1.01))
#        self.assertEqual(0, math.floor(0.5))
#        self.assertEqual(-1, math.floor(-0.5))
#        self.assertEqual(-2, math.floor(-1.1))
#
#    def testCeil(self):
#        self.assertEqual(2, math.ceil(1.01))
#        self.assertEqual(1, math.ceil(0.5))
#        self.assertEqual(0, math.ceil(-0.5))
#        self.assertEqual(-1, math.ceil(-1.1))


if __name__ == "__main__":
    unittest.main()