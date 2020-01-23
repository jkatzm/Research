from io_helper import *

########################################################################
# subject helper functions
########################################################################
def get_subject_timeseries(subject_id):
    """
    Input: subject_id integer
    Output: fMRI time series matrix of shape (264, 119): nodes x timesteps
    """
    file_name = penn_timecourse_dir + str(subject_id) + '.csv'
    return pd.read_csv(file_name).as_matrix().T


def get_subject_graph(subject_id, abs=True):
    """
    Input: subject_id integer
    Output: adj_to_nx(corr(get_subject_timeseries(subject_id))) or
            adj_to_nx(np.abs(corr(get_subject_timeseries(subject_id))))
            depending on whether 'abs' is True or False
    Note: loading the weighted_edgelist_csv files is faster than
    		this sequence of operations
    """
    if abs==True:
        file_name = penn_graph_dir + 'edges_abs_r/' + str(subject_id) + '_weighted_edgelist.csv'
    else:
        file_name = penn_graph_dir + 'edges_r/' + str(subject_id) + '_weighted_edgelist.csv'
    return nx.read_weighted_edgelist(file_name)


# TODO: add path length metric, integration matric, etc.

def get_subject_CFBC(subject_id, abs=True):
    G = get_subject_graph(subject_id, abs)
    return nx.current_flow_betweenness_centrality(G, weight='weight')

def get_subject_CFCS(subject_id, abs=True):
    G = get_subject_graph(subject_id, abs)
    return nx.current_flow_closeness_centrality(G, weight='weight')

def get_subject_CC(subject_id):
    G = get_subject_graph(subject_id, True)
    return nx.clustering(G, weight='weight')

def get_subject_pagerank(subject_id):
    G = get_subject_graph(subject_id, True)
    return nx.pagerank_numpy(G)





