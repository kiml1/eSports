#### libraries ####
library(shiny)
library(googleVis)
library(data.table)
library(tidyverse)
library(ggplot2)


#### data set ####
countryEarnings.df <- read.csv("./scrapy/countryEarnings/countryEarnings.csv")


###
plot1_1 <- countryEarnings.df %>% 
  mutate(country = ifelse(country == "Korea, Republic of", "South Korea", country)) %>% 
  mutate(country = ifelse(country == "Russian Federation", "Russia", country)) %>% 
  mutate(country = ifelse(country == "Taiwan, Republic of China", "Taiwan", country))