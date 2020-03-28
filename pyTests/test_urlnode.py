import unittest
import sys
sys.path.append("..")
from urlmapper import UrlNode


mynode = UrlNode('localhost')
mynode.set_ip()

class TestUrlNode(unittest.TestCase):
    # test to see we get the correct ip
    def test_ip(self):
        self.assertEqual(mynode.ip, '127.0.0.1')

    # test to see that our url is correct
    def test_url(self):
        self.assertEqual(mynode.curr_url, 'localhost')
    
    
        
        



if __name__ == '__main__':
    unittest.main()