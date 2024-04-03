import matplotlib.pyplot as plt
import pandas as pd
from main import *
import numpy as np
import seaborn as sns
NB_GAMES = 10
agents = ["random","alphabeta","mcts","agent"]
#agents = ["random"]
#test = {"random":RandomAgent(1, ShobuGame()),"alphabeta": AlphaBetaAgent(0, ShobuGame(), 3)}
draw = {}

df = pd.DataFrame(0, index=agents, columns=agents)


for agent1 in agents:
    for agent2 in agents:
        if(agent1 == agent2):
            continue
        if(df[agent1][agent2] != 0 or df[agent2][agent1] != 0):
            continue
        print("--- ", agent1," VS ",agent2)
        args = argparse.Namespace(white=agent1, black=agent2)
        args.white = agent1
        args.black = agent2
        agent_white,agent_black  = get_agents(args, False)

        NB_WHITE_WINS, NB_BLACK_WINS, NB_DRAWS = 0, 0, 0

        for i in range(NB_GAMES):
            print("Game ",i)
            winner, n_moves = main(agent_white, agent_black)
            if winner == 0:
                NB_WHITE_WINS += 1
            elif winner == 1:
                NB_BLACK_WINS += 1
            else:
                NB_DRAWS += 1

        PERC_NB_WHITE_WINS = (100 * NB_WHITE_WINS) / NB_GAMES
        PERC_NB_BLACK_WINS = (100 * NB_BLACK_WINS) / NB_GAMES
        PERC_NB_DRAWS = (100 * NB_DRAWS) / NB_GAMES
        percentages = [PERC_NB_WHITE_WINS, PERC_NB_BLACK_WINS, PERC_NB_DRAWS]
        #res[(agent1,agent2)] = percentages
        df[agent1][agent2] = PERC_NB_WHITE_WINS
        df[agent2][agent1] = PERC_NB_BLACK_WINS
        draw[(agent1,agent2)] = PERC_NB_DRAWS

print(draw)

print(df)
#create heatmap
plt.pcolor(df, cmap='RdBu')
plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
cax = plt.matshow(df, interpolation='nearest')
cax.set_clim(0, 100)
plt.colorbar(cax)
#plt.clim(-4,4)
plt.show()