# Jack Tilley
# January 2020
# This module serves to display the previously scraped websites network

from urlmapper import UrlMap
import networkx as nx
import matplotlib.pyplot as plt
import time

mypath = "/Users/Tilley/Downloads/chromedriver"
myurl = "https://sjrfire.com"
myurlstart = "https://sjrfire.com"
# myurl = "https://youtube.com"
# myurl = "https://reddit.com"

start = time.perf_counter()
mymap = UrlMap(myurl, mypath, myurlstart, dynamic_pages=False)
mymap.create_map()
map1 = mymap.get_map()
end = time.perf_counter()
print(round(end - start, 2))
print(map1)

G = nx.DiGraph(map1)
nx.draw(G, with_labels=True)
plt.draw()
plt.show()


