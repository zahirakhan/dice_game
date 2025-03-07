from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "secret123"

MAX_ROLLS = 10  # Kitne rolls tak game chalega
DICE_IMAGES = {
    1: "🎲 1",
    2: "🎲 2",
    3: "🎲 3",
    4: "🎲 4",
    5: "🎲 5",
    6: "🎲 6"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    session['player1_name'] = request.form['player1']
    session['player2_name'] = request.form['player2']
    session['player1_score'] = 0
    session['player2_score'] = 0
    session['turn'] = "player1"
    session['roll_count'] = 0
    return jsonify({"success": True})

@app.route('/roll')
def roll():
    if session['roll_count'] >= MAX_ROLLS:
        return jsonify({"winner": get_winner()})

    roll_value = random.randint(1, 6)
    dice_image = DICE_IMAGES[roll_value]
    current_player = session['turn']
    session['roll_count'] += 1

    if current_player == "player1":
        session['player1_score'] += roll_value
        session['turn'] = "player2"
    else:
        session['player2_score'] += roll_value
        session['turn'] = "player1"

    return jsonify({
        "dice": dice_image,
        "player1_score": session['player1_score'],
        "player2_score": session['player2_score'],
        "turn": session['turn'],
        "player1_name": session['player1_name'],
        "player2_name": session['player2_name'],
        "rolls_left": MAX_ROLLS - session['roll_count']
    })

def get_winner():
    if session['player1_score'] > session['player2_score']:
        return f"{session['player1_name']} Wins! 🏆"
    elif session['player2_score'] > session['player1_score']:
        return f"{session['player2_name']} Wins! 🏆"
    else:
        return "It's a Tie! 🎲"

if __name__ == "__main__":
    app.run(debug=True)
