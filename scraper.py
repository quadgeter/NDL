from bs4 import BeautifulSoup as bs
import requests
import time
import pandas as pd
from IPython.display import display
import Player
import Injury

def parsePlayer(choice, row):
    name = row[0]
    
    match choice:
        case "passing":
            yards = float(row[1])
            tds = float(row[6])
            ints = float(row[7])

            points = ((yards * 0.04) + (tds * 4) - ints)/15
            points = round(points, 1)
            player = Player.Player(name, points)
            
            return player

        case "rushing":
            yards = float(row[1])
            tds = float(row[3])
            fums = float(row[9])

            points = (((yards * 0.1) + (tds * 6)) - (fums * 2))/15
            points = round(points, 1)
            player = Player.Player(name, points)
           
            return player

        case "recieving":
            recs = float(row[1])
            yards = float(row[2])
            tds = float(row[3])

            points = (((yards * 0.1) + (tds * 6)) + (recs * 0.5))/15
            points = round(points, 1)
            player = Player.Player(name, points)
            
            return player

        case "interceptions":
            ints = float(row[1])
            tds = float(row[2])
            
            points = ((ints * 2) + (tds * 6))/3
            points = round(points, 2)
            player = Player.Player(name, points)
            
            return player
        
    return None


def quickSort(players): # players is an arraylist
    length = len(players)
    if length <= 1:
        return players
    else:
        pivotPlayer = players.pop()
        pivot = pivotPlayer.getScore()

    players_greater = []
    players_less = []

    for player in players:
        if player.getScore() > pivot:
            players_greater.append(player)

        else:
            players_less.append(player)

    return quickSort(players_greater) + [pivotPlayer] + quickSort(players_less)


def parseInjury(row):

    name = row[0]
    pos = row[1]
    problem = row[2]
    status = row[3]

    injury = Injury.Injury(name, pos, problem, status)

    return injury


def scrapeStats(choice):

    stats_map = {
    'passing': "passing/2022/reg/all/passingyards/desc",
    'rushing': "rushing/2022/reg/all/rushingyards/desc",
    'recieving': "receiving/2022/reg/all/receivingreceptions/desc",
    "fumbles": "fumbles/2022/reg/all/defensiveforcedfumble/desc",
    'interceptions': "interceptions/2022/reg/all/defensiveinterceptions/desc",
    }

    root = 'https://www.nfl.com'
    peice1 = "/stats/player-stats/category/"
    url = root + peice1 + stats_map[choice]

    headers = []
    data = []

    response = requests.get(url)

    page = response.text

    soup = bs(page, "html.parser")

    table = soup.find('table', {"class": "d3-o-table d3-o-table--detailed d3-o-player-stats--detailed d3-o-table--sortable"})
    rows = table('tr')

    for row in rows:
        for tag in row:
            if tag.name == "th":
                headers.append(tag.get_text().strip())

    for row in rows:
        curr_row = []
        for tag in row:
            if tag.name == 'td':
                curr_row.append(tag.get_text().strip())
        if curr_row:
            data.append(curr_row)

    link = soup.find('a', {"class": "nfl-o-table-pagination__next"})


    while link is not None:
        try:
            next_url = root + link["href"]
            # print(next_url)
            response = requests.get(next_url)
            page = response.text
            soup = bs(page, "html.parser")

            link = soup.find('a', {'class', "nfl-o-table-pagination__next"})
            time.sleep(1)
            table = soup.find('table', {"class": "d3-o-table d3-o-table--detailed d3-o-player-stats--detailed d3-o-table--sortable"})
            rows = table('tr')

            for row in rows:
                for tag in row:
                    if tag.name == "th":
                        headers.append(tag.get_text().strip())

            for row in rows:
                curr_row = []
                for tag in row:
                    if tag.name == 'td':
                        curr_row.append(tag.get_text().strip())
                    if curr_row:
                        data.append(curr_row)
        except AttributeError:
            break
        except TypeError:
            break




        players = []
        names = []

        for row in data:
            name = row[0]
            if name not in names:
                players.append(parsePlayer(choice, row))
                names.append(name)

        players = quickSort(players)
        print("Successful!")

    return players



# TODO will uncomment when season begins (no injuries to scrape)


# def scrapeInjuries():

#     root = 'https://www.nfl.com'
#     peice1 = '/injuries/league/2022'
#     peice2 = '/REG2'             # TODO variable will be updated when season starts

#     url = root + peice1 + peice2
#     print(url)

#     response = requests.get(url)

#     page = response.text

#     soup = bs(page, "html.parser")

#     table = soup.find('table', {"class": "d3-o-table d3-o-table--detailed d3-o-reports--detailed"})
#     if table:
#         print("yes")
#     else:
#         print("no")
#     rows = table('tr')

#     headers = []
#     data = []


#     for row in rows:
#         for tag in row:
#             if tag.name == "th":
#                 headers.append(tag.get_text().strip())

#     for row in rows:
#         curr_row = []
#         for tag in row:
#             if tag.name == 'td':
#                 curr_row.append(tag.get_text().strip())
#         if curr_row:
#             data.append(curr_row)

#     table = soup.find('table', {"class": "d3-o-table d3-o-table--detailed d3-o-player-stats--detailed d3-o-table--sortable"})

#     while table is not None:
#         try:
#             for row in rows:
#                 curr_row = []
#                 for tag in row:
#                     if tag.name == 'td':
#                         curr_row.append(tag.get_text().strip())
#                     if curr_row:
#                         data.append(curr_row)
#         except AttributeError:
#             break






