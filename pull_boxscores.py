
import requests
import time
from bs4 import BeautifulSoup as bs
import csv

vars = ["PlayerName","Rank",	"Game","Date","Age","Team","Away", "Opp", "Result", "Started",	"Minutes Played",    "FG", "FGA", "FGPCT","THREEPOINT","THREEPOINTATT","THREEPOINTPCT","FT","FTA","FTPCT","ORB","DRB","TRB","AST","STL","BLK","TOV","PF","PTS","GameScore","PlusMinus"]
advanced_vars = ["PlayerName", "Rank",	"Game","Date","Age","Team","Away", "Opp", "Result", "Started",	"Minutes Played", "TSPCT",	"eFGPCT",	"ORB"	,"DRB",	"TRBPCT",	"AST",	"STL"	,"BLKPCT",	"TOV",	"USGPCT",	"ORtg",	"DRtg", "GameScore"]
URL =  "http://www.basketball-reference.com/players/%s/%s/gamelog/%d/"

def readNames(f):
    # take csv file and return list of nba names, with spaces converted to dashes
    reader = csv.reader(f)
    reader.next()
    return [x[0] for x in reader]

def convertLine(line):
    data = [x.string for x in line]
    return data

def pullData(player, page, year, writer_basic, writer_adv):

    soup = bs(page.text, "html.parser")

    #Regular Season Data
    try:
        for child in soup.find(id='pgl_basic').find('tbody').children:
            if len(child) != 1:
                line = []
                for x in child.find_all("td"):
                    line.append(x)
                if len(line) > 0:
                    if line[1].string is not None:
                        writer_basic.writerow([player] + convertLine(line))
                    else:
                        filler = ["N/A"] * (len(vars) - len(convertLine(line)) - 1)
                        writer_basic.writerow([player] + convertLine(line) + filler )
        for child in soup.find(id='pgl_advanced').find('tbody').children:
            if len(child) != 1:
                line = []
                for x in child.find_all("td"):
                    line.append(x)
                if len(line) > 0:
                    if line[1].string is not None:
                        writer_adv.writerow([player] + convertLine(line))
                    else:
                        filler = ["N/A"] * (len(advanced_vars) - len(convertLine(line)) - 1)
                        writer_adv.writerow([player] + convertLine(line) + filler )
    except AttributeError:
        pass

        

def main():
    filename = "data_output.csv"
    with open(filename, 'rb') as f:
        player_names = readNames(f)

    player_names = list(set(player_names))

    filename_basic = "data_boxscores_basic.csv"
    filename_adv = "data_boxscores_adv.csv"

    with open(filename_basic, 'wb') as f:
        with open(filename_adv, 'wb') as f2:
            writer_basic = csv.writer(f)
            writer_adv = csv.writer(f2)
            writer_basic.writerow(vars)
            writer_adv.writerow(advanced_vars)
            for player in player_names:
                print player
                lastname = "".join(player.split(" ")[1:]).lower()
                firstname = player.split(" ")[0].lower()
                if firstname == "manu":
                    lastname = "ginobili"
                shorturl = lastname[:5] + firstname[:2] + "01"
                for year in range(1990, 2015):
                    print year
                    page = requests.get(URL % (lastname[0], shorturl, year))
                    if page.status_code == requests.codes.ok:
                        data = pullData(player, page, year, writer_basic, writer_adv)
                    time.sleep(0.3)
                time.sleep(5)


if __name__ == "__main__":
    main()
