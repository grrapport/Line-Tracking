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
    # opens a session with the site, and then gets the correct links to all the sports by id
    session = requests.session()
    first_page_response = str(session.get(first_url, headers=user_agent).content, 'utf-8')
    first_page_response = first_page_response.replace("\\n", "").replace("\\r", "").replace("\\t", "").replace("\'", "").replace(
        "\\", "")
    id_by_sport = dict()
    init_soup = bs4.BeautifulSoup(first_page_response, features="html5lib")
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
    # bs4 row is passed, date and teams are returned if they can be parsed out. Otherwise, None is returned
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
    team2 = teams[0].strip()
    team1 = teams[1].strip()
    try:
        # adding 5 hours because it defaults to eastern time, we are putting in UTC
        # changing to 4 because of time change
        date_time = datetime.datetime.strptime(date_string, "%A, %B %d, %Y %I:%M %p") + datetime.timedelta(hours=4)
    except:
        return None
    return team1, team2, date_time


def get_game_lines_by_league(session, league_id):
    # takes a valid session obj for web requests and the id of the league to parse
    # returns list of GameLine objects with relevant information
    league_id = 'strID='+league_id
    dimes_response = str(session.post(odds_url, headers=user_agent, cookies=session.cookies, data=league_id).content, 'utf-8')
    dimes_response = unquote(dimes_response)
    dimes_response = dimes_response.replace("\\n", "\n").replace("\\r", "").replace("\\t", "  ").replace("\'", "").replace(
        "\\", "").replace("\xa0", " ").replace("&nbsp;", " ")
    # print(dimes_response)
    soup = bs4.BeautifulSoup(dimes_response, features="html5lib")
    all_tr = soup.findAll("tr", {"class": "LHR"})
    lines = []
    for tr in all_tr:
        temp_teams_date = get_teams_and_date(tr)
        # we only want lines up to a certain future time. Not sure what to make this yet
        if temp_teams_date is not None:
            if datetime.datetime.now() - datetime.timedelta(minutes=15) > temp_teams_date[2]:
                # if it's more than 15 minutes after game time, we don't want lines anymore
                # we were getting a lot of second half lines, which they post with the same format.
                # if we want second halves, we can add them by basically doing the opposite of this  later
                continue
            if temp_teams_date[2] > datetime.datetime.now() + datetime.timedelta(hours=48):
                break
            temp_gt = temp_teams_date[2]
            temp_t1 = temp_teams_date[0]
            temp_t2 = temp_teams_date[1]
            temp_tot = None
            underline = None
            overline = None
            temp_t1_ml = None
            temp_t1_spr = None
            temp_t1_spr_line = None
            temp_t2_ml = None
            temp_t2_spr = None
            temp_t2_spr_line = None

            next_row = tr

            # If a row contains either team name, is hidden  (there are a bunch hidden)
            # or the class is LHR (which is used for titles and also blank lines, we keep going
            while next_row is not None and (temp_t1 in str(next_row) or temp_t2 in str(next_row) or "hidden" in str(next_row) or next_row["class"][0] == "LHR"):
                if next_row is None:
                    break
                if "hidden" in str(next_row) or next_row["class"][0] == "LHR": # add something to check for odds classes, just in case
                    next_row = next_row.find_next("tr")
                    continue
                row_parts = next_row.findAll("td")
                # row_parts = next_row.findChildren(recursive=False)
                #print(row_parts)
                if len(row_parts) < 4:
                    continue

                # next code block gets the spread from this row
                spread_div = row_parts[1]
                # checking to see if any rows don't have a spread at all by checking to see if the price is listed
                if len(spread_div.find_next("span", {"class": "US"}).contents) > 0:
                    spread_str = spread_div.contents[0].replace("½", ".5")
                    spread_juice = int(spread_div.find_next("span", {"class": "US"}).contents[0])
                    # 5Dimes does not juice their CBB spreads or totals, but they offer a ton of alt lines
                    # We only want the actual market lines at -110, so we only use them if they are -110
                    if spread_juice == -110:
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

                # next code block gets the moneyline from this row
                moneyline_div = row_parts[2]
                if len(moneyline_div.find_next("span", {"class": "US"}).contents) > 0:
                    ml = int(moneyline_div.find_next("span", {"class": "US"}).contents[0])
                    if temp_t1 in str(row_parts[0]):
                        temp_t1_ml = ml
                    if temp_t2 in str(row_parts[0]):
                        temp_t2_ml = ml

                # next code block gets the total and total juice
                total_div = row_parts[3]
                # checking to see if any rows don't have a total at all by checking to see if the price is listed
                if len(total_div.find_next("span", {"class": "US"}).contents) > 0:
                    total_str = total_div.contents[0].replace("½", ".5")
                    total_juice = int(total_div.find_next("span", {"class": "US"}).contents[0])
                    # 5Dimes does not juice their CBB spreads or totals, but they offer a ton of alt lines
                    # We only want the actual market lines at -110, so we only use them if they are -110
                    if total_juice == -110:
                        if "Under" in total_str:
                            try:
                                total = float(total_str.split(" ")[1])
                            except:
                                total = None
                            if temp_tot is None:
                                temp_tot = total
                            if temp_tot is not None:
                                underline = total_juice
                        if "Over" in total_str:
                            try:
                                total = float(total_str.split(" ")[1])
                            except:
                                total = None
                            if temp_tot is None:
                                temp_tot = total
                            if temp_tot is not None:
                                overline = total_juice

                next_row = next_row.find_next("tr")
            if temp_tot is not None and temp_tot < 90:
                # another thing to stop half lines from getting in the mix
                continue
            current_line = GameLines.FullGameLine(temp_gt, datetime.datetime.now(), "5Dimes", temp_tot, underline,
                                                  overline, temp_t1, temp_t1_ml,
                                                  temp_t1_spr, temp_t1_spr_line, temp_t2, temp_t2_ml,
                                                  temp_t2_spr, temp_t2_spr_line)
            lines.append(current_line)
    return lines


def get_ncaab_full_game_lines():
    # gets lines for college basketball and extra games
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
    browse.close()
    return full_game_lines


'''
lines = get_ncaab_full_game_lines()
for line in lines:
    print(line.output())
'''

