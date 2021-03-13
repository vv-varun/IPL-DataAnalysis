# Define Functions
from google.cloud import datastore
import mysql.connector

client = datastore.Client()

db_connection = mysql.connector.connect(
  host="localhost",
  port=3308,
  user="root",
  passwd="",
  database="ipldata"
)

# Load Player Profile data
def uploadPlayerProfileData(player_data):
    for player in player_data:
        pk = client.key("Players", player['id'])
        pd = client.get(pk)
        pd["id"] = player['id']
        pd["player_name"] = player['player_name']
        pd["bowling_stats"] = {"end_game_stats":{}, "life_time_stats":{}}
        pd["batting_stats"] = {"end_game_stats":{}, "life_time_stats":{}}
        client.put(pd)
    return "Done"

# Read Player Profile data
def readPlayerProfileData():
    my_database = db_connection.cursor()
    sql_statement = "SELECT * FROM players"
    my_database.execute(sql_statement)
    result_set = my_database.fetchall()
    player_list = []
    for player in result_set:
        player_list.append({"id":player[1], "player_name": player[2]})
    return player_list

# Upload Bowler End Game Statistics
def updateBowlingEndGameStatistics(player_stats):
    for stats in player_stats:
        pid = stats['id']
        stats.pop('id', None)
        pk = client.key("Players", pid)
        pd = client.get(pk)
        pd["bowling_stats"]["end_game_stats"] = stats
        client.put(pd)

# Upload Bowler Life time Statistics
def updateBowlingLifeTimeStatistics(player_stats):
    for stats in player_stats:
        pid = stats['id']
        stats.pop('id', None)
        pk = client.key("Players", pid)
        pd = client.get(pk)
        pd["bowling_stats"]["life_time_stats"] = stats
        client.put(pd)

# Upload Batsman End Game Statistics
def updateBatsmanEndGameStatistics(player_stats):
    for stats in player_stats:
        pid = stats['id']
        stats.pop('id', None)
        pk = client.key("Players", pid)
        pd = client.get(pk)
        pd["batting_stats"]["end_game_stats"] = stats
        client.put(pd)

# Upload Batsman Life time Statistics
def updateBatsmanLifeTimeStatistics(player_stats):
    for stats in player_stats:
        pid = stats['id']
        stats.pop('id', None)
        pk = client.key("Players", pid)
        pd = client.get(pk)
        pd["batting_stats"]["life_time_stats"] = stats
        client.put(pd)

# Read End Game Statistics
def readBowlingEndGameStatistics():
    my_database = db_connection.cursor()
    sql_statement = "SELECT * FROM bowler_eg_stats"
    my_database.execute(sql_statement)
    result_set = my_database.fetchall()
    eg_stats = []
    for stats in result_set:
        eg_stats.append({
            "id":stats[0], 
            "innings_played": stats[1],
            "runs": int(stats[2]),
            "balls": int(stats[3]),
            "wickets": int(stats[4]),
            "economy": float(stats[5]),
            "wkt_avg": round(float(6 * stats[4] / stats[3]),4)
        })
    return eg_stats

def readBowlingLifeTimeStatistics():
    my_database = db_connection.cursor()
    sql_statement = "SELECT * FROM bowler_lt_stats"
    my_database.execute(sql_statement)
    result_set = my_database.fetchall()
    lt_stats = []
    for stats in result_set:
        lt_stats.append({
            "id":stats[0], 
            "innings_played": stats[1],
            "runs": int(stats[2]),
            "balls": int(stats[3]),
            "wickets": int(stats[4]),
            "economy": float(stats[5]),
            "wkt_avg": round(float(6 * stats[4] / stats[3]),4)
        })
    return lt_stats

def readBatsmanLifeTimeStatistics():
    my_database = db_connection.cursor()
    sql_statement = "SELECT * FROM batsman_lt_stats"
    my_database.execute(sql_statement)
    result_set = my_database.fetchall()
    lt_stats = []
    for stats in result_set:
        lt_stats.append({
            "id":stats[0], 
            "innings_played": stats[1],
            "runs": int(stats[2]),
            "balls": int(stats[3]),
            "strike_rate": float(stats[4])
        })
    return lt_stats

def readBatsmanEndGameStatistics():
    my_database = db_connection.cursor()
    sql_statement = "SELECT * FROM batsman_eg_stats"
    my_database.execute(sql_statement)
    result_set = my_database.fetchall()
    eg_stats = []
    for stats in result_set:
        eg_stats.append({
            "id":stats[0], 
            "innings_played": stats[1],
            "runs": int(stats[2]),
            "balls": int(stats[3]),
            "strike_rate": float(stats[4])
        })
    return eg_stats

# Load player profile data
#player_data = readPlayerProfileData()
#uploadPlayerProfileData(player_data)

# Load Bowler End Game Statistics
#eg_stats = readBowlingEndGameStatistics()
#updateBowlingEndGameStatistics(eg_stats)

# Load Bowler Life Time Statistics
#lt_stats = readBowlingLifeTimeStatistics()
#updateBowlingLifeTimeStatistics(lt_stats)

# Load Batsman End Game Statistics
#eg_stats = readBatsmanEndGameStatistics()
#updateBatsmanEndGameStatistics(eg_stats)

# Load Batsman Life Time Statistics
lt_stats = readBatsmanLifeTimeStatistics()
updateBatsmanLifeTimeStatistics(lt_stats)