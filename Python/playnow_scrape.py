import requests
import pandas as pd
from bs4 import BeautifulSoup

win_url = 'https://www.playnow.com/sports?action=GoAjaxEvType&ev_oc_grp_id=389673'
top5_url = 'https://www.playnow.com/sports?action=GoAjaxEvType&ev_oc_grp_id=390354'
top20_url = 'https://www.playnow.com/sports?action=GoAjaxEvType&ev_oc_grp_id=391714'


r = requests.get(win_url)
win = []
for soup in BeautifulSoup(r.content, 'html.parser').find_all('tr'):
    new = {}
    new["Player.Name"] = soup.find('td', {"class":"eventInfoLeft"}).get_text().replace(' \n\n', '')
    new["Win"] = float(soup.find('a', {"class":"price-active control-add-seln marketOdds "}).get_text().replace('\n', '').replace('\t', ''))
    win.append(new)
win = pd.DataFrame(win)

r = requests.get(top5_url)
top5 = []
for soup in BeautifulSoup(r.content, 'html.parser').find_all('tr'):
    new = {}
    new["Player.Name"] = soup.find('td', {"class":"eventInfoLeft"}).get_text().replace(' \n\n', '')
    new["Top5"] = float(soup.find('a', {"class":"price-active control-add-seln marketOdds "}).get_text().replace('\n', '').replace('\t', ''))
    top5.append(new)
top5 = pd.DataFrame(top5)


r = requests.get(top20_url)
top20 = []
for soup in BeautifulSoup(r.content, 'html.parser').find_all('tr'):
    new = {}
    new["Player.Name"] = soup.find('td', {"class":"eventInfoLeft"}).get_text().replace(' \n\n', '')
    new["Top20"] = float(soup.find('a', {"class":"price-active control-add-seln marketOdds "}).get_text().replace('\n', '').replace('\t', ''))
    top20.append(new)
top20 = pd.DataFrame(top20)

first = pd.merge(win, top5, on="Player.Name")
final = pd.merge(first, top20, on="Player.Name")

final["Win"] = 1 / final["Win"]
final["Top5"] = 1 / final["Top5"]
final["Top20"] = 1 / final["Top20"]

final.loc[final['Player.Name'].str.split().str.len() == 2, 'Player.Name'] = \
            final['Player.Name'].str.split().str[-1] + ', ' + final['Player.Name'].str.split().str[0]
 
final.loc[final['Player.Name'].str.split().str.len() > 2, 'Player.Name'] = \
            final['Player.Name'].str.split().str[1] + ' ' + final['Player.Name'].str.split().str[2] + \
            ', ' + final['Player.Name'].str.split().str[0]


final.to_csv('~/Dropbox/Prediction Model/playnow_odds.csv', sep=',', index=False)
