from bs4 import BeautifulSoup
import requests
import json

url = "https://www.vitibet.com/index.php?clanek=quicktips&sekce=fotbal&lang=en"
resp = requests.get(url)
soup = BeautifulSoup(resp.content,'html.parser')

full_data_raw = soup.find('table',{'id':'example'})

categories = [{}]

def get_categories():
    categories_raw = full_data_raw.find_all('tr',{'class':'odseknutiligy'})
    category_obj = {}
    for category in categories_raw:
        category_name = category.find('a').get_text()
        category_obj |= {f"{category_name}":[]}
        categories[0].update(category_obj)

def get_in_category_fixtures():
    get_categories()
    category_fixtures_raw = full_data_raw.find_all('tr')[2:]
    working_category = ""
    for fixture in category_fixtures_raw:
        if fixture.get_text() in categories[0].keys():
            working_category = fixture.get_text()
        else:
            category_data_raw = fixture.find_all('td')
            team_data_structured = []
            for team_data in category_data_raw:
                team_data_structured.append(team_data.get_text())
            try:
                home_team = team_data_structured[1]
                away_team= team_data_structured[2]
                final_score = team_data_structured[3:6]
                percentages ={
                    "home":team_data_structured[6],
                    "draw":team_data_structured[7],
                    "away":team_data_structured[8],
                }
                tip=team_data_structured[9]
                category_fixtures_obj={}
                category_fixtures_obj|={
                    "home_team":home_team,
                    "away_team":away_team,
                    "final_score":' '.join(final_score),
                    "percentages":percentages,
                    "tip":tip
                }
                (categories[0][working_category]).append(category_fixtures_obj)
            except IndexError as e:
                print(f"Error: {e}")
                pass
    return categories

with open("fixtures_and_predictions.json","w") as file:
   json.dump(get_in_category_fixtures(),file,indent=4)