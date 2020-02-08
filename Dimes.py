import requests
import bs4
import datetime
import GameLines

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
data = 'strID=l_39'


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
        print(dictionary_name, curr_id)
        id_by_sport[dictionary_name] = curr_id

    return session, id_by_sport


def get_teams_and_date(tr):
    row = tr.findChildren(recursive=False)[0].contents
    # getting the first element out of the contents, which is just the text
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


def get_dict_sports_id(soup):
    return None


def get_odds_from_row(tr):
    # print(type(tr))
    return None


def get_game_lines_by_league(league_id):
    dimes_response = str(session.post(odds_url, headers=user_agent, cookies=session.cookies, data=league_id).content, 'utf-8')
    dimes_response = dimes_response.replace("\\n", "").replace("\\r", "").replace("\\t", "").replace("\'", "").replace(
        "\\", "")
    # TODO: Replace 1/2 symbols with .5
    soup = bs4.BeautifulSoup(dimes_response, features="html.parser")
    all_tr = soup.findAll("tr")
    lines = []
    current_line = None
    for tr in all_tr:
        temp_teams_date = get_teams_and_date(tr)
        if temp_teams_date is not None:
            if current_line is not None:
                lines.append(current_line)
                current_line = None
            if temp_teams_date[2] > datetime.datetime.now() + datetime.timedelta(hours=36):
                break
            current_line = GameLines.FullGameLine(temp_teams_date[2], datetime.datetime.now(), "5Dimes", None, None,
                                                  None, temp_teams_date[0], None,
                                                  None, None, temp_teams_date[1], None, None, None)
        else:
            if get_odds_from_row(tr) is None:
                continue

        # TODO: Loop over odds rows like below and add to the GameLines objects
    return lines


initialize()
odds = get_game_lines_by_league(data)
print(odds)
for line in odds:
    print(line.output())
