from ScraperUtils import scrape_user_id, scrape_match_list, scrape_match_data
import csv
from urllib.error import HTTPError
from time import sleep
import re


# seed_name = 'JPFog'


def collect_data_from_seed_player(seed_name):
    seed_id = scrape_user_id(seed_name)
    name_id_set = {(seed_name, seed_id)}
    match_set = scrape_match_list(seed_id)
    with open("PUBG_match_ids.tsv", 'a') as f:
        f.write(re.sub('[\s+]', '', str(match_set)) + "\t" + "\n")
    used_names = {seed_name}
    with open("PUBG_used_names.tsv", 'a') as f:
        f.write(re.sub('[\s+]', '', str(used_names)) + "\t" + "\n")
    used_matches = set()
    counter = 0
    for match_id in match_set:
        while True:
            try:
                name_ids_from_match, data_from_match = scrape_match_data(match_id)
                new_name_ids_from_match = name_ids_from_match - name_id_set
                with open("PUBG_name_ids.tsv", 'a') as f:
                    f.write(re.sub('[\s+]', '', str(new_name_ids_from_match)))
                name_id_set.update(name_ids_from_match)
                with open("PUBG_MatchData.tsv", 'a') as f:
                    f.write(re.sub('[\s+]', '', str(data_from_match)) + "\t" + "\n")
                used_matches.add(match_id)
                with open("PUBG_used_match_ids.tsv", 'a') as f:
                    f.write(re.sub('[\s+]', '', str(match_id)))
                counter = counter+1
                print(counter)
                break
            except HTTPError:
                try:
                    print('Ratelimited!')
                    sleep(10)
                    name_ids_from_match, data_from_match = scrape_match_data(match_id)
                    new_name_ids_from_match = name_ids_from_match - name_id_set
                    with open("PUBG_name_ids.tsv", 'a') as f:
                        f.write(re.sub('[\s+]', '', str(new_name_ids_from_match)))
                    name_id_set.update(name_ids_from_match)
                    with open("PUBG_MatchData.tsv", 'a') as f:
                        f.write(re.sub('[\s+]', '', str(data_from_match)) + "\t" + "\n")
                    used_matches.add(match_id)
                    with open("PUBG_used_match_ids.tsv", 'a') as f:
                        f.write(re.sub('[\s+]', '', str(match_id)))
                    counter = counter+1
                    print(counter)
                    continue
                except HTTPError:
                    print('Double HTTPError! SKIPPING!')
                    break


def collect_data_expand_from_file():

    counter = 1

    with open('PUBG_name_ids.tsv', 'r') as f:
        reader = csv.reader(f)
        name_id_set = set(reader)
    with open('PUBG_used_names.tsv', 'r') as f:
        reader = csv.reader(f)
        used_names = set(reader)
    with open('PUBG_match_ids.tsv', 'r') as f:
        reader = csv.reader(f)
        match_set = set(reader)
    with open('PUBG_used_match_ids.tsv', 'r') as f:
        reader = csv.reader(f)
        used_matches = set(reader)

    for (name, player_id) in name_id_set:
        if name not in used_names:
            match_ids = scrape_match_list(player_id)
            new_match_ids = match_ids - match_set
            match_set.update(match_ids)
            with open("PUBG_match_ids.tsv", 'a') as f:
                f.write(re.sub('[\s+]', '', str(new_match_ids)))
            used_names.add(name)
            with open("PUBG_used_names.tsv", 'a') as f:
                f.write(re.sub('[\s+]', '', str(name)) + "\t" + "\n")
            for match_id in match_ids:
                if match_id not in used_matches:
                    name_ids_from_match, data_from_match = scrape_match_data(match_id)
                    new_name_ids_from_match = name_ids_from_match
                    name_id_set.update(name_ids_from_match)
                    with open("PUBG_name_ids.tsv", 'a') as f:
                        f.write(re.sub('[\s+]', '', str(new_name_ids_from_match)))
                    with open("PUBG_MatchData.tsv", 'a') as f:
                        f.write(re.sub('[\s+]', '', str(data_from_match)) + "\t" + "\n")
                    used_matches.add(match_id)
                    with open("PUBG_used_match_ids.tsv", 'a') as f:
                        f.write(re.sub('[\s+]', '', str(match_id)))
                    counter = counter+1
                    print(counter)
