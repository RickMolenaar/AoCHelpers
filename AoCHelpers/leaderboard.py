import json
from datetime import datetime, timedelta

from AoCHelpers.communicator import Communicator
from AoCHelpers.functions import EST

def get_leaderboard(year: int, leaderboard_id: str = None) -> dict:
    if DUMMY:
        return json.load(open('dummy_leaderboard.txt'))
    leaderboard_id = leaderboard_id or find_leaderboard_id(year)
    c = Communicator()
    url = f'https://adventofcode.com/{year}/leaderboard/private/view/{leaderboard_id}.json'
    resp = c.request(url)
    try:
        return json.loads(resp.content)
    except json.JSONDecodeError:
        raise ValueError('Could not open this leaderboard')

def get_data_by_name(year: int, name: str, leaderboard_id: str = None) -> dict:
    '''Finds data by name. Performs caseless substring checking, so `rick` will find `Rick Molenaar`'''
    leaderboard_id = leaderboard_id or find_leaderboard_id()
    data = get_leaderboard(leaderboard_id, year)
    for member in data['members'].values():
        if name.lower() in member['name'].lower():
            return member
    raise ValueError(f'{name} could not be found on the leaderboard')

def to_solvetime(timestamp: int, year: int, day: int) -> timedelta:
    return datetime.fromtimestamp(timestamp, EST()) - datetime(year, 12, day, tzinfo=EST())

def get_daily_leaderboard(year: int, day: int, leaderboard_id: str = None):
    leaderboard = get_leaderboard(year, leaderboard_id)
    day = str(day)      # That's what json outputs
    times = {}
    for member in leaderboard['members']:
        data = leaderboard['members'][member]
        member_times = {}
        try:
            day_data = data['completion_day_level'][day]
            member_times[1] = day_data['1']['get_star_ts']
            member_times[2] = day_data['2']['get_star_ts']
        except KeyError:
            pass
        times[data['name']] = member_times
    return times

def print_daily_leaderboard(year, day, leaderboard_id = None):
    times = get_daily_leaderboard(year, day, leaderboard_id)
    max_points = len(times)
    scores = {member: {} for member in times if 1 in times[member]}
    for part in (1, 2):
        solved = [member for member in times if part in times[member]]
        solved = sorted(solved, key=lambda m: times[m][part])
        for i, member in enumerate(solved):
            scores[member][part] = max_points - i
    format = '{:<20}| {:>11} | {:>6} | {:>11} | {:>6} | {:>12} |'
    print('{:<20}| {:<11} | {:<6} | {:<11} | {:<6} | {:>12} |'\
          .format('Name', 'Part 1 time', 'Points', 'Part 2 time', 'Points', 'Total points'))

    data = []
    for member in scores:
        args = [member]
        for part in (1, 2):
            if part in scores[member]:
                args.append(str(to_solvetime(times[member][part], year, day)))
                args.append(scores[member][part])
            else:
                args.extend(('', ''))
        args.append(sum(scores[member].values()))
        data.append(args)
    for line in sorted(data, key = lambda row: row[-1], reverse=True):
        print(format.format(*line))

def find_leaderboard_id(year: int):
    page = Communicator().request(f'https://adventofcode.com/{year}/leaderboard/private')
    page = str(page.content)
    leaderboards = []
    pos = 0
    for _ in range(page.count(f'{year}/leaderboard/private/view/')):
        pos = page.index(f'{year}/leaderboard/private/view/', pos) + 30
        id = page[pos:page.index('"', pos)]
        leaderboards.append(id)
    if len(leaderboards) == 1:
        return leaderboards[0]
    raise ValueError('Could not automatically find leaderboard, supply id')

if __name__=='__main__':
    DUMMY = True
    print_daily_leaderboard(2023, 13)