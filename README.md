# tennis_analysis

Name: Sreeharsha Sistla

Final Project Description

What I’m Researching:

How has tennis evolved	over the past 25 years? In particular, are people better at returning these days than they used to be in the past? If so, why is that? Is it due to a better serve percentage?

What My Program Does:

I pulled down the data from a public tennis repo so I’m including 3 different datasets that span from 1991-2017: playerOverviews.csv, scores.csv, and stats.csv. The scores and stats files are used to generate stats for all matches from 1991-2017. Now the actual code spans 3 different files: mainProgram.py, parseData.py, and fetchInfo.py. The mainProgram file handles things like logging setup and the argument handler. In addition, it glues together the parser and the fetcher. The parseData file will parse the 3 data files and then generate a map of the players as well as a Pandas DataFrame corresponding to all the matches listed in scores and stats. Lastly, the fetchInfo file will either fetch info about a given player and show the performance over the years OR show trends in the game of tennis throughout the years. Both of these use Pandas DataFrame quite in depth.

My Analysis:
Based on the 3 images I included, you’ll see that one of the big trends in tennis is that players have gotten better at serving. The increased first serve percentage is very likely the reason why the percentage of return games won has dropped over the years. This trend is also visible in the aces and double faults graph as you see an increase in both, suggesting that players are hitting the first serve more aggressively, hoping to get some easy points.


Example Command Line Invocations:

We can simply run ./main_program -h to get an idea how to run the program. But here are the 2 major commands we can run in the CLI:

1. ./main_program player_info “rafael nadal” :  this will process all the data and print out some basic information about the inputted player as well as some statistics over the years
2. ./main_program trends: this will process all the data and print out different trends over the years to show how the game of tennis is changing these days, and also, maybe why
