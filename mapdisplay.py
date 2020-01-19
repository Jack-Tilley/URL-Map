# Jack Tilley
# January 2020
# This module serves to display the previously scraped websites network

from urlmapper import UrlMap
import networkx as nx
import matplotlib.pyplot as plt

mypath = "/Users/Tilley/Downloads/chromedriver"
myurl = "https://sjrfire.com"
# myurl = "https://youtube.com"
# myurl = "https://reddit.com"

mymap = UrlMap(myurl, mypath)
mymap.create_map()
mymap = mymap.get_map()
print(map)

G = nx.DiGraph(map)
nx.draw(G, with_labels=True)
plt.draw()
plt.show()


