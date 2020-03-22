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

### Please download the graph model from 
### https://drive.google.com/file/d/1tWQljCNCyV01DQrK3tGHlogCiAEqgXI9/view?usp=sharing
G=nx.read_gpickle('./your_data_folder/test.gpicklse')
print('Finished Reading')

################ Generate Tags ##########################
user_friends={}
user_tags={}
max_friends=0
min_friends=200000
tag_users={}


def hasMoreTags(s):
    return s[-1]!=']'

start=time.time()
with open('./data/data.csv', 'r') as infile:
    reader = csv.reader(infile)
    count=-1
    
    for row in reader:
        count += 1
        if count == 0:
            continue
        id=row[0]
        #print(count)
        users[count-1][0]=id
        screenName=row[1]
        
        many_tags=hasMoreTags(row[2])
        
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
print('Spent {} seconds processing'.format(end-start))

def remove_hashtag(raw_str):
  return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",raw_str).split())


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

# Sort by the num of each tag
sorted_tag_nums=tag_nums.sort_values(by=['num'], ascending=[0])
sorted_tag_nums[:10]

sorted_x=sorted_tag_nums['tags'][:5]
sorted_y=sorted_tag_nums['num'][:5]

def calculate_shortest_dist(this_tag):
  count=1
  for a in k_nodes:

    no_paths=[]
    shortest_path_list=[]
    shortest_dist=[]

    for b in k_nodes:
      if a==b:
        continue

      try:
        s_path=nx.shortest_path_length(G,a,b)
        shortest_path_list.append((a,b,s_path))
        shortest_dist.append(s_path)

      except:
        no_paths.append((a,b))

    with open('/content/drive/My Drive/%s_shortest_path.txt'%this_tag,'a+') as fp:
        fp.write('\n'.join('%s %s %s'%x for x in shortest_path_list))

    with open('/content/drive/My Drive/%s_no_path.txt'%this_tag,'a+') as fp:
        fp.write('\n'.join('%s %s'%x for x in no_paths))

    with open('/content/drive/My Drive/%s_shortest_dist.txt'%this_tag,'a+') as fp:
        fp.write('\n'.join('%s'%x for x in shortest_dist))

    print('Finished {} node'.format(count))
    count+=1

# Calculate Six Degree under the
# Step 1: Get the intersaction
top_tags=list(sorted_x)

# Sample 200 user from top 5 tags to calculate 6 degree
k=200


for this_tag in top_tags:
  this_tag_users=set(tag_users[this_tag])
  this_tag_users_list=list(this_tag_users)
  k_nodes=[]

  for i in range(k):
    n1=random.choice(this_tag_users_list)
    k_nodes.append(n1)

  calculate_shortest_dist(this_tag)

# Analyze top 5 tag
for this_tag in top_tags:

   shortest_dist_list = pd.read_csv('./data/%s_shortest_dist.txt'%this_tag, names=['dist'], sep=" ", header=None)
   print(this_tag)
   print(shortest_dist_list['dist'].value_counts())
   print(shortest_dist_list.describe())