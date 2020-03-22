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
G=nx.read_gpickle('./data/test.gpickle')

print('Finished Reading')

## Edge list :https://drive.google.com/file/d/1hq-7hOgGZzkEPhxphy4u6ZiMnEJDhLkQ/view?usp=sharing

## Graph: https://drive.google.com/file/d/1tWQljCNCyV01DQrK3tGHlogCiAEqgXI9/view?usp=sharing


## Node list: https://drive.google.com/file/d/1-w1v0e3RxvocZPJpOZOXUKpOI5xschwN/view?usp=sharing

node_list=[line.rstrip('\n') for line in open('./data/nodelist.txt')]

############### Sampling k nodes #############

k=5000
k_nodes=set()

while len(k_nodes)<k:
  n1=random.choice(node_list)
  if n1 not in k_nodes:
      k_nodes.add(n1)

print('Finished sampling {} nodes'.format(k))

k_nodes=list(k_nodes)

count=1
pairs_count=0

############# Calculate the shortest paths #######
for index_a in range(k):
  no_paths=[]
  shortest_path_list=[]
  shortest_dist=[]

  for index_b in range(index_a+1,k):
    pairs_count+=1
    a=k_nodes[index_a]
    b=k_nodes[index_b]

    try:
      s_path=nx.shortest_path_length(G,a,b)
      shortest_path_list.append((a,b,s_path))
      shortest_dist.append(s_path)

    except:
      no_paths.append((a,b))

  with open('./data/real_%s_shortest_path.txt'%k,'a+') as fp:
      fp.write('\n'.join('%s %s %s'%x for x in shortest_path_list))

  with open('./data/real_%s_no_path.txt'%k,'a+') as fp:
      fp.write('\n'.join('%s %s'%x for x in no_paths))

  with open('./data/real_%s_shortest_dist.txt'%k,'a+') as fp:
      fp.write('\n'.join('%s'%x for x in shortest_dist))

  print('Finished {} node'.format(count))
  count+=1
