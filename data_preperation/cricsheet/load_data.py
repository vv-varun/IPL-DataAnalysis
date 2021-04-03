import mysql.connector
import yaml
from os import path, listdir
import shutil
import datetime

db_connection = mysql.connector.connect(
  host="localhost",
  port=3308,
  user="root",
  passwd="",
  database="ipldata"
)

# Global Variable
player_data = {}

# Query Team details by name
def queryTeamDetailsByName(team_name):
    my_database = db_connection.cursor()
    sql_statement = "SELECT * FROM teams WHERE Team_Name = '" + team_name + "'"
    my_database.execute(sql_statement)
    result_set = my_database.fetchall()
    for team in result_set:
        team_details = {"id":team[1], "team_name": team[2]}
    return team_details

# Add new player to DB.
def addPlayer(player_name):
    # Here we assume that the player does not exist.
    # To keep it safe - lets add a unique index on Player name
    my_database = db_connection.cursor()
    sql_statement = "SELECT max(Player_Id) as C FROM players"
    my_database.execute(sql_statement)
    result_set = my_database.fetchall()
    id = result_set[0][0] + 1

    # Now insert.
    sql_statement = "INSERT INTO players (PLAYER_SK, Player_Id, Player_Name) VALUES (%s, %s, %s)"
    values = (id,id,player_name)
    my_database.execute(sql_statement, values)
    db_connection.commit()
    return {"id":id, "player_name": player_name}

# Get Player details by name
def getPlayerDetailsByName(player_name):
    
    if player_name == '': return {"id":"","player_name":player_name}

    if player_name in player_data:
        return player_data[player_name]
    else:
        my_database = db_connection.cursor()
        sql_statement = "SELECT * FROM players WHERE Player_Name = '" + player_name + "'"
        my_database.execute(sql_statement)
        result_set = my_database.fetchall()
        if len(result_set) > 0:
            # We found entry
            for player in result_set:
                player_details = {"id":player[1], "player_name": player[2]}
                player_data[player_name] = player_details
                #print("Read " + player_name + " from DB")
        else:
            # This is a new player ! Create entry.
            player_details = addPlayer(player_name)
            player_data[player_name] = player_details
        
        return player_data[player_name]

# Read data from YAML file
def readDataFromFile(filename):
    # Get the filename without extension to extract the match id
    match_id = path.splitext(filename)[0]
    # Open YAML file and load data
    file = path.dirname(__file__) + '/to_load/' + filename
    with open(file, 'r') as stream:
        try:
            match_data = yaml.safe_load(stream)
            match_data['info']['match_id'] = match_id
        except yaml.YAMLError as exc:
            print(exc)   
    return match_data

# Read files from folders
def readFilesInFolder():
    return listdir(path.dirname(__file__) + "/to_load")

# Upload data into MySQL DB
def parseAndUploadDataToDB(match_data):
    # Prepare match info.
    match_info = {}
    ball_details = []
    
    match_info['Match_SK'] = match_info['match_id'] = match_data['info']['match_id']
    match_info['Team1'] = match_data['info']['teams'][0]
    match_info['Team2'] = match_data['info']['teams'][1]
    match_info['match_date_str'] = match_data['info']['dates'][0]
    match_info['match_date'] = datetime.datetime.strptime(match_data['info']['dates'][0], "%Y-%m-%d").date()
    match_info['Season_Year'] = match_info['match_date'].year
    match_info['Venue_Name'] = match_data['info']['venue']
    match_info['City_Name'] = match_data['info'].get('city','')
    match_info['Country_Name'] = ''
    match_info['Toss_Winner'] = match_data['info']['toss']['winner']
    match_info['Toss_Name'] = match_data['info']['toss']['decision']

    if 'winner' in match_data['info']['outcome'].keys():
        match_info['Outcome_Type'] = 'Result'
        match_info['match_winner'] = match_data['info']['outcome']['winner']
        match_info['Win_Type'] = list(match_data['info']['outcome']['by'].keys())[0]
        match_info['Win_Margin'] = list(match_data['info']['outcome']['by'].values())[0]
    else:
        match_info['Outcome_Type'] = match_data['info']['outcome']['result']
        match_info['match_winner'] = ''
        match_info['Win_Type'] = ''
        match_info['Win_Margin'] = ''
    
    if 'player_of_match' in match_data['info'].keys():
        match_info['ManOfMach'] = match_data['info']['player_of_match'][0]
    else:
        match_info['ManOfMach'] = ''
    
    match_info['Country_id'] = ''
    #print(match_info)

    first_innings_data = match_data['innings'][0]['1st innings']
    fi_team = queryTeamDetailsByName(first_innings_data['team'])
    
    second_innings_data = match_data['innings'][1]['2nd innings']
    si_team = queryTeamDetailsByName(second_innings_data['team'])
    
    #Parse 1st innings
    first_innings = parseInningsData(first_innings_data)
    for bd in first_innings: 
        bd['match_id'] = match_info['match_id']
        bd['innings_no'] = 1
        bd['Team_Batting'] = fi_team['id']
        bd['Team_Bowling'] = si_team['id']
    
    # Put all details in a list for Update
    ball_details.extend(first_innings)

    #Parse 2nd Innings
    second_innings = parseInningsData(second_innings_data)
    for bd in second_innings: 
        bd['match_id'] = match_info['match_id']
        bd['innings_no'] = 2
        bd['Team_Batting'] = si_team['id']
        bd['Team_Bowling'] = fi_team['id']
    
    # Put all details in a list for Update
    ball_details.extend(second_innings)

    #May be there are super overs !
    if len(match_data['innings']) > 2:
        # More than 2 innings ! - Super Over!
        so_first_innings_data = list(match_data['innings'][2].values())[0]
        so_fi_team = queryTeamDetailsByName(so_first_innings_data['team'])

        so_second_innings_data = list(match_data['innings'][3].values())[0]
        so_si_team = queryTeamDetailsByName(so_second_innings_data['team'])

        so_first_innings = parseInningsData(so_first_innings_data)
        for bd in so_first_innings:
            bd['match_id'] = match_info['match_id']
            bd['innings_no'] = 3
            bd['Team_Batting'] = so_fi_team['id']
            bd['Team_Bowling'] = so_si_team['id']
        
        ball_details.extend(so_first_innings)
        
        so_second_innings = parseInningsData(so_second_innings_data)
        for bd in so_second_innings: 
            bd['match_id'] = match_info['match_id']
            bd['innings_no'] = 4
            bd['Team_Batting'] = si_team['id']
            bd['Team_Bowling'] = fi_team['id']
        
        ball_details.extend(so_first_innings)

    # Now update all in a transaction
    uploadDataToDB(match_info, ball_details)
    
    # Print Random for testing
    #print(first_innings[20])
    #print(first_innings[12])
    #print(second_innings[20])
    #print(second_innings[7])
    
    return

