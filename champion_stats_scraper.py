from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

url = 'https://lol.fandom.com/wiki/2022_Season_World_Championship/Main_Event/Champion_Statistics'

result = requests.get(url)
soup = BeautifulSoup(result.text, 'html.parser')

table = soup.find('table', class_="wikitable sortable spstats plainlinks hoverable-rows")
table_rows = table.find_all('tr')
table_body = soup.find_all('tbody')

header = [h.text.strip() for h in table_rows[4].find_all("th")]

table_data = table_body[4].find_all("tr")

data = []

for i in range(5,99):
    row = [r.text.strip() for r in table_data[i].find_all("td")]
    data.append(row)

df = pd.DataFrame(data, columns=header)
df = df.drop(df.columns[-1], axis=1)
df.replace('-', np.NaN, inplace=True)

df.to_excel('worlds_2022_champion_stats.xlsx')