Plot visualizations
================

Please note that all plots are generated using mock data and therefore
do not resemble to our actual findings.

``` r
library(dplyr)
```

    ## 
    ## Attaching package: 'dplyr'

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

``` r
library(ggplot2)
```

    ## Warning: package 'ggplot2' was built under R version 4.3.3

``` r
library(gridExtra)
```

    ## 
    ## Attaching package: 'gridExtra'

    ## The following object is masked from 'package:dplyr':
    ## 
    ##     combine

``` r
library(reshape2)
library(tidycensus)
library(tidyr)
```

    ## 
    ## Attaching package: 'tidyr'

    ## The following object is masked from 'package:reshape2':
    ## 
    ##     smiths

``` r
library(sf)
```

    ## Linking to GEOS 3.11.2, GDAL 3.7.2, PROJ 9.3.0; sf_use_s2() is TRUE

``` r
setwd("C:/Users/armit/GA/Data_and_code/")
```

##### Distribution of total solution counts by non-dominated front ranks and their variations with increased population size

``` r
dat = read.csv("Output/param_select/hilltop_nsga2_sorted_popsize.csv")
dat = dat %>% filter(nondomination_rank <4)
dat$nondomination_rank = as.factor(dat$nondomination_rank+1)
dat$popsize = as.factor(dat$popsize)

popsize = dat %>% select(nondomination_rank, popsize, area)

popsize2 = data.frame(table(popsize))
p1<-ggplot(popsize2, aes(x=nondomination_rank, y=Freq, fill=popsize)) +
  geom_bar(position="dodge", stat="identity") +
  ylab("Solution count") + xlab("Nondominated fronts") +
  scale_fill_brewer(palette="Set3", name = "Population size") +
  theme(axis.title.x = element_text(size = 12),
        axis.title.y = element_text(size = 12),
        axis.text.x = element_text(size = 12, angle = 0), 
        axis.text.y= element_text(size = 12, angle = 0),
        legend.position="bottom",
        panel.background = element_blank(),
        #panel.grid.major.x = element_line(colour = "grey"),
        panel.border = element_rect(colour = "black", fill=NA, size=0.5)) +
  facet_wrap(~area)
```

    ## Warning: The `size` argument of `element_rect()` is deprecated as of ggplot2 3.4.0.
    ## ℹ Please use the `linewidth` argument instead.
    ## This warning is displayed once every 8 hours.
    ## Call `lifecycle::last_lifecycle_warnings()` to see where this warning was
    ## generated.

``` r
p1
```

![](Plot_visualizations_files/figure-gfm/unnamed-chunk-2-1.png)<!-- -->

##### Distribution of total solution counts by non-dominated front ranks and their variations with increased number of generations

``` r
dat = read.csv("Output/param_select/hilltop_nsga2_sorted_numgen.csv")

dat = dat %>% filter(nondomination_rank <4)
dat$nondomination_rank = as.factor(dat$nondomination_rank+1)
dat$numgen = as.factor(dat$numgen)


numgen = dat %>% select(nondomination_rank, numgen, area)

numgen2 = data.frame(table(numgen))
p2<-ggplot(numgen2, aes(x=nondomination_rank, y=Freq, fill=numgen)) +
  geom_bar(position="dodge", stat="identity") +
  ylab("Solution count") + xlab("Nondominated fronts") +
  scale_fill_brewer(palette="Set3", name = "Number of generations") +
  theme(axis.title.x = element_text(size = 12),
        axis.title.y = element_text(size = 12),
        axis.text.x = element_text(size = 12, angle = 0), 
        axis.text.y= element_text(size = 12, angle = 0),
        legend.position="bottom",
        panel.background = element_blank(),
        #panel.grid.major.x = element_line(colour = "grey"),
        panel.border = element_rect(colour = "black", fill=NA, size=0.5)) +
  facet_wrap(~area)
p2
```

![](Plot_visualizations_files/figure-gfm/unnamed-chunk-3-1.png)<!-- -->

##### Distribution of total solution counts by non-dominated front ranks and their variations with increased mutation probability

