# Jack Tilley
# January 2020
# The purpose of this module is to scrape the links from a website and find all links that the website contains
# This module combines with mapdisplay.py to show the networking of the site

from webscraping_tools import ezScrape
from bs4 import BeautifulSoup
import requests


class UrlMap:  # a graph containing the links a website has, links in the form of UrlNode
    def __init__(self, base_url, path,starting_url="", url_map={}, local_only=True, dynamic_pages=False):
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
        self.stop_flag = False

    def get_links(self, url, html):  # finds all the links on the specified url
        root_node = UrlNode(url)
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a")

        for link in links:
            new_node_url = link.get("href")  # collects link

            if new_node_url is None:  # link is broken or missing, do nothing
                continue

            if new_node_url.startswith("/"):  # node stays within current site
                new_node_url = self.base_url + new_node_url
            elif new_node_url.startswith("http"):  # node leads to another site
                if self.local_only:
                    continue
                else:
                    new_node_url = new_node_url
            else:  # unidentified url, do nothing
                continue

            # print(new_node_url)

            # self.seen_nodes[new_node_url] = self.seen_nodes.get(new_node_url, 0) + 1
            #  adds new node to our seen collection, inc times seen

            root_node.connections[new_node_url] = root_node.connections.get(new_node_url, 0) + 1
            # adds new node to root_nodes connections, inc times seen

            if new_node_url not in self.queue and new_node_url not in self.explored:
                # adds new node to queue to be explored
                self.queue.append(new_node_url)

        self.url_map[root_node.curr_url] = root_node.connections  # add the node we just explored to our graph
        self.explored[root_node.curr_url] = 1  # adds current node to our explored dictionary
        # print(self.url_map)

    def create_map(self, total_iterations=-1):  # bfs to find all nodes
        iteration = 0  # bfs will stop when iteration == total_iterations,
        # if total_iteration is negative we will continue until we have exhausted the queue
        while self.queue and iteration != total_iterations:
            current_node_url = self.queue.pop(0)  # get top node in queue
            # print(current_node_url)
            if self.explored.get(current_node_url, 0) == 0:  # check if url has been explored yet
                html = self.get_html(current_node_url)
                self.get_links(current_node_url, html)  # get each link from that url
                ## attempt to use multithreading

            iteration += 1
        # print("done")

    def get_map(self):
        return self.url_map

    def get_html(self, url):
        if self.dynamic_pages:
            html = ezScrape.getHTML(url, self.path)  # gets dynamically loaded html
        else:
            html = requests.get(url).text  # gets regular html (might not be 100% accurate)
        return html


class UrlNode:  # a node containing the links a url contains
    def __init__(self, curr_url, html, ip, files=[]):
        self.curr_url = curr_url
        self.connections = {}
        self.html = html
        self.files = files
        self.ip = ip

