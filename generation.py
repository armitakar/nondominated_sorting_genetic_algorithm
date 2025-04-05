# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 19:39:41 2023

@author: armit
"""
import numpy as np
from connectivity import *
from basic_GA import *
from NSGA import *
from repair import repair

def generation(road_dat, nn, popsize, grp, len_min, len_max, population, objs, crowding,
               pcrossover, pmutation):
    rd_len = list(road_dat['length'].values)
    newpop = []
    while len(newpop) < popsize:
        #print("new population",len(newpop))
        pop_ind = selTournamentDCD(population, objs, crowding, 2)
        
        p1 = population[pop_ind[0]]
        p2 = population[pop_ind[1]]
        offspring = crossover(p1, p2, pcrossover)[0]
        for s in offspring:
            c = mutation(s, pmutation)
            old_len = calculate_len(rd_len, c)
            print("repairing in generation")
            c1 = repair(road_dat, nn, c, len_min, len_max)
            tot_len = calculate_len(rd_len, c1)
            #print("old_len",old_len, "new_len",tot_len, len(newpop))
            if (tot_len >=len_min) & (tot_len <=len_max) & (len(newpop) < len(population)):
                newpop.append(c1)
                print(len(newpop))
            else:
                break
    newpop = newpop + population
    
    newobjs= []
    for k in range(len(newpop)):
        avg_gain = []
        for i in grp:
            #print(i)
            new_imp = list(road_dat['%s_new'%i])
            old_imp = list(road_dat['%s_old'%i])

            obj_val = obj(new_imp, old_imp, newpop[k])
            avg_gain.append(obj_val)
            
        newobjs.append(avg_gain)
    newobjs = np.array(newobjs)
    newconn = [calculate_connectivity(road_dat, _, nn) for _ in newpop]
    
    newfronts = fast_calculate_pareto_fronts(newobjs)
    
    newcrowding = calculate_crowding_metrics(newobjs,newfronts)
    newcrowding[newcrowding == np.inf] = np.max(newcrowding[newcrowding != np.inf])
    #print("new crowding before conn", newcrowding)
    newcrowding = [newcrowding[_]* newconn[_] for _ in range(len(newpop))]
    #print(newconn, newcrowding)
    
    # sort the new populations
    nondomination_rank_dict = fronts_to_nondomination_rank(newfronts)
    
    # Sort the population
    non_domiated_sorted_indicies = nondominated_sort(nondomination_rank_dict,newcrowding)
    
    # The better half of the population survives to the next generation and have a chance to reproduce
    # The rest of the population is discarded
    
    surviving_pop = []
    surviving_objs = []
    surviving_crwd = []
    i = 0
    while len(surviving_pop) < popsize:
        ind = non_domiated_sorted_indicies[i]
        if newcrowding[ind] > 0:
            surviving_pop.append(newpop[ind])
            surviving_objs.append(newobjs[ind])
            surviving_crwd.append(newcrowding[ind])
        i = i+1
    
    
    print(len(population), len(newpop))
    population = surviving_pop
    objs = surviving_objs
    crowding = surviving_crwd
    return population, objs, crowding
