from matplotlib import pyplot as plt
from main import *

def createBarGraph(percentages, white_player, black_player):
    text = ['White','Black','Draw']
    colors_list = ['Red','Orange', 'Purple']

    plt.figure(figsize=(8, 8))
    graphBar = plt.bar(text, percentages, color=colors_list)
    plt.title("Win rate : White = {} and Black = {}".format(white_player, black_player))
    
    for i, bar in enumerate(graphBar):
        width = bar.get_width()
        height = bar.get_height()
        x, y = bar.get_xy()
        plt.text(x + width / 2, y + height * 1.01, str(percentages[i]) + '%', ha='center', weight='bold')

    plt.show()
    plt.savefig("WinRate_{}_against_{}.png".format(white_player, black_player))


if __name__ == "__main__":

    agent_white = AlphaBetaAgent(0, ShobuGame(), 3)
    agent_black = RandomAgent(1, ShobuGame())

    NB_GAMES = 1
    NB_WHITE_WINS, NB_BLACK_WINS, NB_DRAWS = 0, 0, 0

    for i in range(NB_GAMES):
        winner, n_moves = main(agent_white, agent_black)
        if winner == 0: NB_WHITE_WINS += 1
        elif winner == 1: NB_BLACK_WINS += 1
        else: NB_DRAWS += 1
    
    PERC_NB_WHITE_WINS = (100 * NB_WHITE_WINS) / NB_GAMES
    PERC_NB_BLACK_WINS = (100 * NB_BLACK_WINS) / NB_GAMES
    PERC_NB_DRAWS      = (100 * NB_DRAWS) / NB_GAMES
    percentages = [PERC_NB_WHITE_WINS, PERC_NB_BLACK_WINS, PERC_NB_DRAWS]
    
    createBarGraph(percentages, agent_white, agent_black)