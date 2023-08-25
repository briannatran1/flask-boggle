from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})


@app.post('/api/score-word')
def score_word():
    """Checks if word is in word list and can be found on game board"""
    #api/score-word should receive JSON data containing the word.
    data = request.json #word
    word = data.get("word") #key needed
    game_id = data.get("gameId")

    if games[game_id].is_word_in_word_list(word):
        if games[game_id].check_word_on_board(word):
            return jsonify({"result": "ok"})

        elif not games[game_id].check_word_on_board(word):
            return jsonify({"result": "not-on-board"})
    else:
        return jsonify({"result": "not-word"})
