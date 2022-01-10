from collections import defaultdict
import copy
import numpy as np
from optparse import OptionParser 
import networkx as nx
import pandas as pd

def _isConverge(s1, s2, eps=1e-4):
    for i in s1.keys():
        for j in s1[i].keys():
            if abs(s1[i][j] - s2[i][j]) >= eps:
                return False
    return True

def simrank(graph, c=0.9, maxIter=100):
    # init. vars
    simOld = defaultdict(list)
    sim = defaultdict(list)
    for n in graph.nodes():
        sim[n] = defaultdict(int)
        sim[n][n] = 1
        simOld[n] = defaultdict(int)
        simOld[n][n] = 0

    # recursively calculate simrank
    for iterCtr in range(maxIter):
        if _isConverge(sim, simOld):
            break
    simOld = copy.deepcopy(sim)
    for u in graph.nodes():
        for v in graph.nodes():
            if u == v:
                continue
            sUV = 0.0
            
            uNeighbors = len(list(graph.predecessors(u)))
            vNeighbors = len(list(graph.predecessors(v)))
            if (uNeighbors == 0 or vNeighbors == 0):
                continue
            for nU in graph.predecessors(u):
                for nV in graph.predecessors(v):
                    sUV += simOld[nU][nV]
            sim[u][v] = (c * sUV / (uNeighbors * vNeighbors))
    return sim

if __name__ == '__main__':

    parser = OptionParser() 
    parser.add_option('-f', '--input_file',
                         dest='input_file',
                         help='CSV filename',
                         default='graph_1')
    
    (options, args) = parser.parse_args()

    file_name = options.input_file + '.txt'
    file_path = 'hw3dataset/' + file_name

    G = nx.DiGraph()
    G.add_edges_from(pd.read_csv(file_path, header=None).to_numpy())

    sim = simrank(G)
    sim = pd.DataFrame(data=sim)

    np.savetxt(f'result/{options.input_file}/{options.input_file}_SimRank ..txt', sim,fmt='%10.5f')