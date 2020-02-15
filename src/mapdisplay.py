# Jack Tilley
# January 2020
# This module serves to display the previously scraped websites network

from urlmapper import UrlMap
import networkx as nx
import matplotlib.pyplot as plt
import time
import json
from operator import itemgetter

mypath = "/Users/Tilley/Downloads/chromedriver"
myurl = "https://sjrfire.com"
myurlstart = "https://sjrfire.com"
# myurl = "https://youtube.com"
# myurl = "https://reddit.com"

start = time.perf_counter()

url_map = UrlMap(myurl, mypath, myurlstart, dynamic_pages=False)
url_map.create_map()
# site_mapping = url_map.get_map()

site_map_json_list = url_map.json_list
site_map_json = json.dumps(site_map_json_list, indent=4)

with open('site_map.json', 'w', encoding='utf-8') as f:
    json.dump(site_map_json, f, ensure_ascii=False, indent=4)

end = time.perf_counter()


print(round(end - start, 2))
# print(map1)
#
# G = nx.DiGraph(map1)
# nx.draw(G, with_labels=True)
# plt.draw()
# plt.show()


