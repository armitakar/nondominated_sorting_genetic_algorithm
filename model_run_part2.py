# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:16:19 2023

@author: armita kar
"""
import sys
import pandas as pd

import numpy as np
import itertools


import time
import multiprocessing as mp

from connectivity import *
from basic_GA import *
from NSGA import *
from repair import repair
from initialization import *
from generation import generation


########## find extreme and non-dominated solutions  ##################

grp = ['male_high_white', 'female_high_white', 
       'male_high_poc', 'female_high_poc', 
       'male_med_white', 'female_med_white', 
       'male_med_poc', 'female_med_poc', 
       'male_low_white', 'female_low_white',
       'male_low_poc', 'female_low_poc']

# non-domination among all solutions
df = pd.read_csv(r'Output\hilltop_sol.csv')
df['area'] = "Hilltop"
df = df.drop_duplicates(subset=['objs%s'%(_+1) for _ in range(len(grp))], keep='first')


objs = [[df['objs%s'%(_+1)].iloc[i] for _ in range(len(grp))] for i in range(len(df))]
objs = np.array(objs)

fronts = calculate_pareto_fronts(objs)
nondomination_rank_dict = fronts_to_nondomination_rank(fronts)
non_domiated_sorted_indicies = nondominated_sort(nondomination_rank_dict,df['fitness'].values.tolist())
non_domiated_sorted_indicies
df['nondomination_rank'] = [nondomination_rank_dict[i] for i in range(len(df))]
df['nondomination_crowding_rank'] = [non_domiated_sorted_indicies.index(i) for i in range(len(df))]
df['sol_type'] = "Non-dominated"

# extreme solutions for all groups
c = df[df['objs1'] == max(df['objs1'])]
c['sol_type'] = 'Extreme (%s)'%grp[0]

for i in range(11):
    ex = df[df['objs%s'%(i+2)] == max(df['objs%s'%(i+2)])]
    ex['sol_type'] = 'Extreme (%s)'%grp[i+1]
    c = pd.concat([c, ex])

df = pd.concat([df, c])
df.to_csv(r'Output\hilltop_final solutions_sorted.csv')
df.to_pickle(r'Output\hilltop_final solutions_sorted.pkl')


########## find naive solutions  ##################
#road dataset with no sidewalk
gap = pd.read_csv(r'Data\sidewalk_gap_hilltop.csv')

nearest_dat = pd.read_pickle(r'Data\hilltop_nearest_rd_no_geom.pkl')
nearest_dat = nearest_dat[['OBJECTID', 'nearest']]
nn = nearest_dat.groupby(['OBJECTID'],sort=False).sum().reset_index()


#### plot naive solutions
area = "Hilltop"
sols = []
objs = []

for i in range(5):
    sol = generate_naive_solutions(gap, nn, 19000)
    
    avg_gain = []
    for i in grp:
        obj_val = obj(gap['%s_new'%i], gap['%s_old'%i], sol)
        avg_gain.append(obj_val)
    
    sols.append(sol)
    objs.append(avg_gain)

objs = pd.DataFrame(objs)
objs['sols'] = sols

objs.to_csv(r'Output\hilltop_naive_solution.csv')
objs.to_pickle(r'Output\hilltop_naive_solution.pkl')






