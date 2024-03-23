import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

user_agent = UserAgent()
headers = {'User-Agent': user_agent.random}

url = 'https://www.hltv.org/matches'

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    upcoming_matches = soup.find('div', class_='upcomingMatchesAll')

    if upcoming_matches:
        matches_text = upcoming_matches.get_text().strip()
        matches_list = [match.strip() for match in matches_text.split('\n\n') if
                        match.strip()]  # Split matches and remove extra spaces

        for match in matches_list:
            match_lines = match.split('\n')
            for i, line in enumerate(match_lines):
                if ':' in line:  # Check if the line contains a colon
                    if i == 0:  # Add a space above the time if it's not the first line
                        print()
                if "Odds" not in line:  # Check if the line does not contain "Odds"
                    print(line.strip().center(80))
    else:
        print("Div not found")
else:
    print("Failed to retrieve webpage:", response.status_code)
