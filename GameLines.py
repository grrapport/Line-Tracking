import datetime


class FullGameLine:
    def __init__(self, gtime, ltime, bookmaker, tot, underline, overline, t1, t1ml, t1spr, t1sprl, t2, t2ml, t2spr, t2sprl):
        try:
            self.game_time = gtime
            self.line_time = ltime
            self.book = bookmaker.strip()
            self.team1 = t1.strip()
            self.team2 = t2.strip()
            try:
                self.total = float(tot)
                self.under_line = int(underline)
                self.over_line = int(overline)
            except Exception as e:
                print("Total not available for game")
                print(str(e))
                self.total = None
                self.under_line = None
                self.over_line = None
            try:
                self.team1_moneyline = int(t1ml)
                self.team2_moneyline = int(t2ml)
            except Exception as e:
                print("Moneylines not available for game")
                print(str(e))
                self.team1_moneyline = None
                self.team2_moneyline = None
            try:
                self.team1_spread = float(t1spr)
                self.team1_spread_line = int(t1sprl)
                self.team2_spread = float(t2spr)
                self.team2_spread_line = int(t2sprl)
            except Exception as e:
                print("Point spreads not available for game")
                print(str(e))
                self.team1_spread = None
                self.team1_spread_line = None
                self.team2_spread = None
                self.team2_spread_line = None
        except Exception as e:
            print("Error Message: " + str(e))

    def __eq__(self, other):
        gt_bool = self.game_time == other.game_time
        team1_bool = self.team1 == other.team1 or self.team1 == other.team2
        team2_bool = self.team2 == other.team1 or self.team2 == other.team2
        tot_bool = self.total == other.total
        tot_line_bool = self.under_line == other.under_line and self.over_line == other.over_line
        if self.team1 == other.team1:
            t1spread_bool = self.team1_spread == other.team1_spread and self.team1_spread_line == other.team1_spread_line
            t2spread_bool = self.team2_spread == other.team2_spread and self.team2_spread_line == other.team2_spread_line
            moneyline_bool = self.team1_moneyline == other.team1_moneyline and self.team2_moneyline == other.team2_moneyline
        else:
            t1spread_bool = self.team1_spread == other.team2_spread and self.team1_spread_line == other.team2_spread_line
            t2spread_bool = self.team2_spread == other.team1_spread and self.team2_spread_line == other.team1_spread_line
            moneyline_bool = self.team1_moneyline == other.team2_moneyline and self.team2_moneyline == other.team1_moneyline
        return gt_bool and team1_bool and team2_bool and tot_bool and tot_line_bool and t1spread_bool and t2spread_bool and moneyline_bool

    def is_same_game(self, other):
        gt_bool = self.game_time == other.game_time
        team1_bool = self.team1 == other.team1 or self.team1 == other.team2
        team2_bool = self.team2 == other.team1 or self.team2 == other.team2
        return gt_bool and team2_bool and team1_bool



