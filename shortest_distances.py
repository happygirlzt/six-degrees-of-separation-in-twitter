import pandas as pd
import numpy as np
import ast
import csv
import time
import re
import random

from operator import itemgetter
import networkx as nx
from networkx.algorithms import community

import matplotlib.pyplot as plt

################ Read Graph and nodes ####################
G=nx.read_gpickle('/data/test.gpickle')
node_list=[line.rstrip('\n') for line in open('/data/nodelist.txt')]

############### Calculate the shortest paths #############

k=5000
k_nodes=[]

for i in range(k):
  n1=random.choice(node_list)
  k_nodes.append(n1)

print('Finished sampling')

remain_nodes=list(set(node_list)-set(k_nodes))

no_path=[]
shortest_path_list=[]
shortest_dist=[]
pairs_count=0

for a in k_nodes:
  for b in remain_nodes:
    pairs_count+=1

    try:
      s_path=nx.shortest_path(G,a,b)
      shortest_path_list.append((a,b,s_path))
      shortest_dist.append(s_path)

    except:
      no_path.append((a,b))