import datetime
import GameLines
import NcaabSqlHandler
import time


def get_all_lines_older_than_7_days(sql):
    week_ago = datetime.datetime.now() + datetime.timedelta(days=7)
    print(week_ago.strftime('%Y-%m-%d %H:%M:%S'))
    return sql.select_old_available_ncaab_full_game_lines(week_ago)


sql_conn = NcaabSqlHandler.SqlHandler()
old_lines = get_all_lines_older_than_7_days(sql_conn)
time.sleep(10)
for line in old_lines:
    try:
        sql_conn.insert_archive_ncaab_full_game_line(line)
        print("successfully inserted ")
        print(line.output())
    except Exception as e:
        print(str(e))
        time.sleep(10)


