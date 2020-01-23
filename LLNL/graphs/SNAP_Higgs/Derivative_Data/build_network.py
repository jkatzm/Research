import networkx as nx

directory  = "/Users/katz13/Desktop/Data/SNAP_Higgs/Original_Data/"
filename = "higgs-activity_time.txt"

G = nx.MultiDiGraph()



print("building the graph...")
f = open(directory + filename, "r")

for line in f:
	split_line = line.split()

	userA = int(split_line[0])
	userB = int(split_line[1])

	if userA == userB: # we don't want self-loops
		continue

	timestamp = int(split_line[2])
	interaction = split_line[3]

	if interaction == "MT":
		G.add_edge(userA, userB, weight=timestamp)

	elif interaction == "RT":
		G.add_edge(userB, userA, weight=timestamp)

f.close()
print("number of nodes:", len(G.nodes()))
print("...complete\n")



print("relabeling...")
G_relabeled = nx.convert_node_labels_to_integers(G)
print("...complete\n")


print("printing edgelist...")
f_out = open("higgs_edgelist.txt", "w")

for i,j,t in G_relabeled.edges(data=True):
	f_out.write(str(i) + " " + str(j) + " " + str(t['weight']) + "\n")

f_out.close()
print("...complete\n")