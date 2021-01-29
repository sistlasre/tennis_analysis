#!/usr/bin/env python3

from sys import exit
import logging
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from parseData import process_atp_data
import fetchInfo

'''
Configures the logging for the program.
'''
def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Add a file to log everything at/above DEBUG
    file_logger = logging.FileHandler('tennis_program.log', 'w')
    logger.addHandler(file_logger)

    # Only print the logs that are set to INFO or higher
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)


'''
Parses the arguments to the program and returns a tuple (command, sort_order) of what was passed in.
'''
def configure_arg_parser():
    parser = argparse.ArgumentParser(description = "Analyze ATP Tennis 1991-2017 Data Set")

    subparsers = parser.add_subparsers(title="commands", dest="command")

    player_info = subparsers.add_parser('player_info', help='Spits out player info from 1991-2017')
    player_info.add_argument('name', nargs='+', help='Name of player whose info you want', type=str.lower)

    trends = subparsers.add_parser('trends', help='Prints and displays interesting trends in tennis from 1991-2017')

    parser.add_argument('-o', '--overviews', metavar='<overviewsFile>', type=str, dest='overviews_file', action='store', help="File to fetch the player overviews", default="input_datasets/playerOverviews.csv")
    parser.add_argument('-sc', '--scores', metavar='<scoresFile>', type=str, dest='scores_file', action='store', help="File to fetch all match scores from 1991-2017", default="input_datasets/scores.csv")
    parser.add_argument('-st', '--stats', metavar='<statsFile>', type=str, dest='stats_file', action='store', help="File to fetch all match stats from 1991-2017", default="input_datasets/stats.csv")
    
    return parser


def main():
    configure_logging()

    arg_parser = configure_arg_parser()
    args = arg_parser.parse_args()

    # The argument parser handles invalid commands but it won't handle an empty one so let's explicitly print the usage.
    if not args.command:
        arg_parser.print_usage()
        exit()


    # Now, onto the real program...
    players, df = process_atp_data(args.overviews_file, args.scores_file, args.stats_file)

    if args.command == 'player_info':
        fetchInfo.display_player_info(' '.join(args.name), players, df)
    else:
        fetchInfo.show_trends_through_the_years(df)



# Run the actual program if being invoked from the shell
if __name__ == "__main__":
    main()
