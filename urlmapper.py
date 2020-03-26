# Jack Tilley
# January 2020
# The purpose of this module is to scrape the links from a website and find all links that the website contains
# This module combines with mapdisplay.py to show the networking of the site

## WEBSCRAPING_TOOLS MAY NOT WORK FOR WINDOWS
## NEEDS TO BE TESTED/FIXED
## IF IT DOESNT WORK ON YOUR MACHINE PLEASE ASK ME
from webscraping_tools import ezScrape
from bs4 import BeautifulSoup
import requests

# a graph containing the links a website has, links in the form of UrlNode
class UrlMap:
    def __init__(self, base_url, path, starting_url="", url_map={}, local_only=True, dynamic_pages=False):
        self.base_url = base_url  # initial url. ex: https://www.youtube.com
        self.path = path  # path to chrome driver
        self.starting_url = starting_url
        self.url_map = url_map  # dictionary containing UrlNodes
        self.seen_nodes = {}  # nodes that we have seen so far and how many times we have seen it
        self.explored = {}  # explored for bfs
        if self.starting_url == "":
            self.starting_url = self.base_url
        self.queue = [self.starting_url]  # queue for bfs
        self.local_only = local_only  # if true, only stays on base url, else is allowed to go to other sites
        self.dynamic_pages = dynamic_pages # setting this to true will cause the program to run significantly slower
        # but the program scraping will be extremely more accurate
        self.stop_flag = False  # flag that stops while loop
        self.json_list = []
        self.json_links_list = []
        self.json_nodes_list = []
        if self.local_only:
            self.end_url_index = len(base_url) - 1  # helps get the number of "/"
        else:
            self.end_url_index = -2 # this needs to be fixed

    # finds all the links on the specified url
    def get_links(self, url, html):
        # creates a root node for the current page
        # gets all links from the html of that page
        root_node = UrlNode(url, html)
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a")

        # loops through each link we found earlier
        # creates a new node if the format is valid
        for link in links:
            # collects link
            new_node_url = link.get("href")

            # if link is broken or missing, do nothing
            if new_node_url is None: 
                continue

            # if node stays within current site
            if new_node_url.startswith("/"):
                new_node_url = self.base_url + new_node_url

            # if node leads to another site
            elif new_node_url.startswith("http"): 
                # if we only want links from the current site
                # we throw away this url
                if self.local_only:
                    continue
                # otherwise we keep the url
                else:
                    new_node_url = new_node_url
            # otherwise we have a unidentified url, do nothing
            else: 
                continue

            # print(new_node_url)

            # self.seen_nodes[new_node_url] = self.seen_nodes.get(new_node_url, 0) + 1

            #  adds new node to our seen collection, inc times seen
            root_node.connections[new_node_url] = root_node.connections.get(new_node_url, 0) + 1

            # if we haven't yet seen this url
            if new_node_url not in self.queue and new_node_url not in self.explored:
                # adds new node to queue to be explored
                self.queue.append(new_node_url)

        # gives the root node its link level
        root_node.link_level = self.get_link_level(root_node.curr_url, self.end_url_index)

        # add the node we just explored to our graph
        # adds current node to our explored dictionary
        # updates our json output to include this node
        self.url_map[root_node.curr_url] = root_node.connections 
        self.explored[root_node.curr_url] = 1 
        self.update_json(root_node)

    # bfs to find all nodes from the given url
    def create_map(self, total_iterations=-1):
        ## total_iterations usage SHOULD BE UPDATED AS IT IS NOT PROPER STYLE

        # bfs will stop when iteration == total_iterations,
        # if total_iteration is negative we will continue until we have exhausted the queue
        iteration = 0  
        while self.queue and iteration != total_iterations:
            current_node_url = self.queue.pop(0) 
            # print(current_node_url)

            # check if url has been explored yet
            if self.explored.get(current_node_url, 0) == 0:
                html = self.get_html(current_node_url)
                self.get_links(current_node_url, html)
                ## ATTEMPT TO USE MULTITHREADING HERE

            iteration += 1
        # print("done")

    # updates json file with new node
    def update_json(self, root_node):
        root_node.json["url"] = root_node.curr_url
        url_links = [{"url_link": key, "times_linked": val}
                     for key, val in root_node.connections.items()]
        root_node.json["url_links"] = url_links
        # root_node.json["url_links"] = root_node.connections
        # root_node.json["files"] = root_node.files
        # root_node.json["ip"] = root_node.ip
        # root_node.json["html"] = root_node.html
        self.json_list.append(root_node.json)
        # print(self.url_map)

        root_node.json_node["id"] = root_node.curr_url
        # root_node.json_node["group"] = root_node.level #  this should return the bfs level
        self.json_nodes_list.append(root_node.json_node)

        for key, val in root_node.connections.items():
            self.json_links_list.append({"source": root_node.curr_url, "target": key, "value": val})
        # self.json_links_list.append(root_node.json_links)

    # returns the map we have created
    def get_map(self):
        return self.url_map

    # gets html dynamically or standard
    # dynamically takes significantly longer
    # but is truer to the actual html of the page
    # standard is faster but might not represent
    # the actual contents of the page
    def get_html(self, url):
        if self.dynamic_pages:
            # gets dynamically loaded html
            html = ezScrape.getHTML(url, self.path)
        else:
            # gets regular html (might not be 100% accurate)
            html = requests.get(url).text 
        return html

    # gets the link level of the given node
    # (how many / it contains compared to base url)
    ## THIS COULD USE SOME MODIFICATION
    def get_link_level(self, url, base_url_index):
        ending_url = url[base_url_index:]
        return ending_url.count("/")

# a node containing the links a url contains
# along with other data it might have
class UrlNode: 
    def __init__(self, curr_url, html="", ip="", files=[], bfs_level=0, link_level=0):
        self.curr_url = curr_url # this nodes url
        self.connections = {} # this nodes outgoing links
        self.html = html # this nodes html
        self.files = files # the filenames in this nodes html
        self.ip = ip # this nodes ip
        self.json = {} # this node formatted to json
        self.json_links = []
        self.json_node = {}
        self.bfs_level = bfs_level # level of bfs the node was discovered on
        self.link_level = link_level # number of links away from base url

