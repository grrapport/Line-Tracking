import requests
import bs4
import datetime
import GameLines
from urllib.parse import unquote


user_agent = {
    'User-Agent': 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'authority': 'www.5dimes.eu',
    'origin': 'https://www.5dimes.eu',
    'content-type': 'text/plain;charset=UTF-8',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'referer': 'https://www.5dimes.eu/livelines/livelines.aspx',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9'
    }

first_url = "https://www.5dimes.eu/livelines/livelines.aspx"
odds_url = "https://www.5dimes.eu/livelines/ajax/Player.LiveLines,LiveLines.ashx?_method=GetLinesForSport&_session=no"


def initialize():
    session = requests.session()
    first_page_response = str(session.get(first_url, headers=user_agent).content, 'utf-8')
    first_page_response = first_page_response.replace("\\n", "").replace("\\r", "").replace("\\t", "").replace("\'", "").replace(
        "\\", "")
    id_by_sport = dict()
    init_soup = bs4.BeautifulSoup(first_page_response, features="html.parser")
    sports = init_soup.findAll("span", {"class": "Group SportSubType"})
    for sport in sports:
        # to get the overarching sport, we need to look above at the most recent div with class "Sport"
        sport_cat = sport.find_previous("div", {"class": "Sport"}).contents[0].strip()
        curr_id = sport.find("input").get("id").replace("/", "").strip()
        name = sport.find("a").contents[0].strip()
        dictionary_name = sport_cat+"-"+name
        id_by_sport[dictionary_name] = curr_id

    return session, id_by_sport


def get_teams_and_date(tr):
    row = tr.findChildren(recursive=False)[0].contents
    # getting the first element out of the contents, which is just the text
    if len(row) == 0:
        return None
    row = row[0]
    teams_date = row.split("-")
    if len(teams_date) < 2:
        return None
    date_string = teams_date[-1].strip()
    teams = teams_date[0].split(" at ")
    if len(teams) < 2:
        return None
    team1 = teams[0].strip()
    team2 = teams[1].strip()
    try:
        date_time = datetime.datetime.strptime(date_string, "%A, %B %d, %Y %I:%M %p")
    except:
        return None
    return team1, team2, date_time


def get_odds_from_row(tr):
    # print(type(tr))
    return None


def get_game_lines_by_league(session, league_id):
    league_id = 'strID='+league_id
    dimes_response = str(session.post(odds_url, headers=user_agent, cookies=session.cookies, data=league_id).content, 'utf-8')
    dimes_response = unquote(dimes_response)
    dimes_response = dimes_response.replace("\\n", "").replace("\\r", "").replace("\\t", "").replace("\'", "").replace(
        "\\", "").replace("\xa0", " ")
    soup = bs4.BeautifulSoup(dimes_response, features="html.parser")
    all_tr = soup.findAll("tr", {"class": "LHR"})
    lines = []
    for tr in all_tr:
        temp_teams_date = get_teams_and_date(tr)
        # we only want lines up to a certain future time. Not sure what to make this yet
        if temp_teams_date is not None:
            if temp_teams_date[2] > datetime.datetime.now() + datetime.timedelta(hours=36):
                break
            temp_gt = temp_teams_date[2]
            temp_t1 = temp_teams_date[0]
            temp_t2 = temp_teams_date[1]
            temp_tot = None
            underline = None
            overline = ""
            temp_t1_ml = None
            temp_t1_spr = None
            temp_t1_spr_line = None
            temp_t2_ml = None
            temp_t2_spr = None
            temp_t2_spr_line = None

            next_row = tr.find_next("tr")

            # If a row contains either team name, is hidden  (there are a bunch hidden)
            # or the class is LHR (which is used for titles and also blank lines, we keep going
            while temp_t1 in str(next_row) or temp_t2 in str(next_row) or "hidden" in str(next_row) or next_row["class"][0] == "LHR":
                if ("hidden" in str(next_row) or next_row["class"][0] == "LHR") and True: # add something to check for odds classes, just in case
                    next_row = next_row.find_next("tr")
                    continue
                row_parts = next_row.findAll("td")

                # next code block gets the spread from this row
                spread_div = row_parts[1]
                # checking to see if any rows don't have a spread at all by checking to see if the price is listed
                # TODO: check of alternate lines by looking for prices that are not -110
                if len(spread_div.find_next("span", {"class": "US"}).contents) > 0:
                    spread_str = spread_div.contents[0].replace("½", ".5")
                    print(spread_str)
                    print(spread_div.find_next("span", {"class": "US"}).contents)
                    spread_juice = int(spread_div.find_next("span", {"class": "US"}).contents[0])
                    if spread_str is None or spread_str == " ":
                        spread = None
                    else:
                        if "pk" in spread_str:
                            spread = 0.0
                        else:
                            spread = float(spread_str)
                    if temp_t1 in str(row_parts[0]):
                        temp_t1_spr = spread
                        temp_t1_spr_line = spread_juice
                    if temp_t2 in str(row_parts[0]):
                        temp_t2_spr = spread
                        temp_t2_spr_line = spread_juice

                next_row = next_row.find_next("tr")
            print("\n\n\tthis row broke the loop for "+temp_t1+" and "+temp_t2)
            print(str(next_row)+"\n\n")
            current_line = GameLines.FullGameLine(temp_gt, datetime.datetime.now(), "5Dimes", None, None,
                                                  None, temp_t1, None,
                                                  temp_t1_spr, temp_t1_spr_line, temp_t2, None,
                                                  temp_t2_spr, temp_t2_spr_line)
            lines.append(current_line)
    return lines


def get_ncaab_full_game_lines():
    full_game_lines = []
    init_vals = initialize()
    browse = init_vals[0]
    sport_dict = init_vals[1]
    if "Basketball-College" in sport_dict:
        game_line = get_game_lines_by_league(browse, sport_dict["Basketball-College"])
        full_game_lines.extend(game_line)
    if "Basketball-College Extra" in sport_dict:
        game_line = get_game_lines_by_league(browse, sport_dict["Basketball-College Extra"])
        full_game_lines.extend(game_line)
    return full_game_lines


odds = get_ncaab_full_game_lines()
for line in odds:
    print(line.output())

