import Bookmaker
import Bovada
import Dimes
import GameLines
import NcaabSqlHandler
import datetime
import time
import smtplib
import traceback


def update_lines_db(lines, sql_conn):
    for line in lines:
        match = sql_conn.select_latest_ncaa_line(line.game_time, line.book, line.team1, line.team2)
        if match is None:
            print("No match found, will insert new line")
            sql_conn.insert_latest_ncaab_full_game_line(line)
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


def send_email(text):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("actionchase@gmail.com", "lnkyaliduvshwicn")
    try:
        server.sendmail("actionchase@gmail.com", "grrapport@gmail.com", text)
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
            bovada_exception_string += "\n\n"+str(e)
            if bovada_consecutive_fail > 25:
                bovada_exception_string = "More than 25 consecutive failures have occured for Bovada. Exception text below \n\n "+bovada_exception_string
                send_email(bovada_exception_string)
                bovada_consecutive_fail = 0
                bovada_exception_string = ""

        try:
            current_bookmaker_lines = Bookmaker.get_ncaab_full_game_lines()
            update_lines_db(current_bookmaker_lines, conn)
            bookmaker_consecutive_fail = 0
            bookmaker_exception_string = ""
        except Exception as e:
            bookmaker_consecutive_fail += 1
            bookmaker_exception_string += "\n\n"+str(e)
            if bookmaker_consecutive_fail > 25:
                bookmaker_exception_string = "More than 25 consecutive failures have occured for Bovada. Exception text below \n\n "+bovada_exception_string
                send_email(bookmaker_exception_string)
                bookmaker_consecutive_fail = 0
                bookmaker_exception_string = ""
        time.sleep(7)
except Exception as e:
    print(str(e))
    email_text = "Line Getter Service has stopped.\n"
    email_text += "Time: "+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    email_text += "Exception: \n\n"
    email_text += str(e)
    send_email(email_text)
    conn.close()


