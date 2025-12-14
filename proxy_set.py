# BEFORE YOU USE PROXY_SET, YOU NEED A NATIVE PROXY
import logging
import time
from collections import deque

# ref: https://en.clash.wiki/runtime/external-controller.html

import requests

import block_detector

BASE_URL = "http://127.0.0.1:9890"
SECRET = "123456"
HEADERS = {"Authorization": f"Bearer {SECRET}"}
PROXY_NAME = "GLOBAL"

# a auto proxy's node switching strategy: using latest unused node like queue
node_pool = deque()


# rule > proxy > node

# get all proxies
def get_all_proxies():
    return requests.get(f"{BASE_URL}/proxies", headers=HEADERS).json()


# get current connection group
def get_current_connection_group():
    r = requests.get(f"{BASE_URL}/connections", headers=HEADERS).json()
    logging.info(f"current connection group is: {r}")
    return r


# get all nodes
def get_nodes_all():
    r = requests.get(f"{BASE_URL}/proxies", headers=HEADERS).json()
    logging.info(f"all nodes [{r}] queried")
    return r


# get specific proxy's nodes
def get_nodes_specific_by_proxy(proxy_name):
    r = requests.get(f"{BASE_URL}/proxies/{proxy_name}", headers=HEADERS).json()
    # delete 'Direct' and 'Reject'
    r = r['all'][2:]
    logging.info(f"all nodes [{r}] queried")
    return r


# get node under a specific selector
def get_node(node_name):
    data = {"name": node_name}
    logging.info(f"node [{data}] got")
    return requests.get(f"{BASE_URL}/proxies/{PROXY_NAME}", headers=HEADERS, json=data).json()


# shift node under a specific selector
def switch_node(node_name):
    data = {"name": node_name}
    logging.info(f"node [{data}] selected")
    return requests.put(f"{BASE_URL}/proxies/{PROXY_NAME}", headers=HEADERS, json=data)


# auto detecting & shifting
def auto_handle_proxy(agent):
    # detect if blocked by website
    if block_detector.is_blocked(agent):
        logging.warning("Page Blocked, switching proxy...")
        # popleft & append to the end
        temp_node = node_pool.popleft()
        node_pool.append(temp_node)
        # re-pickup the head
        switch_node(node_pool[0])
        time.sleep(5)


# init the node pool and pick switch a HEAD node
def init_node_pool():
    # get GLOBAL's all nodes
    node_list = get_nodes_specific_by_proxy(PROXY_NAME)
    # import all nodes into a deque
    node_pool.extend(node_list)
    logging.warning(f"node_pool init succeed: {node_pool}")
    # pick up a HEAD node
    switch_node(node_pool[0])
    logging.info(f"node [{node_pool[0]}] picked up")
