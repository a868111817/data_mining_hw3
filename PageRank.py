import numpy as np
from optparse import OptionParser 
import networkx as nx
import pandas as pd

def PageRank(graph, iterations):

    tolarance=1.0e-8
    d = 0.15
    n = graph.number_of_nodes()
    dd = d / n
    rank = dict.fromkeys(graph, 1.0 / n)

    for t in range(iterations):
        lastRank = rank

        for node in rank:
            rankSum = 0
            neighbors = graph.out_edges(node)
            for n in neighbors:
                outlinks = len(graph.out_edges(n[1]))
                if outlinks > 0:
                    rankSum += (1.0 / outlinks) * lastRank[n[1]]
            rank[node] = dd + ((1 - d) * rankSum)

        err = sum([(lastRank[node] - rank[node]) for node in rank])
        if (err  < tolarance):
            break   

    return rank   

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

    page_rank = PageRank(G,5)
    page_rank = np.array(list(page_rank.values()))

    np.savetxt(f'result/{options.input_file}/{options.input_file}_PageRank.txt', [page_rank],fmt='%10.5f')