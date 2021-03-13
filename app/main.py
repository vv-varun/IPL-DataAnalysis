# Copyright 2020 Varun Verma
#


from flask import Flask, render_template, request, jsonify
from src.app_functions import predict_match_result
from google.cloud import datastore

app = Flask(__name__)
client = datastore.Client()


@app.route('/')
def root():

    return render_template(
        'index.html')


@app.route('/predictMatchResult', methods = ['POST'])
def match_predict_final_over():
    input_data = request.json
    prediction_result = predict_match_result(input_data)
    return jsonify(prediction_result)


# API To get Player details
@app.route('/players', methods = ['GET'])
def getPlayerNames():
    query = client.query(kind="Players")
    query.projection = ["player_name"]
    players = list(query.fetch())
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
