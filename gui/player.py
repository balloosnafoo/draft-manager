from Tkinter import *

#Player model is found in ./models/player

class PlayerFrame(LabelFrame):
    def __init__(self, parent, player):
        LabelFrame.__init__(self, parent, text=player.get_name())

        self.parent = parent
        self.player = player
        self.active = False

        #self.name_frame = Frame(self)
        #self.name_frame.pack(side=TOP)
        #self.name_label = Label(self, text=self.player.get_name())
        #self.name_label.pack(side=TOP)

        self.mid_frame = Frame(self)
        self.mid_frame.pack(side=TOP)

        self.stat_categories_frame = Frame(self.mid_frame)
        self.stat_categories_frame.pack(side=LEFT)
        
        categories = ["Position", "Team", "Rank", "Age"]
        self.category_labels = []
        for i in range(len(categories)):
            self.category_labels.append(Label(self.stat_categories_frame, text=categories[i]))
            self.category_labels[i].pack(side=TOP)

        self.info_frame = Frame(self.mid_frame)
        self.info_frame.pack(side=LEFT)

        self.info = []
        player_position = self.player.get_position()
        self.info.append(Label(self.info_frame, text=player_position))
        player_team     = self.player.get_team()
        self.info.append(Label(self.info_frame, text=player_team))
        player_rank     = self.player.get_rank()
        self.info.append(Label(self.info_frame, text=player_rank))
        player_age      = self.player.get_age()
        self.info.append(Label(self.info_frame, text=player_age))
        for item in self.info:
            item.pack(side=TOP)

    def update_player(self, player):
        #self.name_label.configure(text=player.get_name())
        self.configure(text=player.get_name())
        self.info[0].configure(text=player.get_position())
        self.info[1].configure(text=player.get_team())
        self.info[2].configure(text=player.get_rank())
        self.info[3].configure(text=player.get_age())
        if player.position == "RB":
            print "Depth:", player.depth_pos
            print "Distance to next:", player.above_next
            print "Distance to prev:", player.below_next

    def is_active(self):
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

