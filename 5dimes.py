import requests
import bs4
import datetime
import GameLines
import json
'''
curl 'https://www.5dimes.eu/livelines/ajax/Player.LiveLines,LiveLines.ashx?_method=GetLinesForSport&_session=no' -H 'authority: www.5dimes.eu' -H 'origin: https://www.5dimes.eu' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36' -H 'content-type: text/plain;charset=UTF-8' -H 'accept: */*' -H 'sec-fetch-site: same-origin' -H 'sec-fetch-mode: cors' -H 'referer: https://www.5dimes.eu/livelines/livelines.aspx' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9' -H 'cookie: Fivedimes=2667581612.47873.0000; visid_incap_1316303=7IhGolXHTZeZ+ObrVUT6o6BhJl4AAAAAQUIPAAAAAABCO7a0JQlCGLGMBXqCQeW9; nlbi_1316303=1qN7RX9QQHtjmil5SDB6YwAAAABAlN5RykdJmwnBSsZ0Eltw; incap_ses_619_1316303=Eh2tAcgXCGgGkF8AmCKXCKFhJl4AAAAAr56tc+3DmOn92Hsr8BmbqA==; lc_sso7584861=1579573680639; __lc.visitor_id.7584861=S1579573680.24a784d35f; ASP.NET_SessionId=xlxhxg4uwq1lsfdkbpsmgfsw; cookiesEnabled=1; ioDeviceChecked=5d2546861%2Dc6b7d730%2D0ca7%2D47c8%2Db020%2D113fec23d01a; affiliatecode=; TagACons=0; TagA=0; ASPSESSIONIDSWBRQDTS=NPPAIAPCGAMEMJBCIHCCJHAG' --data-binary 'strID=l_10' --compressed
curl 'https://www.5dimes.eu/livelines/ajax/Player.LiveLines,LiveLines.ashx?_method=GetLinesForSport&_session=no' --data-binary 'strID=l_10' --compressed



'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
'''


user_agent = {'User-Agent':'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
url = "https://www.5dimes.eu/livelines/ajax/Player.LiveLines,LiveLines.ashx?_method=GetLinesForSport&_session=no"
data = 'strID=l_10'
dimes_response = str(requests.post(url, headers=user_agent, data=data).content, 'utf-8')
dimes_response = dimes_response.replace("\\n", "").replace("\\r", "").replace("\\t", "").replace("\'", "").replace("\\", "")
soup = bs4.BeautifulSoup(dimes_response, features="html.parser")
allTR = soup.findAll("tr", {"class": "LHR"})
num = 0
for tr in allTR:
    row = tr.findChildren(recursive=False)[0].contents
    teams_date = str(row).split("-")
    if len(teams_date) < 2:
        continue
    date_string = teams_date[1]
    teams = teams_date[0].split(" at ")
    team1 = teams[0].strip()
    team2 = teams[1].strip()
    date_time = datetime.datetime.strptime(date_string, 
    '''
    Saturday, February 1, 2020 3:00 PM
    '''
    print(team1, team2)
    print(date_string)

'''
for row in allTR:
    row_str = str(row)
    if 'nonalt' in row_str:
        num += 1
        print("row number "+str(num))
        print(row)
'''

'''
<tr class="\'LR" nonalt\'=""><!--<td rowspan=\'2\'>1/23/2020<br/>10:00 PM (EST)</td>--><td>665&nbsp;&nbsp;&nbsp;BYU</td><td>-6 <span class="US">-110</span><span class="\'EU\'">1.909</span></td><td><span class="US">-265</span><span class="\'EU\'">1.377</span></td><td>Over 136½ <span class="US">-110</span><span class="\'EU\'">1.909</span></td></tr>
'''




