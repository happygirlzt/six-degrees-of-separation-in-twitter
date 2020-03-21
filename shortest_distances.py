import pandas as pd
import numpy as np
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
G=nx.read_gpickle('test.gpickle')

print('Finished Reading')

## Edge list :https://drive.google.com/file/d/1hq-7hOgGZzkEPhxphy4u6ZiMnEJDhLkQ/view?usp=sharing

## Graph: https://drive.google.com/file/d/1tWQljCNCyV01DQrK3tGHlogCiAEqgXI9/view?usp=sharing

node_list=[line.rstrip('\n') for line in open('./data/nodelist.txt')]

############### Calculate the shortest paths #############

k=5000
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
      s_path=nx.shortest_path_length(G,a,b)
      shortest_path_list.append((a,b,s_path))
      shortest_dist.append(s_path)

    except:
      no_paths.append((a,b))

  with open('./data/%s_shortest_path.txt'%k,'a+') as fp:
      fp.write('\n'.join('%s %s %s'%x for x in shortest_path_list))

  with open('./data/%s_no_path.txt'%k,'a+') as fp:
      fp.write('\n'.join('%s %s'%x for x in no_paths))

  with open('./data/%s_shortest_dist.txt'%k,'a+') as fp:
      fp.write('\n'.join('%s'%x for x in shortest_dist))

  print('Finished {} node'.format(count))
  count+=1
