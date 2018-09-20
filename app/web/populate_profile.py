"""
main script to populate initial profile
"""
import asyncio

from database import main_db
from riot import main_riot_api


async def populate_profile(postcode, region, summoner_name):
    """
    async func to populate profile
    """
    await main_db('add_postcode', postcode)
    summoner_content =\
        await main_riot_api(
            'retrieve_summoner_by_name',
            region,
            summoner_name
        )

    await main_db(
        'add_summoner',
        summoner_content['id']
    )

    additional_profile_info =\
        await main_riot_api([
            'account_info_by_summoner_id',
            'champion_mastery_by_summoner_id'],
            region,
            summoner_content['id'])

    await main_db(
        'relationship_postcode_summoner', {
            'postcode': postcode,
            'summoner_id': summoner_content['id']
        })

    await main_db(
        'add_base_summoner_info', {
            'base_profile_info': summoner_content,
            'additional_info': additional_profile_info
        })


loop = asyncio.get_event_loop()
future =\
    asyncio.ensure_future(
        populate_profile(
            'se164ae',
            'euw1',
            'meow side' ))
loop.run_until_complete(future)
