import numpy as np
import pandas as pd
import itertools
from ast import literal_eval
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import pdist
from utils.routing.distances import *


def cluster_locations(list_coord, eps, min_samples, dist_method, clust_start):
    ''' Step 1: Create clusters of locations using DBSCAN'''
    # If using Euclidean distance
    if dist_method == 'euclidean':
        coords = np.array(list_coord)
    else:
        # You can replace this with your custom distance function if needed
        coords = np.array(list_coord)  # For example, using a custom distance function

    # Apply DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean')  # 'euclidean' can be changed if necessary
    clust_id = dbscan.fit_predict(coords)

    # Adjust cluster IDs to start from 'clust_start' and handle noise (label -1)
    clust_id = [i + clust_start if i != -1 else -1 for i in clust_id]
    return clust_id


def clustering_mapping(df, eps, min_samples, orders_number, wave_start, clust_start, df_type):  # clustering_loc
    '''Step 2: Clustering and mapping using DBSCAN'''
    # 1. Create Clusters
    list_coord, list_OrderNumber, clust_id, df = cluster_wave(df, eps, min_samples, 'euclidean', clust_start, df_type)
    clust_idmax = max(clust_id)  # Last Cluster ID
    # 2. Mapping Order lines
    dict_map, dict_omap, df, Wave_max = lines_mapping_clst(df, list_coord, list_OrderNumber, clust_id, orders_number,
                                                           wave_start)
    return dict_map, dict_omap, df, Wave_max, clust_idmax


def cluster_wave(df, eps, min_samples, dist_method, clust_start, df_type):
    '''Step 3: Create waves by clusters using DBSCAN'''
    # Create Column for Clustering
    if df_type == 'df_mono':
        df['Coord_Cluster'] = df['Coord']  # Assuming 'Coord' column exists

    # Mapping points
    df_map = pd.DataFrame(df.groupby(['OrderNumber', 'Coord_Cluster'])['SKU'].count()).reset_index()
    list_coord, list_OrderNumber = np.stack(
        df_map.Coord_Cluster.apply(lambda t: literal_eval(t)).values), df_map.OrderNumber.values

    # Cluster locations using DBSCAN
    clust_id = cluster_locations(list_coord, eps, min_samples, dist_method, clust_start)

    # Adjust cluster ids
    clust_id = [(i + clust_start) for i in clust_id]

    # List coordinates
    list_coord = np.stack(list_coord)
    return list_coord, list_OrderNumber, clust_id, df


def lines_mapping(df, orders_number, wave_start):
    '''Step 4: Mapping Order lines mapping without clustering '''
    # Unique order numbers list
    list_orders = df.OrderNumber.unique()
    # Dictionnary for mapping
    dict_map = dict(zip(list_orders, [i for i in range(1, len(list_orders))]))
    # Order ID mapping
    df['OrderID'] = df['OrderNumber'].map(dict_map)
    # Grouping Orders by Wave of orders_number
    df['WaveID'] = (df.OrderID % orders_number == 0).shift(1).fillna(0).cumsum() + wave_start
    # Counting number of Waves
    waves_number = df.WaveID.max() + 1
    return df, waves_number


def lines_mapping_clst(df, list_coord, list_OrderNumber, clust_id, orders_number, wave_start):
    '''Step 4: Mapping Order lines mapping with clustering '''
    # Dictionnary for mapping by cluster
    dict_map = dict(zip(list_OrderNumber, clust_id))
    # Dataframe mapping
    df['ClusterID'] = df['OrderNumber'].map(dict_map)
    # Order by ID and mapping
    df = df.sort_values(['ClusterID', 'OrderNumber'], ascending=True)
    list_orders = list(df.OrderNumber.unique())
    # Dictionnary for order mapping
    dict_omap = dict(zip(list_orders, [i for i in range(1, len(list_orders))]))
    # Order ID mapping
    df['OrderID'] = df['OrderNumber'].map(dict_omap)
    # Create Waves: Increment when reaching orders_number or changing cluster
    df['WaveID'] = wave_start + ((df.OrderID % orders_number == 0) | (df.ClusterID.diff() != 0)).shift(1).fillna(
        0).cumsum()

    wave_max = df.WaveID.max()
    return dict_map, dict_omap, df, wave_max


def locations_listing(df_orderlines, wave_id):
    ''' Step 5: Listing location per Wave of orders'''

    # Filter by wave_id
    df = df_orderlines[df_orderlines.WaveID == wave_id]
    # Create coordinates listing
    list_coord = list(df['Coord'].apply(lambda t: literal_eval(t)).values)  # Here we use Coord for distance
    list_coord.sort()
    # Get unique Unique coordinates
    list_coord = list(k for k, _ in itertools.groupby(list_coord))
    n_locs = len(list_coord)
    n_lines = len(df)
    n_pcs = df.PCS.sum()

    return list_coord, n_locs, n_lines, n_pcs


# Example Usage:

eps = 0.5  # Max distance between points in the same cluster
min_samples = 5  # Minimum number of points to form a cluster
orders_number = 10  # Number of orders per wave
wave_start = 0  # Starting wave ID
clust_start = 1  # Starting cluster ID
df_type = 'df_mono'  # Assuming this is the dataframe type

# Assuming 'df' is your DataFrame with order lines and coordinates
dict_map, dict_omap, df, wave_max, clust_idmax = clustering_mapping(df, eps, min_samples, orders_number, wave_start,
                                                                    clust_start, df_type)

print(f"Clustering complete. Total waves: {wave_max}, Max cluster ID: {clust_idmax}")
