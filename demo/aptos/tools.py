from openalea.mtg import *
from openalea.mtg.turtle import *

import numpy as np
from numpy import *

import pandas as pd
from pandas import *

###################################

# This function enables to record the properties of each element of the MTG:
def recording_MTG_properties(g, file_name):
    """This function records the properties of each node of the MTG "g" inside a csv file.
    
    Parameters
    ---------
    g: MTG 
        MTG where properties are recorded
    file_name: csv fil name (or xlsx)
        the name of the csv file where properties of each node will be recorded
    
    Returns
    ------
    [no return]

    Authors
    -------
    Frederic REES

    """
    # We define the list of all properties of the MTG:
    initial_list_of_properties = list(g.properties().keys())
    # We verify that the list does not contain any "None" property:
    list_of_properties = []
    for property in initial_list_of_properties:
        if property is None:
            print("WARNING: a None property was detected in the MTG!")
            continue
        else:
            list_of_properties.append(property)
    # We sort the list by alphabetical order
    list_of_properties.sort()

    # We create an empty list of node indices:
    node_index = []
    # We create an empty list that will contain the properties of each node:
    g_properties = []

    # We cover all the vertices in the MTG:
    max_scale = g.max_scale()

    for vid in g.vertices_iter(scale = max_scale):
        # Initializing an empty list of properties for the current node:
        node_properties = []
        # Adding the index at the beginning of the list:
        node_properties.append(vid)
        # n represents the vertex:
        n = g.node(vid)
        # For each possible property:
        for property in list_of_properties:
            # We add the value of this property to the list:
            node_properties.append(getattr(n, property, "NA"))
        # Finally, we add the new node's properties list as a new item in g_properties:
        g_properties.append(node_properties)
    # We create a list containing the headers of the dataframe:
    column_names = ['node_index']
    column_names.extend(list_of_properties)
    # We create the final dataframe:
    data_frame = pd.DataFrame(g_properties, columns=column_names)
    # We record the dataframe as a csv file:
    #data_frame.to_csv(file_name, na_rep='NA', index=False, header=True)
    # We record the dataframe as a excel file:
    data_frame.to_excel(file_name,  na_rep='NA', index=False, header=True)

    return


def recording_MTG_df(g, file_name):
    """This function records the properties of each node of the MTG "g" from a dataframe to a csv (or xlsx) file.
    
    Parameters
    ---------
    g: MTG 
        MTG where properties are recorded
    file_name: csv fil name (or xlsx)
        the name of the csv file where properties of each node will be recorded
    
    Returns
    ------
    [no return]

    Authors
    -------
    Armand GRUMEL
    Solen FARRA

    """
    
    results =dict()
    results = g.properties()
    results =pd.DataFrame.from_dict(results, orient='columns')

    #results.to_excel(file_name,  na_rep='NA', index=False, header=True)
    
    #filtered_results = Results[Results['label']=='Plant']
    #filtered_results.to_excel(file_name,  na_rep='NA', index=False, header=True)
    
    #filtered_results = Results[Results['label']=='Leaf']
    #filtered_results.to_excel(file_name,  na_rep='NA', index=False, header=True)

    filtered_results = results[results['label'].isin(['Leaf', 'Plant', 'DeadLeaf'])]
    
    #global results_concat
    #global results_before
    #results_concat = pd.concat([filtered_results, results_before])
    #results_before = filtered_results

    #filtered_results = results[results['label'].isin(['Leaf', 'Plant', 'Internode'])]
    filtered_results.to_excel(file_name,  na_rep='NA', index=False, header=True)

    print(filtered_results[['Time','Fall', 'LeafPosition']].to_string())

    return filtered_results


def create_MTG_from_csv_file(_init_, csv_filename):
    """This function use datas from the csv file to create each node of the MTG "g".
    
    Parameters
    ---------
    g: MTG 
        MTG where properties are recorded
    csv_file_name: csv fil name
        the name of the csv file where properties of each node will be recorded
    
    Returns
    ------
    [no return]

    AUTHORS
    -------
    Frederic REES

    """
    # We first read the csv file where all the properties of each vertex has been previously recorded:
    dataframe = pd.read_csv(csv_filename, sep=',', header=0)
    # We initialize an empty MTG:
    g = MTG()

    # We define the list of vertices and properties to be added to the MTG:
    list_of_vid = dataframe['node_index']
    list_of_properties = list(dataframe.columns.values)
    list_of_properties.remove('node_index')

    # We initialize the first vid, to which a new element will be added:
    vid = g.root

    for vid in list_of_vid:
        n = g.node(vid-1)
        n = n.add_child()
        for property in list_of_properties:
            g.property(property)[vid] = dataframe[property].loc[dataframe['node_index'] == vid]

    return g

