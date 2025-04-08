# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 08:53:11 2023

"""

#Non-dominated sorting GA 
#Source code: https://github.com/adam-katona/NSGA_2_tutorial/blob/master/NSGA_2_tutorial.ipynb



import numpy as np
import functools

# With Multiobjective optimization, we simultaneously optimize for multiple objectives.
# The goal of the multiobjective optimization is to find a set of solutions which is not dominated by any other solution.

# But what is domination?
# A solution dominates another solution if in all of the objectives it is better or equal, and in at least one it is better.

def dominates(fitnesses_1,fitnesses_2):
    # fitnesses_1 is a array of objectives of solution 1 [objective1, objective2 ...]
    larger_or_equal = fitnesses_1 >= fitnesses_2
    larger = fitnesses_1 > fitnesses_2
    if np.all(larger_or_equal) and np.any(larger):
        return True
    return False

# A set of solutions which do not dominate each other is called a Pareto front.
# When there is no solution which dominates any of members of the front, it is called an optimal Pareto front.
# The goal of multiobjective optimization is to find the optimal Pareto front.

def calculate_pareto_fronts(fitnesses):
    
    # Calculate dominated set for each individual
    domination_sets = []
    domination_counts = []
    for fitnesses_1 in fitnesses:
        current_dimination_set = set()
        domination_counts.append(0)
        for i,fitnesses_2 in enumerate(fitnesses):
            if dominates(fitnesses_1,fitnesses_2):
                current_dimination_set.add(i)
            elif dominates(fitnesses_2,fitnesses_1):
                domination_counts[-1] += 1

        domination_sets.append(current_dimination_set)

    domination_counts = np.array(domination_counts)
    fronts = []
    while True:
        current_front = np.where(domination_counts==0)[0]
        if len(current_front) == 0:
            #print("Done")
            break
        #print("Front: ",current_front)
        fronts.append(current_front)

        for individual in current_front:
            domination_counts[individual] = -1 # this individual is already accounted for, make it -1 so  ==0 will not find it anymore
            dominated_by_current_set = domination_sets[individual]
            for dominated_by_current in dominated_by_current_set:
                domination_counts[dominated_by_current] -= 1
            
    return fronts


# An important aspect of multiobjective optimization is that we explore the different possible tradoffs.
# To do this effectively we need to encourage a diversity in the population.
# NSGA-II uses a crowding metric to do this.
# The crowding metric is based on how close the neerest neighbors in the same front are for each objective. 


def calculate_crowding_metrics(fitnesses,fronts):
    
    num_objectives = fitnesses.shape[1]
    num_individuals = fitnesses.shape[0]
    
    # Normalise each objectives, so they are in the range [0,1]
    # This is necessary, so each objective's contribution have the same magnitude to the crowding metric.
    normalized_fitnesses = np.zeros_like(fitnesses)
    for objective_i in range(num_objectives):
        min_val = np.min(fitnesses[:,objective_i])
        max_val = np.max(fitnesses[:,objective_i])
        val_range = max_val - min_val
        normalized_fitnesses[:,objective_i] = (fitnesses[:,objective_i] - min_val) / val_range
    
    fitnesses = normalized_fitnesses
    crowding_metrics = np.zeros(num_individuals)

    for front in fronts:
        for objective_i in range(num_objectives):
            
            sorted_front = sorted(front,key = lambda x : fitnesses[x,objective_i])
            
            crowding_metrics[sorted_front[0]] = np.inf
            crowding_metrics[sorted_front[-1]] = np.inf
            if len(sorted_front) > 2:
                for i in range(1,len(sorted_front)-1):
                    crowding_metrics[sorted_front[i]] += fitnesses[sorted_front[i+1],objective_i] - fitnesses[sorted_front[i-1],objective_i]

    return  crowding_metrics


# For sorting the population we need both the nondomination rank and the crowding metric
# In this algorithm, we further multiply the crowding distance with continuity ratio to estimate a crowd-continuous index and use that value for fitness evaluation
# We always consider the nondomination rank first, but in a tie we use the crowding metric

# helper function
def fronts_to_nondomination_rank(fronts):
    nondomination_rank_dict = {}
    for i,front in enumerate(fronts):
        for x in front:   
            nondomination_rank_dict[x] = i
    return nondomination_rank_dict
        

def nondominated_sort(nondomination_rank_dict,crowding):
    
    num_individuals = len(crowding)
    indicies = list(range(num_individuals))

    def nondominated_compare(a,b):
        # returns 1 if a dominates b, or if they equal, but a is less crowded
        # return -1 if b dominates a, or if they equal, but b is less crowded
        # returns 0 if they are equal in every sense
        
        
        if nondomination_rank_dict[a] > nondomination_rank_dict[b]:  # domination rank, smaller better
            return -1
        elif nondomination_rank_dict[a] < nondomination_rank_dict[b]:
            return 1
        else:
            if crowding[a] < crowding[b]:   # crowd-continuous metrics, larger better
                return -1
            elif crowding[a] > crowding[b]:
                return 1
            else:
                return 0

    non_domiated_sorted_indicies = sorted(indicies,key = functools.cmp_to_key(nondominated_compare),reverse=True) # decreasing order, the best is the first
    return non_domiated_sorted_indicies

def calculate_domination_matrix(fitnesses):    
    
    pop_size = fitnesses.shape[0]
    num_objectives = fitnesses.shape[1]
    
    fitness_grid_x = np.zeros([pop_size,pop_size,num_objectives])
    fitness_grid_y = np.zeros([pop_size,pop_size,num_objectives])
    
    for i in range(pop_size):
        fitness_grid_x[i,:,:] = fitnesses[i]
        fitness_grid_y[:,i,:] = fitnesses[i]
    
    larger_or_equal = fitness_grid_x >= fitness_grid_y
    larger = fitness_grid_x > fitness_grid_y
    
    return np.logical_and(np.all(larger_or_equal,axis=2),np.any(larger,axis=2))


def fast_calculate_pareto_fronts(fitnesses):
    
    # Calculate dominated set for each individual
    domination_sets = []
    domination_counts = []
    
    domination_matrix = calculate_domination_matrix(fitnesses)
    pop_size = fitnesses.shape[0]
    
    for i in range(pop_size):
        current_dimination_set = set()
        domination_counts.append(0)
        for j in range(pop_size):
            if domination_matrix[i,j]:
                current_dimination_set.add(j)
            elif domination_matrix[j,i]:
                domination_counts[-1] += 1
                
        domination_sets.append(current_dimination_set)

    domination_counts = np.array(domination_counts)
    fronts = []
    while True:
        current_front = np.where(domination_counts==0)[0]
        if len(current_front) == 0:
            #print("Done")
            break
        #print("Front: ",current_front)
        fronts.append(current_front)

        for individual in current_front:
            domination_counts[individual] = -1 # this individual is already accounted for, make it -1 so  ==0 will not find it anymore
            dominated_by_current_set = domination_sets[individual]
            for dominated_by_current in dominated_by_current_set:
                domination_counts[dominated_by_current] -= 1
            
    return fronts
