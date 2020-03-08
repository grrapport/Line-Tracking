import Bookmaker
import Bovada
import GameLines
import Dimes
import NcaabSqlHandler
import datetime
import time
import smtplib


def update_lines_db(lines, sql_conn):
    for line in lines:
        get_ids_for_line(line)
        if line.game_id is None or line.book_id is None:
            continue
        match = sql_conn.select_latest_ncaab_line_id(line.game_id, line.book_id)
        if match is None:
            if not (line.total is None and line.team1_moneyline is None and line.team1_spread is None):
                sql_conn.insert_latest_ncaab_full_game_line(line)
            continue
        if line == match:
            continue
        if line != match:
            # checking to make sure the new line is not Null before marking all the other lines old
            if not (line.total is None and line.team1_moneyline is None and line.team1_spread is None):
                print("Line changed! Will update entries in db and insert new one")
                print("new line: " + line.output())
                print("match in db: " + match.output())
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


def get_team_id(name):
    ret_id = None
    if name in team_mappings:
        ret_id = team_mappings[name]
        return ret_id
    else:
        if name not in missing_names:
            print("missing name " + name + " in mapping table")
            send_email("missing name " + name + " in mapping table")
            missing_names.append(name)
        ret_id = None
    return ret_id


def get_bookmaker_id(book):
    book_id = bookmaker_ids[book]
    return book_id


def get_set_game_id(game):
    if game.team1_id is None or game.team2_id is None or game.book_id is None:
        return
    game_id = conn.select_game_ids(game.team1_id, game.team2_id, game.game_time.date())
    if game_id is None:
        conn.create_new_game_id(game.team1_id, game.team2_id, game.game_time.date())
        game_id = conn.select_game_ids(game.team1_id, game.team2_id, game.game_time.date())
    game.game_id = game_id.ID
    if game_id.team1_ID == game.team2_id and game_id.team2_ID == game.team1_id:
        game.switch_team1_and_team2()


def get_ids_for_line(line):
    line.book_id = get_bookmaker_id(line.book)
    line.team1_id = get_team_id(line.team1)
    line.team2_id = get_team_id(line.team2)
    if line.team1_id is not None and line.team2_id is not None and line.book_id is not None:
        get_set_game_id(line)


print("Starting NCAAB Line Getter Service")
conn = NcaabSqlHandler.SqlHandler()
team_mappings = conn.get_all_names_id_mappings()
missing_names = []
bookmaker_ids = conn.get_all_bookmaker_ids_()

# declaring variables for consecutive failures and error messages for each sportsbook
bovada_consecutive_fail = 0
bovada_exception_string = ""

bookmaker_consecutive_fail = 0
bookmaker_exception_string = ""
bookmaker_counter = 0

dimes_consecutive_fail = 0
dimes_exception_string = ""

try:
    while True:
        try:
            current_bovada_lines = Bovada.get_bovada_ncaab_odds()
            update_lines_db(current_bovada_lines, conn)
            bovada_consecutive_fail = 0
            bovada_exception_string = ""
        except Exception as e:
            bovada_consecutive_fail += 1
            print(str(e))
            bovada_exception_string += "\n\n"+str(e)
            if bovada_consecutive_fail > 25:
                bovada_exception_string = "More than 25 consecutive failures have occured for Bovada. Exception text below \n\n "+bovada_exception_string
                send_email(bovada_exception_string)
                bovada_consecutive_fail = 0
                bovada_exception_string = ""

        try:
            bookmaker_counter += 1
            if bookmaker_counter % 4 == 0:
                bookmaker_counter = 1
                current_bookmaker_lines = Bookmaker.get_ncaab_full_game_lines()
                update_lines_db(current_bookmaker_lines, conn)
                bookmaker_consecutive_fail = 0
                bookmaker_exception_string = ""
        except Exception as e:
            bookmaker_consecutive_fail += 1
            print(str(e))
            bookmaker_exception_string += "\n\n"+str(e)
            if bookmaker_consecutive_fail > 25:
                bookmaker_exception_string = "More than 25 consecutive failures have occured for Bookmaker. Exception text below \n\n "+bovada_exception_string
                send_email(bookmaker_exception_string)
                bookmaker_consecutive_fail = 0
                bookmaker_exception_string = ""

        try:
            current_dimes_lines = Dimes.get_ncaab_full_game_lines()
            update_lines_db(current_dimes_lines, conn)
            dimes_consecutive_fail = 0
            dimes_exception_string = ""
        except Exception as e:
            dimes_consecutive_fail += 1
            print(str(e))
            dimes_exception_string += "\n\n"+str(e)
            if dimes_consecutive_fail > 5:
                dimes_exception_string = "More than 25 consecutive failures have occured for 5Dimes. Exception text below \n\n "+dimes_exception_string
                send_email(dimes_exception_string)
                dimes_consecutive_fail = 0
                dimes_exception_string = ""

        time.sleep(10)
except Exception as e:
    print(str(e))
    email_text = "Line Getter Service has stopped.\n"
    email_text += "Time: "+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    email_text += "Exception: \n\n"
    email_text += str(e)
    send_email(email_text)
    conn.close()


