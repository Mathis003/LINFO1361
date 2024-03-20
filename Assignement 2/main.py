from agents.random_agent import RandomAgent
from agents.human_agent import HumanAgent
from agents.alphabeta_agent import AlphaBetaAgent
from agents.uct_agent import UCTAgent
from agents.contest_agent import AI
from shobu import ShobuGame

from logs import *
from interface import *

import argparse
import time
import random

from matplotlib import pyplot as plt

def get_agents(args, display):

    def get_agent(player, agent_name):
        if agent_name == "human":
            return HumanAgent(player)
        elif agent_name == "random":
            return RandomAgent(player, ShobuGame())
        elif agent_name == "alphabeta":
            return AlphaBetaAgent(player, ShobuGame(), 3) # 3 depth
        elif agent_name == "mcts":
            return UCTAgent(player, ShobuGame(), 50) # 500 iterations
        elif agent_name == "agent":
            return AI(player, ShobuGame())
        else:
            raise Exception(f"Invalid player: {agent_name}")
    
    if not display and (args.white == "human" or args.black == "human"):
        raise Exception("Cannot have human player without display")
    
    return get_agent(0, args.white), get_agent(1, args.black)


"""
Estimates the average branching factor of the game tree by simulating a number of games.

Args:
    game (ShobuGame): The game instance to simulate.
    num_simulations (int): The number of games to simulate.

Returns:
    float: The estimated average branching factor of the game tree.
"""
def calculate_branching_factor(game, num_simulations=1000):

    # Initialize the state and the branching factor
    MAX_TURNS = 500
    estimated_branching_factor = 0
    init_state = game.initial
    state = init_state

    # Simulate a number of games to estimate the average branching factor
    for _ in range(num_simulations):
        
        # Reset the number of turns and the branching factor
        nb_turns = 0
        branching_factor = 0

        # Simulate a game until it reaches a terminal state
        while not game.is_terminal(state) and nb_turns < MAX_TURNS:
            nb_turns += 1
            possible_actions = game.actions(state)
            branching_factor += len(possible_actions)
            action = random.choice(possible_actions)
            state = game.result(state, action)

        # print(f"Current branching factor: {branching_factor / nb_turns}")

        # Add the current branching factor to the estimated one
        estimated_branching_factor += branching_factor / nb_turns

        # Reset the state to the initial state
        state = init_state

    # Return the average branching factor over all simulations
    return estimated_branching_factor / num_simulations


def main(agent_white, agent_black, display=False, log_file=None, play_time=600):

    game = ShobuGame()
    state = game.initial

    # Get the average branching factor of the game tree
    # branching_factor = calculate_branching_factor(game, 100000)
    # print("Average branching factor: ", branching_factor)

    run = 1
    logs = []
    n_moves = 0

    if display:
        init_pygame()

    remaining_time_0 = play_time
    remaining_time_1 = play_time

    try:
        while not game.is_terminal(state) and run != -1 and remaining_time_0 > 0 and remaining_time_1 > 0:
            if n_moves > 10000:
                return -1, n_moves
            
            if run == 1:
                
                if game.to_move(state) == 0:
                    t0 = time.perf_counter()
                    action = agent_white.play(state, remaining_time_0)
                    while action == -2:
                        action = agent_white.play(state, remaining_time_0)
                    if play_time is not None:
                        remaining_time_0 -= time.perf_counter() - t0
                elif game.to_move(state) == 1:
                    t0 = time.perf_counter()
                    action = agent_black.play(state, remaining_time_1)
                    while action == -2:
                        action = agent_black.play(state)
                    if play_time is not None:
                        remaining_time_1 -= time.perf_counter() - t0
                else:
                    raise Exception(f"Invalid player: {state.to_move}")
                
                if log_file is not None:
                    logs.append(create_log(action, n_moves))

                if action not in game.actions(state):
                    raise Exception(f"Invalid action: {action}")
                
                state = game.result(state, action)

                n_moves += 1

            # TODO : To change to hide/see the game
            # display = False
            if display:
                run = update_ui(state)
        
    except Exception as e:
        if log_file is not None:
            write_logs(logs, log_file)
        raise e
    
    if remaining_time_0 <= 0:
        state = state._replace(utility=-1)
    if remaining_time_1 <= 0:
        state = state._replace(utility=1)

    while run != -1 and display:
        run = update_ui(state)

    if log_file is not None:
        write_logs(logs, log_file)

    if game.utility(state, 0) == 0:
        return -1, n_moves
    elif game.utility(state, 0) == 1:
        return 0, n_moves
    else:
        return 1, n_moves


