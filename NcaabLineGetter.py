import Bookmaker
import Bovada
import GameLines
import NcaabSqlHandler
import datetime
import time
import smtplib
import traceback


def update_lines_db(lines, sql_conn):
    old_lines = sql_conn.select_all_available_ncaab_full_game_lines_by_bookmaker(lines[0].book)
    match = None
    for line in lines:
        for old in old_lines:
            if line.is_same_game(old):
                match = old
                break
        if match is None:
            print("*********************************************************")
            print("No match found, will insert new line")
            sql_conn.insert_latest_ncaab_full_game_line(line)
            print("*********************************************************")
            print("*********************************************************")
            print("\n\n\n\n\n")
            continue
        if line == match:
            continue
        if line != match:
            print("Line changed! Will update entries in db and insert new one")
            print("new line: " + line.output())
            print("match in db: " + match.output())
            sql_conn.update_games_to_old_line(line.game_time, line.book, line.team1, line.team2)
            sql_conn.insert_latest_ncaab_full_game_line(line)
            continue


def send_email(email_text):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("actionchase@gmail.com", "lnkyaliduvshwicn")
    try:
        server.sendmail("actionchase@gmail.com", "grrapport@gmail.com", email_text)
    except Exception as e:
        print(e)


conn = NcaabSqlHandler.SqlHandler()

bovada_consecutive_fail = 0
bovada_exception_string = ""

bookmaker_consecutive_fail = 0
bookmaker_exception_string = ""
try:
    while True:
        try:
            current_bovada_lines = Bovada.get_bovada_ncaab_odds()
            update_lines_db(current_bovada_lines, conn)
            bovada_consecutive_fail = 0
            bovada_exception_string = ""
        except Exception as e:
            bovada_consecutive_fail += 1
            bovada_exception_string += "\n\n"+traceback.print_exc()
            if bovada_consecutive_fail > 15:
                bovada_exception_string = "More than 15 consecutive failures have occured for Bovada. Exception text below \n\n "+bovada_exception_string
                send_email(bovada_exception_string)

        try:
            current_bookmaker_lines = Bookmaker.get_ncaab_full_game_lines()
            update_lines_db(current_bookmaker_lines, conn)
            bookmaker_consecutive_fail = 0
            bookmaker_exception_string = ""
        except Exception as e:
            bookmaker_consecutive_fail += 1
            bookmaker_exception_string += "\n\n"+traceback.print_exc()
            if bookmaker_consecutive_fail > 15:
                bookmaker_exception_string = "More than 15 consecutive failures have occured for Bovada. Exception text below \n\n "+bovada_exception_string
                send_email(bookmaker_exception_string)
        time.sleep(10)
except Exception:
    traceback.print_exc()
    conn.close()


