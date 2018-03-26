from ScraperUtils import scrape_user_id, scrape_match_list, scrape_match_data
import csv
from urllib.error import HTTPError
from time import sleep
import re


# seed_name = 'JPFog'


def collect_data_from_seed_player(seed_name):
    seed_id = scrape_user_id(seed_name)
    name_set = {seed_name}
    match_set = scrape_match_list(seed_id)
    with open("PUBG_match_ids.tsv", 'a') as f:
        f.write(re.sub('[\s+]', '', str(match_set)) + "\t" + "\n")
    with open("PUBG_used_names.tsv", 'a') as f:
        f.write(re.sub('[\s+]', '', str(seed_name)) + "\t" + "\n")
    used_matches = set()
    counter = 0
    for match_id in match_set:
        while True:
            try:
                names_from_match, data_from_match = scrape_match_data(match_id)
                new_names_from_match = names_from_match - name_set
                with open("PUBG_names.tsv", 'a') as f:
                    f.write(re.sub('[\s+]', '', str(new_names_from_match)))
                name_set.update(names_from_match)
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
                    print('Ratelimited?')
                    sleep(5)
                    names_from_match, data_from_match = scrape_match_data(match_id)
                    new_names_from_match = names_from_match - name_set
                    with open("PUBG_names.tsv", 'a') as f:
                        f.write(re.sub('[\s+]', '', str(new_names_from_match)))
                    name_set.update(names_from_match)
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
    return counter


def collect_data_expand_from_file(counter=99):
    with open('PUBG_names.tsv', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        name_set = set()
        for row in reader:
            listofsets = eval("[" + re.sub('}{', '},{', ', '.join(row)) + "]")
            for item in listofsets:
                name_set.update(item)
                name_set.discard('')

    with open('PUBG_used_names.tsv', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        used_names = set()
        for row in reader:
            used_names.update(set(row))
            used_names.discard('')

    with open('PUBG_match_ids.tsv', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        match_set = set()
        for row in reader:
            listofsets = eval("[" + re.sub('}{', '},{', ', '.join(row)) + "]")
            for item in listofsets:
                match_set.update(item)
                match_set.discard('')

    with open('PUBG_used_match_ids.tsv', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        used_matches = set()
        for row in reader:
            listofsets = eval("[{'" + re.sub("=", "='},{'", ', '.join(row)) + "'}]")
            for item in listofsets:
                used_matches.update(item)
                used_matches.discard('')

    usable_names = name_set.copy()
    usable_names -= used_names
    for name in usable_names:
        player_id = scrape_user_id(name)
        if not player_id:
            break
        match_ids = scrape_match_list(player_id)
        if not match_ids:
            break
        new_match_ids = match_ids - match_set
        match_set.update(match_ids)
        with open("PUBG_match_ids.tsv", 'a') as f:
            f.write(re.sub('[\s+]', '', str(new_match_ids)))
        used_names.add(name)
        with open("PUBG_used_names.tsv", 'a') as f:
            f.write(re.sub('[\s+]', '', str(name)) + "\t" + "\n")

        usable_matches = match_set.copy()
        usable_matches -= used_matches

        for match_id in usable_matches:
            while True:
                try:
                    names_from_match, data_from_match = scrape_match_data(match_id)
                    if not names_from_match:
                        break
                    new_names_from_match = names_from_match
                    name_set.update(names_from_match)
                    with open("PUBG_names.tsv", 'a') as f:
                        f.write(re.sub('[\s+]', '', str(new_names_from_match)))
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
                        print('Ratelimited?')
                        sleep(5)
                        names_from_match, data_from_match = scrape_match_data(match_id)
                        if not names_from_match:
                            break
                        new_names_from_match = names_from_match
                        name_set.update(names_from_match)
                        with open("PUBG_names.tsv", 'a') as f:
                            f.write(re.sub('[\s+]', '', str(new_names_from_match)))
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
    return counter
