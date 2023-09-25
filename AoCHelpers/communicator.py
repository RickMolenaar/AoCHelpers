import datetime
from typing import *
import pathlib

from .tools import Singleton

class Communicator(object, metaclass=Singleton):
    def __init__(self):
        self.recent_calls: List[Tuple[datetime.datetime, str]] = []
        with open('session.cookie') as f:
            self.cookie = f.readline()

    def get_input(self, day, year):
        pass

    def submit_answer(self, day, year, answer):
        pass

    def get_star_stats(self, year):
        pass

    def request(self, url):
        now = datetime.datetime.now()
        if len(self.recent_calls) == 3 and all((now - call[0]).seconds < 60 for call in self.recent_calls):
            print(f'Blocking call to {url} for rate limiting purposes')
            return
        self.recent_calls.append((now, url))
        if len(self.recent_calls) > 3:
            self.recent_calls = self.recent_calls[1:]

if __name__=='__main__':
    c = Communicator()