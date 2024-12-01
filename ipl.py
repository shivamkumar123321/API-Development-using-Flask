import pandas as pd
import numpy as np

ipl_matches = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRy2DUdUbaKx_Co9F0FSnIlyS-8kp4aKv_I0-qzNeghiZHAI_hw94gKG22XTxNJHMFnFVKsO4xWOdIs/pub?gid=1655759976&single=true&output=csv"
matches = pd.read_csv(ipl_matches)

print(matches.head())

def teamsAPI():
    teams = list(set(list(matches['Team1']) + list(matches['Team2'])))
    team_dict = {
        'teams':teams
    }

    return team_dict

def teamVteamAPI(team1,team2):

    valid_teams = list(set(list(matches['Team1']) + list(matches['Team2'])))

    if team1 in valid_teams and team2 in valid_teams:

        temp_df = matches[(matches['Team1'] == team1) & (matches['Team2'] == team2) | (matches['Team1'] == team2) & (matches['Team2'] == team1)]
        total_matches = temp_df.shape[0]

        matches_won_team1 = temp_df['WinningTeam'].value_counts()[team1]
        matches_won_team2 = temp_df['WinningTeam'].value_counts()[team2]

        draws = total_matches - (matches_won_team1 + matches_won_team2)

        response = {
              'total_matches': str(total_matches),
              team1: str(matches_won_team1),
              team2: str(matches_won_team2),
              'draws': str(draws)
          }

        return response
    else:
        return {'message':'invalid team name'}


def batsmanRecord(batsman):
    ipl_ball = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRu6cb6Pj8C9elJc5ubswjVTObommsITlNsFy5X0EiBY7S-lsHEUqx3g_M16r50Ytjc0XQCdGDyzE_Y/pub?output=csv"
    balls = pd.read_csv(ipl_ball)


    # Ensure dataframe is not empty
    if balls.empty:
        return np.nan

    # Filter records where the batsman is involved
    df = balls[balls['batter'] == batsman]

    # If no records for the batsman, return default stats
    if df.empty:
        return {
            'innings': 0,
            'runs': 0,
            'fours': 0,
            'sixes': 0,
            'avg': 0,
            'strikeRate': 0,
            'fifties': 0,
            'hundreds': 0,
            'highestScore': 0,
            'notOut': 0,
        }

    # Count number of times the batsman got out
    out = balls[balls['player_out'] == batsman].shape[0]

    # Number of innings played
    innings = df['ID'].nunique()

    # Total runs scored
    runs = df['batsman_run'].sum()

    # Count boundaries
    fours = df[(df['batsman_run'] == 4) & (df['non_boundary'] == 0)].shape[0]
    sixes = df[(df['batsman_run'] == 6) & (df['non_boundary'] == 0)].shape[0]

    # Calculate batting average
    avg = runs / out if out > 0 else np.inf

    # Calculate strike rate
    nballs = df[df['extra_type'] != 'wides'].shape[0]
    strike_rate = (runs / nballs) * 100 if nballs > 0 else 0

    # Group data by innings to calculate milestones
    gb = df.groupby('ID').sum()
    fifties = gb[(gb['batsman_run'] >= 50) & (gb['batsman_run'] < 100)].shape[0]
    hundreds = gb[gb['batsman_run'] >= 100].shape[0]

    # Calculate the highest score
    if not gb.empty:
        highest_score = gb['batsman_run'].max()
        highest_innings = gb['batsman_run'].idxmax()
        if balls[(balls['ID'] == highest_innings) & (balls['player_out'] == batsman)].empty:
            highest_score = f"{highest_score}*"
    else:
        highest_score = 0

    # Calculate not-out innings
    not_out = innings - out

    # Count Player of the Match awards
    # mom = balls[balls['Player_of_Match'] == batsman]['ID'].nunique()

    # Create and return the data dictionary
    response = {
        'innings': str(innings),
        'runs': str(runs),
        'fours': str(fours),
        'sixes': str(sixes),
        'avg': str(avg),
        'strikeRate': str(strike_rate),
        'fifties': str(fifties),
        'hundreds': str(hundreds),
        'highestScore': str(highest_score),
        'notOut': str(not_out)
    }

    return response



