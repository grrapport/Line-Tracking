import datetime


class FullGameLine:
    def __init__(self, gtime, ltime, bookmaker, tot, underline, overline, t1, t1ml, t1spr, t1sprl, t2, t2ml, t2spr, t2sprl):
        try:
            self.game_time = gtime
            self.line_time = ltime
            self.book = bookmaker
            self.team1 = t1
            self.team2 = t2
            try:
                self.total = float(tot)
                self.under_line = int(underline)
                self.over_line = int(overline)
            except Exception as e:
                print("Total not available for game")
                self.total = None
                self.under_line = None
                self.over_line = None
            try:
                self.team1_moneyline = int(t1ml)
                self.team2_moneyline = int(t2ml)
            except Exception as e:
                print("Moneylines not available for game")
                self.team1_moneyline = None
                self.team2_moneyline = None
            try:
                self.team1_spread = float(t1spr)
                self.team1_spread_line = int(t1sprl)
                self.team2_spread = float(t2spr)
                self.team2_spread_line = int(t2sprl)
            except:
                print("Point spreads not available for game")
                self.team1_spread = None
                self.team1_spread_line = None
                self.team2_spread = None
                self.team2_spread_line = None
        except Exception as e:
            print("Error Message: " + str(e))

