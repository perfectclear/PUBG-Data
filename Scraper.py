from ScraperUtils import ScrapeUserId, ScrapeMatchList, ScrapeMatchData
import csv

#seed_name = 'JPFog'

def CollectDataFromSeedPlayer(seed_name):
    seed_id = ScrapeUserId(seed_name)
    name_id_set = set((seed_name, seed_id))
    match_set = ScrapeMatchList(seed_id)
    with open("PUBG_match_ids.csv", 'a') as f:
        f.write(str(match_set) + "," + "\n")
    used_names = set(seed_name)
    with open("PUBG_used_names.csv", 'a') as f:
        f.write(str(seed_name) + "," + "\n")
    used_matches = set()
    match_data = set()
    counter = 0
    for match_id in match_set:
        name_ids_from_match, data_from_match = ScrapeMatchData(match_id)
        name_id_set.add(name_ids_from_match)
        with open("PUBG_name_ids.csv", 'a') as f:
            f.write(str(name_ids_from_match) + "," + "\n")
        match_data.add(data_from_match)
        with open("PUBG_MatchData.csv", 'a') as f:
            f.write(str(data_from_match) + "," + "\n")
        used_matches.add(match_id)
        with open("PUBG_used_match_ids.csv", 'a') as f:
            f.write(str(match_id) + "," + "\n")
        counter = counter+1
        print(counter)


def CollectDataExpandFromFile():

    counter = 1

    with open('PUBG_name_ids.csv', 'r') as f:
        reader = csv.reader(f)
        name_id_set = set(reader)
    with open('PUBG_used_names.csv', 'r') as f:
        reader = csv.reader(f)
        used_names = set(reader)
    with open('PUBG_match_ids.csv', 'r') as f:
        reader = csv.reader(f)
        match_set = set(reader)
    with open('PUBG_used_match_ids.csv', 'r') as f:
        reader = csv.reader(f)
        used_matches = set(reader)
    with open('PUBG_MatchData.csv', 'r') as f:
        reader = csv.reader(f)
        match_data = set(reader)

    for (name,id) in name_id_set:
        if name not in used_names:
            match_ids = ScrapeMatchList(id)
            match_set.add(match_ids)
            with open("PUBG_match_ids.csv", 'a') as f:
                f.write(str(match_set) + "," + "\n")
            used_names.add(name)
            with open("PUBG_used_names.csv", 'a') as f:
                f.write(str(name) + "," + "\n")
            for match_id in match_ids:
                if match_id not in used_matches:
                    name_ids_from_match, data_from_match = ScrapeMatchData(match_id)
                    name_id_set.add(name_ids_from_match)
                    with open("PUBG_name_ids.csv", 'a') as f:
                        f.write(str(name_ids_from_match) + "," + "\n")
                    match_data.add(data_from_match)
                    with open("PUBG_MatchData.csv", 'a') as f:
                        f.write(str(data_from_match) + "," + "\n")
                    used_matches.add(match_id)
                    with open("PUBG_used_match_ids.csv", 'a') as f:
                        f.write(str(match_id) + "," + "\n")
                    counter = counter+1
                    print(counter)

