from urlmapper import UrlMap
import time
import json
from operator import itemgetter

mypath = "/Users/Tilley/Downloads/chromedriver"
myurl = "https://sjrfire.com"
myurlstart = "https://sjrfire.com"
# myurl = "https://youtube.com"
# myurl = "https://reddit.com"


# creates our UrlMap object
url_map = UrlMap(myurl, mypath, myurlstart, dynamic_pages=False)
url_map.create_map(total_iterations=5)

print(url_map.this_map)