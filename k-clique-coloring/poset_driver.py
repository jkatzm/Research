import matplotlib.pyplot as plt
import networkx as nx

from poset_algorithm import *
from k_clique_helper import create_vertices
from k_clique_helper import is_valid_coloring

# Set global parameters
########################

NUM_NODES = 13
X_MAX = 3
Y_MAX = 0.86

########################

vertices = create_vertices(NUM_NODES, X_MAX, Y_MAX)

G = nx.random_geometric_graph(NUM_NODES, 1, pos=vertices)

points = set(vertices.values())

colors = poset_algorithm(points)
# colors = {vertices[i] : 'b' for i in range(NUM_NODES)}

if is_valid_coloring(list(colors.values()), G) == False:
	print("coloring is not valid...")

print("coloring:", colors, '\n')

for i in range(NUM_NODES):
	plt.scatter([vertices[i][0]], [vertices[i][1]], color=colors[vertices[i]])
plt.show()

nx.draw(
	G,
	labels={i:i for i in range(NUM_NODES)},
	node_color=[colors[vertices[i]] for i in range(NUM_NODES)]
)

plt.show()




