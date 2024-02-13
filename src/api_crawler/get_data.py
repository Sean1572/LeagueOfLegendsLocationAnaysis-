from riotwatcher import LolWatcher, ApiError
## Pulls out the data we care about from here!

def get_players_part_id(parts, puuid):
        return {x["puuid"]: x["participantId"] for x in parts}[puuid]

def get_particpants_puuid(parts, part_id):
    return {x["participantId"]: x["puuid"] for x in parts}[part_id]

def select_player_locations(match_meta,  timeline, data = [], lol_watcher=LolWatcher, region="na1"):
    frames = timeline["info"]["frames"]
    parts = timeline["info"]["participants"]
    match_type = match_meta["info"]["gameMode"]
    match_id = match_meta["metadata"]["matchId"]

    # Trying to not redo these every frame to save on api limits!
    tiers, ranks = [], []
    #print(len(match_meta["info"]["participants"]))
    for player in range(1, 11):
        summoner_id = match_meta["info"]["participants"][player-1]["summonerId"]
        summoner_meta = lol_watcher.league.by_summoner(region, summoner_id)
        if len(summoner_meta) > 0:
            rank_meta = summoner_meta[0]
            tiers.append(rank_meta["tier"])
            ranks.append(rank_meta["rank"])
        else:
            tiers.append("UNKN")
            ranks.append("UNKN")
    #print(tiers)
    #print(ranks)


    for frame_idx, frame in enumerate(frames):
        for player in frame["participantFrames"].keys():
            player_meta = frame["participantFrames"][player]
            player = int(player)
            player_list = int(player) - 1
            pos = player_meta["position"]
            level = player_meta["level"]
            puuid = get_particpants_puuid(parts, player)
            team_id = match_meta["info"]["participants"][player_list]["teamId"]
            win = match_meta["info"]["participants"][player_list]["win"]
            team_pos  = match_meta["info"]["participants"][player_list]["teamPosition"]
            indiv_pos = match_meta["info"]["participants"][player_list]["individualPosition"]
            lane = match_meta["info"]["participants"][player_list]["lane"]
            tier = tiers[player_list]
            rank = ranks[player_list]

            data.append({
                "match_ids": match_id,
                "match_type": match_type,
                "frame": frame_idx,
                "player_part_id": player,
                "player_puuid": puuid,
                "player_summoner_id": summoner_id,
                "x": pos["x"],
                "y": pos["y"],
                "team_id": team_id,
                "win": win,
                "position": team_pos,
                "indiv_pos": indiv_pos,
                "lane": lane,
                "level": level,
                "tier": tier,
                "rank": rank
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