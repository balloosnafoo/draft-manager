from models.player import Player
from models.helpers import *
from models.team import Team

class Draft(object):
    def __init__(self, teams, user_name):
        self.draft_pool = DraftPool()
        self.teams = []
        for team in teams:
            is_user = user_name == team
            self.teams.append(Team(team, is_user))
        self.order = self.create_draft_order()
        self.current_pick = 0
        self.current_round = 1

        # for development only
        self.export_managers()

    def create_draft_order(self):
        num_teams = len(self.teams)
        forward = range(num_teams)
        backward = forward[:]
        backward.reverse()
        order = []
        for i in range(15):
            if i % 2 == 0:
                order += forward
            else:
                order += backward
        return order

    def draft_by_name(self, name):
        return self.draft_pool.draft_by_name(name)

    def get_player_by_name(self, name):
        return self.draft_pool.get_player_by_name(name)

    def increment_current_pick(self):
        self.current_pick += 1
        if self.current_pick % len(self.teams) == 0:
            self.current_round += 1

    # Export functions
    def export_managers(self):
        teams = []
        for idx in range(len(self.teams)):
            teams.append((idx, self.teams[idx].get_manager()))
        create_team_table(tuple(teams))

    def export_teams(self):
        create_player_table()
        export = []
        for idx in range(len(self.teams)):
            players = self.teams[idx].export_players()
            for p in players:
                export.append((idx, p[0], p[1], p[2], p[3], p[4], p[5]))
        export_players(tuple(export))


    # Getters and setters
    def get_players(self):
        return self.draft_pool.get_players()

    def get_current_pick(self):
        return self.current_pick

    def get_num_picks_before_next(self):
        cur     = self.current_pick
        team    = self.order[cur]
        counter = 0
        while cur + counter < len(self.order):
            counter += 1
            if self.order[cur + counter] == team:
                break
        return counter

    def get_next(self, position, offset):
        players = self.get_players()
        for i in range(offset, len(players)):
            if players[i].get_position() == position:
                return players[i].get_name(), i - offset

    def get_next_as_object(self, position, offset):
        players = self.get_players()
        for i in range(offset, len(players)):
            if players[i].get_position() == position:
                return players[i], i - offset

class DraftPool(object):
    def __init__(self):
        self.players =  import_fpros_overall()
        self.players += import_fpros_k()
        self.players += import_fpros_dst()

    def draft_by_name(self, name):
        """Returns player and removes from draft pool"""
        for i in range(len(self.players)):
            if self.players[i].get_name() == name:
                return self.players.pop(i)

    def get_player_by_name(self, name):
        """Returns player but doesn't remove from pool"""
        for i in range(len(self.players)):
            if self.players[i].get_name() == name:
                return self.players[i]

    def get_players(self):
        return self.players


