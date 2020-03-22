import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

######### Please download the result from 
## https://drive.google.com/drive/folders/151u_rRMOXfBAdZVeJ5ZUrtnUalqgz4IX?usp=sharing

shortest_dist_list = pd.read_csv('./your_result_folder/5000_shortest_dist.txt', names=['dist'], sep=" ", header=None)

print(shortest_dist_list['dist'].value_counts())
print(shortest_dist_list.describe())

sd_count=shortest_dist_list['dist'].value_counts().rename_axis('shortest_dist').reset_index(name='counts')

x=sd_count['shortest_dist']
y=sd_count['counts']
fig, axes = plt.subplots(figsize=(7,5), dpi=100)
plt.bar(x, height=y)

degree_greater_than_6=sd_count.loc[sd_count['shortest_dist'] > 6]
print(degree_greater_than_6)

degree_greater_than_6_count=degree_greater_than_6['counts'].sum()
print(degree_greater_than_6_count)

degree_less_than_6=sd_count.loc[sd_count['shortest_dist']<6]
print(degree_less_than_6)

degree_less_than_6_count=degree_less_than_6['counts'].sum()
print(degree_less_than_6_count)

degree_equal_to_6=sd_count.loc[sd_count['shortest_dist']==6]
print(degree_equal_to_6)
degree_equal_to_6_count=degree_equal_to_6['counts'].sum()
print(degree_equal_to_6_count)

# Visualization
x_dist=['Smaller than 6', 'Equal to 6', 'Larger than 6']
y_count=[degree_less_than_6_count,degree_equal_to_6_count,degree_greater_than_6_count]
fig, axes = plt.subplots(figsize=(7,5), dpi=100)
plt.plot(x_dist, y_count,'go-', label='line 1', linewidth=2)

#kwargs = dict(alpha=0.5, bins=100)
#plt.hist(y_count, **kwargs, color='g', label='Ideal')
# bar chart
fig, axes = plt.subplots(figsize=(7,5), dpi=100)
plt.bar(x_dist, height=y_count)

shortest_dist_list.describe()