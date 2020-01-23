import random
import argparse
import networkx as nx

####################################################################################
# function definitions
####################################################################################

def get_command_line():
	# parse the command line
	parser = argparse.ArgumentParser()

	parser.add_argument('-x', action='store', dest='x_in', default=4, help="max x-value") 
	parser.add_argument('-y', action='store', dest='y_in', default=0.505, help="max y-value")
	parser.add_argument('-r', action='store', dest='r_in', default=5, help="number of graphs to generate")
	parser.add_argument('-n', action='store', dest='n_in', default=5, help="number of nodes per graph")
	parser.add_argument('-v', action='store', dest='v_in', default=False, help="toggle True or False to view extra graphs")

	args = parser.parse_args()

	assert(float(args.x_in) > 0)
	assert(float(args.y_in) > 0)
	assert(int(args.r_in) > 0)
	assert(int(args.n_in) > 1)

	return args


def create_vertices(num_nodes, x_max, y_max):
	"""
	Input
	----------
	num_nodes: positive integer
	x_max: positive float
	y_max: positive float

	Output
	----------
	Returns a dictionary whose keys correspond to nodes and whose values correspond to
	the node's (x,y) coordinates in [0, x_max) X [0, y_max) in R^2.
	"""
	pos_dict = {}
	for i in range(num_nodes):
		x = round(random.uniform(0, x_max), 3)
		y = round(random.uniform(0, y_max), 3)
		pos_dict[i] = (x, y)
	return pos_dict


def promising(current_coloring, current_vertex, cliques_per_vertex):
	# returns True if the current setup doesn't violate the clique-coloring property
	for clique in cliques_per_vertex[current_vertex]:
		colors_present = set(current_coloring[n] for n in clique)
		if len(colors_present) == 1:
			return False
	return True


def recursive_k_clique_coloring(current_coloring, current_vertex, cliques_per_vertex, k):	
	"""
	Input
	----------
	current_coloring: a list whose ith index corresponds to the color of the ith node
	current_vertex: an int specifying the next vertex to check
	cliques_per_vertex: a dictionary whose keys are vertices and values are the cliques
		containing that vertex
	k: an integer specifying how many colors are allowed

	Output
	----------
	Returns a dictionary whose keys correspond to nodes and whose values correspond to
	the node's (x,y) coordinates in [0, x_max) X [0, y_max) in R^2.
	"""

	# BASE CASE
	if current_vertex == len(cliques_per_vertex):
		# this is the final coloring
		# print(current_coloring, '\n')
		return True

	# RED and GREEN sub-trees
	for color in list(range(k)):
		current_coloring[current_vertex] = str(color)

		if promising(current_coloring, current_vertex, cliques_per_vertex):
			if recursive_k_clique_coloring(current_coloring, current_vertex+1, cliques_per_vertex, k):
				return True

		current_coloring[current_vertex] = '?' # reset and try a different color

	return False


def is_valid_coloring(coloring, graph):
	# returns True iff 'coloring' is a valid clique coloring of G

	max_cliques = (c for c in nx.find_cliques(graph) if len(c) > 1)
	for clique in max_cliques:
		colors_present = set(coloring[n] for n in clique)
		if (len(colors_present) == 1):
			return False
	return True





