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
    plt.savefig("WinRate_{}_against_{}.pdf".format(white_player, black_player))


def plotExecTime(execTime, nbCoups):

    plt.plot([i for i in range(1, 1 + nbCoups["RandomAgent"])], execTime["RandomAgent"][:nbCoups["RandomAgent"]], label='RandomAgent')
    plt.plot([i for i in range(1, 1 + nbCoups["UCTAgent"])], execTime["UCTAgent"][:nbCoups["UCTAgent"]], label='UCTAgent')
    plt.plot([i for i in range(1, 1 + nbCoups["AlphaBetaAgent"])], execTime["AlphaBetaAgent"][:nbCoups["AlphaBetaAgent"]], label='AlphaBetaAgent')
    plt.plot([i for i in range(1, 1 + nbCoups["ContestAgent"])], execTime["ContestAgent"][:nbCoups["ContestAgent"]], label='ContestAgent')

    plt.xlabel('Number of moves [/]')
    plt.xticks([i for i in range(0, 1 + max(nbCoups.values()), 10)])
    plt.ylabel('Execution time [s]')
    plt.title('Execution time by move for each agent')
    plt.legend()
    plt.grid()
    plt.show()
    plt.savefig("TempsExecutionParCoup.pdf")


def lineChart_ExecTime_AgainstRandomAgent():

    agent_whites = [AlphaBetaAgent(0, ShobuGame(), 3), UCTAgent(0, ShobuGame(), 100), AI(0, ShobuGame()), RandomAgent(0, ShobuGame())]
    agent_black = RandomAgent(0, ShobuGame())

    execTime = {"RandomAgent": [], "UCTAgent": [], "AlphaBetaAgent": [], "ContestAgent": []}
    nbMoves = {"RandomAgent": 0, "UCTAgent": 0, "AlphaBetaAgent": 0, "ContestAgent": 0}

    for i in range(4):
        agent_white = agent_whites[i]
        main(agent_white, agent_black)
        execTime[str(agent_white)] += agent_white.time
        nbMoves[str(agent_white)] = agent_white.coup_i
  
    plotExecTime(execTime, nbMoves)


def lineChart_ExecTime_AgainstThemself():

    agents = [AlphaBetaAgent(0, ShobuGame(), 3), UCTAgent(0, ShobuGame(), 100), AI(0, ShobuGame())]

    execTime = {"UCTAgent": [], "AlphaBetaAgent": [], "ContestAgent": []}
    nbMoves  = {"UCTAgent": 0, "AlphaBetaAgent": 0, "ContestAgent": 0}

    for i in range(3):
        agent_white = agents[i]
        agent_black = agents[i]
        main(agent_white, agent_black)
        execTime[str(agent_white)] += agent_white.time
        nbMoves[str(agent_white)] = agent_white.coup_i
    
    plt.plot([i for i in range(1, 1 + nbMoves["UCTAgent"])], execTime["UCTAgent"][:nbMoves["UCTAgent"]], label='UCTAgent')
    plt.plot([i for i in range(1, 1 + nbMoves["AlphaBetaAgent"])], execTime["AlphaBetaAgent"][:nbMoves["AlphaBetaAgent"]], label='AlphaBetaAgent')
    plt.plot([i for i in range(1, 1 + nbMoves["ContestAgent"])], execTime["ContestAgent"][:nbMoves["ContestAgent"]], label='ContestAgent')

    plt.xlabel('Number of moves [/]')
    plt.xticks([i for i in range(0, 1 + max(nbMoves.values()), 10)])
    plt.ylabel('Execution time [s]')
    plt.title('Execution time by move for each agent')
    plt.legend()
    plt.grid()
    plt.show()
    plt.savefig("TempsExecutionParCoup.pdf")

def getNodeExploredAgainstRandomAgent():
    
    agents_white = [AlphaBetaAgent(0, ShobuGame(), 3), UCTAgent(0, ShobuGame(), 100), AI(0, ShobuGame()), RandomAgent(0, ShobuGame())]
    agent_black = RandomAgent(0, ShobuGame())

    for i in range(4):
        agent_white = agents_white[i]
        main(agent_white, agent_black)
        print("Node explored for {} : {} in {} moves => Node explored by move : {}\n".format(agent_white, agent_white.nodeExplored, agent_white.coup_i, agent_white.nodeExplored / agent_white.coup_i))

def getNodeExploredAgainstAgent():
    
    agents_white = [AlphaBetaAgent(0, ShobuGame(), 3), UCTAgent(0, ShobuGame(), 100), AI(0, ShobuGame()), RandomAgent(0, ShobuGame())]
    agents_black = [AlphaBetaAgent(0, ShobuGame(), 3), UCTAgent(0, ShobuGame(), 100), AI(0, ShobuGame()), RandomAgent(0, ShobuGame())]

    for i in range(4):
        agent_white = agents_white[i]
        agent_black = agents_black[i]
        main(agent_white, agent_black)
        print("Node explored for {} : {} in {} moves => Node explored by move : {}\n".format(agent_white, agent_white.nodeExplored, agent_white.coup_i, agent_white.nodeExplored / agent_white.coup_i))

if __name__ == "__main__":

    # getNodeExploredAgainstAgent()
    # getNodeExploredAgainstRandomAgent()
    # lineChart_ExecTime_AgainstRandomAgent()
    lineChart_ExecTime_AgainstThemself()

    NB_GAMES = 1
    NB_WHITE_WINS, NB_BLACK_WINS, NB_DRAWS = 0, 0, 0
    tmps_exec = {"RandomAgent": [], "UCTAgent": [], "AlphaBetaAgent": [], "ContestAgent": []}
    nbCoups = {"RandomAgent": 0, "UCTAgent": 0, "AlphaBetaAgent": 0, "ContestAgent": 0}

    PERC_NB_WHITE_WINS = (100 * NB_WHITE_WINS) / NB_GAMES
    PERC_NB_BLACK_WINS = (100 * NB_BLACK_WINS) / NB_GAMES
    PERC_NB_DRAWS      = (100 * NB_DRAWS) / NB_GAMES
    percentages        = [PERC_NB_WHITE_WINS, PERC_NB_BLACK_WINS, PERC_NB_DRAWS]
    
    createBarGraph(percentages, agent_white, agent_black)