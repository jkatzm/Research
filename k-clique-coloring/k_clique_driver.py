import time
import matplotlib.pyplot as plt
from numpy import average

from k_clique_helper import *

####################################################################################
# Command line interface and global variables
####################################################################################

print("##################################")
print("generating graphs...\n")

t_start = time.time()

invalids_2 = []
invalids_3 = []
clique_densities = []


args = get_command_line()

X_MAX = float(args.x_in)
Y_MAX = float(args.y_in)
NUM_RUNS = int(args.r_in)
NUM_NODES = int(args.n_in)
VIEWER_MODE = bool(args.v_in)

####################################################################################
####################################################################################
############################## Main program ########################################
####################################################################################
####################################################################################

for i in range(NUM_RUNS):
	# the set of random nodes. each node is bounded in the plane by 'x_max' and 'y_max'
	random_vertices = create_vertices(NUM_NODES, X_MAX, Y_MAX)
	# random_vertices = {0: (0.5, 0.2), 1: (0.5, 1), 2: (1.5, 0.2), 3: (1.6, 1), 4: (1, 1.7)} # C5

	# the geometric graph derived from V. all pairs of nodes of distance ≤ 1 have an edge.
	G = nx.random_geometric_graph(NUM_NODES, 1, pos=random_vertices)

	if VIEWER_MODE:
		nx.draw(G, node_size=10, font_size=20)
		plt.show()

	# a list of non-trivial maximal cliques of G
	max_cliques = [c for c in nx.find_cliques(G) if len(c) > 1]

	# a dictionary with keys = nodes V, values = the cliques in 'max_cliques' containing V
	clique_vertex_dict = { v : [c for c in max_cliques if v in set(c)] for v in range(NUM_NODES) }	

	# add to our list
	clique_densities.append(len(max_cliques) / (X_MAX * Y_MAX))

	#check 2-clique-colorability
	initial = list(str(0)+'?'*(NUM_NODES-1))

	is_2_clique_colorable = recursive_k_clique_coloring(initial, 1, clique_vertex_dict, 2)

	if is_2_clique_colorable == False:
		invalids_2.append(random_vertices)

		print("Found a graph with no valid 2-clique-coloring.")

		nx.draw(G, node_size=10, font_size=20)
		plt.show()
		
		print("Checking 3-clique-colorability...")

		initial = list(str(0)+'?'*(NUM_NODES-1))
		is_3_clique_colorable = recursive_k_clique_coloring(initial, 1, clique_vertex_dict, 3)

		if is_3_clique_colorable == False:
			invalids_3.append(random_vertices)

			print("No valid 3-clique-coloring exists!!!")
			print(random_vertices)

		else:
			print("Valid 3-clique-coloring exists.", '\n')


####################################################################################
# Summary / Outro
####################################################################################

print("##################################")
print("number of graphs generated:", NUM_RUNS)
print("total time:", round(time.time()-t_start, 2), "seconds")
print("average clique density:", round(average(clique_densities), 2))

print("\n##################################")
print("number without a valid 2-clique-coloring:", len(invalids_2))
print("number without a valid 3-clique-colorings:", len(invalids_3))

# TODO: do more with the "invalids_k" lists



