import argparse
from urlmapper import UrlMap
import networkx as nx
import matplotlib.pyplot as plt
import time
import json
from operator import itemgetter

def collect_args():
    parser = argparse.ArgumentParser(description='testing argparse')
    parser.add_argument("--url", default="nourlentered", help="This is the 'url' variable")
    parser.add_argument("--mn", default="-1", help="This is the 'maxnodes' variable")
    parser.add_argument("--dy", default="False", help="This is the 'dynamic' variable")

    args = parser.parse_args()
    url = args.url
    max_nodes = args.mn
    dynamic = args.dy

    # work is done here
    # print("hello", url, max_nodes, dynamic)
    return(url, max_nodes, dynamic)

args = collect_args()
mypath = "/Users/Tilley/Downloads/chromedriver"
myurl = args[0]
mymaxnodes = int(args[1])
if args[2] == 'True':
    mydynamic = True
else:
    mydynamic = False


url_map = UrlMap(myurl, mypath, myurl, dynamic_pages=mydynamic)
url_map.create_map()

# properly formats json data for d3.js
llu = url_map.json_links_list
nlu = url_map.json_nodes_list
nodes_and_links = {}
nodes_and_links["nodes"] = nlu
nodes_and_links["links"] = llu
# print(nodes_and_links)

# dumps the properly formatted json data to file
jsonnodesandlinks = json.dumps(nodes_and_links, indent=4)
with open('public/json_files/JSONOUTPUT.json', 'w', encoding='utf-8') as f:
    f.write(jsonnodesandlinks)

# print(jsonnodesandlinks)

# end = time.perf_counter()
# print(url_map.url_map)

