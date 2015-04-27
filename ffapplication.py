from Tkinter import *
import random

from gui.team import TeamFrame
from gui.toptwenty import DPListbox
from gui.player import PlayerFrame
from gui.nextrounders import NextRoundLB
from gui.helpers import generate_fake_players, filter_fakes_by_position, filter_players_by_position

from models.draft import *
from models.player import Player

OFFENSIVE_POSITIONS = ["QB", "WR", "RB", "TE"]
NUM_TEAMS = 10
TEAMS = ["Matt", "Mike", "Kevin", "Dave", "Will", "Francos", "Greg", "Evan", "Jason", "Some Guy"]
random.shuffle(TEAMS)
SNAKE_DRAFT = True
IS_USER = "Matt"


class Application(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Draft Manager")
        
        self.pack(fill=BOTH, expand=1)

        # Top container holds top 20 lists
        self.top_container  = Frame(self)
        self.top_container.pack(side=TOP)

        # Mid container holds manipulation buttons
        self.mid_container  = Frame(self)
        self.mid_container.pack(side=TOP)

        # Mid container 2 holds comparison frames (left) and
        #                       next rounders (right)
        self.mid_container2 = Frame(self)
        self.mid_container2.pack(side=TOP)

        self.mid2_left = Frame(self.mid_container2)
        self.mid2_left.pack(side=LEFT)

        self.mid2_right = Frame(self.mid_container2)
        self.mid2_right.pack(side=RIGHT)

        # Bottom container holds team rosters
        self.bottom_container = Frame(self)
        self.bottom_container.pack(side=BOTTOM)
        self.bottom1 = Frame(self.bottom_container)
        self.bottom1.pack(side=TOP)
        self.bottom2 = Frame(self.bottom_container)
        self.bottom2.pack(side=TOP)

        # Initialize Draft object
        self.draft = Draft(TEAMS, IS_USER)

        # Initialize team frames
        self.init_teams()

        # Initialize manipulation buttons
        self.init_UI()

        # Initialize comparison frames
        self.init_comparison_frames(self.mid2_left)

        # Initialize next round listbox
        self.init_next_round_lb(self.mid2_right)

        # Initialize top 20 list boxes
        self.init_top20s()

    def init_teams(self):
        self.team_widgets = []
        for i in range(NUM_TEAMS):
            if i < NUM_TEAMS / 2:
                self.team_widgets.append(TeamFrame(self.bottom1, TEAMS[i]))
                if i == 0:
                    self.team_widgets[i].highlight_team()
            else:
                self.team_widgets.append(TeamFrame(self.bottom2, TEAMS[i]))

        for team_widget in self.team_widgets:
            team_widget.pack(side=LEFT, ipadx="10m", ipady=10)

    def init_top20s(self):

        """Creates top twenty label boxes for offensive positions.
        defenses and kickers are ommitted because of limited screen
        space and low value""" 

        # Randomly generate players for development
        # players = generate_fake_players()

        players = self.draft.get_players()

        self.top20_widgets = []
        self.top20_widgets.append(DPListbox(self.top_container, players,
                                                   "Overall", True)) 
        for pos in OFFENSIVE_POSITIONS:
            pos_players = filter_players_by_position(players, pos, 20)
            self.top20_widgets.append(DPListbox(self.top_container,
                                                pos_players, pos))

        for widget in self.top20_widgets:
            widget.pack(side=LEFT)

    def init_UI(self):

        self.search_entry = Entry(self.mid_container)
        self.search_entry.pack(side=LEFT)
        self.search_entry.bind("<Return>", self.draft_button_click)

        self.draft_button = Button(self.mid_container, text="Draft")
        self.draft_button.pack(side=LEFT, padx=10, pady=5)
        self.draft_button.bind("<Button-1>", self.draft_button_click)

        self.upside_plus_button = Button(self.mid_container, text="+ Upside Weight")
        self.upside_plus_button.pack(side=LEFT)

        self.upside_minus_button = Button(self.mid_container, text="- Upside Weight")
        self.upside_minus_button.pack(side=LEFT)

    def init_comparison_frames(self, parent):

        # Uses first two ranked players as default compares
        player1 = self.draft.draft_pool.players[0]
        player2 = self.draft.draft_pool.players[1]

        self.player1_frame = PlayerFrame(parent, player1)
        self.player1_frame.pack(side=LEFT, ipadx="10m")
        self.player1_button = Button(self.player1_frame, text="Update")
        self.player1_button.pack(side=BOTTOM)
        self.player1_button.bind("<Button-1>", self.insert_comparison)

        self.player2_frame = PlayerFrame(parent, player2)
        self.player2_frame.pack(side=LEFT, ipadx="10m")
        self.player2_button = Button(self.player2_frame, text="Update")
        self.player2_button.pack(side=BOTTOM)
        self.player2_button.bind("<Button-1>", self.insert_comparison)

    def init_next_round_lb(self, parent):
        self.next_round_lb = NextRoundLB(parent)
        self.next_round_lb.pack(side=LEFT)

    def draft_button_click(self, event):
        current_focus = self.focus_get()
        if isinstance(current_focus, Listbox):

            # Get index/name/player/position object and clear entry
            index = current_focus.curselection()[0]
            name = current_focus.get(index)
            current_focus.delete(index)
            draftee = self.draft.draft_by_name(name)
            position = draftee.get_position()

            # discover id of active top 20 widget
            counter = 0
            for widget in self.top20_widgets:
                if current_focus.winfo_parent() == str(widget):
                    current_focus = widget
                    break
                else:
                    counter += 1

            if counter == 0:
                # case in which player has been selected from overall top 20
                if position != "DST" and position != "K":
                    counter = OFFENSIVE_POSITIONS.index(position) + 1
                    needs_replacement = name in self.top20_widgets[counter].get(0, END)
                    self.top20_widgets[counter].delete_by_name(name)
            else:
                # if player has been selected from position sorted top 20
                self.top20_widgets[0].delete_by_name(name)
                needs_replacement = True

        # If player was drafted through the entry field
        elif isinstance(current_focus, Entry):
            name = current_focus.get()
            current_focus.delete(0, END)
            draftee = self.draft.draft_by_name(name)
            if draftee == None:
                return
            position = draftee.get_position()
            self.top20_widgets[0].delete_by_name(name)
            if not position == "DST" and not position == "K":
                counter = OFFENSIVE_POSITIONS.index(position) + 1
                needs_replacement = name in self.top20_widgets[counter].get(0, END)
                self.top20_widgets[counter].delete_by_name(name)

        # insert new name to fill position top 20 widget if not K or D/ST
        if not position == "DST" and not position == "K" and needs_replacement:
            new_list = filter_players_by_position(self.draft.get_players(),
                                                  OFFENSIVE_POSITIONS[counter - 1], 20)
            if len(new_list) == 20:
                self.top20_widgets[counter].add_name(new_list[-1].get_name())

        # send player to Team, retreive placement info, adjust TeamFrame
        current_pick = self.draft.get_current_pick()
        drafting_team = self.draft.order[current_pick]
        placement = self.draft.teams[drafting_team].place_draftee(draftee, current_pick)
        self.team_widgets[drafting_team].update_position(draftee.get_name(), placement)

        # increment counter, update highlights for TeamLabels
        self.draft.increment_current_pick()
        self.team_widgets[drafting_team].unhighlight_team()
        self.team_widgets[self.draft.order[
                          self.draft.current_pick]].highlight_team()

        self.update_next_rounders()

    def update_next_rounders(self):
        team = self.draft.teams[self.draft.order[self.draft.get_current_pick()]]
        if team.is_user:
            self.next_round_lb.delete(0,END)
            for position in OFFENSIVE_POSITIONS:
                offset = self.draft.get_num_picks_before_next()
                next_player, cushion = self.draft.get_next(position, offset)
                string = "%s: %s (%s)" % (position, next_player, str(cushion))
                self.next_round_lb.insert(END, string)

    def insert_comparison(self, event):
        if event.widget == self.player1_button:
            player_frame = self.player1_frame
        else:
            player_frame = self.player2_frame

        current_focus = self.focus_get()
        index = current_focus.curselection()[0]
        name = current_focus.get(index)
        player = self.draft.get_player_by_name(name)

        player_frame.update_player(player)

root = Tk()
app  = Application(root)
root.mainloop()
app.draft.export_teams()


