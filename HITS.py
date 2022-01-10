import numpy as np
from optparse import OptionParser 
import networkx as nx
import pandas as pd

def norm(x):
    return np.abs(x).sum(axis=0)

def HITS(graph,iterations):

    hubs = dict.fromkeys(graph, 1.0 )
    auth = dict.fromkeys(graph, 1.0 )
    tolarance=1.0e-8

    for t in range(iterations):
        lastHubs = hubs
        lastAuth = auth
        hubs = dict.fromkeys(lastHubs.keys(), 0)
        auth = dict.fromkeys(lastHubs.keys(), 0)

        for node in auth:
            for neighbor in graph[node]:
                auth[neighbor] += lastHubs[node] * graph[node][neighbor].get('weight', 1)
        for node in hubs:
            for neighbor in graph[node]:
                hubs[node] += auth[neighbor] * graph[node][neighbor].get('weight', 1)

        authNorm = 0
        hubsNorm = 0
        
        authNorm = norm(np.array([val for val in auth.values()]))
        hubsNorm = norm(np.array([val for val in hubs.values()]))

        auth = {key:auth[key]/authNorm for key in auth.keys()}
        hubs = {key:hubs[key]/hubsNorm for key in hubs.keys()}
        
        err = sum([(auth[node] - lastAuth[node]) for node in auth]) + sum([abs(hubs[node] - lastHubs[node]) for node in hubs])
        if (err  < tolarance):
            break
        
    return auth, hubs
    
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
    
    auth, hubs = HITS(G,5)

    auth = np.array(list(auth.values()))
    hubs = np.array(list(hubs.values()))

    np.savetxt(f'result/{options.input_file}/{options.input_file}_HITS_authority.txt', [auth],fmt='%10.3f')
    np.savetxt(f'result/{options.input_file}/{options.input_file}_HITS_hub.txt', [hubs],fmt='%10.3f')