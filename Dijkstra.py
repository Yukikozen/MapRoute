import math

from collections import defaultdict

MAX_WALK_RANGE = 0.08  # km
WALK_SPEED = 5.0  # km
BUS_SPEED = 30.0  # km
MRT_SPEED = 80.0  # km

class Dijkstra:

    # constructor to recieve a dictionary of nodes. (key = string name, value = [lat,long])
    def __init__(self, nodes):
        self.nodes = nodes
        self.edges = []
        self.busnodes = {}
        self.busroutes = {}
        self.mrtnodes = {}
        self.mrtroutes = {}

    # function called by main.py after creating busedges, busnodes, and busroutes.
    # this functions adds bus edges into the existing edges.
    def create_bus_edgenodes(self, edges, busnodes, busroutes):
        self.edges = self.edges + edges
        self.busnodes = busnodes
        self.busroutes = busroutes

    # function called by main.py after creating MRTedges, MRTnodes, and MRTroutes.
    # this functions adds bus edges into the existing edges.
    def create_mrt_edgenodes(self, edges, mrtnodes, mrtroutes):
        self.edges = self.edges + edges
        self.mrtnodes = mrtnodes
        self.mrtroutes = mrtroutes

    # to be called by gui to create edges
    def create_edges(self):
        # for every node in the dictionary of nodes
        for k1, v1 in self.nodes.items():
            # checks all the nodes in the dictionary of they are neighbor
            for k2, v2 in self.nodes.items():
                # checks if the two nodes are neighbor, if true then create a walking edge between the 2 of them.
                edge = add_neighbour(k1, v1, k2, v2)
                if edge is not None:
                    self.edges.append(edge)

    # to be called by gui
    # builds a graph which contains a dictionary of all the nodes with a list of edges as their values.
    def build_graph(self):
        graph = defaultdict(list)
        seen_edges = defaultdict(int)

        # for every edge in the list of edges
        for src, dst, weight, mode in self.edges:
            # checking for duplicated edge entries
            seen_edges[(src, dst, weight)] += 1
            if seen_edges[(src, dst, weight)] > 1:  # dont add to graph if duplicated
                continue
            graph[src].append([dst, weight, mode]) # add edge to graph

        return graph

    # to be called by gui
    # builds a graph which contains a dictionary of all the nodes with a list of edges as their values.
    def build_MRTgraph(self):
        graph = defaultdict(list)
        seen_edges = defaultdict(int)

        # for every edge in the list of edges
        for src, dst, weight, mode in self.edges:
            # checking for duplicated edge entries
            seen_edges[(src, dst, weight)] += 1
            if seen_edges[(src, dst, weight)] > 1:  # dont add to graph if duplicated
                continue
            graph[src].append([dst, weight, mode]) # add edge to graph
            # remove this line of edge list is directed
            graph[dst].append([src, weight, mode])

        return graph

    # function to be called by gui to find path from src to dst, returns a list of coordinates for plotting lines
    def find_shortest_path(self, graph, src, dst):
        d, prev = dijkstra(graph, src, dst)
        path = find_path(prev, [dst, 'walk'])
        newpath = []
        print(path)

        # for every node in the path , get the coordinates of the node and add it into newpath
        # swap is used to change the order of long, lat to lat, long
        for x in path:
            if x[0] in self.nodes:
                newpath.append(swap(self.nodes[x[0]]))
            elif x[0] in self.busnodes:
                newpath.append(swap(self.busnodes[x[0]]))
            elif x[0] in self.mrtnodes:
                newpath.append(swap(self.mrtnodes[x[0]]))
            elif x[1] == "LRT":
                newpath.append(swap(self.mrtroutes[x[0]]))
            else:
                newpath.append(swap(self.busroutes[x[0]]))
        return newpath


# checks if it is a neighbour then return an edge , [src, dest,weight,modeoftravel]. Else return none


def add_neighbour(k1, v1, k2, v2):
    # If it is within walking distance then there is an edge between the 2 points
    distance = calc_distance(v1, v2)
    if distance < MAX_WALK_RANGE:
        return [k1, k2, distance, 'walk']


# to be called by gui after calling build graph
# generate the shortest graph based on the src
def dijkstra(graph, src, dst=None):
    nodes = []
    for n in graph:
        nodes.append(n)
        nodes += [x[0] for x in graph[n]]

    # create a queue of the nodes
    q = set(nodes)
    nodes = list(q)

    # create a dictionary for prev and distance
    dist = dict()
    prev = dict()

    # set every node to unvisted (infinity cost)
    for n in nodes:
        dist[n] = float('inf')
        prev[n] = None

    dist[src] = 0 # initialise starting point as 0 cost

    # while the queue is not empty
    while q:
        u = min(q, key=dist.get) # get the lowest cost out of all the edges
        q.remove(u) # remove the first item

        # if the item removed is the destination then return the distance and all the previous nodes taken
        if dst is not None and u == dst:
            return dist[dst], prev

        # From the neighbouring node with the lowest cost, get a list of all of its edges
        for v, w, mode in graph.get(u, []):

            # add the weight of the edge into the existing cost
            alt = dist[u] + w
            # checks if the cost is lesser then the previously existing cost
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = [u, mode]

    return dist, prev


def find_path(pr, node):  # generate path list based on parent points 'prev'
    p = []

    while node is not None:
        p.append(node)
        node = pr[node[0]]
    return p[::-1]


# swaps coordinates
def swap(coord):
    return [coord[1], coord[0]]


# returns the midpoint of the polygon coordinates
def find_midpoint(L):
    lat = []
    long = []
    for l in L[0]:
        lat.append(l[0])
        long.append(l[1])

    return [sum(lat) / len(lat), sum(long) / len(long)]


# Receives 2 list/tuple of coordinates, (srclat,srclong)(destLat,destLong), returns the distance between 2 points
# Calculate distance between two location using coordinates
def calc_distance(src, dest):
    lat1, lon1 = src
    lat2, lon2 = dest
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d

