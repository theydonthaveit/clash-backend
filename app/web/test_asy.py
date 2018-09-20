"""
Riot API
"""
import aiohttp
import asyncio
from database import access_correct_function_to_engage_with_db

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

REGION = 'euw1'
BASE_URL = 'https://{}.api.riotgames.com/{}/{}'
RETRIEVE_SUMMONER_BY_NAME = '/lol/summoner/v3/summoners/by-name'
ACCOUNT_INFO_BY_SUMMONER_ID = '/lol/league/v3/positions/by-summoner'
CHAMPION_MASTERY_BY_SUMMONER_ID =\
    '/lol/champion-mastery/v3/'\
    + 'champion-masteries/by-summoner'

RETRIEVE_BASE_PROFILE_URL =\
    BASE_URL.format(REGION, RETRIEVE_SUMMONER_BY_NAME, 'meow side')
ACCOUNT_RANK_INFO_DETAILS_URL =\
    BASE_URL.format(REGION, ACCOUNT_INFO_BY_SUMMONER_ID, '102738872')
CHAMPION_MASTERY_DETAILS_URL =\
    BASE_URL.format(REGION, CHAMPION_MASTERY_BY_SUMMONER_ID, '102738872')


async def fetch(session, url):
    async with session.get(url) as RESPONSE:
        return await RESPONSE.json()


async def main():
    tasks = []
    res = ''
    async with aiohttp.ClientSession(headers=HEADERS) as SESSION:
        res = await fetch(SESSION, RETRIEVE_BASE_PROFILE_URL)
        print(res)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
