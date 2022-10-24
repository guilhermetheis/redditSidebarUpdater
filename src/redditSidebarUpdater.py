# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 12:29:06 2022

@author: Guilherme Theis
"""


## Import space
import pandas as pd
import numpy as np
import re

## functions space
def remove(list):
    pattern = '[0-9]'
    list = [re.sub(pattern, '', i) for i in list]
    return list

## LUTS space


LUT_Teams_newRed = {
        'Philadelphia':'[Philly](/r/sixers)',
        'Miami':'[Heat](/r/heat)',
        'Orlando':'[Magic](/r/OrlandoMagic)',
        'Chicago': '[Bulls](/r/chicagobulls)',
        'Cleveland':'[Cavs](/r/clevelandcavs)',
        'Washington':'[Wizards](/r/washingtonwizards)',
        'New York':'[Knicks](/r/NYKnicks)',
        'Memphis':'[Memphis](/r/memphisgrizzlies)',
        'Detroit':'[Pistons](/r/DetroitPistons)',
        'Oklahoma City':'[Thunder](/r/Thunder)',
        'Atlanta':'[Hawks](/r/AtlantaHawks)',
        'New Orleans':'[Pelicans](/r/NOLAPelicans)',
        'Dallas':'[Dallas](/r/Mavericks)',
        'Sacramento':'[Kings](/r/kings)',
        'Charlotte':'[Hornets](/r/CharlotteHornets)',
        'Brooklyn':'[Nets](/r/GoNets)',
        'Toronto':'[Raptors](/r/torontoraptors)',
        'Phoenix':'[Suns](/r/suns)',
        'Golden State':'[Warriors](/r/warriors)',
        'LA':'[Clippers](LAClippers)',
        'Los Angeles':'[Lakers](/r/lakers)',
        'Indiana':'[Pacers](/r/pacers)',
        'Milwaukee':'[Bucks](/r/MkeBucks)',
        'Houston':'[Houston](/r/rockets)',
        'Denver':'[Denver](/r/denvernuggets)',
        'San Antonio':'[Spurs](/r/NBASpurs)',
        'Portland':'[Blazers](/r/ripcity)',
        'Utah':'[Jazz](UtahJazz)',
        'Minnesota':'[Wolves](/r/timberwolves)'   
    }

LUT_Teams_oldRed = {
        'Philadelphia':'[](/r/sixers)',
        'Miami':'[](/r/heat)',
        'Orlando':'[](/r/OrlandoMagic)',
        'Chicago': '[](/r/chicagobulls)',
        'Cleveland':'[](/r/clevelandcavs)',
        'Washington':'[](/r/washingtonwizards)',
        'New York':'[](/r/NYKnicks)',
        'Memphis':'[](/r/memphisgrizzlies)',
        'Detroit':'[](/r/DetroitPistons)',
        'Oklahoma City':'[](/r/Thunder)',
        'Atlanta':'[](/r/AtlantaHawks)',
        'New Orleans':'[](/r/NOLAPelicans)',
        'Dallas':'[](/r/Mavericks)',
        'Sacramento':'[](/r/kings)',
        'Charlotte':'[](/r/CharlotteHornets)',
        'Brooklyn':'[](/r/GoNets)',
        'Toronto':'[](/r/torontoraptors)',
        'Phoenix':'[](/r/suns)',
        'Golden State':'[](/r/warriors)',
        'LA':'[](LAClippers)',
        'Los Angeles':'[](/r/lakers)',
        'Indiana':'[](/r/pacers)',
        'Milwaukee':'[](/r/MkeBucks)',
        'Houston':'[](/r/rockets)',
        'Denver':'[](/r/denvernuggets)',
        'San Antonio':'[](/r/NBASpurs)',
        'Portland':'[](/r/ripcity)',
        'Utah':'[](UtahJazz)',
        'Minnesota':'[](/r/timberwolves)'   
    }

#Roster
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
outputRoster_df.to_markdown('../outputs/roster.md',index=False)

#Schedule

month = datetime.today().strftime('%b')

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

boleeanPlayed = table_schedule_playedGames['DATE'].str.contains(month)

boleeanToBePlayed = table_schedule_toBePlayed['DATE'].str.contains(month)

finaltable_schedule_playedGames = table_schedule_playedGames[boleeanPlayed]
finaltable_schedule_toBePlayed = table_schedule_toBePlayed[boleeanToBePlayed]

finaltable_schedule_playedGames = finaltable_schedule_playedGames[['DATE', 'OPPONENT','RESULT']]
finaltable_schedule_toBePlayed = finaltable_schedule_toBePlayed[['DATE', 'OPPONENT','TIME']]
final_schedule = pd.concat([finaltable_schedule_playedGames, finaltable_schedule_toBePlayed], axis=0, ignore_index=True)
final_schedule = final_schedule.fillna('')

final_schedule.to_markdown('../outputs/schedule.md',index=False)

#Standings

standings_url = 'https://www.espn.com/nba/standings'

standings_teamNames = pd.read_html(standings_url)[0]
standings_records = pd.read_html(standings_url)[1]
a =standings_teamNames.columns.to_frame()

a = a.rename(columns={a.columns[0]:standings_teamNames.columns[0]})


standings_teamNames = pd.concat([a,standings_teamNames])

standings_teamNames = standings_teamNames.rename(columns={standings_teamNames.columns[0]:'Team'})

standings_teamNames = standings_teamNames.reset_index(drop=True)

standings_teamNames['Team']

finalStandings = pd.concat([standings_teamNames,standings_records['W'],standings_records['L'],standings_records['PCT'],standings_records['GB']], axis =1)

finalStandings = finalStandings.rename(columns={'PCT':'W%'})

finalStandings.to_markdown('../outputs/standings.md',index=False)
