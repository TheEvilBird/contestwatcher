import asyncio
import time
from colorama import Fore
import aiohttp
import requests
import json
import datetime


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def get_last():
    a = requests.get('https://codeforces.com/api/contest.list')
    all_codeforces_contests = json.loads(a.text)
    for contest in all_codeforces_contests['result']:
        if contest['phase'] == 'FINISHED':
            return f'<a href="https://codeforces.com/contest/{contest["id"]}">{contest["name"]}</a>'


async def get_rating(handle):
    a = requests.get(f'https://codeforces.com/api/user.info?handles={handle}')
    await asyncio.sleep(0.5)
    result = json.loads(a.text)
    return result['result'][0].get('rating', 0)


async def check_handle(handle):
    a = requests.get(f'https://codeforces.com/api/user.info?handles={handle}')
    result = json.loads(a.text)
    if result['status'] != 'OK':
        return False
    return result['result'][0]['handle']


def get_rating_changes(id):
    a = requests.get(f'https://codeforces.com/api/contest.ratingChanges?contestId={id}')
    result = json.loads(a.text)
    if result['status'] == 'FAILED':
        if result['comment'] == 'contestId: Rating changes are unavailable for this contest':
            return False, False
        return False, True
    elif len(result['result']) == 0:
        return False, True
    else:
        return True, result['result']


async def get_upcoming():
    import bot

    a = await get('https://codeforces.com/api/contest.list')

    all_codeforces_contests = json.loads(a)
    codeforces_contests = []
    times = []
    names = []
    durations = []
    for i in all_codeforces_contests['result']:
        if i['id'] == int(bot.db['last_codeforces']['name'][40:bot.db['last_codeforces']['name'].find('>') - 1]):
            break
        codeforces_contests.append(i)
        times.append(datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=i['startTimeSeconds']))
        names.append(f"<a href=\"https://codeforces.com/contest/{i['id']}\">{i['name']}</a>")
        durations.append(str(i['durationSeconds'] // 60) + ' minutes')

    table = []
    contest_type = 'cf'
    for i in range(len(times)):
        table.append([times[i], names[i], durations[i], contest_type])

    return table


if __name__ == '__main__':
    for i in range(5):
        print(asyncio.run(get('https://codeforces.com/api/contest.list'))[:40])
    time.sleep(0.5)
    print(Fore.BLUE + 'Sleeping')
    print(Fore.LIGHTWHITE_EX, end='')
    for i in range(5):
        print(asyncio.run(get('https://codeforces.com/api/contest.list'))[:40])
