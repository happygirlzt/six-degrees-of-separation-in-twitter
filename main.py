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

users=np.zeros((40000, 1))

user_friends={}
user_tags={}
max_friends=0
min_friends=200000
tag_users={}


def more_tags(s):
    return s[-1]!=']'

def remove_hashtag(raw_str):
  return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",raw_str).split())

############### Generate User:Tags Map ###########################
start=time.time()

def preprocess():
    with open('./data/data.csv', 'r') as infile:
        reader = csv.reader(infile)
        count=-1
        
        for row in reader:
            count += 1

            if count == 0:
                continue
            id=row[0]

            users[count-1][0]=id
            screenName=row[1]
            
            many_tags=more_tags(row[2])
            
            offset=0

            if many_tags:
                this_tags=[]
                for j in range(20):
                    this_tags.append(row[2+j].strip('[]').strip(''))
                    if row[2+j][-1]==']':
                        break
                user_tags[id]=this_tags
                offset=len(this_tags)-1
            else:
                user_tags[id]=row[2].strip('[]').strip('')
                
            friendsCount=int(row[5+offset])

            max_friends=max(max_friends,friendsCount)
            min_friends=min(min_friends,friendsCount)
            friends=row[9+offset:]
            friends[0]=friends[0].strip('[]')
            friends[-1]=friends[-1].strip('[]')
            friends=[i.replace('"', '') for i in friends]
            friends=[i.strip() for i in friends]
            user_friends[id]=friends

end=time.time()
print('Spent {} seconds to preprocess the data'.format(end-start))

############### Generate/Read all tags #######################
try:
  all_tags=pd.read_csv('./data/all_tags_saved.csv')
except:
  all_tags=set()

  for u in user_tags:
    tags=user_tags[u]

    if type(tags) == str:
      all_tags.add(remove_hashtag(tags))
    else:
      for tag in tags:
        all_tags.add(remove_hashtag(tag))

  pd.DataFrame(list(all_tags)).to_csv('./data/all_tags_saved.csv')

################# Generate Tag:User Map #######################
def generate_tag_users():
  for u in user_tags:
    tags=user_tags[u]
    if type(tags)==str:
        normalized_tag=remove_hashtag(tags)
        if normalized_tag in tag_users:
            cur_tags=tag_users[normalized_tag]
            cur_tags.append(u)
            tag_users[normalized_tag]=cur_tags
        else:
            cur_tags=[]
            cur_tags.append(u)
            tag_users[normalized_tag]=cur_tags
    else:
        for tag in tags:
            normalized_tag=remove_hashtag(tag)
            if normalized_tag in tag_users:
                cur_tags=tag_users[normalized_tag]
                cur_tags.append(u)
                tag_users[normalized_tag]=cur_tags
            else:
                cur_tags=[]
                cur_tags.append(u)
                tag_users[normalized_tag]=cur_tags


x=list(tag_users.keys())
y=[len(item) for item in tag_users.values()]

tag_nums=pd.DataFrame({'tags':x,'num':y})
plt.plot(x[:5], y[:5],'go-', label='line 1', linewidth=2)
plt.savefig('tag_distribution.png')

# Generate the nodes and edges
nodes=user_friends.keys()

node_list=list(nodes)

with open('./data/nodelist.txt', 'w') as filehandle:
    for listitem in node_list:
        filehandle.write('%s\n' % listitem)

# Calculate Six Degree under the same tag 'nationaldogday'
# Step 1: Get the intersaction
national_users=set(tag_users['nationaldogday'])
all_users=set(user_friends.keys())
common_users=national_users.intersection(all_users)

################## Read the graph ##########################

begin=time.time()
try:
    # nx.write_gpickle(G,"test.gpickle")
    # Read from pickle
    G=nx.read_gpickle("./data/test.gpickle")
    end=time.time()
    print('Spent {} in reading graph'.format(end-begin))
except:
    
    G=nx.Graph()

    edges=[]

    for u in user_friends:
        for v in user_friends[u]:
            edges.append(tuple((u,v)))

    # Save edges
    with open('./data/twitter_edges.edgelist', 'w') as fp:
        fp.write('\n'.join('%s %s' % x for x in edges))
    
    G.add_edges_from(edges)

############### Sample 5000 nodes ########################
# Calculate the shortest path
k=5000
k_nodes=[]

for i in range(k):

  n1=random.choice(node_list)
  k_nodes.append(n1)

print('Finished sampling')

remain_nodes=list(set(nodes)-set(k_nodes))

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