import datetime
import pandas as pd


# Define API KEY
RAPIDAPI_KEY = "832cc5fef8mshf0dfd8a2c357840p1a6b87jsnc5253dfa2ef4"
    
# Set up request header and authentication
headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
    }
# Setup API URL and parameters
url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
params = {"league":"39","season":"2023"}
def process_top_scorers(data):
    """
    Parse the JSON data required for the top scorers 
    """
    top_scorers = []
    for scorer_data in data['response']:
        statistics = scorer_data['statistics'][0]

        # Set up constants for processing data 
        player = scorer_data['player']
        player_name = player['name']
        club_name = statistics['team']['name']
        total_goals = int(statistics['goals']['total'])
        penalty_goals = int(statistics['penalty']['scored'])
        assists = int(statistics['goals']['assists']) if statistics['goals']['assists'] else 0
        matches_played = int(statistics['games']['appearences'])
        minutes_played = int(statistics['games']['minutes'])
        #dob = datetime.strptime(player['birth']['date'], '%Y-%m-%d')
        #age = (datetime.now() - dob).days // 365

        # Append data 
        top_scorers.append({
            'player': player_name,
            'club': club_name,
            'total_goals': total_goals,
            'penalty_goals': penalty_goals,
            'assists': assists,
            'matches': matches_played,
            'mins': minutes_played
        })
    return top_scorers

def create_dataframe(top_scorers):

    """
    Convert list of dictionaries into a Pandas dataframe and process it
    """

    df = pd.DataFrame(top_scorers)

    # Sort dataframe first by 'total_goals' in descending order, then by 'assists
    df.sort_values(by=['total_goals','assists'],ascending=[False,False], inplace=True)

    # Reset index after sorting to reflect new order
    df.reset_index(drop=True, inplace=True)

    # recalculate rank based on the sorting order
    df['position'] = df['total_goals'].rank(method='dense',ascending=False).astype(int)

    # select the required columns to write to into final table
    df = df[['position','player','club','total_goals','penalty_goals','assists','matches','mins']]

    return df




#data = get_top_scorer(url,headers,params)
#players = process_top_scorers(data)
#print(players)




