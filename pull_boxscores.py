
import requests
import time
from bs4 import BeautifulSoup as bs
import csv


URL =  "http://www.basketball-reference.com/players/%s/%s/gamelog/%d/"

def readNames(f):
    # take csv file and return list of nba names, with spaces converted to dashes
    reader = csv.reader(f)
    reader.next()
    return [x[0] for x in reader]


def main():
    filename = "data_output.csv"
    with open(filename, 'rb') as f:
        player_names = readNames(f)

    for player in player_names:
        print player
        lastname = "".join(player.split(" ")[1:]).lower()
        firstname = player.split(" ")[0].lower()
        if firstname == "manu":
            lastname = "ginobili"
        shorturl = lastname[:5] + firstname[:2] + "01"
        year = 2015
        print URL % ("b", shorturl, year)


    
    

if __name__ == "__main__":
    main()
