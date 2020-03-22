This project is aimed to find whether the Six Degrees of Separation still holds in Twitter in two dimensions:
1. Ramdomly sample 5000 users without consider common tags.
2. Randomly sample 200 users under the top 5 mentioned tags in the dataset.

# Six Degrees of Separation
Please refer to the corresponding [Wikipedia](https://en.wikipedia.org/wiki/Six_degrees_of_separation) page for further information

# Dataset
Thanks for the [kaggle dataset](https://www.kaggle.com/hwassner/TwitterFriends)

# Experiments
## Data Preprocessing
The dataset is screwed, such as different users has different numbers of friends. CSV is not an ideal file format to save this kind of information. The first thing we did is to change the data format to some useful dictionaries. Basically, we used several dictionary for further uses:
1. user_friends: A user and his friends. We firstly built a unweighted edge list, secondly, we built a graph based on this edgelist. We leveraged the package: networkx.
2. user_tags: A user and his used tags
3. tag_users: A tag and its corresponding users. By this dictionary, we could find the top used tags in this dataset.
### Summary of this graph
- Number of nodes: 12891798
- Number of edges: 32842959
- Average degree:   5.0952

Actually, there are 40000 users in the given dataset. The reason why in total there are 12891798 users is that we treat each user's mentioned friend as a node too. For example, if user 1 has 600 friends, we treat all 600 friends are nodes.

## Calculating the shortest distancs
### Without specific tags, sampled 5000 users
We sampled 5000 users from 40000 users. And calculated the shortest distances from each user to all other 4999 users.

### With specific tags, sampled 200 users for each tag
We found that the top 10 mentioned tags were as follows:

| tags   | num  |
|---|---|
|nationaldogday  |  30513 |  
|respecttylerjoseph	|6054|
|	gloryoutnow|	600|
|	backtohogwarts	|310|
|	narcos	|269|
|steve rogers|	211|
|louisweloveyou	|142|
|bournemouth|	130|
|bundesliga	|122|
|harry potter|	103|

We sampled 200 users from each tag and calculated their shortest distances.

# Result
We could conclude that the Six Degrees of Separation still holds in Twitter. Even in a smaller context, which means to calculate the shortest paths under the same tag.

## Without specific tags
TBA


## With specific tags
### Top 1 used tag: nationaldogday
|Shortest Distance| Pair Count|
|--|--|
|2|9343|
|3|7202|
|4|2960|
|5|347|
|6|47|
|7|1|

The total pairs calculated is 19900 \\
The average degree is 2.7214070351758792 \\

### Top 2 used tag: respecttylerjoseph
|Shortest Distance|Pair Count|
|--|--|
|2|18629|
|3|1146|
|1|89|
|4|33|
|5|3|

The total pairs calculated is 19900 \\
The average degree is 2.056884422110553 \\

### Top 3 used tag: gloryoutnow
|Shortest Distance|Pair Count|
|--|--|
|2|18940|
|3|539|
|1|239|
|4|182|

The total pairs calculated is 19900 \\
The average degree is 2.033366834170854 \\


### Top 4 used tag: backtohogwarts
|Shortest Distance|Pair Count|
|--|--|
|2|13935|
|3|3354|
|4|2586|
|5|17|
|1|7|
|6|1|

The total pairs calculated is 19900 \\
The average degree is 2.430854271356784 \\

### Top 5 used tag: 
|Shortest Distance|Pair Count|
|--|--|
|2|10906|
|3|4180|
|4|4049|
|5|670|
|6|77|
|1|14|
|7|4|

The total pairs calculated is 19900 \\
The average degree is 2.7337688442211054 \\
