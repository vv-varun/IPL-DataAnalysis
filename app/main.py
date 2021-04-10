# Copyright 2020 Varun Verma
#


from flask import Flask, render_template, request, jsonify
from src.app_functions import predict_match_result
from src.app_functions import update_team_assignment
from src.app_functions import current_match_prediction
from google.cloud import datastore

app = Flask(__name__)
client = datastore.Client()


@app.route('/')
def root():
    return render_template('index.html')

@app.route('/test/')
def localTest():
    return render_template('test.html')

@app.route('/predictMatchResult', methods = ['POST'])
def match_predict_final_over():
    input_data = request.json
    prediction_result = predict_match_result(input_data)
    return jsonify(prediction_result)

@app.route('/currentMatchPrediction', methods = ['POST'])
def currentMatchPrediction():
    input_data = request.json
    prediction_result = current_match_prediction(input_data)
    return jsonify(prediction_result)

@app.route('/test/updateTeamAssignments', methods = ['POST'])
def updateTeamAssignments():
    input_data = request.json
    update_result = update_team_assignment(input_data)
    return jsonify(update_result)

# API To get Player details
@app.route('/players', methods = ['GET'])
def getPlayerNames():
    query = client.query(kind="Players")
    query.projection = ["player_name"]
    players = list(query.fetch())
    return jsonify(players)

# API To get Team details
@app.route('/teams', methods = ['GET'])
def getTeamNames():
    query = client.query(kind="Teams")
    query.projection = ["team_name"]
    teams = list(query.fetch())
    return jsonify(teams)

# API To get Current Match details
@app.route('/currentMatchPlayers/<team_type>', methods = ['GET'])
def getCurrentMatchPlayers(team_type):
    query = client.query(kind="Matches")
    query.add_filter("active", "=", True)
    match = list(query.fetch())[0]

    if team_type == 'bowling':
        query = client.query(kind="Teams")
        query.add_filter("team_name", "=", match['innings']['innings2']['bowling_team'])
        t1players = list(query.fetch())[0]['players']
        return jsonify(t1players)
    elif team_type == 'batting':
        query = client.query(kind="Teams")
        query.add_filter("team_name", "=", match['innings']['innings2']['batting_team'])
        t2players = list(query.fetch())[0]['players']
        return jsonify(t2players)
    else:
        query = client.query(kind="Teams")
        query.add_filter("team_name", "=", match['team1'])
        t1players = list(query.fetch())[0]['players']

        query = client.query(kind="Teams")
        query.add_filter("team_name", "=", match['team2'])
        t2players = list(query.fetch())[0]['players']
        
        players = []
        players.extend(t1players)
        players.extend(t2players)
        return jsonify(players)

    return jsonify(players)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='localhost', port=8080, debug=True)
