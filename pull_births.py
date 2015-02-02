
import requests
from bs4 import BeautifulSoup as bs

PROFILE_URL = "http://www.famoushookups.com/site/celebrity_profile.php"
RELATIONSHIP_URL = "http://www.famoushookups.com/site/relationship_detail.php"


def readNames():
    # take csv file and return list of nba names, with spaces converted to dashes
    return None

def getRelations(page):
    # take an HTML page and find all relationships with nonzero children
    # return list of urls with nonzero children
    soup = bs(page.text)
    kidData =  soup.find_all('td', attrs={'class':'col_rel_kids'})
    kidUrlList= []
    for kid in kidData:
        try:
            if int(kid.text) > 0:
                kidUrlList.append(kid.find('a').get('href'))
        except ValueError:
            pass
    return kidUrlList

def getChildren(page):
    # take an HTML page and find all birthdays and genders for given relationship
    # return list of dates
    soup = bs(page.text)
    kidData = soup.find('tr', attrs={'class':'rel_child_header'})
    birthDates=[]
    for child in  kidData.parent.children:
        try:
            birthDates.extend(child.find_all('td', attrs={'class':'rel_child_col2'}))
        except AttributeError:
            pass
    return [x.text for x in birthDates]
def main():
    player_names = ["Michael Jordan"]
    data = {}    
    for player_name in player_names:

        player_name2 = player_name.replace(" ", "-")
        print player_name

        payload = {'name' : player_name2}
        page = requests.get(PROFILE_URL, params=payload)

        relUrlList = getRelations(page)
        
        dateList = []
        for relation in relUrlList:
            page = requests.get(relation)
            dateList.extend(getChildren(page))
        data[player_name] = dateList
    print data

if __name__ == "__main__":
    main()