# API for bowling performance
def bowling_stats(player):
    ipl = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vRy2DUdUbaKx_Co9F0FSnIlyS-8kp4aKv_I0-qzNeghiZHAI_hw94gKG22XTxNJHMFnFVKsO4xWOdIs/pub?gid=1655759976&single=true&output=csv")
    ipl2 = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vRu6cb6Pj8C9elJc5ubswjVTObommsITlNsFy5X0EiBY7S-lsHEUqx3g_M16r50Ytjc0XQCdGDyzE_Y/pub?output=csv")

    # Total wickets taken
    matches = ipl2[(ipl2.bowler == 'I Sharma') & (ipl2.isWicketDelivery == 1) & (ipl2.kind != 'run out')]
    tot_wickets = matches.shape[0]

    # Total matches played
    df = ipl[ipl['Team1Players'].str.contains(player) | ipl['Team2Players'].str.contains(player)]
    tot_matches = df.shape[0]

    # Total overs,balls given
    valid_balls = ipl2[ipl2['extra_type'].isna()]
    balls_bowled = valid_balls[valid_balls['bowler'] == player].shape[0]
    overs_bowled = balls_bowled // 6 + (balls_bowled % 6) / 10

    # Total runs conceded
    Total_runs_conceded = ipl2[ipl2['bowler'] == player]['total_run'].sum()

    # Economy and average of bowler
    economy = round(Total_runs_conceded / overs_bowled, 2)
    average = round(Total_runs_conceded / tot_wickets, 2)

    # Best performance of bowler
    data = ipl2[ipl2['bowler'] == player]
    wickets_taken = data.groupby('ID')['isWicketDelivery'].sum().sort_values(ascending=False).head(1).values[0]

    runs_given = data.groupby(['ID', 'bowler'])[['isWicketDelivery', 'total_run']].sum() \
        .sort_values(by=['isWicketDelivery', 'total_run'], ascending=[False, True]) \
        .head(1).values[0][1]

    best_performance = "{} / {}".format(wickets_taken, runs_given)

    result = {
        'Player': str(player),
        'Total Matches': str(tot_matches),
        'Total Wickets': str(tot_wickets),
        'Total Overs': str(overs_bowled),
        'Total Runs Conceded': str(Total_runs_conceded),
        'Economy': str(economy),
        'Average': str(average),
        'Best Performance': str(best_performance)
    }

    return result


def batter_vs_teams(player):
    # Datasets
    ipl = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vRy2DUdUbaKx_Co9F0FSnIlyS-8kp4aKv_I0-qzNeghiZHAI_hw94gKG22XTxNJHMFnFVKsO4xWOdIs/pub?gid=1655759976&single=true&output=csv")
    ipl2 = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vRu6cb6Pj8C9elJc5ubswjVTObommsITlNsFy5X0EiBY7S-lsHEUqx3g_M16r50Ytjc0XQCdGDyzE_Y/pub?output=csv")

    # Merge datasets
    data = pd.merge(ipl, ipl2, on='ID')

    # unique teams
    all_teams = (data['Team1']).unique()

    results = {}  # Store results

    for team in all_teams:
        # Filter data for
        xyz = data[(data['batter'] == player) & ((data['Team2'] == team) | (data['Team1'] == team))]

        # Total matches
        Total_matches = xyz['ID'].nunique()

        # Total runs
        Total_runs = xyz['batsman_run'].sum()

        # Fifties and Hundreds
        gb = xyz.groupby('ID').sum()
        fifties = gb[(gb['batsman_run'] >= 50) & (gb['batsman_run'] < 100)].shape[0]
        hundreds = gb[gb['batsman_run'] >= 100].shape[0]

        # Strike rate
        valid_balls = xyz[xyz['extra_type'].isna()]  # Exclude extras
        Total_balls = valid_balls.shape[0]
        stk_rate = round((Total_runs / Total_balls) * 100, 2) if Total_balls > 0 else 0.0

        # Average
        out = xyz[xyz['player_out'] == player].shape[0]
        bat_avg = round(Total_runs / out, 2) if out > 0 else Total_runs

        # Max score
        max_score = gb['batsman_run'].max() if not gb.empty else 0

        # Add result to the dictionary
        results[team] = {
            'Total Matches': str(Total_matches),
            'Total Runs': str(Total_runs),
            'Fifties': str(fifties),
            'Hundreds': str(hundreds),
            'Strike Rate': str(stk_rate),
            'Average': str(bat_avg),
            'Max Score': str(max_score)
        }

    return results


