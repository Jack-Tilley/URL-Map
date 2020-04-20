from urlmapper import UrlMap
import time

mypath = "/Users/Tilley/Downloads/chromedriver"
myurl = "https://www.google.com/"
myurlstart = "https://www.google.com/"

url_map = UrlMap(myurl, mypath, myurlstart, dynamic_pages=False)
#2.9747540950775146 sec for 10 nodes
#37.1645712852478 sec for 100 nodes
#424.85131096839905 sec for 1000 nodes
start = time.time()
url_map.create_map(total_iterations=1000)
end = time.time()
print(url_map.this_map)
print(end-start)