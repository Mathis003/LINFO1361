import itertools
import concurrent.futures
import threading
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from main import *

NB_GAMES = 5
agents = ["random", "alphabeta", "mcts", "agent"]
agents = ["random", "alphabeta", "mcts"]
draw = {}

df = pd.DataFrame(0, index=agents, columns=agents)

print_lock = threading.Lock()

def play_games(agent1, agent2):

    if (agent1 == agent2 or df[agent1][agent2] != 0 or df[agent2][agent1] != 0): return

    args = argparse.Namespace(white=agent1, black=agent2)
    args.white = agent1
    args.black = agent2
    agent_white,agent_black  = get_agents(args, False)

    NB_WHITE_WINS, NB_BLACK_WINS, NB_DRAWS = 0, 0, 0

    for i in range(NB_GAMES):

        with print_lock: print("--- ", i ,"-", agent1, " VS ", agent2)

        winner, _ = main(agent_white, agent_black)
        if winner == 0:   NB_WHITE_WINS += 1
        elif winner == 1: NB_BLACK_WINS += 1
        else:             NB_DRAWS += 1

    PERC_NB_WHITE_WINS = (100 * NB_WHITE_WINS) / NB_GAMES
    PERC_NB_BLACK_WINS = (100 * NB_BLACK_WINS) / NB_GAMES
    PERC_NB_DRAWS      = (100 * NB_DRAWS) / NB_GAMES

    df[agent1][agent2] = PERC_NB_WHITE_WINS
    df[agent2][agent1] = PERC_NB_BLACK_WINS
    draw[(agent1,agent2)] = PERC_NB_DRAWS

actions = list(itertools.combinations(agents, 2))

with concurrent.futures.ThreadPoolExecutor() as executor:
    future_to_game = {executor.submit(play_games, agent1, agent2): (agent1, agent2) for agent1, agent2 in actions}
    for future in concurrent.futures.as_completed(future_to_game):
        try:
            agent1, agent2 = future_to_game[future]
        except Exception as exc:
            print('%r generated an exception: %s' % (agent1, agent2, exc))

print(draw)
print(df)

# Create heatmap
plt.pcolor(df, cmap='RdBu')

cax = plt.matshow(df, interpolation='nearest')
cax.set_clim(0, 100)
plt.colorbar(cax)
plt.yticks(np.arange(0, len(df.index), 1), df.index, rotation=45)
plt.xticks(np.arange(0, len(df.columns), 1), df.columns)
plt.savefig("WinRate.pdf")
plt.show()