import json
import matplotlib.pyplot as plt
from pprint import pprint
import pandas as pd
import numpy as np
import re

def json_to_dict(filename):
    """
    This function pulls a Python dictionary formatted as a .json file
    and converts it to an actual dictionary
    
    Parameters
    ----------
    filename - A string that contains the location of the .json file

    Returns
    -------
    network_perf - a dictionary of {strings:3x3 arrays} with encoded
                   networks and [epsilon, matches, parameters] arrays x3
    """
    # with open(filename) as f:
    with open('computations2019_02_19_15_32_55/results/pattern_matches.json') as f:
        data = json.load(f)

    return data


def convert_edge_form(model):
    """
    This function takes an edge as defined in a lem file and converts it
    to DSGRN json format

    Parameters
    ----------
    model - A string of the form XXXXX_XXXXXXX=r(XXXXX_XXXXXXX)

    Returns
    -------
    DSGRN model - A string of the form XXXXX_XXXXXXX : (~XXXXX_XXXXXXX)
    """
    if model[14] == 'r' or model[14] == 'R':
        gap = '~'
    else:
        gap = ''

    return "{} : ({}{})".format(model[0:13], gap, model[16:29])
    

    

def lem_parser(filename):
    """
    This function takes a lem file and builds a dictionary of edges and
    their lem scores

    Parameters
    ----------
    filename - A string that contains the location of the lem file

    Returns
    -------
    lem_dict - A dictionary of edges and their weights
    """
    # df = pd.read_csv(filename, delim_whitespace=True, comment="#")
    df = pd.read_csv('50tf_lem.tsv', delim_whitespace=True, comment="#")

    lem_dict = {}
    
    for _, values in df.iterrows():
        lem_dict[convert_edge_form(values[0])] = values[3]

    return lem_dict


def detangle_edge(node):
    """
    This function splits a node:nodenodenode+ relationship to separate
    node:node relationships

    Parameters
    ----------
    node - A string of the form node : (node)(node)...

    Returns
    -------
    edges - A list of strings, where each string is of the form node : node
    """
    origin = node[0:13]
    destinations = re.split('\)\(|\(|\)| \+ ', node[16:])
    destinations = list(filter(None, destinations))
    edges = []
    
    for destination in destinations:
        edges.append(origin + ' : (' + destination + ')')

    return edges


def scatter(network_perf, lem_dict):
    """
    This function generates a scatter plot of % pattern match against 
    normalized edge rank.

    Parameters
    ----------
    network_perf - A dictionary of {strings:3x3 arrays} with encoded networks
                   and [epsilon, matches, parameters] arrays x3
    lem_dict - A dictionary of each edge and its calculated lem score

    Returns
    -------
    
    """
    chart_array = np.empty((0,4), float)
    
    for network in network_perf:
        # Deal with the list of edges
        network_edges = network.split(" : E\n")

        total, count = 0, 0
        for node in network_edges:
            edges = detangle_edge(node)

            for edge in edges:
                print(edge)
                print(lem_dict[edge])
                total += lem_dict[edge]
                count += 1


        y_val = total/count

        values = network_perf[network]

        x_val_0 = values[0][1] / values[0][2]
        x_val_1 = values[1][1] / values[1][2]
        x_val_2 = values[2][1] / values[2][2]
        
        chart_array = np.append(chart_array, \
                                 [[y_val, x_val_0, x_val_1, x_val_2]], \
                                 axis=0)


    plot_axes = [0, 1, 0, 1]

    plt.plot(chart_array[:,0], chart_array[:,2], 'bo')
    plt.axis(plot_axes)
    plt.show()


network_perf = json_to_dict('dummy')
lem_dict = lem_parser('dummy')
scatter(network_perf, lem_dict)
