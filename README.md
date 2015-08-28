# draft-manager

This is a personal project that has three goals:
* Learn something about GUIs (specifically Tkinter)
* Win my fantasy football draft (obviously)
* Gather information about how others draft

# Features

* Uses rankings from Fantasy Pros. This is not currently integrated into the script itself, rather the user has
to hit the 'export' link on the fantasy pros website to get draft rankings.

* Uses player information gathered from the nflgame package in order to calculate the player's current age as well
as displaying the number of seasons played.

* Calculates a measure of positional security for each player by examining the distance between that player and
the next ranked player at the same position on the same team. 
  * Ex: if G. Bernard (RB, CIN) ranks 45 and J. Hill (RB, CIN) ranks 39, it might be the case that J. Hill is not
  particularly secure in his role, or that they split carries a lot.
  
* Displays all team rosters, so that the user can quickly see who has positional needs that might affect who is drafted
between now and their next pick.

* Displays the players that are going to be available next round assuming that everyone between the user's current
pick and their next pick drafts the best available player.
