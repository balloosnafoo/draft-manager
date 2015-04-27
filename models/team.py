
class Team(object):
    def __init__(self, manager, is_user):

        self.manager = manager
        self.is_user = is_user

        self.starting_qbs = []
        self.starting_rbs = []
        self.starting_wrs = []
        self.starting_tes = []
        self.starting_flex= []
        self.starting_dst = []
        self.starting_k   = []
        self.bench        = []

    # General placement wrapper
    def place_draftee(self, player, current_pick):
        position = player.get_position()
        player.set_picked_at(current_pick)
        if position == "QB":
            return self.place_qb(player)
        elif position == "WR":
            return self.place_wr(player)
        elif position == "RB":
            return self.place_rb(player)
        elif position == "TE":
            return self.place_te(player)
        elif position == "K":
            return self.place_k( player)
        elif position == "DST":
            return self.place_dst(player)

    # Placement functions
    def place_qb(self, player):
        if len(self.starting_qbs) < 1:
            self.starting_qbs.append(player)
            return "QB"
        else:
            self.bench.append(player)
            return "BN%s" % (str(len(self.bench)))

    def place_wr(self, player):
        if len(self.starting_wrs) < 2:
            self.starting_wrs.append(player)
            return "WR" + str(len(self.starting_wrs))
        elif len(self.starting_flex) < 1:
            self.starting_flex.append(player)
            return "FLEX"
        else:
            self.bench.append(player)
            return "BN%s" % (str(len(self.bench)))
            
    def place_rb(self, player):
        if len(self.starting_rbs) < 2:
            self.starting_rbs.append(player)
            return "RB" + str(len(self.starting_rbs))
        elif len(self.starting_flex) < 1:
            self.starting_flex.append(player)
            return "FLEX"
        else:
            self.bench.append(player)
            return "BN%s" % (str(len(self.bench)))

    def place_te(self, player):
        if len(self.starting_tes) < 1:
            self.starting_tes.append(player)
            return "TE"
        elif len(self.starting_flex) < 1:
            self.starting_flex.append(player)
            return "FLEX"
        else:
            self.bench.append(player)
            return "BN%s" % (str(len(self.bench)))

    def place_k(self, player):
        if len(self.starting_k) < 1:
            self.starting_k.append(player)
            return "K"
        else:
            self.bench.append(player)
            return "BN%s" % (str(len(self.bench)))

    def place_dst(self, player):
        if len(self.starting_dst) < 1:
            self.starting_dst.append(player)
            return "D/ST"
        else:
            self.bench.append(player)
            return "BN%s" % (str(len(self.bench)))

    # Exportation
    def export_players(self):
        export = []
        players = self.get_all_players()
        for player in players:
            name     = player.get_name()
            position = player.get_position()
            age      = player.get_age()
            team     = player.get_team()
            subj_val = player.get_subjective_value()
            if position == "K":
                age = 0
            elif position == "DST":
                age = 0
                team = None
            export.append([name, position, age, team, subj_val])
        return export

    # Getters and setters
    def get_manager(self):
        return self.manager

    def get_all_players(self):
        players  = self.starting_qbs[:]
        players += self.starting_wrs
        players += self.starting_rbs
        players += self.starting_tes
        players += self.starting_flex
        players += self.starting_k
        players += self.starting_dst
        players += self.bench
        return players
