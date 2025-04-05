# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 19:19:40 2023

@author: armit
"""

from random import random, randint, uniform
import numpy as np
from NSGA import *

def flip(prob):
    #from random import random
    if random() < prob:
        return True
    return False

def norm(dist):
    dist_min = min(dist)
    dist_max = max(dist)
    dist_norm = [(a - dist_min) / (dist_max - dist_min) for a in dist]
    return dist_norm

def obj(new_imp, old_imp, pop): #our objective is to maximize gain
    gain = [new_imp[i] - old_imp[i] for i in range(len(new_imp))]
    n_rd = 0
    tot_gain = 0

    for j in range(len(pop)):
        if pop[j] == 1:
            n_rd +=1
            #print(n_rd)
            tot_gain += gain[j]
            #print(tot_gain)
    avg_gain = (tot_gain / n_rd)
    #imp = tot_gain #(tot_gain + sum(old_imp)) / len(pop)
    #return imp
    return avg_gain
    #return tot_gain

# =============================================================================
# def fitness_score(ws, objs, conn, popsize): #assign based on weighted sum of gains scaled on a 0-1 scale
#     scr = [0 for i in range(popsize)]
#     for i in range(len(ws)):
#         w_obj = [ws[i]*objs[i][j] for j in range(popsize)] 
#         scr = [(scr[j] + w_obj[j]) for j in range(len(scr))]
#     #scr_min = min(scr)
#     #scr_max = max(scr)
#     #scr_norm = [(a - scr_min) / (scr_max - scr_min) for a in scr]
#     scr = [scr[i]* conn[i] for i in range(len(scr))]
#     return scr
# 
# 
# def sharing(distance, sigma, alpha):
#     # takes a list of dist from pop i to all pop j
#     # estimates sharing value
#     res = []
#     dist_norm = norm(distance)
#     #print(dist_norm)
#     res = [(1 - (i/sigma)**alpha) if i < sigma else 0 for i in dist_norm]
#     return res
# 
# def shared_fitness(population, fitness, sigma, alpha):
#     #estimates shared fitness for all individual
#     shared_fitness = []
#     for i in range(len(population)):
#         dist = []
#         sharing_dist = []
#         for j in range(len(population)):
#             #print(i, j)
#             dist_ij = np.linalg.norm(np.array(population[i])-np.array(population[j]))
#             dist.append(dist_ij)
#             #print(dist)
#         sharing_dist = sharing(dist, sigma, alpha)
#         shared_fitness.append(fitness[i]/sum(sharing_dist))
#     return(shared_fitness)
# 
# def select(fitnesses):
#     total = sum(fitnesses)
#     r = uniform(0, total)
#     acc = 0
#     for i in range(len(fitnesses)):
#         acc += fitnesses[i]
#         if acc >= r:
#             return i
# =============================================================================
        
        
def calculate_len(rd_len, sol):
    tot_len = 0
    for i in range(len(rd_len)):
        if sol[i] == 1:
            tot_len += rd_len[i]
    return tot_len

def touranment_selection(num_parents,num_offspring):
    offspring_parents = []
    for _ in range(num_offspring):
        contestants = np.random.randint(0,num_parents,2) # generate 2 random numbers, take the smaller (parent list is already sorted, smaller index, better)
        winner = np.min(contestants)
        offspring_parents.append(winner)
    
    return offspring_parents

def selTournamentDCD(individuals, fitnesses, crowding, k):
    """Tournament selection based on dominance (D) between two individuals, if
    the two individuals do not interdominate the selection is made
    based on crowding distance (CD). The *individuals* sequence length has to
    be a multiple of 4 only if k is equal to the length of individuals. 
    Starting from the beginning of the selected individuals, two consecutive 
    individuals will be different (assuming all individuals in the input list 
    are unique). Each individual from the input list won't be selected more 
    than twice.
    This selection requires the individuals to have a :attr:`crowding_dist`
    attribute, which can be set by the :func:`assignCrowdingDist` function.
    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select. Must be less than or equal 
              to len(individuals).
    :returns: A list of selected individuals.
    """

    if k > len(individuals): 
        raise ValueError("selTournamentDCD: k must be less than or equal to individuals length")

    if k == len(individuals) and k % 4 != 0:
        raise ValueError("selTournamentDCD: k must be divisible by four if k == len(individuals)")

    def tourn(ind1, ind2):
        if dominates(fitnesses[ind1],fitnesses[ind2]):
            return ind1
        elif dominates(fitnesses[ind2],fitnesses[ind1]):
            return ind2

        if crowding[ind1] < crowding[ind2]:
            return ind1
        elif crowding[ind1] > crowding[ind2]:
            return ind2

        if random() <= 0.5:
            return ind1
        return ind2

    chosen = []
    for i in range(k):
        ind = np.random.randint(0,len(individuals),2)
        ind1 = ind[0]
        ind2 = ind[1]
        chosen.append(tourn(ind1,   ind2))

    return chosen
        
def crossover(p1, p2, prob):
    if not flip(prob):
        return [p1, p2], 0
    x = randint(0, len(p1)-1)
    c1 = p1[:x] + p2[x:]
    c2 = p2[:x] + p1[x:]
    return [c1, c2], x

def mutation(s, prob):
    _mutate = lambda i: 1 if i==0 else 0
    mutated = []
    for c in s:
        if flip(prob):
            mutated.append(_mutate(c))
        else:
            mutated.append(c)
    return mutated
