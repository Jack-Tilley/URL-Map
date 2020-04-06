# Jack Tilley
# January 2020
# This module serves to display the previously scraped websites network

from urlmapper import UrlMap
import time
import json
from operator import itemgetter

mypath = "/Users/Tilley/Downloads/chromedriver"
myurl = "https://sjrfire.com"
myurlstart = "https://sjrfire.com"
# myurl = "https://youtube.com"
# myurl = "https://reddit.com"

start = time.perf_counter()

# creates our UrlMap object
url_map = UrlMap(myurl, mypath, myurlstart, dynamic_pages=False)
url_map.create_map()

# site_mapping = url_map.get_map()
# site_map_json_list = url_map.json_list
# site_map_json = json.dumps(site_map_json_list, indent=4)
# print(site_map_json)

# with open('site_map.json', 'w', encoding='utf-8') as f:
#     json.dump(site_map_json, f, ensure_ascii=False, indent=4)

# gets data and formats it so d3.js can read it properly
llu = url_map.json_links_list
nlu = url_map.json_nodes_list
nodes_and_links = {}
nodes_and_links["nodes"] = nlu
nodes_and_links["links"] = llu
# print(nodes_and_links)

# dumps the properly formatted json data to file
jsonnodesandlinks = json.dumps(nodes_and_links, indent=4)
with open('nodesandlinks', 'w', encoding='utf-8') as f:
    json.dump(jsonnodesandlinks, f, ensure_ascii=False, indent=4)

# print(jsonnodesandlinks)

end = time.perf_counter()
print(round(end - start, 2))

# draws the map in python
# print(map1)
#
# G = nx.DiGraph(map1)
# nx.draw(G, with_labels=True)
# plt.draw()
# plt.show()


