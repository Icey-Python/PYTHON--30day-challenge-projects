from bs4 import BeautifulSoup
import requests

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
        category_obj |= {f"{category_name}":{}}
        categories[0].update(category_obj)

def get_in_category_fixtures():
    get_categories()
    category_fixtures_raw = full_data_raw.find_all('tr')
    working_category = ""
    for fixture in category_fixtures_raw:
        if fixture.get_text() in categories[0].keys():
            working_category = fixture.get_text()
        else:
            category_data_raw = fixture.find_all('td',{'class':'standardbunka'})
            category_data =[]
            for category_team in category_data_raw:
                category_data.append(category_team.text)
            

            # away_team= fixture.find_all('td',{'class':'standardbunka'})[2].get_text()
            # category_fixtures_obj={}
            # category_fixtures_obj|={
            #     "home_team":home_team,
            #     "away_team":away_team
            # }
            # print(category_fixtures_obj)

def structure_data():
    pass

get_in_category_fixtures()