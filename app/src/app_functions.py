from joblib import load
import pandas as pd;
from google.cloud import datastore
from os import path

def predict_match_result(input_data):
    # Get the bowler statistics.
    bo_stats = get_bowler_stats(input_data['bowler'])
    ba_stats = get_batsman_stats(input_data['batsman'])
    ns_stats = get_batsman_stats(input_data['non_striker'])
    
    # Right now our prediction is based on the V2 Model.
    testinput = {
        "runs_to_win": input_data["runs_to_win"],
        "wickets_in_hand": input_data["wickets_in_hand"],
        "bowler_eg_economy": bo_stats["end_game_stats"]["economy"],
        "batsman_eg_sr": ba_stats["end_game_stats"]["strike_rate"],
        "non_striker_eg_sr": ns_stats["end_game_stats"]["strike_rate"]
    }
    mymodel = load(path.dirname(__file__) + '/../ml_model.joblib')
    tdf = pd.DataFrame([testinput])
    test_results = mymodel.predict_proba(tdf)
    if test_results[0][1] <= 0.5:
        result = "Lost"
    else:
        result = "Win"
    
    return {"result":result,"win_probability":int(100 * test_results[0][1])}

def get_bowler_stats(bowler_name):
    client = datastore.Client()
    query = client.query(kind="Players")
    query.add_filter("player_name", "=", bowler_name)
    players = list(query.fetch())
    stats = players[0]["bowling_stats"]
    return stats

def get_batsman_stats(batsman_name):
    client = datastore.Client()
    query = client.query(kind="Players")
    query.add_filter("player_name", "=", batsman_name)
    players = list(query.fetch())
    stats = stats = players[0]["batting_stats"]
    return stats