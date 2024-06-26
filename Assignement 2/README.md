# LINFO1361-Shobu

## Files to modify
agent.py => Create our own agent

## Run the code
You can run the code with the following command

> python3 main.py

Different options are made available:
- **-w {random|alphabeta|mcts|agent|human}**: white player agent
- **-b {random|alphabeta|mcts|agent|human}**: black player agent
- **-t \<time value\>**: time (in seconds) allowed to each player to complete the game
- **-d**: display option, shows a graphical interface for the game
- **-l \<filename\>**: log option, stores the game into the given filename
- **-r \<filename\>**: replay option, use the log file given as filename to replay the recorded
game
- **-dt \<value\>**: delay time option, time (in seconds) between each move when replaying
a game
- **-st \<value\>**: start turn option, the number of turn at which the replay should start

For example, you can use this command to run a game and record it into "logs.txt"

> python3 main.py -w human -b agent -t 600 -d -l logs.txt

and you can use this command to replay this game from the 42nd turn with a delay of 1 second between each replayed move

> python3 main.py -r logs.txt -dt 1 -st 42