import chess
import random
import json
import operator
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
import argparse
import os

# Create the neural network. Input is the chess board state and output is the Q-values for the possible moves.
model = Sequential()
model.add(Dense(20, input_shape=(65,), kernel_initializer='uniform', activation='relu'))
model.add(Dense(18, kernel_initializer='uniform', activation='relu'))
model.add(Dense(18, kernel_initializer='uniform', activation='relu'))
model.add(Dense(18, kernel_initializer='uniform', activation='relu'))
model.add(Dense(18, kernel_initializer='uniform', activation='relu'))
model.add(Dense(10, kernel_initializer='uniform', activation='relu'))
model.add(Dense(10, kernel_initializer='uniform', activation='relu'))
model.add(Dense(1, kernel_initializer='uniform', activation='linear'))  # Change activation to 'linear' for output
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

np.set_printoptions(threshold=np.inf)

state_board = np.zeros((1, 65))  # The array representing the board of 8x8 plus a move from possible ones

# Value of every piece
switch = {
    'p': 10, 'P': -10, 'q': 90, 'Q': -90, 'n': 30, 'N': -30,
    'r': 50, 'R': -50, 'b': 30, 'B': -30, 'k': 900, 'K': -900, 'None': 0
}

# Command-line argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--number_of_games', type=int, default=100)  # Changed to int
parser.add_argument('--winner_reward', type=float, default=1)
parser.add_argument('--loser_malus', type=float, default=-1)
parser.add_argument('--epsilon', type=float, default=1)
parser.add_argument('--decremental_epsilon', type=float, default=0.0001)
parser.add_argument('--gamma', type=float, default=0.05)
args = parser.parse_args()

# Assigning parameters from the arguments
arguments = {
    'training_games': args.number_of_games,
    'winner_reward': args.winner_reward,
    'loser_malus': args.loser_malus,
    'epsilon': args.epsilon,
    'decremental_epsilon': args.decremental_epsilon,
    'gamma': args.gamma
}

general_moves = {}

# Training parameters
steps = 1000
training_games = arguments['training_games']
winner_reward = arguments['winner_reward']
loser_malus = arguments['loser_malus']
epsilon = arguments['epsilon']
decremental_epsilon = 1 / training_games
gamma = arguments['gamma']  # Discounted future reward

print("Training the Deep-Q-Network with parameters:")
print(f"Number of training games: {training_games}")
print(f"Winner Reward: {winner_reward}")
print(f"Loser Malus: {loser_malus}")
print(f"Epsilon: {epsilon}")
print(f"Decremental Epsilon: {decremental_epsilon}")
print(f"Gamma: {gamma}")

def evaluate_board(turn, board):  # Evaluate the board following the value of each piece
    total = 0
    mult = 1 if turn else -1
    for a in chess.SQUARES:
        piece_value = mult * switch[str(board.piece_at(a))]
        state_board[0][a] = piece_value  # Update the state_board variable used for predictions
        total += piece_value
    return total

def get_int(move):  # Get the integer representation of the move for input to the DNN
    if str(move) not in general_moves:
        general_moves[str(move)] = len(general_moves)
    return general_moves[str(move)]

def reward(fen_history, moves, lose_fen, lose_moves):  # Final reward at the end of the game
    for i, (fen, move) in enumerate(zip(fen_history, moves)):
        fen[0][64] = get_int(move)
        model.train_on_batch(np.array(fen), model.predict(np.array(fen)) + winner_reward * (1 / len(fen_history)) * i)

    for i, (fen, move) in enumerate(zip(lose_fen, lose_moves)):
        fen[0][64] = get_int(move)
        model.train_on_batch(np.array(fen), model.predict(np.array(fen)) + loser_malus * (1 / len(lose_fen)) * i)

winners = {}  # Variable to count the number of wins of each player

# Main training loop
for joum in range(steps):
    i = 0
    all_number_of_moves = []
    board = chess.Board()
    epsilon = arguments['epsilon']

    while i < training_games:
        print("\n" * 50)  # Clear the console output
        print(f"/--- Training Step {joum}/{steps} ---/")
        print(f"Game N° {i}")
        print(f"WINNERS COUNT: \n{winners}")
        print(f"Number of remaining training games: {training_games - i}")
        fen_history = []
        black_moves = []
        white_moves = []
        black_fen_history = []
        white_fen_history = []
        number_of_moves = 0

        while not board.is_game_over():
            number_of_moves += 1
            if np.random.rand() <= epsilon:
                god_damn_move = random.choice(list(board.legal_moves))  # Random move
            else:
                evaluate_board(board.turn, board)  # Pass board to evaluate_board
                Q = {}
                for kr in board.legal_moves:
                    br = get_int(kr)
                    state_board[0][64] = br
                    Q[kr] = model.predict(np.array(state_board))  # Q-values prediction
                god_damn_move = max(Q.items(), key=operator.itemgetter(1))[0]  # Get move with the highest Q-value

            fen_history.append(np.array(state_board, copy=True))
            if board.turn:
                white_moves.append(god_damn_move)
                white_fen_history.append(np.array(state_board, copy=True))
            else:
                black_moves.append(god_damn_move)
                black_fen_history.append(np.array(state_board, copy=True))
            board.push(chess.Move.from_uci(str(god_damn_move)))

        all_number_of_moves.append(number_of_moves)
        i += 1

        if board.result() == "1-0":
            reward(white_fen_history, white_moves, black_fen_history, black_moves)
        elif board.result() == "0-1":
            reward(black_fen_history, black_moves, white_fen_history, white_moves)
        elif board.result() == "1/2-1/2":  # Handle draws
            continue  # You can add handling for draws if needed

        winners[str(board.result())] = winners.get(str(board.result()), 0) + 1
        board.reset()
        epsilon = max(0.01, epsilon - decremental_epsilon)  # Set a minimum epsilon

print(f"WINNERS COUNT:\n{winners}")

# Save the mapping Move/Index to be used in the future
with open('generalized_moves.json', 'w') as fp:
    json.dump(general_moves, fp)

# Save the model architecture and weights
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model.weights.h5")
