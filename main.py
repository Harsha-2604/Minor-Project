import os
from flask import Flask, render_template, send_from_directory, request, jsonify
from keras.models import model_from_json
import chess
import numpy as np
import operator
import json

app = Flask(__name__)

# Print the current working directory
print("Current Working Directory: ", os.getcwd())

# Load the saved model
model_json_path = os.path.join(os.path.dirname(__file__), 'model.json')
if not os.path.exists(model_json_path):
    raise FileNotFoundError(f"Model JSON file not found at {model_json_path}")

with open(model_json_path, 'r') as json_file:
    loaded_model_json = json_file.read()

loaded_model = model_from_json(loaded_model_json)

model_weights_path = os.path.join(os.path.dirname(__file__), 'model.weights.h5')
if not os.path.exists(model_weights_path):
    raise FileNotFoundError(f"Model weights file not found at {model_weights_path}")

loaded_model.load_weights(model_weights_path)
loaded_model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

# Load generalized moves
generalized_moves_path = os.path.join(os.path.dirname(__file__), 'generalized_moves.json')
if not os.path.exists(generalized_moves_path):
    raise FileNotFoundError(f"Generalized moves file not found at {generalized_moves_path}")

with open(generalized_moves_path, 'r') as json_file:
    generalized_moves = json.load(json_file)

# Initialize state board for model input
state_board = np.zeros((1, 65))
switch = {
    'p': 10,
    'P': -10,
    'q': 90,
    'Q': -90,
    'n': 30,
    'N': -30,
    'r': 50,
    'R': -50,
    'b': 30,
    'B': -30,
    'k': 900,
    'K': -900,
    None: 0
}
squares = chess.SQUARES

@app.route('/')
def index():
    return render_template("reinforced.html")


@app.route('/img/<path:path>')
def send_js(path):
    return send_from_directory('static/img', path)

@app.route('/send_move', methods=['POST'])
def sender_moves():
    # Check if the request contains the necessary data
    if request.method == "POST":
        if 'fen' not in request.json or 'turn' not in request.json:
            return jsonify({"error": "Invalid input"}), 400

        fen = request.json['fen']
        turn = request.json['turn']

        # Validate the FEN string
        try:
            board = chess.Board(fen=fen)
        except ValueError:
            return jsonify({"error": "Invalid FEN string"}), 400

        # Determine whose turn it is
        board.turn = (turn != "b")  # True for White's turn, False for Black's

        Q = {}
        mult = 1 if board.turn else -1
        
        # Update the state_board for the current board position
        for a, i in enumerate(squares):
            piece = board.piece_at(i)
            state_board[0][a] = mult * switch[str(piece)] if piece else 0

        # Predict the value for each legal move
        for move in board.legal_moves:
            move_str = str(move)
            if move_str not in generalized_moves:
                continue  # Skip invalid moves

            state_board[0][64] = generalized_moves[move_str]  # Update the last index with the generalized move
            Q[move_str] = loaded_model.predict(state_board)  # Get the predicted value

        if not Q:
            return jsonify({"error": "No legal moves available"}), 400  # No moves predicted

        # Find the best move based on predicted values
        best_move = max(Q.items(), key=operator.itemgetter(1))[0]
        return jsonify({"best_move": best_move}), 200  # Respond with the best move

if __name__ == '__main__':
    app.run(debug=True)
