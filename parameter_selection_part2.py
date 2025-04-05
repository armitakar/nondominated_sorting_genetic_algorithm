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


########## combining all solutions of different parameter compositions  ##################
a = pd.read_csv(r'Output\hilltop_sol_0_8.csv')
b = pd.read_csv(r'Output\hilltop_sol_8_16.csv')
c = pd.read_csv(r'Output\hilltop_sol_16_28.csv')
df = pd.concat([a, b, c])
df['area'] = "Hilltop"


grp = ['male_high_white', 'female_high_white', 
       'male_high_poc', 'female_high_poc', 
       'male_med_white', 'female_med_white', 
       'male_med_poc', 'female_med_poc', 
       'male_low_white', 'female_low_white',
       'male_low_poc', 'female_low_poc']

######## identifying and sorting solutions with various numgen parameter ###############

df1 = df[df['popsize'] == 100]
df1 = df1[df1['min_len'] == 19000]
df1 = df1[df1['pcrossover'] == 0.7]
df1 = df1[df1['pmutation'] == 0.001]
df2 = df1[df1['numgen'] != 100]
df3 = df1[df1['numgen'] == 100].head(100)
df1 = pd.concat([df2, df3])

# objective function values for each solution
objs = [[df1['objs%s'%(_+1)].iloc[i] for _ in range(len(grp))] for i in range(len(df1))]
objs = np.array(objs)

# Sort and rank the population based on non-domiation fronts
fronts = fast_calculate_pareto_fronts(objs)
nondomination_rank_dict = fronts_to_nondomination_rank(fronts)
non_domiated_sorted_indicies = nondominated_sort(nondomination_rank_dict,df1['fitness'].values.tolist())
non_domiated_sorted_indicies
df1['nondomination_rank'] = [nondomination_rank_dict[i] for i in range(len(df1))]
df1['nondomination_crowding_rank'] = [non_domiated_sorted_indicies.index(i) for i in range(len(df1))]

# save the results
df1.to_csv(r'Output\param_select\hilltop_nsga2_sorted_numgen.csv')
df1.to_pickle(r'Output\param_select\hilltop_nsga2_sorted_numgen.pkl')



######## identifying and sorting solutions with various popsize parameter ###############

df1 = df[df['numgen'] == 100]
df1 = df1[df1['min_len'] == 19000]
df1 = df1[df1['pcrossover'] == 0.7]
df1 = df1[df1['pmutation'] == 0.001]
df2 = df1[df1['popsize'] != 100]
df3 = df1[df1['popsize'] == 100].head(100)
df1 = pd.concat([df2, df3])

# objective function values for each solution
objs = [[df1['objs%s'%(_+1)].iloc[i] for _ in range(len(grp))] for i in range(len(df1))]
objs = np.array(objs)

# Sort and rank the population based on non-domiation fronts
fronts = fast_calculate_pareto_fronts(objs)
nondomination_rank_dict = fronts_to_nondomination_rank(fronts)
non_domiated_sorted_indicies = nondominated_sort(nondomination_rank_dict,df1['fitness'].values.tolist())
non_domiated_sorted_indicies
df1['nondomination_rank'] = [nondomination_rank_dict[i] for i in range(len(df1))]
df1['nondomination_crowding_rank'] = [non_domiated_sorted_indicies.index(i) for i in range(len(df1))]

# save the results
df1.to_csv(r'Output\param_select\hilltop_nsga2_sorted_popsize.csv')
df1.to_pickle(r'Output\param_select\hilltop_nsga2_sorted_popsize.pkl')

######## identifying and sorting solutions with various crossover parameter ###############
df1 = df[df['numgen'] == 100]
df1 = df1[df1['popsize'] == 100]
df1 = df1[df1['min_len'] == 19000]
df1 = df1[df1['pmutation'] == 0.001]
df2 = df1[df1['pcrossover'] != 0.7]
df3 = df1[df1['pcrossover'] == 0.7].head(100)
df1 = pd.concat([df2, df3])

#df1 = df1.drop_duplicates(subset=['objs%s'%(_+1) for _ in range(len(grp))], keep='first')
objs = [[df1['objs%s'%(_+1)].iloc[i] for _ in range(len(grp))] for i in range(len(df1))]
objs = np.array(objs)
fronts = fast_calculate_pareto_fronts(objs)
nondomination_rank_dict = fronts_to_nondomination_rank(fronts)
# Sort the population
non_domiated_sorted_indicies = nondominated_sort(nondomination_rank_dict,df1['fitness'].values.tolist())
non_domiated_sorted_indicies
df1['nondomination_rank'] = [nondomination_rank_dict[i] for i in range(len(df1))]
df1['nondomination_crowding_rank'] = [non_domiated_sorted_indicies.index(i) for i in range(len(df1))]

df1.to_csv(r'Output\param_select\hilltop_nsga2_sorted_pcrossover.csv')
df1.to_pickle(r'Output\param_select\hilltop_nsga2_sorted_pcrossover.pkl')


######## identifying and sorting solutions with various pmutation parameter ###############

df1 = df[df['numgen'] == 100]
df1 = df1[df1['popsize'] == 100]
df1 = df1[df1['min_len'] == 19000]
df1 = df1[df1['pcrossover'] == 0.7]
df2 = df1[df1['pmutation'] != 0.001]
df3 = df1[df1['pmutation'] == 0.001].head(100)
df1 = pd.concat([df2, df3])

# objective function values for each solution
objs = [[df1['objs%s'%(_+1)].iloc[i] for _ in range(len(grp))] for i in range(len(df1))]
objs = np.array(objs)

# Sort and rank the population based on non-domiation fronts
fronts = fast_calculate_pareto_fronts(objs)
nondomination_rank_dict = fronts_to_nondomination_rank(fronts)
non_domiated_sorted_indicies = nondominated_sort(nondomination_rank_dict,df1['fitness'].values.tolist())
non_domiated_sorted_indicies
df1['nondomination_rank'] = [nondomination_rank_dict[i] for i in range(len(df1))]
df1['nondomination_crowding_rank'] = [non_domiated_sorted_indicies.index(i) for i in range(len(df1))]

# save the results
df1.to_csv(r'Output\param_select\hilltop_nsga2_sorted_pmutation.csv')
df1.to_pickle(r'Output\param_select\hilltop_nsga2_sorted_pmutation.pkl')



























