import requests
import datetime
import pytz
import xml.etree.ElementTree as ET
import GameLines


bookmaker_url = "http://lines.bookmaker.eu/"
user_agent = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
# TODO: Find a way to account for time changes. Daylight Savings sucks


def get_bookmaker_odds(league_id):
    odds_avail = []
    bookmaker_response = requests.get(bookmaker_url, headers=user_agent).content
    root = ET.fromstring(bookmaker_response)
    for child in root.findall("./Leagues/league"):
        if child.attrib['IdLeague'] == str(league_id):
            league_elem = child
            break

    for child in league_elem.findall("./game"):
        try:
            odd_xml = child.findall("./line")[0]
            # Adding 7 hours to the game time because the time is in UTC-7 and we are standardizing on UTC
            game_time = datetime.datetime.strptime(child.attrib["gmdt"]+" "+child.attrib["gmtm"], "%Y%m%d %H:%M:%S") + datetime.timedelta(hours=7)
            line_time = datetime.datetime.now()
            game = GameLines.FullGameLine(game_time, line_time, "Bookmaker", odd_xml.attrib['unt'], odd_xml.attrib['unoddst'], odd_xml.attrib['ovoddst'], child.attrib['htm'], odd_xml.attrib['hoddst'], odd_xml.attrib['hsprdt'], odd_xml.attrib['hsprdoddst'], child.attrib['vtm'], odd_xml.attrib['voddst'], odd_xml.attrib['vsprdt'], odd_xml.attrib['vsprdoddst'])
            odds_avail.append(game)
        except Exception as e:
            print(str(e))
            continue
    return odds_avail

# 4 is ncaab game lines
# get_bookmaker_odds(205) #205 is ncaab first half lines


def get_ncaab_full_game_lines():
    return get_bookmaker_odds(4)


'''
lines = get_ncaab_full_game_lines()
for line in lines:
    print(line.output())
'''



