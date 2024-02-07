## Pulls out the data we care about from here!

def get_players_part_id(parts, puuid):
        return {x["puuid"]: x["participantId"] for x in parts}[puuid]

def get_particpants_puuid(parts, part_id):
    return {x["participantId"]: x["puuid"] for x in parts}[part_id]

def select_player_locations(match_id, match_type,  timeline, data = []):
    frames = timeline["info"]["frames"]
    parts = timeline["info"]["participants"]

    for frame_idx, frame in enumerate(frames):
        for player in frame["participantFrames"].keys():
            player_meta = frame["participantFrames"][player]
            pos = player_meta["position"]
            level = player_meta["level"]
            data.append({
                "match_ids": match_id,
                "match_type": match_type,
                "frame": frame_idx,
                "player_part_id": player,
                "player_puuid": get_particpants_puuid(parts, int(player)),
                "x": pos["x"],
                "y": pos["y"],
                "level": level,
            })
        
    return data

import random

## The idea is to crawll by selecting new matches that we likely haven't seen before
# The way I'm going to do this is out of the list of this match partipants
# Select a random player in the other team than the user we had before
# Reasoning: If players played with friends, we could hurt our data by having the same matches appear more than 10 times
# Like imagine we choose only friends to a given player, we bounce around a lot 
# So choose the enemy team, probably not friends :)
#def select_next_match(timeline, curr_puuid):

# assume players 1 - 5 are on one team, players 5 - 10 on the other

def get_next_puuid(puuid,timeline):
    parts = timeline["info"]["participants"]

    if get_players_part_id(parts, puuid) in list(range(1, 6)):
        new_player = random.randint(1, 5)
    else:
        new_player = random.randint(5, 10)

    return get_particpants_puuid(parts, new_player)


# Crawl the riot games api simliar to https://github.com/christophM/LolCrawler 
def get_n_matches_data(lol_watcher, puuid, n, my_region="na1"):
    data = []
    for _ in range(n):
        match_ids = lol_watcher.match.matchlist_by_puuid(my_region, puuid)
        match_id = random.choice(match_ids)
        
        match_meta = lol_watcher.match.by_id(my_region, match_id)
        match_type = match_meta["info"]["gameMode"]

        timeline = lol_watcher.match.timeline_by_match(my_region, match_id)
        
        data = select_player_locations(match_id, match_type, timeline, data=data)
        puuid = get_next_puuid(puuid, timeline)
    return data