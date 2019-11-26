import Bookmaker
import Bovada
import GameLines
import NcaabSqlHandler
import datetime
import time


def update_lines_db(lines, sql_conn):
    old_lines = sql_conn.select_all_available_ncaab_full_game_lines_by_bookmaker(lines[0].book)
    match = None
    for line in lines:
        for old in old_lines:
            if line.is_same_game(old):
                match = old
                break
        if match is None:
            sql_conn.insert_latest_ncaab_full_game_line(line)
            continue
        if line == match:
            continue
        if line != match:
            sql_conn.update_games_to_old_line(line.game_time, line.book, line.team1, line.team2)
            sql_conn.insert_latest_ncaab_full_game_line(line)
            continue


conn = NcaabSqlHandler.SqlHandler()
while True:
    current_bovada_lines = Bovada.get_bovada_ncaab_odds()
    update_lines_db(current_bovada_lines, conn)
    current_bookmaker_lines = Bookmaker.get_ncaab_full_game_lines()
    update_lines_db(current_bookmaker_lines, conn)
    time.sleep(5)

conn.close()


