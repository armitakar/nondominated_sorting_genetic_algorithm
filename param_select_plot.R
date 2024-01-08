library(dplyr)
library(ggplot2)
library(gridExtra)

dat1 = read.csv("E:/PhD work/Inclusive_accessibility_project_work/ga_application/hilltop_sorted_len_29000.csv")
dat11 = dat1 %>% filter(dat1$sol_type != 'Dominated')
dat11$n = nrow(dat11)
  
dat2 = read.csv("E:/PhD work/Inclusive_accessibility_project_work/ga_application/hilltop_sorted_len_19000.csv")
dat22 = dat2 %>% filter(dat2$sol_type != 'Dominated')
dat22$n = nrow(dat22)

dat3 = read.csv("E:/PhD work/Inclusive_accessibility_project_work/ga_application/hilltop_sorted_len_9000.csv")
dat33 = dat3 %>% filter(dat3$sol_type != 'Dominated')
dat33$n = nrow(dat33)

dat4 = read.csv("E:/PhD work/Inclusive_accessibility_project_work/ga_application/hilltop_sorted_len_4000.csv")
dat44 = dat4 %>% filter(dat4$sol_type != 'Dominated')
dat44$n = nrow(dat44)

dat = rbind(dat11, dat22, dat33, dat44)

dat$pcrossover = as.factor(dat$pcrossover)
dat$pmutation = as.factor(dat$pmutation)
dat$numgen = as.factor(dat$numgen)
dat$popsize = as.factor(dat$popsize)
dat$min_len = as.factor(dat$min_len)

pcrossover = dat %>% group_by(pcrossover, min_len) %>% 
  summarise(total_count=n(),
            n = mean(n))#%>% rename("value"="pcrossover")
pcrossover$pct_non_dominated = pcrossover$total_count/pcrossover$n

p1<-ggplot(pcrossover, aes(x=pcrossover, y=pct_non_dominated, fill=min_len)) +
  geom_bar(position="dodge", stat="identity") +
  ylab("solution (%) \n non-dom and extreme") +
  scale_fill_brewer(palette="Set3")
p1


pmutation = dat %>% group_by(pmutation, min_len) %>% 
  summarise(total_count=n(),
            n = mean(n))#%>% rename("value"="pmutation")
pmutation$pct_non_dominated = pmutation$total_count/pmutation$n

p2<-ggplot(pmutation, aes(x=pmutation, y=pct_non_dominated, fill=min_len)) +
  geom_bar(position="dodge", stat="identity") +
  ylab("solution (%) \n non-dom and extreme") +
  scale_fill_brewer(palette="Set3")
p2

numgen = dat %>% group_by(numgen, min_len) %>% 
  summarise(total_count=n(),
            n = mean(n))#%>% rename("value"="numgen")
numgen$pct_non_dominated = numgen$total_count/numgen$n

p3<-ggplot(numgen, aes(x=numgen, y=pct_non_dominated, fill=min_len)) +
  geom_bar(position="dodge", stat="identity") +
  ylab("solution (%) \n non-dom and extreme") +
  scale_fill_brewer(palette="Set3")
p3

popsize = dat %>% group_by(popsize, min_len) %>% 
  summarise(total_count=n(),
            n = mean(n))#%>% rename("value"="popsize")
popsize$pct_non_dominated = popsize$total_count/popsize$n

p4<-ggplot(popsize, aes(x=popsize, y=pct_non_dominated, fill=min_len)) +
  geom_bar(position="dodge", stat="identity") +
  ylab("solution (%) \n non-dom and extreme") +
  scale_fill_brewer(palette="Set3")
p4



grid.arrange(p1, p2, p3, p4, nrow = 4)
