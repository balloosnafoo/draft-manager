
class Player(object):
    def __init__(self, name, position, age, team, rank):
        self.name = name
        self.position = position
        self.age = age
        self.team = team
        self.rank = rank

        """
        These attributes give an idea of how secure a player is in
        his position in the depth chart
        """
        if self.position == "RB":
            self.depth_pos = 0
            self.above_next = 500
            self.below_next = 0

        self.picked_at = None

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

    def get_rank(self):
        return self.rank

    def get_age(self):
        return self.age

    def get_team(self):
        return self.team

    def get_picked_at(self):
        return self.picked_at

    def get_subjective_value(self):
        if self.position in ["DST", "K"]:
            return -999 
        return int(self.rank) - self.picked_at 

    def set_picked_at(self, number):
        self.picked_at = number
