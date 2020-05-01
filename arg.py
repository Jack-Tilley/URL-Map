## This file serves to read user input from the webpage and output
## a jsonfile from these inputs to the json_files dir

import argparse
from urlmapper import UrlMap
import json
import time
import requests

# collects the arguments passed by main.go
def collect_args():
    parser = argparse.ArgumentParser(description='collecting arg vals via argparse')
    parser.add_argument("--url", default="nourlentered", help="This is the 'url' variable")
    parser.add_argument("--mn", default="30", help="This is the 'maxnodes' variable")
    parser.add_argument("--dy", default="False", help="This is the 'dynamic' variable")

    args = parser.parse_args()

    url = args.url
    max_nodes = args.mn
    dynamic = args.dy

    return(url, max_nodes, dynamic)

# casts variables to their proper types, if values aren't of the proper type, throw error
def format_args(args):
    # attempt to validate website exists
    myurl = args[0]
    requests.get(myurl)
    # attempts to convert max_nodes to int
    mymaxnodes = int(args[1])
    # attempt to convert dynamic to boolean
    if args[2] == "True":
        mydynamic = True
    elif args[2] == "False":
        mydynamic = False
    else:
        raise Exception("The dynamic variable is neither True nor False, cannot convert to boolean")

    return (myurl,mymaxnodes,mydynamic)

# creates the map based on user input
def make_map(arg_tuple):
    dynamic_path = "/usr/lib/chromium-browser/chromedriver"

    url = arg_tuple[0]
    max_nodes = arg_tuple[1]
    dynamic = arg_tuple[2]

    url_map = UrlMap(url, dynamic_path, url, dynamic_pages=dynamic)
    url_map.create_map(total_iterations=max_nodes)

    return url_map

def format_json(url_map):
    # output format to be converted to json
    nodes_and_links = {}

    # nodes key in json
    nlu = url_map.d3_json_nodes_list
    # links key in json
    llu = url_map.d3_json_links_list
    # time key in json
    tlu = url_map.json_time

    nodes_and_links["nodes"] = nlu
    nodes_and_links["links"] = llu
    nodes_and_links["exectime"] = tlu
    print(nodes_and_links)

    return nodes_and_links

# dumps the properly formatted json data to file
def write_to_json(path_to_json_file, nodes_and_links):
    jsonnodesandlinks = json.dumps(nodes_and_links, indent=4)
    with open(path_to_json_file, 'w', encoding='utf-8') as f:
        f.write(jsonnodesandlinks)

def main():
    args = collect_args()
    arg_tuple = format_args(args)
    url_map = make_map(arg_tuple)
    nodes_and_links = format_json(url_map)
    write_to_json('public/json_files/JSONOUTPUT.json', nodes_and_links)

if __name__ == '__main__':
    main()

