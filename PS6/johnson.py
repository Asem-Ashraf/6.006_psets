INF = 99999  # distance magnitudes will not be larger than this number
import copy

# weight function example
# W1 = {0: {1: -2},               W2 = {0: {1: 1, 3: 2, 4: -1},
#       1: {2: 0},                      1: {0: 1},
#       2: {0: 1},                      2: {3: 0},
#       3: {4: 3}}                      3: {0: 2, 2: 0},
#                                       4: {0: -1}}


def johnson(n, S):
    '''
    Input:  n | Number of vertices in the graph
            S | Tuple of triples (u, v, www) representing edge (u, v) of weight www
    Output: D | Tuple of tuples where D[u][v] is the distance from u to v
              |   or INF if v is not reachable from u
              |   or None if the input graph contains a negative-weight cycle
    '''
    D = [[INF for _ in range(n)] for _ in range(n)]
    ttt = [[INF for _ in range(n)] for _ in range(n)] # made to temporary take the output of the dijkstra function

    Adj, www, s, adjs, ws = superNodeGraph(S, n)

    def ww(u, v):
        if v in ws[u]:
            return ws[u][v]
        else : return INF

    t=()
    t = bellman_ford(adjs, ww, s)
    if t is None:
        return None

    WWW = copy.deepcopy(www)
    def W(u, v):
        if v in WWW[u]:
            return WWW[u][v]
        else: return INF

    for node in range(n):
        for i in list(WWW[node]):
            WWW[node][i] = WWW[node][i] + abs(t[0][i]) - abs(t[0][node])

    for node in range(n):
            ttt[node], P = dijkstra(Adj, W, node)
            dd=weightsByParent(www,P,n,node)
            D[node]=dd

    D = tuple(tuple(row) for row in D)
    return D


def weightsByParent(w,p,n,source):
    '''
        given the weight function |w|, the parent tree of shortest path to a single source |p|, the source |source| and the number of nodes |n|
        returns the weight of the shortest path from every vertex to the source
    '''

    d=[INF for _ in range(n)] # all distances are infinity
    for k in range(n): # for every node
        i=k
        if p[i]== None: # if the parent is none
            if i==source: # then by design it is either the source
                d[i]=0
            else:          # or
                d[i]=INF   # the node is unreachable form the source
        else :             # if reachable then
            delta = 0      # initialize the distance variable
            for _ in range(n):  # loop for at most the number of nodes in the graph
                parent = p[i]   # trace back from the node in the shortest path tree
                if parent == source:  # till we find the source then we r done with our path
                    delta+=w[source][i]
                    break
                else:
                    delta=delta+w[parent][i]
                    i=parent
            d[k]=delta
    return d

def superNodeGraph(S, n):
    '''
    input:    S | Tuple of triples (u, v, w) representing edge (u, v) of weight w
              n | Number of vertices in the graph
    output: Adj | Direct access array mapping a vertex to a list of adjacencies
              w | Function w(u, v): weight of the edge from u to v
              s | supernode in the graph Adj
           Adjs | Direct access array mapping a vertex to a list of adjacencies with the supernode
             ws | Function w(u, v): weight of the edge from u to v with the supernode
    '''
    Adj, w = edgesToAdj(S, n) # this is the adjacency map and weight function of the graph before adding the supernode

    ADJs=copy.deepcopy(Adj)
    Ws=copy.deepcopy(w)
    ADJs.append([]) # this is the adjacency map after adding the supernode
    Ws[n]={} # this is the weight function after adding the supernode
    for i in range(n):
        edge=(n,i,0)
        ADJs[edge[0]].append(edge[1])
        Ws[edge[0]][edge[1]] = edge[2]
    return Adj, w, n, ADJs, Ws


def edgesToAdj(S, n):
    '''
        input:    S | an edge list of a graph
                  n | the number of vertices in the graph
        output: Adj | Direct access array mapping a vertex to a list of adjacencies
                  w | Function w(u, v): weight of the edge from u to v
    '''

    # there is n nodes in the graph initially they are not connected to anything
    Adj = [[] for _ in range(n)]
    # there are n nodes that could have n weights
    w = {}
    for i in range(n):
        w[i]={}
    # input sample: ((0, 1, -1), (0, 2, -2), (1, 3, -5), (2, 1, -3), (2, 3, -4))
    for edge in S: # get the data from each edge and put it in the form of the adj map and weight function
        Adj[edge[0]].append(edge[1])
        w[edge[0]][edge[1]] = edge[2]
    return Adj, w


