
import requests
import time
from bs4 import BeautifulSoup as bs
import csv

PROFILE_URL = "http://www.famoushookups.com/site/celebrity_profile.php"
RELATIONSHIP_URL = "http://www.famoushookups.com/site/relationship_detail.php"


def readNames(f):
    # take csv file and return list of nba names, with spaces converted to dashes
    reader = csv.reader(f)
    reader.next()
    return [x[2] for x in reader]

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
    if kidData is None:
        return ["No Data"]
    for child in  kidData.parent.children:
        try:
            birthDates.extend(child.find_all('td', attrs={'class':'rel_child_col2'}))
        except AttributeError:
            pass
    return [x.text for x in birthDates]
def main():
    #player_names = ["Michael Jordan"]
    filename = "wikipedia_allstars_clean.csv"
    with open(filename, 'rb') as f:
        player_names = readNames(f)
    
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
        
        #Sleep to not overwhelm the server
        time.sleep(0.1)  

    with open('data_output.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['Player', 'Birthdate'])
        for key in data.keys():
            for date in data[key]:
                writer.writerow([key, date])

if __name__ == "__main__":
    main()





