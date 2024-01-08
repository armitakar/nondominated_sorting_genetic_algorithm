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
                 pcrossover, pmutation):
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
        #self.elitism = elitism


def GA(param):
    print("initializing")
    population_all = [] 
    objs_all = [] 
    crowding_all = [] 
    gen = []
    
    population, objs, crowding = initialization(param.road_dat, param.nn, param.popsize, param.grp, 
                                                 param.len_min, param.len_max)
    for i in range(param.numgen):
        print("generation", i)
        
            
        population, objs, crowding = generation(
            param.road_dat, param.nn, param.popsize, param.grp, param.len_min, param.len_max, 
            population, objs, crowding, param.pcrossover, param.pmutation)
        
        if (i%5 == 0):
            population_all = population_all + population
            objs_all = objs_all + objs
            crowding_all = crowding_all + crowding
            gen = gen + [i for _ in range(len(population))]
        
    return [population_all, objs_all, crowding_all, gen]

########################## model runs ##############################

#road dataset with no sidewalk

gap1 = pd.read_csv(r'C:\Users\kar.34\GA\ga_application\mideast_sol_check.csv')
gap2 = pd.read_csv(r'C:\Users\kar.34\GA\ga_application\linden_sol_check.csv')
gap3 = pd.read_csv(r'C:\Users\kar.34\GA\ga_application\clintonville_sol_check.csv')
gap4 = pd.read_csv(r'C:\Users\kar.34\GA\ga_application\hilltop_sol_check.csv')

nearest_dat1 = pd.read_pickle(r'C:\Users\kar.34\GA\ga_application\mideast_nearest_rd_no_geom.pkl')
nearest_dat1 = nearest_dat1[['OBJECTID', 'nearest']]
nn1 = nearest_dat1.groupby(['OBJECTID'],sort=False).sum().reset_index()

nearest_dat2 = pd.read_pickle(r'C:\Users\kar.34\GA\ga_application\linden_nearest_rd_no_geom.pkl')
nearest_dat2 = nearest_dat2[['OBJECTID', 'nearest']]
nn2 = nearest_dat2.groupby(['OBJECTID'],sort=False).sum().reset_index()

nearest_dat3 = pd.read_pickle(r'C:\Users\kar.34\GA\ga_application\clintonville_nearest_rd_no_geom.pkl')
nearest_dat3 = nearest_dat3[['OBJECTID', 'nearest']]
nn3 = nearest_dat3.groupby(['OBJECTID'],sort=False).sum().reset_index()

nearest_dat4 = pd.read_pickle(r'C:\Users\kar.34\GA\ga_application\hilltop_nearest_rd_no_geom.pkl')
nearest_dat4 = nearest_dat4[['OBJECTID', 'nearest']]
nn4 = nearest_dat4.groupby(['OBJECTID'],sort=False).sum().reset_index()

# set group names
grp = ['male_high_white', 'female_high_white', 
       'male_high_poc', 'female_high_poc', 
       'male_med_white', 'female_med_white', 
       'male_med_poc', 'female_med_poc', 
       'male_low_white', 'female_low_white',
       'male_low_poc', 'female_low_poc']



#set parameters
param_dict = {
    "numgen" : 51, #100
    "popsize" : 1000, #100
    "min_len" : 19000, 
    "pcrossover" : 0.9, #0.7
    "pmutation" : 0}

gap = [gap1, gap2, gap3, gap4]
nn = [nn1, nn2, nn3, nn4]
output_file_name = ["mideast_sol", "linden_sol",
                    "clintonville_sol", "hilltop_sol"
                    ]
######################### define task #####################################

def task(gap, nn, output_file):
    # create dataframe
    df1 = pd.DataFrame(columns=['objs%s'%(i+1) for i in range(len(grp))])
    df1['sols'] = 0
    df1['fitness'] = 0
    df1[['numgen', 'popsize', 'min_len', 'max_len', 'pcrossover', 'pmutation', 'generation']] = 0     
    param_done = []
    
    #print(i, flush = True)
    sys.stdout.flush()
    param = Parameters(road_dat = gap, 
                        nn = nn,
                        numgen = param_dict['numgen'], 
                        popsize = param_dict['popsize'], 
                        grp = grp, 
                        #ws = param_list[i]['ws'], 
                        len_min = param_dict['min_len'], 
                        len_max = param_dict['min_len'] + 1000,
                        pcrossover = param_dict['pcrossover'], 
                        pmutation = param_dict['pmutation'])

    result = GA(param)
    df = pd.DataFrame(index=range(len(result[0])), columns=['objs%s'%(_+1) for _ in range(len(grp))])
    #df[['w%s'%(_+1) for _ in range(len(grp))]] = param_list[i]['ws']
    
    for _ in range(len(grp)):
        df[['objs%s'%(_+1) for _ in range(len(grp))]] = [result[1][_] for _ in range(len(result[0]))]

    df['sols'] = [result[0][_] for _ in range(len(result[0]))]
    df['fitness'] = [result[2][_] for _ in range(len(result[0]))]
    df['numgen'] = param_dict['numgen']
    df['popsize'] = param_dict['popsize']
    df['pcrossover'] = param_dict['pcrossover']
    df['pmutation'] = param_dict['pmutation']
    df['min_len'] = param_dict['min_len']
    df['max_len'] = param_dict['min_len'] +1000
    df['generation'] = [result[3][_] for _ in range(len(result[0]))]
    #df['sigma'] = param_list[i]['sigma']
    #df['alpha'] = param_list[i]['alpha']
    df1 = pd.concat([df1, df], ignore_index = True)
    
    #param_done.append(param_dict[i])
    
    
    #print('exporting', i)
    df1.to_pickle(r"C:\Users\kar.34\GA\ga_application\%s.pkl"%output_file)
    df1.to_csv(r'C:\Users\kar.34\GA\ga_application\%s.csv'%output_file)
        
        

########################## run the processes ##########################

if __name__ == '__main__':
    start_time = time.perf_counter()
    pool = mp.Pool(processes=4)
    var = [[gap[j], nn[j], output_file_name[j]] for j in range(len(gap))]
    res = pool.starmap(task, var)
    pool.close()
    pool.join()
    finish_time = time.perf_counter()
    print(f"Program finished in {finish_time-start_time} seconds")
    print ("all done")
    

        









