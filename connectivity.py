# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 19:03:53 2023

@author: armit
"""
from random import randint
import numpy as np

'''this function returns a index value of the gap roads that has atleast one connection with previously built road'''
def find_connection_with_old_road(road_dat, nn): 
    rd_id = list(road_dat['OBJECTID'].values)
    while True:
        # randomly picks one road
        ind = randint(1, len(road_dat)-1)
        #print(ind)
        # get its objectID
        objid = road_dat['OBJECTID'].iloc[ind]
        # get objectID of its nearest neighbors
        nn_objid = nn[nn['OBJECTID'] == objid]['nearest'].values[0]
        
        #break when atleast one of the nearest road is not gap road 
        #indicating one of the nearest road already has sidewalks
        if (any(_ not in rd_id for _ in nn_objid) == True):
            break
    return ind


# this function returns the ids of connected roads and gap roads for a single index given a nearest neighbor dataset
# the nearest neighbor dataset is based on shapely's nearest_point function
# it lists all the road ids that are connected to a road (with or without sidewalk)

def connected_gap_road(road_dat, ind, nn):
    rd_id = list(road_dat['OBJECTID'].values)
    
    objid = rd_id[ind]
    nn_objid = nn[nn['OBJECTID'] == objid]['nearest'].values[0] # get all nearest road ids
    nn_gap_id = [_ for _ in nn_objid if _ in rd_id] #keep the nearest road ids that are also gap roads
    nn_con_id = [_ for _ in nn_objid if _ not in rd_id]
    #print(nn_objid)
    return (nn_gap_id, nn_con_id)


# this function returns index values and their length-based order for the gap roads
def sort_road_id(road_dat, nn_id, var_list):
    rd_id = list(road_dat['OBJECTID'].values)
    #rd_len = list(road_dat['length'].values)
    
    #find indexes in the gap road data for all nearest road ids
    ind = [rd_id.index(_) for _ in nn_id] 
    var = [var_list[_] for _ in ind] # length of nearest neighbors
    nn_sorted = list(np.argsort(var)) #sorted length from smallest to highest
    #print(ind, nn_len, nn_len_sorted)
    return ind, nn_sorted


# this function counts the number of existing connected road and road to be connected for each road in the solution
def count_road_connections(road_dat, sol, nn):
    rd_id = list(road_dat['OBJECTID'].values)
    
    # get index of current solutions
    sol_ind = [ _ for _ in range(len(sol)) if sol[_] == 1] 
    conn_rd = []
    conn_gap_rd = []
    
    
    
    for j in sol_ind:
        #number of connected road
        connected_rd = len(connected_gap_road(road_dat, j, nn)[1])
        #number of gap road
        gap_id = connected_gap_road(road_dat, j, nn)[0]
        #index of those gap ids
        gap_id_ind = [rd_id.index(i) for i in gap_id]
        
        gap_rd = 0
        #number of gap road to be connected
        for i in gap_id_ind:
            if sol[i] == 1:
                gap_rd += 1
        conn_rd.append(connected_rd + gap_rd)
        conn_gap_rd.append(gap_rd)
    return sol_ind, conn_rd, conn_gap_rd

# this function calculates the ratio of roads with zero connection and total number of road in solution as a connectivity measure
def calculate_connectivity(road_dat, sol, nn):
    #how many road has connection with existing or newly constructed road
    conn_rd = count_road_connections(road_dat, sol, nn)[1]
    #how many road does not have any connection with existing or newly constructed road
    no_conn = conn_rd.count(0)
    #their ratio no connection/total road (lower value better)
    ratio = (len(conn_rd) - no_conn) / len(conn_rd)
    #print(conn_rd, no_conn)
    return ratio
