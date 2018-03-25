# PUBG-Data
This repository contains my scraper for collecting PUBG data from pubg.op.gg, and perhaps some models in the future.

# Scraper Utils:
Contains the utils needed to scrape data from pubg.op.gg, based on a player's name. With this you can get that player's internal id, their last 100 fpp squad matches' ids, and the names and ids of everyone they played with (that killed anyone or died, so not someone who got first without killing anyone) in any given match searched by internal match id.

# Scraper:
Contains a scraper to scrape from a seed name, and a scraper to scrape based on files saved by other scraper. Currently set to have 0 sleep, may need to change that if you get ratelimited/want to be polite. To build my database with sleep of 5 seconds would take 2 months, so I am not using a sleep.

# ScraperRunner:
Runs the seed scraper with seedname "JPFog" and then the expansion scraper once.
