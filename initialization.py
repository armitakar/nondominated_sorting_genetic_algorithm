# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 19:25:25 2023

@author: armit
"""
import numpy as np

from connectivity import *
from basic_GA import *
from NSGA import *
from repair import repair
from random import choice

def generate_solutions(road_dat, nn):
    rd_id = list(road_dat['OBJECTID'].values)
    rd_len = list(road_dat['length'].values)
    
    # find a road that has atleast one connected road
    val = find_connection_with_old_road(road_dat, nn)

    sol = [0 for i in range(len(road_dat))]
    sol[val] = 1
    nn_con_id = []
    old_val = []

    i = 0
    while i < 100:
        #print("i",i, "val", val)
        old_val.append(val)
        
        #curr_val = val
        #print("i",i,"current val,",val, "number of roads picked",len(old_val))
        nn_gap_id = connected_gap_road(road_dat, val, nn)[0]
        nn_con_id_val = connected_gap_road(road_dat, val, nn)[1]
        nn_con_id = nn_con_id + nn_con_id_val

        nn_gap_ind = sort_road_id(road_dat, nn_gap_id, rd_len)[0]

        if (all(_ in old_val for _ in nn_gap_ind) == True):
            #print("all nearest road of current val are ones, checking for new val")
            #get neartest road ids for each of them:
            j = 0
            while j<20:
                ab = []
                for _ in nn_con_id:
                    nearest_objids = nn[nn['OBJECTID'] == _]['nearest'].values[0] #list of nearest road ids for that connected road
                    ab = ab + nearest_objids
                    if (j>1) & (len(ab)>5000):
                        break
                #print("j",j, len(ab))
                if (any(_ in rd_id for _ in ab) == True): #if all nearest roads are not in road id == false
                    #print([_ in rd_id for _ in ab])
                    objids = [_ for _ in ab if _ in rd_id] #roads that fullfil the condition
                    obj_ind = [rd_id.index(_) for _ in objids] # index of those roads
                    obj_ind_sel = [_ for _ in obj_ind if _ not in old_val] # not in val
                    #print(objids)
                    if len(obj_ind_sel) != 0:
                        val = choice(obj_ind_sel) # pick any of it randomly
                        #print("found new val", val)
                        break
                    else:
                        #print("no gap road")
                        nn_con_id = [_ for _ in ab if _ not in rd_id]
                        j = j + 1
                else:
                    #print("no gap road")
                    nn_con_id = [_ for _ in ab if _ not in rd_id]
                    j = j + 1
        
        for _ in range(len(nn_gap_id)):
            if (sol[nn_gap_ind[_]] == 0):
                val = nn_gap_ind[_]
                sol[val] = 1
                break
        if (val in old_val) == True:
            val = find_connection_with_old_road(road_dat, nn)
            #print("val already checked", val)   
        i = i+1
    
         
    tot_len = calculate_len(rd_len, sol)
    #print(tot_len)
    return sol



def initialization(road_dat, nn, popsize, grp, len_min, len_max): 
    #rd_id = list(road_dat['OBJECTID'].values)
    rd_len = list(road_dat['length'].values)
    
    sols = []
    while True:
        print("initial generating solution")
        ran_sols = generate_solutions(road_dat, nn)
        tot_len = calculate_len(rd_len, ran_sols)
        print("initial repairing")
        sol = repair(road_dat, nn, ran_sols, len_min, len_max)
        sols.append(sol)
        print(len(sols))
        if len(sols) == popsize:
            break
    
    objs= []
    
    for k in range(popsize):
        avg_gain = []
        for i in grp:
            #print(i)
            new_imp = list(road_dat['%s_new'%i])
            old_imp = list(road_dat['%s_old'%i])

            obj_val = obj(new_imp, old_imp, sols[k])
            avg_gain.append(obj_val)
            
        objs.append(avg_gain)
    conn = [calculate_connectivity(road_dat, _, nn) for _ in sols]
    objs = np.array(objs)
    
    fronts = calculate_pareto_fronts(objs)
    nondomination_rank_dict = fronts_to_nondomination_rank(fronts)
    
    crowding = calculate_crowding_metrics(objs,fronts)
    print(crowding)
    crowding[crowding == np.inf] = np.max(crowding[crowding != np.inf])
    crowding = [crowding[_]* conn[_] for _ in range(popsize)]
    #fitnesses_0 = fitness_score(ws, objs, conn, popsize)
    #fitnesses = shared_fitness(sols, fitnesses_0, sigma, alpha)
    return sols, objs, crowding