``` r
dat = read.csv("Output/param_select/hilltop_nsga2_sorted_pmutation.csv")

dat = dat %>% filter(nondomination_rank <4)
dat$nondomination_rank = as.factor(dat$nondomination_rank+1)
dat$pmutation = as.factor(dat$pmutation)


pmutation = dat %>% select(nondomination_rank, pmutation, area)

pmutation2 = data.frame(table(pmutation))
p3<-ggplot(pmutation2, aes(x=nondomination_rank, y=Freq, fill=pmutation)) +
  geom_bar(position="dodge", stat="identity") +
  ylab("Solution count") + xlab("Nondominated fronts") +
  scale_fill_brewer(palette="Set3", name = "Mutation") +
  theme(axis.title.x = element_text(size = 12),
        axis.title.y = element_text(size = 12),
        axis.text.x = element_text(size = 12, angle = 0), 
        axis.text.y= element_text(size = 12, angle = 0),
        legend.position="bottom",
        panel.background = element_blank(),
        #panel.grid.major.x = element_line(colour = "grey"),
        panel.border = element_rect(colour = "black", fill=NA, size=0.5)) +
  facet_wrap(~area)
p3
```

![](Plot_visualizations_files/figure-gfm/unnamed-chunk-4-1.png)<!-- -->

##### Distribution of total solution counts by non-dominated front ranks and their variations with increased crossover probability

``` r
dat = read.csv("Output/param_select/hilltop_nsga2_sorted_pcrossover.csv")

dat = dat %>% filter(nondomination_rank <4)
dat$nondomination_rank = as.factor(dat$nondomination_rank+1)
dat$pcrossover = as.factor(dat$pcrossover)


pcrossover = dat %>% select(nondomination_rank, pcrossover, area)

pcrossover2 = data.frame(table(pcrossover))
p4<-ggplot(pcrossover2, aes(x=nondomination_rank, y=Freq, fill=pcrossover)) +
  geom_bar(position="dodge", stat="identity") +
  ylab("Solution count") + xlab("Nondominated fronts") +
  scale_fill_brewer(palette="Set3", name = "Crossover") +
  theme(axis.title.x = element_text(size = 12),
        axis.title.y = element_text(size = 12),
        axis.text.x = element_text(size = 12, angle = 0), 
        axis.text.y= element_text(size = 12, angle = 0),
        legend.position="bottom",
        panel.background = element_blank(),
        #panel.grid.major.x = element_line(colour = "grey"),
        panel.border = element_rect(colour = "black", fill=NA, size=0.5)) +
  facet_wrap(~area)
p4
```

