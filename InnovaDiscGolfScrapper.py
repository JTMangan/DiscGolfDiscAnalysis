import gspread
import requests
import time
from bs4 import BeautifulSoup

innovaStarTeam = "https://www.innovadiscs.com/team-innova/star-team/"
innovaChampionTeam = "https://www.innovadiscs.com/team-innova/team-champion/"

starTeamPage = requests.get(innovaStarTeam)
starTeamSoup = BeautifulSoup(starTeamPage.content,'html.parser')
championTeamPage = requests.get(innovaChampionTeam)
championTeamSoup = BeautifulSoup(championTeamPage.content,'html.parser')

starTeamResults = starTeamSoup.find(id="tshowcase_id_0")
championTeamResults = championTeamSoup.find(id="tshowcase_id_0")

#print(starTeamResults.prettify())

innovaStarTeamMembers = starTeamResults.find_all('a', class_='')
innovaChampionTeamMembers = championTeamResults.find_all('a', class_='')

teamMemberUrl = []
for starTeamMember in innovaStarTeamMembers:
    memberUrl = starTeamMember.get('href')
    if memberUrl.find("https://www.innovadiscs.com/team/") == 0 :
        teamMemberUrl.append(memberUrl)

for championTeamMember in innovaChampionTeamMembers:
    memberUrl = championTeamMember.get('href')
    if memberUrl.find("https://www.innovadiscs.com/team/") == 0 :
        teamMemberUrl.append(memberUrl)

teamMemberUrl = list(dict.fromkeys(teamMemberUrl))
teamMemberUrl.remove("https://www.innovadiscs.com/team/eveliina-salonen/")
teamMemberUrl.remove("https://www.innovadiscs.com/team/holly-finley/")
teamMemberUrl.remove("https://www.innovadiscs.com/team/josh-anthon/")
teamMemberUrl.remove("https://www.innovadiscs.com/team/ohn-scoggins/")
teamMemberUrl.remove("https://www.innovadiscs.com/team/callie-mcmorran/")
teamMemberUrl.remove("https://www.innovadiscs.com/team/ellen-widboom/")

def gatherDiscs(url,row):
    proPage = requests.get(url)
    proPageSoup = BeautifulSoup(proPage.content,'html.parser')
    proName = proPageSoup.find('h1', class_='entry-title').text

    startSubstring = proPage.text.find('<div id="inthebag">') + len('<div id="inthebag">')
    endSubstring = proPage.text.find("<!-- .entry-content -->")
    discSubstring = proPage.text[startSubstring:endSubstring]


    distance = discSubstring[discSubstring.find('DISTANCE') + len('DISTANCE'):discSubstring.find('FAIRWAY')]
    fairway = discSubstring[discSubstring.find('FAIRWAY') + len('FAIRWAY'):discSubstring.find('MID-RANGE')]
    midrange = discSubstring[discSubstring.find('MID-RANGE') + len('MID-RANGE'):discSubstring.find('PUTT & APPROACH')]
    putter = discSubstring[discSubstring.find('PUTT & APPROACH') + len('PUTT & APPROACH'):discSubstring.find('<!-- End Tabs --!>')]

    distanceSoup = BeautifulSoup(distance, "html.parser")
    distancelinks = distanceSoup.find_all('a')
    distanceDiscs = []

    for distance in distancelinks :
        distanceDiscs.append(distance.text)

    fairwaySoup = BeautifulSoup(fairway, "html.parser")
    fairwaylinks = fairwaySoup.find_all('a')
    fairwayDiscs = []

    for fairway in fairwaylinks:
        fairwayDiscs.append(fairway.text)

    midrangeSoup = BeautifulSoup(midrange, "html.parser")
    midrangelinks = midrangeSoup.find_all('a')
    midrangeDiscs = []

    for midrange in midrangelinks:
        midrangeDiscs.append(midrange.text)

    putter = BeautifulSoup(putter, "html.parser")
    putterlinks = putter.find_all('a')
    putters = []

    for putter in putterlinks:
        putters.append(putter.text)

    memberToGoogleSheet(distanceDiscs,fairwayDiscs,midrangeDiscs,putters,proName,row)

def memberToGoogleSheet(distance, fairway, midrange, putter, name, row):
    print(name)
    gc = gspread.service_account('Your API json key')
    discSpreadsheet =  gc.open("Disc Golf")
    players = discSpreadsheet.worksheet("Players")
    distanceLetters = ['C','D','E','F','G','H','I','J','K','L']
    fairwayLetters = ['M','N','O','P']
    midrangeLetters = ['Q','R','S','T','U']
    putterLetters = ['V','W','X','Y','Z']
    players.update('A'+row,name)
    players.update('B'+row,"Innova")
    count = 0
    for disc in distance:
        players.update(distanceLetters[count]+row,disc)
        count = count + 1

    count = 0
    for disc in fairway:
        players.update(fairwayLetters[count]+row,disc)
        count = count + 1
        
    count = 0
    for disc in midrange:
        players.update(midrangeLetters[count]+row,disc)
        count = count + 1
    
    count = 0
    for disc in putter:
        players.update(putterLetters[count]+row,disc)
        count = count + 1
    time.sleep(15)
        
count = 2
for memberUrl in teamMemberUrl:
    gatherDiscs(memberUrl,str(count))
    count = count + 1