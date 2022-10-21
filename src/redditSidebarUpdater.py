# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 12:29:06 2022

@author: Guilherme Theis
"""



import pandas as pd
import numpy as np
import re

def remove(list):
    pattern = '[0-9]'
    list = [re.sub(pattern, '', i) for i in list]
    return list

roster_url = 'https://www.espn.com/nba/team/roster/_/name/bos/boston-celtics'

table_roster_init = pd.read_html(roster_url)[0]
table_roster_links_init = pd.read_html(roster_url,extract_links='body')[0] 
table_roster_links = table_roster_links_init['Name']
names = []
espn_links = []
for i in range(len(table_roster_links)):
    names.append(table_roster_links[i][0])
    espn_links.append(str(table_roster_links[i][1]))
names = remove(names)
table_roster_dropped = (table_roster_init.copy())

name_link_dict = {}

for i in range(len(table_roster_links)):
    name_link_dict[names[i]] = espn_links[i]

table_roster_dropped = table_roster_dropped.drop(['Unnamed: 0'], axis=1)
table_roster_dropped['Salary'] = table_roster_dropped['Salary'].str.replace('$', '',regex=True)
table_roster_dropped['Salary'] = table_roster_dropped['Salary'].str.replace('--', '0',regex=True)
table_roster_dropped['Salary'] = table_roster_dropped['Salary'].str.replace(',', '', regex=True)
table_roster_dropped['Salary'] = table_roster_dropped['Salary'].astype(int)
table_roster_dropped['Salary'] = table_roster_dropped['Salary'].replace(0, np.nan)
table_roster_dropped.sort_values(by='Salary', inplace=True, ascending=False)
table_roster_dropped['Salary'] = table_roster_dropped['Salary'].div(1e6).round(decimals=1)
table_roster_dropped['Name'] = table_roster_dropped['Name'].str.replace('\d+', '',regex=True)
table_roster_dropped = table_roster_dropped.reset_index(drop=True)

outputRoster = []

for i in range(len(table_roster_dropped)):
    nameAndLink = '[' + table_roster_dropped['Name'][i] +']('+name_link_dict[table_roster_dropped['Name'][i]]+')'
    tempSalary = str(table_roster_dropped['Salary'][i]) + 'M'
    outputRoster.append(
        {
            'Name':nameAndLink,
            'Age':table_roster_dropped['Name'][i],
            'Salary': tempSalary
        }
    )

outputRoster_df = pd.DataFrame(outputRoster)
#outputRoster_df.to_markdown('../outputs/roster.md',index=False)

schedule_url = 'https://www.espn.com/nba/team/schedule/_/name/bos/season/2023'
table_schedule_init = pd.read_html(schedule_url)[0]
duplicatedValues = table_schedule_init.duplicated(subset=[0,1])
numRows = 0
for i in range(len(table_schedule_init)):
    if duplicatedValues[i]:
        break
    else:
        numRows = numRows+1
table_schedule_playedGames = table_schedule_init[0:numRows]
table_schedule_playedGames.columns = table_schedule_playedGames.iloc[0]
table_schedule_playedGames = table_schedule_playedGames.reset_index()
table_schedule_playedGames = table_schedule_playedGames.drop([0], axis=0)
table_schedule_toBePlayed = table_schedule_init[numRows:]
table_schedule_toBePlayed = table_schedule_toBePlayed.reset_index()
table_schedule_toBePlayed.columns = table_schedule_toBePlayed.iloc[0]
table_schedule_toBePlayed = table_schedule_toBePlayed.drop([0], axis=0)

LUT_Teams = {
        'Philadelphia':'[Philly](/r/sixers)',
        'Miami':'[Heat](/r/heat)',
        'Orlando':'[Magic](/r/OrlandoMagic)',
        'Chicago': '[Bulls](/r/chicagobulls)',
        'Cleveland':'[Cavs](/r/clevelandcavs)',
    }

