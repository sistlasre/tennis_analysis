import csv
from collections import namedtuple
import pandas as pd
import logging

Player = namedtuple('Player', 'id,first_name,last_name')
Score = namedtuple('Score', 'match_id,year,winner,loser')


def _parse_player_overviews(overviewsFileName):
    logging.info(f"Processing player overviews file <{overviewsFileName}>")
    players = {}
    with open(overviewsFileName) as playerOverviewsFile:
        reader = csv.DictReader(playerOverviewsFile)
        for player in reader:
            players[f"{player['first_name']} {player['last_name']}".lower()] = Player(player['player_id'], player['first_name'], player['last_name'])

    return players

def _parse_scores(scoresFileName):
    logging.info(f"Processing scores file <{scoresFileName}>")
    scores = {}
    with open(scoresFileName) as scoresFile:
        reader = csv.DictReader(scoresFile)
        for score in reader:
            winner = score['winner_player_id']
            loser = score['loser_player_id']
            year = score['tourney_year_id'].split('-')[0]
            match_id = score['match_id']
            scores[match_id] = Score(match_id, year, winner, loser)

    return scores

def _parse_stats(statsFileName):
    logging.info(f"Processing stats file <{statsFileName}>")
    stats = []
    with open(statsFileName) as statsFile:
        reader = csv.DictReader(statsFile)
        MatchStat = namedtuple('MatchStat', reader.fieldnames)
        for stat in reader:
            stats.append(MatchStat(*stat.values()))

    return stats


'''
Generates a Pandas DataFrame based on the scores and stats that were parsed in previous steps.
'''
def _generate_data_frame_from_scores_and_stats(scores, stats):
    data = []
    for stat in stats:
        if stat.match_id not in scores or not stat.match_duration:
            logging.debug(f"Skipping match with id <{stat.match_id}>")
            continue

        score = scores[stat.match_id]
        match = _combine_stats(stat)

        data.append({'year': score.year, 'winner': score.winner, 'loser': score.loser, **match})

    return pd.DataFrame(data)

'''
Combines the stats of the appropriate winner and loser columns to populate the DataFrame generated above.
Returns a dictionary of the stat: value
'''
def _combine_stats(stat):
    match = {}
    match['aces'] = int(stat.winner_aces) + int(stat.loser_aces)
    match['double_faults'] = int(stat.winner_double_faults) + int(stat.loser_double_faults)
    match['return_games_won'] = int(stat.winner_break_points_converted) + int(stat.loser_break_points_converted)
    match['total_games'] = int(stat.winner_service_games_played) + int(stat.loser_service_games_played)
    match['first_serves_attempted'] = int(stat.winner_first_serves_total) + int(stat.loser_first_serves_total)
    match['first_serves_in'] = int(stat.winner_first_serves_in) + int(stat.loser_first_serves_in)
    match['first_serves_won'] = int(stat.winner_first_serve_points_won) + int(stat.loser_first_serve_points_won)

    return match


'''
Processes the ATP data files and returns a tuple (overviews, dataFrame).
overviews contains the player overviews and is searchable by player name.
dataFrame is a dataFrame with the necessary information to show different trends from 1991-2017
'''
def process_atp_data(overviewsFileName, scoresFileName, statsFileName):
    players = _parse_player_overviews(overviewsFileName)
    scores = _parse_scores(scoresFileName)
    stats = _parse_stats(statsFileName)
    df = _generate_data_frame_from_scores_and_stats(scores, stats)

    return (players, df)