![](Plot_visualizations_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->

#### Convergence of NSGA-II models over multiple generations

``` r
dat = read.csv("Output/hilltop_sol.csv")

dat1 = dat %>% mutate(solution = row_number())
dat1 = dat1 %>% dplyr::select('objs1', 'objs2', 'objs3',
                             'objs4', 'objs5', 'objs6',
                             'objs7', 'objs8', 'objs9',
                             'objs10', 'objs11', 'objs12', "generation", "solution")

dat1 = melt(dat1, id.vars = c("generation", "solution")) 

grp = c('High-income \n white men', 'High-income \n white women', 
        'High-income \n men of color', 'High-income \n women of color', 
        'Mid-income \n white men', 'Mid-income \n white women', 
        'Mid-income \n men of color', 'Mid-income \n women of color', 
        'Low-income \n white men', 'Low-income \n white women', 
        'Low-income \n men of color', 'Low-income \n women of color')

ggplot() +
  geom_line(data=dat1, aes(x=variable, y=value, group = solution, 
                           color=generation, alpha = generation))+
  geom_point(data=dat1, aes(x=variable, y=value)) + xlab("Social groups") + ylab("Gains in walking perceptions") +
  scale_x_discrete(labels=grp) +
  scale_alpha_continuous(range=c(0.8, 0.2),guide = 'none') +
  scale_color_continuous(type = "viridis", name = "Generation", limits = c(0, 50), breaks = c(0, 10, 20, 30, 40, 50)) +
  guides(color = guide_colorbar(barwidth = 20, barheight = 0.5)) +
  theme(axis.text.y =element_text(size=12),
        axis.text.x = element_blank(),#element_text(size=18, angle = 45),
        axis.ticks = element_blank(),
        axis.title = element_text(size=12),
        legend.position="bottom", 
        legend.title = element_text(size=12), 
        legend.text = element_text(size=12),
        panel.background = element_blank(),
        panel.grid.major = element_line(colour = "grey", linetype = "dashed"),
        panel.grid.major.y =element_blank(),
        panel.grid.minor = element_blank(),
        strip.text.x = element_text(size = 12)) 
```

![](Plot_visualizations_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->

#### Naive and extreme optimal solutions and respective walking perception gains across groups

``` r
naive = read.csv("Output/hilltop_naive_solution.csv")
naive$sol_type = "Naive solutions"
naive = naive %>% select(-c("sols", "X"))
colnames(naive) = c("objs1","objs2","objs3","objs4","objs5","objs6","objs7",
         "objs8","objs9","objs10","objs11","objs12","sol_type")

dat = read.csv("Output/hilltop_final solutions_sorted.csv")
dat = dat %>% 
  dplyr::select("objs1","objs2","objs3","objs4","objs5","objs6","objs7",
         "objs8","objs9","objs10","objs11","objs12","sol_type")
dat = rbind(naive, dat)

dat1 = dat %>% mutate(solution = row_number())
dat1 = melt(dat1, id.vars = c("solution", "sol_type")) 

dat1 = dat1 %>% filter (sol_type != "Non-dominated")
dat1$sol_type1 = ifelse(((dat1$sol_type != "Non-dominated")&
                          (dat1$sol_type != "Naive solutions")), 
                        "Extreme Solutions by income level",dat1$sol_type )

dat1 <- dat1 %>%
    mutate(Income = recode(sol_type, 'Extreme (male_high_white)' = 'High', 
                           'Extreme (female_high_white)' = 'High', 
                           'Extreme (male_high_poc)' =  'High',
                           'Extreme (female_high_poc)' = 'High',
                           'Extreme (male_med_white)' = 'Moderate', 
                           'Extreme (female_med_white)' = 'Moderate', 
                           'Extreme (male_med_poc)' =  'Moderate',
                           'Extreme (female_med_poc)' = 'Moderate',
                           'Extreme (male_low_white)' = 'Low', 
                           'Extreme (female_low_white)' = 'Low', 
                           'Extreme (male_low_poc)' =  'Low',
                           'Extreme (female_low_poc)' = 'Low',
                           ))

dat1$linesize = ifelse((dat1$sol_type == "Extreme (female_med_poc)")|
  (dat1$sol_type == "Extreme (male_high_white)")|(dat1$sol_type == "Extreme (female_low_white)"), 
  2, 0.5)


ggplot(data=dat1, aes(x=variable, y=value, group = solution)) +
  geom_line(aes(color=Income, size = linesize))+
  scale_size("Scale", range = c(0.4, 2), guide = "none") +
  #geom_line()+
  #geom_point() + 
  xlab("Social groups") + ylab("Gains in walking perceptions") +
  scale_x_discrete(labels=grp) +
  scale_alpha_manual(values = c(1, 0.3)) +
  scale_color_manual(values = c("#4daf4a","#e41a1c","#ffa500", "grey")) +
  #guides(color = guide_colorbar(barwidth = 20, barheight = 0.5)) +
  theme(axis.text.y =element_text(size=12),
        #axis.text.x =element_text(size=14, angle = 45),
        axis.text.x = element_text(size=5), 
        axis.ticks = element_blank(),
        axis.title = element_text(size=12),
        legend.position="bottom", 
        legend.title = element_text(size=12), 
        legend.text = element_text(size=12),
        panel.background = element_blank(),
        panel.grid.major = element_line(colour = "grey", linetype = "dashed"),
        panel.grid.major.y =element_blank(),
        panel.grid.minor = element_blank(),
        strip.text.x = element_text(size = 12)) 
```

    ## Warning: Using `size` aesthetic for lines was deprecated in ggplot2 3.4.0.
    ## ℹ Please use `linewidth` instead.
    ## This warning is displayed once every 8 hours.
    ## Call `lifecycle::last_lifecycle_warnings()` to see where this warning was
    ## generated.

![](Plot_visualizations_files/figure-gfm/unnamed-chunk-7-1.png)<!-- -->
