import datetime


class FullGameLine:
    def __init__(self, gtime, ltime, bookmaker, tot, underline, overline, t1, t1ml, t1spr, t1sprl, t2, t2ml, t2spr, t2sprl):
        try:
            self.game_time = gtime
            self.game_id = None
            self.line_time = ltime
            if bookmaker is not None:
                self.book = bookmaker.strip()
            else:
                self.book = ""
            self.book_id = None
            self.team1 = clean_team_name(t1)
            self.team1_id = None
            self.team2 = clean_team_name(t2)
            self.team2_id = None
            self.latest = None
            try:
                self.total = float(tot)
                self.under_line = int(underline)
                self.over_line = int(overline)
            except Exception as e:
                self.total = None
                self.under_line = None
                self.over_line = None
            try:
                self.team1_moneyline = int(t1ml)
                self.team2_moneyline = int(t2ml)
            except Exception as e:
                self.team1_moneyline = None
                self.team2_moneyline = None
            try:
                self.team1_spread = float(t1spr)
                self.team1_spread_line = int(t1sprl)
                self.team2_spread = float(t2spr)
                self.team2_spread_line = int(t2sprl)
            except Exception as e:
                self.team1_spread = None
                self.team1_spread_line = None
                self.team2_spread = None
                self.team2_spread_line = None
        except Exception as e:
            print("Error Message: " + str(e))

    def __eq__(self, other):
        game_id_bool = self.game_id == other.game_id
        tot_bool = self.total == other.total
        tot_line_bool = self.under_line == other.under_line and self.over_line == other.over_line
        if self.team1_id == other.team1_id:
            print("team1 ids are the same")
            print(self.team1_spread, other.team1_spread)
            print(self.team2_spread, other.team2_spread)
            print(self.team1_moneyline, other.team1_moneyline)
            print(self.team2_moneyline, other.team2_moneyline)
            t1spread_bool = self.team1_spread == other.team1_spread and self.team1_spread_line == other.team1_spread_line
            t2spread_bool = self.team2_spread == other.team2_spread and self.team2_spread_line == other.team2_spread_line
            moneyline_bool = self.team1_moneyline == other.team1_moneyline and self.team2_moneyline == other.team2_moneyline
        else:
            print("team1 ids are not the same")
            print(self.team1_spread, other.team1_spread)
            print(self.team2_spread, other.team2_spread)
            print(self.team1_moneyline, other.team1_moneyline)
            print(self.team2_moneyline, other.team2_moneyline)
            t1spread_bool = self.team1_spread == other.team2_spread and self.team1_spread_line == other.team2_spread_line
            t2spread_bool = self.team2_spread == other.team1_spread and self.team2_spread_line == other.team1_spread_line
            moneyline_bool = self.team1_moneyline == other.team2_moneyline and self.team2_moneyline == other.team1_moneyline
        print(game_id_bool, tot_bool, tot_line_bool, t1spread_bool, t2spread_bool, moneyline_bool)
        return game_id_bool and tot_bool and tot_line_bool and t1spread_bool and t2spread_bool and moneyline_bool

    def is_same_game(self, other):
        return self.game_id == other.game_id

    def switch_team1_and_team2(self):
        # switch the names
        temp_team1 = self.team2
        self.team2 = self.team1
        self.team1 = temp_team1
        temp_team1_id = self.team2_id
        self.team2_id = self.team1_id
        self.team1_id = temp_team1_id
        # switch moneylines
        temp_team1_ml = self.team2_moneyline
        self.team2_moneyline = self.team1_moneyline
        self.team1_moneyline = temp_team1_ml
        # switch spreads and spread juice
        temp_team1_spread = self.team2_spread
        temp_team1_spreadline = self.team2_spread_line
        self.team2_spread = self.team1_spread
        self.team2_spread_line = self.team1_spread_line
        self.team1_spread = temp_team1_spread
        self.team2_spread_line = temp_team1_spreadline

    def output(self):
        if self.game_time is None:
            gt_str = "not found"
        else:
            gt_str = self.game_time.strftime('%Y-%m-%d %H:%M:%S')
        outstring = """
                    {}
                    Team 1: {}         Team 2: {}
                    {}                 {}
                    {} {}              {} {}
                    O/U: {}
                    Over:{}             Under: {}
                    """.format(gt_str, self.team1,
                               self.team2, self.team1_moneyline, self.team2_moneyline,
                               self.team1_spread, self.team1_spread_line, self.team2_spread,
                               self.team2_spread_line, self.total, self.over_line,
                               self.under_line
                               )
        return outstring


class GameID:
    def __init__(self, game_id, team1_id, team2_id, date):
        self.ID = game_id
        self.team1_ID = team1_id
        self.team2_ID = team2_id
        self.date = date


def clean_team_name(name):
    clean = ""
    if name is None:
        return ""
    # adding a bunch of replaces to clean up these team names after seeing some problems with Bovada
    name = name.replace("\\n", "").replace("\\r", "").replace("\\t", "").replace("\'", "").replace(
                        "\xa0", "").replace("&nbsp;", " ").replace("\\", "")

    parts = name.split(" ")
    # this removes the ranking from Bovada team names. Caused us a lot of pain in the past :(
    if parts[len(parts)-1].startswith("(#"):
        parts.pop()
        clean = "".join(parts).strip()
    else:
        clean = name.strip()
    return clean


