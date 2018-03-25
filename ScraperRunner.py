from Scraper import collect_data_from_seed_player, collect_data_expand_from_file
counter = collect_data_from_seed_player('JPFog')
counter = collect_data_expand_from_file(counter)
print("You have collected match data on {} unique matches!".format(counter))