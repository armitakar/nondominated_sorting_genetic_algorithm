# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:16:19 2023

@author: armit
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


########## putting everything together into class  ##################

class Parameters:
    def __init__(self, numgen, road_dat, nn, popsize, grp, len_min, len_max, 
                 pcrossover, pmutation, elitism):
        self.numgen = numgen
        self.road_dat = road_dat
        self.nn = nn
        self.popsize = popsize
        self.grp = grp
        #self.ws = ws
        self.len_min = len_min
        self.len_max = len_max
        #self.flip_prob = flip_prob
        self.pcrossover = pcrossover
        self.pmutation = pmutation
        #self.sigma = sigma
        #self.alpha = alpha
        self.elitism = elitism

def GA(param):
    population, objs, crowding = initialization(param.road_dat, param.nn, param.popsize, param.grp, 
                                                 param.len_min, param.len_max)
    for i in range(param.numgen):
        print("generation", i)
        population, objs, crowding = generation(
            param.road_dat, param.nn, param.grp, param.len_min, param.len_max, 
            population, objs, crowding, param.pcrossover, param.pmutation, param.elitism)
    return [population, objs, crowding]


########################## model runs ##############################

#road dataset with no sidewalk
gap2 = pd.read_csv(r'C:\Users\kar.34\GA\ga_application\sidewalk_gap_hilltop.csv')
#gap2 = gap2.sample(n=100)
nearest_dat = pd.read_pickle(r'C:\Users\kar.34\GA\ga_application\hilltop_nearest_rd_no_geom.pkl')
nearest_dat = nearest_dat[['OBJECTID', 'nearest']]
nn = nearest_dat.groupby(['OBJECTID'],sort=False).sum().reset_index()

# set group names
grp = ['male_high_white', 'female_high_white', 
       'male_high_poc', 'female_high_poc', 
       'male_med_white', 'female_med_white', 
       'male_med_poc', 'female_med_poc', 
       'male_low_white', 'female_low_white',
       'male_low_poc', 'female_low_poc']

# =============================================================================
# #################### assign weights  ###########################
# mandatory_weight = [0.001, 0.1, 0.3, 0.5, 0.7]
# 
# final = []
# for m in mandatory_weight:
#     rem = 1 - m   #(connectivity weight 20%)
#     ws_list = np.random.dirichlet(np.ones(11),size=12)
#     ws_list1 = [(ws_list[i]*rem).tolist() for i in range(len(ws_list))]
#     ws_list2 =[ws_list1[i].insert(i, m) for i in range(len(ws_list))]
#     for i in range(len(ws_list)):
#         final.append(ws_list1[i])
# 
# #[sum(ws_list1[i]) for i in range(len(ws_list))]
# add_w = np.random.dirichlet(np.ones(12),size=9)
# 
# for i in range(len(add_w)):
#         final.append(add_w[i])
# 
# ws = pd.DataFrame(final)
# ws.loc[len(ws.index)] = [1/12 for i in range(12)]
# 
# ws.sum(axis = 1)
# #ws.to_csv(r'E:\PhD work\Inclusive_accessibility_project_work\ga_application\weight_final.csv')
# ws = pd.read_csv(r'E:\PhD work\Inclusive_accessibility_project_work\ga_application\weight_final.csv')
# =============================================================================

###################### set parameters ###############################
param_dict = {
    "numgen" : [25, 50, 100], 
    "popsize" : [25, 50, 100],
    "min_len" : [19000],
    "pcrossover" : [0.7, 0.8, 0.9, 1],
    "pmutation" : [0.1, 0]}    

keys = param_dict.keys()
values = (param_dict[key] for key in keys)
param_comb = [dict(zip(keys, combination)) for combination in itertools.product(*values)]
print(len(param_comb))

param_comb_frac = [param_comb[30:45],
                   param_comb[45:60],
                   param_comb[60:73]]
output_file_name = ["hilltop_sol_weights_30_45", 
                    "hilltop_sol_weights_45_60", 
                    "hilltop_sol_weights_60_72"]
######################### define task #####################################

def task(param_list, output_file):
    # create dataframe
    df1 = pd.DataFrame(columns=['objs%s'%(i+1) for i in range(len(grp))])
    df1['sols'] = 0
    df1['fitness'] = 0
    df1[['numgen', 'popsize', 'min_len', 'max_len', 'pcrossover', 'pmutation']] = 0     
    param_done = []
    for i in range(len(param_list)):
        print(i, flush = True)
        sys.stdout.flush()
        param = Parameters(road_dat = gap2, 
                            nn = nn,
                            numgen = param_list[i]['numgen'], 
                            popsize = param_list[i]['popsize'], 
                            grp = grp, 
                            #ws = param_list[i]['ws'], 
                            len_min = param_list[i]['min_len'], 
                            len_max = param_list[i]['min_len'] + 1000,
                            pcrossover = param_list[i]['pcrossover'], 
                            pmutation = param_list[i]['pmutation'], 
                            #sigma = param_list[i]['sigma'],
                            #alpha = param_list[i]['alpha'],
                            elitism = True)

        result = GA(param)
        df = pd.DataFrame(index=range(len(result[0])), columns=['objs%s'%(_+1) for _ in range(len(grp))])
        #df[['w%s'%(_+1) for _ in range(len(grp))]] = param_list[i]['ws']
        
        for _ in range(len(grp)):
            df[['objs%s'%(_+1) for _ in range(len(grp))]] = [result[1][_] for _ in range(param_list[i]['popsize'])]

        df['sols'] = [result[0][_] for _ in range(param_list[i]['popsize'])]
        df['fitness'] = [result[2][_] for _ in range(param_list[i]['popsize'])]
        df['numgen'] = param_list[i]['numgen']
        df['popsize'] = param_list[i]['popsize']
        df['pcrossover'] = param_list[i]['pcrossover']
        df['pmutation'] = param_list[i]['pmutation']
        df['min_len'] = param_list[i]['min_len']
        df['max_len'] = param_list[i]['min_len'] +1000
        #df['sigma'] = param_list[i]['sigma']
        #df['alpha'] = param_list[i]['alpha']
        df1 = pd.concat([df1, df], ignore_index = True)
        
        param_done.append(param_list[i])
        
        if ((i % 5 == 0) & (i != 0)) | (i == (len(param_list)-1)):
            #print('exporting', i)
            df1.to_pickle(r"C:\Users\kar.34\GA\ga_application\%s.pkl"%output_file)
            df1.to_csv(r'C:\Users\kar.34\GA\ga_application\%s.csv'%output_file)
        
        

########################## run the processes ##########################

if __name__ == '__main__':
    start_time = time.perf_counter()
    pool = mp.Pool(processes=3)
    var = [[param_comb_frac[j], output_file_name[j]] for j in range(len(param_comb_frac))]
    res = pool.starmap(task, var)
    pool.close()
    pool.join()
    finish_time = time.perf_counter()
    print(f"Program finished in {finish_time-start_time} seconds")
    print ("all done")
    

        









