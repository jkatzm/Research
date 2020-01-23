This derived network is a MultiDiGraph, edges are of the form (i,j,t)

(i,j,t) represents "node i influenced node j at time t."

node i can influence node j by mentioning them (MT) or when node j retweets (RT) node i

No self-influence is allowed (i.e. i ≠ j)

Nodes are labeled 0 to |V|-1