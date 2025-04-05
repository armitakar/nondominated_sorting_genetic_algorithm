# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 19:35:28 2023

@author: armit
"""

from connectivity import *
from basic_GA import *
import numpy as np

####### without length consideration

def repair(road_dat, nn, sol, len_min, len_max):
    print("repairing")
    rd_id = list(road_dat['OBJECTID'].values)
    rd_len = list(road_dat['length'].values)
    
    ##### eliminate no connected solution
    sol_ind = count_road_connections(road_dat, sol, nn)[0]
    conn_rd = count_road_connections(road_dat, sol, nn)[1]
    conn_gap_rd = count_road_connections(road_dat, sol, nn)[2]
    #print(sol_ind)
    
    for _ in range(len(sol_ind)):
        if (len(sol_ind) > 1) & (conn_gap_rd[_] == 0):
            sol[sol_ind[_]] = 0
    
    # update solution
    tot_len = calculate_len(rd_len, sol)
    sol_ind = count_road_connections(road_dat, sol, nn)[0]
    conn_rd = count_road_connections(road_dat, sol, nn)[1]
    conn_gap_rd = count_road_connections(road_dat, sol, nn)[2]
    
    conn_sorted = list(np.argsort(conn_rd))
    conn_gap_sorted = list(np.argsort(conn_gap_rd))
    #print(sol_ind)
                    
    nn_con_id = []
    i = 0
    while i < len(sol_ind):
        
        ##### print(val, count_road_connections(road_dat, sol)[0])
        # if length > max threshold, eliminate the least connected roads based on their order
        if (tot_len > len_max):
            val = sol_ind[conn_sorted.index(i)]
            sol[val] = 0
            #print('length longer')
            tot_len = tot_len - rd_len[val]
            #print(tot_len,"number of solutions", sol.count(1))
                
        ##### if length < min threshold,
        if (tot_len < len_min):
            val = sol_ind[conn_gap_sorted.index(len(sol_ind)-(i+1))]
            #print('length shorter')
            # find nearest gap road and connected road of this index
            nn_gap_id = connected_gap_road(road_dat, val, nn)[0] 
            nn_con_id_val = connected_gap_road(road_dat, val, nn)[1]
            nn_con_id = nn_con_id + nn_con_id_val
        
            #get their indexes
            nn_gap_ind = sort_road_id(road_dat, nn_gap_id, rd_len)[0]
            

            for _ in range(len(nn_gap_id)):
                ####### flip them based on total length
                if (sol[nn_gap_ind[_]] == 0):
                    val = nn_gap_ind[_]
                    sol[val] = 1
                    tot_len = tot_len + rd_len[val]
                    #print(tot_len,"number of solutions", sol.count(1))
                if (i == (len(sol_ind) - 1)) & (_ == (len(nn_gap_id) - 1)) & (tot_len < len_min):
                    #print("need for new code")
                    ab = []
                    for _ in nn_con_id:
                        nearest_objids = nn[nn['OBJECTID'] == _]['nearest'].values[0] #list of nearest road ids for that connected road
                        ab = ab + nearest_objids
                        #print(nearest_objids)
                        for _ in ab:
                            #print(_, _ in rd_id)
                            if _ in rd_id:
                                val = rd_id.index(_)
                                if (sol[val] == 0):
                                    sol[val] = 1
                                    tot_len = tot_len + rd_len[val]
                                    #print(tot_len,"number of solutions", sol.count(1))
                            if (tot_len > len_max):
                                #print("final solution length", tot_len)
                                sol_ind = count_road_connections(road_dat, sol, nn)[0]
                                conn_rd = count_road_connections(road_dat, sol, nn)[1]
                                conn_gap_rd = count_road_connections(road_dat, sol, nn)[2]
                                
                                conn_sorted = list(np.argsort(conn_rd))
                                conn_gap_sorted = list(np.argsort(conn_gap_rd))
                                #print(sol_ind)
                                nn_con_id = []
                                i = 0
                                break
                            if (tot_len > len_min) & (tot_len < len_max):
                                #print("final solution length", tot_len)
                                break 
                            if (_ not in rd_id) & (_ not in nn_con_id):
                                nn_con_id.append(_)
                        
                if (tot_len > len_min) & (tot_len < len_max):
                    #print("final solution length", tot_len)
                    break
        
        if ((tot_len > len_min) & (tot_len < len_max)): #| (sol.count(1) ==1 ):
            #print("repaird, final solution length", tot_len)
            break
        
        i = i+1
    return sol


# =============================================================================
# def repair(road_dat, nn, sol, len_min, len_max):
#     rd_id = list(road_dat['OBJECTID'].values)
#     rd_len = list(road_dat['length'].values)
#     
#     ##### eliminate no connected solution
#     sol_ind = count_road_connections(road_dat, sol, nn)[0]
#     conn_rd = count_road_connections(road_dat, sol, nn)[1]
#     conn_gap_rd = count_road_connections(road_dat, sol, nn)[2]
#     #print(sol_ind)
#     
#     for _ in range(len(sol_ind)):
#         if (len(sol_ind) > 1) & (conn_gap_rd[_] == 0):
#             sol[sol_ind[_]] = 0
#     
#     # update solution
#     tot_len = calculate_len(rd_len, sol)
#     sol_ind = count_road_connections(road_dat, sol, nn)[0]
#     conn_rd = count_road_connections(road_dat, sol, nn)[1]
#     conn_gap_rd = count_road_connections(road_dat, sol, nn)[2]
#     
#     conn_sorted = list(np.argsort(conn_rd))
#     conn_gap_sorted = list(np.argsort(conn_gap_rd))
#     #print(sol_ind)
#                    
#     nn_con_id = []
#     i = 0
#     while i < len(sol_ind):
#         
#         ##### print(val, count_road_connections(road_dat, sol)[0])
#         # if length > max threshold, eliminate the least connected roads based on their order
#         if (tot_len > len_max):
#             val = sol_ind[conn_sorted.index(i)]
#             sol[val] = 0
#             tot_len = tot_len - rd_len[val]
#             
#                 
#         ##### if length < min threshold,
#         if (tot_len < len_min):
#             val = sol_ind[conn_gap_sorted.index(len(sol_ind)-(i+1))]
#             #print('length shorter')
#             # find nearest gap road and connected road of this index
#             nn_gap_id = connected_gap_road(road_dat, val, nn)[0] 
#             nn_con_id_val = connected_gap_road(road_dat, val, nn)[1]
#             nn_con_id = nn_con_id + nn_con_id_val
#         
#             #get their indexes
#             nn_gap_ind = sort_road_id(road_dat, nn_gap_id, rd_len)[0]
#             #sort them by length
#             nn_len_sorted = sort_road_id(road_dat, nn_gap_id, rd_len)[1]
#             #print("lowest connection", k, "number of gap roads", len(nn_gap_id))
# 
#             for _ in range(len(nn_gap_id)):
#                 #a = nn_len_sorted.index(_)
#                 b = nn_len_sorted.index(_)
#                 # print(a, val)
#                 # print("gap road", nn_gap_ind[a], sol[nn_gap_ind[a]]
#                 
#                 ####### flip them based on total length
#                 if (sol[nn_gap_ind[b]] == 0):
#                     val = nn_gap_ind[b]
#                     sol[val] = 1
#                     tot_len = tot_len + rd_len[val]
#                     #print(tot_len,"number of solutions", sol.count(1))
#                 if (i == (len(sol_ind) - 1)) & (_ == (len(nn_gap_id) - 1)) & (tot_len < len_min):
#                     #print("need for new code")
#                     ab = []
#                     for _ in nn_con_id:
#                         nearest_objids = nn[nn['OBJECTID'] == _]['nearest'].values[0] #list of nearest road ids for that connected road
#                         ab = ab + nearest_objids
#                         #print(nearest_objids)
#                         for _ in ab:
#                             #print(_, _ in rd_id)
#                             if _ in rd_id:
#                                 val = rd_id.index(_)
#                                 if (sol[val] == 0):
#                                     sol[val] = 1
#                                     tot_len = tot_len + rd_len[val]
#                                     #print("sol updated", tot_len)
#                             if (tot_len > len_max):
#                                 #print("final solution length", tot_len)
#                                 sol_ind = count_road_connections(road_dat, sol, nn)[0]
#                                 conn_rd = count_road_connections(road_dat, sol, nn)[1]
#                                 conn_gap_rd = count_road_connections(road_dat, sol, nn)[2]
#                                 
#                                 conn_sorted = list(np.argsort(conn_rd))
#                                 conn_gap_sorted = list(np.argsort(conn_gap_rd))
#                                 #print(sol_ind)
#                                 nn_con_id = []
#                                 i = 0
#                                 break
#                             if (tot_len > len_min) & (tot_len < len_max):
#                                 #print("final solution length", tot_len)
#                                 break 
#                             if (_ not in rd_id) & (_ not in nn_con_id):
#                                 nn_con_id.append(_)
#                         
#                 if (tot_len > len_min) & (tot_len < len_max):
#                     #print("final solution length", tot_len)
#                     break
#         
#         if ((tot_len > len_min) & (tot_len < len_max)): #| (sol.count(1) ==1 ):
#             #print("repaird, final solution length", tot_len)
#             break
#         
#         i = i+1
#     return sol
# 
# =============================================================================



