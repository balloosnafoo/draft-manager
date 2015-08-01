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

        self.left_frame = Frame(self)
        self.left_frame.pack(side=LEFT)

        # Only used for rbs
        self.right_frame = Frame(self)
        self.right_frame.pack(side=LEFT)

        self.gen_categories_frame = Frame(self.left_frame)
        self.gen_categories_frame.pack(side=LEFT)
        
        gen_categories = ["Position", "Team", "Rank", "Age"]
        self.gen_category_labels = []
        for i in range(len(gen_categories)):
            self.gen_category_labels.append(Label(self.gen_categories_frame, text=gen_categories[i],
                                                  font=("Sans", 8)))
            self.gen_category_labels[i].pack(side=TOP)

        self.gen_info_frame = Frame(self.left_frame)
        self.gen_info_frame.pack(side=LEFT)

        self.gen_info = []
        player_position = self.player.get_position()
        self.gen_info.append(Label(self.gen_info_frame, text=player_position, font=("Sans", 8)))
        player_team     = self.player.get_team()
        self.gen_info.append(Label(self.gen_info_frame, text=player_team, font=("Sans", 8)))
        player_rank     = self.player.get_rank()
        self.gen_info.append(Label(self.gen_info_frame, text=player_rank, font=("Sans", 8)))
        player_age      = self.player.get_age()
        self.gen_info.append(Label(self.gen_info_frame, text=player_age, font=("Sans", 8)))
        for item in self.gen_info:
            item.pack(side=TOP)

        #if self.player.get_position() == "RB":
        #    self.init_rb()

    def init_rb(self):

        self.rb_categories_frame = Frame(self.right_frame)
        self.rb_categories_frame.pack(side=LEFT)

        rb_categories = ["Depth", "R Behind", "R Ahead"]
        self.rb_category_labels = []
        for i in range(len(rb_categories)):
            self.rb_category_labels.append(Label(self.rb_categories_frame, text=rb_categories[i],
                                                 font=("Sans", 8)))
            self.rb_category_labels[i].pack(side=TOP)

        self.rb_info_frame = Frame(self.right_frame)
        self.rb_info_frame.pack(side=LEFT)

        self.rb_info = []
        player_depth = self.player.depth_pos
        self.rb_info.append(Label(self.gen_info_frame, text=player_depth, font=("Sans", 8)))

    def update_player(self, player):
        #self.name_label.configure(text=player.get_name())
        self.configure(text=player.get_name())
        self.gen_info[0].configure(text=player.get_position())
        self.gen_info[1].configure(text=player.get_team())
        self.gen_info[2].configure(text=player.get_rank())
        self.gen_info[3].configure(text=player.get_age())
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

