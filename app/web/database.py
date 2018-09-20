"""
Neo4j database calls
"""

import asyncio
from neo4j.v1 import GraphDatabase

# Initialize DB connection
db = GraphDatabase.driver(
    "bolt://0.0.0.0:7700",
    auth=(
        "neo4j",
        "clash" ))


def add_postcode_to_neo4j(txn, postcode):
    """
    check and/or add postcode
    """
    txn.run("MERGE (:PostCode {postcode: $postcode})",
            postcode=postcode)


def add_summoner_to_neo4j(txn, summoner_id):
    """
    check and/or add user
    """
    txn.run("MERGE (:Summoner {id: $summoner_id})",
            summoner_id=summoner_id)


def add_base_summoner_info_neo4j(txn, additional_info):
    """
    check and/or add user
    """
    base_info = additional_info['base_profile_info']
    profile_info = additional_info['additional_info']

    rank_info = profile_info[0]
    champion_info = profile_info[1]

    txn.run("MATCH (s:Summoner {id: $summoner_id})\
            SET s += {\
                account_id:$account_id,\
                summoner_name:$name,\
                profile_icon_id:$profile_icon_id,\
                date_joined_game:$date_joined_game,\
                summoner_level:$summoner_level\
            }",
            summoner_id=base_info['id'],
            account_id=base_info['accountId'],
            name=base_info['name'],
            profile_icon_id=base_info['profileIconId'],
            date_joined_game=base_info['revisionDate'],
            summoner_level=base_info['summonerLevel'])

    for r_info in rank_info:
        txn.run("MERGE (t:Tier {tier: $tier})\
                MERGE (r:Rank {rank: $rank})\
                MERGE (ln:LeagueName {name: $name})\
                MERGE (qt: QueueType {type: $qtype})",
                tier=r_info['tier'],
                rank=r_info['rank'],
                name=r_info['leagueName'],
                qtype=r_info['queueType'])

        txn.run("MATCH (r:Rank), (t:Tier)\
                WHERE t.tier=$tier\
                AND r.rank=$rank\
                MERGE (t)-[:TIER]-(r)",
                tier=r_info['tier'],
                rank=r_info['rank'])

        # txn.run("MATCH (t:Tier), (ln:LeagueName)\
        #         WHERE t.tier=$tier\
        #         AND ln.name=$lname\
        #         MERGE (t)-[:LEAGUENAME]-(ln)",
        #         tier=r_info['tier'],
        #         lname=r_info['leagueName'])


    for c_info in champion_info:
        txn.run("MERGE (ci:ChampionId {cid: $cid})",
                cid=c_info['championId'])


    txn.run("MATCH ()")

# {'playerId': 102738872, 'championId': 62, 'championLevel': 5, 'championPoints': 49811, 'lastPlayTime': 1533485027000, 'championPointsSinceLastLevel': 28211, 'championPointsUntilNextLevel': 0, 'chestGranted': True, 'tokensEarned': 2}
# {'leagueId': 'c9391f90-6477-11e8-b684-c81f66dacb22', 'leagueName': "Swain's Shadows", 'tier': 'GOLD', 'queueType': 'RANKED_SOLO_5x5', 'rank': 'V', 'playerOrTeamId': '102738872', 'playerOrTeamName': 'meow side', 'leaguePoints': 32, 'wins': 249, 'losses': 242, 'veteran': True, 'inactive': False, 'freshBlood': False, 'hotStreak': False}

def create_postcode_summoner_relationship(txn, relationship_info):
    """
    create relationships
    """
    txn.run("MATCH (p:PostCode), (s:Summoner)\
            WHERE p.postcode=$postcode\
            AND s.id=$summoner_id\
            MERGE (p)-[:BELONGS_TO_REGION]-(s)",
            postcode=relationship_info['postcode'],
            summoner_id=relationship_info['summoner_id'])


def use_correct_db_function(what_we_are_doing):
    """
    retrieve the correct function to interact with the neo4j DB
    """
    all_possible_functions = {
        'add_postcode': add_postcode_to_neo4j,
        'add_summoner': add_summoner_to_neo4j,
        'add_base_summoner_info': add_base_summoner_info_neo4j,
        'relationship_postcode_summoner':\
            create_postcode_summoner_relationship
    }

    return all_possible_functions[what_we_are_doing]


async def main_db(what_we_want_to_do, info):
    """
    async call to run neo4j function
    """
    with db.session() as SESSION:
        SESSION.write_transaction(
            use_correct_db_function(what_we_want_to_do),
            info
        )
