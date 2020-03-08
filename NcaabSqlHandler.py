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
                                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                        )
        if line.total is None and line.team1_moneyline is None and line.team1_spread is None:
            return
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
        print(data)
        self.cursor.execute(insert_ncaab_full_game_query, data)
        self.mydb.commit()

    def insert_ncaab_full_game_line_id(self, line):
        insert_ncaab_full_game_query = ("INSERT INTO NCAAB_Full_Game_Lines_IDs "
                                        "(GameID, BookID, LineTime,"
                                        " Total, OverLine, UnderLine,"
                                        " T1Moneyline, T1Spread, T1SpreadLine, T2Moneyline, T2Spread, T2SpreadLine,"
                                        " Newest) "
                                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                        )
        if line.total is None and line.team1_moneyline is None and line.team1_spread is None:
            return
        data = (
            line.game_id,
            line.book_id,
            line.line_time,
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
        print(data)
        self.cursor.execute(insert_ncaab_full_game_query, data)
        self.mydb.commit()

    def select_latest_ncaab_line(self, gametime, bookmaker, team1, team2):
        new_line = None
        select_latest_full_game_ncaab_query = ("SELECT * FROM NCAAB_Full_Game_Lines WHERE "
                                               "(Team1 = %s or Team2 = %s) AND "
                                               "(Team1 = %s or Team2 = %s) AND "
                                               "GameTime = %s AND "
                                               "Bookmaker = %s AND "
                                               "Newest = 1 "
                                               "Limit 1"
                                               )
        self.cursor.execute(select_latest_full_game_ncaab_query, (team1, team1, team2, team2,
                                                                  gametime.strftime('%Y-%m-%d %H:%M:%S'), bookmaker))
        result = self.cursor.fetchall()
        for temp in result:
            new_line = GameLines.FullGameLine(temp[0], temp[1], temp[2], temp[5], temp[7], temp[6], temp[3], temp[8],
                                              temp[9], temp[10], temp[4], temp[11], temp[12], temp[13])
            break
        return new_line

    def select_latest_ncaab_line_id(self, gameid, bookid):
        new_line = None
        select_latest_full_game_ncaab_query = ("SELECT * FROM NCAAB_Full_Game_Lines_IDs WHERE "
                                               "GameID = %s AND "
                                               "BookID = %s"
                                               "order by LineTime desc "
                                               "Limit 1"
                                               )
        self.cursor.execute(select_latest_full_game_ncaab_query, (gameid, bookid))
        result = self.cursor.fetchall()
        for temp in result:
            new_line = GameLines.FullGameLine(None, temp[2], None, temp[3], temp[5], temp[4],
                                              None, temp[6], temp[7], temp[8], None, temp[9], temp[10], temp[11])
            new_line.game_id = temp[0]
            new_line.book_id = temp[1]
            new_line.latest = True
            break
        return new_line

    def select_all_available_ncaab_full_game_lines(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ret = []
        select_all_full_game_ncaab_query = "SELECT * FROM NCAAB_Full_Game_Lines WHERE GameTime > %s"
        self.cursor.execute(select_all_full_game_ncaab_query, (now, ))
        result = self.cursor.fetchall()
        for temp in result:
            new_line = GameLines.FullGameLine(temp[0], temp[1], temp[2], temp[5], temp[7], temp[6], temp[3], temp[8],
                                              temp[9], temp[10], temp[4], temp[11], temp[12], temp[13])
            ret.append(new_line)
        return ret

    def select_all_available_ncaab_full_game_lines_by_bookmaker(self, bookmaker):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ret = []
        select_all_full_game_ncaab_query = "SELECT * FROM NCAAB_Full_Game_Lines WHERE GameTime > %s and Bookmaker = %s and Newest = 1"
        self.cursor.execute(select_all_full_game_ncaab_query, (now, bookmaker))
        result = self.cursor.fetchall()
        for temp in result:
            new_line = GameLines.FullGameLine(temp[0], temp[1], temp[2], temp[5], temp[7], temp[6], temp[3], temp[8],
                                              temp[9], temp[10], temp[4], temp[11], temp[12], temp[13])
            ret.append(new_line)
        return ret

    """def update_games_to_old_line(self, gametime, bookmaker, team1, team2):
        update_latest_column = ("UPDATE NCAAB_Full_Game_Lines "
                                "SET Newest = 0 "
                                "WHERE (Team1 = %s or Team2 = %s) AND "
                                "(Team1 = %s or Team2 = %s) AND "
                                "GameTime = %s AND "
                                "Bookmaker = %s"
                                )
        self.cursor.execute(update_latest_column,  (team1, team1, team2, team2,
                                                    gametime.strftime('%Y-%m-%d %H:%M:%S'), bookmaker))
    """

    def select_old_available_ncaab_full_game_lines(self, dt):
        now = dt.strftime('%Y-%m-%d %H:%M:%S')
        ret = []
        select_all_full_game_ncaab_query = "SELECT * FROM NCAAB_Full_Game_Lines WHERE GameTime < %s"
        self.cursor.execute(select_all_full_game_ncaab_query, (now, ))
        result = self.cursor.fetchall()
        for temp in result:
            new_line = GameLines.FullGameLine(temp[0], temp[1], temp[2], temp[5], temp[7], temp[6], temp[3], temp[8],
                                              temp[9], temp[10], temp[4], temp[11], temp[12], temp[13])
            ret.append(new_line)
        return ret

    def insert_archive_ncaab_full_game_line(self, line):
        insert_ncaab_full_game_query = ("INSERT INTO NCAAB_Full_Game_Lines_Archive "
                                        "(GameTime, LineTime, Bookmaker, Team1, Team2, Total, OverLine, UnderLine,"
                                        " T1Moneyline, T1Spread, T1SpreadLine, T2Moneyline, T2Spread, T2SpreadLine,"
                                        " Newest) "
                                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                        )
        if line.total is None and line.team1_moneyline is None and line.team1_spread is None:
            return
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
            False
        )
        print(data)
        self.cursor.execute(insert_ncaab_full_game_query, data)
        self.mydb.commit()

    def get_all_names_id_mappings(self):
        select_all_names_query = "select * from NCAAB_Team_ID_Mapping"
        self.cursor.execute(select_all_names_query)
        result = self.cursor.fetchall()
        ret = dict()
        for temp in result:
            ret[temp[1]] = temp[0]
        return ret

    def get_all_bookmaker_ids_(self):
        select_all_names_query = "select ID,Name from Bookmaker_IDs"
        self.cursor.execute(select_all_names_query)
        result = self.cursor.fetchall()
        ret = dict()
        for temp in result:
            ret[temp[1]] = temp[0]
        return ret

    def select_game_ids(self, team1, team2, date):
        ret = None
        select_latest_full_game_ncaab_query = ("SELECT * FROM NCAAB_Game_IDs WHERE "
                                               "(Team1 = %s or Team2 = %s) AND "
                                               "(Team1 = %s or Team2 = %s) AND "
                                               "GameDate = %s"
                                               )
        self.cursor.execute(select_latest_full_game_ncaab_query, (team1, team1, team2, team2,
                                                                  date))
        result = self.cursor.fetchall()
        for temp in result:
            try:
                ret = GameLines.GameID(int(temp[0]), int(temp[1]), int(temp[2]), temp[3])
                return ret
            except:
                continue
        return ret

    def create_new_game_id(self, team1, team2, date):
        insert_ncaab_full_game_archive_query = ("INSERT INTO NCAAB_Game_IDs "
                                                "(Team1, Team2, GameDate)"
                                                "VALUES (%s, %s, %s)"
                                                )
        self.cursor.execute(insert_ncaab_full_game_archive_query, (team1, team2, date))
        self.mydb.commit()

    def close(self):
        self.cursor.close()
        self.mydb.close()