####################################
# USE BUT DO NOT MODIFY CODE BELOW #
####################################
def bellman_ford(Adj, w, s):  # from R12
    '''
    Input: Adj | Direct access array mapping a vertex to a list of adjacencies
             w | Function w(u, v): weight of the edge from u to v
             s | Vertex where 0 <= s < |Adj|
    Output:  d | Direct access array mapping a vertex to distance from s
               |   or INF if v is not reachable from u
               |   or None if the input graph contains a negative-weight cycle
        parent | Direct access array mapping a vertex to parent on shortest path
    '''
    d = [INF for _ in Adj]
    parent = [None for _ in Adj]
    d[s], parent[s] = 0, None
    V = len(Adj)
    for k in range(V - 1):
        for u in range(V):
            for v in Adj[u]:
                if (d[v] > d[u] + w(u, v)) and (d[u] < INF):
                    d[v] = d[u] + w(u, v)
                    parent[v] = u
    for u in range(V):
        for v in Adj[u]:
            if d[v] > d[u] + w(u, v):
                return None
    return (d, parent)  # edited this to be able to take this or a None as output


def dijkstra(Adj, w, s):  # from R13
    '''
    Input: Adj | Direct access array mapping a vertex to a list of adjacencies
             w | Function w(u, v): non-negative weight of the edge from u to v
             s | Vertex where 0 <= s < |Adj|
    Output:  d | Direct access array mapping a vertex to distance from s
               |   or INF if v is not reachable from u
        parent | Direct access array mapping a vertex to parent on shortest path
    '''
    d = [INF for _ in Adj]
    parent = [None for _ in Adj]
    d[s], parent[s] = 0, None
    Q = PriorityQueue()
    V = len(Adj)
    for v in range(V):
        Q.insert(v, d[v])
    for _ in range(V):
        u = Q.extract_min()
        for v in Adj[u]:
            if (d[v] > d[u] + w(u, v)) and (d[u] < INF):
                d[v] = d[u] + w(u, v)
                parent[v] = u
            Q.decrease_key(v, d[v])
    return d, parent


class Item:
    def __init__(self, label, key):
        self.label, self.key = label, key


class PriorityQueue:
    def __init__(self):
        self.A = []
        self.label2idx = {}

    def min_heapify_up(self, c):
        if c == 0: return
        p = (c - 1) // 2
        if self.A[p].key > self.A[c].key:
            self.A[c], self.A[p] = self.A[p], self.A[c]
            self.label2idx[self.A[c].label] = c
            self.label2idx[self.A[p].label] = p
            self.min_heapify_up(p)

    def min_heapify_down(self, p):
        if p >= len(self.A): return
        l = 2 * p + 1
        r = 2 * p + 2
        if l >= len(self.A): l = p
        if r >= len(self.A): r = p
        c = l if self.A[r].key > self.A[l].key else r
        if self.A[p].key > self.A[c].key:
            self.A[c], self.A[p] = self.A[p], self.A[c]
            self.label2idx[self.A[c].label] = c
            self.label2idx[self.A[p].label] = p
            self.min_heapify_down(c)

    def insert(self, label, key):
        self.A.append(Item(label, key))
        idx = len(self.A) - 1
        self.label2idx[self.A[idx].label] = idx
        self.min_heapify_up(idx)

    def extract_min(self):
        self.A[0], self.A[-1] = self.A[-1], self.A[0]
        self.label2idx[self.A[0].label] = 0
        del self.label2idx[self.A[-1].label]
        min_label = self.A.pop().label
        self.min_heapify_down(0)
        return min_label

    def decrease_key(self, label, key):
        if label in self.label2idx:
            idx = self.label2idx[label]
            if key < self.A[idx].key:
                self.A[idx].key = key
                self.min_heapify_up(idx)
