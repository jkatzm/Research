import numpy as np
import networkx as nx

########################################################################
# data manipulation helper functions
########################################################################
def corr(M):
    return np.corrcoef(M)

def threshold(X, theta):
    """
    Input: X = np.ndarray, theta = float
    Output: Thresholded copy of adj_mat
    """
    X_copy = np.copy(X)
    X_copy[np.abs(X_copy) < theta] = 0
    return X_copy

def vectorize(M):
    """
    Input: M = matrix
    Output: the upper-triangular components flattened into a feature vector
    """
    return M[np.triu_indices_from(M, k=1)]

def adj_to_nx(adj_mat):
    """
    Input: adj_mat = np.ndarray (adjacency matrix)
    Output: graph in NetworkX format
    """
    return nx.convert_matrix.from_numpy_matrix(adj_mat)

def nx_to_adj(graph):
    """
    Input: graph in NetworkX format
    Output: adjacency matrix of the network
    """
    return nx.convert_matrix.to_numpy_matrix(graph)


def dict_to_features(dict, subjects):
	features = []
	for s in subjects:
		features.append(list(dict[s].values()))
	return np.array(features)

