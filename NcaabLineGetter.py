import Bookmaker
import Bovada
import GameLines
import NcaabSqlHandler
import datetime


init_conn = NcaabSqlHandler.SqlHandler()
current_lines = init_conn.select_all_available_ncaab_full_game_lines()

bovada_lines = Bovada.get_bovada_ncaab_odds()
bookmaker_lines = Bookmaker.get_bookmaker_odds()
all_lines = bookmaker_lines + bovada_lines
for line in all_lines:
    init_conn.insert_latest_ncaab_full_game_line(line)

