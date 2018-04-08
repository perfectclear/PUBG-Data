# PUBG-Data
This repository contains my scraper for collecting PUBG data from pubg.op.gg, and perhaps some models in the future.

# Scraper Utils:
Contains the utils needed to scrape data from pubg.op.gg, based on a player's name. With this you can get that player's internal id, their last 100 fpp squad matches' ids, and the names and ids of everyone they played with (that killed anyone or died, so not someone who got first without killing anyone) in any given match searched by internal match id.

# Scraper:
Contains a scraper to scrape from a seed name, and a scraper to scrape based on files saved by other scraper. Currently set to have 0 sleep, may need to change that if you get ratelimited/want to be polite. To build my database with sleep of 5 seconds would take 2 months, so I am not using a sleep.

# ScraperRunner:
Runs the seed scraper with seedname "JPFog" and then the expansion scraper once.

# DataLoader:
Loads in the data you saved through scraping and reformats into a pandas dataframe. you will need to change the os.chdir() directory to the directory you saved your data in. DataLoader also currently saves a flattened version of MatchData for easier future use.


# Known current issues:

~~If you run ScraperRunner as is, it stops after collecting the match data on the first 199 players (about 16.5k matches)~~ fixed 

If you try expanding on a large file, csv cannot handle it. Batching is a solution that has not yet been implemented.

After running for a while, slows down. Solution: put http error matches into a "bad match list" and exclude them from the matches to search, so you dont check the same matches over and over. needs more investigation

# Analysis
Message me if you want your analysis included here.
Here is a kill/death heatmap analysis https://www.kaggle.com/michaelapers/pubg-kill-death-heatmaps made by me
