from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

roles = ['Top', 'Jungle', 'Mid', 'Bot', 'Support']
headers = ['Champion', 'Role']
data = {}

def get_url(role):
    url = f'https://lol.fandom.com/wiki/Special:RunQuery/TournamentStatistics?TS%5Bpreload%5D=TournamentByChampionRole&TS%5Brole%5D={role}&TS%5Btournament%5D=2022+Season+World+Championship%2FMain+Event&_run='
    return url

def get_soup(url):
    webpage = requests.get(url).text
    soup = BeautifulSoup(webpage, 'html.parser')
    return soup

def create(role, soup):
    url = get_url(role)
    table = soup.find('table', class_="wikitable sortable spstats plainlinks hoverable-rows")
    table_body = soup.find_all('tbody')
    table_data = table_body[0].find_all('tr')

    for i in range(3, len(table_data)):
        for r in table_data[i].find('td'):
            x = r.text.strip()
            if x in data.keys():
                data[x] += [role]
            else:
                data[x] = [role]

for role in roles:
    url = get_url(role)
    soup = get_soup(url)
    create(role, soup)

df = pd.DataFrame(data.items(), columns=headers)

df.to_excel('worlds_2022_champion_roles.xlsx')