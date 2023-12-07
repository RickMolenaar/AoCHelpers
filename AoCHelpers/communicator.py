import datetime
import os
from typing import *
import requests

from .tools import Singleton

class Communicator(object, metaclass=Singleton):
    def __init__(self):
        self.recent_calls: List[Tuple[datetime.datetime, str]] = []
        if not os.path.exists('session.cookie'):
            open('session.cookie', 'w').close()
        with open('session.cookie') as f:
            self.cookie = f.readline()
        if not self.cookie:
            print("session.cookie not populated, can't communicate with AoC website")

    def get_input(self, year, day):
        if not self.cookie:
            print("Can't get input without cookie")
            return ''
        url = f'https://adventofcode.com/{year}/day/{day}/input'
        resp = self.request(url)
        return resp.text

    def get_problem(self, year, day):
        url = f'https://adventofcode.com/{year}/day/{day}'
        resp = self.request(url)
        return resp.content

    def submit_answer(self, year, day, part, answer) -> requests.Response:
        if not self.cookie:
            print("Can't submit answer without cookie")
            return
        url = f'https://adventofcode.com/{year}/day/{day}/answer'
        data = {'level': str(part), 'answer': str(answer)}
        resp = self.request(url, 'POST', data)
        content = str(resp.content)
        if 'That\\\'s not the right answer' in content:
            print(f'{answer} is not the right answer')
            if "too low" in content:
                print("Your answer is too low")
            elif "too high" in content:
                print("Your answer is too high")
            return False
        elif 'That\\\'s the right answer' in content:
            print(f'{answer} is correct!')
            if part == 1:
                print('Part 1 is solved, continue with part 2')
            else:
                print(f'Day {day} is solved. Continue optimizing or quit the watcher')
            return True
        else:
            print('Could not parse response:')
            print(content)

    def get_star_stats(self, year):
        pass

    def request(self, url: str, method: str = 'GET', data: dict = {}):
        if method.upper() not in ('GET', 'POST'):
            raise ValueError(f'Unsupported method {method.upper()}')
        now = datetime.datetime.now()
        if len(self.recent_calls) == 3 and all((now - call[0]).seconds < 60 for call in self.recent_calls):
            print(f'Blocking call to {url} for rate limiting purposes')
            return
        self.recent_calls.append((now, url))
        if len(self.recent_calls) > 3:
            self.recent_calls = self.recent_calls[1:]
        cookies = {'session': self.cookie}
        resp = requests.request(method, url, data=data, cookies=cookies)
        
        if resp.status_code == 400:
            print(f'400 error calling {url}. Is your cookie up to date?')
        elif resp.status_code not in (200, 201):
            print(f'Unexpected status code calling {url}: {resp.status_code}')
        return resp

if __name__=='__main__':
    c = Communicator()