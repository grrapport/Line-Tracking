import requests
import bs4
import datetime
import GameLines


user_agent = {'User-Agent':'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
odds_url = "https://www.5dimes.eu/livelines/ajax/Player.LiveLines,LiveLines.ashx?_method=GetLinesForSport&_session=no"
data = 'strID=l_6'


def get_teams_and_date(tr):
    row = tr.findChildren(recursive=False)[0].contents
    # casting row to a string and then removing excess brackets and single quotes
    row = str(row).replace("[\'", "").replace("\']", "")
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
    print(type(tr))
    return None


def get_odds_by_league(league_id):
    dimes_response = str(requests.post(odds_url, headers=user_agent, data=league_id).content, 'utf-8')
    dimes_response = dimes_response.replace("\\n", "").replace("\\r", "").replace("\\t", "").replace("\'", "").replace(
        "\\", "")
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
            current_line = GameLines.FullGameLine(temp_teams_date[2], datetime.datetime.now(), "5Dimes", None, None, None, temp_teams_date[0], None,
                                                  None, None, temp_teams_date[1], None, None, None)
        else:
            print(tr)
        if get_odds_from_row(tr) is None:
            continue

        # TODO: Loop over odds rows like below and add to the GameLines objects
    return lines





'''
for row in allTR:
    row_str = str(row)
    if 'nonalt' in row_str:
        num += 1
        print("row number "+str(num))
        print(row)
        
-4½ 

'''

'''
<tr class="\'LR" nonalt\'=""><!--<td rowspan=\'2\'>1/23/2020<br/>10:00 PM (EST)</td>--><td>665&nbsp;&nbsp;&nbsp;BYU</td><td>-6 <span class="US">-110</span><span class="\'EU\'">1.909</span></td><td><span class="US">-265</span><span class="\'EU\'">1.377</span></td><td>Over 136½ <span class="US">-110</span><span class="\'EU\'">1.909</span></td></tr>
'''
odds = get_odds_by_league(data)
print(odds)
for line in odds:
    print(line.output())



