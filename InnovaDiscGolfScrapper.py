import gspread
import requests
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

#print(teamMemberUrl)

def memberToGoogleSheet(memberUrl):
    print(memberUrl)

#gc = gspread.service_account('discgolfproscraper-b3cb7d11da63.json')

#discSpreadsheet =  gc.open("Disc Golf")

#for memberUrl in teamMemberUrl:
    #memberPage = requests.get(memberUrl)
proPage = requests.get(teamMemberUrl[0])
proPageSoup = BeautifulSoup(proPage.content,'html.parser')
proName = proPageSoup.find('h1', class_='entry-title').text
#print(memberName)
#print(proPageSoup.prettify())
inthebag = proPageSoup.find('div', class_='site-content')
print(inthebag)
discCategories = inthebag.find_all('a')
print(discCategories)



    



