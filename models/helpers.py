import sqlite3 as lite
import datetime
import nflgame as nfl

from datetime import date

from models.player import Player
from models.team import Team

# Data importing functions

def import_fpros_overall():
    f = open('data/fpros_overall.csv', 'r')
    for i in range(7):
        f.readline()
    players = []
    for line in f:
        stats = line.split('\t')
        name, position, best_rank = stats[1], stats[2], stats[5]
        team, rank = stats[3], stats[0]
        age = get_player_age(name, position)
        players.append(Player(name, position, age, team, rank))
    f.close() 
    add_distance_to_next(players)
    return players

def get_player_age(name, position):
    player_nfl = get_player_nfl_object(name, position)
    if player_nfl == "N/A":
        return 0
    # print "get_player_age:", player_nfl # Helps find differences in names and nflgame and ffp
    birthdate = player_nfl.birthdate.split("/")
    birth_month = int(birthdate[0])
    birth_year  = int(birthdate[2])
    cur_year    = date.today().year
    cur_month   = date.today().month

    age = cur_year - birth_year
    if cur_month < birth_month:
        age -= 1

    return age

EXCEPTIONS = {
    #FProsName: nflgameName
    "Odell Beckham Jr.": "Odell Beckham",
    "Ty Hilton": "T.Y. Hilton",
    "Christopher Ivory": "Chris Ivory",
    "Daniel Herron": "Dan Herron"
}

POSITION_ERRORS = {
    "Charles Clay": "RB"
}

def get_player_nfl_object(name, position):
    if name in EXCEPTIONS.keys():
        name = EXCEPTIONS[name]
    if name in POSITION_ERRORS.keys():
        position = POSITION_ERRORS[name]
    elif position == "DST" or position == "K":
        return "N/A"
    matches = nfl.find(name)
    if len(matches) == 1:
        return matches[0]
    else:
        for p in matches:
            if position == p.position:
                return p

def add_distance_to_next(players):
    depth_charts = {}
    for i in range(len(players)):
        if players[i].position != "RB":
            continue
        team_i = players[i].team
        if not team_i in depth_charts.keys():
            depth_charts[team_i]  = 1
        else:
            depth_charts[team_i] += 1
        players[i].depth_pos = depth_charts[team_i]
        for j in range(len(players[i:])):
            if players[i+j].position != "RB" or j == 0:
                continue
            team_j = players[i+j].team
            if team_i == team_j:
                players[i].above_next   = j
                players[i+j].below_next = j
                break

def import_fpros_k():
    f = open('data/fpros_k.csv', 'r')
    for i in range(7):
        f.readline()
    players = []
    for line in f:
        stats = line.split('\t')
        name, position, best_rank = stats[1], "K", "N/A"
        age, team, rank = "N/A", stats[2], "N/A"
        players.append(Player(name, position, age, team, rank))
    f.close()
    return players

def import_fpros_dst():
    f = open('data/fpros_dst.csv', 'r')
    for i in range(7):
        f.readline()
    players = []
    for line in f:
        stats = line.split('\t')
        name, position, best_rank = stats[1], "DST", "N/A"
        age, team, rank = "N/A", "N/A", "N/A"
        players.append(Player(name, position, age, team, rank))
    f.close() 
    return players

# Database helpers

def create_team_table(teams):
    """Function receives tuple of tuples with team info, clears previous records,
    records in db"""
    con = lite.connect('data/results.db')

    with con:
        cur = con.cursor()
        # Comment out following line if keeping track of all drafts        
        cur.execute("DROP TABLE IF EXISTS Teams")
        cur.execute("CREATE TABLE IF NOT EXISTS Teams(TeamId INT, Manager TEXT)")
        cur.executemany("INSERT INTO Teams VALUES(?, ?)", teams)

def create_player_table():
    con = lite.connect('data/results.db')
    with con:
        cur = con.cursor()
        # Comment out following line if keeping track of all drafts
        cur.execute("DROP TABLE IF EXISTS Players")
        cur.execute("CREATE TABLE IF NOT EXISTS Players(TeamId INT, Name TEXT, Position TEXT, Age INT, Team TEXT, SubjVal INT)")

def export_players(data):
    con = lite.connect('data/results.db')
    with con:
        cur = con.cursor()
        cur.executemany("INSERT INTO Players VALUES(?, ?, ?, ?, ?, ?)", data)

def export_draft(picks_made, picks_possible):
    """
    UNFINISHED, UNINTEGRATED Creates table allowing for all drafts to be tracked.
    """
    con = lite.connect('data/results.db')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Drafts(DraftId INT AUTO_INCREMENT, " +
                    "                     Date TEXT, PicksMade INT, PicksPossible INT)")
        date = datetime.date.today()
        cur.execute("INSERT INTO Drafts VALUES(?, ?, ?)", (str(date), 0, 0))













