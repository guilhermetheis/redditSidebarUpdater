# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 12:29:06 2022

@author: Guilherme Theis
"""


## Import space
import pandas as pd
import numpy as np
import re
from datetime import datetime
from pytz import timezone
#import praw


## functions space
def remove(list):
    pattern = '[0-9]'
    list = [re.sub(pattern, '', i) for i in list]
    return list

## LUTS space

LUT_Standings_newRed = {         
        'Milwaukee Bucks':'[Bucks](/r/MkeBucks)',
         'Boston Celtics':'[Celtics](/r/bostonceltics)',
    'Charlotte Hornets':'[Hornets](/r/CharlotteHornets)',
     'Cleveland Cavaliers':'[Cavs](/r/clevelandcavs)',
         'New York Knicks':'[Knicks](/r/NYKnicks)',
      'Washington Wizards':'[Wizards](/r/washingtonwizards)',
           'Atlanta Hawks':'[Hawks](/r/AtlantaHawks)',
         'Toronto Raptors':'[Raptors](/r/torontoraptors)',
           'Chicago Bulls':'[Bulls](/r/chicagobulls)',
           'Brooklyn Nets':'[Nets](/r/GoNets)',
        'Detroit Pistons':'[Pistons](/r/DetroitPistons)',
     'Philadelphia 76ers':'[Philly](/r/sixers)',
         'Indiana Pacers':'[Pacers](/r/pacers)',
             'Miami Heat':'[Heat](/r/heat)',
          'Orlando Magic':'[Magic](/r/OrlandoMagic)'
    }

LUT_Standings_oldRed = {         
        'Milwaukee Bucks':'[](/r/mkebucks) Bucks',
         'Boston Celtics':'[](/r/bostonceltics) Celtics',
    'Charlotte Hornets':'[](/r/charlottehornets) Hornets',
     'Cleveland Cavaliers':'[](/r/clevelandcavs) Cavs',
         'New York Knicks':'[](/r/nyknicks) Knicks',
      'Washington Wizards':'[](/r/washingtonwizards) Wizards',
           'Atlanta Hawks':'[](/r/atlantahawks) Hawks',
         'Toronto Raptors':'[](/r/torontoraptors) Raptors',
           'Chicago Bulls':'[](/r/chicagobulls) Bulls',
           'Brooklyn Nets':'[](/r/gonets) Nets',
        'Detroit Pistons':'[](/r/detroitpistons) Pistons',
     'Philadelphia 76ers':'[](/r/sixers) Philly',
         'Indiana Pacers':'[](/r/pacers) Pacers',
             'Miami Heat':'[](/r/heat) Heat',
          'Orlando Magic':'[](/r/orlandomagic) Magic'
    }

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
        'Orlando':'[](/r/orlandomagic)',
        'Chicago': '[](/r/chicagobulls)',
        'Cleveland':'[](/r/clevelandcavs)',
        'Washington':'[](/r/washingtonwizards)',
        'New York':'[](/r/nyknicks)',
        'Memphis':'[](/r/memphisgrizzlies)',
        'Detroit':'[](/r/detroitpistons)',
        'Oklahoma City':'[](/r/thunder)',
        'Atlanta':'[](/r/atlantahawks)',
        'New Orleans':'[](/r/nolapelicans)',
        'Dallas':'[](/r/mavericks)',
        'Sacramento':'[](/r/kings)',
        'Charlotte':'[](/r/charlottehornets)',
        'Brooklyn':'[](/r/gonets)',
        'Toronto':'[](/r/torontoraptors)',
        'Phoenix':'[](/r/suns)',
        'Golden State':'[](/r/warriors)',
        'LA':'[](laclippers)',
        'Los Angeles':'[](/r/lakers)',
        'Indiana':'[](/r/pacers)',
        'Milwaukee':'[](/r/mkebucks)',
        'Houston':'[](/r/rockets)',
        'Denver':'[](/r/denvernuggets)',
        'San Antonio':'[](/r/nbaspurs)',
        'Portland':'[](/r/ripcity)',
        'Utah':'[](utahjazz)',
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
    nameAndLink = '[' + table_roster_dropped['Name'][i].split(' ',1)[1] +']('+name_link_dict[table_roster_dropped['Name'][i]]+')'
    tempSalary = str(table_roster_dropped['Salary'][i]) + 'M'
    outputRoster.append(
        {
            'Name':nameAndLink,
            'Age':table_roster_dropped['Age'][i],
            'Salary': tempSalary
        }
    )

outputRoster_df = pd.DataFrame(outputRoster)


allStats = []
for index, row in table_roster_dropped.iterrows():
    #print(row)
    dataread = pd.read_html(name_link_dict[row['Name']])
    if len(dataread)>1:
        
        if 'GP' in dataread[2].columns:
            allStats.append(
                {   
                    'Name':row['Name'],
                    'PPG':dataread[2]['PTS'][0],
                    'FG%':dataread[2]['FG%'][0],
                    '3P%':dataread[2]['3P%'][0],
                    'RBG': dataread[2]['REB'][0],
                    'APG': dataread[2]['AST'][0],
                    'STOCK':sum(dataread[2]['BLK']+dataread[2]['STL'])
                    })
        else:
            
            allStats.append({   
                'Name':row['Name'],
                'PPG':np.nan,
                'FG%':np.nan,
                '3P%':np.nan,
                'RBG':np.nan,
                'APG':np.nan,
                'STOCK':(np.nan)
                })
    else:
        allStats.append({   
            'Name':row['Name'],
            'PPG':np.nan,
            'FG%':np.nan,
            '3P%':np.nan,
            'RBG':np.nan,
            'APG':np.nan,
            'STOCK':(np.nan)
            })
        



allStats_df = pd.DataFrame(allStats)
dict_lookup = dict(zip(allStats_df['Name'], outputRoster_df['Name']))
allStats_df = allStats_df.replace({'Name':dict_lookup})

allStats_df.to_markdown('/home/theis159/redditSidebarUpdater/outputs/roster.md',stralign='center', numalign='center',index=False)

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
final_schedule['RESULT'] = final_schedule['RESULT'].replace('W', 'W ', regex=True)
final_schedule['RESULT'] = final_schedule['RESULT'].replace('L', 'L ', regex=True)

pre_split =  final_schedule['OPPONENT'].str.split('(?=[A-Z])').str[0]

final_schedule['OPPONENT'] = final_schedule['OPPONENT'].str.split(r'vs |@ ').str[1]
final_schedule_new = final_schedule.copy()
final_schedule_old = final_schedule.copy()
final_schedule_new = final_schedule_new.replace({'OPPONENT':LUT_Teams_newRed})
final_schedule_old = final_schedule_old.replace({'OPPONENT':LUT_Teams_oldRed})
final_schedule_new['OPPONENT'] = pre_split+final_schedule_new['OPPONENT']
final_schedule_old['OPPONENT'] = pre_split+final_schedule_old['OPPONENT']

final_schedule_new.to_markdown('/home/theis159/redditSidebarUpdater/outputs/new_schedule.md', stralign='center',numalign='center',index=False)
final_schedule_old.to_markdown('/home/theis159/redditSidebarUpdater/outputs/old_schedule.md', stralign='center',numalign='center',index=False)

#Standings

standings_url = 'https://www.espn.com/nba/standings'

standings_teamNames = pd.read_html(standings_url)[0]
standings_records = pd.read_html(standings_url)[1]
a =standings_teamNames.columns.to_frame()

a = a.rename(columns={a.columns[0]:standings_teamNames.columns[0]})


standings_teamNames = pd.concat([a,standings_teamNames])

standings_teamNames = standings_teamNames.rename(columns={standings_teamNames.columns[0]:'Team'})

standings_teamNames = standings_teamNames.reset_index(drop=True)


standings_teamNames['Team'] = standings_teamNames['Team'].str.split('^\w*([A-Z]{1}[a-z]+.*)$', regex=True).str[1]

standings_records['GB'] = standings_records['GB'].str.replace('-', '0',regex=True)
standings_records['GB'] = standings_records['GB'].replace(0, np.nan)


finalStandings = pd.concat([standings_teamNames,standings_records['W'],standings_records['L'],pd.to_numeric(standings_records['PCT'], downcast='float'), pd.to_numeric(standings_records['GB'], downcast='float')], axis =1)

finalStandings = finalStandings.rename(columns={'PCT':'W%'})
finalStandings['W%'] = finalStandings['W%'].astype('float64')
finalStandings['GB'] = finalStandings['GB'].astype('float64')

finalStandings_oldRed = finalStandings.copy()
finalStandings_oldRed = finalStandings_oldRed.replace({'Team':LUT_Standings_oldRed})

finalStandings_newRed = finalStandings.copy()
finalStandings_newRed = finalStandings_newRed.replace({'Team':LUT_Standings_newRed})

finalStandings_newRed.to_markdown('/home/theis159/redditSidebarUpdater/outputs/standings_new.md', stralign='left',numalign='center', index=False, floatfmt='.3f')
finalStandings_oldRed.to_markdown('/home/theis159/redditSidebarUpdater/outputs/standings_old.md', stralign='left',numalign='center', index=False, floatfmt='.3f')


# PRAW stuff

#get timezone

now_time = datetime.now(timezone('America/New_York'))
updateTime = 'Last Update ' + now_time.strftime('%H:%M, %m/%d/%Y') + ' EDT'

#create old reddit sidebar

f = open("/home/theis159/redditSidebarUpdater/outputs/old_schedule.md", "r")
oldScheduleVar = f.read()+'\n\n'+updateTime
f = open("/home/theis159/redditSidebarUpdater/outputs/standings_old.md", "r")
oldStandingVar = f.read()+'\n\n'+updateTime
f = open("/home/theis159/redditSidebarUpdater/outputs/roster.md", "r")
oldRosterVar = f.read() +'\n\n'+updateTime
f = open("/home/theis159/redditSidebarUpdater/outputs/restOfSidebar.md", "r")
restOfOldReddit = f.read()

oldSidebar = '#Schedule \n\n' + oldScheduleVar + '\n\n#Regular Season Stats \n\n' + oldRosterVar + '\n\n#Standings \n\n' + oldStandingVar + '\n\n' + restOfOldReddit

reddit = praw.Reddit('Bot1', user-agent='bot1 user agent')
bostonceltics = reddit.subreddit('bostoncelticsmods')
widgets = subreddit.widgets #for newReddit


f = open("/home/theis159/redditSidebarUpdater/outputs/new_schedule.md", "r")
newScheduleVar = f.read()+'\n\n'+updateTime
f = open("/home/theis159/redditSidebarUpdater/outputs/standings_new.md", "r")
newStandingVar = f.read()+'\n\n'+updateTime
f = open("/home/theis159/redditSidebarUpdater/outputs/roster.md", "r")
newRosterVar = f.read() +'\n\n'+updateTime

schedule = widgets.sidebar[1]
standings = widgets.sidebar[2]
roster = widgets.sidebar[3]

styles = {"backgroundColor": "#edeff1", "headerColor": "#349e48"}
schedule.mod.update(
    short_name="Schedule", text=newScheduleVar, styles=styles
    )

styles = {"backgroundColor": "#edeff1", "headerColor": "#349e48"}
standings.mod.update(
    short_name="Standings", text=newStandingsVar, styles=styles
    )

styles = {"backgroundColor": "#edeff1", "headerColor": "#349e48"}
roster.mod.update(
    short_name="Player Stats", text=newRosterVar, styles=styles
    )

sidebar = bostonceltics.wiki["config/sidebar"]
sidebar.edit(content=oldSidebar)

