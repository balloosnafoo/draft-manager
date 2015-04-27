from Tkinter import *

class TeamFrame(Frame):
    def __init__(self, parent, team_name):
        Frame.__init__(self, parent)
        self.parent = parent

        self.top_container = Frame(self)
        self.top_container.pack(side=TOP)
        self.left_container  = Frame(self)
        self.left_container.pack(side=LEFT)
        self.right_container = Frame(self)
        self.right_container.pack(side=LEFT)

        self.team_label = Label(self.top_container, text=team_name)
        self.team_label.pack(side=TOP)

        self.positions = ["QB", "WR1", "WR2", "RB1", "RB2", "FLEX", "TE", "K", "D/ST"]
        for i in range(6):
            self.positions.append("BN")

        self.right_labels = []
        for position in self.positions:
            ll = Label(self.left_container,  text=position, font=("Sans", 6))
            rl = Label(self.right_container, text="none", font=("Sans", 6))
            self.right_labels.append(rl)

            ll.pack(side=TOP)
            rl.pack(side=TOP)

    def update_position(self, name, position):
        bench_correction = 0
        if position[0:2] == "BN":
            bench_correction = int(position[-1]) - 1
            position = position[0:2]
        index = self.positions.index(position)
        if bench_correction:
            index += bench_correction
        self.right_labels[index].configure(text=name)

    def highlight_team(self):
        self.team_label.configure(fg="red")

    def unhighlight_team(self):
        self.team_label.configure(fg="black")

def main():
    root = Tk()
    team = TeamFrame(root)
    team.pack(side=LEFT)
    root.mainloop()

if __name__ == '__main__':
    main()

