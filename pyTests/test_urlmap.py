import unittest
import sys
sys.path.append("..")
from urlmapper import UrlMap

myurl1 = "https://google.com/"
myurl2 = "https://reddit.com/"
mypath = "/Users/Tilley/Downloads/chromedriver"

mymap1 = UrlMap(myurl1, mypath, myurl1, dynamic_pages=False)
mymap1.create_map(total_iterations=10)

mymap2 = UrlMap(myurl2, mypath, myurl2)
mymap2.create_map(total_iterations=0)

mymap3 = UrlMap(myurl1, mypath)
mymap3.create_map() # total_iterations defaults to 30

class TestUrlMap(unittest.TestCase):

    # test to see that we get the correct amount of nodes
    def test_map_max_nodes(self):
        self.assertEqual(len(mymap1.this_map.keys()), 10)
        self.assertEqual(len(mymap2.get_map().keys()), 0)
        self.assertEqual(len(mymap3.this_map.keys()), 30)
        # -1 goes forever and cannot be tested
    
    # test to see that our queue remains intact after termination
    # so that maybe we can restart running at a later time
    def test_queue_depleted(self):
        self.assertNotEqual(len(mymap1.queue),0)

    

if __name__ == '__main__':
    unittest.main()

