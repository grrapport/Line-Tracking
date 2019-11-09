import requests
import datetime
import xml.etree.ElementTree as ET
import Game_Lines
import jsonpickle
import json


bookmaker_url = "http://lines.bookmaker.eu/"


def get_bookmaker_odds(league_id):
    odds_avail = []
    bookmaker_response = requests.get(bookmaker_url).content
    root = ET.fromstring(bookmaker_response)
    for child in root.findall("./Leagues/league"):
        if child.attrib['IdLeague'] == str(league_id):
            league_elem = child
            break

    for child in league_elem.findall("./game"):
        try:
            odd_xml = child.findall("./line")[0]
            game_time = datetime.datetime.strptime(child.attrib["gmdt"]+" "+child.attrib["gmtm"], "%Y%m%d %H:%M:%S")
            #game_time = datetime.datetime.strptime("2019 11 09", "%Y %%m %d")
            line_time = datetime.datetime.now()
            game = Game_Lines.FullGameLine(game_time, line_time, "Bookmaker", odd_xml.attrib['unt'], odd_xml.attrib['unoddst'], odd_xml.attrib['ovoddst'], child.attrib['htm'], odd_xml.attrib['hoddst'], odd_xml.attrib['hsprdt'], odd_xml.attrib['hsprdoddst'], child.attrib['vtm'], odd_xml.attrib['voddst'], odd_xml.attrib['vsprdt'], odd_xml.attrib['vsprdoddst'])
            odds_avail.append(game)
        except Exception as e:
            print(e)
            continue
    return odds_avail

#4 is ncaab game lines
#get_bookmaker_odds(205) #205 is ncaab first half lines


for odd in get_bookmaker_odds(4):
    print(odd.team1+str(odd.team1_moneyline)+odd.team2+str(odd.team2_moneyline))
    print(odd.total)
    print(odd.team1_spread)


