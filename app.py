from flask import Flask, render_template, session, redirect, url_for, request
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'number' not in session:
        session['number'] =random.randint(1, 100)
        session['attempts'] = 0
        session['guesses'] = []
    message = None

    if request.method == 'POST':
        guess = int(request.form['guess'])
        session['attempts'] += 1
        session['guesses'].append(guess)

        if guess < session['number']:
            message = "Too low!"
        elif guess > session['number']:
            message = "Too high!"
        else:
            return redirect(url_for('winner'))

        if session['attempts'] >= 5:
            return redirect(url_for('loser'))

    return render_template('index.html', message=message, attempts=session['attempts'])

@app.route('/winner', methods=['GET', 'POST'])
def winner():
    if request.method == 'POST':
        name = request.form['name']
        winners = session.get('winners', [])
        winners.append({'name': name, 'attempts': session['attempts']})
        session['winners'] = winners

        # Clear session data for new game
        session.pop('number', None)
        session.pop('attempts', None)
        session.pop('guesses', None)
        return redirect(url_for('leaderboard'))

    return render_template('winner.html', attempts=session['attempts'])

@app.route('/loser')
def loser(): # Clear session data for new game
    session.pop('number', None)
    session.pop('attempts', None)
    session.pop('guesses', None)
    return render_template('loser.html')

@app.route('/leaderboard')
def leaderboard():    # show name of winners
    winners = session.get('winners', [])
    return render_template('leaderboard.html', winners=winners)

if __name__ == '__main__':
    app.run(debug=True)