def bowler_vs_teams(bowler):
    # Datasets
    ipl = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vRy2DUdUbaKx_Co9F0FSnIlyS-8kp4aKv_I0-qzNeghiZHAI_hw94gKG22XTxNJHMFnFVKsO4xWOdIs/pub?gid=1655759976&single=true&output=csv")
    ipl2 = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vRu6cb6Pj8C9elJc5ubswjVTObommsITlNsFy5X0EiBY7S-lsHEUqx3g_M16r50Ytjc0XQCdGDyzE_Y/pub?output=csv")

    # Merge datasets
    data = pd.merge(ipl, ipl2, on='ID')

    # Unique teams from 'Team1' column
    all_teams = data['Team1'].unique()

    results = {}

    for team in all_teams:
        # Filter data for the specific bowler and team
        xyz = data[(data['bowler'] == bowler) & ((data['Team2'] == team) | (data['Team1'] == team))]

        # Total matches
        Total_matches = xyz['ID'].nunique() if not xyz.empty else 0

        # Total wickets taken by the bowler
        matches = xyz[(xyz['bowler'] == bowler) & (xyz['isWicketDelivery'] == 1) & (xyz['kind'] != 'run out')]
        tot_wickets = matches.shape[0] if not matches.empty else 0

        # Total balls bowled (excluding extras)
        valid_balls = xyz[xyz['extra_type'].isna()]
        balls_bowled = valid_balls[valid_balls['bowler'] == bowler].shape[0]
        overs_bowled = balls_bowled // 6 + (balls_bowled % 6) / 10  # Convert balls to overs

        # Total runs conceded by the bowler
        Total_runs_conceded = xyz[xyz['bowler'] == bowler]['total_run'].sum() if not xyz.empty else 0

        # Economy and average
        economy = round(Total_runs_conceded / overs_bowled, 2) if overs_bowled > 0 else 0.0
        average = round(Total_runs_conceded / tot_wickets, 2) if tot_wickets > 0 else 0.0

        # Best performance
        data_bowler = xyz[xyz['bowler'] == bowler]

        # Handle cases where there are no matches or no wickets
        if not data_bowler.empty:

            wickets_per_match = data_bowler.groupby('ID')['isWicketDelivery'].sum()
            if not wickets_per_match.empty:
                max_wickets = wickets_per_match.max()  # Best wickets in a match
            else:
                max_wickets = 0

            # runs conceded
            runs_per_match = data_bowler.groupby(['ID'])['total_run'].sum()
            if not runs_per_match.empty:
                min_runs = runs_per_match[wickets_per_match.idxmax()] if max_wickets > 0 else 0
            else:
                min_runs = 0

            best_performance = f"{max_wickets} / {min_runs}" if max_wickets > 0 else "No Wickets Taken"
        else:
            best_performance = "No Matches Played"

        # Add result to the dictionary
        results[team] = {
            'Bowler': str(bowler),
            'Team': str(team),
            'Total Matches': str(Total_matches),
            'Total Wickets': str(tot_wickets),
            'Overs Bowled': str(overs_bowled),
            'Total Runs Conceded': str(Total_runs_conceded),
            'Economy': str(economy),
            'Average': str(average),
            'Best Performance': str(best_performance)
        }

    return results










































# def batsman(player):
#     ipl = pd.read_csv(
#         "https://docs.google.com/spreadsheets/d/e/2PACX-1vRu6cb6Pj8C9elJc5ubswjVTObommsITlNsFy5X0EiBY7S-lsHEUqx3g_M16r50Ytjc0XQCdGDyzE_Y/pub?output=csv")
#     player_df = ipl[ipl.batter == player]
#
#     x = player_df['ID'].unique()
#     total_matches = len(x)
#
#     max_score = player_df.groupby('ID')['batsman_run'].sum().sort_values(ascending=False).head(1).iloc[0]
#
#     runs = player_df.groupby('ID')['batsman_run'].sum().sort_values(ascending=False)
#     runs = runs[runs >= 100]
#     no_of_100 = len(runs)
#
#     runs = player_df.groupby('ID')['batsman_run'].sum().sort_values(ascending=False)
#     runs = runs[(runs < 100) & (runs >= 50)]
#     no_of_50 = len(runs)
#
#     total_runs = player_df['batsman_run'].sum()
#
#     stk_rate = round((total_runs / player_df.shape[0]) * 100, 2)
#
#     avg_score = round((player_df['batsman_run'].sum()) / (player_df['player_out'].count()), 2)
#
#     response = {
#         'Total_matches': str(total_matches),
#         'max_score': str(max_score),
#         'no_of_100': str(no_of_100),
#         'no_of_50': str(no_of_50),
#         'Total_runs': str(total_runs),
#         'stk_rate': str(stk_rate),
#         'avg_score': str(avg_score)
#     }
#     return response



















































