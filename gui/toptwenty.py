from Tkinter import *
from helpers import generate_fake_players, filter_fakes_by_position

from models.draft import DraftPool
from models.player import Player

class DPListbox(LabelFrame):
    def __init__(self, parent, players, category, overall=False):
        LabelFrame.__init__(self, parent, text=category)
        self.parent = parent
        self.players = players

        self.top20ListBox = Listbox(self, height=20)
        self.top20ListBox.pack(side=LEFT)
        if overall == False:
            for i in range(20):
                self.top20ListBox.insert(END, self.players[i].get_name())
        else:
            for player in self.players:
                self.top20ListBox.insert(END, player.get_name())

    def delete_by_name(self, name):
        for i in range(self.top20ListBox.size()):
            if self.top20ListBox.get(i) == name:
                self.top20ListBox.delete(i)

    def add_name(self, name):
        self.top20ListBox.insert(END, name)

    def get(self, start, finish):
        return list(self.top20ListBox.get(start, finish))

def main():

    fake_players = generate_fake_players()
    tes          = filter_fakes_by_position(fake_players, "TE", 20)

    root = Tk()
    app = DPListbox(root, tes, "Overall")
    app.pack(side=LEFT)
    root.mainloop()  


if __name__ == '__main__':
    main()
