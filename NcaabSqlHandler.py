import datetime
import mysql.connector
import GameLines


class SqlHandler:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="34.69.249.19",
            user="line-getter",
            passwd="",
            database="bettinglines"
        )
        self.cursor = self.mydb.cursor()

    def insert_latest_ncaab_full_game_line(self, line):
        insert_ncaab_full_game_query = ("INSERT INTO NCAAB_Full_Game_Lines "
                                        "(GameTime, LineTime, Bookmaker, Team1, Team2, Total, OverLine, UnderLine,"
                                        " T1Moneyline, T1Spread, T1SpreadLine, T2Moneyline, T2Spread, T2SpreadLine,"
                                        " Newest) "
                                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
                                        )
        data = (
            line.game_time,
            line.line_time,
            line.book,
            line.team1,
            line.team2,
            line.total,
            line.over_line,
            line.under_line,
            line.team1_moneyline,
            line.team1_spread,
            line.team1_spread_line,
            line.team2_moneyline,
            line.team2_spread,
            line.team2_spread_line,
            True
        )
        self.cursor.execute(insert_ncaab_full_game_query, data)
        self.mydb.commit()

    def select_latest_ncaa_line(self, gametime, bookmaker, team1, team2):
        ret = []
        select_latest_full_game_ncaab_query = ("SELECT TOP 1 * FROM NCAAB_Full_Game_Lines WHERE "
                                               "(Team1 = %s or Team2 = %s) AND "
                                               "(Team1 = %s or Team2 = %s) AND "
                                               "GameTime = %s AND"
                                               "Bookmaker = %s AND"
                                               "Newest = 1"
                                               )
        self.cursor.execute(select_latest_full_game_ncaab_query, (team1, team1, team2, team2, gametime, bookmaker))
        result = self.cursor.fetchall()
        for row in result:
            temp = GameLines.FullGameLine(temp[0], temp[1], temp[2], temp[5], temp[6], temp[7], temp[3], temp[8],
                                          temp[9], temp[10], temp[4], temp[11], temp[12], temp[13])
            ret.append(temp)
        return ret

    def select_all_available_ncaab_full_game_lines(self):
        now = datetime.datetime.now()
        ret = []
        select_all_full_game_ncaab_query = "SELECT * FROM NCAAB_Full_Game_Lines WHERE GameTime > %s"
        self.cursor.execute(select_all_full_game_ncaab_query, now)
        result = self.cursor.fetchall()
        for row in result:
            temp = GameLines.FullGameLine(temp[0], temp[1], temp[2], temp[5], temp[6], temp[7], temp[3], temp[8],
                                          temp[9], temp[10], temp[4], temp[11], temp[12], temp[13])
            ret.append(temp)
        return ret

    def close(self):
        self.cursor.close()
        self.mydb.close()







