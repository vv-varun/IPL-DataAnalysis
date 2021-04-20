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
        result = "Won"
    
    return {"result":result,"win_probability":int(100 * test_results[0][1]),"loose_probability":int(100 * test_results[0][0])}

def current_match_prediction(input_data):
    ba_stats = get_batsman_stats(input_data['cm_batsman'])
    ns_stats = get_batsman_stats(input_data['cm_non_striker'])

    match = get_current_match()
    players = get_team_players(match['innings']['innings2']['bowling_team'])
    testinputlist = []
    for player in players:
        bo_stats = get_bowler_stats(player)
        testinput = {
            "runs_to_win": input_data["runs_to_win"],
            "wickets_in_hand": input_data["wickets_in_hand"],
            "bowler_eg_economy": bo_stats["end_game_stats"]["economy"],
            "batsman_eg_sr": ba_stats["end_game_stats"]["strike_rate"],
            "non_striker_eg_sr": ns_stats["end_game_stats"]["strike_rate"]
        }
        testinputlist.append(testinput)
    
    mymodel = load(path.dirname(__file__) + '/../ml_model.joblib')
    tdf = pd.DataFrame(testinputlist)
    test_results = mymodel.predict_proba(tdf)
    prdiction_result = []
    #print(test_results)
    index = 0
    for player in players:
        testresult = test_results[index]
        if testresult[1] <= 0.5:
            mr = "Lost"
        else:
            mr = "Won"
        
        pr = {"player": player,"result":mr,"win_probability":int(100 * testresult[1])}
        prdiction_result.append(pr)
        index = index + 1
    
    return prdiction_result

def get_bowler_stats(bowler_name):
    client = datastore.Client()
    query = client.query(kind="Players")
    query.add_filter("player_name", "=", bowler_name)
    players = list(query.fetch())
    stats = players[0]["bowling_stats"]
    if 'end_game_stats' not in stats.keys():
        stats['end_game_stats'] = {"economy": 10}
    else:
        if 'economy' not in stats['end_game_stats'].keys():
            stats['end_game_stats']['economy'] = 10
    return stats

def get_batsman_stats(batsman_name):
    client = datastore.Client()
    query = client.query(kind="Players")
    query.add_filter("player_name", "=", batsman_name)
    players = list(query.fetch())
    stats = players[0]["batting_stats"]
    if 'end_game_stats' not in stats.keys():
        stats['end_game_stats'] = {"strike_rate": 100}
    else:
        if 'strike_rate' not in stats['end_game_stats'].keys():
            stats['end_game_stats']['strike_rate'] = 100
    return stats

def update_team_assignment(input_data):
    client = datastore.Client()
    tquery = client.query(kind="Teams")
    tquery.add_filter("team_name", "=", input_data['team'])
    team = list(tquery.fetch())[0]
    
    pquery = client.query(kind="Players")
    pquery.add_filter("player_name", "=", input_data['player'])
    player = list(pquery.fetch())[0]

    if 'players' in team.keys():
        if player['player_name'] not in team['players']:
            team['players'].append(player['player_name'])
        else:
            return "Player already in team"
    else:
        team['players'] = [player['player_name']]
    client.put(team)
    return "Player added in team"

def get_team_players(team_name):
    client = datastore.Client()
    query = client.query(kind="Teams")
    query.add_filter("team_name", "=", team_name)
    team = list(query.fetch())[0]
    players = team["players"]
    return players

def get_current_match():
    client = datastore.Client()
    query = client.query(kind="Matches")
    query.add_filter("active", "=", True)
    match = list(query.fetch())[0]
    return match

def update_match_details(input_data):
    client = datastore.Client()
    pk = client.key("Matches", input_data['matchid'])
    md = client.get(pk)

    innings_details = {
        'innings1': {
            'bowling_team': input_data['team2'],
            'batting_team': input_data['team1']
        },
        'innings2': {
            'bowling_team': input_data['team1'],
            'batting_team': input_data['team2']
        }
    }
    
    # always set other matches as inactive
    if input_data['isActiveMatch'] == 'true':
        set_other_matches_inactive()

    if not md is None:
        md["innings"] = innings_details
        md["active"] = input_data['isActiveMatch']
        client.put(md)

    else:
        md = datastore.Entity(key=pk)
        md['team1'] = input_data['team1']
        md['team2'] = input_data['team2']
        md["innings"] = innings_details
        md["active"] = input_data['isActiveMatch']
        client.put(md)
    
    return "Player added in team"

def set_other_matches_inactive():
    print('In function')
    client = datastore.Client()
    query = client.query(kind="Matches")
    query.add_filter("active", "=", 'true')
    matches = list(query.fetch())
    for match in matches:
        print(match['active'])
        match['active'] = 'false'
        client.put(match)
    
def update_final_over_details(input_data):
    client = datastore.Client()
    pk = client.key("Matches", input_data['matchid'])
    md = client.get(pk)
    final_over_details = {
        'batsman': input_data['batsman'],
        'non_striker': input_data['non_striker'],
        'bowler': input_data['bowler'],
        'runs_to_win': input_data['runs_to_win'],
        'wickets_in_hand': input_data['wickets_in_hand']
    }
    match_result = {
        'actual_result': input_data['result'],
        'predicted_result': '',
        'confidence': '',
        'win_probability': '',
        'loose_probability': ''
    }
    md["final_over"] = final_over_details
    md["match_result"] = match_result
    client.put(md)
    return "Result updated"

def update_predicted_result(match_id):
    client = datastore.Client()
    if match_id == 'all':
        query = client.query(kind="Matches")
        match_list = list(query.fetch())
    else:
        pk = client.key("Matches", match_id)
        md = client.get(pk)
        match_list = [md]
    
    for match in match_list:
        if not 'final_over' in match.keys():
            continue

        input_data = {
            'bowler': match['final_over']['bowler'],
            'batsman': match['final_over']['batsman'],
            'non_striker': match['final_over']['non_striker'],
            'runs_to_win': match['final_over']['runs_to_win'],
            'wickets_in_hand': match['final_over']['wickets_in_hand']
        }
        prediction_result = predict_match_result(input_data)
        match['match_result']['predicted_result'] = prediction_result['result']
        match['match_result']['win_probability'] = prediction_result['win_probability']
        match['match_result']['loose_probability'] = prediction_result['loose_probability']
        if prediction_result['result'] == 'Lost':
            match['match_result']['confidence'] = prediction_result['loose_probability']
        else:
            match['match_result']['confidence'] = prediction_result['win_probability']
        client.put(match)
        
    return