import requests
import datetime
import xml.etree.ElementTree as ET
import Game_Lines
import jsonpickle
import json



user_agent = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

def convert_json_feed_to_line_object(dict):
    teams_obj = dict["competitors"]
    team_1 = teams_obj[0]["name"]
    team_2 = teams_obj[1]["name"]
    game_time = datetime.datetime.fromtimestamp(int(dict["startTime"])/1000)
    odd_time = datetime.datetime.now()
    bookmaker = "Bovada"
    odds_obj = dict["displayGroups"]
    print(game_time.strftime('%Y-%m-%d %H:%M:%S'))
    print(team_1)
    print(team_2)
    print(odds_obj)


def get_bovada_ncaab_odds():
    bovada_ncaab_url = "https://services.bovada.lv/services/sports/event/coupon/events/A/description/basketball/college-basketball?marketFilterId=def&preMatchOnly=true&lang=en"
    bovada_response = requests.get(bovada_ncaab_url, headers=user_agent).content
    test_dict = json.loads(bovada_response)
    #print(test_dict[0]["events"])
    for thing in test_dict[0]["events"]:
        convert_json_feed_to_line_object(thing)
        print("\n\n")
    


get_bovada_ncaab_odds()
