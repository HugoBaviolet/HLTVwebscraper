import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

user_agent = UserAgent()
headers = {'User-Agent': user_agent.random}

url = 'https://www.hltv.org/matches'

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    live_matches = soup.find('div', class_="liveMatches")
    #upcoming_matches = soup.find('div', class_='upcomingMatchesAll')

    if live_matches:
        print(live_matches.get_text())
    else:
        print("Div not found")

    #if upcoming_matches:
      #  print(upcoming_matches.get_text())
    #else:
     #   print("Div not found")
else:
    print("Failed to retrieve webpage:", response.status_code)