# Parse Innings data
def parseInningsData(innings_data):
    ball_data = []
    bowler_wicket_list = ['caught','bowled','lbw','stumped','caught and bowled']
    for delivery in innings_data['deliveries']:
        ball_no = str(list(delivery.keys())[0])
        ball_details = list(delivery.values())[0]

        wicket = ball_details.get('wicket', {'player_out':'','kind':'Not Applicable'})
        wicket_kind = wicket.get('kind','')
        if wicket_kind in bowler_wicket_list:
            wicket['Bowler_Wicket'] = 1
        else:
            wicket['Bowler_Wicket'] = 0

        extras = ball_details.get('extras', {})
        if (len(extras) > 0): extra_type = list(extras.keys())[0]
        else: extra_type = ''
        wides = extras.get('wides',0)
        legbyes = extras.get('legbyes',0)
        noballs = extras.get('noballs',0)
        byes = extras.get('byes',0)
        bowler_extras = wides + noballs

        ball_data.append({
            'match_id': '',
            'over_id': ball_no.split(".")[0],
            'ball_id': ball_no.split(".")[1],
            'innings_no': '',
            'Team_Batting': '',
            'Team_Bowling': '',
            'Striker_Batting_Position': '',
            'Extra_Type': extra_type,
            'Runs_Scored': ball_details['runs']['batsman'],
            'Extra_runs': ball_details['runs']['extras'],
            'Wides': wides,
            'Legbyes': legbyes,
            'Byes': byes,
            'Noballs': noballs,
            'Penalty': '',
            'Bowler_Extras': bowler_extras,
            'Out_type': wicket['kind'],
            'Caught': 1 if wicket_kind == 'caught' else 0,
            'Bowled': 1 if wicket_kind == 'bowled' else 0,
            'Run_out': 1 if wicket_kind == 'run out' else 0,
            'LBW': 1 if wicket_kind == 'lbw' else 0,
            'Retired_hurt': 1 if wicket_kind == 'retired hurt' else 0,
            'Stumped': 1 if wicket_kind == 'stumped' else 0,
            'caught_and_bowled': 1 if wicket_kind == 'caught and bowled' else 0,
            'hit_wicket': 1 if wicket_kind == 'hit wicket' else 0,
            'ObstructingFeild': 1 if wicket_kind == 'obstructing the field' else 0,
            'Bowler_Wicket': wicket['Bowler_Wicket'],
            'Striker': getPlayerDetailsByName(ball_details['batsman'])['id'],
            'Non_Striker': getPlayerDetailsByName(ball_details['non_striker'])['id'],
            'Bowler': getPlayerDetailsByName(ball_details['bowler'])['id'],
            'Player_Out': getPlayerDetailsByName(wicket['player_out'])['id'],
            'Fielders': '',
            'Keeper_Catch': ''
        })
    
    #print(ball_data)
    return ball_data

def uploadDataToDB(match_info, ball_details):
    my_database = db_connection.cursor()
    db_connection.start_transaction()

    # Insert Match Info
    sql_statement = "INSERT INTO matches VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values = tuple(list(match_info.values()))
    my_database.execute(sql_statement, values)

    sql_statement = "INSERT INTO balldetails VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for bd in ball_details:
        values = tuple(list(bd.values()))
        my_database.execute(sql_statement, values)

    # Insert Ball Details
    db_connection.commit()

######  Main Program    ######
# Read files to load from directory
files = readFilesInFolder()

# Read Data from the file.
for file in files:
    print("Processing file: " + file)
    match_data = readDataFromFile(file)
    #print(match_data['info'])
    # Upload into DB
    parseAndUploadDataToDB(match_data)
    shutil.move(path.dirname(__file__) + "/to_load/" + file, path.dirname(__file__) + "/done/" + file)

print("I'm done here !")