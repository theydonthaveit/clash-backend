"""
Riot API
"""
import aiohttp
import asyncio


def headers():
    """
    headers for riot api reqs
    """
    ORIGIN = ""
    ACCEPT_CHARSET = "application/x-www-form-urlencoded; charset=UTF-8"
    X_RIOT_TOKEN = "RGAPI-76dc27ed-58a1-4cb0-9ab5-e9493afb7929"
    ACCEPT_LANGUAGE = "en-GB,en-US;q=0.9,en;q=0.8"
    USER_AGENT =\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "\
        + "(KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"

    HEADERS = {
        "Origin": ORIGIN,
        "Accept-Charset": ACCEPT_CHARSET,
        "X-Riot-Token": X_RIOT_TOKEN,
        "Accept-Language": ACCEPT_LANGUAGE,
        "User-Agent": USER_AGENT
    }

    return HEADERS


def formulate_url(endpoint, region, query_param):
    """
    formulate url for requests
    """
    BASE_URL = 'https://{}.api.riotgames.com/{}/{}'
    POSSIBLE_ENDPOINTS = {
        'retrieve_summoner_by_name':\
            '/lol/summoner/v3/summoners/by-name',
        'account_info_by_summoner_id':\
            '/lol/league/v3/positions/by-summoner',
        'champion_mastery_by_summoner_id':\
            '/lol/champion-mastery/v3/'\
            + 'champion-masteries/by-summoner'
    }

    return BASE_URL.format(
        region,
        POSSIBLE_ENDPOINTS[endpoint],
        query_param )


async def fetch(session, url):
    """
    async func to fetch json based on url
    """
    async with session.get(url) as RESPONSE:
        return await RESPONSE.json()


async def main_riot_api(what_we_want_to_do, region, query_param):
    """
    main async func to init fetch of json data from url
    """
    tasks = []
    res = ''
    async with aiohttp.ClientSession(headers=headers()) as SESSION:
        if isinstance(what_we_want_to_do, list):
            for want_to_do in what_we_want_to_do:
                url = formulate_url(want_to_do, region, query_param)
                task =\
                    asyncio.ensure_future(
                        fetch(
                            SESSION,
                            url ))
                tasks.append(task)
            res = await asyncio.gather(*tasks)
        else:
            url = formulate_url(what_we_want_to_do, region, query_param)
            res = await fetch(SESSION, url)

    return res
