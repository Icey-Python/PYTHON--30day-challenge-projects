import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
url = 'https://www.premierleague.com/'

resp = requests.get(url)
soup = BeautifulSoup(resp.content, 'html.parser')

matchweek_number = soup.find('div', {'class': 'fixtures-abridged-header__title'}).get_text().strip()
fixtures_container = soup.find('div', {'class': 'fixtures-abridged__list js-match-list-container'})
fixtures = fixtures_container.find_all('a')


fixtures_list = []
#get matchday 
def get_matchday_date(match_id)-> str:
    #get the day of the match
    matchday_data = requests.get(f'https://www.premierleague.com/match/{match_id}')
    soup_date = BeautifulSoup(matchday_data.content, 'html.parser')
    global match_date
    match_date = soup_date.find('div',{'class':'mc-summary__info'}).get_text()
    return match_date
#get fixtures
for match in fixtures:
    fixture_object = {"time":"",
                      "home_team":"",
                      "away_team":"",
                      "match_id":"",
                      "date":"",
                      "matchweek":""}
    
    home_team = match.find('div', {'class': 'match-fixture__team match-fixture__team--home'})
    home_team_name = home_team.find('span',{'class':'match-fixture__team-name'}).get_text()
    away_team = match.find('div', {'class': 'match-fixture__team match-fixture__team--away'})
    away_team_name = away_team.find('span',{'class':'match-fixture__team-name'}).get_text()
    kickoff = match.find('time',{'class':'match-fixture__time js-render-ko-container'}).get_text()
    match_id = match['data-matchid']
    fixture_object |={"time":kickoff,"home_team":home_team_name,"away_team":away_team_name,"match_id":match_id,"date":'',"matchweek":matchweek_number}

    fixtures_list.append(fixture_object)

#assign date to the respective object
with ThreadPoolExecutor() as executor:
  results = executor.map(get_matchday_date, [f['match_id'] for f in fixtures_list])

  for fixture, date in zip(fixtures_list, results):
    fixture["date"] = date


print(fixtures_list)

