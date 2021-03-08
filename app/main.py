# Copyright 2020 Varun Verma
#


from flask import Flask, render_template, request
from app_functions import predict_match_result

app = Flask(__name__)


@app.route('/')
def root():

    return render_template(
        'index.html')


@app.route('/match_predict_final_over', methods = ['GET','POST'])
def match_predict_final_over():
    
    innings_1_score = request.form['innings_1_score']
    runs_to_win = request.form['runs_to_win']
    wickets_in_hand = request.form['wickets_in_hand']
    bowler_econ = request.form['bowler_econ']
    bowler_boundaries = request.form['bowler_boundaries']
    batsman_sr = request.form['batsman_sr']
    boundaries = request.form['boundaries']
    testdata = {
        'innings_1_score': innings_1_score,
        'runs_to_win': runs_to_win,
        'RPB': int(runs_to_win) // 6,
        'wickets_in_hand': wickets_in_hand,
        'bowler_econ': bowler_econ,
        'bowler_boundaries': bowler_boundaries,
        'batsman_sr': batsman_sr,
        'boundaries': boundaries
        }
    #print(testdata)
    result = predict_match_result(testdata)
    return result


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='localhost', port=8080, debug=True)
