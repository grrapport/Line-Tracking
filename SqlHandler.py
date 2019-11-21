import datetime
import mysql.connector


#engine = db.create_engine('mysql+mysqldb://line-getter:VeMlIO&zj94cqGyXBoKcu@34.69.249.19')
class SqlHandler:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="34.69.249.19",
            user="line-getter",
            passwd="",
            database="bettinglines"
        )
        self.cursor = mydb.cursor()
        self.insert_ncaab_full_game_line = ("INSERT INTO NCAAB_Full_Game_Lines "
                                            "(GameTime, LineTime, Bookmaker, Team1, Team2, Total, OverLine, UnderLine,"
                                            " T1Moneyline, T1Spread, T1SpreadLine, T2Moneyline, T2Spread, T2SpreadLine,"
                                            " Newest) "
                                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
                                            )


    def close(self):
        self.cursor.close()
        self.mydb.close()




cursor = mydb.cursor()

add_line = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")