def replay_game(actions, delay_time=0.0, display=True, start_turn=0):
    game = ShobuGame()
    state = game.initial
    if display:
        init_pygame()
    
    for action, n_move in actions:
        if action is not None:
            if n_move >= start_turn:
                state = game.result(state, action)
                if display:
                    run = update_ui(state)
                    if run == -1:
                        return
                time.sleep(delay_time)
            else:
                state = game.result(state, action)
    run = 1
    while run != -1 and display:
        run = update_ui(state)


# Ajout de fonction pour créer un graphique à barres
def createBarGraph(percentages):
    text = ['White','Black','Draw']
    colors_list = ['Red','Orange', 'Purple']

    # Create a bar graph to display the percentage of wins for the White and Black players
    plt.figure(figsize=(8, 8))
    graphBar = plt.bar(text, percentages, color=colors_list)
    plt.title('Percentage of wins for the White and Black players')
    
    # Display the percentage on the top of the bars
    for i, bar in enumerate(graphBar):
        width = bar.get_width()
        height = bar.get_height()
        x, y = bar.get_xy()
        plt.text(x + width / 2, y + height * 1.01, str(percentages[i]) + '%', ha='center', weight='bold')

    # Save the graph in a file called percentage.png
    plt.savefig('percentage-MCTS_vs_Random.png')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Shobu game')
    parser.add_argument('-w', '--white', type=str, default="random", help='White player ["random | human | alphabeta | mcts | agent"]')
    parser.add_argument('-b', '--black', type=str, default="random", help='Black player ["random | human | alphabeta | mcts | agent"]')
    parser.add_argument('-t', '--time', type=int, default=600, help='Time per game for each player (in seconds)')
    parser.add_argument('-d', '--display', action='store_true', help='Display game')
    parser.add_argument('-l', '--logs', type=str, default=None, help='path to log file to record the game')
    parser.add_argument('-dt', '--delay_time', type=float, default=0.0, help='Delay time between moves (in seconds)')
    parser.add_argument('-r', '--replay', type=str, default=None, help='Path to log file to replay the game')
    parser.add_argument('-st', '--start_turn', type=int, default=0, help='Start turn for replaying the game')
    parser.add_argument('-n', '--n', type=int, default=1, help='Run N games and report stats')
    args = parser.parse_args()

    if args.replay is not None:
        actions = read_logs(args.replay)
        replay_game(actions, args.delay_time, display=args.display, start_turn=args.start_turn)
    elif args.n > 1:
        winners = {
            0: 0,
            1: 0,
            -1: 0
        }
        total_moves = []
        agent_white, agent_black = get_agents(args, args.display)
        for i in range(0, args.n):
            if i % 25 == 0 and i > 0:
                print(f"{i} -> White : {winners[0] / (i+1)}, Black : {winners[1] / (i+1)}, Draw : {winners[-1] / (i+1)}, mean numer of moves : {sum(total_moves) / len(total_moves)}")
            log_file = args.logs
            winner, n_moves = main(agent_white, agent_black, display=args.display, log_file=log_file)
            winners[winner] += 1
            total_moves.append(n_moves)
            
        print(f" White : {winners[0] / args.n}, Black : {winners[1] / args.n}, Draw : {winners[-1] / args.n}, mean numer of moves : {sum(total_moves) / len(total_moves)}")
    else:
        log_file = args.logs
        agent_white, agent_black = get_agents(args, args.display)

        NB_GAMES = 10
        NB_WHITE_WINS, NB_BLACK_WINS, NB_DRAWS = 0, 0, 0

        for i in range(NB_GAMES):
            winner, n_moves = main(agent_white, agent_black, display=args.display, log_file=log_file, play_time=args.time)
            if winner == 0:
                NB_WHITE_WINS += 1
            elif winner == 1:
                NB_BLACK_WINS += 1
            else:
                NB_DRAWS += 1
        
        PERC_NB_WHITE_WINS = (100 / NB_GAMES) * NB_WHITE_WINS
        PERC_NB_BLACK_WINS = (100 / NB_GAMES) * NB_BLACK_WINS
        PERC_NB_DRAWS = (100 / NB_GAMES) * NB_DRAWS
        percentages = [PERC_NB_WHITE_WINS, PERC_NB_BLACK_WINS, PERC_NB_DRAWS]
        
        createBarGraph(percentages)