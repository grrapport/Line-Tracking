import requests
import datetime
import GameLines
import json


user_agent = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
# TODO: Find a way to account for time changes. Daylight Savings sucks
# TODO: fix headers to really look legit. they're gonna send us to Sinkhole city soon


def convert_json_feed_to_line_object(dict):
    teams_obj = dict["competitors"]
    team_1 = teams_obj[0]["name"]
    team_2 = teams_obj[1]["name"]
    total = None
    under_line = None
    over_line = None
    team1_ml = None
    team1_spread_line = None
    team1_spread = None
    team2_ml = None
    team2_spread_line = None
    team2_spread = None
    # Adding 6 hours to the game time because the time is in UTC-6 and we are standardizing on UTC
    # changing to +5 because of time change
    game_time = datetime.datetime.fromtimestamp(int(dict["startTime"])/1000) + datetime.timedelta(hours=5)
    odd_time = datetime.datetime.now()
    bookmaker = "Bovada"
    odds_obj = dict["displayGroups"]
    for market in odds_obj[0]["markets"]:
        if market["description"] == 'Moneyline':
            for ml in market["outcomes"]:
                if ml["description"] == team_1:
                    team1_ml = ml["price"]["american"]
                if ml["description"] == team_2:
                    team2_ml = ml["price"]["american"]
        if market["description"] == 'Point Spread':
            for ml in market["outcomes"]:
                if ml["description"] == team_1:
                    team1_spread_line = ml["price"]["american"]
                    team1_spread = ml["price"]["handicap"]
                if ml["description"] == team_2:
                    team2_spread_line = ml["price"]["american"]
                    team2_spread = ml["price"]["handicap"]
        if market["description"] == "Total":
            for tot in market["outcomes"]:
                if tot["description"] == "Over":
                    total = tot["price"]["handicap"]
                    over_line = tot["price"]["american"]
                if tot["description"] == "Under":
                    under_line = tot["price"]["american"]
    new_line = GameLines.FullGameLine(game_time, odd_time, bookmaker, total, under_line, over_line, team_1, team1_ml, team1_spread, team1_spread_line, team_2, team2_ml, team2_spread, team2_spread_line)
    return new_line


def get_bovada_ncaab_odds():
    bovada_ncaab_url = "https://services.bovada.lv/services/sports/event/coupon/events/A/description/basketball/college-basketball?marketFilterId=def&preMatchOnly=true&lang=en"
    bovada_response = requests.get(bovada_ncaab_url, headers=user_agent).content
    current_lines = []
    test_dict = json.loads(bovada_response)
    for thing in test_dict[0]["events"]:
        current_lines.append(convert_json_feed_to_line_object(thing))
    return current_lines


'''
for odd in get_bovada_ncaab_odds():
    print(odd.output())
'''

