def generate_fake_players():
    import random
    first_names = []
    last_names  = []
    f = open('names.csv', 'r')
    for line in f:
        first, last = line.split(',')
        first_names.append(first)
        last_names.append(last.strip())
    f.close()
    positions = ["QB", "WR", "RB", "TE"]

    fake_players = []
    for i in range(200):
        first  =first_names[random.randrange(0, len(first_names))]
        last   = last_names[random.randrange(0, len(last_names))]
        position = positions[random.randrange(0, len(positions))]
        fake_players.append("%s %s, %s" % (first, last, position))
    
    return fake_players

def filter_fakes_by_position(overall_list, position, num):
    players = []
    for player in overall_list:
        if player[-2:] == position:
            players.append(player)
        if len(players) >= num:
            break

    return players

def filter_players_by_position(players, position, num):
    filtered_players = []
    for player in players:
        if player.get_position() == position:
            filtered_players.append(player)
        if len(filtered_players) >= num:
            break

    return filtered_players
