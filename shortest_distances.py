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
print('Starting Reading the graph...')
G=nx.read_gpickle('./data/test.gpickle')
print('Finished Reading')
node_list=[line.rstrip('\n') for line in open('./data/nodelist.txt')]

############### Calculate the shortest paths #############

k=1000
k_nodes=[]

for i in range(k):
  n1=random.choice(node_list)
  k_nodes.append(n1)

print('Finished sampling {} nodes'.format(k))

#remain_nodes=list(set(node_list)-set(k_nodes))

count=1
pairs_count=0

for a in k_nodes:
  no_paths=[]
  shortest_path_list=[]
  shortest_dist=[]

  for b in k_nodes:
    if a == b:
      continue

    pairs_count+=1

    try:
      s_path=nx.shortest_path(G,a,b)
      shortest_path_list.append((a,b,s_path))
      shortest_dist.append(s_path)

    except:
      no_paths.append((a,b))

  with open('./data/shortest_path.txt','a+') as fp:
      fp.write('\n'.join('%s %s %s'%x for x in shortest_path_list))

  with open('./data/no_path.txt','a+') as fp:
      fp.write('\n'.join('%s %s'%x for x in no_paths))

  with open('./data/shortest_dist.txt','a+') as fp:
      fp.write('\n'.join('%s'%x for x in shortest_dist))

  print('Finished {} node'.format(count))
  count+=1
