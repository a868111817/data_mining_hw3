import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser 
from HITS import HITS
from PageRank import PageRank
from SimRank import simrank

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

    print('Authority:\n',auth)
    print('Hub:\n',hubs)

    page_rank = PageRank(G,5)
    page_rank = np.array(list(page_rank.values()))
    print('PageRank:\n',page_rank)

    sim = simrank(G)
    sim = pd.DataFrame(data=sim)
    print('SimRank:\n')
    print(sim)