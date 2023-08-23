import time
import requests
from bs4 import BeautifulSoup

url = 'https://www.premierleague.com/'

resp = requests.get(url)
soup = BeautifulSoup(resp.content, 'html.parser')

matchweek_number = soup.find('div', {'class': 'fixtures-abridged-header__title'})
fixtures_container = soup.find('div', {'class': 'fixtures-abridged__list js-match-list-container'})
fixtures = fixtures_container.find_all('a')

print(f"{matchweek_number.get_text()}")
for match in fixtures:
    home_team = match.find('div', {'class': 'match-fixture__team match-fixture__team--home'})
    home_team_name = home_team.find('span',{'class':'match-fixture__team-name'}).get_text()
    away_team = match.find('div', {'class': 'match-fixture__team match-fixture__team--away'})
    away_team_name = away_team.find('span',{'class':'match-fixture__team-name'}).get_text()
    kickoff = match.find('time',{'class':'match-fixture__time js-render-ko-container'}).get_text()
    match_id = match['data-matchid']
    #get the day of the match
    matchday_data = requests.get(f'https://www.premierleague.com/match/{match_id}')
    soup_date = BeautifulSoup(matchday_data.content, 'html.parser')
    match_date = soup_date.find('div',{'class':'mc-summary__info'}).get_text()
    
    print(f'\t\t{kickoff} :  {home_team_name} vs {away_team_name} \t date: {match_date}')
