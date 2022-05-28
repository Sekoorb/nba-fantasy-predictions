from bs4 import BeautifulSoup
import requests
import urllib
import urllib.request
import re
from datetime import datetime
from pytz import timezone
import pytz
import  pandas as pd
import numpy as np

def get_pst_date():
    date_format='%Y-%m-%d'
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    pstDateTime=date.strftime(date_format)
    return pstDateTime

def scrape_depth():
    url = "http://www.espn.com/nba/depth/_/type/full"

    # We use try-except incase the request was unsuccessful because of 
    # wrong URL
    try:
        page = urllib.request.urlopen(url)
    except:
        print("Error opening the URL")

    htmlSource = page.read()  

    soup = BeautifulSoup(htmlSource, 'html.parser')

    tables = []
    for i in soup.select('div.span-1'):
        tables.append(tuple(i.select('tr.colhead, tr[class*="evenrow player-46"], tr[class*="oddrow player-46"]')))

    all_players = []
    first_name = []
    team = []
    position = []
    injury_status = []
    for table in tables:
        for row in table[1:]:
            first_name.append((re.search(r'\d/(.*?)-', str(row)).group(1)))  
            team.append(re.search(r'"colhead"><td>(.*?)</td></tr>', str(table)).group(1))
            position.append(re.search(r'td>(.*) - ', str(row)).group(1))
            injury_status.append(re.search(r'(IL)', str(row)))
            all_players.append(row)

    last_name = []
    for i, n in zip(all_players, first_name):
        last_name.append(re.search(fr'{n}-(.*?)">', str(i)).group(1))

    position_rank = []
    position_type =[]
    for i in position:
        position_rank.append(re.search(r'\d+', str(i)).group(0))
        position_type.append(re.search(r'\D+', str(i)).group(0))

    injury = []
    for i in injury_status:
        if i == None:
            injury.append("active")
        else: 
            injury.append("injured")

    date = get_pst_date()

    date_list = []
    for  i in all_players:
        date_list.append(date)

    player_names = list(zip(date_list, first_name, last_name , position, team))

    primary_key = []
    for i in player_names:
        primary_key.append('-'.join(i))
 
    depth_chart_unprocessed = list(zip(primary_key, date_list, position, first_name, last_name, injury, team, position_rank, position_type))

    df = pd.DataFrame (depth_chart_unprocessed, columns = ['primary_key', 'date', 'position', 'first_name', 
    'last_name', 'injury', 'team', 'position_rank', 'position_type'])

    injured_players = df[df['injury'] == 'injured']

    df_with_injured = pd.merge(df, injured_players[['team','position_type', 'position_rank']], on=['team','position_type'], how='outer')

    df_with_injured['increase_rank'] = np.where((df_with_injured['position_rank_y'] < df_with_injured['position_rank_x']), 'yes', 'no')

    df_with_injured['position_final'] = np.where((df_with_injured['increase_rank'] == 'yes'),
    ((df_with_injured['position_type'].astype(str))+(df_with_injured['position_rank_x'].astype(int)-1).astype(str)), df_with_injured['position'])

    df_final = df_with_injured.rename(columns={'position_rank_x': 'position_rank'})
    df_final.drop(['position_rank_y', 'position_rank', 'position_type'], inplace=True, axis=1)

    tup = [tuple(a) for a in df_final.to_numpy()]
    depth_chart = list(tup)

    return depth_chart

scrape_depth()