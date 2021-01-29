import pandas as pd
import matplotlib.pyplot as plt
import logging
import csv

'''
Takes in a requested player, a dictionary of players, and a Pandas DataFrame, df.
Spits out some information about the requested player.
do_plot is used for testing purposes so we can restrict plotting.
'''
def display_player_info(requested_player, players, df, do_plot=True):
    logging.info(f"Fetching information for <{requested_player}>")
    
    if requested_player in players:
        player = players[requested_player]
        print(player.id)
        print(f"Name: {player.first_name} {player.last_name}")
        numWins = df.loc[df['winner'] == player.id].shape[0]
        print(f"Num Wins: {numWins}")
        numLosses = df.loc[df['loser'] == player.id].shape[0]
        print(f"Num Losses: {numLosses}")

        numWinsByYear = df.loc[df['winner'] == player.id].groupby('year').size()
        numLossesByYear = df.loc[df['loser'] == player.id].groupby('year').size()
        numMatchesByYear = numWinsByYear.add(numLossesByYear, level='year')

        pctWinsByYear = numWinsByYear.div(numMatchesByYear, level='year')

        _plot_single_by_year(numWinsByYear, "Num Wins", f"Wins for Year by {requested_player}")
        _plot_single_by_year(pctWinsByYear, "Pct Wins", f"Pct Wins for Year by {requested_player}")
    else:
        print(f"Player <{requested_player}> does not exist in our dataset")


'''
Plots a single dataset
'''
def _plot_single_by_year(data, ylabel, title):
    _plot_multiple_by_year([data], [''], ylabel, title)


'''
Plots multiple datasets on the same graph.
'''
def _plot_multiple_by_year(datasets, dataset_labels, ylabel, title):
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(ylabel)

    for i in range(len(datasets)):

        file_name = title
        if dataset_labels[i]:
            file_name += '-' + dataset_labels[i]
        file_name += '.csv'

        years = []
        yValues = []

        with open(file_name, 'w') as out_file:
            csv_writer = csv.DictWriter(out_file, fieldnames = ['year', ylabel])

            for year, yValue in datasets[i].items():
                years.append("'" + str(year)[-2:])
                yValues.append(yValue)
                csv_writer.writerow({'year': year, ylabel: yValue})

        plt.plot(years, yValues, label=dataset_labels[i])

    if len(datasets) > 1:
        plt.legend()

    plt.savefig(f"{title}.png")
    plt.show()

'''
Calculates several different trends in how matches have been going year by year.
do_plot is used for testing purposes so we can restrict plotting.
'''
def show_trends_through_the_years(df, do_plot=True):
    aces = df.groupby('year')['aces'].sum()
    double_faults = df.groupby('year')['double_faults'].sum()
    num_matches = df.groupby('year').size()
    # Now, let's plot aces and double faults next to each other
    _plot_multiple_by_year([aces.div(num_matches, level='year'), double_faults.div(num_matches, level='year')], ['Aces', 'Double Faults'], 'Per Match', 'Serves over the Years')

    ret_games_won = df.groupby('year')['return_games_won'].sum()
    total_games = df.groupby('year')['total_games'].sum()
    # Now, let's plot this by itself to see what the trend is over the years in terms of returning
    _plot_single_by_year(ret_games_won.div(total_games, level='year'), 'Percent', 'Pct Return Games Won By Year')

    first_serves_attempted = df.groupby('year')['first_serves_attempted'].sum()
    first_serves_in = df.groupby('year')['first_serves_in'].sum()
    first_serves_won = df.groupby('year')['first_serves_won'].sum()

    # We will first plot the 1st serve percentage by itself
    _plot_single_by_year(first_serves_in.div(first_serves_attempted, level='year'), 'Percent', '1st Serve Pct By Year')
    # Next, we will plot the percentage of first serve points that were won (by the server)
    _plot_single_by_year(first_serves_won.div(first_serves_in, level='year'), 'Percent', '1st Serve Win Pct By Year')

