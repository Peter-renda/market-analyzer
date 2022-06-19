from urllib.request import urlopen, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import requests
from html.parser import HTMLParser
import pandas as pd 
from pandas import DataFrame
import csv
import numpy as np 


towns = ['easton', 'bethlehem', 'allentown', 'pottstown', 'phoenixville',
'philadelphia', 'pittsburgh', 'state-college' ,
'fountain-hill', 'coopersburg', 'emmaus', 'trexlertown', 'macungie', 'alburtis', 'breinigsville',
'east-greenville', 'green-lane', 'lansdale', 'quakertown']


#base URL of the site. The rest of the url follows the
#convention 'city-state_abbreviation' 
base_url = "https://datausa.io/profile/geo/"


url_list = []
for n in range(len(towns)):
    url = f'{base_url}{towns[n]}{"-pa"}'
    url_list.append(url)



#Webscraping at each site to find town name, pop, pop growth, median age, household income and income growth

all_info = []
for eachURL in url_list: 
    req = Request(eachURL, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(req).read()
    soup = BeautifulSoup(data, "html.parser")
    #prints out the title
    town = soup.find('title').contents[0]
    town = str(town)
    town = town.split(',')[0]
    #prints out the population
    population = soup.find("div", {"data-reactid": "50"})
    for child in population.children:
        population = child.contents[0]
        population = population.replace(',' , '')
    #prints out growth grate
    growthRate = soup.find("div", {"data-reactid": "51"})
    for child in growthRate.children:
        growthRate = child.contents[0]
        growthRate = str(growthRate)
        growthRate, direction = growthRate.split('%')        
    #prints out median age
    medianAge = soup.find("div", {"data-reactid": "54"})
    for child in medianAge.children:
        medianAge = child.contents[0]
    #prints out median household income
    householdIncome = soup.find("div", {"data-reactid": "58"})
    for child in householdIncome.children:
        householdIncome = child.contents[0]
        householdIncome = str(householdIncome)
        householdIncome = householdIncome.replace('$', '').replace(',', '')
    #prints out household income growth rate
    incomeGrowth = soup.find("div", {"data-reactid": "59"})
    for child in incomeGrowth.children:
        incomeGrowth = child.contents[0]
        incomeGrowth = str(incomeGrowth)
        incomeGrowth, direction2 = incomeGrowth.split('%')
    info = town, population, growthRate, direction, medianAge, householdIncome, incomeGrowth, direction2
    all_info.append(info)


    db_columns =  ['town', 'population', 'growthRate', 'direction', 'medianAge', 'householdIncome', 'incomeGrowth', 'direction2']
    df = pd.DataFrame(columns = db_columns, data= all_info)


#exports pandas database as an excel file
writer = pd.ExcelWriter('C:/Users/p1sto/OneDrive/Desktop/WebScraper/Real_Estate/market_research.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name = 'Sheet1')
writer.save()


    
print('Done')





# Uncomment if you need a csv instead of an xlsx file!!

# #writes all info to a csv file. Delete lines 70-71 and 74-77
#  with open('C:/Users/p1sto/OneDrive/Desktop/WebScraper/Real_Estate/market_research.csv', 'w') as output:
#     writer = csv.writer(output, lineterminator='\n', delimiter='\t')
#     for val in all_info:
#         writer.writerow(val)  